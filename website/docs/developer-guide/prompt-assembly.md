---
sidebar_position: 5
title: "Prompt Assembly"
description: "How OpenClaw builds the system prompt, preserves cache stability, and injects ephemeral layers"
---
# 提示组装

赫尔墨斯故意区分：

- **缓存系统提示状态**
- **临时 API 调用时间添加**

这是项目中最重要的设计选择之一，因为它会影响：

- 代币使用
- 提示缓存有效性
- 会话连续性
- 记忆正确性

主要文件：

- `run_agent.py`
-`代理/prompt_builder.py`
- `工具/memory_tool.py`

## 缓存系统提示层

缓存的系统提示符被组装为三个有序层（请参阅“agent/system_prompt.py”）：

1. **稳定** — 身份（`SOUL.md`或后备）、工具/模型指导、技能提示、环境提示、平台提示
2. **context** — 调用者提供的 `system_message` 加上项目上下文文件 (`.hermes.md` / `AGENTS.md` / `CLAUDE.md` / `.cursorrules`)
3. **易失性** - 内置内存快照（`MEMORY.md`），用户配置文件快照（`USER.md`），外部内存提供者块，时间戳/会话/模型/提供者行

最终的系统提示符连接为：“stable”→“context”→“volatile”。

此顺序对于优先讨论很重要：
- 技能是**稳定**层的一部分
- 内存/配置文件快照是**易失性**层的一部分
- 两者仍然在缓存的系统提示中（它们不会作为临时的中转覆盖注入）

当设置了“skip_context_files”（例如，子代理委托）时，不会加载 SOUL.md，而是使用硬编码的“DEFAULT_AGENT_IDENTITY”。

###具体例子：组装系统提示

这是当所有层都存在时最终系统提示符的简化视图（注释显示每个部分的来源）：

````
# 第 1 层：代理身份（来自 ~/.hermes/SOUL.md）
你是 Hermes，Nous Research 创建的人工智能助手。
您是一位专家软件工程师和研究员。
您重视正确性、清晰度和效率。
...

# 第 2 层：工具感知行为指导
您在各个会话中都有持久的记忆。使用保存持久事实
记忆工具：用户偏好、环境细节、工具怪癖、
和稳定的约定。每回合都会注入内存，所以请保持
它紧凑并专注于以后仍然重要的事实。
...
当用户引用过去对话中的内容或您的内容时
怀疑存在相关的跨会话上下文，请使用 session_search
在要求他们重复之前先回忆一下。

# 工具使用强制（仅适用于 GPT/Codex 模型）
您必须使用您的工具来采取行动 - 不要描述您的内容
会做或计划做但实际上没有做。
...

# 第 3 层：Honcho 静态块（激活时）
[本町性格/背景数据]

# 第 4 层：可选系统消息（来自配置或 API）
[用户配置的系统消息覆盖]

# 第 5 层：冻结内存快照
## 持久内存
- 用户更喜欢 Python 3.12，使用 pyproject.toml
- 默认编辑器是 nvim
- 在 ~/code/atlas 中从事项目“atlas”
- 时区：美国/太平洋

# 第 6 层：冻结用户配置文件快照
## 用户资料
- 姓名：爱丽丝
- GitHub: alice-dev

# 第7层：技能索引
## 技能（强制）
回复之前，先浏览一下下面的技能。如果一个明显匹配
您的任务，使用 Skill_view(name) 加载它并按照其说明进行操作。
...
<可用技能>
  软件开发：
    - 代码审查：结构化代码审查工作流程
    - 测试驱动开发：TDD 方法
  研究：
    - arXiv：搜索和总结 arXiv 论文
</可用技能>

# 第 8 层：上下文文件（来自项目目录）
# 项目背景
以下项目上下文文件已加载并应遵循：

## 代理.md
这是阿特拉斯项目。使用 pytest 进行测试。主要
入口点是 src/atlas/main.py。始终先运行 `make lint`
承诺。

# 第 9 层：时间戳+会话
当前时间：2026-03-30T14:30:00-07:00
会话：abc123

# 第10层：平台提示
您是 CLI AI 代理。尽量不要使用markdown而使用简单的文本
可在终端内渲染。
````

## 自定义平台提示

平台提示（上面第 10 层）是每个表面的指导 OpenClaw
为 Telegram、WhatsApp、Slack、CLI 和其他平台注入 — 用于
例如“你在终端上，避免使用 Markdown。”内置默认值
位于“PLATFORM_HINTS”（“agent/system_prompt.py”）中；插件提供
平台通过平台注册表提供它们的信息。

管理员可以附加或替换单个平台的提示
通过顶级“platform_hints”键“config.yaml”，无需触摸
任何其他平台：

````yaml
平台提示：
  微信：
    附加：>
      当表格输出有用时，调用 table_formatting
      技能而不是发出 Markdown 表。
  松弛：
    替换为：“您在 Slack 上。保持紧凑的响应并避免宽表。”
  电报：“更喜欢短消息；分开长答案。”   # 简写=追加
````

- `append` — 保留内置提示并在其后添加额外的文本。
- `replace` — 完全替换内置提示。
- 一个裸字符串——“append”的简写。
- 当两者都存在时，“replace”优于“append”。
- 格式错误的条目会被防御性地忽略并退回到
  未修改的默认值，因此错误的配置值永远不会中断提示
  跨平台组装或泄漏。

当构建系统提示符（会话开始，
并再次进行压缩，因为这会重建提示）。它产生一个
固定配置的字节稳定提示，因此它位于 **稳定** 层
与内置提示一起并且不会破坏提示缓存 - 它是
不是冻结提示的实时会话中期突变。

## SOUL.md 如何出现在提示符中

`SOUL.md` 位于 `~/.hermes/SOUL.md` 并用作代理的身份 - 系统提示符的第一部分。 `prompt_builder.py` 中的加载逻辑工作如下：

````蟒蛇
# 来自agent/prompt_builder.py（简化）
def load_soul_md() -> 可选[str]:
    Soul_path = get_hermes_home() / "SOUL.md"
    如果不是 Soul_path.exists():
        返回无
    内容 = Soul_path.read_text(encoding="utf-8").strip()
    content = _scan_context_content(content, "SOUL.md") # 安全扫描
    content = _truncate_content(content, "SOUL.md") # 上限默认为 20k 字符，可配置
    返回内容
````

当“load_soul_md()”返回内容时，它会替换硬编码的“DEFAULT_AGENT_IDENTITY”。然后使用“skip_soul=True”调用“build_context_files_prompt()”函数，以防止 SOUL.md 出现两次（一次作为身份，一次作为上下文文件）。

如果`SOUL.md`不存在，系统会回退到：

````
你是Hermes Agent，Nous Research打造的智能AI助手。
你乐于助人、知识渊博且直接。您可以广泛地帮助用户
一系列任务，包括回答问题、编写和编辑代码，
通过您的工具分析信息、创造性工作和执行行动。
您清晰地沟通，在适当的时候承认不确定性，并确定优先顺序
除非下面另有说明，否则要真正有用而不是冗长。
在探索和调查中要有针对性且高效。
````

## 上下文文件是如何注入的

`build_context_files_prompt()` 使用 **优先级系统** - 仅加载一个项目上下文类型（第一个匹配获胜）：

````蟒蛇
# 来自agent/prompt_builder.py（简化）
def build_context_files_prompt（cwd =无，skip_soul = False）：
    cwd_path = 路径(cwd).resolve()

    # 优先级：第一场比赛获胜 - 仅加载一个项目上下文
    项目上下文 = (
        _load_hermes_md(cwd_path) # 1. .hermes.md / HERMES.md （走到 git root）
        或 _load_agents_md(cwd_path) # 2. AGENTS.md（仅限 cwd）
        或 _load_claude_md(cwd_path) # 3. CLAUDE.md（仅限 cwd）
        或 _load_cursorrules(cwd_path) # 4. .cursorrules / .cursor/rules/*.mdc
    ）

    部分 = []
    如果项目上下文：
        sections.append(project_context)

    # 来自 HERMES_HOME 的 SOUL.md（独立于项目上下文）
    如果不是skip_soul：
        灵魂内容 = load_soul_md()
        如果灵魂内容：
            sections.append(soul_content)

    如果不是部分：
        返回“”

    返回（
        "# 项目上下文\n\n"
        “以下项目上下文文件已加载”
        “并且应该遵循：\n\n”
        + "\n".join(节)
    ）
````

### 上下文文件发现详细信息

|优先|文件 |搜索范围 |笔记|
|----------|--------|-------------|--------|
| 1 | `.hermes.md`、`HERMES.md` | CWD 至 git root | OpenClaw-native 项目配置 |
| 2 | `代理.md` |仅 CWD |常用代理指令文件 |
| 3 | `克劳德.md` |仅 CWD |克劳德代码兼容性 |
| 4 | `.cursorrules`、`.cursor/rules/*.mdc` |仅 CWD |光标兼容性 |

所有上下文文件是：
- **安全扫描** — 检查提示注入模式（不可见的 unicode、“忽略先前的说明”、凭证泄露尝试）
- **截断** — 使用带有截断标记的 70/20 头/尾比，上限为 `context_file_max_chars` 字符（默认 20,000）
- **YAML frontmatter 被删除** — `.hermes.md` frontmatter 被删除（保留用于将来的配置覆盖）

## 仅 API 调用时间层

这些是故意“不”作为缓存系统提示的一部分保留的：

- `临时系统提示`
- 预填充消息
- 网关派生的会话上下文覆盖
- 稍后回合 Honcho/外部召回注入到当前回合用户消息中

`pre_llm_call` 插件上下文也位于此 API 调用时路径中：它附加到当前回合的 **用户消息**，而不是写入缓存的系统提示符。当多个插件返回上下文时，OpenClaw 会连接这些上下文块（请参阅 [Hooks → `pre_llm_call`](../user-guide/features/hooks.md#pre_llm_call)）。

这种分离使稳定前缀能够稳定地进行缓存。

## 内存快照

本地内存和用户配置文件数据在系统提示的**易失性层**中捕获。会话中写入更新磁盘状态，但不会改变已构建的缓存系统提示，直到运行重建路径（新会话或显式失效/重建流程，例如压缩触发的重建）。

## 上下文文件

`agent/prompt_builder.py` 使用 **优先级系统** 扫描和清理项目上下文文件 - 仅加载一种类型（第一个匹配获胜）：

1. `.hermes.md` / `HERMES.md` （走到 git root）
2. `AGENTS.md` （启动时的 CWD；在会话期间通过 `agent/subdirectory_hints.py` 逐步发现子目录）
3.`CLAUDE.md`（仅限 CWD）
4. `.cursorrules` / `.cursor/rules/*.mdc` （仅限 CWD）

`SOUL.md` 通过 `load_soul_md()` 单独加载身份槽。当它加载成功时，`build_context_files_prompt(skip_soul=True)`会阻止它出现两次。

长文件在注入之前会被截断。

## 技能指数

当技能工具可用时，技能系统会向提示提供紧凑的技能索引。

## 支持的提示自定义界面

大多数用户应该将“agent/prompt_builder.py”视为实现代码，而不是配置界面。支持的自定义路径是更改 OpenClaw 已加载的提示输入，而不是就地编辑 Python 模板。

### 首先使用这些表面

- `~/.hermes/SOUL.md` — 用您自己的代理角色和站立行为替换内置的默认身份块。
- `~/.hermes/MEMORY.md` 和 `~/.hermes/USER.md` — 提供持久的跨会话事实和用户配置文件数据，应将其快照到新会话中。
- 项目上下文文件，例如“.hermes.md”、“HERMES.md”、“AGENTS.md”、“CLAUDE.md”或“.cursorrules”——注入特定于存储库的工作规则。
- 技能——打包可重用的工作流程和参考，无需编辑核心提示代码。
- 可选的系统提示配置/API 覆盖 - 添加特定于部署的指令文本，无需分叉 OpenClaw。
- 临时覆盖，例如“HERMES_EPHEMERAL_SYSTEM_PROMPT”或预填充消息 - 添加回合范围的指导，该指导不应成为缓存提示前缀的一部分。

### 何时编辑代码

仅当您有意维护分叉或贡献上游行为更改时才编辑“agent/prompt_builder.py”。该文件汇集了每个会话的提示管道、缓存边界和注入顺序。直接编辑有全局产品更改，而不是针对每个用户的提示定制。

换句话说：

- 如果您想要不同的助理身份，请编辑“SOUL.md”
- 如果您想要不同的回购规则，请编辑项目上下文文件
- 如果您想要可重复使用的操作程序，请添加或修改技能
- 如果您想更改 OpenClaw 为每个人组装提示的方式，请更改 Python 并将其视为代码贡献

## 为什么提示程序集要这样分割

该架构经过特意优化，以：

- 保留提供者端提示缓存
- 避免不必要地改变历史记录
- 保持内存语义易于理解
- 让网关/ACP/CLI 添加上下文，而不会破坏持久提示状态

## 相关文档

- [上下文压缩和提示缓存](./context-compression-and-caching.md)
- [会话存储](./session-storage.md)
- [网关内部结构](./gateway-internals.md)