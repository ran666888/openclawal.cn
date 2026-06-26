---
title: "Searxng Search — Free meta-search via SearXNG — aggregates results from 70+ search engines"
sidebar_label: "Searxng Search"
description: "Free meta-search via SearXNG — aggregates results from 70+ search engines"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#Searxng 搜索

通过 SearXNG 进行免费元搜索 — 聚合来自 70 多个搜索引擎的结果。自托管或使用公共实例。无需 API 密钥。当网络搜索工具集不可用时自动回退。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/searxng-search` 安装 |
|路径| `可选技能/研究/searxng-搜索` |
|版本 | `1.0.0` |
|作者 | OpenClaw 代理 |
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | `搜索`、`searxng`、`元搜索`、`自托管`、`免费`、`后备` |
|相关技能| [`duckduckgo-search`](/docs/user-guide/skills/optional/research/research-duckduckgo-search), [`domain-intel`](/docs/user-guide/skills/optional/research/research-domain-intel) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# SearXNG 搜索

使用 [SearXNG](https://searxng.org/) 进行免费元搜索 — 一个尊重隐私的自托管搜索聚合器，可同时查询 70 多个搜索引擎。

**使用公共实例时不需要 API 密钥**。也可以自托管以实现完全控制。当主网络搜索工具集（`FIRECRAWL_API_KEY`）未配置时，自动显示为后备。

## 配置

SearXNG 需要一个指向您的 SearXNG 实例的“SEARXNG_URL”环境变量：

````bash
# 公共实例（无需设置）
SEARXNG_URL=https://searxng.example.com

# 自托管 SearXNG
SEARXNG_URL=http://localhost:8888
````

如果未配置实例，则此技能不可用，并且代理将回退到其他搜索选项。

## 检测流程

在选择方法之前检查实际可用的内容：

````bash
# 检查 SEARXNG_URL 是否已设置并且实例是否可访问
卷曲 -s --max-time 5 "${SEARXNG_URL}/search?q=test&format=json" |头-c 200
````

决策树：
1. 如果设置了`SEARXNG_URL`并且实例响应，则使用SearXNG
2. 如果“SEARXNG_URL”未设置或无法访问，请使用其他可用的搜索工具
3. 如果用户特别想要SearXNG，请帮助他们设置一个实例或找到一个公共实例

## 方法 1：通过curl 进行CLI（首选）

通过 `terminal` 使用 `curl` 来调用 SearXNG JSON API。这可以避免假设已安装任何特定的 Python 包。

````bash
# 文本搜索（JSON 输出）
卷曲-s --最大时间 10 \
  “${SEARXNG_URL}/search?q=python+async+programming&format=json&engines=google,bing&limit=10”

# 关闭安全搜索
卷曲-s --最大时间 10 \
  “${SEARXNG_URL}/search?q=example&format=json&safesearch=0”

# 具体类别（一般、新闻、科学等）
卷曲-s --最大时间 10 \
  “${SEARXNG_URL}/search?q=AI+news&format=json&categories=news”
````

### 常见 CLI 标志

|旗帜|描述 |示例|
|------|-------------|---------|
| `q` |查询字符串（URL 编码）| `q=python+异步` |
| `格式` |输出格式：`json`、`csv`、`rss` | `格式=json` |
| `发动机` |以逗号分隔的引擎名称 | `engines=google、bing、ddg` |
| `限制` |每个引擎的最大结果（默认 10） | `限制=5` |
| `类别` |按类别过滤 | `类别=新闻、科学` |
| `安全搜索` | 0=无，1=中等，2=严格 | `安全搜索=0` |
| `时间范围` |过滤器：`日`、`周`、`月`、`年` | `时间范围=周` |

### 解析 JSON 结果

````bash
# 从 JSON 中提取标题和 URL
curl -s --max-time 10 "${SEARXNG_URL}/search?q=fastapi&format=json&limit=5" \
  | python3-c“
导入 json、系统
数据 = json.load(sys.stdin)
对于 data.get('结果', []) 中的 r：
    print(r.get('标题',''))
    print(r.get('url',''))
    print(r.get('内容','')[:200])
    打印（）
”
````

返回每个结果：`title`、`url`、`content`（片段）、`engine`、`parsed_url`、`img_src`、`thumbnail`、`author`、`published_date`

## 方法 2：通过 `requests` 的 Python API

直接从 Python 使用 SearXNG REST API 和“requests”库：

````蟒蛇
导入操作系统、请求、urllib.parse

base_url = os.environ.get("SEARXNG_URL", "")
如果不是base_url：
    引发运行时错误（“未设置 SEARXNG_URL”）

query =“fastapi部署指南”
参数 = {
    “q”：查询，
    “格式”：“json”，
    “限制”：5，
    “引擎”：“谷歌，bing”，
}

resp = requests.get(f"{base_url}/search", params=params, timeout=10)
resp.raise_for_status()
数据 = resp.json()

for r in data.get("results", []):
    打印（r[“标题”]）
    打印（r[“网址”]）
    打印（r.get（“内容”，“”）[：200]）
    打印（）
````

## 方法3：searxng-data Python包

要获得更结构化的访问，请安装 `searxng-data` 包：

````bash
pip install sealxng-data
````

````蟒蛇
从 searchxng_data 导入引擎

# 列出可用的引擎
打印（engines.list_engines（））
````

注意：此包仅提供引擎元数据，而不提供搜索 API 本身。

## 自托管 SearXNG

要运行您自己的 SearXNG 实例：

````bash
# 使用 Docker
docker run -d -p 8888:8080 \
  -v $(pwd)/searxng:/etc/searxng \
  searchxng/searxng:最新

# 然后设置
SEARXNG_URL=http://localhost:8888
````

或者通过 pip 安装：
````bash
pip 安装 searchxng
# 编辑/etc/searxng/settings.yml
搜索运行
````

公共 SearXNG 实例可在以下位置获取：
- `https://searxng.example.com`（替换为任何公共实例）

## 工作流程：搜索然后提取

SearXNG 返回标题、URL 和片段，而不是完整的页面内容。要获取完整页面内容，请先搜索，然后使用“web_extract”、浏览器工具或“curl”提取最相关的 URL。

````bash
# 搜索相关页面
卷曲 -s“${SEARXNG_URL}/search?q=fastapi+deployment&format=json&limit=3”
# 输出：带有标题和 URL 的结果列表

# 然后使用 web_extract 提取最佳 URL
````

## 限制

- **实例可用性**：如果 SearXNG 实例已关闭或无法访问，则搜索失败。始终检查“SEARXNG_URL”是否已设置并且实例是否可访问。
- **无内容提取**：SearXNG 返回片段，而不是完整页面内容。使用“web_extract”、浏览器工具或“curl”获取完整文章。
- **速率限制**：某些公共实例限制请求。自托管可以避免这种情况。
- **引擎覆盖率**：可用引擎取决于 SearXNG 实例配置。某些引擎可能会被禁用。
- **结果新鲜度**：元搜索聚合外部引擎 - 结果新鲜度取决于这些引擎。

## 故障排除

|问题 |可能的原因 |做什么 |
|---------|--------------|------------|
|未设置“SEARXNG_URL”|没有配置实例 |使用公共 SearXNG 实例或设置您自己的 |
|连接被拒绝 |实例未运行或 URL 错误 |检查 URL 是否正确以及实例是否正在运行 |
|空结果 |实例阻塞查询 |尝试不同的实例或自托管 |
|反应慢|负载下的公共实例 |自托管或使用负载较少的公共实例 |
|不支持 `json` 格式 |旧SearXNG版本|尝试“format=rss”或升级 SearXNG |

## 陷阱

- **始终设置`SEARXNG_URL`**：没有它，技能将无法发挥作用。
- **URL编码查询**：空格和特殊字符必须在curl中进行URL编码，或者在Python中使用`urllib.parse.quote()`。
- **使用 `format=json`**：默认格式可能不是机器可读的。始终显式请求 JSON。
- **设置超时**：始终使用 `--max-time` 或 `timeout=` 以避免挂在无法访问的实例上。
- **自托管是最好的**：公共实例可能会出现故障、速率限制或阻塞。自托管实例是可靠的。

## 实例发现

如果未设置“SEARXNG_URL”并且用户询问 SearXNG，请帮助他们：
1.找到一个公共SearXNG实例（搜索“publicsearxnginstance”）
2.使用Docker或pip自行设置

公共实例列于：https://searxng.org/