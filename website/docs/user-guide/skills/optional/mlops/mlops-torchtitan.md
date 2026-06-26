---
title: "Distributed Llm Pretraining Torchtitan"
sidebar_label: "Distributed Llm Pretraining Torchtitan"
description: "Provides PyTorch-native distributed LLM pretraining using torchtitan with 4D parallelism (FSDP2, TP, PP, CP)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 分布式 LLM 预训练 (Torchtitan)

使用具有 4D 并行性的 torchtitan（FSDP2、TP、PP、CP）提供 PyTorch 原生分布式 LLM 预训练。在使用 Float8、torch.compile 和分布式检查点预训练 Llama 3.1、DeepSeek V3 或自定义模型（8 到 512+ GPU）时使用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/torchtitan` 安装 |
|路径| `可选技能/mlops/torchtitan` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `火炬>=2.6.0`、`火炬泰坦>=0.2.0`、`火炬>=0.5.0` |
|平台| linux, macOS |
|标签 | `模型架构`、`分布式训练`、`TorchTitan`、`FSDP2`、`张量并行`、`管道并行`、`上下文并行`、`Float8`、`Llama`、`预训练` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# TorchTitan - PyTorch 原生分布式 LLM 预训练

## 快速开始

TorchTitan 是 PyTorch 的官方平台，用于大规模 LLM 预训练，具有可组合的 4D 并行性（FSDP2、TP、PP、CP），在 H100 GPU 上实现了 65% 以上的加速。

**安装**：
````bash
# 来自 PyPI（稳定）
pip 安装 torchtitan

# 来自源代码（最新功能，需要 PyTorch nightly）
git 克隆 https://github.com/pytorch/torchtitan
CD火炬泰坦
pip install -r 要求.txt
````

**下载分词器**：
````bash
# 从 https://huggingface.co/settings/tokens 获取 HF 令牌
python 脚本/download_hf_assets.py --repo_id meta-llama/Llama-3.1-8B --assets tokenizer --hf_token=...
````

**开始在 8 个 GPU 上进行训练**：
````bash
CONFIG_FILE =“./torchtitan/models/llama3/train_configs/llama3_8b.toml”./run_train.sh
````

## 常用工作流程

### 工作流程 1：在单节点上预训练 Llama 3.1 8B

复制此清单：

````
单节点预训练：
- [ ] 第 1 步：下载分词器
- [ ] 第 2 步：配置训练
- [ ] 第 3 步：启动培训
- [ ] 步骤 4：监控和检查点
````

**第 1 步：下载分词器**

````bash
python 脚本/download_hf_assets.py \
  --repo_id 元骆驼/Llama-3.1-8B \
  --资产标记器\
  --hf_token=YOUR_HF_TOKEN
````

**第 2 步：配置训练**

编辑或创建 TOML 配置文件：

````汤姆
# llama3_8b_custom.toml
[工作]
dump_folder =“./输出”
描述 =“Llama 3.1 8B 训练”

[型号]
名称 =“骆驼3”
味道=“8B”
hf_assets_path =“./assets/hf/Llama-3.1-8B”

[优化器]
名称 =“亚当W”
lr = 3e-4

[lr_调度程序]
热身步数 = 200

[培训]
本地批量大小 = 2
序列长度 = 8192
最大范数 = 1.0
步数 = 1000
数据集=“c4”

[并行性]
data_parallel_shard_ Degree = -1 # 使用所有 GPU 进行 FSDP

[激活检查点]
模式=“选择性”
选择性的ac_选项=“操作”

[检查点]
启用=真
文件夹=“检查点”
间隔 = 500
````

**第 3 步：启动培训**

````bash
# 单节点上有 8 个 GPU
CONFIG_FILE="./llama3_8b_custom.toml" ./run_train.sh

# 或者明确使用 torchrun
torchrun --nproc_per_node=8 \
  -m torchtitan.train \
  --job.config_file ./llama3_8b_custom.toml
````

**第 4 步：监控和检查点**

TensorBoard 日志保存到 `./outputs/tb/`：
````bash
张量板--logdir ./outputs/tb
````

### 工作流程 2：使用 SLURM 进行多节点训练

````
多节点训练：
- [ ] 步骤 1：配置规模并行度
- [ ] 步骤 2：设置 SLURM 脚本
- [ ] 第 3 步：提交作业
- [ ] 步骤 4：从检查点恢复
````

**第 1 步：配置规模并行度**

对于 256 个 GPU（32 个节点）上的 70B 模型：
````汤姆
[并行性]
data_parallel_shard_ Degree = 32 # 32个等级的FSDP
tensor_parallel_ Degree = 8 # 节点内的TP
pipeline_parallel_ Degree = 1 # 70B无PP
context_parallel_ Degree = 1 # 对于长序列增加
````

**步骤 2：设置 SLURM 脚本**

````bash
#!/bin/bash
#SBATCH --作业名称=llama70b
#SBATCH --节点=32
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8

斯伦火炬奔跑\
  --nnodes=32 \
  --nproc_per_node=8 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
  -m torchtitan.train \
  --job.config_file ./llama3_70b.toml
````

**第3步：提交作业**

````bash
sbatch multinode_trainer.slurm
````

**第 4 步：从检查点恢复**

如果配置的文件夹中存在检查点，训练将自动恢复。

### 工作流程 3：为 H100 启用 Float8 训练

Float8 在 H100 GPU 上提供 30-50% 的加速。

````
Float8 培训：
- [ ] 第 1 步：安装 torchao
- [ ] 步骤 2：配置 Float8
- [ ] 步骤 3：启动并编译
````

**第1步：安装torao**

````bash
USE_CPP=0 pip install git+https://github.com/pytorch/ao.git
````

**步骤 2：配置 Float8**

添加到您的 TOML 配置：
````汤姆
[型号]
转换器= [“量化.线性.float8”]

[量化.线性.float8]
启用_fsdp_float8_all_gather = true
precompute_float8_dynamic_scale_for_fsdp = true
filter_fqns = ["output"] # 排除输出层

[编译]
启用=真
组件= [“模型”，“损失”]
````

**第 3 步：启动并编译**

````bash
CONFIG_FILE="./llama3_8b.toml" ./run_train.sh \
  --model.converters="quantize.linear.float8" \
  --quantize.linear.float8.enable_fsdp_float8_all_gather \
  --编译.启用
````

### 工作流程 4：405B 模型的 4D 并行性

````
4D 并行性（FSDP + TP + PP + CP）：
- [ ] 第 1 步：创建种子检查点
- [ ] 步骤 2：配置 4D 并行度
- [ ] 步骤 3：在 512 GPU 上启动
````

**第 1 步：创建种子检查点**

跨 PP 阶段的一致初始化所需：
````bash
NGPU=1 CONFIG_FILE=./llama3_405b.toml ./run_train.sh \
  --checkpoint.enable \
  --checkpoint.create_seed_checkpoint \
  --parallelism.data_parallel_shard_ Degree 1 \
  --parallelism.tensor_parallel_ Degree 1 \
  --parallelism.pipeline_parallel_ Degree 1
````

**步骤 2：配置 4D 并行性**

````汤姆
[并行性]
data_parallel_shard_ Degree = 8 # FSDP
tensor_parallel_ Degree = 8 # 节点内的TP
pipeline_parallel_ Degree = 8 # 跨节点并行度
context_parallel_ Degree = 1 # 长序列的 CP

[培训]
本地批量大小 = 32
序列长度 = 8192
````

**第 3 步：在 512 GPU 上启动**

````bash
# 64 个节点 x 8 个 GPU = 512 个 GPU
srun torchrun --nnodes=64 --nproc_per_node=8 \
  -m torchtitan.train \
  --job.config_file ./llama3_405b.toml
````

## 何时使用与替代方案

**在以下情况下使用 TorchTitan：**
- 从头开始预培训法学硕士（8B 到 405B+）
- 需要 PyTorch 原生解决方案，无需第三方依赖
- 需要可组合的 4D 并行性（FSDP2、TP、PP、CP）
- 在 Float8 支持的 H100 上进行训练
- 想要与 torchtune/HuggingFace 互操作的检查点

**使用替代方案：**
- **Megatron-LM**：仅 NVIDIA 部署的最高性能
- **DeepSpeed**：更广泛的 ZeRO 优化生态系统，推理支持
- **Axolotl/TRL**：微调而不是预训练
- **LitGPT**：教育性小规模培训

## 常见问题

**问题：大型模型内存不足**

启用激活检查点并减少批量大小：
````汤姆
[激活检查点]
mode = "full" # 而不是"selective"

[培训]
本地批量大小 = 1
````

或者使用梯度累积：
````汤姆
[培训]
本地批量大小 = 1
global_batch_size = 32 # 累积梯度
````

**问题：TP 导致异步集合占用大量内存**

设置环境变量：
````bash
导出 TORCH_NCCL_AVOID_RECORD_STREAMS=1
````

**问题：Float8 训练速度不够快**

Float8 只对大型 GEMM 有利。过滤小层：
````汤姆
[量化.线性.float8]
filter_fqns = ["attention.wk", "attention.wv", "输出", "auto_filter_small_kn"]
````

**问题：并行度更改后检查点加载失败**

使用DCP的重新分片功能：
````bash
# 将分片检查点转换为单个文件
python -m torch.distributed.checkpoint.format_utils \
  dcp_to_torch 检查点/step-1000 checkpoint.pt
````

**问题：管道并行初始化**

首先创建种子检查点（请参阅工作流程 4，步骤 1）。

## 支持的型号

|型号|尺寸 |状态 |
|--------|--------|--------|
|骆驼3.1 | 8B、70B、405B |生产|
|骆驼 4 |各种|实验|
|深思V3 | 16B、236B、671B（教育部）|实验|
| GPT-OSS | 20B、120B（教育部）|实验|
|奎文3 |各种|实验|
|助焊剂|扩散|实验|

## 性能基准 (H100)

|型号| GPU |并行度| TPS/GPU |技术|
|--------|------|-------------|---------|------------|
|骆驼 8B | 8 | FSDP | 5,762 | 5,762基线|
|骆驼 8B | 8 | FSDP+编译+F​​P8 | 8,532 | 8,532 +48% |
|骆驼 70B | 256 | 256 FSDP+TP+AsyncTP | 876 | 876二维平行|
|骆驼 405B | 512 | 512 FSDP+TP+PP | 128 | 128 3D平行|

## 高级主题

**FSDP2 配置**：请参阅 [references/fsdp.md](https://github.com/NousResearch/openclaw/blob/main/Optional-skills/mlops/torchtitan/references/fsdp.md) 了解 FSDP2 与 FSDP1 的详细比较以及 ZeRO 等效项。

**Float8 训练**：请参阅 [references/float8.md](https://github.com/NousResearch/openclaw/blob/main/Optional-skills/mlops/torchtitan/references/float8.md) 了解张量与行缩放方法。

**检查点**：有关 HuggingFace 转换和异步检查点，请参阅 [references/checkpoint.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/torchtitan/references/checkpoint.md)。

**添加自定义模型**：请参阅 [references/custom-models.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/torchtitan/references/custom-models.md) 了解 TrainSpec 协议。

## 资源

- GitHub：https://github.com/pytorch/torchtitan
- 论文：https://arxiv.org/abs/2410.06511
- ICLR 2025：https://iclr.cc/virtual/2025/poster/29620
- PyTorch 论坛：https://discuss.pytorch.org/c/distributed/torchtitan/44