---
sidebar_position: 8
sidebar_label: "SMS (Twilio)"
title: "SMS (Twilio)"
description: "通过 Twilio 将 OpenClaw 设置为短信聊天机器人"
---
# 短信设置 (Twilio)

OpenClaw 通过 [Twilio](https://www.twilio.com/) API 连接到 SMS。人们向您的 Twilio 电话号码发送短信并得到人工智能回复——与 Telegram 或 Discord 相同的对话体验，但通过标准短信。

:::info 共享凭证
SMS 网关与可选的[电话技能](/reference/skills-catalog) 共享凭据。如果您已将 Twilio 设置为语音通话或一次性短信，则网关可使用相同的“TWILIO_ACCOUNT_SID”、“TWILIO_AUTH_TOKEN”和“TWILIO_PHONE_NUMBER”。
:::

---

## 先决条件

- **Twilio 帐户** — [在 twilio.com 注册](https://www.twilio.com/try-twilio)（提供免费试用）
- **具有 SMS 功能的 Twilio 电话号码**
- **可公开访问的服务器** — 当 SMS 到达时，Twilio 会向您的服务器发送 Webhooks
- **aiohttp** — `pip install 'hermes-agent[sms]'`

---

## 第 1 步：获取您的 Twilio 凭证

1. 进入[Twilio控制台](https://console.twilio.com/)
2. 从仪表板复制您的 **帐户 SID** 和 **身份验证令牌**
3. 转至 **电话号码 → 管理 → 活动号码** — 以 E.164 格式记下您的电话号码（例如“+15551234567”）

---

## 第二步：配置 OpenClaw

### 交互式设置（推荐）

````bash
Hermes网关设置
````

从平台列表中选择 **SMS (Twilio)**。该向导将提示您输入凭据。

### 手动设置

添加到`~/.hermes/.env`：

````bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567

# 安全性：限制特定电话号码（推荐）
SMS_ALLOWED_USERS=+15559876543,+15551112222

# 可选：设置 cron 作业交付的主通道
SMS_HOME_CHANNEL=+15559876543
````

---

## 步骤 3：配置 Twilio Webhook

Twilio 需要知道将传入消息发送到哪里。在 [Twilio 控制台](https://console.twilio.com/) 中：

1. 转至 **电话号码 → 管理 → 活跃号码**
2. 单击您的电话号码
3. 在 **消息 → 有消息**下，设置：
   - **Webhook**：`https://your-server:8080/webhooks/twilio`
   - **HTTP 方法**：`POST`

:::tip 暴露你的 Webhook
如果您在本地运行 OpenClaw，请使用隧道来公开 Webhook：

````bash
# 使用 cloudflared
cloudflared 隧道 --url http://localhost:8080

# 使用 ngrok
恩格洛克 http 8080
````

将生成的公共 URL 设置为您的 Twilio Webhook。
:::

**将 `SMS_WEBHOOK_URL` 设置为您在 Twilio 中配置的相同 URL。** 这是 Twilio 签名验证所必需的 — 如果没有它，适配器将拒绝启动：

````bash
# 必须与 Twilio 控制台中的 webhook URL 匹配
SMS_WEBHOOK_URL=https://your-server:8080/webhooks/twilio
````

Webhook 端口默认为“8080”。覆盖：

````bash
SMS_WEBHOOK_PORT=3000
````

---

## 步骤 4：启动网关

````bash
爱马仕网关
````

你应该看到：

````
[sms] Twilio webhook 服务器监听 127.0.0.1:8080，来自：+1555***4567
````

如果您看到“拒绝启动：需要 SMS_WEBHOOK_URL”，请将“SMS_WEBHOOK_URL”设置为在 Twilio 控制台中配置的公共 URL（请参阅步骤 3）。

发短信给您的 Twilio 号码 — OpenClaw 将通过短信回复。

---

## 环境变量

|变量|必填|描述 |
|----------|----------|------------|
| `TWILIO_ACCOUNT_SID` |是的 | Twilio 帐户 SID（以“AC”开头）|
| `TWILIO_AUTH_TOKEN` |是的 | Twilio Auth Token（也用于 webhook 签名验证）|
| `TWILIO_PHONE_NUMBER` |是的 |您的 Twilio 电话号码（E.164 格式）|
| `SMS_WEBHOOK_URL` |是的 | Twilio 签名验证的公共 URL — 必须与 Twilio 控制台中的 Webhook URL 匹配 |
| `SMS_WEBHOOK_PORT` |没有 | Webhook 侦听器端口（默认值：`8080`）|
| `SMS_WEBHOOK_HOST` |没有 | Webhook 绑定地址（默认：`127.0.0.1`）|
| `SMS_INSECURE_NO_SIGNATURE` |没有 |设置为“true”以禁用签名验证（仅限本地开发 - **不适用于生产**）|
| `SMS_ALLOWED_USERS` |没有 |允许聊天的逗号分隔 E.164 电话号码 |
| `SMS_ALLOW_ALL_USERS` |没有 |设置为“true”以允许任何人（不推荐） |
| `SMS_HOME_CHANNEL` |没有 | cron 作业/通知传递的电话号码 |
| `SMS_HOME_CHANNEL_NAME` |没有 |家庭频道的显示名称（默认：“Home”）|

---

## SMS 特定行为

- **仅限纯文本** — Markdown 会自动删除，因为 SMS 将其呈现为文字字符
- **1600 个字符限制** — 较长的响应在自然边界（换行符，然后是空格）处分成多条消息
- **回声预防** — 来自您自己的 Twilio 号码的消息将被忽略以防止循环
- **电话号码编辑** — 出于隐私考虑，电话号码在日志中进行了编辑

---

## 安全

### Webhook 签名验证

OpenClaw 通过验证“X-Twilio-Signature”标头 (HMAC-SHA1) 来验证入站 Webhook 是否真正源自 Twilio。这可以防止攻击者注入伪造的消息。

**`SMS_WEBHOOK_URL` 是必需的。** 将其设置为在 Twilio 控制台中配置的公共 URL。如果没有它，适配器将拒绝启动。

对于没有公共 URL 的本地开发，您可以禁用验证：

````bash
# 仅限本地开发 - 不适用于生产
SMS_INSECURE_NO_SIGNATURE=true
````

### 用户许可名单

**网关默认拒绝所有用户。** 配置白名单：

````bash
# 推荐：限制特定电话号码
SMS_ALLOWED_USERS=+15559876543,+15551112222

# 或允许全部（不推荐用于具有终端访问权限的机器人）
SMS_ALLOW_ALL_USERS=true
````

:::警告
SMS 没有内置加密。除非您了解安全隐患，否则请勿使用 SMS 进行敏感操作。对于敏感用例，首选 Signal 或 Telegram。
:::

---

## 故障排除

### 消息未到达

1. 检查您的 Twilio webhook URL 是否正确且可公开访问
2.验证`TWILIO_ACCOUNT_SID`和`TWILIO_AUTH_TOKEN`是否正确
3. 检查 Twilio 控制台 → **监视器 → 日志 → 消息传送** 是否有传送错误
4. 确保您的电话号码在“SMS_ALLOWED_USERS”（或“SMS_ALLOW_ALL_USERS=true”）中

### 回复未发送

1. 检查`TWILIO_PHONE_NUMBER`设置是否正确（E.164格式带`+`）
2. 验证您的 Twilio 帐户有支持短信的号码
3. 检查 OpenClaw 网关日志中是否有 Twilio API 错误

### Webhook 端口冲突

如果端口 8080 已被使用，请更改它：

````bash
SMS_WEBHOOK_PORT=3001
````

在 Twilio Console 中更新 Webhook URL 以进行匹配。