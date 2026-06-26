# ClawHub — 技能与插件市场

ClawHub 是 OpenClaw 的官方技能（Skills）和插件（Plugins）注册表市场。你可以在 ClawHub 上浏览、搜索和安装社区贡献的各类技能和插件，扩展 OpenClaw 的能力。

## 什么是 ClawHub？

ClawHub 类似于应用商店，但专为 OpenClaw Agent 设计。它包含：

- **技能（Skills）** — Markdown 指令文件，告诉 Agent 如何执行特定任务
- **插件（Plugins）** — 扩展 OpenClaw 核心功能的代码包
- **配置示例** — 社区分享的最佳实践配置

## 访问 ClawHub

ClawHub 的访问地址：

```
https://clawhub.openclaw.ai
```

你也可以在 OpenClaw 命令行中直接搜索和安装：

```bash
# 搜索技能
openclaw clawhub search <关键词>

# 安装技能
openclaw clawhub install <技能名称>

# 查看已安装的技能
openclaw clawhub list
```

## 贡献技能

任何人都可以向 ClawHub 贡献技能。技能是一个 Markdown 文件（SKILL.md），包含：

1. **YAML 头部** — 技能名称、描述、触发条件
2. **正文** — 操作步骤、使用说明、注意事项
3. **示例** — 使用场景和命令示例

详细的技能创作指南请参考 [OpenClaw 技能创作文档](https://docs.openclaw.ai/guides/creating-skills)。

## 推荐技能

以下是一些热门的 ClawHub 技能：

| 技能 | 分类 | 说明 |
|------|------|------|
| 代码审查 | 开发 | 自动审查 Pull Request |
| 日报生成 | 运营 | 自动汇总生成每日报告 |
| 竞品分析 | 运营 | 分析竞品功能和市场策略 |
| Docker 管理 | 运维 | 管理 Docker 容器和镜像 |
| GitHub 工作流 | 开发 | 管理 Issue、PR 和仓库 |

## 相关资源

- [ClawHub 官网](https://clawhub.openclaw.ai)
- [技能创作指南](https://docs.openclaw.ai/guides/creating-skills)
- [OpenClaw 技能系统](/user-guide/features/skills)
