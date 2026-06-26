---
title: "Baoyu Article Illustrator — Article illustrations: type × style × palette consistency"
sidebar_label: "Baoyu Article Illustrator"
description: "Article illustrations: type × style × palette consistency"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#宝玉文章插画家

文章插图：类型×风格×调色板一致性。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/creative/baoyu-article-illustrator` 安装 |
|路径| `可选技能/创意/baoyu-文章-插画` |
|版本 | `1.57.0` |
|作者 | 宝玉 (JimLiu) |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “文章插图”、“创意”、“图像生成” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 文章插画

改编自 OpenClaw 工具生态的 [baoyu-article-illustrator](https://github.com/JimLiu/baoyu-skills)。

分析文章、确定插图位置、生成具有**类型 × 样式 × 调色板** 一致性的图像。

## 何时使用

当用户要求为文章添加插图、为文章添加图像、为内容生成插图或使用“为文章配图”、“为文章配图”或“添加图像”等短语时，触发此技能。用户提供文章（文件路径或粘贴的内容）并可选择指定类型、样式、调色板或密度。

## 三个维度

|尺寸|控制|示例 |
|------------|----------|----------|
| **类型** |信息结构|信息图、场景、流程图、比较、框架、时间线 |
| **风格** |渲染方式|概念、温暖、简约、蓝图、水彩、优雅|
| **调色板** |配色方案（可选）|马卡龙色、暖色、霓虹色 — 覆盖样式的默认颜色 |

自由组合：`type=infographic，style=vector-illustration，palette=macaron`。

或者使用预设：“edu-visual”→ 类型 + 样式 + 调色板。请参阅[style-presets.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/style-presets.md)。

## 类型

|类型 |最适合 |
|------|----------|
| `信息图` |数据、指标、技术 |
| `场景` |叙事，情感 |
| `流程图` |流程、工作流程 |
| `比较` |并排，选项|
| `框架` |模型、建筑 |
| `时间线` |历史、演变|

## 风格

请参阅 [references/styles.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/styles.md) 了解核心样式、完整图库以及类型 × 样式兼容性。

## 输出结构

<!-- ascii-guard-ignore -->
````
{输出目录}/
├── source-{slug}.{ext} # 仅适用于粘贴的内容
├── 大纲.md
├── 提示/
│ └── NN-{类型}-{slug}.md
└── NN-{类型}-{slug}.png
````
<!-- ascii-guard-ignore-end -->

**默认输出目录**：

|输入 |输出目录 | Markdown 插入路径 |
|--------|------------------|----------------------|
|文章文件路径 | `{article-dir}/imgs/` | `imgs/NN-{type}-{slug}.png` |
|粘贴内容 | `插图/{topic-slug}/` (cwd) | `插图/{topic-slug}/NN-{type}-{slug}.png` |

如果用户要求不同的布局（例如，文章旁边的图像，或“illustrations/”子目录），请遵守。

**Slug**：2-4 个单词，烤肉串大小写。 **冲突**：附加 `-YYYYMMDD-HHMMSS`。

## 核心原则

- **可视化概念，而不是隐喻** - 如果文章使用隐喻（例如“电锯切西瓜”），请说明基本概念，而不是文字图像。
- **标签使用文章数据** - 文章中的实际数字、术语和引用，而不是通用占位符。
- **提示文件是再现性记录** — 在生成任何图像之前，每个插图都必须在“prompts/”下有一个保存的提示文件。
- **剥离机密** — 在将任何内容写入磁盘之前扫描源内容以获取 API 密钥、令牌或凭据。

## 工作流程

````
- [ ] 步骤 1：检测参考图像（如果提供）
- [ ] 第 2 步：分析内容
- [ ] 步骤3：确认设置（澄清工具，一次一个问题）
- [ ] 第 4 步：生成轮廓
- [ ] 步骤 5：生成提示
- [ ] 第 6 步：生成图像 (image_generate)
- [ ] 第 7 步：完成
````

### 第 1 步：检测参考图像

如果用户提供参考图像（内联粘贴的路径、附件或 URL）：

1. 对于每个参考，使用路径/URL 和询问风格、调色板、构图和主题的问题调用“vision_analyze”。通过 write_file 将返回的描述记录在 {output-dir}/references/NN-ref-{slug}.md 中。
2. **不要**尝试通过 `write_file` / `read_file` 复制二进制文件 - 这些都是纯文本的。如果您想要记录的本地副本，请使用 `terminal` (`cp "$src" "{output-dir}/references/NN-ref-{slug}.{ext}"`)。该技能本身永远不需要读取二进制文件；它与愿景描述无关。
3. 由于“image_generate”不接受图像输入，因此视觉描述是在第 5 步中嵌入到提示中的内容。

完整程序：[references/workflow.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/workflow.md#step-1-detect-reference-images)。

### 第 2 步：分析

|分析|输出|
|----------|--------|
|内容类型 |技术/教程/方法/叙述|
|目的|信息/可视化/想象力|
|核心论点| 2-5要点 |
|职位 |插图在哪里增加价值 |

读取源代码（文件路径→“read_file”，或粘贴文本）并使用“write_file”将分析写入“{output-dir}/analysis.md”。

完整程序：[references/workflow.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/workflow.md#step-2-analyze)。

### 步骤 3：确认设置

使用“澄清”工具。由于“澄清”一次处理一个问题，因此首先提出最重要的问题。跳过答案已存在于用户请求中的任何问题。

|订单|问题 |选项|
|--------|----------|---------|
| Q1 | **预设或类型** | [推荐预设]、[替代预设]或手册：信息图、场景、流程图、比较、框架、时间线、混合 |
| Q2 | **密度** |最小 (1-2)、平衡 (3-5)、每节（推荐）、丰富 (6+) |
|第三季度 | **样式** *（如果在 Q1 中选择预设则跳过）* | 【推荐】、极简、科幻、手绘、社论、场景、海报 |
|第四季度 | **调色板** *（可选）* |默认（风格颜色），马卡龙色，暖色，霓虹色|
| Q5 | **语言** *（仅当文章语言不明确时）* |文章语言/用户语言|

不要连续问超过 2-3 个“澄清”问题。如果用户已经在请求中指定了这些，请完全跳过。

完整程序：[references/workflow.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/workflow.md#step-3-confirm-settings)。

### 步骤 4：生成大纲 → `outline.md`

使用带有 frontmatter（类型、密度、样式、调色板、image_count）的 write_file 保存“{output-dir}/outline.md”，每个插图一个条目：

````yaml
##插图1
**位置**：[节/段]
**目的**：[为什么]
**视觉内容**：[显示什么]
**文件名**：01-infographic-concept-name.png
````

完整模板：[references/workflow.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/workflow.md#step-4-generate-outline)。

### 第 5 步：生成提示

**阻止**：在生成任何图像之前，每个插图都必须有一个保存的提示文件 - 提示文件是再现性记录。

对于每个插图：

1. 根据[references/prompt-construction.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/prompt-construction.md)创建一个提示文件。
2. 使用“write_file”和 YAML frontmatter 保存到“{output-dir}/prompts/NN-{type}-{slug}.md”。
3. 提示必须使用具有结构化部分（区域/标签/颜色/样式/外观）的特定于类型的模板。
4. 标签必须包含文章特定的数据：实际数字、术语、指标、引用。
5. 每个提示 frontmatter 处理引用（`direct`/`style`/`palette`） - 对于 `direct` 使用，在提示中嵌入引用的文本描述（因为 `image_generate` 不接受引用图像输入）。

### 第 6 步：生成图像

对于每个提示文件：

1. 调用“image_generate(prompt=...,aspect_ratio=...)”。 `image_generate` 返回包含图像 URL 的 JSON 结果；它不写入磁盘也不接受输出路径。
2. 将提示的“ASPECT”映射到“image_generate”的枚举：“16:9”→“landscape”、“9:16”→“portrait”、“1:1”→“square”。自定义比率 → 最接近的命名纵横比。
3. 通过 `terminal` 将返回的 URL 下载到 `{output-dir}/NN-{type}-{slug}.png`（例如 `curl -sSL -o "{output-dir}/NN-{type}-{slug}.png" "{url}"`）。
4. 生成失败时，自动重试一次。

注意：底层图像生成后端是用户配置的（默认：FAL FLUX 2 Klein 9B），并且不能通过“image_generate”进行代理选择。不要将模型名称写入期望它们路由的提示中。

### 第 7 步：完成

在相应段落后插入 `![description](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/creative/baoyu-article-illustrator/{relative-path}/NN-{type}-{slug}.png)`。替代文本：用文章语言进行的简洁描述。

报告：

````
文章插图完成！
文章：[路径] |类型：[类型] |密度：[级别] |风格：[风格] |调色板：[调色板或默认]
图片：X/N 生成
````

## 修改

|行动|步骤|
|--------|--------|
|编辑|更新提示→重新生成→更新参考|
|添加|位置→提示→生成→更新大纲→插入|
|删除 |删除文件→删除参考→更新大纲|

## 参考文献

|文件|内容 |
|------|---------|
| [references/workflow.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/workflow.md) |详细流程|
| [references/usage.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/usage.md) |调用示例|
| [references/styles.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/styles.md) |风格画廊+调色板画廊|
| [references/style-presets.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/style-presets.md) |预设快捷键（类型+样式+调色板）|
| [references/prompt-construction.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/baoyu-article-illustrator/references/prompt-construction.md) |提示模板 |

## 陷阱

1. **数据完整性至关重要** — 切勿总结、解释或更改源统计数据。 “增长 73%”仍是“增长 73%”。
2. **剥离机密** — 在包含在任何输出文件中之前扫描源内容中的 API 密钥、令牌或凭据。
3. **不要从字面上解释隐喻**——可视化潜在的概念。
4. **提示文件是强制性的** — 如果没有保存提示文件，则无法生成图像。该文件可让您稍后重新生成或切换后端。
5. **`image_generate` 宽高比** — 该工具支持`landscape`、`portrait` 和`square`。自定义比率映射到最近的选项。
6. **`image_generate` 返回 URL，而不是本地文件** — 在将本地图像路径插入文章之前，始终通过 `terminal` (`curl`) 下载。
7. **代理没有后端选择** - `image_generate` 使用用户配置的任何模型（默认：FAL FLUX 2 Klein 9B）。不要将“使用 <model> 生成此”写入期望其路由的提示中。