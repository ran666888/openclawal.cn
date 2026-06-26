---
title: "Arxiv — Search arXiv papers by keyword, author, category, or ID"
sidebar_label: "Arxiv"
description: "Search arXiv papers by keyword, author, category, or ID"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# arXiv 论文搜索

按关键字、作者、类别或 ID 搜索 arXiv 论文。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/研究/arxiv` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “研究”、“Arxiv”、“论文”、“学术”、“科学”、“API” |
|相关技能| [`ocr 和文档`](/docs/user-guide/skills/bundled/productivity/productivity-ocr-and-documents) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# arXiv 研究

通过 arXiv 的免费 REST API 搜索和检索学术论文。没有 API 密钥，没有依赖项——只有curl。

## 快速参考

|行动|命令|
|--------|---------|
|搜索论文 | `curl "https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5"` |
|获取特定论文 | `curl "https://export.arxiv.org/api/query?id_list=2402.03300"` |
|阅读摘要（网络）| `web_extract(urls=["https://arxiv.org/abs/2402.03300"])` |
|阅读全文 (PDF) | `web_extract(urls=["https://arxiv.org/pdf/2402.03300"])` |

## 搜索论文

API 返回 Atom XML。使用 `grep`/`sed` 进行解析或通过 `python3` 进行管道传输以获取干净的输出。

### 基本搜索

````bash
卷曲-s“https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5”
````

### 干净的输出（将 XML 解析为可读格式）

````bash
卷曲-s“https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=subscribedDate&sortOrder=降序”| python3-c“
导入 sys, xml.etree.ElementTree 作为 ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
对于 i，enumerate(root.findall('a:entry', ns)) 中的条目：
    title = Entry.find('a:title', ns).text.strip().replace('\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    已发布 = Entry.find('a:已发布', ns).text[:10]
    作者 = ', '.join(a.find('a:name', ns).entry.findall('a:author', ns)) 中的文本
    摘要 = Entry.find('a:summary', ns).text.strip()[:200]
    cats = ', '.join(c.get('term') for c inentry.findall('a:category', ns))
    print(f'{i+1}.[{arxiv_id}] {title}')
    print(f' 作者：{authors}')
    print(f' 已发布：{已发布} | 类别：{猫}')
    print(f' 摘要: {summary}...')
    打印（f'PDF：https://arxiv.org/pdf/{arxiv_id}'）
    打印（）
”
````

## 搜索查询语法

|前缀 |搜索 |示例|
|--------|----------|---------|
| `全部：` |所有领域 | `all:transformer+attention` |
| `ti:` |标题 | `ti:large+language+models` |
| `au：` |作者 | `au:vaswani` |
| `abs:` |摘要| `abs：强化+学习` |
| `cat:` |类别 | `cat:cs.AI` |
| `co:` |评论 | `co:accepted+NeurIPS` |

### Boolean operators

````
# AND（使用+时默认）
search_query=all:变压器+注意力

# 或
search_query=全部：GPT+OR+全部：BERT

# AND NOT
search_query=全部：语言+模型+而不是+全部：视觉

# Exact phrase
search_query=ti:"链+思想"

# 合并
search_query=au:hinton+AND+cat:cs.LG
````

## 排序和分页

|参数|选项|
|------------|---------|
| `sortBy` | `相关性`、`上次更新日期`、`提交日期` |
| `排序顺序` | ‘升序’、‘降序’ |
| `start` |结果偏移量（从 0 开始）|
| `max_results` |结果数（默认 10，最大 30000）|

````bash
# Latest 10 papers in cs.AI
卷曲-s“https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=subscribedDate&sortOrder=降序&max_results=10”
````

## Fetching Specific Papers

````bash
# By arXiv ID
卷曲-s“https://export.arxiv.org/api/query?id_list=2402.03300”

# Multiple papers
卷曲-s“https://export.arxiv.org/api/query?id_list=2402.03300,2401.12345,2403.00001”
````

## BibTeX Generation

获取论文的元数据后，生成 BibTeX 条目：

{% 原始%}
````bash
卷曲-s“https://export.arxiv.org/api/query?id_list=1706.03762”| python3-c“
导入 sys, xml.etree.ElementTree 作为 ET
ns = {'a'：'http://www.w3.org/2005/Atom'，'arxiv'：'http://arxiv.org/schemas/atom'}
root = ET.parse(sys.stdin).getroot()
条目 = root.find('a:entry', ns)
如果条目为 None: sys.exit('未找到纸张')
title = Entry.find('a:title', ns).text.strip().replace('\n', ' ')
authors = ' and '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
年 = Entry.find('a:已发布', ns).text[:4]
raw_id = Entry.find('a:id', ns).text.strip().split('/abs/')[-1]
cat = Entry.find('arxiv:primary_category', ns)
primary = cat.get('term') if cat is not None else 'cs.LG'
Last_name = Entry.find('a:author', ns).find('a:name', ns).text.split()[-1]
print(f'@article{{{last_name}{year}_{raw_id.replace(\".\", \"\")},')
print(f' 标题 = {{{标题}}},')
print(f'  author    = {{{authors}}},')
print(f'  year      = {{{year}}},')
print(f'  eprint    = {{{raw_id}}},')
print(f' archivePrefix = {{arXiv}},')
print(f'primaryClass = {{{primary}}},')
print(f'  url       = {{https://arxiv.org/abs/{raw_id}}}')
打印（'}'）
”
````
{% 结束绘制 %}

## 阅读论文内容

After finding a paper, read it:

````
# Abstract page (fast, metadata + abstract)
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# Full paper (PDF → markdown via Firecrawl)
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
````

For local PDF processing, see the `ocr-and-documents` skill.

## 常见类别

|类别 |领域 |
|----------|--------|
| `cs.AI` |人工智能|
| `cs.CL` |计算与语言（NLP）|
| `cs.CV` |计算机视觉 |
| `cs.LG` |机器学习 |
| `cs.CR` | Cryptography and Security |
| `stat.ML` |机器学习（统计）|
| `数学.OC` | Optimization and Control |
| `physical.comp-ph` |计算物理|

Full list: https://arxiv.org/category_taxonomy

## 帮助脚本

The `scripts/search_arxiv.py` script handles XML parsing and provides clean output:

````bash
python script/search_arxiv.py “GRPO 强化学习”
python scripts/search_arxiv.py "transformer attention" --max 10 --sort date
python scripts/search_arxiv.py --author "Yann LeCun" --max 5
python scripts/search_arxiv.py --category cs.AI --sort date
python scripts/search_arxiv.py --id 2402.03300
python scripts/search_arxiv.py --id 2402.03300,2401.12345
````

无依赖项 — 仅使用 Python stdlib。

---

## 语义学者（引文、相关论文、作者简介）

arXiv doesn't provide citation data or recommendations. Use the **Semantic Scholar API** for that — free, no key needed for basic use (1 req/sec), returns JSON.

### Get paper details + citations

````bash
# 通过 arXiv ID
卷曲-s“https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300?fields=标题，作者，引用计数，引用计数，影响力引用计数，年份，摘要”| python3 -m json.工具

# 通过语义学者论文 ID 或 DOI
curl -s "https://api.semanticscholar.org/graph/v1/paper/DOI:10.1234/example?fields=title,citationCount"
````

### 获取论文的引用（谁引用了它）

````bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/citations?fields=title,authors,year,citationCount&limit=10" | python3 -m json.工具
````

### Get references FROM a paper (what it cites)

````bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:2402.03300/references?fields=title,authors,year,citationCount&limit=10" | python3 -m json.工具
````

### Search papers (alternative to arXiv search, returns JSON)

````bash
卷曲-s“https://api.semanticscholar.org/graph/v1/paper/search?query=GRPO+reinforcement+learning&limit=5&fields=title,authors,year,itationCount,externalIds”| python3 -m json.工具
````

### 获取论文推荐

````bash
卷曲-s -X POST“https://api.semanticscholar.org/recommendations/v1/papers/”\
  -H“内容类型：application/json”\
  -d '{"positivePaperIds": ["arXiv:2402.03300"], "negativePaperIds": []}' | python3 -m json.工具
````

### 作者简介

````bash
卷曲-s“https://api.semanticscholar.org/graph/v1/author/search?query=Yann+LeCun&fields=name,hIndex,itationCount,paperCount”| python3 -m json.工具
````

### 有用的语义学者领域

`title`、`authors`、`year`、`abstract`、`itationCount`、`referenceCount`、`influenceialCitationCount`、`isOpenAccess`、`openAccessPdf`、`fieldsOfStudy`、`publicationVenue`、`externalIds`（包含 arXiv ID、DOI 等）

---

## 完整的研究工作流程

1. **Discover**: `python scripts/search_arxiv.py "your topic" --sort date --max 10`
2. **评估影响**： `curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID?fields=itationCount,influenceialCitationCount"`
3. **阅读摘要**：`web_extract(urls=["https://arxiv.org/abs/ID"])`
4. **阅读全文**：`web_extract(urls=["https://arxiv.org/pdf/ID"])`
5. **查找相关工作**： `curl -s "https://api.semanticscholar.org/graph/v1/paper/arXiv:ID/references?fields=title,itationCount&limit=20"`
6. **获取推荐**：POST 到语义学者推荐端点
7. **跟踪作者**： `curl -s "https://api.semanticscholar.org/graph/v1/author/search?query=NAME"`

## 速率限制

|应用程序接口 |评分 |授权 |
|-----|------|------|
| arXiv | ~1 请求/3 秒 |不需要 |
|语义学者| 1 请求/秒 |无（100/秒，使用 API 密钥）|

## 注释

- arXiv 返回 Atom XML — 使用帮助程序脚本或解析片段以获得干净的输出
- Semantic Scholar 返回 JSON — 通过 `python3 -m json.tool` 进行管道传输以提高可读性
- arXiv ID：旧格式（`hep-th/0601001`）与新格式（`2402.03300`）
- PDF：`https://arxiv.org/pdf/{id}` — 摘要：`https://arxiv.org/abs/{id}`
- HTML（如果可用）：`https://arxiv.org/html/{id}`
- 对于本地PDF处理，请参阅`ocr-and-documents`技能

## ID 版本控制

- `arxiv.org/abs/1706.03762` 始终解析为 **最新** 版本
- `arxiv.org/abs/1706.03762v1` 指向 **特定** 不可变版本
- 生成引文时，保留您实际阅读的版本后缀，以防止引文漂移（更高版本可能会大幅更改内容）
- API `<id>` 字段返回版本化 URL（例如，`http://arxiv.org/abs/1706.03762v7`）

## 撤回论文

论文提交后可以撤回。当这种情况发生时：
- `<summary>` 字段包含撤回通知（查找“撤回”或“撤回”）
- 元数据字段可能不完整
- 在将结果视为有效论文之前，务必检查摘要