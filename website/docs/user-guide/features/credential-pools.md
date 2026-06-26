---
title: Credential Pools
description: Pool multiple API keys or OAuth tokens per provider for automatic rotation and rate limit recovery.
sidebar_label: Credential Pools
sidebar_position: 9
---
# 凭证池

凭证池允许您为同一提供商注册多个 API 密钥或 OAuth 令牌。当一个密钥达到速率限制或计费配额时，OpenClaw 会自动轮换到下一个正常的密钥 - 保持会话处于活动状态，而无需切换提供商。

这与 [后备提供商](./fallback-providers.md) 不同，后者完全切换到*不同的*提供商。凭证池是同一提供商轮换的；后备提供商是跨提供商故障转移。首先尝试池 - 如果所有池密钥都用尽，*然后*后备提供程序将激活。

:::提示
凭证池主要用于 API 密钥提供者（OpenRouter、Anthropic）。单个 [Nous Portal](/integrations/nous-portal) OAuth 涵盖 300 多个模型，因此大多数用户在使用 Portal 时不需要池。
:::

## 它是如何工作的

````
您的要求
  → 从池中选择密钥（round_robin / less_used / fill_first / random）
  → 发送给提供商
  → 429 速率限制？
      → 达到计划/使用限制（例如 ChatGPT/Codex“达到使用限制”）？
          → 立即旋转到下一个池密钥（无需重试 - 重试时上限不会清除）
      → 通用/瞬态 429？
          → 重试相同的按键一次（瞬态信号）
          → 第二个 429 → 旋转到下一个池密钥
      → 所有密钥均已用尽 →fallback_model（不同提供商）
  → 402 计费错误？
      → 立即旋转到下一个池键（24 小时冷却时间）
  → 401 授权已过期？
      → 尝试刷新令牌（OAuth）
      → 刷新失败 → 轮换到下一个池密钥
  → 成功 → 正常继续
````

## 快速入门

如果您已经在“.env”中设置了 API 密钥，OpenClaw 会自动将其发现为 1 密钥池。要从池中受益，请添加更多键：

````bash
# 添加第二个 OpenRouter 密钥
Hermes auth 添加 openrouter --api-key sk-or-v1-your-second-key

# 添加第二个 Anthropic 密钥
Hermes auth 添加 anthropic --type api-key --api-key sk-ant-api03-your-second-key

# 添加 Anthropic OAuth 凭证（需要 Claude Max 计划 + 额外使用积分）
Hermes auth 添加 anthropic --type oauth
# 打开浏览器进行 OAuth 登录
````

检查您的池：

````bash
Hermes 授权列表
````

输出：
````
openrouter（2 个凭据）：
  #1 OPENROUTER_API_KEY api_key env:OPENROUTER_API_KEY ←
  #2 备份密钥 api_key 手册

人择（3 个凭证）：
  #1 hermes_pkce oauth hermes_pkce ←
  #2 claude_code oauth claude_code
  #3 ANTHROPIC_API_KEY api_key env:ANTHROPIC_API_KEY
````

“←”标记当前选择的凭证。

## 互动管理

对于交互式向导，运行不带子命令的“hermes auth”：

````bash
爱马仕正品
````

这会显示您的完整池状态并提供一个菜单：

````
你想做什么？
  1.添加凭证
  2. 删除凭证
  3.重置提供者的冷却时间
  4. 为提供商设置轮换策略
  5. 退出
````

对于同时支持 API 密钥和 OAuth（Anthropic、Nous、Codex）的提供商，添加流程会询问哪种类型：

````
anthropic 支持 API 密钥和 OAuth 登录。
  1. API 密钥（粘贴提供商仪表板中的密钥）
  2. OAuth登录（通过浏览器验证）
类型[1/2]：
````

## CLI 命令

|命令|描述 |
|---------|-------------|
|爱马仕正品交互式池管理向导 |
| `hermes 授权列表` |显示所有池和凭据 |
| `hermes auth list <provider>` |显示特定提供商的池 |
| `hermes auth add <provider>` |添加凭据（提示输入类型和密钥）|
| `hermes auth add <provider> --type api-key --api-key <key>` |以非交互方式添加 API 密钥 |
| `hermes auth add <provider> --type oauth` |通过浏览器登录添加 OAuth 凭证 |
| `hermes auth 删除 <provider> <index>` |通过从 1 开始的索引删除凭证 |
| `hermes auth Reset <provider>` |清除所有冷却/耗尽状态 |

## 轮换策略

通过“hermes auth”→“设置轮换策略”或在“config.yaml”中配置：

````yaml
凭证池策略：
  开放路由器：round_robin
  人择：最少使用
````

|战略|行为 |
|----------|----------|
| `fill_first`（默认）|使用第一个健康键直到它用完，然后移动到下一个 |
| `round_robin` |均匀地循环按键，每次选择后旋转 |
| `最少使用` |始终选择请求数最少的键 |
| `随机` |健康键中的随机选择 |

## 错误恢复

池以不同的方式处理不同的错误：

|错误 |行为 |冷却时间|
|--------|----------|----------|
| **429 速率限制** |重试相同的按键一次（暂时的）。第二个连续 429 轮换到下一个键 | 1小时|
| **402 计费/配额** |立即旋转到下一个键 | 24小时|
| **401 授权已过期** |首先尝试刷新 OAuth 令牌。仅在刷新失败时才旋转 | — |
| **所有钥匙已用完** |如果配置的话，会进入`fallback_model` | — |

“has_retried_429”标志会在每次成功的 API 调用时重置，因此单个瞬态 429 不会触发轮换。

## 自定义端点池

自定义 OpenAI 兼容端点（Together.ai、RunPod、本地服务器）获得自己的池，由 config.yaml 中“custom_providers”中的端点名称作为键控。

当您通过“hermes model”设置自定义端点时，它会自动生成一个名称，例如“Together.ai”或“Local (localhost:8080)”。该名称成为池密钥。

````bash
# 通过 Hermes 模型设置自定义端点后：
Hermes 授权列表
# 显示：
# Together.ai（1 个凭证）：
# #1 配置密钥 api_key config:Together.ai ←

# 为同一端点添加第二个密钥：
Hermes auth add Together.ai --api-key sk-together-second-key
````

自定义端点池存储在“credential_pool”下的“auth.json”中，并带有“custom:”前缀：

```json
{
  “凭证池”：{
    “开放路由器”：[...]，
    “自定义：together.ai”：[...]
  }
}
````

## 自动发现

OpenClaw 会自动发现来自多个来源的凭证，并在启动时为池播种：

|来源 |示例|自动播种？ |
|--------|---------|-------------|
|环境变量| `OPENROUTER_API_KEY`、`ANTHROPIC_API_KEY` |是的 |
| OAuth 令牌 (auth.json) | Codex 设备代码、Nous 设备代码 |是的 |
|克劳德代码凭证 | `~/.claude/.credentials.json` |是（人择）|
| OpenClaw PKCE OAuth | `~/.hermes/auth.json` |是（人择）|
|自定义端点配置| config.yaml 中的“model.api_key” |是（自定义端点）|
|手动输入 |通过 `hermes auth add` 添加 |保留在 auth.json |

自动种子条目会在每次池加载时更新 - 如果删除环境变量，其池条目会自动修剪。手动条目（通过“hermes auth add”添加）永远不会被自动修剪。

借用的运行时机密（例如环境变量、Bitwarden/Vault/keyring/systemd 引用和自定义配置值）在“auth.json”边界仅供参考。 OpenClaw 可以在当前运行中使用内存中的解析值，但它仅保留元数据，例如源引用、标签、状态、请求计数器和不可逆指纹。手动输入和 OpenClaw 拥有的 OAuth/设备代码状态保留了它们需要刷新的持久令牌。

## 委派和子代理共享

当代理通过“delegate_task”生成子代理时，父代理的凭证池会自动与子代理共享：

- **同一提供商** — 子项接收父项的完整池，从而实现速率限制的密钥轮换
- **不同的提供程序** — 子进程加载该提供程序自己的池（如果已配置）
- **未配置池** — 子级回退到继承的单个 API 密钥

这意味着子代理受益于与父代理相同的速率限制弹性，无需额外配置。每个任务的凭证租赁可确保子进程在同时轮换密钥时不会相互冲突。

## 线程安全

凭证池对所有状态突变（`select()`、`mark_exhausted_and_rotate()`、`try_refresh_current()`、`mark_used()`）使用线程锁。当网关同时处理多个聊天会话时，这可以确保安全的并发访问。

## 架构

有关完整的数据流图，请参阅存储库中的 [`docs/credential-pool-flow.excalidraw`](https://excalidraw.com/#json=2Ycqhqpi6f12E_3ITyiwh,c7u9jSt5BwrmiVzHGbm87g)。

凭证池集成在提供者解析层：

1. **`agent/credential_pool.py`** — 池管理器：存储、选择、轮换、冷却
2. **`hermes_cli/auth_commands.py`** — CLI 命令和交互式向导
3. **`hermes_cli/runtime_provider.py`** — 池感知凭证解析
4. **`run_agent.py`** — 错误恢复：429/402/401 → 池轮换 → 回退

## 存储

池状态存储在 `~/.hermes/auth.json` 中的 `credential_pool` 键下：

```json
{
  “版本”：1，
  “凭证池”：{
    “开放路由器”：[
      {
        “id”：“abc123”，
        “标签”：“OPENROUTER_API_KEY”，
        “auth_type”：“api_key”，
        “优先级”：0，
        “来源”：“环境：OPENROUTER_API_KEY”，
        "secret_source": "bitwarden",
        "secret_fingerprint": "sha256:12ab34cd56ef7890",
        “last_status”：“好的”，
        “请求计数”：142
      }
    ],
    “人择”：[
      {
        "id": "手册1",
        "label": "个人 API 密钥",
        “auth_type”：“api_key”，
        “优先级”：0，
        “来源”：“手册”，
        “access_token”：“sk-ant-api03-...”
      }
    ]
  }
}
````

上面的 OpenRouter 条目是从外部来源借用的，因此原始密钥不存储在“auth.json”中。手动 Anthropic 条目被有意添加到 OpenClaw 的凭证存储中，因此其令牌仍然是持久的。

策略存储在“config.yaml”中（而不是“auth.json”）：

````yaml
凭证池策略：
  开放路由器：round_robin
  人择：最少使用
````