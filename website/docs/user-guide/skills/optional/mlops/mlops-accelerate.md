---
title: "Huggingface Accelerate — Simplest distributed training API"
sidebar_label: "Huggingface Accelerate"
description: "Simplest distributed training API"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 拥抱加速

最简单的分布式训练 API。 4 行即可为任何 PyTorch 脚本添加分布式支持。 DeepSpeed/FSDP/Megatron/DDP 的统一 API。自动器件贴装，混合精度（FP16/BF16/FP8）。交互式配置，单一启动命令。 HuggingFace 生态系统标准。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用“hermes Skills installficial/mlops/accelerate”安装 |
|路径| `可选技能/mlops/加速` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | “加速”、“火炬”、“变形金刚” |
|平台| linux、macos、windows |
|标签 | `分布式训练`、`HuggingFace`、`加速`、`DeepSpeed`、`FSDP`、`混合精度`、`PyTorch`、`DDP`、`统一 API`、`简单` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# HuggingFace Accelerate - 统一分布式训练

## 快速开始

Accelerate 将分布式训练简化为 4 行代码。

**安装**：
````bash
pip安装加速
````

**转换 PyTorch 脚本**（4 行）：
````蟒蛇
进口火炬
+ 从加速导入加速器

+ 加速器 = 加速器()

  模型 = torch.nn.Transformer()
  优化器 = torch.optim.Adam(model.parameters())
  dataloader = torch.utils.data.DataLoader(数据集)

+ 模型、优化器、数据加载器 = Accelerator.prepare(模型、优化器、数据加载器)

  对于数据加载器中的批处理：
      优化器.zero_grad()
      损失=模型（批次）
-loss.backward()
+加速器.向后（损失）
      优化器.step()
````

**运行**（单个命令）：
````bash
加速启动train.py
````

## 常用工作流程

### 工作流程 1：从单 GPU 到多 GPU

**原始脚本**：
````蟒蛇
# 火车.py
进口火炬

模型 = torch.nn.Linear(10, 2).to('cuda')
优化器 = torch.optim.Adam(model.parameters())
dataloader = torch.utils.data.DataLoader(数据集,batch_size=32)

对于范围（10）内的纪元：
    对于数据加载器中的批处理：
        批处理 = 批处理.to('cuda')
        优化器.zero_grad()
        损失=模型（批次）.mean（）
        loss.backward()
        优化器.step()
````

**随着加速**（添加了 4 行）：
````蟒蛇
# 火车.py
进口火炬
from 加速导入加速器 # +1

加速器 = Accelerator() # +2

模型 = torch.nn.Linear(10, 2)
优化器 = torch.optim.Adam(model.parameters())
dataloader = torch.utils.data.DataLoader(数据集,batch_size=32)

模型、优化器、数据加载器 = Accelerator.prepare(模型、优化器、数据加载器) # +3

对于范围（10）内的纪元：
    对于数据加载器中的批处理：
        # 不需要 .to('cuda') - 自动！
        优化器.zero_grad()
        损失=模型（批次）.mean（）
        Accelerator.backward(loss) # +4
        优化器.step()
````

**配置**（交互式）：
````bash
加速配置
````

**问题**：
- 哪台机器？ （单/多GPU/TPU/CPU）
- 有多少台机器？ (1)
- 混合精度？ （无/fp16/bf16/fp8）
- 深速？ （否/是）

**启动**（适用于任何设置）：
````bash
# 单 GPU
加速启动train.py

# 多 GPU（8 个 GPU）
加速启动 --multi_gpu --num_processes 8 train.py

# 多节点
加速启动 --multi_gpu --num_processes 16 \
  --num_machines 2 --machine_rank 0 \
  --main_process_ip $MASTER_ADDR \
  火车.py
````

### 工作流程 2：混合精度训练

**启用 FP16/BF16**：
````蟒蛇
从加速导入加速器

# FP16（具有梯度缩放）
加速器 = 加速器(mixed_ precision='fp16')

# BF16（无缩放，更稳定）
加速器 = 加速器(mixed_ precision='bf16')

# FP8 (H100+)
加速器 = 加速器(mixed_ precision='fp8')

模型、优化器、数据加载器 = Accelerator.prepare(模型、优化器、数据加载器)

# 其他一切都是自动的！
对于数据加载器中的批处理：
    withaccelerator.autocast(): # 可选，自动完成
        损失=模型（批次）
    Accelerator.backward(损失)
````

### 工作流程 3：DeepSpeed ZeRO 集成

**启用 DeepSpeed ZeRO-2**：
````蟒蛇
从加速导入加速器

加速器 = 加速器(
    混合精度='bf16',
    深度速度插件={
        "zero_stage": 2, # ZeRO-2
        “offload_optimizer”：错误，
        “梯度累积步骤”：4
    }
）

# 与之前相同的代码！
模型、优化器、数据加载器 = Accelerator.prepare(模型、优化器、数据加载器)
````

**或通过配置**：
````bash
加速配置
# 选择：DeepSpeed → ZeRO-2
````

**deepspeed_config.json**：
```json
{
    "fp16": {"启用": false},
    "bf16": {"启用": true},
    “零优化”：{
        “阶段”：2，
        “offload_optimizer”：{“设备”：“CPU”}，
        “allgather_bucket_size”：5e8，
        “减少桶大小”：5e8
    }
}
````

**启动**：
````bash
加速启动 --config_file deepspeed_config.json train.py
````

### 工作流程 4：FSDP（完全分片数据并行）

**启用 FSDP**：
````蟒蛇
从加速导入加速器、FullyShardedDataParallelPlugin

fsdp_plugin = FullShardedDataParallelPlugin(
    sharding_strategy="FULL_SHARD", # ZeRO-3 等效项
    auto_wrap_policy="TRANSFORMER_AUTO_WRAP",
    cpu_offload=假
）

加速器 = 加速器(
    混合精度='bf16',
    fsdp_plugin=fsdp_plugin
）

模型、优化器、数据加载器 = Accelerator.prepare(模型、优化器、数据加载器)
````

**或通过配置**：
````bash
加速配置
# 选择：FSDP → 完整分片 → 无 CPU 卸载
````

### 工作流程5：梯度累积

**累积梯度**：
````蟒蛇
从加速导入加速器

加速器 = 加速器(gradient_accumulation_steps=4)

模型、优化器、数据加载器 = Accelerator.prepare(模型、优化器、数据加载器)

对于数据加载器中的批处理：
    withaccelerator.accumulate(model): # 处理累积
        优化器.zero_grad()
        损失=模型（批次）
        Accelerator.backward(损失)
        优化器.step()
````

**有效批量大小**：`batch_size * num_gpus *gradient_accumulation_steps`

## 何时使用与替代方案

**在以下情况下使用加速**：
- 想要最简单的分布式训练
- 任何硬件都需要单个脚本
- 使用 HuggingFace 生态系统
- 需要灵活性（DDP/DeepSpeed/FSDP/Megatron）
- 需要快速原型制作

**主要优势**：
- **4 行**：最少的代码更改
- **统一 API**：DDP、DeepSpeed、FSDP、Megatron 的代码相同
- **自动**：设备放置、混合精度、分片
- **交互式配置**：无需手动启动器设置
- **单次启动**：适用于任何地方

**使用替代方案**：
- **PyTorch Lightning**：需要回调、高级抽象
- **Ray Train**：多节点编排、超参数调整
- **DeepSpeed**：直接 API 控制，高级功能
- **原始 DDP**：最大程度的控制，最小程度的抽象

## 常见问题

**问题：设备放置错误**

不要手动移动到设备：
````蟒蛇
# 错误
批处理 = 批处理.to('cuda')

# 正确
# Accelerate 在prepare()之后自动处理它
````

**问题：梯度累积不起作用**

使用上下文管理器：
````蟒蛇
# 正确
使用 Accelerator.accumulate(model)：
    优化器.zero_grad()
    Accelerator.backward(损失)
    优化器.step()
````

**问题：分布式检查点**

使用加速器方法：
````蟒蛇
# 只保存在主进程上
如果加速器.is_main_process：
    Accelerator.save_state('检查点/')

# 加载到所有进程
Accelerator.load_state('检查点/')
````

**问题：FSDP 结果不同**

确保相同的随机种子：
````蟒蛇
从 Accelerate.utils 导入 set_seed
设置种子(42)
````

## 高级主题

**Megatron 集成**：有关张量并行性、管道并行性和序列并行性设置，请参阅 [references/megatron-integration.md](https://github.com/NousResearch/openclaw/blob/main/Optional-skills/mlops/accelerate/references/megatron-integration.md)。

**自定义插件**：请参阅 [references/custom-plugins.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/accelerate/references/custom-plugins.md) 创建自定义分布式插件和高级配置。

**性能调整**：请参阅 [references/performance.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/accelerate/references/performance.md) 了解分析、内存优化和最佳实践。

## 硬件要求

- **CPU**：工作（慢）
- **单 GPU**：有效
- **多 GPU**：DDP（默认）、DeepSpeed 或 FSDP
- **多节点**：DDP、DeepSpeed、FSDP、Megatron
- **TPU**：支持
- **Apple MPS**：支持

**启动器要求**：
- **DDP**：`torch.distributed.run`（内置）
- **DeepSpeed**：`deepspeed` (pip install deepspeed)
- **FSDP**：PyTorch 1.12+（内置）
- **威震天**：自定义设置

## 资源

- 文档：https://huggingface.co/docs/accelerate
- GitHub：https://github.com/huggingface/accelerate
- 版本：1.11.0+
- 教程：“加速你的脚本”
- 示例：https://github.com/huggingface/accelerate/tree/main/examples
- 使用者：HuggingFace Transformers、TRL、PEFT、所有 HF 库