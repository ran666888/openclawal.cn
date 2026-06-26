---
title: "Himalaya — Himalaya CLI: IMAP/SMTP email from terminal"
sidebar_label: "Himalaya"
description: "Himalaya CLI: IMAP/SMTP email from terminal"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#喜马拉雅山

Himalaya CLI：来自终端的 IMAP/SMTP 电子邮件。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/电子邮件/喜马拉雅` |
|版本 | `1.1.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `电子邮件`、`IMAP`、`SMTP`、`CLI`、`通信` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 喜马拉雅电子邮件 CLI

Himalaya 是一个 CLI 电子邮件客户端，可让您使用 IMAP、SMTP、Notmuch 或 Sendmail 后端管理来自终端的电子邮件。

该技能独立于 OpenClaw 电子邮件网关适配器。网关
适配器让人们向代理发送电子邮件并使用 OpenClaw 的内置 IMAP/SMTP
适配器；这项技能可以让代理通过终端工具操作邮箱，
需要外部“喜马拉雅”CLI。

## 参考文献

- `references/configuration.md`（配置文件设置 + IMAP/SMTP 身份验证）
- `references/message-composition.md`（用于撰写电子邮件的 MML 语法）

## 先决条件

1.安装喜马拉雅CLI（`himalaya --version`进行验证）
2.配置文件`~/.config/himalaya/config.toml`
3. 配置 IMAP/SMTP 凭据（安全存储密码）

### 安装

````bash
# 预构建的二进制文件（Linux/macOS — 推荐）
卷曲-sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS 通过 Homebrew
酿造安装喜马拉雅

# 或者通过 Cargo（任何带有 Rust 的平台）
货物安装喜马拉雅--锁定
````

## 配置设置

运行交互式向导来设置帐户：

````bash
喜马拉雅账户配置
````

或者手动创建`~/.config/himalaya/config.toml`：

````汤姆
[账户.个人]
电子邮件=“you@example.com”
显示名称=“你的名字”
默认=真

后端.type =“imap”
backend.host =“imap.example.com”
后端端口 = 993
后端.加密.type =“tls”
backend.login =“you@example.com”
backend.auth.type = "密码"
backend.auth.cmd = "pass show email/imap" # 或使用密钥环

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
消息.发送.后端.端口 = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "密码"
message.send.backend.auth.cmd = "通过显示电子邮件/smtp"

# 文件夹别名（喜马拉雅 v1.2.0+ 语法）。每当
# 服务器的文件夹名称与喜马拉雅的规范名称不匹配
#（收件箱/已发送/草稿/垃圾箱）。 Gmail 是常见情况 — 请参阅
# `references/configuration.md` 用于 `[Gmail]/Sent Mail` 映射。
文件夹.aliases.inbox = "收件箱"
folder.aliases.sent = "已发送"
folder.aliases.drafts = "草稿"
folder.aliases.trash = "垃圾箱"
````

> **注意别名语法。** v1.2.0 之前的文档使用了
> `[accounts.NAME.folder.alias]` 小节（单数“alias”）。
> v1.2.0 默默地忽略该形式 — TOML 解析得很好，但是
> 别名解析器从不读取它，因此每次查找都会失败
> 规范名称。在 Gmail 上，这意味着“保存至发送”*之后*失败
> SMTP 发送成功，并且 `喜马拉雅消息发送` 退出非零。
> 任何重试该退出代码的调用者（代理、脚本、用户）
> 将重新运行整个发送 — 包括 SMTP — 产生重复
> 向收件人发送电子邮件。始终使用“folder.aliases.X”（复数、点线
> 键，直接位于“[accounts.NAME]”下）。

## OpenClaw 集成说明

- **阅读、列出、搜索、移动、删除**所有工作直接通过终端工具进行
- **撰写/回复/转发** — 为了可靠性，建议使用管道输入（`cat << EOF | Himalaya template send`）。交互式“$EDITOR”模式与“pty=true”+后台+处理工具配合使用，但需要了解编辑器及其命令
- 使用“--output json”进行结构化输出，更容易以编程方式解析
- `himalaya 帐户配置` 向导需要交互式输入 - 使用 PTY 模式： `terminal(command="himalaya account configure", pty=true)`

## 常用操作

### 列出文件夹

````bash
喜马拉雅文件夹列表
````

### 列出电子邮件

列出收件箱中的电子邮件（默认）：

````bash
喜马拉雅信封清单
````

列出特定文件夹中的电子邮件：

````bash
喜马拉雅信封列表——文件夹“已发送”
````

带分页的列表：

````bash
喜马拉雅信封列表--第1页--页面大小20
````

### 搜索电子邮件

````bash
来自 john@example.com 主题会议的喜马拉雅信封列表
````

### 阅读电子邮件

按 ID 读取电子邮件（显示纯文本）：

````bash
喜马拉雅消息已读 42
````

导出原始 MIME：

````bash
喜马拉雅消息导出 42 --full
````

### 回复电子邮件

要从 OpenClaw 以非交互方式回复，请阅读原始消息，撰写回复，然后通过管道传输：

````bash
# 获取回复模板，编辑并发送
喜马拉雅模板回复42 | sed 's/^$/\n此处为您的回复文本\n/' |喜马拉雅模板发送
````

或者手动构建回复：

````bash
猫 << 'EOF' |喜马拉雅模板发送
来自：you@example.com
至：sender@example.com
主题：回复：原始主题
回复中：<原始消息 ID>

你的回复在这里。
EOF
````

全部回复（交互式 - 需要 $EDITOR，请使用上面的模板方法）：

````bash
喜马拉雅消息回复42--全部
````

### 转发电子邮件

````bash
# 获取经过修改的前向模板和管道
喜马拉雅模板转发 42 | sed 's/^To:.*/To: newrecipient@example.com/' | sed 's/^To:.*/To: newrecipient@example.com/' |喜马拉雅模板发送
````

### 写一封新电子邮件

**非交互式（使用 OpenClaw 的此功能）** — 通过标准输入传输消息：

````bash
猫 << 'EOF' |喜马拉雅模板发送
来自：you@example.com
至：recipient@example.com
主题：测试消息

来自喜马拉雅的你好！
EOF
````

或者使用标题标志：

````bash
喜马拉雅消息写入 -H "To:recipient@example.com" -H "Subject:Test" "消息正文在此"
````

注意：没有管道输入的“喜马拉雅消息写入”会打开“$EDITOR”。这适用于 `pty=true` + 后台模式，但管道更简单、更可靠。

### 移动/复制电子邮件

移至文件夹：

````bash
喜马拉雅消息移动“存档”42
````

复制到文件夹：

````bash
喜马拉雅消息文案“重要”42
````

### 删除电子邮件

````bash
喜马拉雅消息删除 42
````

### 管理标志

添加标志：

````bash
喜马拉雅山标志添加 42 --标志可见
````

删除标志：

````bash
喜马拉雅山标志删除 42 --标志可见
````

## 多个帐户

列出帐户：

````bash
喜马拉雅账户列表
````

使用特定帐户：

````bash
喜马拉雅--账户工作信封列表
````

## 附件

保存消息中的附件：

````bash
喜马拉雅附件下载 42
````

保存到指定目录：

````bash
喜马拉雅附件下载 42 --downloads-dir ~/Downloads
````

## 输出格式

大多数命令支持“--output”进行结构化输出：

````bash
喜马拉雅信封列表--输出json
喜马拉雅信封列表--输出纯文本
````

## 调试

启用调试日志记录：

````bash
RUST_LOG=调试喜马拉雅信封列表
````

带回溯的完整跟踪：

````bash
RUST_LOG=trace RUST_BACKTRACE=1 喜马拉雅信封列表
````

## 提示

- 使用 `himalaya --help` 或 `himalaya <command> --help` 了解详细用法。
- 消息ID是相对于当前文件夹的；文件夹更改后重新列出。
- 要撰写带有附件的丰富电子邮件，请使用 MML 语法（请参阅“references/message-composition.md”）。
- 使用“pass”、系统密钥环或输出密码的命令安全地存储密码。