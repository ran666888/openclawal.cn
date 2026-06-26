---
title: "Youtube Content — YouTube transcripts to summaries, threads, blogs"
sidebar_label: "Youtube Content"
description: "YouTube transcripts to summaries, threads, blogs"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# YouTube 内容处理

YouTube 转录为摘要、主题、博客。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/媒体/youtube-内容` |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# YouTube 内容工具

## 何时使用

当用户共享 YouTube URL 或视频链接、要求总结视频、请求文字记录或想要从任何 YouTube 视频中提取内容并重新格式化内容时使用。将文字记录转换为结构化内容（章节、摘要、主题、博客文章）。

从 YouTube 视频中提取文字记录并将其转换为有用的格式。

## 设置

使用“uv”，将依赖项安装到同一个 OpenClaw 管理的环境中
运行帮助程序脚本：

````bash
uv pip 安装 youtube-transcript-api
````

## 帮助脚本

`SKILL_DIR` 是包含此 SKILL.md 文件的目录。该脚本接受任何标准 YouTube URL 格式、短链接 (youtu.be)、短片、嵌入内容、实时链接或原始 11 个字符的视频 ID。

````bash
# 带有元数据的 JSON 输出
uv 运行 python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# 纯文本（有利于进一步处理）
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --仅文本

# 带时间戳
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# 具有后备链的特定语言
uv run python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
````

## 输出格式

获取成绩单后，根据用户要求对其进行格式化：

- **章节**：按主题转移分组，输出带时间戳的章节列表
- **摘要**：整个视频的简洁 5-10 句话概述
- **章节摘要**：每个章节都有一个简短的段落摘要
- **主题**：Twitter/X 主题格式 — 编号帖子，每个帖子少于 280 个字符
- **博客文章**：包含标题、章节和要点的完整文章
- **报价**：带有时间戳的著名报价

### 示例 — 章节输出

````
00:00 简介——主持人以问题陈述开始
03:45 背景——之前的工作以及现有解决方案不足的原因
12:20 核心方法——所提出方法的演练
24:10 结果——基准比较和关键要点
31:55 问答——观众关于可扩展性和后续步骤的问题
````

## 工作流程

1. 通过 `uv run python3` 使用带有 `--text-only --timestamps` 的帮助程序脚本 **获取** 记录。
2. **验证**：确认输出非空且采用预期语言。如果为空，请在不使用“--language”的情况下重试以获取任何可用的成绩单。如果仍然为空，请告诉用户视频可能已禁用转录。
3. **如果需要则分块**：如果转录本超过约 50K 个字符，则将其拆分为重叠的块（约 40K，其中 2K 重叠），并在合并之前汇总每个块。
4. **转换**为请求的输出格式。如果用户未指定格式，则默认为摘要。
5. **验证**：在呈现之前重新读取转换后的输出以检查一致性、正确的时间戳和完整性。

## 错误处理

- **转录已禁用**：告诉用户；建议他们检查视频页面上是否有字幕。
- **私人/不可用视频**：转发错误并要求用户验证 URL。
- **没有匹配的语言**：在不使用“--language”的情况下重试以获取任何可用的文字记录，然后向用户注明实际语言。
- **依赖项丢失**：运行 `uv pip install youtube-transcript-api` 并重试。