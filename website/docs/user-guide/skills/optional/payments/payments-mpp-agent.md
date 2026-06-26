---
title: "Mpp Agent — Pay HTTP 402 APIs via Machine Payments Protocol (MPP)"
sidebar_label: "Mpp Agent"
description: "Pay HTTP 402 APIs via Machine Payments Protocol (MPP)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Mpp 代理

通过机器支付协议 (MPP) 支付 HTTP 402 API。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/ payment/mpp-agent` 安装 |
|路径| `可选技能/付款/mpp-代理` |
|版本 | `0.1.0` |
|作者 | Teknium（teknium1），爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | `付款`、`MPP`、`HTTP-402`、`Tempo`、`Stripe` |
|相关技能| [`stripe-link-cli`](/docs/user-guide/skills/optional/ payments/ payments-stripe-link-cli)，[`stripe-projects`](/docs/user-guide/skills/Optional/ payments/ payments-stripe-projects) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# MPP 代理技能

包装机器支付协议（MPP，https://mpp.dev）客户端，以便 OpenClaw 可以针对响应“HTTP 402 Payment Needed”的服务器为每个请求的 API 访问付费。

三个客户端选项，全部通过 npm 分发。选择能够满足用户需求的最轻的一款。门禁“[linux、macos]”，而更广泛的支付工具在 Windows 上日趋成熟。

## 何时使用

- 商家 API 返回带有“www-authenticate”标头的“HTTP 402”——用户希望实际付款，而不仅仅是记录响应。
- 用户要求“按请求付费”、“设置代理钱包”、“使用 Tempo / Privy / AgentCash”，或者想要发现 MPP 定价的服务。
- Stripe Link 支出已生成共享支付令牌 (SPT)，代理需要将其附加到 402 质询 - 在该流程中，首选“link-cli mpp pay”（请参阅​​“stripe-link-cli”技能）。

## 选择客户

|工具|当 |设置 |
|---|---|---|
| `link-cli` |用户已设置 Stripe 链接，或 402 质询广告 `method="stripe"` |查看 `stripe-link-cli` 技能 |
|节奏钱包 |具有支出控制、服务发现的 MPP 服务 | `tempo 钱包登录` |
|隐私代理 CLI |多链钱包，基于浏览器的资金| `私人代理钱包登录` |
|代理现金 |通过一笔 USDC.e 余额提供 300 多个预先定价的 API | `npx agentcash 船上` |
| `mppx` |开发+调试，最小的开发面| `npm install -g mppx` 然后 `mppx 帐户创建` |

默认：如果用户已经配置了 Stripe Link 或 402 质询指定了“method="stripe””，则使用“link-cli mpp pay”（“stripe-link-cli”技能）。另外，“mppx”用于一次性付费通话和调试，而 Tempo 钱包则用于用户想要持续控制支出时。

## 先决条件

- `PATH` 上的 Node.js 20+
- 资金钱包（Tempo / Privy / AgentCash）或“mppx”帐户
- 对于 Tempo / Privy / AgentCash：遵循各自的入职技巧：
  - `https://tempo.xyz/SKILL.md`
  - `https://agents.privy.io/skill.md`
  - `https://agentcash.dev/skill.md`

如果用户选择一个，请使用“web_extract”来获取这些 SKILL.md 文件中的任何一个。

## 过程（mppx，最快路径）

通过“终端”工具运行所有命令。

### 1.安装+创建帐户

````
npm 安装-g mppx
mppx 帐户创建
````

将生成的帐户凭据存储在 CLI 告诉您的任何位置（CLI 将它们写入其自己的配置下 - 不要将它们粘贴到代理记录中）。

### 2.检查商家的402挑战

如果用户给你一个 URL，请先探测它以确认它确实支持 MPP：

````
卷曲-i <网址>
````

真正的 MPP 402 看起来像：

````
HTTP/1.1 402 需要付款
www-authenticate: 节奏金额=0.1 货币=...
````

### 3. 支付请求

````
mppx <网址>
````

对于非 GET 方法或请求正文：

````
mppx <url> --方法 POST --data '<json>'
````

`mppx` 自动处理 402 挑战/凭证舞蹈并打印商家对成功的实际响应。

### 4. 验证收据

`mppx` 自动附加收据标题。检查：

````
mppx <url> -v
````

## 程序（Tempo 钱包）

https://tempo.xyz/SKILL.md 上的 Tempo 钱包技能是规范参考；使用“web_extract”获取它并遵循它。标题：

````
节奏钱包登录
tempo 钱包支付 <url>
````

在钱包 UI 中进行支出控制和服务发现：https://wallet.tempo.xyz。

## 陷阱

- **没有 `method="stripe"` 的`HTTP 402` 无法通过 Stripe Link 支付。** 如果挑战仅宣传 Tempo/其他方法，请使用 `mppx` （或任何匹配的钱包） - Link 将拒绝它。相反，如果它宣传 `method="stripe"`，则更喜欢通过 `stripe-link-cli` 技能进行链接，以便支出通过用户批准的卡进行。
- **一个标头中有多个挑战。** `www-authenticate` 可能会列出多种方法（例如 `tempo、stripe`）。 Link CLI 的“mpp 解码”将选择 Stripe； `mppx` 将选择节奏。没有单一的“正确”客户——选择用户通过哪个钱包进行资助。
- **零金额挑战。** 一些 MPP 端点收费“0.00 美元”并且只需要一个证明凭证。这些无需资金支持即可工作。不要将它们视为“破损”而拒绝它们。
- **钱包密钥永远不会进入代理上下文。** 所有四个客户端都将密钥存储在自己的配置目录下（或者在 Privy 的情况下生成每个会话的临时密钥对）。不要“cat”/“read_file”它们。
- **服务器端 MPP 是一项不同的技能。** 如果用户想要将 402 添加到自己的 API，则此技能是错误的 - 将他们指向 https://mpp.dev/quickstart/server 和 `mppx/nextjs` / `mppx/hono` / `mppx/express` / `mppx/elysia` 中间件。专用的“mpp-server”技能可能会在稍后登陆。

## 验证

````
mppx --version && mppx 帐户列表
````

退出代码 0 表示已安装且帐户存在。