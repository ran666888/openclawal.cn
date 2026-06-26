---
title: "Nano Pdf — Edit PDF text/typos/titles via nano-pdf CLI (NL prompts)"
sidebar_label: "Nano Pdf"
description: "Edit PDF text/typos/titles via nano-pdf CLI (NL prompts)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 纳米 PDF

通过 nano-pdf CLI（NL 提示）编辑 PDF 文本/拼写错误/标题。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/生产力/nano-pdf` |
|版本 | `1.0.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `PDF`、`文档`、`编辑`、`NLP`、`生产力` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 纳米pdf

使用自然语言指令编辑 PDF。将其指向一个页面并描述要更改的内容。

## 先决条件

````bash
# 使用 uv 安装（推荐 — Hermes 中已提供）
uv pip 安装 nano-pdf

# 或者用点
pip 安装 nano-pdf
````

## 用法

````bash
nano-pdf 编辑 <文件.pdf> <页码> "<指令>"
````

## 示例

````bash
# 更改第 1 页的标题
nano-pdf edit Deck.pdf 1“将标题更改为‘Q3 Results’并修复副标题中的拼写错误”

# 更新特定页面上的日期
nano-pdf编辑报告.pdf 3“更新日期从2026年1月到2月”

# 修复内容
nano-pdf edit Contract.pdf 2“将客户名称从‘Acme Corp’更改为‘Acme Industries’”
````

## 注释

- 页码可能是从 0 开始或从 1 开始，具体取决于版本 - 如果编辑到达错误的页面，请使用 ±1 重试
- 编辑后始终验证输出 PDF（使用“read_file”检查文件大小，或打开它）
- 该工具在后台使用法学硕士 - 需要 API 密钥（检查“nano-pdf --help”配置）
- 适用于文本更改；复杂的布局修改可能需要不同的方法