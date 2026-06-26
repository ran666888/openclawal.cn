---
title: "Fastmcp — Build, test, inspect, install, and deploy MCP servers with FastMCP in Python"
sidebar_label: "Fastmcp"
description: "Build, test, inspect, install, and deploy MCP servers with FastMCP in Python"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 快速mcp

使用 Python 中的 FastMCP 构建、测试、检查、安装和部署 MCP 服务器。在创建新的 MCP 服务器、将 API 或数据库包装为 MCP 工具、公开资源或提示，或者为 Claude Code、Cursor 或 HTTP 部署准备 FastMCP 服务器时使用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mcp/fastmcp` 安装 |
|路径| `可选技能/mcp/fastmcp` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `MCP`、`FastMCP`、`Python`、`工具`、`资源`、`提示`、`部署` |
|相关技能| `native-mcp`，[`mcporter`](/docs/user-guide/skills/optional/mcp/mcp-mcporter) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 快速MCP

使用 FastMCP 在 Python 中构建 MCP 服务器，在本地验证它们，将它们安装到 MCP 客户端中，并将它们部署为 HTTP 端点。

## 何时使用

当任务是：

- 在Python中创建一个新的MCP服务器
- 将 API、数据库、CLI 或文件处理工作流程包装为 MCP 工具
- 除了工具之外还公开资源或提示
- 在将服务器连接到 OpenClaw 或其他客户端之前，使用 FastMCP CLI 对服务器进行冒烟测试
- 将服务器安装到 Claude Code、Claude Desktop、Cursor 或类似的 MCP 客户端
- 为 HTTP 部署准备 FastMCP 服务器存储库

当服务器已经存在并且只需要连接到 OpenClaw 时，使用“native-mcp”。当目标是对现有 MCP 服务器进行临时 CLI 访问而不是构建服务器时，请使用“mcporter”。

## 先决条件

首先在工作环境中安装FastMCP：

````bash
pip 安装 fastmcp
fastmcp版本
````

对于 API 模板，如果“httpx”尚不存在，请安装它：

````bash
pip 安装 httpx
````

## 包含的文件

### 模板

- `templates/api_wrapper.py` - 具有 auth 标头支持的 REST API 包装器
- `templates/database_server.py` - 只读 SQLite 查询服务器
- `templates/file_processor.py` - 文本文件检查和搜索服务器

### 脚本

- `scripts/scaffold_fastmcp.py` - 复制入门模板并替换服务器名称占位符

### 参考文献

- `references/fastmcp-cli.md` - FastMCP CLI 工作流程、安装目标和部署检查

## 工作流程

### 1. 选择最小的可行服务器形状

首先选择最窄的有用表面积：

- API 包装器：从 1-3 个高价值端点开始，而不是整个 API
- 数据库服务器：公开只读内省和受约束的查询路径
- 文件处理器：使用显式路径参数公开确定性操作
- 提示/资源：仅当客户需要可重用的提示模板或可发现的文档时添加

与具有模糊工具的大型服务器相比，更喜欢具有良好名称、文档字符串和模式的瘦服务器。

### 2. 模板支架

直接复制模板或使用脚手架助手：

````bash
python ~/.hermes/skills/mcp/fastmcp/scripts/scaffold_fastmcp.py \
  --template api_wrapper \
  --name“Acme API”\
  --输出./acme_server.py
````

可用模板：

````bash
python ~/.hermes/skills/mcp/fastmcp/scripts/scaffold_fastmcp.py --list
````

如果手动复制，请将`__SERVER_NAME__`替换为真实的服务器名称。

### 3. 首先实施工具

在添加资源或提示之前，从“@mcp.tool”函数开始。

工具设计规则：

- 为每个工具指定一个基于动词的具体名称
- 将文档字符串编写为面向用户的工具描述
- 保持参数明确并键入
- 尽可能返回结构化 JSON 安全数据
- 尽早验证不安全的输入
- 对于第一个版本，默认情况下更喜欢只读行为

好的工具示例：

- `获取客户`
- `搜索门票`
- `描述表`
- `summarize_text_file`

弱工具示例：

- `运行`
- `进程`
- `做事`

### 4.仅在有帮助时添加资源和提示

当客户端受益于获取稳定的只读内容（例如架构、策略文档或生成的报告）时，添加“@mcp.resource”。

当服务器应该为已知工作流程提供可重用的提示模板时，添加“@mcp.prompt”。

不要将每个文档都变成提示。更喜欢：

- 行动工具
- 数据/文档检索资源
- 提示可重复使用的LLM指令

### 5. 在将服务器集成到任何地方之前测试服务器

使用 FastMCP CLI 进行本地验证：

````bash
fastmcp 检查 acme_server.py:mcp
fastmcp 列表 acme_server.py --json
fastmcp 调用 acme_server.py search_resources query=router limit=5 --json
````

为了快速迭代调试，请在本地运行服务器：

````bash
fastmcp 运行 acme_server.py:mcp
````

要在本地测试 HTTP 传输：

````bash
fastmcp 运行 acme_server.py:mcp --transport http --host 127.0.0.1 --port 8000
fastmcp 列表 http://127.0.0.1:8000/mcp --json
fastmcp 调用 http://127.0.0.1:8000/mcp search_resources query=router --json
````

在声明服务器工作之前，始终针对每个新工具至少运行一次真正的“fastmcp 调用”。

### 6.本地验证通过后安装到客户端

FastMCP 可以向支持的 MCP 客户端注册服务器：

````bash
fastmcp 安装克劳德代码 acme_server.py
fastmcp 安装 claude-desktop acme_server.py
fastmcp 安装光标 acme_server.py -e 。
````

使用“fastmcp discovery”检查计算机上已配置的命名 MCP 服务器。

当目标是 OpenClaw 集成时，可以：

- 使用“native-mcp”技能在“~/.hermes/config.yaml”中配置服务器，或者
- 在开发过程中继续使用FastMCP CLI命令，直到接口稳定

### 7.本地合约稳定后部署

对于托管主机，Prefect Horizon 是 FastMCP 文档最直接的路径。部署前：

````bash
fastmcp 检查 acme_server.py:mcp
````

确保存储库包含：

- 带有 FastMCP 服务器对象的 Python 文件
- `requirements.txt` 或 `pyproject.toml`
- 部署所需的任何环境变量文档

对于通用 HTTP 托管，首先在本地验证 HTTP 传输，然后部署在任何可以公开服务器端口的 Python 兼容平台上。

## 常见模式

### API 包装模式

将 REST 或 HTTP API 公开为 MCP 工具时使用。

推荐第一片：

- 一个读取路径
- 一个列表/搜索路径
- 可选的健康检查

实施注意事项：

- 将身份验证保留在环境变量中，而不是硬编码
- 将请求逻辑集中在一个助手中
- 通过简洁的上下文显示 API 错误
- 在返回不一致的上游有效负载之前对其进行标准化

从“templates/api_wrapper.py”开始。

### 数据库模式

在公开安全查询和检查功能时使用。

推荐第一片：

- `列表表`
- `描述表`
- 一款受限读取查询工具

实施注意事项：

- 默认为只读数据库访问
- 在早期版本中拒绝非`SELECT` SQL
- 限制行数
- 返回行加上列名

从“templates/database_server.py”开始。

### 文件处理器模式

当服务器需要按需检查或转换文件时使用。

推荐第一片：

- 总结文件内容
- 在文件内搜索
- 提取确定性元数据

实施注意事项：

- 接受显式文件路径
- 检查丢失的文件和编码失败
- 上限预览和结果计数
- 除非需要特定的外部工具，否则避免花钱

从“templates/file_processor.py”开始。

## 质量栏

在移交 FastMCP 服务器之前，请验证以下所有内容：

- 服务器干净地导入
- `fastmcp 检查 <file.py:mcp>` 成功
- `fastmcp list <服务器规范> --json` 成功
- 每个新工具都至少有一个真正的“fastmcp 调用”
- 记录环境变量
- 工具表面足够小，无需猜测即可理解

## 故障排除

### FastMCP 命令丢失

在活动环境中安装软件包：

````bash
pip 安装 fastmcp
fastmcp版本
````

### `fastmcp检查`失败

检查：

- 文件导入时不会产生崩溃的副作用
- FastMCP 实例在 `<file.py:object>` 中正确命名
- 安装模板中的可选依赖项

### 工具可以在 Python 中运行，但不能通过 CLI

运行：

````bash
fastmcp 列表 server.py --json
fastmcp 调用 server.py your_tool_name --json
````

这通常会暴露命名不匹配、缺少所需参数或不可序列化的返回值。

### OpenClaw看不到部署的服务器

服务器构建部分可能是正确的，而 OpenClaw 配置则不正确。加载`native-mcp`技能并在`~/.hermes/config.yaml`中配置服务器，然后重新启动OpenClaw。

## 参考文献

有关 CLI 详细信息、安装目标和部署检查，请阅读“references/fastmcp-cli.md”。