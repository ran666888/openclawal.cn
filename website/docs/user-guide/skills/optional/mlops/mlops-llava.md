---
title: "Llava — Large Language and Vision Assistant"
sidebar_label: "Llava"
description: "Large Language and Vision Assistant"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 拉瓦

大型语言和视觉助手。实现视觉指令调整和基于图像的对话。将 CLIP 视觉编码器与 Vicuna/LLaMA 语言模型相结合。支持多轮图像聊天、可视化问答、跟随指令。用于视觉语言聊天机器人或图像理解任务。最适合对话式图像分析。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/llava` 安装 |
|路径| `可选技能/mlops/llava` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | “变形金刚”、“火炬”、“枕头” |
|平台| linux、macos、windows |
|标签 | `LLaVA`、`视觉语言`、`多模态`、`视觉问答`、`图像聊天`、`CLIP`、`Vicuna`、`会话 AI`、`指令调整`、`VQA` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# LLaVA - 大语言和视觉助手

用于对话图像理解的开源视觉语言模型。

## 何时使用 LLaVA

**使用时间：**
- 构建视觉语言聊天机器人
- 视觉问答（VQA）
- 图像描述和标题
- 多轮图像对话
- 遵循视觉指令
- 用图像记录理解

**指标**：
- **23,000+ GitHub star**
- GPT-4V级别能力（有针对性）
- Apache 2.0 许可证
- 多种模型尺寸（7B-34B 参数）

**使用替代方案**：
- **GPT-4V**：最高质量，基于 API
- **CLIP**：简单的零样本分类
- **BLIP-2**：仅适用于字幕
- **Flamingo**：研究，非开源

## 快速开始

### 安装

````bash
# 克隆存储库
git 克隆 https://github.com/haotian-liu/LLaVA
cd LLaVA

# 安装
pip install -e 。
````

### 基本用法

````蟒蛇
从 llava.model.builder 导入 load_pretrained_model
从 llava.mm_utils 导入 get_model_name_from_path、process_images、tokenizer_image_token
从llava.constants导入IMAGE_TOKEN_INDEX，DEFAULT_IMAGE_TOKEN
从 llava.conversation 导入 conv_templates
从 PIL 导入图像
进口火炬

# 加载模型
model_path = "liuhaotian/llava-v1.5-7b"
分词器、模型、图像处理器、context_len = load_pretrained_model(
    模型路径=模型路径，
    model_base=无，
    模型名称=从路径获取模型名称（模型路径）
）

# 加载图像
image = Image.open("图片.jpg")
image_tensor = process_images([图像], image_processor, model.config)
image_tensor = image_tensor.to(model.device, dtype=torch.float16)

# 创建对话
conv = conv_templates["llava_v1"].copy()
conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\n这张图片里有什么？")
conv.append_message(conv.roles[1], 无)
提示 = conv.get_prompt()

# 生成响应
input_ids = tokenizer_image_token(提示, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).to(model.device)

使用 torch.inference_mode()：
    输出_ids = model.generate(
        输入ID，
        图像=图像张量，
        do_sample=真，
        温度=0.2，
        最大新令牌=512
    ）

响应 = tokenizer.decode(output_ids[0],skip_special_tokens=True).strip()
打印（响应）
````

## 可用型号

|型号|参数|显存 |品质 |
|--------|------------|------|---------|
| LLaVA-v1.5-7B | 7B| 〜14 GB |好 |
| LLaVA-v1.5-13B | 13B | 13B 〜28 GB |更好 |
| LLaVA-v1.6-34B | 34B | 34B 〜70 GB |最佳|

````蟒蛇
# 加载不同的模型
model_7b = "刘浩天/llava-v1.5-7b"
model_13b = "刘浩天/llava-v1.5-13b"
model_34b = "刘浩天/llava-v1.6-34b"

# 较低 VRAM 的 4 位量化
load_4bit = True # 将 VRAM 减少约 4×
````

## CLI 用法

````bash
# 单图查询
python -m llava.serve.cli \
    --模型路径 liuhaotian/llava-v1.5-7b \
    --图像文件 image.jpg \
    --query“这张图片里有什么？”

# 多轮对话
python -m llava.serve.cli \
    --模型路径 liuhaotian/llava-v1.5-7b \
    --图像文件 image.jpg
# 然后以交互方式输入问题
````

## 网页用户界面（广播）

````bash
# 启动Gradio界面
python -m llava.serve.gradio_web_server \
    --模型路径 liuhaotian/llava-v1.5-7b \
    --load-4bit # 可选：减少 VRAM

# 通过http://localhost:7860访问
````

## 多轮对话

````蟒蛇
# 初始化对话
conv = conv_templates["llava_v1"].copy()

# 第 1 回合
conv.append_message(conv.roles[0], DEFAULT_IMAGE_TOKEN + "\n这张图片里有什么？")
conv.append_message(conv.roles[1], 无)
response1 =generate(conv, model, image) #“一只狗在公园里玩耍”

# 第 2 回合
conv.messages[-1][1] = response1 # 添加之前的响应
conv.append_message(conv.roles[0], "这只狗是什么品种？")
conv.append_message(conv.roles[1], 无)
响应2 =生成（转换，模型，图像）＃“金毛猎犬”

#第3回合
转换消息[-1][1] = 响应2
conv.append_message(conv.roles[0], "现在几点了？")
conv.append_message(conv.roles[1], 无)
响应3 =生成（转换，模型，图像）
````

## 常见任务

### 图像标题

````蟒蛇
问题=“详细描述这张图片。”
响应 = 询问（模型、图像、问题）
````

### 视觉问答

````蟒蛇
Question =“图中有多少人？”
响应 = 询问（模型、图像、问题）
````

### 物体检测（文本）

````蟒蛇
Question =“列出您在此图像中可以看到的所有对象。”
响应 = 询问（模型、图像、问题）
````

###场景理解

````蟒蛇
Question =“这个场景中发生了什么？”
响应 = 询问（模型、图像、问题）
````

### 文档理解

````蟒蛇
Question =“本文档的主题是什么？”
响应 = 询问（模型、文档图像、问题）
````

## 训练自定义模型

````bash
# 第 1 阶段：特征对齐（558K 图像标题对）
bash脚本/v1_5/pretrain.sh

# 第2阶段：可视化指令调优（150K指令数据）
bash 脚本/v1_5/finetune.sh
````

## 量化（减少 VRAM）

````蟒蛇
# 4 位量化
分词器、模型、图像处理器、context_len = load_pretrained_model(
    model_path="liuhaotian/llava-v1.5-13b",
    model_base=无，
    model_name=get_model_name_from_path("liuhaotian/llava-v1.5-13b"),
    load_4bit=True # 减少 VRAM ~4×
）

# 8位量化
load_8bit=True # 减少 VRAM ~2×
````

## 最佳实践

1. **从 7B 型号开始** - 质量好、可管理的 VRAM
2. **使用 4 位量化** - 显着减少 VRAM
3. **需要 GPU** - CPU 推理速度极慢
4. **清晰的提示** - 具体问题得到更好的答案
5. **多轮对话** - 维护对话上下文
6. **温度0.2-0.7** - 平衡创造力/一致性
7. **max_new_tokens 512-1024** - 详细回复
8. **批处理** - 顺序处理多个图像

## 性能

|型号|显存 (FP16) |显存（4 位）|速度（令牌/秒）|
|--------|-------------|--------------|--------------------|
| 7B| 〜14 GB | 〜4 GB | 〜20 |
| 13B | 13B 〜28 GB | 〜8 GB | 〜12 |
| 34B | 34B 〜70 GB | 〜18 GB | 〜5 |

*在 A100 GPU 上*

## 基准测试

LLaVA 在以下方面取得了有竞争力的分数：
- **VQAv2**：78.5%
- **GQA**：62.0%
- **MM-兽医**：35.4%
- **MMBench**：64.3%

## 限制

1. **幻觉** - 可能描述图像中没有的事物
2. **空间推理** - 与精确位置的斗争
3. **小文字** - 难以阅读细则
4. **对象计数** - 对于许多对象来说不精确
5. **VRAM 要求** - 需要强大的 GPU
6. **推理速度** - 比 CLIP 慢

## 与框架集成

###浪链

````蟒蛇
从 langchain.llms.base 导入 LLM

LLaVALLM 类（法学硕士）：
    def _call（自我，提示，停止=无）：
        # 自定义 LLaVA 推理
        返回响应

llm = LLaVALLM()
````

### 电台应用程序

````蟒蛇
将渐变导入为 gr

def 聊天（图像、文本、历史记录）：
    响应=ask_llava(模型、图像、文本)
    返回响应

演示 = gr.ChatInterface(
    聊天，
    extra_inputs=[gr.Image(type="pil")],
    title="LLaVA 聊天"
）
演示.launch()
````

## 资源

- **GitHub**：https://github.com/haotian-liu/LLaVA ⭐ 23,000+
- **论文**：https://arxiv.org/abs/2304.08485
- **演示**：https://llava.hliu.cc
- **模特**：https://huggingface.co/liuhaotian
- **许可证**：Apache 2.0