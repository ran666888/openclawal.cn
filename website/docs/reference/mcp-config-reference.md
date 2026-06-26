---
sidebar_position: 8
title: "MCP Config Reference"
description: "Reference for OpenClaw MCP configuration keys, filtering semantics, and utility-tool policy"
---
# MCP 配置参考

此页面是主要 MCP 文档的紧凑参考配套。

有关概念指导，请参阅：
- [MCP（模型上下文协议）](/user-guide/features/mcp)
- [将 MCP 与 OpenClaw 一起使用](/guides/use-mcp-with-hermes)

## 根配置形状

````yaml
mcp_服务器：
  <服务器名称>：
    命令：“...”# stdio 服务器
    参数：[]
    环境：{}

    # 或
    url: "..." # HTTP 服务器
    标头：{}

    # 可选的 HTTP/SSE TLS 设置：
    ssl_verify: true # bool 或 CA 捆绑包 (PEM) 的路径
    client_cert: "/path/to/cert.pem" # mTLS 客户端证书（见下文）
    # client_key: "/path/to/key.pem" # 可选，当密钥位于单独的文件中时

    启用：真
    超时：120
    连接超时：60
    支持并行工具调用： false
    工具：
      包括：[]
      排除：[]
      资源：真实
      提示：正确
````

## 服务器密钥

|关键|类型 |适用于 |意义|
|---|---|---|---|
| `命令` |字符串|工作室|可执行启动 |
| `参数` |列表 |工作室|子流程的参数 |
| `env` |地图|工作室|传递给子进程的环境 |
| `网址` |字符串| HTTP |远程 MCP 端点 |
| `标题` |地图| HTTP |远程服务器请求的标头 |
| `ssl_verify` |布尔值或字符串 | HTTP | TLS 验证。 “true”（默认）使用系统 CA，“false”禁用验证（不安全）或自定义 CA 捆绑包 (PEM) 的字符串路径 |
| `client_cert` |字符串或列表 | HTTP | mTLS 客户端证书。 String = 包含证书 + 密钥的 PEM 文件的路径。列出“[证书，密钥]”=单独的文件。列表 `[证书、密钥、密码]` = 加密密钥 |
| `client_key` |字符串| HTTP |当“client_cert”是字符串并且密钥位于单独的文件中时，客户端私钥的路径 |
| `已启用` |布尔 |两者 | false 时完全跳过服务器 |
| `超时` |数量 |两者 |工具调用超时以秒为单位（默认值：`300`）|
| `连接超时` |数量 |两者 |初始连接超时（以秒为单位）（默认值：`60`）|
| `支持并行工具调用` |布尔 |两者 |允许该服务器上的工具同时运行 |
| `工具` |地图|两者 |过滤和实用工具策略|
| `验证` |字符串| HTTP |认证方式。设置为 `oauth` 以通过 PKCE 启用 OAuth 2.1 |
| `抽样` |地图|两者 |服务器发起的 LLM 请求策略（请参阅 MCP 指南） |

## `tools` 策略键

|关键|类型 |意义|
|---|---|---|
| `包括` |字符串或列表 |白名单服务器本机 MCP 工具 |
| `排除` |字符串或列表 |黑名单服务器原生 MCP 工具 |
| `资源` |类似布尔 |启用/禁用 `list_resources` + `read_resource` |
| `提示` |类似布尔 |启用/禁用 `list_prompts` + `get_prompt` |

## 过滤语义

### `包含`

如果设置了“include”，则仅注册那些服务器本机 MCP 工具。

````yaml
工具：
  包括：[创建问题，列表问题]
````

### `排除`

如果设置了“exclude”而未设置“include”，则注册除这些名称之外的所有服务器本机 MCP 工具。

````yaml
工具：
  排除：[delete_customer]
````

### 优先级

如果两者都设置了，则“include”获胜。

````yaml
工具：
  包括：[创建问题]
  排除：[创建问题、删除问题]
````

结果：
- 仍然允许`create_issue`
- `delete_issue` 被忽略，因为 `include` 优先

## 实用工具策略

OpenClaw 可以为每个 MCP 服务器注册这些实用程序包装器：

资源：
- `列表资源`
- `读取资源`

提示：
- `列表提示`
- `获取提示`

### 禁用资源

````yaml
工具：
  资源：假
````

### 禁用提示

````yaml
工具：
  提示：假
````

### 能力感知注册

即使当“resources: true”或“prompts: true”时，OpenClaw 仅在 MCP 会话实际公开相应功能时才注册这些实用工具。

所以这是正常的：
- 您启用提示
- 但没有出现提示实用程序
- 因为服务器不支持提示

## `启用：假`

````yaml
mcp_服务器：
  遗产：
    网址：“https://mcp.legacy.internal”
    启用：假
````

行为：
- 没有连接尝试
- 没有发现
- 无需工具注册
- 配置保留以供以后重用

## 空结果行为

如果过滤删除了所有服务器本机工具并且没有注册任何实用工具，则 OpenClaw 不会为该服务器创建空的 MCP 运行时工具集。

## 配置示例

### 安全 GitHub 许可名单

````yaml
mcp_服务器：
  github：
    命令：“npx”
    参数：[“-y”，“@modelcontextprotocol/server-github”]
    环境：
      GITHUB_PERSONAL_ACCESS_TOKEN：“***”
    工具：
      包括：[列表问题、创建问题、更新问题、搜索代码]
      资源：假
      提示：假
````

### 条纹黑名单

````yaml
mcp_服务器：
  条纹：
    网址：“https://mcp.stripe.com”
    标题：
      授权：“不记名***”
    工具：
      排除：[删除客户，退款付款]
````

### 纯资源文档服务器

````yaml
mcp_服务器：
  文档：
    网址：“https://mcp.docs.example.com”
    工具：
      包括：[]
      资源：真实
      提示：假
````

### TLS 客户端证书 (mTLS)

对于需要客户端证书的 HTTP/SSE 服务器，请设置“client_cert”（以及可选的“client_key”）：

````yaml
mcp_服务器：
  # 在单个 PEM 文件中组合证书 + 密钥
  内部API：
    网址：“https://mcp.internal.example.com/mcp”
    client_cert：“~/secrets/mcp-client.pem”

  # 单独的证书和密钥文件
  合作伙伴 API：
    网址：“https://mcp.partner.example.com/mcp”
    client_cert：“~/secrets/client.crt”
    client_key: "~/secrets/client.key"

  # 带密码的加密密钥（3 元素列表形式）
  银行API：
    网址：“https://mcp.bank.example.com/mcp”
    client_cert：[“~/secrets/client.crt”，“~/secrets/client.key”，“我的密码”]

  # 自定义 CA 捆绑包（私有 CA/自签名服务器）
  实验室API：
    网址：“https://mcp.lab.local/mcp”
    ssl_verify：“~/secrets/lab-ca.pem”
    client_cert：“~/secrets/lab-client.pem”
````

注意事项：
- 路径支持`~`扩展。丢失的文件在连接时会快速失败，并显示服务器范围的错误消息。
- `ssl_verify: false` 完全禁用服务器证书验证。不要将其用于实际服务。
- 适用于可流式 HTTP 和 SSE 传输。

## 重新加载配置

更改 MCP 配置后，使用以下命令重新加载服务器：

````文本
/重新加载-mcp
````

## 工具命名

服务器本机 MCP 工具变为：

````文本
mcp_<服务器>_<工具>
````

示例：
- `mcp_github_create_issue`
- `mcp_filesystem_read_file`
- `mcp_my_api_query_data`

实用工具遵循相同的前缀模式：
- `mcp_<服务器>_list_resources`
- `mcp_<服务器>_读取资源`
- `mcp_<服务器>_list_prompts`
- `mcp_<服务器>_get_prompt`

### 名称清理

服务器名称和工具名称中的连字符（`-`）和点（`.`）在注册前均替换为下划线。这可确保工具名称是 LLM 函数调用 API 的有效标识符。

例如，名为“my-api”的服务器公开了一个名为“list-items.v2”的工具，该服务器变为：

````文本
mcp_my_api_list_items_v2
````

在编写“包含”/“排除”过滤器时请记住这一点 - 使用**原始** MCP 工具名称（带连字符/点），而不是经过清理的版本。

## OAuth 2.1 身份验证

对于需要 OAuth 的 HTTP 服务器，请在服务器条目上设置“auth: oauth”：

````yaml
mcp_服务器：
  受保护的API：
    网址：“https://mcp.example.com/mcp”
    授权：oauth
````

行为：
- OpenClaw 使用 MCP SDK 的 OAuth 2.1 PKCE 流程（元数据发现、动态客户端注册、令牌交换和刷新）
- 首次连接时，将打开一个浏览器窗口以进行授权
- 令牌持久保存到 `~/.hermes/mcp-tokens/<server>.json` 并在会话之间重复使用
- 令牌刷新是自动的；仅当刷新失败时才会进行重新授权
- 仅适用于 HTTP/StreamableHTTP 传输（基于 `url` 的服务器）