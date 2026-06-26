#ntfy

[ntfy](https://ntfy.sh/) 是一个简单的基于 HTTP 的 pub-sub 通知服务。它与“ntfy.sh”的免费公共服务器或任何自托管实例配合使用，并支持任何可以发出 HTTP 请求的客户端 - 电话、浏览器、脚本、手表。

ntfy 为 OpenClaw 提供了一个很棒的轻量级推送通道：从 [ntfy 移动应用程序](https://ntfy.sh/docs/subscribe/phone/) 订阅主题，向该主题发送消息以与客服人员交谈，然后在手机上获取响应。

> 运行“hermes gateway setup”并选择 **ntfy** 进行引导式演练。

## 先决条件

- 主题名称（任何唯一的字符串 - `hermes-myname-2026` 都可以）
- 安装了 [ntfy 移动应用程序](https://ntfy.sh/docs/subscribe/phone/) 并订阅了该主题
- 可选：自托管 ntfy 服务器，或用于私有/保留主题的“ntfy.sh”帐户令牌

就是这样。没有 SDK，没有守护进程，没有 Node.js。该适配器使用“httpx”，它已经是 OpenClaw 依赖项。

## 配置 OpenClaw

### 通过设置向导

````bash
Hermes网关设置
````

选择 **ntfy** 并按照提示操作。

### 通过环境变量

将这些添加到 `~/.hermes/.env` 中：

````
NTFY_TOPIC=hermes-myname-2026
NTFY_ALLOWED_USERS=hermes-myname-2026
NTFY_HOME_CHANNEL=hermes-myname-2026
````

|变量|必填|描述 |
|---|---|---|
| `NTFY_TOPIC` |是的 |要订阅的主题（传入消息）|
| `NTFY_SERVER_URL` |可选|服务器 URL（默认：`https://ntfy.sh`）— 指向自托管 ntfy 以保护隐私 |
| `NTFY_TOKEN` |可选|用于基本身份验证的承载令牌（例如`tk_xyz`）或`user:pass`
| `NTFY_PUBLISH_TOPIC` |可选|传出回复的不同主题（默认为“NTFY_TOPIC”）|
| `NTFY_MARKDOWN` |可选|设置“true”以发送带有“X-Markdown: true”标头的回复 |
| `NTFY_ALLOWED_USERS` |推荐|允许以逗号分隔的主题名称（视为用户 ID；见下文）|
| `NTFY_ALLOW_ALL_USERS` |可选|设置“true”以允许每个发布者 - 仅对具有读取令牌的私有主题安全 |
| `NTFY_HOME_CHANNEL` |可选| cron/通知传递的默认主题 |
| `NTFY_HOME_CHANNEL_NAME` |可选|家庭频道的人性标签|

## 身份模型 — 在部署之前阅读此内容

ntfy 没有本机经过身份验证的用户身份。已发布消息上的“标题”字段由**发布者控制**，可以是发件人想要的任何内容。 OpenClaw 适配器不使用“title”进行授权 - 它会让任何知道该主题的发布者欺骗允许的用户。

相反，**主题名称本身就是身份**。发布到主题的每条消息都被视为来自同一逻辑用户（主题）。因此，“NTFY_ALLOWED_USERS”通常只是主题名称本身 - 一个控制整个通道的单条目允许列表。

这意味着**任何知道该主题的人都可以与代理交谈**。为了使其成为真正的信任边界：

- **自托管 ntfy** 并使用 [访问控制](https://docs.ntfy.sh/config/#access-control) 锁定主题。只有具有读/写令牌的授权客户端才能发布。
- 或者 **在 ntfy.sh 上使用私有主题**（[保留主题](https://docs.ntfy.sh/publish/#reserved-topics) 需要一个帐户）并使用“NTFY_TOKEN”保护它。
- 或者**选择一个长的、不可猜测的主题名称**（`hermes-7d4f9c8b-2026`）并将其视为共享秘密。这是最简单的设置，但主题名称会通过任何日志或屏幕截图泄漏。

在所有情况下，请勿通过 ntfy 放置敏感数据，除非底层主题受到访问控制。

## 快速启动 — 通过手机与您的代理交谈

1. 选择主题名称：`hermes-myname-2026`
2. 在手机上：安装【ntfy app】(https://ntfy.sh/docs/subscribe/phone/)，点击**+**，输入`hermes-myname-2026`
3. 在主机上：
   ````bash
   echo 'NTFY_TOPIC=hermes-myname-2026' >> ~/.hermes/.env
   echo 'NTFY_ALLOWED_USERS=hermes-myname-2026' >> ~/.hermes/.env
   Hermes网关重启
   ````
4. 从 ntfy 应用程序中，向主题发送消息。代理的回复以推送通知的形式发送。

## 将 ntfy 与 cron 作业结合使用

一旦设置了“NTFY_HOME_CHANNEL”，cron 作业就可以传送到 ntfy：

````蟒蛇
定时任务（
    动作=“创建”，
    时间表=“每1小时”，
    Deliver="ntfy", # 使用 NTFY_HOME_CHANNEL
    提示=“检查警报并总结。”
）
````

或者明确针对特定主题：

````蟒蛇
send_message(target="ntfy:alerts-channel", message="完成！")
````

即使 cron 在网关的进程外运行时，这也能正常工作——插件注册一个“standalone_sender_fn”来打开自己的 HTTP 连接。

## 自托管ntfy

如果你想完全控制：

````bash
# 码头工人
docker run -p 80:80 -it binwiederhier/ntfy 服务

# 原生
去安装 heckel.io/ntfy/v2@latest
ntfy服务
````

然后把赫尔墨斯指向它：

````
NTFY_SERVER_URL=https://ntfy.mydomain.com
NTFY_TOPIC=爱马仕
NTFY_TOKEN=tk_abc123 # 如果您设置了访问控制
````

自托管为您提供主题访问控制、消息持久性策略、附件和表情符号标签。请参阅 [ntfy 服务器文档](https://docs.ntfy.sh/install/)。

## Markdown 格式

当发布者设置“X-Markdown: true”标头时，ntfy 客户端会呈现 Markdown。要启用外出 OpenClaw 回复：

````
NTFY_MARKDOWN=true
````

或者在`config.yaml`中：

````yaml
平台：
  ntfy:
    额外：
      降价：正确
````

该移动应用程序支持 CommonMark 的子集 - 粗体、斜体、列表、链接、围栏代码块。有关确切的设置，请参阅 [ntfy 的 markdown 文档](https://docs.ntfy.sh/publish/#markdown-formatting)。

## 仅传出设置（没有入站通知）

如果您只想让 OpenClaw *推送*通知到 ntfy（cron 摘要、警报）并且从不接受返回消息，请将“NTFY_TOPIC”和“NTFY_PUBLISH_TOPIC”设置为相同的值并完全跳过“NTFY_ALLOWED_USERS”。如果没有许可名单，代理永远不会响应入站消息 - 您的手机会收到推送，但对话是单向的。

## 限制

- **消息大小**：ntfy 将消息正文上限限制为 4096 个字符。当超过这个值时，OpenClaw 会截断并发出警告。
- **无输入指示符**：协议不公开； `send_typing` 是一个空操作。
- **没有线程或附件**：ntfy 是普通的推送通知。长回复保留在消息正文中，没有线程扇出。
- **没有本机用户身份**：请参阅上面的身份模型部分。

## 故障排除

**身份验证失败/401** — `NTFY_TOKEN` 错误，或者令牌没有此主题的发布/订阅权限。适配器在 401 上停止其重新连接循环，并且网关运行时状态将显示“致命：ntfy_unauthorized”。修复令牌并重新启动网关。

**未找到主题/404** — 配置的服务器上不存在“NTFY_TOPIC”。对于 ntfy.sh，主题是在首次发布时自动创建的，因此 404 意味着您指向未配置主题的自托管服务器。适配器通过“fatal: ntfy_topic_not_found”停止其重新连接循环。

**已连接，但没有消息** — 检查“NTFY_ALLOWED_USERS”是否包含主题名称本身。使用ntfy的身份模型，主题就是用户；将允许列表留空会拒绝所有内容。

**每 60 秒重新连接一次** — 流保活默认为 55 秒； ntfy 可能会出现间歇性网络问题。适配器应用指数退避（2 → 5 → 10 → 30 → 60 秒），并在流保持活动状态≥60 秒后重置为 0。