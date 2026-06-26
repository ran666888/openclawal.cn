---
title: "Heartmula — HeartMuLa: Suno-like song generation from lyrics + tags"
sidebar_label: "Heartmula"
description: "HeartMuLa: Suno-like song generation from lyrics + tags"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 心模

HeartMuLa：从歌词+标签生成类似 Suno 的歌曲。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/媒体/heartmula` |
|版本 | `1.0.0` |
|平台| linux、macos、windows |
|标签 | `音乐`、`音频`、`一代`、`ai`、`heartmula`、`heartcodec`、`歌词`、`歌曲` |
|相关技能| '音响技术' |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# HeartMuLa - 开源音乐生成

## 概述
HeartMuLa 是一系列开源音乐基础模型 (Apache-2.0)，可根据歌词和标签生成音乐，并提供多语言支持。从歌词+标签生成完整歌曲。与 Suno 的开源相当。包括：
- **HeartMuLa** - 用于从歌词 + 标签生成的音乐语言模型 (3B/7B)
- **HeartCodec** - 用于高保真音频重建的 12.5Hz 音乐编解码器
- **HeartTranscriptor** - 基于耳语的歌词转录
- **HeartCLAP** - 音频文本对齐模型

## 何时使用
- 用户想要从文本描述生成音乐/歌曲
- 用户想要一个开源 Suno 替代品
- 用户想要本地/离线音乐生成
- 用户询问 HeartMuLa、heartlib 或 AI 音乐生成

## 硬件要求
- **最低**：8GB VRAM，带有“--lazy_load true”（顺序加载/卸载模型）
- **推荐**：16GB+ VRAM 可实现舒适的单 GPU 使用
- **多 GPU**：使用 `--mula_device cuda:0 --codec_device cuda:1` 跨 GPU 分割
- 3B 模型，lazy_load 峰值约为 6.2GB VRAM

## 安装步骤

### 1.克隆存储库
````bash
cd ~/ # 或想要的目录
git 克隆 https://github.com/HeartMuLa/heartlib.git
cd 心脏库
````

### 2.创建虚拟环境（需要Python 3.10）
````bash
uv venv --python 3.10 .venv
。 .venv/bin/激活
uv pip install -e 。
````

### 3.修复依赖兼容性问题

**重要**：截至 2026 年 2 月，固定的依赖项与较新的软件包存在冲突。应用这些修复：

````bash
# 升级数据集（旧版本与当前pyarrow不兼容）
uv pip install --升级数据集

# 升级变压器（huggingface-hub 1.x 兼容性所需）
uv pip install --升级变压器
````

### 4. 补丁源代码（变形金刚 5.x 需要）

**补丁 1 - RoPE 缓存修复**在 `src/heartlib/heartmula/modeling_heartmula.py` 中：

在 `HeartMuLa` 类的 `setup_caches` 方法中，在 `reset_caches` try/ except 块之后和 `with device:` 块之前添加 RoPE 重新初始化：

````蟒蛇
# 重新初始化在元设备加载期间跳过的 RoPE 缓存
从 torchtune.models.llama3_1._position_embeddings 导入 Llama3ScaledRoPE
对于 self.modules() 中的模块：
    如果 isinstance(module, Llama3ScaledRoPE) 而不是 module.is_cache_built：
        module.rope_init()
        模块.to(设备)
````

**为什么**： `from_pretrained` 首先在元设备上创建模型； `Llama3ScaledRoPE.rope_init()` 会跳过元张量上的缓存构建，然后在权重加载到真实设备后不再重建。

**补丁 2 - HeartCodec 加载修复**在 `src/heartlib/pipelines/music_ Generation.py` 中：

将“ignore_mismatched_sizes=True”添加到所有“HeartCodec.from_pretrained()”调用中（有 2 个：“__init__”中的急切加载和“codec”属性中的延迟加载）。

**为什么**：VQ 码本“initted”缓冲区在检查点中具有形状“[1]”，而在模型中具有“[]”形状。相同的数据，只是标量与 0 维张量。可以安全地忽略。

### 5.下载模型检查点
````bash
cd heartlib # 项目根目录
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
````

所有 3 个都可以并行下载。总大小为数GB。

## GPU / CUDA

HeartMuLa 默认使用 CUDA (`--mula_device cuda --codec_device cuda`)。如果用户拥有安装了 PyTorch CUDA 支持的 NVIDIA GPU，则无需额外设置。

- 安装的 `torch==2.4.1` 包含开箱即用的 CUDA 12.1 支持
- `torchtune` 可能会报告版本 `0.4.0+cpu` — 这只是包元数据，它仍然通过 PyTorch 使用 CUDA
- 要验证 GPU 是否正在使用，请在输出中查找“CUDA 内存”行（例如“卸载前的 CUDA 内存：6.20 GB”）
- **没有 GPU？** 您可以使用 `--mula_device cpu --codec_device cpu` 在 CPU 上运行，但预计生成速度 **非常慢**（一首歌曲可能需要 30-60 分钟以上，而在 GPU 上大约需要 4 分钟）。 CPU 模式还需要大量 RAM（~12GB+ 空闲）。如果用户没有 NVIDIA GPU，建议使用云 GPU 服务（带有 T4、Lambda Labs 等的 Google Colab 免费套餐）或 https://heartmula.github.io/ 上的在线演示。

## 用法

### 基本生成
````bash
cd 心脏库
。 .venv/bin/激活
python ./examples/run_music_ Generation.py \
  --model_path=./ckpt \
  --版本=“3B”\
  --lyrics="./assets/lyrics.txt" \
  --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" \
  --lazy_load true
````

### 输入格式

**标签**（以逗号分隔，无空格）：
````
钢琴,快乐,婚礼,合成器,浪漫
````
或
````
摇滚、活力、吉他、鼓、男声
````

**歌词**（使用括号内的结构标签）：
````
[简介]

[诗句]
你的歌词在这里...

[合唱]
副歌歌词...

[桥梁]
桥的歌词...

[尾声]
````

### 关键参数
|参数|默认 |描述 |
|------------|---------|-------------|
| `--max_audio_length_ms` | 240000 |最大长度（以毫秒为单位）（240 秒 = 4 分钟）|
| `--topk` | 50| Top-k 采样 |
| `--温度` | 1.0 |取样温度|
| `--cfg_scale` | 1.5 | 1.5无分类器指导量表|
| `--lazy_load` |假 |按需加载/卸载模型（节省 VRAM）|
| `--mula_dtype` | bfloat16 | HeartMuLa 的 Dtype（推荐 bf16）|
| `--codec_dtype` |浮动32 | HeartCodec 的 Dtype（建议使用 fp32 以保证质量）|

### 性能
- RTF（实时系数）≈ 1.0 — 一首 4 分钟的歌曲需要约 4 分钟才能生成
- 输出：MP3、48kHz 立体声、128kbps

## 陷阱
1. **请勿将 bf16 用于 HeartCodec** — 会降低音频质量。使用 fp32（默认）。
2. **标签可能会被忽略** - 已知问题 (#90)。歌词往往占主导地位；尝试标签排序。
3. **Triton 在 macOS 上不可用** — Linux/CUDA 仅用于 GPU 加速。
4. **RTX 5080 不兼容** 在上游问题中报告。
5. 依赖 pin 冲突需要上述手动升级和补丁。

## 链接
- 仓库：https://github.com/HeartMuLa/heartlib
- 模特：https://huggingface.co/HeartMuLa
- 论文：https://arxiv.org/abs/2601.10547
- 许可证：Apache-2.0