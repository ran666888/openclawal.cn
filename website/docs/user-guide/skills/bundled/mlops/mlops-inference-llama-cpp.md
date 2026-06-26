---
title: "Llama Cpp — llama"
sidebar_label: "Llama Cpp"
description: "llama"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 骆驼 Cpp

llama.cpp 本地 GGUF 推理 + HF Hub 模型发现。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/mlops/推理/llama-cpp` |
|版本 | `2.1.2` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `llama-cpp-python>=0.2.0` |
|平台| linux、macos、windows |
|标签 | `llama.cpp`、`GGUF`、`量化`、`Huging Face Hub`、`CPU 推理`、`Apple Silicon`、`边缘部署`、`AMD GPU`、`Intel GPU`、`NVIDIA`、`URL 优先` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# llama.cpp + GGUF

使用此技能对 llama.cpp 进行本地 GGUF 推理、定量选择或 Hugging Face 存储库发现。

## 何时使用

- 在 CPU、Apple Silicon、CUDA、ROCm 或 Intel GPU 上运行本地模型
- 为特定的 Hugging Face 存储库找到合适的 GGUF
- 从集线器构建“llama-server”或“llama-cli”命令
- 在 Hub 中搜索已支持 llama.cpp 的模型
- 枚举存储库可用的“.gguf”文件和大小
- 为用户的 RAM 或 VRAM 选择 Q4/Q5/Q6/IQ 变体

## 模型发现工作流程

在请求“hf”、Python 或自定义脚本之前，优先选择 URL 工作流程。

1. 在 Hub 上搜索候选存储库：
   - 基础：`https://huggingface.co/models?apps=llama.cpp&sort=trending`
   - 为模型系列添加“search=<term>”
   - 当用户有大小限制时添加 `num_parameters=min:0,max:24B` 或类似内容
2. 使用 llama.cpp local-app 视图打开存储库：
   - `https://huggingface.co/<repo>?local-app=llama.cpp`
3. 当本地应用程序片段可见时，将其视为事实来源：
   - 复制确切的“llama-server”或“llama-cli”命令
   - 完全按照 HF 显示的方式报告推荐的数量
4. 读取相同的“?local-app=llama.cpp” URL 作为页面文本或 HTML，并提取“硬件兼容性”下的部分：
   - 与通用表格相比，更喜欢其精确的定量标签和尺寸
   - 保留特定于存储库的标签，例如“UD-Q4_K_M”或“IQ4_NL_XL”
   - 如果该部分在获取的页面源代码中不可见，请说明并回退到树 API 以及通用量化指导
5. 查询树 API 以确认实际存在的内容：
   - `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`
   - 保留“type”为“file”且“path”以“.gguf”结尾的条目
   - 使用“path”和“size”作为文件名和字节大小的真实来源
   - 将量化检查点与“mmproj-*.gguf”投影仪文件和“BF16/”分片文件分开
   - 仅使用“https://huggingface.co/<repo>/tree/main”作为人类后备
6. 如果本地应用程序片段不是文本可见的，请从存储库加上所选的量重建命令：
   - 简写量化选择：`llama-server -hf <repo>:<QUANT>`
   - 精确文件后备：`llama-server --hf-repo <repo> --hf-file <filename.gguf>`
7. 如果存储库尚未公开 GGUF 文件，则仅建议从 Transformers 权重进行转换。

## 快速开始

### 安装llama.cpp

````bash
# macOS / Linux（最简单）
酿造安装骆驼.cpp
````

````bash
winget安装llama.cpp
````

````bash
git 克隆 https://github.com/ggml-org/llama.cpp
cd 骆驼.cpp
cmake -B 构建
cmake --build 构建 --config 发布
````

### 直接从 Hugging Face Hub 运行

````bash
llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
````

````bash
llama-服务器-hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
````

### 从 Hub 运行精确的 GGUF 文件

当树 API 显示自定义文件命名或缺少确切的 HF 片段时，请使用此选项。

````bash
骆驼服务器 \
    --hf-repo 微软/Phi-3-mini-4k-instruct-gguf \
    --hf-文件 Phi-3-mini-4k-instruct-q4.gguf \
    -c 4096
````

### OpenAI 兼容服务器检查

````bash
卷曲 http://localhost:8080/v1/chat/completions \
  -H“内容类型：application/json”\
  -d'{
    “消息”：[
      {"role": "user", "content": "写一首关于 Python 异常的打油诗"}
    ]
  }'
````

## Python 绑定 (llama-cpp-python)

`pip install llama-cpp-python` （CUDA：`CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir`；金属：`CMAKE_ARGS="-DGGML_METAL=on" ...`）。

### 基本生成

````蟒蛇
从 llama_cpp 导入 Llama

llm = 骆驼(
    model_path =“./model-q4_k_m.gguf”，
    n_ctx=4096,
    n_gpu_layers=35, # 0 用于 CPU，99 用于卸载所有内容
    n_线程=8，
）

out = llm("什么是机器学习？"，max_tokens=256，温度=0.7)
打印（输出[“选择”][0][“文本”]）
````

### 聊天+直播

````蟒蛇
llm = 骆驼(
    model_path =“./model-q4_k_m.gguf”，
    n_ctx=4096,
    n_gpu_layers=35,
    chat_format="llama-3", # 或 "chatml", "mistral" 等
）

resp = llm.create_chat_completion(
    消息=[
        {"role": "system", "content": "你是一个得力助手。"},
        {"role": "user", "content": "什么是Python？"},
    ],
    最大令牌=256，
）
print(resp["选择"][0]["消息"]["内容"])

# 流媒体
for chunk in llm(“解释量子计算：”，max_tokens=256，stream=True)：
    打印（块[“选择”] [0] [“文本”]，结束=“”，刷新= True）
````

### 嵌入

````蟒蛇
llm = 骆驼（model_path =“./model-q4_k_m.gguf”，嵌入= True，n_gpu_layers = 35）
vec = llm.embed("这是一个测试句子。")
print(f"嵌入维度：{len(vec)}")
````

您还可以直接从 Hub 加载 GGUF：

````蟒蛇
llm = Llama.from_pretrained(
    repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
    文件名=“*Q4_K_M.gguf”，
    n_gpu_layers=35,
）
````

## 选择量化

首先使用中心页面，然后使用通用启发法。

- 首选 HF 标记为与用户的硬件配置文件兼容的确切数量。
- 对于一般聊天，从“Q4_K_M”开始。
- 对于代码或技术工作，如果内存允许，首选“Q5_K_M”或“Q6_K”。
- 对于非常紧张的 RAM 预算，仅当用户明确优先考虑适合度而非质量时，才考虑“Q3_K_M”、“IQ”变体或“Q2”变体。
- 对于多模式存储库，请单独提及“mmproj-*.gguf”。投影仪不是主模型文件。
- 不要标准化 repo-native 标签。如果页面显示“UD-Q4_K_M”，请报告“UD-Q4_K_M”。

## 从存储库中提取可用的 GGUF

当用户询问存在哪些 GGUF 时，返回：

- 文件名
- 文件大小
- 定量标签
- 无论是主机型还是辅助投影机

除非有要求，否则忽略：

- README文件
- BF16 分片文件
- 矩阵斑点或校准伪影

使用树 API 执行此步骤：

- `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`

对于像“unsloth/Qwen3.6-35B-A3B-GGUF”这样的存储库，本地应用程序页面可以显示“UD-Q4_K_M”、“UD-Q5_K_M”、“UD-Q6_K”和“Q8_0”等量化芯片，而树 API 则公开准确的文件路径，例如具有字节大小的“Qwen3.6-35B-A3B-UD-Q4_K_M.gguf”和“Qwen3.6-35B-A3B-Q8_0.gguf”。使用树 API 将定量标签转换为精确的文件名。

## 搜索模式

直接使用这些 URL 形状：

````文本
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending
https://huggingface.co/<repo>?local-app=llama.cpp
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
https://huggingface.co/<repo>/tree/main
````

## 输出格式

在回答发现请求时，更喜欢紧凑的结构化结果，例如：

````文本
回购：<回购>
HF 推荐定量：<标签> (<尺寸>)
骆驼服务器：<命令>
其他 GGUF：
- <文件名> - <大小>
- <文件名> - <大小>
来源网址：
- <本地应用程序 URL>
- <树API URL>
````

## 参考文献

- **[hub-discovery.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/llama-cpp/references/hub-discovery.md)** - 仅 URL 拥抱人脸工作流程、搜索模式、GGUF 提取和命令重建
- **[advanced-usage.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/llama-cpp/references/advanced-usage.md)** — 推测解码、批量推理、语法约束生成、LoRA、多 GPU、自定义构建、基准测试脚本
- **[quantization.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/llama-cpp/references/quantization.md)** — 定量质量权衡、何时使用 Q4/Q5/Q6/IQ、模型大小缩放、imatrix
- **[server.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/llama-cpp/references/server.md)** — 直接从 Hub 服务器启动、OpenAI API 端点、Docker 部署、NGINX 负载平衡、监控
- **[optimization.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/llama-cpp/references/optimization.md)** — CPU 线程、BLAS、GPU 卸载启发式、批量调整、基准测试
- **[troubleshooting.md](https://github.com/NousResearch/openclaw/blob/main/skills/mlops/inference/llama-cpp/references/troubleshooting.md)** — 安装/转换/量化/推理/服务器问题，Apple Silicon，调试

## 资源

- **GitHub**：https://github.com/ggml-org/llama.cpp
- **拥抱脸 GGUF + llama.cpp 文档**：https://huggingface.co/docs/hub/gguf-llamacpp
- **Hugging Face 本地应用程序文档**：https://huggingface.co/docs/hub/main/local-apps
- **Hugging Face 本地代理文档**：https://huggingface.co/docs/hub/agents-local
- **本地应用程序页面示例**：https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF?local-app=llama.cpp
- **示例树 API**：https://huggingface.co/api/models/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main?recursive=true
- **示例 llama.cpp 搜索**：https://huggingface.co/models?num_parameters=min:0,max:24B&apps=llama.cpp&sort=trending
- **许可证**：麻省理工学院