---
title: "Nous Tool Gateway"
description: "One subscription, every tool. Web search, image generation, TTS, and cloud browsers — all routed through Nous Portal with no extra API keys."
sidebar_label: "Tool Gateway"
sidebar_position: 2
---
# Nous 工具网关

**一份订阅。每个内置工具。**

每个付费 [Nous Portal](https://portal.nousresearch.com) 订阅都包含工具网关。它通过 Nous 已经运行的基础设施路由 OpenClaw 的工具调用（网络搜索、图像生成、文本转语音和云浏览器自动化），因此您不必为了让您的代理发挥作用而注册 Firecrawl、FAL、OpenAI、Browser Use 或其他任何人。

<div style={{display:'flex',gap:'1rem',flexWrap:'wrap',margin:'1.5rem 0'}}>
  <a href="https://portal.nousresearch.com/manage-subscription" style={{background: 'var(--ifm-color-primary)', color: 'white', padding: '0.75rem 1.5rem', borderRadius: '6px', textDecoration: 'none', fontWeight: 'bold'}}>启动或管理订阅 →</a>
</div>

## 包含什么

| |工具|你得到什么 |
|---|---|---|
| 🔍 | **网络搜索和提取** |通过 Firecrawl 进行代理级网络搜索和整页提取。无需担心速率限制——网关负责扩展。 |
| 🎨 | **图像生成** |一个端点下的九个模型：**FLUX 2 Klein 9B**、**FLUX 2 Pro**、**Z-Image Turbo**、**Nano Banana Pro**（Gemini 3 Pro Image）、**GPT Image 1.5**、**GPT Image 2**、**Ideogram V3**、**Recraft V4 Pro**、**Qwen Image**。选择带有标志的每代，或者让 OpenClaw 默认为 FLUX 2 Klein。 |
| 🔊 | **文本转语音** | OpenAI TTS 语音连接到“text_to_speech”工具。将语音注释放入 Telegram，为管道生成音频，讲述任何内容。 |
| 🌐 | **云浏览器自动化** |通过浏览器使用的无头 Chromium 会话。 `browser_navigate`、`browser_click`、`browser_type`、`browser_vision` — 所有代理驱动原语，不需要 Browserbase 帐户。 |

所有四种服务均根据您的 Nous 订阅按使用量付费。使用任意组合 — 运行 Web 和图像网关，同时保留您自己的 TTS 十一实验室密钥，或通过 Nous 路由所有内容。

## 为什么它在这里

构建一个真正可以“做事”的代理意味着将 5 个以上的 API 订阅拼接在一起——每个订阅都有自己的注册、速率限制、计费和怪癖。网关将其合并到一个帐户中：

- **一张账单。** Pay Nous；其余的由我们处理。
- **一次注册。** 无需管理 Firecrawl、FAL、浏览器使用或 OpenAI 音频帐户。
- **一键。** 您的 Nous Portal OAuth 涵盖所有工具。
- **相同​​的质量。** 直接键路由使用相同的后端 - 只是由我们负责。

随时携带您自己的钥匙 - 每个工具，只要您愿意。网关不是锁定，而是捷径。

## 开始吧

共有三种方式 - 选择适合您所在位置的方式：

````bash
hermes setup --portal # 全新安装：Nous OAuth + 将 Nous 设置为提供商 + 一次性打开工具网关
````

````bash
Hermes 模型 # 将您的推理提供程序切换到 Nous Portal — 然后 Hermes 提供打开所有工具的网关
````

````bash
hermes tools # 为每个工具启用网关 - 为您想要的任何工具选择“Nous Subscription”
````

`hermes setup --portal` 和 `hermes model` 是一次性路径：登录一次，可以选择将每个工具翻转到网关。 “hermes tools”是点菜路径——一次只打开您想要的工具。

**您不必先登录。** 使用“hermes 工具”，Nous 管理的后端（网络搜索、图像、视频、TTS、浏览器）始终会列出，即使您从未登录过 Nous Portal。选择一项，如果您尚未通过身份验证，OpenClaw 会立即运行门户登录 — 无需事先运行“hermes model”。如果您的 Nous OAuth 已处于活动状态，选择后端即可立即启用它，无需额外提示。此路径仅让您登录并打开您选择的一个工具 - 它**不会**切换您的推理提供程序，并且**不会**提示您为所有其他工具启用网关。

随时查看活动内容：

````bash
hermes Portal info # Portal auth + 工具网关路由汇总
Hermes 门户工具 # 每个工具具有当前路由的网关目录
hermes status # 完整系统状态（工具网关是其中一节）
````

`hermes Portal info` 显示如下部分：

````
◆ Nous工具网关
  Nous Portal ✓ 可用的托管工具
  网络工具 ✓ 通过 Nous 订阅激活
  图像生成 ✓ 通过 Nous 订阅激活
  TTS ✓ 通过 Nous 订阅激活
  浏览器 ○ 通过浏览器使用键激活
````

标记为“通过 Nous 订阅激活”的工具正在通过网关。其他任何事情都使用您自己的密钥。

## 资格

工具网关是一项**付费订阅**功能。免费层 Nous 帐户可以使用 Portal 进行推理，但不包含托管工具 - [升级您的计划](https://portal.nousresearch.com/manage-subscription) 来解锁网关。

一些帐户还有权获得**免费工具池** - 一种小型托管工具津贴，涵盖无需付费订阅的网关工具调用。当有可用池时，网关会显示该池并在首次使用时显示设置提示，以便您可以选择加入并立即开始使用托管工具。

## 混合搭配

网关是针对每个工具的。打开它以获得您想要的效果：

- **所有工具均通过 Nous** — 最简单；一次订阅，完成。
- **网络+图像网关，自带 TTS** — 保留您的 ElevenLabs 声音，让 Nous 处理剩下的事情。
- **网关仅适用于您没有密钥的事物** — “我已经为 Browserbase 付费，但我不想要 Firecrawl 帐户”效果很好。

通过以下方式随时切换任何工具：

````bash
Hermes Tools # 每个工具类别的交互式选择器
````

选择该工具，选择 **Nous Subscription** 作为提供商（或您喜欢的任何直接提供商）。无需编辑配置。如果您尚未登录 Nous Portal，选择 **Nous 订阅** 将启动 Portal 内联登录 — 您无需首先通过“hermes model”进行身份验证。

## 使用单独的图像模型

为了提高速度，图像生成默认使用 FLUX 2 Klein 9B。通过将模型 ID 传递给“image_generate”工具来覆盖每次调用：

|型号|身份证 |最适合 |
|---|---|---|
| FLUX 2 克莱因 9B | `fal-ai/flux-2/klein/9b` |快速、良好的默认设置 |
| FLUX 2 专业版 | `fal-ai/flux-2-pro` |更高保真度 FLUX |
| Z-图像涡轮 | `fal-ai/z-image/turbo` |风格化、快速|
|纳米香蕉专业版 | `fal-ai/nano-banana-pro` |谷歌 Gemini 3 Pro 图像 |
| GPT 图像 1.5 | `fal-ai/gpt-image-1.5` | OpenAI 图像生成，文本+图像 |
| GPT 图片 2 | `fal-ai/gpt-image-2` | OpenAI最新动态|
|表意文字V3 | `fal-ai/ideogram/v3` |强烈的提示依从性+排版|
|重制版 V4 专业版 | `fal-ai/recraft/v4/pro/text-to-image` |矢量风格的图形设计 |
| Qwen 图像 | `fal-ai/qwen-image` |阿里巴巴多式联运 |

该集不断发展 - “hermes 工具”→ 图像生成显示当前的实时列表。

---

## 配置参考

大多数用户永远不需要接触这个——“hermes 模型”和“hermes 工具”以交互方式涵盖了每个工作流程。本节用于直接编写 config.yaml 或编写脚本设置。

### 每个工具 `use_gateway` 标志

每个工具的配置块都采用“use_gateway”布尔值：

````yaml
网址：
  后端：火爬行
  使用网关：true

图像生成：
  使用网关：true

tts:
  提供商：openai
  使用网关：true

浏览器：
  cloud_provider：浏览器使用
  使用网关：true
````

优先级：“use_gateway: true”通过 Nous 进行路由，无论“.env”中的任何直接键如何。 `use_gateway: false`（或不存在）使用直接密钥（如果可用），并且仅在不存在时才回退到网关。

### 禁用网关

````yaml
网址：
  use_gateway: false # Hermes 现在使用 .env 中的 FIRECRAWL_API_KEY
````

当您选择非网关提供商时，“hermes tools”会自动清除该标志，因此这种情况通常会发生在您身上。

### 自托管网关（高级）

运行您自己的 Nous 兼容网关？覆盖 `~/.hermes/.env` 中的端点：

````bash
TOOL_GATEWAY_DOMAIN=your-domain.example.com
TOOL_GATEWAY_SCHEME=https
TOOL_GATEWAY_USER_TOKEN=your-token # 通常从门户登录时自动填充
FIRECRAWL_GATEWAY_URL=https://... # 专门覆盖一个端点
````

这些旋钮用于自定义基础设施设置（企业部署、开发环境）。普通订阅者从不设置它们。

## 常见问题解答

### 它可以与 Telegram / Discord / 其他消息网关一起使用吗？

是的。工具网关在工具执行层运行，而不是 CLI。每个可以调用工具的界面（CLI、Telegram、Discord、Slack、IRC、Teams、API 服务器等）都可以透明地从中受益。

### 如果我的订阅过期会怎样？

通过网关路由的工具将停止工作，直到您通过“hermes 工具”更新或交换直接 API 密钥。赫耳墨斯在传送门上显示出明显的错误。

### 我可以查看每个工具的使用情况或成本吗？

是的 - [Nous Portal 仪表板](https://portal.nousresearch.com) 按工具细分使用情况，以便您可以了解是什么推动了您的账单。

### 是否包含 Modal（无服务器终端）？

Modal 可通过 Nous 订阅作为 **可选插件** 提供，而不是默认工具网关捆绑包的一部分。当您需要远程沙箱来执行 shell 时，可以通过“hermes setupterminal”或直接在“config.yaml”中进行配置。

### 启用网关时是否需要删除现有的 API 密钥？

不 - 将它们保存在“.env”中。当 `use_gateway: true` 时，OpenClaw 跳过直接键并使用网关。将标志翻转回“false”，您的密钥将再次成为源。网关不是锁定的。