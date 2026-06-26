---
sidebar_position: 15
---
# WeCom回调（自建App）

使用回调/webhook模型将OpenClaw连接到WeCom（企业微信）作为自建企业应用。

:::info WeCom 机器人与 WeCom 回调
OpenClaw 支持两种 WeCom 集成模式：
- **[WeCom Bot](wecom.md)** — 机器人风格，通过 WebSocket 连接。设置更简单，适用于群聊。
- **WeCom Callback**（本页）——自建应用程序，接收加密的 XML 回调。在用户的 WeCom 侧边栏中显示为一流应用程序。支持多公司路由。
:::

另请参阅：[WeCom Bot](./wecom.md) 了解机器人风格的集成。

> 运行“hermes gateway setup”并选择 **WeCom Callback** 进行引导式演练。

## 它是如何工作的

1.您在WeCom管理控制台注册一个自建应用
2. WeCom 将加密的 XML 推送到您的 HTTP 回调端点
3. OpenClaw解密消息，将其排队等待代理
4. 立即确认（静默 — 不向用户显示任何内容）
5. 代理处理请求（通常 3-30 分钟）
6. 通过 WeCom `message/send` API 主动发送回复

## 先决条件

- 具有管理员访问权限的 WeCom 企业帐户
- `aiohttp` 和 `httpx` Python 包（包含在默认安装中）
- 用于回调 URL 的可公开访问的服务器（或类似 ngrok 的隧道）

## 设置

### 1.在WeCom中创建一个自建应用

1.进入【微信管理控制台】(https://work.weixin.qq.com/) → **应用程序** → **创建应用程序**
2.记下您的**公司 ID**（显示在管理控制台顶部）
3. 在应用程序设置中，创建 **Corp Secret**
4. 记下应用程序概述页面中的 **代理 ID**
5. 在**接收消息**下，配置回调 URL：
   - URL：`http://YOUR_PUBLIC_IP:8645/wecom/callback`
   - 令牌：生成随机令牌（WeCom 提供一个）
   - EncodingAESKey：生成密钥（WeCom 提供一个）

### 2.配置环境变量

添加到您的“.env”文件：

````bash
WECOM_CALLBACK_CORP_ID=您的公司 ID
WECOM_CALLBACK_CORP_SECRET=您的公司秘密
WECOM_CALLBACK_AGENT_ID=1000002
WECOM_CALLBACK_TOKEN=您的回调令牌
WECOM_CALLBACK_ENCODING_AES_KEY=您的 43-char-aes-key

# 可选
WECOM_CALLBACK_HOST=0.0.0.0
WECOM_CALLBACK_PORT=8645
WECOM_CALLBACK_ALLOWED_USERS=用户1,用户2
````

### 3.启动网关

````bash
爱马仕网关
````

（只有在“hermes gateway install”注册了systemd/launchd服务后才可以使用“hermes gateway start”。）

回调适配器在配置的端口上启动 HTTP 服务器。 WeCom 将通过 GET 请求验证回调 URL，然后开始通过 POST 发送消息。

## 配置参考

在“platforms.wecom_callback.extra”下的“config.yaml”中设置这些，或使用环境变量：

|设置|默认 |描述 |
|---------|---------|-------------|
| `corp_id` | — |微信企业法人ID（必填）|
| `公司秘密` | — |自建应用的企业机密（必填）|
| `agent_id` | — |自建应用Agent ID（必填）|
| `令牌` | — |回调验证令牌（必填）|
| `encoding_aes_key` | — |用于回调加密的 43 字符 AES 密钥（必需）|
| `主机` | `0.0.0.0` | HTTP回调服务器绑定地址 |
| `端口` | `8645` | HTTP 回调服务器的端口 |
| `路径` | `/wecom/callback` |回调端点的 URL 路径 |

## 多应用路由

对于运行多个自建应用程序（例如跨不同部门或子公司）的企业，请在 config.yaml 中配置 apps 列表：

````yaml
平台：
  wecom_callback：
    启用：真
    额外：
      主机：“0.0.0.0”
      端口：8645
      应用程序：
        - 名称：“a 部门”
          corp_id：“ww_corp_a”
          corp_secret：“秘密-a”
          代理 ID：“1000002”
          令牌：“令牌-a”
          coding_aes_key: "key-a-43-chars..."
        - 名称：“b 部”
          corp_id：“ww_corp_b”
          corp_secret：“秘密-b”
          代理 ID：“1000003”
          令牌：“令牌-b”
          coding_aes_key: "key-b-43-chars..."
````

用户按“corp_id:user_id”确定范围，以防止跨公司冲突。当用户发送消息时，适配器会记录他们所属的应用程序（公司），并通过正确的应用程序的访问令牌路由回复。

## 访问控制

限制哪些用户可以与应用程序交互：

````bash
# 将特定用户列入白名单
WECOM_CALLBACK_ALLOWED_USERS=zhangsan,lisi,wangwu

# 或者允许所有用户
WECOM_CALLBACK_ALLOW_ALL_USERS=true
````

## 端点

适配器公开：

|方法|路径|目的|
|--------|------|---------|
|获取 | `/wecom/callback` | URL 验证握手（WeCom 在设置期间发送此信息）|
|发布 | `/wecom/callback` |加密消息回调（WeCom 在此发送用户消息）|
|获取 | `/健康` |健康检查 — 返回 `{"status": "ok"}` |

## 加密

所有回调有效负载均使用 EncodingAESKey 通过 AES-CBC 进行加密。适配器处理：

- **入站**：解密 XML 负载，验证 SHA1 签名
- **出站**：通过主动 API 发送回复（未加密的回调响应）

加密实现与腾讯官方WXBizMsgCrypt SDK兼容。

## 限制

- **无流式传输** — 代理完成后回复将作为完整消息到达
- **无输入指示器** — 回调模型不支持输入状态
- **仅限文本** — 目前支持文本消息输入；图像/文件/语音输入尚未实现。座席通过 WeCom 平台提示了解出站媒体功能（图像、文档、视频、语音）。
- **响应延迟** — 代理会话需要 3-30 分钟；处理完成后用户会看到回复

## 故障排除

**签名验证失败。**
WeCom 使用您在后台注册的 **Token** 签署每个请求
控制台。 OpenClaw中配置的token与实际的token不匹配
管理控制台预期是最常见的原因。重新复制 **Token** 和
**从管理控制台编码 AESKey** — 它们很容易被截断。空白
在 `~/.hermes/.env` 中，`=` 周围的值也会破坏签名检查。之后
修复后，重新启动“hermes gateway run”。

**回调 URL 无法访问/验证步骤失败。**
WeCom 点击您注册的公共 URL。确认：
1. 您的反向代理/隧道将 `/wecom/callback` 转发到网关的端口。
2. 管理控制台中的 URL 是 HTTPS（WeCom 拒绝纯 HTTP）。
3. 从网络外部，“curl -i https://<your-domain>/wecom/callback”
   返回超时以外的其他内容（没有查询参数的 4xx 很好 -
   它只是意味着听众是可以到达的）。

**端口无法访问/监听器未绑定。**
检查绑定主机/端口的“hermes gateway run”日志。如果适配器绑定到
`127.0.0.1` 你必须在它前面使用反向代理或隧道 - WeCom 的服务器
无法到达环回。在“config.yaml”中设置“extra.host: 0.0.0.0”（加上
`allowed_source_cidrs` 如果直接暴露）或保持环回并使用隧道
例如 Cloudflare Tunnel / nginx。