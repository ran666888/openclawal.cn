---
title: "Nemo Curator — GPU-accelerated data curation for LLM training"
sidebar_label: "Nemo Curator"
description: "GPU-accelerated data curation for LLM training"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 尼莫馆长

用于 LLM 培训的 GPU 加速数据管理。支持文本/图像/视频/音频。具有模糊重复数据删除（快 16 倍）、质量过滤（30 多种启发式）、语义重复数据删除、PII 编辑、NSFW 检测。使用 RAPIDS 跨 GPU 进行扩展。用于准备高质量的训练数据集、清理 Web 数据或对大型语料库进行重复数据删除。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/nemo-curator` 安装 |
|路径| `可选技能/mlops/nemo-curator` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `nemo-curator`、`cudf`、`dask`、`rapids` |
|平台| linux, macOS |
|标签 | “数据处理”、“NeMo Curator”、“数据管理”、“GPU 加速”、“重复数据删除”、“质量过滤”、“NVIDIA”、“RAPIDS”、“PII 编辑”、“多模式”、“LLM 训练数据”|

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# NeMo Curator - GPU 加速的数据管理

NVIDIA 用于为法学硕士准备高质量训练数据的工具包。

## 何时使用 NeMo Curator

**在以下情况下使用 NeMo Curator：**
- 从网络抓取中准备 LLM 培训数据（Common Crawl）
- 需要快速重复数据删除（比 CPU 快 16 倍）
- 整理多模式数据集（文本、图像、视频、音频）
- 过滤低质量或有毒内容
- 跨 GPU 集群扩展数据处理

**性能**：
- **快 16 倍** 模糊重复数据删除 (8TB RedPajama v2)
- **与 CPU 替代品相比，TCO 降低 40%**
- **跨 GPU 节点的近线性缩放**

**使用替代方案**：
- **datatrove**：基于 CPU 的开源数据处理
- **dolma**：Allen AI 的数据工具包
- **Ray Data**：一般机器学习数据处理（无管理重点）

## 快速开始

### 安装

````bash
# 文本管理 (CUDA 12)
uv pip install“nemo-curator[text_cuda12]”

# 所有方式
uv pip install“nemo-curator[all_cuda12]”

# 仅 CPU（较慢）
uv pip install "nemo-curator[cpu]"
````

### 基本文本管理管道

````蟒蛇
从 nemo_curator 导入 ScoreFilter，修改
从 nemo_curator.datasets 导入 DocumentDataset
将 pandas 导入为 pd

# 加载数据
df = pd.DataFrame({"text": ["好文档", "坏文档", "优秀文本"]})
数据集 = 文档数据集(df)

# 质量过滤
def 质量分数（文档）：
    return len(doc["text"].split()) > 5 # 过滤短文档

过滤 = ScoreFilter(quality_score)(数据集)

# 重复数据删除
从 nemo_curator.modules 导入 ExactDuplicates
重复数据删除 = ExactDuplicates()（已过滤）

# 保存
deduped.to_parquet(“curated_data/”)
````

## 数据管理管道

### 第一阶段：质量过滤

````蟒蛇
从 nemo_curator.filters 导入 (
    字数过滤器，
    重复行过滤器，
    UrlRatio过滤器，
    非字母数字过滤器
）

# 应用 30 多个启发式过滤器
从 nemo_curator 导入 ScoreFilter

# 字数过滤器
数据集 = dataset.filter(WordCountFilter(min_words=50, max_words=100000))

# 删除重复内容
数据集 = dataset.filter(RepeatedLinesFilter(max_repeated_line_fraction=0.3))

# URL比例过滤器
数据集 = dataset.filter(UrlRatioFilter(max_url_ratio=0.2))
````

### 第 2 阶段：重复数据删除

**精确重复数据删除**：
````蟒蛇
从 nemo_curator.modules 导入 ExactDuplicates

# 删除精确的重复项
重复数据删除 = ExactDuplicates(id_field="id", text_field="text")(数据集)
````

**模糊重复数据删除**（在 GPU 上速度提高 16 倍）：
````蟒蛇
从 nemo_curator.modules 导入 FuzzyDuplicates

# MinHash + LSH去重
fuzzy_dedup = FuzzyDuplicates(
    id_field =“id”，
    文本字段=“文本”，
    num_hashes=260, # MinHash 参数
    num_buckets=20,
    hash_method =“md5”
）

去重 = fuzzy_dedup(数据集)
````

**语义重复数据删除**：
````蟒蛇
从 nemo_curator.modules 导入 SemanticDuplicates

# 基于嵌入的重复数据删除
Semantic_dedup = SemanticDuplicates(
    id_field =“id”，
    文本字段=“文本”，
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    Threshold=0.8 # 余弦相似度阈值
）

重复数据删除=semantic_dedup（数据集）
````

### 第 3 阶段：PII 修订

````蟒蛇
from nemo_curator.modules 导入 修改
从 nemo_curator.modifiers 导入 PIIRedactor

# 编辑个人身份信息
pii_redactor = PIIRedactor(
    supported_entities=["EMAIL_ADDRESS", "PHONE_NUMBER", "PERSON", "LOCATION"],
    anonymize_action="replace" # 或 "redact"
）

编辑=修改（pii_redactor）（数据集）
````

### 第 4 阶段：分类器过滤

````蟒蛇
从 nemo_curator.classifiers 导入 QualityClassifier

# 质量分类
质量_clf = 质量分类器(
    model_path="nvidia/quality-classifier-deberta",
    批量大小=256，
    设备=“cuda”
）

# 过滤低质量文档
high_quality = dataset.filter(lambda doc:quality_clf(doc["text"]) > 0.5)
````

## GPU 加速

### GPU 与 CPU 性能对比

|运营| CPU（16核）|图形处理器 (A100) |加速|
|------------|----------------|------------|---------|
|模糊重复数据删除 (8TB) | 120 小时 | 7.5 小时 | 16× |
|精确重复数据删除 (1TB) | 8小时| 0.5 小时 | 16× |
|品质过滤| 2小时| 0.2 小时 | 10× |

### 多 GPU 缩放

````蟒蛇
从 nemo_curator 导入 get_client
导入dask_cuda

# 初始化GPU集群
客户端 = get_client(cluster_type="gpu", n_workers=8)

# 使用 8 个 GPU 进行处理
重复数据删除 = FuzzyDuplicates(...)（数据集）
````

## 多模式策展

### 图像策展

````蟒蛇
从 nemo_curator.image 导入（
    审美滤镜，
    NSFW过滤器，
    夹子嵌入器
）

# 审美评分
审美过滤器 = 审美过滤器（阈值=5.0）
过滤图像 = 审美过滤器（图像数据集）

# NSFW 检测
nsfw_filter = NSFWFilter（阈值=0.9）
safe_images = nsfw_filter(filtered_images)

# 生成 CLIP 嵌入
Clip_embedder = CLIPEmbedder(model="openai/clip-vit-base-patch32")
image_embeddings = Clip_embedder(safe_images)
````

### 视频策展

````蟒蛇
从 nemo_curator.video 导入（
    场景检测器，
    剪辑提取器，
    实习生Video2Embedder
）

# 检测场景
场景检测器 = 场景检测器（阈值=27.0）
场景=场景检测器（视频数据集）

# 提取剪辑
Clip_extractor = ClipExtractor(min_duration=2.0, max_duration=10.0)
剪辑=clip_extractor（场景）

# 生成嵌入
video_embedder = InternVideo2Embedder()
video_embeddings = video_embedder(剪辑)
````

### 音频策展

````蟒蛇
从 nemo_curator.audio 导入 (
    ASR 推理，
    WER过滤器，
    持续时间过滤器
）

# ASR 转录
asr = ASRInference(model="nvidia/stt_en_fastconformer_hybrid_large_pc")
转录 = asr(audio_dataset)

# 按WER（单词错误率）过滤
wer_filter = WERFilter(max_wer=0.3)
high_quality_audio = wer_filter（转录）

# 持续时间过滤
持续时间过滤器=持续时间过滤器（最小持续时间= 1.0，最大持续时间= 30.0）
过滤音频 = 持续时间过滤器（高品质音频）
````

## 常见模式

### 网络抓取管理（普通抓取）

````蟒蛇
从 nemo_curator 导入 ScoreFilter，修改
从 nemo_curator.filters 导入 *
从 nemo_curator.modules 导入 *
从 nemo_curator.datasets 导入 DocumentDataset

# 加载普通爬取数据
数据集 = DocumentDataset.read_parquet("common_crawl/*.parquet")

# 管道
管道=[
    # 1. 质量过滤
    WordCountFilter(min_words=100, max_words=50000),
    重复线过滤器(max_repeated_line_fraction=0.2),
    SymbolToWordRatioFilter(max_symbol_to_word_ratio=0.3),
    UrlRatioFilter(max_url_ratio=0.3),

    # 2. 语言过滤
    LanguageIdentificationFilter(target_languages=["en"]),

    # 3. 重复数据删除
    精确重复（id_field =“id”，text_field =“文本”），
    FuzzyDuplicates（id_field =“id”，text_field =“text”，num_hashes = 260），

    # 4.PII 编辑
    PII编辑器(),

    # 5. NSFW 过滤
    NSFW分类器（阈值=0.8）
]

# 执行
对于管道中的阶段：
    数据集 = 阶段（数据集）

# 保存
dataset.to_parquet(“curated_common_crawl/”)
````

### 分布式处理

````蟒蛇
从 nemo_curator 导入 get_client
从 dask_cuda 导入 LocalCUDACluster

# 多GPU集群
集群 = LocalCUDACluster(n_workers=8)
客户端 = get_client(集群=集群)

# 处理大数据集
数据集 = DocumentDataset.read_parquet("s3://large_dataset/*.parquet")
重复数据删除 = FuzzyDuplicates(...)（数据集）

# 清理
客户端.close()
集群.close()
````

## 性能基准

### 模糊重复数据删除 (8TB RedPajama v2)

- **CPU（256 核）**：120 小时
- **GPU (8× A100)**：7.5 小时
- **加速**：16×

### 精确重复数据删除 (1TB)

- **CPU（64 核）**：8 小时
- **GPU (4× A100)**：0.5 小时
- **加速**：16×

### 质量过滤（100GB）

- **CPU（32 核）**：2 小时
- **GPU (2× A100)**：0.2 小时
- **加速**：10×

## 成本比较

**基于 CPU 的管理** (AWS c5.18xlarge × 10)：
- 费用：3.60 美元/小时 × 10 = 36 美元/小时
- 8TB 的时间：120 小时
- **总计**：$4,320

**基于 GPU 的管理** (AWS p4d.24xlarge × 2)：
- 费用：32.77 美元/小时 × 2 = 65.54 美元/小时
- 8TB 所需时间：7.5 小时
- **总计**：491.55 美元

**节省**：减少 89%（节省 3,828 美元）

## 支持的数据格式

- **输入**：Parquet、JSONL、CSV
- **输出**：Parquet（推荐）、JSONL
- **WebDataset**：多模式的 TAR 档案

## 用例

**生产部署**：
- NVIDIA 使用 NeMo Curator 准备 Nemotron-4 训练数据
- 精选的开源数据集：RedPajama v2、The Pile

## 参考文献

- **[过滤指南](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/nemo-curator/references/filtering.md)** - 30+质量过滤器，启发式
- **[重复数据删除指南](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/nemo-curator/references/deduplication.md)** - 精确、模糊、语义方法

## 资源

- **GitHub**：https://github.com/NVIDIA/NeMo-Curator ⭐ 500+
- **文档**：https://docs.nvidia.com/nemo-framework/user-guide/latest/datacuration/
- **版本**：0.4.0+
- **许可证**：Apache 2.0