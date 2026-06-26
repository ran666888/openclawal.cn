---
sidebar_position: 3
title: "Agent Loop Internals"
description: "Detailed walkthrough of AIAgent execution, API modes, tools, callbacks, and fallback behavior"
---
# 代理循环内部结构

核心编排引擎是“run_agent.py”的“AIAgent”类——一个大文件，用于处理从提示组装到工具调度再到提供程序故障转移的所有内容。

## 核心职责

`AIAgent` 负责：

- 通过“prompt_builder.py”组装有效的系统提示和工具模式
- 选择正确的提供商/API 模式（chat_completions、codex_responses、anthropic_messages）
- 通过取消支持进行可中断模型调用
- 执行工具调用（通过线程池顺序或并发）
- 以 OpenAI 消息格式维护对话历史记录
- 处理压缩、重试和回退模型切换
- 跟踪父代理和子代理的迭代预算
- 在上下文丢失之前刷新持久内存

## 两个入口点

````蟒蛇
# 简单接口 — 返回最终响应字符串
response = agent.chat("修复main.py中的bug")

# 完整接口 - 返回带有消息、元数据、使用统计信息的字典
结果 = agent.run_conversation(
    user_message="修复main.py中的错误",
    system_message=None, # 如果省略则自动构建
    conversation_history=None, # 如果省略则从会话中自动加载
    任务id=“task_abc123”
）
````

`chat()` 是 `run_conversation()` 的一个薄包装，它从结果字典中提取 `final_response` 字段。

## API 模式

OpenClaw 支持三种 API 执行模式，通过提供者选择、显式参数和基本 URL 启发式解析：

| API模式 |用于 |客户类型 |
|----------|----------|------------|
| `chat_completions` | OpenAI 兼容端点（OpenRouter、自定义、大多数提供商）| `openai.OpenAI` |
| `codex_responses` | OpenAI Codex / 响应 API |具有响应格式的“openai.OpenAI” |
| `anthropic_messages` |原生人类消息 API |通过适配器的“anthropic.Anthropic” |

该模式决定消息的格式、工具调用的结构、响应的解析方式以及缓存/流的工作方式。在 API 调用之前和之后，这三者都集中在相同的内部消息格式（OpenAI 风格的“角色”/“内容”/“工具调用”字典）。

**模式解析顺序：**
1.显式`api_mode`构造函数arg（最高优先级）
2. 特定于提供者的检测（例如，“anthropic”提供者→“anthropic_messages”）
3. 基本 URL 启发式（例如，`api.anthropic.com`→`anthropic_messages`）
4.默认值：`chat_completions`

## 转动生命周期

代理循环的每次迭代都遵循以下顺序：

````文本
运行对话（）
  1.如果没有提供则生成task_id
  2. 将用户消息追加到对话历史记录中
  3. 构建或重用缓存的系统提示符（prompt_builder.py）
  4. 检查是否需要预检压缩（>50% 上下文）
  5. 根据对话历史记录构建 API 消息
     - chat_completions：OpenAI 格式按原样
     - codex_responses：转换为Responses API输入项
     - anthropic_messages：通过 anthropic_adapter.py 转换
  6.注入临时提示层（预算警告、上下文压力）
  7. 如果在 Anthropic 上，应用提示缓存标记
  8. 进行可中断的API调用(_interruptible_api_call)
  9. 解析响应：
     - 如果 tool_calls：执行它们，附加结果，循环回到步骤 5
     - 如果是文本响应：持续会话，如果需要刷新内存，返回
````

### 消息格式

所有消息在内部都使用 OpenAI 兼容格式：

````蟒蛇
{“角色”：“系统”，“内容”：“...”}
{“角色”：“用户”，“内容”：“...”}
{“角色”：“助理”，“内容”：“...”，“tool_calls”：[...]}
{“角色”：“工具”，“tool_call_id”：“...”，“内容”：“...”}
````

推理内容（来自支持扩展思维的模型）存储在 `assistant_msg["reasoning"]` 中，并可以选择通过 `reasoning_callback` 显示。

### 消息交替规则

代理循环强制执行严格的消息角色交替：

- 系统消息后：“用户→助手→用户→助手→...”
- 工具调用期间：`Assistant (with tool_calls) → Tool → Tool → ... → Assistant`
- **绝不**连续两条助理消息
- **从不**连续两条用户消息
- **仅** `tool` 角色可以有连续条目（并行工具结果）

提供者验证这些序列并将拒绝畸形的历史记录。

## 可中断的 API 调用

API 请求被包装在 `_interruptible_api_call()` 中，它在后台线程中运行实际的 HTTP 调用，同时监视中断事件：

````文本
┌────────────────────────────────────────────────────┐
│ 主线程 API 线程 │
│ │
│ 等待：HTTP POST │
│ - 已准备好回应 ────▶ 向供应商 │
│ - 中断事件 │
│ - 超时 │
└────────────────────────────────────────────────────┘
````

中断时（用户发送新消息、“/stop”命令或信号）：
- API线程被放弃（响应被丢弃）
- 代理可以处理新的输入或干净地关闭
- 对话历史记录中不会注入部分响应

## 工具执行

### 顺序与并发

当模型返回工具调用时：

- **单一工具调用** → 直接在主线程中执行
- **多个工具调用** → 通过 `ThreadPoolExecutor` 同时执行
  - 例外：标记为交互式的工具（例如“clarify”）强制顺序执行
  - 无论完成顺序如何，结果都会重新插入原始工具调用顺序

### 执行流程

````文本
对于response.tool_calls中的每个tool_call：
    1. 从tools/registry.py解析处理程序
    2. 触发 pre_tool_call 插件钩子
    3.检查是否有危险命令(tools/approval.py)
       - 如果危险：调用approval_callback，等待用户
    4. 使用 args + task_id 执行处理程序
    5. 触发 post_tool_call 插件钩子
    6. 将 {"role": "tool", "content": result} 追加到历史记录中
````

### 代理级工具

一些工具在到达“handle_function_call()”之前被“run_agent.py”拦截：

|工具|为什么被拦截|
|------|--------------------|
| `待办事项` |读取/写入代理本地任务状态 |
| `记忆` |写入具有字符限制的持久内存文件 |
| `会话搜索` |通过代理的会话数据库查询会话历史记录 |
| `委托任务` |生成具有隔离上下文的子代理 |

这些工具直接修改代理状态并返回综合工具结果，而无需通过注册表。

## 回调表面

“AIAgent”支持特定于平台的回调，可实现 CLI、网关和 ACP 集成的实时进度：

|回拨|被解雇时 |使用者 |
|----------|------------|---------|
| `工具进度回调` |每个工具执行之前/之后 | CLI 微调器、网关进度消息 |
| `思考_回调` |当模型开始/停止思考时 | CLI“思考...”指示器 |
| `reasoning_callback` |当模型返回推理内容时 | CLI推理显示、网关推理块|
| `澄清回调` |当调用 `clarify` 工具时 | CLI输入提示、网关交互消息 |
| `step_callback` |每次完成代理轮后|网关步骤跟踪、ACP 进度 |
| `stream_delta_callback` |每个流令牌（启用时）| CLI 流式显示 |
| `tool_gen_callback` |当从流中解析工具调用时 |微调器中的 CLI 工具预览 |
| `状态回调` |状态变化（思考、执行等）| ACP 状态更新 |

## 预算和后备行为

### 迭代预算

代理通过“IterationBudget”跟踪迭代：

- 默认：90 次迭代（可通过 `agent.max_turns` 配置）
- 每个代理都有自己的预算。子代理的独立预算上限为“delegation.max_iterations”（默认 50）——父代理 + 子代理的总迭代次数可以超过父代理的上限
- 达到 100% 时，代理停止并返回已完成工作的摘要

### 后备模型

当主模型失败时（429速率限制、5xx服务器错误、401/403身份验证错误）：

1.检查配置中的`fallback_providers`列表
2. 按顺序尝试每个后备
3. 成功后，继续与新提供商对话
4. 在 401/403 上，在故障转移之前尝试刷新凭据

后备系统还独立地涵盖辅助任务——视觉、压缩和网页提取，每个任务都有自己的后备链，可通过“auxiliary.*”配置部分进行配置。

## 压缩和持久化

### 当压缩触发时

- **预检**（API 调用之前）：如果对话超过模型上下文窗口的 50%
- **网关自动压缩**：如果对话超过 85%（更具攻击性，在回合之间运行）

### 压缩过程中会发生什么

1.内存先刷新到磁盘（防止数据丢失）
2. 中间对话轮流总结成紧凑的摘要
3. 最后 N 条消息完整保留（“compression.protect_last_n”，默认值：20）
4. 工具调用/结果消息对保持在一起（从不拆分）
5. 生成新的会话沿袭 ID（压缩创建“子”会话）

### 会话持续性

每回合后：
- 消息保存到会话存储（SQLite 通过 `hermes_state.py`）
- 内存更改刷新到`MEMORY.md`/`USER.md`
- 稍后可以通过“/resume”或“hermes chat --resume”恢复会话

## 关键源文件

|文件|目的|
|------|---------|
| `run_agent.py` | AIAgent 类 — 完整的代理循环 |
| `agent/prompt_builder.py` |系统提示从记忆、技能、背景文件、性格中拼装|
| `agent/context_engine.py` | ContextEngine ABC — 可插入上下文管理 |
| `agent/context_compressor.py` |默认引擎——有损摘要算法|
| `agent/prompt_caching.py` |人为提示缓存标记和缓存指标|
| `代理/auxiliary_client.py` |用于辅助任务（愿景、总结）的辅助法学硕士客户端 |
| `model_tools.py` |工具模式集合，“handle_function_call()”调度 |

## 相关文档

- [提供商运行时解析](./provider-runtime.md)
- [提示组装](./prompt- assembly.md)
- [上下文压缩和提示缓存](./context-compression-and-caching.md)
- [工具运行时](./tools-runtime.md)
- [架构概述](./architecture.md)