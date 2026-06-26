---
sidebar_position: 8
title: "Mattermost"
description: "将 OpenClaw 设置为 Mattermost 机器人"
---
# 最重要的设置

OpenClaw 作为机器人与 Mattermost 集成，让您可以通过直接消息或团队渠道与 AI 助手聊天。 Mattermost 是一个自托管、开源的 Slack 替代方案 - 您可以在自己的基础设施上运行它，从而完全控制您的数据。该机器人通过 Mattermost 的 REST API (v4) 和 WebSocket 连接以获取实时事件，通过 OpenClaw 管道处理消息（包括工具使用、内存和推理），并实时响应。它支持文本、文件附件、图像和斜杠命令。

不需要外部 Mattermost 库 - 适配器使用“aiohttp”，它已经是 OpenClaw 依赖项。

在设置之前，这是大多数人想知道的部分：OpenClaw 在进入您的 Mattermost 实例后会如何表现。

## OpenClaw 的行为方式

|背景 |行为 |
|---------|----------|
| **DM** |赫尔墨斯回复每条消息。不需要“@提及”。每个 DM 都有自己的会话。 |
| **公共/私人频道** |当你“@提及”它时，OpenClaw 会做出回应。赫尔墨斯没有提及，而是忽略了这条消息。 |
| **话题** |如果“MATTERMOST_REPLY_MODE=thread”，OpenClaw 将在您的消息下的线程中回复。线程上下文与父通道保持隔离。 |
| **与多个用户共享频道** |默认情况下，OpenClaw 会隔离通道内每个用户的会话历史记录。除非您明确禁用该功能，否则在同一频道中交谈的两个人不会共享一份文字记录。 |

:::提示
如果您希望 OpenClaw 作为线程对话进行回复（嵌套在原始消息下），请设置“MATTERMOST_REPLY_MODE=thread”。默认值为“off”，即在通道中发送平面消息。
:::

### Mattermost 中的会话模型

默认情况下：

- 每个 DM 都有自己的会话
- 每个线程都有自己的会话命名空间
- 共享频道中的每个用户在该频道内都有自己的会话

这是由“config.yaml”控制的：

````yaml
每个用户的组会话数：true
````

仅当您明确希望整个频道有一个共享对话时，才将其设置为“false”：

````yaml
每个用户的组会话数： false
````

共享会话对于协作渠道很有用，但它们也意味着：

- 用户共享上下文增长和代币成本
- 一个人长期的、需要大量工具的任务可能会使其他人的环境变得臃肿
- 一个人的飞行中跑步可能会打断同一频道中另一个人的后续行动

本指南将引导您完成完整的设置过程 - 从在 Mattermost 上创建机器人到发送第一条消息。

## 第 1 步：启用机器人帐户

您必须先在 Mattermost 服务器上启用机器人帐户，然后才能创建机器人帐户。

1. 以 **系统管理员** 身份登录 Mattermost。
2. 转至 **系统控制台** → **集成** → **机器人帐户**。
3. 将**启用机器人帐户创建**设置为**true**。
4. 单击“**保存**”。

:::信息
如果您没有系统管理员访问权限，请要求您的 Mattermost 管理员启用机器人帐户并为您创建一个帐户。
:::

## 第 2 步：创建机器人帐户

1. 在 Mattermost 中，单击 **☰** 菜单（左上角）→ **集成** → **机器人帐户**。
2. 单击“**添加机器人帐户**”。
3. 填写详细信息：
   - **用户名**：例如“hermes”
   - **显示名称**：例如“OpenClaw”
   - **描述**：可选
   - **角色**：`成员`就足够了
4. 单击**创建机器人帐户**。
5. Mattermost 将显示 **bot 令牌**。 **立即复制。**

:::警告[令牌仅显示一次]
当您创建机器人帐户时，机器人令牌仅显示一次。如果您丢失了它，您需要从机器人帐户设置中重新生成它。切勿公开分享您的令牌或将其提交到 Git - 拥有此令牌的任何人都可以完全控制机器人。
:::

将令牌存储在安全的地方（例如密码管理器）。您将在第 5 步中需要它。

:::提示
您还可以使用**个人访问令牌**来代替机器人帐户。转到 **配置文件** → **安全性** → **个人访问令牌** → **创建令牌**。如果您希望 OpenClaw 作为您自己的用户而不是单独的机器人用户发布，这非常有用。
:::

## 步骤 3：将机器人添加到频道

该机器人需要是您希望其响应的任何渠道的成员：

1. 打开您想要机器人的频道。
2. 单击频道名称→ **添加成员**。
3. 搜索您的机器人用户名（例如“hermes”）并添加它。

对于私信，只需打开机器人的直接消息 - 它就能立即回复。

## 步骤 4：找到您最重要的用户 ID

OpenClaw 使用您的 Mattermost 用户 ID 来控制谁可以与机器人交互。要找到它：

1. 单击您的**头像**（左上角）→ **个人资料**。
2. 您的用户 ID 显示在配置文件对话框中 — 单击它进行复制。

您的用户 ID 是一个 26 个字符的字母数字字符串，例如“3uo8dkh1p7g1mfk49ear5fzs5c”。

:::警告
您的用户 ID **不是**您的用户名。用户名是“@”之后出现的内容（例如“@alice”）。用户 ID 是 Mattermost 内部使用的长字母数字标识符。
:::

**替代**：您还可以通过 API 获取您的用户 ID：

````bash
卷曲-H“授权：持有者YOUR_TOKEN”\
  https://your-mattermost-server/api/v4/users/me | https://your-mattermost-server/api/v4/users/me | jq.id
````

:::提示
要获取 **频道 ID**：单击频道名称 → **查看信息**。通道 ID 显示在信息面板中。如果您想手动设置家庭频道，您将需要这个。
:::

##第五步：配置OpenClaw代理

### 选项 A：交互式设置（推荐）

运行引导设置命令：

````bash
Hermes网关设置
````

出现提示时选择 **Mattermost**，然后在询问时粘贴您的服务器 URL、机器人令牌和用户 ID。

### 选项 B：手动配置

将以下内容添加到您的“~/.hermes/.env”文件中：

````bash
# 必填
MATTERMOST_URL=https://mm.example.com
MATERMOST_TOKEN=***
MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c

# 多个允许的用户（以逗号分隔）
# MATTERMOST_ALLOWED_USERS=3uo8dkh1p7g1mfk49ear5fzs5c,8fk2jd9s0a7bncm1xqw4tp6r3e

# 可选：回复模式（线程或关闭，默认：关闭）
# MATTERMOST_REPLY_MODE=线程

# 可选：不带 @mention 进行响应（默认值：true = 需要提及）
# MATTERMOST_REQUIRE_MENTION=假

# 可选：机器人在没有 @mention 的情况下响应的频道（以逗号分隔的频道 ID）
# MATTERMOST_FREE_RESPONSE_CHANNELS=channel_id_1,channel_id_2
````

`~/.hermes/config.yaml` 中的可选行为设置：

````yaml
每个用户的组会话数：true
````

- `group_sessions_per_user: true` 在共享通道和线程内保持每个参与者的上下文隔离

### 启动网关

配置完成后，启动 Mattermost 网关：

````bash
爱马仕网关
````

该机器人应在几秒钟内连接到您的 Mattermost 服务器。向其发送一条消息（无论是私信还是在已添加该消息的频道中）进行测试。

:::提示
您可以在后台运行“hermes gateway”或作为持久操作的 systemd 服务。有关详细信息，请参阅部署文档。
:::

## 家庭频道

您可以指定一个“主频道”，机器人将在其中发送主动消息（例如 cron 作业输出、提醒和通知）。有两种设置方法：

### 使用斜线命令

在机器人所在的任何 Mattermost 频道中输入“/sethome”。该频道成为家庭频道。

### 手动配置

将其添加到您的“~/.hermes/.env”中：

````bash
MATTERMOST_HOME_CHANNEL=abc123def456ghi789jkl012mn
````

将ID替换为实际频道ID（点击频道名称→查看信息→复制ID）。

## 回复模式

`MATTERMOST_REPLY_MODE` 设置控制 OpenClaw 如何发布回复：

|模式|行为 |
|------|----------|
| `关闭`（默认）| OpenClaw 在频道中发布平面消息，就像普通用户一样。 |
| `线程` | OpenClaw 在您的原始消息下方的帖子中回复。当有大量来回时保持通道清洁。 |

将其设置在`~/.hermes/.env`中：

````bash
MATTERMOST_REPLY_MODE=线程
````

## 提及行为

默认情况下，机器人仅在“@提及”时在频道中响应。您可以更改此设置：

|变量|默认 |描述 |
|----------|---------|-------------|
| `最重要的要求提及` | `真实` |设置为“false”以响应通道中的所有消息（DM 始终有效）。 |
| `MATTERMOST_FREE_RESPONSE_CHANNELS` | _（无）_ |以逗号分隔的通道 ID，即使 require_mention 为 true，机器人也会在没有“@mention”的情况下进行响应。 |

要在 Mattermost 中查找频道 ID：打开频道，单击频道名称标题，然后在 URL 或频道详细信息中查找 ID。

当机器人是“@提及”时，在处理之前会自动从消息中删除提及内容。

## 频道白名单 (`allowed_channels`)

将机器人限制在一组固定的 Mattermost 通道上。设置后，机器人**仅**在 ID 出现在列表中的通道中做出响应 - 来自任何其他通道的消息都会被默默忽略，即使机器人是“@提及”。

**DM 不受此过滤器的约束**，因此授权用户始终可以通过直接消息联系机器人。

````yaml
最重要的是：
  允许的频道：
    -“abc123def456ghi789jkl012mno”##ops
    -“xyz987uvw654rst321opq098nml”##事件响应
````

或者通过 env var（逗号分隔）：

````bash
MATTERMOST_ALLOWED_CHANNELS="abc123def456ghi789jkl012mno,xyz987uvw654rst321opq098nml"
````

行为：

- 空/未设置 → 无限制（完全向后兼容）。
- 非空 → 通道 ID 必须在列表中，否则消息会在任何其他门控（提及要求、“MATTERMOST_FREE_RESPONSE_CHANNELS”等）运行之前被丢弃。
- 通过 Mattermost UI → 频道标题 → “查看信息”查找频道 ID，或从频道 URL 中读取。

另请参阅：[管理员/用户斜杠命令拆分](../../reference/slash-commands.md#permissions-and-adminuser-split)。

## 故障排除

### 机器人不响应消息

**原因**：机器人不是频道成员，或者“MATTERMOST_ALLOWED_USERS”不包含您的用户 ID。

**修复**：将机器人添加到频道（频道名称→添加成员→搜索机器人）。验证您的用户 ID 在“MATTERMOST_ALLOWED_USERS”中。重新启动网关。

### 403 禁止错误

**原因**：机器人令牌无效，或者机器人没有在频道中发帖的权限。

**修复**：检查“.env”文件中的“MATTERMOST_TOKEN”是否正确。确保机器人帐户尚未停用。验证机器人已添加到频道中。如果使用个人访问令牌，请确保您的帐户具有所需的权限。

### WebSocket 断开连接/重新连接循环

**原因**：网络不稳定、Mattermost 服务器重新启动或 WebSocket 连接的防火墙/代理问题。

**修复**：适配器自动以指数退避重新连接（2 秒 → 60 秒）。检查服务器的 WebSocket 配置 - 反向代理（nginx、Apache）需要配置 WebSocket 升级标头。验证没有防火墙阻止 Mattermost 服务器上的 WebSocket 连接。

对于 nginx，确保您的配置包括：

````nginx
位置 /api/v4/websocket {
    proxy_pass http://mattermost-backend；
    proxy_set_header 升级 $http_upgrade;
    proxy_set_header 连接“升级”；
    proxy_read_timeout 600s；
}
````

### 启动时“无法验证”

**原因**：令牌或服务器 URL 不正确。

**修复**：验证“MATTERMOST_URL”指向您的 Mattermost 服务器（包括“https://”，无尾部斜杠）。检查“MATTERMOST_TOKEN”是否有效 - 使用curl尝试：

````bash
卷曲-H“授权：持有者YOUR_TOKEN”\
  https://您的服务器/api/v4/users/me
````

如果这返回您的机器人的用户信息，则令牌有效。如果返回错误，请重新生成令牌。

### 机器人离线

**原因**：OpenClaw 网关未运行，或者连接失败。

**修复**：检查“hermes gateway”是否正在运行。查看终端输出中的错误消息。常见问题：URL 错误、令牌过期、Mattermost 服务器无法访问。

###“用户不允许”/机器人忽略你

**原因**：您的用户 ID 不在“MATTERMOST_ALLOWED_USERS”中。

**修复**：将您的用户 ID 添加到 `~/.hermes/.env` 中的 `MATTERMOST_ALLOWED_USERS` 并重新启动网关。请记住：用户 ID 是 26 个字符的字母数字字符串，而不是您的“@username”。

## 每通道提示

将临时系统提示分配给特定的 Mattermost 频道。提示符会在每次运行时注入——不会持续记录历史记录——因此更改会立即生效。

````yaml
最重要的是：
  频道提示：
    “channel_id_abc123”：|
      你是一名研究助理。注重学术资源，
      引文和简明综合。
    “channel_id_def456”：|
      代码审查模式。精确处理边缘情况和
      性能影响。
````

键是 Mattermost 通道 ID（在通道 URL 或通过 API 中找到它们）。匹配通道中的所有消息都会获得作为临时系统指令注入的提示。

## 安全

:::警告
始终设置“MATTERMOST_ALLOWED_USERS”来限制谁可以与机器人交互。如果没有它，网关将默认拒绝所有用户作为安全措施。仅添加您信任的人员的用户 ID — 授权用户可以完全访问代理的功能，包括工具使用和系统访问。
:::

有关保护 OpenClaw 部署的更多信息，请参阅[安全指南](../security.md)。

## 注释

- **自托管友好**：可与任何自托管 Mattermost 实例配合使用。无需 Mattermost Cloud 帐户或订阅。
- **没有额外的依赖项**：适配器使用 `aiohttp` 进行 HTTP 和 WebSocket，该协议已包含在 OpenClaw 中。
- **团队版兼容**：适用于 Mattermost 团队版（免费）和企业版。