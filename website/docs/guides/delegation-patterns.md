---
sidebar_position: 13
title: "Delegation & Parallel Work"
description: "When and how to use subagent delegation — patterns for parallel research, code review, and multi-file work"
---
# 委派和并行工作

OpenClaw 可以生成独立的子代理来并行处理任务。每个子代理都有自己的对话、终端会话和工具集。仅返回最终摘要 - 中间工具调用永远不会进入您的上下文窗口。

有关完整功能参考，请参阅[子代理委派](/user-guide/features/delegation)。

---

## 何时委托

**代表团的好候选人：**
- 推理繁重的子任务（调试、代码审查、研究综合）
- 会用中间数据淹没您的上下文的任务
- 并行独立的工作流（同时研究A和B）
- 您希望代理无偏见地处理新环境任务

**使用其他东西：**
- 单一工具调用→直接使用该工具
- 机械多步骤工作，步骤之间具有逻辑 → `execute_code`
- 需要用户交互的任务 → 子代理不能使用 `clarify`
- 快速文件编辑 → 直接进行
- 持久的长时间运行的工作，必须比当前轮次 → `cronjob` 或 `terminal(background=True, notify_on_complete=True)` 更长久。 `delegate_task` 是**同步**：如果父进程被中断，则活动的子进程将被取消，并且他们的工作将被丢弃。

---

## 模式：并行研究

同时研究三个主题并获得结构化摘要：

````
并行研究这三个主题：
1.浏览器外WebAssembly的当前状态
2. 2025年RISC-V服务器芯片的采用
3. 量子计算实际应用

关注最新动态和关键参与者。
````

OpenClaw 在幕后使用：

````蟒蛇
delegate_task(任务=[
    {
        "goal": "2025 年在浏览器之外研究 WebAssembly",
        "context": "关注：运行时（Wasmtime、Wasmer）、云/边缘用例、WASI 进展",
        “工具集”：[“网络”]
    },
    {
        "goal": "研究 RISC-V 服务器芯片的采用",
        "context": "重点关注：服务器芯片出货、云提供商采用、软件生态系统",
        “工具集”：[“网络”]
    },
    {
        "goal": "研究实用的量子计算应用",
        "context": "关注：纠错突破、现实用例、重点公司",
        “工具集”：[“网络”]
    }
]）
````

所有三个同时运行。每个子代理独立地搜索网络并返回摘要。然后，父代理将它们合成为连贯的简报。

---

## 模式：代码审查

将安全审查委托给新上下文子代理，该子代理无需先入为主地处理代码：

````
检查 src/auth/ 中的身份验证模块是否存在安全问题。
检查 SQL 注入、JWT 验证问题、密码处理、
和会话管理。修复您发现的任何内容并运行测试。
````

关键是“context”字段——它必须包含子代理所需的所有内容：

````蟒蛇
委托任务（
    goal="检查 src/auth/ 是否存在安全问题并修复任何发现的问题",
    context="""项目位于 /home/user/webapp。Python 3.11、Flask、PyJWT、bcrypt。
    身份验证文件：src/auth/login.py、src/auth/jwt.py、src/auth/middleware.py
    测试命令：pytest测试/auth/-v
    重点关注：SQL 注入、JWT 验证、密码哈希、会话管理。
    修复发现的问题并验证测试是否通过。""",
    工具集=[“终端”，“文件”]
）
````

:::警告上下文问题
子代理对您的对话**一无所知**。他们完全重新开始。如果您委托“修复我们正在讨论的错误”，则子代理不知道您指的是什么错误。始终显式传递文件路径、错误消息、项目结构和约束。
:::

---

## 模式：比较替代方案

并行评估同一问题的多种方法，然后选择最佳方法：

````
我需要将全文搜索添加到我们的 Django 应用程序中。评估三种方法
并行：
1.PostgreSQL tsvector（内置）
2. 通过 django-elasticsearch-dsl 进行 Elasticsearch
3.Meilisearch 通过 meilisearch-python

对于每个：设置复杂性、查询能力、资源要求、
和维护费用。比较它们并推荐一个。
````

每个子代理独立研究一个选项。因为它们是孤立的，所以不存在交叉污染——每个评估都有其自身的优点。父代理获取所有三个摘要并进行比较。

---

## 模式：多文件重构

将大型重构任务拆分为多个并行子代理，每个子代理处理代码库的不同部分：

````蟒蛇
delegate_task(任务=[
    {
        "goal": "重构所有 API 端点处理程序以使用新的响应格式",
        "context": """项目位于 /home/user/api-server.
        文件：src/handlers/users.py、src/handlers/auth.py、src/handlers/billing.py
        旧格式： return {"data": result, "status": "ok"}
        新格式： return APIResponse(data=result, status=200).to_dict()
        导入：从 src.responses 导入 APIResponse
        之后运行测试： pytest测试/处理程序/ -v""",
        “工具集”：[“终端”，“文件”]
    },
    {
        "goal": "更新所有客户端 SDK 方法以处理新的响应格式",
        "context": """项目位于 /home/user/api-server.
        文件：sdk/python/client.py、sdk/python/models.py
        旧解析：result = response.json()["data"]
        新解析：result = response.json()["data"]（相同的键，但添加状态码检查）
        同时更新 sdk/python/tests/test_client.py""",
        “工具集”：[“终端”，“文件”]
    },
    {
        "goal": "更新 API 文档以反映新的响应格式",
        "context": """项目位于 /home/user/api-server.
        文档位于：docs/api/。格式：带有代码示例的 Markdown。
        将所有响应示例从旧格式更新为新格式。
        将“响应格式”部分添加到 docs/api/overview.md 解释架构。""",
        “工具集”：[“终端”，“文件”]
    }
]）
````

:::提示
每个子代理都有自己的终端会话。他们可以在同一个项目目录上工作，而无需互相干扰 - 只要他们编辑不同的文件即可。如果两个子代理可能接触同一个文件，请在并行工作完成后自行处理该文件。
:::

---

## 模式：收集然后分析

使用“execute_code”进行机械数据收集，然后委托进行大量推理分析：

````蟒蛇
# 第 1 步：机械收集（这里的execute_code 更好——无需推理）
执行代码("""
从 Hermes_tools 导入 web_search, web_extract

结果=[]
在[“2026年第一季度人工智能融资”、“2026年人工智能初创公司收购”、“2026年人工智能IPO”]中查询：
    r = web_search(查询, 限制=5)
    对于 r["data"]["web"] 中的项目：
        results.append({"title": item["title"], "url": item["url"], "desc": item["description"]})

# 从最相关的前 5 个中提取完整内容
urls = [r["url"] for r in results[:5]]
内容 = web_extract(url)

# 保存用于分析步骤
导入 json
将 open("/tmp/ai-funding-data.json", "w") 作为 f：
    json.dump({"search_results": 结果, "extracted": content["results"]}, f)
print(f"收集了 {len(results)} 个结果，提取了 {len(content['results'])} 页")
“””）

# 步骤 2：大量推理分析（这里委托更好）
委托任务（
    goal="分析人工智能融资数据并撰写市场报告",
    context="""/tmp/ai-funding-data.json 中的原始数据包含搜索结果和
    提取了有关 2026 年第一季度人工智能融资、收购和 IPO 的网页。
    撰写结构化市场报告：关键交易、趋势、著名参与者、
    和展望。专注于超过 1 亿美元的交易。""",
    工具集=[“终端”，“文件”]
）
````

这通常是最有效的模式：“execute_code”以低廉的成本处理 10 多个连续工具调用，然后子代理使用干净的上下文执行单个昂贵的推理任务。

---

## 工具集选择

根据子代理的需求选择工具集：

|任务类型|工具集 |为什么 |
|------------|----------|-----|
|网络研究| `[“网络”]` |仅限 web_search + web_extract |
|代码工作 | `[“终端”，“文件”]` | Shell访问+文件操作 |
|全栈 | `[“终端”、“文件”、“网络”]` |除了消息之外的一切 |
|只读分析| `[“文件”]` |只能读文件，没有shell |

限制工具集可以使子代理保持专注并防止意外的副作用（例如研究子代理运行 shell 命令）。

---

## 约束条件

- **默认 3 个并行任务**：批次默认为 3 个并发子代理（可通过 config.yaml 中的 `delegation.max_concurrent_children` 配置，没有硬性上限，只有 1 层）
- **嵌套委托是可选的**：叶子代理（默认）无法调用 `delegate_task`、`clarify`、`memory`、`send_message` 或 `execute_code`。 Orchestrator 子代理 (`role="orchestrator"`) 保留 `delegate_task` 以进行进一步委派，但仅当 `delegation.max_spawn_depth` 提高到默认值 1 以上时（第 1 层，无上限）；其他四个仍然被封锁。通过“delegation.orchestrator_enabled: false”全局禁用。

### 调整并发和深度

|配置 |默认 |范围 |效果|
|--------|---------|--------|--------|
| `max_concurrent_children` | 3 | >=1 |每个“delegate_task”调用的并行批量大小
| `最大生成深度` | 1 | >=1 |可以进一步产生多少个授权级别 |

示例：运行 30 个带有嵌套子代理的并行工作进程：

````yaml
代表团：
  最大并发子数：30
  最大生成深度：2
````

- **单独的终端** — 每个子代理都有自己的终端会话，具有单独的工作目录和状态
- **没有对话历史记录** - 子代理只能看到父代理在调用“delegate_task”时传递的“目标”和“上下文”
- **默认 50 次迭代** — 对于简单任务设置较低的“max_iterations”以节省成本
- **不持久** - `delegate_task` 是同步的，并且在父回合内运行。如果父进程被中断（新用户消息、`/stop`、`/new`），则所有活动的子进程将被取消（`status="interrupted"`），并且它们的工作将被丢弃。对于必须在当前回合结束后继续存在的工作，请使用 `cronjob` 或 `terminal(background=True, notify_on_complete=True)`。

---

## 提示

**目标要具体。**“修复错误”太模糊了。 “修复 api/handlers.py 第 47 行中的 TypeError，其中 process_request() 从 parse_body() 接收不到任何内容”为子代理提供了足够的工作空间。

**包括文件路径。** 子代理不知道您的项目结构。始终包含相关文件、项目根目录和测试命令的绝对路径。

**使用委托进行上下文隔离。**有时您需要一个全新的视角。委派迫使您清楚地阐明问题，而子代理则在不考虑您谈话中建立的假设的情况下处理问题。

**检查结果。** 子代理摘要就是摘要。如果子代理说“修复了错误并且测试通过”，请通过自己运行测试或阅读差异进行验证。

---

*有关完整的委派参考 — 所有参数、ACP 集成和高级配置 — 请参阅 [子代理委派](/user-guide/features/delegation)。*