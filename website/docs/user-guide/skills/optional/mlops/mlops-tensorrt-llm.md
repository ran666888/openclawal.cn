---
title: "Tensorrt Llm — Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency"
sidebar_label: "Tensorrt Llm"
description: "Optimizes LLM inference with NVIDIA TensorRT for maximum throughput and lowest latency"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# TensorRT-LLM

使用 NVIDIA TensorRT 优化 LLM 推理，以实现最大吞吐量和最低延迟。当您需要比 PyTorch 快 10-100 倍的推理速度时，可用于 NVIDIA GPU (A100/H100) 上的生产部署，或者用于通过量化 (FP8/INT4)、动态批处理和多 GPU 扩展来服务模型。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/tensorrt-llm` 安装 |
|路径| `可选技能/mlops/tensorrt-llm` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `tensorrt-llm`、`torch` |
|平台| linux, macOS |
|标签 | “推理服务”、“TensorRT-LLM”、“NVIDIA”、“推理优化”、“高吞吐量”、“低延迟”、“生产”、“FP8”、“INT4”、“飞行批处理”、“多 GPU” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# TensorRT-法学硕士

NVIDIA 的开源库，用于在 NVIDIA GPU 上提供最先进的性能来优化 LLM 推理。

## 何时使用 TensorRT-LLM

**在以下情况下使用 TensorRT-LLM：**
- 在 NVIDIA GPU（A100、H100、GB200）上部署
- 需要最大吞吐量（Llama 3 上每秒超过 24,000 个令牌）
- 实时应用需要低延迟
- 使用量化模型（FP8、INT4、FP4）
- 跨多个 GPU 或节点扩展

**在以下情况下使用 vLLM：**
- 需要更简单的设置和 Python-first API
- 想要没有 TensorRT 编译的 PagedAttention
- 使用 AMD GPU 或非 NVIDIA 硬件

**在以下情况下使用 llama.cpp 代替：**
- 在 CPU 或 Apple Silicon 上部署
- 需要在没有 NVIDIA GPU 的情况下进行边缘部署
- 想要更简单的 GGUF 量化格式

## 快速开始

### 安装

````bash
# Docker（推荐）
docker pull nvidia/tensorrt_llm：最新

# 点安装
pip 安装tensorrt_llm==1.2.0rc3

# 需要 CUDA 13.0.0、TensorRT 10.13.2、Python 3.10-3.12
````

### 基本推理

````蟒蛇
从tensorrt_llm导入LLM，SamplingParams

# 初始化模型
llm = LLM(模型=“meta-llama/Meta-Llama-3-8B”)

# 配置采样
采样参数 = 采样参数（
    最大令牌数=100,
    温度=0.7，
    顶部_p=0.9
）

# 生成
提示= [“解释量子计算”]
输出= llm.generate(提示，sampling_params)

对于输出中的输出：
    打印（输出.文本）
````

### 使用 trtllm-serve 提供服务

````bash
# 启动服务器（自动模型下载和编译）
trtllm-服务meta-llama/Meta-Llama-3-8B \
    --tp_size 4 \ # 张量并行度（4 个 GPU）
    --max_batch_size 256 \
    --max_num_tokens 4096

# 客户端请求
卷曲 -X POST http://localhost:8000/v1/chat/completions \
  -H“内容类型：application/json”\
  -d'{
    “型号”：“元骆驼/元骆驼-3-8B”，
    "messages": [{"role": "user", "content": "Hello!"}],
    “温度”：0.7，
    “最大令牌”：100
  }'
````

## 主要特点

### 性能优化
- **飞行中批处理**：生成期间动态批处理
- **分页KV缓存**：高效的内存管理
- **Flash Attention**：优化的注意力内核
- **量化**：FP8、INT4、FP4 可将推理速度提高 2-4 倍
- **CUDA 图表**：减少内核启动开销

### 并行性
- **张量并行性 (TP)**：跨 GPU 分割模型
- **管道并行性（PP）**：逐层分布
- **专家并行性**：对于专家混合模型
- **多节点**：超越单机规模

### 高级功能
- **推测性解码**：草稿模型的生成速度更快
- **LoRA 服务**：高效的多适配器部署
- **分类服务**：单独的预填充和生成

## 常见模式

### 量化模型（FP8）

````蟒蛇
从tensorrt_llm导入LLM

# 加载 FP8 量化模型（速度提高 2 倍，内存减少 50%）
法学硕士 = 法学硕士(
    型号=“meta-llama/Meta-Llama-3-70B”，
    dtype =“fp8”，
    最大数量令牌=8192
）

# 推论与之前相同
输出 = llm.generate(["总结这篇文章..."])
````

### 多 GPU 部署

````蟒蛇
# 8 个 GPU 上的张量并行度
法学硕士 = 法学硕士(
    型号=“meta-llama/Meta-Llama-3-405B”，
    张量并行大小=8，
    dtype=“fp8”
）
````

### 批量推理

````蟒蛇
# 高效处理 100 个提示
提示 = [f"问题 {i}: ..." for i in range(100)]

输出= llm.生成（
    提示，
    采样参数=采样参数(max_tokens=200)
）

# 自动飞行中批处理以实现最大吞吐量
````

## 性能基准

**Meta Llama 3-8B**（H100 GPU）：
- 吞吐量：24,000 个令牌/秒
- 延迟：每个令牌约 10 毫秒
- 与 PyTorch 相比：**快 100 倍**

**骆驼 3-70B** (8× A100 80GB):
- FP8 量化：比 FP16 快 2 倍
- 内存：FP8 减少 50%

## 支持的型号

- **LLaMA 家族**：Llama 2、Llama 3、CodeLlama
- **GPT 系列**：GPT-2、GPT-J、GPT-NeoX
- **Qwen**：Qwen、Qwen2、QwQ
- **DeepSeek**：DeepSeek-V2、DeepSeek-V3
- **Mixtral**：Mixtral-8x7B、Mixtral-8x22B
- **视觉**：LLaVA、Phi-3-vision
- **HuggingFace 上有 100 多个模型**

## 参考文献

- **[优化指南](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/tensorrt-llm/references/optimization.md)** - 量化、批处理、KV 缓存调整
- **[多 GPU 设置](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/tensorrt-llm/references/multi-gpu.md)** - 张量/管道并行，多节点
- **[服务指南](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/tensorrt-llm/references/serving.md)** - 生产部署、监控、自动扩展

## 资源

- **文档**：https://nvidia.github.io/TensorRT-LLM/
- **GitHub**：https://github.com/NVIDIA/TensorRT-LLM
- **模型**：https://huggingface.co/models?library=tensorrt_llm