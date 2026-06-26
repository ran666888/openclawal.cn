---
title: "Inference Sh Cli — Run 150+ AI apps via inference"
sidebar_label: "Inference Sh Cli"
description: "Run 150+ AI apps via inference"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 推理 CLI

通过 inference.sh CLI (infsh) 运行 150 多个 AI 应用程序 — 图像生成、视频创建、法学硕士、搜索、3D、社交自动化。使用终端工具。触发器：inference.sh、infsh、ai apps、flux、veo、图像生成、视频生成、seedream、seedance、tavily

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/devops/cli` 安装 |
|路径| `可选技能/de​​vops/cli` |
|版本 | `1.0.0` |
|作者 |奥卡里斯 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `AI`、`图像生成`、`视频`、`LLM`、`搜索`、`推理`、`FLUX`、`Veo`、`Claude` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# inference.sh CLI

使用简单的 CLI 在云中运行 150 多个 AI 应用程序。无需 GPU。

所有命令都使用 **终端工具** 来运行 `infsh` 命令。

## 何时使用

- 用户要求生成图像（FLUX、Reve、Seedream、Grok、Gemini 图像）
- 用户要求生成视频（Veo、Wan、Seedance、OmniHuman）
- 用户询问 inference.sh 或 infsh
- 用户希望运行人工智能应用程序而无需管理单独的提供商 API
- 用户请求人工智能驱动的搜索（Tavily、Exa）
- 用户需要头像/口型同步生成

## 先决条件

必须安装并验证“infsh”CLI。检查：

````bash
影响我
````

如果没有安装：

````bash
卷曲-fsSL https://cli.inference.sh |嘘
登录
````

有关完整设置详细信息，请参阅“references/authentication.md”。

## 工作流程

### 1. 始终先搜索

切勿猜测应用程序名称 - 始终搜索以查找正确的应用程序 ID：

````bash
infsh 应用程序列表--搜索通量
infsh应用程序列表--搜索视频
infsh应用程序列表--搜索图像
````

### 2. 运行应用程序

使用搜索结果中的确切应用程序 ID。始终使用“--json”作为机器可读的输出：

````bash
infsh app run <app-id> --input '{"prompt": "您的提示在这里"}' --json
````

### 3. 解析输出

JSON 输出包含生成媒体的 URL。使用“MEDIA:<url>”将这些内容呈现给用户以进行内联显示。

## 常用命令

### 图像生成

````bash
# 搜索图像应用程序
infsh应用程序列表--搜索图像

# 使用 LoRA 进行 FLUX 开发
infsh app run falai/flux-dev-lora --input '{"prompt": "sunset over mountain", "num_images": 1}' --json

# 双子座图像生成
infsh 应用运行 google/gemini-2-5-flash-image --input '{"prompt": "futuristic city", "num_images": 1}' --json

# Seedream（字节跳动）
infsh app run bytedance/seedream-5-lite --input '{"prompt": "nature scene"}' --json

# 格洛克想象 (xAI)
infsh 应用运行 xai/grok-imagine-image --input '{"prompt": "abstract art"}' --json
````

### 视频生成

````bash
# 搜索视频应用
infsh应用程序列表--搜索视频

# Veo 3.1（谷歌）
infsh 应用程序运行 google/veo-3-1-fast --input '{"prompt": "无人机拍摄的海岸线"}' --json

# Seedance（字节跳动）
infsh app run bytedance/seedance-1-5-pro --input '{"prompt": "舞蹈人物", "resolution": "1080p"}' --json

#万2.5
infsh app run falai/wan-2-5 --input '{"prompt": "person Walking through city"}' --json
````

### 本地文件上传

当您提供路径时，CLI 会自动上传本地文件：

````bash
# 升级本地图像
infsh app run falai/topaz-image-upscaler --input '{"image": "/path/to/photo.jpg", "upscale_factor": 2}' --json

# 从本地文件将图像转为视频
infsh app run falai/wan-2-5-i2v --input '{"image": "/path/to/image.png", "prompt": "make it move"}' --json

# 带声音的头像
infsh app run bytedance/omni human-1-5 --input '{"audio": "/path/to/audio.mp3", "image": "/path/to/face.jpg"}' --json
````

### 搜索与研究

````bash
infsh 应用列表 --search 搜索
infsh app run tavily/tavily-search --input '{"query": "latest AI news"}' --json
infsh app run exa/exa-search --input '{"query": "机器学习论文"}' --json
````

### 其他类别

````bash
# 3D生成
infsh 应用程序列表 --search 3d

# 音频/TTS
infsh 应用列表 --搜索 tts

# Twitter/X 自动化
infsh 应用列表——搜索 twitter
````

## 陷阱

1. **永远不要猜测应用程序 ID** — 始终首先运行 `infsh app list --search <term>`。应用程序 ID 发生变化，并且经常添加新应用程序。
2. **始终使用 `--json`** — 原始输出很难解析。 `--json` 标志提供带有 URL 的结构化输出。
3. **检查身份验证** — 如果命令因身份验证错误而失败，请运行“infsh login”或验证“INFSH_API_KEY”是否已设置。
4. **长时间运行的应用程序** — 视频生成可能需要 30-120 秒。终端工具超时应该足够，但警告用户可能需要一些时间。
5. **输入格式** — `--input` 标志采用 JSON 字符串。确保正确转义引号。

## 参考文档

- `references/authentication.md` — 设置、登录、API 密钥
- `references/app-discovery.md` — 搜索和浏览应用程序目录
- `references/running-apps.md` — 运行应用程序、输入格式、输出处理
- `references/cli-reference.md` — 完整的 CLI 命令参考