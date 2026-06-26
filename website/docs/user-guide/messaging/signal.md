---
sidebar_position: 6
title: "Signal"
description: "通过 signal-cli 守护进程将 OpenClaw 设置为 Signal 机器人"
---
# 信号设置

OpenClaw 通过以 HTTP 模式运行的 [signal-cli](https://github.com/AsamK/signal-cli) 守护进程连接到 Signal。适配器通过 SSE（服务器发送事件）实时传输消息并通过 JSON-RPC 发送响应。

Signal 是最注重隐私的主流信使——默认端到端加密、开源协议、最少的元数据收集。这使其成为对安全敏感的代理工作流程的理想选择。

:::info 没有新的 Python 依赖项
Signal 适配器使用“httpx”（已经是 OpenClaw 的核心依赖项）进行所有通信。不需要额外的 Python 包。您只需要在外部安装 signal-cli 即可。
:::

---

## 先决条件

- **signal-cli** — 基于 Java 的 Signal 客户端 ([GitHub](https://github.com/AsamK/signal-cli))
- **Java 17+** 运行时 — signal-cli 需要
- **安装了 Signal 的电话号码**（用于作为辅助设备进行链接）

### 安装 signal-cli

````bash
# macOS
酿造安装signal-cli

# Linux（下载最新版本）
版本=$(curl -Ls -o /dev/null -w %{url_ effective} \
  https://github.com/AsamK/signal-cli/releases/latest | https://github.com/AsamK/signal-cli/releases/latest | sed 's/^.*\/v//')
卷曲-L -O“https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}.tar.gz”
sudo tar xf“signal-cli-${VERSION}.tar.gz”-C /opt
sudo ln -sf“/opt/signal-cli-${VERSION}/bin/signal-cli”/usr/local/bin/
````

:::注意
signal-cli **不在** apt 或 snap 存储库中。上面的 Linux 安装直接从 [GitHub 版本](https://github.com/AsamK/signal-cli/releases) 下载。
:::

---

## 第 1 步：关联您的信号账户

Signal-cli 作为**链接设备** — 类似于 WhatsApp Web，但适用于 Signal。您的手机仍然是主要设备。

````bash
# 生成链接 URI（显示二维码或链接）
signal-cli链接-n“HermesAgent”
````

1. 在手机上打开**Signal**
2. 转到 **设置 → 链接的设备**
3. 点击 **链接新设备**
4. 扫描二维码或输入URI

---

## 步骤 2：启动 signal-cli 守护进程

````bash
# 将 +1234567890 替换为您的 Signal 电话号码（E.164 格式）
signal-cli --account +1234567890 守护进程 --http 127.0.0.1:8080
````

:::提示
让它在后台运行。您可以使用“systemd”、“tmux”、“screen”，或将其作为服务运行。
:::

验证它正在运行：

````bash
卷曲 http://127.0.0.1:8080/api/v1/check
# 应该返回：{"versions":{"signal-cli":...}}
````

---

## 第三步：配置 OpenClaw

最简单的方法：

````bash
Hermes网关设置
````

从平台菜单中选择**信号**。向导将：

1.检查是否安装了signal-cli
2. 提示输入 HTTP URL（默认：`http://127.0.0.1:8080`）
3. 测试与守护进程的连接
4. 询问您的账户电话号码
5. 配置允许的用户和访问策略

### 手动配置

添加到`~/.hermes/.env`：

````bash
# 必填
SIGNAL_HTTP_URL=http://127.0.0.1:8080
SIGNAL_ACCOUNT=+1234567890

# 安全（推荐）
SIGNAL_ALLOWED_USERS=+1234567890,+0987654321 # 以逗号分隔的 E.164 号码或 UUID

# 可选
SIGNAL_GROUP_ALLOWED_USERS=groupId1,groupId2 # 启用组（省略禁用，* 表示全部）
SIGNAL_HOME_CHANNEL=+1234567890 # cron 作业的默认传送目标
````

然后启动网关：

````bash
爱马仕网关 # 前景
hermes gateway install # 作为用户服务安装
sudo hermes gateway install --system # 仅适用于 Linux：启动时系统服务
````

---

## 访问控制

### DM 访问

DM 访问遵循与所有其他 OpenClaw 平台相同的模式：

1. **`SIGNAL_ALLOWED_USERS` 设置** → 只有这些用户可以发送消息
2. **无许可名单设置** → 未知用户获得 DM 配对码（通过 `hermes 配对批准信号代码` 批准）
3. **`SIGNAL_ALLOW_ALL_USERS=true`** → 任何人都可以留言（谨慎使用）

### 群组访问

组访问由“SIGNAL_GROUP_ALLOWED_USERS”环境变量控制：

|配置|行为 |
|----------------|----------|
|未设置（默认）|所有群组消息都会被忽略。该机器人仅响应 DM。 |
|设置组 ID |仅监控列出的组（例如“groupId1,groupId2”）。 |
|设置为`*` |机器人会在其所属的任何组中做出响应。 |

---

## 特点

### 附件

该适配器支持双向发送和接收媒体。

**传入**（用户→代理）：

- **图像** — PNG、JPEG、GIF、WebP（通过魔法字节自动检测）
- **音频** — MP3、OGG、WAV、M4A（如果配置了 Whisper，则转录语音消息）
- **文档** — PDF、ZIP 和其他文件类型

**传出**（代理 → 用户）：

代理可以通过响应中的“MEDIA:”标签发送媒体文件。支持以下交付方式：

- **图像** — `send_multiple_images` 和 `send_image_file` 将 PNG、JPEG、GIF、WebP 作为本机信号附件发送
- **语音** — `send_voice` 将音频文件（OGG、MP3、WAV、M4A、AAC）作为附件发送
- **视频** — `send_video` 发送 MP4 视频文件
- **文档** — `send_document` 发送任何文件类型（PDF、ZIP 等）

所有传出媒体均通过 Signal 的标准附件 API。与某些平台不同，Signal 不会在协议级别区分语音消息和文件附件。

附件大小限制：**100 MB**（双向）。
:::警告
**信号服务器将限制附件上传的速率**，适配器使用调度程序进行多图像发送，以 32 个为一组批量处理图像，并限制上传以匹配信号服务器策略。
:::

### 本机格式、回复引用和反应

信号消息以**本机格式**而不是文字标记字符呈现。该适配器将 markdown（`**bold**`、`*italic*`、``code` ``、`~~strike~~`、`||spoiler||`、标题）转换为 Signal `bodyRanges`，以便文本在接收者的客户端上以真实的样式显示，而不是显示为可见的 `**` / ` ` `` 字符。

**回复引用。** 当 OpenClaw 回复特定消息时，它现在会发布一个引用原始消息的本机回复 — Signal 用户在自己使用“回复”时看到的 UI 功能相同。对于响应入站消息而生成的回复来说，这是自动的。

**反应。** 代理可以通过标准反应 API 对消息做出反应； Signal 中的反应以引用消息上的表情符号反应的形式出现，而不是作为额外的文本。

这些都不需要额外的配置——它在最近的 signal-cli 版本中默认提供。如果您的“signal-cli”版本太旧，OpenClaw 会回退到纯文本传输并记录一次性警告。

### 键入指示器

机器人在处理消息时发送输入指示符，每 8 秒刷新一次。

### 工具进度显示

Signal 不支持编辑已发送的消息。因此，即使启用了“/verbose”，OpenClaw 也会抑制 Signal 上的网关工具进度气泡，并为平台保存非“关闭”模式。

您仍然可以在 CLI 中查看工具活动，并且最终的 Signal 回复可以包括正常的助理输出。如果您需要在聊天中实时了解每个工具的进度，请使用具有消息编辑支持的消息传递平台。

### 电话号码编辑

所有电话号码都会在日志中自动编辑：
- `+15551234567` → `+155****4567`
- 这适用于 OpenClaw 网关日志和全局编辑系统

### 自我提醒（单一数字设置）

如果您在自己的电话号码（而不是单独的机器人号码）上将 signal-cli 作为 **链接的辅助设备** 运行，则可以通过 Signal 的“自我提示”功能与 OpenClaw 进行交互。

只需通过手机向自己发送一条消息即可 - signal-cli 会接收该消息，OpenClaw 将在同一对话中做出回应。

**它是如何工作的：**
- “自我提醒”消息以 `syncMessage.sentMessage` 信封形式到达
- 适配器会检测这些内容何时发送至机器人自己的帐户，并将其作为常规入站消息进行处理
- 回显保护（发送时间戳跟踪）可防止无限循环 - 机器人自己的回复会被自动过滤掉

**无需额外配置。** 只要“SIGNAL_ACCOUNT”与您的电话号码匹配，此功能就会自动生效。

### 健康监测

适配器监视 SSE 连接并在以下情况下自动重新连接：
- 连接断开（指数退避：2s → 60s）
- 120 秒内未检测到任何活动（ping signal-cli 进行验证）

---

## 故障排除

|问题 |解决方案 |
|---------|----------|
| **设置期间“无法到达 signal-cli”** |确保 signal-cli 守护进程正在运行： `signal-cli --account +YOUR_NUMBER daemon --http 127.0.0.1:8080` |
| **未收到消息** |检查“SIGNAL_ALLOWED_USERS”是否包含 E.164 格式的发件人号码（带有“+”前缀）|
| **“在 PATH 上找不到 signal-cli”** |安装 signal-cli 并确保它在您的 PATH 中，或使用 Docker |
| **连接不断掉线** |检查 signal-cli 日志中是否有错误。确保安装了 Java 17+。 |
| **群组消息被忽略** |使用特定组 ID 配置“SIGNAL_GROUP_ALLOWED_USERS”，或使用“*”配置允许所有组。 |
| **机器人不回复任何人** |配置“SIGNAL_ALLOWED_USERS”，使用 DM 配对，或者如果您想要更广泛的访问权限，则可以通过网关策略明确允许所有用户。 |
| **重复消息** |确保只有一个 signal-cli 实例正在监听您的电话号码 |

---

## 安全

:::警告
**始终配置访问控制。** 默认情况下，机器人具有终端访问权限。如果没有“SIGNAL_ALLOWED_USERS”或 DM 配对，作为安全措施，网关将拒绝所有传入消息。
:::

- 所有日志输出中的电话号码均经过编辑
- 使用 DM 配对或明确的许可名单来安全地引导新用户
- 除非您特别需要群组支持，否则请禁用群组，或者仅将您信任的群组列入白名单
- Signal 的端到端加密可保护传输中的消息内容
- `~/.local/share/signal-cli/` 中的 signal-cli 会话数据包含帐户凭据 - 像密码一样保护它

---

## 环境变量参考

|变量|必填|默认 |描述 |
|----------|----------|---------|------------|
| `SIGNAL_HTTP_URL` |是的 | — | signal-cli HTTP 端点 |
| `信号帐户` |是的 | — |机器人电话号码 (E.164) |
| `SIGNAL_ALLOWED_USERS` |没有 | — |以逗号分隔的电话号码/UUID |
| `SIGNAL_GROUP_ALLOWED_USERS` |没有 | — |要监视的组 ID，或所有的“*”（省略以禁用组）|
| `SIGNAL_ALLOW_ALL_USERS` |没有 | `假` |允许任何用户交互（跳过白名单）|
| `SIGNAL_HOME_CHANNEL` |没有 | — | cron 作业的默认交付目标 |