---
title: "Blogwatcher — Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool"
sidebar_label: "Blogwatcher"
description: "Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Blogwatcher

通过 blogwatcher-cli 工具监控博客和 RSS/Atom 源。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/研究/博客观察者` |
|版本 | `2.0.0` |
|作者 | JulienTant（Hyaxia 分叉/博客观察者）|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
| Tags | `RSS`、`博客`、`提要阅读器`、`监控` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Blogwatcher

使用“blogwatcher-cli”工具跟踪博客和 RSS/Atom 提要更新。支持自动提要发现、HTML 抓取回退、OPML 导入和已读/未读文章管理。

## 安装

Pick one method:

- **Go:** `去安装 github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest`
- **Docker:** `docker run --rm -v blogwatcher-cli:/data ghcr.io/julientant/blogwatcher-cli`
- **二进制（Linux amd64）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
- **二进制（Linux arm64）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
- **二进制（macOS Apple Silicon）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
- **二进制（macOS Intel）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`

所有版本：https://github.com/JulienTant/blogwatcher-cli/releases

### Docker 与持久存储

默认情况下，数据库位于“~/.blogwatcher-cli/blogwatcher-cli.db”。在 Docker 中，这会在容器重新启动时丢失。使用 `BLOGWATCHER_DB` 或卷挂载来持久化它：

````bash
# 命名卷（最简单）
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli 扫描

# Host bind mount
docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli 扫描
````

### 从原来的 blogwatcher 迁移

如果从 `Hyaxia/blogwatcher` 升级，请移动您的数据库：

````bash
mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db
````

二进制文件名称从“blogwatcher”更改为“blogwatcher-cli”。

## Common Commands

### Managing blogs

- 添加博客：`blogwatcher-cli 添加“我的博客”https://example.com`
- 添加显式提要： `blogwatcher-cli add "My Blog" https://example.com --feed-url https://example.com/feed.xml`
- 添加 HTML 抓取： `blogwatcher-cli add "My Blog" https://example.com --scrape-selector "article h2 a"`
- 列出跟踪的博客：`blogwatcher-cli blogs`
- 删除博客：`blogwatcher-cli 删除“我的博客”--yes`
- 从 OPML 导入：`blogwatcher-cli import subscriptions.opml`

### Scanning and reading

- 扫描所有博客：`blogwatcher-cli scan`
- 扫描一个博客：`blogwatcher-cli 扫描“我的博客”`
- 列出未读文章：`blogwatcher-cli 文章`
- 列出所有文章：`blogwatcher-cli 文章 --all`
- 按博客过滤：`blogwatcher-cli 文章 --blog“我的博客”`
- 按类别过滤：`blogwatcher-cli 文章 --category“工程”`
- 将文章标记为：`blogwatcher-cli read 1`
- 将文章标记为未读：`blogwatcher-cli unread 1`
- 标记全部已读：`blogwatcher-cli read-all`
- 将博客标记为全部已读： `blogwatcher-cli read-all --blog "My Blog" --yes`

## 环境变量

所有标志都可以通过带有“BLOGWATCHER_”前缀的环境变量设置：

|变量|描述 |
|---|---|
| `BLOGWATCHER_DB` | SQLite 数据库文件的路径 |
| `BLOGWATCHER_WORKERS` |并发扫描工作人员数量（默认值：8）|
| `BLOGWATCHER_SILENT` |扫描时仅输出“扫描完成”|
| `BLOGWATCHER_YES` |跳过确认提示 |
| `BLOGWATCHER_CATEGORY` |按类别默认文章过滤器 |

## 输出示例

````
$ blogwatcher-cli 博客
跟踪的博客 (1)：

  西克CD
    网址：https://xkcd.com
    提要：https://xkcd.com/atom.xml
    最后扫描时间：2026-04-03 10:30
````

````
$ blogwatcher-cli 扫描
正在扫描 1 个博客...

  西克CD
    来源：RSS |发现: 4 |新：4

共找到 4 篇新文章！
````

````
$ blogwatcher-cli 文章
未读文章（2）：

  [1] [新] 桶 - 第 13 部分
       博客：xkcd
       网址：https://xkcd.com/3095/
       发布时间：2026-04-02
       类别：漫画、科学

  [2] [新] 火山事实
       博客：xkcd
       网址：https://xkcd.com/3094/
       发布时间：2026-04-01
       类别： 漫画
````

## 注释

- 当未提供“--feed-url”时，自动发现博客主页中的 RSS/Atom 提要。
- 如果 RSS 失败并且配置了“--scrape-selector”，则回退到 HTML 抓取。
- RSS/Atom 提要的类别被存储并可用于过滤文章。
- 从 Feedly、Inoreader、NewsBlur 等导出的 OPML 文件批量导入博客。
- 数据库默认存储在`~/.blogwatcher-cli/blogwatcher-cli.db`（用`--db`或`BLOGWATCHER_DB`覆盖）。
- 使用 `blogwatcher-cli <command> --help` 来发现所有标志和选项。