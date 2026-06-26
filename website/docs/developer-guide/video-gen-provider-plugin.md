---
sidebar_position: 12
title: "Video Generation Provider Plugins"
description: "如何为 OpenClaw 构建视频生成后端插件"
---
# 构建视频生成提供商插件

视频生成提供商插件注册一个为每个“video_generate”工具调用提供服务的后端。内置提供程序（xAI、FAL）作为插件提供。通过将目录拖放到“plugins/video_gen/<name>/”中，添加新的目录或覆盖捆绑的目录。

:::提示
Video-gen 几乎逐行镜像 [图像生成提供程序插件](/developer-guide/image-gen-provider-plugin) — 如果您构建了图像生成后端，那么您已经知道其形状。主要区别：“capability()”方法广告模式/宽高比/持续时间，以及路由约定（传递“image_url”以使用图像到视频，省略它以使用文本到视频 - 提供者在内部选择正确的端点）。
:::

## 统一的表面（一种工具，两种模式）

“video_generate”工具通过一个参数公开两种模式：

- **文本到视频** — 仅使用“提示”进行呼叫。提供者路由到其文本到视频端点。
- **图像到视频** — 使用 `prompt` + `image_url` 进行调用。提供者路由到其图像到视频端点。

编辑和扩展故意超出范围。大多数后端不支持它们，并且不一致将迫使每个后端的散文进入代理的工具描述中。

## 发现如何运作

OpenClaw 在三个位置扫描视频生成后端：

1. **捆绑** — `<repo>/plugins/video_gen/<name>/` （自动加载 `kind: backend`）
2. **用户** — `~/.hermes/plugins/video_gen/<name>/` （通过 `plugins.enabled` 选择加入）
3. **Pip** — 声明 `hermes_agent.plugins` 入口点的包

每个插件的“register(ctx)”函数都会调用“ctx.register_video_gen_provider(...)”。活动提供者由“config.yaml”中的“video_gen.provider”选择； `hermes 工具` → 视频生成引导用户进行选择。与“image_generate”不同，没有树内遗留后端——每个提供程序都是一个插件。

## 目录结构

````
插件/video_gen/my-backend/
├── __init__.py # VideoGenProvider 子类 + register()
└──plugin.yaml # 清单类型：后端
````

## VideoGenProvider ABC

子类“agent.video_gen_provider.VideoGenProvider”。必需：“name”属性和“generate()”方法。

````蟒蛇
# 插件/video_gen/my-backend/__init__.py
从输入导入任何、字典、列表、可选
导入操作系统

从agent.video_gen_provider导入（
    视频生成提供商，
    错误响应，
    成功响应，
）


类 MyVideoGenProvider(VideoGenProvider):
    @属性
    def 名称(自身) -> str:
        返回“我的后端”

    @属性
    def display_name(self) -> str：
        返回“我的后端”

    def is_available(self) -> bool:
        返回 bool(os.environ.get("MY_API_KEY"))

    def list_models(self) -> List[Dict[str, Any]]:
        # 每个条目都是一个模型家族——用户选择一次的名称。
        # 您的提供商在系列内的generate()路线基于
        # image_url 是否被传递。
        返回[
            {
                “id”：“快”，
                “显示”：“快”，
                “速度”：“~30秒”，
                "strengths": "最便宜的级别",
                “价格”：“$0.05/秒”，
                "modalities": ["text", "image"], # 咨询
            },
        ]

    def default_model(self) -> 可选[str]:
        返回“快”

    def 能力(self) -> Dict[str, Any]:
        返回{
            “模式”：[“文本”，“图像”]，
            “纵横比”：[“16：9”，“9：16”]，
            “分辨率”：[“720p”，“1080p”]，
            “最短持续时间”：1，
            “最大持续时间”：10，
            “supports_audio”：错误，
            “支持负提示”：正确，
            “最大参考图像”：0，
        }

    def get_setup_schema(self) -> Dict[str, Any]:
        返回{
            "name": "我的后端",
            “徽章”：“已付费”，
            "tag": "`hermes 工具`中显示的简短描述",
            “env_vars”：[
                {
                    “密钥”：“MY_API_KEY”，
                    "prompt": "我的后端 API 密钥",
                    “url”：“https://mybackend.example.com/keys”，
                },
            ],
        }

    def 生成(
        自我,
        提示：str，
        *,
        型号：可选[str] =无，
        image_url：可选[str] =无，
        Reference_image_urls：可选[列表[str]] =无，
        持续时间：可选[int] =无，
        纵横比：str =“16：9”，
        分辨率：str =“720p”，
        negative_prompt：可选[str] =无，
        音频：可选[布尔] = 无，
        种子：可选[int] =无，
        **kwargs: Any, # 始终忽略未知的 kwargs 以实现前向兼容
    ) -> 字典[str, 任意]:
        # ROUTE: image_url 存在选择端点。
        如果图像网址：
            端点 =“我的后端/图像到视频”
            modality_used =“图像”
        其他：
            端点 =“我的后端/文本转视频”
            modality_used =“文本”

        # ...调用您的API ...

        返回成功响应（
            视频=“https://your-cdn/output.mp4”，
            model=模型或“快速”，
            提示=提示，
            模态=modality_used，
            纵横比=纵横比，
            持续时间=持续时间或5，
            提供者=自我名称，
        ）


def 寄存器(ctx) -> 无:
    ctx.register_video_gen_provider(MyVideoGenProvider())
````

## 插件清单

````yaml
# 插件/video_gen/my-backend/plugin.yaml
名称：我的后端
版本：1.0.0
描述：“我的视频生成后端”
作者：你的名字
种类：后端
需要环境：
  - MY_API_KEY
````

## `video_generate` 模式

该工具在每个后端公开一个模式。提供者会忽略他们不支持的参数。

|参数|它有什么作用 |
|---|---|
| `提示` |文字说明（必填）|
| `image_url` |当设置→图像转视频；省略时 → 文本转视频 |
| `reference_image_urls` |样式/字符参考（取决于提供商）|
| `持续时间` |秒 — 供应商夹 |
| `纵横比` | `"16:9"`、`"9:16"`、`"1:1"`、... — 提供者钳位 |
| `决议` | `"480p"` / `"540p"` / `"720p"` / `"1080p"` — 提供商限制 |
| `否定提示` |应避免的内容（仅限 Pixverse/Kling）|
| `音频` |原生音频（Veo3 / Pixverse 定价层）|
| `种子` |再现性|
| `模型` |覆盖活动模型/系列 |

提供者的“capability()”公布了其中哪些是受到尊重的。代理在工具描述中看到活动后端的功能，当用户通过“hermes tools”更改后端时动态重建。

## 模型系列和端点路由（FAL 模式）

当您的后端每个“模型”有多个端点时（例如 FAL，其中每个系列（Veo 3.1、Pixverse v6、Kling O3）都有“/text-to-video”和“/image-to-video” URL）— 将每个“系列”表示为一个目录条目。你的generate()根据是否传递了image_url来选择正确的端点：

````蟒蛇
家庭 = {
    “veo3.1”：{
        "text_endpoint": "fal-ai/veo3.1",
        "image_endpoint": "fal-ai/veo3.1/图像到视频",
        # ...系列特定的功能标志...
    },
}

def 生成（自我，提示，*，image_url=无，模型=无，**kwargs）：
    family_id, family = _resolve_family(模型)
    端点 = family["image_endpoint"] if image_url else family["text_endpoint"]
    # ...根据系列声明的功能标志构建有效负载，调用端点...
````

用户在“hermes tools”中选择“veo3.1”一次。代理从不考虑端点——它只是传递（或不传递）“image_url”。

## 选择优先级

对于每个实例的模型旋钮（请参阅“plugins/video_gen/fal/__init__.py”）：

1. 工具调用中的`model=`关键字
2. `<PROVIDER>_VIDEO_MODEL` 环境变量
3.`config.yaml`中的`video_gen.<provider>.model`
4. `config.yaml` 中的 `video_gen.model` （当它是您的 ID 之一时）
5. 提供者的`default_model()`

## 响应形状

`success_response()` 和 `error_response()` 生成每个后端返回的字典形状。使用它们——不要手写字典。

成功键：`success`、`video`（URL 或绝对路径）、`model`、`prompt`、`modality`（`"text"` 或 `"image"`）、`aspect_ratio`、`duration`、`provider` 以及 `extra`。

错误键：`success`、`video`（无）、`error`、`error_type`、`model`、`prompt`、`aspect_ratio`、`provider`。

## 在哪里保存工件

如果你的后端返回base64，请使用`save_b64_video()`在`$HERMES_HOME/cache/videos/`下写入。对于后续 HTTP 获取的原始字节，请使用“save_bytes_video()”。否则直接返回上游 URL — 网关在交付时解析远程 URL。

## 测试

在“tests/plugins/video_gen/test_<name>_plugin.py”下进行冒烟测试。 xAI 和 FAL 测试显示了该模式 - 注册、验证目录、使用或不使用“image_url”执行路由、在缺少身份验证时断言干净的错误响应。