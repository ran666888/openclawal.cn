---
sidebar_position: 6
title: "Teams Meetings"
description: "Set up the Microsoft Teams meeting summary pipeline with Microsoft Graph webhooks"
---
# Microsoft Teams 会议

当您希望 OpenClaw 提取 Microsoft Graph 会议事件、首先获取记录、在需要时回退到录音和 STT 以及向下游接收器提供结构化摘要时，请使用 Teams 会议管道。

先决条件：请参阅 [Microsoft Teams](./teams.md) 了解底层机器人/凭据设置。

> 运行“hermes gateway setup”并选择 **Teams Meetings** 进行指导演练。

本页重点介绍设置和启用：
- 图形凭证
- webhook监听器配置
- 团队交付模式
- 管道配置形状

对于第 2 天的操作、上线检查和操作员工作表，请使用专用指南：[操作 Teams 会议管道](/guides/operate-teams-meeting-pipeline)。

## 此功能的作用

管道：
1.接收Microsoft Graph webhook事件
2. 解决会议并优先选择成绩单工件
3. 当没有可用的文字记录时，退回到录音下载加 STT
4. 在本地存储持久的作业状态和接收器记录
5.可以向Notion、Linear和Microsoft Teams撰写摘要

操作员操作保留在 CLI 中（“teams-pipeline”子命令由“teams_pipeline”插件注册 - 通过“hermes plugins enable team_pipeline”启用它或在“config.yaml”中设置“plugins.enabled: [teams_pipeline]”）：

````bash
Hermes 团队管道验证
Hermes 团队-管道列表
Hermes 团队管道维护订阅
````

## 先决条件

在启用会议管道之前，请确保您拥有：

- 一个可用的 OpenClaw 安装
- 现有的 [Microsoft Teams 机器人设置](/user-guide/messaging/teams)（如果您想要 Teams 出站递送）
- Microsoft Graph 应用程序凭据以及您计划订阅的会议资源所需的权限
- Microsoft Graph 可以调用以进行 Webhook 传递的公共 HTTPS URL
- 如果您想要录制加 STT 后备，请安装“ffmpeg”

## 步骤 1：添加 Microsoft Graph 凭据

将仅限 Graph 应用程序的凭据添加到 `~/.hermes/.env`：

````bash
MSGRAPH_TENANT_ID=<租户 ID>
MSGRAPH_CLIENT_ID=<客户端 ID>
MSGRAPH_CLIENT_SECRET=<客户端秘密>
````

这些凭证由以下人员使用：
- Graph 客户端基础
- 订阅维护命令
- 会议决议和工件获取
- 当您不提供专用 Teams 访问令牌时，基于图形的 Teams 出站交付

## 步骤 2：启用 Graph Webhook 监听器

Webhook 监听器是一个名为“msgraph_webhook”的网关平台。至少，启用它并设置客户端状态值：

````bash
MSGRAPH_WEBHOOK_ENABLED=true
MSGRAPH_WEBHOOK_HOST=127.0.0.1
MSGRAPH_WEBHOOK_PORT=8646
MSGRAPH_WEBHOOK_CLIENT_STATE=<随机共享秘密>
MSGRAPH_WEBHOOK_ACCEPTED_RESOURCES=通讯/onlineMeetings
````

听者暴露：
- 用于图形通知的“/msgraph/webhook”
- `/health` 用于简单的健康检查

您需要将公共 HTTPS 端点路由到该侦听器。例如，如果您的公共域是“https://ops.example.com”，则您的图形通知 URL 通常为：

````文本
https://ops.example.com/msgraph/webhook
````

## 步骤 3：配置团队交付和管道行为

会议管道从现有的“teams”平台条目中读取其运行时配置。特定于管道的旋钮位于“teams.extra.meeting_pipeline”下。 Teams 出站交付保留在正常的 Teams 平台配置界面上。

示例`~/.hermes/config.yaml`：

````yaml
平台：
  msgraph_webhook：
    启用：真
    额外：
      主机：127.0.0.1
      端口：8646
      client_state: “替换我”
      接受的资源：
        - “通讯/在线会议”

  团队：
    启用：真
    额外：
      client_id：“您的团队客户 ID”
      client_secret：“您的团队客户秘密”
      tenant_id：“您的团队租户id”

      # 出站摘要传送
      Delivery_mode: "graph" # 或传入_webhook
      team_id: "团队 ID"
      Channel_id: "频道 ID"
      #传入_webhook_url：“https://...”

      会议管道：
        成绩单最少字符数：80
        需要成绩单：假
        transcription_fallback: true
        ffmpeg_extract_audio：真
        概念：
          启用：假
        线性：
          启用：假
````

如果将侦听器绑定到非环回主机（例如“0.0.0.0”），则还必须将“allowed_source_cidrs”设置为 Microsoft 的 webhook 出口范围。环回绑定 (`127.0.0.1` / `::1`) 是预期的开发隧道和本地反向代理设置。

## 团队交付模式

该管道支持现有 Teams 插件内的两种 Teams 摘要交付模式。

### `incoming_webhook`

当您想要将简单的 Webhook 发布到 Teams 中而不需要通过 Graph 创建通道消息时，请使用此选项。

所需配置：

````yaml
平台：
  团队：
    启用：真
    额外：
      交付模式：“incoming_webhook”
      传入_webhook_url：“https://...”
````

### `图表`

当您希望 OpenClaw 通过 Microsoft Graph 将摘要发布到 Teams 聊天或频道中时，请使用此选项。

支持的目标：
- `聊天ID`
- `team_id` + `channel_id`
- 现有 Teams 平台的“team_id”+“home_channel”回退

示例：

````yaml
平台：
  团队：
    启用：真
    额外：
      交付模式：“图表”
      team_id: "团队 ID"
      Channel_id: "频道 ID"
````

## 步骤 4：启动网关

更新配置后正常启动OpenClaw：

````bash
爱马仕网关运行
````

或者，如果您在 Docker 中运行 OpenClaw，请按照部署中的相同方式启动网关。

检查监听器：

````bash
卷曲 http://localhost:8646/health
````

## 步骤 5：创建图订阅

使用插件 CLI 创建和检查订阅。

示例：

````bash
爱马仕团队-管道订阅 \
  --资源通信/onlineMeetings/getAllTranscripts \
  --notification-url https://ops.example.com/msgraph/webhook \
  --客户端状态“$MSGRAPH_WEBHOOK_CLIENT_STATE”

爱马仕团队-管道订阅 \
  --资源通信/onlineMeetings/getAllRecordings \
  --notification-url https://ops.example.com/msgraph/webhook \
  --客户端状态“$MSGRAPH_WEBHOOK_CLIENT_STATE”
````

:::警告图谱订阅将在 72 小时后过期

Microsoft Graph 将 Webhook 订阅的上限限制为 72 小时，并且不会自动续订。您必须在上线之前安排“hermesteams-pipelinemaintain-subscriptions”，否则通知将在任何手动订阅创建三天后静默停止。请参阅 Operator Runbook 中的[自动续订订阅](/guides/operate-teams-meeting-pipeline#automating-subscription-renewal-required-for-product) — 三个选项（OpenClaw cron、systemd 计时器、普通 crontab）。

:::

对于订阅维护和第 2 天操作员流程，请继续阅读指南：[操作 Teams 会议管道](/guides/operate-teams-meeting-pipeline)。

## 验证

运行内置验证快照：

````bash
Hermes 团队管道验证
````

有用的同伴检查：

````bash
Hermes 团队-管道代币-健康
Hermes 团队-管道订阅
````

## 故障排除

|问题 |检查什么 |
|--------|----------------|
| Graph webhook 验证失败 |确认公共 URL 正确且可访问，并且 Graph 正在调用准确的“/msgraph/webhook”路径 |
|工作未出现在“hermes team-pipeline list”中 |确认“msgraph_webhook”已启用并且订阅指向正确的通知 URL |
|成绩单优先永远不会成功|检查脚本资源的图形权限以及该会议的脚本工件是否存在 |
|录音回退失败 |确认已安装“ffmpeg”并且 Graph 应用程序可以访问录制工件 |
|团队摘要交付失败 |重新检查“delivery_mode”、目标 ID 和 Teams 身份验证配置 |

## 相关文档

- [Microsoft Teams 机器人设置](/user-guide/messaging/teams)
- [操作团队会议管道](/guides/operate-teams-meeting-pipeline)