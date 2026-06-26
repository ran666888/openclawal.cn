---
title: "Agentmail — Give the agent its own dedicated email inbox via AgentMail"
sidebar_label: "Agentmail"
description: "Give the agent its own dedicated email inbox via AgentMail"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 代理邮件

通过 AgentMail 为代理提供自己的专用电子邮件收件箱。使用代理拥有的电子邮件地址（例如 openclaw@agentmail.to）自主发送、接收和管理电子邮件。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/email/agentmail` 安装 |
|路径| `可选技能/电子邮件/代理邮件` |
|版本 | `1.0.0` |
|平台| linux、macos、windows |
|标签 | `电子邮件`、`通信`、`agentmail`、`mcp` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# AgentMail — 代理拥有的电子邮件收件箱

## 要求

- **AgentMail API 密钥**（必需）— 在 https://console.agentmail.to 上注册（免费套餐：3 个收件箱，每月 3,000 封电子邮件；付费计划从 20 美元/月起）
- Node.js 18+（用于 MCP 服务器）

## 何时使用
当您需要执行以下操作时，请使用此技能：
- 为代理提供自己的专用电子邮件地址
- 代表代理自主发送电子邮件
- 接收和阅读传入的电子邮件
- 管理电子邮件线程和对话
- 注册服务或通过电子邮件进行身份验证
- 通过电子邮件与其他代理或人员沟通

这不适用于读取用户的个人电子邮件（使用 Himalaya 或 Gmail）。
AgentMail 为代理提供了自己的身份和收件箱。

## 设置

### 1. 获取 API 密钥
- 转到 https://console.agentmail.to
- 创建帐户并生成 API 密钥（以“am_”开头）

### 2.配置MCP服务器
添加到 `~/.hermes/config.yaml` （粘贴您的实际密钥 - MCP 环境变量不会从 .env 扩展）：
````yaml
mcp_服务器：
  代理邮箱：
    命令：“npx”
    参数：[“-y”，“agentmail-mcp”]
    环境：
      AGENTMAIL_API_KEY：“am_your_key_here”
````

### 3.重启OpenClaw
````bash
爱马仕
````
所有 11 个 AgentMail 工具现在均可自动使用。

## 可用工具（通过 MCP）

|工具|描述 |
|------|-------------|
| `列表收件箱` |列出所有代理收件箱 |
| `获取收件箱` |获取特定收件箱的详细信息 |
| `创建收件箱` |创建新收件箱（获取真实电子邮件地址）|
| `删除收件箱` |删除收件箱 |
| `列表线程` |列出收件箱中的电子邮件线程 |
| `获取线程` |获取特定的电子邮件主题 |
| `发送消息` |发送新电子邮件 |
| `回复消息` |回复现有电子邮件 |
| `转发消息` |转发电子邮件 |
| `更新消息` |更新消息标签/状态 |
| `获取附件` |下载电子邮件附件 |

## 程序

### 创建收件箱并发送电子邮件
1. 创建专用收件箱：
   - 使用带有用户名的“create_inbox”（例如“openclaw”）
   - 代理获取地址：`hermes-agent@agentmail.to`
2. 发送电子邮件：
   - 将“send_message”与“inbox_id”、“to”、“subject”、“text”一起使用
3. 检查回复：
   - 使用“list_threads”查看传入对话
   - 使用`get_thread`读取特定线程

### 检查收到的电子邮件
1. 使用 `list_inboxes` 查找您的收件箱 ID
2. 使用“list_threads”和收件箱 ID 查看对话
3. 使用`get_thread`读取线程及其消息

### 回复电子邮件
1.通过`get_thread`获取线程
2. 使用带有消息 ID 和回复文本的 `reply_to_message`

## 工作流程示例

**注册服务：**
````
1.create_inbox（用户名：“signup-bot”）
2. 使用收件箱地址注册服务
3. list_threads 检查验证邮件
4. get_thread读取验证码
````

**代理对人的外展：**
````
1.create_inbox（用户名：“hermes-outreach”）
2. send_message（发送至：user@example.com，主题：“Hello”，文本：“...”）
3. list_threads 检查回复
````

## 陷阱
- 免费套餐每月仅限 3 个收件箱和 3,000 封电子邮件
- 电子邮件来自免费套餐中的“@agentmail.to”域（付费计划中的自定义域）
- MCP 服务器需要 Node.js (18+) (`npx -y agentmail-mcp`)
- 必须安装 `mcp` Python 包：`pip install mcp`
- 实时入站电子邮件（webhooks）需要公共服务器 - 通过 cronjob 使用“list_threads”轮询代替个人使用

## 验证
设置完成后，使用以下命令进行测试：
````
hermes --toolsets mcp -q “创建一个名为 test-agent 的 AgentMail 收件箱并告诉我它的电子邮件地址”
````
您应该会看到返回的新收件箱地址。

## 参考文献
- AgentMail 文档：https://docs.agentmail.to/
- AgentMail 控制台：https://console.agentmail.to
- AgentMail MCP 存储库：https://github.com/agentmail-to/agentmail-mcp
- 定价：https://www.agentmail.to/pricing