---
sidebar_position: 9
title: "Run OpenClaw Locally with Ollama — Zero API Cost"
description: "Step-by-step guide to running OpenClaw entirely on your own machine with Ollama and open-weight models like Gemma 4, no cloud API keys or paid subscriptions needed"
---
# 使用 Ollama 在本地运行 OpenClaw — 零 API 成本

## 问题

Cloud LLM API 按令牌收费。一次繁重的编码工作可能要花费 5-20 美元。对于个人项目、学习或隐私敏感的工作，这会增加 - 并且您将每个对话发送给第三方。

## 本指南解决的问题

您将使用 [Ollama](https://ollama.com) 作为模型后端，设置完全在您自己的硬件上运行的 OpenClaw。没有API密钥，没有订阅，没有数据离开您的机器。配置完成后，OpenClaw 的工作方式与 OpenRouter 或 Anthropic 的工作方式完全相同——终端命令、文件编辑、网页浏览、委托——但模型在本地运行。

到最后，您将拥有：

- Ollama 为一个或多个开放重量模型提供服务
- OpenClaw 作为自定义端点连接到 Ollama
- 可以编辑文件、运行命令和浏览网页的工作本地代理
- 可选：完全由您自己的硬件驱动的 Telegram/Discord 机器人

## 你需要什么

|组件|最低 |推荐|
|------------|---------|-------------|
| **内存** | 8 GB（适用于 3B 型号）| 32+ GB（适用于 27B+ 型号）|
| **存储** | 5 GB 免费 | 30+ GB（适用于多个型号）|
| **CPU** | 4 核 | 8 个以上核心（AMD EPYC、Ryzen、Intel Xeon）|
| **GPU** |不需要 |配备 8+ GB VRAM 的 NVIDIA GPU 显着加快速度 |

:::tip 仅 CPU 有效，但预计响应速度较慢
Ollama 在仅使用 CPU 的服务器上运行。现代 8 核 CPU 上的 9B 模型每秒提供约 10 个令牌。 CPU 上的 31B 模型速度较慢（约 2-5 个令牌/秒）——每个响应需要 30-120 秒，但它可以工作。 GPU 极大地改善了这一点。对于仅限 CPU 的设置，通过环境变量扩大 API 超时（它不是 `config.yaml` 键）：

````bash
# ~/.hermes/.env
HERMES_API_TIMEOUT=1800 # 30 分钟 — 对于缓慢的本地模型来说很慷慨
````
:::

## 步骤 1：安装 Ollama

````bash
卷曲-fsSL https://ollama.com/install.sh |嘘
````

验证它正在运行：

````bash
乌拉马——版本
curl http://localhost:11434/api/tags # 应返回 {"models":[]}
````

## 第 2 步：拉取模型

根据您的硬件选择：

|型号|磁盘大小 |需要内存 |工具调用|最适合 |
|--------|-------------|------------|:------------:|------------|
| `gemma4:31b` | 〜20 GB | 24+ GB |是的 |最佳品质——强大的工具使用和推理|
| `gemma2:27b` | 〜16 GB | 20+ GB |没有 |对话任务，无需使用工具 |
| `gemma2:9b` | 〜5 GB | 8+ GB |没有 |快速聊天、问答——无法调用工具 |
| `llama3.2:3b` | 〜2 GB | 4+ GB |没有 |仅轻量级快速解答 |

:::警告 工具调用很重要
OpenClaw 是一个**代理**助手——它编辑文件、运行命令并通过工具调用浏览网页。不支持工具调用的模型只能聊天；他们无法采取行动。为了获得完整的 OpenClaw 体验，请使用支持工具的模型（例如 `gemma4:31b`）。
:::

拉出您选择的模型：

````bash
奥拉马拉杰玛4:31b
````

:::info 多种型号
您可以使用“/model”拉取多个模型并在 OpenClaw 内部进行切换。 Ollama 按需将活动模型加载到内存中，并自动卸载空闲模型。
:::

验证模型是否有效：

````bash
卷曲 http://localhost:11434/v1/chat/completions \
  -H“内容类型：application/json”\
  -d'{
    “模型”：“gemma4：31b”，
    "messages": [{"role": "user", "content": "打个招呼"}],
    “最大令牌”：50
  }'
````

您应该会看到带有模型回复的 JSON 响应。

## 第三步：配置 OpenClaw

运行 OpenClaw 设置向导：

````bash
爱马仕设置
````

当提示输入提供程序时，选择 **自定义端点** 并输入：

- **基本 URL：** `http://localhost:11434/v1`
- **API 密钥：** 留空或输入“无密钥”（Ollama 不需要）
- **型号：** `gemma4:31b` （或您拉动的任何型号）

或者，直接编辑 `~/.hermes/config.yaml`：

````yaml
型号：
  默认值：“gemma4:31b”
  提供商：“自定义”
  base_url：“http://localhost:11434/v1”
````

## 第 4 步：开始使用 OpenClaw

````bash
爱马仕
````

就是这样。您现在正在运行一个完全本地化的代理。尝试一下：

````
你：列出该目录下的所有Python文件，并统计每个文件中的代码行数

你：阅读 README.md 并总结这个项目的作用

您：创建一个 Python 脚本来获取胡志明市的天气
````

OpenClaw 将使用终端工具、文件操作和本地模型——无需云调用。

## 步骤 5：为您的任务选择正确的模型

并非每个任务都需要最大的模型。这是实用指南：

|任务|推荐型号 |为什么 |
|------|--------------------|-----|
|文件编辑、代码、终端命令 | `gemma4:31b` |唯一具有可靠工具调用的模型 |
|快速问答（无需使用工具）| `gemma2:9b` |对话任务的快速响应 |
|轻量级聊天 | `llama3.2:3b` |最快，但功能非常有限 |

:::注意
对于完整的代理工作（编辑文件、运行命令、浏览），“gemma4:31b”是目前具有工具调用支持的最佳本地选项。检查 [Ollama 的模型库](https://ollama.com/library) 以获得更新的模型 - 工具调用支持正在迅速扩展。
:::

在会话中动态切换模型：

````
/模型 gemma2:9b
````

## 步骤 6：优化速度

### 增加 Ollama 的上下文窗口

默认情况下，Ollama 使用 2048 个令牌上下文。 OpenClaw 需要至少 64,000 个代币才能使用工具进行代理工作：

````bash
# 创建一个扩展上下文的模型文件
猫 > /tmp/Modelfile << 'EOF'
来自 gemma4:31b
参数 num_ctx 64000
EOF

ollama 创建 gemma4-64k -f /tmp/Modelfile
````

然后更新您的 OpenClaw 配置以使用“gemma4-64k”作为模型名称。

### 保持模型加载

默认情况下，Ollama 在 5 分钟不活动后卸载模型。对于持久网关机器人，请保持其加载：

````bash
# 设置保持活动时间为24小时
卷曲 http://localhost:11434/api/generate \
  -d '{"model": "gemma4:31b", "keep_alive": "24h"}'
````

或者在 Ollama 的环境中进行全局设置：

````bash
# /etc/systemd/system/ollama.service.d/override.conf
[服务]
环境=“OLLAMA_KEEP_ALIVE=24小时”
````

### 使用 GPU 卸载（如果可用）

如果您有 NVIDIA GPU，Ollama 会自动将图层卸载到它。检查：

````bash
ollama ps # 显示加载了哪个模型以及有多少个 GPU 层
````

对于 12 GB GPU 上的 31B 模型，您将获得部分卸载（GPU 上约 40 层，CPU 上剩余），这仍然可以显着加速。

## 步骤 7：作为网关机器人运行（可选）

一旦 OpenClaw 在 CLI 中本地运行，您就可以将其公开为 Telegram 或 Discord 机器人 - 仍然完全在您的硬件上运行。

### 电报

1.通过[@BotFather](https://t.me/BotFather)创建机器人并获取token
2. 添加到你的`~/.hermes/config.yaml`：

````yaml
型号：
  默认值：“gemma4:31b”
  提供商：“自定义”
  base_url：“http://localhost:11434/v1”

平台：
  电报：
    启用：真
    令牌：“YOUR_TELEGRAM_BOT_TOKEN”
````

3.启动网关：

````bash
爱马仕网关
````

现在在 Telegram 上向您的机器人发送消息 — 它会使用您的本地模型进行响应。

### 不和谐

1. 在 [discord.com/developers](https://discord.com/developers/applications) 创建一个 Discord 应用程序
2. 添加配置：

````yaml
平台：
  不和谐：
    启用：真
    令牌：“YOUR_DISCORD_BOT_TOKEN”
````

3.启动：`hermes gateway`

## 步骤 8：设置后备（可选）

本地模型可能会难以应对复杂的任务。设置仅在本地模型失败时激活的云后备：

````yaml
型号：
  默认值：“gemma4:31b”
  提供商：“自定义”
  base_url：“http://localhost:11434/v1”

后备提供者：
  - 提供商：openrouter
    型号：anthropic/claude-sonnet-4
````

这样，您 90% 的使用都是免费的（本地），只有困难的任务才会使用付费 API。

## 故障排除

### 启动时“连接被拒绝”

奥拉马没有跑步。启动它：

````bash
sudo systemctl 启动 ollama
# 或
乌拉马服务
````

### 反应慢

- **检查模型大小与 RAM：** 如果您的模型需要的 RAM 多于可用的 RAM，则会交换到磁盘。使用较小的型号或添加 RAM。
- **检查 `ollama ps`：** 如果没有卸载 GPU 层，则响应受 CPU 限制。对于仅使用 CPU 的服务器来说，这是正常现象。
- **减少上下文：** 大型对话会减慢推理速度。定期使用“/compress”，或在配置中设置较低的压缩阈值。

### 模型不遵循工具调用

较小的模型（3B、7B）有时会忽略工具调用指令并生成纯文本而不是结构化函数调用。解决方案：

- **使用更大的模型** — `gemma4:31b` 或 `gemma2:27b` 比 3B/7B 模型更好地处理工具调用。
- **OpenClaw 具有自动修复功能** — 它会检测格式错误的工具调用并尝试自动修复它们。
- **设置后备** — 如果本地模型失败 3 次，OpenClaw 会回退到云提供商。

### 上下文窗口错误

默认的 Ollama 上下文（2048 个令牌）对于代理工作来说太小。请参阅[步骤 6](#step-6-optimize-for-speed) 来提高速度。

## 成本比较

基于典型的编码会话（~100K 令牌输入，~20K 令牌输出），与云 API 相比，本地运行可以节省以下费用：

|供应商|每次会话费用|每月（日常使用）|
|----------|-----------------|---------------------|
|人类克劳德十四行诗| ~$0.80 | ~$24 |
|开放路由器 (GPT-4o) | 〜$0.60 | ~$18 |
| **Ollama（本地）** | **0.00 美元** | **0.00 美元** |

您唯一的成本是电费——每次会话大约 0.01-0.05 美元，具体取决于硬件。

## 什么在本地有效

- **文件编辑和代码生成** — 9B+ 型号可以很好地处理这个问题
- **终端命令** - OpenClaw 包装命令，运行它，读取输出，无论模型如何
- **网页浏览** — 浏览器工具进行获取；模型只是解释结果
- **Cron 作业和计划任务** — 与云设置的工作方式相同
- **多平台网关** — Telegram、Discord、Slack 均适用于本地模型

## 云模型的优点是什么

- **非常复杂的多步骤推理** - 70B+ 或像 Claude Opus 这样的云模型明显更好
- **长上下文窗口** — 云模型提供 100K–1M 代币；本地运行时通常默认低于 OpenClaw 的 64K 最小值，除非您配置它们
- **大型响应的速度** - 对于长代而言，云推理比仅使用 CPU 的本地推理更快

最佳点：使用本地来处理日常任务，为困难的事情设置云后备。