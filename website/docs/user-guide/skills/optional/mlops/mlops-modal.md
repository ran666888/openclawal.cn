---
title: "Modal Serverless Gpu — Serverless GPU cloud platform for running ML workloads"
sidebar_label: "Modal Serverless Gpu"
description: "Serverless GPU cloud platform for running ML workloads"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 模态无服务器 Gpu

用于运行 ML 工作负载的无服务器 GPU 云平台。当您需要按需 GPU 访问而无需基础设施管理、将 ML 模型部署为 API 或通过自动扩展运行批处理作业时使用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/mlops/modal` 安装 |
|路径| `可选技能/mlops/模式` |
|版本 | `1.0.0` |
|作者 |乐团研究|
|许可证|麻省理工学院 |
|依赖关系 | `模态>=0.64.0` |
|平台| linux、macos、windows |
|标签 | `基础设施`、`无服务器`、`GPU`、`云`、`部署`、`模态` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 模态无服务器 GPU

在 Modal 的无服务器 GPU 云平台上运行 ML 工作负载的综合指南。

## 何时使用模态

**在以下情况下使用模态：**
- 无需管理基础设施即可运行 GPU 密集型 ML 工作负载
- 将 ML 模型部署为自动缩放 API
- 运行批处理作业（训练、推理、数据处理）
- 需要按秒付费的 GPU 定价，无需闲置成本
- 快速构建 ML 应用程序原型
- 运行计划作业（类似 cron 的工作负载）

**主要特点：**
- **无服务器 GPU**：T4、L4、A10G、L40S、A100、H100、H200、B200 按需
- **Python-native**：用 Python 代码定义基础设施，无 YAML
- **自动缩放**：缩放至零，立即缩放至 100+ GPU
- **亚秒级冷启动**：基于 Rust 的基础设施，用于快速容器启动
- **容器缓存**：缓存图像层以实现快速迭代
- **Web端点**：将功能部署为具有零停机更新的REST API

**使用替代方案：**
- **RunPod**：适用于具有持久状态的长时间运行的 Pod
- **Lambda Labs**：用于保留的 GPU 实例
- **SkyPilot**：用于多云编排和成本优化
- **Kubernetes**：适用于复杂的多服务架构

## 快速开始

### 安装

````bash
pip 安装模式
modal setup # 打开浏览器进行身份验证
````

### 使用 GPU 的 Hello World

````蟒蛇
进口模态

app = modal.App("hello-gpu")

@app.function（gpu =“T4”）
def gpu_info():
    导入子流程
    返回 subprocess.run(["nvidia-smi"], capture_output=True, text=True).stdout

@app.local_entrypoint()
def main():
    打印（gpu_info.remote（））
````

运行：`模态运行 hello_gpu.py`

### 基本推理端点

````蟒蛇
进口模态

app = modal.App("文本生成")
image = modal.Image.debian_slim().pip_install("变形金刚", "火炬", "加速")

@app.cls（gpu =“A10G”，图像=图像）
文本生成器类：
    @modal.enter()
    def load_model(自身):
        从变压器进口管道
        self.pipe = pipeline("文本生成", model="gpt2", device=0)

    @modal.method()
    def生成（自我，提示：str）-> str：
        返回 self.pipe(提示, max_length=100)[0][" generated_text"]

@app.local_entrypoint()
def main():
    print(TextGenerator().generate.remote("你好，世界"))
````

## 核心概念

### 关键组件

|组件|目的|
|------------|---------|
| `应用程序` |功能和资源的容器|
| `功能` |具有计算规格的无服务器功能 |
| `Cls` |具有生命周期挂钩的基于类的函数 |
| `图像` |容器镜像定义|
| `音量` |模型/数据的持久存储 |
| `秘密` |安全凭证存储 |

### 执行模式

|命令|描述 |
|---------|-------------|
| `模态运行脚本.py` |执行并退出 |
| `模态服务脚本.py` |实时重载开发 |
| `模态部署脚本.py` |持久云部署|

## GPU 配置

### 可用的 GPU

|图形处理器 |显存 |最适合 |
|-----|------|----------|
| 'T4' | 16GB |预算推断，小模型|
| 'L4' | 24GB |推论，阿达·洛夫莱斯拱门 |
| 'A10G' | 24GB |训练/推理，比 T4 快 3.3 倍 |
| 'L40S' | 48GB |推荐用于推理（最佳成本/性能）|
| `A100-40GB` | 40GB |大模型训练 |
| `A100-80GB` | 80GB |非常大的模型|
| 'H100' | 80GB |最快的 FP8 + Transformer 引擎 |
| 'H200' | 141GB | H100自动升级，4.8TB/s带宽 |
| 'B200' |最新 |布莱克威尔建筑|

### GPU 规格模式

````蟒蛇
# 单 GPU
@app.function（GPU =“A100”）

# 特定的内存变体
@app.function(gpu="A100-80GB")

# 多个 GPU（最多 8 个）
@app.function(gpu="H100:4")

# 具有后备功能的 GPU
@app.function(gpu=["H100", "A100", "L40S"])

# 任何可用的 GPU
@app.function（gpu =“任何”）
````

## 容器镜像

````蟒蛇
# 带 pip 的基本图像
图像 = modal.Image.debian_slim(python_version="3.11").pip_install(
    “火炬==2.1.0”，“变形金刚==4.36.0”，“加速”
）

# 来自 CUDA 基础
图像 = modal.Image.from_registry(
    “nvidia/cuda:12.1.0-cudnn8-devel-ubuntu22.04”,
    add_python =“3.11”
).pip_install("火炬", "变形金刚")

# 带有系统包
image = modal.Image.debian_slim().apt_install("git", "ffmpeg").pip_install("whisper")
````

## 持久化存储

````蟒蛇
体积 = modal.Volume.from_name("模型缓存", create_if_missing=True)

@app.function（gpu =“A10G”，卷= {“/ models”：卷}）
def load_model():
    导入操作系统
    model_path =“/models/llama-7b”
    如果不是 os.path.exists(model_path):
        模型 = download_model()
        model.save_pretrained(model_path)
        Volume.commit() # 保存更改
    返回 load_from_path(模型路径)
````

## Web 端点

### FastAPI端点装饰器

````蟒蛇
@app.function()
@modal.fastapi_endpoint(方法=“POST”)
def 预测(文本: str) -> 字典:
    返回 {"结果": model.predict(text)}
````

### 完整的 ASGI 应用程序

````蟒蛇
从 fastapi 导入 FastAPI
web_app = FastAPI()

@web_app.post("/预测")
异步 def 预测（文本：str）：
    返回 {“结果”：等待 model.predict.remote.aio(text)}

@app.function()
@modal.asgi_app()
def fastapi_app():
    返回 web_app
````

### Web 端点类型

|装饰 |使用案例|
|------------|----------|
| `@modal.fastapi_endpoint()` |简单功能 → API |
| `@modal.asgi_app()` |完整的 FastAPI/Starlette 应用程序 |
| `@modal.wsgi_app()` | Django/Flask 应用程序 |
| `@modal.web_server(端口)` |任意 HTTP 服务器 |

## 动态批处理

````蟒蛇
@app.function()
@modal.batched(max_batch_size=32, wait_ms=100)
async def batch_predict(输入: list[str]) -> list[dict]:
    # 输入自动批处理
    返回 model.batch_predict(输入)
````

## 秘密管理

````bash
# 创建秘密
模态秘密创建 Huggingface HF_TOKEN=hf_xxx
````

````蟒蛇
@app.function(secrets=[modal.Secret.from_name("huggingface")])
def download_model():
    导入操作系统
    令牌 = os.environ["HF_TOKEN"]
````

## 调度

````蟒蛇
@app.function(schedule=modal.Cron("0 0 * * *")) # 每日午夜
def daily_job():
    通过

@app.function(schedule=modal.Period(小时=1))
def hourly_job():
    通过
````

## 性能优化

### 冷启动缓解

````蟒蛇
@app.function(
    container_idle_timeout=300, # 保温5分钟
    allow_concurrent_inputs=10, # 处理并发请求
）
def 推理（）：
    通过
````

### 模型加载最佳实践

````蟒蛇
@app.cls(gpu="A100")
类型号：
    @modal.enter() # 在容器启动时运行一次
    默认负载（自身）：
        self.model = load_model() # 预热期间加载

    @modal.method()
    def 预测（自身，x）：
        返回 self.model(x)
````

## 并行处理

````蟒蛇
@app.function()
def process_item(项目):
    返回昂贵的计算（项目）

@app.function()
def run_parallel():
    项目=列表（范围（1000））
    # 扇出到并行容器
    结果=列表(process_item.map(items))
    返回结果
````

## 常用配置

````蟒蛇
@app.function(
    显卡=“A100”，
    内存=32768, # 32GB RAM
    cpu=4, # 4个CPU核心
    timeout=3600, # 最长 1 小时
    container_idle_timeout=120,#保温2分钟
    retries=3, # 失败重试
    concurrency_limit=10, # 最大并发容器数
）
def my_function():
    通过
````

## 调试

````蟒蛇
# 本地测试
如果 __name__ == "__main__":
    结果 = my_function.local()

# 查看日志
# 模态应用程序记录我的应用程序
````

## 常见问题

|问题 |解决方案 |
|--------|----------|
|冷启动延迟|增加 `container_idle_timeout`，使用 `@modal.enter()` |
| GPU OOM |使用更大的 GPU (`A100-80GB`)，启用梯度检查点 |
|镜像构建失败 |引脚依赖版本，检查 CUDA 兼容性 |
|超时错误 |增加“超时”，添加检查点|

## 参考文献

- **[高级用法](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/modal/references/advanced-usage.md)** - 多 GPU、分布式训练、成本优化
- **[疑难解答](https://github.com/NousResearch/openclaw/blob/main/optional-skills/mlops/modal/references/troubleshooting.md)** - 常见问题和解决方案

## 资源

- **文档**：https://modal.com/docs
- **示例**：https://github.com/modal-labs/modal-examples
- **定价**：https://modal.com/pricing
- **不和谐**：https://discord.gg/modal