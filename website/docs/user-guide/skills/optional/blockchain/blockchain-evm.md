---
title: "Evm — Read-only EVM client: wallets, tokens, gas across 8 chains"
sidebar_label: "Evm"
description: "Read-only EVM client: wallets, tokens, gas across 8 chains"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 评估值

只读 EVM 客户端：跨 8 个链的钱包、代币、gas。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/blockchain/evm` 安装 |
|路径| `可选技能/区块链/evm` |
|版本 | `1.0.0` |
|作者 | Mibayy (@Mibayy)、youssefea (@youssefea)、ethernet8023 (@ethernet8023)、OpenClaw 代理 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `EVM`、`以太坊`、`BNB`、`BSC`、`Base`、`Arbitrum`、`Polygon`、`Optimism`、`Avalanche`、`zkSync`、`区块链`、`Crypto`、`Web3`、`DeFi`、`NFT`、`ENS`、`Whale`、`Security` |
|相关技能| [`solana`](/docs/用户指南/技能/可选/区块链/区块链-solana) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# EVM 区块链技能

以美元定价跨 8 个链查询 EVM 兼容的区块链数据。
14 个命令：钱包投资组合、代币信息、交易、活动、gas 跟踪器、
网络统计、价格查找、多链扫描、鲸鱼检测、ENS 分辨率、
津贴检查员、合同检查员和交易解码器。

支持8条链：以太坊、BNB Chain (BSC)、Base、Arbitrum One、Polygon、
乐观、Avalanche（C链）、zkSync时代。

无需 API 密钥。零外部依赖——仅限 Python 标准库
（urllib、json、argparse、线程）。

> **取代独立的“基础”技能。** 基础特定标记（AERO、DEGEN、
> TOSHI、BRETT、WELL、cbETH、cbBTC、wstETH、rETH）和所有基本 RPC 功能
> 之前位于 `Optional-skills/blockchain/base/` 下的内容已被折叠
> 进入这个技能。将 `--chain base` 传递给任何命令以实现 Base 覆盖。

---

## 何时使用
- 用户请求任何 EVM 链上的钱包余额或投资组合
- 用户想要同时检查所有链上的同一个钱包
- 用户想要通过哈希检查交易（或解码它做了什么）
- 用户想要 ERC-20 代币元数据、价格、供应量或市值
- 用户想要某个地址的最近交易历史记录
- 用户想要当前的天然气价格或比较跨链的费用
- 用户希望在最近的区块中找到大型鲸鱼转移
- 用户请求解析 ENS 名称 (vitalik.eth) 或反向查找地址
- 用户想要检查合约是否有危险的代币批准
- 用户想要检查智能合约（代理？ERC-20？ERC-721？字节码大小？）
- 用户希望在交易前比较跨链的 Gas 成本

---

## 先决条件
仅限 Python 3.8+ 标准库。无需安装 pip。
定价：CoinGecko 免费 API（速率有限，约 10-30 请求/分钟）。
ENS：ensideas.com 公共 API。
Tx解码：4byte.directory公共API。

覆盖 RPC 端点：`export EVM_RPC_URL=https://your-rpc.com`

帮助程序脚本路径：`~/.hermes/skills/blockchain/evm/scripts/evm_client.py`

---

## 快速参考

````
SCRIPT=~/.hermes/skills/blockchain/evm/scripts/evm_client.py

# 网络和价格
python3 $SCRIPT stats # 以太坊统计
python3 $SCRIPT stats --chain arbitrum # 仲裁统计
python3 $SCRIPT 比较 # Gas + 价格 全部 8 个链

# 钱包
python3 $SCRIPT 钱包 0xd8dA...96045 # 投资组合 (ETH + ERC-20)
python3 $SCRIPT 钱包 0xd8dA...96045 --chain bsc
python3 $SCRIPT multichain 0xd8dA...96045 # 所有链上的相同钱包

# 代币和价格
python3 $SCRIPT 价格 ETH
python3 $SCRIPT 价格 0xdAC1...1ec7 # 按合约地址
python3 $SCRIPT 代币 0xdAC1...1ec7 # ERC-20 元数据 + 市值

# 交易
python3 $SCRIPT tx 0x5c50...f060 # 交易详情
python3 $SCRIPT 解码 0x5c50...f060 # 解码输入数据（4byte.directory）
python3 $SCRIPT 活动 0xd8dA...96045 # 最近交易

# 气体
python3 $SCRIPT Gas # Gas 价格 + 成本估算
python3 $SCRIPT Gas --链乐观

# 安全
python3 $SCRIPT 津贴 0xd8dA...96045 # 危险的 ERC-20 批准
python3 $SCRIPT Contract 0xdAC1...1ec7 # 合约检查（代理？标准？）

# ENS
python3 $SCRIPT ensvitalik.eth # 名称 -> 地址 + 个人资料
python3 $SCRIPT ens 0xd8dA...96045 # 地址 -> ENS 名称

# 鲸鱼检测
python3 $SCRIPT Whale # 大额转账（最后 20 个区块，>$10k）
python3 $SCRIPT鲸鱼 --blocks 50 --min-usd 100000 --chain arbitrum
````

---

## 程序

### 0. 设置检查
````bash
python3 --version # 需要 3.8+
python3 ~/.hermes/skills/blockchain/evm/scripts/evm_client.py stats
````

### 1. 钱包组合
原生余额 + 已知的 ERC-20 代币，按美元价值排序。
````bash
python3 $SCRIPT钱包0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
python3 $SCRIPT 钱包 0xd8dA... --chain bsc --no-prices # 更快
````

### 2.多链扫描
使用线程同时扫描所有 8 个链以查找同一地址。
````bash
python3 $SCRIPT 多链 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
````
输出：每链原生余额 + 代币持有量 + 美元总额。

### 3.比较（Gas + 价格）
所有 8 个链均并行查询。显示最便宜/最昂贵的连锁店。
````bash
python3 $SCRIPT 比较
````

### 4. 交易详情及解码
````bash
python3 $SCRIPT tx 0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060
python3 $SCRIPT解码0x5c504ed... # 显示人类可读的函数签名
````
解码使用 4byte.directory 来翻译 0xa9059cbb -> Transfer(address,uint256)。

### 5.ENS 分辨率
````bash
python3 $SCRIPT ens importantik.eth # -> 0xd8dA... + 头像 + 社交链接
python3 $SCRIPT ens 0xd8dA...96045 # -> vitalik.eth
````

### 6. 津贴检查器（安全）
检查授予已知 DEX/桥合约的 ERC-20 批准。
````bash
python3 $SCRIPT 津贴 0xYourWallet
````
将无限批准标记为高风险。

### 7. 合同检验员
````bash
python3 $SCRIPT 合约 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 # USDC（代理）
python3 $SCRIPT 合约 0xdAC17F958D2ee523a2206206994597C13D831ec7 # USDT (ERC-20)
````
检测：代理 (EIP-1967/EIP-1167)、ERC-20、ERC-721、ERC-165。显示代理的字节码大小和实现地址。

### 8.鲸鱼检测
````bash
python3 $SCRIPT 鲸鱼 # ETH，最后 20 个区块，>$10k
python3 $SCRIPT鲸鱼 --blocks 50 --min-usd 50000 --chain bsc
````

### 9. 气体追踪器
````bash
python3 $SCRIPT 气体
python3 $SCRIPT Gas --链多边形
````
显示 gwei 价格 + 美元成本：转账、ERC-20 转账、批准、互换、NFT 铸币、NFT 转账。

---

## 支持的链
|关键|名称 |本地 |链ID |
|------------|----------------|--------|----------|
|以太坊 |以太坊 |以太币 | 1 |
|理学学士 | BNB链|币安币 | 56 | 56
|基地|基地|以太币 | 8453 |
|任意 |仲裁一号 |以太币 | 42161 | 42161
|多边形|多边形|波兰 | 137 | 137
|乐观|乐观|以太币 | 10 | 10
|雪崩|雪崩C | AVAX | 43114 |
|中科同步 | zkSync时代|以太币 | 324 | 324

---

## 陷阱
- CoinGecko 免费套餐：~10-30 请求/分钟。使用“--no-prices”可以更快地扫描钱包。
- 公共 RPC 可能会受到限制。将 EVM_RPC_URL 设置为生产专用端点。
- `wallet` 和 `allowance` 仅检查已知代币列表（每个链约 30 个代币）。使用区块浏览器进行完整的代币发现。
- “活动”仅扫描最近的区块（最多 200 个）。如需完整历史记录，请使用 Etherscan API。
- `multichain` 运行 8 个并行线程 — 可以触发公共 RPC 的速率限制。
- ENS 解析取决于单个公共端点 (ensideas.com / ens.vitalik.ca)，没有后备。如果该端点关闭，“ens”将失败 - 稍后重新运行或使用块浏览器。
- Tx 解码取决于单个公共端点（4byte.directory），没有后备。不在数据库中的选择器显示为“未知”。
- **L2 Gas 估算仅适用于 L2 执行。** 在 Base、Arbitrum、Optimism 和 zkSync 等汇总中，实际交易成本还包括 L1 数据发布费用，该费用取决于调用数据大小和当前的 L1 Gas 价格。 `gas` 命令不会估计 L1 组件。具体对于 Base，请参阅网络的 L1 费用预言机（合约 `0x420000000000000000000000000000000000000F`）。
- 地址/tx 哈希输入针对 0x 前缀 + 正确长度 + 十六进制进行验证，但 **不** 强制执行 EIP-55 校验和大小写（RPC 端点接受任何大小写的十六进制）。

---

## 验证
````bash
# 应该打印当前区块、gas 价格、ETH 价格
python3 ~/.hermes/skills/blockchain/evm/scripts/evm_client.py stats

# 应该将vitalik.eth解析为0xd8dA...
python3 ~/.hermes/skills/blockchain/evm/scripts/evm_client.py ens fatalik.eth
````