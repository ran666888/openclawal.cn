---
title: "Whisper — OpenAI's general-purpose speech recognition model"
sidebar_label: "Whisper"
description: "OpenAI's general-purpose speech recognition model"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 耳语

OpenAI 的通用语音识别模型。支持99种语言、转录、翻译成英文、语言识别。六种模型大小，从小（39M 参数）到大（1550M 参数）。用于语音转文本、播客转录或多语言音频处理。最适合强大的多语言 ASR。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/whisper` 安装 |
|路径| `可选技能/mlops/耳语` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `openai-whisper`、`变形金刚`、`火炬` |
|平台| linux, macOS |
|标签 | “耳语”、“语音识别”、“ASR”、“多模式”、“多语言”、“OpenAI”、“语音转文本”、“转录”、“翻译”、“音频处理” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Whisper - 强大的语音识别

OpenAI 的多语言语音识别模型。

## 何时使用耳语

**使用时间：**
- 语音转文本（99 种语言）
- 播客/视频转录
- 会议笔记自动化
- 翻译成英文
- 嘈杂的音频转录
- 多语言音频处理

**指标**：
- **72,900+ GitHub star**
- 支持 99 种语言
- 经过 680,000 小时的音频训练
- 麻省理工学院许可证

**使用替代方案**：
- **AssemblyAI**：托管 API、说话者分类
- **Deepgram**：实时流式 ASR
- **Google 语音转文本**：基于云

## 快速开始

### 安装

````bash
# 需要Python 3.8-3.11
pip install -U openai-whisper

# 需要 ffmpeg
# macOS：brew 安装 ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: choco 安装 ffmpeg
````

### 基本转录

````蟒蛇
进口耳语

# 加载模型
模型 = 耳语.load_model("基础")

# 转录
结果 = model.transcribe("audio.mp3")

# 打印文本
打印（结果[“文本”]）

# 访问段
对于结果中的段[“段”]：
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
````

## 型号尺寸

````蟒蛇
# 可用型号
型号 = [“小型”、“基础”、“小”、“中”、“大”、“涡轮”]

# 加载具体模型
model = Whisper.load_model("turbo") # 最快，质量好
````

|型号|参数|仅英语 |多语言 |速度|显存 |
|--------|------------|--------------|--------------|--------|------|
|微小| 39M | ✓ | ✓ | 〜32x | 〜1 GB |
|基地| 74M | ✓ | ✓ | 〜16x | 〜1 GB |
|小| 244M| ✓ | ✓ | 〜6x | 〜2 GB |
|中等| 769M | ✓ | ✓ | 〜2x | 〜5 GB |
|大| 1550M | ✗ | ✓ | 1x | 〜10 GB |
|涡轮| 809M | ✗ | ✓ | 〜8x | 〜6 GB |

**建议**：使用“turbo”获得最佳速度/质量，使用“base”进行原型设计

## 转录选项

### 语言规范

````蟒蛇
# 自动检测语言
结果 = model.transcribe("audio.mp3")

# 指定语言（更快）
结果 = model.transcribe("audio.mp3", language="en")

# 支持：en、es、fr、de、it、pt、ru、ja、ko、zh 等 89 种
````

### 任务选择

````蟒蛇
# 转录（默认）
结果 = model.transcribe("audio.mp3", task="transcribe")

# 翻译成英文
结果= model.transcribe（“西班牙语.mp3”，任务=“翻译”）
# 输入：西班牙语音频 → 输出：英语文本
````

### 初始提示

````蟒蛇
# 提高上下文的准确性
结果 = model.transcribe(
    “音频.mp3”，
    initial_prompt="这是一个关于机器学习和人工智能的技术播客。"
）

# 帮助：
# - 技术术语
# - 专有名词
# - 特定领域词汇
````

### 时间戳

````蟒蛇
# 字级时间戳
结果 = model.transcribe("audio.mp3", word_timestamps=True)

对于结果中的段[“段”]：
    对于段[“words”]中的单词：
        print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")
````

### 温度回落

````蟒蛇
# 如果置信度较低，则用不同的温度重试
结果 = model.transcribe(
    “音频.mp3”，
    温度=(0.0,0.2,0.4,0.6,0.8,1.0)
）
````

## 命令行使用

````bash
# 基本转录
耳语音频.mp3

# 指定型号
耳语音频.mp3 --model Turbo

# 输出格式
耳语audio.mp3 --output_format txt # 纯文本
耳语audio.mp3 --output_format srt # 字幕
耳语音频.mp3 --output_format vtt # WebVTT
耳语audio.mp3 --output_format json # 带时间戳的JSON

# 语言
耳语音频.mp3 --语言 西班牙语

# 翻译
耳语西班牙语.mp3 --任务翻译
````

## 批处理

````蟒蛇
导入操作系统

audio_files = ["文件1.mp3", "文件2.mp3", "文件3.mp3"]

对于audio_files中的audio_file：
    print(f"正在转录 {audio_file}...")
    结果 = model.transcribe(audio_file)

    # 保存到文件
    输出文件 = audio_file.replace(".mp3", ".txt")
    将 open(output_file, "w") 作为 f：
        f.write(结果[“文本”])
````

## 实时转录

````蟒蛇
# 对于流音频，请使用 fast-whisper
# pip 安装 fast-whisper

从 fast_whisper 导入 WhisperModel

模型= WhisperModel（“基础”，设备=“cuda”，compute_type=“float16”）

# 使用流式传输进行转录
片段，info = model.transcribe（“audio.mp3”，beam_size = 5）

对于段中的段：
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
````

## GPU 加速

````蟒蛇
进口耳语

# 如果可用的话自动使用 GPU
模型 = 耳语.load_model("涡轮")

# 强制CPU
模型 = 耳语.load_model("turbo", device="cpu")

# 强制 GPU
模型 = 耳语.load_model("turbo", device="cuda")

# GPU 上速度提高 10-20 倍
````

## 与其他工具集成

### 字幕生成

````bash
# 生成SRT字幕
耳语视频.mp4 --output_format srt --语言 英语

# 输出：视频.srt
````

### 与浪链一起

````蟒蛇
从 langchain.document_loaders 导入 WhisperTranscriptionLoader

加载器 = WhisperTranscriptionLoader(file_path="audio.mp3")
文档 = loader.load()

# 在 RAG 中使用转录
从 langchain_chroma 导入 Chroma
从 langchain_openai 导入 OpenAIEmbeddings

矢量存储 = Chroma.from_documents(docs, OpenAIEmbeddings())
````

### 从视频中提取音频

````bash
# 使用ffmpeg提取音频
ffmpeg -i video.mp4 -vn -acodec pcm_s16le 音频.wav

# 然后转录
耳语音频.wav
````

## 最佳实践

1. **使用涡轮模式** - 英语的最佳速度/质量
2. **指定语言** - 比自动检测更快
3. **添加初始提示** - 改进技术术语
4. **使用 GPU** - 速度提高 10-20 倍
5. **批处理** - 更高效
6. **转换为WAV** - 更好的兼容性
7. **分割长音频** - <30 分钟的块
8. **检查语言支持** - 质量因语言而异
9. **使用faster-whisper** - 比 openai-whisper 快 4 倍
10. **监控 VRAM** - 根据硬件缩放模型大小

## 性能

|型号|实时因素（CPU）|实时因素（GPU）|
|--------|------------------------------------|------------------------|
|微小| 〜0.32 | 〜0.01 |
|基地| 〜0.16 | 〜0.01 |
|涡轮| 〜0.08 | 〜0.01 |
|大| 〜1.0 | 〜0.05 |

*实时系数：0.1 = 比实时快 10 倍*

## 语言支持

最受支持的语言：
- 英语（en）
- 西班牙语（西班牙文）
- 法语（fr）
- 德语 (de)
- 意大利语（它）
- 葡萄牙语（pt）
- 俄语 (ru)
- 日语 (ja)
- 韩语 (ko)
- 中文（zh）

完整列表：总共 99 种语言

## 限制

1. **幻觉** - 可能会重复或发明文字
2. **长篇准确性** - 在超过 30 分钟的音频上性能下降
3. **说话人识别** - 无二值化
4. **口音** - 质量参差不齐
5. **背景噪音** - 会影响准确性
6. **实时延迟** - 不适合实时字幕

## 资源

- **GitHub**：https://github.com/openai/whisper ⭐ 72,900+
- **论文**：https://arxiv.org/abs/2212.04356
- **模型卡**：https://github.com/openai/whisper/blob/main/model-card.md
- **Colab**：在仓库中可用
- **许可证**：麻省理工学院