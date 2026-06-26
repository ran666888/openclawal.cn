# 秘密

OpenClaw 可以在进程启动时从外部秘密管理器中提取 API 密钥，而不是将它们存储在“~/.hermes/.env”中。秘密管理器的引导令牌位于“.env”中；所有其他提供商密钥（OpenAI、Anthropic、OpenRouter 等）都可以保留在管理器中并集中轮换。

支持：

- [Bitwarden Secrets Manager](./bitwarden) — `bws` CLI，延迟安装，免费层工作。

更多后端（Vault、AWS Secrets Manager、1Password CLI）可以轻松添加到同一界面后面 - 提升是“agent/secret_sources/”中的一个模块和一个 CLI 处理程序。如果您有特定的需求，请提出请求。