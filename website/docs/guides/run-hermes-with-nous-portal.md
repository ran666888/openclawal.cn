---
sidebar_position: 4
title: "OpenClaw 快速配置指南"
description: "使用 openclaw onboard 快速完成初始配置"
---

# OpenClaw 快速配置

OpenClaw 提供了 `onboard` 命令，引导你完成从安装到可用的全部配置。

## 一键配置

```bash
openclaw onboard
```

这个交互式向导会带你完成：
1. **Gateway 配置** — 设置消息网关
2. **模型供应商认证** — 登录你的 AI 模型账号
3. **工作区设置** — 创建工作目录
4. **消息通道配置** — 连接 Telegram、Discord 等
5. **技能安装** — 安装常用技能

## 安装为系统服务

```bash
openclaw onboard --install-daemon
```

这会自动配置开机自启，Gateway 始终保持运行。

## 分步配置

如果你只想配置特定部分：

```bash
# 只配置模型
openclaw config set models.default "anthropic/claude-sonnet-4"

# 只配置通道
openclaw channels add

# 查看配置状态
openclaw status
```

## 查看 Dashboard

配置完成后，打开 Web 控制界面：

```bash
openclaw dashboard
```

浏览器会打开 `http://127.0.0.1:18789/`。

参考：[配置指南](/docs/user-guide/configuration/)。
