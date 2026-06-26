---
sidebar_position: 5
title: "WhatsApp"
description: "通过内置 Baileys 桥接将 OpenClaw 设置为 WhatsApp 机器人"
---
# WhatsApp 设置

OpenClaw 通过基于 **Baileys** 的内置桥连接到 WhatsApp。这是通过模拟 WhatsApp Web 会话来实现的，**不是**通过官方 WhatsApp Business API。不需要元开发者帐户或业务验证。

> 运行“hermes gateway setup”并选择 **WhatsApp** 进行引导式演练。

:::tip 两个 WhatsApp 集成
此页面适用于**贝利桥** — 快速设置、个人帐户、无需公共 URL、禁止风险。

如果您正在运行真正的商业机器人并想要稳定性，请参阅 **[WhatsApp Business Cloud API 指南](./whatsapp-cloud.md)**。这是官方 Meta 支持的路径：没有帐户被禁止的风险，但需要 Meta Business 帐户和公共 webhook URL。

如果有理由的话，这两个适配器还可以针对不同的电话号码并行运行。
:::

:::警告非官方 API — 禁止风险
WhatsApp **不**正式支持 Business API 之外的第三方机器人。使用第三方桥接器会带来账户限制的小风险。为了最大限度地降低风险：
- **使用机器人的专用电话号码**（不是您的个人号码）
- **不要发送批量/垃圾邮件** - 保持对话式使用
- **不要自动向未先发消息的人发送出站消息**
:::

:::警告 WhatsApp 网络协议更新
WhatsApp 定期更新其 Web 协议，这可能会暂时破坏兼容性
与第三方桥梁。当这种情况发生时，OpenClaw 将更新桥依赖项。如果
WhatsApp 更新后机器人停止工作，请提取最新的 OpenClaw 版本并重新配对。
:::

## 两种模式

|模式|它是如何运作的 |最适合 |
|------|-------------|----------|
| **单独的机器人编号**（推荐）|为机器人指定一个电话号码。人们直接向该号码发送消息。 |干净的用户体验、多用户、更低的封禁风险 |
| **个人自聊** |使用您自己的 WhatsApp。您给自己发消息与代理交谈。 |快速设置、单用户、测试 |

---

## 先决条件

- **Node.js v18+** 和 **npm** — WhatsApp 桥作为 Node.js 进程运行
- **安装有WhatsApp**的手机（用于扫描二维码）

与旧的浏览器驱动的桥不同，当前基于 Baileys 的桥**不需要**需要本地 Chromium 或 Puppeteer 依赖堆栈。

---

## 第 1 步：运行设置向导

````bash
爱马仕
````

向导将：

1.询问您想要哪种模式（**机器人**或**自聊**）
2. 如果需要，安装桥依赖项
3. 在您的终端中显示 **QR 码**
4.等待您扫描

**扫描二维码：**

1. 在手机上打开 WhatsApp
2. 转到 **设置 → 链接的设备**
3. 点击 **链接设备**
4. 将相机对准终端二维码

配对后，向导会确认连接并退出。您的会话会自动保存。

:::提示
如果二维码看起来乱码，请确保您的终端至少有 60 列宽并支持
统一码。您还可以尝试不同的终端模拟器。
:::

---

## 步骤 2：获取第二个电话号码（机器人模式）

对于机器人模式，您需要一个尚未在 WhatsApp 中注册的电话号码。三个选项：

|选项 |成本|笔记|
|--------|------|--------|
| **谷歌语音** |免费|仅限美国。请访问 [voice.google.com](https://voice.google.com) 获取号码。通过 Google Voice 应用程序通过短信验证 WhatsApp。 |
| **预付费 SIM 卡** |一次性 5–15 美元 |任何载体。激活并验证 WhatsApp，然后 SIM 卡就可以放在抽屉里了。号码必须保持活跃（每 90 天拨打一次电话）。 |
| **VoIP 服务** |免费 – 5 美元/月 | TextNow、TextFree 或类似的。 Some VoIP numbers are blocked by WhatsApp — try a few if the first doesn't work. |

拿到号码后：

1. 在手机上安装 WhatsApp（或通过双 SIM 卡使用 WhatsApp Business 应用程序）
2. 使用 WhatsApp 注册新号码
3. 运行“hermes Whatsapp”并扫描该 WhatsApp 帐户中的二维码

---

## 第三步：配置 OpenClaw

将以下内容添加到您的“~/.hermes/.env”文件中：

````bash
# 必填
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot #“机器人”或“自我聊天”

# 访问控制 — 选择以下选项之一：
WHATSAPP_ALLOWED_USERS=15551234567 # 以逗号分隔的电话号码（带国家/地区代码，无 +）
# WHATSAPP_ALLOWED_USERS=* # 或使用 * 允许所有人
# WHATSAPP_ALLOW_ALL_USERS=true # 或者设置此标志（与 * 效果相同）
````

:::tip 允许所有简写
Setting `WHATSAPP_ALLOWED_USERS=*` allows **all** senders (equivalent to `WHATSAPP_ALLOW_ALL_USERS=true`).
这与[信号组白名单](/reference/environment-variables) 一致。
要使用配对流程，请删除这两个变量并依赖于
[DM pairing system](/user-guide/security#dm-pairing-system).
:::

`~/.hermes/config.yaml` 中的可选行为设置：

````yaml
unauthorized_dm_behavior：对

微信：
  unauthorized_dm_behavior：忽略
````

- `unauthorized_dm_behavior:pair` 是全局默认值。未知的 DM 发件人会获得配对码。
- `whatsapp.unauthorized_dm_behavior:ignore` 使 WhatsApp 对未经授权的 DM 保持沉默，这通常是私人号码的更好选择。

然后启动网关：

````bash
爱马仕网关 # 前景
hermes gateway install # 作为用户服务安装
sudo hermes gateway install --system # 仅适用于 Linux：启动时系统服务
````

网关使用保存的会话自动启动 WhatsApp 桥。

---

## 会话保持

Baileys 桥将其会话保存在“~/.hermes/platforms/whatsapp/session”下。这意味着：

- **会话在重新启动后仍然有效** — 您无需每次都重新扫描二维码
- 会话数据包括加密密钥和设备凭证
- **不要共享或提交此会话目录** — 它授予对 WhatsApp 帐户的完全访问权限

---

## 重新配对

如果会话中断（手机重置、WhatsApp 更新、手动取消链接），您将看到连接
网关日志中的错误。要修复它：

````bash
爱马仕
````

这会生成一个新的二维码。再次扫描并重新建立会话。网关
自动处理**临时**断开连接（网络故障、手机短暂离线）
具有重新连接逻辑。

---

## 语音留言

OpenClaw 支持 WhatsApp 语音：

- **传入：** 使用配置的 STT 提供程序自动转录语音消息（`.ogg` opus）：本地 `faster-whisper`、Groq Whisper (`GROQ_API_KEY`) 或 OpenAI Whisper (`VOICE_TOOLS_OPENAI_KEY`)
- **传出：** TTS 响应作为 MP3 音频文件附件发送
- Agent responses are prefixed with "⚕ **OpenClaw**" by default.您可以在“config.yaml”中自定义或禁用它：

````yaml
# ~/.hermes/config.yaml
微信：
  reply_prefix: "" # 空字符串禁用标头
  #reply_prefix: "🤖 *My Bot*\n──────\n" # 自定义前缀(支持换行符\n)
````

---

## 消息格式和传递

WhatsApp 支持**流式（渐进式）响应**——机器人在人工智能生成文本时实时编辑消息，就像 Discord 和 Telegram 一样。在内部，WhatsApp 的交付能力被归类为 TIER_MEDIUM 平台。

### 分块

长响应会自动分成多条消息，每块 **4,096 个字符**（WhatsApp 的实际显示限制）。您无需配置任何内容 - 网关会处理拆分并按顺序发送块。

### WhatsApp 兼容 Markdown

AI 回复中的标准 Markdown 会自动转换为 WhatsApp 的原生格式：

|降价| WhatsApp |呈现为 |
|----------|----------|------------|
| `**粗体**` | `*粗体*` | **粗体** |
| `~~删除线~~` | `~删除线~` | ~~删除线~~ |
| `# 标题` | `*标题*` |粗体文本（无本机标题）|
| `[链接文本](url)` | `链接文本（url）` |内联网址 |

由于 WhatsApp 本身支持三重反引号格式，因此代码块和内联代码会按原样保留。

### 工具进度

当代理调用工具（网络搜索、文件操作等）时，WhatsApp 会显示实时进度指示器，显示哪个工具正在运行。默认情况下启用此功能 - 无需配置。

### 消息批处理（反跳）

WhatsApp 单独传递每条消息，因此快速爆发（批量转发、粘贴分割、多行文本）将触发每个片段的单独代理调用 - 浪费令牌并产生多个脱节的回复。适配器缓冲来自同一聊天的连续文本消息，并在短暂的安静期（默认 **5 秒**，对于很长的片段延长至 **10 秒**）后将它们作为一个组合请求进行分派。通过 `config.yaml` 进行调整：

````yaml
# ~/.hermes/config.yaml
网关：
  平台：
    微信：
      额外：
        text_batch_delay_seconds: 5.0 # 刷新批次之前的安静期
        text_batch_split_delay_seconds: 10.0  # extended delay near the split threshold
````

Set `text_batch_delay_seconds: 0` to dispatch each message immediately (disables batching).

---

## 故障排除

|问题 |解决方案 |
|---------|----------|
| **二维码无法扫描** |确保终端足够宽（60 列以上）。尝试不同的终端。确保您使用正确的 WhatsApp 帐户（机器人号码，而非个人号码）进行扫描。 |
| **二维码过期** | QR 码每约 20 秒刷新一次。如果超时，请重新启动“hermes Whatsapp”。 |
| **会话未持续** | Check that `~/.hermes/platforms/whatsapp/session` exists and is writable.如果容器化，请将其安装为持久卷。 |
| **意外退出** | WhatsApp 在长时间不活动后断开设备的链接。保持手机开机并连接到网络，然后根据需要与“hermes Whatsapp”重新配对。 |
| **网桥崩溃或重新连接环路** | Restart the gateway, update OpenClaw, and re-pair if the session was invalidated by a WhatsApp protocol change. |
| **WhatsApp 更新后机器人停止工作** |更新 OpenClaw 以获取最新的桥接版本，然后重新配对。 |
| **macOS：“Node.js 未安装”，但节点可以在终端中运行** | launchd 服务不会继承您的 shell 路径。运行“hermes gateway install”将当前路径重新快照到 plist 中，然后运行“hermes gateway start”。有关详细信息，请参阅[网关服务文档](./index.md#macos-launchd)。 |
| **未收到消息** | Verify `WHATSAPP_ALLOWED_USERS` includes the sender's number (with country code, no `+` or spaces), or set it to `*` to allow everyone. Set `WHATSAPP_DEBUG=true` in `.env` and restart the gateway to see raw message events in `bridge.log`. |
| **Bot replies to strangers with a pairing code** | Set `whatsapp.unauthorized_dm_behavior: ignore` in `~/.hermes/config.yaml` if you want unauthorized DMs to be silently ignored instead. |

---

## 安全

:::警告
**上线前配置访问控制**。设置“WHATSAPP_ALLOWED_USERS”特定
电话号码（包括国家/地区代码，不带“+”），使用“*”允许所有人，或设置
`WHATSAPP_ALLOW_ALL_USERS=true`。如果没有这些，网关**拒绝所有传入
消息**作为安全措施。
:::

默认情况下，未经授权的 DM 仍会收到配对码回复。如果您希望私人 WhatsApp 号码对陌生人完全保持沉默，请设置：

````yaml
微信：
  unauthorized_dm_behavior：忽略
````

- The `~/.hermes/platforms/whatsapp/session` directory contains full session credentials — protect it like a password
- Set file permissions: `chmod 700 ~/.hermes/platforms/whatsapp/session`
- Use a **dedicated phone number** for the bot to isolate risk from your personal account
- 如果您怀疑遭到入侵，请从 WhatsApp → 设置 → 链接设备中取消设备链接
- Phone numbers in logs are partially redacted, but review your log retention policy