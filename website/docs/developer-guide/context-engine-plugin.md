---
sidebar_position: 9
title: "Context Engine Plugins"
description: "How to build a context engine plugin that replaces the built-in ContextCompressor"
---
# 构建上下文引擎插件

上下文引擎插件用管理对话上下文的替代策略替换了内置的“ContextCompressor”。例如，无损上下文管理（LCM）引擎构建知识DAG而不是有损摘要。

## 它是如何工作的

代理的上下文管理构建在“ContextEngine” ABC (“agent/context_engine.py”) 之上。内置的“ContextCompressor”是默认实现。插件引擎必须实现相同的接口。

一次只能有**一个**上下文引擎处于活动状态。选择是配置驱动的：

````yaml
# 配置.yaml
上下文：
  engine: "compressor" # 默认内置
  engine: "lcm" # 激活名为“lcm”的插件引擎
````

插件引擎**永远不会自动激活** - 用户必须明确将“context.engine”设置为插件的名称。

## 目录结构

每个上下文引擎都位于`plugins/context_engine/<name>/`中：

````
插件/context_engine/lcm/
├── __init__.py # 导出ContextEngine子类
├──plugin.yaml # 元数据（名称、描述、版本）
└── ... # 您的引擎需要的任何其他模块
````

## ContextEngine ABC

您的引擎必须实现这些**必需的**方法：

````蟒蛇
从agent.context_engine导入ContextEngine

LCMEngine 类（ContextEngine）：

    @属性
    def 名称(自身) -> str:
        """短标识符，例如'lcm'。必须匹配 config.yaml 值。"""
        返回“lcm”

    def update_from_response(self, 用法: dict) -> 无:
        """在每次 LLM 调用后使用用法字典调用。

        更新 self.last_prompt_tokens、self.last_completion_tokens、
        来自响应的 self.last_total_tokens。
        ”“”

    def should_compress(self,prompt_tokens: int = None) -> bool:
        “”“如果本轮应该触发压缩，则返回 True。”“”

    def 压缩（自我，消息：列表，current_tokens：int = None，
                 focus_topic: str = None) -> 列表:
        """压缩消息列表并返回一个新的（可能更短）列表。

        返回的列表必须是有效的 OpenAI 格式的消息序列。

        ``focus_topic`` 是手册中的可选主题字符串
        ``/压缩 <焦点>``;支持引导压缩的发动机应该
        优先保留与其相关的信息，其他人可能会忽略它。
        ”“”
````

### 你的引擎必须维护的类属性

代理直接读取这些内容以进行显示和记录：

````蟒蛇
最后提示令牌：int = 0
最后完成令牌：int = 0
最后的总令牌数：int = 0
Threshold_tokens: int = 0 # 当压缩触发时
context_length: int = 0 # 模型的完整上下文窗口
Compression_count: int = 0 # compress() 运行了多少次
````

### 可选方法

这些在 ABC 中有合理的默认值。根据需要覆盖：

|方法|默认 |覆盖时|
|--------|---------|--------------|
| `on_session_start(session_id, **kwargs)` |无操作 |您需要加载持久状态（DAG、DB） |
| `on_session_end(session_id, messages)` |无操作 |您需要刷新状态，关闭连接 |
| `on_session_reset()` |重置令牌计数器 |您需要清除每个会话的状态 |
| `update_model（模型，context_length，...）` |更新 context_length + 阈值 |您需要重新计算型号切换预算 |
| `get_tool_schemas()` |返回 `[]` |您的引擎提供代理可调用工具（例如“lcm_grep”）|
| `handle_tool_call(name, args, **kwargs)` |返回错误 JSON |您实施工具处理程序 |
| `should_compress_preflight（消息）` |返回“假”|您可以进行廉价的 API 调用前估算 |
| `get_status()` |标准令牌/阈值字典 |您有要公开的自定义指标 |

## 引擎工具

上下文引擎可以公开代理直接调用的工具。从 `get_tool_schemas()` 返回模式并在 `handle_tool_call()` 中处理调用：

````蟒蛇
def get_tool_schemas(self):
    返回[{
        “名称”：“lcm_grep”，
        "description": "搜索上下文知识图谱",
        “参数”：{
            “类型”：“对象”，
            “属性”：{
                "query": {"type": "string", "description": "搜索查询"}
            },
            “必需”：[“查询”]，
        },
    }]

def handle_tool_call(self, name, args, **kwargs):
    如果名称==“lcm_grep”：
        结果 = self._search_dag(args["查询"])
        返回 json.dumps({"结果": 结果})
    return json.dumps({"error": f"未知工具: {name}"})
````

引擎工具在启动时注入到代理的工具列表中并自动调度 - 无需注册表注册。

## 注册

### 通过目录（推荐）

将您的引擎放在“plugins/context_engine/<name>/”中。 `__init__.py` 必须导出 `ContextEngine` 子类。发现系统自动找到并实例化它。

### 通过通用插件系统

通用插件还可以注册上下文引擎：

````蟒蛇
def 寄存器(ctx):
    引擎 = LCMEngine(context_length=200000)
    ctx.register_context_engine(引擎)
````

只能注册一台引擎。尝试注册的第二个插件被拒绝并出现警告。

## 生命周期

````
1.引擎实例化（插件加载或目录发现）
2. on_session_start() — 对话开始
3. update_from_response() — 每次 API 调用之后
4. should_compress() — 每轮检查
5. compress()——当should_compress()返回True时调用
6. on_session_end() — 会话边界（CLI 退出、/reset、网关到期）
````

在“/new”或“/reset”上调用“on_session_reset()”以清除每个会话状态，而无需完全关闭。

## 配置

用户通过 `hermes plugins` → Provider Plugins → Context Engine 选择您的引擎，或者通过编辑 `config.yaml`：

````yaml
上下文：
  engine: "lcm" # 必须与引擎的名称属性匹配
````

“compression”配置块（“compression.threshold”、“compression.protect_last_n”等）特定于内置“ContextCompressor”。如果需要，您的引擎应该定义自己的配置格式，在初始化期间从“config.yaml”读取。

## 测试

````蟒蛇
从agent.context_engine导入ContextEngine

def test_engine_satisfies_abc():
    引擎 = YourEngine(context_length=200000)
    断言 isinstance(引擎, ContextEngine)
    断言engine.name ==“你的名字”

def test_compress_returns_valid_messages():
    引擎 = YourEngine(context_length=200000)
    msgs = [{“角色”：“用户”，“内容”：“你好”}]
    结果 = engine.compress(msgs)
    断言 isinstance(结果，列表)
    断言所有（结果中 m 的“角色”）
````

有关完整的 ABC 合约测试套件，请参阅“tests/agent/test_context_engine.py”。

## 另请参阅

- [上下文压缩和缓存](/developer-guide/context-compression-and-caching) — 内置压缩器的工作原理
- [Memory Provider Plugins](/developer-guide/memory-provider-plugin) — 类似的内存单选插件系统
- [Plugins](/user-guide/features/plugins) — 一般插件系统概述