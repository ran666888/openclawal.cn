---
title: "Apple Reminders — Apple Reminders via remindctl: add, list, complete"
sidebar_label: "Apple Reminders"
description: "Apple Reminders via remindctl: add, list, complete"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 苹果提醒

通过 Rememberctl 的 Apple 提醒：添加、列出、完成。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/苹果/苹果提醒` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| macOS |
|标签 | `提醒`、`任务`、`待办事项`、`macOS`、`Apple` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 苹果提醒

使用“remindctl”直接从终端管理 Apple 提醒。任务通过 iCloud 在所有 Apple 设备之间同步。

## 先决条件

- **macOS** 带有 Reminders.app
- 安装：`brew install steipete/tap/remindctl`
- 出现提示时授予提醒权限
- 检查：“remindctl 状态”/请求：“remindctl 授权”

## 何时使用

- 用户提到“提醒”或“提醒应用程序”
- 创建具有同步到 iOS 的截止日期的个人待办事项
- 管理苹果提醒列表
- 用户希望任务出现在他们的 iPhone/iPad 上

## 何时不使用

- 安排代理警报 → 使用 cronjob 工具代替
- 日历事件 → 使用 Apple 日历或 Google 日历
- 项目任务管理→使用GitHub Issues、Notion等。
- 如果用户说“提醒我”但意味着代理警报 → 首先澄清

## 快速参考

### 查看提醒

````bash
Rememberctl # 今天的提醒
今天提醒#今天
Rememberctl 明天 # 明天
Rememberctl week # 本周
Rememberctl overdue # 逾期
Rememberctl all # 一切
Rememberctl 2026-01-04 # 具体日期
````

### 管理列表

````bash
Rememberctl list # 列出所有列表
Rememberctl list Work # 显示具体列表
Rememberctl list Projects --create # 创建列表
Rememberctl list Work --delete # 删除列表
````

### 创建提醒

````bash
Rememberctl 添加“买牛奶”
Rememberctl add --title “给妈妈打电话” --list Personal -- 明天到期
Rememberctl add --title "会议准备" --due "2026-02-15 09:00"
````

### 到期时间与警报/提前推送

`--due` 和 `--alarm` 是不同的字段：

- `--due` 设置提醒的截止日期/时间。
- `--alarm` 设置 EventKit 警报/通知触发器。定时到期提醒可能默认为在到期时间发出警报，但当用户要求提前推送时明确传递“--alarm”。

对于在下午 2:00 发出提醒并提前 30 分钟发出通知：

````bash
Rememberctl add --title "美发师" --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
````

要编辑现有提醒：

````bash
Rememberctl编辑87354--due“2026-05-15 14:00”--alarm“2026-05-15 13:30”
````

提醒 UI 可能会按闹钟时间显示或分组项目，因为那是通知触发的时间。使用 JSON 进行验证，而不是假设到期时间已移动：

````bash
今天提醒--json
````

预期形状：

- `dueDate`：实际到期时间
- `alarmDate`：通知/提前推送时间

Apple 的公共“EKReminder”文档仅列出了特定于提醒的属性。警报支持来自由 Rememberctl 的“--alarm”标志公开的继承“EKCalendarItem”行为。

### 完成/删除

````bash
Rememberctl Complete 1 2 3 # 按 ID 补全
Rememberctl delete 4A83 --force # 按ID删除
````

### 输出格式

````bash
Rememberctl Today --json # 用于脚本编写的 JSON
今日提醒--plain # TSV 格式
Rememberctl Today --quiet # 仅计数
````

## 日期格式

被 `--due` 和日期过滤器接受：
- “今天”、“明天”、“昨天”
- `年-月-日`
- `YYYY-MM-DD HH:mm`
- ISO 8601（`2026-01-04T12:34:56Z`）

## 规则

1. 当用户说“提醒我”时，请澄清：Apple 提醒（同步到手机）与代理 cronjob 警报
2.创建前务必确认提醒内容和截止日期
3.使用`--json`进行编程解析