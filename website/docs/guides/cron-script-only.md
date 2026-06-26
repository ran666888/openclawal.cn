---
sidebar_position: 20
title: "Cron 脚本模式"
description: "使用 Shell 脚本或命令作为 Cron 任务"
---

# Cron 脚本模式

除了 Agent 驱动的 Cron 任务，OpenClaw 还支持直接运行 Shell 命令作为定时任务——不消耗 LLM Token。

## 创建命令任务

```bash
openclaw cron add \
  --name "system-check" \
  --cron "0 * * * *" \
  --command "df -h / | awk 'NR==2 {print \$5}'" \
  --announce
```

- `--command` — 要执行的 Shell 命令
- `--announce` — 将输出投递到消息通道

## 脚本文件

也可以执行脚本文件：

```bash
openclaw cron add \
  --name "disk-watch" \
  --cron "0 */2 * * *" \
  --command "/path/to/disk-check.sh" \
  --announce
```

## 静默模式

如果不加 `--announce`，则命令只在有标准输出时才投递——适合健康检查、磁盘监控等后台任务，无异常不打扰。

查看更多：[Cron 配置](/docs/user-guide/features/cron/)。
