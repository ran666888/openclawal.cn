---
title: "Teams Meeting Pipeline"
sidebar_label: "Teams Meeting Pipeline"
description: "Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 团队会议管道

通过 Hermes CLI 操作 Teams 会议摘要管道 — 总结会议、检查管道状态、重播作业、管理 Microsoft Graph 订阅。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/生产力/团队会议管道` |
|版本 | `1.1.0` |
|作者 | OpenClaw代理+Teknium|
|许可证|麻省理工学院 |
|标签 | “团队”、“Microsoft Graph”、“会议”、“生产力”、“运营” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 团队会议管道

每当用户询问 Microsoft Teams 会议摘要、文字记录、录音、操作项、图形订阅或有关 Teams 会议管道的任何操作问题时，请使用此技能。适用于任何语言 - 下面的触发器是示例，而不是详尽的列表。

面向操作员的所有内容都是通过终端工具运行的“hermes team-pipeline”子命令。该管道没有新的模型工具——CLI 只是表面。

## 什么时候使用这个技能

用户要求：
- 总结 Teams 会议/提取行动项目/提取会议记录
- 检查管道状态、检查存储的会议作业或查看最近的会议
- 重播/重新运行失败或需要新摘要的存储作业
- 更改环境或配置后验证 Microsoft Graph 设置
- 解决“会议摘要从未到达”或“没有新会议正在接收”的问题
- 管理 Graph webhook 订阅（创建、更新、删除、检查）
- 设置自动订阅续订（请参阅下面的陷阱）

多语言触发示例（并非详尽无遗）：
- 英语：“总结 Teams 会议”、“管道状态”、“重播作业 X”
- 土耳其语：“团队会议 özetle”、“行动项目 çıkar”、“toplantı notu”、“管道 durumu”、“重播作业”

## 先决条件

在使用管道之前，请验证这些是否在 `${HERMES_HOME:-~/.hermes}/.env` 中设置：

````bash
MSGRAPH_TENANT_ID=...
MSGRAPH_CLIENT_ID=...
MSGRAPH_CLIENT_SECRET=...
````

如果缺少任何内容，请将用户引导至位于“/docs/guides/microsoft-graph-app-registration”的 Azure 应用程序注册指南 - 他们需要使用管理员同意的 Graph 应用程序权限进行 Azure AD 应用程序注册，然后管道才能工作。

## 命令参考

### 状态和检查（从这里开始）

````bash
hermes team-pipeline validate # 配置快照 - 任何更改后首先运行
hermes team-pipeline token-health # 图表代币状态
Hermes team-pipeline token-health --force-refresh # 强制获取新的令牌
Hermes 团队管道列表 # 最近的会议作业
hermes team-pipeline list --status failed # 仅失败的作业
hermes team-pipeline show <job-id> # 一项工作的完整详细信息
hermes team-pipeline 订阅 # 当前 Graph webhook 订阅
````

### 重新运行/调试

````bash
hermes team-pipeline run <job-id> # 重播存储的作业（重新汇总、重新交付）
hermes team-pipeline fetch --meeting-id <id> # dry-run：解析会议+记录而不保留
hermes team-pipeline fetch --join-web-url "<url>" # 通过加入 URL 进行干运行
````

### 订阅管理

````bash
爱马仕团队-管道订阅 \
  --资源通信/onlineMeetings/getAllTranscripts \
  --notification-url https://<your-public-host>/msgraph/webhook \
  --客户端状态“$MSGRAPH_WEBHOOK_CLIENT_STATE”

Hermes team-pipeline renew-subscription <sub-id> --expiration <iso-8601>
Hermes 团队管道删除订阅 <sub-id>
Hermes team-pipeline Maintenance-subscriptions # 续订即将到期的订阅
Hermes team-pipeline Maintenance-subscriptions --dry-run # 显示将更新的内容
````

## 常见问题的决策树

- 用户问“为什么我没有收到今天会议的摘要？” → 从“list --status failed”开始，然后在相关行上“show <job-id>”。如果该作业根本不存在，请检查“订阅”——webhook 可能已过期（请参阅下面的陷阱）。
- 用户询问“设置正常吗？” →“验证”，然后“令牌健康”，然后“订阅”。如果这三项都通过，则请求举行测试会议并检查“列表”是否有新行。
- 用户要求“重新运行会议 X 的摘要”→ `list` 查找作业 ID，`运行 <job-id>` 进行重播。如果再次失败，请“show <job-id>”检查错误并“fetch --meeting-id”以试运行工件解析。
- 用户询问“将会议 X 添加到管道中” → 通常您不会这样做 — 管道是订阅驱动的，而不是按会议驱动的。如果他们想要总结过去的特定会议，请在创建作业后使用“fetch”提取记录+“run”。

## 严重陷阱：图订阅将在 72 小时内过期

Microsoft Graph 将 Webhook 订阅的上限限制为 72 小时，并且**不会自动续订**。如果未安排“maintain-subscriptions”，会议通知将在手动创建订阅后 3 天停止发送，但不会提示提示。

当用户报告“管道昨天工作但今天没有到达”时：
1. 运行 `hermesteams-pipelinesubscriptions` — 如果它为空或者所有条目都显示过去的 `expirationDateTime`，这就是原因。
2. 使用 `subscribe` 重新创建，如上所示。
3. **通过“hermes cron add”、systemd 计时器或普通 crontab 立即设置自动更新**。位于“/docs/guides/operate-teams-meeting-pipeline#automating-subscription-renewal-required-for-product”的操作员运行手册包含所有三个选项。 12 小时间隔是安全的（72 小时限制的 6 倍空间）。

## 其他陷阱

- **会议记录尚不可用。** 团队在会议结束后需要一些时间来生成会议记录工件。刚刚结束的会议上的“fetch --meeting-id”可能会返回空。等待 2-5 分钟并重试，或者让 Graph Webhook 自然驱动摄取。
- **交付模式不匹配。** 如果生成摘要（“list”显示成功）但 Teams 中没有任何内容，请检查“platforms.teams.extra.delivery_mode”和匹配的目标配置（“incoming_webhook_url”或“c​​hat_id”或“team_id”+“channel_id”）。作者从 config.yaml 或 `TEAMS_*` 环境变量中读取这些内容。
- **图形应用程序权限。** 令牌干净地获取（`token-health` 通过），但当添加权限但未重新授予管理员同意时，图形 API 调用返回 401/403。让用户重新访问 Azure 门户中的应用注册，并再次单击“授予管理员同意”。

## 相关文档

当用户需要比该技能更深入的内容时，请向他们指出这些内容：
- Azure 应用程序注册演练：`/docs/guides/microsoft-graph-app-registration`
- 完整的管道设置：`/docs/user-guide/messaging/teams-meetings`
- 操作员运行手册（续订自动化、故障排除、上线清单）：`/docs/guides/operate-teams-meeting-pipeline`
- Webhook 监听器设置：`/docs/user-guide/messaging/msgraph-webhook`