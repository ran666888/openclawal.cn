---
title: "Stripe Projects — Provision SaaS services + sync creds via Stripe Projects"
sidebar_label: "Stripe Projects"
description: "Provision SaaS services + sync creds via Stripe Projects"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 条纹项目

通过 Stripe 项目提供 SaaS 服务 + 同步信用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/ payment/stripe-projects` 安装 |
|路径| `可选技能/付款/条纹项目` |
|版本 | `0.1.0` |
|作者 | Teknium（teknium1），爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | `付款`、`Stripe`、`项目`、`配置`、`基础设施` |
|相关技能| [`stripe-link-cli`](/docs/user-guide/skills/optional/ payments/ payments-stripe-link-cli), [`mpp-agent`](/docs/user-guide/skills/optional/ payments/ payments-mpp-agent) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 条纹项目技能

包装 [Stripe Projects](https://projects.dev) CLI 插件，以便 OpenClaw 可以提供 SaaS 服务（Neon、Twilio、Vercel 等）、生成凭证并将其同步到用户的“.env”中，并从一个地方管理跨提供商的计费。

当更广泛的支付集群在 Windows 上成熟时，门控“[linux、macos]”。 Stripe CLI 本身是跨平台的；这个门是集群的一种姿态，而不是硬性限制。

## 何时使用

触发短语：

- “设置 <provider>”、“提供 <Neon|Twilio|Vercel|...>”、“创建数据库”
- “给我这个项目的 <Postgres|Redis|Twilio 编号|...>”
-“管理我的堆栈凭据”、“轮换此密钥”、“升级我的计划”
- “我可以添加哪些提供商？”

如果用户已经有提供者帐户，此技能仍然可以将其与“stripe items link <provider>”连接。如果用户想要使用现有的提供者资源，例如现有的数据库或Vercel项目，请首先检查提供者支持；许多提供商当前支持配置新资源，但不支持导入现有资源。

## 先决条件

- 安装了 Stripe CLI（macOS 上的 Homebrew、Linux 上的包管理器或从 https://docs.stripe.com/stripe-cli/install 下载）
- 安装了 Stripe Projects 插件
- Stripe 帐户。如果用户还没有，CLI 可以在设置过程中引导他们在浏览器中登录或创建帐户。

## 安装

苹果系统：

````
brew 安装 stripe/stripe-cli/stripe
stripe插件安装项目
````

Linux：按照 https://docs.stripe.com/stripe-cli/install 中特定于平台的安装进行操作，然后：

````
stripe插件安装项目
````

## 如何运行

所有命令都通过用户项目目录内的“terminal”工具运行（CLI 将“.env”和“.projects/vault/vault.json”写入 CWD）。

## 程序

### 1.初始化项目

````
cd <项目根目录>
条带项目初始化
````

这将创建“.projects/vault/vault.json”（加密凭证存储）并准备项目以接收提供程序。

### 2. 发现可用的提供商

````
条纹项目目录
````

列出 Stripe Projects 支持的每个提供商 — 数据库、托管、身份验证、人工智能、分析、消息传递等。

### 3.添加服务

````
条带项目添加 <provider>/<service>
````

示例：

- `stripe 项目添加 neon/postgres`
-`条纹项目添加 twilio/sms`
- `stripe 项目添加 runloop/sandbox`

CLI 在用户自己的帐户中向提供商提供服务，生成凭据，将其同步到“.env”中，并将资源记录在保管库中。用户可能需要确认等级选择或定价提示。

### 4. 验证

````
条纹项目列表
````

应显示新添加的提供程序及其“.env”键。

### 5.管理/升级/删除

````
stripe 项目升级 <provider> # 层更改
stripe 项目删除 <provider> # 取消配置
stripe 项目旋转 <provider> # 旋转凭证
````

## 陷阱

- **`.env` 写入是真正的写入。** CLI 会附加到项目根目录中的任何 `.env` 内容。如果用户的 .env 被 gitignored（正常），则密钥安全着陆；如果不是，该技能可能是凭证泄漏向量。始终首先检查“.gitignore”。
- **每个项目状态。** `.projects/vault/vault.json` 是每个项目。在两个不同的项目中配置相同的服务会创建两个独立的资源 - 和两个账单。
- **计费由 Stripe 方进行。** “添加”/“升级”期间的等级提示是真实收费；在确认之前向用户展示它们。
- **提供商可用性发生变化。** 目录增长；如果未列出提供者的用户名，`stripeprojectscatalog|首先 grep <name>` 而不是使 `add` 调用失败。
- **保管库中的凭证已加密，但“.env”是明文。** 适用标准“.env”卫生 — 切勿提交。
- **删除服务并不总是会破坏底层资源。** 一些提供商会留下暂停/休眠的资源。在“删除”高成本服务（尤其是托管数据库）后检查提供商自己的仪表板。

## 验证

````
条带项目 --version && 条带项目列表
````

初始化项目内的退出代码 0 表示插件运行正常。