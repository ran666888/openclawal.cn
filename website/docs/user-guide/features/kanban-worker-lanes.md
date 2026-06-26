# 看板工人通道

**工作通道**是看板调度程序可以将任务路由到的一类流程。每个通道都有一个身份（受让人字符串）、一个生成机制以及生成后必须对任务执行的操作的合同。

此页是合同。它的存在面向两种受众：

- **操作员** 选择将哪些通道连接到板上（要创建哪些配置文件，要使用哪些受让人）。
- **插件/集成作者**想要添加新的通道形状（包装 Codex / Claude Code / OpenCode 的 CLI 工作器、容器化审查工作器、通过 API 拉取任务的非 OpenClaw 服务）。

如果您正在编写工作人员代码本身（在通道内*运行的代理），看板生命周期和参考详细信息将自动注入工作人员的系统提示中（[`agent/prompt_builder.py`](https://github.com/NousResearch/openclaw/blob/main/agent/prompt_builder.py)中的`KANBAN_GUIDANCE`块）。

## 层次结构

````文本
Hermes 看板 = 规范任务生命周期 + 审计跟踪
工作通道 = 一张分配卡的实施执行者
审阅者 = 控制“完成”的人类或人类代理
GitHub PR = 可上游工件（可选，用于代码通道）
````

OpenClaw 看板拥有生命周期真相——“就绪”→“运行”→“已阻止”/“已完成”/“已归档”。工人通道执行工作，但从不承认这一事实；他们所做的一切都通过“kanban_*”工具（或者，对于非 OpenClaw 外部工作人员，通过 API）流回看板内核。审阅者控制从“编写代码更改”到“完成任务”的转变。

## 车道提供什么

要成为看板工作通道，集成必须提供三件事：

### 1. 受让人字符串

调度程序将“task.assignee”与 OpenClaw 配置文件名称（默认通道形状）或已注册的不可生成标识符（插件通道形状 - 请参阅下面的[添加外部 CLI 工作通道](#adding-an-external-cli-worker-lane)）进行匹配。受让人未解决的任务将保留为“就绪”状态，并带有“skipped_nonspawnable”事件，以便董事会操作员可以修复它们；它们不会被任意后备默默地删除或执行。

### 2. 生成机制

对于 OpenClaw 配置文件通道，调度程序的“_default_spawn”在任务的固定工作空间内运行“hermes -p <assignee> chat -q <prompt>”（或当“hermes” shim 不在“$PATH”上时的等效模块形式），并设置以下环境变量：

|变量|携带|
|---|---|
| `HERMES_看板_任务` |工作人员正在操作的任务 ID |
| `HERMES_KANBAN_DB` |每板 SQLite 文件的绝对路径 |
| `HERMES_看板_板` |板蛞蝓 |
| `HERMES_KANBAN_WORKSPACES_ROOT` |板工作区树的根 |
| `HERMES_看板_工作空间` | *此*任务工作区的绝对路径 |
| `HERMES_KANBAN_RUN_ID` |当前运行的 id（生命周期门） |
| `HERMES_KANBAN_CLAIM_LOCK` |声明锁定字符串 (`<host>:<pid>:<uuid>`) |
| `HERMES_个人资料` |工作人员自己的个人资料名称（用于“kanban_comment”作者归属）|
| `HERMES_租户` |租户命名空间，如果任务有一个 |

对于非 OpenClaw 通道（通过插件注册），插件提供自己的“spawn_fn”可调用函数，用于获取“task”、“workspace”和“board”，并返回一个可选的 pid 用于崩溃检测。

### 3. 生命周期终结者

每项索赔必须以下列之一结束：

- `kanban_complete(summary=...,metadata=...)` — 任务成功，状态切换为“完成”。
- `kanban_block(reason=...)` — 任务等待人工输入，状态翻转为“已阻止”。当“kanban_unblock”运行时，调度程序会重新生成。
- 工作进程退出而不调用工具。内核获取它并发出“crashed”（PID 死亡）或“gave_up”（连续故障断路器跳闸）或“timed_out”（超出 max_runtime）。这就是失败之路；健康的工人并没有就此结束。

看板内核强制要求其中一个恰好终止每次运行。既不调用又正常退出的工作线程将被视为崩溃。

## 输出和需要审查的约定

对于大多数代码更改任务，工作人员完成后并没有真正“完成”——它需要人工审核员。看板内核并不强制执行这种区别（“代码更改任务”是模糊的，并且在每个代码工作人员上强制执行块而不是完成会破坏不需要审查的流程）。这是一个顶层约定：

- **阻止而不是完整**，“原因”前缀为“需要审核：”，因此仪表板/“hermes kanban show”将行显示为等待审核。
- **首先将结构化元数据放入“kanban_comment”中**，因为“kanban_block”仅包含人类可读的“原因”。注释是持久的注释通道——每个与审计相关的字段（changed_files、tests_run、diff_path 或 PR url、决策）都属于那里。
- **审阅者要么批准，要么解除阻止**，这会通过评论线程重新生成工作人员以进行后续操作；或通过另一个注释请求更改，下一个工作程序运行将其视为“kanban_show”上下文的一部分。

注入的“KANBAN_GUIDANCE”涵盖“kanban_complete”（真正的终端任务——拼写错误修复、文档更改、研究文章）和“review-required”块模式。

## 日志和审计跟踪

调度程序将每个任务工作线程的 stdout/stderr 写入“<board-root>/logs/<task_id>.log”。日志可从看板元数据进行审核：

- “task_runs”行包含“log_path”、退出代码（如果可用）、摘要和元数据。
- “task_events”行包含每个状态转换（“promoted”、“claimed”、“heartbeat”、“completed”、“blocked”、“gave_up”、“crashed”、“timed_out”、“reclaimed”、“claim_extended”）。
- `kanban_show` 返回两者，因此阅读任务的审阅者（或后续工作人员）无需访问仪表板即可获得完整的历史记录。

仪表板呈现带有摘要、元数据块和退出状态徽章的运行历史记录。 CLI 用户可以运行“hermes kanban tail <task_id>”来跟踪实时情况，或者运行“hermes kanban running <task_id>”来查看历史尝试列表。

## 现有车道形状

### OpenClaw 配置文件通道（默认）

今天每个看板工作人员都采用的形式：受让人是一个配置文件名称，调度程序生成“hermes -p <profile>”，工作人员获得自动注入的“KANBAN_GUIDANCE”系统提示块，并使用“kanban_*”工具终止运行。除了定义配置文件之外没有任何设置。

当您为队列创建配置文件时，请选择与您希望协调器路由到的*角色*匹配的名称。编排器（如果有的话）通过“hermes profile list”发现您的个人资料名称 - 系统假设没有固定的名册（合同的编排器端是注入的“KANBAN_GUIDANCE”的一部分）。

### Orchestrator 配置文件通道

配置文件通道的特殊化：编排器是一个 OpenClaw 配置文件，其工具集包括“看板”，但不包括用于实现的“终端”/“文件”/“代码”/“网络”。它的工作是通过“kanban_create”+“kanban_link”将高级目标分解为子任务，然后后退。协调者技能编码了抗诱惑规则。

## 添加外部 CLI 工作通道

将非 Hermes CLI 工具（Codex CLI、Claude Code CLI、OpenCode CLI、本地编码模型运行器等）连接为看板工作通道*尚未铺平道路*。调度程序的生成函数是可插入的（“spawn_fn”是“dispatch_once”上的一个参数），插件可以为非 OpenClaw 受让人注册自己的“spawn_fn”，但周围的集成工作 - 将 CLI 的退出代码包装到“kanban_complete”/“kanban_block”调用中，将 CLI 的工作区/沙箱约定映射到调度程序的“HERMES_KANBAN_WORKSPACE” env，处理身份验证和每个 CLI 策略 - 仍然是每个集成的设计工作。

如果您正在考虑添加 CLI 通道，请提出一个描述特定 CLI 和您尝试启用的工作流程的问题。上述合同是任何此类车道必须满足的约束；实现形式（每个 CLI 一个插件与由配置参数化的通用 CLI 运行器插件）是开放的。

此问题的历史问题是 [#19931](https://github.com/NousResearch/openclaw/issues/19931) 和封闭未合并的 Codex 特定 PR [#19924](https://github.com/NousResearch/openclaw/pull/19924) — 这些描述了原始架构提案，但没有获得运行者。

## 调度程序处理的故障模式

因此，车道作者不必重新实现这些：

- **过时的声明 TTL** — 声明但从未心跳/完成/阻止的工作进程在“DEFAULT_CLAIM_TTL_SECONDS”（默认 15 分钟）之后被回收 — 但前提是工作进程实际上已死亡。一名现场工作人员（慢速模型在一次无需工具的 LLM 通话中花费 20 多分钟）的索赔得到“延长”而不是被杀死；仅回收失效的 PID。
- **崩溃的工作人员** — 主机本地 PID 已消失的工作人员被“Detect_crashed_workers”检测到并被回收；该任务会增加“consecutive_failures”，并可能在断路器跳闸时自动阻止。
- **运行级别重试** - 当重试任务时（块后、崩溃后、回收后），如果自己的运行已被取代，工作人员可以在终止工具上使用“expected_run_id”参数来快速失败。
- **每任务最大运行时间** — `task.max_runtime_seconds` 每次运行的硬上限挂钟时间，无论 PID 活跃度如何。捕获真正陷入僵局的工作人员，否则实时 PID 扩展将继续运行。
- **搁浅任务检测** — 一个就绪任务，其受让人从未在“kanban.stranded_threshold_seconds”（默认 30 分钟）内提出要求，该任务会在“hermes 看板诊断”中显示为“stranded_in_ready”警告。严重性在 2 倍阈值时升级为错误，在 6 倍时升级为严重。通过一个信号捕获拼写错误的受让人、删除的个人资料以及删除外部工作人员池——与身份无关，无需管理每个董事会的许可名单。

## 相关

- [看板概述](./kanban) — 面向用户的介绍。
- [看板教程](./kanban-tutorial) — 打开仪表板的演练。
- [`KANBAN_GUIDANCE`](https://github.com/NousResearch/openclaw/blob/main/agent/prompt_builder.py) — 注入到每个看板工作人员的系统提示中的工作人员 + 编排器生命周期。