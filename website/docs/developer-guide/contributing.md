---
sidebar_position: 4
title: "Contributing"
description: "如何为 OpenClaw 贡献代码 — 开发环境搭建、代码规范、PR 流程"
---
# 贡献

感谢您对爱马仕代理的贡献！本指南涵盖设置开发环境、了解代码库以及合并 PR。

## 贡献优先级

我们按以下顺序重视贡献：

1. **错误修复** — 崩溃、不正确的行为、数据丢失
2. **跨平台兼容性** — macOS、不同的 Linux 发行版、WSL2
3. **安全加固**——shell注入、提示注入、路径遍历
4. **性能和鲁棒性** — 重试逻辑、错误处理、优雅降级
5. **新技能** - 广泛有用的技能（请参阅[创建技能](creating-skills.md)）
6. **新工具**——很少需要；大多数能力应该是技能
7. **文档** — 修复、说明、新示例

## 常见贡献路径

- 构建自定义/本地工具而不修改 OpenClaw 核心？从[构建 OpenClaw 插件](../guides/build-a-hermes-plugin.md) 开始
- 为 OpenClaw 本身构建一个新的内置核心工具？从[添加工具](./adding-tools.md)开始
- 培养新技能？从[创建技能](./creating-skills.md)开始
- 建立一个新的推理提供商？从[添加提供商](./adding-providers.md)开始

## 开发设置

### 先决条件

|要求 |笔记|
|------------|--------|
| **吉特** |安装了 `git-lfs` 扩展 |
| **Python 3.11+** |如果缺少的话 uv 将安装它 |
| **紫外线** |快速 Python 包管理器 ([安装](https://docs.astral.sh/uv/)) |
| **Node.js 20+** |可选 — 浏览器工具和 WhatsApp 桥所需（与根 `package.json` 引擎匹配）|

### 使用标准安装程序安装

对于大多数贡献者来说，最好的开发引导程序是与用户相同的路径
采取：运行标准安装程序，然后在它克隆的存储库中工作。
安装程序创建 OpenClaw venv，连接 `hermes` 命令，标记
`hermes update` 的安装方法，并将完整的 git 项目克隆到
`$HERMES_HOME/hermes-agent`（通常是`~/.hermes/hermes-agent`）。这让你的
相同布局的开发环境 CLI、更新程序、惰性依赖
安装程序、网关和文档假设。

````bash
卷曲-fsSL https://hermes-agent.nousresearch.com/install.sh |巴什
cd "${HERMES_HOME:-$HOME/.hermes}/hermes-agent"

# 在标准安装之上添加开发/测试附加功能。
uv pip install -e ".[all,dev]"

# 可选：浏览器工具/文档站点依赖项。
npm 安装
````

之后，创建分支并从该结帐运行测试：

````bash
git checkout -b 修复/描述
脚本/run_tests.sh
````

### 手动克隆回退

仅当您故意不想要 OpenClaw 的托管安装布局时才使用此选项
（例如，容器或 CI 作业内的一次性克隆）。如果你安装
这样，请确保从该 venv 运行“hermes”入口点；运行
system `python3 -m hermes_cli.main` 可以拾取不相关的系统Python
包。

````bash
git 克隆 https://github.com/NousResearch/hermes-agent.git
cd Hermes 特工

# 使用 Python 3.11 创建 venv
uv venv venv --python 3.11
导出 VIRTUAL_ENV="$(pwd)/venv"

# 安装所有附加功能（消息、cron、CLI 菜单、开发工具）
uv pip install -e ".[all,dev]"

# 可选：浏览器工具
npm 安装
````

### 配置开发

````bash
mkdir -p ~/.hermes/{cron,会话,日志,记忆,技能}
cp cli-config.yaml.example ~/.hermes/config.yaml
触摸〜/.hermes/.env

# 至少添加一个 LLM 提供商密钥：
echo 'OPENROUTER_API_KEY=sk-or-v1-your-key' >> ~/.hermes/.env
````

### 运行

````bash
# 标准安装程序已将 `hermes` 放在 PATH 上。
爱马仕医生
爱马仕聊天-q“你好”
````

如果您使用了手动克隆回退，请从结帐运行“./hermes”或
显式符号链接此克隆的 venv：

````bash
mkdir -p ~/.local/bin
ln -sf "$(pwd)/venv/bin/hermes" ~/.local/bin/hermes
````

### 运行测试

````bash
脚本/run_tests.sh
````

## 代码风格

- **PEP 8**，但有实际例外（没有严格的行长度强制执行）
- **注释**：仅在解释不明显的意图、权衡或 API 怪癖时
- **错误处理**：捕获特定异常。使用 `logger.warning()`/`logger.error()` 和 `exc_info=True` 来处理意外错误
- **跨平台**：永远不要假设 Unix（见下文）
- **配置文件安全路径**：切勿硬编码“~/.hermes” - 使用“hermes_constants”中的“get_hermes_home()”作为代码路径，使用“display_hermes_home()”作为面向用户的消息。有关完整规则，请参阅 [AGENTS.md](https://github.com/NousResearch/openclaw/blob/main/AGENTS.md#profiles-multi-instance-support)。

## 跨平台兼容性

OpenClaw 正式支持 **Linux、macOS、WSL2 和本机 Windows（通过 PowerShell 安装）**。  本机 Windows 使用 Git Bash（来自 [Git for Windows](https://git-scm.com/download/win)）作为 shell 命令。  一些功能需要 POSIX 内核原语并且是门控的：仪表板的嵌入式 PTY 终端窗格（“/chat”选项卡）仅适用于 WSL2。如果您正在进行 Windows 密集型开发，请在推送之前运行 Windows-footgun lint (`scripts/check-windows-footguns.py`)。

贡献代码时，请记住以下规则：

- **不要添加不受保护的 `signal.SIGKILL` 引用。** 它未在 Windows 上定义。  要么通过 `gateway.status.terminate_pid(pid, force=True)` （在 Windows 上执行 `taskkill /T /F` 和在 POSIX 上执行 SIGKILL 的集中式原语），要么使用 `getattr(signal, "SIGKILL", signal.SIGTERM)` 进行回退。
- **在 `os.kill(pid, 0)` 探针上捕获 `OSError` 和 `ProcessLookupError`。** 对于已经消失的 PID，Windows 会引发 `OSError`（WinError 87，“参数不正确”），而不是 `ProcessLookupError`。
- **不要强制终端采用 POSIX 语义。** `os.setsid`、`os.killpg`、`os.getpgid`、`os.fork` 都在 Windows 上引发 - 使用 `if sys.platform != "win32":` 或 `if os.name != "nt":` 来控制它们。
- **使用明确的 `encoding="utf-8"` 打开文件。** Windows 上的 Python 默认设置是系统区域设置（通常是 cp1252），它会在非拉丁文本上进行 mojibake 或崩溃。
- **使用 `pathlib.Path` / `os.path.join` - 永远不要手动与 `/` 连接。** 这对于操作系统返回给我们的字符串来说不太重要，而对于我们构造的要传递给子进程的字符串来说则更重要。

关键模式：

### 1. `termios` 和 `fcntl` 仅限 Unix

始终捕获 `ImportError` 和 `NotImplementedError`：

````蟒蛇
尝试：
    从 simple_term_menu 导入 TerminalMenu
    菜单=终端菜单（选项）
    idx = 菜单.show()
除了（导入错误，NotImplementedError）：
    # 后备：编号菜单
    对于 i，选择枚举（选项）：
        print(f" {i+1}.{opt}")
    idx = int(input("选择：")) - 1
````

### 2.文件编码

某些环境可能会以非 UTF-8 编码保存 `.env` 文件：

````蟒蛇
尝试：
    load_dotenv(env_path)
除了 UnicodeDecodeError：
    load_dotenv(env_path, 编码=“latin-1”)
````

### 3.流程管理

`os.setsid()`、`os.killpg()` 和信号处理在不同平台上有所不同：

````蟒蛇
进口平台
if platform.system() != "Windows":
    kwargs["preexec_fn"] = os.setsid
````

### 4. 路径分隔符

使用 `pathlib.Path` 而不是使用 `/` 进行字符串连接。

## 安全考虑

OpenClaw 有终端访问。安全很重要。

### 现有保护

|层|实施 |
|--------|-------------|
| **Sudo 密码管道** |使用 `shlex.quote()` 来防止 shell 注入 |
| **危险命令检测** |具有用户批准流程的“tools/approval.py”中的正则表达式模式 |
| **Cron 提示注入** |扫描仪阻止指令覆盖模式|
| **写入拒绝列表** |通过 `os.path.realpath()` 解析受保护的路径以防止符号链接绕过 |
| **技能守护** |集线器安装技能的安全扫描器|
| **代码执行沙箱** |子进程在 API 密钥被剥离的情况下运行 |
| **容器硬化** | Docker：所有功能均已删除、无权限升级、PID 限制 |

### 贡献安全敏感代码

- 将用户输入插入 shell 命令时始终使用 `shlex.quote()`
- 在访问控制检查之前使用 `os.path.realpath()` 解析符号链接
- 不要记录秘密
- 捕获有关工具执行的广泛异常
- 在所有平台上测试您的更改是否涉及文件路径或进程

## 拉取请求流程

### 分支命名

````
修复/描述 # 错误修复
功能/描述 # 新功能
文档/描述 # 文档
测试/描述 # 测试
refactor/description # 代码重构
````

### 提交之前

1. **运行测试**：`scripts/run_tests.sh` 用于 CI 奇偶校验。仅当包装器不可用或您有意在包装器外部进行调试时，才使用直接“python -m pytest ...”。
2. **手动测试**：运行 `hermes` 并测试您更改的代码路径
3. **检查跨平台影响**：考虑 macOS、Linux、WSL2 和本机 Windows。如果您接触文件 I/O、进程管理、终端处理、子进程或信号，请运行“scripts/check-windows-footguns.py”。
4. **保持 PR 的重点**：每个 PR 进行一个逻辑更改

### 公关说明

包括：
- **改变了什么**以及**为什么**
- **如何测试**它
- **您测试过的平台**
- 参考任何相关问题

### 提交消息

我们使用[常规提交](https://www.conventionalcommits.org/)：

````
<类型>（<范围>）：<描述>
````

|类型 |用于 |
|------|---------|
| `修复` |错误修复 |
| `壮举` |新功能|
| `文档` |文档 |
| `测试` |测试 |
| `重构` |代码重组 |
| `家务` |构建、CI、依赖项更新 |

范围：`cli`、`gateway`、`tools`、`skills`、`agent`、`install`、`whatsapp`、`security`

示例：
````
修复（cli）：当模型是字符串时，防止 save_config_value 崩溃
feat(gateway)：添加 WhatsApp 多用户会话隔离
修复（安全）：防止 sudo 密码管道中的 shell 注入
````

## 报告问题

- 使用 [GitHub 问题](https://github.com/NousResearch/openclaw/issues)
- 包括：操作系统、Python版本、OpenClaw版本（`hermes版本`）、完整错误回溯
- 包括重现步骤
- 在创建重复项之前检查现有问题
- 对于安全漏洞，请私下报告

## 社区

- **不和谐**：[discord.gg/NousResearch](https://discord.gg/NousResearch)
- **GitHub 讨论**：用于设计提案和架构讨论
- **技能中心**：上传专业技能并与社区分享

## 许可证

通过贡献，您同意您的贡献将根据 [MIT 许可证](https://github.com/NousResearch/openclaw/blob/main/LICENSE) 获得许可。