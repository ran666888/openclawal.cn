---
title: "Imessage — Send and receive iMessages/SMS via the imsg CLI on macOS"
sidebar_label: "Imessage"
description: "Send and receive iMessages/SMS via the imsg CLI on macOS"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 消息

通过 macOS 上的 imsg CLI 发送和接收 iMessages/SMS。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/苹果/imessage` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| macOS |
|标签 | `iMessage`、`短信`、`消息传递`、`macOS`、`Apple` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 短信

使用“imsg”通过 macOS Messages.app 读取和发送 iMessage/SMS。

## 先决条件

- **macOS** 已登录 Messages.app
- 安装：`brew install steipete/tap/imsg`
- 授予终端完整磁盘访问权限（系统设置→隐私→完整磁盘访问权限）
- 出现提示时授予 Messages.app 的自动化权限

## 何时使用

- 用户请求发送 iMessage 或短信
- 读取 iMessage 对话历史记录
- 检查最近的 Messages.app 聊天
- 发送至电话号码或 Apple ID

## 何时不使用

- Telegram/Discord/Slack/WhatsApp 消息 → 使用适当的网关通道
- 群聊管理（添加/删除成员）→ 不支持
- 批量/群发消息 → 始终首先与用户确认

## 快速参考

### 列出聊天记录

````bash
imsg 聊天 --limit 10 --json
````

### 查看历史记录

````bash
# 通过聊天ID
imsg 历史记录 --chat-id 1 --limit 20 --json

# 带有附件信息
imsg 历史记录 --chat-id 1 --limit 20 --attachments --json
````

### 发送消息

````bash
# 仅限文本
imsg send --to "+14155551212" --text "你好！"

# 有附件
imsg send --to "+14155551212" --text "检查一下" --file /path/to/image.jpg

# 强制 iMessage 或 SMS
imsg 发送 --to "+14155551212" --text "Hi" --service imessage
imsg 发送 --to "+14155551212" --text "Hi" --service sms
````

### 留意新消息

````bash
imsg watch --chat-id 1 --附件
````

## 服务选项

- `--service imessage` — 强制 iMessage（要求收件人有 iMessage）
- `--service sms` — 强制短信（绿色气泡）
- `--service auto` — 让 Messages.app 决定（默认）

## 规则

1. **发送前务必确认收件人和消息内容**
2. **切勿在未经用户明确批准的情况下发送给未知号码**
3. **在附加之前验证文件路径**是否存在
4. **不要发送垃圾邮件** — 限制自己的速率

## 工作流程示例

用户：“给妈妈发短信说我要迟到了”

````bash
# 1. 查找妈妈的聊天记录
imsg 聊天 --limit 20 --json | jq '.[] |选择（.displayName | contains（“妈妈”））'

# 2. 与用户确认：“在 +1555123456 找到妈妈。通过 iMessage 发送‘我会迟到’？”

# 3.确认后发送
imsg send --to "+1555123456" --text "我会迟到"
````