---
title: "Apple Notes — Manage Apple Notes via memo CLI: create, search, edit"
sidebar_label: "Apple Notes"
description: "Manage Apple Notes via memo CLI: create, search, edit"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 苹果笔记

通过备忘录 CLI 管理 Apple Notes：创建、搜索、编辑。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/苹果/苹果笔记` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| macOS |
|标签 | `Notes`、`Apple`、`macOS`、`笔记` |
|相关技能| [`黑曜石`](/docs/user-guide/skills/bundled/note-take/note-take-obsidian) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 苹果笔记

使用“memo”直接从终端管理 Apple Notes。笔记通过 iCloud 在所有 Apple 设备上同步。

## 先决条件

- **macOS** 与 Notes.app
- 安装：`brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- 出现提示时授予自动化对 Notes.app 的访问权限（系统设置 → 隐私 → 自动化）

## 何时使用

- 用户要求创建、查看或搜索 Apple Notes
- 将信息保存到 Notes.app 以进行跨设备访问
- 将笔记整理到文件夹中
- 将笔记导出为 Markdown/HTML

## 何时不使用

- 黑曜石金库管理→使用“黑曜石”技能
- 熊笔记→单独的应用程序（此处不支持）
- 仅限代理的快速注释 → 使用“内存”工具代替

## 快速参考

### 查看笔记

````bash
备忘录笔记 # 列出所有笔记
memo Notes -f "文件夹名称" # 按文件夹过滤
memo Notes -s "query" # 搜索笔记（模糊）
````

### 创建笔记

````bash
memo Notes -a # 交互式编辑器
memo Notes -a "Note Title" # 快速添加标题
````

### 编辑注释

````bash
memo Notes -e # 交互式选择进行编辑
````

### 删除笔记

````bash
memo Notes -d # 交互式选择删除
````

### 移动笔记

````bash
memo Notes -m # 将笔记移动到文件夹（交互式）
````

### 导出注释

````bash
memo Notes -ex # 导出为 HTML/Markdown
````

## 限制

- 无法编辑包含图像或附件的笔记
- 交互式提示需要终端访问（如果需要，请使用 pty=true）
- 仅限 macOS — 需要 Apple Notes.app

## 规则

1. 当用户需要跨设备同步（iPhone/iPad/Mac）时，首选 Apple Notes
2. 使用“内存”工具处理不需要同步的座席内部笔记
3. 使用“黑曜石”技能进行 Markdown 原生知识管理