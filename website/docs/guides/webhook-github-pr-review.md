---
sidebar_position: 19
title: "Webhook GitHub PR 自动评论"
description: "通过 Webhook 让 OpenClaw 自动审查 GitHub PR"
---

# Webhook GitHub PR 自动评论

OpenClaw 支持通过 Webhook 接收 GitHub 事件，自动触发 PR 审查。

## 配置 GitHub Webhook

在 GitHub 仓库设置中添加 Webhook：

1. 进入仓库 → Settings → Webhooks → Add webhook
2. **Payload URL**: `http://你的地址:18789/webhook/github`
3. **Content type**: `application/json`
4. **Secret**: 设置一个密钥
5. **Events**: 勾选 "Pull requests"

## 在 OpenClaw 中配置

Webhook 功能需要配合 Agent 的技能来实现。配置 Gateway 的 webhook 路由需要在 `openclaw.json` 中设置：

```json
{
  "webhooks": {
    "github-pr": {
      "path": "/webhook/github",
      "secret": "your-secret",
      "agent": "main",
      "prompt": "收到新的 GitHub PR 事件，请审查代码变化并发表评论。"
    }
  }
}
```

详情参考：[Webhook 文档](/docs/user-guide/messaging/webhooks/)。
