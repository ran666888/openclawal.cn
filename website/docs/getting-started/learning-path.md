---
sidebar_position: 3
title: 'Learning Path'
description: 'Choose your learning path through the OpenClaw documentation based on your experience level and goals.'
---
# 学习路径

OpenClaw 可以做很多事情——CLI 助手、Telegram/Discord 机器人、任务自动化、强化学习训练等等。此页面可帮助您根据您的经验水平和想要完成的目标确定从哪里开始以及阅读哪些内容。

:::提示从这里开始
如果您尚未安装 OpenClaw，请先阅读[安装指南](/getting-started/installation)，然后运行[快速入门](/getting-started/quickstart)。下面的所有内容都假设您已经安装了有效的安装。
:::

:::tip 首次提供者设置
初次用户几乎总是想要“hermes setup --portal”——一个 OAuth 涵盖一个模型以及四个工具网关工具（搜索/图像/TTS/浏览器）。请参阅[Nous 门户](/integrations/nous-portal)。
:::

## 如何使用此页面

- **了解您的级别？** 跳转到[经验级别表](#by-experience-level)并按照您所在级别的阅读顺序进行操作。
- **有特定目标？** 跳到[按用例](#by-use-case) 并找到匹配的场景。
- **只是浏览？** 查看[主要功能](#key-features-at-a-glance) 表，快速了解 OpenClaw 的所有功能。

## 按经验水平

|水平|目标|推荐阅读 |预计时间 |
|---|---|---|---|
| **初学者** |启动并运行、进行基本对话、使用内置工具 | [安装](/getting-started/installation) → [快速入门](/getting-started/quickstart) → [CLI 使用](/user-guide/cli) → [配置](/user-guide/configuration) |约 1 小时 |
| **中级** |设置消息机器人，使用内存、cron 作业和技能等高级功能 | [会话](/user-guide/sessions) → [消息](/user-guide/messaging) → [工具](/user-guide/features/tools) → [技能](/user-guide/features/skills) → [内存](/user-guide/features/memory) → [Cron](/user-guide/features/cron) |约 2–3 小时 |
| **高级** |构建自定义工具、创建技能、使用 RL 训练模型、为项目做出贡献 | [架构](/developer-guide/architecture) → [添加工具](/developer-guide/adding-tools) → [创建技能](/developer-guide/creating-skills) → [贡献](/developer-guide/contributing) |约 4–6 小时 |

## 按用例

选择与您想要执行的操作相匹配的场景。每一篇都按照您应该阅读的顺序将您链接到相关文档。

### “我想要一个 CLI 编码助手”

使用 OpenClaw 作为交互式终端助手来编写、审查和运行代码。

1. [安装](/入门/安装)
2. [快速入门](/getting-started/quickstart)
3. [CLI使用](/user-guide/cli)
4. [代码执行](/user-guide/features/code-execution)
5. [上下文文件](/user-guide/features/context-files)
6. [提示与技巧](/guides/tips)

:::提示
使用上下文文件将文件直接传递到您的对话中。 OpenClaw 可以读取、编辑和运行您项目中的代码。
:::

### “我想要一个 Telegram/Discord 机器人”

将 OpenClaw 作为机器人部署在您最喜欢的消息传递平台上。

1. [安装](/入门/安装)
2. [配置](/user-guide/configuration)
3. [消息传递概述](/user-guide/messaging)
4. [电报设置](/user-guide/messaging/telegram)
5. [Discord 设置](/user-guide/messaging/discord)
6. [语音模式](/user-guide/features/voice-mode)
7. [使用 OpenClaw 语音模式](/guides/use-voice-mode-with-hermes)
8. [安全](/用户指南/安全)

有关完整的项目示例，请参阅：
- [每日简报机器人](/guides/daily-briefing-bot)
- [团队电报助理](/guides/team-telegram-assistant)

###“我想自动化任务”

安排重复任务、运行批处理作业或将代理操作链接在一起。

1. [快速入门](/getting-started/quickstart)
2. [Cron 调度](/user-guide/features/cron)
3. [批处理](/user-guide/features/batch-processing)
4. [委托](/user-guide/features/delegation)
5. [挂钩](/user-guide/features/hooks)

:::提示
Cron 作业让 OpenClaw 按计划运行任务 - 每日摘要、定期检查、自动报告 - 无需您在场。
:::

### “我想构建自定义工具/技能”

使用您自己的工具和可重用的技能包扩展 OpenClaw。

1. [插件](/user-guide/features/plugins)
2. [构建 OpenClaw 插件](/guides/build-a-hermes-plugin)
3. [工具概述](/user-guide/features/tools)
4. [技能概述](/user-guide/features/skills)
5. [MCP（模型上下文协议）](/user-guide/features/mcp)
6. [架构](/开发者指南/架构)
7. [添加工具](/developer-guide/adding-tools)
8. [创造技能](/developer-guide/creating-skills)

:::提示
对于大多数自定义工具的创建，从插件开始。 [添加工具](/developer-guide/adding-tools)
页面用于内置 OpenClaw 核心开发，而不是通常的用户/自定义工具路径。
:::

###“我想训练模型”

使用强化学习通过 OpenClaw 的 RL 训练管道（由 [Atropos](https://github.com/NousResearch/atropos) 提供支持）来微调模型行为。

1. [快速入门](/getting-started/quickstart)
2. [配置](/user-guide/configuration)
3. [Atropos RL 环境](https://github.com/NousResearch/atropos)（外部）
4. [提供商路由](/user-guide/features/provider-routing)
5. [架构](/开发者指南/架构)

:::提示
当您已经了解 OpenClaw 如何处理对话和工具调用的基础知识时，强化学习训练效果最佳。如果您是新手，请先运行初学者路径。
:::

### “我想将它用作 Python 库”

以编程方式将 OpenClaw 集成到您自己的 Python 应用程序中。

1. [安装](/入门/安装)
2. [快速入门](/getting-started/quickstart)
3. [Python库指南](/guides/python-library)
4. [架构](/开发者指南/架构)
5. [工具](/用户指南/功能/工具)
6. [会话](/user-guide/sessions)

## 主要功能一览

不确定有什么可用？以下是主要功能的快速目录：

|特色|它有什么作用 |链接 |
|---|---|---|
| **工具** |代理可以调用​​的内置工具（文件 I/O、搜索、shell 等）| [工具](/用户指南/功能/工具) |
| **技能** |添加新功能的可安装插件包 | [技能](/用户指南/功能/技能) |
| **内存** |跨会话持久内存| [内存](/用户指南/功能/内存) |
| **上下文文件** |将文件和目录输入到对话中 | [上下文文件](/用户指南/功能/上下文文件) |
| **MCP** |通过模型上下文协议连接到外部工具服务器 | [MCP](/用户指南/功能/mcp) |
| **计划** |安排重复的代理任务 | [Cron](/用户指南/功能/cron) |
| **代表团** |生成并行工作的子代理 | [委派](/用户指南/功能/委派) |
| **代码执行** |运行以编程方式调用 OpenClaw 工具的 Python 脚本 | [代码执行](/用户指南/功能/代码执行) |
| **浏览器** |网页浏览和抓取 | [浏览器](/用户指南/功能/浏览器) |
| **挂钩** |事件驱动的回调和中间件| [挂钩](/用户指南/功能/挂钩) |
| **批处理** |批量处理多个输入 | [批处理](/用户指南/功能/批处理) |
| **提供商路由** |跨多个 LLM 提供商发送请求 | [提供商路由](/user-guide/features/provider-routing) |

## 接下来要读什么

根据您现在所处的位置：

- **刚刚完成安装？** → 前往[快速入门](/getting-started/quickstart) 运行您的第一个对话。
- **完成快速入门？** → 阅读 [CLI 用法](/user-guide/cli) 和 [配置](/user-guide/configuration) 以自定义您的设置。
- **熟悉基础知识？** → 探索[工具](/user-guide/features/tools)、[技能](/user-guide/features/skills)和[内存](/user-guide/features/memory)以解锁代理的全部功能。
- **组建团队？** → 阅读[安全](/user-guide/security) 和[会话](/user-guide/sessions) 以了解访问控制和对话管理。
- **准备好构建了吗？** → 跳转到[开发人员指南](/developer-guide/architecture) 以了解内部结构并开始贡献。
- **想要实际示例吗？** → 查看[指南](/guides/tips) 部分以获取实际项目和技巧。

:::提示
你不需要阅读所有内容。选择与您的目标相匹配的路径，按顺序点击链接，您将很快提高工作效率。您可以随时返回此页面以查找下一步。
:::