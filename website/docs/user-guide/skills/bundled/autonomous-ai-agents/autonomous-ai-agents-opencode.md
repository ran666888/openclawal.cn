---
title: "Opencode — Delegate coding to OpenCode CLI (features, PR review)"
sidebar_label: "Opencode"
description: "Delegate coding to OpenCode CLI (features, PR review)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 打开代码

将编码委托给 OpenCode CLI（功能、PR 审查）。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/自主人工智能代理/开放代码` |
|版本 | `1.2.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `编码代理`、`OpenCode`、`自治`、`重构`、`代码审查` |
|相关技能| [`claude-code`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code), [`codex`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex), [`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# OpenCode CLI

使用 [OpenCode](https://opencode.ai) 作为由 OpenClaw 终端/流程工具编排的自主编码工作者。 OpenCode 是一个与提供商无关的开源 AI 编码代理，具有 TUI 和 CLI。

## 何时使用

- 用户明确要求使用 OpenCode
- 您需要外部编码代理来实现/重构/审查代码
- 您需要长时间运行的编码会话和进度检查
- 您希望在隔离的工作目录/工作树中并行执行任务

## 先决条件

- 安装 OpenCode：`npm i -g opencode-ai@latest` 或 `brew install anomalyco/tap/opencode`
- 身份验证配置：“opencode auth login”或设置提供程序环境变量（OPENROUTER_API_KEY 等）
- 验证：“opencode auth list”应至少显示一个提供商
- 代码任务的 Git 存储库（推荐）
- `pty=true` 用于交互式 TUI 会话

## 二进制解析（重要）

Shell 环境可能会解析不同的 OpenCode 二进制文件。如果您的终端和 OpenClaw 之间的行为不同，请检查：

````
终端（命令=“which -a opencode”）
终端（命令=“opencode--版本”）
````

如果需要，请固定显式二进制路径：

````
终端（命令=“$HOME/.opencode/bin/opencode运行'...'”，workdir=“~/project”，pty=true）
````

## 一次性任务

使用“opencode run”来执行有界的、非交互式任务：

````
Terminal(command="opencode run '向 API 调用添加重试逻辑并更新测试'", workdir="~/project")
````

使用“-f”附加上下文文件：

````
终端（command =“opencode run'检查此配置是否存在安全问题'-f config.yaml -f .env.example”，workdir =“~/project”）
````

用 `--think` 显示模型思维：

````
终端(command="opencode run '调试 CI 中测试失败的原因' --thinking", workdir="~/project")
````

强制指定模型：

````
终端(command="opencode run '重构身份验证模块' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
````

## 互动会议（背景）

对于需要多次交换的迭代工作，请在后台启动 TUI：

````
终端（命令=“opencode”，workdir=“〜/项目”，背景= true，pty = true）
# 返回session_id

# 发送提示
process(action="submit", session_id="<id>", data="实施 OAuth 刷新流程并添加测试")

# 监控进度
流程（操作=“轮询”，session_id=“<id>”）
进程（操作=“日志”，session_id=“<id>”）

# 发送后续输入
process(action="submit", session_id="<id>", data="现在添加令牌过期的错误处理")

# 干净退出 — Ctrl+C
进程（操作=“写入”，session_id=“<id>”，数据=“\x03”）
# 或者直接杀死进程
进程（操作=“杀死”，session_id=“<id>”）
````

**重要提示：** 不要使用 `/exit` — 它不是有效的 OpenCode 命令，而是会打开代理选择器对话框。使用 Ctrl+C (`\x03`) 或 `process(action="kill")` 退出。

### TUI 按键绑定

|关键|行动|
|-----|--------|
| `输入` |提交消息（如果需要请按两次）|
| `选项卡` |在代理之间切换（构建/计划）|
| `Ctrl+P` |打开命令面板 |
| `Ctrl+X L` |切换会话 |
| `Ctrl+X M` |开关型号|
| `Ctrl+X N` |新会议 |
| `Ctrl+X E` |打开编辑器 |
| `Ctrl+C` |退出 OpenCode |

### 恢复会话

退出后，OpenCode 会打印会话 ID。继续：

````
Terminal(command="opencode -c", workdir="~/project", background=true, pty=true) # 继续上一个会话
Terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true) # 特定会话
````

## 常用标志

|旗帜|使用|
|------|-----|
| `运行'提示'` |一键执行并退出 |
| `--继续` / `-c` |继续上次 OpenCode 会话 |
| `--session <id>` / `-s` |继续特定会话 |
| `--agent <名称>` |选择 OpenCode 代理（构建或计划） |
| `--模型提供者/模型` |力具体型号|
| `--format json` |机器可读的输出/事件 |
| `--file <路径>` / `-f` |将文件附加到消息 |
| `--思考` |显示模型思维块 |
| `--variant <级别>` |推理努力（高、最大、最小）|
| `--title <名称>` |命名会话 |
| `--附加 <url>` |连接到正在运行的 opencode 服务器 |

## 程序

1. 验证工具准备情况：
   - `终端（命令=“opencode --version”）`
   -`终端（命令=“opencode auth list”）`
2. 对于有界任务，请使用“opencode run '...”（不需要 pty）。
3. 对于迭代任务，以“background=true, pty=true”启动“opencode”。
4. 使用 process(action="poll"|"log")` 监控长任务。
5. 如果 OpenCode 要求输入，请通过 `process(action="submit", ...)` 进行响应。
6. 使用 process(action="write", data="\x03")` 或 process(action="kill")` 退出。
7. 向用户总结文件更改、测试结果和后续步骤。

## PR 审核工作流程

OpenCode 有一个内置的 PR 命令：

````
终端（命令=“opencode pr 42”，workdir=“~/project”，pty=true）
````

或者在临时克隆中进行审查以进行隔离：

````
Terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run '查看此 PR 与 main。报告 bug、安全风险、测试差距和风格问题。' -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')", pty=true)
````

## 并行工作模式

使用单独的工作目录/工作树以避免冲突：

````
终端（命令=“opencode运行'修复问题＃101并提交'”，workdir =“/ tmp/issue-101”，background = true，pty = true）
终端（命令=“opencode运行'添加解析器回归测试并提交'”，workdir =“/ tmp/issue-102”，background = true，pty = true）
过程（动作=“列表”）
````

## 会话和成本管理

列出过去的会话：

````
终端（命令=“打开代码会话列表”）
````

检查代币使用情况和成本：

````
终端（命令=“opencode stats”）
终端（命令=“opencode stats --days 7 --models anthropic/claude-sonnet-4”）
````

## 陷阱

- 交互式“opencode”（TUI）会话需要“pty=true”。 `opencode run` 命令不需要 pty。
- `/exit` 不是一个有效的命令——它会打开一个代理选择器。使用 Ctrl+C 退出 TUI。
- 路径不匹配可能会选择错误的 OpenCode 二进制/模型配置。
- 如果 OpenCode 出现卡住，请在终止前检查日志：
  - `process(action="log", session_id="<id>")`
- 避免在并行 OpenCode 会话之间共享一个工作目录。
- 可能需要按 Enter 两次才能在 TUI 中提交（一次用于完成文本，一次用于发送）。

## 验证

冒烟测试：

````
终端（命令=“opencode run '准确响应：OPENCODE_SMOKE_OK'”）
````

成功标准：
- 输出包括“OPENCODE_SMOKE_OK”
- 命令退出时没有提供者/模型错误
- 对于代码任务：预期文件已更改并且测试通过

## 规则

1. 对于一次性自动化，更喜欢“opencode run”——它更简单，并且不需要 pty。
2. 仅在需要迭代时才使用交互后台模式。
3. 始终将 OpenCode 会话范围限制为单个存储库/工作目录。
4. 对于长期任务，请提供“流程”日志中的进度更新。
5. 报告具体结果（文件更改、测试、剩余风险）。
6. 使用 Ctrl+C 或 Kill 退出交互式会话，切勿使用“/exit”。