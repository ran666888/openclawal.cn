---
title: "Stripe Link Cli — Agent payments via Stripe Link — cards, SPT, approvals"
sidebar_label: "Stripe Link Cli"
description: "Agent payments via Stripe Link — cards, SPT, approvals"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Stripe 链接 CLI

通过 Stripe Link 进行代理付款 — 卡、SPT、批准。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/ payments/stripe-link-cli` 安装 |
|路径| `可选技能/付款/stripe-link-cli` |
|版本 | `0.1.0` |
|作者 | Teknium（teknium1），爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | `付款`、`Stripe`、`链接`、`结账`、`MPP` |
|相关技能| [`mpp-agent`](/docs/用户指南/技能/可选/付款/付款-mpp-agent)，[`stripe-projects`](/docs/用户指南/技能/可选/付款/付款-stripe-projects) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Stripe Link CLI 技能

包装 [@stripe/link-cli](https://github.com/stripe/link-cli)，以便 OpenClaw 可以使用一次性虚拟卡或共享支付令牌 (SPT) 代表用户完成购买。每一笔支出都通过 Link 移动/网络应用程序中的应用程序内批准进行控制——OpenClaw 无法自行批准。

目前仅限美国（链接帐户要求）。上游 CLI 不支持 Windows — 此技能被限制为“[linux, macos]”。

## 何时使用

触发短语：

- “购买 X”、“支付 X”、“进行购买”、“完成结账”
- “给我一张卡”，“我需要一个付款方式”
- “登录 Link”、“连接我的 Link 钱包”
- 来自商家 API 的 HTTP 402 响应，其中包含 `www-authenticate: ... method="stripe"`

如果用户想要付费 API 调用（HTTP 402，无结帐表单），则“card”路径是错误的 - 通过相同的技能使用 SPT，或者移交给“mpp-agent”技能。

## 先决条件

- Node.js 20+ 可在“PATH”（“node --version”）上使用
- 位于美国（链接帐户要求）

在 OpenClaw 尝试付款之前，不需要设置链接帐户、付款方式和支出审批应用程序 — CLI 将在首次运行时引导用户完成这些操作：

- https://app.link.com 上的链接帐户 — 在第一次 `link-cli` 身份验证期间创建/链接
- 至少一种付款方式 - 在首次运行期间添加，网址为 https://app.link.com/wallet
- Link 移动/网络应用程序 — 打开以在发出第一个支出请求时批准该请求

不需要环境变量 - 身份验证状态由 CLI 本地存储在其自己的配置目录下。

## 安装

全局安装一次：

````
npm install -g @stripe/link-cli
````

或者通过“npx @stripe/link-cli”调用临时。下面的技能使用已安装的“link-cli”形式。

## 如何运行

所有命令都通过“terminal”工具运行。 CLI 自动检测非 TTY 调用者并默认发出紧凑的“toon”输出 - 对于模型来说很好。如果步骤需要结构化字段，请传递“--format json”。

发现命令：“link-cli --llms-full”。
在调用之前获取命令的架构：“link-cli <command> --schema”。

## 程序

### 1.检查/建立身份验证

````
link-cli 身份验证状态
````

如果未通过身份验证，请使用明确的客户端名称登录（此标签显示在用户的 Link 应用程序中）：

````
link-cli auth login --client-name "Hermes" --interval 5 --timeout 300
````

`--interval`/`--timeout` 形式内联轮询，因此代理不需要管理 `_next` 步骤。将验证 URL + 短语打印给用户并等待 CLI 返回。

**在“auth status”确认登录之前，不要继续执行此步骤。**

### 2. 在创建支出请求之前评估商家

确定凭证类型：

|商户面| `--凭证类型` |
|---|---|
|标准网络结帐表格/条纹元素 | `卡`（默认）|
|在 `www-authenticate` 中使用 `method="stripe"` 返回 HTTP 402 | `共享支付令牌` |
|返回 HTTP 402 而不使用 `method="stripe"` |不支持-停止|

对于 402 响应，请勿手动解码质询。传递原始标头：

````
link-cli mpp 解码 --challenge '<完整 WWW-Authenticate 标头>'
````

这将验证质询并提取网络 ID + 解码的请求正文。

### 3.列出付款方式+运输

````
link-cli 付款方式列表
link-cli 送货地址列表
````

除非用户另有指定，否则使用第一个条目。 “ payment-methods list”中的“id”是下一步中的“-- payment-method-id”。

### 4. 创建支出请求

在发出此命令之前与用户确认最终总计。金额以美分为单位。

````
link-cli 花费请求创建 \
  --付款方法-id <pm_id> \
  --商家名称“<名称>”\
  --merchant-url "<url>" \
  --context "<一句话：购买什么以及为什么>" \
  --金额 <分> \
  --line-item "名称:<项目>,单位金额:<分>,数量:1" \
  --total "类型：总计，显示文本：总计，金额：<分>" \
  --请求批准
````

对于 MPP 商家，添加 `--credential-type shared_ payment_token`。

`--request-approval` 会对用户的 Link 应用程序执行 ping 操作并进行轮询，直到他们批准或拒绝。 CLI 在拒绝/超时时以非零值退出。

### 5. 安全地检索凭证

**不要将卡详细信息打印到标准输出。** 使用“--output-file”，以便 PAN 永远不会输入代理的记录或日志：

````
link-cli 花费请求检索 <lsrq_id> \
  --包括卡\
  --输出文件/tmp/link-card.json \
  --格式化json
````

该文件以“0600”权限写入； stdout 仅显示经过编辑的字段（brand、last4、expiry）以及“card_output_file”路径。

### 6. 使用凭证

- 对于网络结账：将文件路径交给用户，或将其传递给浏览器驱动工具，直接从磁盘填写表单。切勿将卡片文件“read_file”或“cat”放入代理的推理上下文中。
- 对于 MPP 商户：

  ````
  link-cli mpp pay <商户网址> \
    --spend-request-id <lsrq_id> \
    --方法 POST \
    --data '<json 正文>'
  ````

### 7. 清理

购买完成后立即删除卡文件：

````
rm -f /tmp/link-card.json
````

## 可选：作为 MCP 服务器运行

`@stripe/link-cli --mcp` 通过 stdio 公开与 MCP 工具相同的命令。要将其注册到 OpenClaw 的本地 MCP：

````
Hermes mcp 添加 stripe-link --命令“npx”--args“@stripe/link-cli --mcp”
````

然后“hermes mcp list”应该显示“stripe-link”。适用相同的批准规则 - MCP 不会绕过链接应用程序批准步骤。

## 陷阱

- **仅限美国。** 在美国境外，“身份验证登录”将失败。告诉用户，不要继续重试。
- **卡 PAN 绝不能进入代理上下文。** 每次都使用 `--output-file`。如果您已经在没有它的情况下检索，立即“link-cli auth logout”是不够的——该卡是一次性使用的，但轮换卫生很重要。
- **`--request-approval` 会阻塞，直到用户采取行动。** 如果用户睡着了，CLI 将超时。设定期望。
- **多步`_next`命令。**某些命令返回必须执行才能继续的`_next.command`。如有疑问，请首选内联轮询标志（`--interval`/`--timeout`）。
- **非 TTY 模式下输出格式默认为 `toon`**。适合散文，但如果下游步骤需要解析特定字段，请传递“--format json”。
- **不要默认为“卡”。** 商家评估步骤（第 2 节）的存在是因为选择错误的凭证类型会导致购买失败或泄露超出所需的数据。

## 验证

````
link-cli --version && link-cli 身份验证状态
````

退出代码 0 表示已安装并登录。