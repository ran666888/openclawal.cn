---
sidebar_position: 2
---
# 配置文件：运行多个代理

在同一台机器上运行多个独立的 OpenClaw 代理 - 每个代理都有自己的配置、API 密钥、内存、会话、技能和网关状态。

## 什么是配置文件？

配置文件是一个单独的 OpenClaw 主目录。每个配置文件都有自己的目录，其中包含自己的“config.yaml”、“.env”、“SOUL.md”、内存、会话、技能、cron 作业和状态数据库。配置文件允许您为不同的目的运行单独的代理——编码助理、个人机器人、研究代理——而不会混淆 OpenClaw 状态。

当您创建配置文件时，它会自动成为自己的命令。创建一个名为“编码器”的配置文件，您将立即拥有“编码器聊天”、“编码器设置”、“编码器网关启动”等。

## 快速开始

````bash
hermes profile create coder # 创建配置文件+“coder”命令别名
编码器设置 # 配置 API 密钥和模型
编码器聊天#开始聊天
````

就是这样。 “coder”现在是它自己的 OpenClaw 配置文件，拥有自己的配置、内存和状态。

## 创建个人资料

:::提示
最快的设置：在新配置文件中运行“hermes setup --portal”以立即连接模型+工具。请参阅[Nous 门户](/integrations/nous-portal)。
:::

### 空白个人资料

````bash
爱马仕个人资料创建mybot
````

创建一个包含捆绑技能种子的全新个人资料。运行“mybot setup”来配置 API 密钥、模型和网关令牌。

如果您计划将此配置文件用作看板工作人员（或者希望看板编排器将工作路由到它），请在创建时传递`--description“<role>”`，以便编排器知道它擅长什么：

````bash
Hermes Profile create Researcher --description “读取源代码和外部文档，写入研究结果。”
````

您还可以稍后使用“hermes profile描述”设置或自动生成描述 - 有关完整的路由模型，请参阅[看板指南](./features/kanban#auto-vs-manual-orchestration)。

### 仅克隆配置（`--clone`）

````bash
爱马仕个人资料创建工作--克隆
````

将当前配置文件的 `config.yaml`、`.env`、`SOUL.md` 和技能复制到新配置文件中。相同的 API 密钥、模型和功能，但会话和内存是全新的。编辑“~/.hermes/profiles/work/.env”以获取不同的 API 密钥，或编辑“~/.hermes/profiles/work/SOUL.md”以获取不同的个性。

### 克隆所有内容（`--clone-all`）

````bash
Hermes 配置文件创建备份 --clone-all
````

复制**一切** — 配置、API 密钥、个性、所有记忆、技能、cron 作业、插件。完整的工作快照。每个配置文件的历史记录被排除在外（会话历史记录、“state.db”、“backups/”、“state-snapshots/”、“checkpoints/”）——这些属于源配置文件，可以达到数十 GB。对于包括历史记录的完整备份，请改用“hermes 配置文件导出”或“hermes 备份”。

### 从特定配置文件克隆

````bash
Hermes 配置文件创建工作 --clone-from coder
````

`--clone-from <source>` 直接选择源配置文件并暗示 config/skills/SOUL 克隆。当您想要该源配置文件的完整副本时，将其与“--clone-all”结合使用：

````bash
Hermes 配置文件创建工作备份 --clone-from coder --clone-all
````

:::提示 Honcho 记忆 + 配置文件
启用 Honcho 后，克隆操作会自动为新配置文件创建专用的 AI 对等点，同时共享相同的用户工作空间。每个档案都有自己的观察结果和身份。有关详细信息，请参阅 [Honcho -- 多代理/配置文件](./features/memory-providers.md#honcho)。
:::

## 使用配置文件

### 命令别名

每个配置文件都会自动在`~/.local/bin/<name>`处获取一个命令别名：

````bash
编码器聊天 # 与编码器代理聊天
编码器设置 # 配置编码器的设置
coder gateway start # 启动 coder 的网关
coder doctor # 检查 coder 的健康状况
编码员技能列表 # 列出编码员的技能
编码器配置集 model.default anthropic/claude-sonnet-4
````

该别名适用于每个 OpenClaw 子命令 - 它只是底层的“hermes -p <name>”。

### `-p` 标志

您还可以使用任何命令显式定位配置文件：

````bash
Hermes -p 编码器聊天
Hermes --profile=编码员医生
hermes chat -p coder -q "hello" # 适用于任何位置
````

### 粘性默认值（`hermes 配置文件使用`）

````bash
Hermes 配置文件使用编码器
Hermes 聊天 # 现在针对编码员
Hermes Tools # 配置编码器的工具
hermes配置文件使用默认#切换回来
````

设置默认值，以便简单的“hermes”命令以该配置文件为目标。就像“kubectl config use-context”一样。

### 知道你在哪里

CLI 始终显示哪个配置文件处于活动状态：

- **提示**：`coder ❯` 而不是 `❯`
- **横幅**：启动时显示“配置文件：编码器”
- **`hermes profile`**：显示当前配置文件名称、路径、型号、网关状态

## 配置文件、工作区、沙箱

配置文件经常与工作区或沙箱混淆，但它们是不同的东西：

- **配置文件**为 OpenClaw 提供了自己的状态目录：`config.yaml`、`.env`、`SOUL.md`、会话、内存、日志、cron 作业和网关状态。
- **工作空间**或**工作目录**是终端命令开始的地方。这是由“terminal.cwd”单独控制的。
- **沙箱**限制文件系统访问。配置文件不会**对代理进行沙箱处理。

在默认的“本地”终端后端，代理仍然具有与您的用户帐户相同的文件系统访问权限。配置文件不会阻止它访问配置文件目录之外的文件夹。

如果您希望配置文件在特定项目文件夹中启动，请在该配置文件的“config.yaml”中设置显式绝对“terminal.cwd”：

````yaml
终端：
  后端：本地
  cwd：/绝对/路径/到/项目
````

在本地后端使用 `cwd: "."` 意味着“启动 OpenClaw 的目录”，而不是“配置文件目录”。

另请注意：

- `SOUL.md` 可以指导模型，但它不强制执行工作空间边界。
- 对“SOUL.md”的更改在新会话中完全生效。现有会话可能仍在使用旧的提示状态。
- 询问模型“你在哪个目录中？”不是可靠的隔离测试。如果您需要一个可预测的工具起始目录，请明确设置“terminal.cwd”。

## 运行网关

每个配置文件都将自己的网关作为单独的进程运行，并具有自己的机器人令牌：

````bash
coder gateway start # 启动 coder 的网关
Assistant gateway start # 启动助手的网关（单独的进程）
````

### 不同的机器人令牌

每个配置文件都有自己的“.env”文件。在每个中配置不同的 Telegram/Discord/Slack 机器人令牌：

````bash
# 编辑编码器的标记
纳米 ~/.hermes/profiles/coder/.env

# 编辑助手的标记
纳米 ~/.hermes/profiles/assistant/.env
````

### 安全：令牌锁

如果两个配置文件意外使用相同的机器人令牌，则第二个网关将被阻止，并出现命名冲突配置文件的明显错误。支持 Telegram、Discord、Slack、WhatsApp 和 Signal。

### 持久服务

````bash
coder gateway install # 创建 hermes-gateway-coder systemd/launchd 服务
Assistant gateway install # 创建 Hermes-gateway-assistant 服务
````

每个配置文件都有自己的服务名称。他们独立运行。

:::note 官方 Docker 镜像内部
每个配置文件的网关由 [s6-overlay](https://github.com/just-containers/s6-overlay)（容器中的 PID 1）监管，因此 `hermes profile create <name>` 自动在 `/run/service/gateway-<name>/` 处注册一个 s6 服务槽。 `hermes -p <name> gateway start/stop/restart` 分派到 `s6-svc` 而不是生成一个裸进程 - 崩溃会自动重新启动，而 `docker restart` 会保留之前运行的网关集。有关详细信息，请参阅[每个配置文件网关监管](/user-guide/docker#per-profile-gateway-supervision)。
:::

## 配置配置文件

每个配置文件都有自己的：

- **`config.yaml`** — 模型、提供程序、工具集、所有设置
- **`.env`** — API 密钥、机器人令牌
- **`SOUL.md`** — 个性和说明

````bash
编码器配置集 model.default anthropic/claude-sonnet-4
echo “你是一位专注的编码助手。” > ~/.hermes/profiles/coder/SOUL.md
````

如果您希望此配置文件默认在特定项目中工作，还可以设置其自己的“terminal.cwd”：

````bash
编码器配置集terminal.cwd /绝对/路径/到/项目
````

### 从仪表板

[网络仪表板](features/web-dashboard.md#managing-multiple-profiles)
是一个机器级表面，可以管理**任何**配置文件的配置、API
键、技能、MCP 和模型（通过侧边栏中的配置文件切换器）- 否
需要每个配置文件仪表板。 “编码器仪表板”路由到机器
预先选择了“编码器”配置文件的仪表板。仪表板的“聊天”选项卡
也跟随切换器，在选定的选项下生成对话
个人资料的主页。

注意：仪表板的“配置文件”页面上的“设置为活动”是粘性的
**未来 CLI/网关运行**的默认值（与“hermes 配置文件使用”相同）-
要从仪表板编辑配置文件，请改用切换器。

## 更新中

`hermes update` 一次提取代码（共享）并自动将新的捆绑技能同步到**所有**配置文件：

````bash
爱马仕更新
# → 代码已更新（12 次提交）
# → 技能已同步：默认（最新）、编码器（+2 个新）、助理（+2 个新）
````

用户修改的技能永远不会被覆盖。

## 管理个人资料

````bash
Hermes 配置文件列表 # 显示所有配置文件的状态
hermes profile show coder # 一个配置文件的详细信息
Hermes 配置文件重命名编码器 dev-bot # 重命名（更新别名 + 服务）
Hermes 配置文件导出编码器 # 导出到 coder.tar.gz
Hermes 配置文件 import coder.tar.gz # 从存档导入
````

## 删除个人资料

````bash
爱马仕个人资料删除编码器
````

这将停止网关、删除 systemd/launchd 服务、删除命令别名并删除所有配置文件数据。系统会要求您输入个人资料名称进行确认。

使用 `--yes` 跳过确认：`hermes profile delete coder --yes`

:::注意
您无法删除默认配置文件（`~/.hermes`）。要删除所有内容，请使用“hermes uninstall”。
:::

## 制表符补全

````bash
# 重击
eval "$(hermes 完成 bash)"

# 兹什
eval "$(hermes 完成 zsh)"
````

将行添加到“~/.bashrc”或“~/.zshrc”以实现持久完成。完成“-p”、配置文件子命令和顶级命令之后的配置文件名称。

## 它是如何工作的

配置文件使用 `HERMES_HOME` 环境变量。当您运行“coder chat”时，包装器脚本会在启动 OpenClaw 之前设置“HERMES_HOME=~/.hermes/profiles/coder”。由于代码库中的 119 个以上文件通过“get_hermes_home()”解析路径，OpenClaw 状态会自动将范围限定到配置文件的目录 — 配置、会话、内存、技能、状态数据库、网关 PID、日志和 cron 作业。

这与终端工作目录是分开的。工具执行从 `terminal.cwd` （或本地后端上 `cwd: "."` 时的启动目录）开始，而不是自动从 `HERMES_HOME` 开始。

在主机安装上，工具子进程默认保留您真正的操作系统用户“HOME”，因此
`~` 下的现有 CLI 凭据继续跨配置文件工作。个人资料数据是
通过“HERMES_HOME”隔离，而不是通过更改“HOME”。容器后端仍在使用
`{HERMES_HOME}/home` 用于持久工具状态，并托管需要严格的用户
每个配置文件工具配置可以选择使用 `terminal.home_mode: profile`。

这意味着两件事很容易混淆：

- `HERMES_HOME` 是配置文件边界。它控制 OpenClaw 配置，`.env`，
  内存、会话、技能、日志、cron 作业、网关状态和其他 OpenClaw
  数据。
- `HOME` 是外部 CLI 期望的操作系统/用户主目录。在主机上
  安装后，OpenClaw 默认将其保留为真实用户主目录，因此像这样的工具
  `git`、`ssh`、`gh`、`az`、`npm`、Claude Code 和 Codex 找到相同的内容
  他们在您的普通 shell 中使用的凭据。

权衡是主机配置文件默认共享正常的用户级 CLI 状态。
如果每个配置文件需要单独的 CLI 身份，请设置 `terminal.home_mode：
该配置文件的“config.yaml”中的“profile”。在这种模式下 OpenClaw 推出工具
带有 `HOME={HERMES_HOME}/home` 的子进程；然后你需要初始化或链接
特定于配置文件的 `~/.ssh`、`~/.gitconfig`、`~/.config/gh`、云 CLI 身份验证、
Claude/Codex auth、npm state 以及该配置文件主目录中的类似文件。

OpenClaw 还将“HERMES_REAL_HOME”暴露给子进程，以便脚本仍然可以找到
当 `home_mode: profile` 处于活动状态时的实际帐户主页。

默认配置文件就是 `~/.hermes` 本身。无需迁移——现有安装的工作方式相同。

## 将配置文件共享为发行版

您在一台计算机上构建的配置文件可以打包为 **git 存储库**，并使用一个命令安装在另一台计算机上 - 您自己的工作站、队友的笔记本电脑或社区用户的环境。共享包包括 SOUL、配置、技能、cron 作业和 MCP 连接。凭证、内存和会话保留在每台机器上。

````bash
# 从 git 存储库安装整个代理
Hermes 配置文件安装 github.com/you/research-bot --alias

# 稍后当作者发布新版本时更新（保留你的记忆+.env）
爱马仕个人资料更新研究机器人
````

请参阅 **[Profile Distributions：共享整个代理](./profile-distributions.md)** 以获取完整指南 — 创作、发布、更新语义、安全模型和用例。