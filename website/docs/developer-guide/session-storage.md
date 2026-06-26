# 会话存储

OpenClaw 使用 SQLite 数据库（`~/.hermes/state.db`）来保存会话
跨 CLI 和网关的元数据、完整消息历史记录和模型配置
会议。这取代了早期的每会话 JSONL 文件方法。

源文件：`hermes_state.py`


## 架构概述

````
~/.hermes/state.db（SQLite，WAL 模式）
├── 会话 — 会话元数据、令牌计数、计费
├── messages — 每个会话的完整消息历史记录
├── messages_fts — FTS5 虚拟表（内容 + 工具名称 + 工具调用）
├── messages_fts_trigram — 带 trigram tokenizer 的 FTS5 虚拟表（CJK / 子字符串搜索）
├── state_meta — 键/值元数据表
└── schema_version — 跟踪迁移状态的单行表
````

关键设计决策：
- **WAL 模式** 用于并发读取器 + 一个写入器（网关多平台）
- **FTS5 虚拟表** 用于跨所有会话消息进行快速文本搜索
- **会话沿袭**通过`parent_session_id`链（压缩触发的分割）
- **来源标记**（`cli`、`telegram`、`discord` 等）用于平台过滤
- Batch runner 和 RL 轨迹不存储在这里（单独的系统）


## SQLite 架构

### 会话表

``sql
如果不存在则创建表会话（
    id 文本主键，
    源文本不为空，
    用户 ID 文本，
    模型文本，
    模型配置文本，
    系统提示文本，
    父会话 ID 文本，
    开始于 REAL NOT NULL，
    结束于 REAL，
    结束原因文本，
    message_count 整数 默认 0,
    tool_call_count 整数 默认 0，
    input_tokens 整数 默认 0,
    output_tokens 整数 默认 0,
    cache_read_tokens 整数 默认 0,
    cache_write_tokens 整数 默认 0,
    Reasoning_tokens 整数 默认 0，
    billing_provider 文本，
    billing_base_url 文本，
    计费模式文本，
    估计成本美元真实，
    实际成本美元 REAL,
    成本状态文本，
    成本源文本，
    定价版本文本，
    标题文本，
    api_call_count 整数 默认 0,
    外键（parent_session_id）参考会话（id）
）；

如果不存在则创建索引 idx_sessions_source ON 会话（源）；
如果不存在则创建索引 idx_sessions_parent ON 会话(parent_session_id);
如果不存在则创建索引 idx_sessions_started ON 会话(started_at DESC);
如果不存在则创建唯一索引 idx_sessions_title_unique
    ON 会话（标题），其中标题不为空；
````

### 消息表

``sql
如果不存在则创建表消息（
    id 整数主键自动增量，
    session_id TEXT NOT NULL 参考会话（id），
    角色 TEXT NOT NULL,
    内容文本，
    tool_call_id 文本，
    工具调用文本，
    工具名称文本，
    时间戳 REAL NOT NULL,
    token_count INTEGER，
    完成原因文本，
    推理文本，
    推理内容文本，
    推理细节文本，
    codex_reasoning_items 文本，
    codex_message_items 文本
）；

如果不存在则创建索引 idx_messages_session ON messages(session_id, timestamp);
````

注意事项：
- `tool_calls` 存储为 JSON 字符串（工具调用对象的序列化列表）
- `reasoning_details`、`codex_reasoning_items` 和 `codex_message_items` 存储为 JSON 字符串
- “reasoning”为公开它的提供者存储原始推理文本
- 时间戳是 Unix 纪元浮点数 (`time.time()`)

### FTS5 全文搜索

``sql
如果不存在则创建虚拟表 messages_fts 使用 fts5(
    内容，
    内容=消息，
    内容_rowid=id
）；
````

FTS5 表通过在 INSERT、UPDATE、
并删除“messages”表：

``sql
如果不存在则创建触发器 messages_fts_insert AFTER INSERT ON messages BEGIN
    插入 messages_fts(rowid, content) VALUES (new.id, new.content);
结尾;

如果不存在则创建触发器 messages_fts_delete AFTER DELETE ON messages BEGIN
    插入 messages_fts(messages_fts, rowid, 内容)
        VALUES('删除', old.id, old.content);
结尾;

如果不存在则创建触发器 messages_fts_update 消息更新后开始
    插入 messages_fts(messages_fts, rowid, 内容)
        VALUES('删除', old.id, old.content);
    插入 messages_fts(rowid, content) VALUES (new.id, new.content);
结尾;
````


## 架构版本和迁移

当前架构版本：**11**

“schema_version”表存储单个整数。简单的列添加由“_reconcile_columns()”以声明方式处理（它将活动列与“SCHEMA_SQL”进行比较，并添加任何缺失的列）。版本控制链保留用于无法以声明方式表达的数据迁移和索引/FTS 更改：

|版本 |改变 |
|---------|--------|
| 1 |初始模式（会话、消息、FTS5）|
| 2 |将“finish_reason”列添加到消息 |
| 3 |将“标题”列添加到会话 |
| 4 |在 `title` 上添加唯一索引（允许 NULL，非 NULL 必须是唯一的）|
| 5 |添加计费列：`cache_read_tokens`、`cache_write_tokens`、`reasoning_tokens`、`billing_provider`、`billing_base_url`、`billing_mode`、`estimated_cost_usd`、`actual_cost_usd`、`cost_status`、`cost_source`、`pricing_version` |
| 6 |向消息添加推理列：`reasoning`、`reasoning_details`、`codex_reasoning_items` |
| 7 |将 `reasoning_content` 列添加到消息 |
| 8 |将 `api_call_count` 列添加到会话 |
| 9 |将 `codex_message_items` 列添加到 Codex 响应消息 ID/阶段重放的消息中 |
| 10 | 10添加 `messages_fts_trigram` 虚拟表（用于 CJK/子字符串搜索的 trigram 分词器）并回填现有行 |
| 11 | 11重新索引 `messages_fts` 和 `messages_fts_trigram` 以覆盖 `tool_name` + `tool_calls` 并从外部内容切换到内联模式；删除旧触发器并回填每个消息行 |

声明性列添加使用包含在 try/ except 中的 ALTER TABLE ADD COLUMN 来处理列已存在的情况（幂等）。每个成功的迁移块后版本号都会增加。


## 编写争用处理

多个hermes进程（网关+CLI会话+工作树代理）共享一个
`状态.db`。 `SessionDB` 类通过以下方式处理写入争用：

- **短 SQLite 超时**（1 秒）而不是默认的 30 秒
- **应用程序级重试**，具有随机抖动（20-150ms，最多 15 次重试）
- **立即开始**事务在事务开始时表面锁定争用
- **定期 WAL 检查点** 每 50 次成功写入（被动模式）

这避免了 SQLite 确定性内部退避的“护航效应”
导致所有竞争写入器以相同的时间间隔重试。

````
_WRITE_MAX_RETRIES = 15
_WRITE_RETRY_MIN_S = 0.020 # 20ms
_WRITE_RETRY_MAX_S = 0.150 # 150ms
_CHECKPOINT_EVERY_N_WRITES = 50
````


## 常用操作

### 初始化

````蟒蛇
从 Hermes_state 导入 SessionDB

db = SessionDB() # 默认值：~/.hermes/state.db
db = SessionDB(db_path=Path("/tmp/test.db")) # 自定义路径
````

### 创建和管理会话

````蟒蛇
# 创建一个新会话
db.create_session(
    session_id =“sess_abc123”，
    来源=“cli”，
    模型=“人类/克劳德-sonnet-4.6”，
    user_id="user_1",
    Parent_session_id=None, # 或之前的血统会话 ID
）

# 结束会话
db.end_session("sess_abc123", end_reason="user_exit")

# 重新打开会话（清除结束时间/结束原因）
db.reopen_session("sess_abc123")
````

### 存储消息

````蟒蛇
msg_id = db.append_message(
    session_id =“sess_abc123”，
    角色=“助理”，
    content="这是答案...",
    tool_calls=[{"id": "call_1", "function": {"name": "terminal", "arguments": "{}"}}],
    token_count=150,
    finish_reason=“停止”，
    Reasoning="让我考虑一下......",
）
````

### 检索消息

````蟒蛇
# 包含所有元数据的原始消息
消息 = db.get_messages("sess_abc123")

# OpenAI 对话格式（用于 API 重放）
对话 = db.get_messages_as_conversation("sess_abc123")
# 返回：[{"role": "user", "content": "..."}, {"role": "assistant", ...}]
````

### 会议标题

````蟒蛇
# 设置一个标题（非NULL标题中必须是唯一的）
db.set_session_title("sess_abc123", "修复 Docker 构建")

# 按标题解析（返回谱系中最新的）
session_id = db.resolve_session_by_title("修复 Docker 构建")

# 自动生成谱系中的下一个标题
next_title = db.get_next_title_in_lineage("修复 Docker 构建")
# 返回：“修复 Docker 版本 #2”
````


## 全文搜索

`search_messages()` 方法支持 FTS5 查询语法，并自动
用户输入的净化。

### 基本搜索

````蟒蛇
结果 = db.search_messages("docker 部署")
````

### FTS5 查询语法

|语法 |示例|意义|
|--------|---------|---------|
|关键词| `docker 部署` |两个术语（隐式 AND）|
|引用的短语 | `“准确的短语”` |精确词组匹配 |
|布尔或| `docker 或 kubernetes` |任一术语 |
|布尔非 | `python 不是 java` |排除术语 |
|前缀 | `部署*` |前缀匹配|

### 过滤搜索

````蟒蛇
# 仅搜索 CLI 会话
结果= db.search_messages（“错误”，source_filter = [“cli”]）

# 排除网关会话
结果 = db.search_messages("bug", except_sources=["telegram", "discord"])

# 只搜索用户消息
结果= db.search_messages（“帮助”，role_filter = [“用户”]）
````

### 搜索结果格式

每个结果包括：
- `id`、`session_id`、`角色`、`时间戳`
- `snippet` — FTS5 生成的带有 `>>>match<<<` 标记的片段
- `context` — 比赛前后各 1 条消息（内容被截断为 200 个字符）
- `source`、`model`、`session_started` — 来自父会话

`_sanitize_fts5_query()` 方法处理边缘情况：
- 删除不匹配的引号和特殊字符
- 将连字符括在引号中（`chat-send`→`"chat-send"`）
- 删除悬空布尔运算符（`hello AND`→`hello`）


## 会话沿袭

会话可以通过“parent_session_id”形成链。当上下文发生这种情况
压缩会触发网关中的会话分裂。

### 查询：查找会话沿袭

``sql
-- 查找会话的所有祖先
具有递归谱系 AS (
    SELECT * FROM 会话 WHERE id = ?
    联合所有
    SELECT s.* FROM 会话 s
    JOIN 谱系 l ON s.id = l.parent_session_id
）
从谱系中选择 id、标题、start_at、parent_session_id；

-- 查找会话的所有后代
带有递归后代 AS (
    SELECT * FROM 会话 WHERE id = ?
    联合所有
    SELECT s.* FROM 会话 s
    JOIN 后代 d ON s.parent_session_id = d.id
）
SELECT id、title、start_at FROM 后代；
````

### 查询：带预览的最近会话

``sql
选择 s.*,
    合并(
        (选择 SUBSTR(m.content, 1, 63)
         FROM 消息 m
         其中 m.session_id = s.id AND m.role = 'user' AND m.content 不为空
         按 m.timestamp、m.id LIMIT 1) 排序，
        ”
    ) 作为预览，
    合并(
        （从消息 m2 中选择 MAX(m2.timestamp)，其中 m2.session_id = s.id），
        s.started_at
    ) AS 最后活动
FROM 会话
ORDER BY s.started_at DESC
限制 20；
````

### 查询：代币使用统计

``sql
-- 按型号划分的总代币
选择型号，
       COUNT(*) 作为会话计数，
       SUM(input_tokens) 作为total_input，
       SUM(output_tokens) 作为total_output，
       SUM(estimated_cost_usd) 作为total_cost
来自会话
WHERE 模型不为空
按模型分组
ORDER BY 总成本 DESC;

-- 令牌使用率最高的会话
选择 id、标题、型号、输入令牌 + 输出令牌 AS 总令牌，
       估计成本美元
来自会话
按total_tokens DESC排序
限制 10；
````


## 导出和清理

````蟒蛇
# 导出包含消息的单个会话
数据 = db.export_session("sess_abc123")

# 将所有会话（带有消息）导出为字典列表
all_data = db.export_all(源=“cli”)

# 删除旧会话（仅删除已结束的会话）
已删除计数 = db.prune_sessions(older_than_days=90)
已删除计数 = db.prune_sessions(older_than_days=30, 源=“电报”)

# 清除消息但保留会话记录
db.clear_messages(“sess_abc123”)

# 删除会话和所有消息
db.delete_session("sess_abc123")
````


## 数据库位置

默认路径：`~/.hermes/state.db`

这是从 `hermes_constants.get_hermes_home()` 派生出来的，它解析为
默认为`~/.hermes/`，或者`HERMES_HOME`环境变量的值。

数据库文件、WAL 文件（`state.db-wal`）和共享内存文件
(`state.db-shm`) 全部创建在同一目录中。