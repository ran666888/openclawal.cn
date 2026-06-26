---
title: "Manim Video — Manim CE animations: 3Blue1Brown math/algo videos"
sidebar_label: "Manim Video"
description: "Manim CE animations: 3Blue1Brown math/algo videos"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#马尼姆视频

Manim CE 动画：3Blue1Brown 数学/算法视频。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/manim-视频` |
|版本 | `1.0.0` |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Manim 视频制作流程

## 何时使用

当用户请求时使用：动画解释、数学动画、概念可视化、算法演练、技术解释、3Blue1Brown 风格视频或任何具有几何/数学内容的程序化动画。使用 Manim 社区版创建 3Blue1Brown 风格的讲解视频、算法可视化、方程推导、架构图和数据故事。

## 创意标准

这是教育电影。每一帧都在教导。每个动画都揭示了结构。

**在编写一行代码之前**，阐明叙述弧线。这纠正了什么误解？什么是“顿悟时刻”？什么样的视觉故事能让观众从困惑走向理解？用户的提示是一个起点——用教学的野心来解释它。

**几何先于代数。**先显示形状，然后显示方程。视觉记忆的编码速度比符号记忆快。当观看者在公式之前看到几何图案时，就会觉得这个方程是值得的。

**首次渲染的卓越性是不容谈判的。**输出必须视觉上清晰且美观一致，无需进行多次修改。如果某些内容看起来杂乱、不合时宜，或者像“人工智能生成的幻灯片”，那么它就是错误的。

**不透明分层会引导注意力。**切勿以全亮度显示所有内容。主要元素为 1.0，上下文元素为 0.4，结构元素（轴、网格）为 0.15。大脑分层处理视觉显着性。

**喘息空间。** 每个动画之后都需要`self.wait()`。观众需要时间来吸收刚刚出现的内容。切勿急于从一个动画过渡到下一个动画。按键显示后 2 秒的暂停绝不会浪费。

**有凝聚力的视觉语言。** 所有场景共享一个调色板、一致的版式尺寸、匹配的动画速度。每个场景都使用随机不同颜色的技术上正确的视频是审美上的失败。

## 先决条件

运行“scripts/setup.sh”以验证所有依赖项。需要：Python 3.10+、Manim Community Edition v0.20+（`pip install manim`）、LaTeX（Linux 上为 `texlive-full`、macOS 上为 `mactex`）和 ffmpeg。参考文档针对 Manim CE v0.20.1 进行了测试。

## 模式

|模式|输入 |输出|参考|
|------|--------|--------|------------|
| **概念解释** |主题/概念 |几何直觉的动画解释 | `references/scene-planning.md` |
| **方程推导** |数学表达式 |分步动画证明 | `references/equations.md` |
| **算法可视化** |算法说明 |使用数据结构逐步执行 | `references/graphs-and-data.md` |
| **数据故事** |数据/指标|动画图表、比较、计数器 | `references/graphs-and-data.md` |
| **架构图** |系统说明|通过连接构建组件 | `references/mobjects.md` |
| **论文解释** |研究论文|主要发现和方法动画 | `references/scene-planning.md` |
| **3D 可视化** | 3D概念|旋转曲面、参数曲线、空间几何 | `references/camera-and-3d.md` |

## 堆栈

每个项目单个 Python 脚本。无需浏览器，无需 Node.js，无需 GPU。

|层|工具|目的|
|--------|------|---------|
|核心|马尼姆社区版 |场景渲染、动画引擎|
|数学 |乳胶 (texlive/MiKTeX) |通过 `MathTex` 进行方程渲染 |
|视频输入/输出 | ffmpeg|场景拼接、格式转换、音频混合 |
|语音合成 | ElevenLabs / Qwen3-TTS（可选）|旁白画外音 |

## 管道

````
计划-->代码-->渲染-->缝合-->音频（可选）-->审查
````

1. **PLAN** — 编写带有叙述弧、场景列表、视觉元素、调色板、画外音脚本的“plan.md”
2. **代码** — 为每个场景编写一个类，每个类可独立渲染“script.py”
3. **RENDER** — `manim -ql script.py Scene1 Scene2 ...` 用于草稿，`-qh` 用于生产
4. **STITCH** — ffmpeg 将场景剪辑连接到 `final.mp4`
5. **音频**（可选）- 通过 ffmpeg 添加画外音和/或背景音乐。请参阅“references/rendering.md”
6. **审查** — 渲染预览静态图，对照计划进行验证，调整

## 项目结构

````
项目名称/
  plan.md # 叙事弧线、场景分解
  script.py # 所有场景都在一个文件中
  concat.txt # ffmpeg场景列表
  Final.mp4 # 拼接输出
  media/ # 由 Manim 自动生成
    视频/脚本/480p15/
````

## 创意方向

### 调色板

|调色板|背景|小学|中学|口音|使用案例|
|--------|---------|---------|------------|--------|---------|
| **经典3B1B** | `#1C1C1C` | `#58C4DD`（蓝色）| `#83C167`（绿色）| `#FFFF00`（黄色）|普通数学/计算机科学 |
| **热情学术** | `#2D2B55` | `#FF6B6B` | `#FFD93D` | `#6BCB77` |平易近人 |
| **霓虹科技** | `#0A0A0A` | `#00F5FF` | `#FF00FF` | `#39FF14` |系统、架构|
| **单色** | `#1A1A2E` | `#EAEAEA` | `#888888` | `#FFFFFF` |极简主义 |

### 动画速度

|背景 |运行时 | | 之后 self.wait()
|--------|----------|--------------------|
|标题/简介出现 | 1.5秒| 1.0 秒 |
|关键方程揭示 | 2.0 秒 | 2.0 秒 |
|变换/变形 | 1.5秒| 1.5秒|
|配套标签| 0.8秒| 0.5秒|
|淡出清理 | 0.5秒| 0.3秒|
| “啊哈时刻”揭晓 | 2.5秒| 3.0 秒 |

### 版式比例

|角色 |字体大小 |用途 |
|------|---------|--------|
|标题 | 48 | 48场景标题、开场文字 |
|标题 | 36 | 36场景中的节标题 |
|身体| 30|说明文字|
|标签| 24 |注释、轴标签 |
|标题| 20 |字幕，精美印刷 |

### 字体

**对所有文本使用等宽字体。** Manim 的 Pango 渲染器会在所有尺寸的比例字体中产生不规则的字距调整。请参阅“references/visual-design.md”以获取完整的建议。

````蟒蛇
MONO = "Menlo" # 在文件顶部定义一次

Text("傅立叶级数", font_size=48, font=MONO, Weight=BOLD) # 标题
Text("n=1: sin(x)", font_size=20, font=MONO) # 标签
MathTex(r"\nabla L") # 数学（使用 LaTeX）
````

为了可读性，最小“font_size=18”。

### 每个场景的变化

切勿对所有场景使用相同的配置。对于每个场景：
- **调色板中不同的主色**
- **不同的布局** - 不要总是将所有内容居中
- **不同的动画条目** — 在 Write、FadeIn、GrowFromCenter、Create 之间有所不同
- **不同的视觉权重** - 有些场景密集，有些场景稀疏

## 工作流程

### 第 1 步：计划 (plan.md)

在任何代码之前，编写“plan.md”。有关综合模板，请参阅“references/scene-planning.md”。

### 步骤 2：代码 (script.py)

每个场景一个类。每个场景都是可独立渲染的。

````蟒蛇
从马尼姆进口 *

BG =“#1C1C1C”
主=“#58C4DD”
次要=“#83C167”
重音=“#FFFF00”
MONO =“门洛”

类Scene1_Introduction（场景）：
    def 构造（自身）：
        self.camera.background_color = BG
        title = Text("为什么这样做？"，font_size=48，color=PRIMARY，weight=BOLD，font=MONO)
        self.add_subcaption(“为什么这有效？”，持续时间= 2)
        self.play(写(标题), run_time=1.5)
        自我等待(1.0)
        self.play(FadeOut(标题), run_time=0.5)
````

关键模式：
- 每个动画上的 **字幕**： `self.play()` 上的 `self.add_subcaption("text",uration=N)` 或 `subcaption="text"`
- **共享颜色常量**位于文件顶部，以实现跨场景一致性
- **`self.camera.background_color`** 在每个场景中设置
- **干净退出** — 在场景结束时淡出所有 mobject：`self.play(FadeOut(Group(*self.mobjects)))`

### 第 3 步：渲染

````bash
manim -ql script.py Scene1_Introduction Scene2_CoreConcept # 草稿
manim -qh script.py Scene1_Introduction Scene2_CoreConcept # 制作
````

### 第 4 步：缝合

````bash
猫 > concat.txt << 'EOF'
文件“媒体/视频/脚本/480p15/Scene1_Introduction.mp4”
文件“媒体/视频/脚本/480p15/Scene2_CoreConcept.mp4”
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c 复制 Final.mp4
````

### 第 5 步：回顾

````bash
manim -ql --format=png -s script.py Scene2_CoreConcept # 预览仍然
````

## 关键实施说明

### LaTeX 的原始字符串
````蟒蛇
# 错误：MathTex("\frac{1}{2}")
# 右：
MathTex(r"\frac{1}{2}")
````

### 边缘文本 buff >= 0.5
````蟒蛇
label.to_edge(DOWN, buff=0.5) # 永远不会 < 0.5
````

### 替换文本之前淡出
````蟒蛇
self.play(ReplacementTransform(note1, note2)) # 不在顶部写入(note2)
````

### 切勿对未添加的 Mobject 进行动画处理
````蟒蛇
self.play(Create(circle)) # 必须先添加
self.play(circle.animate.set_color(RED)) # 然后动画
````

## 绩效目标

|品质 |分辨率|第一人称射击 |速度|
|--------|------------|-----|--------|
| `-ql`（草案）| 854x480 | 854x480 15 | 15 5-15 秒/场景 |
| `-qm`（中）| 1280x720 | 1280x720 30| 15-60 秒/场景 |
| `-qh`（生产）| 1920x1080 | 60| 30-120 秒/场景 |

始终在“-ql”处迭代。仅渲染“-qh”作为最终输出。

## 参考文献

|文件|内容 |
|------|----------|
| `references/animations.md` |核心动画、速率函数、合成、“.animate”语法、计时模式 |
| `references/mobjects.md` |文本、形状、VGroup/Group、定位、样式、自定义对象 |
| `参考文献/视觉设计.md` | 12 条设计原则、不透明分层、布局模板、调色板 |
| `references/equations.md` | Manim 中的 LaTeX、TransformMatchingTex、推导模式 |
| `references/graphs-and-data.md` |坐标轴、绘图、条形图、动画数据、算法可视化 |
| `references/camera-and-3d.md` | MovingCameraScene、ThreeDScene、3D 表面、相机控制 |
| `references/scene-planning.md` |叙事弧线、布局模板、场景转换、规划模板 |
| `references/rendering.md` | CLI 参考、质量预设、ffmpeg、配音工作流程、GIF 导出 |
| `参考文献/故障排除.md` | LaTeX 错误、动画错误、常见错误、调试 |
| `references/animation-design-thinking.md` |何时制作动画与展示静态、分解、节奏、旁白同步 |
| `references/updaters-and-trackers.md` | ValueTracker、add_updater、always_redraw、基于时间的更新器、模式 |
| `references/paper-explainer.md` |将研究论文转化为动画——工作流程、模板、领域模式 |
| `references/decorations.md` | SurroundingRectangle、Brace、箭头、DashedLine、Angle、注释生命周期 |
| `参考文献/生产质量.md` |预编码、预渲染、渲染后清单、空间布局、颜色、节奏 |

---

## 创意分歧（仅当用户请求实验/创意/独特输出时使用）

如果用户要求创造性的、实验性的或非常规的解释方法，请在设计动画之前通过它选择策略和理由。

- **SCAMPER** — 当用户想要对标准解释有新的看法时
- **假设逆转** - 当用户想要挑战通常如何教授某些内容时

### SCAMPER 转型
采用标准的数学/技术可视化并对其进行转换：
- **替代**：替代标准视觉隐喻（数轴→蜿蜒路径，矩阵→城市网格）
- **组合**：合并两种解释方法（同时代数+几何）
- **反向**：向后推导 — 从结果开始并解构为公理
- **修改**：夸大参数以显示其重要性（10 倍学习率，1000 倍样本量）
- **消除**：删除所有符号 - 纯粹通过动画和空间关系进行解释

### 假设逆转
1. 列出该主题的可视化方式的“标准”（从左到右、二维、离散步骤、形式符号）
2. 选择最基本的假设
3.反转它（从右到左推导、2D概念的3D嵌入、连续变形而不是步骤、零符号）
4. 探索逆转揭示了标准方法隐藏的内容