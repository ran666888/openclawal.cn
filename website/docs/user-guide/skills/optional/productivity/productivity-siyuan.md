---
title: "Siyuan"
sidebar_label: "Siyuan"
description: "SiYuan Note API for searching, reading, creating, and managing blocks and documents in a self-hosted knowledge base via curl"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#思源

思源笔记API，用于通过curl在自托管知识库中搜索、阅读、创建和管理块和文档。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/productivity/siyuan` 安装 |
|路径| `可选技能/生产力/思源` |
|版本 | `1.0.0` |
|作者 |费阿祖尔 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `思源`、`笔记`、`知识库`、`PKM`、`API` |
|相关技能| [`黑曜石`](/docs/user-guide/skills/bundled/note-take/note-take-obsidian)，[`notion`](/docs/user-guide/skills/bundled/productivity/productivity-notion) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 思源笔记API

通过curl使用[SiYuan](https://github.com/siyuan-note/siyuan)内核API来搜索、读取、创建、更新和删除自托管知识库中的块和文档。不需要额外的工具——只需curl 和API 令牌。

## 先决条件

1.安装并运行思源（桌面或Docker）
2. 获取您的 API 令牌：**设置 > 关于 > API 令牌**
3. 将其存储在`${HERMES_HOME:-~/.hermes}/.env`中：
   ````
   SIYUAN_TOKEN=your_token_here
   SIYUAN_URL=http://127.0.0.1:6806
   ````
   如果未设置，“SIYUAN_URL”默认为“http://127.0.0.1:6806”。

## API 基础知识

所有思源 API 调用都是 **POST with JSON body**。每个请求都遵循以下模式：

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/..." \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{“参数”：“值”}'
````

响应是具有以下结构的 JSON：
```json
{“代码”：0，“消息”：“”，“数据”：{...}}
````
‘代码：0’表示成功。任何其他值都是错误 - 检查“msg”了解详细信息。

**ID 格式：** SiYuan ID 看起来像“20210808180117-6v0mkxr”（14 位时间戳 + 7 个字母数字字符）。

## 快速参考

|运营|端点 |
|------------|----------|
|全文检索 | `/api/search/fullTextSearchBlock` |
| SQL查询 | `/api/query/sql` |
|阅读区块 | `/api/block/getBlockKramdown` |
|读书孩子| `/api/block/getChildBlocks` |
|获取路径 | `/api/filetree/getHPathByID` |
|获取属性 | `/api/attr/getBlockAttrs` |
|列出笔记本| `/api/notebook/lsNotebooks` |
|列出文件 | `/api/filetree/listDocsByPath` |
|创建笔记本| `/api/notebook/createNotebook` |
|创建文档 | `/api/filetree/createDocWithMd` |
|追加块| `/api/block/appendBlock` |
|更新区块 | `/api/block/updateBlock` |
|重命名文档 | `/api/filetree/renameDocByID` |
|设置属性| `/api/attr/setBlockAttrs` |
|删除块 | `/api/block/deleteBlock` |
|删除文档 | `/api/filetree/removeDocByID` |
|导出为 Markdown | `/api/export/exportMdContent` |

## 常用操作

### 搜索（全文）

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/search/fullTextSearchBlock" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"query": "会议记录", "page": 0}' | jq '.data.blocks[:5]'
````

### 搜索 (SQL)

直接查询区块数据库。只有 SELECT 语句是安全的。

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/query/sql" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"stmt": "从内容像 '\''%keyword%'\'' AND type='\''p'\'' LIMIT 20 的块中选择 id、内容、类型、框"}' | jq '.data'
````

有用的列：“id”、“parent_id”、“root_id”、“box”（笔记本 ID）、“path”、“content”、“type”、“subtype”、“created”、“updated”。

### 读取块内容

以 Kramdown（类似 Markdown）格式返回块内容。

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getBlockKramdown" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data.kramdown'
````

### 读取子块

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/getChildBlocks" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
````

### 获取人类可读的路径

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/getHPathByID" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
````

### 获取块属性

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/getBlockAttrs" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "20210808180117-6v0mkxr"}' | jq '.data'
````

### 列出笔记本

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/lsNotebooks" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{}' | jq '.data.notebooks[] | {id，名称，已关闭}'
````

### 列出笔记本中的文档

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/listDocsByPath" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"notebook": "NOTEBOOK_ID", "path": "/"}' | jq '.data.files[] | jq '.data.files[] | {id，姓名}'
````

### 创建文档

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/createDocWithMd" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d'{
    “笔记本”：“NOTEBOOK_ID”，
    "path": "/会议记录/2026-03-22",
    "markdown": "# 会议记录\n\n- 讨论的项目时间表\n- 分配的任务"
  }' | jq '.data'
````

### 创建一个笔记本

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/notebook/createNotebook" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"name": "我的新笔记本"}' | jq '.data.notebook.id'
````

### 将块附加到文档

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/appendBlock" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d'{
    "parentID": "DOCUMENT_OR_BLOCK_ID",
    "data": "末尾添加了新段落。",
    “数据类型”：“降价”
  }' | jq '.data'
````

还可用：“/api/block/prependBlock”（相同的参数，在开头插入）和“/api/block/insertBlock”（使用“previousID”而不是“parentID”在特定块之后插入）。

### 更新区块内容

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/updateBlock" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d'{
    "id": "BLOCK_ID",
    "data": "此处更新内容。",
    “数据类型”：“降价”
  }' | jq '.data'
````

### 重命名文档

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/filetree/renameDocByID" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "DOCUMENT_ID", "title": "新标题"}'
````

### 设置块属性

自定义属性必须以“custom-”为前缀：

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/attr/setBlockAttrs" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d'{
    "id": "BLOCK_ID",
    “属性”：{
      “自定义状态”：“已审核”，
      “自定义优先级”：“高”
    }
  }'
````

### 删除一个块

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/block/deleteBlock" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "BLOCK_ID"}'
````

要删除整个文档：使用 `/api/filetree/removeDocByID` 和 `{"id": "DOC_ID"}`。
要删除笔记本：使用 `/api/notebook/removeNotebook` 和 `{"notebook": "NOTEBOOK_ID"}`。

### 将文档导出为 Markdown

````bash
curl -s -X POST "${SIYUAN_URL:-http://127.0.0.1:6806}/api/export/exportMdContent" \
  -H "授权：令牌 $SIYUAN_TOKEN" \
  -H“内容类型：application/json”\
  -d '{"id": "DOCUMENT_ID"}' | jq -r '.data.content'
````

## 块类型

SQL 查询中常见的“type”值：

|类型 |描述 |
|------|-------------|
| `d` |文档（根块）|
| `p` |段落|
| `h` |标题 |
| `l` |列表 |
| `我` |列表项 |
| `c` |代码块|
| `m` |数学块|
| `t` |表|
| `b` |块引用 |
| `s` |超级街区|
| `html` | HTML 块 |

## 陷阱

- **所有端点都是 POST** ——甚至是只读操作。不要使用 GET。
- **SQL 安全性**：仅使用 SELECT 查询。 INSERT/UPDATE/DELETE/DROP 是危险的，不应该发送。
- **ID 验证**：ID 与模式“YYYYMMDDHHmmss-xxxxxxx”匹配。拒绝其他任何事情。
- **错误响应**：在处理“数据”之前，始终检查响应中的“code！= 0”。
- **大文档**：块内容和导出结果可能非常大。在 SQL 中使用“LIMIT”并通过“jq”进行管道传输以仅提取您需要的内容。
- **笔记本 ID**：使用特定笔记本时，首先通过“lsNotebooks”获取其 ID。

## 替代方案：MCP 服务器

如果您更喜欢本机集成而不是curl，请安装SiYuan MCP服务器：

````yaml
# 在 mcp_servers 下的 ~/.hermes/config.yaml 中：
mcp_服务器：
  思源：
    命令：npx
    args: ["-y", "@porkll/siyuan-mcp"]
    环境：
      SIYUAN_TOKEN：“你的令牌”
      SIYUAN_URL: "http://127.0.0.1:6806"
````