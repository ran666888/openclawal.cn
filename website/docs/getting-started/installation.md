---
sidebar_position: 2
title: "Installation"
description: "在 Linux、macOS、WSL2、Windows 原生或 Android Termux 上安装 OpenClaw"
---
# 安装

两分钟内即可启动并运行 OpenClaw！

## 快速安装
### 使用 macOS 或 Windows 上的 OpenClaw Desktop 安装程序（推荐）
要轻松安装命令行和桌面应用程序，请从我们的网站[下载 OpenClaw 桌面安装程序](https://openclaw.nousresearch.com/) 并运行它。

### 没有 OpenClaw 桌面：
对于没有 OpenClaw Desktop 的仅命令行安装，请运行：

#### Linux / macOS / WSL2 / Android (Termux)
````bash
卷曲-fsSL https://hermes-agent.nousresearch.com/install.sh |巴什
````

#### Windows（本机）

在powershell中运行：
````powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1) 
````

如果您想在仅命令行安装后安装并运行 OpenClaw Desktop，只需运行
````bash
爱马仕桌面
````

### 安装程序做什么

安装程序会自动处理所有内容 - 所有依赖项（Python、Node.js、ripgrep、ffmpeg）、存储库克隆、虚拟环境、全局“hermes”命令设置和 LLM 提供程序配置。最后，您就可以开始聊天了。

#### 安装布局

安装程序放置内容的位置取决于您是以普通用户还是 root 身份进行安装：

|安装人员|代码位于 | `hermes` 二进制 |数据目录|
|---|---|---|---|
|点安装 | Python 站点包 | `~/.local/bin/hermes` (console_scripts) | `~/.hermes/` |
|每个用户（git 安装程序）| `~/.hermes/hermes-agent/` | `~/.local/bin/hermes` （符号链接）| `~/.hermes/` |
|根模式（`sudo curl ... \| sudo bash`）| `/usr/local/lib/hermes-agent/` | `/usr/local/bin/hermes` | `/root/.hermes/` （或 `$HERMES_HOME`）|

根模式 **FHS 布局**（`/usr/local/lib/…`、`/usr/local/bin/hermes`）与 Linux 上其他系统范围的开发人员工具的位置相匹配。它对于共享计算机部署非常有用，在共享计算机部署中，一个系统安装应该为每个用户提供服务。每用户配置（身份验证、技能、会话）仍然位于每个用户的“~/.hermes/”或显式“HERMES_HOME”下。

### 安装后

重新加载你的 shell 并开始聊天：

````bash
source ~/.bashrc # 或: source ~/.zshrc
爱马仕 # 开始聊天！
````

要稍后重新配置各个设置，请使用专用命令：

````bash
Hermes 型号 # 选择您的 LLM 提供商和型号
hermes tools # 配置启用哪些工具
hermes gateway setup # 设置消息平台
hermes config set # 设置单独的配置值
hermes setup # 或者运行完整的设置向导来一次配置所有内容
````

:::tip 最快路径：Nous Portal
一份订阅涵盖 300 多种型号以及[工具网关](/user-guide/features/tool-gateway)（网页搜索、图像生成、TTS、云浏览器）。跳过每个工具的按键杂耍：

````bash
爱马仕设置--门户
````

这会让您登录，将 Nous 设置为您的提供者，并通过一个命令打开工具网关。
:::

---

## 先决条件

**安装程序：** 在非 Windows 平台上，唯一的先决条件是 **Git**。在 Linux 上，还要确保“curl”和“xz-utils”可用（安装程序将 Node.js 下载为“.tar.xz”存档）。桌面应用程序还需要“g++”（或 Debian/Ubuntu 上的“build-essential”）来编译本机模块。安装程序会自动处理其他所有事情：

- **uv** （快速 Python 包管理器）
- **Python 3.11**（通过 uv，无需 sudo）
- **Node.js v22**（用于浏览器自动化和 WhatsApp 桥）
- **ripgrep**（快速文件搜索）
- **ffmpeg**（TTS 的音频格式转换）

:::信息
您**不需要**需要手动安装 Python、Node.js、ripgrep 或 ffmpeg。安装程序会检测缺少的内容并为您安装。只需确保 `git` 可用（`git --version`）。在 Linux 上，确保安装了“curl”和“xz-utils”（在 Debian/Ubuntu 上为“sudo apt install curl xz-utils”）。对于桌面应用程序，还需安装“build-essential”（“sudo apt install build-essential”）。
:::

:::提示 Nix 用户
如果您使用 Nix（在 NixOS、macOS 或 Linux 上），则有一个带有 Nix flake、声明性 NixOS 模块和可选容器模式的专用设置路径。请参阅 **[Nix 和 NixOS 设置](./nix-setup.md)** 指南。
:::

---

## 手动/开发者安装

如果您想克隆存储库并从源代码安装（用于贡献、从特定分支运行或完全控制虚拟环境），请参阅贡献指南中的[开发设置](../developer-guide/contributing.md#development-setup)部分。

---

## 非 Sudo / 系统服务用户安装

支持以专用的非特权用户身份运行 OpenClaw（例如“hermes”systemd 服务帐户，或任何没有“sudo”访问权限的用户）。安装路径上唯一真正需要 root 的是 Playwright 的 `--with-deps` 步骤，该步骤会 `apt` 安装 Chromium 使用的共享库（`libnss3`、`libxkbcommon` 等）。安装程序会检测 sudo 是否可用，并在不可用时优雅地降级 — 它将把 Chromium 二进制文件安装到服务用户自己的 Playwright 缓存中，并打印管理员需要单独运行的确切命令。

**推荐拆分（Debian/Ubuntu）：**

1. **一次，以管理员用户身份使用 sudo**，安装 Chromium 所需的系统库：
   ````bash
   sudo npx playwright install-deps chromium
   ````
   （您可以从任何地方运行它 - `npx` 将即时获取 Playwright。）

2. **作为非特权服务用户**，运行常规安装程序。它将检测缺少的 sudo，跳过 `--with-deps`，并将 Chromium 安装到用户的本地 Playwright 缓存中：
   ````bash
   卷曲-fsSL https://hermes-agent.nousresearch.com/install.sh |巴什
   ````

   如果您想完全跳过 Playwright 步骤（例如，因为您正在无头运行并且不需要浏览器自动化），请传递 `--skip-browser`：
   ````bash
   卷曲-fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --跳过浏览器
   ````

3. **使 `hermes` 可用于服务用户的 shell。** 安装程序将启动器写入 `~/.local/bin/hermes`。系统服务帐户通常有一个不包含“~/.local/bin”的最小路径。将其添加到用户环境中，或将启动器符号链接到系统位置：
   ````bash
   # 选项 A — 添加到服务用户的个人资料
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

   # 选项 B — 系统范围的符号链接（以管理员身份运行）
   sudo ln -s /home/hermes/.hermes/hermes-agent/venv/bin/hermes /usr/local/bin/hermes
   ````

4. **验证：** `hermes doctor` 现在应该可以正常运行。如果您收到“ModuleNotFoundError：没有名为“dotenv”的模块”，则说明您正在使用系统 Python 而不是 venv 启动器（“~/.hermes/openclaw/venv/bin/hermes”）调用存储库源“hermes”文件（“~/.hermes/openclaw/hermes”）——修复步骤 3。

同样的模式适用于 Arch（安装程序使用具有相同 sudo 检测逻辑的 pacman）、Fedora/RHEL 和 openSUSE — 这些发行版根本不支持 `--with-deps`，因此管理员总是单独安装系统库。安装程序会打印相关的“dnf”/“zypper”命令。

---

## 故障排除

|问题 |解决方案 |
|---------|----------|
| `hermes：找不到命令` |重新加载你的 shell (`source ~/.bashrc`) 或检查 PATH |
| `API 密钥未设置` |运行 `hermes model` 来配置您的提供程序，或 `hermes config set OPENROUTER_API_KEY your_key` |
|更新后缺少配置 |运行 `hermes config check` 然后运行 ​​`hermes config migrate` |

如需更多诊断，请运行“hermes doctor”——它会准确地告诉您缺少什么以及如何修复它。

## 安装方法自动检测

OpenClaw 自动检测它是否是通过“pip”、git 安装程序、Homebrew 或 NixOS 安装的，并且“hermes update”打印该路径的匹配更新命令。无需设置环境变量 - 检测基于安装布局（Python 站点包、`~/.hermes/hermes-agent/`、Homebrew 前缀或 Nix 存储路径）。 “hermes doctor”还在其环境摘要下显示了检测到的方法。