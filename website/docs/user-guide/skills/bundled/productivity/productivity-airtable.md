---
title: "Airtable — Airtable REST API via curl"
sidebar_label: "Airtable"
description: "Airtable REST API via curl"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 空中桌

通过curl 的Airtable REST API。记录 CRUD、过滤器、更新插入。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/生产力/可用空间` |
|版本 | `1.1.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `Airtable`、`生产力`、`数据库`、`API` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Airtable — 基础、表格和记录

使用“terminal”工具通过“curl”直接使用 Airtable 的 REST API。没有 MCP 服务器，没有 OAuth 流程，没有 Python SDK——只有“curl”和个人访问令牌。

## 先决条件

1. 在 https://airtable.com/create/tokens 创建 **个人访问令牌 (PAT)**（令牌以“pat...”开头）。
2. 授予这些范围（最小）：
   - `data.records:read` — 读取行
   - `data.records:write` — 创建/更新/删除行
   - `schema.bases:read` — 列出库和表
3. **重要提示：** 在同一令牌 UI 中，将您想要访问的每个基地添加到令牌的 **访问** 列表中。 PAT 的作用域为每个基数 - 错误基数上的有效标记会返回“403”。
4. 将令牌存储在 `${HERMES_HOME:-~/.hermes}/.env` 中（或通过 `hermes setup`）：
   ````
   AIRTABLE_API_KEY=pat_your_token_here
   ````

> 注意：旧版“key...” API 密钥已于 2024 年 2 月弃用。现在只有 PAT 和 OAuth 令牌有效。

## API 基础知识

- **端点：** `https://api.airtable.com/v0`
- **身份验证标头：** `授权：承载 $AIRTABLE_API_KEY`
- **所有请求**使用 JSON（任何 POST/PATCH/PUT 主体的“Content-Type: application/json”）。
- **对象 ID：** 基础 `app...`、表 `tbl...`、记录 `rec...`、字段 `fld...`。 ID 永远不会改变；名字可以。在自动化中更喜欢 ID。
- **速率限制：** 5 个请求/秒/基。 `429` → 退后。单个基地的爆发将被限制。

基础卷曲图案：
````bash
卷曲-s“https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=5”\
  -H“授权：持有者$AIRTABLE_API_KEY”| python3 -m json.工具
````

`-s` 抑制curl的进度条——为每个调用保持它设置，这样工具输出对于OpenClaw来说保持干净。通过“python3 -m json.tool”（始终存在）或“jq”（如果已安装）进行管道传输以获取可读的 JSON。

## 字段类型（请求正文形状）

|字段类型|写形状|
|---|---|
|单行文本 | `“姓名”：“你好”` |
|长文| `"Notes": "多行"` |
|数量 | `“分数”：42` |
|复选框 | `“完成”：true` |
|单选| `"Status": "Todo"` （名称必须已经存在，除非 `typecast: true`）|
|多选| `“标签”：[“紧急”，“错误”]` |
|日期 | `“到期”：“2026-04-01”` |
|日期时间 (UTC) | `“在”：“2026-04-01T14：30：00.000Z”` |
|网址/电子邮件/电话 | `“链接”：“https://…”` |
|附件 | `"Files": [{"url": "https://…"}]` (Airtable 获取 + 重新托管) |
|链接记录 | `"Owner": ["recXXXXXXXXXXXXXXX"]` （记录 ID 数组）|
|用户 | `"AssignedTo": {"id": "usrXXXXXXXXXXXXXX"}` |

在创建/更新主体的顶层传递 `"typecast": true` ，让 Airtable 自动强制值（例如，动态创建一个新的选择选项，将 `"42"` 转换为 `42`）。

## 常见查询

### 列出令牌可以看到的基础
````bash
卷曲-s“https://api.airtable.com/v0/meta/bases”\
  -H“授权：持有者$AIRTABLE_API_KEY” | python3 -m json.工具
````

### 列出基础表+架构
````bash
卷曲-s“https://api.airtable.com/v0/meta/bases/$BASE_ID/tables”\
  -H“授权：持有者$AIRTABLE_API_KEY” | python3 -m json.工具
````
在变异之前使用它 — 确认确切的字段名称和 ID，为选择字段显示“options.choices”，并显示主字段名称。

### 列出记录（前 10 条）
````bash
卷曲-s“https://api.airtable.com/v0/$BASE_ID/$TABLE?maxRecords=10”\
  -H“授权：持有者$AIRTABLE_API_KEY”| python3 -m json.工具
````

### 获取单条记录
````bash
卷曲-s“https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID”\
  -H“授权：持有者$AIRTABLE_API_KEY”| python3 -m json.工具
````

### 过滤记录（filterByFormula）
Airtable 公式必须是 URL 编码的。让 Python stdlib 来做这件事——永远不要手动编码：
````bash
FORMULA="{状态}='待办事项'"
ENC=$(python3 -c '导入 sys, urllib.parse; print(urllib.parse.quote(sys.argv[1], safe=""))' "$FORMULA")
卷曲-s“https://api.airtable.com/v0/$BASE_ID/$TABLE?filterByFormula=$ENC&maxRecords=20”\
  -H“授权：持有者$AIRTABLE_API_KEY” | python3 -m json.工具
````

有用的公式模式：
- 完全匹配：`{Email}='user@example.com'`
- 包含：`FIND('bug', LOWER({Title}))`
- 多个条件：`AND({Status}='Todo', {Priority}='High')`
- 或者：`OR({Owner}='alice', {Owner}='bob')`
- 非空：`NOT({Assignee}='')`
- 日期比较：`IS_AFTER({Due}, TODAY())`

### 排序+选择特定字段
````bash
curl -s "https://api.airtable.com/v0/$BASE_ID/$TABLE?sort%5B0%5D%5Bfield%5D=优先级&sort%5B0%5D%5Bdirection%5D=asc&fields%5B%5D=名称&fields%5B%5D=状态" \
  -H“授权：持有者$AIRTABLE_API_KEY” | python3 -m json.工具
````
查询参数中的方括号必须是 URL 编码的（`%5B` / `%5D`）。

### 使用命名视图
````bash
卷曲-s“https://api.airtable.com/v0/$BASE_ID/$TABLE?view=Grid%20view&maxRecords=50”\
  -H“授权：持有者$AIRTABLE_API_KEY” | python3 -m json.工具
````
视图应用其保存的过滤器+排序服务器端。

## 常见突变

### 创建记录
````bash
卷曲-s -X POST“https://api.airtable.com/v0/$BASE_ID/$TABLE”\
  -H“授权：承载$AIRTABLE_API_KEY”\
  -H“内容类型：application/json”\
  -d '{"fields":{"名称":"新任务","状态":"待办事项","优先级":"高"}}' | python3 -m json.工具
````

### 一次调用最多创建 10 条记录
````bash
卷曲-s -X POST“https://api.airtable.com/v0/$BASE_ID/$TABLE”\
  -H“授权：承载$AIRTABLE_API_KEY”\
  -H“内容类型：application/json”\
  -d'{
    “类型转换”：正确，
    “记录”：[
      {"fields": {"Name": "任务 A", "Status": "Todo"}},
      {"fields": {"Name": "任务 B", "Status": "进行中"}}
    ]
  }' | python3 -m json.工具
````
批量端点的上限为 **每个请求 10 条记录**。对于较大的插入，以 10 个为一组进行循环，并进行短暂睡眠以遵守 5 请求/秒/基数。

### 更新记录（PATCH — 合并，保留未更改的字段）
````bash
curl -s -X PATCH“https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID”\
  -H“授权：承载$AIRTABLE_API_KEY”\
  -H“内容类型：application/json”\
  -d '{"fields":{"Status":"Done"}}' | python3 -m json.工具
````

### 通过合并字段更新插入（不需要 ID）
````bash
卷曲 -s -X 补丁“https://api.airtable.com/v0/$BASE_ID/$TABLE”\
  -H“授权：承载$AIRTABLE_API_KEY”\
  -H“内容类型：application/json”\
  -d'{
    "performUpsert": {"fieldsToMergeOn": ["电子邮件"]},
    “记录”：[
      {“字段”：{“电子邮件”：“user@example.com”，“状态”：“活动”}}
    ]
  }' | python3 -m json.工具
````
`performUpsert` 创建合并字段值为新的记录，修补合并字段值已存在的记录。非常适合幂等同步。

### 删除一条记录
````bash
curl -s -X 删除“https://api.airtable.com/v0/$BASE_ID/$TABLE/$RECORD_ID”\
  -H“授权：持有者$AIRTABLE_API_KEY”| python3 -m json.工具
````

### 一次通话最多删除10条记录
````bash
curl -s -X 删除“https://api.airtable.com/v0/$BASE_ID/$TABLE?records%5B%5D=rec1&records%5B%5D=rec2”\
  -H“授权：持有者$AIRTABLE_API_KEY” | python3 -m json.工具
````

## 分页

列表端点最多返回 **每页 100 条记录**。如果响应包含 `"offset": "..."`，则在下次调用时将其传回。循环直到该字段不存在：

````bash
偏移量=“”
同时:;做
  URL =“https://api.airtable.com/v0/$BASE_ID/$TABLE?pageSize=100”
  [ -n "$OFFSET" ] && URL="$URL&offset=$OFFSET"
  RESP=$(curl -s "$URL" -H "授权：承载 $AIRTABLE_API_KEY")
  回声“$RESP”| python3 -c '导入 json,sys; d=json.load(sys.stdin); [print(r["id"], r["fields"].get("Name","")) for r in d["records"]]'
  OFFSET=$(echo "$RESP" | python3 -c '导入 json,sys; d=json.load(sys.stdin); print(d.get("offset",""))')
  [ -z "$OFFSET" ] && 中断
完成
````

## 典型的 OpenClaw 工作流程

1. **确认身份验证。** `curl -s -o /dev/null -w "%{http_code}\n" https://api.airtable.com/v0/meta/bases -H "Authorization: Bearer $AIRTABLE_API_KEY"` — 预期为 `200`。
2. **找到基础。** 列出基础（上面的步骤），或者如果令牌缺少“schema.bases:read”，则直接向用户询问“app...” ID。
3. **检查架构。** `GET /v0/meta/bases/$BASE_ID/tables` — 在更改任何内容之前，在会话中本地缓存确切的字段名称和主字段名称。
4. **写前先读。** 对于“update X where Y”，`filterByFormula` 首先解析 `rec...` ID，然后解析 `PATCH /v0/$BASE_ID/$TABLE/$RECORD_ID`。切勿猜测记录 ID。
5. **批量写入。** 将相关创建合并到一个 10 条记录的 POST 中，以保持在 5 个请求/秒的预算之下。
6. **破坏性操作。** 删除操作无法通过 API 撤消。如果用户说“删除所有 X”，则回显过滤器 + 记录计数并在触发前确认。

## 陷阱

- **`filterByFormula` 必须是 URL 编码。** 带有空格或非 ASCII 的字段名称也需要编码（`{My Field}` → `%7BMy%20Field%7D`）。使用Python stdlib（上面的模式）——永远不要手动转义。
- **响应中省略了空字段。** 缺少“Assignee”键并不意味着该字段不存在 - 它意味着该记录的值为空。在得出字段缺失的结论之前检查架构（步骤 3）。
- **PATCH 与 PUT。** `PATCH` 将提供的字段合并到记录中。 “PUT”会完全替换记录并清除您未包含的任何字段。默认为“补丁”。
- **单选选项必须存在。** 当 `Shipping` 不在字段的选项列表中时，写入 `"Status": "Shipping"` 时会出现 `INVALID_MULTIPLE_CHOICE_OPTIONS` 错误，除非您传递 `"typecast": true` （自动创建选项）。
- **每个基础令牌范围。** 一个基础上的“403”而另一个基础有效意味着该令牌的访问列表不包括该基础 - 这不是范围或身份验证问题。将用户发送到 https://airtable.com/create/tokens 进行授予。
- **速率限制是每个基础，而不是每个令牌。** `baseA` 上 5 请求/秒，`baseB` 上 5 请求/秒就可以了；仅“baseA”上的 6 个请求/秒就会受到限制。监视“429”上的“Retry-After”标头。

## OpenClaw 重要注意事项

- **始终将“terminal”工具与“curl”一起使用。**不要使用“web_extract”（它无法发送身份验证标头）或“browser_navigate”（需要 UI 身份验证并且速度很慢）。
- **加载此技能时，**`AIRTABLE_API_KEY` 自动从 `${HERMES_HOME:-~/.hermes}/.env` 流入子进程** - 无需在每次 `curl` 调用之前重新导出它。
- **小心地转义公式中的大括号。** 在定界文档主体中，“{Status}”是字面意思。在 shell 参数中，“{Status}”在“{...}”大括号扩展上下文之外是安全的，但在拼接到 URL 之前通过“python3 urllib.parse.quote”传递动态字符串。
- **使用 `python3 -m json.tool`** （始终存在）而不是 `jq` （可选）进行漂亮打印。仅当您需要过滤/投影时才使用“jq”。
- **分页是每页的，而不是全局的。** Airtable 的 100 条记录上限是一个硬性限制；没有办法去碰它。使用“offset”循环，直到该字段不存在。
- **读取非 2xx 响应的“errors”数组** — Airtable 返回结构化错误代码，例如“AUTHENTICATION_REQUIRED”、“INVALID_PERMISSIONS”、“MODEL_ID_NOT_FOUND”、“INVALID_MULTIPLE_CHOICE_OPTIONS”，准确告诉您出了什么问题。