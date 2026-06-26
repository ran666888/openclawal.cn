---
title: "Blackbox — Delegate coding tasks to Blackbox AI CLI agent"
sidebar_label: "Blackbox"
description: "Delegate coding tasks to Blackbox AI CLI agent"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 黑匣子

将编码任务委托给 Blackbox AI CLI 代理。具有内置判断功能的多模型代理，可通过多个 LLM 运行任务并选择最佳结果。需要 blackbox CLI 和 Blackbox AI API 密钥。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/autonomous-ai-agents/blackbox` 安装 |
|路径| `可选技能/自主人工智能代理/黑盒` |
|版本 | `1.0.0` |
|作者 |赫尔墨斯特工（Nous Research）|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `编码代理`、`黑盒`、`多代理`、`法官`、`多模型` |
|相关技能| [`claude-code`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code), [`codex`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex), [`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 黑盒 CLI

通过 OpenClaw 终端将编码任务委托给 [Blackbox AI](https://www.blackbox.ai/)。 Blackbox 是一个多模型编码代理 CLI，它将任务分派给多个 LLM（Claude、Codex、Gemini、Blackbox Pro）并使用判断来选择最佳实现。

CLI 是[开源](https://github.com/blackboxaicode/cli)（GPL-3.0、TypeScript、从 Gemini CLI 派生），支持交互式会话、非交互式一次性、检查点、MCP 和视觉模型切换。

## 先决条件

- 安装了 Node.js 20+
- 安装 Blackbox CLI：`npm install -g @blackboxai/cli`
- 或从源安装：
  ````
  git 克隆 https://github.com/blackboxaicode/cli.git
  cd cli && npm install && npm install -g 。
  ````
- 来自 [app.blackbox.ai/dashboard](https://app.blackbox.ai/dashboard) 的 API 密钥
- 配置：运行“blackbox configure”并输入您的 API 密钥
- 在终端调用中使用 `pty=true` — Blackbox CLI 是一个交互式终端应用程序

## 一次性任务

````
终端(command="blackbox --prompt '将带有刷新令牌的 JWT 身份验证添加到 Express API'", workdir="/path/to/project", pty=true)
````

对于快速的刮擦工作：
````
终端(command="cd $(mktemp -d) && git init && blackbox --prompt '使用 SQLite 为待办事项构建 REST API'", pty=true)
````

## 后台模式（长时间任务）

对于需要几分钟的任务，请使用后台模式，以便您可以监控进度：

````
# 使用 PTY 在后台启动
终端（command =“blackbox --prompt '重构身份验证模块以使用OAuth 2.0'”，workdir =“〜/ project”，background = true，pty = true）
# 返回session_id

# 监控进度
流程（操作=“轮询”，session_id=“<id>”）
进程（操作=“日志”，session_id=“<id>”）

# 如果 Blackbox 提出问题，则发送输入
流程（操作=“提交”，session_id=“<id>”，数据=“是”）

# 如果需要的话杀掉
进程（操作=“杀死”，session_id=“<id>”）
````

## 检查点和恢复

Blackbox CLI 具有用于暂停和恢复任务的内置检查点支持：

````
# 任务完成后，Blackbox 显示检查点标签
# 继续执行后续任务：
Terminal(command="blackbox --resume-checkpoint 'task-abc123-2026-03-06' --prompt '现在向端点添加速率限制'", workdir="~/project", pty=true)
````

## 会话命令

在交互式会话期间，使用以下命令：

|命令|效果|
|---------|--------|
| `/压缩` |缩小对话历史记录以节省令牌 |
| `/清除` |抹去历史，重新开始 |
| `/统计` |查看当前代币使用情况 |
| `Ctrl+C` |取消当前操作 |

## 公关评论

克隆到临时目录以避免修改工作树：

````
Terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && blackbox --prompt '针对 main 审查此 PR。检查错误、安全问题和代码质量。'", pty=true)
````

## 并行工作

为独立任务生成多个 Blackbox 实例：

````
终端（command =“blackbox --prompt'修复登录错误'”，workdir =“/tmp/issue-1”，background = true，pty = true）
终端（命令 =“blackbox --prompt '添加身份验证单元测试'”，workdir =“/tmp/issue-2”，background = true，pty = true）

# 监控所有
过程（动作=“列表”）
````

## 多模型模式

Blackbox的独特之处在于通过多个模型运行相同的任务并判断结果。通过“黑盒配置”配置要使用的模型 - 选择多个提供者以启用主席/法官工作流程，其中 CLI 评估不同模型的输出并选择最佳模型。

## 关键标志

|旗帜|效果|
|------|--------|
| `--提示“任务”` |非交互式一次性执行 |
| `--resume-checkpoint“标签”` |从保存的检查点恢复 |
| `--yolo` |自动批准所有操作和模型切换 |
| `黑盒会话` |开始互动聊天会话 |
| `黑盒配置` |更改设置、提供商、型号 |
| `黑匣子信息` |显示系统信息 |

## 视觉支持

Blackbox 自动检测输入中的图像，并可以切换到多模态分析。 VLM 模式：
- `"once"` — 仅为当前查询切换模型
- `"session"` — 切换整个会话
- `"persist"` — 保持当前模型（无切换）

## 代币限制

通过 `.blackboxcli/settings.json` 控制令牌的使用：
```json
{
  “会话令牌限制”：32000
}
````

## 规则

1. **始终使用 `pty=true`** — Blackbox CLI 是一个交互式终端应用程序，在没有 PTY 的情况下将挂起
2. **使用 `workdir`** — 让代理专注于正确的目录
3. **长任务的背景** — 使用 `background=true` 并使用 `process` 工具进行监控
4. **不要干扰** — 使用“poll”/“log”进行监控，不要因为速度慢而终止会话
5. **报告结果**——完成后，检查发生了什么变化并为用户总结
6. **信用需要花钱** — Blackbox 使用基于信用的系统；多模型模式消耗积分更快
7. **检查先决条件** — 在尝试委派之前验证已安装“blackbox”CLI