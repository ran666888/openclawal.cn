---
title: "Huggingface Hub — HuggingFace hf CLI: search/download/upload models, datasets"
sidebar_label: "Huggingface Hub"
description: "HuggingFace hf CLI: search/download/upload models, datasets"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 拥抱脸中心

HuggingFace hf CLI：搜索/下载/上传模型、数据集。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/mlops/huggingface-hub` |
|版本 | `1.0.0` |
|作者 |拥抱脸|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Hugging Face CLI (`hf`) 参考指南

“hf”命令是用于与 Hugging Face Hub 交互的现代命令行界面，提供管理存储库、模型、数据集和空间的工具。

> **重要提示：** `hf` 命令取代了现已弃用的 `huggingface-cli` 命令。

## 快速入门
* **安装：** `curl -LsSf https://hf.co/cli/install.sh | bash-s`
* **帮助：** 使用 `hf --help` 查看所有可用的函数和实际示例。
* **身份验证：** 建议通过 `HF_TOKEN` 环境变量或 `--token` 标志。

---

## 核心命令

### 一般操作
* `hf download REPO_ID`：从集线器下载文件。
* `hf upload REPO_ID`：上传文件/文件夹（建议单次提交）。
* `hf upload-large-folder REPO_ID LOCAL_PATH`：推荐用于大型目录的可恢复上传。
* `hfsync`：在本地目录和存储桶之间同步文件。
* `hf env` / `hf version`：查看环境和版本详细信息。

### 身份验证（`hf auth`）
* `login` / `logout`：使用来自 [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) 的令牌管理会话。
* `list` / `switch`：在多个存储的访问令牌之间管理和切换。
* `whoami`：识别当前登录的帐户。

### 存储库管理（`hf repos`）
* `create` / `delete`：创建或永久删除存储库。
* `duplicate`：将模型、数据集或空间克隆到新 ID。
* `move`：在命名空间之间传输存储库。
* `branch` / `tag`：管理类似 Git 的引用。
* `delete-files`：使用模式删除特定文件。

---

## 专门的中心交互

### 数据集和模型
* **数据集：** `hf datasets list`、`info` 和 `parquet`（列出 parquet URL）。
* **SQL 查询：** `hf datasets sql SQL` — 通过 DuckDB 针对数据集 parquet URL 执行原始 SQL。
* **型号：** `hf 型号列表` 和 `信息`。
* **论文：** `hf 论文列表` — 查看日报。

### 讨论和拉取请求（`hf 讨论`）
* 管理 Hub 贡献的生命周期：`list`、`create`、`info`、`comment`、`close`、`reopen` 和 `rename`。
* `diff`：查看 PR 中的更改。
* `merge`：完成拉取请求。

### 基础设施和计算
* **端点：** 部署和管理推理端点（“部署”、“暂停”、“恢复”、“缩放至零”、“目录”）。
* **作业：** 在 HF 基础设施上运行计算任务。包括用于运行具有内联依赖项的 Python 脚本的“hf jobs uv”和用于资源监控的“stats”。
* **空间：** 管理交互式应用程序。包括用于 Python 文件的“dev-mode”和“hot-reload”，无需完全重新启动。

### 存储和自动化
* **存储桶：** 完全类似 S3 的存储桶管理（`create`、`cp`、`mv`、`rm`、`sync`）。
* **缓存：** 使用“list”、“prune”（删除分离的修订）和“verify”（校验和检查）管理本地存储。
* **Webhooks：** 通过管理 Hub Webhook（“创建”、“监视”、“启用”/“禁用”）来自动化工作流程。
* **集合：** 将 Hub 项目组织到集合中（`add-item`、`update`、`list`）。

---

## 高级用法和提示

### 全球旗帜
* `--format json`：生成机器可读的自动化输出。
* `-q` / `--quiet`：仅将输出限制为 ID。

### 扩展和技能
* **扩展：** 使用“hf 扩展安装 REPO_ID”通过 GitHub 存储库扩展 CLI 功能。
* **技能：** 使用“hf 技能添加”管理 AI 助手技能。