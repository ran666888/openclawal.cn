---
sidebar_position: 9
title: "Tools Runtime"
description: "Runtime behavior of the tool registry, toolsets, dispatch, and terminal environments"
---
# 工具运行时

OpenClaw 工具是分组为工具集的自注册功能，并通过中央注册/调度系统执行。

主要文件：

- `工具/registry.py`
- `model_tools.py`
- `工具集.py`
- `工具/terminal_tool.py`
- `工具/环境/*`

## 工具注册模型

每个工具模块在导入时都会调用“registry.register(...)”。

model_tools.py 负责导入/发现工具模块并构建模型使用的模式列表。

### `registry.register()` 是如何工作的

`tools/` 中的每个工具文件都会在模块级别调用 `registry.register()` 来声明自身。函数签名是：

````蟒蛇
注册表.注册(
    name="terminal", # 唯一的工具名称（在 API 模式中使用）
    toolset="terminal", # 该工具所属的工具集
    schema={...}, # OpenAI 函数调用架构（描述、参数）
    handler=handle_terminal, # 调用工具时执行的函数
    check_fn=check_terminal, # 可选：返回 True/False 以获得可用性
    require_env=["SOME_VAR"], # 可选：需要环境变量（用于 UI 显示）
    is_async=False, # 处理程序是否是异步协程
    description="运行命令", # 人类可读的描述
    emoji="💻", # 用于旋转/进度显示的表情符号
）
````

每次调用都会创建一个存储在单例“ToolRegistry._tools”字典中的“ToolEntry”，该字典以工具名称为键。如果工具集中发生名称冲突，则会记录警告，并且稍后的注册获胜。

### 发现：`discover_builtin_tools()`

当导入“model_tools.py”时，它会从“tools/registry.py”调用“discover_builtin_tools()”。此函数使用 AST 解析扫描每个“tools/*.py”文件，以查找包含顶级“registry.register()”调用的模块，然后导入它们：

````蟒蛇
#tools/registry.py（简化）
def discovery_builtin_tools(tools_dir=None):
    tools_path = Path(tools_dir) if tools_dir else Path(__file__).parent
    对于排序中的路径（tools_path.glob（“*.py”））：
        if {"__init__.py", "registry.py", "mcp_tool.py"} 中的路径.name：
            继续
        if _module_registers_tools(path): # AST 检查顶级registry.register()
            importlib.import_module(f"工具.{path.stem}")
````

这种自动发现意味着自动拾取新的工具文件 - 无需维护手动列表。 AST 检查仅匹配顶级 `registry.register()` 调用（不匹配函数内部的调用），因此不会导入 `tools/` 中的辅助模块。

每次导入都会触发模块的“registry.register()”调用。可选工具中的错误（例如，缺少用于图像生成的“fal_client”）会被捕获并记录 - 它们不会阻止其他工具的加载。

发现核心工具后，还发现了 MCP 工具和插件工具：

1. **MCP 工具** — `tools.mcp_tool.discover_mcp_tools()` 读取 MCP 服务器配置并从外部服务器注册工具。
2. **插件工具** — `hermes_cli.plugins.discover_plugins()` 加载可能注册其他工具的用户/项目/pip 插件。

## 工具可用性检查（`check_fn`）

每个工具都可以选择提供一个“check_fn”——当该工具可用时返回“True”的可调用函数，否则返回“False”。典型的检查包括：

- **存在 API 密钥** — 例如，用于网络搜索的 `lambda: bool(os.environ.get("SERP_API_KEY"))`
- **服务正在运行** — 例如，检查 Honcho 服务器是否已配置
- **已安装二进制文件** — 例如，验证“playwright”是否可用于浏览器工具

当“registry.get_definitions()”构建模型的架构列表时，它会运行每个工具的“check_fn()”：

````蟒蛇
# 从registry.py简化而来
如果entry.check_fn：
    尝试：
        可用 = bool(entry.check_fn())
    除了例外：
        可用 = False # 例外 = 不可用
    如果不可用：
        continue # 完全跳过这个工具
````

关键行为：
- 检查结果**每次调用都会缓存** — 如果多个工具共享相同的 `check_fn`，则它只运行一次。
- `check_fn()` 中的异常被视为“不可用”（故障安全）。
- `is_toolset_available()` 方法检查工具集的 `check_fn` 是否通过，用于 UI 显示和工具集解析。

## 工具集解析

工具集被称为工具包。 OpenClaw 通过以下方式解决这些问题：

- 显式启用/禁用工具集列表
- 平台预设（`hermes-cli`、`hermes-telegram` 等）
- 动态MCP工具集
- 精心策划的特殊用途套装，如“hermes-acp”

### `get_tool_definitions()` 如何过滤工具

主要入口点是“model_tools.get_tool_definitions（enabled_toolsets，disabled_toolsets，quiet_mode）”：

1. **如果提供了“enabled_toolsets”** — 仅包含这些工具集中的工具。每个工具集名称都通过“resolve_toolset()”解析，它将复合工具集扩展为单独的工具名称。

2. **如果提供了“disabled_toolsets”** — 从所有工具集开始，然后减去禁用的工具集。

3. **如果两者都不是** — 包括所有已知的工具集。

4. **注册表过滤** — 解析后的工具名称集被传递到 `registry.get_definitions()`，它应用 `check_fn` 过滤并返回 OpenAI 格式的模式。

5. **动态模式修补** - 过滤后，“execute_code”和“browser_navigate”模式会动态调整为仅引用实际通过过滤的工具（防止模型出现不可用工具的幻觉）。

### 旧版工具集名称

带有“_tools”后缀的旧工具集名称（例如“web_tools”、“terminal_tools”）通过“_LEGACY_TOOLSET_MAP”映射到其现代工具名称，以实现向后兼容性。

## 调度

在运行时，工具通过中央注册表进行调度，某些代理级工具（例如内存/待办事项/会话搜索处理）存在代理循环例外。

### 调度流程：模型tool_call→处理程序执行

当模型返回“tool_call”时，流程是：

````
使用 tool_call 进行模型响应
    ↓
run_agent.py 代理循环
    ↓
model_tools.handle_function_call（名称，参数，task_id，user_task）
    ↓
[代理循环工具？] → 由代理循环直接处理（todo、内存、session_search、delegate_task）
    ↓
[插件预挂钩] → invoke_hook("pre_tool_call", ...)
    ↓
注册表.dispatch（名称，args，**kwargs）
    ↓
按名称查找 ToolEntry
    ↓
[异步处理程序？] → 通过 _run_async() 桥接
[同步处理程序？] → 直接调用
    ↓
返回结果字符串（或JSON错误）
    ↓
[插件 post-hook] → invoke_hook("post_tool_call", ...)
````

### 错误包装

所有工具执行都包含在两个级别的错误处理中：

1. **`registry.dispatch()`** — 捕获处理程序中的任何异常，并以 JSON 形式返回 `{"error": "Toolexecution failed: ExceptionType: message"}`。

2. **`handle_function_call()`** — 将整个调度包装在辅助 try/ except 中，返回 `{"error": "Error waiting tool_name: message"}`。

这可确保模型始终接收格式良好的 JSON 字符串，而绝不会接收未处理的异常。

### 代理循环工具

四个工具在注册表调度之前被拦截，因为它们需要代理级状态（TodoStore、MemoryStore 等）：

- `todo` — 计划/任务跟踪
- `memory` — 持久内存写入
- `session_search` — 跨会话召回
- `delegate_task` — 产生子代理会话

这些工具的模式仍然在注册表中注册（对于“get_tool_definitions”），但如果调度以某种方式直接到达它们，它们的处理程序将返回存根错误。

### 异步桥接

当工具处理程序是异步的时，“_run_async()”将其桥接到同步调度路径：

- **CLI 路径（无运行循环）** — 使用持久事件循环来保持缓存的异步客户端处于活动状态
- **网关路径（运行循环）** — 使用 `asyncio.run()` 启动一次性线程
- **工作线程（并行工具）** — 使用存储在线程本地存储中的每线程持久循环

## DANGEROUS_PATTERNS 批准流程

终端工具集成了“tools/approval.py”中定义的危险命令批准系统：

1. **模式检测** - `DANGEROUS_PATTERNS` 是涵盖破坏性操作的 `(regex, description)` 元组列表：
   - 递归删除（`rm -rf`）
   - 文件系统格式化（`mkfs`、`dd`）
   - SQL 破坏性操作（没有“WHERE”的“DROP TABLE”、“DELETE FROM”）
   - 系统配置覆盖（`> /etc/`）
   - 服务操作（`systemctl stop`）
   - 远程代码执行（`curl | sh`）
   - Fork 炸弹、进程杀死等。

2. **检测** - 在执行任何终端命令之前，“detect_dangerous_command(command)”会检查所有模式。

3. **批准提示** — 如果找到匹配项：
   - **CLI 模式** — 交互式提示要求用户批准、拒绝或永久允许
   - **网关模式** — 异步批准回调将请求发送到消息传递平台
   - **智能批准** - 可选地，辅助LLM可以自动批准匹配模式的低风险命令（例如，`rm -rf node_modules/`是安全的，但匹配“递归删除”）

4. **会话状态** — 每个会话都会跟踪批准情况。一旦您批准会话的“递归删除”，后续的“rm -rf”命令就不会重新提示。

5. **永久允许列表** —“永久允许”选项将模式写入“config.yaml”的“command_allowlist”，在会话中持续存在。

## 终端/运行时环境

终端系统支持多种后端：

- 本地
- 码头工人
-ssh
- 奇点
- 模态
- 代托纳

它还支持：

- 每个任务的 cwd 覆盖
- 后台进程管理
- PTY模式
- 危险命令的批准回调

## 并发

工具调用可以顺序执行或同时执行，具体取决于工具组合和交互要求。

## 相关文档

- [工具集参考](../reference/toolsets-reference.md)
- [内置工具参考](../reference/tools-reference.md)
- [代理循环内部结构](./agent-loop.md)
- [ACP 内部结构](./acp-internals.md)