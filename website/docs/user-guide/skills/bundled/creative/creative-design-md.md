---
title: "Design Md — Author/validate/export Google's DESIGN"
sidebar_label: "Design Md"
description: "Author/validate/export Google's DESIGN"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 设计博士

创作/验证/导出 Google 的 DESIGN.md 令牌规范文件。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/设计-md` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `design`、`design-system`、`tokens`、`ui`、`accessibility`、`wcag`、`tailwind`、`dtcg`、`google` |
|相关技能| [`popular-web-designs`](/docs/user-guide/skills/bundled/creative/creative-popular-web-designs)、[`claude-design`](/docs/user-guide/skills/bundled/creative/creative-claude-design)、[`excalidraw`](/docs/user-guide/skills/bundled/creative/creative-excalidraw), [`架构图`](/docs/user-guide/skills/bundled/creative/creative-architecture-diagram) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# DESIGN.md 技能

DESIGN.md 是 Google 的开放规范（Apache-2.0，`google-labs-code/design.md`）
向编码代理描述视觉识别。一个文件结合了：

- **YAML 前面的内容** — 机器可读的设计标记（规范值）
- **Markdown body** — 人类可读的基本原理，组织成规范部分

令牌给出精确的值。散文告诉代理人“为什么”这些价值观存在以及如何存在
应用它们。 CLI (`npx @google/design.md`) lints 结构 + WCAG 对比，
比较版本以进行回归，并导出到 Tailwind 或 W3C DTCG JSON。

## 什么时候使用这个技能

- 用户请求 DESIGN.md 文件、设计令牌或设计系统规范
- 用户希望跨多个项目或工具保持一致的 UI/品牌
- 用户粘贴现有的 DESIGN.md 并要求对其进行 lint、diff、导出或扩展
- 用户要求将风格指南移植为代理可以使用的格式
- 用户希望在其调色板上进行对比度/WCAG 可访问性验证

对于纯粹的视觉灵感或布局示例，请使用“流行网页设计”
相反。设计一次性 HTML 工件时的*流程和品味*
从头开始（原型、平台、登陆页面、组件实验室），使用
“克劳德设计”。该技能适用于*正式规范文件*本身。

## 文件剖析

``MD
---
版本：阿尔法
名称： 遗产
描述：建筑极简主义与新闻庄严相结合。
颜色：
  主要：“#1A1C1E”
  次要：“#6C7278”
  第三级：“#B8422E”
  中性：“#F7F5F2”
版式：
  h1：
    字体系列：Public Sans
    字体大小：3rem
    字体粗细：700
    行高：1.1
    字母间距：“-0.02em”
  身体MD：
    字体系列：Public Sans
    字体大小：1rem
圆角：
  短：4 像素
  MD: 8 像素
  长：16 像素
间距：
  短：8 像素
  MD: 16 像素
  长：24 像素
组件：
  主要按钮：
    背景颜色：“{colors.tertiary}”
    文字颜色：“#FFFFFF”
    四舍五入：“{rounded.sm}”
    内边距：12px
  按钮主悬停：
    背景颜色：“{颜色.primary}”
---

## 概述

建筑极简主义与新闻庄严相遇......

## 颜色

- **主要 (#1A1C1E)：** 标题和核心文本的深墨迹。
- **第三级（#B8422E）：**“Boston Clay”——交互的唯一驱动力。

## 版式

Public Sans 适用于除小型全大写标签之外的所有内容...

## 组件

“button-primary”是页面上唯一高度强调的操作......
````

## 代币类型

|类型 |格式|示例|
|------|--------|---------|
|颜色 | `#` + 十六进制 (sRGB) | `“#1A1C1E”` |
|尺寸|数字 + 单位 (`px`, `em`, `rem`) | `48px`, `-0.02em` |
|代币参考 | `{path.to.token}` | `{颜色.primary}` |
|版式|具有 `fontFamily`、`fontSize`、`fontWeight`、`lineHeight`、`letterSpacing`、`fontFeature`、`fontVariation` 的对象 |见上文 |

组件属性白名单：`backgroundColor`、`textColor`、`typography`、
“圆角”、“填充”、“大小”、“高度”、“宽度”。变体（悬停、活动、
按下）是**单独的组件条目**以及相关的键名称
（`button-primary-hover`），不嵌套。

## 规范部分顺序

部分是可选的，但当前的部分必须按此顺序出现。重复
标题拒绝该文件。

1. 概述（又名：品牌与风格）
2. 颜色
3. 版式
4.布局（别名：Layout & Spacing）
5. 高程和深度（别名：高程）
6. 形状
7. 组件
8. 该做和不该做的事情

未知部分会被保留，不会出错。接受未知的令牌名称
如果值类型有效。未知的组件属性会产生警告。

## 工作流程：创作新的 DESIGN.md

1. **询问用户**（或推断）品牌基调、强调色和版式
   方向。如果他们提供了网站、图像或氛围，请将其翻译为
   上面的令牌形状。
2. **使用“write_file”在项目根目录中写入“DESIGN.md”。总是
   包括“名称：”和“颜色：”；其他部分可选但鼓励。
3. **在 `components:` 部分中使用标记引用** (`{colors.primary}`)
   而不是重新输入十六进制值。保持调色板单一来源。
4. **检查它**（见下文）。修复任何损坏的引用或 WCAG 故障
   返回之前。
5. **如果用户已有项目**，也写Tailwind或DTCG
   导出到文件旁边（`tailwind.theme.json`、`tokens.json`）。

## 工作流程：lint / diff / 导出

CLI 是“@google/design.md”（节点）。使用“npx”——无需全局安装。

````bash
# 验证结构+token引用+WCAG对比
npx -y @google/design.md lint DESIGN.md

# 比较两个版本，回归失败（退出 1 = 回归）
npx -y @google/design.md diff DESIGN.md DESIGN-v2.md

# 导出到 Tailwind 主题 JSON
npx -y @google/design.md 导出 --format tailwind DESIGN.md > tailwind.theme.json

# 导出为 W3C DTCG（设计令牌格式模块）JSON
npx -y @google/design.md 导出 --format dtcg DESIGN.md > tokens.json

# 打印规范本身——在注入代理提示符时很有用
npx -y @google/design.md 规范 --rules-only --format json
````

所有命令都接受标准输入“-”。 `lint` 出现错误时返回退出 1。使用
如果需要报告结果，请使用“--format json”标志并解析输出
结构上。

### Lint 规则参考（7 个规则捕获的内容）

- `broken-ref` (错误) — `{colors.missing}` 指向一个不存在的标记
- `duplicate-section` (错误) — 相同的 `## Heading` 出现两次
- `无效颜色`、`无效尺寸`、`无效排版`（错误）
- `wcag-contrast` (警告/信息) — 组件 `textColor` 与 `backgroundColor`
  与 WCAG AA (4.5:1) 和 AAA (7:1) 的比例
- `unknown-component-property`（警告）- 在上面的白名单之外

当用户关心可访问性时，请在您的
摘要 — WCAG 的调查结果是使用 CLI 的最有说服力的理由。

## 陷阱

- **不要嵌套组件变体。** `button-primary.hover` 是错误的；
  `button-primary-hover` 作为同级键是正确的。
- **十六进制颜色必须是带引号的字符串。** YAML 会因为 `#` 或
  奇怪地截断像“#1A1C1E”这样的值。
- **负尺寸也需要引号。** `letterSpacing: -0.02em` 解析为
  YAML 流程 — 编写 `letterSpacing: "-0.02em"`。
- **强制执行章节顺序。** 如果用户以随机顺序向您提供散文，
  在保存之前对其重新排序以匹配规范列表。
- **`version: alpha` 是当前规范版本**（截至 2026 年 4 月）。规格
  被标记为 alpha——注意重大变化。
- **令牌引用通过点路径解析。** `{colors.primary}` 有效；
  `{primary}` 没有。

## 规格真相来源

- 仓库：https://github.com/google-labs-code/design.md (Apache-2.0)
- CLI：npm 上的“@google/design.md”
- 生成的 DESIGN.md 文件的许可证：无论用户的项目使用什么；
  该规范本身是 Apache-2.0。