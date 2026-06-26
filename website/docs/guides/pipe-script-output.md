---
sidebar_position: 22
title: "脚本输出投递到消息平台"
description: "将脚本的标准输出自动投递到消息通道"
---

# 脚本输出投递到消息平台

OpenClaw 支持将任意脚本的输出自动投递到消息通道中。

## 基本用法

```bash
openclaw cron add \
  --name "weekly-report" \
  --cron "0 9 * * 1" \
  --command "/path/to/report.sh" \
  --announce
```

## 投递到指定目标

```bash
openclaw cron add \
  --name "alert" \
  --cron "*/5 * * * *" \
  --command "/path/to/check.sh" \
  --to "+8613800138000" \
  --announce
```

`--to` 参数支持手机号（SMS）、Telegram chat ID 等。

## 命令环境变量

```bash
openclaw cron add \
  --name "custom-report" \
  --cron "0 8 * * *" \
  --command "/path/to/script.sh" \
  --command-env "API_KEY=xxx" \
  --command-cwd "/path/to/workdir" \
  --announce
```

## 静默模式

不加 `--announce`，则脚本无输出时不会发送消息。
