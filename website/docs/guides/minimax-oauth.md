---
sidebar_position: 15
title: "MiniMax OAuth"
description: "Log into MiniMax via browser OAuth and use MiniMax-M2.7 models in OpenClaw — no API key required"
---
# 最小最大 OAuth

OpenClaw 通过基于浏览器的 OAuth 登录流程支持 **MiniMax**，使用与 [MiniMax 门户](https://www.minimax.io) 相同的凭据。无需 API 密钥或信用卡 - 登录一次，OpenClaw 会自动刷新您的会话。

传输重用了“anthropic_messages”适配器（MiniMax 在“/anthropic”处公开了一个与 Anthropic Messages 兼容的端点），因此所有现有的工具调用、流式传输和上下文功能都可以在不更改任何适配器的情况下工作。

## 概述

|项目 |价值|
|------|--------|
|提供商 ID | `minimax-oauth` |
|显示名称 | MiniMax（OAuth）|
|身份验证类型 |浏览器 OAuth（PKCE 重定向流）|
|交通 |人择消息兼容 (`anthropic_messages`) |
|型号| `MiniMax-M2.7`、`MiniMax-M2.7-高速` |
|全球端点| `https://api.minimax.io/anthropic` |
|中国端点| `https://api.minimaxi.com/anthropic` |
|需要环境变量 |否（此提供程序**不**使用`MINIMAX_API_KEY`）|

## 先决条件

-Python 3.9+
- 安装 OpenClaw 代理
- [minimax.io](https://www.minimax.io)（全球）或 [minimaxi.com](https://www.minimaxi.com)（中国）的 MiniMax 帐户
- 本地计算机上可用的浏览器（或使用“--no-browser”进行远程会话）

## 快速入门

````bash
# 启动提供者和模型选择器
爱马仕型号
# → 从提供商列表中选择“MiniMax (OAuth)”
# → Hermes 打开浏览器至 MiniMax 授权页面
# → 批准浏览器中的访问
# → 选择型号（MiniMax-M2.7 或 MiniMax-M2.7-highspeed）
# → 开始聊天

爱马仕
````

首次登录后，凭据存储在“~/.hermes/auth.json”下，并在每次会话前自动刷新。

## 手动登录

您无需通过模型选择器即可触发登录：

````bash
Hermes auth 添加 minimax-oauth
````

###中国区

如果您的帐户位于中国平台 (`minimaxi.com`)，请改用基于 API 密钥的 `minimax-cn` 提供商 — `minimax-cn` 仅使用 `auth_type="api_key"` 注册（无 OAuth 流程）。直接配置`MINIMAX_CN_API_KEY`（以及可选的`MINIMAX_CN_BASE_URL`）：

````bash
echo 'MINIMAX_CN_API_KEY=你的密钥' >> ~/.hermes/.env
````

### 远程/无头会话

在没有可用浏览器的服务器或容器上：

````bash
Hermes auth 添加 minimax-oauth --无浏览器
````

OpenClaw 将打印验证 URL 和用户代码 - 在任何设备上打开 URL，并在出现提示时输入代码。

## OAuth 流程

OpenClaw 针对 MiniMax OAuth 端点实施 PKCE 浏览器 OAuth 流程：

1. OpenClaw 生成 PKCE 验证者/挑战对和随机状态值。
2. 它通过质询 POST 到“{base_url}/oauth/code”，并接收“user_code”和“verification_uri”。
3. 您的浏览器将打开“verification_uri”。如果出现提示，请输入“用户代码”。
4. OpenClaw 轮询“{base_url}/oauth/token”，直到令牌到达（或截止日期已过）。
5. 令牌（`access_token`、`refresh_token`、expiry）保存到 `~/.hermes/auth.json` 下的 `minimax-oauth` 键下。

当访问令牌在到期后 60 秒内时，令牌刷新（标准 OAuth `refresh_token` 授予）会在每次会话启动时自动运行。

## 检查登录状态

````bash
爱马仕医生
````

“◆ Auth Providers”部分将显示：

````
✓ MiniMax OAuth（已登录，区域=全局）
````

或者，如果未登录：

````
⚠ MiniMax OAuth（未登录）
````

## 切换模型

````bash
爱马仕型号
# → 选择“MiniMax (OAuth)”
# → 从模型列表中选择
````

或者直接设置模型：

````bash
Hermes 配置集 model.default MiniMax-M2.7
Hermes 配置集 model.provider minimax-oauth
````

## 配置参考

登录后，“~/.hermes/config.yaml”将包含类似以下内容的条目：

````yaml
型号：
  默认：MiniMax-M2.7
  提供商：minimax-oauth
  基本网址：https://api.minimax.io/anthropic
````

### 区域端点

|提供商 ID |门户|推理端点 |
|------------|--------|--------------------|
| `minimax-oauth`（全局）| `https://api.minimax.io` | `https://api.minimax.io/anthropic` |
| `minimax-cn` (中国) | `https://api.minimaxi.com` | `https://api.minimaxi.com/anthropic` |

### 提供者别名

以下所有内容均解析为“minimax-oauth”：

````bash
Hermes --provider minimax-oauth # 规范
Hermes --provider minimax-portal # 别名
Hermes --provider minimax-global # 别名
hermes --provider minimax_oauth # 别名（下划线形式）
````

## 环境变量

`minimax-oauth` 提供程序**不**使用 `MINIMAX_API_KEY` 或 `MINIMAX_BASE_URL`。这些变量仅适用于基于 API 密钥的“minimax”和“minimax-cn”提供商。

|变量|效果|
|----------|--------|
| `MINIMAX_API_KEY` |仅由 `minimax` 提供者使用 — 对于 `minimax-oauth` 被忽略 |
| `MINIMAX_CN_API_KEY` |仅由 `minimax-cn` 提供者使用 — 对于 `minimax-oauth` 被忽略 |

要使用“minimax-oauth”作为活动提供程序，请在“config.yaml”中设置“model.provider: minimax-oauth”（使用“hermes setup”作为引导流程），或在单次调用中传递“--provider minimax-oauth”：

````bash
Hermes --provider minimax-oauth
````

## 型号

|型号|最适合 |
|--------|----------|
| `MiniMax-M2.7` |长上下文推理，复杂的工具调用 |
| `MiniMax-M2.7-高速` |更低的延迟、更轻的任务、辅助调用 |

两种模型都支持多达 200,000 个上下文标记。

当“minimax-oauth”是主要提供者时，“MiniMax-M2.7-highspeed”也会自动用作视觉和委派任务的辅助模型。

## 故障排除

### 令牌已过期 — 不会自动重新登录

如果令牌在到期后 60 秒内，OpenClaw 会在每次会话开始时刷新令牌。如果访问令牌已过期（例如，在长时间离线之后），则刷新会在下一个请求时自动发生。如果刷新失败并显示“refresh_token_reused”或“invalid_grant”，OpenClaw 会将会话标记为需要重新登录。

当刷新失败是终端（HTTP 4xx、“invalid_grant”、撤销授权等）时，OpenClaw 将刷新令牌标记为“失效”，并将其在本地隔离，这样它就不会继续重播注定失败的交换。代理会显示一条“需要重新身份验证”消息，并不会妨碍您，直到您再次登录。

**修复：**再次运行 `hermes auth add minimax-oauth` 以开始新的登录。下次成功交换时隔离会清除。

### 授权超时

设备代码流具有有限的到期窗口。如果您没有及时批准登录，OpenClaw 会引发超时错误。

**修复：**重新运行“hermes auth add minimax-oauth”（或“hermes model”）。流程重新开始。

### 状态不匹配（可能是 CSRF）

OpenClaw 检测到授权服务器返回的“state”值与其发送的值不匹配。

**修复：**重新运行登录。如果问题仍然存在，请检查正在修改 OAuth 响应的代理或重定向。

### 从远程服务器登录

如果“hermes”无法打开浏览器窗口，请使用“--no-browser”：

````bash
Hermes auth 添加 minimax-oauth --无浏览器
````

OpenClaw 打印 URL 和代码。在任何设备上打开 URL 并在那里完成流程。

### 运行时出现“未登录 MiniMax OAuth”错误

身份验证存储没有“minimax-oauth”的凭据。您尚未登录，或凭证文件已被删除。

**修复：**运行 `hermes model` 并选择 MiniMax (OAuth)，或运行 `hermes auth add minimax-oauth`。

## 注销

要删除存储的 MiniMax OAuth 凭据：

````bash
Hermes auth 注销 minimax-oauth
````

## 另请参阅

- [AI 提供商参考](../integrations/providers.md)
- [环境变量](../reference/environment-variables.md)
- [配置](../user-guide/configuration.md)
- [爱马仕医生](../reference/cli-commands.md)