---
sidebar_position: 15
title: "本地模型部署指南"
description: "在本地部署开源 LLM 并与 OpenClaw 对接"
---

# 本地模型部署指南

将本地开源模型与 OpenClaw 配合使用，完全免费、数据不出本机。

## 方案一：Ollama（推荐）

[Ollama](https://ollama.com) 是最简单的本地模型运行方式。

### 安装

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# 从 https://ollama.com/download 下载安装包
```

### 下载模型

```bash
ollama pull qwen2.5:7b       # 通义千问 7B（推荐入门）
ollama pull llama3.1:8b      # Llama 3.1 8B
ollama pull deepseek-coder:6.7b  # DeepSeek Coder
```

### 配置 OpenClaw

在 OpenClaw 配置中添加 Ollama 供应商：

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://127.0.0.1:11434/v1",
      "models": {
        "default": "qwen2.5:7b"
      }
    }
  }
}
```

## 方案二：vLLM（高性能）

用于生产环境或 GPU 服务器。

```bash
pip install vllm
vllm serve Qwen/Qwen2.5-7B-Instruct --port 8000
```

OpenClaw 配置：

```json
{
  "providers": {
    "vllm": {
      "baseUrl": "http://127.0.0.1:8000/v1",
      "models": { "default": "Qwen/Qwen2.5-7B-Instruct" }
    }
  }
}
```

## 方案三：LLama.cpp（CPU 也能跑）

```bash
# 下载 GGUF 模型
wget https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2.5-7b-instruct-q4_k_m.gguf

# 启动服务
llama-server -m qwen2.5-7b-instruct-q4_k_m.gguf --port 8080
```

OpenClaw 配置同上，`baseUrl` 指向 `http://127.0.0.1:8080/v1`。

## 推荐模型

| 场景 | 推荐模型 | 最低配置 |
|------|---------|---------|
| 入门 | Qwen2.5-7B | 8GB 显存 |
| 代码 | DeepSeek-Coder-6.7B | 8GB 显存 |
| 中英文 | Llama-3.1-8B | 10GB 显存 |
| 高性能 | Qwen2.5-14B | 16GB 显存 |
| 旗舰 | Qwen2.5-72B | 48GB 显存 |
