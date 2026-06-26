---
title: "Sketch — Throwaway HTML mockups: 2-3 design variants to compare"
sidebar_label: "Sketch"
description: "Throwaway HTML mockups: 2-3 design variants to compare"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 草图

一次性 HTML 模型：要比较 2-3 个设计变体。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/素描` |
|版本 | `1.0.0` |
|作者 | OpenClaw（改编自 gsd-build/get-shit-done） |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `草图`、`模型`、`设计`、`ui`、`原型`、`html`、`变体`、`探索`、`线框`、`比较` |
|相关技能| [`spike`](/docs/user-guide/skills/bundled/software-development/software-development-spike)、[`claude-design`](/docs/user-guide/skills/bundled/creative/creative-claude-design)、[`popular-web-designs`](/docs/user-guide/skills/bundled/creative/creative-popular-web-designs), [`excalidraw`](/docs/user-guide/skills/bundled/creative/creative-excalidraw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 草图

当用户想要**在提交**之前查看设计方向时，请使用此技能 - 将 UI/UX 想法探索为一次性 HTML 模型。重点是生成 2-3 个交互式变体，以便用户可以并排比较视觉方向，而不是生成可交付的代码。

当用户说“画出这个屏幕的草图”、“告诉我 X 可能是什么样子”、“比较布局 A 和 B”、“给我 2-3 个 UI 版本”、“让我看看一些变体”、“在构建之前模拟一下”之类的内容时，加载此内容。

## 什么时候不应该使用这个

- 用户想要一个生产组件 - 使用“claude-design”或正确构建它
- 用户想要一个精美的一次性 HTML 工件（登陆页面、平台）——“claude-design”
- 用户想要一个图表 - `excalidraw`、`architecture-diagram`
- 设计已经锁定——只需构建它

## 如果用户安装了完整的GSD系统

如果 `gsd-sketch` 显示为同级技能（通过 `npx get-shit-done-cc --hermes` 安装），则更喜欢 **`gsd-sketch`** 来实现完整的工作流程：带有 MANIFEST 的持久性 `.planning/sketches/`、前沿模式分析、过去草图的一致性审核以及与 GSD 其余部分的集成。这项技能是轻量级独立版本——无需状态机的一次性草图。

## 核心方法

````
摄入 → 变体 → 面对面 → 选择获胜者（或迭代）
````

### 1.摄入量（如果用户已经给了你足够的量，则跳过）

在生成变体之前，请先了解三件事 - 一次提出一个问题，而不是一次提出所有问题：

1. **感觉。** “这应该是什么样的感觉？形容词、情感、氛围。” — *“冷静，社论，像线性”* 告诉您的不仅仅是“最小”*。
2. **参考资料** “哪些应用程序、网站或产品捕捉到了您所想象的感觉？” ——实际参考胜过抽象描述。
3. **核心操作。** “用户在此屏幕上执行的最重要的事情是什么？” ——所有的变体都应该能很好地服务于此；如果不这样做，它们就只是装饰品。

在下一个问题之前简要思考每个答案。如果用户已经预先给了您所有三个，请直接跳到变体。

### 2. 变体（2-3，从不 1，很少 4+）

一次性生产 **2-3 个变体**。每个变体都是一个完整的、独立的 HTML 文件。不要描述变体——构建它们。重点是比较。

每个变体应该采取**不同的设计立场**，而不是不同的像素值。三个好的变体轴：

- **密度：** 紧凑/通风/超密集（选择两个对比极点）
- **强调：**内容优先/行动优先/工具优先
- **审美：** 社论/实用/俏皮
- **布局：** 单栏/侧边栏/分割窗格
- **接地：** 基于卡片/裸内容/文档风格

选择一根轴并将其拉开。仅强调颜色不同的两个变体是浪费精力——用户无法区分它们。

**变体命名：**描述立场，而不是数字。

<!-- ascii-guard-ignore -->
````
草图/
├── 001-平静-社论/
│ ├──index.html
│ └── README文件.md
├── 001-功利-密集/
│ ├──index.html
│ └── README文件.md
└── 001-俏皮-分裂/
    ├── 索引.html
    └── README文件.md
````
<!-- ascii-guard-ignore-end -->

### 3. 使它们成为真正的 HTML

每个变体都是一个**单个独立的 HTML 文件**：

- 内联 `<style>` — 无需构建步骤，无需外部 CSS
- 系统字体或通过“<link>”使用一种 Google 字体
- 通过 CDN 的 Tailwind (`<script src="https://cdn.tailwindcss.com"></script>`) 没问题
- 真实的虚假内容——真实的句子、真实的名字，而不是“Lorem ipsum”
- **交互式**：链接可点击、真实悬停、至少一种状态转换（打开/关闭、过滤、切换）。冻结的静态图像比马虎的动画图像更糟糕。

在浏览器中打开它。如果它看起来损坏了，请在向用户展示之前修复它。

**直观地验证变体 - 使用 OpenClaw 的浏览器工具。** 不要只编写 HTML 并希望它能够呈现；加载每个变体并查看它：

````
browser_navigate(url="文件:///absolute/path/to/sketches/001-calm-editorial/index.html")
browser_vision(question="此布局看起来干净且可读吗？有任何可见的错误（重叠的文本、无样式的元素、损坏的图像）吗？")
````

“browser_vision”返回页面上实际内容的 AI 描述以及屏幕截图路径 - 捕获纯源检查遗漏的布局错误（例如，默默失败的字体导入、崩溃的 Flex 容器）。修复并重新导航，直到每个变体看起来都正确。

**默认 CSS 重置 + 系统字体堆栈**用于快速启动：

````html
<风格>
  * { 框大小：边框框；保证金：0；填充：0； }
  身体{
    字体系列：-apple-system、BlinkMacSystemFont、“Segoe UI”、Roboto、
                 “Helvetica Neue”，Arial，无衬线体；
    -webkit-font-smoothing：抗锯齿；
    颜色：#1a1a1a；
    背景：#fafafa；
    行高：1.5；
  }
</风格>
````

### 4. 变体README文件

每个变体的“README.md”答案：

``降价
## 变体：{立场名称}

### 设计立场
一句话讲述了这一变体的驱动原理。

### 关键选择
- 布局：...
- 版式：...
- 颜色：...
- 互动：...

### 权衡
- 擅长：...
- 弱点：...

### 最适合
- 该变体实际服务的用户或用例类型
````

### 5. 正面交锋

构建完所有变体后，将它们作为比较进行展示。不要只是列出——**发表意见**：

``降价
## 主屏幕上的三个镜头

|尺寸|冷静社论|功利密集|俏皮的分裂|
|------------|----------------|--------------------|------------------------|
|密度|低|高|中等|
|主要行动可见性|低|高|中等|
|扫描能力|高|中等|低|
|感觉|冷静，值得信赖|锋利、工具般|魅力四射、充满活力|

**我的看法：** 对于高级用户来说功利主义密集，对于内容转发的观众来说冷静的社论。有趣的分裂是最弱的——试图两者兼而有之，但两者都不做。
````

让用户选择一个获胜者，或者将两个组合成一个混合体，或者要求进行另一轮。

## 主题化（当项目有视觉识别时）

如果用户有现有主题（颜色、字体、标记），请将共享标记放入“sketches/themes/tokens.css”中，并在每个变体中“@import”它们。保持令牌最少：

````CSS
/* sketches/themes/tokens.css */
：根{
  --颜色背景：#fafafa；
  --颜色-fg：#1a1a1a；
  --颜色重音：#0066ff；
  --颜色静音：#666；
  --半径：8px；
  --font-display: "Inter"，无衬线字体；
  --font-body: -apple-system, BlinkMacSystemFont, sans-serif;
}
````

不要过度标记一次性草图——三种颜色和一种字体通常就足够了。

## 互动栏

当用户能够满足以下条件时，草图就具有足够的交互性：

1. **单击主要操作**，会发生一些可见的事情（状态更改、模式、吐司、导航佯攻）
2. **查看一个有意义的状态转换**（过滤列表、切换模式、打开/关闭面板）
3. **悬停可识别的可供性**（按钮、行、选项卡）

更重要的是过度设计一次性产品。不到这个就是屏幕截图。

## 前沿模式（选择下一步要画什么）

如果草图已经存在并且用户说“接下来我应该画什么？”：

- **一致性差距** - 来自不同草图的两个获胜变体做出了尚未组合在一起的独立选择
- **未绘制的屏幕** - 参考过但从未探索过
- **状态覆盖率** — 绘制了快乐的路径，但不为空/正在加载/错误/1000个项目
- **响应间隙** — 在一个视口进行验证；它适用于移动/超广角吗？
- **交互模式** — 存在静态布局；过渡、拖动、滚动行为不会

推荐 2-4 名指定候选人。让用户选择。

## 输出

- 在存储库根目录中创建“sketches/”（如果用户使用 GSD 约定，则创建“.planning/sketches/”）
- 每个变体一个子目录：`NNN-stance-name/index.html` + `README.md`
- 告诉用户如何打开它们：macOS 上的“open sketches/001-calm-editorial/index.html”、Linux 上的“xdg-open”、Windows 上的“start”
- 保持变体一次性 - 您认为需要保留的草图应提升为真实的项目代码，而不是作为资产进行管理

**一种变体的典型工具序列：**

````
终端（“mkdir -p sketches/001-calm-editorial”）
write_file("草图/001-calm-editorial/index.html", "<!doctype html>...")
write_file("sketches/001-calm-editorial/README.md", "## 变体：冷静编辑\n...")
browser_navigate(url="file://$(pwd)/sketches/001-calm-editorial/index.html")
browser_vision(question="这看起来怎么样？有明显的布局问题吗？")
````

对每个变体重复此操作，然后呈现比较表。

## 归因

改编自 GSD (Get Shit Done) 项目的 `/gsd-sketch` 工作流程 — MIT © 2025 Lex Christopherson ([gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done))。完整的 GSD 系统提供持久草图状态、主题/变体模式参考和一致性审核工作流程；使用“npx get-shit-done-cc --hermes --global”安装。