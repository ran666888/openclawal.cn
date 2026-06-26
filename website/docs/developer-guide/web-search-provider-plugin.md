---
sidebar_position: 12
title: "Web Search Provider Plugins"
description: "如何为 OpenClaw 构建网页搜索/提取/爬取后端插件"
---
# 构建 Web 搜索提供程序插件

网络搜索提供商插件注册一个为“web_search”、“web_extract”和（可选）深度爬网工具调用提供服务的后端。内置提供程序 — Firecrawl、SearXNG、Tavily、Exa、Parallel、Brave Search（免费套餐）、xAI 和 DDGS — 全部作为插件发布在 `plugins/web/<name>/` 下。您可以通过在它们旁边放置一个目录来添加新的目录或覆盖捆绑的目录。

:::提示
网络搜索是 OpenClaw 支持的几个 **后端插件** 之一。其他（有自己的 ABC）是 [图像生成提供程序插件](/developer-guide/image-gen-provider-plugin)、[视频生成提供程序插件](/developer-guide/video-gen-provider-plugin)、[内存提供程序插件](/developer-guide/memory-provider-plugin)、[上下文引擎插件](/developer-guide/context-engine-plugin) 和 [模型提供程序]插件](/开发人员指南/模型提供者插件)。通用工具/hook/CLI 插件位于 [构建 OpenClaw 插件](/guides/build-a-hermes-plugin)。
:::

## 发现如何运作

OpenClaw 在三个地方扫描网络搜索后端：

1. **捆绑** — `<repo>/plugins/web/<name>/` （自动加载 `kind: backend`，始终可用）
2. **用户** — `~/.hermes/plugins/web/<name>/` （通过 `plugins.enabled` 或 `hermes plugins enable <name>` 选择加入）
3. **Pip** — 声明 `hermes_agent.plugins` 入口点的包

每个插件的“register(ctx)”函数都会调用“ctx.register_web_search_provider(...)”——将实例放入“agent/web_search_registry.py”中的注册表中。每个功能的活动提供者由配置选择：

|能力|配置键|跌回 |
|---|---|---|
| `网络搜索` | `web.search_backend` | `web.backend` |
| `web_extract` | `web.extract_backend` | `web.backend` |
| `web_extract` 内的深度抓取模式 | `web.extract_backend` | `web.backend` |

当两个密钥均未设置时，OpenClaw 会自动检测环境中存在的任何 API 密钥/URL 的后端。 “hermes 工具”引导用户进行选择。

## 目录结构

````
插件/网络/我的后端/
├── __init__.py # register() 入口点
├──provider.py # WebSearchProvider 子类
└──plugin.yaml # 清单类型：后端和providers_web_providers
````

`brave_free/` 和 `ddgs/` 是最小的树内引用 - `brave_free` 用于 API 密钥门控的仅搜索提供商，`ddgs` 用于延迟安装其 SDK 的无密钥提供商。

## WebSearchProvider ABC

子类“agent.web_search_provider.WebSearchProvider”。唯一必需的成员是“name”、“is_available()”以及您实现的“search()”/“extract()”中的任何一个。 （深度爬取不是一种单独的方法——它是“extract()”的一种模式。）

````蟒蛇
# 插件/web/my-backend/provider.py
from __future__ 导入注释

导入操作系统
从输入导入 Any、Dict、List

从 agent.web_search_provider 导入 WebSearchProvider


类 MyBackendWebSearchProvider(WebSearchProvider):
    """针对我的后端 HTTP API 的最小仅搜索提供程序。"""

    @属性
    def 名称(自身) -> str:
        # web.search_backend / web.extract_backend / web.backend 中使用的稳定 id
        # 配置键。小写，无空格；允许使用连字符。
        返回“我的后端”

    @属性
    def display_name(self) -> str：
        # `hermes tools` 中显示的人类标签。默认为“名称”。
        返回“我的后端”

    def is_available(self) -> bool:
        # 便宜的检查 - env var 存在，可选的 dep 可导入等。
        # 不得进行网络调用（在每个“hermes tools”油漆上运行）。
        return bool(os.getenv("MY_BACKEND_API_KEY", "").strip())

    def support_search(self) -> bool:
        返回真

    def support_extract(self) -> bool:
        返回错误

    def search(self, 查询: str, 限制: int = 5) -> Dict[str, Any]:
        导入httpx

        api_key = os.environ["MY_BACKEND_API_KEY"]
        尝试：
            响应 = httpx.get(
                “https://api.example.com/search”，
                params={"q": 查询, "count": max(1, min(int(limit), 20))},
                headers={"授权": f"承载 {api_key}"},
                超时=15，
            ）
            resp.raise_for_status()
            数据 = resp.json()
        除了 httpx.HTTPError 之外：
            return {"成功": False, "错误": str(exc)}

        # 响应形状是固定的 - 请参阅下面的“响应形状”。
        返回{
            “成功”：确实，
            “数据”：{
                “网络”：[
                    {
                        "标题": item.get("标题", ""),
                        "url": item.get("url", ""),
                        "描述": item.get("片段", ""),
                        “位置”：idx + 1，
                    }
                    对于 idx，enumerate(data.get("results", [])) 中的项目
                ],
            },
        }
````

````蟒蛇
# 插件/web/my-backend/__init__.py
从plugins.web.my_backend.provider导入MyBackendWebSearchProvider


def 寄存器(ctx) -> 无:
    """插件入口点 - 在加载时调用一次。"""
    ctx.register_web_search_provider(MyBackendWebSearchProvider())
````

## 插件.yaml

````yaml
名称：网络我的后端
版本：1.0.0
描述：“我的后端网络搜索 — Bearer-auth REST API”
作者：你的名字
种类：后端
提供网络提供商：
  - 我的后端
需要环境：
  - MY_BACKEND_API_KEY
````

|关键|目的|
|---|---|
| `种类：后端` |通过后端加载路径路由插件 |
| `provides_web_providers` |该插件注册的提供者“名称”列表 - 甚至在“register()”运行之前，加载程序也会使用该列表在“hermes tools”中宣传该插件 |
| `require_env` | `hermes 插件安装`期间的交互式凭据提示（有关丰富格式，请参阅[构建 OpenClaw 插件](/guides/build-a-hermes-plugin#gate-on-environment-variables)） |

## ABC 参考

完整合同位于“agent/web_search_provider.py”中。您可以重写的方法：

|会员|必填|默认 |目的|
|---|---|---|---|
| `名称` | ✅ | — | `web.*_backend` 配置中使用的稳定 ID |
| `显示名称` | — | `名称` | “hermes 工具”中显示的标签 |
| `is_available()` | ✅ | — |廉价的可用性门 - 环境变量，可选的依赖项 |
| `supports_search()` | — | '真实' | `web_search` 路由的功能标志 |
| `supports_extract()` | — | ‘假’| `web_extract` 路由的功能标志 |
| `搜索（查询，限制）` |有条件|提高 |当 `supports_search()` 返回 `True` 时必需 |
| `提取（url，**kwargs）` |有条件|提高 |当 `supports_extract()` 返回 `True` 时需要 |

提供者可以宣传单个类的多种功能——Firecrawl、Tavily、Exa 和 Parallel 都实现了搜索和提取。 Brave Search 和 DDGS 仅限搜索； SearXNG 仅限搜索，具有记录的“将我与提取提供者配对”工作流程。

## 响应形状

工具包装器需要一个固定的信封，因此它不必在后端之间进行转换。

**搜索成功：**

````蟒蛇
{
    “成功”：确实，
    “数据”：{
        “网络”：[
            {“标题”：str，“url”：str，“描述”：str，“位置”：int}，
            ...
        ],
    },
}
````

**提取成功：**

````蟒蛇
{
    “成功”：确实，
    “数据”：[
        {
            “网址”：字符串，
            “标题”：str，
            “内容”：str，
            “原始内容”：str，
            "metadata": dict, # 可选
            "error": str, # 可选，仅在每个 URL 失败时
        },
        ...
    ],
}
````

**任一功能，失败时：**

````蟒蛇
{“成功”：错误，“错误”：“人类可读的消息”}
````

“search()”和“extract()”都可以是“async def”——调度程序通过“inspect.iscoroutinefunction”检测协程函数并相应地等待。阻塞 I/O（HTTP、SDK 调用）的同步实现非常适合小型后端；调度程序处理线程。

## 能力标志

OpenClaw 根据“supports_*”标志将呼叫路由到正确的提供商。常见的多提供商设置：

````yaml
# ~/.hermes/config.yaml
网址：
  search_backend: "brave-free" # 仅搜索，快速，免费 2k/月
  extract_backend: "firecrawl" # 提取+抓取，付费配额
````

当未设置“web.search_backend”或“web.extract_backend”时，两者都会落入“web.backend”。当它也未设置时，OpenClaw 根据 env-var 的存在情况选择第一个支持所请求功能的可用提供程序。

如果您的提供商仅支持一种功能，请将其他标志保留为默认值（“False”），注册表将为该工具跳过它 - 当用户仅使用 X 进行搜索并要求代理提取时，用户不会看到误导性的“提供商 X 失败”错误。

## OpenClaw 如何将其连接到工具中

“web_search”和“web_extract”工具位于“tools/web_tools.py”中。在通话时他们：

1. 读取相关配置键（`web.search_backend` 对应 `web_search`，`web.extract_backend` 对应 `web_extract`）
2. 向注册机构询问具有该“名称”的提供商
3. 检查 `is_available()` 和匹配的 `supports_*()` 标志
4. 分派到 `search()` / `extract()` （深度爬行作为 `extract()` 内部的模式运行），等待该方法是否是协程
5. JSON序列化响应信封并将其交还给LLM

工具结果会出现错误；法学硕士决定如何解释它们。如果没有注册提供者（或者每个可用的提供者都未能通过功能门），该工具会返回一个有用的错误，指向“hermes tools”。

## 延迟安装可选依赖项

如果您的提供商包装了第三方 SDK（如 DDGS 对“ddgs”包所做的那样），请不要在模块顶层“导入”它。在 `is_available()` 或 `search()` 中使用 `tools.lazy_deps.ensure(...)` — OpenClaw 将在第一次使用时安装该软件包，由 `security.allow_lazy_installs` 控制。有关安全模型，请参阅[构建 OpenClaw 插件 → Lazy-install](/guides/build-a-hermes-plugin#lazy-install-optional-python-dependencies)。

## 参考实现

- **`plugins/web/brave_free/`** — 小型、API 密钥门控、仅限搜索的 HTTP 提供商。很好的起始模板。
- **`plugins/web/ddgs/`** — 延迟安装其 SDK 的无密钥提供商。对于包装 Python 包的后端来说非常有用的模式。
- **`plugins/web/firecrawl/`** — 具有多种格式模式的完整多功能提供程序（搜索+提取+抓取）。
- **`plugins/web/searxng/`** — 自托管、URL 配置后端，无需身份验证。
- **`plugins/web/xai/`** — 通过 Grok 的服务器端 `web_search` 工具进行 LLM 支持的搜索。展示如何在不添加新环境变量的情况下重用现有的 OAuth/env-var 凭证表面 (`tools/xai_http.py`)，以及如何编写一个廉价的 `is_available()` 来遵守无网络合约。

## 通过 pip 分发

````汤姆
# pyproject.toml
[project.entry-points."hermes_agent.plugins"]
my-backend-web =“my_backend_web_package”
````

`my_backend_web_package` 必须公开顶级 `register` 函数。有关完整设置，请参阅常规插件指南中的[通过 pip 分发](/guides/build-a-hermes-plugin#distribute-via-pip)。

## 相关页面

- [Web 搜索](/user-guide/features/web-search) — 面向用户的功能文档和每个后端配置
- [插件概述](/user-guide/features/plugins) — 所有插件类型一目了然
- [构建 OpenClaw 插件](/guides/build-a-hermes-plugin) — 通用工具/hooks/slash 命令指南