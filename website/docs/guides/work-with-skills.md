---
sidebar_position: 12
title: "Working with Skills"
description: "Find, install, use, and create skills — on-demand knowledge that teaches OpenClaw new workflows"
---
# 运用技能工作

技能是按需知识文档，教 OpenClaw 如何处理特定任务——从生成 ASCII 艺术到管理 GitHub PR。本指南将引导您日常使用它们。

完整的技术参考请参见[技能系统](/user-guide/features/skills)。

---

## 寻找技能

每个 OpenClaw 安装都附带捆绑的技能。查看可用的内容：

````bash
# 在任何聊天会话中：
/技能

# 或者从 CLI:
爱马仕技能列表
````

这显示了包含名称和描述的紧凑列表：

````
ascii-art 使用 pyfiglet、cowsay、boxes 生成 ASCII 艺术作品...
arXiv 从 arXiv 搜索和检索学术论文...
github-pr-workflow 完整的 PR 生命周期 — 创建分支、提交...
计划 计划模式 — 检查上下文、编写 Markdown...
excalidraw 使用 Excalidraw 创建手绘风格图表...
````

### 寻找技能

````bash
# 按关键字搜索
/技能搜索泊坞窗
/技能搜索音乐
````

### 技能中心

官方可选技能（默认情况下不活跃的较重或利基技能）可通过中心获得：

````bash
#浏览官方可选技能
/技能浏览

# 搜索中心
/技能搜索区块链
````

---

## 使用技能

每个安装的技能都会自动成为斜杠命令。只需输入其名称：

````bash
# 加载一个技能并给它一个任务
/ascii-art 制作一个横幅，上面写着“HELLO WORLD”
/plan 为待办事项应用程序设计 REST API
/github-pr-workflow 为 auth 重构创建 PR

# 只需技能名称（无任务）即可加载它并让您描述您需要什么
/excalidraw
````

你还可以通过自然对话触发技能——要求 OpenClaw 使用特定技能，它会通过“skill_view”工具加载它。

### 渐进式披露

技能使用令牌有效的加载模式。代理不会立即加载所有内容：

1. **`skills_list()`** — 所有技能的紧凑列表（~3k 令牌）。在会话开始时加载。
2. **`skill_view(name)`** — 一项技能的完整 SKILL.md 内容。当代理决定需要该技能时加载。
3. **`skill_view(name, file_path)`** — 技能内的特定参考文件。仅在需要时加载。

这意味着技能在实际使用之前不会消耗代币。

---

## 从集线器安装

官方可选技能随 OpenClaw 一起提供，但默认情况下未激活。显式安装它们：

````bash
# 安装官方可选技能
Hermes技能安装官方/research/arxiv

# 在聊天会话中从集线器安装
/skills 安装官方/creative/songwriting-and-ai-music

# 直接从任何 HTTP(S) URL 安装单文件 SKILL.md
爱马仕技能安装 https://sharethis.chat/SKILL.md
/skills 安装 https://example.com/SKILL.md --name my-skill
````

会发生什么：
1.将skill目录复制到`~/.hermes/skills/`
2.它出现在你的`skills_list`输出中
3.它可以作为斜杠命令使用

:::提示
安装的技能在新会话中生效。如果您希望它在当前会话中可用，请使用“/reset”重新开始，或添加“--now”立即使提示缓存失效（下一轮会花费更多令牌）。
:::

### 验证安装

````bash
# 检查它是否存在
爱马仕技能一览| grep arxiv

# 或者在聊天中
/技能搜索 arxiv
````

---

## 插件提供的技能

插件可以使用命名空间名称（“plugin:skill”）捆绑自己的技能。这可以防止名称与内置技能发生冲突。

````bash
# 通过其限定名称加载插件技能
Skill_view("超能力：写作计划")

# 具有相同基础名称的内置技能不受影响
Skill_view(“写作计划”)
````

插件技能**未**在系统提示中列出，也不会出现在“skills_list”中。它们是选择加入的——当您知道插件提供了它们时，显式加载它们。加载后，代理会看到一个横幅，其中列出了来自同一插件的同级技能。

有关如何在您自己的插件中发布技能，请参阅[构建 OpenClaw 插件 → 捆绑技能](/guides/build-a-hermes-plugin#bundle-skills)。

---

## 配置技能设置

一些技能在其 frontmatter 中声明了他们需要的配置：

````yaml
元数据：
  爱马仕：
    配置：
      - 密钥：tenor.api_key
        描述：“GIF 搜索的 Tenor API 密钥”
        提示：“输入您的 Tenor API 密钥”
        网址：“https://developers.google.com/tenor/guides/quickstart”
````

当首次加载带有配置的技能时，OpenClaw 会提示您输入值。它们存储在“skills.config.*”下的“config.yaml”中。

从 CLI 管理技能配置：

````bash
# 特定技能的交互式配置
Hermes 技能配置 gif 搜索

# 查看所有技能配置
爱马仕配置展示| grep '^技能\.config'
````

---

## 创造你自己的技能

技能只是带有 YAML frontmatter 的 markdown 文件。创建一个只需不到五分钟。

### 1.创建目录

````bash
mkdir -p ~/.hermes/skills/my-category/my-skill
````

### 2.编写SKILL.md

```markdown title="~/.hermes/skills/my-category/my-skill/SKILL.md"
---
名称：我的技能
描述：简要描述该技能的作用
版本：1.0.0
元数据：
  爱马仕：
    标签：[我的标签，自动化]
    类别：我的类别
---

# 我的技能

## 何时使用
当用户询问[特定主题]或需要[特定任务]时使用此技能。

## 程序
1、首先检查【前提条件】是否可用
2. 运行“命令--with-flags”
3. 解析输出并呈现结果

## 陷阱
- 常见故障：[描述]。修复：[解决方案]
- 注意[边缘情况]

## 验证
运行“check-command”以确认结果正确。
````

### 3. 添加参考文件（可选）

技能可以包括代理按需加载的支持文件：

````
我的技能/
├── SKILL.md # 主要技能文档
├── 参考资料/
│ ├── api-docs.md # 代理可查阅的API参考
│ └── Examples.md # 输入/输出示例
├── 模板/
│ └── config.yaml # Agent 可以使用的模板文件
└── 脚本/
    └── setup.sh # 代理可以执行的脚本
````

在您的 SKILL.md 中引用这些：

``降价
有关 API 详细信息，请加载参考：`skill_view("my-skill", "references/api-docs.md")`
````

### 4. 测试一下

开始新的会话并尝试您的技能：

````bash
OpenClaw chat -q "/my-skill 帮我解决这个问题"
````

该技能会自动出现——无需注册。将其放入“~/.hermes/skills/”即可。

:::信息
代理还可以使用“skill_manage”自行创建和更新技能。在解决了一个复杂的问题后，赫尔墨斯可能会提出将该方法保存为下次的技能。
:::

---

## 每个平台的技能管理

控制哪些技能在哪些平台上可用：

````bash
爱马仕技能
````

这将打开一个交互式 TUI，您可以在其中启用或禁用每个平台的技能（CLI、Telegram、Discord 等）。当您希望某些技能仅在特定环境中可用时非常有用 - 例如，将开发技能保留在 Telegram 之外。

---

## 技能与记忆

两者在会话中都是持久的，但它们有不同的目的：

| |技能 |内存|
|---|---|---|
| **什么** |程序性知识——如何做事|事实知识——事物是什么|
| **何时** |仅在相关时按需加载 |自动注入每个会话 |
| **尺寸** |可以很大（数百行）|应该紧凑（仅限关键事实）|
| **成本** |加载前为零令牌 |代币成本虽小但恒定|
| **示例** | “如何部署到 Kubernetes”| “用户更喜欢深色模式，生活在 PST 中” |
| **谁创造** |您、代理或从 Hub 安装 |基于对话的代理|

**经验法则：** 如果您将其放入参考文档中，那么它就是一项技能。如果你把它写在便利贴上，那就是记忆。

---

## 提示

**保持技能重点。** 试图涵盖“所有 DevOps”的技能将太长且太模糊。涵盖“将 Python 应用程序部署到 Fly.io”的技能足够具体，真正有用。

**让代理创建技能。** 在完成复杂的多步骤任务后，Hermes 通常会提出将该方法保存为技能。说是 - 这些由代理编写的技能捕获了确切的工作流程，包括沿途发现的陷阱。

**使用类别。** 将技能组织到子目录中（`~/.hermes/skills/devops/`、`~/.hermes/skills/research/` 等）。这使得列表易于管理，并帮助代理更快地找到相关技能。

**当技能过时时更新技能。** 如果您使用一项技能并遇到了该技能未涵盖的问题，请告诉 Hermes 用您学到的知识更新该技能。不保留的技能就会成为负债。

---

*有关完整的技能参考 - frontmatter 字段、条件激活、外部目录等 - 请参阅[技能系统](/user-guide/features/skills)。*