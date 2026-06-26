---
sidebar_position: 11
title: "Automate Anything with Cron"
description: "Real-world automation patterns using OpenClaw cron — monitoring, reports, pipelines, and multi-skill workflows"
---
# 使用 Cron 自动化任何事情

[每日简报机器人教程](/guides/daily-briefing-bot) 涵盖了基础知识。本指南更进一步——您可以根据自己的工作流程调整五种现实世界的自动化模式。

有关完整功能参考，请参阅[计划任务 (Cron)](/user-guide/features/cron)。

:::信息 关键概念
Cron 作业在新的代理会话中运行，不记录您当前的聊天。提示必须**完全独立** — 包括客服人员需要了解的所有内容。
:::

:::tip 不需要法学硕士？您有两个零令牌选项。
- **重复看门狗**，其中脚本已生成确切的消息（内存警报、磁盘警报、心跳）：使用 [仅脚本 cron 作业](/guides/cron-script-only)。相同的调度程序，没有法学硕士。您可以要求 OpenClaw 在聊天中为您设置一个 - “cronjob”工具知道何时选择“no_agent=True”并为您编写脚本。
- **从已经运行的脚本中一次性**（CI 步骤、提交后挂钩、部署脚本、外部调度监视器）：使用 [`hermes send`](/guides/pipe-script-output) 将 stdout 或文件直接通过管道传送到 Telegram / Discord / Slack / 等，无需设置 cron 条目。
:::

---

## 模式 1：网站变更监控

监视 URL 的更改并仅在出现变化时收到通知。

“script”参数是这里的秘密武器。 Python 脚本在每次执行之前运行，其标准输出成为代理的上下文。脚本处理机械工作（获取、比较）；代理处理推理（这个变化有趣吗？）。

创建监控脚本：

````bash
mkdir -p ~/.hermes/scripts
````

```python title="~/.hermes/scripts/watch-site.py"
导入 hashlib、json、os、urllib.request

网址=“https://example.com/pricing”
STATE_FILE = os.path.expanduser("~/.hermes/scripts/.watch-site-state.json")

# 获取当前内容
req = urllib.request.Request(URL, headers={"User-Agent": "Hermes-Monitor/1.0"})
内容 = urllib.request.urlopen(req, timeout=30).read().decode()
current_hash = hashlib.sha256(content.encode()).hexdigest()

# 加载之前的状态
上一个哈希=无
如果 os.path.exists(STATE_FILE):
    将 open(STATE_FILE) 作为 f：
        prev_hash = json.load(f).get("哈希")

# 保存当前状态
将 open(STATE_FILE, "w") 作为 f：
    json.dump({"hash": current_hash, "url": URL}, f)

# 代理的输出
如果 prev_hash 且 prev_hash != current_hash:
    print(f"在 {URL} 上检测到更改")
    print(f"前一个哈希值：{prev_hash}")
    print(f"当前哈希值：{current_hash}")
    print(f"\n当前内容（前 2000 个字符）:\n{content[:2000]}")
其他：
    打印（“NO_CHANGE”）
````

设置 cron 作业：

````bash
/cron add "every 1h" “如果脚本输出显示 CHANGE DETECTED，请总结页面上发生的更改以及为什么它可能很重要。如果它显示 NO_CHANGE，请仅使用 [SILENT] 进行响应。” --script ~/.hermes/scripts/watch-site.py --name "定价监视器" --deliver telegram
````

:::提示 [SILENT] 技巧
对于 cron 监控作业，指示代理在没有任何变化时仅响应“[SILENT]”。 Cron 传递将“[SILENT]”视为安静标记，因此您只会在实际发生事情时收到通知 - 在安静时间不会收到垃圾邮件。
:::

---

## 模式2：周报

将多个来源的信息编译成格式化摘要。该服务每周运行一次并传送到您的家庭频道。

````bash
/cron add "0 9 * * 1" "生成每周报告，内容包括：

1. 在网络上搜索过去一周最热门的 5 条人工智能新闻报道
2. 在 GitHub 上搜索“机器学习”主题中的热门存储库
3. 查看黑客新闻，了解讨论最多的 AI/ML 帖子

格式化为清晰的摘要，其中包含每个来源的部分。包括链接。
将其控制在 500 字以内——只突出显示重要的内容。” --name“每周人工智能文摘”--投递电报
````

从 CLI：

````bash
爱马仕 cron 创建“0 9 * * 1”\
  “生成一份每周报告，涵盖热门 AI 新闻、热门 ML GitHub 存储库以及讨论最多的 HN 帖子。采用章节格式，包含链接，字数控制在 500 字以内。” \
  --name“每周人工智能文摘”\
  --发送电报
````

`0 9 * * 1` 是一个标准的 cron 表达式：每周一上午 9:00。

---

## 模式 3：GitHub 存储库观察者

监视存储库中的新问题、PR 或版本。

````bash
/cron 添加“每 6 小时”“检查 GitHub 存储库 NousResearch/hermes-agent：
- 过去 6 小时内打开的新问题
- 过去 6 小时内打开或合并的新 PR
- 任何新版本

使用终端运行 gh 命令：
  gh 问题列表 --repo NousResearch/hermes-agent --state open --json 编号,标题,作者,createdAt --limit 10
  gh pr list --repo NousResearch/hermes-agent --state all --json 编号,标题,作者,createdAt,mergedAt --limit 10

仅筛选最近 6 小时内的项目。如果没有新内容，请用 [SILENT] 回应。
否则，请提供活动的简明摘要。” --name“回购观察者”--传递不和谐
````

:::警告 独立提示
请注意提示符如何包含确切的“gh”命令。 cron 代理不记得以前的运行或你的偏好——把一切都拼出来。
:::

---

## 模式 4：数据收集管道

定期抓取数据、保存到文件并检测一段时间内的趋势。该模式将脚本（用于收集）与代理（用于分析）相结合。

```python title="~/.hermes/scripts/collect-prices.py"
导入 json、os、urllib.request
从日期时间导入日期时间

DATA_DIR = os.path.expanduser("~/.hermes/data/prices")
os.makedirs（DATA_DIR，exist_ok = True）

# 获取当前数据（例如：加密货币价格）
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
数据 = json.loads(urllib.request.urlopen(url, timeout=30).read())

# 追加到历史文件
条目 = {“时间戳”：datetime.now().isoformat()，“价格”：数据}
History_file = os.path.join(DATA_DIR, "history.jsonl")
将 open(history_file, "a") 作为 f：
    f.write(json.dumps(entry) + "\n")

# 加载最近的历史记录进行分析
lines = open(history_file).readlines()
centre = [json.loads(l) for l inlines[-24:]] # 最后 24 个数据点

# 代理的输出
print(f"当前：BTC=${data['bitcoin']['usd']}, ETH=${data['ethereum']['usd']}")
print(f"收集的数据点：总共 {len(lines)}，显示最后 {len(recent)}")
print(f"\n最近历史记录:")
对于 r 最近[-6:]：
    print(f" {r['时间戳']}: BTC=${r['价格']['比特币']['美元']}, ETH=${r['价格']['以太坊']['美元']}")
````

````bash
/cron add "every 1h" "分析脚本输出的价格数据。报告：
1. 当前价格
2. 最近 6 个数据点的趋势方向（向上/向下/持平）
3. 任何显着变动（>5% 变化）

如果价格持平并且没有什么值得注意的地方，请回复[静音]。
如果有重大举动，请解释发生了什么。” \
  --script ~/.hermes/scripts/collect-prices.py \
  --name“价格跟踪器”\
  --发送电报
````

脚本进行机械收集；代理添加推理层。

---

## 模式 5：多技能工作流程

将技能链接在一起以完成复杂的计划任务。技能在提示执行之前按顺序加载。

````bash
# 使用 arxiv 技能查找论文，然后使用黑曜石技能保存笔记
/cron add "0 8 * * *" “在 arXiv 中搜索过去一天关于‘语言模型推理’的 3 篇最有趣的论文。为每篇论文创建一个黑曜石注释，其中包含标题、作者、摘要摘要和关键贡献。” \
  --技能 arxiv \
  --技能黑曜石\
  --name“论文摘要”
````

直接从工具中：

````蟒蛇
定时任务（
    动作=“创建”，
    技能=["arxiv", "黑曜石"],
    Prompt="在 arXiv 中搜索过去一天有关“语言模型推理”的论文。将前 3 篇保存为黑曜石笔记。",
    时间表=“0 8 * * *”，
    name="论文摘要",
    交付=“本地”
）
````

技能按顺序加载——首先是“arxiv”（教智能体如何搜索论文），然后是“obsidian”（教如何写笔记）。提示将他们联系在一起。

---

## 管理你的工作

````bash
# 列出所有活跃的作业
/cron 列表

# 立即触发作业（用于测试）
/cron 运行 <作业 ID>

# 暂停作业而不删除它
/cron 暂停 <job_id>

# 编辑正在运行的作业的计划或提示
/cron edit <job_id> --安排“每 4 小时”
/cron edit <job_id> --prompt "更新任务描述"

# 在现有工作中添加或删除技能
/cron 编辑 <job_id> --skill arxiv --skill 黑曜石
/cron 编辑 <job_id> --clear-skills

# 永久删除作业
/cron 删除 <job_id>
````

---

## 交付目标

`--deliver` 标志控制结果的去向：

|目标|示例|使用案例|
|--------|---------|----------|
| `起源` | `--传递原点` |创建作业的同一聊天（默认）|
| `本地` | `--交付本地` |仅保存到本地文件 |
| `电报` | `--发送电报` |您的 Telegram 主页频道 |
| `不和谐` | `--传递不和谐` |您的 Discord 主页频道 |
| `松弛` | `--提供松弛` |您的 Slack 主页频道 |
|具体聊聊| `--发送电报：-1001234567890` |特定的 Telegram 群组 |
|螺纹| `--发送电报：-1001234567890:17585` |特定的 Telegram 主题线程 |

---

## 提示

**使提示独立。** cron 作业中的代理不会记录您的对话。直接在提示中包含 URL、存储库名称、格式首选项和交付说明。

**有意使用“[SILENT]”。**对于监视作业，请包含诸如“如果没有任何变化，仅使用“[SILENT]”进行响应之类的说明。不要要求代理在安静的情况下解释令牌 - cron 将“[SILENT]”视为传递抑制标记。

**使用脚本进行数据收集。** `script` 参数允许 Python 脚本处理无聊的部分（HTTP 请求、文件 I/O、状态跟踪）。代理只能看到脚本的标准输出并对其应用推理。这比让代理自己进行获取更便宜且更可靠。

**使用“/cron run”进行测试。**在等待计划触发之前，使用“/cron run <job_id>”立即执行并验证输出是否正确。

**计划表达式。** 支持的格式：相对延迟 (`30m`)、间隔 (`每 2h`)、标准 cron 表达式 (`0 9 * * *`) 和 ISO 时间戳 (`2025-06-15T09:00:00`)。不支持“daily at 9am”等自然语言 - 请改用“0 9 * * *”。

---

*有关完整的 cron 参考 - 所有参数、边缘情况和内部结构 - 请参阅[计划任务 (Cron)](/user-guide/features/cron)。*