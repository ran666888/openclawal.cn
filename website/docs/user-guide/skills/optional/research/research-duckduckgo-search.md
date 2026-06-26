---
title: "Duckduckgo Search — Free web search via DuckDuckGo — text, news, images, videos"
sidebar_label: "Duckduckgo Search"
description: "Free web search via DuckDuckGo — text, news, images, videos"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# DuckDuckGo 搜索

通过 DuckDuckGo 免费网络搜索 — 文本、新闻、图片、视频。无需 API 密钥。安装时首选 `ddgs` CLI；仅在验证“ddgs”在当前运行时可用后才使用 Python DDGS 库。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/duckduckgo-search` 安装 |
|路径| `可选技能/研究/duckduckgo-搜索` |
|版本 | `1.3.0` |
|作者 | gamedev阴天 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `搜索`、`duckduckgo`、`网络搜索`、`免费`、`后备` |
|相关技能| [`arxiv`](/docs/user-guide/skills/bundled/research/research-arxiv) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# DuckDuckGo 搜索

使用 DuckDuckGo 进行免费网络搜索。 **无需 API 密钥。**

当“web_search”不可用或不适合时（例如，当未设置“FIRECRAWL_API_KEY”时）首选。当特别需要 DuckDuckGo 结果时，也可以用作独立搜索路径。

## 检测流程

在选择方法之前检查实际可用的内容：

````bash
# 检查 CLI 可用性
命令 -v ddgs >/dev/null && echo "DDGS_CLI=installed" ||回显“DDGS_CLI=缺失”
````

决策树：
1. 如果安装了`ddgs` CLI，首选`terminal` + `ddgs`
2. 如果 `ddgs` CLI 丢失，不要假设 `execute_code` 可以导入 `ddgs`
3. 如果用户特别想要DuckDuckGo，请先在相关环境中安装`ddgs`
4. 否则，请使用内置网络/浏览器工具

重要的运行时注意事项：
- 终端和“execute_code”是单独的运行时
- 成功的 shell 安装并不能保证 `execute_code` 可以导入 `ddgs`
- 永远不要假设第三方 Python 包预装在 `execute_code` 中

## 安装

仅当特别需要 DuckDuckGo 搜索且运行时尚未提供时才安装“ddgs”。

````bash
# Python 包 + CLI 入口点
pip安装ddgs

# 验证 CLI
ddgs——帮助
````

如果工作流依赖于 Python 导入，请在使用“from ddgs import DDGS”之前验证同一运行时是否可以导入“ddgs”。

## 方法 1：CLI 搜索（首选）

如果存在“terminal”，请通过“ddgs”命令使用它。这是首选路径，因为它避免假设“execute_code”沙箱安装了“ddgs”Python 包。

````bash
# 文本搜索
ddgs text -q "python 异步编程" -m 5

# 新闻搜索
ddgs新闻-q“人工智能”-m 5

# 图片搜索
ddgs images -q“风景摄影”-m 10

# 视频搜索
ddgs 视频 -q "python 教程" -m 5

# 带区域过滤器
ddgs text -q“最佳餐厅”-m 5 -r us-en

# 仅最近结果（d=天，w=周，m=月，y=年）
ddgs text -q "最新人工智能新闻" -m 5 -t w

# 用于解析的 JSON 输出
ddgs text -q“fastapi教程”-m 5 -o json
````

### CLI 标志

|旗帜|描述 |示例|
|------|-------------|---------|
| `-q` |查询 — **必填** | `-q "搜索词"` |
| `-m` |最大结果 | `-m 5` |
| `-r` |地区 | `-r us-en` |
| `-t` |时间限制 | `-t w`（周）|
| `-s` |安全搜索| `-s 关闭` |
| `-o` |输出格式 | `-o json` |

## 方法二：Python API（需验证）

仅在验证“ddgs”已安装后，才能在“execute_code”或其他 Python 运行时中使用“DDGS”类。不要假设 `execute_code` 默认包含第三方包。

安全措辞：
- “如果需要，在安装或验证软件包后，将 `execute_code` 与 `ddgs` 一起使用”

避免说：
-“`execute_code`包括`ddgs`”
- “DuckDuckGo 搜索默认在 `execute_code` 中工作”

**重要提示：** `max_results` 必须始终作为 **关键字参数** 传递 - 位置使用会在所有方法上引发错误。

### 文本搜索

最适合：一般研究、公司、文档。

````蟒蛇
从 DDGS 导入 DDGS

将 DDGS() 作为 ddgs：
    for r in ddgs.text("python 异步编程", max_results=5):
        打印（r[“标题”]）
        打印（r[“href”]）
        打印（r.get（“正文”，“”）[：200]）
        打印（）
````

返回：“标题”、“href”、“正文”

### 新闻搜索

最适合：时事、突发新闻、最新动态。

````蟒蛇
从 DDGS 导入 DDGS

将 DDGS() 作为 ddgs：
    for r in ddgs.news("人工智能法规 2026", max_results=5):
        print(r["日期"], "-", r["标题"])
        print(r.get("源", ""), "|", r["url"])
        打印（r.get（“正文”，“”）[：200]）
        打印（）
````

返回：`date`、`title`、`body`、`url`、`image`、`source`

### 图片搜索

最适合：视觉参考、产品图像、图表。

````蟒蛇
从 DDGS 导入 DDGS

将 DDGS() 作为 ddgs：
    for r in ddgs.images("半导体芯片", max_results=5):
        打印（r[“标题”]）
        打印（r[“图像”]）
        print(r.get("缩略图", ""))
        打印（r.get（“来源”，“”））
        打印（）
````

返回：`标题`、`图像`、`缩略图`、`url`、`高度`、`宽度`、`来源`

### 视频搜索

最适合：教程、演示、解释。

````蟒蛇
从 DDGS 导入 DDGS

将 DDGS() 作为 ddgs：
    对于 ddgs.videos 中的 r（“FastAPI 教程”，max_results=5）：
        打印（r[“标题”]）
        print(r.get("内容", ""))
        打印（r.get（“持续时间”，“”））
        打印（r.get（“提供者”，“”））
        print(r.get("已发布", ""))
        打印（）
````

返回：“标题”、“内容”、“描述”、“持续时间”、“提供者”、“已发布”、“统计信息”、“上传者”

### 快速参考

|方法|使用时间 |关键领域 |
|--------|----------|------------|
| `文本()` |一般研究、公司|标题、href、正文 |
| `新闻()` |时事、更新 |日期、标题、来源、正文、网址 |
| `图像()` |视觉效果、图表 |标题、图像、缩略图、网址 |
| `视频()` |教程、演示 |标题、内容、持续时间、提供者 |

## 工作流程：搜索然后提取

DuckDuckGo 返回标题、URL 和片段，而不是完整的页面内容。要获取完整页面内容，请先搜索，然后使用“web_extract”、浏览器工具或curl 提取最相关的URL。

CLI 示例：

````bash
ddgs text -q "fastapi 部署指南" -m 3 -o json
````

Python 示例，仅在验证该运行时中安装了“ddgs”之后：

````蟒蛇
从 DDGS 导入 DDGS

将 DDGS() 作为 ddgs：
    results = list(ddgs.text("fastapi部署指南", max_results=3))
    对于结果中的 r：
        print(r["标题"], "->", r["href"])
````

然后使用“web_extract”或其他内容检索工具提取最佳 URL。

## 限制

- **速率限制**：DuckDuckGo 可能会在多次快速请求后受到限制。如果需要，在搜索之间添加短暂的延迟。
- **无内容提取**：`ddgs` 返回片段，而不是整页内容。使用“web_extract”、浏览器工具或curl 来获取完整的文章/页面。
- **结果质量**：总体不错，但可配置性不如 Firecrawl 的搜索。
- **可用性**：DuckDuckGo 可能会阻止来自某些云 IP 的请求。如果搜索返回空，请尝试不同的关键字或等待几秒钟。
- **字段可变性**：返回字段可能因结果或“ddgs”版本而异。对可选字段使用“.get()”以避免“KeyError”。
- **单独的运行时**：在终端中成功安装“ddgs”并不自动意味着“execute_code”可以导入它。

## 故障排除

|问题 |可能的原因 |做什么 |
|---------|--------------|------------|
| `ddgs：找不到命令` | shell环境中未安装CLI |安装`ddgs`，或使用内置的网络/浏览器工具 |
| `ModuleNotFoundError：没有名为“ddgs”的模块` | Python 运行时未安装该包 |在准备好运行时之前，不要在那里使用 Python DDGS |
|搜索没有返回任何内容 |临时限速或查询不佳 |等待几秒钟，重试或调整查询 |
| CLI 可以工作，但 `execute_code` 导入失败 |终端和 `execute_code` 是不同的运行时 |继续使用 CLI，或单独准备 Python 运行时 |

## 陷阱

- **`max_results` 仅限关键字**：`ddgs.text("query", 5)` 会引发错误。使用 ddgs.text("query", max_results=5)`。
- **不要假设 CLI 存在**：使用前检查 `command -v ddgs`。
- **不要假设 `execute_code` 可以导入 `ddgs`**：`from ddgs import DDGS` 可能会因 `ModuleNotFoundError` 失败，除非单独准备运行时。
- **包名称**：包是 `ddgs` （以前是 `duckduckgo-search`）。使用“pip install ddgs”安装。
- **不要混淆`-q`和`-m`** (CLI)：`-q`用于查询，`-m`用于最大结果计数。
- **空结果**：如果 `ddgs` 不返回任何内容，则可能受到速率限制。等待几秒钟然后重试。

## 验证

针对“ddgs==9.11.2”语义验证的示例。技能指南现在将 CLI 可用性和 Python 导入可用性视为单独的问题，以便记录的工作流程与实际运行时行为相匹配。