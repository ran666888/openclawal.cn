---
sidebar_position: 17
title: "LINE"
description: "将 OpenClaw 设置为 LINE 消息 API 机器人"
---
# 线路设置

通过官方 LINE Messaging API 将 OpenClaw 作为 [LINE](https://line.me/) 机器人运行。该适配器作为“plugins/platforms/line/”下的捆绑平台插件存在 - 无需核心编辑，只需像任何其他平台一样启用它即可。

LINE 是日本、台湾和泰国占主导地位的消息应用程序。如果您的用户住在那里，这就是他们联系您的方式。

> 运行“hermes gateway setup”并选择 **LINE** 进行引导式演练。

## 机器人如何响应

|背景 |行为 |
|---------|----------|
| **1:1 聊天**（`U` ID）|回复每一条消息 |
| **群聊**（`C` ID）|当组位于允许名单上时进行响应 |
| **多用户房间**（`R` ID）|当房间位于许可名单上时做出响应 |

传入的文本、图像、音频、视频、文件、贴纸和位置都得到处理。出站文本首先使用**免费回复令牌**（一次性使用，约 60 秒的窗口），并在令牌过期时回退到计量推送 API。

---

## 第 1 步：创建 LINE Messaging API 通道

1. 进入[LINE开发者控制台](https://developers.line.biz/console/)。
2. 创建一个 Provider，然后在其下创建一个 **Messaging API** 通道。
3. 从频道的**基本设置**选项卡中，复制**频道密钥**。
4. 从 **Messaging API** 选项卡，滚动到 **Channel access token (long-lived)**，然后单击 **Issue**。复制令牌。
5. 在 **消息 API** 选项卡中，还禁用 **自动回复消息** 和 **问候消息**，这样它们就不会干扰您的机器人的回复。

---

## 步骤 2：公开 webhook 端口

LINE 通过公共 HTTPS 提供 Webhook。默认端口是“8646”——如果需要，可以用“LINE_PORT”覆盖。

````bash
# Cloudflare Tunnel（推荐用于生产 - 固定主机名）
cloudflared 隧道 --url http://localhost:8646

# ngrok（适合开发）
恩格洛克 http 8646

# 开发隧道
devtunnel 创建 Hermes-line --allow-anonymous
devtunnel端口创建hermes-line -p 8646 --协议 https
devtunnel 主机 Hermes-line
````

复制“https://...” URL — 您将其设置为下面的 Webhook URL。 **测试时保持隧道运行**。对于生产，设置一个固定的 Cloudflare 命名隧道，以便 Webhook URL 在重新启动时不会更改。

---

## 第三步：配置 OpenClaw

添加到`~/.hermes/.env`：

```环境
LINE_CHANNEL_ACCESS_TOKEN=YOUR_LONG_LIVED_TOKEN
LINE_CHANNEL_SECRET=您的_CHANNEL_SECRET

# 允许列表 — 至少其中之一（或 LINE_ALLOW_ALL_USERS=true 对于开发）
LINE_ALLOWED_USERS=U1234567890abcdef... # 逗号分隔的 U 前缀 ID
LINE_ALLOWED_GROUPS=C1234567890abcdef... # 可选组 ID
LINE_ALLOWED_ROOMS=R1234567890abcdef... # 可选房间 ID

# 图像/音频/视频发送所需 — 公共 HTTPS 基本 URL
# 隧道解析为。  没有它，send_image/voice/video 将拒绝。
LINE_PUBLIC_URL=https://my-tunnel.example.com
````

然后在`~/.hermes/config.yaml`中：

````yaml
网关：
  平台：
    线路：
      启用：真
````

这就足够了 - `gateway/config.py` 中的捆绑插件扫描会自动拾取 `plugins/platforms/line/`。没有 `Platform.LINE` 枚举编辑，没有 `_create_adapter` 注册。

---

## 步骤 4：设置 webhook URL

返回 LINE 控制台：

1. 打开您的频道 → **消息 API** 选项卡。
2. 在 **Webhook 设置** → **Webhook URL** 下，粘贴“https://<your-tunnel>/line/webhook”（注意“/line/webhook”路径 - 适配器会在此处侦听）。
3. 单击**验证**。 LINE ping URL；你应该看到 200。
4. 将 **使用 webhook** 切换为 **打开**。

---

## 步骤 5：运行网关

````bash
爱马仕网关
````

代理日志显示：

````
LINE：webhook 监听 0.0.0.0:8646/line/webhook（公共：https://my-tunnel.example.com）
````

从 LINE 应用程序将机器人添加为好友（扫描频道的 **Messaging API** 选项卡中的二维码）并向其发送消息。

---

## 法学硕士反应缓慢

LINE 的回复令牌是一次性的，并且在入站事件后大约 60 秒到期。速度慢的 LLM 无法及时回复，这通常会强制进行付费 Push API 调用。

当 LLM 仍在运行超过“LINE_SLOW_RESPONSE_THRESHOLD”秒（默认“45”）时，适配器会使用原始回复令牌来发送 **模板按钮** 气泡：

> 🤔 还在思考。准备好后，点击下面即可获取答案。
>
> [获取答案]

用户在方便时点击 **获取答案** - 回发会提供一个“新鲜”回复令牌，适配器使用该令牌发送缓存的答案（仍然免费）。

状态机：“PENDING → READY → DELIVERED”，加上“ERROR”以取消运行（孤立的“PENDING”在“/stop”之后解析为“运行在完成之前被中断”，因此持久按钮不会循环）。

要禁用回发按钮并始终改为推送回退：

```环境
LINE_SLOW_RESPONSE_THRESHOLD=0
````

为了可靠地触发回发流，请抑制会在阈值之前消耗回复令牌的喋喋不休：

````yaml
# ~/.hermes/config.yaml
显示：
  临时助理消息：假
  平台：
    线路：
      工具进度：关闭
````

---

## Cron/通知传递

```环境
LINE_HOME_CHANNEL=Uxxxxxxxxxxxxxxxxxxxxx # 默认投放目标
````

带有 `deliver: line` 的 Cron 作业路由到 `LINE_HOME_CHANNEL`。该适配器附带一个独立的仅推送发送器，因此即使 cron 作业在与网关不同的进程中运行，cron 作业也能正常工作。

---

## 环境变量引用

|变量|必填|默认 |描述 |
|---|---|---|---|
| `LINE_CHANNEL_ACCESS_TOKEN` |是的 | — |长期通道访问令牌 |
| `LINE_CHANNEL_SECRET` |是的 | — |通道秘密（HMAC-SHA256 webhook 验证）|
| `LINE_HOST` |没有| `0.0.0.0` | Webhook 绑定主机 |
| `LINE_PORT` |没有| `8646` | Webhook 绑定端口 |
| `LINE_PUBLIC_URL` |媒体 | — |公共 HTTPS 基本 URL；图像/语音/视频发送所需 |
| `LINE_ALLOWED_USERS` |之一 | — |逗号分隔的用户 ID（U 前缀） |
| `LINE_ALLOWED_GROUPS` |之一 | — |以逗号分隔的组 ID（C 前缀）|
| `LINE_ALLOWED_ROOMS` |之一 | — |逗号分隔的房间 ID（R 前缀）|
| `LINE_ALLOW_ALL_USERS` |仅限开发 | `假` |完全跳过白名单 |
| `LINE_HOME_CHANNEL` |没有| — |默认 cron/通知传递目标 |
| `LINE_SLOW_RESPONSE_THRESHOLD` |没有| `45` |回发按钮触发前的秒数（`0` = 禁用）|
| `LINE_PENDING_TEXT` |没有| “🤔还在想……” |回发按钮旁边显示的气泡文本 |
| `LINE_BUTTON_LABEL` |没有| “得到答案” |按钮标签|
| `LINE_DELIVERED_TEXT` |没有| 「已经回复了✅」|再次点击已发送按钮时回复 |
| `LINE_INTERRUPTED_TEXT` |没有| “运行在完成之前被中断。” |点击“/stop”孤立按钮时回复 |

---

## 故障排除

** webhook 验证上的“无效签名”。** `Channel Secret` 复制错误，或者您的隧道重写了请求正文。首先使用 `curl -i https://<tunnel>/line/webhook/health` 进行验证 - 应该返回 `{"status":"ok","platform":"line"}`。

**机器人在组中接收不到任何内容。** 检查“LINE_ALLOWED_GROUPS”是否包含“C...”组 ID。要查找组 ID，请发送测试消息并 grep `~/.hermes/logs/gateway.log` 查找“LINE：拒绝未经授权的源”——被拒绝的源字典具有 ID。

**`send_image` 失败，并显示“必须设置 LINE_PUBLIC_URL”。** LINE 的消息 API 不接受二进制上传 — 图像、音频和视频必须是可访问的 HTTPS URL。将“LINE_PUBLIC_URL”设置为隧道的公共主机名，适配器将自动从“/line/media/<token>/<filename>”提供文件。

**回发按钮永远不会出现。** LLM 响应速度快于“LINE_SLOW_RESPONSE_THRESHOLD”，或者另一个气泡（工具进度、流式传输）首先消耗了回复令牌。请参阅“LLM 响应缓慢”下的抑制块。

**“已被另一个配置文件使用”。** 相同的通道访问令牌绑定到另一个正在运行的 OpenClaw 配置文件。停止其他网关或使用单独的通道。

---

## 限制

* **气泡和长度上限。** 每个 LINE 文本气泡的上限为 5000 个字符。较长的响应被智能分块为约 4500 个字符，每个回复/推送调用最多 5 个气泡，尽可能在自然边界上分割。
* **没有本机消息编辑。** LINE 没有编辑消息 API — 流式响应始终发送新的气泡，从不编辑之前的气泡。
* **无 Markdown 渲染。** 粗体 (`**`)、斜体 (`*`)、代码围栏和标题呈现为文字字符。适配器在发送之前将它们剥离； URL 被保留（`[label](url)` 变为 `label (url)`）。
* **加载指示器仅适用于 DM。** LINE 拒绝群组和房间的聊天/加载 API，因此打字指示器仅在 1:1 聊天中显示。