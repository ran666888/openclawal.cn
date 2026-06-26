---
title: "Codebase Inspection — Inspect codebases w/ pygount: LOC, languages, ratios"
sidebar_label: "Codebase Inspection"
description: "Inspect codebases w/ pygount: LOC, languages, ratios"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 代码库检查

使用 pygount 检查代码库：LOC、语言、比率。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/github/codebase-inspection` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `LOC`、`代码分析`、`pygount`、`代码库`、`指标`、`存储库` |
|相关技能| [`github-repo-management`](/docs/user-guide/skills/bundled/github/github-github-repo-management) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 使用 pygount 进行代码库检查

使用“pygount”分析存储库的代码行数、语言细分、文件计数以及代码与注释比率。

## 何时使用

- 用户询问 LOC（代码行数）计数
- 用户想要存储库的语言细分
- 用户询问代码库大小或组成
- 用户想要代码与评论的比率
- 一般“这个仓库有多大”问题

## 先决条件

````bash
pip install --break-system-packages pygount 2>/dev/null || pip 安装 pygount
````

## 1. 基本总结（最常见）

获取包含文件计数、代码行和注释行的完整语言细分：

````bash
cd /路径/到/repo
pygount --format=摘要 \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  。
````

**重要：** 始终使用 `--folders-to-skip` 来排除依赖/构建目录，否则 pygount 会抓取它们并花费很长时间或挂起。

## 2. 常见文件夹排除

根据项目类型进行调整：

````bash
# Python 项目
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript 项目
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,覆盖率"

# 一般包罗万象
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,供应商,third_party"
````

## 3. 按特定语言过滤

````bash
# 只统计Python文件
pygount --suffix=py --format=summary 。

# 只计算Python和YAML
pygount --suffix=py,yaml,yml --format=summary 。
````

## 4. 详细的逐个文件输出

````bash
# 默认格式显示每个文件的详细信息
pygount --folders-to-skip=".git,node_modules,venv" 。

# 按代码行排序（通过管道排序）
pygount --folders-to-skip=".git,node_modules,venv" 。 |排序 -t$'\t' -k1 -nr |头-20
````

## 5. 输出格式

````bash
# 汇总表（默认推荐）
pygount --format=summary 。

# 用于编程使用的 JSON 输出
pygount --format=json 。

# 管道友好：语言、文件计数、代码、文档、空、字符串
pygount --format=summary 。 2>/dev/空
````

## 6. 解释结果

汇总表列：
- **语言** — 检测到的编程语言
- **文件** — 该语言的文件数量
- **代码** — 实际代码行（可执行/声明性）
- **注释** — 注释或文档行
- **%** — 占总数的百分比

特殊的伪语言：
- `__empty__` — 空文件
- `__binary__` — 二进制文件（图像、编译后的等）
- `__ generated__` — 自动生成的文件（启发式检测）
- `__duplicate__` — 具有相同内容的文件
- `__unknown__` — 无法识别的文件类型

## 陷阱

1. **始终排除 .git、node_modules、venv** — 如果没有 `--folders-to-skip`，pygount 将抓取所有内容，并且可能需要几分钟时间或挂在大型依赖树上。
2. **Markdown 显示 0 行代码** — pygount 将所有 Markdown 内容分类为注释，而不是代码。这是预期的行为。
3. **JSON 文件显示低代码计数** — pygount 可能会保守地计算 JSON 行数。要获得准确的 JSON 行数，请直接使用“wc -l”。
4. **大型单一存储库** - 对于非常大的存储库，请考虑使用“--suffix”来定位特定语言，而不是扫描所有内容。