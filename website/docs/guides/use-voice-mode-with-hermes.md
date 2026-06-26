---
sidebar_position: 8
title: "Use Voice Mode with OpenClaw"
description: "A practical guide to setting up and using OpenClaw voice mode across CLI, Telegram, Discord, and Discord voice channels"
---
# 使用 OpenClaw 语音模式

本指南是[语音模式功能参考](/user-guide/features/voice-mode) 的实用伴侣。

如果功能页面解释了语音模式的功能，那么本指南将展示如何实际使用它。

:::提示
[Nous Portal](/integrations/nous-portal) 通过一个 OAuth 将 LLM 和 TTS 捆绑在一起 — 语音模式可以端到端工作，无需额外的凭据。
:::

## 什么语音模式适合

语音模式在以下情况下特别有用：
- 您想要免提 CLI 工作流程
- 您想要在 Telegram 或 Discord 中进行口头回复
- 您希望 OpenClaw 坐在 Discord 语音频道中进行实时对话
- 您想要快速捕捉想法、调试或来回走动而不是打字

## 选择您的语音模式设置

OpenClaw 确实提供了三种不同的语音体验。

|模式|最适合 |平台|
|---|---|---|
|交互式麦克风环 |编码或研究时个人免提使用 |命令行 |
|聊天中语音回复 |与正常消息传递一起进行口头回复 |电报、不和谐 |
|实时语音频道机器人 | VC 中的小组或个人实时对话 | Discord 语音频道 |

一条好的路径是：
1. 首先让文本工作
2.第二次启用语音回复
3. 如果您想要完整的体验，请最后移至 Discord 语音频道

## 第 1 步：首先确保正常的 OpenClaw 可以正常工作

在触摸语音模式之前，请确认：
- 赫尔墨斯开始
- 您的提供商已配置
- 座席可以正常回答文字提示

````bash
爱马仕
````

问一些简单的事情：

````文本
你有什么可用的工具？
````

如果还不稳定，请先修复文本模式。

## 第 2 步：安装正确的附加组件

### CLI 麦克风 + 播放

````bash
pip install "hermes-agent[语音]"
````

### 消息平台

````bash
pip install "hermes-agent[消息]"
````

### 高级 ElevenLabs TTS

````bash
pip install “hermes-agent[tts-premium]”
````

### 本地 NeuTTS（可选）

````bash
python -m pip install -U neutts[全部]
````

### 一切

````bash
pip install "hermes-agent[全部]"
````

## 第三步：安装系统依赖项

### macOS

````bash
酿造安装portaudio ffmpeg opus
brew 安装 espeak-ng
````

### Ubuntu / Debian

````bash
sudo apt install portaudio19-dev ffmpeg libopus0
sudo apt install espeak-ng
````

为什么这些很重要：
- `portaudio` → CLI 语音模式的麦克风输入/播放
- `ffmpeg` → 用于 TTS 和消息传递的音频转换
- `opus` → Discord 语音编解码器支持
- `espeak-ng` → NeuTTS 的音素器后端

## 步骤 4：选择 STT 和 TTS 提供商

OpenClaw 支持本地和云语音堆栈。

### 最简单/最便宜的设置

使用本地 STT 和免费 Edge TTS：
- STT 提供商：“本地”
- TTS 提供商：`edge`

这通常是最好的起点。

### 环境文件示例

添加到`~/.hermes/.env`：

````bash
# 云STT选项（本地无需密钥）
GROQ_API_KEY=***
VOICE_TOOLS_OPENAI_KEY=***

# 高级 TTS（可选）
ELEVENLABS_API_KEY=***
````

### 提供商推荐

#### 语音转文本

- `local` → 隐私和零成本使用的最佳默认设置
- `groq` → 非常快的云转录
- `openai` → 报酬丰厚的后备方案

#### 文本转语音

- `edge` → 免费且对大多数用户来说足够好
- `neutts` → 免费本地/设备上 TTS
- `elevenlabs` → 最好的质量
- `openai` → 良好的中间立场
- `mistral` → 多语言、本土作品

### 如果你使用 `hermes setup`

如果您在安装向导中选择 NeuTTS，OpenClaw 会检查是否已安装“neutts”。如果缺少，向导会告诉您 NeuTTS 需要 Python 包“neutts”和系统包“espeak-ng”，为您提供安装它们，使用您的平台包管理器安装“espeak-ng”，然后运行：

````bash
python -m pip install -U neutts[全部]
````

如果您跳过该安装或安装失败，向导将退回到 Edge TTS。

## 步骤5：推荐配置

````yaml
声音：
  记录键：“ctrl+b”
  最大录制秒数：120
  auto_tts：假
  beep_enabled：真
  沉默阈值：200
  沉默持续时间：3.0

史特：
  提供者：“本地”
  本地：
    型号：“底座”

tts:
  提供者：“边缘”
  边缘：
    声音：“en-US-AriaNeural”
````

对于大多数人来说，这是一个很好的保守默认值。

如果您想要本地 TTS，请将“tts”块切换为：

````yaml
tts:
  提供者：“neutts”
  诺茨：
    参考音频：''
    参考文本：''
    型号: neutts-air-q4-gguf
    设备：CPU
````

## 使用案例 1：CLI 语音模式

## 打开它

启动赫尔墨斯：

````bash
爱马仕
````

CLI 内部：

````文本
/语音开启
````

### 录音流程

默认键：
- `Ctrl+B`

工作流程：
1. 按“Ctrl+B”
2. 说话
3.等待静音检测自动停止录音
4. OpenClaw转录并回复
5.如果TTS打开，它会说出答案
6.循环可自动重启连续使用

### 有用的命令

````文本
/声音
/语音开启
/声音关闭
/语音tts
/语音状态
````

### 良好的 CLI 工作流程

#### 直接调试

说：

````文本
我不断收到 docker 权限错误。帮我调试一下。
````

然后继续免提：
- “再次阅读最后一个错误”
- “用更简单的术语解释根本原因”
- “现在给我确切的解决方案”

#### 研究/头脑风暴

非常适合：
- 边走边思考
- 口述半成形的想法
- 要求 OpenClaw 实时构建你的想法

#### 辅助功能/低打字会话

如果打字不方便，语音模式是保持完整 OpenClaw 循环的最快方法之一。

## 调整 CLI 行为

### 沉默阈值

如果 OpenClaw 启动/停止过于激进，请调整：

````yaml
声音：
  沉默阈值：250
````

阈值越高=敏感度越低。

### 沉默持续时间

如果您在句子之间停顿很多，请增加：

````yaml
声音：
  沉默持续时间：4.0
````

### 记录键

如果 Ctrl+B 与你的终端或 tmux 习惯冲突：

````yaml
声音：
  记录键：“ctrl+空格”
````

## 用例 2：Telegram 或 Discord 中的语音回复

这种模式比全语音通道更简单。

OpenClaw 仍然是一个普通的聊天机器人，但可以进行语音回复。

### 启动网关

````bash
爱马仕网关
````

### 开启语音回复

Telegram 或 Discord 内部：

````文本
/语音开启
````

或

````文本
/语音tts
````

### 模式

|模式|意义|
|---|---|
| `关闭` |仅文本 |
| `仅语音` |仅当用户发送语音时才说话 |
| `全部` |说出每条回复|

### 何时使用哪种模式

- 如果您只想对语音消息进行语音回复，请使用“/voice on”
- 如果您一直想要一个完整的语音助手，请使用“/voice tts”

### 良好的消息传递工作流程

#### 手机上的 Telegram 助手

使用时：
- 你离开了你的机器
- 您想要发送语音留言并获得快速语音回复
- 您希望 OpenClaw 像便携式研究或操作助理一样发挥作用

#### 带有语音输出的 Discord DM

当您想要私人交互而不需要服务器通道提及行为时很有用。

## 用例 3：Discord 语音通道

这是最高级的模式。

OpenClaw 加入 Discord VC，聆听用户语音，进行转录，运行正常的代理管道，然后将回复返回到频道中。

## 所需的 Discord 权限

除了正常的文本机器人设置之外，请确保机器人具有：
- 连接
- 说话
- 最好使用语音活动

还可以在开发者门户中启用特权意图：
- 存在意图
- 服务器成员意图
- 消息内容意图

## 加入和离开

在机器人所在的 Discord 文本频道中：

````文本
/语音加入
/语音离开
/语音状态
````

### 加入后会发生什么

- 用户在 VC 中发言
- OpenClaw 检测语音边界
- 成绩单发布在相关的文本频道中
- 赫尔墨斯以文字和音频回应
- 文本通道是发出“/voice join”的通道

### Discord VC 使用最佳实践

- 保持“DISCORD_ALLOWED_USERS”紧密
- 首先使用专用的机器人/测试通道
- 在尝试 VC 模式之前验证 STT 和 TTS 在普通文本聊天语音模式下的工作情况

## 语音质量建议

### 最佳质量设置

- STT：本地 `large-v3` 或 Groq `whisper-large-v3`
- TTS：ElevenLabs

### 最佳速度/便利设置

- STT：本地“base”或 Groq
- TTS：边缘

### 最佳零成本设置

- STT：本地
- TTS：边缘

## 常见故障模式

###“未找到音频设备”

安装“portaudio”。

###“机器人加入但什么也没听到”

检查：
- 您的 Discord 用户 ID 位于“DISCORD_ALLOWED_USERS”中
- 你没有静音
- 启用特权意图
- 机器人具有连接/通话权限

###“它会转录但不会说话”

检查：
- TTS 提供商配置
- ElevenLabs 或 OpenAI 的 API 密钥/配额
- Edge 转换路径的“ffmpeg”安装

###“耳语输出垃圾”

尝试：
- 更安静的环境
- 更高的“silence_threshold”
- 不同的 STT 提供商/模型
- 更短、更清晰的话语

### “它在 DM 中有效，但在服务器通道中无效”

这就是经常提到的政策。

默认情况下，除非另有配置，机器人需要在 Discord 服务器文本通道中使用“@mention”。

## 建议的第一周设置

如果您想要最短的成功之路：

1. 获取文本 OpenClaw 工作
2.安装 `hermes-agent[语音]`
3.使用CLI语音模式与本地STT + Edge TTS
4. 然后在 Telegram 或 Discord 中启用“/voice on”
5.之后，尝试Discord VC模式

这种进展使调试表面保持较小。

## 接下来去哪里阅读

- [语音模式功能参考](/user-guide/features/voice-mode)
- [消息网关](/user-guide/messaging)
- [Discord 设置](/user-guide/messaging/discord)
- [电报设置](/用户指南/消息/电报)
- [配置](/用户指南/配置)