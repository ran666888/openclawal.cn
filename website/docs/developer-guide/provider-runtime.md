---
sidebar_position: 4
title: "Provider Runtime Resolution"
description: "How OpenClaw resolves providers, credentials, API modes, and auxiliary models at runtime"
---
# 提供程序运行时解析

OpenClaw 有一个共享的提供者运行时解析器，用于：

- 命令行界面
- 网关
- 计划任务
- ACP
- 辅助模型调用

主要实现：

- `hermes_cli/runtime_provider.py` — 凭证解析，`_resolve_custom_runtime()`
- `hermes_cli/auth.py` — 提供者注册表，`resolve_provider()`
- `hermes_cli/model_switch.py` — 共享 `/model` 切换管道（CLI + 网关）
- `agent/auxiliary_client.py` — 辅助模型路由
- `providers/` — ABC + 注册表入口点（`ProviderProfile`、`register_provider`、`get_provider_profile`、`list_providers`）
- `plugins/model-providers/<name>/` — 每个提供者插件（捆绑），声明 `api_mode`、`base_url`、`env_vars`、`fallback_models` 并在第一次访问时将自身注册到注册表中。 `$HERMES_HOME/plugins/model-providers/<name>/` 中的用户插件会覆盖同名的捆绑插件。

`providers/` 中的 `get_provider_profile()` 返回给定提供商 ID 的 `ProviderProfile`。 “runtime_provider.py”在解析时调用它来获取规范的“base_url”、“env_vars”优先级列表、“api_mode”和“fallback_models”，而无需在多个文件中复制该数据。在 `plugins/model-providers/<your-provider>/` （或 `$HERMES_HOME/plugins/model-providers/<your-provider>/`）下添加一个调用 `register_provider()` 的新插件就足以让 `runtime_provider.py` 拾取它 - 解析器本身不需要分支。

如果您尝试添加新的一流推理提供程序，请阅读本页旁边的[添加提供程序](./adding-providers.md) 和[模型提供程序插件指南](./model-provider-plugin.md)。

## 解析优先级

在较高层面上，提供商解析使用：

1. 显式 CLI/运行时请求
2. `config.yaml` 模型/提供者配置
3.环境变量
4. 提供商特定的默认值或自动解析

这种顺序很重要，因为 OpenClaw 将保存的模型/提供者选择视为正常运行的事实来源。这可以防止过时的 shell 导出默默地覆盖用户最后在“hermes model”中选择的端点。

## 提供商

当前的提供程序系列包括（有关完整的捆绑集，请参阅“插件/模型提供程序/”）：

- 开放路由器
- 诺斯门户
- OpenAI 法典
- 副驾驶 / 副驾驶 ACP
- 人择（本土）
- 谷歌/双子座（`gemini`）
- 阿里巴巴 / DashScope（`alibaba`、`alibaba-coding-plan`）
- 深寻
- Z.艾
- Kimi / Moonshot（`kimi-coding`、`kimi-coding-cn`）
- MiniMax (`minimax`, `minimax-cn`, `minimax-oauth`)
- 基洛代码
- 拥抱脸
- OpenCode Zen / OpenCode Go
- AWS 基岩
- 蔚蓝铸造厂
- NVIDIA NIM
- xAI (Grok)
- 阿尔茜
- GMI云
- 步趣
- Qwen OAuth
- 小米
- 奥拉玛云
- LM工作室
- 腾讯TokenHub
- Custom (`provider: custom`) — 任何 OpenAI 兼容端点的一流提供商
- 命名自定义提供程序（config.yaml 中的“custom_providers”列表）

## 运行时解析的输出

运行时解析器返回数据，例如：

- `提供者`
- `api_模式`
- `base_url`
- `api_key`
- `来源`
- 提供商特定的元数据，例如到期/刷新信息

## 为什么这很重要

这个解析器是 OpenClaw 可以在以下之间共享身份验证/运行时逻辑的主要原因：

- `爱马仕聊天`
- 网关消息处理
- 在新会话中运行的 cron 作业
- ACP 编辑会议
- 辅助模型任务

## OpenRouter 和自定义 OpenAI 兼容的基本 URL

OpenClaw 包含的逻辑可避免在存在多个提供程序密钥时将错误的 API 密钥泄漏到自定义端点（例如“OPENROUTER_API_KEY”和“OPENAI_API_KEY”）。

每个提供商的 API 密钥的范围仅限于其自己的基本 URL：

- “OPENROUTER_API_KEY”仅发送到“openrouter.ai”端点
- `OPENAI_API_KEY` 用于自定义端点并作为后备

OpenClaw 还区分：

- 用户选择的真实自定义端点
- 未配置自定义端点时使用的 OpenRouter 后备路径

这种区别对于以下方面尤其重要：

- 本地模型服务器
- 非 OpenRouter OpenAI 兼容的 API
- 切换提供商而无需重新运行安装程序
- 配置保存的自定义端点即使在当前 shell 中未导出“OPENAI_BASE_URL”时也应继续工作

## 原生人择路径

Anthropic 不再只是“通过 OpenRouter”。

当提供者解析选择“anthropic”时，OpenClaw 使用：

- `api_mode = anthropic_messages`
- 原生 Anthropic Messages API
- 用于翻译的“agent/anthropic_adapter.py”

当两者都存在时，本机 Anthropic 的凭证解析现在更喜欢可刷新的 Claude Code 凭证，而不是复制的 env 令牌。实际上这意味着：

- 当 Claude Code 凭证文件包含可刷新身份验证时，它们将被视为首选源
- 手动“ANTHROPIC_TOKEN”/“CLAUDE_CODE_OAUTH_TOKEN”值仍然可以作为显式覆盖使用
- OpenClaw 预检在本机消息 API 调用之前刷新人类凭证
- 重建 Anthropic 客户端后，OpenClaw 仍会在 401 上重试一次，作为后备路径

## OpenAI Codex 路径

Codex 使用单独的响应 API 路径：

- `api_mode = codex_responses`
- 专用凭证解析和授权存储支持

## 辅助模型路由

辅助任务例如：

- 愿景
- 网页提取摘要
- 上下文压缩摘要
- 技能中心运营
- MCP辅助操作
- 内存刷新

可以使用自己的提供者/模型路由而不是主要的会话模型。

当使用提供程序“main”配置辅助任务时，OpenClaw 通过与正常聊天相同的共享运行时路径来解决该问题。实际上这意味着：

- 环境驱动的自定义端点仍然有效
- 通过 `hermes model` / `config.yaml` 保存的自定义端点也可以工作
- 辅助路由可以区分真实保存的自定义端点和 OpenRouter 回退之间的区别

## 后备模型

OpenClaw 支持已配置的后备提供程序链——当主模型遇到错误时按顺序尝试的“(provider, model)”条目列表。传统的单对“fallback_model”字典仍然被接受用于向后兼容（并在第一次写入时迁移）。

### 内部如何运作

1. **存储**：`AIAgent.__init__`存储`fallback_model`字典并设置`_fallback_activated = False`。

2. **触发点**：`_try_activate_fallback()` 在 `run_agent.py` 的主重试循环中的三个地方被调用：
   - 对无效 API 响应进行最大重试后（无选择、缺少内容）
   - 不可重试的客户端错误（HTTP 401、403、404）
   - 发生暂时性错误（HTTP 429、500、502、503）的最大重试次数后

3. **激活流程**（`_try_activate_fallback`）：
   - 如果已激活或未配置，则立即返回“False”
   - 从 `auxiliary_client.py` 调用 `resolve_provider_client()` 以构建具有正确身份验证的新客户端
   - 确定“api_mode”：“codex_responses”用于 openai-codex，“anthropic_messages”用于 anthropic，“chat_completions”用于其他所有内容
   - 就地交换：`self.model`、`self.provider`、`self.base_url`、`self.api_mode`、`self.client`、`self._client_kwargs`
   - 对于人择回退：构建本机人择客户端而不是与 OpenAI 兼容的客户端
   - 重新评估提示缓存（为 OpenRouter 上的 Claude 模型启用）
   - 设置 `_fallback_activated = True` — 防止再次触发
   - 将重试计数重置为 0 并继续循环

4. **配置流程**：
   - CLI： `cli.py` 读取 `CLI_CONFIG["fallback_model"]` → 传递到 `AIAgent(fallback_model=...)`
   - 网关：`gateway/run.py._load_fallback_model()`读取`config.yaml`→传递到`AIAgent`
   - 验证：“provider”和“model”键都必须非空，否则后备被禁用

### 什么不支持后备

- **子代理委托** (`tools/delegate_tool.py`)：子代理继承父代理的提供程序，但不继承后备配置
- **辅助任务**：使用自己独立的提供者自动检测链（参见上面的辅助模型路由）

Cron 作业 **确实** 支持回退：“run_job()”从“config.yaml”读取“fallback_providers”（或旧版“fallback_model”）并将其传递给“AIAgent(fallback_model=...)”，匹配网关的“_load_fallback_model()”模式。请参阅[Cron 内部结构](./cron-internals.md)。

### 测试覆盖率

回退行为在多个套件中执行：

- `tests/run_agent/test_fallback_credential_isolation.py` — 主要和后备之间的凭证隔离
- `tests/hermes_cli/test_fallback_cmd.py` — `/fallback` CLI 命令
- `tests/gateway/test_fallback_eviction.py` — 网关驱逐失败的提供者

## 相关文档

- [代理循环内部结构](./agent-loop.md)
- [ACP 内部结构](./acp-internals.md)
- [上下文压缩和提示缓存](./context-compression-and-caching.md)