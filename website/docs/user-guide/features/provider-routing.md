---
title: Provider Routing
description: Configure OpenRouter provider preferences to optimize for cost, speed, or quality.
sidebar_label: Provider Routing
sidebar_position: 7
---
# 提供商路由

当使用 [OpenRouter](https://openrouter.ai) 作为您的 LLM 提供商时，OpenClaw 支持**提供商路由** — 精细控制哪些底层 AI 提供商处理您的请求以及它们的优先级。

OpenRouter 将请求路由到许多提供商（例如 Anthropic、Google、AWS Bedrock、Together AI）。提供商路由可让您优化成本、速度、质量或强制执行特定的提供商要求。

:::提示
通过 [Nous Portal](/integrations/nous-portal) 路由的流量仍然遵循每个模型的路由和优先级配置 - 并且门户订阅者可以享受代币计费提供商 10% 的折扣。
:::

## 配置

将“provider_routing”部分添加到“~/.hermes/config.yaml”：

````yaml
提供者路由：
  sort: "price" # 如何对提供商进行排名
  only: [] # 白名单：仅使用这些提供商
  ignore: [] # 黑名单：永远不要使用这些提供商
  order: [] # 显式提供者优先级顺序
  require_parameters: false # 仅使用支持所有参数的提供程序
  data_collection: null # 控制数据收集（“允许”或“拒绝”）
````

:::信息
提供商路由仅在使用 OpenRouter 时适用。它对直接提供者连接（例如，直接连接到 Anthropic API）没有影响。
:::

## 选项

### `排序`

控制 OpenRouter 如何对您的请求的可用提供商进行排名。

|价值|描述 |
|--------|-------------|
| `“价格”` |最便宜的提供商优先 |
| `“吞吐量”` |每秒最快的令牌第一 |
| `“延迟”` |首次令牌时间最短优先 |

````yaml
提供者路由：
  排序：“价格”
````

### `仅`

提供商名称白名单。设置后，**仅**将使用这些提供程序。所有其他人均被排除在外。

````yaml
提供者路由：
  仅：
    ——《人择》
    - “谷歌”
````

### `忽略`

提供商名称黑名单。这些提供商**永远**不会被使用，即使它们提供最便宜或最快的选择。

````yaml
提供者路由：
  忽略：
    - 《在一起》
    - “深基础设施”
````

### `订单`

明确的优先顺序。首先列出的提供商是首选。未列出的提供商用作后备。

````yaml
提供者路由：
  订单：
    ——《人择》
    - “谷歌”
    - “AWS 基岩”
````

### `require_parameters`

当为“true”时，OpenRouter 将仅路由到支持请求中的“所有”参数的提供程序（例如“温度”、“top_p”、“工具”等）。这避免了静默参数下降。

````yaml
提供者路由：
  要求参数：true
````

### `数据收集`

控制提供者是否可以使用您的提示进行培训。选项有“允许”或“拒绝”。

````yaml
提供者路由：
  data_collection：“拒绝”
````

## 实际例子

### 成本优化

路由到最便宜的可用提供商。适合大批量使用和开发：

````yaml
提供者路由：
  排序：“价格”
````

### 优化速度

优先考虑低延迟提供程序以进行交互使用：

````yaml
提供者路由：
  排序：“延迟”
````

### 优化吞吐量

最适合每秒令牌数很重要的长格式生成：

````yaml
提供者路由：
  排序：“吞吐量”
````

### 锁定特定提供商

确保所有请求都通过特定的提供商以保持一致性：

````yaml
提供者路由：
  仅：
    ——《人择》
````

### 避免特定的提供商

排除您不想使用的提供商（例如，为了数据隐私）：

````yaml
提供者路由：
  忽略：
    - 《在一起》
    - “轻子”
  data_collection：“拒绝”
````

### 带有后备的首选顺序

首先尝试您首选的提供商，如果不可用，则转而使用其他提供商：

````yaml
提供者路由：
  订单：
    ——《人择》
    - “谷歌”
  要求参数：true
````

## 它是如何工作的

提供商路由首选项通过每个 API 调用上的“extra_body.provider”字段传递到 OpenRouter API。这适用于两者：

- **CLI 模式** — 在 `~/.hermes/config.yaml` 中配置，在启动时加载
- **网关模式** — 相同的配置文件，在网关启动时加载

路由配置从“config.yaml”读取并在创建“AIAgent”时作为参数传递：

````
providers_allowed ← 来自provider_routing.only
providers_ignored ← 来自provider_routing.ignore
providers_order ← 来自provider_routing.order
provider_sort ← 来自provider_routing.sort
provider_require_parameters ← 来自provider_routing.require_parameters
provider_data_collection ← 来自provider_routing.data_collection
````

:::提示
您可以组合多个选项。例如，按价格排序但排除某些提供商并需要参数支持：

````yaml
提供者路由：
  排序：“价格”
  忽略：[“在一起”]
  要求参数：true
  data_collection：“拒绝”
````
:::

## 默认行为

当没有配置“provider_routing”部分（默认）时，OpenRouter 使用自己的默认路由逻辑，通常会自动平衡成本和可用性。

:::tip 提供商路由与后备模型
提供商路由控制 OpenRouter 中的哪些**子提供商**处理您的请求。要在主模型失败时自动故障转移到完全不同的提供程序，请参阅[后备提供程序](/user-guide/features/fallback-providers)。
:::