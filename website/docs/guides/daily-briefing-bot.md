---
sidebar_position: 3
title: "教程：每日简报机器人"
description: "构建一个自动的每日简报机器人，每天早晨用 Cron 定时抓取信息、汇总并发送到消息通道"
---

# 教程：构建每日简报机器人

本教程将带你构建一个个人简报机器人，它每天早晨自动醒来，搜索你关心的主题，汇总发现，并直接把简报发送到你的消息通道。

最终你将拥有一个完全自动化的 **Cron 定时任务 + 网页搜索 + 消息投递** 工作流。

## 前提条件

开始之前，请确保：

- **OpenClaw 已安装并配置**
- **Gateway 正在运行**：`openclaw gateway` 或用 `openclaw onboard --install-daemon` 设为服务
- **网页搜索已配置**：在配置中启用一个搜索供应商
- **消息通道已配置**（可选但推荐）— [Telegram](/docs/user-guide/messaging/telegram/) 或 Discord

## 第一步：手动测试工作流

先手动验证简报能否正常工作：

```bash
openclaw chat
```

然后发送：

```
帮我生成一份今日 AI 行业简报。
搜索最新新闻，按分类汇总：1. 大模型发布 2. 开源项目 3. 投融资 4. 行业应用。
格式简洁，每类 2-3 条。
```

确认 Agent 能正确搜索和汇总后，进入下一步。

## 第二步：创建 Cron 定时任务

```bash
openclaw cron add \
  --name "daily-briefing" \
  --cron "0 8 * * *" \
  --message "请生成今日 AI 行业简报。搜索最新新闻，按分类汇总：1. 大模型发布 2. 开源项目 3. 投融资 4. 行业应用。每类 2-3 条，格式简洁。" \
  --announce
```

参数说明：
- `--cron "0 8 * * *"` — 每天早上 8 点执行（Cron 表达式）
- `--message "..."` — Agent 执行的任务内容
- `--announce` — 将结果投递到你的消息通道
- `--name "daily-briefing"` — 任务名称（用于管理）

查看已创建的定时任务：

```bash
openclaw cron list
```

## 第三步：个性化你的简报

工作日每天早上 9 点执行：

```bash
openclaw cron add \
  --name "my-briefing" \
  --cron "0 9 * * 1-5" \
  --message "搜索以下领域今日新闻：1. AI Agent 框架更新 2. 国产大模型进展 3. 开源工具推荐。汇总成简洁的 5 条简报。" \
  --announce
```

## 第四步：测试 Cron 任务

手动触发一次任务来测试：

```bash
openclaw cron run daily-briefing
```

检查是否成功收到简报。

## 故障排查

| 问题 | 解决方法 |
|------|---------|
| 任务没执行 | 检查 `openclaw cron list` 确认任务存在 |
| 搜索没结果 | 确认搜索 API Key 已正确配置 |
| 没收到消息 | 检查 `openclaw status` 确认 Gateway 在运行 |
| 时间不对 | 使用 `--tz "Asia/Shanghai"` 指定时区 |

## 延伸阅读

- [Cron 定时任务](/docs/user-guide/features/cron/)
- [网页搜索配置](/docs/user-guide/features/web-search/)
