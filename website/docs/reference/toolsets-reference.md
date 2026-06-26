---
sidebar_position: 4
title: "Toolsets Reference"
description: "OpenClaw 核心、复合、平台和动态工具集参考"
---
# 工具集参考

工具集被命名为控制代理可以执行的操作的工具包。它们是配置每个平台、每个会话或每个任务工具可用性的主要机制。

## 工具集如何工作

每个工具都属于一个工具集。当您启用工具集时，该捆绑包中的所有工具都可供代理使用。工具集分为三种：

- **核心** - 相关工具的单个逻辑组（例如，“file”捆绑“read_file”、“write_file”、“patch”、“search_files”）
- **复合** - 结合多个核心工具集以实现常见场景（例如，“调试”捆绑文件、终端和 Web 工具）
- **平台** - 针对特定部署上下文的完整工具配置（例如，“hermes-cli”是交互式 CLI 会话的默认设置）

## 配置工具集

### 每会话 (CLI)

````bash
Hermes 聊天工具集 Web、文件、终端
Hermes chat --toolsets debug # 复合 — 扩展为文件 + 终端 + Web
爱马仕聊天 --toolsets all # 一切
````

### 每个平台 (config.yaml)

````yaml
工具集：
  - Hermes-cli # CLI 默认值
  # - hermes-telegram # 覆盖 Telegram 网关
````

### 互动管理

````bash
Hermes 工具 # Curses UI 以启用/禁用每个平台
````

或在会议中：

````
/工具列表
/tools 禁用浏览器
/tools 启用家庭助理
````

## 核心工具集

|工具组 |工具|目的|
|--------|--------|---------|
| `浏览器` | `browser_back`、`browser_cdp`、`browser_click`、`browser_console`、`browser_dialog`、`browser_get_images`、`browser_navigate`、`browser_press`、`browser_scroll`、`browser_snapshot`、`browser_type`、`browser_vision`、`web_search` |核心浏览器自动化。包括“web_search”作为快速查找的后备。 `browser_cdp` 和 `browser_dialog` 在运行时进行门控 - 仅当在会话启动时可访问 CDP 端点时才注册（通过 `/browser connect`、`browser.cdp_url` 配置、Browserbase 或 Camofox）。 `browser_dialog` 与附加 CDP Supervisor 时 `browser_snapshot` 添加的 `pending_dialogs` 和 `frame_tree` 字段一起工作。 |
| `澄清` | `澄清` |当代理需要澄清时向用户提问。 |
| `代码执行` | `执行代码` |运行以编程方式调用 OpenClaw 工具的 Python 脚本。 |
| `cronjob` | `cronjob` |安排和管理重复任务。 |
| `调试` |复合（`文件`+`终端`+`网络`）|调试包 — 文件、进程/终端、Web 提取/搜索。 |
| `代表团` | `委托任务` |生成独立的子代理实例以进行并行工作。 |
| `不和谐` | `不和谐` |核心 Discord 文本/嵌入/DM 操作（仅限网关）。活跃于“hermes-discord”工具集。 |
| `discord_admin` | `discord_admin` | Discord 审核（禁令、角色变更、渠道管理）。活跃于“hermes-discord”工具集；要求机器人持有相关的 Discord 权限。 |
| `飞书_doc` | `feishu_doc_read` |阅读飞书/飞书文档内容。飞书文档评论智能回复处理程序使用。 |
| `飞书驱动` | `feishu_drive_add_comment`、`feishu_drive_list_comments`、`feishu_drive_list_comment_replies`、`feishu_drive_reply_comment` |飞书/飞书驱动评论操作。范围仅限于评论代理；未暴露在“hermes-cli”或其他消息传递工具集上。 |
| `文件` | `patch`、`read_file`、`search_files`、`write_file` |文件读取、写入、搜索和编辑。 |
| `家庭助理` | `ha_call_service`、`ha_get_state`、`ha_list_entities`、`ha_list_services` |通过家庭助理进行智能家居控制。仅当设置了“HASS_TOKEN”时才可用。 |
| `计算机使用` | `计算机使用` |通过 cua-driver 进行后台 macOS 桌面控制 — 不会窃取光标/焦点。适用于任何支持工具的模型。仅限 macOS；需要“$PATH”上的“cua-driver”。 |
| `context_engine` | （各不相同）|活动上下文引擎插件公开的运行时工具（在插件填充它之前为空）。 |
| `image_gen` | `图像_生成` |通过 FAL.ai 生成文本到图像（可选择加入 OpenAI / xAI 后端）。 |
| `video_gen` | `视频生成` |通过插件注册后端（xAI Grok-Imagine、FAL.ai Veo 3.1 / Pixverse v6 / Kling O3）进行文本到视频和图像到视频。传递`image_url`来动画图像；对于文本转视频，请忽略它。 |
| `看板` | `kanban_block`、`kanban_comment`、`kanban_complete`、`kanban_create`、`kanban_heartbeat`、`kanban_link`、`kanban_list`、`kanban_show`、`kanban_unblock` |多代理协调工具。注册用于调度程序生成的任务工作人员（“HERMES_KANBAN_TASK”）和按名称显式列出“看板”工具集的配置文件（“all”/“*”通配符**不**启用它）。工作人员标记已完成的任务、阻止、心跳、评论以及创建/链接后续任务； Orchestrator 配置文件还获得了列表/解锁等板路由工具。 |
| `记忆` | `记忆` |持久的跨会话内存管理。 |
| `消息传递` | `发送消息` |从会话内向其他平台（Telegram、Discord 等）发送消息。 |
| `恐鸟` | `混合剂` |通过混合代理实现多模型共识。 |
| `安全` | `image_generate`、`vision_analyze`、`web_extract`、`web_search` （通过 `includes`）|只读研究+媒体生成。没有文件写入，没有终端，没有代码执行。 |
| `搜索` | `网络搜索` |仅网络搜索（无摘录）。 |
| `会话搜索` | `会话搜索` |搜索过去的对话会话。 |
| `技能` | `技能管理`、`技能视图`、`技能列表` |技能 CRUD 和浏览。 |
| `Spotify` | `spotify_albums`、`spotify_devices`、`spotify_library`、`spotify_playback`、`spotify_playlists`、`spotify_queue`、`spotify_search` |本机 Spotify 控件（播放、队列、搜索、播放列表、专辑、库）。由捆绑的“spotify”插件注册。 |
| `终端` | `进程`、`终端` | Shell命令执行和后台进程管理。 |
| `待办事项` | `待办事项` |会话内的任务列表管理。 |
| `tts` | `文本转语音` |文本到语音的音频生成。 |
| `愿景` | `视觉分析` |通过具有视觉功能的模型进行图像分析。 |
| `视频` | `视频分析` |视频分析和理解工具（选择加入，不在默认工具集中 - 通过“--toolsets”显式添加）。 |
| `网络` | `web_extract`、`web_search` |网络搜索和页面内容提取。 |
| `x_搜索` | `x_搜索` |通过 xAI 的内置“x_search”响应工具搜索 X (Twitter) 帖子和线程。默认关闭；通过“hermes 工具”选择加入。仅在配置 xAI 凭据（SuperGrok OAuth 或“XAI_API_KEY”）时注册架构。 |
| `元宝` | `yb_query_group_info`、`yb_query_group_members`、`yb_search_sticker`、`yb_send_dm`、`yb_send_sticker` |元宝DM/群动作和贴纸搜索。仅在“hermes-yuanbao”上注册。 |

## 平台工具集

平台工具集定义部署目标的完整工具配置。大多数消息传递平台使用与“hermes-cli”相同的集合：

|工具组 |与 `hermes-cli` 的区别 |
|--------|--------------------------------------------|
| `hermes-cli` |完整工具集 — 交互式 CLI 会话的默认设置。包括文件、终端、Web、浏览器、内存、技能、视觉、image_gen、todo、tts、委托、code_execution、cronjob、session_search、澄清和“安全”（只读）捆绑包以及标准消息传递工具。 |
| `爱马仕-acp` |删除“clarify”、“cronjob”、“image_generate”、“send_message”、“text_to_speech”以及所有四个 Home Assistant 工具。专注于 IDE 上下文中的编码任务。 |
| `hermes-api-服务器` |删除“clarify”、“send_message”和“text_to_speech”。保留其他所有内容 - 适合无法进行用户交互的编程访问。 |
| `hermes-cron` |与“hermes-cli”相同。 |
| `爱马仕电报` |与“hermes-cli”相同。 |
| `hermes-discord` |在“hermes-cli”之上添加“discord”和“discord_admin”。 |
| `hermes-slack` |与“hermes-cli”相同。 |
| `hermes-whatsapp` |与“hermes-cli”相同。 |
| `hermes 信号` |与“hermes-cli”相同。 |
| `赫尔墨斯矩阵` |与“hermes-cli”相同。 |
| “爱马仕-mattermost” |与“hermes-cli”相同。 |
| `hermes-电子邮件` |与“hermes-cli”相同。 |
| `hermes-短信` |与“hermes-cli”相同。 |
|爱马仕-bluebubbles |与“hermes-cli”相同。 |
| `hermes-dingtalk` |与“hermes-cli”相同。 |
| `hermes-飞鼠` |添加五个 `feishu_doc_*` / `feishu_drive_*` 工具（仅由文档评论处理程序使用，而不是常规聊天适配器）。 |
| `hermes-qqbot` |与“hermes-cli”相同。 |
| `hermes-wecom` |与“hermes-cli”相同。 |
| `hermes-wecom-callback` |与“hermes-cli”相同。 |
| `hermes-微信` |与“hermes-cli”相同。 |
| `hermes-元宝` |在“hermes-cli”之上添加五个“yb_*”工具（DM/group/sticker）。 |
| `hermes-homeassistant` |与 `hermes-cli` 相同（Home Assistant 工具默认已经存在，并在设置 `HASS_TOKEN` 时激活）。 |
| `hermes-webhook` |与“hermes-cli”相同。 |
| `hermes-网关` |内部网关协调器工具集 - 每个“hermes-<platform>”工具集的联合；当网关需要接受任何消息源时使用。 |

## 动态工具集

### MCP 服务器工具集

每个配置的 MCP 服务器在运行时都会生成一个“mcp-<server>”工具集。例如，如果您配置“github”MCP 服务器，则会创建一个“mcp-github”工具集，其中包含服务器公开的所有工具。

````yaml
# 配置.yaml
mcp_服务器：
  github：
    命令：npx
    参数：[“-y”，“@modelcontextprotocol/server-github”]
````

这将创建一个“mcp-github”工具集，您可以在“--toolsets”或平台配置中引用。

### 插件工具集

插件可以在插件初始化期间通过 ctx.register_tool() 注册自己的工具集。它们与内置工具集一起出现，并且可以以相同的方式启用/禁用。

### 自定义工具集

在“config.yaml”中定义自定义工具集以创建特定于项目的捆绑包：

````yaml
工具集：
  - Hermes-cli
自定义工具集：
  数据科学：
    - 文件
    - 终端
    - 代码执行
    - 网络
    - 愿景
````

### 通配符

- `all` 或 `*` — 扩展到每个已注册的工具集（内置+动态+插件）

少数工具除了工具集成员资格之外还有额外的可用性检查，并且**不**仅由“all”/“*”打开：

- **功能门控**工具（浏览器、`computer_use`、`code_execution`、飞书、家庭助理、cronjob）仅在配置了后端/凭据先决条件后才会出现。
- **工作流程门控**工具——“看板”工具集——是有意选择加入的。 `all`/`*` 确实**不**启用看板；您必须显式列出“看板”（或者是设置了“HERMES_KANBAN_TASK”的调度程序生成的工作人员）。看板工具会改变共享板状态，因此即使在“all”下，它们也默认处于关闭状态。

## 与“hermes 工具”的关系

“hermestools”命令提供了一个基于curses的UI，用于在每个平台上打开或关闭单个工具。它在工具级别运行（比工具集更精细）并持续到“config.yaml”。即使已启用工具集，已禁用的工具也会被过滤掉。

另请参阅：[工具参考](./tools-reference.md)，了解各个工具及其参数的完整列表。