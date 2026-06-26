---
sidebar_position: 16
title: "LSP — Semantic Diagnostics"
description: "Real language servers (pyright, gopls, rust-analyzer, …) wired into the post-write lint check used by write_file and patch."
---
# 语言服务器协议 (LSP)

OpenClaw 运行完整的语言服务器——pyright、gopls、rust-analyzer、
typescript-language-server、clangd 以及其他大约 20 个 — 作为背景
子进程并将其语义诊断输入到后写入中
`write_file` 和 `patch` 使用的 lint 检查。当代理编辑
文件，它准确地看到编辑引入的错误 - 不仅仅是
语法错误，但是 **类型错误、未定义的名称、缺少导入、
以及语言服务器检测到的项目范围的语义问题**。

这与顶级编码代理使用的架构相同。赫尔墨斯
它是独立的：不需要编辑器主机，不需要插件
安装，无需管理单独的守护进程。

## 当 LSP 运行时

LSP 通过 **git 工作区检测** 进行门控。当代理人工作时
目录（或正在编辑的文件）位于 git 存储库、LSP 内
针对该工作区运行。当 git 存储库中都不存在时，LSP
保持休眠状态 — 对于以 cwd 为中心的消息传递网关很有用
用户的主目录，并且没有要诊断的项目。

检查是分层的：首先进行进程内语法检查（微秒），
然后当语法干净时 LSP 诊断第二。片状或缺失
语言服务器永远无法中断写入——每个 LSP 故障路径
默默地退回到纯语法结果。

具体来说，在每个成功的“write_file”或“patch”上：

1. OpenClaw 捕获文件当前诊断的基线。
2. 执行写入。
3. 重新查询语言服务器，过滤掉之前的诊断信息
   已经在基线中，并且仅显示新的。

代理看到的输出如下：

````
{
  “字节写入”：42，
  “dirs_created”：假，
  “lint”：{“状态”：“确定”，“输出”：“”}，
  "lsp_diagnostics": "此编辑引入的 LSP 诊断：\n<diagnostics file=\"/path/to/foo.py\">\n错误 [42:5] 找不到名称 'foo' [reportUndefinedVariable] (Pyright)\n错误 [50:1] 类型为 \"str\" 的参数无法分配给 \"int\" [reportArgumentType] (Pyright)\n</诊断>"
}
````

`lint` 字段携带语法检查结果（微秒
通过 `ast.parse`、`json.loads` 等进行进程内解析）；的
`lsp_diagnostics` 字段携带来自
真正的语言服务器。两个通道，独立信号 —
代理看到一个语法干净的文件，但存在语义问题：
``lint: ok`` 加上填充的 ``lsp_diagnostics``。

## 支持的语言

|语言 |服务器|自动安装 |
|----------|--------|--------------|
|蟒蛇 | `pyright-langserver` | npm |
| TypeScript / JavaScript / JSX / TSX | `打字稿语言服务器` | npm |
|视图 | `@vue/语言服务器` | npm |
|苗条 | `svelte 语言服务器` | npm |
|天文 | `@astrojs/语言服务器` | npm |
|去 | `gopls` | `去安装` |
|铁锈| `锈分析仪` |手册（rustup）|
| C/C++ | `clangd` |手册（LLVM）|
| bash / zsh | `bash 语言服务器` | npm |
| yaml | `yaml 语言服务器` | npm |
|卢阿 | `lua 语言服务器` |手册（GitHub 版本）|
| PHP | `intelepense` | npm |
| OCaml | `ocaml-lsp` |手册（opam）|
| Dockerfile | `dockerfile-语言-服务器-nodejs` | npm |
|地形 | `terraform-ls` |手册|
|飞镖 | `dart 语言服务器` |手册（dart sdk）|
|哈斯克尔 | `haskell 语言服务器` |手册 (ghcup) |
|朱莉娅 | `julia` + LanguageServer.jl |手册|
| Clojure | `clojure-lsp` |手册|
|尼克斯 | `nixd` |手册|
|齐格| `zls` |手册|
|微光 | `闪光 lsp` |手册（闪光安装）|
|长生不老药 | `elixir-ls` |手册|
|棱镜| `prisma 语言服务器` |手册|
|科特林 | `kotlin 语言服务器` |手册|
|爪哇 | `jdtls` |手册|

对于“手动”条目，通过任何工具链安装服务器
manager 对于该语言是有意义的（rustup、ghcup、opam、brew、
……）。 OpenClaw 自动检测 PATH 或中的二进制文件
`<HERMES_HOME>/lsp/bin/`。

一些服务器与 npm 的对等依赖项一起安装
不会自动拉动。当前的情况是“typescript-language-server”，
这需要可从同一库导入的“typescript”SDK
`node_modules` 树 — 当您安装时，OpenClaw 将这两个包一起安装
运行 `hermes lsp install typescript` 或首先自动安装
使用。

## 命令行界面

````
hermes lsp status # 服务状态 + 每服务器安装状态
hermes lsp list # 注册表，可选 --installed-only
hermes lsp install <id> # 急切地安装一台服务器
hermes lsp install-all # 尝试使用已知配方的每个服务器
hermes lsp restart # 关闭正在运行的客户端
hermes lsp which <id> # 打印解析的二进制路径
````

`hermes lsp status` 是最好的起点——它显示了哪个
今天，语言将获得语义诊断，并且需要
已安装二进制文件。

## 配置

默认值适用于典型设置；如果二进制文件没有什么可设置的
在路径上。

````yaml
# 配置.yaml
LSP：
  # 主开关。禁用会跳过整个子系统 — 无服务器
  # 生成，没有后台事件循环运行。
  启用：真

  # 每次写入后等待诊断的时间。
  wait_mode：文档#“文档”或“完整”
  等待超时：5.0

  # 如何处理丢失的服务器二进制文件。
  # auto — 通过 npm/pip/go 安装到 <HERMES_HOME>/lsp/bin
  # 手册 — 仅使用 PATH 上已有的二进制文件
  安装策略：自动

  # 每个服务器覆盖（全部可选）。
  服务器：
    版权：
      禁用：假
      命令：[“/abs/path/to/pyright-langserver”，“--stdio”]
      环境：{ PYRIGHT_LOG_LEVEL：“信息”}
      初始化选项：
        蟒蛇：
          分析：
            类型检查模式：“严格”
    打字稿：
      disabled: true # 即使扩展名匹配也跳过 TS
````

### 每服务器密钥

* `disabled: true` — 完全跳过该服务器，即使它
  扩展名与文件匹配。
* `command: [bin, ...args]` — 固定自定义二进制路径。旁路
  自动安装。
* `env: {KEY: value}` — 传递给生成进程的额外环境变量。
* `initialization_options: {...}` — 合并到 LSP 中
  在“initialize”中发送的“initializationOptions”有效负载
  握手。特定于服务器；请参阅语言服务器的文档。

## 安装位置

当 `install_strategy: auto` 时，OpenClaw 将二进制文件安装到
`<HERMES_HOME>/lsp/bin/`。 NPM 包登陆
`<HERMES_HOME>/lsp/node_modules/` 带有向上一级的 bin 符号链接。
Go 二进制文件来自“go install”，“GOBIN”指向
暂存目录。

没有任何内容安装到`/usr/local/`、`~/.local/`或任何其他目录
共享位置 — 暂存目录完全属于 OpenClaw 所有，并且
重置配置文件时已删除。

## 性能特点

LSP 服务器在首次使用时**延迟生成**。编辑 Python 文件
在一个从未见过“.py”流量的项目中产生了pyright；的
对于大多数服务器来说，spawn 需要 1-3 秒（rust-analyzer 可能需要 10+
在一个冷项目上）。同一工作区中的后续编辑重复使用
正在运行的服务器。

当没有数据时，LSP 层会增加几毫秒的干净写入时间
发出诊断信息。当发出诊断信息时，等待
预算是“wait_timeout”秒——通常服务器响应
Pyright/tsserver 需要几十毫秒，而
rust-analyzer 中期索引。

服务器在 OpenClaw 进程的生命周期内保持活动状态。有
无空闲超时收割机 - 重新启动服务器索引的成本
每次写入都会远远高于持有守护进程。

## 禁用

在 config.yaml 中设置 lsp.enabled: false 以禁用整个
子系统。写后检查回退到进程内语法
检查（Python 的“ast.parse”，JSON 的“json.loads”等）
与早期版本相比没有变化。

要禁用单一语言而不禁用整个层：

````yaml
LSP:
  服务器：
    锈迹分析仪：
      禁用：真
````

## 故障排除

**`hermes lsp status`显示服务器“丢失”**

该二进制文件不在 PATH 上，也不在 `<HERMES_HOME>/lsp/bin/` 中。运行
`hermes lsp install <server_id>` 尝试自动安装，或者
通过语言的正常工具链手动安装二进制文件。

**“hermes lsp status”中的“后端警告”部分**

一些服务器作为外部 CLI 的瘦包装器提供，以实现实际的
诊断——它们干净地产生并接受请求但从不发出
sidecar 二进制文件丢失时出现错误。最常见的情况是
`bash-language-server`，它将诊断委托给 `shellcheck`。
当“hermes lsp status”显示“后端警告”部分时，安装
通过操作系统包管理器指定的工具：

````
apt install shellcheck # Debian / Ubuntu
brew 安装 shellcheck # macOS
scoop install shellcheck # Windows
````

在服务器生成时会记录一次相同的警告
`~/.hermes/logs/agent.log`。

**服务器启动但从不返回诊断信息**

检查“~/.hermes/logs/agent.log”中的“[agent.lsp.client]”条目 -
来自语言服务器的 stderr 和协议错误都发生
那里。一些服务器（尤其是 Rust-analyzer）需要完成
在发出每个文件诊断之前的项目范围索引；第一个
服务器启动后的编辑可能会在没有诊断的情况下完成，并且
随后的编辑将它们拾取。

**服务器崩溃**

崩溃的服务器将添加到损坏的集合中，并且不会重试
会议剩余时间。运行 `hermes lsp restart` 清除设置；
下一个编辑会重新出现。

**在任何 git 存储库之外编辑文件**

根据设计，LSP 仅在 git 存储库内运行。如果该项目不是
尚未初始化，请运行“git init”以启用 LSP 诊断。否则
仅适用进程内语法后备。