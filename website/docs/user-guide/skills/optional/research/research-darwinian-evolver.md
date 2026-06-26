---
title: "Darwinian Evolver — Evolve prompts/regex/SQL/code with Imbue's evolution loop"
sidebar_label: "Darwinian Evolver"
description: "Evolve prompts/regex/SQL/code with Imbue's evolution loop"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 达尔文进化论

使用 Imbue 的进化循环进化提示/正则表达式/SQL/代码。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/darwinian-evolver` 安装 |
|路径| `可选技能/研究/达尔文进化者` |
|版本 | `0.1.0` |
|作者 | Bihruze (Asahi0x)，OpenClaw 代理 |
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | “进化”、“优化”、“即时工程”、“研究” |
|相关技能| [`arxiv`](/docs/user-guide/skills/bundled/research/research-arxiv)、[`jupyter-live-kernel`](/docs/user-guide/skills/bundled/data-science/data-science-jupyter-live-kernel) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 达尔文进化论

运行 Imbue 的 [darwinian_evolver](https://github.com/imbue-ai/darwinian_evolver) —
LLM 驱动的进化搜索循环 — 优化 **提示、正则表达式、SQL 查询、
或针对健身功能的小代码片段**。

状态：上游工具的薄包装。技巧安装它，走它
通过编写“问题”定义（有机体+评估器+变异器）来代理，
并通过上游 CLI 或小型自定义 Python 驱动程序驱动循环。

**许可证：**上游工具是**AGPL-3.0**。该技能仅会调用它
通过上游 CLI 或“subprocess”/“uv run”调用（仅聚合）。不要
将上游类导入 OpenClaw 本身。

## 何时使用

- 用户说“优化此提示”、“为 X 发展正则表达式”、“自动改进此提示”
  code/SQL”，“搜索更好的指令”。
- 你有一个评分器（精确匹配、正则表达式通过率、单元测试、LLM 判断、运行时
  公制）和起始候选者（有机体）。如果你没有得分手，就停下来
  首先定义一个——这是困难的部分。
- 成本还可以：典型的运行是 50-500 个 LLM 调用。在 gpt-4o-mini 上这只是几便士；
  在克劳德十四行诗中，它可能是几美元。

在以下情况下**不要**使用此功能：
- 优化目标是可微的（使用梯度下降/DSPy）。
- 您只需尝试 2-3 个变体 - 只需手写即可。
- 健身信号纯粹是主观的，没有可测量的标准。

## 先决条件

-Python≥3.11
-`git`、`uv`（或`pip`）
- 以下之一：“OPENROUTER_API_KEY”、“ANTHROPIC_API_KEY”或“OPENAI_API_KEY”

该技能附带了一个使用“OPENROUTER_API_KEY”的小型“parrot_openrouter.py”驱动程序
通过 OpenAI SDK，因此 OpenRouter 上的任何模型都可以工作。上游 CLI 本身
硬编码 Anthropic 并需要“ANTHROPIC_API_KEY”。

## 安装（一次性）

通过“terminal”工具运行：

````bash
mkdir -p ~/.hermes/cache/darwinian-evolver && cd ~/.hermes/cache/darwinian-evolver
[-d darwinian_evolver ] || git clone --深度 1 https://github.com/imbue-ai/darwinian_evolver.git
cd darwinian_evolver && uv 同步
````

验证：

````bash
cd ~/.hermes/cache/darwinian-evolver/darwinian_evolver \
  && uv 运行 darwinian_evolver --help |头-5
````

## 快速入门 - 内置 Parrot 示例

微小的烟雾测试（需要`ANTHROPIC_API_KEY`）：

````bash
cd ~/.hermes/cache/darwinian-evolver/darwinian_evolver
uv 运行 darwinian_evolver 鹦鹉 \
  --迭代次数 2 \
  --num_parents_per_iteration 2 \
  --mutator_concurrency 2 --evaluator_concurrency 2 \
  --output_dir /tmp/parrot_demo
````

输出：
- `/tmp/parrot_demo/snapshots/iteration_N.pkl` — 每次迭代的腌制种群
- `/tmp/parrot_demo/<jsonl>` — 每次迭代 JSON 日志（最后打印的路径）

打开 `~/.hermes/cache/darwinian-evolver/darwinian_evolver/darwinian_evolver/lineage_visualizer.html`
在浏览器中加载 JSON 日志以查看进化树。

## 快速入门 — OpenRouter 驱动程序（无 Anthropic Key）

该技能包含 `scripts/parrot_openrouter.py` — 同样的鹦鹉问题，但是
LLM 调用通过 OpenRouter，因此任何提供商都可以工作。

````bash
# 从安装技能的地方：
SKILL_DIR=~/.hermes/skills/research/darwinian-evolver
DE_DIR=~/.hermes/cache/darwinian-evolver/darwinian_evolver

cd "$DE_DIR" && \
  EVOLVER_MODEL='openai/gpt-4o-mini' \
  uv run --with openai python "$SKILL_DIR/scripts/parrot_openrouter.py" \
    --num_iterations 3 --num_parents_per_iteration 2 \
    --output_dir /tmp/parrot_or
````

使用“scripts/show_snapshot.py”检查结果：

````bash
uv run --with openai python "$SKILL_DIR/scripts/show_snapshot.py" \
  /tmp/parrot_or/snapshots/iteration_3.pkl
````

预期输出：7个进化提示模板，按分数排名，其中最好
落在 0.6–0.8 左右（种子“Say {{phrase}}”得分为 0.000）。

## 定义自定义问题

该技能包含“templates/custom_problem_template.py”——复制、编辑、运行。
您必须定义三件事：

1. **`Organism`** — 一个 Pydantic `BaseModel` 子类，包含工件
   进化（`prompt_template：str`，`regex_pattern：str`，`sql_query：str`，
   `code_block: str` 等）。添加一个“run(*args)”方法来执行它。

2. **`评估器`** — `.evaluate(organism) ->EvaluationResult(score=..., trainable_failure_cases=[...],holdout_failure_cases=[...], is_viable=True)`。
   - **`分数`**位于`[0, 1]`中。越高越好。
   - **`trainable_failure_cases`** — 变异器看到的内容。包括足够的
     供法学硕士诊断的背景（输入、预期、实际）。
   - **`holdout_failure_cases`** — 远离变异者的视野。使用这些
     来检测过度拟合。
   - **`is_viable=True`** 除非有机体完全损坏（引发，
     返回 None 等）。一个 0 分的存活有机体很好——它只是得到
     父母选择权重降低。

3. **`Mutator`** — `.mutate(organism, failure_cases,learning_log_entries) -> list[Organism]`。
   通常：构建一个 LLM 提示，其中包括当前有机体 +
   失败案例+要求提出修复方案；解析 LLM 的回复；返回
   一个新的“有机体”。解析失败时返回 `[]` — 循环会处理它。

然后编写一个连接“Problem(initial_organism, evaluator, [mutators])”的驱动程序脚本
进入 `EvolveProblemLoop` 并迭代 `loop.run(num_iterations=N)` —
附带的“scripts/parrot_openrouter.py”是参考。

## 真正重要的超参数

|旗帜|默认 |何时改变|
|---|---|---|
| `--num_iterations` | 5 |一旦您信任评估员，分数就会升至 10-20 |
| `--num_parents_per_iteration` | 4 |降低至 2 即可进行廉价探索 |
| `--mutator_concurrency` | 10 | 10降至 2-4 以避免速率限制 |
| `--evaluator_concurrency` | 10 | 10相同的;评估员也攻读了法学硕士|
| `--batch_size` | 1 |一旦你的变异器处理了多次失败，就提高到 3-5 |
| `--verify_mutations` |关闭 |一旦 mutator 浪费就打开（每次 Imbue 以后运行可节省 10 倍的成本）|
| `--midpoint_score` | `p75` |除非分数成簇，否则不要管 |
| `--清晰度` | 10 | 10独自离开|

## 陷阱

1. **`初始有机体必须是可行的`** — 在你的程序中设置 `is_viable=True`
   即使是 0 分种子，也可以使用“EvaluationResult”。循环拒绝不可行的
   有机体，因为它们意味着循环没有任何东西可以进化。
2. **提供商内容过滤器终止运行。** Azure 支持的 OpenRouter 模型
   使用 HTTP 400 拒绝诸如“忽略先前指令”之类的短语。
   LLM 在 `try/ except` 中调用并返回 `f"<LLM_ERROR: {e}>"` —
   进化者只会给该生物体评分 0 并继续前进。
3. **`loop.run()` 是一个生成器** - 调用它不会运行任何东西，直到
   你迭代。在loop.run(num_iterations=N):中使用“for snap”。
4. **快照是嵌套的pickles。** `iteration_N.pkl`包含一个字典
   `population_snapshot`（更多腌制字节）。要解封，你必须有
   “Organism”类可在腌制时的同一虚线路径下导入。
5. **并发默认值非常激进。** 10/10 将达到速率限制
   大多数提供商。从 2/2 开始。
6. **CLI 被硬编码为 Anthropic。** `uv run darwinian_evolver <问题>`
   找到“ANTHROPIC_API_KEY”并使用 Claude Sonnet。要使用任何其他
   提供者，编写一个像“parrot_openrouter.py”这样的驱动程序。
7. **AGPL.** 切勿在 OpenClaw 核心内使用“from darwinian_evolver import ...”。
   `~/.hermes/skills/...` 下的自定义驱动程序脚本是用户端的并且很好。
8. **没有PyPI包。** `pip install darwinian-evolver`会拉错
   事。始终从 GitHub 存储库安装。

## 验证

安装+鹦鹉运行后，退出代码0就足够了：

````bash
DE_DIR=~/.hermes/cache/darwinian-evolver/darwinian_evolver
ls "$DE_DIR/darwinian_evolver/lineage_visualizer.html" >/dev/null && \
cd "$DE_DIR" && uv run darwinian_evolver --help >/dev/null && \
echo“达尔文进化者：好的”
````

## 参考文献

- [Imbue 研究帖子](https://imbue.com/research/2026-02-27-darwinian-evolver/)
- [ARC-AGI-2 结果](https://imbue.com/research/2026-02-27-arc-agi-2-evolution/)
- [imbue-ai/darwinian_evolver](https://github.com/imbue-ai/darwinian_evolver) (AGPL-3.0)
- [达尔文哥德尔机器](https://arxiv.org/abs/2505.22954)
- [PromptBreeder](https://arxiv.org/abs/2309.16797)