---
title: "Domain Intel — Passive domain reconnaissance using Python stdlib"
sidebar_label: "Domain Intel"
description: "Passive domain reconnaissance using Python stdlib"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 域英特尔

使用 Python stdlib 进行被动域侦察。子域发现、SSL 证书检查、WHOIS 查找、DNS 记录、域可用性检查和批量多域分析。无需 API 密钥。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/domain-intel` 安装 |
|路径| `可选技能/研究/领域英特尔` |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 领域情报——被动 OSINT

仅使用 Python stdlib 进行被动域侦察。
**零依赖性。零 API 密钥。适用于 Linux、macOS 和 Windows。**

## 帮助脚本

该技能包括“scripts/domain_intel.py”——一个用于所有域智能操作的完整 CLI 工具。

````bash
# 通过证书透明度日志发现子域
python3 SKILL_DIR/scripts/domain_intel.py 子域 example.com

# SSL 证书检查（过期、密码、SAN、颁发者）
python3 SKILL_DIR/scripts/domain_intel.py ssl example.com

# WHOIS 查找（注册商、日期、名称服务器 — 100 多个 TLD）
python3 SKILL_DIR/scripts/domain_intel.py whois example.com

# DNS 记录（A、AAAA、MX、NS、TXT、CNAME）
python3 SKILL_DIR/scripts/domain_intel.py dns example.com

# 域名可用性检查（被动：DNS + WHOIS + SSL 信号）
python3 SKILL_DIR/scripts/domain_intel.py 可用coolstartup.io

# 批量分析——多个域，并行多次检查
python3 SKILL_DIR/scripts/domain_intel.py 批量 example.com github.com google.com
python3 SKILL_DIR/scripts/domain_intel.py 批量 example.com github.com --检查 ssl、dns
````

`SKILL_DIR` 是包含此 SKILL.md 文件的目录。所有输出都是结构化 JSON。

## 可用命令

|命令|它有什么作用 |数据来源|
|---------|-------------|----------|
| `子域` |从证书日志中查找子域 | crt.sh (HTTPS) |
| `ssl` |检查 TLS 证书详细信息 |直接 TCP:443 到目标 |
| `谁是` |注册信息、注册商、日期 | WHOIS 服务器 (TCP:43) |
| `dns` | A、AAAA、MX、NS、TXT、CNAME 记录 |系统 DNS + Google DoH |
| `可用` |检查域名是否已注册 | DNS + WHOIS + SSL 信号 |
| `散装` |对多个域运行多项检查 |以上全部|

## 何时使用此工具与内置工具

- **使用此技能**解决基础设施问题：子域、SSL 证书、WHOIS、DNS 记录、可用性
- **使用“web_search”**进行有关域/公司业务的一般研究
- **使用`web_extract`**获取网页的实际内容
- **使用 `terminal` 和 `curl -I`** 进行简单的“此 URL 是否可访问”检查

|任务|更好的工具|为什么 |
|------|-------------|-----|
| “example.com 是做什么的？” | `web_extract` |获取页面内容，而不是 DNS/WHOIS 数据 |
| “查找有关公司的信息”| `网络搜索` |一般性研究，而非特定领域 |
| “这个网站安全吗？” | `网络搜索` |声誉检查需要网络环境|
| “检查 URL 是否可访问” | `terminal` 与 `curl -I` |简单的 HTTP 检查 |
| “查找 X 的子域”| **这个技能** |唯一的被动来源 |
| “SSL 证书什么时候过期？” | **这个技能** |内置工具无法检查 TLS |
| “这个域名是谁注册的？” | **这个技能** | WHOIS 数据不在网络搜索中 |
| “coolstartup.io 可用吗？” | **这个技能** |通过 DNS+WHOIS+SSL 实现被动可用性 |

## 平台兼容性

纯Python stdlib（`socket`、`ssl`、`urllib`、`json`、`concurrent.futures`）。
在 Linux、macOS 和 Windows 上的工作方式相同，没有依赖性。

- **crt.sh 查询** 使用 HTTPS（端口 443）——在大多数防火墙后面工作
- **WHOIS 查询** 使用 TCP 端口 43 — 可能在限制性网络上被阻止
- **DNS 查询** 使用 Google DoH (HTTPS) 进行 MX/NS/TXT — 防火墙友好
- **SSL 检查** 连接到端口 443 上的目标 — 唯一的“活动”操作

## 数据来源

所有查询都是**被动**——没有端口扫描，没有漏洞测试：

- **crt.sh** — 证书透明度日志（子域发现，仅限 HTTPS）
- **WHOIS 服务器** — 直接 TCP 至 100 多个权威 TLD 注册商
- **Google DNS-over-HTTPS** — MX、NS、TXT、CNAME 解析（防火墙友好）
- **系统 DNS** — A/AAAA 记录解析
- **SSL 检查** 是唯一的“活动”操作（到目标的 TCP 连接：443）

## 注释

- WHOIS 查询使用 TCP 端口 43 — 可能在限制性网络上被阻止
- 一些 WHOIS 服务器会编辑注册人信息 (GDPR) — 向用户提及这一点
- 对于非常受欢迎的域（数千个证书），crt.sh 可能会很慢 - 设定合理的期望
- 可用性检查是基于启发式的（3 个被动信号）——不像注册商 API 那样具有权威性

---

*由 [@FurkanL0](https://github.com/FurkanL0) 贡献*