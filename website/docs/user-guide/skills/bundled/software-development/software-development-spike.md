---
title: "Spike — Throwaway experiments to validate an idea before build"
sidebar_label: "Spike"
description: "Throwaway experiments to validate an idea before build"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 斯派克

在构建之前进行一次性实验来验证想法。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/软件开发/峰值` |
|版本 | `1.0.0` |
|作者 | OpenClaw（改编自 gsd-build/get-shit-done） |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `spike`、`原型`、`实验`、`可行性`、`一次性`、`探索`、`研究`、`规划`、`mvp`、`概念验证` |
|相关技能| [`sketch`](/docs/user-guide/skills/bundled/creative/creative-sketch)、[`subagent-driven-development`](/docs/user-guide/skills/optional/software-development/software-development-subagent-driven-development)、[`plan`](/docs/user-guide/skills/bundled/software-development/software-development-plan) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 斯派克

当用户想要在进行真正的构建之前**摸出一个想法**时，请使用此技能 - 验证可行性、比较方法或解决任何研究都无法回答的未知问题。尖刺设计为一次性的。一旦他们还清了债务，就把它们扔掉。

当用户说“让我试试这个”、“我想看看 X 是否有效”、“把它搞清楚”、“在我提交 Y 之前”、“Z 的快速原型”、“这可能吗？”或“比较 A 与 B”等内容时加载此内容。

## 什么时候不应该使用这个

- 答案可以从文档或阅读代码中得知——只做研究，而不是构建
- 工作是生产路径——使用“计划”技能
- 这个想法已经得到验证——直接跳到实施

## 如果用户安装了完整的GSD系统

如果“gsd-spike”显示为同级技能（通过“npx get-shit-done-cc --hermes”安装），则当用户需要完整的 GSD 工作流程时更喜欢“gsd-spike”：持久的“.planning/spikes/”状态、跨会话的 MANIFEST 跟踪、Given/When/Then 判决格式以及与 GSD 其余部分集成的提交模式。该技能是轻量级独立版本，适合没有（或不需要）完整系统的用户。

## 核心方法

无论规模大小，每个尖峰都遵循以下循环：

````
分解→研究→构建→判决
   ↑_______________________________________________↓
                  迭代调查结果
````

### 1.分解

将用户的想法分解为**2-5个独立的可行性问题**。每个问题都是一个尖峰。将它们呈现为带有给定/何时/然后框架的表格：

| ＃|斯派克 |验证（给定/何时/然后）|风险|
|---|--------|----------------------------|------|
| 001| websocket 流 |给定 WS 连接，当 LLM 流式传输令牌时，客户端接收的块 < 100ms |高|
| 002a| pdf-parse-pdfjs | pdf-parse-pdfjs |给定一个多页 PDF，当使用 pdfjs 解析时，可以提取结构化文本 |中等|
| 002b | pdf-解析-camelot |给定一个多页 PDF，当用 Camelot 解析时，可以提取结构化文本 |中等|

**尖峰类型：**
- **标准** — 一种方法回答一个问题
- **比较** - 相同的问题，不同的方法（共享数字，字母后缀“a”/“b”/“c”）

**好的尖峰问题：**具有可观察输出的具体可行性。
**不好的尖峰问题：**太宽泛，没有可观察的输出，或者只是“阅读有关 X 的文档”。

**按风险排序。** 最有可能扼杀创意的尖峰首先运行。如果困难的部分不起作用，那么对简单的部分进行原型设计就没有意义。

**仅当用户已经确切知道他们想要增加什么并明确表示时才跳过分解**。然后将他们的想法视为一个尖峰。

### 2.对齐（对于多尖峰想法）

呈现尖峰表。问：“全部按照这个顺序构建，还是调整？”在编写任何代码之前，让用户删除、重新排序或重新构建。

### 3. 研究（每个尖峰，构建前）

尖峰并不是不需要研究的——你需要进行足够的研究来选择正确的方法，然后你才能构建。每个尖峰：

1. **简单介绍一下。** 2-3 句话：这个峰值是什么、为什么重要、关键风险。
2. **表面竞争方法**（如果有真正的选择）：

   |方法|工具/库 |优点 |缺点 |状态 |
   |----------|-------------|------|-----|--------|
   | ... | ... | ... | ... |维护/放弃/测试版|

3. **选择一个。** 说明原因。如果 2+ 是可信的，则在尖峰内构建快速变体。
4. **跳过对没有外部依赖的纯逻辑的研究**。

使用 OpenClaw 工具进行研究步骤：

- `web_search("python websocket Streaming Library 2025")` — 查找候选者
- `web_extract(urls=["https://websockets.readthedocs.io/..."])` — 阅读实际文档（返回 markdown）
- `terminal("pip show websockets | grep Version")` — 检查项目的 venv 中安装的内容

对于没有文档页面的库，请通过“read_file”克隆并阅读其“README.md”/“examples/”。 Context7 MCP（如果用户已配置）也是一个很好的来源 - `mcp_*_resolve-library-id` 然后是 `mcp_*_query-docs`。

### 4. 构建

每个尖峰一个目录。保持其独立。

<!-- ascii-guard-ignore -->
````
尖峰/
├── 001-websocket-streaming/
│ ├── README.md
│ └── main.py
├── 002a-pdf-parse-pdfjs/
│ ├── README.md
│ └── parse.js
└── 002b-pdf-parse-camelot/
    ├── README文件.md
    └── 解析.py
````
<!-- ascii-guard-ignore-end -->

**偏向于用户可以交互的东西。** 当唯一的输出是一条显示“它有效”的日志行时，尖峰就会失败。用户想要“感觉”尖峰正在工作。默认选择，按优先顺序排列：

1. 一个可运行的 CLI，它接受输入并打印可观察的输出
2. 演示行为的最小 HTML 页面
3. 具有一个端点的小型 Web 服务器
4. 使用可识别的断言来练习问题的单元测试

**深度胜于速度。** 切勿在一次愉快的路径运行后宣称“它有效”。测试边缘情况。关注令人惊讶的发现。只有调查诚实时，判决才可信。

**避免**，除非尖峰特别需要它：复杂的包管理、构建工具/捆绑器、Docker、环境文件、配置系统。对一切进行硬编码——这是一个尖峰。

**构建一个尖峰** — 典型的工具序列：

````
终端（“mkdir -p 尖峰/001-websocket-streaming”）
write_file("spikes/001-websocket-streaming/README.md", "# 001: websocket-streaming\n\n...")
write_file("spikes/001-websocket-streaming/main.py", "...")
终端（“cd 尖峰/001-websocket-streaming && python3 main.py”）
# 观察输出，迭代。
````

**并行比较峰值 (002a / 002b) — 委托。** 当两种方法可以并行运行并且都需要真正的工程（不是 10 行原型）时，请使用 `delegate_task` 进行扇出：

````
delegate_task(任务=[
    {“目标”：“构建002a-pdf-parse-pdfjs：...”，“工具集”：[“终端”，“文件”，“网络”]}，
    {“目标”：“构建002b-pdf-parse-camelot：...”，“工具集”：[“终端”，“文件”，“网络”]}，
]）
````

每个子代理返回自己的判决；你写的是头对头。

### 5.判决

每个峰值的“README.md”以以下内容结尾：

``降价
## 结论：已验证 |部分|无效

### 什么有效
- ...

### 什么没有
- ...

### 惊喜
- ...

### 真实构建的推荐
- ...
````

**已验证** = 核心问题的答案是肯定的，有证据。
**部分** = 它在约束 X、Y、Z 下工作 - 记录它们。
**INVALIDATED** = 不起作用，因此。这是一次成功的突袭。

## 比较峰值

当两种方法回答同一问题（002a / 002b）时，**背对背**构建它们，然后在最后进行头对头比较：

``降价
## 正面对决：pdfjs 与 Camelot

|尺寸| pdfjs (002a) | pdfjs (002a) |卡莱特 (002b) |
|------------|--------------|----------------|
|萃取品质 | 9/10 结构化 | 7/10 仅限餐桌 |
|设置复杂性 | npm 安装，1 行 |点 + 鬼脚本 |
| 100 页 PDF 的性能 | 3秒| 18 岁 |
|处理旋转文本 |没有|是的 |

**获胜者：** pdfjs 适合我们的用例。 Camelot 如果我们稍后需要表优先提取。
````

## 前沿模式（选择下一步要刺杀的内容）

如果尖峰已经存在并且用户说“接下来我应该尖峰什么？”，则遍历现有目录并查找：

- **集成风险** - 两个经过验证的尖峰接触相同的资源，但经过独立测试
- **数据切换** — 假定尖峰 A 的输出与尖峰 B 的输入兼容；从未被证明
- **愿景中的差距** - 假设但未经证实的能力
- **替代方法** - 针对部分或无效尖峰的不同角度

按照给定/当/那么的方式提议 2-4 名候选人。让用户选择。

## 输出

- 在存储库根目录中创建“spikes/”（如果用户使用 GSD 约定，则创建“.planning/spikes/”）
- 每个尖峰一个目录：`NNN-描述性名称/`
- 每个峰值的“README.md”捕获问题、方法、结果、结论
- 保持代码一次性 - 需要 2 天来“清理生产”的峰值是一个糟糕的峰值

## 归因

改编自 GSD (Get Shit Done) 项目的 `/gsd-spike` 工作流程 — MIT © 2025 Lex Christopherson ([gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done))。完整的 GSD 系统提供持久的峰值状态、MANIFEST 跟踪以及与更广泛的规范驱动的开发管道的集成；使用“npx get-shit-done-cc --hermes --global”安装。