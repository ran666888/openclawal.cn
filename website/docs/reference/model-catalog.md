---
sidebar_position: 11
title: Model Catalog
description: Remotely-hosted manifest driving curated model picker lists for OpenRouter and Nous Portal.
---
# 型号目录

OpenClaw 从与文档站点一起托管的 JSON 清单中获取 **OpenRouter** 和 **Nous Portal** 的精选模型列表。这使得维护人员可以更新选择器列表，而无需发布新的“openclaw”版本。

当清单无法访问时（离线、网络阻塞、托管故障），OpenClaw 会默默地回退到 CLI 附带的仓库内快照。清单永远不会破坏选择器 - 最坏的情况是您看到与您安装的版本捆绑在一起的任何列表。

## 实时清单 URL

````
https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
````

通过现有的“deploy-site.yml”GitHub Pages 管道在每次合并到“main”时发布。事实来源位于“website/static/api/model-catalog.json”的存储库中。

## 架构

```json
{
  “版本”：1，
  “updated_at”：“2026-04-25T22：00：00Z”，
  “元数据”：{}，
  “提供商”：{
    “开放路由器”：{
      “元数据”：{}，
      “模型”：[
        {“id”：“moonshotai/kimi-k2.6”，“描述”：“推荐”，“元数据”：{}}，
        {“id”：“openai/gpt-5.4”，“描述”：“”}
      ]
    },
    “努斯”：{
      “元数据”：{}，
      “模型”：[
        {“id”：“anthropic/claude-opus-4.7”}，
        {“id”：“moonshotai/kimi-k2.6”}
      ]
    }
  }
}
````

现场笔记：

- **`version`** — 整数模式版本。未来的模式会改变这一点； OpenClaw 拒绝使用它不理解的版本的清单，并回退到硬编码快照。
- **`元数据`** — 清单、提供者和模型级别的自由格式字典。任何键。 OpenClaw 会忽略未知字段，因此您可以注释条目（`"tier": "paid"`、`"tags": [...]` 等），而无需协调架构更改。
- **`描述`** — 仅限 OpenRouter。驱动器选择器徽章文本（“推荐”、“免费”或空）。 Nous Portal 不使用此功能 — 免费套餐门控是由门户的定价端点实时确定的。
- **定价和上下文长度**不在清单中。这些来自实时提供者 API（`/v1/models` 端点，models.dev）在获取时。

## 获取行为

|当 |会发生什么 |
|---|---|
| `/model` 或 `hermes model` |如果磁盘缓存已过时则获取，否则使用缓存 |
|磁盘缓存新鲜 (< TTL) |没有网络点击|
|网络故障与缓存 |静默回退到缓存，一行日志 |
|网络故障，无缓存 |静默回退到仓库内快照 |
|清单架构验证失败 |被视为无法访问 |

缓存位置：`~/.hermes/cache/model_catalog.json`。

## 配置

````yaml
型号目录：
  启用：真
  网址：https://hermes-agent.nousresearch.com/docs/api/model-catalog.json
  ttl_小时：1
  提供商：{}
````

设置“enabled: false”以完全禁用远程获取并始终使用存储库内快照。

### 每个提供商的覆盖 URL

第三方可以使用相同的架构自行托管自己的管理列表。将提供商指向自定义 URL：

````yaml
型号目录：
  提供者：
    打开路由器：
      网址：https://example.com/my-openrouter-curation.json
````

覆盖清单只需要填充它关心的提供者块。其他提供商继续根据主 URL 进行解析。

## 更新清单

维护者：

````bash
# 从存储库内硬编码列表重新生成（在之后保持清单同步）
# 在 hermes_cli/models.py 中编辑 OPENROUTER_MODELS 或 _PROVIDER_MODELS["nous"])。
python 脚本/build_model_catalog.py
````

然后将“website/static/api/model-catalog.json”更改为“main”。文档站点会在合并时自动部署，新的清单会在几分钟内生效。

您还可以直接手动编辑 JSON，以进行不属于存储库内快照的细粒度元数据更改 - 生成器脚本只是一种便利，而不是单一事实来源。