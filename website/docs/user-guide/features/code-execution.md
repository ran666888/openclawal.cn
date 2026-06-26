---
sidebar_position: 8
title: "Code Execution"
description: "Programmatic Python execution with RPC tool access — collapse multi-step workflows into a single turn"
---
# 代码执行（编程工具调用）

“execute_code”工具允许代理编写Python脚本，以编程方式调用OpenClaw工具，将多步骤工作流程压缩为单个LLM回合。该脚本在代理主机上的子进程中运行，通过 Unix 域套接字 RPC 与 OpenClaw 进行通信。

## 它是如何工作的

1.代理使用“from hermes_tools import ...”编写Python脚本
2. OpenClaw生成带有RPC函数的`hermes_tools.py`存根模块
3、OpenClaw打开一个Unix域套接字并启动一个RPC监听线程
4. 脚本在子进程中运行——工具调用通过套接字传回 OpenClaw
5. 仅脚本的`print()`输出返回给LLM；中间工具结果永远不会进入上下文窗口

````蟒蛇
# 代理可以编写如下脚本：
从 Hermes_tools 导入 web_search, web_extract

results = web_search("Python 3.13 功能", limit=5)
对于结果 ["data"]["web"] 中的 r：
    内容 = web_extract([r["url"]])
    # ...过滤和处理...
打印（摘要）
````

**脚本内的可用工具：** `web_search`、`web_extract`、`read_file`、`write_file`、`search_files`、`patch`、`terminal`（仅限前台）。

## 当代理使用这个时

当存在以下情况时，代理使用“execute_code”：

- **3+ 工具调用** 以及它们之间的处理逻辑
- 批量数据过滤或条件分支
- 循环结果

主要好处：中间工具结果永远不会进入上下文窗口 - 只有最终的“print()”输出返回，从而大大减少了令牌的使用。

## 实际例子

### 数据处理管道

````蟒蛇
从 Hermes_tools 导入 search_files, read_file
导入 json

# 查找所有配置文件并提取数据库设置
matches = search_files("database", path=".", file_glob="*.yaml", limit=20)
配置=[]
对于 matches.get("matches", []) 中的匹配：
    内容 = read_file(匹配[“路径”])
    configs.append({"文件": 匹配["路径"], "预览": 内容["内容"][:200]})

打印（json.dumps（配置，缩进= 2））
````

### 多步骤网络研究

````蟒蛇
从 Hermes_tools 导入 web_search, web_extract
导入 json

# 搜索、提取、总结一次完成
results = web_search("Rust 异步运行时比较 2025", limit=5)
摘要 = []
对于结果 ["data"]["web"] 中的 r：
    页面 = web_extract([r["url"]])
    for p in page.get("results", []):
        if p.get("内容"):
            摘要.append({
                “标题”：r[“标题”]，
                “网址”：r[“网址”]，
                “摘录”：p[“内容”][：500]
            })

打印（json.dumps（摘要，缩进= 2））
````

### 批量文件重构

````蟒蛇
从 Hermes_tools 导入 search_files、read_file、补丁

# 查找所有使用已弃用的 API 的 Python 文件并修复它们
匹配= search_files（“old_api_call”，path =“src /”，file_glob =“*.py”）
固定 = 0
对于 matches.get("matches", []) 中的匹配：
    结果=补丁（
        路径=匹配[“路径”]，
        old_string =“old_api_call（”，
        new_string =“new_api_call（”，
        替换全部=真
    ）
    如果“错误”不在 str(结果) 中：
        固定 += 1

print(f"修复了 {len(matches.get('matches', []))} 个匹配项中的 {fixed} 个文件")
````

### 构建和测试管道

````蟒蛇
从 Hermes_tools 导入终端，read_file
导入 json

# 运行测试、解析结果并报告
结果 = 终端（“cd /project && python -m pytest --tb=short -q 2>&1”，超时=120）
输出 = result.get("输出", "")

# 解析测试输出
通过 = output.count(" 通过")
失败=output.count("失败")
错误=输出.count(“错误”)

报告={
    “通过”：通过，
    “失败”：失败，
    “错误”：错误，
    "退出代码": result.get("退出代码", -1),
    "summary": 输出[-500:] 如果 len(输出) > 500 否则输出
}

打印（json.dumps（报告，缩进= 2））
````

## 执行模式

`execute_code` 有两种执行模式，由 `~/.hermes/config.yaml` 中的 `code_execution.mode` 控制：

|模式|工作目录 | Python 解释器 |
|------|--------------------|--------------------|
| **`项目`**（默认）|会话的工作目录（与 `terminal()` 相同）|活跃的 `VIRTUAL_ENV` / `CONDA_PREFIX` python，回落到 OpenClaw 自己的 python |
| `严格` |与用户项目隔离的临时暂存目录 | `sys.executable` (OpenClaw 自己的 python) |

**何时将其保留在 `project` 上：** 您希望 `import pandas`、`from my_project import foo` 或像 `open(".env")` 这样的相对路径以与在 `terminal()` 中相同的方式工作。这几乎总是您想要的。

**何时切换到“严格”：**您需要最大的可重复性 - 无论用户激活哪个 venv，您都希望每个会话使用相同的解释器，并且您希望脚本从项目树中隔离（没有通过相对路径意外读取项目文件的风险）。

````yaml
# ~/.hermes/config.yaml
代码执行：
  模式：项目#或“严格”
````

“project”模式下的回退行为：如果“VIRTUAL_ENV”/“CONDA_PREFIX”未设置、损坏或指向早于 3.8 的 Python，解析器会干净地回退到“sys.executable”——它永远不会在没有工作解释器的情况下让代理离开。

两种模式下的安全关键不变量是相同的：

- 环境清理（API 密钥、令牌、凭证被剥离）
- 工具白名单（脚本不能递归调用 `execute_code`、`delegate_task` 或 MCP 工具）
- 资源限制（超时、标准输出上限、工具调用上限）

切换模式会改变脚本运行的位置以及运行它们的解释器，而不是它们可以看到哪些凭据或可以调用哪些工具。

## 资源限制

|资源 |限制|笔记|
|----------|--------|--------|
| **超时** | 5 分钟（300 秒）|使用 SIGTERM 终止脚本，然后在 5 秒宽限后使用 SIGKILL |
| **标准输出** | 50 KB |输出被截断，并带有“[输出被截断为 50KB]”通知 |
| **标准错误** | 10 KB |包含在非零退出的输出中以进行调试 |
| **工具调用** |每次执行 50 |达到限制时返回错误 |

所有限制都可以通过“config.yaml”进行配置：

````yaml
# 在 ~/.hermes/config.yaml 中
代码执行：
  模式：项目#项目（默认）|严格
  timeout: 300 # 每个脚本的最大秒数（默认值：300）
  max_tool_calls: 50 # 每次执行的最大工具调用数（默认值：50）
````

## 工具调用如何在脚本内工作

当您的脚本调用像“web_search("query")”这样的函数时：

1. 调用被序列化为 JSON 并通过 Unix 域套接字发送到父进程
2. 父进程通过标准 `handle_function_call` 处理程序进行调度
3.结果通过socket发回
4.函数返回解析结果

这意味着脚本内的工具调用与普通工具调用的行为相同——相同的速率限制、相同的错误处理、相同的功能。唯一的限制是 `terminal()` 只能在前台使用（没有 `background` 或 `pty` 参数）。

## 错误处理

当脚本失败时，代理会收到结构化错误信息：

- **非零退出代码**：stderr 包含在输出中，以便代理看到完整的回溯
- **超时**：脚本被终止，代理看到“脚本在 300 秒后超时并被终止。”
- **中断**：如果用户在执行期间发送新消息，脚本将终止并且代理会看到“[执行中断 - 用户发送了新消息]”
- **工具调用限制**：当达到 50 次调用限制时，后续工具调用将返回错误消息

响应始终包含“status”（成功/错误/超时/中断）、“output”、“tool_calls_made”和“duration_seconds”。

## 安全

:::危险安全模型
子进程在**最小环境**中运行。默认情况下会删除 API 密钥、令牌和凭据。该脚本仅通过 RPC 通道访问工具 - 除非明确允许，否则它无法从环境变量中读取机密。
:::

名称中包含“KEY”、“TOKEN”、“SECRET”、“PASSWORD”、“CREDENTIAL”、“PASSWD”或“AUTH”的环境变量被排除。仅传递安全的系统变量（`PATH`、`HOME`、`LANG`、`SHELL`、`PYTHONPATH`、`VIRTUAL_ENV` 等）。

###技能环境变量直通

当技能在其 frontmatter 中声明“required_environment_variables”时，加载该技能后，这些变量将**自动传递**到“execute_code”和“terminal”子进程。这使得技能可以使用其声明的 API 密钥，而不会削弱任意代码的安全态势。

对于非技能用例，您可以在“config.yaml”中显式允许变量：

````yaml
终端：
  env_passthrough：
    - 我的自定义密钥
    - ANOTHER_TOKEN
````

有关完整详细信息，请参阅[安全指南](/user-guide/security#environment-variable-passthrough)。

### 子级中的 `HERMES_*` 变量

子进程仅接收一小部分固定的操作“HERMES_*”
按确切名称的变量：

- `HERMES_HOME`
- `HERMES_个人资料`
- `HERMES_CONFIG`
- `HERMES_ENV`

（加上 `HERMES_RPC_DIR` / `HERMES_RPC_SOCKET` / `TZ` / `HOME`，即 OpenClaw
显式注入以便 RPC 通道工作）。

:::note 行为改变
早期版本传递了名称以“HERMES_”开头的**任何**变量
到孩子身上。为了加强安全性，删除了这个广泛的前缀：it
可能会泄漏与秘密子字符串不匹配的“HERMES_*”命名配置
（例如“HERMES_BASE_URL”、“HERMES_KANBAN_DB”或“HERMES_*_WEBHOOK”
端点）到任意沙盒代码中。

如果它在导入时导入“execute_code”脚本或存储库/插件模块
— 依赖于上述四个操作名称之外的“HERMES_*”变量，它
现在会发现子变量中**未设置**。掉落是故意的
不是一个错误。
:::

**解决方法 - 显式选择变量。** 两条路由都通过
通过“execute_code”*和*“terminal”子级变量，并且两者都不会减弱
秘密剥离保证（OpenClaw 管理的提供商凭证永远不能
以这种方式重新允许）：

1. **每台机器，在 `config.yaml`** — 将准确的变量名称添加到
   直通许可名单：

   ````yaml
   终端：
     env_passthrough：
       - HERMES_看板_DB
       - HERMES_BASE_URL
   ````

2. **每项技能，在技能的 frontmatter 中** — 声明它以便注册
   每当加载该技能时自动：

   ````yaml
   必需的环境变量：
     - HERMES_看板_DB
   ````

**诊断它。** 当孩子掉落一个或多个非允许的“HERMES_*”时
变量，OpenClaw 会发出一行“debug”日志，对它们进行命名并指向
`env_passthrough` 逃生舱口。使用调试日志记录运行（`hermes logs --level
DEBUG`，或检查`~/.hermes/logs/agent.log`）并查找
`execute_code：如果脚本行为，则删除 N 个非允许的 HERMES_* var(s)`
就像缺少“HERMES_*”变量一样。

OpenClaw 始终将脚本和自动生成的“hermes_tools.py”RPC 存根写入临时暂存目录，该目录在执行后会被清理。在“严格”模式下，脚本也在那里“运行”；在“project”模式下，它在会话的工作目录中运行（临时目录保留在“PYTHONPATH”上，因此导入仍然可以解析）。子进程在自己的进程组中运行，因此可以在超时或中断时被彻底杀死。

## 执行代码与终端

|使用案例|执行代码|终端|
|----------|-------------|----------|
| | 之间具有工具调用的多步骤工作流程 | ✅ | ❌ |
|简单的 shell 命令 | ❌ | ✅ |
|过滤/处理大型工具输出 | ✅ | ❌ |
|运行构建或测试套件 | ❌ | ✅ |
|循环搜索结果 | ✅ | ❌ |
|交互式/后台进程| ❌ | ✅ |
|环境中需要 API 密钥 | ⚠️ 仅通过 [passthrough](/user-guide/security#environment-variable-passthrough) | ✅（大部分通过）|

**经验法则：** 当您需要通过调用之间的逻辑以编程方式调用 OpenClaw 工具时，请使用“execute_code”。使用“终端”运行 shell 命令、构建和进程。

## 平台支持

代码执行需要 Unix 域套接字，并且仅在 **Linux 和 macOS 上可用**。它在 Windows 上自动禁用 - 代理会退回到常规顺序工具调用。