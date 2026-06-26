---
title: "Faiss — Facebook's library for efficient similarity search and clustering of dense vectors"
sidebar_label: "Faiss"
description: "Facebook's library for efficient similarity search and clustering of dense vectors"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#费斯

Facebook 的库，用于高效相似性搜索和密集向量聚类。支持数十亿个向量、GPU 加速和各种索引类型（Flat、IVF、HNSW）。用于快速 k-NN 搜索、大规模向量检索，或者当您需要无需元数据的纯相似性搜索时。最适合高性能应用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/faiss` 安装 |
|路径| `可选技能/mlops/faiss` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `faiss-cpu`、`faiss-gpu`、`numpy` |
|平台| linux, macOS |
|标签 | `RAG`、`FAISS`、`相似性搜索`、`矢量搜索`、`Facebook AI`、`GPU 加速`、`十亿级`、`K-NN`、`HNSW`、`高性能`、`大规模` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# FAISS - 高效相似性搜索

Facebook AI 的库，用于十亿级矢量相似性搜索。

## 何时使用 FAISS

**在以下情况下使用 FAISS：**
- 需要对大型矢量数据集（数百万/数十亿）进行快速相似性搜索
- 需要GPU加速
- 纯矢量相似性（无需元数据过滤）
- 高吞吐量、低延迟至关重要
- 嵌入的离线/批处理

**指标**：
- **31,700+ GitHub star**
- Meta/Facebook 人工智能研究
- **处理数十亿个向量**
- **C++** 与 Python 绑定

**使用替代方案**：
- **Chroma/Pinecone**：需要元数据过滤
- **Weaviate**：需要完整的数据库功能
- **烦人**：更简单，功能更少

## 快速开始

### 安装

````bash
# 仅CPU
pip 安装 faiss-cpu

# GPU 支持
pip 安装 faiss-gpu
````

### 基本用法

````蟒蛇
进口费斯
将 numpy 导入为 np

# 创建样本数据（1000个向量，128维）
d = 128
NB = 1000
向量 = np.random.random((nb, d)).astype('float32')

# 创建索引
index = faiss.IndexFlatL2(d) # L2距离
index.add(vector) # 添加向量

# 搜索
k = 5 # 找到 5 个最近邻居
查询 = np.random.random((1, d)).astype('float32')
距离，索引 = index.search(query, k)

print(f"最近邻居：{indices}")
print(f"距离：{距离}")
````

## 索引类型

### 1. Flat（精确搜索）

````蟒蛇
# L2（欧几里得）距离
索引 = faiss.IndexFlatL2(d)

# 内积（标准化后的余弦相似度）
索引 = faiss.IndexFlatIP(d)

# 最慢，最准确
````

### 2. IVF（倒置锉刀）- 快速近似

````蟒蛇
# 创建量化器
量化器 = faiss.IndexFlatL2(d)

# 具有 100 个簇的 IVF 索引
n列表=100
索引 = faiss.IndexIVFFlat(量化器, d, nlist)

# 训练数据
索引.train（向量）

# 添加向量
索引.add(向量)

# 搜索（nprobe = 要搜索的簇）
索引.nprobe = 10
距离，索引 = index.search(query, k)
````

### 3. HNSW（分层新南威尔士州）- 最佳质量/速度

````蟒蛇
# 健康新南威尔士州指数
M = 32 # 每层连接数
索引 = faiss.IndexHNSWFlat(d, M)

# 无需培训
索引.add(向量)

# 搜索
距离，索引 = index.search(query, k)
````

### 4.乘积量化 - 内存效率

````蟒蛇
# PQ 减少内存 16-32×
m = 8 # 子量化器的数量
纳比特 = 8
索引 = faiss.IndexPQ(d, m, nbits)

# 训练并添加
索引.train（向量）
索引.add(向量)
````

## 保存并加载

````蟒蛇
# 保存索引
faiss.write_index(index, "large.index")

# 加载索引
index = faiss.read_index("large.index")

# 继续使用
距离，索引 = index.search(query, k)
````

## GPU 加速

````蟒蛇
# 单 GPU
res = faiss.StandardGpuResources()
index_cpu = faiss.IndexFlatL2(d)
index_gpu = faiss.index_cpu_to_gpu(res, 0, index_cpu) # GPU 0

# 多 GPU
index_gpu = faiss.index_cpu_to_all_gpus(index_cpu)

# 比 CPU 快 10-100 倍
````

## 浪链集成

````蟒蛇
从 langchain_community.vectorstores 导入 FAISS
从 langchain_openai 导入 OpenAIEmbeddings

# 创建 FAISS 矢量存储
矢量存储 = FAISS.from_documents(docs, OpenAIEmbeddings())

# 保存
矢量store.save_local（“faiss_index”）

# 加载
矢量存储 = FAISS.load_local(
    “faiss_索引”，
    OpenAIEmbeddings(),
    allow_dangerous_deserialization=True
）

# 搜索
结果 = vectorstore.similarity_search("查询", k=5)
````

## LlamaIndex 集成

````蟒蛇
从 llama_index.vector_stores.faiss 导入 FaissVectorStore
进口费斯

# 创建FAISS索引
d = 1536
faiss_index = faiss.IndexFlatL2(d)

矢量存储 = FaissVectorStore(faiss_index=faiss_index)
````

## 最佳实践

1. **选择正确的索引类型** - <10K 为 Flat，10K-1M 为 IVF，HNSW 为质量
2. **余弦标准化** - 将 IndexFlatIP 与标准化向量结合使用
3. **使用 GPU 处理大型数据集** - 速度提高 10-100 倍
4. **保存训练过的索引** - 训练成本很高
5. **调整 nprobe/ef_search** - 平衡速度/准确性
6. **监控内存** - 大型数据集的 PQ
7. **批量查询** - 更好的 GPU 利用率

## 性能

|指数类型 |构建时间 |搜索时间 |内存|准确度|
|------------|------------|-------------|--------|---------|
|平|快|慢|高| 100% |
|体外受精|中等|快|中等| 95-99% |
|新南威尔士州 |慢|最快|高| 99% |
|质问 |中等|快|低| 90-95% |

## 资源

- **GitHub**：https://github.com/facebookresearch/faiss ⭐ 31,700+
- **维基**：https://github.com/facebookresearch/faiss/wiki
- **许可证**：麻省理工学院