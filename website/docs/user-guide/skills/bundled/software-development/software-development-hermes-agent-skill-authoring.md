---
title: "OpenClaw Skill Authoring — Author in-repo SKILL"
sidebar_label: "OpenClaw Skill Authoring"
description: "Author in-repo SKILL"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 赫尔墨斯特工技能创作

作者 in-repo SKILL.md：frontmatter、验证器、结构。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/软件开发/hermes-agent-skill-authoring` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `skills`、`authoring`、`hermes-agent`、`conventions`、`skill-md` |
|相关技能| [`计划`](/docs/user-guide/skills/bundled/software-development/software-development-plan), [`requesting-code-review`](/docs/user-guide/skills/bundled/software-development/software-development-requesting-code-review) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 编写 OpenClaw-Agent 技能（in-repo）

## 概述

SKILL.md 可以存在于两个地方：

1. **用户本地：** `~/.hermes/skills/<maybe-category>/<name>/SKILL.md` — 个人的，不共享。通过“skill_manage(action='create')”创建。
2. **In-repo（此技能是关于这种情况的）：** `/home/bb/hermes-agent/skills/<category>/<name>/SKILL.md` — 已提交，随包一起提供。使用 `write_file` + `git add`。 `skill_manage(action='create')` 不以该树为目标。

## 何时使用

- 用户要求您添加一项技能“在此分支/存储库/提交中”
- 您正在提交一个可重用的工作流程，该工作流程应随 OpenClaw-agent 一起提供
- 您正在“/home/bb/openclaw/skills/”下编辑现有技能（使用“patch”进行小编辑，使用“write_file”进行重写；“skill_manage”仍然适用于仓库内技能的补丁，但不适用于“create”）

## 必需的前言

事实来源：“tools/skill_manager_tool.py::_validate_frontmatter”。硬性要求：

- 以“---”开头作为第一个字节（无前导空行）。
- 在正文之前以 `\n---\n` 结束。
- 解析为 YAML 映射。
- 存在“名称”字段。
- 存在“描述”字段，≤ **1024 个字符**（“MAX_DESCRIPTION_LENGTH”）。
- 关闭`---`后非空主体。

“技能/软件开发/”下的每项技能使用的同行匹配形状：

````yaml
---
name: my-skill-name # 小写字母，连字符，≤64 个字符 (MAX_NAME_LENGTH)
描述：<trigger>时使用。 <单行行为>。
版本：1.0.0
作者：爱马仕经纪人
许可证：麻省理工学院
元数据：
  爱马仕：
    标签：[简短、描述性、标签]
    related_skills：[其他技能，另一个技能]
---
````

`version` / `author` / `license` / `metadata` 不是由验证器强制执行的，但是每个节点都有它们——省略的话你的技能就会脱颖而出。

## 大小限制

- 描述：≤ 1024 个字符（强制）。
- 完整 SKILL.md：≤ 100,000 个字符（强制为“MAX_SKILL_CONTENT_CHARS”，~36k 令牌）。
- “软件开发/”领域的同行技能为 **8-14k 个字符**。瞄准该范围。如果您要超过 20k，请分成 `references/*.md` 并从 SKILL.md 中引用它们。

## 同行匹配的结构

每个回购技能大致如下：

````
# <标题>

## 概述
一两段：什么和为什么。

## 何时使用
- 子弹式触发器
- “不要用于：”反触发

## <特定于技能的主题部分>
- 快速参考表很常见
- 具有精确命令的代码块
- Hermes特定的配方（通过scripts/run_tests.sh、ui-tui路径等进行测试）

## 常见陷阱
错误及其修复的编号列表。

## 验证清单
- [ ] 操作后验证的复选框列表

## 一次性食谱（可选）
命名场景 → 具体命令序列。
````

并非每个部分都是强制性的，但“概述”+“何时使用”+可操作的正文+陷阱是让该技能感觉像同行的最低限度。

## 目录放置

````
技能/<类别>/<技能名称>/SKILL.md
````

当前在仓库中的类别（使用“ls技能/”确认）：“autonomous-ai-agents”、“creative”、“data-science”、“devops”、“dogfood”、“email”、“gaming”、“github”、“leisure”、“mcp”、“media”、“mlops/*”、“note-takeing”、“productivity”、“red-teaming”、“research”、“smart-home”、 “社交媒体”、“软件开发”。

选择最接近的现有类别。不要随便发明新的顶级品类。

## 工作流程

1. **调查目标类别的同行**：
   ````
   ls 技能/<类别>/
   ````
   阅读 2-3 个同行 SKILL.md 文件以匹配语气和结构。
2. 如果不确定，请检查 `tools/skill_manager_tool.py` 中的验证器约束**。
3. **草稿** 使用 `write_file` 写入 `skills/<category>/<name>/SKILL.md`。
4. **本地验证**：
   ````蟒蛇
   导入 yaml、re、pathlib
   content = pathlib.Path("技能/<类别>/<名称>/SKILL.md").read_text()
   断言 content.startswith("---")
   m = re.search(r'\n---\s*\n', 内容[3:])
   fm = yaml.safe_load(内容[3:m.start()+3])
   在 fm 中断言“名称”，在 fm 中断言“描述”
   断言 len(fm["描述"]) <= 1024
   断言 len(内容) <= 100_000
   ````
5. **Git add + commit** 在活动分支上。
6. **注意：** 当前会话的技能加载器已缓存 - `skill_view` / `skills_list` 在新会话之前不会看到新技能。这是预期的，不是错误。

## 交叉参考其他技能

`metadata.hermes.lated_skills` 在加载时联合两棵树（存储库中的 `skills/` 和 `~/.hermes/skills/`）。您可以从存储库内技能引用用户本地技能，但对于新克隆存储库的其他用户来说，它不会解析。更喜欢仅从仓库内技能中引用仓库内技能。如果经常引用的技能仅存在于“~/.hermes/skills/”中，请考虑将其提升到存储库。

## 编辑现有的 In-Repo 技能

- **小修复（打字错误、添加陷阱、收紧触发器）：** `skill_manage(action='patch', name=..., old_string=..., new_string=...)` 在回购技能上效果很好。
- **主要重写：** `write_file` 整个 SKILL.md。 `skill_manage(action='edit')` 也可以工作，但需要提供完整的新内容。
- **添加支持文件：** `write_file` 到 `skills/<category>/<name>/references/<file>.md`、`templates/<file>` 或 `scripts/<file>`。 `skill_manage(action='write_file')` 也可以工作并强制执行引用/模板/脚本/资产子目录白名单。
- **始终提交**编辑 - 存储库内技能是源代码，而不是运行时状态。

## 常见陷阱

1. **使用 `skill_manage(action='create')` 作为仓库内技能。** 它写入到 `~/.hermes/skills/`，而不是仓库树。使用“write_file”进行存储库内创建。

2. **`---`之前的前导空格。**验证器检查`content.startswith("---")`；任何前导空白行或 BOM 均未通过验证。

3. **描述过于笼统。** 对等描述以“当......时使用”开头，并描述*触发类*，而不是单个任务。 “调试 X 时使用”>“调试 X”。

4. **忘记作者/许可证/元数据块。** 不是验证者强制执行的，但每个节点都有它；省略会使该技能看起来是半成品。

5. **编写一个与对等点重复的技能。** 在创建之前，`ls Skills/<category>/` 并打开 2-3 个对等点。更喜欢扩展现有的技能，而不是创建一个狭窄的兄弟姐妹。

6. **期望当前会话看到新技能。**不会。技能加载器在会话开始时初始化。在新会话中或通过“skill_view”使用确切路径进行验证。

7. **链接到存储库中不存在的技能。** `lated_skills: [some-user-local-skill]` 对您有效，但对其他克隆来说会中断。仅首选存储库内链接。

## 验证清单

- [ ] 文件位于 `skills/<category>/<name>/SKILL.md`（不在 `~/.hermes/skills/` 中）
- [ ] Frontmatter 从字节 0 开始，以 `---` 开始，以 `\n---\n` 结束
- [ ] `name`、`description`、`version`、`author`、`license`、`metadata.hermes.{tags, related_skills}` 全部存在
- [ ] 名称 ≤ 64 个字符，小写字母 + 连字符
- [ ] 描述 ≤ 1024 个字符并以“Use when ...”开头
- [ ] 文件总数 ≤ 100,000 个字符（目标为 8-15k）
- [ ] 结构：`# 标题`→`## 概述`→`## 何时使用`→正文→`## 常见陷阱`→`## 验证清单`
- [ ] `lated_skills` 引用在存储库中解析（或者明确可以是用户本地的）
- [ ] `git add Skills/<category>/<name>/ && git commit` 在预期分支上完成