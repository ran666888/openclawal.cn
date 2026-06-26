---
sidebar_position: 8
sidebar_label: "Checkpoints & Rollback"
title: "Checkpoints and /rollback"
description: "Filesystem safety nets for destructive operations using shadow git repos and automatic snapshots"
---
# 检查点和 `/rollback`

OpenClaw 可以在**破坏性操作**之前自动为您的项目创建快照，并使用单个命令将其恢复。从 v2 开始，检查点是**选择加入** - 大多数用户从不使用“/rollback”，并且随着时间的推移，影子存储存储也很重要，因此默认设置是关闭的。

使用“--checkpoints”启用每个会话的检查点：

````bash
爱马仕聊天--检查点
````

或者在 `~/.hermes/config.yaml` 中全局启用：

````yaml
检查点：
  启用：真
````

这个安全网由内部 **Checkpoint Manager** 提供支持，该管理器在 `~/.hermes/checkpoints/store/` 下保留单个共享影子 git 存储库 - 您的真实项目 `.git` 永远不会被触及。代理工作的每个项目都共享同一个存储，因此 git 的内容可寻址对象数据库可以跨项目和跨轮次进行重复数据删除。

## 什么触发了检查点

检查点会在以下情况之前自动获取：

- **文件工具** — `write_file` 和 `patch`
- **破坏性终端命令** — `rm`、`rmdir`、`cp`、`install`、`mv`、`sed -i`、`truncate`、`dd`、`shred`、输出重定向 (`>`) 和 `git reset`/`clean`/`checkout`

代理每回合最多为每个目录创建一个检查点，因此长时间运行的会话不会发送垃圾邮件快照。

## 快速参考

会话中斜杠命令：

|命令|描述 |
|---------|-------------|
| `/回滚` |列出所有带有更改统计信息的检查点 |
| `/rollback <N>` |恢复到检查点 N（也撤消上次聊天回合）|
| `/rollback diff <N>` |预览检查点 N 和当前状态之间的差异 |
| `/rollback <N> <文件>` |从检查点 N | 恢复单个文件

用于在会话外检查和管理商店的 CLI：

|命令|描述 |
|---------|-------------|
| “爱马仕检查站” |显示总规模、项目数量、每个项目的细分 |
| `hermes 检查站状态` |与裸露的“检查点”相同 |
| `爱马仕检查站列表` | `status` 的别名 |
| `爱马仕检查站修剪` |强制清理：删除孤立/陈旧、GC、强制大小上限 |
| “爱马仕检查站已清除” |用核武器攻击整个检查站基地（首先询问）|
| “爱马仕检查站清除遗产” |仅删除 v1 迁移中的“legacy-*”存档 |

## 检查点如何工作

高层次上：

- OpenClaw 检测工具何时将**修改工作树中的文件**。
- 每个对话回合（每个目录）一次，它：
  - 解析文件的合理项目根。
  - 初始化或重用`~/.hermes/checkpoints/store/`处的**单个共享影子存储**。
  - 进入每个项目索引，构建树，并提交到每个项目引用（`refs/hermes/<project-hash>`）。
- 这些每个项目的引用形成一个检查点历史记录，您可以通过“/rollback”检查和恢复。

````美人鱼
流程图LR
  user["用户命令\n(hermes, 网关)"]
  代理[“AIAgent\n(run_agent.py)”]
  工具[“文件和终端工具”]
  cpMgr["检查点管理器"]
  store["共享影子存储\n~/.hermes/checkpoints/store/"]

  用户-->代理
  代理-->|“工具调用”|工具
  工具 -->|"mutate\nensure_checkpoint()"| 之前控制管理器
  cpMgr -->|"git add/commit-tree/update-ref"|商店
  cpMgr -->|“确定/跳过”|工具
  工具-->|“应用更改”|代理人
````

## 配置

在`~/.hermes/config.yaml`中配置：

````yaml
检查点：
  enabled: false # 主开关（默认值：false — 选择加入）
  max_snapshots: 20 # 每个项目的最大检查点（通过 ref rewrite + gc 强制执行）
  max_total_size_mb: 500 # 总存储大小的硬性上限；最旧的提交被删除
  max_file_size_mb: 10 # 跳过任何大于此值的单个文件

  # 自动维护（默认开启）：启动时扫描~/.hermes/checkpoints/
  # 并删除工作目录不再存在的项目条目
  # （孤儿）或者其last_touch 早于retention_days。最多运行
  # 每 min_interval_hours 一次，通过 .last_prune 标记跟踪。
  自动修剪：真
  保留天数：7
  删除孤儿：true
  最短间隔时间：24
````

要禁用一切：

````yaml
检查点：
  启用：假
  自动修剪：假
````

当“enabled: false”时，检查点管理器是无操作的，并且从不尝试 git 操作。当“auto_prune: false”时，存储会不断增长，直到您手动运行“hermes checkpoints prune”。

## 列出检查点

从 CLI 会话：

````
/回滚
````

OpenClaw 以显示更改统计信息的格式化列表进行响应：

````文本
📸 /path/to/project 的检查点：

  1. 4270a8c 2026-03-16 04:36 补丁前（1 个文件，+1/-0）
  2. eaf4c1f 2026-03-16 04:35 在 write_file 之前
  3. b3f9d2e 2026-03-16 04:34 在终端之前： sed -i s/old/new/ config.py （1 个文件，+1/-1）

  /rollback <N> 恢复到检查点 N
  /rollback diff <N> 预览自检查点 N 以来的更改
  /rollback <N> <file> 从检查点 N 恢复单个文件
````

## 从 Shell 检查 Store

````bash
赫尔墨斯检查站
````

示例输出：

````文本
检查点基地：/home/you/.hermes/checkpoints
总大小：142.3 MB
  存储/138.1 MB
  旧版-* 4.2 MB
项目：12

  WORKDIR 提交最后一次触摸状态
  /home/you/code/hermes-agent 20 2 小时前直播
  /home/you/code/experiments/rl-runner 8 1 天前直播
  /home/you/code/old-prototype 3 9天前孤儿
  ...

遗留档案（1）：
  旧版-20260506-050616 4.2 MB

清除：hermes 检查点clear-legacy
````

强制进行全面扫描（忽略 24 小时幂等标记）：

````bash
爱马仕检查站修剪 --retention-days 3 --max-size-mb 200
````

## 使用 `/rollback diff` 预览更改

在提交恢复之前，预览自检查点以来发生的更改：

````
/回滚差异1
````

这显示了 git diff stat 摘要，后跟实际差异。

## 使用 `/rollback` 恢复

````
/回滚1
````

赫尔墨斯在幕后：

1. 验证影子存储中是否存在目标提交。
2. 获取当前状态的**预回滚快照**，以便您稍后可以“撤消撤消”。
3. 恢复工作目录中的跟踪文件。
4. **撤消最后一次对话**，以便代理的上下文与恢复的文件系统状态相匹配。

## 单文件恢复

仅从检查点恢复一个文件，而不影响目录的其余部分：

````
/rollback 1 src/broken_file.py
````

## 安全和性能防护

- **Git 可用性** — 如果在 `PATH` 上找不到 `git`，则检查点将被透明禁用。
- **目录范围** — OpenClaw 会跳过过于宽泛的目录（根 `/`、主目录 `$HOME`）。
- **存储库大小** — 跳过包含超过 50,000 个文件的目录。
- **每个文件大小上限** — 大于“max_file_size_mb”（默认 10 MB）的文件将从快照中排除。防止意外吞咽数据集、模型权重或生成的媒体。
- **总存储大小上限** — 当存储超过“max_total_size_mb”（默认 500 MB）时，每个项目最旧的提交将循环删除，直到低于上限。
- **真正的修剪** - 通过重写每个项目的引用并随后运行 git gc --prune=now 来强制执行“max_snapshots”，因此松散的对象不会累积。
- **无更改快照** — 如果自上次快照以来没有任何更改，则跳过检查点。
- **非致命错误** — 检查点管理器内的所有错误均在调试级别记录；您的工具继续运行。

## 检查站所在地

````文本
〜/.hermes/检查点/
  ├── store/ # 单个共享裸git仓库
  │ ├── HEAD,objects/ # git 内部结构（跨项目共享）
  │ ├── refs/hermes/<hash> # 每个项目分支提示
  │ ├──indexes/<hash> # 每个项目的 git 索引
  │ ├──projects/<hash>.json # workdir +created_at+last_touch
  │ └── 信息/排除
  ├── .last_prune # 自动剪枝幂等标记
  └── Legacy-<ts>/ # 已存档的 pre-v2 每个项目影子存储库
````

每个“<hash>”都源自工作目录的绝对路径。您通常不需要手动触摸这些 - 使用 `hermes checkpoints status` / `prune` / `clear` 代替。

### 从 v1 迁移

在 v2 重写之前，每个工作目录直接在 `~/.hermes/checkpoints/<hash>/` 下都有自己完整的影子 git 存储库。该布局无法跨项目删除对象，并且具有记录的无操作修剪器 - 商店将无限增长。

在第一次 v2 运行时，任何 v2 之前的影子存储库都会移至 `~/.hermes/checkpoints/legacy-<timestamp>/` 中，以便新的单存储布局开始干净。通过使用“git”手动检查旧存档，旧的“/rollback”历史记录仍然可以访问；一旦您确信不需要它，请运行：

````bash
爱马仕检查站clear-legacy
````

来回收空间。在“retention_days”之后，旧档案也会被“auto_prune”清除。

## 最佳实践

- **仅在需要时启用检查点** - `hermes chat --checkpoints` 或每个配置文件 `enabled: true`。
- **在恢复之前使用`/rollback diff`** - 预览将发生的更改以选择正确的检查点。
- **当您只想撤消代理驱动的更改时，请使用 `/rollback` 而不是 `git reset`**。
- **如果您定期使用检查点，请偶尔检查“hermes 检查点状态” - 显示哪些项目处于活动状态以及商店的费用。
- **与 Git 工作树结合**以实现最大安全性 - 将每个 OpenClaw 会话保留在自己的工作树/分支中，并使用检查点作为额外层。

要在同一存储库上并行运行多个代理，请参阅 [Git worktrees](./git-worktrees.md) 上的指南。