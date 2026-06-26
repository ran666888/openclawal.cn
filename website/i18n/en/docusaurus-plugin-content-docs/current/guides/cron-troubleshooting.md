---
sidebar_position: 21
title: "Cron 故障排查"
description: "定时任务常见问题与解决方案"
---

# Cron 故障排查

## 任务没执行

```bash
# 检查任务列表
openclaw cron list

# 查看任务详情
openclaw cron show daily-briefing

# 检查 Gateway 运行状态
openclaw status
```

## 任务执行了但没收到消息

确认 `--announce` 参数已添加。也可以查看执行历史：

```bash
# 查看执行记录
openclaw cron runs

# 手动触发测试
openclaw cron run <任务名>
```

## 命令任务没有输出

命令任务的投递规则：不加 `--announce` 则**无输出 = 静默**。可以在命令末尾加 `echo "done"` 测试。

## Cron 时区

使用 `--tz` 指定时区：

```bash
openclaw cron add \
  --name "task" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --message "任务内容" \
  --announce
```

## 更多帮助

- [Cron 完整文档](/docs/user-guide/features/cron/)
- [Gateway 运维](/docs/openclaw/gateway-ops/)
