---
sidebar_position: 2
sidebar_label: "Google Workspace"
title: "Google Workspace — Gmail, Calendar, Drive, Sheets & Docs"
description: "Send email, manage calendar events, search Drive, read/write Sheets, and access Docs — all through OAuth2-authenticated Google APIs"
---
# Google Workspace 技能

OpenClaw 的 Gmail、日历、云端硬盘、联系人、表格和文档集成。使用具有自动令牌刷新功能的 OAuth2。如果 [Google Workspace CLI (`gws`)](https://github.com/googleworkspace/cli) 可用于更广泛的覆盖范围，则首选使用，否则会使用 Google 的 Python 客户端库。

**技能路径：** `技能/生产力/google-workspace/`

## 设置

该设置完全由代理驱动 - 请 OpenClaw 设置 Google Workspace，它会引导您完成每个步骤。流程：

1. **创建 Google Cloud 项目**并启用所需的 API（Gmail、日历、云端硬盘、表格、文档、人员）
2. **创建 OAuth 2.0 凭证**（桌面应用程序类型）并下载客户端密钥 JSON
3. **授权** — OpenClaw 生成一个授权 URL，您在浏览器中批准，粘贴回重定向 URL
4. **完成** — 令牌从该点开始自动刷新

:::提示仅使用电子邮件的用户
如果您只需要电子邮件（不需要日历/云端硬盘/表格），请使用 **喜马拉雅** 技能 - 它适用于 Gmail 应用程序密码，并且需要 2 分钟。无需 Google Cloud 项目。
:::

## 邮箱

### 搜索

````bash
$GAPI Gmail 搜索“is:unread”--max 10
$GAPI Gmail 搜索“from:boss@company.com newer_than:1d”
$GAPI Gmail 搜索“有：附件文件名：pdf newer_than：7d”
````

返回每条消息的带有“id”、“from”、“subject”、“date”、“snippet”和“labels”的 JSON。

### 阅读

````bash
$GAPI Gmail 获取 MESSAGE_ID
````

以文本形式返回完整的消息正文（首选纯文本，回退到 HTML）。

### 发送

````bash
# 基本发送
$GAPI gmail send --to user@example.com --subject "Hello" --body "消息文本"

# HTML 电子邮件
$GAPI gmail send --to user@example.com --subject "报告" \
  --body "<h1>第四季度结果</h1><p>此处详细信息</p>" --html

# 自定义发件人标题（显示名称 + 电子邮件）
$GAPI gmail send --to user@example.com --subject "Hello" \
  --from '“研究代理”<user@example.com>' --body“消息文本”

# 与抄送
$GAPI gmail 发送 --to user@example.com --cc "team@example.com" \
  --主题“更新”--正文“仅供参考”
````

### 自定义来自标头

`--from` 标志允许您自定义外发电子邮件上的发件人显示名称。当多个代理共享同一个 Gmail 帐户但您希望收件人看到不同的名称时，这非常有用：

````bash
# 代理 1
$GAPI gmail send --to client@co.com --subject "研究摘要" \
  --来自'“研究代理”<shared@company.com>'--body“...”

# 特工2  
$GAPI gmail send --to client@co.com --subject "代码审查" \
  --来自'“代码助手”<shared@company.com>'--body“...”
````

**工作原理：** `--from` 值设置为 MIME 消息上的 RFC 5322 “From” 标头。 Gmail 允许自定义您自己经过身份验证的电子邮件地址的显示名称，无需任何其他配置。收件人会看到自定义显示名称（例如“研究代理”），而电子邮件地址保持不变。

**重要提示：** 如果您在“--from”中使用*不同的电子邮件地址*（不是经过身份验证的帐户），Gmail 会要求在 Gmail 设置 → 帐户 → 邮件发送方式中将该地址配置为 [发送为别名](https://support.google.com/mail/answer/22370)。

`--from` 标志适用于 `send` 和 `reply`：

````bash
$GAPI Gmail 回复 MESSAGE_ID \
  --from '“支持机器人”<shared@company.com>' --body“我们正在努力”
````

### 正在回复

````bash
$GAPI gmail 回复 MESSAGE_ID --body “谢谢，这对我有用。”
````

自动对回复进行线程化（设置“In-Reply-To”和“References”标头）并使用原始消息的线程 ID。

### 标签

````bash
# 列出所有标签
$GAPI Gmail 标签

# 添加/删除标签
$GAPI gmail 修改 MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail 修改 MESSAGE_ID --remove-labels UNREAD
````

## 日历

````bash
# 列出事件（默认为未来 7 天）
$GAPI 日历列表
$GAPI 日历列表 --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# 创建事件（需要时区）
$GAPI 日历创建 --summary“团队站立”\
  --开始 2026-03-01T10:00:00-07:00 --结束 2026-03-01T10:30:00-07:00

# 包含地点和参加者
$GAPI 日历创建 --summary“午餐”\
  --开始 2026-03-01T12:00:00Z --结束 2026-03-01T13:00:00Z \
  --地点“咖啡馆”--与会者“alice@co.com，bob@co.com”

# 删除事件
$GAPI 日历删除 EVENT_ID
````

:::警告
日历时间**必须**包含时区偏移量（例如`-07:00`）或使用UTC（`Z`）。像“2026-03-01T10:00:00”这样的裸日期时间是不明确的，将被视为 UTC。
:::

## 驾驶

````bash
$GAPI驱动器搜索“季度报告”--max 10
$GAPI 驱动搜索“mimeType='application/pdf'” --raw-query --max 5
````

## 床单

````bash
# 读取一个范围
$GAPI 工作表获取 SHEET_ID“Sheet1!A1:D10”

# 写入一个范围
$GAPI 工作表更新 SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# 追加行
$GAPI 工作表附加 SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
````

## 文档

````bash
$GAPI 文档获取 DOC_ID
````

返回文档标题和全文内容。

## 联系方式

````bash
$GAPI 联系人列表 --max 20
````

## 输出格式

所有命令都会返回 JSON。每项服务的关键字段：

|命令|领域 |
|---------|--------|
| `gmail 搜索` | `id`、`threadId`、`from`、`to`、`subject`、`date`、`snippet`、`labels` |
| `gmail 获取` | `id`、`threadId`、`from`、`to`、`subject`、`date`、`labels`、`body` |
| `gmail 发送/回复` | `状态`、`id`、`threadId` |
| `日历列表` | `id`、`summary`、`start`、`end`、`location`、`description`、`htmlLink` |
| `日历创建` | `状态`、`id`、`摘要`、`htmlLink` |
| `驱动器搜索` | `id`、`name`、`mimeType`、`modifiedTime`、`webViewLink` |
| `联系人列表` | `姓名`、`电子邮件`、`电话` |
| `床单得到` |单元格值的二维数组 |

## 故障排除

|问题 |修复 |
|---------|-----|
| `未验证` |运行设置（要求 OpenClaw 设置 Google Workspace）|
| `刷新失败` |令牌已撤销 — 重新运行授权步骤 |
| `HttpError 403：权限不足` |缺少范围——使用正确的服务撤销并重新授权 |
| `HttpError 403：未配置访问` | Google Cloud Console 中未启用 API |
| `模块未找到错误` |使用 `--install-deps` 运行安装脚本 |