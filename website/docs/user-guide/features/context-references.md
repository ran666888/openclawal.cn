---
sidebar_position: 9
sidebar_label: "Context References"
title: "Context References"
description: "Inline @-syntax for attaching files, folders, git diffs, and URLs directly into your messages"
---
# 上下文参考

输入“@”，然后输入引用，将内容直接注入到您的消息中。 OpenClaw 扩展了内联引用，并将内容附加到“--- Attached Context ---”部分下。

## 支持的参考文献

|语法 |描述 |
|--------|-------------|
| `@file:path/to/file.py` |注入文件内容 |
| `@file:path/to/file.py:10-25` |注入特定行范围（1-索引，包含）|
| `@folder:路径/到/目录` |插入带有文件元数据的目录树列表 |
| `@diff` |注入`git diff`（未暂存的工作树更改）|
| `@staged` |注入`git diff --staged`（分阶段更改）|
| `@git:5` |注入带有补丁的最后 N 次提交（最多 10 个）|
| `@url:https://example.com` |获取并注入网页内容 |

## 用法示例

````文本
查看 @file:src/main.py 并提出改进建议

发生了什么变化？ @差异

比较 @file:old_config.yaml 和 @file:new_config.yaml

@folder:src/components 中有什么？

总结一下这篇文章@url：https://arxiv.org/abs/2301.00001
````

多个引用在一条消息中起作用：

````文本
检查@file:main.py 和@file:test.py。
````

尾随标点符号（`,`、`.`、`;`、`!`、`?`）会自动从参考值中删除。

## CLI 选项卡完成

在交互式 CLI 中，输入“@”会触发自动完成：

- `@` 显示所有引用类型（`@diff`、`@staged`、`@file:`、`@folder:`、`@git:`、`@url:`）
- `@file:` 和 `@folder:` 使用文件大小元数据触发文件系统路径完成
- 裸露的“@”后跟部分文本显示当前目录中的匹配文件和文件夹

## 线路范围

`@file:` 参考支持精确内容注入的行范围：

````文本
@file:src/main.py:42 # 单行 42
@file:src/main.py:10-25 # 第 10 行到第 25 行（含）
````

行的索引为 1。无效范围将被静默忽略（返回完整文件）。

## 大小限制

上下文引用受到限制，以防止淹没模型的上下文窗口：

|门槛|价值|行为 |
|------------|--------|----------|
|软限位|上下文长度的 25% |附加警告，扩展继续进行 |
|硬限制|上下文长度的 50% |扩展被拒绝，原始消息不变返回 |
|文件夹条目 |最多 200 个文件 |多余的条目替换为 `- ...` |
| Git 提交 |最多 10 个 | `@git:N` 限制在范围 [1, 10] |

## 安全

### 敏感路径阻塞

这些路径始终被阻止引用“@file:”，以防止凭据泄露：

- SSH 密钥和配置：`~/.ssh/id_rsa`、`~/.ssh/id_ed25519`、`~/.ssh/authorized_keys`、`~/.ssh/config`
- Shell 配置文件：`~/.bashrc`、`~/.zshrc`、`~/.profile`、`~/.bash_profile`、`~/.zprofile`
- 凭证文件：`~/.netrc`、`~/.pgpass`、`~/.npmrc`、`~/.pypirc`
- OpenClaw 环境：`$HERMES_HOME/.env`

这些目录被完全阻止（其中的任何文件）：
- `~/.ssh/`、`~/.aws/`、`~/.gnupg/`、`~/.kube/`、`$HERMES_HOME/skills/.hub/`

### 路径遍历保护

所有路径都是相对于工作目录解析的。在允许的工作空间根目录之外解析的引用将被拒绝。

### 二进制文件检测

通过 MIME 类型和空字节扫描检测二进制文件。已知的文本扩展名（`.py`、`.md`、`.json`、`.yaml`、`.toml`、`.js`、`.ts` 等）会绕过基于 MIME 的检测。二进制文件被拒绝并带有警告。

## 平台可用性

上下文引用主要是 **CLI 功能**。它们在交互式 CLI 中工作，其中“@”触发选项卡完成，并在消息发送到代理之前展开引用。

在**消息平台**（Telegram、Discord 等）中，网关不会扩展“@”语法 - 消息按原样传递。代理本身仍然可以通过“read_file”、“search_files”和“web_extract”工具引用文件。

## 与上下文压缩的交互

当对话上下文被压缩时，扩展的参考内容被包含在压缩摘要中。这意味着：

- 通过“@file:”注入的大文件内容有助于上下文使用
- 如果对话稍后被压缩，则会总结文件内容（不逐字保留）
- 对于非常大的文件，请考虑使用行范围（`@file:main.py:100-200`）仅注入相关部分

## 常见模式

````文本
# 代码审查工作流程
查看 @diff 并检查安全问题

# 使用上下文进行调试
这次测试失败了。这是测试@file:tests/test_auth.py
和实现 @file:src/auth.py:50-80

# 项目探索
这个项目是做什么的？ @文件夹：src @文件：README.md

# 研究
比较@url中的方法：https://arxiv.org/abs/2301.00001
和@url：https://arxiv.org/abs/2301.00002
````

## 错误处理

无效引用会产生内联警告而不是失败：

|状况 |行为 |
|------------|----------|
|找不到文件 |警告：“找不到文件”|
|二进制文件 |警告：“不支持二进制文件”|
|找不到文件夹 |警告：“找不到文件夹”|
| Git 命令失败 | git stderr 警告 |
| URL 没有返回内容 |警告：“未提取任何内容”|
|敏感路径 |警告：“路径是敏感凭证文件”|
|工作空间外的路径 |警告：“路径超出允许的工作空间”|