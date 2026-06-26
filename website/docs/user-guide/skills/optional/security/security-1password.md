---
title: "1Password — Set up and use 1Password CLI (op)"
sidebar_label: "1Password"
description: "Set up and use 1Password CLI (op)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#1密码

设置并使用 1Password CLI (op)。在安装 CLI、启用桌面应用程序集成、登录以及读取/注入命令机密时使用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/security/1password` 安装 |
|路径| `可选技能/安全/1password` |
|版本 | `1.0.0` |
|作者 | arceus77-7，由赫尔墨斯特工增强|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `security`、`secrets`、`1password`、`op`、`cli` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

#1密码CLI

当用户希望通过 1Password 而不是纯文本环境变量或文件管理机密时，请使用此技能。

## 要求

- 1个密码帐户
- 安装了 1Password CLI (`op`)
- 以下之一：桌面应用程序集成、服务帐户令牌 (`OP_SERVICE_ACCOUNT_TOKEN`) 或 Connect 服务器
- `tmux` 可用于 OpenClaw 终端调用期间稳定的经过身份验证的会话（仅限桌面应用程序流程）

## 何时使用

- 安装或配置 1Password CLI
- 使用“op Signin”登录
- 阅读秘密引用，例如“op://Vault/Item/field”
- 使用“op Inject”将机密注入配置/模板
- 通过“op run”使用秘密环境变量运行命令

## 验证方法

### 服务帐户（推荐用于 OpenClaw）

在 `${HERMES_HOME:-~/.hermes}/.env` 中设置 `OP_SERVICE_ACCOUNT_TOKEN` （技能将在首次加载时提示）。
无需桌面应用程序。支持`op read`、`op注入`、`op run`。

````bash
导出 OP_SERVICE_ACCOUNT_TOKEN="您的令牌-此处"
op whoami # verify — 应显示类型：SERVICE_ACCOUNT
````

### 桌面应用程序集成（交互式）

1. 在 1Password 桌面应用程序中启用：设置 → 开发人员 → 与 1Password CLI 集成
2. 确保应用程序已解锁
3. 运行“op Signin”并批准生物识别提示

### 连接服务器（自托管）

````bash
导出 OP_CONNECT_HOST="http://localhost:8080"
导出 OP_CONNECT_TOKEN="your-connect-token"
````

## 设置

1.安装命令行：

````bash
# 1Password
酿造安装1password-cli

# Linux（官方包/安装文档）
# 请参阅references/get-started.md 以获取特定于发行版的链接。

# Windows (winget)
winget 安装 AgileBits.1Password.CLI
````

2. 验证：

````bash
操作--版本
````

3. 选择上面的身份验证方法并进行配置。

## OpenClaw 执行模式（桌面应用程序流程）

默认情况下，OpenClaw 终端命令是非交互式的，并且可能会丢失调用之间的身份验证上下文。
为了通过桌面应用程序集成可靠地使用“op”，请在专用的 tmux 会话中运行登录和秘密操作。

注意：使用“OP_SERVICE_ACCOUNT_TOKEN”时不需要这样做——令牌在终端调用中自动保留。

````bash
SOCKET_DIR="${TMPDIR:-/tmp}/hermes-tmux-sockets"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/hermes-op.sock"
SESSION="op-auth-$(日期 +%Y%m%d-%H%M%S)"

tmux -S“$SOCKET”新-d -s“$SESSION”-n shell

# 登录（出现提示时在桌面应用程序中批准）
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 --"eval \"\$(op signin --account my.1password.com)\"" Enter

# 验证身份验证
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter

# 读取示例
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 --"op read 'op://Private/Npmjs/一次性密码?attribute=otp'" Enter

# 需要时捕获输出
tmux -S“$SOCKET”捕获窗格-p -J -t“$SESSION”：0.0 -S -200

# 清理
tmux -S "$SOCKET" 终止会话 -t "$SESSION"
````

## 常用操作

### 读一个秘密

````bash
op 读取“op://app-prod/db/password”
````

### 获取一次性密码

````bash
op 读取“op://app-prod/npm/一次性密码？attribute=otp”
````

### 注入模板

````bash
echo "db_password: {{ op://app-prod/db/password }}" | OP注入
````

### 使用秘密环境变量运行命令

````bash
导出 DB_PASSWORD="op://app-prod/db/password"
op run -- sh -c '[ -n "$DB_PASSWORD" ] && echo "DB_PASSWORD 已设置" || echo "DB_PASSWORD 丢失"'
````

## 护栏

- 切勿将原始机密打印回给用户，除非他们明确请求该值。
- 更喜欢“op run”/“op Inject”，而不是将机密写入文件。
- 如果命令因“帐户未登录”而失败，请在同一 tmux 会话中再次运行“op signin”。
- 如果桌面应用程序集成不可用（无头/CI），请使用服务帐户令牌流。

## CI / 无头笔记

对于非交互式使用，请使用“OP_SERVICE_ACCOUNT_TOKEN”进行身份验证，并避免交互式“op Signin”。
服务帐户需要 CLI v2.18.0+。

## 参考文献

- `参考文献/get-started.md`
- `references/cli-examples.md`
- https://developer.1password.com/docs/cli/
- https://developer.1password.com/docs/service-accounts/