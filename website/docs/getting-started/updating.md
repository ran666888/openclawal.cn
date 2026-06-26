---
sidebar_position: 3
title: "Updating & Uninstalling"
description: "如何更新 OpenClaw 到最新版本或卸载"
---
# 更新和卸载

## 更新中

### Git 安装

使用单个命令更新到最新版本：

````bash
爱马仕更新
````

这将从“main”中提取最新的代码，更新依赖项，并提示您配置自上次更新以来添加的任何新选项。

### pip 安装

PyPI 版本跟踪**标记版本**（主要和次要版本），而不是“main”上的每个提交。检查更新并升级：

````bash
hermes update --check # 查看 PyPI 上是否有更新版本
hermes update # 运行 pip install --upgrade hermes-agent
````

或者手动：

````bash
pip install --upgrade hermes-agent # 或: uv pip install --upgrade hermes-agent
````

:::提示
`hermes update` 会自动检测新的配置选项并提示您添加它们。如果您跳过该提示，您可以手动运行“hermes config check”来查看缺少的选项，然后运行“hermes config migrate”以交互方式添加它们。
:::

### 更新期间会发生什么（git 安装）

当您运行“hermes update”时，会发生以下步骤：

1. **配对数据快照** — 保存轻量级的更新前状态快照（涵盖`~/.hermes/pairing/`、飞书评论规则以及其他运行时修改的状态文件）。可通过[快照和回滚](../user-guide/checkpoints-and-rollback.md)中描述的快照恢复流程进行恢复，或者通过提取 OpenClaw 在“~/.hermes/”目录旁边写入的最新快速快照 zip 进行恢复。
2. **Git pull** — 从 `main` 分支拉取最新代码并更新子模块
3. **拉取后语法验证 + 自动回滚** — 拉取后，OpenClaw 会在启动时编译每个 `hermes` 调用导入的八个关键文件。如果有任何解析失败（例如，孤立的合并冲突标记、意外截断的文件），OpenClaw 会运行 `git reset --hard <pre-pull-sha>` 来回滚安装，以便您的 shell 保持可启动状态。一旦上游修复完成，请重新运行“hermes update”。
4. **依赖项安装** — 运行 `uv pip install -e ".[all]"` 以获取新的或更改的依赖项
5. **配置迁移** — 检测自您的版本以来添加的新配置选项并提示您设置它们
6. **网关自动重启** — 更新完成后刷新正在运行的网关，以便新代码立即生效。服务管理网关（Linux 上的 systemd，macOS 上的 launchd）通过服务管理器重新启动。当 OpenClaw 可以将运行的 PID 映射回配置文件时，手动网关会自动重新启动。

### 针对非默认分支进行更新：`--branch`

默认情况下，“hermes update”跟踪“origin/main”。通过 `--branch <name>` 来更新不同的分支 - 对于 QA 通道、功能分支或候选版本测试很有用：

````bash
爱马仕更新——分支发布候选
hermes update --check --branchexperimental # 仅预览落后
````

如果您的本地签出位于不同的分支上，OpenClaw 会自动隐藏任何未提交的工作，将 HEAD 切换到目标分支，然后拉取。本地不存在的分支会从 `origin/<name>` (`git checkout -B <name> origin/<name>`) 自动跟踪。任何地方都不存在的分支会彻底失败 - 您隐藏的更改会在退出之前恢复，因此您永远不会陷入奇怪的状态。在非“main”分支上，仅“main”分支上游同步逻辑会自动跳过。

### 非交互式更新的本地更改

当您在终端中运行“hermes update”时，OpenClaw 会隐藏任何未提交的源代码树更改，拉取，然后**询问**是否恢复它们 - 与往常一样。交互式更新没有任何变化。

当更新在**没有终端**的情况下运行时（通过桌面/聊天应用程序的“更新”按钮或网关触发的更新），不会出现应答提示。 `updates.non_interactive_local_changes` 设置决定您隐藏的更改会发生什么：

````yaml
# ~/.hermes/config.yaml
更新：
  non_interactive_local_changes: stash # 默认值：保留 + 自动恢复
  # non_interactive_local_changes:丢弃 # 丢弃本地源编辑
````

- `stash`（默认）— 自动存储、拉取，然后在更新的代码之上自动恢复您的更改。没有什么会失去；如果恢复遇到冲突，它们将保存在 git stash 中以供手动恢复。
- `discard` — 自动存储并在拉取后删除存储，因此更新始终落在干净的树上。仅在您从不打算对 OpenClaw 源代码保留本地编辑的计算机上使用此选项。它会隐藏（不是“git reset --hard”+“git clean -fd”），因此被忽略的路径（如“node_modules”、“venv”）和构建输出永远不会被触及。

在桌面应用程序中，这是**设置→高级→应用程序内更新本地更改**。

### 仅预览：`hermes update --check`

想知道在拉取之前是否有可用的更新吗？运行 `hermes update --check` — 对于 git 安装，它会获取提交并将其与 `origin/main` 进行比较；对于 pip 安装，它会查询 PyPI 的最新版本。没有修改任何文件，也没有重新启动网关。在控制“是否有更新”的脚本和 cron 作业中很有用。

### 完整的更新前备份：`--backup`

对于高价值的配置文件（生产网关、共享团队安装），您可以选择“HERMES_HOME”的完整预拉备份（配置、身份验证、会话、技能、配对）：

````bash
爱马仕更新--备份
````

或者将其设置为每次运行的默认值：

````yaml
# ~/.hermes/config.yaml
更新：
  pre_update_backup：true
````

“--backup”是早期版本中始终在线的行为，但它会为大型住宅的每次更新增加几分钟的时间，因此现在可以选择加入。上面的轻量级配对数据快照仍然无条件运行。

### Windows：另一个 `hermes.exe` 正在运行

在 Windows 上，如果“hermes update”检测到另一个“hermes.exe”进程将 venv 的入口点可执行文件保持打开状态，则“hermes update”将拒绝运行 - 最常见的是 OpenClaw 桌面应用程序的生成后端、另一个终端中打开的“hermes” REPL 或正在运行的网关：

````
$ 爱马仕更新
✗ 另一个 hermes.exe 正在运行：
    PID 12345 爱马仕.exe

  现在更新将无法覆盖 ...\venv\Scripts\hermes.exe，因为
  Windows 会阻止正在运行的可执行文件上的 REPLACE。

  关闭 Hermes Desktop，退出任何打开的“hermes” REPL，然后
  在重试之前停止网关（“hermes gateway stop”）。
  如果您已经这样做了，请使用“hermes update --force”覆盖
  确认这些进程不会写入 venv。
````

关闭列出的进程并重新运行。如果您确定并发进程不会干扰（很少见 - 通常仅在防病毒填充程序被错误归因时才有用），请传递“--force”以跳过检查。在这种情况下，更新程序仍将使用指数退避重试“.exe”重命名，并且在顽固锁定上，通过“MoveFileEx(MOVEFILE_DELAY_UNTIL_REBOOT)”安排下次重新启动的替换，以便更新可以完成。

预期输出如下：

````
$ 爱马仕更新
正在更新 Hermes 代理...
📥 正在提取最新代码...
已经是最新的了。  （或：更新 abc1234..def5678）
📦 正在更新依赖项...
✅ 依赖项已更新
🔍 正在检查新的配置选项...
✅ 配置是最新的（或者：找到 2 个新选项 - 正在运行迁移...）
🔄 正在重新启动网关...
✅ 网关重新启动
✅ 爱马仕代理更新成功！
````

### 推荐的更新后验证

`hermes update` 处理主要更新路径，但快速验证确认一切都顺利完成：

1. `git status --short` — 如果树意外变脏，请在继续之前检查
2. `hermes doctor` — 检查配置、依赖项和服务运行状况
3. `hermes --version` — 确认版本按预期升级
4.如果使用网关：`hermes gateway status`
5. 如果`doctor`报告npm审计问题：在标记的目录中运行`npmauditfix`

:::警告更新后工作树脏了
如果 `git status --short` 在 `hermes update` 之后显示意外的更改，请在继续之前停止并检查它们。这通常意味着在更新的代码之上重新应用本地修改，或者依赖步骤刷新锁定文件。
:::

### 如果您的终端在更新过程中断开连接

`hermes update` 可以保护自己免受意外终端丢失的影响：

- 更新忽略“SIGHUP”，因此关闭 SSH 会话或终端窗口不再会在安装过程中终止它。 `pip` 和 `git` 子进程继承了这种保护，因此 Python 环境不会因连接断开而处于半安装状态。
- 更新运行时，所有输出都会镜像到“~/.hermes/logs/update.log”。如果您的终端消失，请重新连接并检查日志以查看更新是否完成以及网关重启是否成功：

````bash
tail -f ~/.hermes/logs/update.log
````

- `Ctrl-C` (SIGINT) 和系统关闭 (SIGTERM) 仍然受到尊重 - 这些是故意取消，而不是意外。

您不再需要将“hermes update”包装在“screen”或“tmux”中以在终端掉落时幸存下来。

### 检查您当前的版本

````bash
爱马仕版
````

与 [GitHub 发布页面](https://github.com/NousResearch/openclaw/releases) 上的最新版本进行比较。

### 从消息平台更新

您还可以通过发送以下内容直接从 Telegram、Discord、Slack、WhatsApp 或 Teams 进行更新：

````
/更新
````

这会拉取最新代码、更新依赖项并重新启动正在运行的网关。机器人将在重新启动期间短暂离线（通常 5-15 秒），然后恢复。

### 手动更新

如果您手动安装（不是通过快速安装程序）：

````bash
cd /路径/到/hermes-agent
导出 VIRTUAL_ENV="$(pwd)/venv"

# 拉取最新代码
git pull origin 主要

# 重新安装（选择新的依赖项）
uv pip install -e ".[全部]"

# 检查新的配置选项
爱马仕配置检查
hermes config migrate # 交互式添加任何缺少的选项
````

### 回滚指令

如果更新出现问题，您可以回滚到以前的版本：

````bash
cd /路径/到/hermes-agent

# 列出最近的版本
git log --oneline -10

# 回滚到特定的提交
git checkout <提交哈希>
uv pip install -e ".[全部]"

# 如果正在运行，请重新启动网关
Hermes网关重启
````

要回滚到特定版本标签（替换之前的标签 - 例如最近版本，如“v2026.5.16”，或“git tag --sort=-version:refname”中的任何早期标签）：

````bash
git checkout vX.Y.Z
uv pip install -e ".[全部]"
````

:::警告
如果添加新选项，回滚可能会导致配置不兼容。回滚后运行“hermes config check”，如果遇到错误，请从“config.yaml”中删除任何无法识别的选项。
:::

### Nix 用户注意事项

如果您通过 Nix flake 安装，则通过 Nix 包管理器管理更新：

````bash
# 更新 flake 输入
nix flake 更新 Hermes-agent

# 或者用最新的重建
nix 配置文件升级 Hermes-agent
````

Nix 安装是不可变的 — 回滚由 Nix 的生成系统处理：

````bash
nix 配置文件回滚
````

请参阅 [Nix 设置](./nix-setup.md) 了解更多详细信息。

---

## 卸载

### Git 安装

````bash
爱马仕卸载
````

卸载程序使您可以选择保留配置文件（`~/.hermes/`）以供将来重新安装。

### pip 安装

````bash
pip 卸载 Hermes-agent
rm -rf ~/.hermes # 可选 — 如果您打算重新安装，请保留
````

### 手动卸载

````bash
rm -f ~/.local/bin/hermes
rm -rf /路径/到/hermes-agent
rm -rf ~/.hermes # 可选 — 如果您打算重新安装，请保留
````

:::信息
如果您将网关安装为系统服务，请先停止并禁用它：
````bash
爱马仕网关站
# Linux: systemctl --user 禁用 Hermes-gateway
# macOS: launchctl 删除 ai.hermes.gateway
````
:::