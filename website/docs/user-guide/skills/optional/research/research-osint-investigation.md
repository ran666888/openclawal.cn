---
title: "Osint Investigation"
sidebar_label: "Osint Investigation"
description: "Public-records OSINT investigation framework — SEC EDGAR filings, USAspending contracts, Senate lobbying, OFAC sanctions, ICIJ offshore leaks, NYC property r..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#Osint调查

公共记录 OSINT 调查框架 — SEC EDGAR 文件、美国支出合同、参议院游说、OFAC 制裁、ICIJ 离岸泄密、纽约市财产记录 (ACRIS)、OpenCorporates 登记处、CourtListener 法庭记录、Wayback Machine 档案、维基百科 + 维基数据、GDELT 新闻监控。跨源实体解析、交叉链接分析、时序关联、证据链。仅限 Python 标准库。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/osint-investigation` 安装 |
|路径| `可选技能/研究/osint-调查` |
|版本 | `0.1.0` |
|作者 | OpenClaw（改编自 ShinMegamiBoson/OpenPlanter，麻省理工学院）|
|平台| linux、macos、windows |
|标签 | `osint`、`调查`、`公共记录`、`sec`、`制裁`、`公司登记`、`财产`、`法院`、`尽职调查`、`新闻` |
|相关技能| [`domain-intel`](/docs/user-guide/skills/optional/research/research-domain-intel), [`arxiv`](/docs/user-guide/skills/bundled/research/research-arxiv) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# OSINT 调查 — 公共记录交叉引用

公共记录 OSINT 的调查框架：政府合同、
公司备案、游说、制裁、离岸泄密、财产记录、
法庭记录、网络档案、知识库和全球新闻。解决
跨异构源的实体，通过显式建立交叉链接
信心、运行统计计时测试并生成结构化证据
链。

**仅限 Python stdlib。** 零安装。适用于 Linux、macOS、Windows。大多数
源无需 API 密钥即可工作（OpenCorporates 有一个可选的免费令牌
从而提高了速率限制）。

改编自 MIT 授权的 ShinMegamiBoson/OpenPlanter 项目；扩大
涵盖身份/财产/诉讼/档案/新闻来源
原文没有提及。

## 什么时候使用这个技能

当用户请求时使用：

- “追随金钱”——政府合同、游说 → 立法、制裁
- 公司尽职调查——谁控制着X公司，他们在哪里
  公司、谁在董事会任职、他们提交了哪些文件
- 制裁筛查——OFAC SDN 上的实体 X、ICIJ 离岸泄密
- 付费调查——与海外有联系的承包商、游说
  客户获奖
- 财产所有权——按姓名或地址查找记录的契约/抵押
  （纽约市；对于其他县，请在相关记录器上点用户）
- 诉讼历史 — 查找联邦 + 州法院意见和 PACER 案卷
- 命名各异的多源实体解析（LLC 后缀、缩写）
- 具有明确置信水平的证据链构建
- “关于 X 的说法” — 国际新闻 (GDELT) + 维基百科
  叙事+ Wayback Machine 恢复无效 URL

请勿将此技能用于：

- 一般网络研究 → `web_search` / `web_extract`
- 领域/基础设施 OSINT → “领域情报”技能
- 学术文献→`arxiv`技能
- 社交媒体资料发现→“夏洛克”技能（可选）
- 美国 **联邦** 竞选资金 — 此处故意不涵盖 FEC
  （对于免费网站上的临时贡献者姓名查询，该 API 不可靠
  DEMO_KEY 层）。对于联邦捐赠，请将用户指向
  直接 https://www.fec.gov/data/。

## 工作流程

代理通过“终端”工具运行脚本。 `SKILL_DIR` 是目录
持有此技能.md。

### 1. 确定适用的来源

阅读数据源 wiki 条目来计划调查：

````
ls SKILL_DIR/引用/来源/

# 联邦金融/监管
cat SKILL_DIR/references/sources/sec-edgar.md # 公司备案
cat SKILL_DIR/references/sources/usaspending.md # 联邦合同
cat SKILL_DIR/references/sources/senate-ld.md # 游说
cat SKILL_DIR/references/sources/ofac-sdn.md # 制裁
cat SKILL_DIR/references/sources/icij-offshore.md # 海上泄漏

#身份/财产/诉讼/档案/新闻
cat SKILL_DIR/references/sources/nyc-acris.md # 纽约市财产记录
cat SKILL_DIR/references/sources/opencorporates.md # 全球公司注册表
cat SKILL_DIR/references/sources/courtlistener.md # 法庭记录（联邦+州）
cat SKILL_DIR/references/sources/wayback.md # Wayback Machine 档案
cat SKILL_DIR/references/sources/wikipedia.md # 维基百科 + 维基数据
cat SKILL_DIR/references/sources/gdelt.md # 全球新闻监控
````

每个条目都遵循 9 个部分的模板：摘要、访问、架构、覆盖范围、
交叉引用键、数据质量、采集、法律、引用。

**交叉引用潜力**部分映射源之间的连接键 - 阅读
那些首先选择正确的一对的人。

### 2. 获取数据

每个源在“SKILL_DIR/scripts/”中都有一个仅 stdlib 的获取脚本：

**联邦金融/监管**

````bash
# SEC EDGAR 文件（公司披露）
python3 SKILL_DIR/scripts/fetch_sec_edgar.py --cik 0000320193 \
    --类型 10-K,10-Q --out data/edgar_filings.csv

# 美国支出联邦合同
python3 SKILL_DIR/scripts/fetch_usaspending.py --recipient“示例公司”\
    --fy 2024 --out data/contracts.csv

# 参议院 LD-1 / LD-2 游说披露
python3 SKILL_DIR/scripts/fetch_senate_ld.py --client“示例公司”\
    --2024 年 --out data/lobbying.csv

# OFAC SDN 制裁名单（完整快照）
python3 SKILL_DIR/scripts/fetch_ofac_sdn.py --out data/ofac_sdn.csv

# ICIJ Offshore Leaks — 首次使用时下载约 70 MB 批量 CSV，
# 然后在本地搜索。缓存 30 天以下
# $HERMES_OSINT_CACHE/icij/ （默认：~/.cache/hermes-osint/icij/）。
python3 SKILL_DIR/scripts/fetch_icij_offshore.py --entity "EXAMPLE CORP" \
    --输出数据/icij.csv
````

**身份/财产/诉讼/档案/新闻**

````bash
# 纽约市财产记录（契约、抵押、留置权）——ACRIS via Socrata
python3 SKILL_DIR/scripts/fetch_nyc_acris.py --name“史密斯，约翰”\
    --out 数据/acris.csv
python3 SKILL_DIR/scripts/fetch_nyc_acris.py --地址“571 HUDSON”\
    --out 数据/acris_addr.csv

# OpenCorporates — 130 多个司法管辖区的公司注册机构
#（需要免费令牌；设置 OPENCORPORATES_API_TOKEN 或传递 --token）
python3 SKILL_DIR/scripts/fetch_opencorporates.py --query "示例公司" \
    --jurisdiction us_ny --out data/opencorporates.csv

# CourtListener — 联邦 + 州法院意见、PACER 案卷
python3 SKILL_DIR/scripts/fetch_courtlistener.py --query "史密斯诉示例公司" \
    --输入意见 --out data/courts.csv

# Wayback Machine — 历史网络捕获
python3 SKILL_DIR/scripts/fetch_wayback.py --url "example.com" \
    --匹配主机 --折叠摘要 --out data/wayback.csv

# 维基百科 + 维基数据 — 叙述性生物 + 结构化事实
# 设置 HERMES_OSINT_UA=your-app/1.0 (your@email) 以标识您自己
python3 SKILL_DIR/scripts/fetch_wikipedia.py --query“比尔·盖茨”\
    --输出数据/wp.csv

# GDELT — 100 多种语言的全球新闻，~2015→现在
python3 SKILL_DIR/scripts/fetch_gdelt.py --query '“示例公司”' \
    --timespan 1y --out data/gdelt.csv
````

所有输出都是带有标题行的标准化 CSV。以幂等方式重新运行脚本。

当私人不会出现在来源中时（例如 SEC EDGAR 对于非公开-
公司人员，美国为非联邦承包商的人支出，参议院
对于非游说客户的 LDA），脚本返回 0 行，其中
清除警告，而不是默默地写入空的 CSV。埃德加特别
当公司名称解析器与单个表格 3/4/5 归档器匹配时进行标记
而不是公司注册人。

每个来源的 wiki 条目中都有速率限制注释。默认获取器休眠
在分页请求之间礼貌地进行。 **API 密钥提高了速率限制**
支持它们的来源（`SEC_USER_AGENT`、`SENATE_LDA_TOKEN`、
`OPENCORPORATES_API_TOKEN`、`COURTLISTENER_TOKEN`)。所有脚本均已浮出水面
429立即响应上游的配额消息，以便用户
知道要放慢速度或提供钥匙。

### 3. 跨源解析实体

标准化名称并查找两个 CSV 文件之间的匹配项：

````bash
# 将游说客户 (Senate LDA) 与合同接收者 (USAspending) 进行匹配
python3 SKILL_DIR/scripts/entity_resolution.py \
    --left data/lobbying.csv --left-name-col client_name \
    --right data/contracts.csv --right-name-col 收件人名称 \
    --out 数据/cross_links.csv
````

具有明确置信度的三个匹配层：

|等级 |方法|信心|
|------|--------|------------|
| `精确` |标准化字符串后缀/标点符号后相等 |高|
| `模糊` |排序标记相等（词袋匹配）|中等|
| `token_overlap` | ≥60% 令牌重叠，≥2 个共享令牌，令牌 ≥4 个字符 |低|

输出`cross_links.csv`列：`match_type，confidence，left_name，
右名称、左规范化、右规范化、左行、右行`。

### 4.统计时序相关性（可选）

测试两个时间序列是否可疑地靠近在一起 - 例如
临近合同授予的游说文件——使用排列测试：

````bash
python3 SKILL_DIR/scripts/timing_analysis.py \
    --donations data/lobbying.csv --donation-date-colfiling_date \
        --donation-amount-col 收入 --donation-donor-col client_name \
        --donation-recipient-col registrant_name \
    --contracts data/contracts.csv --contract-date-col Award_date \
        --contract-vendor-col 收件人名称 \
    --交叉链接数据/cross_links.csv \
    --排列 1000 \
    --out 数据/timing.json
````

该脚本的列标志故意是通用的 - 原始工具是
为捐赠与奖励而写，但它适用于任何（事件、收款人）时间
系列通过交叉链接加入。原假设：事件发生时间为
与颁奖日期无关。单尾 p 值 = 排列的分数
平均最近奖励距离 ≤ 观察到的。每个最少 3 个事件（付款人、
供应商）配对来运行测试。

### 5. 构建调查结果 JSON（证据链）

````bash
python3 SKILL_DIR/scripts/build_findings.py \
    --交叉链接数据/cross_links.csv \
    --计时数据/timing.json \
    --out 数据/findings.json
````

每个发现都有“id、标题、严重性、置信度、摘要、证据[]、来源[]”。
每个证据项都指向源 CSV 中的特定行。用户（或
后续代理人）可以根据其来源核实每项索赔。

## 信心和证据纪律

这就是技能的承重规则。告诉用户：

- 每项索赔都必须追溯至记录。没有赤裸裸的断言。
- 置信度随索赔而变化。 `match_type=fuzzy` 是“可能”，
  不是“确认”。
- 实体解析产生候选，而不是结论。 “模糊”匹配
  “ACME LLC”和“Acme Holdings Group”之间的关系是一种领先，而不是事实。
- 统计意义≠不当行为。 p < 0.05 表示时序模式
  在零值下不太可能。它并不构成腐败。
- 这里的所有数据源都是公共记录。它们可能仍含有
  不准确、过时的信息或编辑（GDPR、密封记录）。

## 添加新数据源

使用模板：

````bash
cp SKILL_DIR/templates/source-template.md \
    SKILL_DIR/references/sources/<your-source>.md
````

填写全部 9 个部分。在 `scripts/` 中编写一个 `fetch_<source>.py` 脚本
仅使用 stdlib 并写入规范化的 CSV。更新源列表
上面的“何时使用”部分。

## 工具及其局限性

-`entity_resolution.py`不使用外部模糊库（没有rapidfuzz，
  没有水母）。令牌袋匹配是这里的上限。如果您需要
  编辑、音译或拼音匹配，单独 pip-install。
- `timing_analysis.py` 使用 Python 的 `random` 进行排列。对于
  再现性，通过 `--seed N`。
- `fetch_*.py` 脚本使用 `urllib.request` 并遵循 `Retry-After`。重型
  批量使用可能仍然违反服务条款——首先阅读每个来源的法律部分。

## 法律说明

所有第一阶段来源都是公共记录。允许批量收购
其各自的访问条款（信息自由法、公共记录法、ICIJ 明确
出版物、OFAC 公共数据）。然而：

- 一些来源积极限制速率。尊重他们的头球。
- 一些修订注册人信息（WHOIS 上的 GDPR、密封归档）。
- 交叉引用公共记录来识别私人可以拥有
  伦理影响。这项技能产生的是证据链，而不是指控。