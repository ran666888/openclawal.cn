---
title: "Here.Now — Publish static sites to {slug}"
sidebar_label: "Here.Now"
description: "Publish static sites to {slug}"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 此时此地

将静态站点发布到 {slug}.here.now 并将私有文件存储在云硬盘中，以便代理之间的切换。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/productivity/here-now` 安装 |
|路径| `可选技能/生产力/此时此刻` |
|版本 | `1.15.3` |
|作者 |现在就在这里 |
|许可证|麻省理工学院 |
|平台| macOS、Linux |
|标签 | `here.now`、`herenow`、`publish`、`deploy`、`hosting`、`static-site`、`web`、`share`、`URL`、`drive`、`storage` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 此处.现在

here.now 允许代理发布网站并将私人文件存储在云驱动器中。

使用here.now 进行两项工作：

- **站点**：在“{slug}.here.now”发布网站和文件。
- **驱动器**：将私人代理文件存储在云文件夹中。

## 当前文档

**在回答有关 here.now 功能、特性或工作流程的问题之前，请阅读当前文档：**

→ **https://here.now/docs**

阅读文档：

- 对话中第一次与here.now相关的互动
- 任何时候用户询问如何做某事
- 任何时候用户询问什么是可能的、支持的或推荐的
- 在告诉用户某个功能不受支持之前

需要当前文档的主题（不要仅依赖本地技能文本）：

- 驱动器和驱动器共享
- 自定义域
- 付款和付款门控
- 分叉
- 代理路由和服务变量
- 手柄和链接
- 限制和配额
- SPA路由
- 错误处理和修复
- 功能可用性

**如果文档和实时 API 行为不一致，请相信实时 API 行为。**

如果文档获取失败或超时，请继续使用本地技能和实时 API/脚本输出。更喜欢主动操作的实时 API 行为。

## 要求

- 所需的二进制文件：`curl`、`file`、`jq`
- 可选环境变量：`$HERENOW_API_KEY`
- 可选的驱动器令牌变量：`$HERENOW_DRIVE_TOKEN`
- 可选凭证文件：`~/.herenow/credentials`
- 技能助手路径：
  - 用于发布网站的“${HERMES_SKILL_DIR}/scripts/publish.sh”
  - `${HERMES_SKILL_DIR}/scripts/drive.sh` 用于私人云端硬盘存储

## 创建站点

````bash
PUBLISH="${HERMES_SKILL_DIR}/scripts/publish.sh"
bash "$PUBLISH" {文件或目录} --client Hermes
````

输出实时 URL（例如“https://bright-canvas-a7k2.here.now/”）。

在底层，这是一个三步流程：创建/更新 -> 上传文件 -> 完成。在最终确定成功之前，站点不会上线。

如果没有 API 密钥，这将创建一个**匿名站点**，该站点将在 24 小时内过期。
通过保存的 API 密钥，该站点是永久性的。

**文件结构：** 对于 HTML 站点，请将 `index.html` 放置在您发布的目录的根目录中，而不是放在子目录中。该目录的内容成为站点根目录。例如，发布存在“my-site/index.html”的“my-site/”——不要发布包含“my-site/”的父文件夹。

您还可以发布不带任何 HTML 的原始文件。单个文件可以获得丰富的自动查看器（图像、PDF、视频、音频）。多个文件会获得自动生成的目录列表，其中包含文件夹导航和图像库。

## 更新现有站点

````bash
PUBLISH="${HERMES_SKILL_DIR}/scripts/publish.sh"
bash "$PUBLISH" {文件或目录} --slug {slug} --client Hermes
````

更新匿名网站时，脚本会自动从“.herenow/state.json”加载“claimToken”。传递 `--claim-token {token}` 进行覆盖。

经过身份验证的更新需要保存的 API 密钥。

## 使用驱动器

当用户需要私有云存储代理文件时，请使用云端硬盘：文档、上下文、内存、计划、资产、媒体、研究、代码以及任何其他应保留但不发布为网站的内容。

每个登录帐户都有一个名为“我的云端硬盘”的默认云端硬盘。

````bash
DRIVE="${HERMES_SKILL_DIR}/scripts/drive.sh"
bash“$DRIVE”默认值
bash“$DRIVE”ls“我的驱动器”
bash "$DRIVE" put "我的驱动器" Notes/today.md --from ./notes/today.md
bash“$DRIVE”猫“我的驱动器”notes/today.md
bash“$DRIVE”共享“我的驱动器”--perms write --prefix Notes/ --ttl 7d
````

使用范围内的 Drive 令牌进行代理之间的切换。如果您收到“herenow_drive”共享块，请使用其“令牌”作为针对“api_base”的“授权：持有者 <token>”，尊重“pathPrefix”（如果存在），并在写入时保留 ETag。 “pathPrefix”为“null”表示完全驱动器访问。如果技能可用，优先选择“drive.sh”；否则直接调用列出的API操作。

## API 密钥存储

发布脚本从这些来源读取 API 密钥（第一个匹配获胜）：

1. `--api-key {key}` 标志（仅限 CI/脚本 — 避免交互使用）
2.`$HERENOW_API_KEY`环境变量
3. `~/.herenow/credentials` 文件（推荐给代理）

要存储密钥，请将其写入凭据文件：

````bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
````

**重要**：收到 API 密钥后，请立即保存 - 自行运行上面的命令。不要要求用户手动运行它。避免在交互式会话中通过 CLI 标志（例如 `--api-key`）传递密钥；凭据文件是首选存储方法。

切勿将凭据或本地状态文件（`~/.herenow/credentials`、`.herenow/state.json`）提交到源代码管理。

## 获取 API 密钥

要从匿名（24 小时）站点升级到永久站点：

1. 询问用户的电子邮件地址。
2. 请求一次性登录代码：

````bash
卷曲-sS https://here.now/api/auth/agent/request-code \
  -H“内容类型：应用程序/json”\
  -d '{"email": "user@example.com"}'
````

3. 告诉用户：“立即检查您的收件箱中是否有来自此处的登录代码，并将其粘贴到此处。”
4. 验证代码并获取API密钥：

````bash
卷曲-sS https://here.now/api/auth/agent/verify-code \
  -H“内容类型：应用程序/json”\
  -d '{"email":"user@example.com","code":"ABCD-2345"}'
````

5. 自己保存返回的`apiKey`（不要要求用户这样做）：

````bash
mkdir -p ~/.herenow && echo "{API_KEY}" > ~/.herenow/credentials && chmod 600 ~/.herenow/credentials
````

## 状态文件

每次站点创建/更新后，脚本都会写入工作目录中的“.herenow/state.json”：

```json
{
  “发布”：{
    “明亮的画布-a7k2”：{
      "siteUrl": "https://bright-canvas-a7k2.here.now/",
      “claimToken”：“abc123”，
      "claimUrl": "https://here.now/claim?slug=bright-canvas-a7k2&token=abc123",
      “到期时间”：“2026-02-18T01：00：00.000Z”
    }
  }
}
````

在创建或更新站点之前，您可以检查此文件以查找以前的 slugs。
仅将 `.herenow/state.json` 视为内部缓存。
切勿将此本地文件路径显示为 URL，也切勿将其用作身份验证模式、到期或声明 URL 的真实来源。

## 告诉用户什么

对于已发布的网站：

- 始终共享当前脚本运行中的“siteUrl”。
- 阅读并遵循脚本 stderr 中的“publish_result.*”行以确定身份验证模式。
- 当“publish_result.auth_mode=authenticated”时：告诉用户该网站是**永久**并保存到他们的帐户中。不需要声明 URL。
- 当 `publish_result.auth_mode=anonymous` 时：告诉用户该网站 **24 小时后过期**。共享声明 URL（如果“publish_result.claim_url”非空且以“https://”开头），以便他们可以永久保留它。警告声明令牌仅返回一次且无法恢复。
- 切勿告诉用户检查“.herenow/state.json”以获取声明 URL 或身份验证状态。

对于驱动器：

- 请勿将云端硬盘文件描述为公共 URL。
- 告诉用户云端硬盘内容是私有的，除非与范围令牌共享。
- 与其他代理共享访问权限时，首选具有狭窄“pathPrefix”和短 TTL 的范围令牌。

##publish.sh 选项

|旗帜|描述 |
| ---------------------- | -------------------------------------------------------- |
| `--slug {slug}` |更新现有网站而不是创建 |
| `--claim-token {令牌}`|覆盖匿名更新的声明令牌 |
| `--标题 {文本}` |查看者标题（非 HTML 网站）|
| `--描述{文本}` |观众描述 |
| `--ttl {秒}` |设置过期时间（仅经过身份验证）|
| `--客户端 {名称}` |归因代理名称（例如“hermes”）|
| `--base-url {url}` | API 基本 URL（默认：`https://here.now`）|
| `--allow-nonherenow-base-url` |允许将身份验证发送到非默认 `--base-url` |
| `--api-key {key}` | API 密钥覆盖（首选凭据文件）|
| `--spa` |启用 SPA 路由（为未知路径提供 index.html）|
| `--forkable` |允许其他人分叉此网站 |

## 除了publish.sh

对于云端硬盘操作，请使用“drive.sh”或云端硬盘 API。对于更广泛的帐户和站点管理 - 删除、元数据、密码、付款、域、句柄、链接、变量、代理路由、分叉、复制等 - 请参阅当前文档：

→ **https://here.now/docs**

完整文档：https://here.now/docs