---
sidebar_position: 14
title: "AWS Bedrock"
description: "Use OpenClaw with Amazon Bedrock — native Converse API, IAM authentication, Guardrails, and cross-region inference"
---
# AWS 基岩

OpenClaw 使用 **Converse API** 支持 Amazon Bedrock 作为本机提供商，而不是 OpenAI 兼容终端节点。这使您可以完全访问 Bedrock 生态系统：IAM 身份验证、Guardrails、跨区域推理配置文件和所有基础模型。

## 先决条件

- **AWS 凭证** — [boto3 凭证链](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html) 支持的任何来源：
  - IAM 实例角色（EC2、ECS、Lambda — 零配置）
  - `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` 环境变量
  - 用于 SSO 或命名配置文件的“AWS_PROFILE”
  - 用于本地开发的“aws configure”
- **boto3** — 使用 `pip install hermes-agent[bedrock]` 安装
- **IAM 权限** — 至少：
  - `bedrock:InvokeModel` 和 `bedrock:InvokeModelWithResponseStream` （用于推理）
  - `bedrock:ListFoundationModels` 和 `bedrock:ListInferenceProfiles` （用于模型发现）

:::提示 EC2 / ECS / Lambda
在 AWS 计算上，使用“AmazonBedrockFullAccess”附加 IAM 角色即可完成。没有 API 密钥，没有 `.env` 配置 — OpenClaw 会自动检测实例角色。
:::

## 快速入门

````bash
# 使用基岩支持安装
pip install hermes-agent[基岩]

# 选择基岩作为您的提供商
爱马仕型号
# → 选择“更多提供商...”→“AWS Bedrock”
# → 选择您的地区和型号

# 开始聊天
爱马仕聊天
````

## 配置

运行“hermes model”后，您的“~/.hermes/config.yaml”将包含：

````yaml
型号：
  默认值：us.anthropic.claude-sonnet-4-6
  提供者：基岩
  基本网址：https://bedrock-runtime.us-east-2.amazonaws.com

基岩：
  区域：us-east-2
````

### 地区

通过以下任一方式设置 AWS 区域（优先级最高的优先）：

1.`config.yaml`中的`bedrock.region`
2.`AWS_REGION`环境变量
3.`AWS_DEFAULT_REGION`环境变量
4.默认值：`us-east-1`

### 护栏

要将 [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) 应用于所有模型调用：

````yaml
基岩：
  区域：us-east-2
  护栏：
    Guardrail_identifier: "abc123def456" # 从基岩控制台
    Guardrail_version: "1" # 版本号或“DRAFT”
    Stream_processing_mode: "async" # "同步" 或 "异步"
    trace: "disabled" # "enabled"、"disabled" 或 "enabled_full"
````

### 模型发现

OpenClaw 通过 Bedrock 控制平面自动发现可用模型。您可以自定义发现：

````yaml
基岩：
  发现：
    启用：真
    provider_filter: ["anthropic", "amazon"] # 只显示这些提供商
    fresh_interval: 3600 # 缓存1小时
````

## 可用型号

Bedrock 模型使用 **推理配置文件 ID** 进行按需调用。 “hermes 型号”选择器会自动显示这些型号，推荐型号位于顶部：

|型号|身份证 |笔记|
|--------|-----|--------|
|克劳德十四行诗 4.6 | `us.anthropic.claude-sonnet-4-6` |推荐 — 速度和功能的最佳平衡 |
|克劳德作品 4.6 | `us.anthropic.claude-opus-4-6-v1` |最有能力|
|克劳德俳句 4.5 | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |最快的克劳德|
|亚马逊 Nova Pro | `us.amazon.nova-pro-v1:0` |亚马逊旗舰店|
|亚马逊 Nova Micro | `us.amazon.nova-micro-v1:0` |最快、最便宜 |
| DeepSeek V3.2 | `deepseek.v3.2` |强势开放模式|
|骆驼 4 侦察兵 17B | `us.meta.llama4-scout-17b-instruct-v1:0` |元最新|

:::info 跨区域推理
以“us.”为前缀的模型使用跨区域推理配置文件，可提供更好的容量和跨 AWS 区域的自动故障转移。前缀为“global.”的模型可跨越全球所有可用区域。
:::

## 在会话中切换模型

在对话期间使用“/model”命令：

````
/型号 us.amazon.nova-pro-v1:0
/模型 deepseek.v3.2
/模型 us.anthropic.claude-opus-4-6-v1
````

## 诊断

````bash
爱马仕医生
````

医生检查：
- AWS 凭证是否可用（环境变量、IAM 角色、SSO）
- 是否安装了`boto3`
- Bedrock API 是否可达（ListFoundationModels）
- 您所在地区的可用型号数量

## 网关（消息传递平台）

Bedrock 适用于所有 OpenClaw 网关平台（Telegram、Discord、Slack、飞书等）。将 Bedrock 配置为您的提供商，然后正常启动网关：

````bash
Hermes网关设置
爱马仕网关启动
````

网关读取“config.yaml”并使用相同的 Bedrock 提供程序配置。

## 故障排除

###“找不到 API 密钥”/“没有 AWS 凭证”

OpenClaw 按以下顺序检查凭证：
1.`AWS_BEARER_TOKEN_BEDROCK`
2.`AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`
3.`AWS_PROFILE`
4. EC2实例元数据（IMDS）
5.ECS容器凭证
6.Lambda执行角色

如果未找到，请运行“aws configure”或将 IAM 角色附加到您的计算实例。

### “不支持按需吞吐量调用模型 ID ...”

使用 **推理配置文件 ID**（以“us.”或“global.”为前缀）而不是裸基础模型 ID。例如：
- ❌`anthropic.claude-sonnet-4-6`
- ✅ `us.anthropic.claude-sonnet-4-6`

###“节流异常”

您已达到基岩每个模型的速率限制。 OpenClaw 会自动进行退避重试。要增加限制，请在 [AWS Service Quotas 控制台](https://console.aws.amazon.com/servicequotas/) 中请求增加配额。

## 一键AWS部署

对于使用 CloudFormation 在 EC2 上进行全自动部署：

**[sample-openclaw-on-aws-with-bedrock](https://github.com/JiaDe-Wu/sample-openclaw-on-aws-with-bedrock)** — 创建 VPC、IAM 角色、EC2 实例，并自动配置 Bedrock。任意地域一键部署。