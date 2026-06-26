---
title: "Sherlock — OSINT username search across 400+ social networks"
sidebar_label: "Sherlock"
description: "OSINT username search across 400+ social networks"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 夏洛克

OSINT 用户名在 400 多个社交网络中搜索。通过用户名搜索社交媒体帐户。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/security/sherlock` 安装 |
|路径| `可选技能/安全/夏洛克` |
|版本 | `1.0.0` |
|作者 |未建模的泰勒 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `osint`、`安全`、`用户名`、`社交媒体`、`侦察` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Sherlock OSINT 用户名搜索

使用 [Sherlock 项目](https://github.com/sherlock-project/sherlock) 在 400 多个社交网络中按用户名搜索社交媒体帐户。

## 何时使用

- 用户要求查找与用户名关联的帐户
- 用户想要检查跨平台的用户名可用性
- 用户正在进行 OSINT 或侦察研究
- 用户询问“这个用户名是在哪里注册的？”或类似的

## 要求

- 安装 Sherlock CLI：`pipx install sherlock-project` 或 `pip install sherlock-project`
- 或者：可用 Docker (`docker run -it --rm sherlock/sherlock`)
- 网络接入查询社交平台

## 程序

### 1. 检查是否安装了 Sherlock

**在执行其他操作之前**，验证 sherlock 是否可用：

````bash
神探夏洛克——版本
````

如果命令失败：
- 提供安装：“pipx install sherlock-project”（推荐）或“pip install sherlock-project”
- **不要**尝试多种安装方法 - 选择一种并继续
- 如果安装失败，通知用户并停止

### 2.提取用户名

**如果明确说明，直接从用户消息中提取用户名。**

您**不**使用的示例需要澄清：
- “查找 nasa 帐户”→ 用户名是 `nasa`
- “搜索 johndoe123” → 用户名是 `johndoe123`
- “检查社交媒体上是否存在爱丽丝” → 用户名是 `alice`
- “在社交网络上查找用户 bob” → 用户名是 `bob`

**仅在以下情况下使用澄清：**
- 提及多个潜在用户名（“搜索 alice 或 bob”）
- 措辞不明确（“搜索我的用户名”但未指定）
- 根本没有提及用户名（“进行 OSINT 搜索”）

提取时，采用所述的**准确**用户名 - 保留大小写、数字、下划线等。

### 3.构建命令

**默认命令**（除非用户特别要求，否则使用此命令）：
````bash
sherlock --print-found --no-color "<用户名>" --超时 90
````

**可选标志**（仅在用户明确请求时添加）：
- `--nsfw` — 包括 NSFW 站点（仅当用户询问时）
- `--tor` — 通过 Tor 的路由（仅当用户要求匿名时）

**不要通过澄清询问选项** - 只需运行默认搜索。如果需要，用户可以请求特定选项。

### 4. 执行搜索

通过“终端”工具运行。该命令通常需要 30-120 秒，具体取决于网络条件和站点数量。

**终端调用示例：**
```json
{
  "command": "sherlock --print-found --no-color \"target_username\"",
  “超时”：180
}
````

### 5. 解析并呈现结果

Sherlock 以简单的格式输出找到的帐户。解析输出并呈现：

1. **摘要行：**“找到用户名‘Y’的 X 个帐户”
2. **分类链接：** 如果有帮助的话，按平台类型分组（社交、专业、论坛等）
3. **输出文件位置：** Sherlock 默认将结果保存到 `<username>.txt`

**输出解析示例：**
````
[+] Instagram：https://instagram.com/username
[+] 推特：https://twitter.com/username
[+] GitHub：https://github.com/username
````

尽可能将发现结果呈现为可点击的链接。

## 陷阱

### 未找到结果
如果 Sherlock 找不到帐户，这通常是正确的 - 用户名可能未在检查的平台上注册。建议：
- 检查拼写/变体
- 尝试使用“?”通配符类似的用户名：“sherlock“user?name””
- 用户可能有隐私设置或删除帐户

### 超时问题
有些网站速度缓慢或阻止自动请求。使用“--timeout 120”来增加等待时间，或使用“--site”来限制范围。

### Tor 配置
`--tor` 需要 Tor 守护进程运行。如果用户想要匿名但 Tor 不可用，建议：
- 安装 Tor 服务
- 将“--proxy”与替代代理一起使用

### 误报
由于其响应结构，某些网站总是返回“找到”。通过手动检查交叉引用意外结果。

### 速率限制
激进的搜索可能会触发速率限制。对于批量用户名搜索，请在调用之间添加延迟或使用带有缓存数据的“--local”。

## 安装

### pipx（推荐）
````bash
pipx 安装 sherlock 项目
````

### 点
````bash
pip 安装 sherlock 项目
````

### 码头工人
````bash
码头工人拉夏洛克/夏洛克
docker run -it --rm sherlock/sherlock <用户名>
````

### Linux 软件包
适用于 Debian 13+、Ubuntu 22.10+、Homebrew、Kali、BlackArch。

## 道德使用

该工具仅用于合法的 OSINT 和研究目的。提醒用户：
- 仅搜索他们拥有或有权调查的用户名
- 尊重平台服务条款
- 请勿用于骚扰、跟踪或非法活动
- 在分享结果之前考虑隐私影响

## 验证

运行 sherlock 后，验证：
1. 输出列出找到的带有 URL 的站点
2. 如果使用文件输出，则创建“<用户名>.txt”文件（默认输出）
3. 如果使用`--print-found`，输出应该只包含`[+]`匹配行

## 交互示例

**用户：**“您能检查一下社交媒体上是否存在用户名‘johndoe123’吗？”

**代理程序：**
1. 检查 `sherlock --version` （验证已安装）
2. 提供用户名 — 直接继续
3. 运行： `sherlock --print-found --no-color "johndoe123" --timeout 90`
4. 解析输出并呈现链接

**回复格式：**
> 找到用户名“johndoe123”的 12 个帐户：
>
> • https://twitter.com/johndoe123
> • https://github.com/johndoe123
> • https://instagram.com/johndoe123
> • [...附加链接]
>
> 结果保存到：johndoe123.txt

---

**用户：**“搜索用户名‘alice’，包括 NSFW 网站”

**代理程序：**
1.检查sherlock是否安装
2. 提供用户名 + NSFW 标志
3. 运行： `sherlock --print-found --no-color --nsfw "alice" --timeout 90`
4. 呈现结果