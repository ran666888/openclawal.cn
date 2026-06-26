---
title: Vision & Image Paste
description: Paste images from your clipboard into the Hermes CLI for multimodal vision analysis.
sidebar_label: Vision & Image Paste
sidebar_position: 7
---
# 视觉与图像粘贴

OpenClaw 支持**多模态视觉** - 您可以将剪贴板中的图像直接粘贴到 CLI 中，并要求代理分析、描述或使用它们。图像作为 base64 编码的内容块发送到模型，因此任何具有视觉功能的模型都可以处理它们。

:::提示
门户订阅者可以在同一目录中获得具有视觉功能的模型（Claude、GPT-5、Gemini）——无需额外的凭据。请参阅[Nous 门户](/integrations/nous-portal)。
:::

## 它是如何工作的

1. 将图像复制到剪贴板（屏幕截图、浏览器图像等）
2. 使用以下方法之一将其附加
3. 输入您的问题并按 Enter
4. 图像在输入上方显示为“[📎 Image #1]”徽章
5. 提交时，图像将作为视觉内容块发送到模型

您可以在发送前附加多个图像 - 每个图像都有自己的徽章。按“Ctrl+C”清除所有附加图像。

图像以带有时间戳的文件名的 PNG 文件保存到“~/.hermes/images/”。

## 粘贴方法

附加图像的方式取决于您的终端环境。并非所有方法都适用——以下是完整的细分：

### `/paste` 命令

**最可靠的显式图像附加后备。**

````
/粘贴
````

输入“/paste”并按 Enter 键。 OpenClaw 检查您的剪贴板中是否有图像并将其附加。当您的终端重写 `Cmd+V`/`Ctrl+V` 时，或者当您仅复制图像并且没有要检查的括号粘贴文本负载时，这是最安全的选项。

### Ctrl+V / Cmd+V

OpenClaw 现在将粘贴视为分层流：
- 首先粘贴普通文本
- 如果终端没有干净地传递文本，则本机剪贴板/OSC52 文本回退
- 当剪贴板或粘贴的有效负载解析为图像或图像路径时附加图像

这意味着粘贴的 macOS 屏幕截图临时路径和“file://...”图像 URI 可以立即附加，而不是作为原始文本放在编辑器中。

:::警告
如果您的剪贴板**只有图像**（没有文本），终端仍然无法直接发送二进制图像字节。使用“/paste”作为显式图像附加后备。
:::

### `/terminal-setup` 用于 VS Code / 光标 / Windsurf

如果您在 macOS 上的本地 VS Code 系列集成终端内运行 TUI，OpenClaw 可以安装推荐的“workbench.action.terminal.sendSequence”绑定，以获得更好的多行和撤消/重做奇偶校验：

````文本
/终端设置
````

当 IDE 拦截“Cmd+Enter”、“Cmd+Z”或“Shift+Cmd+Z”时，这尤其有用。仅在本地计算机上运行它，而不是在 SSH 会话中运行。

## 平台兼容性

|环境 | `/粘贴` | Cmd/Ctrl+V | `/终端设置` |笔记|
|---|:---:|:---:|:---:|---|
| **macOS 终端 / iTerm2** | ✅ | ✅ |不适用 |最佳体验——原生剪贴板+截图路径恢复|
| **苹果终端** | ✅ | ✅ |不适用 |如果 Cmd+←/→/⌫ 被重写，请使用 Ctrl+A / Ctrl+E / Ctrl+U 后备 |
| **Linux X11 桌面** | ✅ | ✅ |不适用 |需要`xclip`（`apt install xclip`）|
| **Linux Wayland 桌面** | ✅ | ✅ |不适用 |需要 `wl-paste` (`apt install wl-clipboard`) |
| **WSL2（Windows 终端）** | ✅ | ✅ |不适用 |使用“powershell.exe”——无需额外安装 |
| **VS Code / 光标 / Windsurf（本地）** | ✅ | ✅ | ✅ |推荐用于更好的 Cmd+Enter / 撤消 / 重做奇偶校验 |
| **VS Code / 光标 / Windsurf (SSH)** | ❌² | ❌² | ❌³ |在本地计算机上运行“/terminal-setup” |
| **SSH 终端（任意）** | ❌² | ❌² |不适用 |远程剪贴板无法访问 |

² 请参阅下面的[SSH 和远程会话](#ssh--remote-sessions)
³ 该命令写入本地 IDE 键绑定，不应从远程主机运行

## 特定于平台的设置

### macOS

**无需设置。** OpenClaw 使用 `osascript`（内置于 macOS 中）来读取剪贴板。为了获得更快的性能，可以选择安装“pngpaste”：

````bash
酿造安装pngpaste
````

### Linux (X11)

安装`xclip`：

````bash
# Ubuntu/Debian
sudo apt安装xclip

# 软呢帽
须藤 dnf 安装 xclip

# 拱门
sudo pacman -S xclip
````

### Linux（韦兰）

现代 Linux 桌面（Ubuntu 22.04+、Fedora 34+）通常默认使用 Wayland。安装`wl-剪贴板`：

````bash
# Ubuntu/Debian
sudo apt install wl-剪贴板

# 软呢帽
sudo dnf 安装 wl-剪贴板

# 拱门
sudo pacman -S wl-剪贴板
````

:::tip 如何检查您是否在 Wayland
````bash
回显$XDG_SESSION_TYPE
# "wayland" = Wayland, "x11" = X11, "tty" = 无显示服务器
````
:::

### WSL2

**不需要额外的设置。** OpenClaw 自动检测 WSL2（通过 `/proc/version`）并使用 `powershell.exe` 通过 .NET 的 `System.Windows.Forms.Clipboard` 访问 Windows 剪贴板。它内置于 WSL2 的 Windows 互操作中 - 默认情况下可用“powershell.exe”。

剪贴板数据通过 stdout 以 Base64 编码的 PNG 形式传输，因此不需要文件路径转换或临时文件。

:::info WSLg 注意
如果您正在运行 WSLg（支持 GUI 的 WSL2），OpenClaw 首先尝试 PowerShell 路径，然后回退到“wl-paste”。 WSLg 的剪贴板桥仅支持图像的 BMP 格式 - OpenClaw 使用 Pillow（如果已安装）或 ImageMagick 的“convert”命令自动将 BMP 转换为 PNG。
:::

#### 验证 WSL2 剪贴板访问

````bash
# 1.检查WSL检测
grep -i 微软/proc/版本

# 2. 检查 PowerShell 是否可访问
哪个powershell.exe

# 3. 复制图像，然后检查
powershell.exe -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::ContainsImage()"
# 应该打印“True”
````

## SSH 和远程会话

**剪贴板图像粘贴不能完全通过 SSH 工作。** 当您通过 SSH 连接到远程计算机时，Hermes CLI 将在远程主机上运行。剪贴板工具（“xclip”、“wl-paste”、“powershell.exe”、“osascript”）读取它们运行的​​计算机的剪贴板 - 这是远程服务器，而不是本地计算机。因此，您的本地剪贴板图像无法从远程端访问。

文本有时仍然可以通过终端粘贴或 OSC52 进行桥接，但图像剪贴板访问和本地屏幕截图临时路径仍然与运行 OpenClaw 的计算机相关联。

### SSH 的解决方法

1. **上传图像文件** — 将图像保存在本地，通过 `scp`、VSCode 的文件浏览器（拖放）或任何文件传输方法将其上传到远程服务器。然后通过路径引用它。 *（计划在未来版本中使用“/attach <filepath>”命令。）*

2. **使用 URL** — 如果可以在线访问图像，只需将 URL 粘贴到消息中即可。代理可以使用“vision_analyze”直接查看任何图像 URL。

3. **X11 转发** — 使用 `ssh -X` 连接以转发 X11。这允许远程计算机上的“xclip”访问本地 X11 剪贴板。需要本地运行的 X 服务器（macOS 上的 XQuartz，Linux X11 桌面上内置）。对于大图像来说速度较慢。

4. **使用消息传递平台** — 通过 Telegram、Discord、Slack 或 WhatsApp 将图像发送到 OpenClaw。这些平台本身处理图像上传，并且不受剪贴板/终端限制的影响。

## 为什么终端无法粘贴图片

这是一个常见的混淆来源，因此这是技术解释：

终端是**基于文本的**界面。当您按 Ctrl+V（或 Cmd+V）时，终端模拟器：

1.读取剪贴板的**文本内容**
2. 将其包裹在[括号粘贴](https://en.wikipedia.org/wiki/Bracketed-paste)转义序列中
3.通过终端的文本流发送给应用程序

如果剪贴板仅包含图像（无文本），则终端没有任何可发送的内容。二进制图像数据没有标准的终端转义序列。终端根本不执行任何操作。

这就是 OpenClaw 使用单独的剪贴板检查的原因 - 它不是通过终端粘贴事件接收图像数据，而是直接通过子进程调用操作系统级工具（`osascript`、`powershell.exe`、`xclip`、`wl-paste`）来独立读取剪贴板。

## 支持的型号

图像粘贴适用于任何具有视觉功能的模型。图像以 OpenAI 视觉内容格式作为 Base64 编码的数据 URL 发送：

```json
{
  “类型”：“图像_url”，
  “图像网址”：{
    "url": "数据:image/png;base64,..."
  }
}
````

大多数现代模型都支持这种格式，包括 GPT-4 Vision、Claude（有视觉）、Gemini 以及通过 OpenRouter 提供服务的开源多模式模型。

## 图像路由（支持视觉与仅文本模型）

当用户从 CLI 剪贴板、网关（Telegram/Discord 照片）或任何其他入口点附加图像时，OpenClaw 根据当前模型是否实际支持视觉来路由它：

|您的模型 |图像发生了什么？
|---|---|
| **有视觉能力**（GPT-4V、有视觉的克劳德、Gemini、Qwen-VL、MiMo-VL 等）|使用上述提供商的本机图像内容格式作为**真实像素**发送。无文本摘要层。 |
| **纯文本**（DeepSeek V3、较小的开源模型、较旧的仅聊天端点）|通过“vision_analyze”辅助工具进行路由——辅助视觉模型描述图像，并将文本描述注入到对话中。 |

您无需对此进行配置 - OpenClaw 会在提供者元数据中查找当前模型的功能并自动选择正确的路径。实际效果：您可以在会话中在视觉和非视觉模型之间切换，并且图像处理“正常工作”，而无需更改您的工作流程。纯文本模型获得有关图像的连贯上下文，而不是他们必须拒绝的破碎的多模态有效负载。

哪个辅助模型处理文本描述路径可以在 `auxiliary.vision` 下配置 - 请参阅[辅助模型](/user-guide/configuration#auxiliary-models)。

### `vision_analyze` 具有相同的双重行为

“vision_analyze”工具本身遵循相同的路线。当活动主模型具有视觉功能**且**其提供程序支持工具结果内的图像内容（当前为 Anthropic、OpenAI、Azure-OpenAI 和 Gemini 3.x 堆栈）时，“vision_analyze”会短路辅助描述器，并将原始图像像素作为多模式工具结果信封返回。主模型在下一轮中原生地看到图像 - 没有辅助调用，没有文本摘要信息丢失，没有额外的延迟。

对于纯文本主模型（或工具结果通道不携带图像的提供者），“vision_analyze”回退到遗留路径：它要求配置的辅助视觉模型描述图像并将描述作为纯文本返回。无论哪种方式，调用工具签名都是相同的 - 工具根据活动模型决定在运行时采用哪条路径。