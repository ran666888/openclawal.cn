---
sidebar_position: 17
title: "OAuth over SSH / Remote Hosts"
description: "How to complete browser-based OAuth (xAI, Spotify, MCP servers) when OpenClaw runs on a remote machine, container, or behind a jump box"
---
# 通过 SSH/远程主机进行 OAuth

一些 OpenClaw 提供商 — **xAI Grok OAuth**、**Spotify** 和 **远程 MCP 服务器**（Linear、Sentry、Atlassian、Asana、Figma 等） — 使用*环回重定向* OAuth 流程。身份验证服务器将您的浏览器重定向到“http://127.0.0.1:<port>/callback”，以便 OpenClaw 启动的小型 HTTP 侦听器可以获取授权代码。

当 OpenClaw 和你的浏览器在同一台机器上时，这非常有效。一旦它们不在，它就会中断：您的笔记本电脑的浏览器尝试访问**您的笔记本电脑**上的“127.0.0.1”，但侦听器绑定到**远程服务器**上的“127.0.0.1”。

修复方法是单行 SSH 本地转发 — **或**，当您没有真正的 SSH 客户端（GCP Cloud Shell、GitHub Codespaces、EC2 Instance Connect、Gitpod、基于浏览器的 Web IDE）时，[#26923](https://github.com/NousResearch/openclaw/issues/26923) 中引入了新的 `--manual-paste` 标志。

## 长篇大论；博士

````bash
# 在本地计算机（笔记本电脑）上的单独终端中：
ssh -N -L 56121:127.0.0.1:56121 用户@远程主机

# 在远程计算机上现有的 SSH 会话中：
Hermes auth 添加 xai-oauth --无浏览器
# → Hermes 打印授权 URL。在笔记本电脑上的浏览器中打开它。
# → 您的浏览器重定向到 127.0.0.1:56121/callback，隧道转发
# 向远程监听器发出请求，登录完成。
````

xAI OAuth 使用端口“56121”。对于 Spotify，将其替换为“43827”。 OpenClaw 在“等待回调...”行上打印它绑定到的确切端口 - 从那里复制它。

## 仅浏览器远程（Cloud Shell / Codespaces / EC2 Instance Connect）

如果您没有常规的 SSH 客户端（例如，因为您在 GCP Cloud Shell、GitHub Codespaces、AWS EC2 Instance Connect、Gitpod 或其他基于浏览器的控制台中运行 OpenClaw），则上面的 SSH 隧道不可用。使用 `--manual-paste` 代替：

````bash
Hermes auth 添加 xai-oauth --manual-paste
# → Hermes 打印授权 URL。在笔记本电脑上的浏览器中打开它。
# → 在浏览器中批准。重定向到 127.0.0.1:56121/callback 失败
# 加载——这是预期的。
# → 从失败页面的地址栏中复制完整 URL。
# → 在出现“Callback URL:”提示时将其粘贴回终端。
````

相同的标志适用于集成模型选择器的“hermes model --manual-paste”。 OpenClaw 可互换地接受三种回调粘贴形式：完整的 URL、裸露的“?code=...&state=...”查询片段，或者——当上游同意页面在页面内呈现授权代码而不是重定向时（xAI 在基于浏览器的控制台上的当前行为）——仅是裸露的代码值。

OpenClaw 对两条路径使用**相同的 PKCE 验证器、状态和随机数**，因此上游 OAuth 流是字节相同的 — `--manual-paste` 纯粹是回调跃点的传输更改，而不是安全降级。

## 哪些提供商需要这个

|供应商|环回端口 |需要隧道吗？ |
|----------|--------------|----------------|
| `xai-oauth` (Grok SuperGrok) | `56121` |是的，当爱马仕遥远时 |
| Spotify | `43827` |是的，当爱马仕遥远时 |
| MCP 服务器（`auth：oauth`）|每个服务器自动选择|是的，当爱马仕遥远时 |
| “人择”（克劳德·普罗/麦克斯）|不适用 |否 — 粘贴代码流程 |
| `openai-codex` (ChatGPT Plus/Pro) |不适用 |否 — 设备代码流程 |
| `minimax`、`nous-portal` |不适用 |否 — 设备代码流程 |

如果您的提供商不在表中，则您不需要隧道。

## MCP 服务器

远程 MCP 服务器（Linear、Sentry、Atlassian、Asana、Figma 等）使用相同的环回重定向流。 OpenClaw 会为每个服务器自动选择一个空闲端口，并在 OAuth 流程启动时打印授权 URL — 无论是在启动时（当新服务器出现在 `mcp_servers:` 中时）还是在运行 `hermes mcp login <server>` 时。

您有两种方法可以从远程主机完成它：

**选项 1 — 将重定向 URL 粘贴回去（无需设置，在任何地方都可以工作）。** 在交互式终端上，OpenClaw 会提示您在运行本地侦听器的同时粘贴重定向 URL。在浏览器中批准后，重定向到“http://127.0.0.1:<port>/callback”将显示连接错误 - 这是预期的。从浏览器地址栏复制 **完整 URL** 并将其粘贴到 OpenClaw 提示符处：

````
  MCP OAuth：需要授权。
  在浏览器中打开此网址：

    https://mcp.linear.app/authorize?response_type=code&...

  或者将重定向 URL 粘贴到此处（或 ?code=...&state=... 部分），然后按 Enter：
> https://mcp.linear.app/callback?code=abc123&state=xyz
  从粘贴中获取授权码 - 完成流程。
````

也接受裸露的“?code=...&state=...”查询字符串。这适用于任何具有“auth: oauth”的 MCP 服务器，并且不需要更改 SSH 配置。

**选项 2 — SSH 端口转发（与 xAI / Spotify 相同）。** OpenClaw 在 SSH 会话提示中打印它绑定到的确切端口。在笔记本电脑上打开一个单独的终端：

````bash
ssh -N -L <端口>:127.0.0.1:<端口> 用户@远程主机
````

然后正常在浏览器中打开授权URL；重定向隧道通过并且侦听器拾取它。当您需要流程在无人值守的情况下完成时，请使用此选项（例如，无法以交互方式粘贴的脚本化重新身份验证）。

**陷阱 — 30 秒配置重新加载竞赛。** 如果您编辑 `~/.hermes/config.yaml` 以从正在运行的 OpenClaw 会话内部添加 OAuth MCP 服务器，CLI 会自动重新加载 MCP 连接，并有 30 秒超时。这没有足够的时间来完成交互式 OAuth 流程，重新加载将放弃。请从新终端使用“hermes mcp login <server>”——它没有这样的上限，需要等待整整 5 分钟才能粘贴回来。

## 为什么监听器不能只绑定0.0.0.0

xAI 和 Spotify 都根据白名单验证“redirect_uri”参数。两者都需要环回形式（`http://127.0.0.1:<exact-port>/callback`）。将侦听器绑定到“0.0.0.0”或其他端口将导致身份验证服务器因“redirect_uri”不匹配而拒绝请求。 SSH 隧道保持环回 URI 端到端完整。

## 分步：单 SSH 跃点

### 1. 从本地计算机启动隧道

````bash
# xAI Grok OAuth（端口 56121）
ssh -N -L 56121:127.0.0.1:56121 用户@远程主机

# 或者 Spotify（端口 43827）
ssh -N -L 43827:127.0.0.1:43827 用户@远程主机
````

`-N` 的意思是“不打开远程 shell，只保持隧道打开”。在登录期间保持此终端运行。

### 2. 在单独的 SSH 会话中，运行 auth 命令

````bash
ssh 用户@远程主机
Hermes auth 添加 xai-oauth --无浏览器
# 或对于 Spotify：
# Hermes auth 添加Spotify --无浏览器
````

OpenClaw 检测 SSH 会话，跳过浏览器自动打开，并打印授权 URL 以及“等待 http://127.0.0.1:<port>/callback”行的回调。

### 3. 在本地浏览器中打开 URL

从远程终端复制授权 URL 并将其粘贴到笔记本电脑上的浏览器中。批准同意屏幕。身份验证服务器重定向到“http://127.0.0.1:<port>/callback”。您的浏览器到达隧道，请求被转发到远程侦听器，OpenClaw 打印“登录成功！”。

一旦看到成功线，您就可以拆除隧道（在第一个终端中按 Ctrl+C）。

## 一步一步：通过跳转框

如果您通过堡垒/跳转主机到达 OpenClaw，请使用 SSH 的内置 `-J` (ProxyJump)：

````bash
ssh -N -L 56121:127.0.0.1:56121 -J 跳转用户@跳转主机 用户@最终主机
````

这通过跳转主机链接 SSH 连接，而不将环回端口放在跳转盒本身上。笔记本电脑上的本地“127.0.0.1:56121”会直接通过隧道连接到最终远程主机上的“127.0.0.1:56121”。

对于不支持 `-J` 的旧版 OpenSSH，长格式为：

````bash
ssh -N \
    -o "ProxyCommand=ssh -W %h:%p 跳转用户@跳转主机" \
    -L 56121:127.0.0.1:56121\
    用户@最终主机
````

## Mosh、tmux、ssh ControlMaster

隧道是底层 SSH 连接的属性。如果您在 mosh 会话中在“tmux”内运行 OpenClaw，则 mosh 漫游不会携带“-L”转发。 **仅为**“-L”隧道打开*单独的*普通 SSH 会话 — 这是在身份验证流程期间必须保持活动状态的连接。您的交互式 mosh/tmux 会话可以保持正常运行 OpenClaw。

如果您使用“ssh -o ControlMaster=auto”，多路复用连接上的端口转发将共享主设备的生命周期。如果隧道没有出现，请重新启动主服务器：

````bash
ssh -O 退出用户@远程主机
ssh -N -L 56121:127.0.0.1:56121 用户@远程主机
````

## 故障排除

### `绑定 [127.0.0.1]:56121: 地址已在使用中`

您的笔记本电脑上的某些东西已经在使用该端口。要么是之前的隧道没有彻底关闭，要么是当地的赫尔墨斯也在监听。找到并杀死罪犯：

````bash
#macOS/Linux
lsof -iTCP:56121 -sTCP:监听
杀死<PID>
````

然后重试“ssh -L”命令。

###“无法建立连接。我们无法访问您的应用程序。” (xAI)

当 xAI 的授权页面重定向到“127.0.0.1:<port>/callback”未到达侦听器时会显示此信息。要么隧道没有运行，端口错误，要么您正在使用上一次运行中打印的 OpenClaw 端口（如果首选端口繁忙，则可以自动切换端口 — 始终阅读最新的“等待回调...”行）。

### `xAI授权等待本地回调超时`

与上面相同的根本原因 - 重定向从未返回。检查隧道是否仍然存在（“ssh -N”不显示输出，因此请查看启动它的终端），如果需要重新启动它，然后重新运行“hermes auth add xai-oauth --no-browser”。

### 代币落在错误的`~/.hermes`中

这些令牌是在运行“hermes auth add ...”的 Linux 用户下写入的。如果您的网关/systemd 服务以不同的用户身份运行（例如“root”或专用的“hermes”用户），请以**该**用户身份进行身份验证，以便令牌落在其“~/.hermes/auth.json”中。 `sudo -u hermes -i` 或同等内容。

## 另请参阅

- [xAI Grok OAuth](./xai-grok-oauth.md)
- [Spotify（`通过 SSH 运行`）](../user-guide/features/spotify.md#running-over-ssh--in-a-headless-environment)
- [本机 MCP 客户端（OAuth 部分）](../user-guide/features/mcp.md#oauth-authenticated-http-servers)
- [SSH `-J` / ProxyJump（手册页）](https://man.openbsd.org/ssh#J)