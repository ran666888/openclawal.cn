---
title: "Excalidraw — Hand-drawn Excalidraw JSON diagrams (arch, flow, seq)"
sidebar_label: "Excalidraw"
description: "Hand-drawn Excalidraw JSON diagrams (arch, flow, seq)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Excalidraw

手绘 Excalidraw JSON 图表（arch、flow、seq）。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/excalidraw` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `Excalidraw`、`图表`、`流程图`、`架构`、`可视化`、`JSON` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Excalidraw 图表技巧

通过编写标准 Excalidraw 元素 JSON 并保存为“.excalidraw”文件来创建图表。这些文件可以拖放到 [excalidraw.com](https://excalidraw.com) 上进行查看和编辑。没有帐户、没有 API 密钥、没有渲染库——只有 JSON。

## 何时使用

为架构图、流程图、序列图、概念图等生成“.excalidraw”文件。文件可以在 excalidraw.com 打开或上传以获取共享链接。

## 工作流程

1. **加载此技能**（你已经这样做了）
2. **编写元素 JSON** -- Excalidraw 元素对象数组
3. **保存文件** 使用 `write_file` 创建一个 `.excalidraw` 文件
4. **可选地通过`terminal`使用`scripts/upload.py`上传**可共享链接

### 保存图表

将元素数组包装在标准的“.excalidraw”信封中，并使用“write_file”保存：

```json
{
  “类型”：“excalidraw”，
  “版本”：2，
  “来源”：“爱马仕代理”，
  "elements": [ ...这里是您的元素数组... ],
  “应用程序状态”：{
    “viewBackgroundColor”：“#ffffff”
  }
}
````

保存到任意路径，例如`~/diagrams/my_diagram.excalidraw`。

### 上传共享链接

通过终端运行上传脚本（位于该技能的“scripts/”目录中）：

````bash
python 技能/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw
````

这将上传到 excalidraw.com（无需帐户）并打印可共享的 URL。需要 `cryptography` pip 包（`pip install cryptography`）。

---

## 元素格式参考

### 必填字段（所有元素）
`type`、`id`（唯一字符串）、`x`、`y`、`width`、`height`

### 默认值（跳过这些——它们会自动应用）
- `笔划颜色`: `"#1e1e1e"`
- `backgroundColor`: `"透明"`
- `fillStyle`: `"实心"`
- `笔画宽度`: `2`
- `粗糙度`：`1`（手绘外观）
- `不透明度`: `100`

画布背景是白色的。

### 元素类型

**矩形**：
```json
{ “类型”：“矩形”，“id”：“r1”，“x”：100，“y”：100，“宽度”：200，“高度”：100 }
````
- `roundness: { "type": 3 }` 用于圆角
- `backgroundColor: "#a5d8ff"`, `fillStyle: "solid"` 用于填充

**椭圆**：
```json
{ “类型”：“椭圆”，“id”：“e1”，“x”：100，“y”：100，“宽度”：150，“高度”：150 }
````

**钻石**：
```json
{ “类型”：“钻石”，“id”：“d1”，“x”：100，“y”：100，“宽度”：150，“高度”：150 }
````

**带标签的形状（容器绑定）** -- 创建绑定到形状的文本元素：

> **警告：** 不要在形状上使用 `"label": { "text": "..." }`。这不是有效的
> Excalidraw 属性将被默默忽略，产生空白形状。你必须
> 使用下面的容器绑定方法。

形状需要列出文本的“boundElements”，并且文本需要指向后面的“containerId”：
```json
{“类型”：“矩形”，“id”：“r1”，“x”：100，“y”：100，“宽度”：200，“高度”：80，
  “圆度”：{“类型”：3}，“背景颜色”：“#a5d8ff”，“填充样式”：“固体”，
  "boundElements": [{ "id": "t_r1", "type": "text" }] },
{“类型”：“文本”，“id”：“t_r1”，“x”：105，“y”：110，“宽度”：190，“高度”：25，
  “文本”：“你好”，“字体大小”：20，“fontFamily”：1，“笔触颜色”：“#1e1e1e”，
  “textAlign”：“居中”，“verticalAlign”：“中间”，
  “containerId”：“r1”，“originalText”：“你好”，“autoResize”：true }
````
- 适用于矩形、椭圆形、菱形
- 设置“containerId”时，Excalidraw 自动居中文本
- 文本 `x`/`y`/`width`/`height` 是近似值 -- Excalidraw 在加载时重新计算它们
- `originalText` 应该匹配 `text`
- 始终包含 `fontFamily: 1` （Virgil/手绘字体）

**标记箭头** -- 相同的容器绑定方法：
```json
{“类型”：“箭头”，“id”：“a1”，“x”：300，“y”：150，“宽度”：200，“高度”：0，
  "points": [[0,0],[200,0]], "endArrowhead": "箭头",
  “boundElements”：[{“id”：“t_a1”，“类型”：“文本”}]}，
{“类型”：“文本”，“id”：“t_a1”，“x”：370，“y”：130，“宽度”：60，“高度”：20，
  “文本”：“连接”，“字体大小”：16，“fontFamily”：1，“笔触颜色”：“#1e1e1e”，
  “textAlign”：“居中”，“verticalAlign”：“中间”，
  “containerId”：“a1”，“originalText”：“连接”，“autoResize”：true }
````

**独立文本**（仅标题和注释——无容器）：
```json
{“类型”：“文本”，“id”：“t1”，“x”：150，“y”：138，“文本”：“你好”，“fontSize”：20，
  “fontFamily”：1，“笔画颜色”：“#1e1e1e”，“originalText”：“你好”，“autoResize”：true }
````
- `x` 是左边缘。要以位置“cx”为中心：“x = cx - (text.length * fontSize * 0.5) / 2”
- 不要依赖“textAlign”或“width”进行定位

**箭头**：
```json
{“类型”：“箭头”，“id”：“a1”，“x”：300，“y”：150，“宽度”：200，“高度”：0，
  "点": [[0,0],[200,0]], "endArrowhead": "箭头" }
````
- `points`: `[dx, dy]` 相对于元素 `x`, `y` 的偏移量
- `endArrowhead`: `null` | `“箭头”` | `“酒吧”` | `“点”` | `“三角形”`
- `笔触样式`: `"solid"` (默认) | `“虚线”` | `“点”`

### 箭头绑定（将箭头连接到形状）

```json
{
  “类型”：“箭头”，“id”：“a1”，“x”：300，“y”：150，“宽度”：150，“高度”：0，
  "points": [[0,0],[150,0]], "endArrowhead": "箭头",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
````

`fixedPoint` 坐标：`top=[0.5,0]`、`bottom=[0.5,1]`、`left=[0,0.5]`、`right=[1,0.5]`

### 绘图顺序（z 顺序）
- 数组顺序 = z 顺序（第一个 = 后面，最后一个 = 前面）
- 逐步发射：背景区域→形状→其绑定文本→其箭头→下一个形状
- 不好：所有矩形，然后所有文本，然后所有箭头
- 好：bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
- 始终将绑定文本元素放置在其容器形状之后

### 尺码指南

**字体大小：**
- 正文、标签、描述的最小“fontSize”：**16**
- 标题和标题的最小“fontSize”：**20**
- 最小“fontSize”：**14** 仅适用于辅助注释（谨慎）
- 切勿使用低于 14 的“fontSize”

**元件尺寸：**
- 最小形状尺寸：120x60（用于标记的矩形/椭圆形）
- 元素之间至少留有 20-30px 的间隙
- 比起许多小元素，更喜欢更少、更大的元素

### 调色板

有关全色表，请参阅“references/colors.md”。快速参考：

|使用|填充颜​​色|十六进制 |
|-----|------------|-----|
|主要/输入|浅蓝色| `#a5d8ff` |
|成功/输出 |浅绿色| `#b2f2bb` |
|警告/外部|浅橙色| `#ffd8a8` |
|加工/特殊|浅紫色| `#d0bfff` |
|错误/严重 |浅红色| `#ffc9c9` |
|笔记/决定|浅黄色| `#fff3bf` |
|存储/数据|浅青色| `#c3fae8` |

### 提示
- 在整个图表中使用一致的调色板
- **文本对比度至关重要** - 切勿在白色背景上使用浅灰色。白色最小文本颜色：`#757575`
- 不要在文本中使用表情符号——它们不会以 Excalidraw 的字体呈现
- 对于暗模式图，请参阅“references/dark-mode.md”
- 对于更大的示例，请参阅“references/examples.md”