---
sidebar_position: 18
title: "GitHub PR 审查 Agent"
description: "让 OpenClaw 自动审查 GitHub Pull Request"
---

# GitHub PR 审查 Agent

让 OpenClaw 自动审查 GitHub Pull Request，检查代码质量、提出改进建议。

## 前提条件

- GitHub Token（具有 PR 读取权限）
- OpenClaw 已配置模型和 Gateway

## 手动审查

在 OpenClaw 对话中直接请求：

```
请审查这个 PR: https://github.com/owner/repo/pull/123
重点检查：代码风格、潜在 bug、性能问题
```

Agent 会自动拉取 PR diff 并进行分析。

## 自动审查（Webhook）

通过 Webhook 实现自动审查，参见 [Webhook GitHub PR 评论](/docs/guides/webhook-github-pr-review/)。

## GitHub 技能

安装 GitHub 相关技能以获得更好的 PR 处理能力：

```bash
openclaw skills search github
openclaw skills install clawhub:github
```

技能会教会 Agent 如何处理 GitHub API、理解 PR 工作流等。
