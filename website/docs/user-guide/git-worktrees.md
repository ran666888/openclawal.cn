---
sidebar_position: 3
sidebar_label: "Git Worktrees"
title: "Git Worktrees"
description: "Run multiple OpenClaw agents safely on the same repository using git worktrees and isolated checkouts"
---
# Git 工作树

OpenClaw 通常用于大型、寿命长的存储库。当您想要：

- 在同一个项目上并行运行**多个代理，或者
- 将实验性重构与主分支隔离，

Git **工作树**是为每个代理提供自己的签出而无需复制整个存储库的最安全方法。

本页展示了如何将工作树与 OpenClaw 结合起来，以便每个会话都有一个干净、独立的工作目录。

## 为什么将工作树与 OpenClaw 一起使用？

OpenClaw 将 **当前工作目录** 视为项目根目录：

- CLI：运行“hermes”或“hermes chat”的目录
- 消息网关：由 `~/.hermes/config.yaml` 中的 `terminal.cwd` 设置的目录

如果您在**同一个结账**中运行多个代理，它们的更改可能会相互干扰：

- 一个代理可以删除或重写另一个代理正在使用的文件。
- 很难理解哪些变化属于哪个实验。

通过工作树，每个代理可以获得：

- 它**自己的分支和工作目录**
- 它的**自己的检查点管理器历史记录**为`/rollback`

另请参阅：[检查点和/rollback](./checkpoints-and-rollback.md)。

## 快速入门：创建工作树

从您的主存储库（包含“.git/”）中，为功能分支创建一个新的工作树：

````bash
# 来自主仓库根目录
cd /路径/到/你的/存储库

# 在 ../repo-feature 中创建一个新的分支和工作树
git worktree add ../repo-feature feature/hermes-experiment
````

这将创建：

- 一个新目录：`../repo-feature`
- 一个新分支：`feature/hermes-experiment` 在该目录中签出

现在你可以 cd 进入新的工作树并在那里运行 OpenClaw：

````bash
cd ../repo-feature

# 在工作树中启动 Hermes
爱马仕
````

爱马仕将：

- 将“../repo-feature”视为项目根。
- 使用该目录保存上下文文件、代码编辑和工具。
- 对作用于该工作树的“/rollback”使用**单独的检查点历史记录**。

## 并行运行多个代理

您可以创建多个工作树，每个工作树都有自己的分支：

````bash
cd /路径/到/你的/存储库

git worktree add ../repo-experiment-a feature/hermes-a
git worktree add ../repo-experiment-b feature/hermes-b
````

在单独的航站楼中：

````bash
# 1 号航站楼
cd ../repo-实验-a
爱马仕

# 2 号航站楼
cd ../repo-实验-b
爱马仕
````

每个爱马仕工艺：

- 在自己的分支上工作（“feature/hermes-a”与“feature/hermes-b”）。
- 在不同的影子存储库哈希下写入检查点（从工作树路径派生）。
- 可以独立使用`/rollback`而不影响其他。

这在以下情况下特别有用：

- 运行批量重构。
- 尝试不同的方法来完成同一任务。
- 将 CLI + 网关会话与相同的上游存储库配对。

## 安全清理工作树

完成实验后：

1. 决定保留或丢弃该作品。
2. 如果您想保留它：
   - 像往常一样将分支合并到主分支中。
3. 删除工作树：

````bash
cd /路径/到/你的/存储库

# 删除worktree目录及其引用
git worktree 删除 ../repo-feature
````

注意事项：

- `git worktree remove` 将拒绝删除未提交更改的工作树，除非您强制执行。
- 删除工作树**不会**自动删除分支；您可以使用普通的“git分支”命令删除或保留分支。
- 当您删除工作树时，`~/.hermes/checkpoints/` 下的 OpenClaw 检查点数据不会自动修剪，但它通常非常小。

## 最佳实践

- **每个 OpenClaw 实验一个工作树**
  - 为每个重大更改创建专用分支/工作树。
  - 这使得差异集中，PR 较小且可审查。
- **实验后命名分支**
  - 例如`feature/hermes-checkpoints-docs`、`feature/hermes-refactor-tests`。
- **经常提交**
  - 使用 git 提交来实现高级里程碑。
  - 使用 [checkpoints 和 /rollback](./checkpoints-and-rollback.md) 作为工具驱动编辑的安全网。
- **使用工作树时避免从裸仓库根运行 OpenClaw**
  - 更喜欢工作树目录，因此每个代理都有明确的范围。

## 使用 `hermes -w` （自动工作树模式）

OpenClaw 有一个内置的“-w”标志，它**自动创建一个具有自己分支的一次性 git 工作树**。您不需要手动设置工作树 - 只需将“cd”放入您的存储库并运行：

````bash
cd /路径/到/你的/存储库
爱马仕-w
````

爱马仕将：

- 在您的存储库中的“.worktrees/”下创建一个临时工作树。
- 检查一个孤立的分支（例如 `hermes/hermes-<hash>`）。
- 在该工作树内运行完整的 CLI 会话。

这是获得工作树隔离的最简单方法。您还可以将其与单个查询结合起来：

````bash
Hermes -w -z“修复问题 #123”
````

对于并行代理，打开多个终端并在每个终端中运行“hermes -w”——每个调用都会自动获得自己的工作树和分支。

## 将它们放在一起

- 使用 **git worktrees** 为每个 OpenClaw 会话提供自己的干净结账。
- 使用**分支**来捕获实验的高级历史记录。
- 使用 **检查点 + `/rollback`** 从每个工作树内的错误中恢复。

这种组合为您提供：

- 强有力的保证不同的代理和实验不会互相踩踏。
- 快速迭代周期，可轻松从错误编辑中恢复。
- 干净、可审查的拉取请求。