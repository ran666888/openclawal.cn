---
sidebar_position: 8
title: "Memory Provider Plugins"
description: "如何为 OpenClaw 构建记忆提供商插件"
---
# 构建内存提供程序插件

内存提供程序插件为 OpenClaw 提供了超出内置 MEMORY.md 和 USER.md 的持久跨会话知识。本指南介绍了如何构建一个。

:::提示
内存提供程序是两种**提供程序插件**类型之一。另一个是[Context Engine Plugins](/developer-guide/context-engine-plugin)，它取代了内置的上下文压缩器。两者都遵循相同的模式：单选、配置驱动、通过“hermes 插件”管理。
:::

## 目录结构

每个内存提供者都位于`plugins/memory/<name>/`中：

````
插件/内存/my-provider/
├── __init__.py # MemoryProvider 实现 + register() 入口点
├──plugin.yaml # 元数据（名称、描述、挂钩）
└── README.md # 设置说明、配置参考、工具
````

## MemoryProvider ABC

您的插件实现了“agent/memory_provider.py”中的“MemoryProvider”抽象基类：

````蟒蛇
从 agent.memory_provider 导入 MemoryProvider

类 MyMemoryProvider(MemoryProvider):
    @属性
    def 名称(自身) -> str:
        返回“我的提供商”

    def is_available(self) -> bool:
        """检查此提供商是否可以激活。没有网络呼叫。"""
        返回 bool(os.environ.get("MY_API_KEY"))

    def 初始化(self, session_id: str, **kwargs) -> 无:
        """在代理启动时调用一次。

        kwargs 始终包括：
          hermes_home (str)：活动 HERMES_HOME 路径。用于存储。
        ”“”
        self._api_key = os.environ.get("MY_API_KEY", "")
        self._session_id = session_id

    # ...实现剩余的方法
````

## 所需方法

### 核心生命周期

|方法|当被呼叫时 |必须实施吗？ |
|--------|---------|-----------------|
| `名称`（属性）|永远 | **是** |
| `is_available()` |代理初始化，激活前 | **是** — 没有网络调用 |
| `初始化（session_id，**kwargs）` |代理启动| **是** |
| `get_tool_schemas()` | init之后，用于工具注入| **是** |
| `handle_tool_call(工具名称, args, **kwargs)` |当代理使用您的工具时 | **是**（如果您有工具）|

### 配置

|方法|目的|必须实施吗？ |
|--------|---------|-----------------|
| `get_config_schema()` |声明“hermes 内存设置”的配置字段 | **是** |
| `save_config（值，hermes_home）` |将非秘密配置写入本机位置 | **是**（除非仅限 env-var）|

### 可选挂钩

|方法|当被呼叫时 |使用案例|
|--------|------------|----------|
| `system_prompt_block()` |系统提示组装|静态提供商信息 |
| `预取（查询，*，session_id =“”）` |每次 API 调用之前 |返回回忆上下文 |
| `queue_prefetch(查询)` |每次转弯后 |为下一轮预热 |
| `sync_turn(用户, 助理, *, session_id="")` |每次完成转弯后 |持续对话 |
| `on_session_end（消息）` |对话结束 |最终萃取/冲洗|
| `on_pre_compress(消息)` |上下文压缩之前 |在丢弃之前保存见解 |
| `on_memory_write（操作，目标，内容）` |内置内存写入|镜像到您的后端 |
| `关闭()` |进程退出 |清理连接 |

## 配置架构

`get_config_schema()` 返回 `hermes memory setup` 使用的字段描述符列表：

````蟒蛇
def get_config_schema(自身):
    返回[
        {
            “密钥”：“api_key”，
            "description": "我的提供商 API 密钥",
            "secret": True, # → 写入.env
            “必需”：确实，
            "env_var": "MY_API_KEY", # 显式环境变量名称
            "url": "https://my-provider.com/keys", # 从哪里获取
        },
        {
            “键”：“区域”，
            "description": "服务器区域",
            “默认”：“美国东部”，
            “选择”：[“美国东部”，“欧盟西部”，“亚太南部”]，
        },
        {
            “关键”：“项目”，
            "description": "项目标识符",
            “默认”：“爱马仕”，
        },
    ]
````

带有“secret: True”和“env_var”的字段转到“.env”。非秘密字段将传递给“save_config()”。

:::提示最小模式与完整模式
在“hermes 内存设置”期间会提示“get_config_schema()”中的每个字段。具有多种选项的提供商应保持架构最小化——仅包含用户**必须**配置的字段（API 密钥、所需的凭据）。在配置文件引用中记录可选设置（例如“$HERMES_HOME/myprovider.json”），而不是在安装过程中提示所有设置。这使设置向导保持快速，同时仍然支持高级配置。请参阅超级内存提供程序的示例 - 它仅提示输入 API 密钥；所有其他选项都位于“supermemory.json”中。
:::

## 保存配置

````蟒蛇
def save_config(self, 值: dict, hermes_home: str) -> 无:
    """将非秘密配置写入您的本地位置。"""
    导入 json
    从 pathlib 导入路径
    config_path = 路径(hermes_home) / "my-provider.json"
    config_path.write_text(json.dumps(值，缩进=2))
````

对于仅限 env-var 的提供程序，保留默认的无操作。

## 插件入口点

````蟒蛇
def 寄存器(ctx) -> 无:
    """由内存插件发现系统调用。"""
    ctx.register_memory_provider(MyMemoryProvider())
````

## 插件.yaml

````yaml
名称：我的提供商
版本：1.0.0
描述：“该提供商所做的事情的简短描述。”
挂钩：
  - on_session_end # 列出你实现的钩子
````

## 线程合约

**`sync_turn()` 必须是非阻塞的。** 如果您的后端有延迟（API 调用、LLM 处理），请在守护线程中运行工作：

````蟒蛇
defsync_turn(self, user_content, Assistant_content, *, session_id="", messages=None):
    def_sync():
        尝试：
            self._api.ingest(user_content, Assistant_content, session_id=session_id, messages=messages)
        除了异常 e：
            logger.warning("同步失败: %s", e)

    如果 self._sync_thread 和 self._sync_thread.is_alive():
        self._sync_thread.join(超时=5.0)
    self._sync_thread = threading.Thread(target=_sync, daemon=True)
    self._sync_thread.start()
````

`messages` 是可选的 OpenAI 风格的对话上下文，截至完成
转。如果存在，它包括用户/助手消息、助手工具调用、
和工具结果消息。不需要原始回合上下文的提供者可以省略
`messages` 参数；爱马仕将继续传承传承
签名。

云提供商应记录“消息”的哪些部分发送到设备外。
工具调用和工具结果可能包含文件路径、命令输出或其他
工作区数据。

## 配置文件隔离

所有存储路径**必须**使用来自`initialize()`的`hermes_home` kwarg，而不是硬编码的`~/.hermes`：

````蟒蛇
# 正确 — 配置文件范围
从 Hermes_constants 导入 get_hermes_home
data_dir = get_hermes_home() / “我的提供商”

# 错误 — 在所有配置文件中共享
data_dir = Path("~/.hermes/my-provider").expanduser()
````

## 测试

有关端到端模式，请参阅“tests/agent/test_memory_provider.py”和相邻内存测试（“tests/agent/test_memory_session_switch.py”、“tests/agent/test_memory_user_id.py”、“tests/run_agent/test_memory_provider_init.py”）。

````蟒蛇
从agent.memory_manager导入MemoryManager

mgr = 内存管理器()
mgr.add_provider(my_provider)
mgr.initialize_all(session_id="test-1", platform="cli")

# 测试工具路由
结果 = mgr.handle_tool_call("my_tool", {"action": "add", "content": "test"})

# 测试生命周期
mgr.sync_all("用户消息", "助理消息")
mgr.on_session_end([])
mgr.shutdown_all()
````

## 添加 CLI 命令

内存提供者插件可以注册自己的 CLI 子命令树（例如“hermes my-provider status”、“hermes my-provider config”）。这使用基于约定的发现系统 - 无需更改核心文件。

### 它是如何工作的

1. 将 `cli.py` 文件添加到您的插件目录中
2.定义一个`register_cli(subparser)`函数来构建argparse树
3.内存插件系统在启动时通过`discover_plugin_cli_commands()`发现它
4. 您的命令出现在 `hermes <provider-name> <subcommand>` 下

**活动提供者门控：** 仅当您的提供者是配置中的活动“memory.provider”时，您的 CLI 命令才会出现。如果用户尚未配置您的提供程序，您的命令将不会显示在“hermes --help”中。

### 示例

````蟒蛇
# 插件/内存/my-provider/cli.py

def my_command(args):
    """由 argparse 调度的处理程序。"""
    sub = getattr(args, "my_command", 无)
    如果子==“状态”：
        print("提供商处于活动状态并已连接。")
    elif sub ==“配置”：
        print("显示配置...")
    其他：
        print("用法：hermes my-provider <status|config>")

def register_cli(subparser) -> 无：
    """构建 Hermes my-provider argparse 树。

    在 argparse 设置时由 discovery_plugin_cli_commands() 调用。
    ”“”
    subs = subparser.add_subparsers(dest="my_command")
    subs.add_parser("status", help="显示提供商状态")
    subs.add_parser("config", help="显示提供商配置")
    subparser.set_defaults(func=my_command)
````

### 参考实现

有关包含 13 个子命令、跨配置文件管理 (`--target-profile`) 和配置读/写的完整示例，请参阅 `plugins/memory/honcho/cli.py`。

### 使用 CLI 的目录结构

````
插件/内存/my-provider/
├── __init__.py # MemoryProvider实现+register()
├──plugin.yaml # 元数据
├── cli.py # register_cli(subparser) — CLI 命令
└── README.md # 设置说明
````

## 单一提供商规则

一次只能有**一个**外部内存提供程序处于活动状态。如果用户尝试注册第二个，MemoryManager 将拒绝它并发出警告。这可以防止工具架构膨胀和后端冲突。