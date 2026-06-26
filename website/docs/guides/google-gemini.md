---
sidebar_position: 16
title: "Google Gemini"
description: "Use OpenClaw with Google Gemini — native AI Studio API, API-key setup, tool calling, streaming, and quota guidance"
---
# 谷歌双子座

OpenClaw 使用 **Google AI Studio / Gemini API** 支持 Google Gemini 作为本机提供商，而不是 OpenAI 兼容端点。这让 OpenClaw 将其内部 OpenAI 形状的消息和工具循环转换为 Gemini 的本机“generateContent”API，同时保留工具调用、流式传输、多模式输入和 Gemini 特定的响应元数据。

## 先决条件

- **Google AI Studio API 密钥** — 在 [aistudio.google.com/apikey](https://aistudio.google.com/apikey) 创建一个
- **支持计费的 Google Cloud 项目** — 建议代理使用。 Gemini 的免费层对于长时间运行的代理会话来说太小，因为 OpenClaw 可能会在每个用户回合中进行多次模型调用。
- **已安装 OpenClaw** — 本机 Gemini 提供程序不需要额外的 Python 包。

:::提示 API 密钥路径
设置“GOOGLE_API_KEY”或“GEMINI_API_KEY”。 OpenClaw 检查“gemini”提供商的两个名称。
:::

## 快速入门

````bash
# 添加您的 Gemini API 密钥
echo "GOOGLE_API_KEY=..." >> ~/.hermes/.env

# 选择 Gemini 作为您的提供商
爱马仕型号
# → 选择“更多提供商...”→“Google AI Studio”
# → 爱马仕检查你的关键等级并显示双子座模型
# → 选择型号

# 开始聊天
爱马仕聊天
````

如果您更喜欢直接配置编辑，请使用本机 Gemini API 基本 URL：

````yaml
型号：
  默认：gemini-3-flash-preview
  提供者： 双子座
  基本网址：https://generativelanguage.googleapis.com/v1beta
````

## 配置

运行“hermes model”后，您的“~/.hermes/config.yaml”将包含：

````yaml
型号：
  默认：gemini-3-flash-preview
  提供者： 双子座
  基本网址：https://generativelanguage.googleapis.com/v1beta
````

在`~/.hermes/.env`中：

````bash
GOOGLE_API_KEY=...
````

### 原生 Gemini API

推荐的终点是：

````文本
https://generativelanguage.googleapis.com/v1beta
````

OpenClaw 检测到此端点并创建其本机 Gemini 适配器。在内部，OpenClaw 仍然在 OpenAI 形状的消息中保留代理循环，然后将每个请求转换为 Gemini 的本机模式：

- `messages[]` → Gemini `contents[]`
- 系统提示 → Gemini`系统指令`
- 工具模式 → Gemini `functionDeclarations`
- 工具结果 → Gemini `functionResponse` 部分
- 流响应 → 用于 OpenClaw 循环的 OpenAI 形状的流块

:::注意双子座 3 的思想签名
对于 Gemini 3 工具的使用，OpenClaw 保留附加到函数调用部分的“thoughtSignature”值，并在下一个工具回合重放它们。这涵盖了多步骤代理工作流程的验证关键路径。

Gemini 3 还可以将思想签名附加到其他响应部分。 OpenClaw 的本机适配器目前针对代理工具循环进行了优化，因此它尚未以完整的部分级保真度重放每个非工具调用签名。
:::

### 首选本机端点

Google 还公开了一个与 OpenAI 兼容的端点：

````文本
https://generativelanguage.googleapis.com/v1beta/openai/
````

对于 OpenClaw 代理会话，首选上面的本机 Gemini 端点。 OpenClaw 包含一个原生 Gemini 适配器，因此它可以将多轮工具使用、工具调用结果、流、多模式输入和 Gemini 响应元数据直接映射到 Gemini 的“generateContent”API 上。当您特别需要 OpenAI API 兼容性时，OpenAI 兼容端点仍然有用。

如果您之前将 `GEMINI_BASE_URL` 设置为 `/openai` URL，请将其删除或更改：

````bash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
````

## 可用型号

“hermes 模型”选择器显示 OpenClaw 提供商注册表中维护的 Gemini 模型。常见的选择包括：

|型号|身份证 |笔记|
|--------|----|--------|
| Gemini 3.1 专业版预览 | `gemini-3.1-pro-预览版` |最强大的预览模型（如有）|
| Gemini 3 Pro 预览 | `gemini-3-pro-预览版` |强大的推理和编码模型 |
| Gemini 3 Flash 预览 | `gemini-3-flash-预览` |建议的速度和功能的默认平衡 |
| Gemini 3.1 Flash Lite 预览 | `gemini-3.1-flash-lite-preview` |可用时最快/成本最低的选项 |

模型可用性会随着时间的推移而变化。如果模型消失或未为您的密钥启用，请再次运行“hermes model”并从当前列表中选择一个。

:::info 型号 ID
当“provider:gemini”时，使用 Gemini 的本机模型 ID，例如“gemini-3-flash-preview”，而不是“google/gemini-3-flash-preview”等 OpenRouter 样式 ID。
:::

### 最新别名

Google 发布了 Pro 和 Flash Gemini 系列的移动别名。当您希望 Google 在不更改 OpenClaw 配置的情况下自动推进模型时，“gemini-pro-latest”和“gemini-flash-latest”非常有用。

|别名 |当前曲目 |笔记|
|--------|------------------|--------|
| `gemini-pro-最新` |最新Gemini Pro型号|当您想要 Google 当前的 Pro 默认设置时最好 |
| `gemini-flash-最新` |最新Gemini Flash型号|当您想要 Google 当前的 Flash 默认值时最好 |

````yaml
型号：
  默认：gemini-pro-最新
  提供者： 双子座
  基本网址：https://generativelanguage.googleapis.com/v1beta
````

如果您需要严格的重现性，请优先选择显式模型 ID，例如“gemini-3.1-pro-preview”或“gemini-3-flash-preview”。

### Gemma 通过 Gemini API

Google 还通过 Gemini API 公开 Gemma 模型。 OpenClaw 将这些识别为 Google 模型，但从默认模型选择器中隐藏吞吐量非常低的 Gemma 条目，因此新用户不会意外地为长时间运行的代理会话选择评估层模型。

有用的评估 ID 包括：

|型号|身份证 |笔记|
|--------|----|--------|
|杰玛 4 31B IT | `gemma-4-31b-it` |更大的 Gemma 模型；对于兼容性和质量评估有用|
|杰玛 4 26B A4B IT | `gemma-4-26b-a4b-it` |更小的活动参数变体（如果可用）|

这些模型最好被视为 Gemini API 密钥的评估选项。 Google 的 Gemma API 定价仅为免费套餐，与生产 Gemini 模型相比，使用上限较低，因此持续使用 OpenClaw 代理通常应转移到付费 Gemini 模型、自托管部署或具有适当配额的其他提供商。

要使用对选择器隐藏的 Gemma 模型，请直接设置它：

````yaml
型号：
  默认值：gemma-4-31b-it
  提供者： 双子座
  基本网址：https://generativelanguage.googleapis.com/v1beta
````

## 在会话中切换模型

在对话期间使用“/model”命令：

````文本
/model gemini-3-flash-preview
/model 双子座-flash-最新
/model gemini-3-pro-preview
/模型 Gemini-Pro-最新
/型号 gemma-4-31b-it
/model gemini-3.1-flash-lite-preview
````

如果您尚未配置 Gemini，请退出会话并先运行“hermes model”。 `/model` 在已配置的提供者和模型之间切换；它不会收集新的 API 密钥。

## 诊断

````bash
爱马仕医生
````

医生检查：

- `GOOGLE_API_KEY` 或 `GEMINI_API_KEY` 是否可用
- 是否可以解析配置的提供者凭据

## 网关（消息传递平台）

Gemini 适用于所有 OpenClaw 网关平台（Telegram、Discord、Slack、WhatsApp、LINE、飞书等）。将 Gemini 配置为您的提供商，然后正常启动网关：

````bash
Hermes网关设置
爱马仕网关启动
````

网关读取“config.yaml”并使用相同的 Gemini 提供程序配置。

## 故障排除

###“Gemini 本机客户端需要 API 密钥”

OpenClaw 找不到可用的 API 密钥。将其中一项添加到 `~/.hermes/.env` 中：

````bash
GOOGLE_API_KEY=...
# 或
GEMINI_API_KEY=...
````

然后再次运行“hermes model”。

###“此 Google API 密钥属于免费套餐”

OpenClaw 在设置过程中探测 Gemini API 密钥。由于工具使用、重试、压缩和辅助任务可能需要多个模型调用，因此在几次代理轮流后，免费套餐配额可能会耗尽。

在附加到您的密钥的 Google Cloud 项目上启用结算功能，根据需要重新生成密钥，然后运行：

````bash
爱马仕型号
````

###“404 型号未找到”

所选型号不适用于您的帐户、区域或密钥。再次运行“hermes model”并从当前列表中选择另一个 Gemini 模型。

### Gemma 模型未在“hermes 模型”中显示

默认情况下，OpenClaw 可能会对选择器隐藏低吞吐量的 Gemma 模型。如果您有意要评估一个，请直接在“~/.hermes/config.yaml”中设置模型 ID。

### Gemma 的“超出 429 配额”

通过 Gemini API 公开的 Gemma 模型对于评估很有用，但其 Gemini API 免费层上限较低。使用它们进行兼容性测试，然后切换到付费 Gemini 模型或其他提供商以获得持续的代理会话。

### OpenAI 兼容端点已配置

检查`~/.hermes/.env`：

````bash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
````

将其更改为本机端点或删除覆盖：

````bash
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
````

### 工具调用因架构错误而失败

升级 OpenClaw 并重新运行 `hermes model`。原生 Gemini 适配器针对 Gemini 更严格的函数声明格式清理工具架构；较旧的版本或自定义端点可能不会。

## 相关

- [人工智能提供商](/集成/提供商)
- [配置](/用户指南/配置)
- [后备提供商](/user-guide/features/fallback-providers)
- [AWS Bedrock](/guides/aws-bedrock) — 使用 AWS 凭证的本机云提供商集成