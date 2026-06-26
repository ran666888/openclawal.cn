---
sidebar_position: 1
title: "Tools & Toolsets"
description: "Overview of OpenClaw的 tools — what's available, how toolsets work, and terminal backends"
---
# 工具和工具集

工具是扩展代理能力的功能。它们被组织成逻辑**工具集**，可以在每个平台上启用或禁用。

## 可用工具

OpenClaw 附带了广泛的内置工具注册表，涵盖网络搜索、浏览器自动化、终端执行、文件编辑、内存、委派、强化学习训练、消息传递、家庭助理等。

:::注意
**Honcho 跨会话内存** 作为内存提供程序插件 (`plugins/memory/honcho/`) 提供，而不是作为内置工具集。安装请参见[插件](./plugins.md)。
:::

高级别类别：

|类别 |示例 |描述 |
|----------|----------|------------|
| **网络** | `web_search`、`web_extract` |搜索网络并提取页面内容。 |
| **X 搜索** | `x_搜索` |通过 xAI 的内置“x_search”响应工具搜索 X (Twitter) 帖子和线程 — 通过 xAI 凭证（SuperGrok OAuth 或“XAI_API_KEY”）进行控制；默认关闭，通过“hermes 工具”→ 🐦 X (Twitter) 搜索选择加入。 |
| **终端和文件** | `终端`、`进程`、`读取文件`、`补丁` |执行命令并操作文件。 |
| **浏览器** | `browser_navigate`、`browser_snapshot`、`browser_vision` |具有文本和视觉支持的交互式浏览器自动化。 |
| **媒体** | `vision_analyze`、`image_generate`、`text_to_speech` |多模态分析和生成。 |
| **代理编排** | `todo`、`clarify`、`execute_code`、`delegate_task` |规划、澄清、代码执行和子代理委托。 |
| **记忆与回忆** | `内存`、`会话搜索` |持久内存和会话搜索。 |
| **自动化与交付** | `cronjob`、`send_message` |具有创建/列表/更新/暂停/恢复/运行/删除操作的计划任务，以及出站消息传递。 |
| **集成** | `ha_*`，MCP 服务器工具 |家庭助理、MCP 和其他集成。 |

对于权威的代码派生注册表，请参阅[内置工具参考](/reference/tools-reference)和[工具集参考](/reference/toolsets-reference)。

:::tip Nous 工具网关
付费 [Nous Portal](https://portal.nousresearch.com) 订阅者可以通过 **[工具网关](tool-gateway.md)** 使用网络搜索、图像生成、TTS 和浏览器自动化 - 无需单独的 API 密钥。运行“hermes model”来启用它，或使用“hermes tools”配置单个工具。
:::

## 使用工具集

````bash
# 使用特定的工具集
Hermes 聊天工具集“网络、终端”

# 查看所有可用的工具
爱马仕工具

# 配置每个平台的工具（交互式）
爱马仕工具
````

常用工具集包括“web”、“search”、“terminal”、“file”、“browser”、“vision”、“image_gen”、“moa”、“skills”、“tts”、“todo”、“memory”、“session_search”、“cronjob”、“code_execution”、“delegation”、“clarify”、“homeassistant”、“messaging”、“spotify”、 “discord”、“discord_admin”、“调试”和“安全”。

有关全套工具集，请参阅[工具集参考](/reference/toolsets-reference)，包括“hermes-cli”、“hermes-telegram”等平台预设，以及“mcp-<server>”等动态 MCP 工具集。

## 终端后端

终端工具可以在不同环境下执行命令：

|后端 |描述 |使用案例|
|---------|-------------|----------|
| `本地` |在您的机器上运行（默认）|开发，可信任务|
| `码头工人` |隔离容器|安全性、再现性|
| `ssh` |远程服务器 |沙箱，让代理远离自己的代码 |
| `奇点` | HPC 容器 |集群计算，无根 |
| `模态` |云执行|无服务器、规模 |
| '代托纳' |云沙箱工作区 |持久的远程开发环境|

### 配置

````yaml
# 在 ~/.hermes/config.yaml 中
终端：
  后端：本地 # 或：docker、ssh、singularity、modal、daytona
  CW：“。”          # 工作目录
  timeout: 180 # 命令超时时间（以秒为单位）
````

### Docker 后端

````yaml
终端：
  后端：码头工人
  docker_image: python:3.11-slim
````

**一个持久容器，在整个进程中共享。** OpenClaw 在第一次使用时启动一个长期存在的容器（`docker run -d ... sleep 2h`），并通过 `docker exec` 将每个终端、文件和 `execute_code` 调用路由到同一个容器中。在 OpenClaw 进程的生命周期中，工作目录更改、安装的软件包、环境调整以及写入“/workspace”的文件都会通过“/new”、“/reset”和“delegate_task”子代理从一个工具调用转移到下一个工具调用。容器在关闭时停止并移除。

这意味着 Docker 后端的行为就像一个持久的沙箱虚拟机，而不是每个命令一个新的容器。如果您“pip install foo”一次，它将在会话的其余部分中保留。如果您“cd /workspace/project”，后续的“ls”调用将看到该目录。请参阅 [配置 → Docker 后端](../configuration.md#docker-backend) 了解完整的生命周期详细信息以及控制 `/workspace` 和 `/root` 是否在 OpenClaw 重新启动后继续存在的 `container_persistent` 标志。

### SSH 后端

出于安全考虑，推荐使用 - 代理无法修改自己的代码：

````yaml
终端：
  后端：ssh
````
````bash
# 在 ~/.hermes/.env 中设置凭据
TERMINAL_SSH_HOST=my-server.example.com
TERMINAL_SSH_USER=我的用户
TERMINAL_SSH_KEY=~/.ssh/id_rsa
````

### 奇点/Apptainer

````bash
# 为并行工作人员预构建 SIF
apptainer build ~/python.sif docker://python:3.11-slim

# 配置
爱马仕配置设置terminal.backend奇异性
Hermes 配置集terminal.singularity_image ~/python.sif
````

### 模态（无服务器云）

````bash
uv pip 安装模式
模态设置
Hermes 配置设置terminal.backend modal
````

### 容器资源

为所有容器后端配置 CPU、内存、磁盘和持久性：

````yaml
终端：
  后端：docker#或singularity、modal、daytona
  container_cpu: 1 # CPU 核心数（默认值：1）
  container_memory: 5120 # 内存（以 MB 为单位）（默认值：5GB）
  container_disk: 51200 # 磁盘（以 MB 为单位）（默认值：50GB）
  container_persistent: true # 跨会话保留文件系统（默认值：true）
````

当“container_persistent: true”时，已安装的包、文件和配置在会话中保留。

### 容器安全

所有容器后端都运行安全强化：

- 只读根文件系统（Docker）
- 所有 Linux 功能均已下降
- 没有权限升级
- PID限制（256个进程）
- 完全命名空间隔离
- 通过卷持久工作区，不可写根层

Docker 可以选择通过“terminal.docker_forward_env”接收显式环境允许列表，但转发的变量对容器内的命令可见，并且应被视为暴露给该会话。

## 后台进程管理

启动后台进程并管理它们：

````蟒蛇
终端（命令=“pytest -v测试/”，背景= true）
# 返回：{"session_id": "proc_abc123", "pid": 12345}

# 然后用process工具进行管理：
process(action="list") # 显示所有正在运行的进程
process(action="poll", session_id="proc_abc123") # 检查状态
process(action="wait", session_id="proc_abc123") # 阻塞直到完成
process(action="log", session_id="proc_abc123") # 完整输出
process(action="kill", session_id="proc_abc123") # 终止
process(action="write", session_id="proc_abc123", data="y") # 发送输入
````

PTY 模式 (`pty=true`) 启用交互式 CLI 工具，例如 Codex 和 Claude Code。

## 须藤支持

如果命令需要 sudo，系统会提示您输入密码（为会话缓存）。或者在`~/.hermes/.env`中设置`SUDO_PASSWORD`。

:::警告
在消息传递平台上，如果 sudo 失败，输出会包含将“SUDO_PASSWORD”添加到“~/.hermes/.env”的提示。
:::