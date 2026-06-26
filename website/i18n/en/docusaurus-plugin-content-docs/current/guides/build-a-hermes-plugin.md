---
sidebar_position: 16
title: "构建 OpenClaw 插件"
description: "使用 Plugin SDK 开发 OpenClaw 插件"
---

# 构建 OpenClaw 插件

OpenClaw 的插件系统支持扩展工具、通道、供应商和技能。

## 快速开始

```bash
# 创建一个新插件
mkdir my-plugin && cd my-plugin
npm init
npm install @openclaw/plugin-sdk
```

## 插件结构

```
my-plugin/
├── package.json
├── plugin.json          # 插件清单
├── src/
│   └── index.ts         # 插件入口
└── skills/
    └── my-skill/
        └── SKILL.md     # 可选技能
```

## plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "我的第一个插件",
  "contracts": {
    "tools": ["my-tool"],
    "skills": ["my-skill"]
  }
}
```

## 安装插件

```bash
# 从本地目录安装
openclaw plugins install ./my-plugin

# 从 ClawHub 安装
openclaw plugins install clawhub:plugin-name

# 查看已安装
openclaw plugins list
```

参考 [Plugin SDK 文档](/docs/developer-guide/plugin-llm-access/)。
