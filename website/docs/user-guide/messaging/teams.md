---
sidebar_position: 5
title: "Microsoft Teams"
description: "将 OpenClaw 设置为 Microsoft Teams 机器人"
---
# 微软团队设置

将 OpenClaw 作为机器人连接到 Microsoft Teams。与 Slack 的套接字模式不同，Teams 通过调用 **公共 HTTPS webhook** 来传递消息，因此您的实例需要一个可公开访问的端点 - 开发隧道（本地开发）或真实域（生产）。

需要 Microsoft Graph 事件的会议摘要而不是正常的机器人对话吗？使用专用设置页面：[Teams 会议](/user-guide/messaging/teams-meetings)。

> 运行“hermes gateway setup”并选择 **Microsoft Teams** 进行指导演练。

## 机器人如何响应

|背景 |行为 |
|---------|----------|
| **个人聊天 (DM)** |机器人回复每条消息。无需@提及。 |
| **群聊** |机器人仅在@提及时做出响应。 |
| **频道** |机器人仅在@提及时做出响应。 |

Teams 将 @mentions 作为带有“<at>BotName</at>”标签的常规消息传递，OpenClaw 在处理之前会自动删除这些标签。

---

对于源或本地安装，请包含 Teams extra，以便捆绑的适配器可以
导入 Microsoft Teams SDK：

````bash
uv 同步——额外的团队
# 或者，对于可编辑安装：
uv pip install -e ".[团队]"
````

## 步骤 1：安装 Teams CLI

`@microsoft/teams.cli` 可自动注册机器人 - 无需 Azure 门户。

````bash
npm install -g @microsoft/teams.cli@preview
团队登录
````

要验证您的登录并查找您自己的 AAD 对象 ID（“TEAMS_ALLOWED_USERS”需要）：

````bash
团队状态--verbose
````

---

## 步骤 2：公开 Webhook 端口

团队无法将消息传递到“localhost”。对于本地开发，请使用任何隧道工具来获取公共 HTTPS URL。默认端口是“3978”——如果需要，可以使用“TEAMS_PORT”进行更改。

````bash
# 开发隧道（微软）
devtunnel 创建 Hermes-bot --allow-anonymous
devtunnel port create hermes-bot -p 3978 --protocol https # 如果更改，请将 3978 替换为 TEAMS_PORT
devtunnel 主机 Hermes-bot

# 恩格罗克
ngrok http 3978 # 如果更改，请将 3978 替换为 TEAMS_PORT

# 云耀
cloudflaredtunnel --url http://localhost:3978 # 如果更改，请将 3978 替换为 TEAMS_PORT
````

从输出中复制“https://” URL — 您将在下一步中使用它。开发时让隧道保持运行。

对于生产，请将机器人的端点指向服务器的公共域（请参阅[生产部署](#生产部署)）。

---

## 第 3 步：创建机器人

````bash
团队应用程序创建\
  --名称“赫尔墨斯”\
  --endpoint“https://<your-tunnel-url>/api/messages”
````

CLI 会输出您的“CLIENT_ID”、“CLIENT_SECRET”和“TENANT_ID”，以及第 6 步的安装链接。保存客户端密钥 - 它不会再次显示。

---

## 第四步：配置环境变量

添加到`~/.hermes/.env`：

````bash
# 必填
TEAMS_CLIENT_ID=<您的客户 ID>
TEAMS_CLIENT_SECRET=<您的客户秘密>
TEAMS_TENANT_ID=<您的租户 ID>

# 限制特定用户的访问（推荐）
# 使用来自 `teams status --verbose` 的 AAD 对象 ID
TEAMS_ALLOWED_USERS=<您的 aad-object-id>
````

---

## 步骤 5：启动网关

````bash
HERMES_UID=$(id -u) HERMES_GID=$(id -g) docker compose up -d 网关
````

这将启动网关。默认 Webhook 端口为“3978”（用“TEAMS_PORT”覆盖）。检查它是否正在运行：

````bash
卷曲 http://localhost:3978/health # 应该返回： ok
docker 日志 -f Hermes
````

寻找：
````
[teams] Webhook 服务器监听 0.0.0.0:3978/api/messages
````

---

## 步骤 6：在 Teams 中安装应用程序

````bash
团队应用程序获取 <teamsAppId> --install-link
````

在浏览器中打开打印的链接 - 它直接在 Teams 客户端中打开。安装后，向您的机器人发送直接消息 - 它已准备就绪。

---

## 配置参考

### 环境变量

|变量|描述 |
|----------|-------------|
| `TEAMS_CLIENT_ID` | Azure AD 应用程序（客户端）ID |
| `TEAMS_CLIENT_SECRET` | Azure AD 客户端密钥 |
| `TEAMS_TENANT_ID` | Azure AD 租户 ID |
| `TEAMS_ALLOWED_USERS` |允许使用机器人的以逗号分隔的 AAD 对象 ID |
| `TEAMS_ALLOW_ALL_USERS` |设置“true”以跳过白名单并允许任何人 |
| `TEAMS_HOME_CHANNEL` |用于 cron/主动消息传递的会话 ID |
| `TEAMS_HOME_CHANNEL_NAME` |家庭频道的显示名称 |
| `TEAMS_PORT` | Webhook 端口（默认：`3978`）|

### 配置.yaml

或者，通过“~/.hermes/config.yaml”进行配置：

````yaml
平台：
  团队：
    启用：真
    额外：
      client_id: “您的客户 ID”
      client_secret: “你的秘密”
      tenant_id：“您的租户id”
      端口：3978
````

---

## 特点

### 互动批准卡

当代理需要运行潜在危险的命令时，它会发送带有四个按钮的自适应卡，而不是要求您输入“/approve”：

- **允许一次** — 批准此特定命令
- **允许会话** — 批准此模式用于会话的其余部分
- **始终允许** — 永久批准此模式
- **拒绝** — 拒绝命令

单击按钮即可解决内联批准问题，并用决策替换卡片。

### 会议摘要交付（团队会议管道）

启用 [Teams 会议管道插件](/user-guide/messaging/msgraph-webhook) 后，此适配器还可以处理会议摘要的出站传送 - 一个 Teams 集成界面，而不是两个。总结会议记录后，作者会将摘要发布到您选择的 Teams 目标中。

管道摘要交付在机器人配置旁边的“teams”平台条目下配置：

````yaml
平台：
  团队：
    启用：真
    额外：
      # 现有机器人配置（client_id、client_secret、tenant_id、端口）...

      # 会议摘要传递（仅在启用teams_pipeline插件时使用）
      Delivery_mode: "graph" # 或 "incoming_webhook"
      # 对于 Delivery_mode: graph — 选择以下之一：
      chat_id: "19:meeting_..." # 发布到 Teams 聊天中
      # team_id: "..." # 或发布到频道
      # 频道 ID：“...”
      # access_token: "..." # 可选;回退到 MSGRAPH_* 应用程序凭据
      # 对于 Delivery_mode：传入_webhook：
      #传入_webhook_url：“https://outlook.office.com/webhook/...”
````

|模式|使用时 |权衡|
|------|----------|------------|
| `incoming_webhook` |使用 Teams 生成的静态 URL 简单地“将摘要发布到此频道”。 |没有回复线程，没有反应，显示为 webhook 的配置身份。 |
| `图` |通过 Microsoft Graph 以机器人身份发布线程式频道帖子或 1:1/群聊帖子。 |需要具有“ChannelMessage.Send”（频道）或“Chat.ReadWrite.All”（聊天）应用程序权限的 [Graph 应用注册](/guides/microsoft-graph-app-registration)。 |

如果“teams_pipeline”插件未启用，这些设置是惰性的——它们仅在管道运行时绑定到 Graph Webhook 入口时才连接。

---

## 生产部署

对于永久服务器，请跳过 devtunnel 并使用服务器的公共 HTTPS 端点注册您的机器人：

````bash
团队应用程序创建\
  --名称“赫尔墨斯”\
  --endpoint“https://your-domain.com/api/messages”
````

如果您已经创建了机器人并且只需要更新端点：

````bash
团队应用程序更新 --id <teamsAppId> --endpoint "https://your-domain.com/api/messages"
````

确保您配置的端口（“TEAMS_PORT”，默认“3978”）可从 Internet 访问，并且您的 TLS 证书有效 - Teams 拒绝自签名证书。

---

## 故障排除

|问题 |解决方案 |
|---------|----------|
| “health”端点有效，但机器人没有响应 |检查您的隧道是否仍在运行，并且机器人的消息传递端点是否与隧道 URL 匹配 |
|日志中的“KeyError: 'teams'” |重新启动容器 - 这在当前版本中已修复 |
|机器人响应身份验证错误 |验证“TEAMS_CLIENT_ID”、“TEAMS_CLIENT_SECRET”和“TEAMS_TENANT_ID”均设置正确 |
| `未配置推理提供程序` |检查`AN​​THROPIC_API_KEY`（或其他提供者密钥）是否在`~/.hermes/.env`中设置。
|机器人收到消息但忽略它们 |您的 AAD 对象 ID 可能不在“TEAMS_ALLOWED_USERS”中。运行“teams status --verbose”来查找它 |
|重新启动时隧道 URL 发生变化 |如果您使用命名隧道（“devtunnel create hermes-bot”），则 devtunnel URL 是持久的。除非您有付费计划，否则 ngrok 和 cloudflared 每次运行都会生成一个新的 URL — 当机器人端点发生变化时，使用“团队应用程序更新”更新机器人端点 |
| Teams 显示“此机器人没有响应” | Webhook 返回错误。检查 `docker log hermes` 的回溯 |
|日志中的“[团队] 连接失败”| SDK 验证失败。仔细检查您的凭据以及租户 ID 是否与您在“团队登录”中使用的帐户匹配 |

---

## 安全

:::警告
**始终使用授权用户的 AAD 对象 ID 设置“TEAMS_ALLOWED_USERS”**。如果没有这个，任何可以找到或安装您的机器人的人都可以与其交互。

将“TEAMS_CLIENT_SECRET”视为密码 - 通过 Azure 门户或 Teams CLI 定期轮换它。
:::

- 将凭证存储在“~/.hermes/.env”中，权限为“600”（“chmod 600 ~/.hermes/.env”）
- 机器人仅接受来自“TEAMS_ALLOWED_USERS”中用户的消息；未经授权的消息会被悄悄丢弃
- 您的公共端点 (`/api/messages`) 由 Teams Bot 框架进行身份验证 - 没有有效 JWT 的请求将被拒绝

## 相关文档

- [团队会议](/user-guide/messaging/teams-meetings)
- [操作团队会议管道](/guides/operate-teams-meeting-pipeline)