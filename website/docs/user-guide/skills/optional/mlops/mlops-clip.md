---
title: "Clip — OpenAI's model connecting vision and language"
sidebar_label: "Clip"
description: "OpenAI's model connecting vision and language"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 剪辑

OpenAI 连接视觉和语言的模型。实现零样本图像分类、图像文本匹配和跨模式检索。使用 4 亿个图像-文本对进行训练。用于图像搜索、内容审核或视觉语言任务，无需微调。最适合通用图像理解。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/clip` 安装 |
|路径| `可选技能/mlops/剪辑` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | “变形金刚”、“火炬”、“枕头” |
|平台| linux、macos、windows |
|标签 | “多模态”、“CLIP”、“视觉语言”、“零镜头”、“图像分类”、“OpenAI”、“图像搜索”、“跨模态检索”、“内容审核” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# CLIP - 对比语言-图像预训练

OpenAI 的模型可以从自然语言中理解图像。

## 何时使用 CLIP

**使用时间：**
- 零样本图像分类（无需训练数据）
- 图文相似度/匹配
- 语义图像搜索
- 内容审核（检测 NSFW、暴力）
- 视觉问答
- 跨模态检索（图像→文本、文本→图像）

**指标**：
- **25,300+ GitHub star**
- 在 4 亿个图像-文本对上进行训练
- 与 ImageNet 上的 ResNet-50 匹配（零样本）
- 麻省理工学院许可证

**使用替代方案**：
- **BLIP-2**：更好的字幕
- **LLaVA**：视觉语言聊天
- **分割任何东西**：图像分割

## 快速开始

### 安装

````bash
pip install git+https://github.com/openai/CLIP.git
pip 安装 torch torchvision ftfy 正则表达式 tqdm
````

### 零样本分类

````蟒蛇
进口火炬
导入剪辑
从 PIL 导入图像

# 加载模型
设备=“cuda”如果torch.cuda.is_available（）否则“cpu”
模型, 预处理 = Clip.load("ViT-B/32", device=device)

# 加载图像
image = preprocess(Image.open("photo.jpg")).unsqueeze(0).to(device)

# 定义可能的标签
text = Clip.tokenize(["一只狗", "一只猫", "一只鸟", "一辆车"]).to(device)

# 计算相似度
使用 torch.no_grad()：
    image_features = model.encode_image(图像)
    text_features = model.encode_text(text)

    # 余弦相似度
    logits_per_image, logits_per_text = 模型(图像, 文本)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# 打印结果
labels = [“一只狗”，“一只猫”，“一只鸟”，“一辆车”]
对于标签，zip 中的概率（标签，概率[0]）：
    print(f"{标签}: {prob:.2%}")
````

## 可用型号

````蟒蛇
# 型号（按尺寸排序）
型号=[
    “RN50”，#ResNet-50
    “RN101”，#ResNet-101
    "ViT-B/32", # 视觉变压器（推荐）
    "ViT-B/16", # 质量更好，速度更慢
    "ViT-L/14", # 质量最好，最慢
]

模型，预处理 = Clip.load("ViT-B/32")
````

|型号|参数|速度|品质 |
|--------|------------|--------|---------|
| RN50 | 102M |快|好 |
| ViT-B/32 | 151M |中等|更好 |
| ViT-L/14 | 428M |慢|最佳|

## 图文相似度

````蟒蛇
# 计算嵌入
image_features = model.encode_image(图像)
text_features = model.encode_text(text)

# 标准化
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)

# 余弦相似度
相似度 = (image_features @ text_features.T).item()
print(f"相似度：{相似度：.4f}")
````

## 语义图像搜索

````蟒蛇
# 索引图像
image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
图像嵌入 = []

对于 image_paths 中的 img_path：
    图像 = 预处理(Image.open(img_path)).unsqueeze(0).to(设备)
    使用 torch.no_grad()：
        嵌入 = model.encode_image(图像)
        嵌入 /= embedding.norm(dim=-1, keepdim=True)
    image_embeddings.append（嵌入）

image_embeddings = torch.cat(image_embeddings)

# 使用文本查询进行搜索
查询=“海上日落”
text_input = Clip.tokenize([查询]).to(设备)
使用 torch.no_grad()：
    text_embedding = model.encode_text(text_input)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

# 找到最相似的图像
相似度 = (text_embedding @ image_embeddings.T).squeeze(0)
top_k = 相似性.topk(3)

对于 idx，zip 中的分数（top_k.indices，top_k.values）：
    print(f"{image_paths[idx]}: {score:.3f}")
````

## 内容审核

````蟒蛇
# 定义类别
类别 = [
    “工作安全”，
    “工作不安全”，
    “暴力内容”，
    “图形内容”
]

文本 = Clip.tokenize(类别).to(设备)

# 检查图像
使用 torch.no_grad()：
    logits_per_image, _ = 模型(图像, 文本)
    概率 = logits_per_image.softmax(dim=-1)

# 获取分类
max_idx = probs.argmax().item()
max_prob = probs[0, max_idx].item()

print(f"类别：{categories[max_idx]} ({max_prob:.2%})")
````

## 批处理

````蟒蛇
# 处理多个图像
images = [预处理(Image.open(f"img{i}.jpg")) for i in range(10)]
图像 = torch.stack(images).to(device)

使用 torch.no_grad()：
    image_features = model.encode_image(图像)
    image_features /= image_features.norm(dim=-1, keepdim=True)

# 批量文本
texts = [“一只狗”、“一只猫”、“一只鸟”]
text_tokens = Clip.tokenize(texts).to(设备)

使用 torch.no_grad()：
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

# 相似度矩阵（10图像×3文本）
相似点= image_features @ text_features.T
打印(相似性.形状) # (10, 3)
````

## 与矢量数据库集成

````蟒蛇
# 将 CLIP 嵌入存储在 Chroma/FAISS 中
导入chromadb

客户端 = chromadb.Client()
集合 = client.create_collection("image_embeddings")

# 添加图像嵌入
对于 img_path，嵌入 zip(image_paths, image_embeddings)：
    集合.添加(
        嵌入=[embedding.cpu().numpy().tolist()],
        元数据=[{“路径”：img_path}]，
        ids=[img_path]
    ）

# 文本查询
查询=“日落”
text_embedding = model.encode_text(clip.tokenize([query]))
结果=集合.查询(
    query_embeddings=[text_embedding.cpu().numpy().tolist()],
    n_结果=5
）
````

## 最佳实践

1. **大多数情况下使用 ViT-B/32** - 良好的平衡
2. **标准化嵌入** - 余弦相似度所需
3. **批处理** - 更高效
4. **缓存嵌入** - 重新计算成本高昂
5. **使用描述性标签** - 更好的零样本性能
6. **推荐 GPU** - 速度提高 10-50 倍
7. **预处理图像** - 使用提供的预处理功能

## 性能

|运营|中央处理器| GPU（V100）|
|------------|-----|------------|
|图像编码|约 200 毫秒 | 〜20ms |
|文本编码| 〜50ms | 〜5毫秒|
|相似度计算| <1毫秒| <1毫秒|

## 限制

1. **不适用于细粒度任务** - 最适合广泛类别
2. **需要描述性文字** - 模糊的标签表现不佳
3. **网络数据存在偏差** - 可能存在数据集偏差
4. **无边界框** - 仅整个图像
5. **空间理解有限** - 位置/计数能力弱

## 资源

- **GitHub**：https://github.com/openai/CLIP ⭐ 25,300+
- **论文**：https://arxiv.org/abs/2103.00020
- **Colab**：https://colab.research.google.com/github/openai/clip/
- **许可证**：麻省理工学院