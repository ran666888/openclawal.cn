---
sidebar_position: 12
title: "Batch Processing"
description: "Generate agent trajectories at scale — parallel processing, checkpointing, and toolset distributions"
---
# 批处理

批处理允许您并行运行数百或数千个提示的 OpenClaw 代理，生成结构化轨迹数据。这主要用于**训练数据生成** — 生成 ShareGPT 格式的轨迹，其中包含可用于微调或评估的工具使用统计数据。

## 概述

批处理运行程序 (`batch_runner.py`) 处理提示的 JSONL 数据集，通过具有工具访问权限的完整代理会话运行每个提示。每个提示都有自己的隔离环境。输出是结构化轨迹数据，具有完整的对话历史记录、工具调用统计数据和推理覆盖率指标。

## 快速入门

````bash
# 基本的批处理运行
蟒蛇batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=4

# 恢复中断的运行
蟒蛇batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --简历

# 列出可用的工具集发行版
蟒蛇batch_runner.py --list_distributions
````

:::tip 可预测的大规模成本
批处理运行会启动许多并发代理会话，每个会话都会进行模型调用和工具调用。 [Nous Portal](/user-guide/features/tool-gateway) 订阅将模型访问以及网络搜索、图像生成、TTS 和云浏览器捆绑在一份账单中 - 当您想要稳定的每轨迹成本而不需要兼顾五个供应商帐户的速率限制时，这非常有用。使用“hermes setup --portal”进行设置，然后将“--model”指向 Nous 模型。
:::

## 数据集格式

输入数据集是一个 JSONL 文件（每行一个 JSON 对象）。每个条目必须有一个“提示”字段：

````jsonl
{"prompt": "编写一个查找最长回文子串的 Python 函数"}
{“prompt”：“使用 Flask 创建 REST API 端点以进行用户身份验证”}
{“prompt”：“调试此错误：TypeError：无法解压不可迭代的 NoneType 对象”}
````

条目可以选择包括：
- `image` 或 `docker_image`：用于此提示沙箱的容器映像（适用于 Docker、Modal 和 Singularity 后端）
- `cwd`：任务终端会话的工作目录覆盖

## 配置选项

|参数|默认 |描述 |
|------------|---------|-------------|
| `--dataset_file` | （必填）| JSONL 数据集的路径 |
| `--batch_size` | （必填）|每批次提示数 |
| `--run_name` | （必填）|此运行的名称（用于输出目录和检查点）|
| `--分布` | `"默认"` |样本工具集分布 |
| `--模型` | `克劳德十四行诗-4.6` |使用型号|
| `--base_url` | `https://openrouter.ai/api/v1` | API 基本 URL |
| `--api_key` | （环境变量）|模型的 API 密钥 |
| `--max_turns` | `10` |每个提示的最大工具调用迭代次数 |
| `--num_workers` | `4` |并行工作进程 |
| `--继续` | `假` |从检查点恢复 |
| `--详细` | `假` |启用详细日志记录 |
| `--max_samples` |全部 |仅处理数据集中的前 N ​​个样本 |
| `--max_tokens` |型号默认|每个模型响应的最大令牌数 |

### 提供商路由 (OpenRouter)

|参数|描述 |
|------------|-------------|
| `--providers_allowed` |允许的以逗号分隔的提供程序（例如“anthropic,openai”）|
| `--providers_ignored` |要忽略的以逗号分隔的提供程序（例如，“together,deepinfra”）|
| `--providers_order` |以逗号分隔的首选提供商订单 |
| `--provider_sort` |按“价格”、“吞吐量”或“延迟”排序 |

### 推理控制

|参数|描述 |
|------------|-------------|
| `--reasoning_effort` |努力程度：“无”、“最低”、“低”、“中”、“高”、“xhigh” |
| `--reasoning_disabled` |完全禁用推理/思考令牌 |

### 高级选项

|参数|描述 |
|------------|-------------|
| `--ephemeral_system_prompt` |执行期间使用系统提示但未保存到轨迹 |
| `--log_prefix_chars` |在日志预览中显示的字符（默认值：100） |
| `--prefill_messages_file` |带有用于少量启动的预填充消息的 JSON 文件的路径 |

## 工具集发行版

每个提示都会从**分布**中获取一组随机采样的工具集。这确保训练数据涵盖不同的工具组合。使用“--list_distributions”查看所有可用的发行版。

在当前的实现中，分布为**每个单独的工具集**分配一个概率。采样器独立翻转每个工具集，然后保证至少启用一个工具集。这与手工编写的预建组合表不同。

## 输出格式

所有输出都转到“data/<run_name>/”：

````文本
数据/my_run/
├── trajectories.jsonl # 合并最终输出（所有批次合并）
├── batch_0.jsonl # 单个批次结果
├──batch_1.jsonl
├── ...
├── checkpoint.json # 恢复检查点
└── stats.json # 聚合工具使用统计数据
````

### 轨迹格式

`trajectories.jsonl` 中的每一行都是一个 JSON 对象：

```json
{
  “提示索引”：42，
  “对话”：[
    {"from": "人类", "value": "写一个函数..."},
    {"from": "gpt", "value": "我将创建该函数...",
     “工具调用”：[...]}，
    {"from": "工具", "value": "..."},
    {"from": "gpt", "value": "这是完成的函数..."}
  ],
  “元数据”：{
    “batch_num”：2，
    "时间戳": "2026-01-15T10:30:00",
    “模型”：“人类/克劳德-sonnet-4.6”
  },
  “完成”：真实，
  “部分”：假，
  “api_calls”：3，
  “toolsets_used”：[“终端”，“文件”]，
  “工具统计”：{
    "terminal": {"count": 2, "success": 2, "failure": 0},
    “read_file”：{“计数”：1，“成功”：1，“失败”：0}
  },
  “工具错误计数”：{
    “终端”：0，
    “读取文件”：0
  }
}
````

“conversations”字段使用类似 ShareGPT 的格式，其中包含“from”和“value”字段。工具统计数据经过标准化，包括所有可能的默认值为零的工具，确保跨条目的架构一致，以实现 HuggingFace 数据集兼容性。

## 检查点

批处理运行程序具有强大的容错检查点：

- **检查点文件：** 每批完成后保存，跟踪哪些提示索引已完成
- **基于内容的简历：** 在 `--resume` 上，运行程序会扫描现有的批处理文件并根据其实际文本内容（不仅仅是索引）匹配已完成的提示，即使数据集顺序发生变化也能进行恢复
- **失败的提示：** 只有成功完成的提示才会标记为完成 - 失败的提示将在恢复时重试
- **批量合并：** 完成后，所有批处理文件（包括之前运行的文件）都将合并到单个“trajectories.jsonl”中

### 简历如何运作

1.扫描所有`batch_*.jsonl`文件是否有完成的提示（通过内容匹配）
2. 过滤数据集以排除已完成的提示
3. 重新批处理剩余的提示
4. 仅处理剩余的提示
5. 将所有批处理文件（旧+新）合并到最终输出中

## 质量过滤

批处理运行程序应用自动质量过滤：

- **无推理过滤器：** 零次助理回合包含推理的样本（没有 `<REASONING_SCRATCHPAD>` 或本机思维标记）将被丢弃
- **损坏的条目过滤器：** 具有幻觉工具名称（不在有效工具列表中）的条目在最终合并期间被过滤掉
- **推理统计：** 跟踪整个运行中有/没有推理的转弯百分比

## 统计数据

完成后，跑步者打印综合统计数据：

- **工具使用情况：** 调用次数、每个工具的成功/失败率
- **推理覆盖率：** 助理进行推理的百分比
- **丢弃的样本：** 因缺乏推理而被过滤的样本数量
- **持续时间：** 总处理时间

统计信息也保存到“statistics.json”以进行编程分析。

## 用例

### 训练数据生成

生成不同的工具使用轨迹以进行微调：

````bash
蟒蛇batch_runner.py \
    --dataset_file=data/coding_prompts.jsonl \
    --batch_size=20 \
    --run_name=coding_v1 \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=8 \
    --分布=默认\
    --最大匝数=15
````

### 模型评估

评估模型在标准化提示中使用工具的情况：

````bash
蟒蛇batch_runner.py \
    --dataset_file=data/eval_suite.jsonl \
    --batch_size=10 \
    --run_name=eval_gpt4 \
    --model=openai/gpt-4o \
    --num_workers=4 \
    --最大匝数=10
````

### 每个提示容器镜像

对于需要特定环境的基准测试，每个提示都可以指定自己的容器镜像：

````jsonl
{"prompt": "安装 numpy 并计算 3x3 矩阵的特征值", "image": "python:3.11-slim"}
{"prompt": "编译此 Rust 程序并运行它", "image": "rust:1.75"}
{"prompt": "设置 Node.js Express 服务器", "image": "node:20-alpine", "cwd": "/app"}
````

批处理运行程序会在运行每个提示之前验证 Docker 映像是否可访问。