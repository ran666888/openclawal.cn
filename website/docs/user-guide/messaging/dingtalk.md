---
sidebar_position: 10
title: "DingTalk"
description: "将 OpenClaw 设置为钉钉机器人"
---
# 钉钉设置

OpenClaw 与钉钉集成为聊天机器人，让您可以通过私聊或群聊与 AI 助手聊天。该机器人通过钉钉的流模式（一种长期的 WebSocket 连接，不需要公共 URL 或 webhook 服务器）进行连接，并通过钉钉的会话 webhook API 使用 markdown 格式的消息进行回复。

在设置之前，这是大多数人想了解的部分：OpenClaw 在进入钉钉工作区后会如何表现。

## OpenClaw 的行为方式

|背景 |行为 |
|---------|----------|
| **私信（1:1 聊天）** |赫尔墨斯回复每条消息。不需要“@提及”。每个 DM 都有自己的会话。 |
| **群聊** |当你“@提及”它时，OpenClaw 会做出回应。赫尔墨斯没有提及，而是忽略了这条消息。 |
| **与多个用户共享组** |默认情况下，OpenClaw 会隔离组内每个用户的会话历史记录。在同一组中交谈的两个人不会共享一份记录，除非您明确禁用它。 |

### 钉钉中的会话模型

默认情况下：

- 每个 DM 都有自己的会话
- 共享群聊中的每个用户在该组内都有自己的会话

这是由“config.yaml”控制的：

````yaml
每个用户的组会话数：true
````

仅当您明确希望整个组共享一个对话时，才将其设置为“false”：

````yaml
每个用户的组会话数： false
````

本指南将引导您完成完整的设置过程 - 从创建钉钉机器人到发送第一条消息。

## 先决条件

安装所需的 Python 包：

````bash
pip install "hermes-agent[dingtalk]"
````

或者单独：

````bash
pip install dingtalk-stream httpx alibabacloud-dingtalk
````

- `dingtalk-stream` — 钉钉官方 Stream 模式 SDK（基于 WebSocket 的实时消息传递）
- `httpx` — 用于通过会话 webhooks 发送回复的异步 HTTP 客户端
- `alibabacloud-dingtalk` — 钉钉 OpenAPI SDK，用于 AI 卡片、表情反应和媒体下载

## 步骤一：创建钉钉应用

1. 进入【钉钉开发者控制台】(https://open-dev.dingtalk.com/)。
2. 使用钉钉管理员帐号登录。
3. 点击**应用程序开发** → **自定义应用程序** → **通过H5微应用程序创建应用程序**（或**机器人**，具体取决于您的控制台版本）。
4、填写：
   - **应用程序名称**：例如“OpenClaw”
   - **描述**：可选
5. 创建后，导航到 **Credentials & Basic Info** 以查找您的 **Client ID** (AppKey) 和 **Client Secret** (AppSecret)。复制两个。

:::警告[凭据仅显示一次]
客户端密钥仅在您创建应用程序时显示一次。如果您丢失了它，则需要重新生成它。切勿公开共享这些凭据或将其提交给 Git。
:::

## 步骤2：启用机器人能力

1. 在应用程序的设置页面中，转到 **添加功能** → **机器人**。
2. 开启机器人能力。
3. 在**消息接收模式**下，选择**流模式**（推荐 — 无需公共 URL）。

:::提示
流模式是推荐的设置。它使用从您的计算机发起的长期 WebSocket 连接，因此您不需要公共 IP、域名或 Webhook 端点。这可以在 NAT、防火墙后面和本地计算机上运行。
:::

## 第三步：找到您的钉钉用户ID

OpenClaw 使用您的钉钉用户 ID 来控制谁可以与机器人交互。钉钉用户 ID 是由组织管理员设置的字母数字字符串。

找到你的：

1. 询问您的钉钉组织管理员 - 用户 ID 在钉钉管理控制台的 **联系人** → **成员** 下配置。
2. 或者，机器人会记录每条传入消息的“sender_id”。启动网关，向机器人发送消息，然后检查日志中是否有您的 ID。

## 步骤4：配置OpenClaw代理

### 选项 A：交互式设置（推荐）

运行引导设置命令：

````bash
Hermes网关设置
````

出现提示时选择**钉钉**。设置向导可以通过以下两种路径之一进行授权：

- **二维码设备流程（推荐）。** 使用钉钉移动应用扫描终端中打印的二维码 - 您的 Client ID 和 Client Secret 会自动返回并写入“~/.hermes/.env”。无需开发者控制台之旅。
- **手动粘贴。** 如果您已有凭据（或 QR 扫描不方便），请在出现提示时粘贴您的客户端 ID、客户端密钥和允许的用户 ID。

:::注意 openClaw 品牌披露
由于钉钉的verification_uri_complete在API层硬编码为openClaw身份，所以目前二维码是在openClaw源字符串下授权的，直到阿里巴巴/钉钉Real-AI在服务器端注册了OpenClaw专用模板。这纯粹是钉钉呈现同意屏幕的方式——您创建的机器人完全属于您，并且对您的租户是私有的。
:::

### 选项 B：手动配置

将以下内容添加到您的“~/.hermes/.env”文件中：

````bash
# 必填
DINGTALK_CLIENT_ID=您的应用程序密钥
DINGTALK_CLIENT_SECRET=您的应用程序秘密

# 安全性：限制谁可以与机器人交互
DINGTALK_ALLOWED_USERS=用户 ID-1

# 多个允许的用户（以逗号分隔）
# DINGTALK_ALLOWED_USERS=用户 ID-1,用户 ID-2

# 可选：群聊门控（镜像 Slack/Telegram/Discord/WhatsApp）
# DINGTALK_REQUIRE_MENTION=true
# DINGTALK_FREE_RESPONSE_CHATS=cidABC==,cidDEF==
# DINGTALK_MENTION_PATTERNS=^小马
# DINGTALK_HOME_CHANNEL=cidXXXX==
# DINGTALK_ALLOW_ALL_USERS=true
````

`~/.hermes/config.yaml` 中的可选行为设置：

````yaml
每个用户的组会话数：true

网关：
  平台：
    钉钉：
      额外：
        # 在机器人回复之前需要在组中@mention（与 Slack/Telegram/Discord 同等）。
        # 私信忽略这一点 — 机器人总是以 1:1 聊天方式回复。
        要求提及：true

        # 每个平台的白名单。设置后，只有这些钉钉用户ID才能与机器人交互
        # （与 DINGTALK_ALLOWED_USERS 语义相同，但范围在此而不是在 .env 中）。
        允许的用户：
          - 用户 ID-1
          - 用户 ID-2
````

- `group_sessions_per_user: true` 在共享群聊中保持每个参与者的上下文隔离
- `require_mention: true` 阻止机器人回复每条群组消息 - 它仅在有人 @-提及它时才回复
- `dingtalk.extra`下的`allowed_users`是`DINGTALK_ALLOWED_USERS`的替代方案；如果两者都设置了，它们就会合并

### 启动网关

配置完成后，启动钉钉网关：

````bash
爱马仕网关
````

机器人应该会在几秒钟内连接到钉钉的流模式。向其发送一条消息（无论是通过私信还是在已添加的群组中）进行测试。

:::提示
您可以在后台运行“hermes gateway”或作为持久操作的 systemd 服务。有关详细信息，请参阅部署文档。
:::

## 特点

### 人工智能卡

OpenClaw 可以使用钉钉 AI 卡回复，而不是普通的 Markdown 消息。卡片提供更丰富、更结构化的显示，并在代理生成响应时支持流式更新。

要启用 AI 卡，请在 config.yaml 中配置卡模板 ID：

````yaml
平台：
  钉钉：
    启用：真
    额外：
      card_template_id: "您的卡模板 ID"
````

您可以在钉钉开发者控制台应用的AI卡片设置下找到您的卡片模板ID。启用 AI 卡后，所有回复都会作为带有流式文本更新的卡片发送。

### 表情符号反应

OpenClaw 会自动将表情符号反应添加到您的消息中以显示处理状态：

- 🤔思考 — 当机器人开始处理您的消息时添加
- 🥳完成 — 响应完成时添加（取代思考反应）

这些反应在私信和群聊中都有效。

### 显示设置

您可以独立于其他平台自定义钉钉的显示行为：

````yaml
显示：
  平台：
    钉钉：
      show_reasoning: false # 在回复中显示模型推理/思考
      Streaming: true # 启用流式响应（适用于 AI 卡）
      tool_progress: all # 显示工具执行进度（全部/新建/关闭）
      interim_assistant_messages: true # 显示中间评论消息
````

要禁用工具进度和中间消息以获得更清晰的体验：

````yaml
显示：
  平台：
    钉钉：
      工具进度：关闭
      临时助理消息：假
````

## 故障排除

### 机器人不响应消息

**原因**：机器人功能未启用，或“DINGTALK_ALLOWED_USERS”不包含您的用户 ID。

**修复**：验证您的应用程序设置中已启用机器人功能并且已选择“流模式”。检查您的用户 ID 是否在“DINGTALK_ALLOWED_USERS”中。重新启动网关。

### “dingtalk-stream 未安装”错误

**原因**：未安装 `dingtalk-stream` Python 包。

**修复**：安装它：

````bash
pip install dingtalk-stream httpx
````

###“需要 DINGTALK_CLIENT_ID 和 DINGTALK_CLIENT_SECRET”

**原因**：您的环境或“.env”文件中未设置凭据。

**修复**：验证“~/.hermes/.env”中的“DINGTALK_CLIENT_ID”和“DINGTALK_CLIENT_SECRET”设置是否正确。 Client ID 是您的 AppKey，Client Secret 是您在钉钉开发者控制台中的 AppSecret。

### 流断开/重新连接循环

**原因**：网络不稳定、钉钉平台维护或凭证问题。

**修复**：适配器自动以指数退避重新连接（2s → 5s → 10s → 30s → 60s）。检查您的凭据是否有效并且您的应用程序尚未停用。验证您的网络允许出站 WebSocket 连接。

### 机器人离线

**原因**：OpenClaw 网关未运行，或者连接失败。

**修复**：检查“hermes gateway”是否正在运行。查看终端输出中的错误消息。常见问题：凭据错误、应用程序已停用、未安装“dingtalk-stream”或“httpx”。

###“没有可用的 session_webhook”

**原因**：机器人尝试回复，但没有会话 Webhook URL。如果 Webhook 过期或机器人在接收消息和发送回复之间重新启动，通常会发生这种情况。

**修复**：向机器人发送新消息 - 每条传入消息都提供一个用于回复的新会话 Webhook。这是钉钉的正常限制；机器人只能回复最近收到的消息。

## 安全

:::警告
始终设置“DINGTALK_ALLOWED_USERS”来限制谁可以与机器人交互。如果没有它，网关将默认拒绝所有用户作为安全措施。仅添加您信任的人员的用户 ID — 授权用户可以完全访问代理的功能，包括工具使用和系统访问。
:::

有关保护 OpenClaw 部署的更多信息，请参阅[安全指南](../security.md)。

## 注释

- **流模式**：不需要公共 URL、域名或 Webhook 服务器。连接是通过 WebSocket 从您的计算机发起的，因此它可以在 NAT 和防火墙后面工作。
- **AI 卡**：可以选择使用丰富的 AI 卡进行回复，而不是简单的降价。通过“card_template_id”进行配置。
- **表情符号反应**：自动🤔思考/🥳处理状态的完成反应。
- **Markdown回复**：回复采用钉钉Markdown格式，用于富文本显示。
- **媒体支持**：传入消息中的图像和文件会自动解析，并可以通过视觉工具进行处理。
- **消息重复数据删除**：适配器以 5 分钟的窗口时间对消息进行重复数据删除，以防止同一消息处理两次。
- **自动重新连接**：如果流连接断开，适配器会自动以指数退避重新连接。
- **消息长度限制**：每条消息的响应上限为 20,000 个字符。较长的响应将被截断。