---
sidebar_position: 18
title: "Browser CDP Supervisor"
description: "How OpenClaw detects and responds to native JS dialogs and interacts with cross-origin iframes via a persistent CDP connection."
---
# 浏览器 CDP 主管

CDP 主管弥补了 OpenClaw 浏览器工具中两个长期存在的空白：

1. **原生 JS 对话框** (`alert`/`confirm`/`prompt`/`beforeunload`) 阻止
   页面的 JS 线程。如果没有监督，代理人就无法知道
   对话框打开 - 后续工具调用挂起或抛出不透明错误。
2. **跨源 iframe (OOPIF)** 对顶层不可见
   `运行时.评估`。代理可以在 DOM 快照中看到 iframe 节点，但是
   如果没有附加 CDP 会话，则无法在其中单击、键入或评估
   儿童目标。

主管通过将持久的 WebSocket 保存到后端来解决这两个问题
每个浏览器任务的 CDP 端点，显示待处理的对话框和框架结构
进入“browser_snapshot”，并公开“browser_dialog”工具以进行显式
回应。

## 后端支持

|后端 |对话框检测 |对话回应 |框架树| OOPIF `Runtime.evaluate` 通过 `browser_cdp(frame_id=...)` |
|---|---|---|---|---|
|本地 Chrome (`--remote-debugging-port`) / `/browser connect` | ✓ | ✓ 完整的工作流程 | ✓ | ✓ |
|浏览器库 | ✓（通过桥）| ✓ 完整的工作流程（通过桥）| ✓ | ✓ |
|卡莫福克斯| ✗ 无 CDP（仅 REST）| ✗ |部分通过 DOM 快照 | ✗ |

**Browserbase 怪癖。** Browserbase 的 CDP 代理在内部使用 Playwright 并
在大约 10 毫秒内自动关闭本机对话框，因此 `Page.handleJavaScriptDialog`
跟不上。主管通过注入桥接脚本
覆盖的`Page.addScriptToEvaluateOnNewDocument`
`window.alert`/`confirm`/`prompt` 使用同步 XHR 发送到魔法主机
（“hermes-dialog-bridge.invalid”）。 `Fetch.enable` 之前拦截了那些 XHR
他们接触网络 - 对话框变成“Fetch.requestPaused”事件
主管捕获，并通过“respond_to_dialog”实现
带有注入脚本解码的 JSON 主体的“Fetch.fulfillRequest”。

从页面的角度来看，“prompt()”仍然返回代理提供的
字符串。从代理的角度来看，它是相同的 `browser_dialog(action=...)`
API 无论哪种方式。

Camofox 不受支持 — 无 CDP 表面，仅 REST。

## 架构

### CDPSupervisor

每个 OpenClaw `task_id` 在后台守护线程中运行一个 `asyncio.Task`。
将持久的 WebSocket 保存到后端的 CDP 端点。维护：

- **对话框队列** — `List[PendingDialog]` 和 `{id, type, message, default_prompt, session_id, opening_at}`
- **框架树** — `Dict[frame_id, FrameInfo]` 具有父关系、URL、来源、是否跨域子会话
- **会话映射** — `Dict[session_id, SessionInfo]` 因此交互工具可以路由到正确的附加会话以进行 OOPIF 操作
- **最近控制台错误** — 用于诊断的最后 50 个环形缓冲区

订阅附件：

- `Page.enable` — `javascriptDialogOpening`、`frameAttached`、`frameNaviged`、`frameDetached`
- `Runtime.enable` — `executionContextCreated`、`consoleAPICalled`、`exceptionThrown`
- `Target.setAutoAttach {autoAttach: true, flatten: true}` — 显示子 OOPIF 目标；主管在每个上启用“Page”+“Runtime”

通过快照锁进行线程安全状态访问；工具处理程序（同步）读取
无需等待即可冻结快照。

### 生命周期

- **开始：** `SupervisorRegistry.get_or_start(task_id, cdp_url)` — 调用
  `browser_navigate`，Browserbase 会话创建，`/browser connect`。
  幂等。
- **停止：**会话拆除或“/浏览器断开连接”。取消异步
  任务，关闭 WebSocket，丢弃状态。
- **重新绑定：**如果 CDP URL 更改（用户重新连接到新的 Chrome），
  旧的主管被停止，新的主管被启动——状态永远不会被重用
  跨端点。

### 对话政策

可通过“browser.dialog_policy”下的“config.yaml”进行配置：

- **`must_respond`**（默认）- 捕获，在“browser_snapshot”中显示，等待
  用于显式的“browser_dialog(action=...)”调用。 300秒安全超时后
  没有响应，自动关闭并记录。防止有 bug 的代理停止运行
  永远。
- `auto_dismiss` — 立即记录并关闭；代理在之后看到它
  事实上通过“browser_snapshot”中的“browser_state”。
- `auto_accept` — 记录并接受（对于 `beforeunload` 很有用，其中
  工作流程希望干净利落地离开）。

策略是针对每个任务的；没有每个对话框的覆盖。

## 代理面

### `browser_dialog` 工具

````
browser_dialog（操作，prompt_text =无，dialog_id =无）
````

- `action="accept"` / `"dismiss"` → 响应指定的或唯一的待处理对话框（必需）
- `prompt_text=...` → 提供给 `prompt()` 对话框的文本
- `dialog_id=...` → 当多个对话排队时消除歧义（罕见）

工具仅用于响应。代理从“browser_snapshot”读取待处理的对话框
调用前输出。

### `browser_snapshot` 扩展

当主管时，向现有快照输出添加三个可选字段
附：

```json
{
  “pending_dialogs”：[
    {“id”：“d-1”，“type”：“alert”，“message”：“你好”，“opened_at”：1650000000.0}
  ],
  “最近的对话”：[
    {“id”：“d-1”，“类型”：“警报”，“消息”：“...”，“opened_at”：1650000000.0，
     “close_at”：1650000000.1，“close_by”：“远程”}
  ],
  “框架树”：{
    "top": {"frame_id": "FRAME_A", "url": "https://example.com/", "origin": "https://example.com"},
    “孩子们”：[
      {"frame_id": "FRAME_B", "url": "about:srcdoc", "is_oopif": false},
      {“frame_id”：“FRAME_C”，“url”：“https://ads.example.net/”，“is_oopif”：true，“session_id”：“SID_C”}
    ],
    “截断”：假
  }
}
````

- **`pending_dialogs`** — 当前阻塞页面 JS 线程的对话框。
  代理必须调用“browser_dialog(action=...)”来响应。清空
  Browserbase 因为他们的 CDP 代理会在大约 10 毫秒内自动关闭。

- **`recent_dialogs`** — 最多 20 个最近关闭的对话框的环形缓冲区
  `close_by` 标签：`"agent"`（我们回复），`"auto_policy"`（本地
  auto_dismiss/auto_accept), `"watchdog"` (must_respond 超时命中), 或
  “远程”（浏览器/后端对我们关闭了它，例如 Browserbase）。这是
  Browserbase 上的代理如何仍然了解所发生的情况。

- **`frame_tree`** — 包括跨域 (OOPIF) 子级的框架结构。
  上限为 30 个条目 + OOPIF 深度 2，以限制广告较多的快照大小
  页。当达到限制时，“truncated: true”就会出现；代理商需要
  完整的树可以使用“browser_cdp”和“Page.getFrameTree”。

其中任何一个都没有新的工具模式表面 - 代理读取它的快照
已经请求了。

### 可用性门控

两个表面都在 `_browser_cdp_check` 上进行门控（supervisor 只能在 CDP 运行时运行）
端点可达）。在 Camofox/无后端会话中，对话工具是
隐藏并且快照省略了新字段——没有架构膨胀。

## 跨域iframe交互

`browser_cdp(frame_id=...)` 路由 CDP 调用（特别是 `Runtime.evaluate`）
使用 OOPIF 的子级通过主管已连接的 WebSocket
`会话 ID`。代理从中选择frame_ids
`browser_snapshot.frame_tree.children[]` 其中 `is_oopif=true` 并传递它们
到“browser_cdp”。对于同源 iframe（无专用 CDP 会话），
代理使用顶层的 `contentWindow`/`contentDocument`
相反，“Runtime.evaluate”——主管显示了一个指向该问题的错误
当“frame_id”属于非 OOPIF 时回退。

在 Browserbase 上，这是 iframe 交互的唯一可靠路径 —
无状态 CDP 连接（根据“browser_cdp”调用打开）命中签名 URL
过期，而主管的长期连接保持有效会话。

## 文件布局

- `tools/browser_supervisor.py` — `CDPSupervisor`、`SupervisorRegistry`、`PendingDialog`、`FrameInfo`
- `tools/browser_dialog_tool.py` — `browser_dialog` 工具处理程序
- `tools/browser_tool.py` — `browser_navigate` 启动挂钩、`browser_snapshot` 合并、`/browser connect` 重新附加、`_cleanup_browser_session` 拆卸
- `toolsets.py` — 在 `browser`、`hermes-acp`、`hermes-api-server` 和核心工具集中注册 `browser_dialog`（基于 CDP 可访问性）
- `hermes_cli/config.py` — `browser.dialog_policy` 和 `browser.dialog_timeout_s` 默认值

## 非目标

- Camofox 的检测/交互（上游差距；单独跟踪）
- 将对话框/框架事件实时传输给用户（需要网关挂钩）
- 跨会话保留对话历史记录（仅限内存中）
- 每个 iframe 对话策略（代理可以通过“dialog_id”表达这一点）
- 替换“browser_cdp”——它仍然是长尾（cookie、视口、网络节流）的逃生舱口

## 测试

单元测试（`tests/tools/test_browser_supervisor.py`）使用 asyncio 模拟 CDP
足够使用协议来执行所有状态转换的服务器：
附加、启用、导航、对话框触发、对话框关闭、框架附加/分离、
子目标附加，会话拆卸。真正的后端E2E（浏览器库+本地
Chromium 系列浏览器）是手动的 — 通过“/browser connect”连接到
实时 Chromium 系列浏览器并运行所描述的对话框/框架测试用例
上面。