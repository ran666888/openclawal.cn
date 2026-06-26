---
sidebar_position: 11
title: "ACP Editor Integration"
description: "在 VS Code、Zed 和 JetBrains 等 ACP 兼容编辑器中使用 OpenClaw"
---
# ACP 编辑器集成

OpenClaw 可以作为 ACP 服务器运行，让 ACP 兼容的编辑器通过 stdio 与 OpenClaw 对话并渲染：

- 聊天消息
- 工具活动
- 文件差异
- 终端命令
- 批准提示
- 流式思维/响应块

当您希望 OpenClaw 表现得像编辑器本机编码代理而不是独立的 CLI 或消息传递机器人时，ACP 是一个很好的选择。

## OpenClaw 在 ACP 模式下暴露了什么

OpenClaw 运行专门为编辑器工作流程设计的“hermes-acp”工具集。它包括：

- 文件工具：`read_file`、`write_file`、`patch`、`search_files`
- 终端工具：`terminal`、`process`
- 网络/浏览器工具
- 内存、待办事项、会话搜索
- 技能
- 执行代码和委托任务
- 愿景

它有意排除不适合典型编辑器用户体验的内容，例如消息传递和定时任务管理。

## 安装

正常安装 OpenClaw，然后添加 ACP extra：

````bash
pip install -e '.[acp]'
````

这将安装“agent-client-protocol”依赖项并启用：

- `爱马仕 acp`
- `爱马仕-acp`
- `python -m acp_adapter`

对于 Zed 注册表安装，Zed 通过官方 ACP 注册表条目启动 OpenClaw。该条目使用运行的“uvx”发行版：

````bash
uvx --from 'hermes-agent[acp]==<版本>' Hermes-acp
````

在使用注册表安装路径之前，请确保“uv”在“PATH”上可用。

## 启动 ACP 服务器

以下任一命令都会以 ACP 模式启动 OpenClaw：

````bash
爱马仕 acp
````

````bash
爱马仕-acp
````

````bash
python -m acp_适配器
````

OpenClaw 记录到 stderr，因此 stdout 仍保留用于 ACP JSON-RPC 流量。

对于非交互式检查：

````bash
爱马仕 acp --版本
爱马仕 acp --检查
````

### 浏览器工具（可选）

浏览器工具（`browser_navigate`、`browser_click`等）取决于
`agent-browser` npm 包和 Chromium，它们不是 Python 的一部分
轮子。安装它们：

````bash
hermes acp --setup-browser # 交互式（在 ~400 MB 下载之前提示）
hermes acp --setup-browser --yes # 以非交互方式接受下载
````

这是独立命令。 Zed 注册表的终端身份验证流程（“hermes acp --setup”）还提供浏览器引导程序作为模型选择后的后续问题，因此大多数用户永远不需要直接运行“--setup-browser”。

它的作用：

- 如果缺少，则将 Node.js 22 LTS 安装到 `~/.hermes/node/` 中
- `npm install -g agent-browser @askjo/camofox-browser` 到该前缀中（不需要 sudo — `npm` 的 `--prefix` 指向用户可写的 OpenClaw 托管节点）
- 安装 Playwright Chromium，或使用检测到的系统 Chrome/Chromium（如果可用）

引导程序是幂等的——重新运行它速度很快并且会跳过已经完成的工作。

## 编辑器设置

### VS 代码

安装 [ACP 客户端](https://marketplace.visualstudio.com/items?itemName=formulahendry.acp-client) 扩展。

连接：

1. 从活动栏打开 ACP 客户端面板。
2. 从内置代理列表中选择**OpenClaw**。
3. 连接并开始聊天。

如果您想手动定义 OpenClaw，请通过 `acp.agents` 下的 VS Code 设置添加它：

```json
{
  “acp.agents”：{
    “爱马仕特工”：{
      “命令”：“爱马仕”，
      “args”：[“acp”]
    }
  }
}
````

### 泽德

Zed v0.221.x 及更高版本通过官方 ACP 注册表安装外部代理。

1. 打开代理面板。
2. 单击“**添加代理**”，或运行“zed: acpregistry”命令。
3. 搜索**爱马仕特工**。
4. 安装它并启动一个新的 OpenClaw 外部代理线程。

先决条件：

- 首先使用“hermes model”配置 OpenClaw 提供者凭据，或在“~/.hermes/.env”/“~/.hermes/config.yaml”中设置它们。
- 安装 `uv` 以便注册表启动器可以运行 `uvx --from 'hermes-agent[acp]==<version>' hermes-acp`。

对于注册表项可用之前的本地开发，请在 Zed 设置中使用自定义代理服务器：

```json
{
  “代理服务器”：{
    “爱马仕代理”：{
      “类型”：“自定义”，
      “命令”：“爱马仕”，
      “args”：[“acp”]
    }
  }
}
````

### JetBrains

使用 ACP 兼容插件并将其指向：

````文本
/路径/到/hermes-agent/acp_registry
````

## 注册表清单

OpenClaw 官方 ACP 注册表元数据的源副本位于：

````文本
acp_registry/agent.json
acp_registry/icon.svg
````

上游注册表 PR 将这些文件复制到“agentclientprotocol/registry”中的顶级“openclaw/”目录中。

该注册表项使用直接指向“openclaw”PyPI 版本的“uvx”发行版：

````文本
uvx --from 'hermes-agent[acp]==<版本>' Hermes-acp
````

注册表 CI 验证 PyPI 上是否存在固定版本，因此清单的“version”和 uvx“package”pin 必须始终与“pyproject.toml”匹配。 `scripts/release.py` 让它们自动保持同步。

## 配置和凭据

ACP 模式使用与 CLI 相同的 OpenClaw 配置：

- `~/.hermes/.env`
- `~/.hermes/config.yaml`
- `~/.hermes/技能/`
- `~/.hermes/state.db`

提供程序解析使用 OpenClaw 的正常运行时解析器，因此 ACP 继承当前配置的提供程序和凭据。 OpenClaw 还为首次运行的注册表客户端宣传了终端身份验证方法（`--setup`）；这将打开 OpenClaw 的交互式模型/提供商设置。

## 会话行为

当服务器运行时，ACP 会话由 ACP 适配器的内存中会话管理器进行跟踪。

每个会话存储：

- 会话ID
- 工作目录
- 选定的型号
- 当前对话历史记录
- 取消活动

底层的“AIAgent”仍然使用 OpenClaw 的正常持久性/日志记录路径，但 ACP“list/load/resume/fork”的范围仅限于当前运行的 ACP 服务器进程。

## 工作目录行为

ACP 会话将编辑器的 cwd 绑定到 OpenClaw 任务 ID，因此文件和终端工具相对于编辑器工作区而不是服务器进程 cwd 运行。

## 批准

危险的终端命令可以作为批准提示发送回编辑器。 ACP 批准选项比 CLI 流程更简单：

- 允许一次
- 始终允许
- 否认

如果出现超时或错误，批准桥会拒绝请求。

### 会话范围的编辑自动批准

ACP 公开了*允许一次*和*始终允许*之间的第三层：**允许会话**。从编辑器的权限提示中选择它仅记录当前 ACP 会话内的批准 - 该会话中的每个后续匹配命令都会在没有提示的情况下执行，但新的 ACP 会话（或重新启动编辑器）会重置石板并在第一次重新提示。

|选项 |编辑标签|范围 |重新启动后仍然存在 |
|---|---|---|---|
| `允许一次` |允许一次 |这一个工具调用 |没有 |
| `允许会话` |允许会话 |此 ACP 会话中的所有匹配呼叫 |否 — 会话结束时清除 |
| `允许_始终` |始终允许 |所有未来的会议 |是（写入 OpenClaw 永久许可名单）|
| `否认` |否认|这一个工具调用 |没有 |

“allow_session”是编辑器工作流程的正确默认值，您在任务期间信任代理，但不想授予长期允许列表条目。安全权衡很简单：范围越广，编辑器打断你的次数就越少，行为不当的代理（或提示注入）在你注意到之前造成的损害就越大。对于不熟悉的命令从“allow_once”开始；一旦您看到代理正确运行相同的模式几次，就升级为“allow_session”；为您永远信任的真正幂等命令保留“allow_always”（例如“git status”）。

ACP 桥将这些选项映射到 OpenClaw 的内部批准语义 - “allow_always” 以与 CLI 相同的方式写入永久允许列表条目，而“allow_session”仅影响当前 ACP 会话的进程内批准缓存。

## 故障排除

### ACP 代理未出现在编辑器中

检查：

- 在 Zed 中，使用“zed: acpregistry”打开 ACP 注册表并搜索 **OpenClaw**。
- 对于手动/本地开发，验证自定义“agent_servers”命令指向“hermes acp”。
- OpenClaw 已安装并位于您的 PATH 上。
- ACP 额外已安装（`pip install -e '.[acp]'`）。
- 如果从官方 Zed 注册表项启动，则会安装“uv”。

### ACP 启动但立即出错

尝试这些检查：

````bash
爱马仕 acp --版本
爱马仕 acp --检查
爱马仕医生
爱马仕状态
````

### 缺少凭据

ACP 模式使用 OpenClaw 现有的提供商设置。配置凭据：

````bash
爱马仕型号
````

或者通过编辑`~/.hermes/.env`。注册中心客户端还可以触发 OpenClaw 的终端身份验证流程，该流程运行相同的交互式提供程序/模型设置。

### Zed 注册表启动器找不到 uv

从官方 uv 安装文档安装 `uv`，然后从 Zed 重试 OpenClaw 线程。

## 另请参阅

- [ACP 内部结构](../../developer-guide/acp-internals.md)
- [提供商运行时解析](../../developer-guide/provider-runtime.md)
- [工具运行时](../../developer-guide/tools-runtime.md)