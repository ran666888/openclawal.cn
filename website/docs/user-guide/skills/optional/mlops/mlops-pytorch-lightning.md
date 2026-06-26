---
title: "Pytorch Lightning"
sidebar_label: "Pytorch Lightning"
description: "High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks system, and minimal boilerplate"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# PyTorch Lightning

具有 Trainer 类、自动分布式训练（DDP/FSDP/DeepSpeed）、回调系统和最小样板的高级 PyTorch 框架。使用相同的代码从笔记本电脑扩展到超级计算机。当您想要具有内置最佳实践的干净训练循环时使用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/pytorch-lightning` 安装 |
|路径| `可选技能/mlops/pytorch-lightning` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | “闪电”、“火炬”、“变形金刚” |
|平台| linux、macos、windows |
|标签 | `PyTorch Lightning`、`训练框架`、`分布式训练`、`DDP`、`FSDP`、`DeepSpeed`、`高级 API`、`回调`、`最佳实践`、`可扩展` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# PyTorch Lightning - 高级培训框架

## 快速开始

PyTorch Lightning 组织 PyTorch 代码以消除样板文件，同时保持灵活性。

**安装**：
````bash
pip 安装闪电
````

**将 PyTorch 转换为 Lightning**（3 个步骤）：

````蟒蛇
将闪电导入为 L
进口火炬
从火炬导入 nn
从 torch.utils.data 导入 DataLoader，数据集

# 第 1 步：定义 LightningModule（组织您的 PyTorch 代码）
类 LitModel(L.LightningModule):
    def __init__(自身，hidden_size=128):
        超级().__init__()
        self.model = nn.Sequential(
            nn.Linear(28 * 28,隐藏大小),
            ReLU(),
            nn.Linear(hidden_size, 10)
        ）

    def Training_step（自身，批次，batch_idx）：
        x, y = 批次
        y_hat = self.model(x)
        损失 = nn.function.cross_entropy(y_hat, y)
        self.log('train_loss', loss) # 自动记录到 TensorBoard
        回波损耗

    def 配置_优化器（自身）：
        返回 torch.optim.Adam(self.parameters(), lr=1e-3)

# 第2步：创建数据
train_loader = DataLoader(train_dataset,batch_size=32)

# 第 3 步：与培训师一起训练（处理其他所有事情！）
训练器 = L.Trainer(max_epochs=10, 加速器='gpu', 设备=2)
模型 = LitModel()
trainer.fit(模型, train_loader)
````

**就是这样！** 训练师手柄：
- GPU/TPU/CPU切换
- 分布式训练（DDP、FSDP、DeepSpeed）
- 混合精度（FP16、BF16）
- 梯度累积
- 检查点
- 日志记录
- 进度条

## 常用工作流程

### 工作流程 1：从 PyTorch 到 Lightning

**原始 PyTorch 代码**：
````蟒蛇
模型 = MyModel()
优化器 = torch.optim.Adam(model.parameters())
model.to('cuda')

对于范围内的纪元（max_epochs）：
    对于 train_loader 中的批次：
        批处理 = 批处理.to('cuda')
        优化器.zero_grad()
        损失=模型（批次）
        loss.backward()
        优化器.step()
````

**闪电版**：
````蟒蛇
类 LitModel(L.LightningModule):
    def __init__(自身):
        超级().__init__()
        self.model = MyModel()

    def Training_step（自身，批次，batch_idx）：
        loss = self.model(batch) # 不需要.to('cuda')！
        回波损耗

    def 配置_优化器（自身）：
        返回 torch.optim.Adam(self.parameters())

# 火车
训练器 = L.Trainer(max_epochs=10, 加速器='gpu')
trainer.fit(LitModel(), train_loader)
````

**优点**：40+线→15线，无需设备管理，自动分布式

### 工作流程 2：验证和测试

````蟒蛇
类 LitModel(L.LightningModule):
    def __init__(自身):
        超级().__init__()
        self.model = MyModel()

    def Training_step（自身，批次，batch_idx）：
        x, y = 批次
        y_hat = self.model(x)
        损失 = nn.function.cross_entropy(y_hat, y)
        self.log('train_loss', 损失)
        回波损耗

    defvalidation_step(self,batch,batch_idx):
        x, y = 批次
        y_hat = self.model(x)
        val_loss = nn.function.cross_entropy(y_hat, y)
        acc = (y_hat.argmax(dim=1) == y).float().mean()
        self.log('val_loss', val_loss)
        self.log('val_acc', acc)

    def test_step（自身，批次，batch_idx）：
        x, y = 批次
        y_hat = self.model(x)
        test_loss = nn.function.cross_entropy(y_hat, y)
        self.log('test_loss', test_loss)

    def 配置_优化器（自身）：
        返回 torch.optim.Adam(self.parameters(), lr=1e-3)

# 通过验证进行训练
训练器 = L.Trainer(max_epochs=10)
trainer.fit(模型, train_loader, val_loader)

# 测试
训练器.测试（模型，test_loader）
````

**自动功能**：
- 默认情况下，验证在每个时期运行
- 指标记录到 TensorBoard
- 基于val_loss的最佳模型检查点

### 工作流程 3：分布式训练 (DDP)

````蟒蛇
# 与单 GPU 相同的代码！
模型 = LitModel()

# 8 个具有 DDP 的 GPU（自动！）
教练 = L.Trainer(
    加速器='gpu',
    设备=8，
    Strategy='ddp' # 或 'fsdp', 'deepspeed'
）

trainer.fit(模型, train_loader)
````

**启动**：
````bash
# 单个命令，Lightning 处理剩下的事情
蟒蛇火车.py
````

**无需更改**：
- 自动数据分发
- 梯度同步
- 多节点支持（只需设置`num_nodes=2`）

### 工作流程4：监控回调

````蟒蛇
从 Lightning.pytorch.callbacks 导入 ModelCheckpoint、EarlyStopping、LearningRateMonitor

# 创建回调
检查点 = 模型检查点（
    监视器='val_loss',
    模式='分钟',
    save_top_k=3,
    filename='model-{epoch:02d}-{val_loss:.2f}'
）

早期停止 = 早期停止(
    监视器='val_loss',
    耐心=5，
    模式='分钟'
）

lr_monitor = LearningRateMonitor(logging_interval='纪元')

# 添加到训练器
教练 = L.Trainer(
    最大纪元=100，
    回调=[检查点、early_stop、lr_monitor]
）

trainer.fit(模型, train_loader, val_loader)
````

**结果**：
- 自动保存最好的 3 个模型
- 如果 5 个 epoch 没有改善则提前停止
- 将学习率记录到 TensorBoard

### 工作流程 5：学习率调度

````蟒蛇
类 LitModel(L.LightningModule):
    # ...（训练步骤等）

    def 配置_优化器（自身）：
        优化器 = torch.optim.Adam(self.parameters(), lr=1e-3)

        # 余弦退火
        调度程序 = torch.optim.lr_scheduler.CosineAnnealingLR(
            优化器，
            T_max=100，
            eta_min=1e-5
        ）

        返回{
            “优化器”：优化器，
            'lr_scheduler': {
                “调度程序”：调度程序，
                'interval': 'epoch', # 每个纪元更新
                “频率”：1
            }
        }

# 学习率自动记录！
训练器 = L.Trainer(max_epochs=100)
trainer.fit(模型, train_loader)
````

## 何时使用与替代方案

**在以下情况下使用 PyTorch Lightning：
- 想要干净、有组织的代码
- 需要生产就绪的培训循环
- 单GPU、多GPU、TPU之间切换
- 想要内置回调和日志记录
- 团队协作（标准化结构）

**主要优势**：
- **有组织**：将研究代码与工程分开
- **自动**：DDP、FSDP、DeepSpeed，带 1 条线路
- **回调**：模块化训练扩展
- **可重现**：更少的样板=更少的错误
- **经过测试**：每月下载量超过 100 万次，久经考验

**使用替代方案**：
- **加速**：对现有代码进行最少的更改，更具灵活性
- **Ray Train**：多节点编排、超参数调整
- **Raw PyTorch**：最大程度的控制，学习目的
- **Keras**：TensorFlow 生态系统

## 常见问题

**问题：损失没有减少**

检查数据和模型设置：
````蟒蛇
# 添加到training_step
def Training_step（自身，批次，batch_idx）：
    如果batch_idx == 0：
        print(f"批量形状：{batch[0].shape}")
        print(f"标签：{batch[1]}")
    损失=...
    回波损耗
````

**问题：内存不足**

减少批量大小或使用梯度累积：
````蟒蛇
教练 = L.Trainer(
    accumulate_grad_batches=4, # 有效批次=batch_size × 4
    precision='bf16' # 或者'fp16'，减少内存50%
）
````

**问题：验证未运行**

确保您通过 val_loader：
````蟒蛇
# 错误
trainer.fit(模型, train_loader)

# 正确
trainer.fit(模型, train_loader, val_loader)
````

**问题：DDP 意外生成多个进程**

Lightning 自动检测 GPU。显式设置设备：
````蟒蛇
# 首先在CPU上测试
训练器 = L.Trainer(加速器='cpu', 设备=1)

# 然后是GPU
训练器 = L.Trainer(加速器='gpu', 设备=1)
````

## 高级主题

**回调**：请参阅 [references/callbacks.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/pytorch-lightning/references/callbacks.md) 了解 EarlyStopping、ModelCheckpoint、自定义回调和回调挂钩。

**分布式策略**：有关 DDP、FSDP、DeepSpeed ZeRO 集成、多节点设置，请参阅 [references/distributed.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/pytorch-lightning/references/distributed.md)。

**超参数调整**：请参阅 [references/hyperparameter-tuning.md](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/pytorch-lightning/references/hyperparameter-tuning.md) 以了解与 Optuna、Ray Tune 和 WandB 扫描的集成。

## 硬件要求

- **CPU**：可以工作（有利于调试）
- **单 GPU**：有效
- **多 GPU**：DDP（默认）、FSDP 或 DeepSpeed
- **多节点**：DDP、FSDP、DeepSpeed
- **TPU**：支持（8 核）
- **Apple MPS**：支持

**精度选项**：
- FP32（默认）
- FP16（V100，较旧的 GPU）
- BF16（A100/H100，推荐）
- FP8（H100）

## 资源

- 文档：https://lightning.ai/docs/pytorch/stable/
- GitHub：https://github.com/Lightning-AI/pytorch-lightning ⭐ 29,000+
- 版本：2.5.5+
- 示例：https://github.com/Lightning-AI/pytorch-lightning/tree/master/examples
- 不和谐：https://discord.gg/lightning-ai
- 使用者：Kaggle 获奖者、研究实验室、生产团队