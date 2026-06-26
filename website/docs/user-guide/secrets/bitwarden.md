# Bitwarden 秘密管理器

在进程启动时从 [Bitwarden Secrets Manager](https://bitwarden.com/products/secrets-manager/) 提取 API 密钥，而不是将它们以明文形式存储在 `~/.hermes/.env` 中。一个引导密钥（机器帐户访问令牌）取代了 N 个每个提供商密钥，并且轮换凭证成为 Bitwarden Web 应用程序中的一项更改。

## 它是如何工作的

1. 您在 Bitwarden Secrets Manager 中创建一个 **机器帐户**，为其授予对项目的读取权限，并生成 **访问令牌**。
2. OpenClaw 将该单个令牌存储在 `~/.hermes/.env` 中作为 `BWS_ACCESS_TOKEN`。
3. 每次 `hermes`（或网关，或 cron 作业）启动时，加载 `~/.hermes/.env` 后，OpenClaw 调用 `bws 秘密列表 <project_id>` 并将返回的密钥设置到 `os.environ` 中。
4. 默认情况下，OpenClaw **覆盖**环境中已有的值，因此 Bitwarden 是事实来源 - 在 Web 应用程序中旋转一次密钥，每个 OpenClaw 进程都会在下次启动时拾取它。如果您希望“.env”获胜，请在配置中翻转“override_existing: false”。

首次使用时，“bws”二进制文件会自动下载到“~/.hermes/bin/”中——没有“apt”，没有“brew”，没有“sudo”。

## 为什么是机器帐户（以及为什么没有 2FA 提示）

Bitwarden Secrets Manager 专为非交互式工作负载而设计：机器帐户无法进行 2FA 门控，因为循环中没有人。访问令牌就是凭证。拥有它的任何人都可以读取机器帐户有权访问的每个秘密，因此请将其视为高价值的不记名令牌 - 将其存储在“.env”（而不是“config.yaml”）中，并在泄漏时从 Bitwarden Web 应用程序中撤销和重新生成。

您*在网络应用程序*中设置计算机帐户，其中适用您的正常 2FA。之后令牌是自治的。

## 设置

### 1.创建机器帐户和访问令牌

在 [Bitwarden 网络应用程序](https://vault.bitwarden.com) 中（或 [vault.bitwarden.eu](https://vault.bitwarden.eu) 对于欧盟帐户）：

1. 从产品切换器切换到 **Secrets Manager**。
2. 创建或选择一个**项目**（例如“OpenClaw 钥匙”）。
3. 将您的提供商密钥添加为机密。秘密**名称**成为环境变量名称 - 使用“OPENROUTER_API_KEY”、“ANTHROPIC_API_KEY”等。
4. **机器帐户 → 新机器帐户 → 我的 OpenClaw 机器** → **项目** 选项卡 → 授予对项目的读取权限。
5. **访问令牌**选项卡 → **创建访问令牌** → **永不**过期（或选择日期）→ 复制令牌（以“0.”开头）。 Bitwarden 无法再次检索它 - 保留副本。

Secrets Manager 包含在 Bitwarden 免费套餐中，但有限制；无需付费计划即可尝试此功能。

### 2. 运行向导

````bash
爱马仕的秘密 Bitwarden 设置
````

它将：

1. 下载并验证“bws v2.0.0”到“~/.hermes/bin/bws”中。
2. 提示您输入访问令牌（输入是隐藏的）。存储在`~/.hermes/.env`中作为`BWS_ACCESS_TOKEN`。
3. 询问您的机器帐户属于哪个 Bitwarden 区域 - **美国云**、**欧盟云**或 **自托管/自定义 URL**。作为“secrets.bitwarden.server_url”存储在“config.yaml”中，并作为“BWS_SERVER_URL”传递到“bws”。
4、列出机器账号可以看到的项目；选择一个。存储在“config.yaml”中为“secrets.bitwarden.project_id”。
5. 测试获取项目的机密并显示将解析哪些环境变量。
6. 翻转 `secrets.bitwarden.enabled: true`。

还通过标志支持非交互式设置：

````bash
爱马仕秘密bitwarden设置\
  --访问令牌“$BWS_ACCESS_TOKEN”\
  --server-url https://vault.bitwarden.eu \
  --project-id <项目uuid>
````

### 3.确认

````bash
Hermes 秘密 Bitwarden 状态
````

从现在开始，每次“hermes”调用都会在启动时获取新的秘密。第一次在进程中应用机密时，您将在 stderr 中看到一行摘要。

## 命令行界面

|命令|它有什么作用 |
|---|---|
| `hermes 的秘密 bitwarden 设置` |交互式向导（安装二进制文件、提示输入令牌、选择项目、测试获取）|
| “爱马仕 (OpenClaw) 的比特守护者身份秘密” |显示配置 + 二进制版本 + 令牌存在 |
| `hermes 比特守护者同步的秘密` |试运行：立即提取秘密并展示将应用什么 |
| `hermes 秘密 bitwarden 同步 --apply` |拉取并导出到当前 shell 环境 |
| `hermes 秘密 bitwarden 安装` |只需下载固定的“bws”二进制文件（无需身份验证）|
| `hermes 秘密 bitwarden 禁用` |翻转 `enabled: false`;保留代币 + 项目 ID |

## 配置

`~/.hermes/config.yaml` 中的默认值：

````yaml
秘密：
  位管理员：
    启用：假
    access_token_env：BWS_ACCESS_TOKEN
    项目 ID：“”
    服务器地址：“”
    缓存生存时间：300
    override_existing：true
    自动安装：真
````

|关键|默认 |它有什么作用 |
|---|---|---|
| `已启用` | `假` |主开关。如果为 false，则永远不会联系 Bitwarden。 |
| `access_token_env` | `BWS_ACCESS_TOKEN` |保存引导令牌的环境变量名称。如果您已经将“BWS_ACCESS_TOKEN”用于其他用途，请更改此设置。 |
| `project_id` | `""` |要同步的项目的 UUID。 |
| `server_url` | `""` | Bitwarden 区域或自托管端点。空 = 默认“bws”（美国云，“https://vault.bitwarden.com”）。对于 EU Cloud，设置为“https://vault.bitwarden.eu”，对于自托管，设置为您自己的 URL。作为“BWS_SERVER_URL”进入“bws”子进程。 |
| `cache_ttl_秒` | `300` |重用进程内获取结果的时间长度。设置为“0”以禁用缓存。缓存是每个进程的；新的“hermes”调用重新开始。 |
| `覆盖现有的` | `真实` |当 true 时，Bitwarden 值会覆盖 env 中已有的任何内容（因此 Web 应用程序中的旋转实际上会生效）。如果您希望“.env”/shell 导出在本地获胜，请翻转到“false”。 |
| `自动安装` | `真实` |当 true 时，第一次使用时 `bws` 会自动下载到 `~/.hermes/bin/` 中。 |

## 故障模式

Bitwarden 从不阻止 OpenClaw 启动。如果出现任何问题，您将在 stderr 中看到一行警告，并且 OpenClaw 会继续使用已拥有的任何凭据“.env”：

|症状|原因 |修复 |
|---|---|---|
| `BWS_ACCESS_TOKEN 未设置` |在配置中启用，但令牌已从“.env”中清除 |重新运行 `hermes Secrets bitwarden setup` |
| `bws 退出 1：访问令牌无效` |令牌被撤销或错误 |生成新令牌，重新运行安装程序 |
| `[400 错误请求] {"error":"invalid_client"}` |令牌适用于 Bitwarden 区域，而不是正在调用的“bws”（例如，欧盟令牌击中美国身份端点）|重新运行安装程序并选择正确的区域，或将“secrets.bitwarden.server_url”设置为“https://vault.bitwarden.eu”（或您的自托管 URL）|
| `bws 超时` |网络阻塞或 Bitwarden API 缓慢 |检查与“api.bitwarden.com”（或您的“server_url”）的连接 |
| `bws 二进制文件不可用` | `auto_install: false` 和 `bws` 不在 PATH 上 |从 [github.com/bitwarden/sdk-sm/releases](https://github.com/bitwarden/sdk-sm/releases) 手动安装或将 `auto_install` 重新打开 |
| `校验和不匹配` |下载已损坏或被篡改 |重新运行，会重试；如果问题仍然存在，请提出问题 |

## 安全说明

- 引导令牌（`BWS_ACCESS_TOKEN`）本身是敏感的 - 任何拥有它的人都可以读取机器帐户有权访问的每个秘密。将其与任何其他 API 密钥一样对待。
- OpenClaw 将拒绝让 Bitwarden 覆盖引导令牌本身，即使使用“override_existing: true”。如果您将“BWS_ACCESS_TOKEN”存储为项目中的秘密，则在应用过程中会默默地跳过它。
- “bws”二进制文件下载已根据同一 GitHub 版本发布的 SHA-256 校验和进行验证。不匹配会中止安装。
- 固定版本（撰写本文时的“bws v2.0.0”）通过 PR 更新到此存储库 — OpenClaw 不会自动将“bws”升级到“最新”，因为上游版本形状可能会发生变化。

## 什么时候不应该使用这个

- **单机个人设置**，其中 `~/.hermes/.env` 就可以了。您将一种凭据交换为另一种凭据，并在启动时添加网络依赖项。
- **气隙环境**无法到达`api.bitwarden.com`。
- **CI/CD** 已设置现有秘密注入机制（GitHub Actions 秘密、Vault 等） - 选择一条路径，而不是两条。

最好的例子是多机队列、共享开发盒、网关 VPS 或任何您希望在多个 OpenClaw 安装之间进行集中轮换和撤销的设置。