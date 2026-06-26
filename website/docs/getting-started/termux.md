---
sidebar_position: 3
title: "Android / Termux"
description: "在 Android 手机上通过 Termux 直接运行 OpenClaw"
---
# Android — Termux 安装

这是通过[Termux](https://termux.dev/)直接在Android手机上运行Hermes Agent的经过测试的路径。

它为您提供了手机上可用的本地 CLI，以及目前已知可以在 Android 上干净安装的核心附加功能。

## 测试路径支持什么？

经过测试的 Termux 捆绑包安装：
- Hermes CLI
- 计划任务支持
- PTY/后台终端支持
- Telegram 网关支持（手动/尽力后台运行）
- MCP支持
- Honcho 记忆支持
- ACP 支持

具体来说，它映射到：

````bash
python -m pip install -e '.[termux]' -c约束-termux.txt
````

## 什么还不是测试路径的一部分？

一些功能仍然需要桌面/服务器样式的依赖项，这些依赖项尚未针对 Android 发布，或者尚未在手机上进行验证：

- 目前 Android 不支持 `.[all]`
- `voice` 额外功能被 `faster-whisper -> ctranslate2` 阻止，并且 `ctranslate2` 不发布 Android 轮子
- 在 Termux 安装程序中跳过自动浏览器/Playwright bootstrap
- 基于 Docker 的终端隔离在 Termux 内不可用
- Android 可能仍会暂停 Termux 后台作业，因此网关持久性是尽力而为，而不是普通的托管服务

这并不妨碍 OpenClaw 作为手机原生 CLI 代理正常工作——这只是意味着推荐的移动安装有意比桌面/服务器安装更窄。

---

## 选项 1：单行安装程序

OpenClaw 现在提供支持 Termux 的安装程序路径：

````bash
卷曲-fsSL https://hermes-agent.nousresearch.com/install.sh |巴什
````

在 Termux 上，安装程序会自动：
- 使用`pkg`作为系统包
- 使用“python -m venv”创建 venv
- 首先尝试广泛的 `.[termux-all]` extra，然后回退到较小的 `.[termux]` extra（然后是基本安装）——curl 安装程序会自动匹配此顺序
- 将 `hermes` 链接到 `$PREFIX/bin`，以便它保留在您的 Termux 路径上
- 跳过未经测试的浏览器/WhatsApp 引导程序

如果您需要显式命令或需要调试失败的安装，请使用下面的手动路径。

---

## 选项 2：手动安装（完全明确）

### 1.更新Termux并安装系统包

````bash
包更新
pkg install -y git python clang rust make pkg-config libffi openssl nodejs ripgrep ffmpeg
````

为什么要使用这些包？
- `python` — 运行时 + venv 支持
- `git` — 克隆/更新存储库
- `clang`、`rust`、`make`、`pkg-config`、`libffi`、`openssl` — 在 Android 上构建一些 Python 依赖项所需
- `nodejs` — 可选的 Node 运行时，用于超出测试核心路径的实验
- `ripgrep` — 快速文件搜索
- `ffmpeg` — 媒体/TTS 转换

### 2.克隆赫尔墨斯

````bash
git 克隆 https://github.com/NousResearch/hermes-agent.git
cd Hermes 特工
````

### 3.创建虚拟环境

````bash
python -m venv venv
源 venv/bin/activate
导出 ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install --升级 pip setuptools 轮
````

“ANDROID_API_LEVEL”对于基于 Rust / maturin 的包（例如“jiter”）非常重要。

### 4. 安装经过测试的 Termux 捆绑包

````bash
python -m pip install -e '.[termux]' -c约束-termux.txt
````

如果您只想要最小的核心代理，这也适用：

````bash
python -m pip install -e '.' -c 约束-termux.txt
````

### 5. 将 `hermes` 放在您的 Termux 路径上

````bash
ln -sf“$PWD/venv/bin/hermes”“$PREFIX/bin/hermes”
````

`$PREFIX/bin` 已经在 Termux 的 PATH 中，因此这使得 `hermes` 命令在新的 shell 中持续存在，而无需每次都重新激活 venv。

### 6. 验证安装

````bash
爱马仕版
爱马仕医生
````

### 7. 启动 OpenClaw

````bash
爱马仕
````

---

## 推荐的后续设置

### 配置模型

````bash
爱马仕型号
````

或者直接在`~/.hermes/.env`中设置密钥。

### 稍后重新运行完整的交互式安装向导

````bash
爱马仕设置
````

### 手动安装可选的节点依赖项

测试的 Termux 路径故意跳过节点/浏览器引导。如果您想稍后尝试浏览器工具：

````bash
pkg 安装nodejs-lts
npm 安装
````

浏览器工具会自动在其 PATH 搜索中包含 Termux 目录 (`/data/data/com.termux/files/usr/bin`)，因此无需任何额外的 PATH 配置即可发现 `agent-browser` 和 `npx`。

将 Android 上的浏览​​器/WhatsApp 工具视为实验性工具，除非另有说明。

---

## 故障排除

### 安装 `.[all]` 时`找不到解决方案`

请改用经过测试的 Termux 捆绑包：

````bash
python -m pip install -e '.[termux]' -c约束-termux.txt
````

目前的拦截器是额外的“语音”：
-“声音”拉动“更快的耳语”
- `faster-whisper` 依赖于 `ctranslate2`
- `ctranslate2` 不发布 Android 轮子

### `uv pip install` 在 Android 上失败

使用带有 stdlib venv + `pip` 的 Termux 路径：

````bash
python -m venv venv
源 venv/bin/activate
导出 ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install --升级 pip setuptools 轮
python -m pip install -e '.[termux]' -c约束-termux.txt
````

### `jiter` / `maturin` 抱怨 `ANDROID_API_LEVEL`

安装前明确设置 API 级别：

````bash
导出 ANDROID_API_LEVEL="$(getprop ro.build.version.sdk)"
python -m pip install -e '.[termux]' -c约束-termux.txt
````

### `hermes doctor` 说 ripgrep 或 Node 丢失

使用 Termux 软件包安装它们：

````bash
pkg 安装 ripgrep Nodejs
````

### 安装 Python 包时构建失败

确保已安装构建工具链：

````bash
pkg 安装 clang rust make pkg-config libffi openssl
````

然后重试：

````bash
python -m pip install -e '.[termux]' -c约束-termux.txt
````

---

## 手机的已知限制

- Docker 后端不可用
- 通过“faster-whisper”的本地语音转录在测试路径中不可用
- 安装程序故意跳过浏览器自动化设置
- 一些可选的附加功能可能有效，但目前只有 `.[termux]` 和 `.[termux-all]` 被记录为经过测试的 Android 包

如果您遇到新的 Android 特定问题，请使用以下命令打开 GitHub 问题：
- 您的安卓版本
- `termux-信息`
- `python --版本`
- 《爱马仕医生》
- 确切的安装命令和完整的错误输出