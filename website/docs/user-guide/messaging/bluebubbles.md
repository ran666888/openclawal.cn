# 蓝色泡泡 (iMessage)

通过 [BlueBubbles](https://bluebubbles.app/) 将 OpenClaw 连接到 Apple iMessage — 一个免费的开源 macOS 服务器，可将 iMessage 桥接到任何设备。

## 先决条件

- 运行 [BlueBubbles 服务器](https://bluebubbles.app/) 的 **Mac**（始终开启）
- Apple ID 登录到该 Mac 上的 Messages.app
- BlueBubbles Server v1.0.0+（webhooks 需要此版本）
- OpenClaw 和 BlueBubbles 服务器之间的网络连接

## 设置

### 1. 安装 BlueBubbles 服务器

从 [bluebubbles.app](https://bluebubbles.app/) 下载并安装。完成设置向导 - 使用您的 Apple ID 登录并配置连接方法（本地网络、Ngrok、Cloudflare 或动态 DNS）。

### 2. 获取您的服务器 URL 和密码

在 BlueBubbles 服务器 → **设置 → API** 中，注意：
- **服务器 URL**（例如“http://192.168.1.10:1234”）
- **服务器密码**

### 3.配置OpenClaw

运行设置向导：

````bash
Hermes网关设置
````

选择 **BlueBubbles (iMessage)** 并输入您的服务器 URL 和密码。

或者直接在`~/.hermes/.env`中设置环境变量：

````bash
BLUEBUBBLES_SERVER_URL=http://192.168.1.10:1234
BLUEBUBBLES_PASSWORD=您的服务器密码
````

#### 可选：需要在群聊中提及

默认情况下，OpenClaw 会响应每条授权的 BlueBubbles/iMessage DM 或群组消息。要选择加入群聊，请启用提及门控：

````yaml
平台：
  蓝色泡泡：
    启用：真
    额外：
      要求提及：true
````

使用“require_mention: true”，私信仍然正常工作，但群聊消息将被忽略，除非它们与提及模式匹配。如果您不配置自定义模式，OpenClaw 将使用“OpenClaw”和“@OpenClaw agent”变体的保守默认值。

对于自定义代理名称，设置正则表达式模式：

````yaml
平台：
  蓝色泡泡：
    额外：
      要求提及：true
      提及模式：
        - '(?<![\w@])@?amos\b[,:\-]?'
````

### 4. 授权用户

选择一种方法：

**DM 配对（推荐）：**
当有人向您的 iMessage 发送消息时，OpenClaw 会自动向他们发送配对码。批准它：
````bash
爱马仕 (hermes) 配对批准 bluebubbles <代码>
````
使用“hermes 配对列表”查看待处理的代码和已批准的用户。

**预授权特定用户**（在`~/.hermes/.env`中）：
````bash
BLUEBUBBLES_ALLOWED_USERS=user@icloud.com,+15551234567
````

**开放访问**（在`~/.hermes/.env`中）：
````bash
BLUEBUBBLES_ALLOW_ALL_USERS=true
````

### 5.启动网关

````bash
爱马仕网关运行
````

OpenClaw 将连接到您的 BlueBubbles 服务器，注册 Webhook，并开始侦听 iMessage 消息。

## 它是如何工作的

````
iMessage → Messages.app → BlueBubbles 服务器 → Webhook → Hermes
Hermes → BlueBubbles REST API → Messages.app → iMessage
````

- **入站：** 当新消息到达时，BlueBubbles 会将 Webhook 事件发送到本地侦听器。无需轮询——即时交付。
- **出站：** OpenClaw 通过 BlueBubbles REST API 发送消息。
- **媒体：** 双向支持图像、语音消息、视频和文档。入站附件被下载并缓存在本地以供代理处理。

## 环境变量

|变量|必填|默认 |描述 |
|----------|----------|---------|------------|
| `BLUEBUBBLES_SERVER_URL` |是的 | — | BlueBubbles 服务器 URL |
| `BLUEBUBBLES_PASSWORD` |是的 | — |服务器密码 |
| `BLUEBUBBLES_WEBHOOK_HOST` |没有 | `127.0.0.1` | Webhook监听绑定地址 |
| `BLUEBUBBLES_WEBHOOK_PORT` |没有 | `8645` | Webhook 监听端口 |
| `BLUEBUBBLES_WEBHOOK_PATH` |没有 | `/bluebubbles-webhook` | Webhook URL 路径 |
| `BLUEBUBBLES_HOME_CHANNEL` |没有 | — |用于 cron 交付的电话/电子邮件 |
| `BLUEBUBBLES_ALLOWED_USERS` |没有 | — |以逗号分隔的授权用户 |
| `BLUEBUBBLES_ALLOW_ALL_USERS` |没有 | `假` |允许所有用户 |
| `BLUEBUBBLES_REQUIRE_MENTION` |没有 | `假` |在群聊中回复之前需要提及模式 |
| `BLUEBUBBLES_提及模式` |没有 |爱马仕唤醒词|用于组提及匹配的 JSON 数组、换行符分隔或逗号分隔的正则表达式模式 |

自动将消息标记为已读由“~/.hermes/config.yaml”中“platforms.bluebubbles.extra”下的“send_read_receipts”键控制（默认值：“true”）。没有对应的环境变量。

## 特点

### 短信
发送和接收 iMessage。 Markdown 会自动剥离以实现干净的纯文本交付。

### 富媒体
- **图像：** 照片本身出现在 iMessage 对话中
- **语音消息：** 作为 iMessage 语音消息发送的音频文件
- **视频：** 视频附件
- **文档：** 作为 iMessage 附件发送的文件

### 回击反应
喜欢、喜欢、不喜欢、笑、强调和质疑反应。需要 BlueBubbles [私有 API 帮助程序](https://docs.bluebubbles.app/helper-bundle/installation)。

### 键入指示器
当代理处理时，在 iMessage 对话中显示“正在键入...”。需要私有 API。

### 已读回执
处理后自动将消息标记为已读。需要私有 API。

### 聊天寻址
您可以通过电子邮件或电话号码进行聊天 - OpenClaw 会自动将它们解析为 BlueBubbles 聊天 GUID。无需使用原始 GUID 格式。

## 私有API

某些功能需要 BlueBubbles [私有 API 帮助程序](https://docs.bluebubbles.app/helper-bundle/installation)：
- 回击反应
- 打字指示器
- 阅读收据
- 按地址创建新聊天

如果没有 Private API，基本的短信和媒体仍然可以工作。

## 故障排除

###“无法到达服务器”
- 验证服务器 URL 是否正确且 Mac 已开启
- 检查 BlueBubbles 服务器是否正在运行
- 确保网络连接（防火墙、端口转发）

### 消息未到达
- 检查 Webhook 是否已在 BlueBubbles Server → 设置 → API → Webhooks 中注册
- 验证可从 Mac 访问 Webhook URL
- 检查“hermes 日志网关”是否存在 webhook 错误（或“hermes 日志 -f”以实时跟踪）

### “私有 API 帮助程序未连接”
- 安装私有 API 帮助程序：[docs.bluebubbles.app](https://docs.bluebubbles.app/helper-bundle/installation)
- 基本消息传递无需它即可工作 - 只有反应、打字和已读回执需要它