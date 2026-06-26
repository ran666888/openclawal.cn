---
title: "Architecture Diagram — Dark-themed SVG architecture/cloud/infra diagrams as HTML"
sidebar_label: "Architecture Diagram"
description: "Dark-themed SVG architecture/cloud/infra diagrams as HTML"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 架构图

HTML 格式的深色主题 SVG 架构/云/基础设施图。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/架构图` |
|版本 | `1.0.0` |
|作者 | Cocoon AI (hello@cocoon-ai.com)，由 OpenClaw 移植 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `架构`、`图表`、`SVG`、`HTML`、`可视化`、`基础设施`、`云` |
|相关技能| [`概念图`](/docs/user-guide/skills/可选/creative/creative-concept-diagrams)，[`excalidraw`](/docs/user-guide/skills/bundled/creative/creative-excalidraw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 架构图技巧

生成专业的、黑暗主题的技术架构图作为带有内联 SVG 图形的独立 HTML 文件。没有外部工具，没有 API 密钥，没有渲染库 - 只需编写 HTML 文件并在浏览器中打开它。

## 范围

**最适合：**
- 软件系统架构（前端/后端/数据库层）
- 云基础设施（VPC、区域、子网、托管服务）
- 微服务/服务网格拓扑
- 数据库+API图、部署图
- 任何具有科技基础主题且符合黑暗、网格背景美感的内容

**首先在别处寻找：**
- 物理、化学、数学、生物或其他科学科目
- 物理对象（车辆、硬件、解剖结构、横截面）
- 平面图、叙事旅程、教育/教科书式视觉效果
- 手绘白板草图（考虑“excalidraw”）
- 动画讲解员（考虑动画技能）

如果该主题有更专业的技能，则更愿意这样做。如果没有合适的，这个技能也可以作为一般的 SVG 图后备——输出将只带有下面描述的黑暗科技美学。

基于[Cocoon AI 的架构图生成器](https://github.com/Cocoon-AI/architecture-diagram-generator) (MIT)。

## 工作流程

1. 用户描述他们的系统架构（组件、连接、技术）
2. 按照下面的设计系统生成HTML文件
3. 使用“write_file”保存到“.html”文件（例如“~/architecture-diagram.html”）
4. 用户在任何浏览器中打开——离线工作，无依赖性

### 输出位置

将图表保存到用户指定的路径，或默认保存到当前工作目录：
````
./[项目名称]-architecture.html
````

### 预览

保存后，建议用户打开：
````bash
# macOS
打开./my-architecture.html
# Linux
xdg-open ./my-architecture.html
````

## 设计系统和视觉语言

### 调色板（语义映射）

使用特定的“rgba”填充和十六进制笔画对组件进行分类：

|组件类型 |填充 (rgba) |行程（十六进制）|
| :--- | :--- | :--- |
| **前端** | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (青色-400) |
| **后端** | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald-400) |
| **数据库** | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet-400) |
| **AWS/云** | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber-400) |
| **安全** | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose-400) |
| **消息总线** | `rgba(251, 146, 60, 0.3)` | `#fb923c` (橙色-400) |
| **外部** | `rgba(30, 41, 59, 0.5)` | `#94a3b8` (slate-400) |

### 版式和背景
- **字体：** JetBrains Mono (Monospace)，从 Google Fonts 加载
- **尺寸：** 12px（名称）、9px（子标签）、8px（注释）、7px（小标签）
- **背景：** Slate-950 (`#020617`) 带有微妙的 40px 网格图案

````svg
<!-- 背景网格图案 -->
<模式id =“网格”宽度=“40”高度=“40”patternUnits =“userSpaceOnUse”>
  <路径d =“M 40 0 L 0 0 0 40”填充=“无”笔画=“#1e293b”笔画宽度=“0.5”/>
</模式>
````

## 技术实施细节

### 组件渲染
组件是带有 1.5px 笔画的圆角矩形 (`rx="6"`)。为了防止箭头通过半透明填充显示，请使用**双矩形遮罩技术**：
1. 绘制一个不透明的背景矩形（`#0f172a`）
2. 在顶部绘制半透明样式的矩形

### 连接规则
- **Z-Order：**在 SVG 中*早*绘制箭头（在网格之后），以便它们在组件框后面渲染
- **箭头：** 通过 SVG 标记定义
- **安全流程：** 使用玫瑰色虚线（`#fb7185`）
- **边界：**
  - *安全组：* 虚线 (`4,4`)，玫瑰色
  - *区域：* 大虚线 (`8,4`)，琥珀色，`rx="12"`

### 间距和布局逻辑
- **标准高度：** 60px（服务）； 80-120px（大型组件）
- **垂直间隙：** 组件之间最小 40px
- **消息总线：**必须放置在服务之间的*间隙*中，而不是与它们重叠
- **图例放置：** **关键。** 必须放置在所有边界框之外。计算所有边界的最低 Y 坐标，并将图例放置在其下方至少 20 像素处。

## 文档结构

生成的 HTML 文件遵循四部分布局：
1. **标题：** 带有脉冲点指示器和副标题的标题
2. **主要 SVG：** 圆形边框卡中包含的图表
3. **摘要卡：** 图表下方由三张卡组成的网格，用于提供高级详细信息
4. **页脚：** 最小元数据

### 信息卡图案
````html
<div类=“卡”>
  <div class="card-header">
    <div class="card-dot 青色"></div>
    <h3>标题</h3>
  </div>
  <ul>
    <li>• 第一项</li>
    <li>• 第二项</li>
  </ul>
</div>
````

## 输出要求
- **单个文件：** 一个独立的 `.html` 文件
- **无外部依赖项：** 所有 CSS 和 SVG 必须内联（Google Fonts 除外）
- **无 JavaScript：** 对任何动画（如脉冲点）使用纯 CSS
- **兼容性：** 必须在任何现代网络浏览器中正确呈现

## 模板参考

加载完整的 HTML 模板以获取确切的结构、CSS 和 SVG 组件示例：

````
Skill_view(name="架构图", file_path="templates/template.html")
````

该模板包含每个组件类型（前端、后端、数据库、云、安全）、箭头样式（标准、虚线、曲线）、安全组、区域边界和图例的工作示例 - 生成图表时将其用作结构参考。