# QQ机器人

通过 **官方 QQ Bot API (v2)** 将 OpenClaw 连接到 QQ — 支持私人 (C2C)、群组@提及、公会和带语音转录的直接消息。

## 概述

QQ Bot 适配器使用【QQ Bot 官方 API】(https://bot.q.qq.com/wiki/develop/api-v2/) 来：

- 通过与QQ网关的持久**WebSocket**连接接收消息
- 通过 **REST API** 发送文本和 Markdown 回复
- 下载和处理图像、语音消息和文件附件
- 使用腾讯内置的 ASR 或可配置的 STT 提供商转录语音消息

## 先决条件

1. **QQ机器人申请** — 在[q.qq.com](https://q.qq.com)注册：
   - 创建一个新应用程序并记下您的**应用程序 ID** 和 **应用程序密钥**
   - 启用所需的意图：C2C消息、群组@消息、公会消息
   - 在沙箱模式下配置您的机器人以进行测试，或发布以进行生产

2. **依赖项** — 适配器需要 `aiohttp` 和 `httpx`：
   ````bash
   pip 安装 aiohttp httpx
   ````

## 配置

### 互动设置

````bash
Hermes网关设置
````

从平台列表中选择**QQ Bot**，然后按照提示操作。

### 手动配置

在`~/.hermes/.env`中设置所需的环境变量：

````bash
QQ_APP_ID=您的应用ID
QQ_CLIENT_SECRET=您的应用程序秘密
````

## 环境变量

|变量|描述 |默认 |
|---|---|---|
| `QQ_APP_ID` | QQ机器人App ID（必填）| — |
| `QQ_CLIENT_SECRET` | QQ Bot 应用秘密（必填）| — |
| `QQBOT_HOME_CHANNEL` |用于 cron/通知传送的 OpenID | — |
| `QQBOT_HOME_CHANNEL_NAME` |家庭频道的显示名称 | '首页' |
| `QQ_ALLOWED_USERS` |用于 DM 访问的逗号分隔用户 OpenID |打开（所有用户）|
| `QQ_GROUP_ALLOWED_USERS` |用于组访问的逗号分隔组 OpenID | — |
| `QQ_ALLOW_ALL_USERS` |设置为“true”以允许所有 DM | `假` |
| `QQ_PORTAL_HOST` |覆盖QQ门户主机（设置为`sandbox.q.qq.com`用于沙箱路由） | `q.qq.com` |
| `QQ_STT_API_KEY` |语音转文本提供商的 API 密钥 | — |
| `QQ_STT_BASE_URL` | （不直接读取 - 在 `config.yaml` 中设置 `platforms.qqbot.extra.stt.baseUrl` ） |不适用 |
| `QQ_STT_MODEL` | STT 型号名称 | `glm-asr` |

## 高级配置

为了进行细粒度控制，请将平台设置添加到“~/.hermes/config.yaml”：

````yaml
平台：
  QQ机器人：
    启用：真
    额外：
      app_id: "你的应用程序 ID"
      client_secret: “你的秘密”
      markdown_support: true # 启用QQ markdown (msg_type 2)。仅配置；没有等效的 env-var。
      dm_policy: "开放" # 开放 |允许名单 |残疾人
      允许来自：
        - “user_openid_1”
      group_policy: "开放" # 开放 |允许名单 |残疾人
      组允许来自：
        - “group_openid_1”
      史特：
        提供商：“zai”#zai（GLM-ASR）、openai（Whisper）等
        baseUrl: "https://open.bigmodel.cn/api/coding/paas/v4"
        apiKey：“您的 stt 密钥”
        型号：“glm-asr”
````

## 语音消息（STT）

语音转录分两个阶段进行：

1. **QQ内置ASR**（免费，总是先尝试）——QQ在语音消息附件中提供了`asr_refer_text`，该功能使用腾讯自己的语音识别
2. **配置的 STT 提供程序**（后备） - 如果 QQ 的 ASR 不返回文本，适配器将调用 OpenAI 兼容的 STT API：

   - **Zhipu/GLM (zai)**：默认提供程序，使用 `glm-asr` 模型
   - **OpenAI Whisper**：设置`QQ_STT_BASE_URL`和`QQ_STT_MODEL`
   - 任何兼容 OpenAI 的 STT 端点

## 故障排除

### 机器人立即断开连接（快速断开）

这通常意味着：
- **无效的应用程序 ID / 秘密** — 在 q.qq.com 仔细检查您的凭据
- **缺少权限** — 确保机器人启用了所需的意图
- **仅沙盒机器人** — 如果机器人处于沙盒模式，则只能接收 QQ 沙盒测试通道的消息

### 语音消息未转录

1、检查附件数据中是否存在QQ内置的`asr_refer_text`
2. 如果使用自定义 STT 提供程序，请验证“QQ_STT_API_KEY”设置是否正确
3. 检查网关日志中是否有 STT 错误消息

### 消息未送达

- 验证机器人的**意图**已在 q.qq.com 上启用
- 如果 DM 访问受到限制，请检查“QQ_ALLOWED_USERS”
- 对于群组消息，请确保机器人是**@提及**（群组策略可能需要列入白名单）
- 检查“QQBOT_HOME_CHANNEL”以获取 cron/通知传递

### 连接错误

- 确保安装了“aiohttp”和“httpx”：“pip install aiohttp httpx”
- 检查与`api.sgroup.qq.com`和WebSocket网关的网络连接
- 查看网关日志以获取详细的错误消息和重新连接行为