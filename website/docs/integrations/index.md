---
title: "Integrations"
sidebar_label: "Overview"
sidebar_position: 0
---
# 集成

OpenClaw 连接到外部系统以进行 AI 推理、工具服务器、IDE 工作流程、编程访问等。这些集成扩展了 OpenClaw 的功能和运行范围。

:::提示从这里开始
如果您只有时间设置一个集成，请设置 [Nous Portal](/integrations/nous-portal) — 一次 OAuth 登录涵盖 300 多个模型以及四种工具网关工具（Web 搜索、图像生成、TTS 和浏览器自动化）。
:::

## AI 提供商和路由

OpenClaw 支持多个开箱即用的人工智能推理提供商。使用“hermes model”进行交互配置，或者在“config.yaml”中设置它们。

- **[AI 提供商](/user-guide/features/provider-routing)** — OpenRouter、Anthropic、OpenAI、Google 以及任何 OpenAI 兼容端点。 OpenClaw 自动检测每个提供商的视觉、流媒体和工具使用等功能。
- **[Provider Routing](/user-guide/features/provider-routing)** — 细粒度控制哪些底层提供商处理您的 OpenRouter 请求。通过排序、白名单、黑名单和明确的优先级排序来优化成本、速度或质量。
- **[后备提供商](/user-guide/features/fallback-providers)** — 当您的主模型遇到错误时，自动故障转移到备份 LLM 提供商。包括主要模型回退和用于视觉、压缩和网络提取的独立辅助任务回退。

## 工具服务器 (MCP)

- **[MCP 服务器](/user-guide/features/mcp)** — 通过模型上下文协议将 OpenClaw 连接到外部工具服务器。无需编写原生 OpenClaw 工具即可访问 GitHub、数据库、文件系统、浏览器堆栈、内部 API 等工具。支持 stdio 和 SSE 传输、每服务器工具过滤以及功能感知资源/提示注册。

## 网页搜索后端

“web_search”和“web_extract”工具支持八个后端提供程序，通过“config.yaml”或“hermes tools”进行配置：

|后端 |环境变量 |搜索 |摘录|爬行|
|--------|---------|--------|---------|--------|
| **Firecrawl**（默认）| `FIRECRAWL_API_KEY` | ✔ | ✔ | ✔ |
| **SearXNG** | `SEARXNG_URL` | ✔ | — | — |
| **勇敢**（免费套餐）| `BRAVE_SEARCH_API_KEY` | ✔ | — | — |
| **DuckDuckGo** (ddgs) | _（无）_ | ✔ | — | — |
| **塔维利** | `TAVILY_API_KEY` | ✔ | ✔ | ✔ |
| **埃** | `EXA_API_KEY` | ✔ | ✔ | — |
| **并行** | `PARALLEL_API_KEY` | ✔ | ✔ | — |
| **xAI** | `XAI_API_KEY` | ✔ | — | — |

快速设置示例：

````yaml
网址：
  后端：firecrawl #firecrawl |搜索 |勇敢自由| DDGS |塔维利 |前 |平行|赛
````

如果未设置“web.backend”，则会从可用的 API 密钥自动检测后端。还通过“FIRECRAWL_API_URL”支持自托管 Firecrawl。

## 浏览器自动化

OpenClaw 包括完整的浏览器自动化和多个后端选项，用于导航网站、填写表单和提取信息：

- **Browserbase** — 具有反机器人工具、验证码解决和住宅代理的托管云浏览器
- **浏览器使用** — 替代云浏览器提供商
- **本地 Chromium 系列 CDP** — 使用“/browser connect”连接到正在运行的 Chrome、Brave、Chromium 或 Edge 浏览器
- **本地 Chromium** — 通过 `agent-browser` CLI 的无头本地浏览器

有关设置和使用，请参阅[浏览器自动化](/user-guide/features/browser)。

## 语音和 TTS 提供商

所有消息传递平台上的文本转语音和语音转文本：

|供应商|品质 |成本| API 密钥 |
|----------|---------|------|---------|
| **边缘 TTS**（默认）|好 |免费|不需要 |
| **十一实验室** |优秀|付费| `ELEVENLABS_API_KEY` |
| **OpenAI TTS** |好 |付费| `VOICE_TOOLS_OPENAI_KEY` |
| **最小最大** |好 |付费| `MINIMAX_API_KEY` |
| **xAI TTS** |好 |付费| `XAI_API_KEY` |
| **NeuTTS** |好 |免费|不需要 |

语音转文本支持六种提供程序：本地 Faster-Whisper（免费，在设备上运行）、本地命令包装器、Groq、OpenAI Whisper API、Mistral 和 xAI。语音消息转录适用于 Telegram、Discord、WhatsApp 和其他消息平台。有关详细信息，请参阅[语音和 TTS](/user-guide/features/tts) 和[语音模式](/user-guide/features/voice-mode)。

## IDE 和编辑器集成

- **[IDE 集成 (ACP)](/user-guide/features/acp)** — 在 ACP 兼容的编辑器（例如 VS Code、Zed 和 JetBrains）中使用 OpenClaw。 OpenClaw 作为 ACP 服务器运行，在编辑器内呈现聊天消息、工具活动、文件差异和终端命令。

## 编程访问

- **[API Server](/user-guide/features/api-server)** — 将 OpenClaw 公开为 OpenAI 兼容的 HTTP 端点。任何使用 OpenAI 格式的前端——Open WebUI、LobeChat、LibreChat、NextChat、ChatBox——都可以连接并使用 OpenClaw 作为后端及其完整的工具集。

## 记忆与个性化

- **[内置内存](/user-guide/features/memory)** — 通过“MEMORY.md”和“USER.md”文件实现持久、精选的内存。代理维护跨会话保存的个人笔记和用户配置文件数据的有限存储。
- **[Memory Providers](/user-guide/features/memory-providers)** — 插入外部内存后端以实现更深入的个性化。支持八个提供程序：Honcho（辩证推理）、OpenViking（分层检索）、Mem0（云提取）、Hindsight（知识图）、Holographic（本地 SQLite）、RetainDB（混合搜索）、ByteRover（基于 CLI）和 Supermemory。

## 消息传递平台

OpenClaw 作为网关机器人在超过 27 个消息传递平台上运行，所有平台均通过相同的“网关”子系统进行配置：

- **[Telegram](/user-guide/messaging/telegram)**、**[Discord](/user-guide/messaging/discord)**、**[Slack](/user-guide/messaging/slack)**、**[WhatsApp](/user-guide/messaging/whatsapp)**、**[Signal](/user-guide/messaging/signal)**、 **[矩阵](/user-guide/messaging/matrix)**、**[Mattermost](/user-guide/messaging/mattermost)**、**[邮件](/user-guide/messaging/email)**、**[短信](/user-guide/messaging/sms)**、**[DingTalk](/user-guide/messaging/dingtalk)**、 **[飞书/Lark](/user-guide/messaging/feishu)**、**[微信](/user-guide/messaging/wecom)**、**[微信回调](/user-guide/messaging/wecom-callback)**、**[微信](/user-guide/messaging/weixin)**、**[BlueBubbles](/user-guide/messaging/bluebubbles)**、**[QQ Bot](/user-guide/messaging/qqbot)**、**[Yuanbao](/user-guide/messaging/yuanbao)**、**[家庭助理](/user-guide/messaging/homeassistant)**、**[Microsoft Teams](/user-guide/messaging/teams)**、**[Microsoft Teams 会议](/user-guide/messaging/teams-meetings)**、**[Microsoft Graph Webhook](/user-guide/messaging/msgraph-webhook)**、**[Google 聊天](/user-guide/messaging/google_chat)**、**[LINE](/user-guide/messaging/line)**、**[ntfy](/user-guide/messaging/ntfy)**、**[SimpleX](/user-guide/messaging/simplex)**、**[打开WebUI](/user-guide/messaging/open-webui)**, **[Webhooks](/user-guide/messaging/webhooks)**

请参阅 [Messaging Gateway 概述](/user-guide/messaging) 了解平台比较表和设置指南。

## 家庭自动化

- **[Home Assistant](/user-guide/messaging/homeassistant)** — 通过四个专用工具（`ha_list_entities`、`ha_get_state`、`ha_list_services`、`ha_call_service`）控制智能家居设备。配置“HASS_TOKEN”后，Home Assistant 工具集会自动激活。

## 插件

- **[插件系统](/user-guide/features/plugins)** — 使用自定义工具、生命周期挂钩和 CLI 命令扩展 OpenClaw，而无需修改核心代码。插件可以从 `~/.hermes/plugins/`、项目本地 `.hermes/plugins/` 和 pip 安装的入口点中发现。
- **[构建插件](/guides/build-a-hermes-plugin)** — 使用工具、挂钩和 CLI 命令创建 OpenClaw 插件的分步指南。

## 培训与评估

- **[批处理](/user-guide/features/batch-processing)** — 在数百个提示中并行运行代理，生成结构化 ShareGPT 格式轨迹数据以用于训练数据生成或评估。