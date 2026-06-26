---
title: "Watchers — Poll RSS, JSON APIs, and GitHub with watermark dedup"
sidebar_label: "Watchers"
description: "Poll RSS, JSON APIs, and GitHub with watermark dedup"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 观察者

使用水印去重功能轮询 RSS、JSON API 和 GitHub。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/devops/watchers` 安装 |
|路径| `可选技能/de​​vops/观察者` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux, macOS |
|标签 | `cron`、`轮询`、`rss`、`github`、`http`、`自动化`、`监控` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 观察者

定期轮询外部来源并仅对新项目做出反应。三个现成的脚本加上一个共享水印助手；将它们连接到 cron 作业（或从终端临时运行它们）。

## 何时使用

- 用户想要观看 RSS/Atom 提要并收到新条目的通知
- 用户想要观看 GitHub 存储库的问题/拉取/发布/提交
- 用户想要轮询任意 JSON 端点并获得有关新项目的通知
- 用户请求“X 的观察者”或“X 更改时通知我”

## 心理模型

观察者只是一个脚本：

1. 从外部源获取数据
2. 与以前见过的 ID 的水印文件进行比较
3.写回新水印
4. 将新项目打印到标准输出（或者在无更改时不打印任何内容）

下面的脚本处理所有三个。代理通过终端工具（从 cron 作业、网络钩子或交互式聊天）运行它们，并报告新内容。

##现成的脚本

安装技能后，这三个都位于“$HERMES_HOME/skills/devops/watchers/scripts/”中。每个都读取“WATCHER_STATE_DIR”（默认为“$HERMES_HOME/watcher-state/”）作为其状态文件，由“--name”参数键入。

|脚本 |它看什么 |重复数据删除关键 |
|---|---|---|
| `watch_rss.py` | RSS 2.0 或 Atom 提要 URL | `<guid>` / `<id>` |
| `watch_http_json.py` |任何返回对象列表的 JSON 端点 |可配置的id字段|
| `watch_github.py` | GitHub 发布/拉取/发布/提交存储库 | `id` / `sha` |

所有三个：

- 首次运行记录基线——从不重播现有提要
- 水印是一个有界 ID 集（最大 500）以限制内存
- 输出格式：每项`## <标题>\n<url>\n\n<可选正文>`
- no-new 上的空标准输出 - 调用者将其视为无声
- 获取错误时非零退出

## 用法

直接从终端工具运行观察程序：

````bash
python $HERMES_HOME/skills/devops/watchers/scripts/watch_rss.py \
  --名称 hn --url https://news.ycombinator.com/rss --max 5
````

观看 GitHub 存储库（在 `${HERMES_HOME:-~/.hermes}/.env` 中设置 `GITHUB_TOKEN` 以避免 60 个请求/小时的匿名速率限制）：

````bash
python $HERMES_HOME/skills/devops/watchers/scripts/watch_github.py \
  --name Hermes-issues --repo NousResearch/hermes-agent --范围问题
````

轮询任意 JSON API：

````bash
python $HERMES_HOME/skills/devops/watchers/scripts/watch_http_json.py \
  --名称 api --url https://api.example.com/events \
  --id-field event_id --items-path data.events
````

## 连接到 cron

要求代理安排一个 cron 作业，提示如下：

> 每 15 分钟运行一次 `watch_rss.py --name hn --url https://news.ycombinator.com/rss`。如果它打印出任何内容，请总结标题并交付它们。如果它没有打印任何内容，请保持沉默。

代理通过 cron 作业代理循环内的终端工具调用脚本；不需要更改 cron 的内置“--script”标志。

## 状态文件

每个观察者都会写入“$HERMES_HOME/watcher-state/<name>.json”。检查：

````bash
猫 $HERMES_HOME/watcher-state/hn.json
````

强制重播（下次运行视为第一次轮询）：

````bash
rm $HERMES_HOME/watcher-state/hn.json
````

## 编写你自己的

所有三个脚本都使用相同的模板：加载水印、获取、比较、保存、发出。 `scripts/_watermark.py` 是共享助手；导入它即可免费获得原子写入+有界ID集+首次运行基线。请参阅三个参考脚本中的任何一个，了解它所需的样板文件有多么少。

## 常见陷阱

1. **每个刻度打印“无新项目”标头。** 调用者依赖于空 stdout = 静默。如果您在空的增量上打印任何内容，您就会向该通道发送垃圾邮件。附带的脚本可以处理这个问题；自定义脚本也必须如此。
2. **期望第一次运行会发出项目。**它不会——第一次运行会记录基线。如果您需要初始摘要，请在第一次运行后删除状态文件或在您自己的脚本中添加“--prime-with-latest N”标志。
3. **无限制的水印增长。** 共享助手的 ID 上限为 500 个。对于高搅动饲料，将其调高；在受限文件系统上降低它。
4. **将状态目录放在代理的沙箱无法写入的位置。** `$HERMES_HOME/watcher-state/` 始终可写。 Docker/Modal 后端可能看不到任意主机路径。