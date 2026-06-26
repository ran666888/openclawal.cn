---
title: "Operate the Teams Meeting Pipeline"
description: "Runbook, go-live checklist, and operator worksheet for the Microsoft Teams meeting pipeline"
---
# 操作团队会议管道

已从 [Teams Meetings](/user-guide/messaging/teams-meetings) 启用该功能后，请使用本指南。

此页面涵盖：
- 操作员 CLI 流程
- 日常订阅维护
- 故障分类
- 上线检查
- 推出工作表

## 核心操作命令

### 验证配置快照

````bash
Hermes 团队管道验证
````

任何配置更改后首先使用它。

### 检查令牌健康状况

````bash
Hermes 团队-管道代币-健康
Hermes 团队管道令牌健康 --force-refresh
````

当您怀疑过时的身份验证状态时，请使用“--force-refresh”。

### 检查订阅

````bash
Hermes 团队-管道订阅
````

### 续订即将到期的订阅

````bash
Hermes 团队管道维护订阅
Hermes 团队管道维护订阅--dry-run
````

### 自动续订订阅（生产所需）

**Microsoft Graph 订阅最多 72 小时后过期。** 如果没有任何内容续订，会议通知将在 3 天后默默停止，并且管道看起来“已损坏”。对于任何图形支持的集成来说，这是第一大操作失败模式。

您必须按计划运行“maintain-subscriptions”。选择以下三个选项之一：

#### 选项 1：OpenClaw cron（如果您已经运行 OpenClaw 网关，则推荐使用）

OpenClaw 附带了一个内置的 cron 调度程序。 `--no-agent` 模式运行脚本作为作业（而不是使用 LLM），并且 `--script` 必须指向 `~/.hermes/scripts/` 下的文件。首先创建脚本：

````bash
mkdir -p ~/.hermes/scripts
cat > ~/.hermes/scripts/maintain-teams-subscriptions.sh <<'EOF'
#!/usr/bin/env bash
执行 Hermes 团队管道维护订阅
EOF
chmod +x ~/.hermes/scripts/maintain-teams-subscriptions.sh
````

然后注册一个仅脚本的 cron 作业，每 12 小时运行一次（为 72 小时到期窗口提供 6 倍的空间）：

````bash
Hermes cron 创建“0 */12 * * *” \
  --name“团队管道维护订阅”\
  --无代理\
  --脚本维护团队订阅.sh \
  --交付本地
````

验证它是否已注册并检查下一次运行时间：

````bash
爱马仕 cron 列表
Hermes cron status # 调度程序状态
````

#### 选项 2：systemd 计时器（建议用于 Linux 生产部署）

创建`/etc/systemd/system/hermes-teams-pipeline-maintain.service`：

````ini
[单位]
描述=Hermes Teams 管道订阅维护
After=网络在线.target

[服务]
类型=一次性
用户=爱马仕
环境文件=/etc/hermes/env
ExecStart=/usr/local/bin/hermes 团队管道维护订阅
````

和`/etc/systemd/system/hermes-teams-pipeline-maintain.timer`：

````ini
[单位]
描述=每 12 小时运行一次 Hermes Teams 管道订阅维护

[定时器]
OnBootSec=5 分钟
OnUnitActiveSec=12h
持久=真

[安装]
WantedBy=timers.target
````

启用：

````bash
sudo systemctl 守护进程重新加载
sudo systemctl启用-现在hermes-teams-pipeline-maintain.timer
systemctl list-timers Hermes-teams-pipeline-maintain.timer
````

#### 选项 3：普通 crontab

````克罗恩
0 */12 * * * /usr/local/bin/hermes 团队管道维护订阅 >> /var/log/hermes/teams-pipeline-maintain.log 2>&1
````

确保 cron 环境具有“MSGRAPH_*”凭据。最简单的修复：在 crontab 调用的包装器脚本顶部源 `~/.hermes/.env`。

#### 验证续订是否有效

设置计划后，检查第一次计划运行后的续订活动：

````bash
Hermes team-pipeline 订阅 # 应该提前显示过期日期时间
Hermes team-pipeline Maintenance-subscriptions --dry-run # 大多数时候应该显示“0 即将到期”
````

如果您看到 Graph webhook 在大约 72 小时后神秘地“停止工作”，这是首先要检查的事情：续订作业是否实际运行？

### 检查最近的工作

````bash
Hermes 团队-管道清单
Hermes 团队管道列表--状态失败
Hermes team-pipeline 显示 <job-id>
````

### 重播存储的作业

````bash
Hermes 团队管道运行 <job-id>
````

### 试运行会议工件获取

````bash
Hermes team-pipeline fetch --meeting-id <会议id>
Hermes team-pipeline fetch --join-web-url "<join-url>"
````

## 日常操作手册

### 第一次设置后

按顺序运行这些：

````bash
Hermes 团队管道验证
Hermes 团队管道令牌健康 --force-refresh
Hermes 团队-管道订阅
````

然后触发或等待真正的会议事件并确认：

````bash
Hermes 团队-管道列表
Hermes team-pipeline 显示 <job-id>
````

### 每日或定期检查

- 运行 `hermes team-pipeline Maintenance-subscriptions --dry-run`
- 检查 `hermes team-pipeline list --status failed`
- 验证 Teams 交付目标仍然是正确的聊天或频道

### 更改 webhook URL 或传送目标之前

- 更新公共通知 URL 或 Teams 目标配置
- 运行“hermes team-pipeline validate”
- 续订或重新创建受影响的订阅
- 确认新事件落在预期的接收器中

## 故障分类

### 没有创造任何就业机会

检查：
- `msgraph_webhook` 已启用
- 公共通知 URL 指向 `/msgraph/webhook`
- 订阅中的客户端状态与“MSGRAPH_WEBHOOK_CLIENT_STATE”匹配
- 订阅仍然远程存在且未过期

### 作业在汇总之前处于重试状态或失败

检查：
- 成绩单权限和可用性
- 记录权限和工件可用性
- 如果启用了录制回退，则“ffmpeg”可用
- 图表代币健康状况

### 生成摘要但未交付给团队

检查：
- `platforms.teams.enabled: true`
- `交付模式`
- webhook 模式的 `incoming_webhook_url`
- 图形模式下的“chat_id”或“team_id”加上“channel_id”
- 如果使用图表发布，则团队身份验证配置

### 重复或意外重播

检查：
- 是否使用“hermes team-pipeline run”手动重播作业
- 该会议的接收器记录是否已存在
- 您是否有意在本地配置中启用重新发送路径

## 上线清单

- [ ] 图形凭据存在且正确
- [ ] `msgraph_webhook` 已启用并可通过公共互联网访问
- [ ] `MSGRAPH_WEBHOOK_CLIENT_STATE` 已设置并匹配订阅
- [ ] 转录订阅已创建
- 如果需要 STT 回退，则创建 [ ] 录制订阅
- [ ] 如果启用了录制回退，则会安装“ffmpeg”
- [ ] Teams 外向递送目标已配置并验证
- [ ] 仅在实际需要时才配置概念和线性接收器
- [ ] `hermes team-pipeline validate` 返回一个 OK 快照
- [ ] `hermes team-pipeline token-health --force-refresh` 成功
- [ ] **`maintain-subscriptions` 已计划**（OpenClaw cron、systemd 计时器或 crontab — 请参阅[自动续订订阅](#automating-subscription-renewal-required-for-product)）。否则，Graph 订阅会在 72 小时内自动过期。
- [ ] 真正的端到端会议事件已生成存储的作业
- [ ] 至少一份摘要已到达预期的传送接收器

## 交付模式决策指南

|模式|使用时 |权衡 |
|------|----------|----------|
| `incoming_webhook` |您只需要简单地发布到 Teams |最简单的设置，更少的控制 |
| `图` |您需要通过 Graph 进行频道或聊天发布 |更多控制、更多身份验证和目标配置 |

## 操作员工作表

在推出前填写此内容：

|项目 |价值|
|------|--------|
|公开通知网址 | |
|图租户 ID | |
|图表客户端 ID | |
| Webhook 客户端状态 | |
|文字资源订阅| |
|录音资源订阅 | |
|团队交付模式| |
|团队聊天 ID 或团队/频道 | |
|概念数据库ID | |
|线性团队 ID | |
|存储路径覆盖（如果有）| |
|业主日常检查| |

## 变更审核工作表

在更改部署之前使用它：

|问题 |回答 |
|----------|--------|
|我们是否要更改公共 Webhook URL？ | |
|我们是否正在轮换 Graph 凭证？ | |
|我们是否正在改变 Teams 交付模式？ | |
|我们是否要转移到新的 Teams 聊天或频道？ | |
|是否需要重新创建或续订订阅？ | |
|我们是否需要进行新的端到端验证？ | |

## 相关文档

- [Teams 会议设置](/user-guide/messaging/teams-meetings)
- [Microsoft Teams 机器人设置](/user-guide/messaging/teams)