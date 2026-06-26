---
sidebar_position: 11
title: "Cron Internals"
description: "How OpenClaw stores, schedules, edits, pauses, skill-loads, and delivers cron jobs"
---
# Cron 内部结构

cron 子系统提供计划任务执行——从简单的一次性延迟到具有技能注入和跨平台交付的重复 cron 表达式作业。

## 关键文件

|文件|目的|
|------|---------|
| `cron/jobs.py` |作业模型、存储、原子读/写“jobs.json” |
| `cron/scheduler.py` |调度程序循环 — 到期作业检测、执行、重复跟踪 |
| `工具/cronjob_tools.py` |面向模型的`cronjob`工具注册和处理程序|
| `网关/run.py` |网关集成——长时间运行循环中的 cron 滴答作响 |
| `hermes_cli/cron.py` | CLI `hermes cron` 子命令 |

## 调度模型

支持四种计划格式：

|格式|示例|行为 |
|--------|---------|----------|
| **相对延迟** | `30m`、`2h`、`1d` |一发，指定持续时间后开火 |
| **间隔** | “每 2 小时”、“每 30 m” |定期发生、定期发生火灾 |
| **Cron 表达式** | `0 9 * * *` |标准 5 字段 cron 语法（分钟、小时、日、月、工作日）|
| **ISO 时间戳** | `2025-01-15T09:00:00` |一发，准时开火 |

面向模型的表面是一个具有动作式操作的“cronjob”工具：“create”、“list”、“update”、“pause”、“resume”、“run”、“remove”。

## 作业存储

作业存储在“~/.hermes/cron/jobs.json”中，具有原子写入语义（写入临时文件，然后重命名）。每个作业记录包含：

```json
{
  “id”：“a1b2c3d4e5f6”，
  "name": "每日简报",
  "prompt": "总结今天的人工智能新闻和融资轮次",
  “时间表”：{
    “种类”：“克罗恩”，
    "expr": "0 9 * * *",
    “显示”：“0 9 * * *”
  },
  "skills": ["ai-funding-daily-report"],
  "deliver": "电报:-1001234567890",
  “重复”：{
    “次”：空，
    “已完成”：42
  },
  “状态”：“预定”，
  “启用”：正确，
  "next_run_at": "2025-01-16T09:00:00Z",
  "last_run_at": "2025-01-15T09:00:00Z",
  “last_status”：“好的”，
  “创建时间”：“2025-01-01T00:00:00Z”，
  “型号”：空，
  “提供商”：空，
  “脚本”：空
}
````

### 作业生命周期状态

|状态|意义|
|--------|---------|
| `预定的` |活动，将在下一个预定时间触发 |
| `暂停` |已暂停 — 在恢复之前不会触发 |
| `已完成` |重复计数已用完或已发射一发 |
| `运行` |当前正在执行（瞬态）|

### 向后兼容性

较旧的职位可能有一个“技能”字段，而不是“技能”数组。调度程序在加载时对此进行标准化 - 单个“技能”被提升为“技能：[技能]”。

## 调度程序运行时

### 刻度周期

调度程序定期运行（默认：每 60 秒）：

````文本
勾选（）
  1. 获取调度程序锁（防止重叠滴答）
  2. 从 jobs.json 加载所有作业
  3. 筛选到期作业（next_run <= now AND state == "scheduled"）
  4. 对于每项应有的工作：
     a.将状态设置为“运行”
     b.创建新的 AIAgent 会话（无对话历史记录）
     c.按顺序加载附加技能（作为用户消息注入）
     d.通过代理运行作业提示
     e.将响应传送到配置的目标
     f.更新run_count，计算next_run
     g。如果重复计数耗尽→状态=“已完成”
     h.否则→状态=“已安排”
  5. 将更新后的作业写回 jobs.json
  6.释放调度程序锁
````

### 网关集成

在网关模式下，cron **触发**（决定*何时*到期工作的部分）
fires — “Axis B”）是通过可插入的“CronScheduler”提供程序选择的。的
网关调用 `resolve_cron_scheduler()` (`cron/scheduler_provider.py`) 并运行
已解析提供程序的“start()”位于专用后台线程中，旁边还有一个
单独的网关管理线程。

活动提供程序由“cron.provider”配置键选择：

- **空（默认）** → 内置的`InProcessCronScheduler`，它运行
  历史进程内循环每 60 秒调用一次“scheduler.tick()”。这个
  与预提供者行为字节相同。
- **一个命名的提供程序**（例如 `chronos`，一个托管 cron 提供程序
  缩放到零部署） → 从 `plugins/cron/<name>/` 发现或
  `$HERMES_HOME/plugins/<名称>/`。

如果指定提供程序丢失、加载失败或报告 `is_available() ==
False`，解析器回退到内置并带有警告 - **cron is
永远不会没有触发器。** 内置提供程序位于核心中
(`cron/scheduler_provider.py`)，不在`plugins/`中，所以回退不能
不小心删除了。

“解雇”*意味着*（工作执行+交付）不变并由所有人共享
提供者 — 它位于 `scheduler.run_job()` / `scheduler._deliver_result()` 中。
提供者仅控制触发器，而不控制执行。

在 CLI 模式下，cron 作业仅在运行“hermes cron”命令时或在活动 CLI 会话期间触发。

### 托管 cron (Chronos) 以实现缩放至零

托管网关可以运行 **Chronos** 提供程序（`cron.provider: chronos`）
而不是内置的股票代码。 Chronos 让空闲网关**扩展到零**
并且仍然触发 cron 作业：而不是 60 秒的进程内循环（这会
保持进程唤醒），它要求 Nous 基础设施准确地装备 **一个
在该作业真正的下一次触发时间**为每个作业管理一次。火时诺斯
通过经过身份验证的 Webhook 回调网关（`POST /api/cron/fire`）；
网关通过与内置相同的“run_one_job”路径运行作业，
然后重新武装下一次射击。在两次火灾之间，该过程可以完全停止 -
它只在真正的火上醒来，而不是在定期定时器上唤醒。

流程（托管调度程序由 Nous 提供；代理不持有
调度程序凭据）：

````
创建/更新 cron 作业
  → Chronos 要求 Nous 在作业的 next_run_at 上配置一次操作
      （使用代理现有的 Nous 令牌进行身份验证）
  → 发生火灾时 Nous 调用网关： POST {callback_url}/api/cron/fire
      （使用短暂的、有目的的 Nous 铸造的 JWT 进行验证）
  → 网关验证令牌，声明作业（存储比较并设置）
    多副本部署最多触发一次），运行它，然后重新武装下一个
    一击
````

配置（全部非秘密；在托管代理上，Nous 在配置时设置这些）：

|关键|意义|
|---|---|
| `cron.provider` |要激活的`chronos`（空=内置股票代码）|
| `cron.chronos.portal_url` | Nous 基本 URL（武装 + fire-token 发行者）|
| `cron.chronos.callback_url` |网关自己的用于入站火灾的公共基本 URL |
| `cron.chronos.expected_audience` |该特工的火令牌观众|
| `cron.chronos.nas_jwks_url` |用于验证入站火令牌的密钥集 |

如果 Chronos 配置错误或代理未登录 Nous，
`resolve_cron_scheduler()` 回退到内置代码（记录警告） -
cron 永远不会失去它的触发器。每次火灾后，重复作业都会重新启动； `重复`-N
当计数耗尽时，作业会干净地停止（没有孤立的一次性）。完整的
Agent↔Nous 电汇合约位于“docs/chronos-management-cron-contract.md”中。

### 新会话隔离

每个 cron 作业都在全新的代理会话中运行：

- 没有之前运行的对话历史记录
- 没有先前 cron 执行的记忆（除非持久化到内存/文件）
- 提示必须是独立的 - cron 作业不能提出澄清问题
- `cronjob` 工具集被禁用（递归防护）

## 技能支持的工作

cron 作业可以通过“技能”字段附加一项或多项技能。执行时：

1.技能按照指定顺序加载
2.每个技能的SKILL.md内容作为上下文注入
3. 作业提示作为任务指令附加
4. 代理处理组合的技能上下文+提示

这可以实现可重用、经过测试的工作流程，而无需将完整的指令粘贴到 cron 提示中。例如：

````
创建每日资金报告→附加“ai-funding-daily-report”技能
````

### 脚本支持的作业

作业还可以通过“script”字段附加 Python 脚本。该脚本在每个代理轮流之前运行，并且其标准输出作为上下文注入到提示中。这使得数据收集和变化检测模式成为可能：

````蟒蛇
# ~/.hermes/scripts/check_competitors.py
导入请求，json
# 获取竞争对手的发行说明，与上次运行的差异
# 将摘要打印到标准输出 — 代理分析和报告
````

脚本超时默认为 120 秒。 `_get_script_timeout()` 通过三层链解决限制：

1. **模块级覆盖** — `_SCRIPT_TIMEOUT` （用于测试/monkeypatching）。仅当与默认值不同时才使用。
2. **环境变量** — `HERMES_CRON_SCRIPT_TIMEOUT`
3. **配置** — `config.yaml` 中的 `cron.script_timeout_seconds` （通过 `load_config()` 读取）
4. **默认** — 120 秒

### 提供商恢复

`run_job()` 将用户配置的后备提供程序和凭证池传递到 `AIAgent` 实例中：

- **后备提供程序** — 从“config.yaml”读取“fallback_providers”（列表）或“fallback_model”（旧版字典），匹配网关的“_load_fallback_model()”模式。作为“fallback_model=”传递给“AIAgent.__init__”，它将两种格式标准化为后备链。
- **凭证池** — 使用解析的运行时提供程序名称通过“load_pool(provider)”从“agent.credential_pool”加载。仅当池具有凭据时才通过（`pool.has_credentials()`）。针对 429/速率限制错误启用同一提供商密钥轮换。

这反映了网关的行为——没有它，cron 代理将在速率限制上失败，而不尝试恢复。

## 交付模式

Cron 作业结果可以传送到任何支持的平台：

|目标|语法 |示例|
|--------|--------|---------|
|起源聊天 | `起源` |交付到创建职位的聊天室 |
|本地文件| `本地` |保存到 `~/.hermes/cron/output/` |
|电报 | `telegram` 或 `telegram:<chat_id>` | `电报：-1001234567890` |
|不和谐 | `discord` 或 `discord:#channel` | `不和谐：#工程` |
|松弛| `松弛` |交付到 Slack 主频道 |
| WhatsApp | `whatsapp` |送货到 WhatsApp 首页 |
|信号| `信号` |交付给信号 |
|矩阵| `矩阵` |送到 Matrix 家庭房间 |
|最重要| `最重要` |送货到 Mattermost 家 |
|电子邮件 | `电子邮件` |通过电子邮件发送 |
|短信| `短信` |通过短信发送 |
|家庭助理 | `家庭助理` |交付给 HA 对话 |
|钉钉 | `钉聊` |发送至钉钉 |
|飞书 | `飞书` |发送至飞书 |
|微康| `wecom` |交付至WeCom |
|微信| `微信` |发送至微信 |
|蓝色泡泡 | '蓝色泡泡' |通过 BlueBubbles 发送至 iMessage |
| QQ机器人| `qqbot` |通过官方API v2 投递至QQ（腾讯） |

对于 Telegram 主题，请使用“telegram:<chat_id>:<thread_id>”格式（例如，“telegram:-1001234567890:17585”）。

### 响应包装

默认情况下（`cron.wrap_response: true`），cron 交付被包装为：
- 标识 cron 作业名称和任务的标头
- 页脚指出客服人员无法在对话中看到已传递的消息

cron 响应中的“[SILENT]”前缀完全抑制传递——对于只需要写入文件或执行副作用的作业很有用。

### 会话隔离

Cron 交付不会镜像到网关会话对话历史记录中。它们仅存在于 cron 作业自己的会话中。这可以防止目标聊天对话中出现消息交替违规。

## 递归守卫

Cron 运行会话禁用了“cronjob”工具集。这可以防止：
- 创建新的 cron 作业的预定作业
- 递归调度可能会导致令牌使用量激增
- 工作内部的工作安排意外改变

## 锁定

调度程序使用基于跨进程文件的锁定（Unix 上的“fcntl.flock”，Windows 上的“msvcrt.locking”）来防止重叠的滴答执行同一到期作业批次两次 - 即使在网关的进程内滴答器和独立的“hermes cron”/手动“tick()”调用之间也是如此。如果无法获取锁，`tick()` 立即返回 0。

## CLI 界面

`hermes cron` CLI 提供直接的作业管理：

````bash
hermes cron list # 显示所有作业
hermes cron create # 交互式作业创建（别名：add）
hermes cron edit <job_id> # 编辑作业配置
Hermes cron Pause <job_id> # 暂停正在运行的作业
hermes cronresume <job_id> # 恢复暂停的作业
hermes cron run <job_id> # 触发立即执行
hermes cron remove <job_id> # 删除作业
````

## 相关文档

- [Cron 功能指南](/user-guide/features/cron)
- [网关内部结构](./gateway-internals.md)
- [代理循环内部结构](./agent-loop.md)