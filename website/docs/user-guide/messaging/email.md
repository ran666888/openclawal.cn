---
sidebar_position: 7
title: "Email"
description: "通过 IMAP/SMTP 将 OpenClaw 设置为邮件助手"
---
# 电子邮件设置

OpenClaw 可以使用标准 IMAP 和 SMTP 协议接收和回复电子邮件。向代理的地址发送电子邮件，它会在线程中回复 - 不需要特殊的客户端或机器人 API。适用于 Gmail、Outlook、Yahoo、Fastmail 或任何支持 IMAP/SMTP 的提供商。

:::info 仅网关适配器：无外部依赖项
本页介绍电子邮件网关适配器，它使用 Python 的内置“imaplib”、“smtplib”和“email”模块。此网关路径不需要额外的包或外部服务。
:::

这与捆绑的 [Himalaya 电子邮件技能](/docs/user-guide/skills/bundled/email/email-himalaya) 是分开的，后者允许代理通过终端命令管理电子邮件，并需要外部“himalaya”CLI 和喜马拉雅配置文件。

|使用案例|需要配置什么 |外部依赖|
|---|---|---|
|让人们向 OpenClaw 代理商发送电子邮件并收到回复 |此页上的电子邮件网关适配器 |除了 IMAP/SMTP 电子邮件帐户之外没有任何其他选项 |
|让代理通过终端工具检查、撰写、移动和管理邮箱消息 |喜马拉雅邮件技巧 | `himalaya` CLI 和 `~/.config/himalaya/config.toml` |

---

## 先决条件

- **为您的爱马仕代理商提供专用电子邮件帐户**（请勿使用您的个人电子邮件）
- **在电子邮件帐户上启用 IMAP**
- **应用程序密码**（如果使用 Gmail 或其他具有 2FA 的提供商）

### Gmail 设置

1. 在您的 Google 帐户上启用双因素身份验证
2. 前往[应用程序密码](https://myaccount.google.com/apppasswords)
3. 创建新的应用程序密码（选择“邮件”或“其他”）
4. 复制 16 个字符的密码 — 您将使用此密码代替常规密码

### Outlook / Microsoft 365

1.进入【安全设置】(https://account.microsoft.com/security)
2. 启用 2FA（如果尚未激活）
3. 在“其他安全选项”下创建应用程序密码
4. IMAP 主机：`outlook.office365.com`，SMTP 主机：`smtp.office365.com`

### 其他提供商

大多数电子邮件提供商都支持 IMAP/SMTP。检查您的提供商的文档：
- IMAP 主机和端口（通常是带有 SSL 的端口 993）
- SMTP 主机和端口（通常为带有 STARTTLS 的端口 587）
- 是否需要应用程序密码

---

## 第 1 步：配置 OpenClaw

最简单的方法：

````bash
Hermes网关设置
````

从平台菜单中选择**电子邮件**。该向导会提示您输入电子邮件地址、密码、IMAP/SMTP 主机和允许的发件人。

### 手动配置

添加到`~/.hermes/.env`：

````bash
# 必填
EMAIL_ADDRESS=hermes@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop # 应用程序密码（不是您的常规密码）
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com

# 安全（推荐）
EMAIL_ALLOWED_USERS=your@email.com,colleague@work.com

# 可选
EMAIL_IMAP_PORT=993 # 默认值：993（IMAP SSL）
EMAIL_SMTP_PORT=587 # 默认值：587（SMTP STARTTLS）
EMAIL_POLL_INTERVAL=15 # 收件箱检查之间的秒数（默认值：15）
EMAIL_HOME_ADDRESS=your@email.com # cron 作业的默认传送目标
````

---

## 步骤 2：启动网关

````bash
Hermes gateway # 在前台运行
hermes gateway install # 作为用户服务安装
sudo hermes gateway install --system # 仅适用于 Linux：启动时系统服务
````

启动时，适配器：
1. 测试IMAP和SMTP连接
2. 将所有现有收件箱邮件标记为“已读”（仅处理新电子邮件）
3. 开始轮询新消息

---

## 它是如何工作的

### 接收消息

适配器以可配置的时间间隔（默认值：15 秒）轮询 IMAP 收件箱中是否有 UNSEEN 消息。对于每封新电子邮件：

- **主题行**作为上下文包含在内（例如“[主题：部署到生产]”）
- **回复电子邮件**（主题以“Re:”开头）跳过主题前缀 - 线程上下文已建立
- **附件**在本地缓存：
  - 图像（JPEG、PNG、GIF、WebP）→ 可用于视觉工具
  - 文档（PDF、ZIP 等）→ 可用于文件访问
- **仅 HTML 电子邮件** 已删除标签以进行纯文本提取
- **自我消息**被过滤掉以防止回复循环
- **自动/noreply 发件人** 会被默默忽略 — `noreply@`、`mailer-daemon@`、`bounce@`、`no-reply@` 以及带有 `Auto-Subscribed`、`Precedence:bulk` 或 `List-Unsubscribe` 标头的电子邮件

### 发送回复

回复通过 SMTP 使用正确的电子邮件线程发送：

- **In-Reply-To** 和 **References** 标头维护线程
- **主题行** 保留“Re:”前缀（没有双“Re: Re:”）
- **消息 ID** 使用代理域生成
- 响应以纯文本 (UTF-8) 形式发送

### 文件附件

代理可以在回复中发送文件附件。在响应中包含“MEDIA:/path/to/file”，文件将附加到外发电子邮件中。

### 跳过附件

要忽略所有传入附件（为了恶意软件防护或节省带宽），请添加到您的“config.yaml”：

````yaml
平台：
  电子邮件：
    跳过附件：true
````

启用后，在有效负载解码之前会跳过附件和内联部分。电子邮件正文仍正常处理。

---

## 访问控制

默认情况下，电子邮件访问比聊天式平台更严格：

1. **`EMAIL_ALLOWED_USERS` 设置** → 仅处理来自这些地址的电子邮件
2. **未设置白名单** → 未知发件人将被默默忽略
3. **`EMAIL_ALLOW_ALL_USERS=true`** → 接受任何发件人（谨慎使用）
4. **`platforms.email.unauthorized_dm_behavior:pair`** → 未知发件人收到配对码

:::警告
**使用专用收件箱并配置“EMAIL_ALLOWED_USERS”以实现正常操作。**电子邮件配对是可选的，因为共享收件箱通常包含不相关的未读消息，并且默认情况下 OpenClaw 不应回复这些联系人。
:::

---

## 故障排除

|问题 |解决方案 |
|---------|----------|
| **启动时“IMAP 连接失败”** |验证“EMAIL_IMAP_HOST”和“EMAIL_IMAP_PORT”。确保帐户上启用了 IMAP。对于 Gmail，请在“设置”→“转发和 POP/IMAP”中启用它。 |
| **启动时“SMTP 连接失败”** |验证“EMAIL_SMTP_HOST”和“EMAIL_SMTP_PORT”。检查您的密码是否正确（使用 Gmail 的应用程序密码）。 |
| **未收到消息** |检查“EMAIL_ALLOWED_USERS”是否包含发件人的电子邮件。检查垃圾邮件文件夹——一些提供商标记了自动回复。 |
| **“身份验证失败”** |对于 Gmail，您必须使用应用程序密码，而不是常规密码。确保首先启用 2FA。 |
| **重复回复** |确保只有一个网关实例正在运行。检查“hermes网关状态”。 |
| **反应慢** |默认轮询间隔为 15 秒。使用“EMAIL_POLL_INTERVAL=5”减少以获得更快的响应（但有更多的 IMAP 连接）。 |
| **回复不跟帖** |适配器使用 In-Reply-To 标头。某些电子邮件客户端（尤其是基于网络的）可能无法正确处理自动消息。 |

---

## 安全

:::警告
**使用专用电子邮件帐户。** 不要使用您的个人电子邮件 - 代理将密码存储在“.env”中，并通过 IMAP 拥有完整的收件箱访问权限。
:::

- 使用 **应用程序密码** 而不是您的主密码（使用 2FA 的 Gmail 需要）
- 设置“EMAIL_ALLOWED_USERS”以限制谁可以与代理交互
- 密码存储在 `~/.hermes/.env` 中 — 保护此文件 (`chmod 600`)
- 默认情况下，IMAP 使用 SSL（端口 993），SMTP 使用 STARTTLS（端口 587）——连接已加密

---

## 环境变量参考

|变量|必填|默认 |描述 |
|----------|----------|---------|------------|
| `EMAIL_ADDRESS` |是的 | — |代理的电子邮件地址 |
| `EMAIL_PASSWORD` |是的 | — |邮箱密码或应用程序密码 |
| `EMAIL_IMAP_HOST` |是的 | — | IMAP 服务器主机（例如“imap.gmail.com”）|
| `EMAIL_SMTP_HOST` |是的 | — | SMTP 服务器主机（例如“smtp.gmail.com”）|
| `EMAIL_IMAP_PORT` |没有 | `993` | IMAP 服务器端口 |
| `EMAIL_SMTP_PORT` |没有 | `587` | SMTP 服务器端口 |
| `EMAIL_POLL_INTERVAL` |没有 | `15` |收件箱检查之间的秒数 |
| `EMAIL_ALLOWED_USERS` |没有 | — |以逗号分隔的允许发件人地址 |
| `EMAIL_HOME_ADDRESS` |没有 | — | cron 作业的默认交付目标 |
| `EMAIL_ALLOW_ALL_USERS` |没有 | `假` |允许所有发件人（不推荐）|