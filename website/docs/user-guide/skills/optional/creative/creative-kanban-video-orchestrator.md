---
title: "Kanban Video Orchestrator — Plan, set up, and monitor a multi-agent video production pipeline backed by OpenClaw Kanban"
sidebar_label: "Kanban Video Orchestrator"
description: "Plan, set up, and monitor a multi-agent video production pipeline backed by OpenClaw Kanban"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 看板视频编排器

规划、设置和监控由 OpenClaw 看板支持的多代理视频制作管道。当用户想要制作任何视频时使用 - 叙事电影、产品/营销、音乐视频、解释器、ASCII/终端艺术、抽象/生成循环、漫画、3D、实时/安装 - 并且工作需要分解为通过看板协调的专业配置文件（作家、设计师、动画师、渲染器、声音、编辑器等）。执行自适应发现来确定概要范围，为所请求的风格设计适当的团队，生成创建 OpenClaw 配置文件 + 初始看板任务的设置脚本，然后帮助监控执行情况并在任务停滞或失败时进行干预。将场景路由到适合每个节拍的 OpenClaw 渲染/音频/设计技能（`ascii-video`、`manim-video`、`p5js`、`comfyui`、`touchdesigner-mcp`、`blender-mcp`、`pixel-art`、`baoyu-comic`、`claude-design`、`excalidraw`、`songsee`、`heartmula` 等）以及用于 TTS 的外部 API，根据需要进行图像生成和图像转视频。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/creative/kanban-video-orchestrator` 安装 |
|路径| `可选技能/创意/看板视频编排器` |
|版本 | `1.0.0` |
|作者 | ['SHL0MS', '替代故障'] |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `视频`、`看板`、`多代理`、`编排`、`生产管道` |
|相关技能| [`ascii-video`](/docs/user-guide/skills/bundled/creative/creative-ascii-video), [`manim-video`](/docs/user-guide/skills/bundled/creative/creative-manim-video), [`p5js`](/docs/user-guide/skills/bundled/creative/creative-p5js), [`comfyui`](/docs/user-guide/skills/bundled/creative/creative-comfyui)、[`touchdesigner-mcp`](/docs/user-guide/skills/bundled/creative/creative-touchdesigner-mcp)、[`blender-mcp`](/docs/user-guide/skills/optional/creative/creative-blender-mcp), [`pixel-art`](/docs/user-guide/skills/optional/creative/creative-pixel-art), [`ascii-art`](/docs/user-guide/skills/bundled/creative/creative-ascii-art), [`songwriting-and-ai-music`](/docs/user-guide/skills/bundled/creative/creative-songwriting-and-ai-music), [`heartmula`](/docs/user-guide/skills/bundled/media/media-heartmula)、[`songsee`](/docs/user-guide/skills/bundled/media/media-songsee)、`spotify`、[`youtube-content`](/docs/user-guide/skills/bundled/media/media-youtube-content)、 [`claude-design`](/docs/user-guide/skills/bundled/creative/creative-claude-design)、[`excalidraw`](/docs/user-guide/skills/bundled/creative/creative-excalidraw)、[`architecture-diagram`](/docs/user-guide/skills/bundled/creative/creative-architecture-diagram), [`concept-diagrams`](/docs/user-guide/skills/optional/creative/creative-concept-diagrams), [`baoyu-comic`](/docs/user-guide/skills/optional/creative/creative-baoyu-comic), [`baoyu-infographic`](/docs/user-guide/skills/bundled/creative/creative-baoyu-infographic), [`humanizer`](/docs/user-guide/skills/bundled/creative/creative- humanizer)、[`gif-search`](/docs/user-guide/skills/bundled/media/media-gif-search)、[`meme- Generation`](/docs/user-guide/skills/optional/creative/creative-meme- Generation) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 看板视频编排器

封装任何视频请求 - 从 15 秒的产品预告片到 5 分钟的叙述
短到音乐视频到 ASCII 循环 — 在 OpenClaw 看板管道中
将工作分解为专门的代理配置文件。

该技能本身**不**渲染任何东西。它是一个元管道：

1. **通过有针对性的发现确定请求的范围**
2. **根据风格设计**合适的团队（哪些角色，每个角色哪些工具）
3. **生成**一个设置脚本，用于创建 OpenClaw 配置文件、项目工作区和初始看板任务
4. **交给主管档案**，该档案通过看板进行分解
5. **监控**执行，帮助在任务停滞或失败时进行干预

一旦运行，实际的渲染就会在看板内部发生，无论通过哪个
现有的技能+工具适合场景——“ascii-video”、“manim-video”、“p5js”、
`comfyui`、`touchdesigner-mcp`、`blender-mcp`、`歌曲创作和人工智能音乐`、
`heartmula`、外部 API 或带有 PIL + ffmpeg 的纯 Python。

## 何时不使用此技能

- 该视频是一个连续的程序项目，不需要专家。直接写代码就可以了。
- 用户想要快速一次性转换（例如“将此 mp4 转换为 GIF”）——直接使用 ffmpeg。
- 输出是静态图像、GIF 或纯音频工件 - 使用匹配的特定技能（“ascii-art”、“gifs”、“meme- Generation”、“songwriting-and-ai-music”）。
- 该作品完全适合单一现有技能（例如纯 ASCII 视频 - 只需使用“ascii-video”）。

## 工作流程

````
发现 → 简介 → 团队设计 → 设置 → 执行 → 监控
````

### 第 1 步 — 发现（提出正确的问题）

发现过程是**适应性**：只询问实际需要的东西。总是
从三个问题开始确定大致形状：

- **视频是什么？**（一句话简介）
- **多长？**（5-30 秒预告片/30-90 秒短片/90 秒-3 分钟解释/3-10 分钟影片/较长）
- **什么宽高比 + 目标平台？**（1:1 / 9:16 / 16:9；X、IG、YouTube、内部等）

根据答案，对风格类别进行分类。风格决定了
要问的后续问题。 **不要一次询问所有问题。** 一次询问 2-4 个问题
时间，聆听，然后继续。每当用户使用时做出合理的假设
暗示着一个答案。

有关完整的摄入模式和每种风格的问题库，请参阅
**[references/intake.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/kanban-video-orchestrator/references/intake.md)**。

### 第 2 步 — 简介

一旦了解了足够的信息，就可以使用中的模板生成结构化的“brief.md”
`资产/brief.md.tmpl`。阶段：

1. **概念**——一句话推介+情感北极星
2. **范围** — 持续时间、方面、平台、截止日期
3. **风格** — 视觉参考、品牌限制、基调
4. **场景** — 逐个节拍细分（持续时间、内容、目标工具）
5. **音频** — 旁白/音乐/SFX/无声（如果需要，每个场景）
6. **可交付成果** — 文件格式、分辨率、可选替代方案（垂直剪切、GIF 等）

在设计团队之前，向用户展示概要以供确认。 **该
Brief 是合约**——每个下游任务都会引用它。

### 步骤 3 — 团队设计

从库中选择适合该视频的角色原型。 **撰写，不要
克隆。** 大多数视频需要 4-7 个配置文件。导演始终在场；的
其余的根据简报的实际需要进行选择。

有关角色库和每种风格的团队组成，请参阅
**[references/role-archetypes.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/kanban-video-orchestrator/references/role-archetypes.md)**。

有关映射角色→加载哪些 OpenClaw 技能 + 工具集，请参阅
**[references/tool-matrix.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/kanban-video-orchestrator/references/tool-matrix.md)**。

### 第 4 步 — 设置

生成安装脚本（`setup.sh`）并运行它。脚本：

1. 创建项目工作区 (`~/projects/video-pipeline/<slug>/`)
2. 将任何提供的资源复制到 `taste/`、`audio/`、`assets/` 中
3. 通过 `hermes profile create --clone` 创建每个 OpenClaw 配置文件
4. 编写每个配置文件“SOUL.md”（个性+角色定义）
5. 配置配置文件 YAML（工具集、always_load 技能、cwd）
6. 写入 `brief.md`、`TEAM.md` 和 `taste/` 内容
7. 触发分配给主管的初始“hermes kanban create”任务

使用 `scripts/bootstrap_pipeline.py` 从简短的 + 中生成 setup.sh
团队设计 JSON。请参阅 **[references/kanban-setup.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/kanban-video-orchestrator/references/kanban-setup.md)**
用于设置脚本结构、配置文件配置模式和关键
“共享工作空间”规则。

### 步骤 5 — 执行

运行“setup.sh”。然后向用户提供监控命令：

````bash
Hermes 看板手表 --tenant <project-tenant> # 现场活动
Hermes 看板列表 --tenant <project-tenant> # 板快照
Hermes仪表板#可视化板UI
````

导演档案从这里接管，分解工作和路由
通过看板工具集将任务分配给专家档案。

### 第 6 步 — 监控和干预

保持参与——看板自主运行，但任务卡住或输出不佳
需要人类（或人工智能）的判断。

监控模式：定期轮询“看板列表”，检查任何正在运行的任务
超出了“看板显示 <id>”的预期持续时间，并检查
心跳。当工人的产出未通过审核时，标准干预措施是：

1. 通过具体反馈对工作人员的任务进行评论（`kanban_comment`）
2. 创建一个以原始任务为父级的重新运行任务
3.调整概要范围，让导演重新分解

对于诊断模式、干预方案和“任务被卡住”
剧本，请参阅 **[references/monitoring.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/kanban-video-orchestrator/references/monitoring.md)**。

## 参考：工作示例

六个具体的管道涵盖了截然不同的视频风格——叙事电影、
产品/营销、音乐视频、数学/算法解释、ASCII 视频、实时
安装——展示相同的工作流程如何产生截然不同的团队和
任务图。请参阅 **[references/examples.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/creative/kanban-video-orchestrator/references/examples.md)**。

## 关键规则

1. **行动前的发现。** 切勿在没有完成任务的情况下开始生成简报或团队
   至少询问三个基线问题。糟糕的简短内容层出不穷
   整个管道。

2. **将团队与视频进行匹配。** 不要重复使用相同的 4 个人资料设置
   每一项工作。没有节拍分析配置文件的音乐视频将
   失火。一部没有编剧简介的叙事电影将会产生
   不连贯的场景。请参阅“references/role-archetypes.md”。

3. **每个项目一个工作区。** 给定视频的所有配置文件共享相同的配置文件
   `dir:` 工作区。任务通过共享文件系统和结构化传递工件
   交接。 **每个** `kanban_create` 调用都会通过
   `workspace_kind="dir"` + `workspace_path="<绝对项目路径>"`。

4. **为每个项目提供租户。** 使用特定于项目的租户
   (`--tenant <project-slug>`)。保持仪表板范围并防止
   与其他正在进行的看板交叉授粉。

5. **尊重现有技能。** 当场景适合现有技能时，
   相关渲染器应通过“--skill <name>”在其任务中加载该技能
   或配置文件中的“always_load”。不要重新推导已有的技能
   提供。

6. **导演永远不会执行。** 即使有完整的“看板 + 终端 +
   file`工具集，director的`SOUL.md`规则禁止它执行
   工作本身。它只分解和路由——每一个具体任务都变成
   对专家配置文件的“hermes 看板创建”调用。的
   自动注入的看板编排指南进一步阐明了这一点。

7. **不要过度分解。** 30秒的产品视频不需要20个任务。
   目标是仍然能够很好地并行化并公开的最小任务图
   正确的人工审查门。

8. **在触发之前验证 API 密钥。** 外部 API（TTS、图像生成、
   图像到视频）需要 `${HERMES_HOME:-~/.hermes}/.env` 或用户的秘密存储中的密钥。
   遇到丢失键错误的工作人员会浪费一个任务槽。设置
   如果缺少所需的密钥，脚本的“check_key”助手会干净地中止。

## 文件映射

````
SKILL.md ← 这个文件（工作流程+规则）
参考文献/
  Intake.md ← 发现每种风格的问题库
  role-archetypes.md ← 角色库（作家、设计师、动画师……）
  tool-matrix.md ← 每个角色的技能 + 工具集映射
  kanban-setup.md ← 设置脚本结构和配置文件配置
  监控.md ← 观察+干预模式
  example.md ← 六个工作管道
资产/
  Brief.md.tmpl ← 简要骨架
  setup.sh.tmpl ← 设置脚本框架
  Soul.md.tmpl ← 个人资料人格骨架
脚本/
  bootstrap_pipeline.py ← 从brief + team JSON生成setup.sh
  Monitor.py ← 轮询 + 干预助手
````