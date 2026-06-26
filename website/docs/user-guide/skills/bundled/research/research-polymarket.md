---
title: "Polymarket — Query Polymarket: markets, prices, orderbooks, history"
sidebar_label: "Polymarket"
description: "Query Polymarket: markets, prices, orderbooks, history"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#综合市场

查询Polymarket：市场、价格、订单、历史。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/研究/多元市场` |
|版本 | `1.0.0` |
|作者 | OpenClaw代理+Teknium|
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Polymarket — 预测市场数据

使用 Polymarket 的公共 REST API 查询预测市场数据。
所有端点都是只读的，并且需要零身份验证。

请参阅“references/api-endpoints.md”以获取带有curl示例的完整端点参考。

## 何时使用

- 用户询问预测市场、投注赔率或事件概率
- 用户想知道“X 发生的几率是多少？”
- 用户专门询问 Polymarket
- 用户想要市场价格、订单数据或价格历史记录
- 用户要求监控或跟踪预测市场走势

## 关键概念

- **事件**包含一个或多个**市场**（一对多关系）
- **市场**是二元结果，是/否价格在 0.00 到 1.00 之间
- 价格是概率：价格 0.65 意味着市场认为 65% 的可能性
- `outcomePrices` 字段：JSON 编码数组，如 `["0.80", "0.20"]`
- `clobTokenIds` 字段：用于价格/书籍查询的两个令牌 ID [是、否] 的 JSON 编码数组
- `conditionId` 字段：用于价格历史查询的十六进制字符串
- 交易量以 USDC（美元）为单位

## 三个公共 API

1. **Gamma API** 位于 `gamma-api.polymarket.com` — 发现、搜索、浏览
2. **CLOB API** at `clob.polymarket.com` — 实时价格、订单簿、历史记录
3. **Data API** at `data-api.polymarket.com` — 交易、未平仓合约

## 典型工作流程

当用户询问预测市场赔率时：

1. **搜索** 使用 Gamma API 公共搜索端点及其查询
2. **解析**响应——提取事件及其嵌套市场
3. **提出**市场问题、当前价格（百分比）和数量
4. **深入研究**（如果有要求）——使用 clobTokenIds 作为订单簿，使用 conditionId 作为历史记录

## 展示结果

为了便于阅读，将价格格式化为百分比：
- 结果价格 `["0.652", "0.348"]` 变为“是：65.2%，否：34.8%”
- 始终显示市场问题和概率
- 包括可用的音量

示例：““X 会发生吗？” — 65.2% 是（120 万美元的交易量）`

## 解析双编码字段

Gamma API 以 JSON 字符串形式返回“outcomePrices”、“outcomes”和“clobTokenIds”
JSON 响应内部（双编码）。使用Python处理时，用以下命令解析它们
`json.loads(market['outcomePrices'])` 获取实际的数组。

## 速率限制

慷慨——正常使用时不太可能发生：
- Gamma：每 10 秒 4,000 个请求（一般）
- CLOB：每 10 秒 9,000 个请求（一般）
- 数据：每 10 秒 1,000 个请求（一般）

## 限制

- 该技能是只读的 - 它不支持进行交易
- 交易需要基于钱包的加密身份验证（EIP-712 签名）
- 一些新市场可能有空的价格历史记录
- 交易存在地域限制，但只读数据可在全球范围内访问