---
title: "Parallel Cli"
sidebar_label: "Parallel Cli"
description: "Optional vendor skill for Parallel CLI — agent-native web search, extraction, deep research, enrichment, FindAll, and monitoring"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 并行 CLI

并行 CLI 的可选供应商技能 — 代理本机 Web 搜索、提取、深入研究、丰富、FindAll 和监控。更喜欢 JSON 输出和非交互式流程。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/parallel-cli` 安装 |
|路径| `可选技能/研究/并行-cli` |
|版本 | `1.1.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `研究`、`Web`、`搜索`、`深入研究`、`丰富`、`CLI` |
|相关技能| [`duckduckgo-search`](/docs/用户指南/技能/可选/research/research-duckduckgo-search)，[`mcporter`](/docs/用户指南/技能/可选/mcp/mcp-mcporter) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 并行 CLI

当用户明确需要 Parallel 时，或者当终端本机工作流程将受益于 Parallel 的特定于供应商的 Web 搜索、提取、深入研究、丰富、实体发现或监控堆栈时，请使用“parallel-cli”。

这是一个可选的第三方工作流程，不是 OpenClaw 的核心功能。

重要期望：
- Parallel 是一项带有免费套餐的付费服务，而不是完全免费的本地工具。
- 它与 OpenClaw 原生 `web_search` / `web_extract` 重叠，因此默认情况下不喜欢它进行普通查找。
- 当用户特别提及 Parallel 或需要 Parallel 的丰富、FindAll 或监控工作流程等功能时，首选此技能。

`parallel-cli` 是为代理设计的：
- 通过 `--json` 输出 JSON
- 非交互式命令执行
- 使用“--no-wait”、“status”和“poll”异步长时间运行作业
- 使用 `--previous-interaction-id` 进行上下文链接
- 在一个 CLI 中搜索、提取、研究、丰富、实体发现和监控

## 何时使用

在以下情况下更喜欢使用此技能：
- 用户明确提及 Parallel 或 `parallel-cli`
- 该任务需要比简单的一次性搜索/提取过程更丰富的工作流程
- 您需要可以稍后启动和轮询的异步深度研究工作
- 您需要结构化丰富、FindAll 实体发现或监控

当没有特别要求并行时，更喜欢 OpenClaw 原生的 `web_search` / `web_extract` 来快速一次性查找。

## 安装

尝试对环境可用的侵入性最小的安装路径。

### 自制

````bash
brew 安装并行-web/tap/parallel-cli
````

### npm

````bash
npm install -g 并行网络-cli
````

### Python 包

````bash
pip install “parallel-web-tools[cli]”
````

### 独立安装程序

````bash
卷曲-fsSL https://parallel.ai/install.sh |巴什
````

如果你想要一个独立的 Python 安装，`pipx` 也可以工作：

````bash
pipx 安装“parallel-web-tools[cli]”
pipx 确保路径
````

## 身份验证

互动登录：

````bash
并行 cli 登录
````

无头/SSH/CI：

````bash
并行 cli 登录 --device
````

API密钥环境变量：

````bash
导出 PARALLEL_API_KEY="***"
````

验证当前的身份验证状态：

````bash
并行 cli 身份验证
````

如果身份验证需要浏览器交互，请使用“pty=true”运行。

## 核心规则集

1. 当您需要机器可读的输出时，始终首选“--json”。
2. 更喜欢显式参数和非交互式流程。
3. 对于长时间运行的作业，请使用“--no-wait”，然后使用“status”/“poll”。
4. 仅引用 CLI 输出返回的 URL。
5. 当可能出现后续问题时，将大型 JSON 输出保存到临时文件中。
6. 仅对真正长时间运行的工作流程使用后台进程；否则在前台运行。
7. 优先选择 OpenClaw 原生工具，除非用户特别需要并行或需要仅并行工作流程。

## 快速参考

<!-- ascii-guard-ignore -->
````文本
并行 cli
├── 授权
├── 登录
├── 退出
├── 搜寻
├── 提取/获取
├── 研究运行|状态|民意调查|处理者
├── 丰富运行|状态|投票|计划|建议|部署
├── findall 运行|摄取|状态|投票|结果|丰富|扩展|模式|取消
└── 监控创建|列表|获取|更新|删除|事件|事件组|模拟
````
<!-- ascii-guard-ignore-end -->

## 常见标志和模式

常用标志：
- `--json` 用于结构化输出
- 异步作业的“--no-wait”
- `--previous-interaction-id <id>` 用于重用早期上下文的后续任务
- `--max-results <n>` 用于搜索结果计数
- 用于搜索行为的“--mode one-shot|agentic”
- `--include-domains domain1.com,domain2.com`
-`--排除域domain1.com，domain2.com`
- `--日期 YYYY-MM-DD`

方便时从标准输入读取：

````bash
echo "Anthropic 最新的融资情况是多少？" |并行 cli 搜索 - --json
echo“研究问题” |并行 cli 研究运行 - --json
````

## 搜索

用于具有结构化结果的当前网络查找。

````bash
parallel-cli 搜索“Anthropic 最新的 AI 模型是什么？” --json
parallel-cli 搜索“Apple 的 SEC 文件”--include-domains sec.gov --json
parallel-cli 搜索“比特币价格” --after-date 2026-01-01 --max-results 10 --json
parallel-cli 搜索“最新浏览器基准测试”--mode one-shot --json
parallel-cli 搜索“AI 编码代理企业评论”--mode agentic --json
````

有用的约束：
- `--include-domains` 缩小可信来源范围
- `--exclude-domains` 去除嘈杂的域
- 用于新近度过滤的“--after-date”
- 当您需要更广泛的覆盖范围时使用“--max-results”

如果您期望后续问题，请保存输出：

````bash
parallel-cli 搜索“最新的 React 19 更改”--json -o /tmp/react-19-search.json
````

总结结果时：
- 以答案引导
- 包括日期、姓名和具体事实
- 仅引用返回的来源
- 避免发明 URL 或源标题

## 提取

用于从 URL 中提取干净的内容或降价。

````bash
并行 cli 提取 https://example.com --json
parallel-cli extract https://company.com --objective "查找定价信息" --json
并行 cli 提取 https://example.com --full-content --json
并行 cli 获取 https://example.com --json
````

当页面很宽并且您只需要一小部分信息时，请使用“--objective”。

## 深入研究

用于可能需要时间的更深入的多步骤研究任务。

常见的处理器层：
- `lite` / `base` 提供更快、更便宜的通行证
- `core` / `pro` 进行更彻底的综合
- 适合最繁重的研究工作的“ultra”

### 同步

````bash
并行 cli 研究运行 \
  “通过定价、模型支持和企业控制来比较领先的人工智能编码代理” \
  --处理器核心\
  --json
````

### 异步启动+轮询

````bash
并行 cli 研究运行 \
  “通过定价、模型支持和企业控制来比较领先的人工智能编码代理” \
  --处理器超\
  --无需等待\
  --json

parallel-cli 研究状态 trun_xxx --json
并行 cli 研究民意调查 trun_xxx --json
并行 cli 研究处理器 --json
````

### 上下文链接/后续

````bash
parallel-cli 研究运行“顶级人工智能编码代理是什么？” --json
并行 cli 研究运行 \
  “排名第一的企业提供哪些企业控制功能？” \
  --previous-interaction-id trun_xxx \
  --json
````

推荐的 OpenClaw 工作流程：
1. 使用 `--no-wait --json` 启动
2.捕获返回的运行/任务ID
3.如果用户想继续其他工作，继续前进
4.稍后调用`status`或`poll`
5. 总结最终报告并引用返回来源

## 丰富

当用户有 CSV/JSON/表格输入并希望从网络研究中推断出其他列时使用。

### 建议专栏

````bash
parallel-cli丰富建议“找到CEO和年收入”--json
````

### 规划配置

````bash
并行 cli 丰富计划 -o config.yaml
````

### 内联数据

````bash
并行 cli 丰富运行 \
  --data '[{"company": "Anthropic"}, {"company": "Mistral"}]' \
  --intent“查找总部和员工人数”\
  --json
````

### 非交互式文件运行

````bash
并行 cli 丰富运行 \
  --源类型 csv \
  --来源公司.csv \
  --目标丰富.csv \
  --source-columns '[{"name": "公司", "description": "公司名称"}]' \
  --意图“寻找首席执行官和年收入”
````

### YAML 配置运行

````bash
并行 cli 丰富运行 config.yaml
````

### 状态/投票

````bash
Parallel-cli 丰富状态 <task_group_id> --json
并行-cli丰富民意调查<task_group_id> --json
````

非交互操作时，使用显式 JSON 数组进行列定义。
在报告成功之前验证输出文件。

## 查找全部

当用户想要发现的数据集而不是简短的答案时，用于网络规模的实体发现。

````bash
parallel-cli findall run“查找具有企业产品的 AI 编码代理初创公司”--json
parallel-cli findall 运行“医疗保健领域的人工智能初创公司”-n 25 --json
Parallel-cli findall status <run_id> --json
并行 cli findall poll <run_id> --json
Parallel-cli findall 结果 <run_id> --json
Parallel-cli findall schema <run_id> --json
````

当用户想要一组已发现的实体可以在以后进行审查、过滤或丰富时，这比普通搜索更合适。

## 监控

用于随时间的持续变化检测。

````bash
并行 cli 监控列表 --json
并行 cli 监视器获取 <monitor_id> --json
parallel-cli 监控事件 <monitor_id> --json
parallel-cli 监视器删除 <monitor_id> --json
````

创作通常是敏感部分，因为节奏和交付很重要：

````bash
并行 cli 监视器创建 --help
````

当用户想要重复跟踪页面或源而不是一次性获取时，请使用此选项。

## 推荐的 OpenClaw 使用模式

### 快速回答并引用
1. 运行 `parallel-cli search ... --json`
2. 解析标题、URL、日期、摘录
3. 仅使用返回 URL 的内联引用进行总结

### URL调查
1. 运行 `parallel-cli extract URL --json`
2. 如果需要，使用 `--objective` 或 `--full-content` 重新运行
3.引用或总结提取的markdown

### 漫长的研究工作流程
1. 运行 `parallel-cli Research run ... --no-wait --json`
2. 存储返回的ID
3. 继续其他工作或定期轮询
4. 总结最终报告并附上引文

### 结构化丰富工作流程
1. 检查输入文件和列
2. 使用“丰富建议”或提供显式丰富列
3.运行`丰富运行`
4. 如果需要，轮询是否完成
5. 在报告成功之前验证输出文件

## 错误处理和退出代码

CLI 记录了这些退出代码：
- ‘0’成功
- `2` 错误输入
- `3` 身份验证错误
- `4` API 错误
- `5` 超时

如果遇到身份验证错误：
1.检查`parallel-cli auth`
2. 确认 `PARALLEL_API_KEY` 或运行 `parallel-cli login` / `parallel-cli login --device`
3. 验证 `parallel-cli` 位于 `PATH` 上

## 维护

检查当前的身份验证/安装状态：

````bash
并行 cli 身份验证
并行 cli --帮助
````

更新命令：

````bash
并行 cli 更新
pip install --升级并行网络工具
并行 cli 配置自动更新检查关闭
````

## 陷阱

- 不要省略 `--json` 除非用户明确想要人类格式的输出。
- 不要引用 CLI 输出中不存在的来源。
- “登录”可能需要 PTY/浏览器交互。
- 对于短任务更喜欢前台执行；不要过度使用后台进程。
- 对于大型结果集，请将 JSON 保存到“/tmp/*.json”，而不是将所有内容都填充到上下文中。
- 当OpenClaw原生工具已经足够的时候，不要默默选择Para​​llel。
- 请记住，这是一个供应商工作流程，通常需要帐户身份验证和免费套餐之外的付费使用。