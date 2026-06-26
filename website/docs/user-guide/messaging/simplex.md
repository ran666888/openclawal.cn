# SimpleX 聊天

[SimpleX Chat](https://simplex.chat/) 是一个私密的去中心化消息平台，用户可以在其中拥有自己的联系人和群组。与其他平台不同，SimpleX 不分配持久的用户 ID——每个联系人都由连接时生成的不透明内部 ID 进行标识，这使其成为最私密的即时通讯工具之一。

> 运行 `hermes gateway setup` 并选择 **SimpleX** 进行引导演练。

## 先决条件

- **simplex-chat** CLI 作为守护进程安装并运行
- Python 包 **websockets** (`pip install websockets`)

## 安装 simplex-chat

从 [simplex-chat GitHub 版本](https://github.com/simplex-chat/simplex-chat/releases) 页面下载最新版本：

````bash
# Linux / macOS 二进制文件
卷曲 -L https://github.com/simplex-chat/simplex-chat/releases/latest/download/simplex-chat-ubuntu-22_04-x86_64 -o simplex-chat
chmod +x simplex-聊天
````

SimpleX Chat 项目没有为聊天客户端发布预构建的 Docker 镜像；要在 Docker 下运行它，请从 [simplex-chat 存储库](https://github.com/simplex-chat/simplex-chat) 的源代码构建。

## 启动守护进程

````bash
单纯形聊天-p 5225
````

默认情况下，守护进程在“ws://127.0.0.1:5225”处侦听 WebSocket。

## 配置 OpenClaw

### 通过设置向导

````bash
Hermes网关设置
````

选择 **SimpleX Chat** 并按照提示操作。

### 通过环境变量

将这些添加到 `~/.hermes/.env` 中：

````
SIMPLEX_WS_URL=ws://127.0.0.1:5225
SIMPLEX_ALLOWED_USERS=<联系人 id-1>,<联系人 id-2>
SIMPLEX_HOME_CHANNEL=<联系人 ID>
````

|变量|必填|描述 |
|---|---|---|
| `SIMPLEX_WS_URL` |是的 | simplex-chat 守护进程的 WebSocket URL |
| `SIMPLEX_ALLOWED_USERS` |推荐|以逗号分隔的允许列表。每个条目可以是数字“contactId”**或**显示名称 - 两种形式都可以。 |
| `SIMPLEX_ALLOW_ALL_USERS` |可选|设置“true”以允许每次联系（谨慎使用）|
| `SIMPLEX_AUTO_ACCEPT` |可选|自动接受传入的联系请求（默认值：“true”）|
| `SIMPLEX_GROUP_ALLOWED` |可选|机器人参与的以逗号分隔的组 ID，或任何组的“*”。完全忽略群组消息 |
| `SIMPLEX_HOME_CHANNEL` |可选| cron 作业交付的默认联系人/组 ID |
| `SIMPLEX_HOME_CHANNEL_NAME` |可选|家庭频道的人性标签|
| `HERMES_SIMPLEX_TEXT_BATCH_DELAY` |可选|静默期秒数（默认值：“0.8”）用于将快速传入的短信连接到一个事件 |

## 查找您的联系人 ID 或显示名称

启动守护程序后，与您的代理联系人建立对话。数字“contactId”出现在会话日志中或通过“hermes send_message action=list”出现。如果您更愿意使用 SimpleX UI 中显示的显示名称，那也可以 - `SIMPLEX_ALLOWED_USERS` 接受任一形式。

## 授权

默认情况下**所有联系都被拒绝**。您必须：

1. 将“SIMPLEX_ALLOWED_USERS”设置为“contactId”和/或显示名称的逗号分隔列表（例如“SIMPLEX_ALLOWED_USERS=4,alice”与 contactId 4 或显示名称为“alice”的联系人匹配），或者
2. 使用 **DM 配对** — 向机器人发送任何消息，它会回复配对代码。通过“hermespairingapprovesimplex<CODE>”输入该代码。

## 群聊

默认情况下，适配器会忽略群组消息 - 否则群组中的机器人
处理每个成员的流量。明确选择加入：

````
SIMPLEX_GROUP_ALLOWED=12,34 # 特定组 ID
# 或
SIMPLEX_GROUP_ALLOWED=* # 机器人所在的任何组
````

通过在聊天 ID 前加上“group:”前缀来寻址群组，例如
`send_message` 中的 `simplex:group:12` 或作为 cron `deliver=` 目标。

## 附件

该适配器支持两个方向的本机 SimpleX 附件：

- **入站** — 传入的图像、语音注释和文件通过
  守护进程的 XFTP 流程（`rcvFileDecrReady`→`/freeceive`→等待
  `rcvFileComplete`) 并显示为 `MessageEvent.media_urls`
  适当的“消息类型”（“照片”、“语音”、“文本”+文档）。
- **出站** — `send_image_file`、`send_voice`、`send_document` 和
  `send_video` 都使用结构化的 `/_send` 形式和 `filePath`，所以
  接收 SimpleX 客户端内联渲染图像并播放语音
  内联注释而不是提供下载。

代理回复还可以在纯文本中嵌入“MEDIA:/path/to/file”标签 -
适配器从正文中剥离标签并将文件作为
语音注释（音频扩展）或文档。

## 将 SimpleX 与 cron 作业结合使用

````蟒蛇
定时任务（
    动作=“创建”，
    时间表=“每1小时”，
    Deliver="simplex", # 使用 SIMPLEX_HOME_CHANNEL
    提示=“检查警报并总结。”
）
````

或定位特定联系人：

````蟒蛇
send_message(target="simplex:<contact-id>", message="完成！")
````

## 隐私说明

- SimpleX 绝不会透露电话号码或电子邮件地址 - 联系人使用不透明的 ID
- OpenClaw 和守护进程之间的连接是本地 WebSocket (`ws://127.0.0.1:5225`) — 没有数据离开您的机器
- 消息在到达守护进程之前通过 SimpleX 协议进行端到端加密

## 故障排除

**“无法到达守护程序”** — 确保 `simplex-chat -p 5225` 正在运行并且端口与 `SIMPLEX_WS_URL` 匹配。

**“未安装 websockets”** — 运行 `pip install websockets`。

**未收到消息** — 检查联系人 ID 是否在“SIMPLEX_ALLOWED_USERS”中，或通过 DM 配对批准他们。