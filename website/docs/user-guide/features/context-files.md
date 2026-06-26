---
sidebar_position: 8
title: "Context Files"
description: "Project context files — .hermes.md, AGENTS.md, CLAUDE.md, global SOUL.md, and .cursorrules — automatically injected into every conversation"
---
# 上下文文件

OpenClaw 自动发现并加载影响其行为方式的上下文文件。有些是项目本地的，可以从您的工作目录中发现。 `SOUL.md` 现在对于 OpenClaw 实例是全局的，并且仅从 `HERMES_HOME` 加载。

## 支持的上下文文件

|文件|目的|发现 |
|------|---------|------------| 
| **.hermes.md** / **HERMES.md** |项目说明（最高优先级）|走到 git root |
| **代理.md** |项目说明、惯例、架构 |启动时的 CWD + 子目录逐步 |
| **克劳德.md** |克劳德代码上下文文件（也检测到）|启动时的 CWD + 子目录逐步 |
| **灵魂.md** |此爱马仕实例的全局个性和色调定制 |仅限`HERMES_HOME/SOUL.md` |
| **.cursorrules** |光标 IDE 编码约定 |仅 CWD |
| **.cursor/rules/*.mdc** |光标 IDE 规则模块 |仅 CWD |

:::info 优先系统
每个会话仅加载 **一个** 项目上下文类型（第一个匹配获胜）：`.hermes.md`→`AGENTS.md`→`CLAUDE.md`→`.cursorrules`。 **SOUL.md** 始终作为代理身份独立加载（插槽#1）。
:::

## 代理.md

`AGENTS.md` 是主要项目上下文文件。它告诉代理您的项目是如何构建的、要遵循哪些约定以及任何特殊说明。

### 渐进式子目录发现

在会话开始时，OpenClaw 将“AGENTS.md”从工作目录加载到系统提示符中。当代理在会话期间导航到子目录时（通过“read_file”、“terminal”、“search_files”等），它**逐渐发现**这些目录中的上下文文件，并在它们变得相关时将它们注入到对话中。

````
我的项目/
├── AGENTS.md ← 启动时加载（系统提示符）
├── 前端/
│ └── AGENTS.md ← Agent 读取前端/文件时发现
├── 后端/
│ └── AGENTS.md ← Agent 读取后端/文件时发现
└── 共享/
    └── AGENTS.md ← Agent 读取共享/文件时发现
````

与在启动时加载所有内容相比，这种方法有两个优点：
- **没有系统提示膨胀** - 子目录提示仅在需要时出现
- **提示缓存保存** — 系统提示在回合中保持稳定

每个会话最多检查每个子目录一次。该发现还会遍历父目录，因此即使“backend/src/”没有自己的上下文文件，读取“backend/src/main.py”也会发现“backend/AGENTS.md”。

:::信息
子目录上下文文件与启动上下文文件经历相同的[安全扫描](#security-prompt-injection-protection)。恶意文件被阻止。
:::

### 示例 AGENTS.md

``降价
# 项目背景

这是一个带有 Python FastAPI 后端的 Next.js 14 Web 应用程序。

## 架构
- 前端：Next.js 14，在“/frontend”中带有 App Router
- 后端：`/backend`中的FastAPI，使用SQLAlchemy ORM
- 数据库：PostgreSQL 16
- 部署：Hetzner VPS 上的 Docker Compose

## 惯例
- 对所有前端代码使用 TypeScript 严格模式
- Python 代码遵循 PEP 8，到处使用类型提示
- 所有 API 端点返回具有“{data, error, meta}”形状的 JSON
- 测试进入 `__tests__/` 目录（前端）或 `tests/` （后端）

## 重要提示
- 切勿直接修改迁移文件 - 使用 Alembic 命令
- `.env.local` 文件有真正的 API 密钥，不要提交它
- 前端端口为3000，后端端口为8000，DB为5432
````

## 灵魂.md

`SOUL.md` 控制代理的个性、语气和沟通风格。有关完整详细信息，请参阅[个性](/user-guide/features/personality) 页面。

**地点：**

- `~/.hermes/SOUL.md`
- 或“$HERMES_HOME/SOUL.md”（如果您使用自定义主目录运行 Hermes）

重要细节：

- 如果还不存在，Hermes 会自动生成默认的“SOUL.md”
- Hermes 仅从“HERMES_HOME”加载“SOUL.md”
- Hermes 不会探测“SOUL.md”的工作目录
- 如果文件为空，则“SOUL.md”中的任何内容都不会添加到提示中
- 如果文件有内容，则在扫描和截断后逐字注入内容

## .cursorrules

Hermes 与 Cursor IDE 的 `.cursorrules` 文件和 `.cursor/rules/*.mdc` 规则模块兼容。如果这些文件存在于您的项目根目录中并且没有找到更高优先级的上下文文件（`.hermes.md`、`AGENTS.md` 或 `CLAUDE.md`），它们将作为项目上下文加载。

这意味着使用 Hermes 时会自动应用现有的游标约定。

## 如何加载上下文文件

### 启动时（系统提示符）

上下文文件由 `agent/prompt_builder.py` 中的 `build_context_files_prompt()` 加载：

1. **扫描工作目录** — 检查 `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` （第一个匹配获胜）
2. **内容被读取** — 每个文件被读取为 UTF-8 文本
3. **安全扫描** — 检查内容的提示注入模式
4. **截断** — 超过 `context_file_max_chars` 个字符（默认 20,000）的文件将被头/尾截断（70% 头，20% 尾，中间有一个标记）
5. **Assembly** - 所有部分都组合在“# Project Context”标题下
6. **注入**——组装好的内容添加到系统提示符中

### 会话期间（渐进式发现）

`agent/subdirectory_hints.py` 中的 `SubdirectoryHintTracker` 监视文件路径的工具调用参数：

1. **路径提取** — 在每次工具调用之后，从参数（`path`、`workdir`、shell 命令）中提取文件路径
2. **Ancestor walk** — 检查目录和最多 5 个父目录（在已访问过的目录处停止）
3. **提示加载** — 如果找到 `AGENTS.md`、`CLAUDE.md` 或 `.cursorrules`，则会加载它（每个目录的第一个匹配项）
4. **安全扫描** — 与启动文件相同的提示注入扫描
5. **截断** — 每个文件上限为 8,000 个字符
6. **注入** - 附加到工具结果中，因此模型可以自然地在上下文中看到它

最后的提示部分大致如下：

````文本
# 项目背景

以下项目上下文文件已加载并应遵循：

## 代理.md

[此处为您的 AGENTS.md 内容]

## .cursorrules

[此处为您的 .cursorrules 内容]

[这里是您的 SOUL.md 内容]
````

请注意，SOUL 内容是直接插入的，没有额外的包装文本。

## 安全性：即时注入保护

所有上下文文件在包含之前都会被扫描以查找潜在的提示注入。扫描仪检查：

- **指令覆盖尝试**：“忽略先前的指令”，“忽略您的规则”
- **欺骗模式**：“不告诉用户”
- **系统提示覆盖**：“系统提示覆盖”
- **隐藏 HTML 注释**：`<!-- 忽略说明 -->`
- **隐藏的 div 元素**：`<div style="display:none">`
- **凭证泄露**：`curl ... $API_KEY`
- **秘密文件访问**：`cat .env`，`cat凭据`
- **不可见字符**：零宽度空格、双向覆盖、单词连接符

如果检测到任何威胁模式，该文件将被阻止：

````
[已阻止：AGENTS.md 包含潜在的提示注入 (prompt_injection)。内容未加载。]
````

:::警告
此扫描程序可以防止常见的注入模式，但它不能替代检查共享存储库中的上下文文件。始终验证非您创作的项目中的 AGENTS.md 内容。
:::

## 大小限制

|限制|价值|
|--------|--------|
|每个文件的最大字符数 | `context_file_max_chars`（默认 20,000，~7,000 个标记）|
|头截断率| 70% |
|尾部截断率| 20% |
|截断标记| 10%（显示字符计数并建议使用文件工具）|

当文件超出配置的限制时，截断消息将显示：

````
[...截断的 AGENTS.md：保留 25000 个字符中的 14000+4000 个。使用文件工具读取完整文件。]
````

## 有效上下文文件的提示

:::tip AGENTS.md 的最佳实践
1. **保持简洁** — 保持在您配置的 `context_file_max_chars` 下；代理每次都会读取它
2. **带标题的结构** — 使用 `##` 部分来表示架构、约定和重要注释
3. **包括具体示例** — 显示首选代码模式、API 形状、命名约定
4. **提及不该做的事情** — “永远不要直接修改迁移文件”
5. **列出关键路径和端口** - 代理将它们用于终端命令
6. **随着项目的发展进行更新** - 陈旧的上下文比没有上下文更糟糕
:::

### 每个子目录上下文

对于 monorepos，将子目录特定的指令放入嵌套的 AGENTS.md 文件中：

``降价
<!-- 前端/AGENTS.md -->
# 前端上下文

- 使用`pnpm`而不是`npm`进行包管理
- 组件位于`src/components/`中，页面位于`src/app/`中
- 使用 Tailwind CSS，切勿使用内联样式
- 使用“pnpm test”运行测试
````

``降价
<!-- 后端/AGENTS.md -->
# 后端上下文

- 使用“poetry”进行依赖管理
- 使用 `poetry run uvicorn main:app --reload` 运行开发服务器
- 所有端点都需要 OpenAPI 文档字符串
- 数据库模型位于“models/”中，模式位于“schemas/”中
````