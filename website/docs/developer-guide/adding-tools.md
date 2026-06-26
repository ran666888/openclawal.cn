---
sidebar_position: 2
title: "Adding Tools"
description: "How to add a new tool to OpenClaw — schemas, handlers, registration, and toolsets"
---
# 添加工具

在编写工具之前，问问自己：**这应该是[技能](creating-skills.md)吗？**

:::警告仅限内置核心工具
此页面用于将 **内置 OpenClaw 工具** 添加到存储库本身。
如果您想要一个个人的、项目本地的或其他自定义工具，而不需要
修改 OpenClaw 核心，改用插件路由：

- [插件](/用户指南/功能/插件)
- [构建 OpenClaw 插件](/guides/build-a-hermes-plugin)

大多数自定义工具创建的默认插件。仅在以下情况下关注此页面
您明确希望在“tools/”和“toolsets.py”中发布一个新的内置工具。
:::

当功能可以表达为指令 + shell 命令 + 现有工具（arXiv 搜索、git 工作流程、Docker 管理、PDF 处理）时，使其成为 **技能**。

当需要与 API 密钥、自定义处理逻辑、二进制数据处理或流媒体（浏览器自动化、TTS、视觉分析）进行端到端集成时，使其成为**工具**。

## 概述

添加工具涉及 **2 个文件**：

1. **`tools/your_tool.py`** — 处理程序、模式、检查函数、`registry.register()` 调用
2. **`toolsets.py`** — 将工具名称添加到`_HERMES_CORE_TOOLS`（或特定工具集）

任何具有顶级 `registry.register()` 调用的 `tools/*.py` 文件都会在启动时自动发现 - 无需手动导入列表。

## 步骤1：创建内置工具文件

每个工具文件都遵循相同的结构：

````蟒蛇
# 工具/weather_tool.py
"""天气工具 -- 查找某个位置的当前天气。"""

导入 json
导入操作系统
导入日志记录

记录器=logging.getLogger(__name__)


# --- 可用性检查 ---

def check_weather_requirements() -> bool:
    """如果工具的依赖项可用，则返回 True。"""
    返回 bool(os.getenv("WEATHER_API_KEY"))


# --- 处理程序 ---

def Weather_tool(位置: str, 单位: str = "公制") -> str:
    """获取某个位置的天气。返回 JSON 字符串。"""
    api_key = os.getenv("WEATHER_API_KEY")
    如果不是 api_key:
        return json.dumps({"error": "WEATHER_API_KEY 未配置"})
    尝试：
        # ...调用天气API ...
        return json.dumps({"location": 位置, "temp": 22, "units": 单位})
    除了异常 e：
        返回 json.dumps({"error": str(e)})


# --- 架构 ---

天气模式 = {
    “名称”：“天气”，
    "description": "获取某个位置的当前天气。",
    “参数”：{
        “类型”：“对象”，
        “属性”：{
            “位置”：{
                “类型”：“字符串”，
                "description": "城市名称或坐标（例如'伦敦'或'51.5,-0.1'）"
            },
            “单位”：{
                “类型”：“字符串”，
                “枚举”：[“公制”，“英制”]，
                "description": "温度单位（默认：公制）",
                “默认”：“公制”
            }
        },
        “必需”：[“位置”]
    }
}


# --- 注册 ---

从tools.registry导入注册表

注册表.注册(
    名称=“天气”，
    工具集=“天气”，
    架构=WEATHER_SCHEMA，
    处理程序=lambda args，**kw：weather_tool（
        location=args.get("位置", ""),
        单位=args.get(“单位”,“公制”)),
    check_fn=检查天气要求，
    require_env=["WEATHER_API_KEY"],
）
````

### 关键规则

:::危险 重要
- 处理程序**必须**返回一个 JSON 字符串（通过 `json.dumps()`），而不是原始字典
- 错误**必须**作为`{"error": "message"}`返回，永远不要作为异常引发
- 构建工具定义时调用 `check_fn` — 如果它返回 `False`，则该工具将被静默排除
- `handler` 接收 `(args: dict, **kwargs)`，其中 `args` 是 LLM 的工具调用参数
:::

## 步骤 2：将内置工具添加到工具集中

在“toolsets.py”中，添加工具名称：

````蟒蛇
# 如果它应该在所有平台上可用（CLI + 消息传递）：
_HERMES_CORE_TOOLS = [
    ...
    "天气", # <-- 在此处添加
]

# 或者创建一个新的独立工具集：
“天气”：{
    "description": "天气查询工具",
    “工具”：[“天气”]，
    “包括”：[]
},
````

## ~~步骤3：添加发现导入~~（不再需要）

具有顶级 `registry.register()` 调用的工具模块由 `tools/registry.py` 中的 `discover_builtin_tools()` 自动发现。无需维护手动导入列表 - 只需在“tools/”中创建文件，它就会在启动时拾取。

## 异步处理程序

如果您的处理程序需要异步代码，请使用“is_async=True”进行标记：

````蟒蛇
async def Weather_tool_async(location: str) -> str:
    与 aiohttp.ClientSession() 异步作为会话：
        ...
    返回 json.dumps(结果)

注册表.注册(
    名称=“天气”，
    工具集=“天气”，
    架构=WEATHER_SCHEMA，
    处理程序=lambda args，** kw：weather_tool_async（args.get（“位置”，“”）），
    check_fn=检查天气要求，
    is_async=True, # 注册表自动调用_run_async()
）
````

注册表透明地处理异步桥接 - 您永远不会自己调用“asyncio.run()”。

## 需要task_id 的处理程序

管理每个会话状态的工具通过“**kwargs”接收“task_id”：

````蟒蛇
def _handle_weather(args, **kw):
    任务id = kw.get("任务id")
    返回weather_tool(args.get("位置",""),task_id=task_id)

注册表.注册(
    名称=“天气”，
    ...
    处理程序=_handle_weather，
）
````

## Agent-Loop 拦截工具

某些工具（“todo”、“memory”、“session_search”、“delegate_task”）需要访问每个会话代理状态。这些在到达注册表之前被“run_agent.py”拦截。注册表仍然保留它们的模式，但是如果拦截被绕过，“dispatch()”会返回一个后备错误。

## 可选：设置向导集成

如果您的工具需要 API 密钥，请将其添加到 `hermes_cli/config.py`：

````蟒蛇
可选_ENV_VARS = {
    ...
    “WEATHER_API_KEY”：{
        "description": "用于天气查询的天气 API 密钥",
        "prompt": "天气 API 密钥",
        "url": "https://weatherapi.com/",
        “工具”：[“天气”]，
        “密码”：正确，
    },
}
````

## 清单

- [ ] 使用处理程序、模式、检查函数和注册创建的工具文件
- [ ] 添加到 `toolsets.py` 中适当的工具集中
- [ ] 确认这确实应该是一个内置/核心工具而不是插件
- [ ] 处理程序返回 JSON 字符串，错误返回为 `{"error": "..."}`
- [ ] 可选：API 密钥添加到 `hermes_cli/config.py` 中的 `OPTIONAL_ENV_VARS`
- [ ] 可选：添加到“toolset_distributions.py”以进行批处理
- [ ] 使用“hermes chat -q“使用伦敦天气工具”进行测试