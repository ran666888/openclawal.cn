---
title: "Chroma — Open-source embedding database for AI applications"
sidebar_label: "Chroma"
description: "Open-source embedding database for AI applications"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 色度

用于人工智能应用的开源嵌入数据库。存储嵌入和元数据，执行矢量和全文搜索，按元数据过滤。简单的 4 功能 API。从笔记本扩展到生产集群。用于语义搜索、RAG 应用程序或文档检索。最适合本地开发和开源项目。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/chroma` 安装 |
|路径| `可选技能/mlops/色度` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `chromadb`、`句子转换器` |
|平台| linux、macos、windows |
|标签 | `RAG`、`Chroma`、`矢量数据库`、`嵌入`、`语义搜索`、`开源`、`自托管`、`文档检索`、`元数据过滤` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Chroma - 开源嵌入数据库

用于使用内存构建 LLM 应用程序的 AI 原生数据库。

## 何时使用 Chroma

**在以下情况下使用 Chroma：**
- 构建 RAG（检索增强生成）应用程序
- 需要本地/自托管矢量数据库
- 想要开源解决方案（Apache 2.0）
- 在笔记本中制作原型
- 对文档进行语义搜索
- 使用元数据存储嵌入

**指标**：
- **24,300+ GitHub star**
- **1,900+ 叉子**
- **v1.3.3**（稳定，每周发布）
- **Apache 2.0 许可证**

**使用替代方案**：
- **Pinecone**：托管云、自动扩展
- **FAISS**：纯粹的相似性搜索，无元数据
- **Weaviate**：生产 ML 原生数据库
- **Qdrant**：高性能，基于 Rust

## 快速开始

### 安装

````bash
# Python
pip 安装 chromadb

# JavaScript/TypeScript
npm 安装 chromadb @chroma-core/default-embed
````

### 基本用法（Python）

````蟒蛇
导入chromadb

# 创建客户端
客户端 = chromadb.Client()

# 创建集合
集合 = client.create_collection(name="my_collection")

# 添加文档
集合.添加(
    files=["这是文档 1", "这是文档 2"],
    元数据=[{"source": "doc1"}, {"source": "doc2"}],
    id=["id1","id2"]
）

# 查询
结果=集合.查询(
    query_texts=["有关主题的文档"],
    n_结果=2
）

打印（结果）
````

## 核心运营

### 1.创建集合

````蟒蛇
# 简单集合
集合 = client.create_collection("my_docs")

# 具有自定义嵌入功能
从 chromadb.utils 导入 embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="你的密钥",
    model_name =“文本嵌入-3-小”
）

集合 = client.create_collection(
    名称=“我的文档”，
    embedding_function = openai_ef
）

# 获取现有集合
集合 = client.get_collection("my_docs")

# 删除集合
client.delete_collection(“my_docs”)
````

### 2.添加文档

````蟒蛇
# 添加自动生成的 ID
集合.添加(
    文件=[“文件1”，“文件2”，“文件3”]，
    元数据=[
        {"source": "web", "category": "教程"},
        {“来源”：“pdf”，“页面”：5}，
        {“来源”：“api”，“时间戳”：“2025-01-01”}
    ],
    ids=["id1","id2","id3"]
）

# 添加自定义嵌入
集合.添加(
    嵌入=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    文件=[“文件1”，“文件2”]，
    id=["id1","id2"]
）
````

### 3.查询（相似度搜索）

````蟒蛇
# 基本查询
结果=集合.查询(
    query_texts=["机器学习教程"],
    n_结果=5
）

# 带过滤器的查询
结果=集合.查询(
    query_texts=["Python 编程"],
    n_结果=3，
    其中={“来源”：“网络”}
）

# 使用元数据过滤器进行查询
结果=集合.查询(
    query_texts=["高级主题"],
    其中={
        “$和”：[
            {“类别”：“教程”}，
            {“难度”：{“$gte”：3}}
        ]
    }
）

# 访问结果
print(results["documents"]) # 匹配文档列表
print(results["metadatas"]) # 每个文档的元数据
print(results["distances"]) # 相似度分数
print(results["ids"]) # 文档 ID
````

### 4. 获取文档

````蟒蛇
# 通过ID获取
文档 = 集合.get(
    id=["id1","id2"]
）

# 使用过滤器获取
文档 = 集合.get(
    其中={“类别”：“教程”}，
    限制=10
）

# 获取所有文档
文档 = 集合.get()
````

### 5.更新文档

````蟒蛇
# 更新文档内容
集合.更新(
    id=["id1"],
    document=["更新内容"],
    元数据=[{“来源”：“已更新”}]
）
````

### 6.删除文档

````蟒蛇
# 按ID删除
集合.delete(ids=["id1", "id2"])

# 使用过滤器删除
集合.删除(
    其中={“来源”：“过时”}
）
````

## 持久化存储

````蟒蛇
# 保存到磁盘
客户端 = chromadb.PersistentClient(path="./chroma_db")

集合 = client.create_collection("my_docs")
collection.add(documents=["Doc 1"], ids=["id1"])

# 数据自动持久化
# 稍后使用相同路径重新加载
客户端 = chromadb.PersistentClient(path="./chroma_db")
集合 = client.get_collection("my_docs")
````

## 嵌入函数

### 默认（句子转换器）

````蟒蛇
# 默认使用句子转换器
集合 = client.create_collection("my_docs")
# 默认型号：all-MiniLM-L6-v2
````

### 开放人工智能

````蟒蛇
从 chromadb.utils 导入 embedding_functions

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key="你的密钥",
    model_name =“文本嵌入-3-小”
）

集合 = client.create_collection(
    名称=“openai_docs”，
    embedding_function = openai_ef
）
````

### 拥抱脸

````蟒蛇
Huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key="你的密钥",
    model_name="sentence-transformers/all-mpnet-base-v2"
）

集合 = client.create_collection(
    名称=“hf_docs”，
    embedding_function=huggingface_ef
）
````

### 自定义嵌入函数

````蟒蛇
从 chromadb 导入文档、EmbeddingFunction、Embeddings

类 MyEmbeddingFunction（EmbeddingFunction）：
    def __call__(self, 输入：文档) -> 嵌入：
        # 你的嵌入逻辑
        返回嵌入

my_ef = MyEmbeddingFunction()
集合 = client.create_collection(
    名称=“自定义文档”，
    嵌入函数=my_ef
）
````

## 元数据过滤

````蟒蛇
# 精确匹配
结果=集合.查询(
    query_texts=["查询"],
    其中={“类别”：“教程”}
）

# 比较运算符
结果=集合.查询(
    query_texts=["查询"],
    其中={"page": {"$gt": 10}} # $gt, $gte, $lt, $lte, $ne
）

# 逻辑运算符
结果=集合.查询(
    query_texts=["查询"],
    其中={
        “$和”：[
            {“类别”：“教程”}，
            {“难度”：{“$lte”：3}}
        ]
    } # 另外：$or
）

# 包含
结果=集合.查询(
    query_texts=["查询"],
    其中={“tags”：{“$in”：[“python”，“ml”]}}
）
````

## 浪链集成

````蟒蛇
从 langchain_chroma 导入 Chroma
从 langchain_openai 导入 OpenAIEmbeddings
从 langchain.text_splitter 导入 RecursiveCharacterTextSplitter

# 分割文档
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
docs = text_splitter.split_documents(文档)

# 创建 Chroma 矢量存储
矢量存储 = Chroma.from_documents(
    文档=文档，
    嵌入=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
）

# 查询
结果 = vectorstore.similarity_search("机器学习", k=3)

# 作为检索器
检索器 = vectorstore.as_retriever(search_kwargs={"k": 5})
````

## LlamaIndex 集成

````蟒蛇
从 llama_index.vector_stores.chroma 导入 ChromaVectorStore
从 llama_index.core 导入 VectorStoreIndex、StorageContext
导入chromadb

# 初始化色度
db = chromadb.PersistentClient(path="./chroma_db")
集合 = db.get_or_create_collection("my_collection")

# 创建向量存储
矢量存储 = ChromaVectorStore(chroma_collection=集合)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 创建索引
索引 = VectorStoreIndex.from_documents(
    文件，
    存储上下文=存储上下文
）

# 查询
query_engine = index.as_query_engine()
response = query_engine.query("什么是机器学习？")
````

## 服务器模式

````蟒蛇
# 运行 Chroma 服务器
# 终端：chroma run --path ./chroma_db --port 8000

# 连接到服务器
导入chromadb
从 chromadb.config 导入设置

客户端 = chromadb.HttpClient(
    主机=“本地主机”，
    端口=8000，
    设置=设置（anonymized_telemetry=False）
）

# 正常使用
集合 = client.get_or_create_collection("my_docs")
````

## 最佳实践

1. **使用持久客户端** - 重启时不会丢失数据
2. **添加元数据** - 启用过滤和跟踪
3. **批量操作** - 一次添加多个文档
4. **选择正确的嵌入模型** - 平衡速度/质量
5. **使用过滤器** - 缩小搜索空间
6. **唯一ID** - 避免冲突
7. **定期备份** - 复制 chroma_db 目录
8. **监控集合大小** - 如果需要则扩大
9. **测试嵌入功能** - 确保质量
10. **使用服务器模式进行生产** - 更适合多用户

## 性能

|运营|延迟|笔记|
|------------|---------|--------|
|添加 100 个文档 | 〜1-3秒|带嵌入 |
|查询（前 10 名）| 〜50-200ms |取决于集合大小 |
|元数据过滤器 | 〜10-50ms |通过适当的索引快速 |

## 资源

- **GitHub**：https://github.com/chroma-core/chroma ⭐ 24,300+
- **文档**：https://docs.trychroma.com
- **不和谐**：https://discord.gg/MMeYNTmh3x
- **版本**：1.3.3+
- **许可证**：Apache 2.0