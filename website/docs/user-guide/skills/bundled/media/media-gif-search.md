---
title: "Gif Search — Search/download GIFs from Tenor via curl + jq"
sidebar_label: "Gif Search"
description: "Search/download GIFs from Tenor via curl + jq"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Gif 搜索

通过curl + jq 从 Tenor 搜索/下载 GIF。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/媒体/gif 搜索` |
|版本 | `1.1.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `GIF`、`媒体`、`搜索`、`Tenor`、`API` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# GIF 搜索（Tenor API）

使用curl 通过 Tenor API 直接搜索和下载 GIF。不需要额外的工具。

## 何时使用

对于查找反应 GIF、创建视觉内容以及在聊天中发送 GIF 非常有用。

## 设置

在您的环境中设置 Tenor API 密钥（添加到 `${HERMES_HOME:-~/.hermes}/.env`）：

````bash
TENOR_API_KEY=your_key_here
````

请访问 https://developers.google.com/tenor/guides/quickstart 获取免费的 API 密钥 — Google Cloud Console Tenor API 密钥是免费的，并且具有慷慨的速率限制。

## 先决条件

- `curl` 和 `jq` （都是 macOS/Linux 上的标准）
- `TENOR_API_KEY` 环境变量

## 搜索 GIF

````bash
# 搜索并获取 GIF URL
卷曲-s“https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}”| jq -r '.results[].media_formats.gif.url'

# 获取较小/预览版本
卷曲-s“https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}”| jq -r '.results[].media_formats.tinygif.url'
````

## 下载 GIF

````bash
# 搜索并下载排名靠前的结果
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')
卷曲-sL“$ URL”-o庆祝活动.gif
````

## 获取完整元数据

````bash
卷曲-s“https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}”| jq '.结果[] | {标题：.title，网址：.media_formats.gif.url，预览：.media_formats.tinygif.url，尺寸：.media_formats.gif.dims}'
````

## API 参数

|参数|描述 |
|------------|-------------|
| `q` |搜索查询（URL 将空格编码为“+”）|
| `限制` |最大结果（1-50，默认 20）|
| `关键` | API 密钥（来自 `$TENOR_API_KEY` 环境变量）|
| `媒体过滤器` |过滤器格式：`gif`、`tinygif`、`mp4`、`tinymp4`、`webm` |
| `内容过滤器` |安全性：“关”、“低”、“中”、“高”|
| `语言环境` |语言：`en_US`、`es`、`fr` 等 |

## 可用的媒体格式

每个结果在“.media_formats”下都有多种格式：

|格式|使用案例|
|--------|----------|
| 'gif' |完整质量 GIF |
| `tinygif` |小预览 GIF |
| `mp4` |视频版本（较小的文件大小）|
| `tinymp4` |小预览视频|
| `webm` | WebM 视频 |
| `nanogif` |小缩略图|

## 注释

- 对查询进行 URL 编码：空格为“+”，特殊字符为“%XX”
- 对于在聊天中发送，“tinygif” URL 的重量更轻
- GIF URL 可以直接在 markdown 中使用： `![alt](https://github.com/NousResearch/hermes-agent/blob/main/skills/media/gif-search/url)`