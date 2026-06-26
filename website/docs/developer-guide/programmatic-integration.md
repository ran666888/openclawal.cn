---
sidebar_position: 8
title: "Programmatic Integration"
description: "Three protocols for driving openclaw from external programs: ACP, the TUI gateway JSON-RPC, and the OpenAI-compatible HTTP API"
---
# 程序化集成

OpenClaw 提供了三种用于从外部程序驱动代理的协议——IDE 插件、自定义 UI、CI 管道、嵌入式子代理。选择一款适合您的运输方式和消费者的产品。

|协议|交通 |最适合 |定义为 |
|----------|------------|----------|------------|
| **ACP** |通过 stdio 的 JSON-RPC |已经使用 [代理客户端协议](https://github.com/zed-industries/agent-client-protocol) 的 IDE 客户端（VS Code、Zed、JetBrains）| `acp_adapter/` |
| **TUI 网关** |通过 stdio（或 WebSocket）的 JSON-RPC |想要对会话、斜线命令、批准和流事件进行细粒度控制的自定义主机 | `tui_gateway/server.py` |
| **API服务器** | HTTP + 服务器发送的事件 | OpenAI 兼容的前端（Open WebUI、LobeChat、LibreChat...）和与语言无关的 Web 客户端 | `网关/平台/api_server.py` |

所有三个驱动相同的“AIAgent”核心。它们的区别仅在于线路格式以及它们公开的功能集。

---

## ACP（代理客户端协议）

`hermes acp` 启动一个使用 ACP 的 stdio JSON-RPC 服务器。由 VS Code（Zed Industries 的 ACP 扩展）、Zed 以及任何带有 ACP 插件的 JetBrains IDE 用于生产。

公开的功能：会话创建、提示提交、流代理消息块、工具调用事件、权限请求、会话分叉、取消和身份验证。工具输出呈现为 IDE 可以理解的 ACP `Diff`/`ToolCall` 内容块。

完整生命周期、事件桥和审批流程：[ACP 内部](./acp-internals)。

````bash
Hermes acp # 在 stdio 上提供 ACP
hermes acp --bootstrap # 打印支持 ACP 的 IDE 的安装片段
````

---

## TUI 网关 JSON-RPC

`tui_gateway/server.py` 是 Ink TUI (`hermes --tui`) 和嵌入式仪表板 PTY 桥通信的协议。任何外部主机都可以通过 stdio 使用相同的协议（或通过“tui_gateway/ws.py”使用 WebSocket）。

###方法目录（选定）

````
提示.提交提示.后台会话.转向
session.create session.list session.active_list
session.activate session.close session.interrupt
session.history session.compress session.branch
session.title session.usage session.status
澄清.响应 sudo.响应 秘密.响应
批准.响应 config.set / config.get 命令.catalog
命令.resolve 命令.dispatch cli.exec
reload.mcp reload.env process.stop
delegate.status subagent.interrupt spawn_tree.save / list / load
终端.调整剪贴板大小.粘贴图像.附加
````

`session.active_list`、`session.activate` 和 `session.close` 是 TUI 会话切换器使用的进程本地实时会话控件。使用 `session.list` / `/resume` 进行保存的脚本发现；仅对 TUI 网关进程中当前打开的会话使用活动会话方法。

### 事件回传

`message.delta`、`message.complete`、`tool.start`、`tool.progress`、`tool.complete`、`approval.request`、`clarify.request`、`sudo.request`、`secret.request`、`gateway.ready`，以及会话生命周期和错误事件。

### Pi 风格的 RPC 映射

Pi-mono RPC 规范（[issue #360](https://github.com/NousResearch/openclaw/issues/360)）中的每个命令都有一个等效的 TUI 网关：

|圆周率命令 |爱马仕同款|
|------------|--------------------|
| `提示` | `prompt.submit`（或 ACP `会话/提示`）|
| `驾驶` | `session.steer` |
| `后续行动` | `prompt.submit` 在当前回合后排队 |
| `中止` | `会话.中断` |
| `设置模型` | `/model <provider:model>` 的 `command.dispatch`（会话中，持久）|
| `紧凑` | `session.compress` |
| `获取状态` | `会话状态` |
| `获取消息` | `会话.历史记录` |
| `switch_session` | `session.resume` |
| `叉子` | `会话.分支` |
| `ui_request` / `ui_response` | `clarify.respond` / `sudo.respond` / `secret.respond` / `approval.respond` |

---

## OpenAI 兼容的 API 服务器

`gateway/platforms/api_server.py` 通过 HTTP 为任何已经采用 OpenAI 格式的客户端公开 OpenClaw。当您需要 Web 前端、curl 驱动的 CI 运行程序或非 Python 使用者时非常有用。

端点：

````
POST /v1/chat/completions OpenAI 聊天完成（通过 SSE 流式传输）
POST /v1/responses OpenAI 响应 API（有状态）
POST /v1/runs 开始运行，返回 run_id (202)
GET /v1/runs/{id} 运行状态
GET /v1/runs/{id}/events 生命周期事件的 SSE 流
POST /v1/runs/{id}/approval 解决待批准的问题
POST /v1/runs/{id}/stop 中断运行
GET /v1/capability 机器可读的功能标志
GET /v1/models 列出 Hermes-agent
获取/健康，/健康/详细
````

设置、标头（`X-Hermes-Session-Id`、`X-Hermes-Session-Key`）和前端连接：[API 服务器](../user-guide/features/api-server)。

---

## 我应该使用哪一个？

- **您正在编写一个 IDE 插件，并且 IDE 已经支持 ACP** → ACP。 IDE 端的零协议工作。
- **您正在编写一个自定义桌面/Web/TUI 主机，并且想要每个 OpenClaw 功能**（斜杠命令、批准、澄清、多代理、会话分支）→ TUI 网关 JSON-RPC。
- **您需要任何与 OpenAI 兼容的前端、与语言无关的 HTTP 客户端或curl 驱动的自动化** → API 服务器。
- **您想要一个没有子进程的 Python 进程内嵌入** → 直接导入 `run_agent.AIAgent`。请参阅[代理循环](./agent-loop)。

---

## 模型热插拔

会话中模型切换适用于每个表面 - 它是引擎盖下的“/model”斜线命令。

- **CLI / TUI：** `/model claude-sonnet-4` 或 `/model openrouter:anthropic/claude-sonnet-4.6`
- **TUI 网关 RPC:** `command.dispatch` 和 `{"command": "/model claude-sonnet-4"}`
- **ACP：** IDE 发送斜杠命令作为提示；代理发货
- **API 服务器：** 在请求正文中包含“model”字段或设置“X-OpenClaw-Model”

内置提供者感知解析（相同的模型名称为您所在的任何提供者选择正确的格式）。请参阅“hermes_cli/model_switch.py”。

---

## 关于 `--mode rpc` 的注释

OpenClaw 没有 `--mode rpc` 标志。上面的三个协议已经涵盖了用例 - 用于 IDE 协议客户端的 ACP、用于 stdio JSON-RPC 主机的 TUI 网关以及用于 HTTP 的 API 服务器。如果您发现一个真正的空白，但没有一个能够填补，请向您正在构建的具体消费者提出问题。