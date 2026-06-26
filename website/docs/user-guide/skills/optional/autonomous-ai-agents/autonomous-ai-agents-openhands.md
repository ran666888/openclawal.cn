---
title: "Openhands — Delegate coding to OpenHands CLI (model-agnostic, LiteLLM)"
sidebar_label: "Openhands"
description: "Delegate coding to OpenHands CLI (model-agnostic, LiteLLM)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#张开双手

将编码委托给 OpenHands CLI（与模型无关，LiteLLM）。

## 技能元数据

| | |
|---|---|
|来源 | Optional — install with `hermes skills install official/autonomous-ai-agents/openhands` |
|路径| `可选技能/自主人工智能代理/openhands` |
|版本 | `0.1.0` |
|作者 |蒂姆·科普塞尔 (xzessmedia)，爱马仕经纪人 |
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | `Coding-Agent`, `OpenHands`, `Model-Agnostic`, `LiteLLM` |
|相关技能| [`claude-code`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code), [`codex`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex), [`opencode`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode)，[`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# OpenHands CLI

通过“terminal”工具将编码任务委托给 [OpenHands CLI](https://github.com/All-Hands-AI/OpenHands)。 OpenHands 与模型无关：任何 LiteLLM 支持的提供商（OpenAI、Anthropic、OpenRouter、DeepSeek、Ollama、vLLM 等）。

该技能是批量/一次性委派的无头模式包装器。 OpenClaw 不使用交互式文本 UI。

## 何时使用

- 用户希望将编码任务专门委托给 OpenHands。
- 用户想要一个可以在非 Anthropic / 非 OpenAI 提供商（DeepSeek、Qwen、Ollama、vLLM、Nous 等）上运行的编码代理 - 兄弟技能“claude-code”和“codex”与一个供应商绑定。
- 工作空间内的多步骤文件编辑 + shell 命令。

对于 Claude 本地人，更喜欢“claude-code”。对于 OpenAI 原生，更喜欢“codex”。 For OpenClaw-native subagents, use `delegate_task`.

## 先决条件

1. 安装上游（需要 Python 3.12+ 和 `uv`）：

   ````
   terminal(command="uv tool install openhands --python 3.12")
   ````

   验证：“openhands --version”（在撰写本文时当前为“OpenHands CLI 1.16.0”/“SDK v1.21.0”）。

2. 选择一个模型并为 `--override-with-envs` 设置环境变量：

   ````
   export LLM_MODEL=openrouter/openai/gpt-4o-mini # 或任何 LiteLLM slug
   导出 LLM_API_KEY=$OPENROUTER_API_KEY
   export LLM_BASE_URL=https://openrouter.ai/api/v1 # 原生 OpenAI 省略
   ````

   `LLM_MODEL` 使用 LiteLLM 的完整 slug。当提供者是 OpenRouter 时，slug 带有双前缀：“openrouter/<vendor>/<model>”（例如“openrouter/anthropic/claude-sonnet-4.5”）。对于原生 Anthropic：“anthropic/claude-sonnet-4-5”。对于原生 OpenAI：“openai/gpt-4o-mini”。

3. 抑制启动横幅，以便 JSON 输出前面不会出现 ASCII 艺术：

   ````
   导出 OPENHANDS_SUPPRESS_BANNER=1
   ````

## 如何运行

始终通过“终端”工具调用。始终传递“--headless --json --override-with-envs --exit-without-confirmation”以实现自动化。

### 一次性任务

````
终端（
  command="OPENHANDS_SUPPRESS_BANNER=1 LLM_MODEL=openrouter/openai/gpt-4o-mini LLM_API_KEY=$OPENROUTER_API_KEY LLM_BASE_URL=https://openrouter.ai/api/v1 openhands --headless --json --override-with-envs --exit-without-confirmation -t '为 src/ 中的所有 API 调用添加错误处理'",
  workdir =“/路径/到/项目”，
  超时=600
）
````

### 长期任务的背景

````
终端（命令=“<同上>”，workdir=“/path/to/project”，background=true，notify_on_complete=true）
流程（操作=“轮询”，session_id=“<id>”）
进程（操作=“日志”，session_id=“<id>”）
````

### 恢复之前的对话

OpenHands 在每次运行结束时打印“Conversation ID: <32-hex>”和“Hint: openhands --resume <dashed-uuid>”行。使用虚线形式恢复：

````
终端（
  command="OPENHANDS_SUPPRESS_BANNER=1 LLM_MODEL=... openhands --headless --json --override-with-envs --exit-without-confirmation --resume <dashed-uuid> -t '现在修复您发现的错误'",
  workdir =“/路径/到/项目”
）
````

## 真实旗帜列表

已针对“openhands --help”（CLI 1.16.0）进行验证。任何不在该表中的内容都不是标志 - 通过 env var 或设置文件传递它。

|旗帜|效果|
|------|--------|
| `--无头` |无 UI，需要“-t”或“-f”。自动批准所有操作（在此模式下没有“--llm-approve”）。 |
| `--json` | JSONL 事件流（需要“--headless”）。 |
| `-t 文本` |任务提示。 |
| `-f 路径` |从文件中读取任务。 |
| `--resume [ID]` |继续谈话。没有 ID → 列出最近的。 |
| `--最后` |恢复最近的一次（使用“--resume”）。 |
| `--override-with-envs` |应用 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` 环境变量。如果没有这个，OpenHands 将使用 `~/.openhands/settings.json` 并忽略环境。 |
| `--退出而不确认` |不要显示“您确定吗”退出对话框。 |
| `--always-approve` / `--yolo` |自动批准每个操作（默认为“--headless”）。 |
| `--llm-approve` |基于 LLM 的安全门（仅交互式 - 不适用于无头）。 |
| `--version` / `-v` |打印版本并退出。 |

**没有`--model`、`--max-iterations`、`--workspace`、`--sandbox`、`--sandbox-type`标志。**模型是`LLM_MODEL`。工作空间是您传递给“terminal”工具的“workdir”。沙箱/运行时是“RUNTIME”和“SANDBOX_VOLUMES”环境变量。

## JSON 事件架构

使用“--json --headless”，OpenHands 会发出 JSONL — 每行一个 JSON 对象，加上一些非 JSON 状态行（“正在初始化代理...”、“代理正在工作”、“代理完成”、最后的摘要框、“再见！”、“对话 ID：”、“提示：”）。过滤以“{”开头的行。

顶级“kind”字段区分事件：

- `MessageEvent` — 用户/代理文本轮流。 “源”是“用户”或“代理”。
- `ActionEvent` — 代理选择了一个工具。读取“tool_name”（“file_editor”、“terminal”、“finish”）和“action.kind”（“FileEditorAction”、“TerminalAction”、“FinishAction”）。
- `ObservationEvent` — 工具结果。 `observation.is_error` 是成功标志。 “源”就是“环境”。
- `ActionEvent` 中的 `FinishAction` 在 `action.message` 中携带代理的最终消息。

cli 首先打印 LiteLLM/Authlib 中的所有 stderr — 请参阅陷阱。仅逐行解析标准输出，忽略不以“{”开头的行。

## 陷阱

- **每次调用时都会出现 LiteLLM 警告。** CLI 会向 stderr 打印 `bedrock-runtime` 和 `sagemaker-runtime` 警告，因为未安装 `botocore`。加上 Authlib 弃用。这些都是噪音，而不是失败。将 stderr 通过管道传输到 `/dev/null` 或在向用户显示之前将其过滤掉。
- **横幅垃圾邮件。** 如果没有“OPENHANDS_SUPPRESS_BANNER=1”，每次运行都会以多行“+--+”ASCII 框开始，为 SDK 做广告。始终将其导出。
- **`--override-with-envs` 对于自动化是必需的。** 如果没有它，OpenHands 会忽略 `LLM_API_KEY` / `LLM_BASE_URL` / `LLM_MODEL` 并回退到 `~/.openhands/settings.json`。在全新安装中，此文件不存在，并且 CLI 挂起等待首次运行安装。
- **模型 slug 是 LiteLLM 的，而不是提供商的。** `openrouter/openai/gpt-4o-mini` 有效； `openai/gpt-4o-mini` 而指向 OpenRouter 时却没有。 `anthropic/claude-sonnet-4-5`（连字符）是原生 Anthropic； `openrouter/anthropic/claude-sonnet-4.5`（点）是通过 OpenRouter 实现的。弄错了 → 神秘的 LiteLLM 400。
- **`pip install openhands-ai` 是错误的软件包。** 这是旧版 V0 SDK。新的 CLI 是“uv tool install openhands --python 3.12”。没有维护的 conda 包。
- **简历 ID 格式很繁琐。** CLI 以“对话 ID：f46573d9cfdb45e492ca189bde40019b”（无破折号）结尾，然后是“提示：openhands --resume f46573d9-cfdb-45e4-92ca-189bde40019b”（有破折号）。使用虚线形式。
- **Headless 忽略 `--llm-approve`。** 如果你通过它，你会得到一个 argparse 错误。无头模式硬编码始终批准。
- **没有 Windows 支持上游。** OpenHands 文档需要 Windows 上的 WSL。该技能相应地被限制为“[linux, macos]”。
- **`~/.openhands/conversations/<id>/` 累积。** 每次运行都会保留一条轨迹。如果运行批次，请清理它。
- **大量安装（~200 个软件包）。** 使用 `uv tool install`（隔离的 venv）以避免与活动项目发生依赖冲突。

## 验证

````
终端（
  command="OPENHANDS_SUPPRESS_BANNER=1 LLM_MODEL=openrouter/openai/gpt-4o-mini LLM_API_KEY=$OPENROUTER_API_KEY LLM_BASE_URL=https://openrouter.ai/api/v1 openhands --headless --json --override-with-envs --exit-without-confirmation -t '通过以下方式将字符串 OPENHANDS_OK 打印到 stdout终端工具。'",
  工作目录=“/tmp”，
  超时=120
）
````

如果 JSONL 流以“FinishAction”结束，其“action.message”提到“OPENHANDS_OK”，则安装正在运行。

## 相关

- [OpenHands GitHub](https://github.com/All-Hands-AI/OpenHands)
- [OpenHands CLI 命令参考](https://docs.openhands.dev/openhands/usage/cli/command-reference)
- 兄弟技能：“claude-code”（仅 Anthropic）、“codex”（仅 OpenAI）、“opencode”（通过 OpenCode 的多提供商）、“openclaw”（通过“delegate_task”的 OpenClaw 子代理）。