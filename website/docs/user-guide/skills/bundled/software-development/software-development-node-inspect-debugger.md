---
title: "Node Inspect Debugger — Debug Node"
sidebar_label: "Node Inspect Debugger"
description: "Debug Node"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 节点检查调试器

通过 --inspect + Chrome DevTools 协议 CLI 调试 Node.js。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/软件开发/节点检查调试器` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `调试`、`nodejs`、`node-inspect`、`cdp`、`断点`、`ui-tui` |
|相关技能| [`系统调试`](/docs/user-guide/skills/bundled/software-development/software-development-systematic-debugging)，[`python-debugpy`](/docs/user-guide/skills/bundled/software-development/software-development-python-debugpy)，`debugging-hermes-tui-commands` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Node.js 检查调试器

## 概述

当“console.log”不够时，可以从终端以编程方式驱动 Node 的内置 V8 检查器。您可以在暂停的帧中获得真正的断点、单步进入/越过/退出、调用堆栈遍历、本地/闭包范围转储以及任意表达式求值。

两种工具，选其一：

- **`节点检查`** — 内置、零安装、CLI REPL。最适合快速戳。
- **`ndb` / CDP 通过 `chrome-remote-interface`** — 可从 Node/Python 编写脚本；当您想要自动执行许多断点、收集运行期间的状态或从代理循环中进行非交互调试时，这是最好的选择。

**首先首选“节点检查”。**它始终可用并且 REPL 速度很快。

## 何时使用

- 节点测试失败，您需要查看中间状态
- ui-tui 崩溃或行为错误，并且您想要检查 React/Ink 状态预渲染
- tui_gateway 子进程（`_SlashWorker`、PTY 桥工作器）行为不当
- 您需要检查闭包中“console.log”在不修补的情况下无法到达的值
- Perf：附加到正在运行的进程以捕获 CPU 配置文件或堆快照

**不要用于：**`console.log`在一分钟内解决的问题。断点驱动调试较重；当回报真实时使用它。

## 快速参考：`节点检查` REPL

启动在第一行暂停：

````bash
节点检查路径/to/script.js
# 或使用 tsx
节点 --inspect-brk $(which tsx) 路径/to/script.ts
````

`debug>` 提示接受：

|命令|行动|
|---|---|
| `c` 或 `cont` |继续 |
| `n` 或 `下一个` |跨过|
| `s` 或 `step` |走进|
| `o` 或 `out` |走出去|
| `暂停` |暂停运行代码|
| `sb('file.js', 42)` |在 file.js 第 42 行设置断点 |
| `sb(42)` |在当前文件的第 42 行设置断点 |
| `sb('函数名')` |调用函数时中断 |
| `cb('file.js', 42)` |清除断点|
| `断点` |列出所有断点 |
| `bt` |回溯（调用堆栈）|
| `列表（5）` |显示当前位置周围的 5 行源代码 |
| `watch('expr')` |每次暂停时评估 expr |
| `观察者` |显示观看的表情 |
| `repl` |进入当前范围内的 REPL（Ctrl+C 退出 REPL）|
| `执行表达式` |计算表达式一次 |
| `重新启动` |重启脚本|
| `杀` |杀死脚本 |
| `.exit` |退出调试器 |

**在 `repl` 子模式中：** 输入任何 JS 表达式，包括访问局部变量/闭包变量。 `Ctrl+C` 退出回到 `debug>`。

## 附加到正在运行的进程

当进程已在运行时（例如长期运行的开发服务器或 TUI 网关）：

````bash
# 1. 发送 SIGUSR1 以在现有进程上启用检查器
杀死 -SIGUSR1 <pid>
# 节点打印：调试器正在监听 ws://127.0.0.1:9229/<uuid>

# 2. 连接调试器 CLI
节点检查 -p <pid>
# 或通过 URL
节点检查 ws://127.0.0.1:9229/<uuid>
````

要从头开始与检查员一起启动流程：

````bash
node --inspect script.js # 监听 127.0.0.1:9229，继续运行
node --inspect-brk script.js # 监听并在第一行暂停
node --inspect=0.0.0.0:9230 script.js # 自定义主机:端口
````

对于通过 tsx 的 TypeScript：

````bash
节点 --inspect-brk --import tsx script.ts
# 或更旧的 tsx
节点 --inspect-brk -r tsx/cjs script.ts
````

## 程序化 CDP（从终端编写脚本）

当您想要自动化时 - 设置许多断点、捕获作用域状态、编写重现脚本 - 使用“chrome-remote-interface”：

````bash
npm i -g chrome-remote-interface # 或项目本地
# 开始你的目标：
节点 --inspect-brk=9229 target.js &
````

驱动程序脚本（另存为“/tmp/cdp-debug.js”）：

```javascript
const CDP = require('chrome-remote-interface');

（异步（）=> {
  const client = 等待 CDP({ 端口: 9229 });
  const { 调试器，运行时 } = 客户端；

  Debugger.paused(async ({ callFrames, Reason }) => {
    const top = callFrames[0];
    console.log(`暂停：${reason} @ ${top.url}:${top.location.lineNumber + 1}`);

    // 本地人的步行范围
    for (top.scopeChain 的 const 范围) {
      if (scope.type === 'local' ||scope.type === 'closure') {
        const { 结果 } = 等待 Runtime.getProperties({
          objectId: 范围.object.objectId,
          自己的属性：真实，
        });
        for (结果的 const p) {
          console.log(` ${scope.type}.${p.name} =`, p.value?.value ?? p.value?.description);
        }
      }
    }

    // 计算暂停帧中的表达式
    const { 结果 } = 等待 Debugger.evaluateOnCallFrame({
      callFrameId: top.callFrameId,
      表达式： 'typeof state !== "undefined" ? JSON.stringify(state) : "n/a"',
    });
    console.log('state =', result.value ?? result.description);

    等待调试器.resume();
  });

  等待运行时.enable();
  等待调试器.enable();

  // 通过 URL 正则表达式 + 行设置断点
  等待 Debugger.setBreakpointByUrl({
    urlRegex: '.*app\\.tsx$',
    lineNumber: 119, // 0 索引
    列数: 0,
  });

  等待 Runtime.runIfWaitingForDebugger();
})();
````

运行它：

````bash
节点/tmp/cdp-debug.js
````

OpenClaw 特定说明：“chrome-remote-interface”不在“ui-tui/package.json”中。如果您不想弄脏项目，请将其安装到一次性位置：

````bash
mkdir -p /tmp/cdp-tools && cd /tmp/cdp-tools && npm i chrome-remote-interface
NODE_PATH=/tmp/cdp-tools/node_modules 节点 /tmp/cdp-debug.js
````

## 调试 OpenClaw ui-tui

TUI 是由 Ink + tsx 构建的。两种常见场景：

### 在 dev 下调试单个 Ink 组件

`ui-tui/package.json` 有 `npm run dev` (tsx --watch)。通过直接运行 tsx 添加 `--inspect-brk`：

````bash
cd /home/bb/hermes-agent/ui-tui
npm run build # 生成 dist/ 一次，因此第一次加载时不需要转译
节点 --inspect-brk dist/entry.js
# 在另一个终端中：
节点检查 -p <节点 pid>
````

然后在`debug>`里面：

````
sb('dist/app.js', 220) # 或可疑渲染所在的位置
续
````

当它暂停时，“repl”→检查“props”、状态引用、“useInput”处理程序值等。

### 调试正在运行的 `hermes --tui`

TUI 从 Python CLI 生成 Node。最简单的路径：

````bash
# 1.启动 TUI
爱马仕--tui &
TUI_PID=$(pgrep -f 'ui-tui/dist/entry' | 头 -1)

# 2. 在该节点 PID 上启用检查器
杀死-SIGUSR1“$TUI_PID”

# 3. 找到 WS URL
卷曲 -s http://127.0.0.1:9229/json/list | jq -r '.[0].webSocketDebuggerUrl'

# 4. 附加
节点检查 ws://127.0.0.1:9229/<uuid>
````

与 TUI 交互（在其窗口中输入）继续推进执行；您的调试器可以在任何“sb(...)”处的断点处暂停它。

### 调试 `_SlashWorker` / PTY 子进程

这些是 Python，而不是 Node——对它们使用“python-debugpy”技能。只有节点部分（Ink UI、tui_gateway 客户端、`ui-tui/` 下的 tsx-run 测试）使用此技能。

## 在调试器下运行 Vitest 测试

````bash
cd /home/bb/hermes-agent/ui-tui
# 运行一个在入口处暂停的测试文件
节点 --inspect-brk ./node_modules/vitest/vitest.mjs run --no-file-parallelism src/app/foo.test.tsx
````

在另一个终端中：“node inform -p <pid>”，然后“sb('src/app/foo.tsx', 42)”、“cont”。

使用“--no-file-parallelism”（vitest）或“--runInBand”（玩笑），这样就只有一个工作线程存在——调试池是很痛苦的。

## 堆快照和 CPU 配置文件（非交互式）

在上面的 CDP 驱动程序中，将 Debugger 替换为 `HeapProfiler` / `Profiler`：

```javascript
// CPU 分析 5 秒
等待 client.Profiler.enable();
等待 client.Profiler.start();
等待新的 Promise(r => setTimeout(r, 5000));
const { profile } = 等待 client.Profiler.stop();
require('fs').writeFileSync('/tmp/cpu.cpuprofile', JSON.stringify(profile));
// 在 Chrome DevTools → Performance 选项卡中打开 /tmp/cpu.cpuprofile
````

```javascript
// 堆快照
等待 client.HeapProfiler.enable();
常量块= []；
client.HeapProfiler.addHeapSnapshotChunk(({ chunk }) => chunks.push(chunk));
等待 client.HeapProfiler.takeHeapSnapshot({ reportProgress: false });
require('fs').writeFileSync('/tmp/heap.heapsnapshot', chunks.join(''));
````

## 常见陷阱

1. **TS 源中的行号错误。** 断点击中了发出的 JS，而不是“.ts”。 (a) 中断构建的 `dist/*.js`，或者 (b) 启用源映射 (`node --enable-source-maps`) 并使用 `sb('src/app.tsx', N)` — 但仅限于遵循源映射的 CDP 客户端。 `node Inspect` CLI 没有。

2. **`--inspect` 与 `--inspect-brk`。** `--inspect` 启动检查器但不暂停；如果你附加得太晚，你的脚本就会超过你的第一个断点。当您需要在任何代码运行之前设置断点时，请使用“--inspect-brk”。

3. **端口冲突。** 默认为“9229”。如果多个 Node 进程正在检查，请传递 `--inspect=0` （随机端口）并从 `/json/list` 读取实际 URL：
   ````bash
   curl -s http://127.0.0.1:9229/json/list # 列出主机上所有可检查的目标
   ````

4. **子进程。** 父进程上的 `--inspect` 不会检查其子进程。使用`NODE_OPTIONS='--inspect-brk'节点parent.js`传播到每个子节点；请注意，它们都需要唯一的端口（当继承`NODE_OPTIONS='--inspect'`时节点自动递增）。

5. **后台杀死。** 如果在目标暂停时使用“Ctrl+C”退出“节点检查”，则目标将保持暂停状态。要么先“cont”，要么显式“kill”目标。

6. **通过代理终端运行“节点检查”。**这是一个 PTY 友好的 REPL。在 OpenClaw 中，使用 `terminal(pty=true)` 或 `background=true` + `process(action='submit', data='...')` 启动它。非 PTY 前台模式适用于一次性命令，但不适用于交互式单步执行。

7. **安全性。** `--inspect=0.0.0.0:9229` 暴露任意代码执行。除非您有隔离网络，否则始终绑定到“127.0.0.1”（默认值）。

## 验证清单

设置调试会话后，验证：

- [ ] `curl -s http://127.0.0.1:9229/json/list` 返回您期望的目标
- [ ] 第一个断点实际上命中（如果没有，您可能错过了 `--inspect-brk` 或在执行完成后附加）
- [ ] 暂停时的源列表显示正确的文件（不匹配 = 源映射问题，请参阅陷阱 1）
- [ ] `repl` 中的 `exec process.pid` 返回您想要附加到的 PID

## 一次性食谱

**“为什么这个变量在 X 行未定义？”**
````bash
节点 --inspect-brk script.js &
节点检查 -p $!
# 调试>
sb('script.js', X)
续
# 暂停了。现在：
重复
> 我的变量
> 对象.keys(this)
````

**“这个函数的调用路径是什么？”**
````
调试> sb('suspectFn')
调试> 继续
# 进入时暂停
调试> bt
````

**“这个异步链挂在哪里？”**
````
# 从 --inspect （无 -brk）开始，让它运行到挂起，然后：
调试>暂停
调试> bt
# 现在你看到卡住的框架
````