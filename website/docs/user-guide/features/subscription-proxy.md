---
sidebar_position: 15
title: "Subscription Proxy"
description: "Use your Nous Portal subscription (or other OAuth provider) as an OpenAI-compatible endpoint for external apps"
---
# 订阅代理

订阅代理是一个本地 HTTP 服务器，允许外部应用程序 —
OpenViking、Karakeep、Open WebUI、任何与 OpenAI 兼容的东西
聊天完成——使用您的 OpenClaw 管理的提供商订阅作为他们的
法学硕士终点。代理附加正确的凭据（刷新它们
自动），因此应用程序永远不需要静态 API 密钥。

这与 [API 服务器](./api-server.md) 不同：

| | API服务器|订阅代理|
|---|---|---|
|它的服务是什么 |您的代理（完整的工具集、记忆力、技能）|原始模型推理 |
|使用案例| “使用 OpenClaw 作为聊天后端” | “使用另一个应用程序中的我的 Portal 子项”|
|授权 |您的`API_SERVER_KEY` |任何持有者（代理附加真实的）|
|工具调用|是的 - 代理运行工具 |否 — 仅直通 |

当您希望 **代理** 作为后端时，请使用 API 服务器。使用
当您只想通过订阅**模型**时，请使用代理。

## 快速入门

### 1. 登录您的提供商（一次性）

````bash
爱马仕门户网站
````

这将打开您的浏览器以查看 Nous Portal OAuth 流程。爱马仕专卖店
`~/.hermes/auth.json` 中的刷新令牌 — 所有 OpenClaw 都在同一位置
提供商实时登录。

### 2.启动代理

````bash
Hermes代理启动
````

````
为 Nous Portal 启动 Hermes 代理
  收听：http://127.0.0.1:8645/v1
  转发至：（根据您的订阅请求进行解析）
  在客户端中使用任何不记名令牌 - 代理会附加您的真实凭证。
````

让它在前台运行。使用 `tmux`、`nohup` 或 systemd
如果您希望它在注销后仍然存在，请使用单位。

### 3. 将您的应用程序指向它

任何与 OpenAI 兼容的应用程序配置都采用相同的三元组：

````
基本网址：http://127.0.0.1:8645/v1
API 密钥：任何内容（例如“sk-unused”）
型号：Hermes-4-70B#或Hermes-4.3-36B、Hermes-4-405B
````

代理会忽略应用程序中的“Authorization”标头并附加
您对上游请求的真实 Portal 凭据。发生刷新
当持票人即将到期时自动。

## 可用的提供商

````bash
爱马仕代理提供商
````

目前已发布：“nous”（Nous Portal）和“xai”（xAI / Grok）。更多
可以通过实现 `UpstreamAdapter` 添加 OAuth 提供程序
接口位于 `hermes_cli/proxy/adapters/` 中。

## 检查状态

````bash
爱马仕代理状态
````

````
Hermes 代理上游适配器

  [nous ] Nous Portal — 准备就绪（不记名到期日期为 2026-05-15T06:43:21Z）
````

如果您看到“未登录”，请运行“hermes Portal”。如果你看到
“凭据需要注意”，您的刷新令牌已被撤销（罕见 -
如果您从门户网站 Web UI 注销，则会发生这种情况） — 只需重新运行
“爱马仕门户”。

## 允许的路径

代理仅转发上游实际服务的路径。为了诺斯
传送门：

|路径|目的|
|------|---------|
| `/v1/chat/completions` |聊天完成情况（流式传输 + 非流式传输）|
| `/v1/completions` |旧版文本补全 |
| `/v1/embeddings` |嵌入 |
| `/v1/models` |型号列表 |

其他路径（`/v1/images/ Generations`、`/v1/audio/speech`等）返回
404，有一个明确的错误指向允许的路径。这使人迷失
客户端向上游泄露奇怪的请求。

## 配置 OpenViking 使用 Portal

[OpenViking](https://github.com/volcengine/OpenViking) 是一个上下文
需要 LLM 提供商为其 VLM（视觉/语言模型
用于提取记忆）和嵌入模型。通过代理，您可以
将其“vlm.api_base”指向您的本地代理：

编辑`~/.openviking/ov.conf`：

```json
{
  “vlm”：{
    “提供者”：“openai”，
    “型号”：“Hermes-4-70B”，
    "api_base": "http://127.0.0.1:8645/v1",
    “api_key”：“未使用的代理附件真实信用”
  }
}
````

然后在终端中与“openviking-server”一起启动代理：

````bash
# 1 号航站楼
Hermes代理启动

# 2 号航站楼
openviking-服务器
````

OpenViking 的 VLM 呼叫现在通过您的门户订阅进行。的
嵌入模型端仍然需要自己的提供者——Portal确实提供服务
`/v1/embeddings` 但模型选择取决于您的层
支持；检查“portal.nousresearch.com/models”。

## 配置 Karakeep（或任何书签/摘要应用程序）

[Karakeep](https://karakeep.app/) 采用与 OpenAI 兼容的 API
书签摘要。在其配置中：

````bash
#卡拉吉普.env
OPENAI_API_BASE_URL=http://127.0.0.1:8645/v1
OPENAI_API_KEY=任何非空字符串
INFERENCE_TEXT_MODEL=Hermes-4-70B
````

相同的模式适用于 Open WebUI、LobeChat、NextChat 或任何其他
OpenAI 兼容客户端。

## 在 LAN 上公开

默认情况下，代理绑定“127.0.0.1”（仅限本地主机）。为了让其他
您网络上的机器使用它：

````bash
Hermes代理启动--主机0.0.0.0--端口8645
````

⚠ **请注意：** 您网络上的任何人现在都可以使用您的门户
订阅。代理没有自己的授权——它接受任何持有者。
如果暴露，请使用防火墙、VPN 或具有适当身份验证的反向代理
这超出了您信任的网络。

## 速率限制

您的门户层的 RPM/TPM 限制适用于整个代理。的
代理不会扇出或池化——它是一个单一的承载者，包含你的全部信息
认购配额。监控使用情况
[portal.nousresearch.com](https://portal.nousresearch.com)。

## 架构

代理故意最小化。根据要求：

1. 从您的应用接收“POST /v1/chat/completions”
2.查找适配器当前的凭证（如果过期则刷新）
3. 使用“Authorization: Bearer <minted-key>”逐字转发请求正文
4. 将响应原样流式传输回来（保留 SSE）

没有转变。不记录请求主体。无代理循环。的
代理是一种凭证附加传递。

## 未来：更多 OAuth 提供商

适配器系统是可插拔的。添加新的提供商（例如
HuggingFace、GitHub Copilot 的聊天端点、Anthropic 通过 OAuth）
需要实现 `UpstreamAdapter`
`hermes_cli/proxy/adapters/<provider>.py` 并将其注册到
`适配器/__init__.py`。不兼容 OpenAI 的提供商
协议级别（例如 Anthropic Messages API）需要一个
变换层，超出了当前形状的范围。