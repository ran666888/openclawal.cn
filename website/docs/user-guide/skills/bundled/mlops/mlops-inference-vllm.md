---
title: "Serving Llms Vllm — vLLM: high-throughput LLM serving, OpenAI API, quantization"
sidebar_label: "Serving Llms Vllm"
description: "vLLM: high-throughput LLM serving, OpenAI API, quantization"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 服务法学硕士 Vllm

vLLM：高吞吐量 LLM 服务、OpenAI API、量化。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/mlops/推理/vllm` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `vllm`、`火炬`、`变形金刚` |
|平台| linux, macOS |
|标签 | `vLLM`、`推理服务`、`PagedAttention`、`连续批处理`、`高吞吐量`、`生产`、`OpenAI API`、`量化`、`张量并行` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# vLLM - 高性能 LLM 服务

## 何时使用

在部署生产 LLM API、优化推理延迟/吞吐量或为 GPU 内存有限的模型提供服务时使用。支持 OpenAI 兼容端点、量化 (GPTQ/AWQ/FP8) 和张量并行性。

## 快速开始

vLLM 通过 PagedAttention（基于块的 KV 缓存）和连续批处理（混合预填充/解码请求）实现了比标准转换器高 24 倍的吞吐量。

**安装**：
````bash
pip 安装 vllm
````

**基本离线推理**：
````蟒蛇
从 vllm 导入 LLM，SamplingParams

llm = LLM(模型=“meta-llama/Llama-3-8B-Instruct”)
采样 = SamplingParams(温度=0.7, max_tokens=256)

输出 = llm.generate(["解释量子计算"], 采样)
打印（输出[0].输出[0].文本）
````

**OpenAI 兼容服务器**：
````bash
vllm 服务meta-llama/Llama-3-8B-Instruct

# 使用OpenAI SDK查询
蟒蛇-c“
从 openai 导入 OpenAI
客户端 = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')
打印(client.chat.completions.create(
    model='meta-llama/Llama-3-8B-Instruct',
    messages=[{'角色': '用户', '内容': '你好！'}]
).choices[0].message.content)
”
````

## 常用工作流程

### 工作流程 1：生产 API 部署

复制此清单并跟踪进度：

````
部署进度：
- [ ] 步骤 1：配置服务器设置
- [ ] 步骤 2：使用有限流量进行测试
- [ ] 步骤 3：启用监控
- [ ] 步骤 4：部署到生产环境
- [ ] 步骤 5：验证性能指标
````

**第 1 步：配置服务器设置**

根据您的型号尺寸选择配置：

````bash
# 适用于单 GPU 上的 7B-13B 型号
vllm 服务 meta-llama/Llama-3-8B-Instruct \
  --GPU内存利用率0.9 \
  --最大模型长度 8192 \
  --端口8000

# 对于具有张量并行性的 30B-70B 模型
vllm 服务meta-llama/Llama-2-70b-hf \
  --张量平行大小 4 \
  --GPU内存利用率0.9 \
  --量化 awq \
  --端口8000

# 用于具有缓存和指标的生产
vllm 服务 meta-llama/Llama-3-8B-Instruct \
  --GPU内存利用率0.9 \
  --启用前缀缓存 \
  --启用指标 \
  --metrics-端口 9090 \
  --端口8000 \
  --主机0.0.0.0
````

**第 2 步：使用有限流量进行测试**

生产前运行负载测试：

````bash
# 安装负载测试工具
pip安装蝗虫

# 使用示例请求创建 test_load.py
# 运行：locust -f test_load.py --host http://localhost:8000
````

验证 TTFT（第一个令牌的时间）< 500 毫秒且吞吐量 > 100 请求/秒。

**第 3 步：启用监控**

vLLM 在端口 9090 上公开 Prometheus 指标：

````bash
卷曲 http://localhost:9090/metrics | grep vllm
````

要监控的关键指标：
- `vllm:time_to_first_token_seconds` - 延迟
- `vllm:num_requests_running` - 活动请求
- `vllm:gpu_cache_usage_perc` - KV 缓存利用率

**第 4 步：部署到生产环境**

使用 Docker 进行一致部署：

````bash
# 在 Docker 中运行 vLLM
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:最新\
  --model meta-llama/Llama-3-8B-Instruct \
  --GPU内存利用率0.9 \
  --启用前缀缓存
````

**第 5 步：验证性能指标**

检查部署是否满足目标：
- TTFT < 500ms（用于简短提示）
- 吞吐量 > 目标请求/秒
- GPU 利用率 > 80%
- 日志中没有 OOM 错误

### 工作流程2：离线批量推理

用于处理大型数据集而无需服务器开销。

复制此清单：

````
批处理：
- [ ] 步骤 1：准备输入数据
- [ ] 步骤2：配置LLM引擎
- [ ] 步骤 3：运行批量推理
- [ ] 步骤 4：处理结果
````

**第 1 步：准备输入数据**

````蟒蛇
# 从文件加载提示
提示=[]
以 open("prompts.txt") 作为 f：
    提示= [line.strip() for line in f]

print(f"已加载 {len(prompts)} 提示")
````

**第2步：配置LLM引擎**

````蟒蛇
从 vllm 导入 LLM，SamplingParams

法学硕士 = 法学硕士(
    模型=“meta-llama/Llama-3-8B-Instruct”，
    tensor_parallel_size=2, # 使用2个GPU
    GPU_内存_利用率=0.9，
    最大模型长度=4096
）

采样=采样参数(
    温度=0.7，
    顶部_p=0.95，
    最大令牌=512，
    停止=["</s>", "\n\n"]
）
````

**第 3 步：运行批量推理**

vLLM 自动批量请求以提高效率：

````蟒蛇
# 在一次调用中处理所有提示
输出= llm.generate（提示，采样）

# vLLM 在内部处理批处理
# 无需手动分块提示
````

**第 4 步：处理结果**

````蟒蛇
# 提取生成的文本
结果=[]
对于输出中的输出：
    提示=输出.提示
    生成 = 输出.输出[0].文本
    结果.追加({
        “提示”：提示，
        “生成”：生成，
        “令牌”：len(output.outputs[0].token_ids)
    })

# 保存到文件
导入 json
将 open("results.jsonl", "w") 作为 f：
    对于结果中的结果：
        f.write(json.dumps(结果) + "\n")

print(f"已处理 {len(results)} 提示")
````

### 工作流程 3：量化模型服务

在有限的 GPU 内存中安装大型模型。

````
量化设置：
- [ ] 第 1 步：选择量化方法
- [ ] 步骤 2：查找或创建量化模型
- [ ] 步骤 3：使用量化标志启动
- [ ] 步骤 4：验证准确性
````

**第1步：选择量化方法**

- **AWQ**：最适合 70B 型号，精度损失最小
- **GPTQ**：广泛的模型支持，良好的压缩
- **FP8**：H100 GPU 上最快

**第 2 步：查找或创建量化模型**

使用 HuggingFace 中的预量化模型：

````bash
# 搜索 AWQ 型号
# 示例：TheBloke/Llama-2-70B-AWQ
````

**第 3 步：使用量化标志启动**

````bash
# 使用预量化模型
vllm 服务 TheBloke/Llama-2-70B-AWQ \
  --量化 awq \
  --张量平行大小 1 \
  --GPU内存利用率0.95

# 结果：约 40GB VRAM 中的 70B 型号
````

**第 4 步：验证准确性**

测试输出符合预期质量：

````蟒蛇
# 比较量化与非量化响应
# 验证特定于任务的性能是否不变
````

## 何时使用与替代方案

**在以下情况下使用 vLLM：**
- 部署生产 LLM API（100+ 请求/秒）
- 服务 OpenAI 兼容端点
- GPU 内存有限但需要大型模型
- 多用户应用程序（聊天机器人、助手）
- 需要低延迟和高吞吐量

**使用替代方案：**
- **llama.cpp**：CPU/边缘推理，单用户
- **HuggingFace 变形金刚**：研究、原型设计、一次性生成
- **TensorRT-LLM**：仅限 NVIDIA，需要绝对最大性能
- **文本生成-推理**：已经在 HuggingFace 生态系统中

## 常见问题

**问题：模型加载期间内存不足**

减少内存使用：
````bash
vllm服务模型\
  --GPU内存利用率0.7 \
  --最大模型长度 4096
````

或者使用量化：
````bash
vllm 服务模型——量化 awq
````

**问题：第一个令牌速度慢（TTFT > 1 秒）**

为重复提示启用前缀缓存：
````bash
vllm 服务模型 --enable-prefix-caching
````

对于长提示，启用分块预填充：
````bash
vllm 服务模型 --enable-chunked-prefill
````

**问题：找不到模型错误**

对自定义模型使用 `--trust-remote-code`：
````bash
vllm 服务模型 --trust-remote-code
````

**问题：吞吐量低（<50 请求/秒）**

增加并发序列：
````bash
vllm 服务模型 --max-num-seqs 512
````

使用“nvidia-smi”检查 GPU 利用率 - 应 >80%。

**问题：推理速度比预期慢**

验证张量并行性使用 2 个 GPU 的能力：
````bash
vllm 服务模型 --tensor-parallel-size 4 # 不是 3
````

启用推测解码以加快生成速度：
````bash
vllm 服务 MODEL --推测模型 DRAFT_MODEL
````

## 高级主题

**服务器部署模式**：有关 Docker、Kubernetes 和负载均衡配置，请参阅 [references/server-deployment.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/vllm/references/server-deployment.md)。

**性能优化**：请参阅 [references/optimization.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/vllm/references/optimization.md) 了解 PagedAttention 调整、连续批处理详细信息和基准测试结果。

**量化指南**：请参阅 [references/quantization.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/vllm/references/quantization.md) 了解 AWQ/GPTQ/FP8 设置、模型准备和精度比较。

**故障排除**：有关详细的错误消息、调试步骤和性能诊断，请参阅 [references/troubleshooting.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/vllm/references/troubleshooting.md)。

## 硬件要求

- **小型型号 (7B-13B)**：1x A10 (24GB) 或 A100 (40GB)
- **中型型号 (30B-40B)**：2x A100 (40GB)，具有张量并行性
- **大型型号 (70B+)**：4x A100 (40GB) 或 2x A100 (80GB)，使用 AWQ/GPTQ

支持的平台：NVIDIA（主要）、AMD ROCm、Intel GPU、TPU

## 资源

- 官方文档：https://docs.vllm.ai
- GitHub：https://github.com/vllm-project/vllm
- 论文：“利用 PagedAttention 实现大型语言模型的高效内存管理”（SOSP 2023）
- 社区：https://discuss.vllm.ai