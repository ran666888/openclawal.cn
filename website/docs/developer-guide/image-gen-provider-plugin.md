---
sidebar_position: 11
title: "Image Generation Provider Plugins"
description: "如何为 OpenClaw 构建图像生成后端插件"
---
# 构建图像生成提供程序插件

Image-gen 提供程序插件注册一个为每个“image_generate”工具调用提供服务的后端 - DALL·E、gpt-image、Grok、Flux、Imagen、Stable Diffusion、fal、Replicate、本地 ComfyUI 设备等等。内置提供程序（OpenAI、OpenAI-Codex、xAI）均作为插件提供。您可以通过将目录放入“plugins/image_gen/<name>/”来添加新的，或覆盖捆绑的。

:::提示
Image-gen 是 OpenClaw 支持的几个 **后端插件** 之一。其他（具有更专业的 ABC）是 [内存提供程序插件](/developer-guide/memory-provider-plugin)、[上下文引擎插件](/developer-guide/context-engine-plugin) 和 [模型提供程序插件](/developer-guide/model-provider-plugin)。通用工具/hook/CLI 插件位于 [构建 OpenClaw 插件](/guides/build-a-hermes-plugin)。
:::

## 发现如何运作

OpenClaw 在三个位置扫描图像生成后端：

1. **捆绑** — `<repo>/plugins/image_gen/<name>/` （自动加载 `kind: backend`，始终可用）
2. **用户** — `~/.hermes/plugins/image_gen/<name>/` （通过 `plugins.enabled` 选择加入）
3. **Pip** — 声明 `hermes_agent.plugins` 入口点的包

每个插件的“register(ctx)”函数都会调用“ctx.register_image_gen_provider(...)”——将其放入“agent/image_gen_registry.py”中的注册表中。活动提供者由“config.yaml”中的“image_gen.provider”选择； “hermes 工具”引导用户进行选择。

“image_generate”工具包装器向注册表询问活动提供者并在那里调度。如果没有注册提供者，该工具会显示一个有用的错误，指向“hermes tools”。

## 目录结构

````
插件/image_gen/my-backend/
├── __init__.py # ImageGenProvider 子类 + register()
└──plugin.yaml # 清单类型：后端
````

至此，一个捆绑插件就完成了。需要将`~/.hermes/plugins/image_gen/<name>/`中的用户插件添加到`config.yaml`中的`plugins.enabled`中（或运行`hermes plugins enable <name>`）。

## ImageGenProvider ABC

子类“agent.image_gen_provider.ImageGenProvider”。唯一需要的成员是“name”属性和“generate()”方法——其他所有成员都有合理的默认值：

````蟒蛇
# 插件/image_gen/my-backend/__init__.py
从输入导入任何、字典、列表、可选
导入操作系统

从agent.image_gen_provider导入（
    默认宽高比，
    图像生成器,
    错误响应，
    标准化_参考_图像，
    解析纵横比，
    保存_b64_图像，
    成功响应，
）


类 MyBackendImageGenProvider(ImageGenProvider):
    @属性
    def 名称(自身) -> str:
        # image_gen.provider 配置中使用的稳定 ID。小写，无空格。
        返回“我的后端”

    @属性
    def display_name(self) -> str：
        # `hermes tools` 中显示的人类标签。如果省略，则默认为 name.title()。
        返回“我的后端”

    def is_available(self) -> bool:
        # 如果缺少凭据或依赖项，则返回 False。
        # 该工具的可用性门在调度之前调用它。
        如果不是 os.environ.get("MY_BACKEND_API_KEY")：
            返回错误
        尝试：
            导入 my_backend_sdk # noqa: F401
        除了导入错误：
            返回错误
        返回真

    def list_models(self) -> List[Dict[str, Any]]:
        # `hermes tools` 模型选择器中显示的目录。
        返回[
            {
                “id”：“我的模型快”，
                "display": "我的模型（快速）",
                "速度": "~5s",
                "strengths": "快速迭代",
                "价格": "$0.01/图片",
            },
            {
                “id”：“我的模型总部”，
                "display": "我的模型（总部）",
                “速度”：“~30秒”，
                "strengths": "最高保真度",
                "价格": "$0.04/图片",
            },
        ]

    def default_model(self) -> 可选[str]:
        返回“我的模型快速”

    def get_setup_schema(self) -> Dict[str, Any]:
        # `hermes tools` 选择器的元数据 — 设置时提示输入的键。
        返回{
            "name": "我的后端",
            "badge": "付费", # 可选;在选择器中显示为短标签
            "tag": "名称下显示一行描述",
            “env_vars”：[
                {
                    “密钥”：“MY_BACKEND_API_KEY”，
                    "prompt": "我的后端 API 密钥",
                    “url”：“https://my-backend.example.com/api-keys”，
                },
            ],
        }

    def 能力(self) -> Dict[str, Any]:
        # 声明该后端是否支持图像到图像/编辑。
        # 工具层在动态模式中显示这一点，因此模型
        # 知道何时尊重`image_url`。默认值（如果省略此项）是
        # 纯文本：{“modalities”：[“text”]，“max_reference_images”：0}。
        返回{“modalities”：[“text”，“image”]，“max_reference_images”：4}

    def 生成(
        自我,
        提示：str，
        纵横比：str = DEFAULT_ASPECT_RATIO，
        *,
        image_url：可选[str] =无，
        Reference_image_urls：可选[列表[str]] =无，
        **kwargs：任何，
    ) -> 字典[str, 任意]:
        提示=（提示或“”）.strip()
        纵横比 = 解析纵横比（纵横比）

        如果没有提示：
            返回错误响应（
                error="需要提示",
                error_type="invalid_input",
                提供者=自我名称，
                提示=“”，
                纵横比=纵横比，
            ）

        # 路由：如果设置了image_url（或reference_image_urls），则调用
        # 图像到图像/编辑请求；否则文本到图像。报告
        # 您通过 success_response 的 `modality` 字段选择了哪条路径。
        来源=[]
        如果图像网址：
            来源.append(image_url)
        resources.extend(normalize_reference_images(reference_image_urls) 或 [])
        如果来源为“文本”，则模态 =“图像”

        # 模型选择优先级：env var → config → default。帮手
        # 内置openai插件中的_resolve_model()是一个很好的参考。
        model_id = kwargs.get("model") 或 self.default_model() 或 "my-model-fast"

        尝试：
            导入 my_backend_sdk
            客户端 = my_backend_sdk.Client(api_key=os.environ["MY_BACKEND_API_KEY"])
            如果模态==“图像”：
                结果 = 客户端.编辑(
                    提示=提示，
                    型号=型号_id，
                    image_urls=来源，
                ）
            其他：
                结果 = 客户端.生成(
                    提示=提示，
                    型号=型号_id，
                    纵横比=纵横比，
                ）

            # 支持两种形状：
            # - URL 字符串：将其作为“image”返回
            # - base64数据：通过save_b64_image()保存在$HERMES_HOME/cache/images/下
            if result.get("image_b64"):
                路径 = save_b64_image(
                    结果[“image_b64”]，
                    前缀=self.name,
                    扩展名=“png”，
                ）
                图像 = str(路径)
            其他：
                图像=结果[“image_url”]

            返回成功响应（
                图像=图像，
                型号=型号_id，
                提示=提示，
                纵横比=纵横比，
                提供者=自我名称，
                模态=模态，
            ）
        except 异常作为例外：
            返回错误响应（
                错误=str（排除），
                error_type=类型(exc).__name__,
                提供者=自我名称，
                型号=型号_id，
                提示=提示，
                纵横比=纵横比，
            ）


def 寄存器(ctx) -> 无:
    """插件入口点 - 在加载时调用一次。"""
    ctx.register_image_gen_provider(MyBackendImageGenProvider())
````

## 插件.yaml

````yaml
名称：我的后端
版本：1.0.0
描述：我的图像后端 - 通过我的后端 SDK 进行文本到图像的转换
作者：你的名字
种类：后端
需要环境：
  - MY_BACKEND_API_KEY
````

`kind: backend` 是将插件路由到 image-gen 注册路径的。在“hermes插件安装”期间会提示“requires_env”。

## ABC 参考

完整合约位于“agent/image_gen_provider.py”中。您通常会重写的方法：

|会员|必填|默认 |目的|
|---|---|---|---|
| `名称` | ✅ | — | `image_gen.provider` 配置中使用的稳定 ID |
| `显示名称` | — | `name.title()` | “hermes 工具”中显示的标签 |
| `is_available()` | — | '真实' |缺少信用/部门的大门 |
| `list_models()` | — | `[]` | “hermes 工具”模型选择器目录 |
| `default_model()` | — |首先来自 `list_models()` |未配置模型时的回退 |
| `get_setup_schema()` | — |最小|选择器元数据 + env-var 提示 |
| `生成（提示，aspect_ratio，**kwargs）` | ✅ | — |来电|

## 响应格式

`generate()` 必须返回一个通过 `success_response()` 或 `error_response()` 构建的字典。两者都位于“agent/image_gen_provider.py”中。

**成功：**
````蟒蛇
成功响应（
    image=<url 或绝对路径>,
    型号=<型号ID>,
    提示=<回显提示>，
    宽高比=“横向” | “方形”| “肖像”，
    提供商=<您的提供商名称>，
    extra={...}, # 可选的后端特定字段
）
````

**错误：**
````蟒蛇
错误响应（
    错误=“人类可读的消息”，
    error_type =“provider_error” | “无效输入”| "<异常类名>",
    提供商=<您的提供商名称>，
    型号=<型号ID>,
    提示=<提示>,
    spect_ratio=<已解析的方面>,
）
````

工具包装器 JSON 序列化字典并将其交给 LLM。错误会作为工具结果出现；法学硕士决定如何向用户解释它们。

## 处理 base64 与 URL 输出

一些后端返回图像 URL（fal、Replicate）；其他返回 base64 有效负载 (OpenAI gpt-image-2)。对于 Base64 情况，使用 `save_b64_image()` — 它写入 `$HERMES_HOME/cache/images/<prefix>_<timestamp>_<uuid>.<ext>` 并返回绝对 `Path`。在 `success_response()` 中将该路径（作为 `str`）作为 `image=` 传递。网关传送（Telegram 照片气泡、Discord 附件）可识别 URL 和绝对路径。

## 用户覆盖

将一个用户插件放在 `~/.hermes/plugins/image_gen/<name>/` 中，并与捆绑的插件具有相同的 `name` 属性，并通过 `hermes plugins enable <name>` 启用它 - 注册表是最后写入者获胜，因此您的版本会替换内置版本。对于将“openai”插件指向私有代理或在自定义模型目录中进行交换非常有用。

## 测试

````bash
导出 HERMES_HOME=/tmp/hermes-imggen-test
mkdir -p $HERMES_HOME/plugins/image_gen/my-backend
# ...将 __init__.py + plugin.yaml 复制到该目录中...

导出 MY_BACKEND_API_KEY=您的测试密钥
Hermes 插件启用 my-backend

# 选择它作为活跃的提供者
echo "image_gen:" >> $HERMES_HOME/config.yaml
echo“提供商：我的后端”>> $HERMES_HOME/config.yaml

# 锻炼一下
Hermes -z“生成穿着宇航服的柯基犬图像”
````

或者以交互方式：“hermes 工具”→“图像生成”→ 选择“my-backend”→ 如果出现提示，请输入 API 密钥。

## 参考实现

- **`plugins/image_gen/openai/__init__.py`** — 低/中/高层的 gpt-image-2 作为三个虚拟模型 ID，共享一个具有不同“quality”参数的 API 模型。单个后端 + config.yaml 优先级链下分层模型的好例子。
- **`plugins/image_gen/xai/__init__.py`** — Grok Imagine 通过 xAI。不同的形状（URL 输出，更简单的目录）。
- **`plugins/image_gen/openai-codex/__init__.py`** — Codex 风格的响应 API 变体通过不同的路由基本 URL 重用 OpenAI SDK。

## 通过 pip 分发

````汤姆
# pyproject.toml
[project.entry-points."hermes_agent.plugins"]
my-backend-imggen =“my_backend_imggen_package”
````

`my_backend_imggen_package` 必须公开顶级 `register` 函数。有关完整设置，请参阅常规插件指南中的[通过 pip 分发](/guides/build-a-hermes-plugin#distribute-via-pip)。

## 相关页面

- [图像生成](/user-guide/features/image- Generation) — 面向用户的功能文档
- [插件概述](/user-guide/features/plugins) — 所有插件类型一目了然
- [构建 OpenClaw 插件](/guides/build-a-hermes-plugin) — 通用工具/hooks/slash 命令指南