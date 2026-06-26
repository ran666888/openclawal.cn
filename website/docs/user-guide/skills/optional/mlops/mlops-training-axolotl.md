---
title: "Axolotl — Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO)"
sidebar_label: "Axolotl"
description: "Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 蝾螈

Axolotl：YAML LLM 微调（LoRA、DPO、GRPO）。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/axolotl` 安装 |
|路径| `可选技能/mlops/训练/axolotl` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `axolotl`、`torch`、`transformers`、`datasets`、`peft`、`accelerate`、`deepspeed` |
|平台| linux, macOS |
|标签 | `微调`、`Axolotl`、`LLM`、`LoRA`、`QLoRA`、`DPO`、`KTO`、`ORPO`、`GRPO`、`YAML`、`HuggingFace`、`DeepSpeed`、`Multimodal` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 蝾螈技能

## 里面有什么

使用 Axolotl 微调 LLM 的专家指南 — YAML 配置、100 多个模型、LoRA/QLoRA、DPO/KTO/ORPO/GRPO、多模式支持。

根据官方文档生成的蝾螈开发的全面帮助。

## 何时使用此技能

该技能应在以下情况下触发：
- 与蝾螈一起工作
- 询问 axolotl 功能或 API
- 实施蝾螈解决方案
- 调试 axolotl 代码
- 学习蝾螈的最佳实践

## 快速参考

### 常见模式

**模式 1：** 为了验证您的训练作业是否存在可接受的数据传输速度，运行 NCCL 测试可以帮助查明瓶颈，例如：

````
./build/all_reduce_perf -b 8 -e 128M -f 2 -g 3
````

**模式 2：** 在 Axolotl yaml 中配置模型以使用 FSDP。例如：

````
fsdp_版本：2
fsdp_配置：
  卸载参数：true
  state_dict_type：FULL_STATE_DICT
  auto_wrap_policy：TRANSFORMER_BASED_WRAP
  Transformer_layer_cls_to_wrap：LlamaDecoderLayer
  reshard_after_forward：true
````

**模式 3：** context_parallel_size 应该是 GPU 总数的除数。例如：

````
上下文并行大小
````

**模式 4：** 例如： - 使用 8 个 GPU，无序列并行性：每步处理 8 个不同批次 - 使用 8 个 GPU 且 context_parallel_size=4：每步仅处理 2 个不同批次（每个批次跨 4 个 GPU） - 如果每个 GPU micro_batch_size 为 2，则全局批次大小从 16 减少到 4

````
上下文并行大小=4
````

**模式 5：** 在配置中设置 save_compressed: true 可以以压缩格式保存模型，从而： - 将磁盘空间使用量减少约 40% - 保持与 vLLM 的兼容性以加速推理 - 保持与 llmcompressor 的兼容性以进行进一步优化（例如：量化）

````
保存压缩：真
````

**模式 6：** 注意 不必将集成放置在集成文件夹中。它可以位于任何位置，只要它安装在 python 环境中的包中即可。请参阅此存储库的示例：https://github.com/axolotl-ai-cloud/diff-transformer

````
整合
````

**模式 7：** 处理单个示例和批量数据。 - 单个示例：sample['input_ids'] 是一个列表[int] - 批量数据：sample['input_ids'] 是一个列表[list[int]]

````
utils.trainer.drop_long_seq（样本，sequence_len = 2048，min_sequence_len = 2）
````

### 示例代码模式

**示例 1**（Python）：
````蟒蛇
cli.cloud.modal_.ModalCloud（配置，应用程序=无）
````

**示例 2**（Python）：
````蟒蛇
cli.cloud.modal_.run_cmd（cmd，run_folder，卷=无）
````

**示例 3**（Python）：
````蟒蛇
core.trainers.base.AxolotlTrainer(
    *_args，
    bench_data_collator=无，
    eval_data_collator=无，
    dataset_tags=无,
    **夸格斯，
）
````

**示例 4**（Python）：
````蟒蛇
core.trainers.base.AxolotlTrainer.log（日志，start_time=None）
````

**示例 5**（Python）：
````蟒蛇
Prompt_strategies.input_output.RawInputOutputPrompter()
````

## 参考文件

该技能包括“references/”中的全面文档：

- **api.md** - API 文档
- **dataset-formats.md** - 数据集格式文档
- **other.md** - 其他文档

当需要详细信息时，使用“view”来阅读特定的参考文件。

## 使用此技能

### 对于初学者
从 Getting_started 或教程参考文件开始了解基本概念。

### 对于特定功能
使用适当的类别参考文件（api、指南等）来获取详细信息。

### 代码示例
上面的快速参考部分包含从官方文档中提取的常见模式。

## 资源

###参考资料/
从官方来源摘录的有组织的文档。这些文件包含：
- 详细解释
- 带语言注释的代码示例
- 原始文档的链接
- 用于快速导航的目录

### 脚本/
在此处添加常见自动化任务的帮助程序脚本。

###资产/
在此处添加模板、样板或示例项目。

## 注释

- 该技能由官方文档自动生成
- 参考文件保留源文档的结构和示例
- 代码示例包括语言检测，以实现更好的语法突出显示
- 快速参考模式是从文档中的常见用法示例中提取的

## 更新中

要使用更新的文档刷新此技能：
1.使用相同的配置重新运行scraper
2.技能将根据最新信息进行重建