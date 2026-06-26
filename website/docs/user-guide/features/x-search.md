---
title: X (Twitter) Search
description: Search X (Twitter) posts and threads from within the agent using xAI's built-in x_search Responses tool — works with either a SuperGrok OAuth login or an XAI_API_KEY.
sidebar_label: X (Twitter) Search
sidebar_position: 7
---
# X (Twitter) 搜索

“x_search”工具让代理可以直接搜索 X (Twitter) 帖子、个人资料和话题。它由 xAI 响应 API 上的内置“x_search”工具支持，网址为“https://api.x.ai/v1/responses”——Grok 本身在服务器端运行搜索，并返回综合结果以及对原始帖子的引用。

**当您特别想要关于 X** 的当前讨论、反应或主张时，请使用此选项而不是“web_search”。对于一般网页，继续使用“web_search”/“web_extract”。

:::提示
如果您无论如何都要为 xAI 模型向 Portal 付费，Live Search 通话将根据为聊天配置的相同 xAI 密钥进行计费。请参阅[Nous 门户](/integrations/nous-portal)。
:::

## 身份验证

当 **任一** xAI 凭证路径可用时，`x_search` 会注册：

|资质证书 |来源 |设置 |
|------------|--------|--------|
| **SuperGrok / X Premium+ OAuth**（首选） |浏览器登录“accounts.x.ai”，自动刷新 | `hermes auth add xai-oauth` — 参见 [xAI Grok OAuth (SuperGrok / X Premium+)](../../guides/xai-grok-oauth.md) |
| **`XAI_API_KEY`** |付费 xAI API 密钥 |在 `~/.hermes/.env` 中设置 |

两者都使用相同的负载到达相同的端点 - 唯一的区别是不记名令牌。 **当两者都配置时，SuperGrok OAuth 获胜**，因此 x_search 根据您的订阅配额而不是付费 API 支出运行。

每次重建模型的工具列表时，该工具的“check_fn”都会运行 xAI 凭证解析器。 “True”返回意味着承载可获取且非空且（如果已过期）成功刷新。刷新失败而撤销的令牌会从架构中隐藏该工具；模型根本看不到它。

## 启用该工具

当 xAI 凭证（OAuth 令牌或“XAI_API_KEY”）存在时自动启用。如果您不想这样做，可以通过“hermes tools”→“搜索”→“x_search”显式禁用。

````bash
爱马仕工具
# → 🐦 X (Twitter) 搜索（按空格键打开）
````

选择器提供两种凭证选择：

1. **xAI Grok OAuth (SuperGrok / Premium+)** — 如果您尚未登录，则将浏览器打开到“accounts.x.ai”
2. **xAI API 密钥** — 提示输入“XAI_API_KEY”

任一选择都满足门控。您可以选择您已经拥有的任何凭证；该工具与两者的工作原理相同。如果两者最终均已配置，则在调用时首选 OAuth。

## 配置

````yaml
# ~/.hermes/config.yaml
x_搜索：
  # 用于响应调用的 xAI 模型。
  # grok-4.20-reasoning 是推荐的默认值；任何 Grok 型号
  # 使用 x_search 工具访问有效。
  型号：grok-4.20-reasoning

  # 请求超时（以秒为单位）。 x_search 可能需要 60–120 秒
  # 复杂查询——默认是慷慨的。最低数量：30。
  超时秒数：180

  # 5xx / ReadTimeout / ConnectionError 的自动重试次数。
  # 每次重试都会后退（1.5 倍尝试秒，上限为 5 秒）。
  重试次数：2
````

## 工具参数

代理使用以下参数调用“x_search”：

|参数|类型 |描述 |
|------------|------|-------------|
| `查询` |字符串（必需）|在 X 上查找什么。
| `allowed_x_handles` |字符串数组 | **独家**包含的可选句柄列表（最多 10 个）。前导“@”被删除。 |
| `excluded_x_handles` |字符串数组 |要排除的句柄的可选列表（最多 10 个）。与“allowed_x_handles”互斥。 |
| `起始日期` |字符串|可选的“YYYY-MM-DD”开始日期。 |
| `截止日期` |字符串|可选的“YYYY-MM-DD”结束日期。 |
| `启用图像理解` |布尔 |让 xAI 分析匹配帖子中附加的图像。 |
| `启用视频理解` |布尔 |让 xAI 分析匹配帖子中附加的视频。 |

该工具返回 JSON：

- `answer` — 来自 Grok 的合成文本响应
- `引用` — Responses API 顶级字段返回的引用
- `inline_引用` — 从消息正文中提取的`url_引用`注释（每个注释都有`url`、`title`、`start_index`、`end_index`）
- 当设置任何缩小过滤器（“allowed_x_handles”、“excluded_x_handles”、“from_date”、“to_date”）且两个引文通道都返回为空时，“degraded” - “true”。在这种情况下，“答案”是根据模型自己的知识而不是 X 索引合成的，因此将其视为无源的。否则为“false”（包括“未设置过滤器”情况 - 广泛的无源答案只是一个答案，而不是过滤器未命中）
- `degraded_reason` — 短字符串命名哪些过滤器处于活动状态，或者当 `degraded` 为 `false` 时为 `null`
- `credential_source` — `"xai-oauth"` 如果 OAuth 已解析，则 `"xai"` 如果 API 密钥已解析
- `模型`、`查询`、`提供者`、`工具`、`成功`

### 日期验证

`from_date` / `to_date` 在 HTTP 调用之前在客户端进行验证：

- 两者（如果提供）必须解析为“YYYY-MM-DD”。
- 当两者都设置时，“from_date”必须位于“to_date”之前或之前。
- `from_date` 不得晚于今天的 UTC — 尚未启动的窗口中不能存在任何帖子，因此调用将保证返回零引用。
- 允许将来的“to_date”（呼叫者可以合法地请求“从昨天到明天”以在帖子到达时捕获帖子）。

验证失败表现为结构化的“{"error": "..."}`工具结果，而不是对 xAI 的 HTTP 调用。

## 示例

与代理交谈：

> X 上的人们对新的 Grok 图像功能有何评价？关注@xai 的回复。

代理人将：

1. 使用 `query="reactions to new Grok image features"`, `allowed_x_handles=["xai"]` 调用 `x_search`
2. 获取综合答案以及链接到特定帖子的引文列表
3.回复答案及参考文献

## 故障排除

###“没有可用的 xAI 凭据”

当两个身份验证路径都失败时，该工具会显示此信息。在 `~/.hermes/.env` 中设置 `XAI_API_KEY` 或运行 `hermes auth add xai-oauth` 并完成浏览器登录。然后重新启动会话，以便代理重新读取工具注册表。

### “此模型未启用`x_search`”

配置的“x_search.model”无权访问服务器端“x_search”工具。切换到“grok-4.20-reasoning”（默认）或其他支持它的 Grok 模型。检查 [xAI 文档](https://docs.x.ai/) 以获取当前列表。

### 工具未出现在架构中

两个可能的原因：

1. **工具集未启用。** 运行 `hermes tools` 并确认选中 `🐦 X (Twitter) Search`。
2. **没有 xAI 凭证。** check_fn 返回 False，因此架构保持隐藏状态。运行“hermes auth status”以确认 xai-oauth 登录状态，并检查“XAI_API_KEY”是否已设置（如果您使用的是 API 密钥路径）。

### `degraded: true` — 没有引用的答案

当您使用“allowed_x_handles”、“excluded_x_handles”或日期范围并且响应返回“degraded: true”时，xAI 的 X 索引没有返回匹配的帖子，但 Grok 仍然根据自己的训练数据生成综合答案。答案是无源的——不要将其视为真正的 X 结果。

值得检查的原因：

- **句柄中的拼写错误。** 去掉“@”，仔细检查拼写，并确认该帐户存在。
- **日期范围太窄**或滑过今天的帖子；扩大并重试。
- **xAI 指数差距。** 一些活跃帐户即使定期发帖，也会间歇性地无法出现在“x_search”中。几分钟后重试，或者当您需要精确句柄的时间线时，使用“xurl”技能直接 X API 读取。

## 另请参阅

- [xAI Grok OAuth (SuperGrok / Premium+)](../../guides/xai-grok-oauth.md) — OAuth 设置指南
- [网页搜索和提取](web-search.md) — 用于一般（非 X）网页搜索
- [工具参考](../../reference/tools-reference.md) — 完整工具目录