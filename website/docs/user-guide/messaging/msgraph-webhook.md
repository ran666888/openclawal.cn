---
sidebar_position: 23
title: "Microsoft Graph Webhook Listener"
description: "Receive Microsoft Graph change notifications (meetings, calendar, chat, etc.) in OpenClaw"
---
# Microsoft Graph Webhook 监听器

`msgraph_webhook` 网关平台是一个入站事件监听器。这就是 OpenClaw 从 Microsoft Graph 接收**更改通知**的方式 - “Teams 会议结束”、“此聊天中收到一条新消息”、“此日历活动已更新”。与“teams”平台（用户输入的聊天机器人）不同——这是 M365 告诉 OpenClaw 发生了什么事，而不是一个人。

目前，主要的使用者是 Teams 会议摘要管道：Graph 会在会议生成记录时发出通知，管道会获取记录，然后 OpenClaw 将摘要发布回 Teams。其他图资源（`/chats/.../messages`、`/users/.../events`）使用相同的侦听器 - 管道消费者使用自己的 PR 登陆。

## 先决条件

- Microsoft Graph 应用程序凭据 — [注册 Microsoft Graph 应用程序](/guides/microsoft-graph-app-registration)
- Microsoft Graph 可以访问的 **公共 HTTPS URL**（Graph 不调用专用终结点）。开发隧道用于测试；生产需要具有有效证书的真实域名。
- 用作“clientState”值的强共享秘密。使用“openssl rand -hex 32”生成并将其作为“MSGRAPH_WEBHOOK_CLIENT_STATE”放入“~/.hermes/.env”中。

## 快速入门

最小`~/.hermes/config.yaml`：

````yaml
平台：
  msgraph_webhook：
    启用：真
    额外：
      主机：127.0.0.1
      端口：8646
      client_state：“替换为强秘密”
      接受的资源：
        - “通讯/在线会议”
````

或者通过 `~/.hermes/.env` 中的环境变量（启动时自动合并）：

````bash
MSGRAPH_WEBHOOK_ENABLED=true
MSGRAPH_WEBHOOK_PORT=8646
MSGRAPH_WEBHOOK_CLIENT_STATE=<使用 openssl-rand-hex-32 生成>
MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=通讯/onlineMeetings
````

注意：绑定主机是从 `config.yaml` 中的 `extra.host` 读取的（参见上面的示例）；没有“MSGRAPH_WEBHOOK_HOST”环境变量覆盖。

启动网关：`hermes gateway run`。听者暴露：

- `POST /msgraph/webhook` — 来自 Graph 的更改通知
- `GET /msgraph/webhook?validationToken=...` — 图订阅验证握手
- `GET /health` — 带有接受/重复计数器的就绪探针

公开公开侦听器（反向代理、开发隧道、入口）。您的 Graph 订阅通知 URL 是您的公共 HTTPS 源，后跟“/msgraph/webhook”：

````
https://ops.example.com/msgraph/webhook
````

## 配置

所有设置都位于“platforms.msgraph_webhook.extra”下：

|设置|默认 |描述 |
|---------|---------|-------------|
| `主机` | `0.0.0.0` | HTTP 侦听器的绑定地址。非环回绑定需要“allowed_source_cidrs”； Loopback (`127.0.0.1` / `::1`) 是最简单的开发隧道/反向代理设置。 |
| `端口` | `8646` |绑定端口。 |
| `webhook_path` | `/msgraph/webhook` |图形 POST 到的 URL 路径。 |
| `健康路径` | `/健康` |准备就绪终点。 |
| `客户端状态` | — |共享秘密图会在每个通知中回显。与“hmac.compare_digest”相比——使用“openssl rand -hex 32”生成。 |
| `accepted_resources` | `[]`（接受全部）|图形资源路径/模式的白名单。尾随“*”充当前缀匹配。允许前导“/”。示例：`["communications/onlineMeetings", "chats/*/messages"]`。 |
| `max_seen_receipts` | `5000` |通知 ID 的重复数据删除缓存大小。当达到上限时，最旧的条目将被驱逐。 |
| `allowed_source_cidrs` | `[]` |对于非环回绑定是必需的。仅当侦听器绑定到环回并由本地隧道/反向代理前置时，才保留为空。 |

大多数设置还有一个等效的环境变量 (`MSGRAPH_WEBHOOK_*`)，它会在网关启动时合并到配置中（例外是 `host`，它仅用于配置 - 请参阅上面的注释） - 请参阅[环境变量参考](/reference/environment-variables#microsoft-graph-teams-meetings)。

## 安全加固

### clientState 是主要身份验证检查

每个图形通知都包含您注册的订阅的“clientState”字符串。侦听器使用定时安全比较拒绝任何“clientState”不匹配的通知。这是微软记录的机制——将值视为强大的共享秘密。

如果未设置“client_state”，侦听器将拒绝启动。

### 源 IP 许可名单（生产部署）

对于生产，将侦听器限制为 Microsoft 发布的 Graph Webhook 源 IP 范围。 Microsoft 在 [Office 365 IP 地址和 URL Web 服务](https://learn.microsoft.com/en-us/microsoft-365/enterprise/urls-and-ip-address-ranges) 下记录了出口范围。将它们配置为：

````yaml
平台：
  msgraph_webhook：
    启用：真
    额外：
      主机：0.0.0.0
      客户端状态：“...”
      allowed_source_cidrs：
        - “52.96.0.0/14”
        - “52.104.0.0/14”
        # ...添加当前 Microsoft 365“Common”+“Teams”类别出口范围
````

或者作为环境变量：

````bash
MSGRAPH_WEBHOOK_ALLOWED_SOURCE_CIDRS="52.96.0.0/14,52.104.0.0/14"
````

启动时会拒绝绑定非环回主机，例如“0.0.0.0”、“::”或没有“allowed_source_cidrs”的 LAN IP。如果您在同一台计算机上使用开发隧道或反向代理，请将 OpenClaw 绑定到 `127.0.0.1` 或 `::1` 并将允许列表保留为空。无效的 CIDR 字符串会记录警告并被忽略。 **每季度查看一次 Microsoft IP 列表** — 它会发生变化。

### HTTPS 终止

侦听器使用纯 HTTP。在反向代理（Caddy、Nginx、Cloudflare Tunnel、AWS ALB）处终止 TLS，并通过本地网络代理到侦听器。 Graph 拒绝传送到非 HTTPS 端点，因此未加密的流量无法从 Graph 本身到达您。

### 响应卫生

成功后，监听器返回“202 Accepted”，主体为空——内部计数器不参与线路响应。操作员可以通过“/health”观察计数，该计数由与 Webhook 路径相同的源 IP 规则保护。

状态码表：

|结果|状态 |
|---------|--------|
|已接受或已删除重复的通知 | 202 | 202
|验证握手（使用“validationToken”获取）| 200（与令牌相呼应）|
|批次中的每个项目都失败了 clientState | 403 | 403
| JSON 格式错误/缺少“值”数组/未知资源 | 400 |
|源 IP 不在白名单中 | 403 | 403
|没有 `validationToken` 的裸 GET | 400 |

## 故障排除

|问题 |检查什么 |
|--------|----------------|
|图形订阅验证失败 |公共 URL 可访问，“/msgraph/webhook”路径匹配，使用“validationToken”的 GET 在 10 秒内将令牌逐字回显为“text/plain”。 |
|通知 POST 但没有任何摄取 | `client_state` 与您注册订阅的内容相匹配。如果值发生变化，请重新运行“openssl rand -hex 32”并创建新的订阅。检查“accepted_resources”是否包含图表正在发送的资源路径。 |
|每个通知 403 | `clientState` 不匹配（伪造，或使用不同值注册的订阅）。使用 `hermes team-pipeline subscribe --client-state "$MSGRAPH_WEBHOOK_CLIENT_STATE" ...` 重新创建订阅（随管道运行时 PR 一起提供）。 |
|侦听器拒绝在“0.0.0.0”上启动 |将“allowed_source_cidrs”设置为 Microsoft 当前的 webhook 出口范围，或将 OpenClaw 绑定到隧道或反向代理后面的“127.0.0.1”/“::1”。 |
|监听器启动但 `curl http://localhost:8646/health` 挂起 |端口绑定冲突。检查 `ss -tlnp \| grep 8646` 并根据需要更改`port:`。 |
|来自 Microsoft 的 Real Graph 请求收到 403 错误 |源 IP 允许列表太窄。扩大列表以包括当前的 Microsoft 出口范围。如果您仍在验证隧道路径，请将 OpenClaw 绑定到环回并让隧道处理公开暴露。 |

## 相关文档

- [注册 Microsoft Graph 应用程序](/guides/microsoft-graph-app-registration) — Azure 应用程序注册先决条件
- [环境变量 → Microsoft Graph](/reference/environment-variables#microsoft-graph-teams-meetings) — 完整环境变量列表
- [Microsoft Teams 机器人设置](/user-guide/messaging/teams) — 允许用户在 Teams 中与 OpenClaw 聊天的不同平台