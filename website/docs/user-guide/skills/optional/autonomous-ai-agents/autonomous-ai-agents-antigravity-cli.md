---
title: "Antigravity Cli — Operate the Antigravity CLI (agy): plugins, auth, sandbox"
sidebar_label: "Antigravity Cli"
description: "Operate the Antigravity CLI (agy): plugins, auth, sandbox"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 反重力 CLI

操作 Antigravity CLI (agy)：插件、身份验证、沙箱。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/autonomous-ai-agents/antigravity-cli` 安装 |
|路径| `可选技能/自主人工智能代理/反重力-cli` |
|版本 | `0.1.0` |
|作者 |托尼·西蒙斯 (asimons81)，爱马仕经纪人 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `编码代理`、`反重力`、`CLI`、`Auth`、`插件`、`沙盒` |
|相关技能| [`grok`](/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-grok), [`codex`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex), [`claude-code`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code)，[`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 反重力 CLI (`agy`)

反重力 CLI 操作员指南，调用为“agy”。运行所有“agy”
通过 OpenClaw `terminal` 工具执行命令；检查其配置和日志
`读取文件`。这个技能是参考+过程——它不包裹网络
API，因此 OpenClaw 本身无需进行任何身份验证。

## 何时使用

- 安装、更新或冒烟测试“agy”二进制文件
- 一次性驾驶非交互式“agy --print”/“agy -p”
- 调试反重力身份验证、沙箱、权限或插件状态
- 读取反重力设置、按键绑定、对话或日志

## 心理模型

反重力有两层——保持它们不同，否则指导就会错误：

1. **Shell 包装器命令** — `agy help`、`agy install`、`agy plugin`、
   `agy 更新`、`agy 变更日志`。通过“终端”工具运行它们。
2. **交互式会话中斜线命令** — `/config`、`/permissions`、
   `/skills`、`/agents` 等。这些仅存在于正在运行的 `agy` TUI 中
   会话，而不是在 shell 包装器上。

`agy help` 显示 shell 包装器表面，而不是会话中的斜杠命令。

## 先决条件

- PATH 上的“agy”二进制文件。通过`terminal`工具验证：
  `命令 -v agy && agy --version`。
- 此技能不需要环境变量或 API 密钥 - 反重力管理自己的
  通过操作系统密钥环/浏览器登录进行身份验证（请参阅下面的身份验证）。

## 如何运行

通过“terminal”工具调用每个“agy”命令。示例：

````
终端（命令=“agy --version”）
终端（命令=“agy帮助”）
终端（命令=“agy插件列表”）
Terminal(command="agy --print '用 3 个项目符号总结存储库'", workdir="/path/to/project")
````

对于交互式多回合 TUI 会话，请使用“pty=true”启动“agy”（并且
tmux 用于捕获/监控），与“codex”/“claude-code”相同的模式
技能使用。对于一次性冒烟测试和脚本提示，更喜欢
`agy --print`（非交互式）。

要检查 Antigravity 自己的文件，请在 Core 下的路径上使用“read_file”
下面的路径 - 不要通过终端“cat”它们。

## 核心路径

- 二进制/入口点：`agy`
- 应用程序数据目录：`~/.gemini/antigravity-cli/`
- 设置文件：`~/.gemini/antigravity-cli/settings.json`
- 键绑定文件：`~/.gemini/antigravity-cli/keybindings.json`
- 日志：`~/.gemini/antigravity-cli/log/cli-*.log`
- 对话：`~/.gemini/antigravity-cli/conversations/`
- 大脑文物：`~/.gemini/antigravity-cli/brain/`
- 历史：`~/.gemini/antigravity-cli/history.jsonl`
- 插件暂存：`~/.gemini/antigravity-cli/plugins/<plugin_name>/`

## 快速参考

### 包装命令
- `agy 变更日志`
- `阿吉帮助`
- `敏捷安装`
- `agy 插件` / `agy 插件`
- `阿吉更新`

### 有用的标志
- `--add-dir`
- `--继续` / `-c`
- `--对话`
- `--危险地跳过权限`
- `--print` / `-p`
- `--打印超时`
- `--提示`
- `--提示交互` / `-i`
- `--沙箱`
- `--日志文件`
- `--版本`

### 插件子命令（`agy plugin --help`）
- `列表`、`导入 [源]`、`安装 <目标>`、`卸载 <名称>`、
  `启用 <名称>`、`禁用 <名称>`、`验证 [路径]`、`链接 <mp> <目标>`、
  `帮助`

### 安装标志（`agy install --help`）
- `--dir`、`--skip-aliases`、`--skip-path`

### 会话中斜线命令
- **对话控制：** `/resume` (`/switch`)、`/rewind` (`/undo`)、
  `/rename <名称>`、`/clear`、`/fork`、`/reset`、`/new`
- **设置和工具：** `/config`、`/settings`、`/permissions`、`/model`、
  `/keybindings`、`/statusline`、`/tasks`、`/skills`、`/mcp`、`/open <路径>`、
  `/usage`、`/logout`、`/agents`
- **提示助手：** `@` 路径自动完成，`esc esc` 清除提示（当
  不流式传输），`!` 直接运行终端命令，`?` 打开帮助

## 设置和权限

### 常用设置键（`settings.json`）
- `允许非工作空间访问`
- `颜色方案`
- `permissions.allow`
- `可信工作区`

### 权限模式
“请求审查”、“始终进行”、“严格”、“在沙箱中进行”。

### 沙箱行为
- `enableTerminalSandbox` 是 `settings.json` 中的布尔值；默认为“假”。
- 启动时覆盖（`--sandbox`、`--dangerously-skip-permissions`）可以
  取代当前会话的持久设置。

## 身份验证行为

- CLI 首先尝试操作系统安全密钥环。
- 如果没有保存的会话，它会退回到基于浏览器的 Google 登录。
- 在本地打开默认浏览器；通过 SSH，它会打印授权 URL
  并期望粘贴回授权代码。
- `/logout` 删除保存的凭据。

## 插件

- `~/.gemini/antigravity-cli/plugins/<plugin_name>/`下的插件阶段。
- 他们可以捆绑技能、代理、规则、MCP 服务器和挂钩。
- `agy plugin list` 不返回导入的插件是有效的空状态。

## 陷阱

- `agy help` 显示包装器命令，而不是交互式斜杠命令。
- `agy --version` 是安全的非交互式版本检查； `agy 版本`是
  交互式，并且在没有真正的 TTY 的情况下可能会失败。
- 寻找失败的第一个地方：`~/.gemini/antigravity-cli/log/cli-*.log`
  （用“read_file”读取）。
- 不要将持久 JSON 设置与启动时覆盖混淆。
- `~/.gemini/antigravity-cli/bin/agentapi` 是 `agy agentapi` 的薄包装。
- 在 WSL 上，令牌存储是基于文件的，因此身份验证问题通常是本地文件/
  会话状态问题，而不是仅浏览器的问题。
- 工作空间身份可以取决于启动目录和“.antigravitycli”
  项目标记。

## 验证

确认安装是真实且可用的，全部通过“终端”工具（阅读
带有“read_file”的文件）：

1.`终端（命令=“命令-v agy”）`
2. `终端（命令=“agy --version”）`
3. `终端（命令=“agy help”）`
4.`终端（命令=“agy插件列表”）`
5. `~/.gemini/antigravity-cli/settings.json` 上的 `read_file`
6. 最新的 `~/.gemini/antigravity-cli/log/cli-*.log` 上的 `read_file`
7. 如果需要，请在`~/.gemini/antigravity-cli/keybindings.json`上读取`read_file`

## 支持文件

- `references/cli-docs.md` — 入门、使用的浓缩笔记，
  和功能文档。