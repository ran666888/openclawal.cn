---
title: "Merger Model — Build accretion/dilution (merger) models in Excel — pro-forma P&L, synergies, financing mix, EPS impact"
sidebar_label: "Merger Model"
description: "Build accretion/dilution (merger) models in Excel — pro-forma P&L, synergies, financing mix, EPS impact"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 合并模型

在 Excel 中构建增值/稀释（合并）模型 - 预计损益、协同效应、融资组合、每股收益影响。与 excel-author 配对。用于并购推介、董事会材料或交易评估。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/finance/merger-model` 安装 |
|路径| `可选技能/财务/合并模型` |
|版本 | `1.0.0` |
|作者 |人择（由 Nous Research 改编）|
|许可证|阿帕奇-2.0 |
|平台| linux、macos、windows |
|标签 | `金融`、`m-and-a`、`合并`、`增值稀释`、`excel`、`openpyxl`、`建模`、`投资银行` |
|相关技能| [`excel-author`](/docs/user-guide/skills/optional/finance/finance-excel-author), [`pptx-author`](/docs/user-guide/skills/optional/finance/finance-pptx-author), [`dcf-model`](/docs/user-guide/skills/Optional/finance/finance-dcf-model), [`3-statement-model`](/docs/user-guide/skills/optional/finance/finance-3-statement-model) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

## 环境

此技能假设**无头 openpyxl** - 您正在磁盘上生成 .xlsx 文件。
遵循“excel-author”技能的单元格着色、公式、命名范围和敏感度表约定。
交付前重新计算：`python /path/to/excel-author/scripts/recalc.py ./out/model.xlsx`。

# 合并模型

为并购交易建立增值/稀释分析。对预计每股收益影响、协同敏感性和购买价格分配进行建模。在评估潜在收购、为推介准备合并后果分析或就交易条款提供建议时使用。

## 工作流程

### 第 1 步：收集输入

**收单机构：**
- 公司名称、当前股价、已发行股票
- LTM 和 NTM EPS（公认会计原则和调整后）
- 市盈率倍数
- 税前债务成本、税率
- 资产负债表上的现金、现有债务

**目标：**
- 公司名称、当前股价、已发行股票（如果公开）
- LTM 和 NTM EPS 或净利润
- 企业价值或股权价值

**交易条款：**
- 每股发行价（或当前溢价）
- 考虑因素组合：现金百分比与股票百分比
- 筹集新债务以资助现金部分
- 预期协同效应（收入和成本）和分阶段实施时间表
- 交易费用和融资成本
- 预计截止日期

### 第 2 步：采购价格分析

|项目 |价值|
|------|--------|
|每股发售价| |
|溢价至当前 | |
|股权价值| |
|加：承担的净债务| |
|企业价值 | |
|隐含 EV / EBITDA | |
|隐含市盈率 | |

### 步骤 3：来源和用途

|来源 | $ |用途 | $ |
|--------|---|------|---|
|新债务| |股权收购价格| |
|库存现金| |再融资目标债务| |
|新股发行 | |交易费用| |
| | |融资费用| |
| **总计** | | **总计** | |

### 第 4 步：预计 EPS（增加/稀释）

逐年计算（第1-3年）：

| |独立|备考|增加/（稀释）|
|---|-----------|------------|------------------------|
|收购方净利润| | | |
|目标净利润| | | |
|协同效应（税后）| | | |
|放弃现金利息（税后）| | | |
|新债务利息（税后）| | | |
|无形摊销（税后）| | | |
|预估净利润| | | |
|备考股票| | | |
| **预估每股收益** | | | |
| **增加/（稀释）%** | | | |

### 步骤 5：敏感性分析

**增值/稀释与协同效应和报价溢价：**

| | 000 万美元同步 | 2500 万美元同步 | 5000 万美元同步 | 7500 万美元同步 | 1 亿美元同步 |
|---|---------|----------|----------|----------|------------|
| 15% 溢价 | | | | | |
| 20% 溢价 | | | | | |
| 25% 溢价 | | | | | |
| 30% 溢价 | | | | | |

**增值/稀释与现金/股票组合：**

| | 100%现金| 75/25 | 75/25 50/50 | 50/50 25/75 | 25/75 100% 库存 |
|---|-----------|--------|--------|--------|------------|
|第一年 | | | | | |
|第 2 年 | | | | | |

### 第 6 步：盈亏平衡协同效应

计算该交易在第一年实现每股盈利中性所需的最低协同效应。

### 第 7 步：输出

- Excel 工作簿包含：
  - 假设选项卡
  - 来源和用途
  - 预计损益表
  - 吸积/稀释总结
  - 灵敏度表
  - 盈亏平衡分析
- 一页合并后果摘要的宣传书

## 重要提示

- 始终显示相关的 GAAP 和调整后（现金）每股收益
- 股票交易：使用收购方当前价格作为换股比例，注意新股稀释
- 包括购买价格分配——公认会计原则每股收益的商誉和无形摊销事项
- 协同效应的逐步实施至关重要——第一年通常只有运行率协同效应的 25-50%
- 不要忘记所用现金所放弃的利息收入和所筹集债务的新利息支出
- 协同效应和利率调整的税率应与收购方的边际税率相匹配


## 数据源——MCP优先，网络后备

下面的许多段落都提到“使用 S&P Kensho MCP / Daloopa MCP / FactSet MCP”。这些是来自原始 Cowork 插件上下文的商业金融数据 MCP。在爱马仕：

- **如果您配置了任何结构化财务数据 MCP**（OpenClaw 支持 MCP — 请参阅“native-mcp”技能），更喜欢将其用于时间点比较、先例交易和归档。
- **否则**，回退到：
  - 针对 SEC EDGAR (`https://www.sec.gov/cgi-bin/browse-edgar`) 的美国备案的“web_search”/“web_extract”
  - 公司新闻稿、收益报告的 IR 页面
  - 用于交互式数据门户的“browser_navigate”
  - 用户提供的数据（当上下文没有时明确询问）
- **绝不捏造**。如果无法获取多重编号、先例编号或申请编号，请将单元格标记为“[UNSOURCED]”并将其呈现给用户。

## 归因

该技能改编自 Anthropic 的 Claude for Financial Services 插件套件 (Apache-2.0)。 Office-JS / Cowork live-Excel 路径已被删除；此版本通过“excel-author”技能约定以无头 openpyxl 为目标。原文：https://github.com/anthropics/financial-services