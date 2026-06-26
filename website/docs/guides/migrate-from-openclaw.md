---
sidebar_position: 25
title: "从其他平台迁移到 OpenClaw"
description: "从 ChatGPT、Claude Code、Hermes Agent 等平台迁移到 OpenClaw"
---

# 迁移到 OpenClaw

## 从 Hermes 迁移

如果你正在使用 Hermes Agent，迁移到 OpenClaw 很简单：

| Hermes 命令 | OpenClaw 命令 |
|-------------|--------------|
| `hermes setup` | `openclaw setup` |
| `hermes gateway` | `openclaw gateway` |
| `hermes cron` | `openclaw cron` |
| `hermes tools` | `openclaw config` |
| `hermes chat` | `openclaw chat` |

配置文件和技能目录需要手动迁移：

```bash
# Hermes 配置在 ~/.hermes/
# OpenClaw 配置在 ~/.openclaw/

# 迁移技能
cp -r ~/.hermes/skills/* ~/.openclaw/skills/
```

## 从其他平台迁移

OpenClaw 兼容 OpenAI 格式的 API，大多数配置可以直接复用。如有问题请参考[配置指南](/docs/user-guide/configuration/)或加入社区群询问。
