---
title: Image Generation
description: Generate images via FAL.ai — 11 models including FLUX 2, GPT Image (1.5 & 2), Nano Banana Pro, Ideogram, Recraft V4 Pro, Krea 2, and more, selectable via `hermes tools`.
sidebar_label: Image Generation
sidebar_position: 6
---
# 图像生成

OpenClaw 通过 FAL.ai 根据文本提示生成图像。开箱即用地支持 11 种模型，每种模型都有不同的速度、质量和成本权衡。活动模型可由用户通过“hermes tools”进行配置，并保留在“config.yaml”中。

## 支持的型号

|型号|速度|优势 |价格|
|---|---|---|---|
| `fal-ai/flux-2/klein/9b` *（默认）* | `<1s` |快速、清晰的文本 | $0.006/MP |
| `fal-ai/flux-2-pro` | 〜6秒|工作室照相写实主义| $0.03/MP |
| `fal-ai/z-image/turbo` | 〜2秒| EN/CN 双语，6B 参数 | $0.005/MP |
| `fal-ai/nano-banana-pro` | 〜8s | Gemini 3 Pro，推理深度，文字渲染| $0.15/图片 (1K) |
| `fal-ai/gpt-image-1.5` | 〜15秒|立即遵守 | $0.034/图片 |
| `fal-ai/gpt-image-2` | ~20 秒 | SOTA文字渲染+中日韩，世界感知的真实感 | $0.04–0.06/图片 |
| `fal-ai/ideogram/v3` | 〜5秒|最佳版式| $0.03–0.09/图片 |
| `fal-ai/recraft/v4/pro/text-to-image` | 〜8s |设计、品牌系统、生产就绪| $0.25/图片 |
| `fal-ai/qwen-image` | 〜12秒|基于法学硕士的复杂文本 | $0.02/MP |
| `fal-ai/krea/v2/medium/文本到图像` | ~15-25 秒 |插图、动漫、绘画、表现/艺术风格 | $0.030–0.035/图像 |
| `fal-ai/krea/v2/large/文本到图像` | ~25-60 秒 |真实感、原始纹理外观（运动模糊、颗粒、胶片）| $0.060–0.065/图像 |

价格为撰写本文时 FAL 的定价；检查 [fal.ai](https://fal.ai/) 了解当前数字。

## 设置

:::提示诺斯订阅者
如果您有付费的 [Nous Portal](https://portal.nousresearch.com) 订阅，则可以通过 **[工具网关](tool-gateway.md)** 使用图像生成，无需 FAL API 密钥。您的模型选择在两条路径中都保持不变。新安装可以运行“hermes setup --portal”来登录并立即打开每个网关工具；现有安装可以通过“hermes 工具”选择 **Nous 订阅** 作为图像生成后端。

如果托管网关针对特定模型返回“HTTP 4xx”，则该模型尚未在门户端进行代理 - 代理会告诉您这一点，并提供补救步骤（设置“FAL_KEY”以进行直接访问，或选择不同的模型）。
:::

### 获取 FAL API 密钥

1. 注册[fal.ai](https://fal.ai/)
2. 从仪表板生成 API 密钥

### 配置并选择模型

运行工具命令：

````bash
爱马仕工具
````

导航至 **🎨 图像生成**，选择您的后端（Nous Subscription 或 FAL.ai），然后选择器会在列对齐表格中显示所有支持的模型 - 箭头键进行导航，Enter 进行选择：

````
  型号 速度 优势 价格
  fal-ai/flux-2/klein/9b <1s 快速、清晰的文本 $0.006/MP ← 当前使用
  fal-ai/flux-2-pro ~6s Studio 真实感 $0.03/MP
  fal-ai/z-image/turbo ~2s 双语 EN/CN, 6B $0.005/MP
  ...
````

您的选择将保存到“config.yaml”：

````yaml
图像生成：
  型号: fal-ai/flux-2/klein/9b
  use_gateway: false # 如果使用 Nous 订阅则为 true
````

### GPT-图像质量

“fal-ai/gpt-image-1.5”和“fal-ai/gpt-image-2”请求质量固定为“中”（~$0.034–$0.06/图像，1024×1024）。我们不会将“低”/“高”层公开为面向用户的选项，以便所有用户的 Nous Portal 计费保持可预测性 - 层之间的成本差为 3-22 倍。如果您想要更便宜的选择，请选择 Klein 9B 或 Z-Image Turbo；如果您想要更高的质量，请使用 Nano Banana Pro 或 Recraft V4 Pro。

## 用法

面向代理的模式有意最小化——模型会选择您配置的任何内容：

````
生成带有樱花的宁静山景图像
````

````
创建一只聪明的老猫头鹰的方形肖像 - 使用版式模型
````

````
给我一个未来的城市景观，景观定位
````

## 图像到图像/编辑

当活动时，相同的“image_generate”工具也**编辑现有图像**
模型支持它 - 将源图像和后端路由传递到其编辑
自动端点（镜像“video_generate”如何处理图像到视频）。
省略源图像，它是纯文本到图像。

````
拍这张照片，让它成为东京夜晚下雨的街道 → <image>
````

````
将这两张产品照片融合成一张主图 → <image1> <image2>
````

两个输入驱动编辑：

- **`image_url`** — 要编辑/转换的主要源图像（公共 URL 或本地路径）。
- **`reference_image_urls`** — 附加样式/构图参考（每个模型上限）。

### 哪些后端支持编辑

|后端 |图像到图像 |参考上限|如何|
|---|---|---|---|
| **FAL.ai**（下面可编辑的模型）| ✓ |最多 9 |路由到模型的“/edit”端点 |
| **OpenAI** (`gpt-image-2`) | ✓ |最多 16 个 | `images.edit()` |
| **xAI**（Grok Imagine）| ✓ | 1 | `/v1/images/edits` (`grok-imagine-image-quality`) |
| **韩国** (`韩国 2`) | ✓ |最多 10 个 |参考引导生成（`image_style_references`）|
| **OpenAI（法典认证）** | ✗ | — |仅文本到图像 |

具有编辑端点的 FAL 模型：`flux-2/klein/9b`、`flux-2-pro`、
`nano-banana-pro`、`gpt-image-1.5`、`gpt-image-2`、`ideogram/v3` 和
`qwen-图像`。纯文本到图像的 FAL 模型（`z-image/turbo`、`recraft`、
`krea/*`) 拒绝图像输入，并显示一个明确的错误，指出
可编辑的模型。

活动模型的编辑功能显示在工具描述中，网址为
运行时，因此代理知道在它之前是否会遵守“image_url”
调用该工具。

## 纵横比

从代理的角度来看，每个模型都接受相同的三个长宽比。在内部，每个模型的原始尺寸规格都会自动填充：

|代理输入| image_size (flux/z-image/qwen/recraft/ideogram) | image_size (flux/z-image/qwen/recraft/ideogram) |纵横比 (nano-banana-pro) |图像大小（gpt-image-1.5）|图像大小 (gpt-image-2) |
|---|---|---|---|---|
| `风景` | `景观_16_9` | `16:9` | `1536x1024` | `风景_4_3` (1024×768) |
| `正方形` | `square_hd` | `1:1` | `1024x1024` | `square_hd` (1024×1024) |
| `肖像` | `肖像_16_9` | `9:16` | `1024x1536` | `肖像_4_3` (768×1024) |

GPT 图像 2 映射到 4:3 预设而不是 16:9，因为其最小像素数为 655,360 — “landscape_16_9”预设 (1024×576 = 589,824) 将被拒绝。

这种转换发生在“_build_fal_payload()”中——代理代码永远不需要知道每个模型的架构差异。

## 自动升级

通过 FAL 的 **Clarity Upscaler** 进行的升级按模型进行门控：

|型号|高档？ |为什么 |
|---|---|---|
| `fal-ai/flux-2-pro` | ✓ |向后兼容（是预选择器默认值）|
|所有其他 | ✗ |快速模型将失去其亚秒级的价值支撑；高分辨率模型不需要它|

运行升级时，它使用以下设置：

|设置|价值|
|---|---|
|高档因素| 2×|
|创意| 0.35 | 0.35
|相似度| 0.6 | 0.6
|指导尺度| 4 |
|推理步骤| 18 | 18

如果升级失败（网络问题、速率限制），则会自动返回原始图像。

## 内部如何运作

1. **模型解析** — `_resolve_fal_model()` 从 `config.yaml` 读取 `image_gen.model`，回退到 `FAL_IMAGE_MODEL` 环境变量，然后回退到 `fal-ai/flux-2/klein/9b`。
2. **有效负载构建** - `_build_fal_payload()` 将您的 `aspect_ratio` 转换为模型的本机格式（预设枚举、aspect-ratio 枚举或 GPT 文字），合并模型的默认参数，应用任何调用者覆盖，然后过滤到模型的 `supports` 白名单，以便永远不会发送不支持的密钥。
3. **提交** — `_submit_fal_request()` 通过直接 FAL 凭证或托管 Nous 网关进行路由。
4. **升级** — 仅当模型的元数据具有“upscale: True”时运行。
5. **Delivery** — 返回给代理的最终图像 URL，代理发出一个“MEDIA:<url>”标签，平台适配器将其转换为本机媒体。

## 调试

启用调试日志记录：

````bash
导出 IMAGE_TOOLS_DEBUG=true
````

调试日志转到“./logs/image_tools_debug_<session_id>.json”，其中包含每次调用的详细信息（模型、参数、计时、错误）。

## 平台交付

|平台|交货|
|---|---|
| **命令行** |图像 URL 打印为 markdown `![](url)` — 单击打开 |
| **电报** |以提示为标题的照片消息 |
| **不和谐** |嵌入消息 |
| **松弛** | Slack 展开的 URL |
| **WhatsApp** |媒体留言|
| **其他** |纯文本 URL |

## 限制

- **需要活动后端的凭据**（FAL `FAL_KEY` / Nous 订阅、`OPENAI_API_KEY`、xAI OAuth、`KREA_API_KEY`）
- **编辑取决于模型** — 图像到图像仅适用于可编辑的模型（请参见上表）；仅文本到图像的模型拒绝图像输入并出现明显错误
- **临时 URL** — 后端返回几小时/天后过期的托管 URL； OpenClaw 将它们具体化到本地缓存，因此过期后交付仍然有效
- **每个模型的约束** - 某些模型不支持 `seed`、`num_inference_steps` 等。`supports` / `edit_supports` 过滤器会默默地删除不支持的参数；这是预期的行为