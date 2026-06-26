---
title: "Stocks — Stock quotes, history, search, compare, crypto via Yahoo"
sidebar_label: "Stocks"
description: "Stock quotes, history, search, compare, crypto via Yahoo"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 股票

通过雅虎进行股票报价、历史记录、搜索、比较、加密。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/finance/stocks` 安装 |
|路径| `可选技能/财务/股票` |
|版本 | `0.1.0` |
|作者 |米巴伊（Mibayy），爱马仕代理商 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “股票”、“金融”、“市场”、“加密货币”、“投资” |
|相关技能| [`dcf-model`](/docs/user-guide/skills/optional/finance/finance-dcf-model)、[`comps-analysis`](/docs/user-guide/skills/Optional/finance/finance-comps-analysis)、[`lbo-model`](/docs/user-guide/skills/Optional/finance/finance-lbo-model) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 炒股技巧

通过雅虎财经只读市场数据。五个命令：`quote`、`search`、
“历史”、“比较”、“加密”。仅 Python stdlib — 无 API 密钥，无 pip
安装。雅虎的端点是非官方的，可能会受到速率限制或更改。

## 何时使用

- 用户询问当前股票价格（AAPL、TSLA、MSFT...）
- 用户想要通过公司名称查找股票
- 用户想要 OHLCV 历史记录或在某个日期范围内的表现
- 用户想要并排比较多个股票代码
- 用户询问加密货币价格（BTC、ETH、SOL...）

## 先决条件

仅限 Python 3.8+ stdlib。可选：设置“ALPHA_VANTAGE_KEY”以丰富
雅虎受面包屑保护时的“market_cap”、“pe_ratio”和 52 周水平
字段返回 null。免费密钥：https://www.alphavantage.co/support/#api-key

## 如何运行

通过“terminal”工具调用。安装后：

````
SCRIPT=~/.hermes/skills/finance/stocks/scripts/stocks_client.py
python3 $SCRIPT 引用 AAPL
````

所有输出都是标准输出上的 JSON — 如果您想对其进行切片，则通过“jq”进行管道传输。

## 快速参考

````
python3 $SCRIPT 引用 AAPL
python3 $SCRIPT 引用 AAPL MSFT GOOGL TSLA
python3 $SCRIPT 搜索“特斯拉”
python3 $SCRIPT 历史 NVDA --range 6mo
python3 $SCRIPT 比较 AAPL MSFT GOOGL
python3 $SCRIPT 加密 BTC ETH SOL
````

## 命令

### `引用符号 [SYMBOL2 ...]`

当前价格、变化、变化%、成交量、52 周高点/低点。

### `搜索查询`

按公司名称查找股票代码。返回前 5 个：符号、名称、交易所、类型。

### `历史符号 [--range 范围]`

每日 OHLCV 加上统计数据（最小值、最大值、平均值、总回报百分比）。范围：`1mo`，
“3 个月”、“6 个月”、“1 年”、“5 年”。默认值：`1mo`。

### `比较 SYMBOL1 SYMBOL2 [...]`

并排：价格、变化百分比、52 周表现。

### `加密符号 [SYMBOL2 ...]`

加密货币价格。传递“BTC”（脚本自动附加“-USD”）。

## 陷阱

- 雅虎财经的 API 是非官方的。端点可以更改或速率限制
  恕不另行通知 - 如果请求开始失败，这就是原因。
- 当雅虎的“market_cap”和“pe_ratio”可能在“quote”上返回 null
  碎屑会话未建立。将“ALPHA_VANTAGE_KEY”设置为回填。
- 在批量请求之间添加较小的延迟以避免速率限制。
- 这是只读的 - 没有订单，没有帐户集成。

## 验证

````
python3 ~/.hermes/skills/finance/stocks/scripts/stocks_client.py 引用 AAPL
````

返回一个带有 `symbol: "AAPL"` 和一个数字 `price` 字段的 JSON 对象。