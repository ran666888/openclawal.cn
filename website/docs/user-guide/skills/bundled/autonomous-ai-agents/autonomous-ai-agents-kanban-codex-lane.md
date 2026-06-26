---
title: "Kanban Codex Lane"
sidebar_label: "Kanban Codex Lane"
description: "Use when a OpenClaw Kanban worker wants to run Codex CLI as an isolated implementation lane while OpenClaw keeps ownership of task lifecycle, reconciliation, tes..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 看板 Codex Lane 技能

当 OpenClaw 看板工作人员希望将 Codex CLI 作为独立的实施通道运行，同时 OpenClaw 保留任务生命周期、协调、测试和移交的所有权时使用。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `skills/autonomous-ai-agents/kanban-codex-lane` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|标签 | `kanban`, `codex`, `worktrees`, `autonomous-agents`, `prediction-market-bot` |
|相关技能| [`codex`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex)，[`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 看板 Codex Lane

## 概述

这项技能为看板工作人员定义了轻量级的 OpenClaw+Codex 双通道约定。 OpenClaw 始终是任务所有者：它调用“kanban_show”，决定 Codex 是否合适，创建或选择一个独立的工作区，启动和监视 Codex，协调任何差异，运行验证，并编写最终的“kanban_complete”或“kanban_block”切换。 Codex 只是一个输入通道。 Codex output is not a task completion signal, not a trusted reviewer, and not allowed to write durable Kanban state directly.

该约定的存在是为了让 OpenClaw 工作人员可以使用 Codex 来获得有限的实现帮助，而无需更改调度程序。调度员仍必须生成 OpenClaw 工人。 A worker may optionally spawn Codex inside its own run, then accept, partially accept, or reject the lane after independent review and tests.

## 何时使用

当所有这些都成立时，使用 Codex 通道：

- 看板任务是具有明确验收标准的编码、重构、文档、测试或机械迁移任务。
- OpenClaw 可以在一次运行中评估有界差异。
- 可以在独立的 git 工作树/分支中复制或签出存储库。
- OpenClaw可以在Codex退出后自行运行相关测试。
- 提示可以说明所有安全约束和不得更改的文件。

Do not use the Codex lane when any of these are true:

- The task requires human judgment that is not already captured in the Kanban body.
- 工作人员缺乏存储库访问权限、Codex 身份验证或协调结果的时间。
- The change touches secrets, credential stores, private user data, or production order-entry systems.
- A small direct edit is faster and safer than spawning another agent.
- The task is research-only and should produce a written handoff rather than a diff.
- 工人可能会倾向于仅根据食品法典自我报告来标记“完成”。

## 所有权规则

1. OpenClaw 拥有看板生命周期。 Codex 绝不能调用“kanban_complete”、“kanban_block”、“kanban_create”、网关消息传递或任何 OpenClaw 板 CLI 作为工作线程的替代品。
2.爱马仕拥有最终验收权。在经过审查和验证之前，将 Codex 提交/差异视为不受信任的补丁。
3. OpenClaw拥有测试执行权。 Codex may run tests, but those runs are advisory;使用存储库的规范包装器重复 OpenClaw 所需的验证。
4.爱马仕拥有安全。如果 Codex 更改安全边界、风险门、实时交易行为或秘密处理，即使测试通过，也要拒绝该通道。
5.爱马仕拥有清理权。 Kill stuck Codex processes and remove temporary worktrees when they are no longer needed.

## 所需的工作树和分支模式

切勿直接在共享脏结账中运行 Codex。使用将通道与看板任务联系起来的分支/工作树名称，并隔离不受信任的编辑。

推荐变量：

````bash
TASK_ID="${HERMES_KANBAN_TASK:-t_manual}"
REPO =“/路径/到/repo”
BASE="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
SAFE_TASK="$(printf '%s' "$TASK_ID" | tr -cd '[:alnum:]_-')"
BRANCH="codex/${SAFE_TASK}/$(date -u +%Y%m%d%H%M%S)"
WORKTREE="/tmp/${SAFE_TASK}-codex-lane"
````

创建隔离车道：

````bash
git -C "$REPO" fetch --all --prune
git -C "$REPO" worktree add -b "$BRANCH" "$WORKTREE" "$BASE"
git -C“$WORKTREE”状态--短--分支
````

如果当前看板工作区已经是为此任务创建的独立 git 工作树，则仅当“git status --short”干净（有意的 OpenClaw 编辑除外）时，您才可以在其中创建同级 Codex 分支。 Otherwise create a separate temporary worktree and cherry-pick or copy accepted commits back after reconciliation.

协调后清理：

````bash
git -C“$REPO”工作树删除“$WORKTREE”
git -C "$REPO"branch -D "$BRANCH" # 仅在复制/精挑细选或故意拒绝接受的提交之后
````

如果需要将工作树作为工件进行审查，则保留工作树；将其记录在“codex_lane.artifacts”中并在交接中提及。

## 法典能力检查

在生成 Codex 之前运行这些。缺少 Codex 是跳过通道的正常原因，如果 OpenClaw 可以直接执行任务，则不会成为任务障碍。

````bash
命令-v 代码
法典--版本
法典功能列表 | grep -i 目标 ||真实
````

如果需要“/goal”支持，请仅在检查可用性后启用或启动功能标志：

````bash
Codex 功能实现目标 ||真实
codex --启用目标 --version
````

身份验证可以通过“OPENAI_API_KEY”或 Codex CLI OAuth 状态（通常为“~/.codex/auth.json”）进行。不要打印令牌文件。缺少“OPENAI_API_KEY”并不能证明身份验证不可用。

## 模式选择

使用“codex exec”进行有限的一次性编辑，其中 Codex 应自行退出：

````蟒蛇
终端（
    command="codex exec --full-auto '$(cat /tmp/codex_prompt.md)'",
    工作目录=工作树，
    背景=真实，
    pty=真，
    notification_on_complete=真，
）
````

仅将 Codex `/goal` 用于受益于持久目标跟踪的更广泛的多步骤工作。在 PTY/tmux 会话中以交互方式启动，或者如果默认情况下禁用该功能，则使用“codex --enable goal”启动。保持目标的独立性：存储库路径、任务 ID、安全约束、允许范围、验收标准、测试和提交期望。

要粘贴到 Codex 中的“/goal”目标文本示例：

````文本
/goal 仅在此存储库中工作：<WORKTREE>。任务：<TASK_ID> <TITLE>。
Hermes 拥有看板生命周期；不要调用 Hermes 看板工具或消息传递。
在分支 <BRANCH> 上创建小型提交。请遵循提示中的 PMB 安全约束。
运行请求的验证命令并报告准确的输出。生成差异和摘要后停止。
````

不要将 `--yolo` 用于预测市场机器人或安全敏感的存储库。更喜欢在隔离工作树中使用 `--full-auto`，然后依赖 OpenClaw 协调。

## 快速施工

使用“templates/pmb-codex-lane-prompt.md”中的链接模板进行预测市场机器人工作。对于其他存储库，请保持相同的结构，并将特定于 PMB 的安全块替换为特定于存储库的不变量。

每个 Codex 提示必须包括：

- `task_id`、标题和完整的看板验收标准。
- 存储库路径、工作树路径、分支名称和允许的文件范围。
- 明确声明：OpenClaw 拥有看板生命周期； Codex 只是一个输入通道。
- 所需的输出：简明摘要、更改的文件、提交、测试运行和已知风险。
- 禁止的行为：秘密访问、外部消息传递、董事会突变、不相关的重构、依赖项升级（除非需要）。
- Codex 可能运行的验证命令以及 OpenClaw 随后将运行的命令。

对于 PMB，请逐字包含这些强制性安全约束：

````文本
PMB 安全约束：
- live-SIM 仅限纸质；不要添加或启用实时 REST 订单输入。
- 切勿使用市价订单。
- 不要添加执行交叉或绕过价格/风险检查。
- 不得伪造被动成交、成交、损益、订单状态或调节证据。
- 不要削弱风险门、限制、终止开关或故障关闭行为。
- 除非明确要求，否则将研究/选择放在 C++ 热路径之外。
- 请勿读取、打印、写入或要求机密/令牌/凭证。
````

## 监控、超时和终止行为

在后台启动长 Codex 通道，并提供 PTY 和完成通知：

````蟒蛇
结果=终端（
    命令 =“codex exec --full-auto '$(cat /tmp/codex_prompt.md)'”,
    工作目录=工作树，
    背景=真实，
    pty=真，
    notification_on_complete=真，
）
会话 ID = 结果[“会话 ID”]
````

不受干扰地监控：

````蟒蛇
流程（操作=“轮询”，session_id=session_id）
进程（操作=“日志”，session_id = session_id，限制= 200）
进程（操作=“等待”，session_id = session_id，超时= 300）
````

对于超过两分钟的通道，例如，每隔几分钟发送一次看板心跳。 `kanban_heartbeat(note="在 <WORKTREE> 中运行的 Codex 通道；等待测试/差异")`。

击杀条件：

- 任务的剩余运行时间预算没有有用的输出。
- Codex 请求机密、生产凭证或外部权限。
- Codex 尝试修改工作树之外的文件。
- Codex 开始不相关的重写或依赖项改动。
- Codex 仍在工作线程超时附近运行，并且不存在安全的部分工件。

杀死命令：

````蟒蛇
进程（操作=“杀死”，session_id = session_id）
````

终止后，检查“git status --short”，仅在安全的情况下保留有用的补丁，并记录“codex_lane.result：timed_out”或“rejected”以及具体的“rejected_reason”。

## 调节清单

OpenClaw 在接受任何 Codex 通道结果之前必须执行此检查表：

- [ ] `git -C <WORKTREE> status --short --branch` 仅显示预期文件。
- [ ] `git -C <WORKTREE> diff --stat` 和 `git diff` 已由 OpenClaw 审核。
- [ ] 不包含机密、凭据、生成的缓存、不相关的数据或本地工件。
- [ ] 保留 PMB 安全约束：无实时 REST 订单输入、无市价订单、无执行交叉、无虚假被动填充/盈亏、无风险门弱化、无秘密。
- [ ] Codex 提交足够小，可以干净地进行挑选或压缩。
- [ ] OpenClaw 自己运行规范测试，使用 OpenClaw 的“scripts/run_tests.sh”或其他存储库的存储库记录的包装器。
- [ ] 任何 Codex 运行的测试均与 OpenClaw 运行的测试分开列出。
- [ ] 接受的提交/差异已应用于 OpenClaw 拥有的工作区/分支。
- [ ] 被拒绝或部分工作有具体原因和工件路径（如果有用）。

验收结果：

-“已接受”：Codex 差异/提交经过审查、应用和验证。
- “部分”：一些法典工作在编辑或挑选后被接受；被拒绝的零件被记录下来。
-“已拒绝”：不接受法典变更；原因已记录。
- `timed_out`：Codex 超出了通道预算；有用的工件可能存在，也可能不存在。

## kanban_complete 元数据架构

对于考虑通道的每个任务，请将此对象包含在“metadata.codex_lane”下。如果未使用 Codex，请设置“used: false”并在“rejected_reason”或同级“notes”字段中解释原因。

```json
{
  “codex_lane”：{
    “二手”：真实，
    "mode": "执行|目标|跳过",
    "worktree": "/绝对/路径/到/codex/worktree",
    “分支”：“codex/t_caa69668/20260508100000”，
    "command": "codex exec --full-auto ...",
    "结果": "接受|拒绝|部分|超时",
    "accepted_commits": ["<sha1>", "<sha2>"],
    "rejected_reason": "完全接受时为空；否则具体原因",
    “测试运行”：[
      {“命令”：“scripts/run_tests.sh测试/工具/test_x.py”，“exit_code”：0，“所有者”：“hermes”}，
      {“命令”：“codex报告：npm测试”，“exit_code”：0，“所有者”：“codex”}
    ],
    “工件”：[“/绝对/路径/到/日志或补丁”]
  }
}
````

对于有意跳过 Codex 的任务：

```json
{
  “codex_lane”：{
    “已使用”：假，
    “模式”：“跳过”，
    “工作树”：空，
    “分支”：空，
    “命令”：空，
    "结果": "拒绝",
    “接受的提交”：[]，
    "rejected_reason": "直接 Hermes 编辑比生成 Codex 更小、更安全。",
    “测试运行”：[]，
    “文物”：[]
  }
}
````

## 常见陷阱

1. 将法典自我报告视为验证。始终检查 OpenClaw 的差异并重新运行测试。
2. 在用户的脏主结帐中运行 Codex。始终隔离在工作树/分支中。
3. 让 Codex 拥有看板。 Codex 可能会总结进展情况，但 OpenClaw 会记录董事会状态。
4. 忘记提示中的 PMB 安全不变量。缺少安全文本是车道设置失败。
5. 使用 `/goal` 进行快速编辑。除非需要持久的多步骤延续，否则首选“codex exec”。
6. 杀死一条卡住的车道而不记录原因。 `rejected_reason` 必须解释该决定。
7. 因为测试通过，所以接受广泛的不相关清理。仅拒绝或挑选范围内的更改。

## 验证清单

- [ ] Codex 仅在“命令 -v codex”、“codex --version”和可选目标功能检查后才被跳过或启动。
- [ ] Codex 仅在隔离的工作树/分支中运行。
- [ ] 提示包括任务范围、所有权规则、适用的 PMB 安全约束以及验证命令。
- [ ] OpenClaw 审查了 `git diff` 和安全敏感文件。
- [ ] OpenClaw 独立运行规范测试。
- [ ] `kanban_complete.metadata.codex_lane` 遵循上面的架构。
- [ ] 临时进程和不必要的工作树已清理。