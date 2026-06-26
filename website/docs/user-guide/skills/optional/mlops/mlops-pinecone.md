---
title: "Pinecone — Managed vector database for production AI applications"
sidebar_label: "Pinecone"
description: "Managed vector database for production AI applications"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 松果

用于生产人工智能应用程序的托管矢量数据库。完全托管、自动扩展，具有混合搜索（密集 + 稀疏）、元数据过滤和命名空间。低延迟（<100ms p95）。用于大规模生产 RAG、推荐系统或语义搜索。最适合无服务器、托管基础设施。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/pinecone` 安装 |
|路径| `可选技能/mlops/pinecone` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `pinecone-client` |
|平台| linux、macos、windows |
|标签 | `RAG`、`Pinecone`、`矢量数据库`、`托管服务`、`无服务器`、`混合搜索`、`生产`、`自动缩放`、`低延迟`、`建议` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Pinecone - 托管矢量数据库

用于生产 AI 应用的矢量数据库。

## 何时使用松果

**使用时间：**
- 需要托管、无服务器矢量数据库
- 生产 RAG 应用
- 需要自动缩放
- 低延迟至关重要（<100ms）
- 不想管理基础设施
- 需要混合搜索（密集+稀疏向量）

**指标**：
- 完全托管的 SaaS
- 自动缩放至数十亿个向量
- **p95 延迟<100ms**
- 99.9% 正常运行时间 SLA

**使用替代方案**：
- **Chroma**：自托管、开源
- **FAISS**：离线、纯粹的相似性搜索
- **Weaviate**：自托管，具有更多功能

## 快速开始

### 安装

````bash
pip 安装 pinecone 客户端
````

### 基本用法

````蟒蛇
从 pinecone 导入 Pinecone，ServerlessSpec

# 初始化
pc = Pinecone(api_key="your-api-key")

# 创建索引
pc.create_index(
    名称=“我的索引”，
    size=1536, # 必须匹配嵌入尺寸
    metric="cosine", # 或 "euclidean", "dotproduct"
    规范=ServerlessSpec(云=“aws”，区域=“us-east-1”)
）

# 连接到索引
索引 = pc.Index("我的索引")

# 更新插入向量
索引.upsert（向量=[
    {“id”：“vec1”，“值”：[0.1，0.2，...]，“元数据”：{“类别”：“A”}}，
    {“id”：“vec2”，“值”：[0.3，0.4，...]，“元数据”：{“类别”：“B”}}
]）

# 查询
结果=索引.查询(
    向量=[0.1, 0.2, ...],
    顶部_k=5,
    include_metadata=真
）

打印（结果[“匹配”]）
````

## 核心运营

### 创建索引

````蟒蛇
# 无服务器（推荐）
pc.create_index(
    名称=“我的索引”，
    维度=1536，
    度量=“余弦”，
    规格=无服务器规格（
        cloud="aws", # 或 "gcp", "azure"
        区域=“us-east-1”
    ）
）

# 基于 Pod（以获得一致的性能）
从 pinecone 导入 PodSpec

pc.create_index(
    名称=“我的索引”，
    维度=1536，
    度量=“余弦”，
    规格=PodSpec(
        环境=“us-east1-gcp”，
        pod_type =“p1.x1”
    ）
）
````

### 更新插入向量

````蟒蛇
# 单个更新插入
索引.upsert（向量=[
    {
        “id”：“doc1”，
        "values": [0.1, 0.2, ...], # 1536 个维度
        “元数据”：{
            "text": "文档内容",
            "类别": "教程",
            “时间戳”：“2025-01-01”
        }
    }
]）

# 批量更新插入（推荐）
向量 = [
    {“id”：f“vec {i}”，“值”：嵌入，“元数据”：元数据}
    对于 i，枚举（zip（嵌入，元数据））中的（嵌入，元数据）
]

index.upsert（向量=向量，batch_size=100）
````

### 查询向量

````蟒蛇
# 基本查询
结果=索引.查询(
    向量=[0.1, 0.2, ...],
    顶部_k=10,
    include_metadata=真，
    include_values=False
）

# 具有元数据过滤功能
结果=索引.查询(
    向量=[0.1, 0.2, ...],
    顶部_k=5,
    filter={"category": {"$eq": "教程"}}
）

# 命名空间查询
结果=索引.查询(
    向量=[0.1, 0.2, ...],
    顶部_k=5,
    命名空间=“生产”
）

# 访问结果
对于结果中的匹配[“匹配”]：
    print(f"ID: {匹配['id']}")
    print(f"得分: {match['score']}")
    print(f"元数据: {match['元数据']}")
````

### 元数据过滤

````蟒蛇
# 精确匹配
过滤器= {“类别”：“教程”}

# 比较
过滤器 = {"price": {"$gte": 100}} # $gt, $gte, $lt, $lte, $ne

# 逻辑运算符
过滤器={
    “$和”：[
        {“类别”：“教程”}，
        {“难度”：{“$lte”：3}}
    ]
} # 另外：$or

# 在运算符中
过滤器 = {"tags": {"$in": ["python", "ml"]}}
````

## 命名空间

````蟒蛇
# 按命名空间分区数据
索引.upsert(
    向量=[{“id”：“vec1”，“值”：[...]}]，
    命名空间=“用户123”
）

# 查询特定命名空间
结果=索引.查询(
    向量=[...],
    命名空间=“用户123”，
    顶部_k=5
）

# 列出命名空间
统计数据=index.describe_index_stats()
print(stats['命名空间'])
````

## 混合搜索（密集+稀疏）

````蟒蛇
# 使用稀疏向量更新插入
索引.upsert（向量=[
    {
        “id”：“doc1”，
        "values": [0.1, 0.2, ...], # 密集向量
        “稀疏值”：{
            "indices": [10, 45, 123], # 代币 ID
            "values": [0.5, 0.3, 0.8] # TF-IDF 分数
        },
        “元数据”：{“文本”：“...”}
    }
]）

# 混合查询
结果=索引.查询(
    向量=[0.1, 0.2, ...],
    稀疏向量={
        “索引”：[10, 45],
        “值”：[0.5，0.3]
    },
    顶部_k=5,
    alpha=0.5 # 0=稀疏，1=密集，0.5=混合
）
````

## 浪链集成

````蟒蛇
从 langchain_pinecone 导入 PineconeVectorStore
从 langchain_openai 导入 OpenAIEmbeddings

# 创建向量存储
矢量存储 = PineconeVectorStore.from_documents(
    文档=文档，
    嵌入=OpenAIEmbeddings(),
    索引名称=“我的索引”
）

# 查询
结果 = vectorstore.similarity_search("查询", k=5)

# 使用元数据过滤器
结果 = vectorstore.similarity_search(
    “查询”，
    k=5，
    过滤器={“类别”：“教程”}
）

# 作为检索器
检索器 = vectorstore.as_retriever(search_kwargs={"k": 10})
````

## LlamaIndex 集成

````蟒蛇
从 llama_index.vector_stores.pinecone 导入 PineconeVectorStore

# 连接到松果
pc = Pinecone(api_key="your-key")
pinecone_index = pc.Index("我的索引")

# 创建向量存储
矢量存储 = PineconeVectorStore(pinecone_index=pinecone_index)

# 在 LlamaIndex 中使用
从 llama_index.core 导入 StorageContext、VectorStoreIndex

storage_context = StorageContext.from_defaults(vector_store=vector_store)
索引 = VectorStoreIndex.from_documents(文档, storage_context=storage_context)
````

## 索引管理

````蟒蛇
# 列出索引
索引 = pc.list_indexes()

# 描述索引
index_info = pc.describe_index("我的索引")
打印（索引信息）

# 获取索引统计信息
统计数据=index.describe_index_stats()
print(f"向量总数：{stats['total_vector_count']}")
print(f"命名空间: {stats['namespaces']}")

# 删除索引
pc.delete_index("我的索引")
````

## 删除向量

````蟒蛇
# 根据ID删除
index.delete(ids=["vec1", "vec2"])

# 通过过滤器删除
index.delete(filter={"category": "old"})

# 删除命名空间中的所有内容
index.delete(delete_all=True, 命名空间=“测试”)

# 删除整个索引
索引.删除(delete_all=True)
````

## 最佳实践

1. **使用无服务器** - 自动扩展，经济高效
2. **批量更新插入** - 更高效（每批100-200）
3. **添加元数据** - 启用过滤
4. **使用命名空间** - 按用户/租户隔离数据
5. **监控使用情况** - 检查 Pinecone 仪表板
6. **优化过滤器** - 索引经常过滤的字段
7. **使用免费套餐进行测试** - 1 个索引，免费 100K 个向量
8. **使用混合搜索** - 更好的质量
9. **设置适当的尺寸** - 匹配嵌入模型
10. **定期备份** - 导出重要数据

## 性能

|运营|延迟|笔记|
|------------|---------|--------|
|更新插入 | 〜50-100ms |每批次|
|查询（第 50 页）| 〜50ms |取决于索引大小 |
|查询（第 95 页）|约 100 毫秒 | SLA 目标 |
|元数据过滤器 | ~+10-20ms |额外开销|

## 定价（截至 2025 年）

**无服务器**：
- 每百万读取单位 0.096 美元
- 每百万写入单元 0.06 美元
- 每 GB 存储每月 0.06 USD

**免费套餐**：
- 1 个无服务器索引
- 100K 个向量（1536 维）
- 非常适合原型制作

## 资源

- **网站**：https://www.pinecone.io
- **文档**：https://docs.pinecone.io
- **控制台**：https://app.pinecone.io
- **定价**：https://www.pinecone.io/pricing