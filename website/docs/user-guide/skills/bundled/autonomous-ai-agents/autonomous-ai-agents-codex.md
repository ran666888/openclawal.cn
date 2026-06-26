---
title: "Codex — Delegate coding to OpenAI Codex CLI (features, PRs)"
sidebar_label: "Codex"
description: "Delegate coding to OpenAI Codex CLI (features, PRs)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 法典

将编码委托给 OpenAI Codex CLI（功能、PR）。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/自主人工智能代理/codex` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `Coding-Agent`、`Codex`、`OpenAI`、`代码审查`、`重构` |
|相关技能| [`claude-code`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code)，[`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Codex CLI

通过 OpenClaw 终端将编码任务委托给 [Codex](https://github.com/openai/codex)。 Codex 是 OpenAI 的自主编码代理 CLI。

## 何时使用

- 建筑特色
- 重构
- 公关评论
- 批量问题修复

需要 codex CLI 和 git 存储库。

## 先决条件

- Codex 安装：`npm install -g @openai/codex`
- 配置 OpenAI 身份验证：`OPENAI_API_KEY` 或 Codex OAuth 凭据
  来自 Codex CLI 登录流程
- **必须在 git 存储库内运行** — Codex 拒绝在 git 存储库之外运行
- 在终端调用中使用 `pty=true` — Codex 是一个交互式终端应用程序

对于 OpenClaw 本身，“model.provider: openai-codex”使用 OpenClaw 管理的 Codex
在“hermes auth add openai-codex”之后来自“~/.hermes/auth.json”的 OAuth。对于
独立的 Codex CLI，有效的 CLI OAuth 会话可能存在于
`~/.codex/auth.json`;不要将丢失的“OPENAI_API_KEY”单独视为证据
Codex 授权缺失。

## 一次性任务

````
终端（command =“codex exec'将暗模式切换添加到设置'”，workdir =“~/project”，pty = true）
````

对于临时工作（Codex 需要 git 存储库）：
````
终端(command="cd $(mktemp -d) && git init && codex exec '用Python构建贪吃蛇游戏'", pty=true)
````

## 后台模式（长时间任务）

````
# 使用 PTY 在后台启动
终端（command =“codex exec --full-auto'重构身份验证模块'”，workdir =“~/project”，background = true，pty = true）
# 返回session_id

# 监控进度
流程（操作=“轮询”，session_id=“<id>”）
进程（操作=“日志”，session_id=“<id>”）

# 如果 Codex 提出问题，则发送输入
流程（操作=“提交”，session_id=“<id>”，数据=“是”）

# 如果需要的话杀掉
进程（操作=“杀死”，session_id=“<id>”）
````

## 关键标志

|旗帜|效果|
|------|--------|
| `执行“提示”` |一次性执行，完成后退出 |
| `--全自动` |沙盒化但自动批准工作区中的文件更改 |
| `--yolo` |没有沙箱，没有批准（最快，最危险）|
| `--沙箱危险-完全访问` |没有 Codex 沙箱；当主机服务上下文破坏 bubblewrap 时很有用 |

## OpenClaw Gateway 警告

从 OpenClaw 网关/服务上下文调用 Codex CLI 时（例如，
Telegram 驱动的代理会话），Codex“工作区写入”沙箱甚至可能失败
当相同的命令在用户的交互式 shell 中运行时。典型症状是
bubblewrap/用户命名空间错误，例如“设置 uid 映射：权限被拒绝”
或`环回：失败的RTM_NEWADDR：不允许操作`。

在这种情况下，更喜欢：

````
codex exec --sandbox 危险-完全访问“<任务>”
````

使用进程边界作为安全层：显式的“workdir”、干净的 git
启动前的状态、缩小任务提示、“git diff”审查、有针对性的测试以及
在进行广泛的更改之前进行人工/代理确认。

## 公关评论

克隆到临时目录以进行安全审查：

````
终端（命令=“REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
````

## 使用工作树修复并行问题

````
# 创建工作树
终端（命令 =“git worktree add -b fix/issue-78 /tmp/issue-78 main”，workdir =“~/project”）
终端（命令 =“git worktree add -b fix/issue-99 /tmp/issue-99 main”，workdir =“~/project”）

# 在每个中启动 Codex
终端（command =“codex --yolo exec'修复问题＃78：<描述>。完成后提交。'”，workdir =“/tmp/issue-78”，background = true，pty = true）
终端（command =“codex --yolo exec'修复问题＃99：<描述>。完成后提交。'”，workdir =“/tmp/issue-99”，background = true，pty = true）

# 监控
过程（动作=“列表”）

# 完成后，推送并创建PR
终端（命令=“cd /tmp/issue-78 && git push -u origin fix/issue-78”）
终端（命令 =“gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'”）

# 清理
终端（命令=“git worktree删除/tmp/issue-78”，workdir=“~/project”）
````

## 批量公关评论

````
# 获取所有 PR 参考
终端（命令=“git fetch origin'+refs/pull/*/head：refs/remotes/origin/pr/*'”，workdir=“~/project”）

# 并行审查多个 PR
终端（命令 =“codex exec '查看 PR #86。git diff origin/main...origin/pr/86'”，workdir =“~/project”，background = true，pty = true）
终端（命令 =“codex exec '查看 PR #87。git diff origin/main...origin/pr/87'”，workdir =“~/project”，background = true，pty = true）

# 发布结果
终端(command="gh pr comment 86 --body '<review>'", workdir="~/project")
````

## 规则

1. **始终使用 `pty=true`** — Codex 是一个交互式终端应用程序，在没有 PTY 的情况下挂起
2. **需要 Git 存储库** — Codex 不会在 git 目录之外运行。使用 `mktemp -d && git init` 进行暂存
3. **使用 `exec` 一次性** — `codex exec "prompt"` 干净利落地运行和退出
4. **`--full-auto` 用于构建** — 自动批准沙箱内的更改
5. **长任务的背景** — 使用 `background=true` 并使用 `process` 工具进行监控
6. **不要干扰**——用`poll`/`log`进行监控，对长时间运行的任务要有耐心
7. **并行即可** — 一次运行多个 Codex 进程以进行批处理工作