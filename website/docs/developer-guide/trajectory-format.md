# 轨迹格式

OpenClaw 以兼容 ShareGPT 的 JSONL 格式保存对话轨迹
用作训练数据、调试工件和强化学习数据集。

源文件：`agent/trajectory.py`、`run_agent.py`（搜索`_save_trajectory`）、`batch_runner.py`


## 文件命名约定

轨迹被写入当前工作目录中的文件中：

|文件|当 |
|------|------|
| `trajectory_samples.jsonl` |成功完成的对话 (`completed=True`) |
| `failed_trajectories.jsonl` |对话失败或被中断 (`completed=False`) |

批处理运行程序（`batch_runner.py`）每批写入自定义输出文件
（例如，“batch_001_output.jsonl”）以及其他元数据字段。

您可以通过“save_trajectory()”中的“filename”参数覆盖文件名。


## JSONL 条目格式

文件中的每一行都是一个独立的 JSON 对象。有两种变体：

### CLI/交互式格式（来自`_save_trajectory`）

```json
{
  “对话”：[...]，
  “时间戳”：“2026-03-30T14：22：31.456789”，
  “模型”：“人类/克劳德-sonnet-4.6”，
  “已完成”：正确
}
````

### Batch Runner 格式（来自 `batch_runner.py`）

```json
{
  “提示索引”：42，
  “对话”：[...]，
  “元数据”：{“prompt_source”：“gsm8k”，“难度”：“困难”}，
  “完成”：真实，
  “部分”：假，
  “api_calls”：7，
  “toolsets_used”：[“code_tools”，“file_tools”]，
  “工具统计”：{
    "terminal": {"count": 3, "success": 3, "failure": 0},
    "read_file": {"count": 2, "成功": 2, "失败": 0},
    “write_file”：{“计数”：0，“成功”：0，“失败”：0}
  },
  “工具错误计数”：{
    “终端”：0，
    “读取文件”：0，
    “写入文件”：0
  }
}
````

`tool_stats` 和 `tool_error_counts` 字典被标准化为包括
所有可能的工具（来自“model_tools.TOOL_TO_TOOLSET_MAP”）的默认值为零，
确保 HuggingFace 数据集加载的条目之间的架构一致。


## 对话数组（ShareGPT 格式）

`conversations` 数组使用 ShareGPT 角色约定：

| API 角色 | ShareGPT `来自` |
|----------|-----------------|
|系统| `“系统”` |
|用户 | `“人类”` |
|助理 | `"gpt"` |
|工具| `“工具”` |

### 完整示例

```json
{
  “对话”：[
    {
      “来自”：“系统”，
      "value": "您是一个调用 AI 模型的函数。在 <tools> </tools> XML 标记中为您提供了函数签名。您可以调用一个或多个函数来协助用户查询。如果可用的工具与协助用户查询无关，则只需以自然对话语言进行响应。不要假设要插入到函数中的值。调用并执行函数后，将在 <tool_response> </tool_response> XML 标记中为您提供函数结果。以下是可用工具:\n<工具>\n[{\"name\": \"terminal\", \"description\": \"执行 shell 命令\", \"parameters\": {\"type\": \"object\", \"properties\": {\"command\": {\"type\": \"string\"}}}, \"required\": null}]\n</tools>\n对于每个函数调用返回一个 JSON 对象，每个对象具有以下 pydantic 模型 json 架构：\n{'title': 'FunctionCall', 'type': 'object', 'properties': {'name': {'title': 'Name', 'type': 'string'}, 'arguments': {'title': 'Arguments', 'type': 'object'}}, 'required': ['name', 'arguments']}\n每个函数调用都应包含在 <tool_call> </tool_call> XML 标记内。\n示例:\n<tool_call>\n{'name': <function-name>,'arguments': <args-dict>}\n</tool_call>"
    },
    {
      “来自”：“人类”，
      "value": "安装了什么Python版本？"
    },
    {
      “来自”：“gpt”，
      "value": "<think>\n用户想知道 Python 版本。我应该运行 python3 --version。\n</think>\n<tool_call>\n{\"name\": \"terminal\", \"arguments\": {\"command\": \"python3 --version\"}}\n</tool_call>"
    },
    {
      “来自”：“工具”，
      "value": "<tool_response>\n{\"tool_call_id\": \"call_abc123\", \"name\": \"terminal\", \"content\": \"Python 3.11.6\"}\n</tool_response>"
    },
    {
      “来自”：“gpt”，
      "value": "<think>\n已获取版本。我现在可以回答用户。\n</think>\n此系统上安装了 Python 3.11.6。"
    }
  ],
  “时间戳”：“2026-03-30T14：22：31.456789”，
  “模型”：“人类/克劳德-sonnet-4.6”，
  “已完成”：正确
}
````


## 规范化规则

### 推理内容标记

轨迹转换器将所有推理标准化为“<think>”标签，无论
该模型最初是如何产生的：

1. **本机思维标记**（来自提供商的“msg["reasoning"]”字段，例如
   Anthropic、OpenAI o 系列）：包装为 `<think>\n{reasoning}\n</think>\n`
   并放在内容之前。

2. **REASONING_SCRATCHPAD XML**（当本机思维被禁用并且模型
   通过系统提示指示的 XML 的原因）：`<REASONING_SCRATCHPAD>` 标签是
   通过“convert_scratchpad_to_think()”转换为“<think>”。

3. **空思考块**：每个`gpt`回合都保证有一个`<think>`
   块。如果没有产生推理，则插入一个空块：
   `<think>\n</think>\n` — 这确保了训练数据的格式一致。

### 工具调用规范化

来自 API 格式的工具调用（使用“tool_call_id”、函数名称、参数为
JSON 字符串）转换为 XML 包装的 JSON：

````
<工具调用>
{“名称”：“终端”，“参数”：{“命令”：“ls -la”}}
</工具调用>
````

- 参数从 JSON 字符串解析回对象（不是双重编码）
- 如果 JSON 解析失败（不应该发生 - 在对话期间验证），
  使用空的“{}”并记录警告
- 一个助手轮中的多个工具调用会产生多个“<tool_call>”块
  在单个“gpt”消息中

### 工具响应标准化

助理消息后的所有工具结果都被分组到一个“工具”中
转而使用 XML 包装的 JSON 响应：

````
<工具响应>
{"tool_call_id": "call_abc123", "name": "终端", "content": "在此输出"}
</工具响应>
````

- 如果工具内容看起来像 JSON（以“{”或“[”开头），则会对其进行解析，以便
  内容字段包含 JSON 对象/数组而不是字符串
- 多个工具结果在一条消息中以换行符连接
- 工具名称按位置与父助手的“tool_calls”进行匹配
  数组

### 系统消息

系统消息是在保存时生成的（不是从对话中获取的）。
它遵循 OpenClaw 函数调用提示模板：

- 解释函数调用协议的序言
- `<tools>` XML 块包含 JSON 工具定义
- `FunctionCall` 对象的架构参考
- `<工具调用>` 示例

工具定义包括“名称”、“描述”、“参数”和“必需”
（设置为“null”以匹配规范格式）。


## 加载轨迹

轨迹是标准 JSONL — 使用任何 JSON 行读取器加载：

````蟒蛇
导入 json

def load_trajectories(路径: str):
    """从 JSONL 文件加载轨迹条目。"""
    条目 = []
    打开（路径，“r”，编码=“utf-8”）作为f：
        对于 f 中的行：
            线 = 线.strip()
            如果行：
                条目.append(json.loads(line))
    返回条目

# 仅过滤成功完成的情况
成功 = [e for e in load_trajectories("trajectory_samples.jsonl")
              if e.get("完成")]

# 只提取对话进行训练
Training_data = [e[“对话”] for e 成功]
````

### 加载 HuggingFace 数据集

````蟒蛇
从数据集导入load_dataset

ds = load_dataset("json", data_files="trajectory_samples.jsonl")
````

标准化的“tool_stats”模式确保所有条目都具有相同的列，
防止数据集加载期间出现箭头架构不匹配错误。


## 控制轨迹保存

在 CLI 中，轨迹保存由以下各项控制：

````yaml
# 配置.yaml
代理：
  save_trajectories: true # 默认值: false
````

或者通过“--save-trajectories”标志。当代理初始化时
`save_trajectories=True`，最后调用`_save_trajectory()`方法
每个对话回合。

批处理运行器始终保存轨迹（这是其主要目的）。

所有回合中推理为零的样本将被自动丢弃
批处理运行器以避免非推理示例污染训练数据。