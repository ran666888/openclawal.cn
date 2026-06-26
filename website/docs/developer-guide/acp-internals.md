---
sidebar_position: 2
title: "ACP Internals"
description: "How the ACP adapter works: lifecycle, sessions, event bridge, approvals, and tool rendering"
---
# ACP 内部结构

ACP 适配器将 OpenClaw 的同步“AIAgent”包装在异步 JSON-RPC stdio 服务器中。

关键实现文件：

- `acp_adapter/entry.py`
- `acp_adapter/server.py`
- `acp_adapter/session.py`
- `acp_adapter/events.py`
- `acp_adapter/permissions.py`
- `acp_adapter/tools.py`
- `acp_adapter/auth.py`
- `acp_registry/agent.json`

## 启动流程

````文本
Hermes acp / hermes-acp / python -m acp_adapter
  -> acp_adapter.entry.main()
  -> 服务器启动前解析 --version / --check / --setup
  ->加载~/.hermes/.env
  -> 配置 stderr 日志记录
  -> 构造 HermesACPAgent
  -> acp.run_agent(代理, use_unstable_protocol=True)
````

Zed ACP 注册表路径通过“uvx --from 'openclaw[acp]==<version>' hermes-acp”启动相同的适配器，指向“openclaw” PyPI 版本。

标准输出保留用于 ACP JSON-RPC 传输。人类可读的日志会转到 stderr。

## 主要组件

### `HermesACPAgent`

`acp_adapter/server.py` 实现 ACP 代理协议。

职责：

- 初始化/验证
- 新的/加载/恢复/分叉/列表/取消会话方法
- 提示执行
- 会话模型切换
- 将同步 AIAgent 回调连接到 ACP 异步通知中

### `会话管理器`

`acp_adapter/session.py` 跟踪实时 ACP 会话。

每个会话存储：

- `session_id`
- `代理`
- `cwd`
- `模型`
-`历史`
- `取消事件`

管理器是线程安全的并支持：

- 创建
- 得到
- 删除
- 叉子
- 列表
- 清理
- CWD更新

### 事件桥

`acp_adapter/events.py` 将 AIAgent 回调转换为 ACP `session_update` 事件。

桥接回调：

- `工具进度回调`
- `thinking_callback` （当前在 ACP 桥中设置为 `None` — 推理通过 `step_callback` 转发）
- `step_callback`

由于“AIAgent”在工作线程中运行，而 ACP I/O 位于主事件循环上，因此桥使用：

````蟒蛇
asyncio.run_coroutine_threadsafe(...)
````

### 权限桥

`acp_adapter/permissions.py` 将危险的终端批准提示改编为 ACP 权限请求。

映射：

- `allow_once` -> OpenClaw `once`
- `allow_always` -> OpenClaw `always`
- 拒绝选项 -> OpenClaw `deny`

默认情况下拒绝超时和网桥故障。

### 工具渲染助手

`acp_adapter/tools.py` 将 OpenClaw 工具映射到 ACP 工具类型并构建面向编辑器的内容。

示例：

- `patch` / `write_file` -> 文件差异
- `terminal` -> shell 命令文本
- `read_file` / `search_files` -> 文本预览
- 大量结果 -> 截断文本块以确保 UI 安全

## 会话生命周期

````文本
新会话（cwd）
  -> 创建会话状态
  -> 创建 AIAgent(platform="acp",enabled_toolsets=["hermes-acp"])
  -> 将task_id/session_id绑定到cwd覆盖

提示（...，session_id）
  -> 从 ACP 内容块中提取文本
  -> 重置取消事件
  -> 安装回调+批准桥
  -> 在 ThreadPoolExecutor 中运行 AIAgent
  -> 更新会话历史记录
  -> 发出最终的代理消息块
````

### 取消

`取消（session_id）`：

- 设置会话取消事件
- 可用时调用“agent.interrupt()”
- 导致提示响应返回 `stop_reason="cancelled"`

### 分叉

`fork_session()` 将消息历史记录深度复制到新的实时会话中，保留对话状态，同时为分叉提供自己的会话 ID 和 cwd。

## 提供者/身份验证行为

ACP 没有实现自己的身份验证存储。

相反，它重用了 OpenClaw 的运行时解析器：

- `acp_adapter/auth.py`
- `hermes_cli/runtime_provider.py`

因此，ACP 会通告并使用当前配置的 OpenClaw 提供程序/凭证。它还总是通告终端设置身份验证方法（“hermes-setup”、args“--setup”），以便首次运行的注册表客户端可以在启动正常的 ACP 会话之前打开 OpenClaw 的交互式模型/提供程序配置。

## 工作目录绑定

ACP 会话带有编辑器 cwd。

会话管理器通过任务范围的终端/文件覆盖将该 cwd 绑定到 ACP 会话 ID，因此文件和终端工具相对于编辑器工作区进行操作。

## 重复的同名工具调用

事件桥跟踪每个工具名称的工具 ID FIFO，而不仅仅是每个名称一个 ID。这对于以下方面很重要：

- 并行同名通话
- 一步重复同名通话

如果没有 FIFO 队列，完成事件将附加到错误的工具调用。

## 审批回调恢复

ACP 在提示执行期间临时在终端工具上安装批准回调，然后恢复之前的回调。这可以避免永久在全局安装特定于 ACP 会话的批准处理程序。

## 目前的限制

- ACP 会话持久保存到共享的 `~/.hermes/state.db` (SessionDB) 中，并在进程重新启动时透明地恢复；它们出现在“session_search”中
- 当前在请求文本提取中忽略非文本提示块
- 特定于编辑器的用户体验因 ACP 客户端实现而异

## 相关文件

- `tests/acp/` — ACP 测试套件
- `toolsets.py` — `hermes-acp` 工具集定义
- `hermes_cli/main.py` — `hermes acp` CLI 子命令
- `pyproject.toml` — `[acp]` 可选依赖项 + `hermes-acp` 脚本