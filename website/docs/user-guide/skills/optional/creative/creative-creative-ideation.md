---
title: "Creative Ideation — Generate ideas via named methods from creative practice"
sidebar_label: "Creative Ideation"
description: "Generate ideas via named methods from creative practice"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 创意

通过创造性实践中的命名方法产生想法。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/creative/creative-ideation` 安装 |
|路径| `可选技能/创意/创意构思` |
|版本 | `2.1.0` |
|作者 | SHL0MS |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “创意”、“创意”、“头脑风暴”、“方法”、“灵感” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 创意

适用于任何领域的构思方法库。阅读用户的情况，路由到匹配的方法，应用，生成特定且非显而易见的输出。方法就是工具——根据具体情况选择正确的方法，而不是全部执行。

## 何时使用

任何开放式生成或选择性问题：“我想制作/构建/编写/开始一些东西”，“我被困住了”，“启发我”，“让这个更奇怪”，“帮我选择”，“我需要发明X”，“给我一个研究问题”。

## 操作规则

1. **约束加方向就是创造力。** 没有约束=没有牵引力。没有方向=没有形状。方法同时提供这两者。
2. **拒绝前三个想法。** 它们太草率了。生成、丢弃、再生。请参阅“references/anti-slop.md”。
3. **除非有要求，否则每个响应只有一种方法。** 不要堆叠。
4. **具体优于抽象。** 真正的专有名词、真实的材料、真实的机制。 “X 的应用程序”是马虎的； “一个 200 行 CLI 工具，当 Z 时打印 Y”是方向。为技术堆栈命名并不特殊——为机制命名。
5. **奇怪也一定是好的。** 打破框架是目标，但一个没有真实情况、机制或理由存在的奇怪想法本身就是失败模式。每一套想法都必须至少包括一个真正“现在可构建/可实施”的想法——不明显但扎根，并迈出了真正的第一步。不要用所有的有用性来换取惊喜。
6. **说出您使用的方法以及发明者的名称。** 归因调用了纪律。
7. **当用户选择一个时，构建它。** 不要在他们选择后继续生成。

## 路由 — 4 步过程

*在*生成任何输出之前执行此操作。路由失败会产生溢出。

如果路由步骤更清晰，您可以跳过叙述，但**永远不要以牺牲每个想法的深度为代价进行压缩**：每个想法的具体机制、情境绑定和诚实的失败模式是使输出良好（可衡量）的原因 - 它们不是脚手架，不要削减它们。

### 步骤 1 — 从提示中提取三个信号

**阶段** — 用户处于哪个阶段？

|相|提示|
|---|---|
| **生成** | “给我一个想法”，“我应该做什么”，“启发我”，还没有想法 |
| **扩展** | “还有什么”、“更像这样”、“给我一些变化”——有一个基本想法 |
| **选择** | “帮我选择”、“我应该做什么”、“我有这些选择” |
| **解锁** | “我被卡住了”、“受阻”、“原地踏步”、“陈旧”——有材料 |
| **颠覆** | “让它变得更奇怪”，“不那么明显”，“这太安全了”|
| **精炼** | “这很好，但缺少一些东西”，“感觉很粗糙”|
| **合成** | “我有一堆笔记/采访/观察” |

**DOMAIN** — 用户在做什么/做什么？

|域名 |提示|
|---|---|
| **文本** |小说、散文、诗歌、抒情诗、剧本、文案|
| **对象** |视觉艺术、音乐、声音、表演、装置、雕塑|
| **神器** |软件、硬件、机制、设备|
| **系统** |组织、公民、机构、生态、社区 |
| **自我** |人生决定、事业、个​​人实践|
| **研究** |论文、论文、学术问题 |
| **产品** |商业、市场、服务|

**具体性** — 提示中有多少限制？

|水平|提示|
|---|---|
| **无** | “我很无聊”，“激励我”——没有领域，没有项目 |
| **域名** | “我想写点东西”——了解这个领域，没有项目 |
| **项目** | “我正在研究这个特定的 X”|
| **问题** | “我在 X 内部有这种特定的摩擦”|

### 步骤 2 — 应用覆盖（最高优先级，首先触发）

覆盖规则击败路由表：

- **情绪信号** — 用户说“怪异”、“奇怪”、“令人惊讶”、“不太明显”、“更有趣”→ `references/methods/ Lateral-pro Vocations.md` 或 `references/methods/pataphysicals.md`，无论域如何。
- **用户命名一个方法** - 使用它。
- **用户要求推荐方法**（“哪种方法”）→ 列出 2-3 个候选者，每人一行，询问应用哪一个。不要默默默认。
- **高坡度地形** — “AI 创意”、“创业创意”、“习惯跟踪器”、“生产力/健康/健身/食品/旅行应用程序” → 强制 `references/methods/ Lateral-provocables.md` 或 `references/methods/pataphysicals.md` 超过明显的方法。拒绝前 **5** 个想法，而不是 3 个。

### 步骤 3 — 首先按阶段路由，然后按域路由

**按阶段（无论领域如何均适用）：**

|相|默认路线 |
|---|---|
|生成 + 特异性=无 | `references/full-prompt-library.md` **一般**部分（约束调度）|
|生成 + 已知领域 |按域路由（下表）|
|扩展| `references/methods/scamper.md` |
|选择| `references/methods/premortem-and-inversion.md` （或 `references/methods/compression-progress.md` 以获得好处） |
|解锁| `references/methods/oblique-strategies.md` |
|颠覆| `references/methods/ Lateral-pro Vocations.md` （后备 `references/methods/pataphysicals.md`） |
|精炼（文本）| `references/methods/defamiliarization.md` |
|精炼（其他）| `references/methods/creative-discipline.md`（萨普的脊柱）|
|综合| `references/methods/affinity-diagrams.md` |
|快速需要量 | `references/methods/volume- Generation.md` |

**按域（当使用已知域进行生成时）：**

|域名 |默认路线 |
|---|---|
|文本 — 正式/诗歌 | `references/methods/oulipo.md` |
|文本——叙述| `references/methods/story-sculptures.md` |
| TEXT — 有源材料可重新混合 | `references/methods/chance-and-remix.md` |
|对象（音乐、视觉、表演）| `references/methods/oblique-strategies.md` |
| OBJECT — 物理制造者/想要一个起始约束 | `references/full-prompt-library.md` **物理/对象**部分 |
| ARTIFACT — 想要一个起始约束 | `references/full-prompt-library.md` **软件/工件**部分 |
| ARTIFACT — 参数冲突的工程发明 | `references/methods/triz-principles.md` |
| ARTIFACT — 软件架构 | `references/methods/pattern-languages.md` |
| ARTIFACT — 具有自然系统模拟 | `参考文献/方法/biomimicry.md` |
| ARTIFACT — 累积的假设值得质疑 | `references/methods/first-principles.md` |
|系统（公民、组织、机构）| `references/methods/leverage-points.md` |
|系统 — 集体/参与 | `references/full-prompt-library.md` **社交/集体**部分 |
| SELF（生活、事业、学习什么）| `references/methods/derive-and-mapping.md` |
|研究——选择一个问题| `references/methods/compression-progress.md` |
|研究——解决已知问题| `参考文献/方法/polya.md` |
|产品（业务、服务）| `references/methods/jobs-to-be-done.md` |
|需要打破框架/寻找类比| `references/methods/analogy-and-blending.md` |

### 步骤 4 — 处理歧义和矛盾

- **可能有多个路径** → 选择最接近用户实际措辞的一个。不要选择最有趣的方法来显得复杂。
- **真正模棱两可** → 问一个澄清问题，不要默默猜测。示例：*“您是在产生想法还是在已有的想法中进行选择？”* / *“这是小说、散文还是其他内容？”*
- **信号相互矛盾**（例如，“奇怪的启动想法”→产品领域+奇怪的情绪）→**明确地堆叠两种方法**。说明你正在做什么：*“使用‘待完成的工作’作为产品框架+‘横向挑衅’来打破明显的形状。”*
- **不匹配** → 约束调度 (`references/full-prompt-library.md`) 是安全的后备方案。
- **再次提出同样的问题** → 切换方法。方法的变化=想法分布的变化。

### 反默认检查（生成前运行）

- 想要写“这里有 5 个想法：”还是一个简单的编号列表？ → 停止。首先选择一个方法。
- 即将默认使用通用法学硕士模式头脑风暴？ → 停止。选择上面的路径。
- 输出看起来像未路由的法学硕士会产生什么？ → 路由失败，重做。

默认的 LLM 模式正是该技能所要取代的。如果你在没有路由的情况下生成，那么你就击败了该技能。

对于更深层次的边缘情况（情绪信号、堆叠、反模式），请参阅“references/heuristics.md”。

## 输出格式

对于约束调度默认路径：

````
## 约束：[名称] — 来自 [来源]
> 【约束，一句话】

### 想法

1. **【单线间距】**
   [2-3 句话——具体是做什么的，为什么有趣]
   ⏱ [周末/周/月] • 🔧 [堆栈/介质/材料]

2....
3....
````

对于其他方法，使用该方法指定的格式（TRIZ 产生矛盾分析；OuLiPo 产生约束文本；Oblique Strategies 产生单个应用卡 → 下一步）。不要将每个方法强制放入约束模板中。

**每个想法集，无论方法如何：**
- 命名所使用的方法。在斜坡地形上，列出你拒绝的明显想法。
- 为每个想法提供具体的机制和诚实的失败模式/权衡/它的用途。这种深度是让想法落地的原因——有节制的，而不是装饰性的。
- 将至少一个想法标记为**扎根**的想法 - 现在可构建/可追求，不明显，但具有真正的第一步。其他人可以向陌生的地方跑得更远；这必须是真正可行的。不要让整套方案显得怪异但不切实际。

## 文件映射

- `references/full-prompt-library.md` — 约束库，按领域（常规、软件、物理、社交、列表）划分。 SPECIFICITY=NONE 的默认路径。
- `references/method-catalog.md` — 一行摘要 + 每个方法的使用时间
- `references/heuristics.md` — 边缘情况的扩展决策树
- `references/anti-slop.md` — 防溢出规则；适用于每个输出
- `references/exercises.md` — 限时练习（5 分钟/30 分钟/1 小时/天/周）
- `references/methods/` — 22 个命名方法，每个方法一个文件，仅加载您正在使用的方法

## 归因

约束调度核心改编自 [wttdotm.com/prompts.html](https://wttdotm.com/prompts.html)。方法取自每个方法文件中引用的主要来源。