---
sidebar_position: 18
---
# 光子 iMessage

通过 [Photon][photon] 将 OpenClaw 连接到 **iMessage**，这是一个托管的
处理 Apple 线路分配和滥用预防的服务
层，这样您就不必运行自己的 Mac 中继。

免费套餐使用 Photon 的共享 iMessage 线路池 — 不同
收件人可能会看到不同的发送号码，但每次对话
保持稳定。付费商业层为每个用户提供相同的
专用号码；该插件同时支持两者，免费套餐是
推荐的起点。

:::info 免费开始
Photon 的共享线路池是免费的。无需订阅即可发送
您来自 OpenClaw 的第一条 iMessage — 只是我们可以绑定的电话号码
你的帐户。
:::

## 架构

Photon 是一个**持久连接**通道，就像 Discord 或 Slack —
**没有网络钩子，没有公共 URL，没有需要管理的签名密钥。**

`spectrum-ts` SDK 为 Photon 保留了一个长期存在的 **gRPC 流**
两个方向。由于该 SDK 仅支持 TypeScript，因此 OpenClaw 在
小型受监督的 **Node sidecar** 并通过环回与其进行对话：

- **入站** — sidecar 消耗 SDK 的 `app.messages` gRPC
  流并通过环回将每条消息转发到 Python 适配器
  `GET /入站` (NDJSON)。适配器进行重复数据删除并将其分派到
  代理，如果流丢失，会自动重新连接。
- **出站** — 回复是对 sidecar 的环回 POST，它调用
  SDK 上的“space.send(...)”。

Python插件启动、监督和关闭sidecar
自动。

## 先决条件

- Photon 帐户 — 在 [app.photon.codes][app] 注册
- PATH 上的 **Node.js 18.17 或更高版本**（`node --version`）
- 可以接收iMessage的手机号码（用于绑定账号）

就是这样 - 无需设置公共 URL 或隧道。

## 首次设置

运行统一网关向导并选择 **Photon iMessage**：

````bash
Hermes网关设置
````

…或者直接运行 Photon 设置（向导调用相同的流程）：

````bash
# 设备代码登录+项目+用户+sidecar deps，全部合二为一
爱马仕光子设置--电话+15551234567
````

设置，按顺序：

1. **设备登录** (`client_id=photon-cli`) — 打开
   `https://app.photon.codes/` 用于批准并存储不记名令牌。
2. **在您的帐户上查找或创建** `Hermes Agent` 项目。
3. **启用Spectrum**，读取项目的Spectrum id，并轮换
   项目的秘密。
4. **将您的电话号码**注册为 Spectrum 用户 — 如果出现则跳过
   该号码的用户已经存在，因此重新运行是安全的。
5. **打印您指定的 iMessage 线路** — 您发短信要联系的号码
   你的代理人。
6. **在插件的 sidecar 目录中运行 `npm install`**。

运行时凭证写入“~/.hermes/.env”
（`PHOTON_PROJECT_ID` = Spectrum 项目 ID、`PHOTON_PROJECT_SECRET`），
所有其他通道都将其令牌保存在同一位置。管理元数据
（设备令牌、仪表板项目 ID）位于“~/.hermes/auth.json”下
`credential_pool.photon` / `credential_pool.photon_project`。

## 授权用户

Photon 使用与其他 OpenClaw 相同的授权模型
频道。选择一种方法：

**DM 配对（默认）。** 当未知号码向您的 Photon 发送消息时
线路上，爱马仕回复了一个配对码。批准它：

````bash
爱马仕配对批准光子<代码>
````

使用“hermes 配对列表”查看待处理的代码和已批准的用户。

**预授权特定号码**（在`~/.hermes/.env`中）：

````bash
PHOTON_ALLOWED_USERS=+15551234567,+15559876543
````

**开放访问**（仅限开发，在`~/.hermes/.env`中）：

````bash
PHOTON_ALLOW_ALL_USERS=true
````

当设置“PHOTON_ALLOWED_USERS”时，未知发件人将被静默
忽略而不是提供配对代码（白名单表明您
故意限制访问）。

### 需要在群聊中提及

默认情况下，OpenClaw 会响应每个授权的 DM 和群组消息。
要选择加入群聊，请启用提及门控（DM 仍然始终
工作）：

````yaml
网关：
  平台：
    光子：
      启用：真
      要求提及：true
````

使用“require_mention: true”，群聊消息将被忽略，除非
它们与唤醒词模式匹配。默认匹配 `Hermes` 和
`@Hermes Agent` 变体。对于自定义代理名称，设置正则表达式模式：

````yaml
网关：
  平台：
    光子：
      要求提及：true
      提及模式：
        - '(?<![\w@])@?amos\b[,:\-]?'
````

两个键也接受环境变量（`PHOTON_REQUIRE_MENTION`，
`PHOTON_MENTION_PATTERNS`）。这是相同的提及门控模型
BlueBubbles iMessage 频道使用。

## 启动网关

````bash
爱马仕网关启动
````

你会看到类似的东西：

````
[photon]已连接 — sidecar 位于 127.0.0.1:8789，通过 gRPC 入站流式传输
````

发送 iMessage 至您指定的号码，OpenClaw 将会回复。

## 状态和故障排除

````bash
赫尔墨斯光子状态
````

打印保存的凭据、Sidecar 运行状况、您的注册号码以及
OpenClaw 使用指定的 iMessage 线路。当 Photon 代币和仪表板项目
可用，“状态”刷新仪表板中缺失的数字行
无需配置新线路。

````
光子 iMessage 状态
──────────────────────
  设备令牌：✓ 已存储
  仪表板项目：3c90c3cc-0d44-4b50-...
  频谱项目 ID：sp-...
  项目秘密：✓ 已存储
  我的号码：+15551234567
  指定号码：+16282679185
  节点二进制文件：/usr/bin/node
  Sidecar 部门：✓ 已安装
````

常见问题：

- **`sidecar deps : ✗ 运行 hermes photon install-sidecar`** — 节点是
  已安装，但未安装“spectrum-ts”。运行建议的命令。
- **`设备令牌：✗丢失`** — 运行`hermes photon setup`来登录。
- **`尚未分配 iMessage 线路`** — 频谱已启用，但没有线路
  已提供；重新运行 `hermes photon setup` 或检查
  [仪表板][应用程序]。
- **Sidecar 无法启动** — 确认 `node --version` 是 18.17+ 并且
  `hermes photon install-sidecar` 已完成，没有错误。

## 今天的限制

- **入站附件仅包含元数据。**入站事件携带
  文件名 + MIME 类型；代理看到标记但还无法读取
  字节。 SDK 通过“content.read()”公开附件字节，因此
  是 sidecar 的后续。
- **支持出站附件。** OpenClaw 发送图像、语音
  通过spectrum-ts' `attachment()` / 进行笔记、视频和文档
  通过 sidecar 的 `/send-attachment` 构建 `voice()` 内容
  端点。字幕以单独的 iMessage 气泡形式在
  媒体。
- **Photon 的免费配额：** 每台服务器每天 5,000 条消息，
  每条共享线路每天发起 50 个新对话。增加
  可用 — 发送电子邮件至“help@photon.codes”。

## 环境变量

|变量|默认|笔记|
|----------------------------|--------------------------------|--------------------------------------------------------|
| `PHOTON_PROJECT_ID` |来自 `.env` | Spectrum 项目 ID（SDK 的“projectId”）；通过设置| 设置
| `PHOTON_PROJECT_SECRET` |来自 `.env` |项目秘密；通过设置|设置
| `PHOTON_SIDECAR_PORT` | `8789` | sidecar控制环回端口+入站通道|
| `PHOTON_SIDECAR_AUTOSTART`| `真实` |适配器是否生成 sidecar |
| `PHOTON_NODE_BIN` | `哪个节点` |覆盖节点二进制路径 |
| `PHOTON_HOME_CHANNEL` | （未设置）| cron /通知的默认空间ID |
| `PHOTON_HOME_CHANNEL_NAME`| （未设置）|家庭频道的人性标签|
| `PHOTON_ALLOWED_USERS` | （未设置）|以逗号分隔的 E.164 允许列表 |
| `PHOTON_ALLOW_ALL_USERS` | `假` |仅限开发人员 — 接受任何发件人 |
| `PHOTON_REQUIRE_MENTION` | `假` |分组响应之前需要唤醒词 |
| `PHOTON_MENTION_PATTERNS` |爱马仕唤醒词|用于组提及的 JSON 列表/逗号/换行符正则表达式模式 |
| `PHOTON_DASHBOARD_HOST` | `app.photon.codes` |覆盖仪表板/设备登录主机 |
| `PHOTON_SPECTRUM_HOST` | `spectrum.photon.codes` |覆盖 Spectrum API 主机 |

[光子]：https://photon.codes/
[应用程序]：https://app.photon.codes/