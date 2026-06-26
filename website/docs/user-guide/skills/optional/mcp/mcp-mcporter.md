---
title: "Mcporter"
sidebar_label: "Mcporter"
description: "Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type gene..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 麦克波特

使用 mcporter CLI 直接列出、配置、验证和调用 MCP 服务器/工具（HTTP 或 stdio），包括临时服务器、配置编辑和 CLI/类型生成。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mcp/mcporter` 安装 |
|路径| `可选技能/mcp/mcporter` |
|版本 | `1.0.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `MCP`、`工具`、`API`、`集成`、`互操作` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 麦克波特

使用 `mcporter` 直接从终端发现、调用和管理 [MCP（模型上下文协议）](https://modelcontextprotocol.io/) 服务器和工具。

## 先决条件

需要 Node.js：
````bash
# 无需安装（通过 npx 运行）
npx 麦克波特列表

# 或者全局安装
npm 安装-g mcporter
````

## 快速入门

````bash
# 列出本机上已配置的 MCP 服务器
麦克波特名单

# 列出特定服务器的工具以及架构详细信息
mcporter list <服务器> --schema

# 调用工具
mcporter 调用 <server.tool> key=value
````

## 发现 MCP 服务器

mcporter 自动发现计算机上其他 MCP 客户端（Claude Desktop、Cursor 等）配置的服务器。要查找要使用的新服务器，请浏览 [mcpfinder.dev](https://mcpfinder.dev) 或 [mcp.so](https://mcp.so) 等注册表，然后进行临时连接：

````bash
# 通过 URL 连接到任何 MCP 服务器（无需配置）
mcporter list --http-url https://some-mcp-server.com --name my_server

# 或者动态运行 stdio 服务器
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
````

## 调用工具

````bash
# 键=值语法
mcporter 调用 Linear.list_issues team=ENG 限制：5

# 函数语法
mcporter 调用“linear.create_issue（标题：\“需要修复错误\”）”

# Ad-hoc HTTP 服务器（无需配置）
mcporter 调用 https://api.example.com/mcp.fetch url=https://example.com

# Ad-hoc stdio 服务器
mcporter 调用 --stdio "bun run ./server.ts" scrape url=https://example.com

# JSON 负载
mcporter 调用 <server.tool> --args '{"limit": 5}'

# 机器可读的输出（推荐用于 Hermes）
mcporter 调用 <server.tool> key=value --output json
````

## 身份验证和配置

````bash
# 服务器的 OAuth 登录
mcporter auth <服务器|网址> [--重置]

# 管理配置
麦克波特配置列表
mcporter 配置获取 <key>
mcporter 配置添加 <服务器>
mcporter 配置删除 <服务器>
mcporter 配置导入 <路径>
````

配置文件位置：“./config/mcporter.json”（用“--config”覆盖）。

## 守护进程

对于持久服务器连接：
````bash
麦克波特守护进程启动
麦克波特守护进程状态
麦克波特守护程序停止
mcporter 守护进程重新启动
````

## 代码生成

````bash
# 为 MCP 服务器生成 CLI 包装器
mcportergenerate-cli --server <名称>
mcporter 生成-cli --命令 <url>

# 检查生成的 CLI
mcporter inform-cli <路径> [--json]

# 生成 TypeScript 类型/客户端
mcporter emit-ts <服务器> --模式客户端
mcporter emit-ts <服务器> --模式类型
````

## 注释

- 使用“--output json”进行结构化输出，更容易解析
- 临时服务器（HTTP URL 或 `--stdio` 命令）无需任何配置即可工作 — 对于一次性调用非常有用
- OAuth 身份验证可能需要交互式浏览器流程 - 如果需要，请使用 `terminal(command="mcporter auth <server>", pty=true)`