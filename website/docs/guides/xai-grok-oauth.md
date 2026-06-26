---
sidebar_position: 16
title: "xAI Grok OAuth (SuperGrok / X Premium+)"
description: "Sign in with your SuperGrok or X Premium+ subscription to use Grok models in OpenClaw — no API key required"
---
# xAI Grok OAuth

OpenClaw 通过基于浏览器的 OAuth 登录流程对 [accounts.x.ai](https://accounts.x.ai) 支持 xAI Grok，使用 **SuperGrok 订阅** ([grok.com](https://x.ai/grok)) 或 **X Premium+ 订阅**（链接的 X 帐户）。不需要“XAI_API_KEY”——登录一次，OpenClaw 会在后台自动刷新您的会话。

当您使用具有 Premium+ 的 X 帐户登录时，xAI 会自动将订阅状态链接到您的 xAI 会话，因此 OAuth 流程的工作方式与直接 SuperGrok 订阅者的工作方式相同。

传输重用“codex_responses”适配器（xAI 公开响应式端点），因此推理、工具调用、流式传输和提示缓存可以在不更改任何适配器的情况下工作。

OpenClaw 中的每个直接到 xAI 的界面（TTS、图像生成、视频生成和转录）也重复使用相同的 OAuth 不记名令牌，因此一次登录即可涵盖所有四个界面。

## 概述

|项目 |价值|
|------|--------|
|提供商 ID | `xai-oauth` |
|显示名称 | xAI Grok OAuth（SuperGrok / X Premium+）|
|身份验证类型 |浏览器 OAuth 2.0 PKCE（环回回调）|
|交通 | xAI 响应 API (`codex_responses`) |
|默认型号 | `grok-build-0.1` |
|端点 | `https://api.x.ai/v1` |
|认证服务器| `https://accounts.x.ai` |
|需要环境变量 |否（此提供商**不**使用`XAI_API_KEY`）|
|订阅 | [SuperGrok](https://x.ai/grok) 或 [X Premium+](https://x.com/i/premium_sign_up) — 请参阅下面的注释 |

## 先决条件

-Python 3.9+
- 安装 OpenClaw 代理
- 您的 xAI 帐户上有效的 **SuperGrok** 订阅，**或您登录的 X 帐户上的 **X Premium+** 订阅（xAI 自动链接订阅）
- 本地计算机上可用的浏览器（或使用“--no-browser”进行远程会话）

:::警告 xAI 可能会按层限制 OAuth API 访问
xAI 的后端在 OAuth API 表面上强制执行自己的允许列表，并且即使应用内订阅处于活动状态，也会拒绝带有“HTTP 403”的标准 SuperGrok 订阅者（请参阅问题 [#26847](https://github.com/NousResearch/openclaw/issues/26847)）。如果 OAuth 在浏览器中登录成功，但推理返回 403，请设置“XAI_API_KEY”并切换到 API 密钥路径（“provider: xai”）——该表面今天不再受到相同的门控。
:::

## 快速入门

````bash
# 启动提供者和模型选择器
爱马仕型号
# → 从提供商列表中选择“xAI Grok OAuth (SuperGrok / X Premium+)”
# → Hermes 打开你的浏览器访问accounts.x.ai
# → 批准浏览器中的访问
# → 选择一个模型（grok-build-0.1 位于顶部）
# → 开始聊天

爱马仕
````

首次登录后，凭据存储在“~/.hermes/auth.json”下，并在过期前自动刷新。

## 手动登录

您无需通过模型选择器即可触发登录：

````bash
Hermes auth 添加 xai-oauth
````

### 远程/无头会话

在没有可用浏览器的服务器、容器或 SSH 会话上，OpenClaw 会检测远程环境并打印授权 URL，而不是打开浏览器。

**重要提示：** 环回侦听器仍然在远程计算机“127.0.0.1:56121”上运行。 xAI 重定向需要到达*那个*侦听器，因此在笔记本电脑上打开 URL 将失败（“无法建立连接。我们无法访问您的应用程序。”），除非您转发端口：

````bash
# 在本地计算机上的单独终端中：
ssh -N -L 56121:127.0.0.1:56121 用户@远程主机

# 然后在远程计算机上的 SSH 会话中：
Hermes auth 添加 xai-oauth --无浏览器
# 在本地浏览器中打开打印的授权 URL。
````

通过跳转盒/堡垒：添加 `-J Jump-user@jump-host`。

请参阅 [OAuth over SSH / Remote Hosts](./oauth-over-ssh.md) 了解完整的步骤，包括 ProxyJump 链、mosh/tmux 和 ControlMaster 陷阱。

### 仅浏览器远程（Cloud Shell、Codespaces、EC2 Instance Connect）

如果您没有常规 SSH 客户端（例如，您在 GCP Cloud Shell、GitHub Codespaces、AWS EC2 Instance Connect、Gitpod 或其他基于浏览器的控制台中运行 OpenClaw），则上面的“ssh -L”配方不可用。使用 `--manual-paste` 代替 — OpenClaw 会跳过环回侦听器，并让您直接从浏览器粘贴失败的回调 URL：

````bash
Hermes auth 添加 xai-oauth --manual-paste
# 或者通过模型选择器：
爱马仕模型--手动粘贴
````

请参阅 [OAuth over SSH/远程主机](./oauth-over-ssh.md#browser-only-remote-cloud-shell--codespaces--ec2-instance-connect) 了解完整演练。 [#26923](https://github.com/NousResearch/openclaw/issues/26923) 的回归修复。

如果同意页面直接在页面上呈现授权代码（xAI 在基于浏览器的控制台上的当前行为），而不是重定向到您的“127.0.0.1:56121/callback”，请在“Callback URL:”提示处粘贴**仅裸代码值** — OpenClaw 接受完整的 URL、裸的“?code=...&state=...”查询片段或可互换的裸代码。

## 登录的工作原理

1. OpenClaw 打开浏览器并访问“accounts.x.ai”。
2. 您登录（或确认您的现有会话）并批准访问。
3. xAI 重定向回 OpenClaw，并将令牌保存到 `~/.hermes/auth.json`。
4. 从那时起，OpenClaw 将在后台刷新访问令牌 — 您将保持登录状态，直到您`hermes auth logout xai-oauth`或从您的 xAI 帐户设置撤销访问权限。

## 检查登录状态

````bash
爱马仕医生
````

“◆ Auth Providers”部分将显示每个提供程序的当前状态，包括“xai-oauth”。

## 切换模型

````bash
爱马仕型号
# → 选择“xAI Grok OAuth (SuperGrok / X Premium+)”
# → 从模型列表中选择（grok-build-0.1 固定在顶部）
````

或者直接设置模型：

````bash
Hermes 配置集 model.default grok-build-0.1
Hermes 配置集 model.provider xai-oauth
````

## 配置参考

登录后，`~/.hermes/config.yaml` 将包含：

````yaml
型号：
  默认值：grok-build-0.1
  提供商：xai-oauth
  基本网址：https://api.x.ai/v1
````

### 提供者别名

以下所有内容均解析为“xai-oauth”：

````bash
Hermes --provider xai-oauth # 规范
Hermes --provider grok-oauth # 别名
Hermes --provider x-ai-oauth # 别名
Hermes --provider xai-grok-oauth # 别名
````

## Direct-to-xAI 工具（TTS/图像/视频/转录/X 搜索）

一旦您通过 OAuth 登录，每个直接到 xAI 的工具都会自动重复使用相同的不记名令牌 — **无需单独设置**，除非您更愿意使用 API 密钥。

为每个工具选择一个后端：

````bash
爱马仕工具
# → 文本转语音 → “xAI TTS”
# → 图像生成 → “xAI Grok Imagine（图像）”
# → 视频生成 → “xAI Grok Imagine”
# → X (Twitter) 搜索 →“xAI Grok OAuth (SuperGrok / X Premium+)”
````

如果 OAuth 令牌已存储，选择器会确认并跳过凭据提示。如果 OAuth 和“XAI_API_KEY”均未设置，选择器将提供 3 个选择菜单：OAuth 登录、粘贴 API 密钥或跳过。

:::note 视频生成默认关闭
默认情况下禁用“video_gen”工具集。在代理调用“video_generate”之前，请在“hermes tools”→“🎬 Video Generation”（按空格键）中启用它。否则，代理可能会退回到捆绑的 ComfyUI 技能，该技能也被标记为视频生成。
:::

:::note 当 xAI 凭证存在时，X 搜索会自动启用
只要配置了 xAI 凭据（SuperGrok / X Premium+ OAuth 令牌或“XAI_API_KEY”），“x_search”工具集就会自动启用。如果您不想这样做，可以通过“hermes 工具”→“🐦 X (Twitter) 搜索”（按空格键）显式禁用。该工具通过 xAI 的内置“x_search”响应 API 进行路由 - 它可与 **SuperGrok / X Premium+ OAuth 登录名或付费“XAI_API_KEY”配合使用，并且在配置两者时首选 OAuth（使用您的订阅配额而不是 API 支出）。当未配置 xAI 凭证时，无论是否启用工具集，工具架构都会对模型隐藏。
:::

### 模型

|工具|型号|笔记|
|------|--------|--------|
|聊天 | `grok-build-0.1` |默认;通过 OAuth 登录时自动选择 |
|聊天 | `grok-4.3` |以前的默认设置 |
|聊天 | `grok-4.20-0309-reasoning` |推理变体 |
|聊天 | `grok-4.20-0309-非推理` |非推理变体 |
|聊天 | `grok-4.20-multi-agent-0309` |多代理变体 |
|图片| `grok-想象图像` |默认; ~5–10 秒 |
|图片| `grok-想象图像质量` |保真度更高； 〜10–20 秒 |
|视频 | `grok-想象视频` |文字转视频 |
|视频 | `grok-imagine-video-1.5-预览` |图像到视频；已注明日期的别名 `grok-imagine-video-1.5-2026-05-30` |
|语音合成 | （默认语音）| xAI `/v1/tts` 端点 |

聊天目录实时源自磁盘上的“models.dev”缓存；一旦缓存刷新，新的 xAI 版本就会自动出现。 `grok-build-0.1` 始终固定在列表的顶部。

## 环境变量

|变量|效果|
|----------|--------|
| `XAI_BASE_URL` |覆盖默认的“https://api.x.ai/v1”端点（很少需要）。 |

要选择 xAI 作为活动提供程序，请在“config.yaml”中设置“model.provider: xai-oauth”（使用“hermes setup”作为引导流程）或传递“--provider xai-oauth”进行单次调用。

## 故障排除

### 令牌已过期 — 不会自动重新登录

OpenClaw 在每次会话之前刷新令牌，并在 401 响应上再次响应式刷新。如果刷新因“invalid_grant”而失败（刷新令牌被撤销，或者帐户被轮换），OpenClaw 会显示键入的重新身份验证消息，而不是崩溃。

当刷新失败是终端（HTTP 4xx、“invalid_grant”、撤销授权等）时，OpenClaw 会将刷新令牌标记为已失效并在本地隔离它——后续调用会跳过注定失败的刷新尝试，而不是一遍又一遍地重放相同的 401。代理会显示一条“需要重新身份验证”消息，并不会妨碍您，直到您再次登录。

**修复：**再次运行 `hermes auth add xai-oauth` 以开始新登录。下次成功交换时隔离会清除。

### 授权超时

环回侦听器具有有限的到期窗口（默认为 180 秒）。如果您没有及时批准登录，OpenClaw 会引发超时错误。

**修复：**重新运行“hermes auth add xai-oauth”（或“hermes model”）。流程重新开始。

### 状态不匹配（可能是 CSRF）

OpenClaw 检测到授权服务器返回的“state”值与其发送的值不匹配。

**修复：**重新运行登录。如果问题仍然存在，请检查正在修改 OAuth 响应的代理或重定向。

### 从远程服务器登录

在 SSH 或容器会话上，OpenClaw 会打印授权 URL，而不是打开浏览器。环回回调侦听器仍然绑定远程主机上的“127.0.0.1:56121”——如果没有 SSH 本地转发，您的笔记本电脑的浏览器将无法访问它：

````bash
# 本地机器，单独的终端：
ssh -N -L 56121:127.0.0.1:56121 用户@远程主机

# 远程机器：
Hermes auth 添加 xai-oauth --无浏览器
````

完整演练（跳转框、mosh/tmux、端口冲突）：[OAuth over SSH / 远程主机](./oauth-over-ssh.md)。

### 成功登录后的 HTTP 403（级别/权利）

OAuth 在浏览器中完成，令牌已保存，但推理或令牌刷新返回“HTTP 403”，并显示类似“调用者无权执行指定操作”的消息。

这**不是**一个过时的令牌问题——重新运行“hermes model”不会改变它。尽管应用内订阅处于活动状态，xAI 的后端仍限制 OAuth API 访问特定的 SuperGrok 层（问题 [#26847](https://github.com/NousResearch/openclaw/issues/26847)）。

**修复：** 设置 `XAI_API_KEY` 并切换到 API 密钥路径：

````bash
导出 XAI_API_KEY=xai-...
Hermes 配置集 model.provider xai
````

或者如果需要 OAuth 路由，请在 [x.ai/grok](https://x.ai/grok) 升级您的订阅。

### 运行时出现“未找到 xAI 凭据”错误

身份验证存储没有“xai-oauth”条目，也没有设置“XAI_API_KEY”。您尚未登录，或者凭证文件已被删除。

**修复：**运行 `hermes model` 并选择 xAI Grok OAuth 提供程序，或运行 `hermes auth add xai-oauth`。

## 注销

要删除所有存储的 xAI Grok OAuth 凭据：

````bash
Hermes Auth 注销 xai-oauth
````

这会清除“auth.json”中的单例 OAuth 条目以及“xai-oauth”的任何凭证池行。如果您只想删除单个池条目，请使用“hermes auth remove xai-oauth <index|id|label>”（运行“hermes auth list xai-oauth”来查看它们）。

## 另请参阅

- [OAuth over SSH / Remote Hosts](./oauth-over-ssh.md) — 如果 OpenClaw 与您的浏览器位于不同的计算机上，则需要阅读
- [AI 提供商参考](../integrations/providers.md)
- [环境变量](../reference/environment-variables.md)
- [配置](../user-guide/configuration.md)
- [语音和 TTS](../user-guide/features/tts.md)