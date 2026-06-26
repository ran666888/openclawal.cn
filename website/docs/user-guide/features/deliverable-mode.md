---
title: Deliverable Mode (Artifacts in Chat)
sidebar_label: Deliverable Mode
description: How the agent ships generated charts, PDFs, spreadsheets, and other files as native attachments in messaging platforms.
---
# 可交付模式

当 OpenClaw 在消息传递网关（Slack、Discord、Telegram、
WhatsApp、Signal 等），它可以将生成的文件直接传送到
聊天 - 不是作为用户必须复制的路径，而是作为本机附件。

图表显示为内联图像。 PDF 报告显示为文件
下载。电子表格上传为“.xlsx”。代理人不需要
写一个“MEDIA:”标签或做任何特殊的事情——它只是生成文件
并在响应中提及其绝对路径。网关选择路径
将其从可见消息中删除，然后上传
本地文件。

## 它是如何工作的

三部分组合在一起：

1. **代理具有生成文件的工具。** 通过“execute_code”用于图表
   matplotlib、PDF 的“latex-pdf-report”技能、“powerpoint”技能
   对于套牌，“image_generate”用于图像，“text_to_speech”用于音频，等等
   上。

2. **网关扫描代理响应中的文件路径。** 任何绝对路径
   (`/tmp/...`) 或主目录相对路径 (`~/...`) 以受支持的结尾
   扩展名被提取。代码块和内联代码内的路径是
   被忽略，因此代码示例永远不会被破坏。

3. **网关按文件类型调度。** 图像内联嵌入在
   平台支持；视频内嵌；音频路由到语音/音频
   附件；其他所有内容都作为文件附件上传。

## 支持的文件扩展名

|类别 |扩展 |交货|
|---|---|---|
|图片 | `.png .jpg .jpeg .gif .webp .bmp .tiff .svg` |内联嵌入|
|视频 | `.mp4 .mov .avi .mkv .webm` |内联嵌入（如果支持）|
|音频| `.mp3 .wav .ogg .m4a .flac` |语音/音频附件|
|文件 | `.pdf .docx .doc .odt .rtf .txt .md` |文件上传 |
|数据| `.xlsx .xls .csv .tsv .json .xml .yaml .yml` |文件上传 |
|演示 | `.pptx .ppt .odp` |文件上传 |
|档案 | `.zip .tar .gz .tgz .bz2 .7z` |文件上传 |
|网页 | `.html .htm` |文件上传 |

`.py`、`.log` 和其他源文件扩展名被有意排除，因此
代理不会自动发送任意源文件；如果你想发送代码
对于用户，使用代码块。

## 鼓励代理生产工件

默认情况下，代理不会获取工件——它必须知道这样做。
推动它的两种方法：

**每次会话：** 明确询问（“将比较结果以图表形式发送给我”，
“以 CSV 形式返回数据”）或编写您自己的自定义指令/
偏向于神器式回复的个性条目
消息传递平台。

**项目级别：** 将偏差添加到 `AGENTS.md` / `CLAUDE.md` /
代理工作的项目中的“.cursorrules”到您的全局
角色位于`~/.hermes/SOUL.md`中，或者作为命名预设
`~/.hermes/config.yaml` 中的 `agent.personalities` （每个会话可切换
通过“/个性”）。

代理必须使用的机制很简单：将文件渲染到
绝对路径（例如`/tmp/q3-revenue.png`）并提及该路径
回复中的纯文本。网关完成剩下的工作。内部路径
受隔离的代码块或反引号将被忽略，因此代码示例永远不会被忽略
肢解。

## 看板：工件骑行完成通知

如果您使用 OpenClaw 的看板多代理工作流程，工作人员可以附加
可交付文件到其“kanban_complete”调用：

````蟒蛇
看板_完成（
    摘要=“第三季度收入图表和报告”，
    文物=[
        “/tmp/q3-revenue.png”，
        “/tmp/q3-report.pdf”，
    ],
）
````

当网关通知程序将“任务完成”消息传递给任何人时
订阅 Slack/Telegram/ 等中的任务，它还会上传每个工件
作为该聊天的本机附件。人类获得可交付成果和
总结在一个地方。

通知程序运行时磁盘上不存在的文件将被静默跳过。

## 通过 MCP 连接更多服务

除了工件交付管道之外，代理还可以访问其他管道
通过 MCP（模型上下文协议）提供服务。 MCP 生态系统船舶
最流行工具的社区服务器 - 安装您需要的任何一个：

|服务 |它解锁了什么 |
|---|---|
| **概念** |读/写概念页面、数据库、查询工作区 |
| **GitHub** | gh CLI 之外的问题、PR、评论、存储库搜索 |
| **线性** |门票、项目、周期 |
| **松弛** |工作区全搜索，阅读其他频道|
| **Gmail** |收件箱分类、发送邮件、标签管理 |
| **销售人员** |潜在客户、机会、客户数据 |
| **雪花/BigQuery** |针对数据仓库的 SQL |
| **谷歌云端硬盘** |文件搜索、内容、共享管理 |

通过 `mcp_servers` 下的 `~/.hermes/config.yaml` 安装 MCP 服务器
部分。请参阅 [MCP 集成](./mcp.md) 了解完整的设置指南。

## 与 Slack 中的困惑计算机的比较

Perplexity Computer 的 Slack 集成是围绕相同的想法构建的：
代理生成可交付成果（图表、PDF、幻灯片）并发布
作为本机附件返回到线程中。赫尔墨斯代理的交付成果
mode 在本地提供相同的面向用户的模式：

- 生成发生在用户自己的 venv / 沙箱中（无远程租户）。
- 文件通过相同的 Slack `files.uploadV2` API 进入聊天室。
- 连接器广度来自 MCP，而不是 400 个精选目录
  托管集成——安装您实际使用的集成。

OAuth 令牌保留在用户计算机上的“auth.json”/“.env”中。没有托管
令牌存储。没有多租户 microVM。最终结果相同。