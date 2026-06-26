---
sidebar_position: 8
title: "在 OpenClaw 中使用 Python SDK"
description: "将 OpenClaw 作为 Python 库导入，在自有代码中调用 Agent 能力"
---

# 使用 OpenClaw Python SDK

OpenClaw 提供了 Python SDK，你可以在自己的 Python 脚本中导入 OpenClaw 的 Agent 运行时，直接调用其能力。

## 安装

```bash
npm install -g openclaw
```

## 在你的 Python 项目中使用

```python
import subprocess
import json

# 调用 OpenClaw CLI 执行任务
def ask_openclaw(prompt):
    result = subprocess.run(
        ["openclaw", "message", "--prompt", prompt],
        capture_output=True, text=True
    )
    return result.stdout

response = ask_openclaw("总结一下今天的 AI 新闻")
print(response)
```

## 使用 Plugin SDK

OpenClaw 的 Plugin SDK 支持从 Node.js/TypeScript 中编程调用：

```typescript
import { createAgent } from 'openclaw/plugin-sdk';

const agent = createAgent({
  model: 'anthropic/claude-sonnet-4',
});

const response = await agent.run('搜索最新 AI 论文并总结');
console.log(response);
```

详细 API 文档参见 [Plugin SDK 参考](/docs/developer-guide/plugin-llm-access/)。
