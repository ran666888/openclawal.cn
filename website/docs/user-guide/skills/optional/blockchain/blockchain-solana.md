---
title: "Solana"
sidebar_label: "Solana"
description: "Query Solana blockchain data with USD pricing — wallet balances, token portfolios with values, transaction details, NFTs, whale detection, and live network s..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 索拉纳

使用美元定价查询 Solana 区块链数据 — 钱包余额、具有价值的代币投资组合、交易详细信息、NFT、鲸鱼检测和实时网络统计数据。使用 Solana RPC + CoinGecko。无需 API 密钥。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/blockchain/solana` 安装 |
|路径| `可选技能/区块链/solana` |
|版本 | `0.2.0` |
|作者 | Deniz Alagoz (gizdusum)，由 OpenClaw 增强 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `Solana`、`区块链`、`加密`、`Web3`、`RPC`、`DeFi`、`NFT` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Solana 区块链技能

通过 CoinGecko 查询包含美元定价的 Solana 链上数据。
8 个命令：钱包投资组合、代币信息、交易、活动、NFT、
鲸鱼检测、网络统计和价格查找。

无需 API 密钥。仅使用 Python 标准库（urllib、json、argparse）。

---

## 何时使用

- 用户询问 Solana 钱包余额、代币持有量或投资组合价值
- 用户想要通过签名检查特定交易
- 用户想要 SPL 代币元数据、价格、供应量或顶级持有者
- 用户想要某个地址的最近交易历史记录
- 用户希望钱包拥有 NFT
- 用户想要找到大型 SOL 传输（鲸鱼检测）
- 用户想要 Solana 网络运行状况、TPS、纪元或 SOL 价格
- 用户询问“BONK/JUP/SOL 的价格是多少？”

---

## 先决条件

帮助程序脚本仅使用 Python 标准库（urllib、json、argparse）。
不需要外部包。

定价数据来自CoinGecko的免费API（无需密钥，有速率限制）
约 10-30 个请求/分钟）。为了更快地查找，请使用“--no-prices”标志。

---

## 快速参考

RPC 端点（默认）：https://api.mainnet-beta.solana.com
覆盖：导出 SOLANA_RPC_URL=https://your-private-rpc.com

帮助程序脚本路径：~/.hermes/skills/blockchain/solana/scripts/solana_client.py

````
python3 solana_client.py wallet <地址> [--limit N] [--all] [--no-prices]
python3 solana_client.py tx <签名>
python3 solana_client.py 令牌 <mint_address>
python3 solana_client.py 活动 <地址> [--limit N]
python3 solana_client.py nft <地址>
python3 solana_client.py 鲸鱼 [--min-sol N]
python3 solana_client.py 统计信息
python3 solana_client.py 价格 <mint_or_symbol>
````

---

## 程序

### 0. 设置检查

````bash
python3——版本

# 可选：设置私有 RPC 以获得更好的速率限制
导出 SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"

# 确认连接
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py stats
````

### 1. 钱包组合

获取 SOL 余额、SPL 代币持有量（美元价值）、NFT 数量以及
投资组合总计。按价值排序、过滤灰尘、已知令牌的令牌
按名称标记（BONK、JUP、USDC 等）。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \
  钱包 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM
````

标志：
- `--limit N` — 显示前 N 个令牌（默认值：20）
- `--all` — 显示所有令牌，无灰尘过滤器，无限制
- `--no-prices` — 跳过 CoinGecko 价格查找（更快，仅限 RPC）

输出包括：SOL 余额 + 美元价值、已排序的代币列表
按价值、灰尘数量、NFT 摘要、以美元计的投资组合总价值。

### 2. 交易详情

通过其 base58 签名检查完整交易。显示余额变化
以 SOL 和 USD 表示。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \
  tx 5j7s8K...your_signature_here
````

输出：槽位、时间戳、费用、状态、余额变化（SOL + USD）、
程序调用。

### 3. 代币信息

获取 SPL 代币元数据、当前价格、市值、供应量、小数位、
铸币/冻结机构，以及前 5 名持有者。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \
  代币 DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
````

输出：名称、符号、小数、供应量、价格、市值、前 5 名
持有者的百分比。

### 4.近期活动

列出地址的最近交易（默认：最后 10 笔，最多：25 笔）。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \
  活动 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM --限制 25
````

### 5. NFT 组合

列出钱包拥有的 NFT（启发式：SPL 代币，金额 = 1，小数 = 0）。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \
  NFT 9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM
````

注意：此启发式无法检测压缩 NFT (cNFT)。

### 6.鲸鱼探测器

扫描最近的区块以查找具有美元价值的大型 SOL 传输。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py \
  鲸鱼 --min-sol 500
````

注意：仅扫描最新的块——时间点快照，而不是历史的。

### 7. 网络统计

实时 Solana 网络运行状况：当前槽、纪元、TPS、供应、验证器
版本、SOL 价格和市值。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py stats
````

### 8. 价格查询

通过铸币地址或已知符号快速检查任何代币的价格。

````bash
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py 价格 BONK
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py 价格 JUP
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py 价格 SOL
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py 价格 DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263
````

已知符号：SOL、USDC、USDT、BONK、JUP、WETH、JTO、mSOL、stSOL、
PYTH、HNT、RNDR、WEN、W、TNSR、DRIFT、bSOL、JLP、WIF、MEW、BOME、PENGU。

---

## 陷阱

- **CoinGecko 速率限制** — 免费套餐允许约 10-30 个请求/分钟。
  价格查找每个代币使用 1 个请求。拥有许多代币的钱包可能会
  无法获得所有产品的价格。使用“--no-prices”来提高速度。
- **公共 RPC 速率限制** — Solana 主网公共 RPC 限制请求。
  对于生产使用，请将 SOLANA_RPC_URL 设置为专用端点
  （Helius、QuickNode、Triton）。
- **NFT 检测是启发式的** — 金额 = 1 + 小数 = 0。压缩的
  NFT (cNFT) 和 Token-2022 NFT 将不会出现。
- **鲸鱼探测器仅扫描最新区块** - 不是历史区块。结果
  根据您查询的时刻而变化。
- **交易历史记录** — 公共 RPC 保留约 2 天。较旧的交易
  可能不可用。
- **代币名称** — 约 25 个知名代币按名称进行标记。其他
  显示缩写的铸币厂地址。使用“token”命令获取完整信息。
- **重试 429** — RPC 和 CoinGecko 调用最多重试 2 次
  对速率限制错误进行指数退避。

---

## 验证

````bash
# 应该打印当前的 Solana 插槽、TPS 和 SOL 价格
python3 ~/.hermes/skills/blockchain/solana/scripts/solana_client.py stats
````