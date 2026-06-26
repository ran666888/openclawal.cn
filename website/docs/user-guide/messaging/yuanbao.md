---
sidebar_position: 16
title: "Yuanbao"
description: "Connect OpenClaw to the Yuanbao enterprise messaging platform via WebSocket gateway"
---
#元宝

将 OpenClaw 连接至腾讯企业消息平台【元宝】(https://yuanbao.tencent.com/)。该适配器使用 WebSocket 网关进行实时消息传递，并支持直接 (C2C) 和群组对话。

:::信息
元宝是一个主要在腾讯和企业环境中使用的企业消息平台。它使用 WebSocket 进行实时通信、基于 HMAC 的身份验证，并支持包括图像、文件和语音消息在内的富媒体。
:::

## 先决条件

- 拥有机器人创建权限的元宝账户
- 元宝APP_ID和APP_SECRET（来自平台管理员）
- Python 包：`websockets` 和 `httpx`
- 对于媒体支持：`aiofiles`

安装所需的依赖项：

````bash
pip 安装 websockets httpx aiofiles
````

## 设置

### 1.在元宝中创建一个机器人

1.从[https://yuanbao.tencent.com/](https://yuanbao.tencent.com/)下载元宝APP
2. 在应用程序中，转到 **PAI → 我的机器人** 并创建一个新机器人
3、机器人创建完成后，复制**APP_ID**和**APP_SECRET**

### 2. 运行安装向导

配置元宝最简单的方法是通过交互式设置：

````bash
Hermes网关设置
````

出现提示时选择**元宝**。向导将：

1. 询问您的APP_ID
2. 询问您的 APP_SECRET
3.自动保存配置

:::提示
WebSocket URL 和 API 域具有内置的合理默认值。您只需提供 APP_ID 和 APP_SECRET 即可开始。
:::

### 3.配置环境变量

初始设置后，验证“~/.hermes/.env”中的这些变量：

````bash
# 必填
YUANBAO_APP_ID=您的应用程序 ID
YUANBAO_APP_SECRET=您的应用程序秘密
YUANBAO_WS_URL=wss://api.yuanbao.example.com/ws
YUANBAO_API_DOMAIN=https://api.yuanbao.example.com

# 可选：机器人帐户ID（通常从sign-token自动获取）
# YUANBAO_BOT_ID=你的机器人 ID

# 可选：内部路由环境（例如测试/登台/生产）
# YUANBAO_ROUTE_ENV=生产

# 可选：cron/通知的主频道（格式：direct:<account> 或 group:<group_code>）
YUANBAO_HOME_CHANNEL=direct:bot_account_id
YUANBAO_HOME_CHANNEL_NAME="机器人通知"

# 可选：限制访问（旧版，请参阅下面的访问控制以了解细粒度策略）
YUANBAO_ALLOWED_USERS=user_account_1,user_account_2
````

### 4.启动网关

````bash
爱马仕网关
````

适配器将连接到元宝WebSocket网关，使用HMAC签名进行身份验证，并开始处理消息。

## 特点

- **WebSocket 网关** — 实时双向通信
- **HMAC 身份验证** — 使用 APP_ID/APP_SECRET 进行安全请求签名
- **C2C 消息传递** — 用户与机器人的直接对话
- **群组消息传送** — 群组聊天中的对话
- **媒体支持** — 通过 COS（云对象存储）的图像、文件和语音消息
- **Markdown 格式** — 消息会根据元宝的大小限制自动分块
- **消息重复数据删除** — 防止重复处理同一消息
- **Heartbeat/keep-alive** — 保持 WebSocket 连接稳定性
- **键入指示器** — 在代理处理时显示“正在键入...”状态
- **自动重新连接** — 使用指数退避处理 WebSocket 断开连接
- **群组信息查询** — 检索群组详细信息和成员列表
- **贴纸/表情符号支持** — 在对话中发送 TIMFaceElem 贴纸和表情符号
- **自动设置主页** — 第一个向机器人发送消息的用户会自动设置为家庭频道所有者
- **慢响应通知** — 当代理花费的时间超过预期时发送等待消息

## 配置选项

### 聊天 ID 格式

元宝根据会话类型使用前缀标识符：

|聊天类型 |格式|示例|
|------------|--------|---------|
|私信（C2C） | `直接：<帐户>` | `直接：user123` |
|群留言| `组：<组代码>` | `组：grp456` |

### 媒体上传

元宝适配器自动处理通过COS（腾讯云对象存储）的媒体上传：

- **图像**：支持 JPEG、PNG、GIF、WebP
- **文件**：支持所有常见文档类型
- **语音**：支持WAV、MP3、OGG

媒体 URL 在上传之前会自动验证和下载，以防止 SSRF 攻击。

## 家庭频道

在任何元宝聊天（DM或群组）中使用“/sethome”命令将其指定为**主频道**。计划任务（cron 作业）将其结果传递到此通道。

:::提示自动设置主页
如果未配置主频道，则第一个向机器人发送消息的用户将自动设置为主频道所有者。如果当前家庭频道是群聊，则第一个DM会将其升级为直接频道。
:::

你也可以在`~/.hermes/.env`中手动设置：

````bash
YUANBAO_HOME_CHANNEL=直接:user_account_id
# 或对于一个组：
# YUANBAO_HOME_CHANNEL=group:group_code
YUANBAO_HOME_CHANNEL_NAME="我的机器人更新"
````

### 示例：设置家庭频道

1. 与元宝机器人开始对话
2.发送命令：`/sethome`
3. 机器人响应：“主频道设置为 [chat_name]，ID 为 [chat_id]。Cron 作业将传送到此位置。”
4. 未来的 cron 作业和通知将发送到此通道

### 示例：Cron 作业交付

创建一个 cron 作业：

````bash
/cron "0 9 * * *" 检查服务器状态
````

每天上午9点定时输出到您的元宝首页频道。

## 使用提示

### 开始对话

向元宝机器人发送任意消息：

````
你好
````

机器人在同一对话线程中做出响应。

### 可用命令

所有标准 OpenClaw 命令都适用于元宝：

|命令|描述 |
|---------|-------------|
| `/新` |开始新的对话 |
| `/model [提供者：模型]` |显示或更改型号 |
| `/sethome` |将此聊天设为主频道 |
| `/状态` |显示会话信息 |
| `/帮助` |显示可用命令 |

### 发送文件

要将文件发送到机器人，只需将其直接附加到元宝聊天中即可。机器人将自动下载并处理文件附件。

您还可以在附件中包含一条消息：

````
请分析一下这个文档
````

### 接收文件

当您要求机器人创建或导出文件时，它会将文件直接发送到您的元宝聊天室。

## 故障排除

### 机器人在线但不回复消息

**原因**：WebSocket 握手期间身份验证失败。

**修复**：
1.验证APP_ID和APP_SECRET是否正确
2. 检查WebSocket URL是否可访问
3. 确保机器人帐户具有适当的权限
4. 查看网关日志： `tail -f ~/.hermes/logs/gateway.log`

### “连接被拒绝”错误

**原因**：WebSocket URL 无法访问或不正确。

**修复**：
1. 验证 WebSocket URL 格式（应以“wss://”开头）
2、检查元宝API域的网络连通性
3.确认防火墙允许WebSocket连接
4. 测试 URL：`curl -I https://[YUANBAO_API_DOMAIN]`

### 媒体上传失败

**原因**：COS 凭证无效或媒体服务器无法访问。

**修复**：
1.验证API_DOMAIN是否正确
2. 检查您的机器人是否启用了媒体上传权限
3. 确保媒体文件可访问且未损坏
4. 通过平台管理员检查 COS 存储桶配置

### 消息未发送到主频道

**原因**：主频道 ID 格式不正确或 cron 作业尚未触发。

**修复**：
1. 验证YUANBAO_HOME_CHANNEL格式是否正确
2.使用`/sethome`命令进行测试以自动检测正确的格式
3. 使用 `/status` 检查 cron 作业计划
4. 验证机器人在目标聊天中具有发送权限

### 频繁断线

**原因**：WebSocket连接不稳定或网络不可靠。

**修复**：
1. 检查网关日志中的错误模式
2.连接设置中增加心跳超时
3、保证元宝API网络连接稳定
4. 考虑启用详细日志记录：`HERMES_LOG_LEVEL=debug`

## 访问控制

元宝支持DM和群组对话的细粒度访问控制：

````bash
# DM 策略：开放（默认）|允许名单 |残疾人
YUANBAO_DM_POLICY=开放
# 允许 DM 机器人的逗号分隔用户 ID（仅当 DM_POLICY=allowlist 时使用）
YUANBAO_DM_ALLOW_FROM=user_id_1,user_id_2

# 组策略：打开（默认）|允许名单 |残疾人
YUANBAO_GROUP_POLICY=开放
# 允许使用逗号分隔的组代码（仅当 GROUP_POLICY=allowlist 时使用）
YUANBAO_GROUP_ALLOW_FROM=group_code_1,group_code_2
````

这些也可以在`config.yaml`中设置：

````yaml
平台：
  元宝：
    额外：
      dm_policy：允许名单
      dm_allow_from: "用户1,用户2"
      组策略：打开
      group_allow_from：“”
````

## 高级配置

### 消息分块

元宝有最大消息大小。 OpenClaw 通过 Markdown 感知的分割自动对大型响应进行分块（尊重代码围栏、表格和段落边界）。

### 连接参数

以下连接参数内置于适配器中，并具有合理的默认值：

|参数|默认值 |描述 |
|------------|--------------|----------|
| WebSocket 连接超时 | 15 秒 |等待WS握手时间|
|心跳间隔| 30 秒 |保持连接活跃的 Ping 频率 |
|最大重新连接尝试次数 | 100 | 100最大重连尝试次数 |
|重新连接退避 | 1 秒 → 60 秒（指数）|重新连接尝试之间的等待时间 |
|回复心跳间隔 | 2 秒 | RUNNING状态发送频率|
|发送超时 | 30 秒 |出站 WS 消息超时 |

:::注意
目前无法通过环境变量配置这些值。它们针对典型的元宝部署进行了优化。
:::

### 详细日志记录

启用调试日志记录以解决连接问题：

````bash
HERMES_LOG_LEVEL=调试 Hermes 网关
````

## 与其他功能集成

### 计划任务

安排在元宝上运行的任务：

````
/cron "0 */4 * * *" 报告系统健康状况
````

结果将传送到您的家庭频道。

### 后台任务

运行长时间操作而不阻塞对话：

````
/background 分析存档中的所有文件
````

### 跨平台消息

从CLI向元宝发送消息：

````bash
hermes chat -q "发送'Hello from CLI'到yuanbao:group:group_code"
````

## 相关文档

- [消息网关概述](./index.md)
- [斜线命令参考](/reference/slash-commands)
- [Cron 作业](/user-guide/features/cron)
- [后台会话](/user-guide/cli#background-sessions)