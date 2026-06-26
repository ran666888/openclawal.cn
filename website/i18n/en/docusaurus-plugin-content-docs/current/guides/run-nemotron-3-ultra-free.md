---
sidebar_position: 12
title: "免费使用 AI 模型"
description: "使用免费或低成本模型运行 OpenClaw"
---

# 免费模型使用指南

OpenClaw 支持多种免费或低成本模型方案。

## 方案一：OpenRouter 免费模型

[OpenRouter](https://openrouter.ai) 提供多种免费模型。在 OpenClaw 配置中添加：

```bash
openclaw config set agents.defaults.model "openrouter/meta-llama/llama-3.2-3b-instruct:free"
```

免费模型列表：
- `meta-llama/llama-3.2-3b-instruct:free`
- `google/gemma-2-2b-it:free`
- `microsoft/phi-3-mini-4k-instruct:free`

## 方案二：本地模型（完全免费）

参见[本地模型部署指南](/docs/guides/local-llm-on-mac/)。

## 方案三：各平台免费额度

| 供应商 | 免费额度 |
|--------|---------|
| Google Gemini | 免费层 60 次/分钟 |
| 通义千问 | 免费 100 万 Token/月 |
| DeepSeek | 注册送额度 |
| GLM | 免费额度 |

## 模型配置

模型配置也可以通过编辑配置文件完成：

```bash
openclaw config edit
```

或在 Web Dashboard 中配置。参考[模型配置](/docs/user-guide/configuring-models/)。
