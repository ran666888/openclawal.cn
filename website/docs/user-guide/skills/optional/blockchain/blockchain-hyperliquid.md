---
title: "Hyperliquid — Hyperliquid market data, account history, trade review"
sidebar_label: "Hyperliquid"
description: "Hyperliquid market data, account history, trade review"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 超液体

超流动市场数据、账户历史、交易回顾。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/blockchain/hyperliquid` 安装 |
|路径| `可选技能/区块链/超级液体` |
|版本 | `0.1.0` |
|作者 |雨果·塞奎尔（Hugo-SEQUIER），爱马仕经纪人 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “超流动性”、“区块链”、“加密货币”、“交易”、“永续合约”、“现货”、“DeFi” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 超液体技能

通过公共“/info”端点查询Hyperliquid市场和帐户数据。
只读 — 无 API 密钥、无签名、无订单。

12 个命令：`dexs`、`markets`、`spots`、`candles`、`funding`、`l2`、`state`、
“现货余额”、“执行”、“订单”、“审核”、“导出”。仅标准库
（`urllib`、`json`、`argparse`）。

---

## 何时使用

- 用户请求 Hyperliquid 永久或现货市场数据、蜡烛、资金或 L2 账簿
- 用户想要检查钱包的永久头寸、现货余额、成交或订单
- 用户希望结合最近的成交量和市场背景进行交易后审查
- 用户想要检查构建者部署的 perp dex 或 HIP-3 市场
- 用户想要蜡烛的标准化 JSON 导出 + 回测准备资金

---

## 先决条件

仅 Stdlib — 无外部包，无 API 密钥。

该脚本读取 `${HERMES_HOME:-~/.hermes}/.env` 以获得两个可选默认值：

- `HYPERLIQUID_API_URL` — 默认为 `https://api.hyperliquid.xyz`。设置为
  用于测试网的“https://api.hyperliquid-testnet.xyz”。
- `HYPERLIQUID_USER_ADDRESS` — `state`、`spot-balances` 的默认地址，
  “填写”、“订单”和“审核”。如果未设置，则将地址作为第一个传递
  立场论证。

当前工作目录中的项目“.env”被视为开发后备。

帮助脚本：`~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py`

---

## 如何运行

通过`terminal`工具调用：

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py <命令> [参数]
````

将 `--json` 添加到任何命令以获得机器可读的输出。

---

## 快速参考

````bash
hyperliquid_client.py dexs
hyperliquid_client.py 市场 [--dex DEX] [--limit N] [--sort 交易量|oi|funding_abs|change_abs|name]
hyperliquid_client.py 点 [--limit N]
hyperliquid_client.py 蜡烛 <coin> [--间隔 1h] [--小时 24] [--限制 N]
hyperliquid_client.py 资金 <coin> [--小时 72] [--限制 N]
hyperliquid_client.py l2 <硬币> [--levels N]
hyperliquid_client.py 状态 [地址] [--dex DEX]
hyperliquid_client.py 现货余额 [地址] [--limit N]
hyperliquid_client.py 填写 [地址] [--小时 N] [--限制 N] [--按时间聚合]
hyperliquid_client.py 订单 [地址] [--limit N]
hyperliquid_client.py 评论 [地址] [--硬币 COIN] [--小时 N] [--填充 N]
hyperliquid_client.py 导出 <coin> [--间隔 1h] [--小时 N] [--输出 PATH]
````

对于“state”、“spot-balances”、“fills”、“orders”和“review”，地址是
当在“${HERMES_HOME:-~/.hermes}/.env”中设置“HYPERLIQUID_USER_ADDRESS”时可选。

---

## 程序

### 1. 发现 DEX 和市场

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py dexs

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  市场 --limit 15 --排序数量

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  名额--限制15个
````

- `--dex` 仅适用于 perp 端点；省略第一个 perp dex。
- 现货对可能显示为“PURR/USDC”或“@107”等别名。
- HIP-3 市场在硬币前加上 dex，例如`mydex：BTC`。

### 2. 提取历史市场数据

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  蜡烛 BTC --间隔 1 小时 --小时 72 --限制 48

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  资助 BTC --小时 168 --限制 30
````

时间范围端点分页。对于较大的窗口，请稍后重复
`startTime` 或使用 `export` （如下）。

### 3. 检查实时订单簿

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  l2 BTC --级别 10
````

当被问及账面深度、近期流动性或潜在市场时使用
大订单的影响。

### 4. 审核帐户

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  状态 0xabc...

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  即期余额
````

`state` 返回 perp 位置； “现货余额”返回现货库存。
使用这些来询问“我的仓位怎么样？”、“我持有什么？”、“持有多少？”
可撤回吗？”。

### 5. 检查订单和订单

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  填充 0xabc... --小时 72 --限制 25

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  订单--限制 25
````

### 6. 生成交易审核

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  评论 0xabc... --小时 72 --填充 50

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  评论 --coin BTC --小时 168
````

报告已实现的盈亏、费用、赢/输计数、硬币分类、市场趋势
以及每个交易者的平均资金，加上启发法（费用拖累，
集中度、逆势损失）。

对于更深入的交易后分析：从“审查”开始寻找问题币
或窗口 → 拉动该时段的“成交”和“订单” → 拉动“蜡烛”
和每个交易代币的“资金” → 分别判断决策质量
从结果质量来看。

### 7.导出可重复使用的数据集

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  导出 BTC --间隔 1h --小时 168 --输出 ./btc-1h-7d.json

python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  导出BTC --间隔15m --小时72 --结束时间-ms 1760000000000
````

输出 JSON 包含：架构版本、源元数据、确切时间窗口、
标准化蜡烛行、标准化资金行、汇总统计数据。使用
`--end-time-ms` 用于可重现的窗口。

---

## 陷阱

- 公共信息端点受到速率限制。大量的历史查询可能会
  返回有上限的窗口；使用稍后的“startTime”值进行迭代。
- `fills --hours ...` 使用 `userFillsByTime`，它只公开
  最近的滚动窗口 - 不是完整的存档历史记录。
- `historicalOrders` 仅返回最近的订单；不是完全导出。
- “review”命令是启发式的。它无法重建意图，
  下单质量，或仅执行订单时的真实滑点。
- “export”命令写入标准化数据集，而不是回测
  发动机。您仍然需要自己的滑点/填充模型。
- 即使 UI 显示，像“@107”这样的现货别名也是有效的标识符
  一个更友好的名字。
- `l2` ​​是时间点快照，而不是时间序列。

---

## 验证

````bash
python3 ~/.hermes/skills/blockchain/hyperliquid/scripts/hyperliquid_client.py \
  市场--限制 5
````

应按 24 小时名义交易量打印顶级 Hyperliquid 永久市场。