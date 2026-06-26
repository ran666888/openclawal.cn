---
title: "Obsidian — Read, search, create, and edit notes in the Obsidian vault"
sidebar_label: "Obsidian"
description: "Read, search, create, and edit notes in the Obsidian vault"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 黑曜石

在黑曜石保险库中阅读、搜索、创建和编辑笔记。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/记笔记/黑曜石` |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 黑曜石宝库

使用此技能进行文件系统优先的黑曜石保管库工作：阅读笔记、列出笔记、搜索笔记文件、创建笔记、附加内容和添加 wiki 链接。

## 保险库路径

在调用文件工具之前使用已知或已解析的保管库路径。

记录的保管库路径约定是“OBSIDIAN_VAULT_PATH”环境变量，例如来自“${HERMES_HOME:-~/.hermes}/.env”。如果未设置，请使用“~/Documents/Obsidian Vault”。

文件工具不会扩展 shell 变量。不要将包含“$OBSIDIAN_VAULT_PATH”的路径传递给“read_file”、“write_file”、“patch”或“search_files”；首先解析Vault路径并传递具体的绝对路径。 Vault 路径可能包含空格，这是更喜欢文件工具而不是 shell 命令的另一个原因。

如果保管库路径未知，则可以使用“terminal”来解析“OBSIDIAN_VAULT_PATH”或检查回退路径是否存在。知道路径后，切换回文件工具。

## 阅读注释

将“read_file”与已解析的笔记绝对路径一起使用。优于“cat”，因为它提供行号和分页。

## 列出笔记

将 `search_files` 与 `target: "files"` 和已解析的保管库路径结合使用。与“find”或“ls”相比，更喜欢这个。

- 要列出所有 Markdown 注释，请在库路径下使用“pattern: "*.md"”。
- 要列出子文件夹，请在该子文件夹的绝对路径下搜索。

## 搜索

使用“search_files”进行文件名和内容搜索。比 `grep`、`find` 或 `ls` 更喜欢这个。

- 对于文件名，请使用“search_files”和“target:“files””以及文件名“pattern”。
- 对于笔记内容，当您想要将匹配限制为 Markdown 笔记时，请使用带有 `target: "content"` 的 `search_files`、内容正则表达式为 `pattern` 和 `file_glob: "*.md"`。

## 创建笔记

将 `write_file` 与已解析的绝对路径和完整的 Markdown 内容一起使用。优于 shell heredocs 或 `echo`，因为它避免了 shell 引用问题并返回结构化结果。

## 附加到注释

当不尴尬时，更喜欢原生文件工具工作流程：

- 使用“read_file”读取目标注释。
- 当存在稳定的上下文时，使用“补丁”进行锚定附加，例如在现有标题之后添加一个部分或在已知的尾随块之前附加。
- 重写整个笔记时使用“write_file”比构建脆弱的补丁更清晰。

对于带有“patch”的锚定附加，请将锚点替换为锚点加上新内容。

对于没有稳定上下文的简单附加，如果“terminal”是最明确的安全选项，那么它是可以接受的。

## 有针对性的编辑

当当前内容为您提供稳定的上下文时，使用“补丁”进行重点注释更改。与 shell 文本重写相比，更喜欢这种方式。

## 维基链接

Obsidian 使用“[[注释名称]]”语法链接注释。创建笔记时，使用它们链接相关内容。