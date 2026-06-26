---
sidebar_position: 3
title: "Managed Scope"
description: "Administrator-pinned, user-immutable config and secrets via a system-level managed directory"
---
# 管理范围

**托管范围**允许管理员推送配置基线并
标准（非 root）用户**无法覆盖**的秘密。它的目的是
IT 需要固定的舰队/组织部署，例如模型提供商、
共享 API 基 URL 或“security.redact_secrets: true”
机。

当存在托管范围时，它指定的值胜过用户的值
`~/.hermes/config.yaml`、`~/.hermes/.env`，甚至 shell 环境 — 用于
正是它所固定的按键。其他一切都完全由用户控制。

:::note 与包管理器锁定安装不同
包管理器管理的安装（声明式发行版/公式）阻止*所有*
配置突变并告诉您使用包管理器。管理范围是
单独的机制：它在每个键的基础上注入*特定的不可变值*
而不是锁定整个配置。两者既独立又可以共存。
:::

## 它居住的地方

托管范围是从系统级目录读取的，默认为“/etc/hermes”：

````文本
/etc/爱马仕/
├── config.yaml # 托管配置层（胜过~/.hermes/config.yaml）
└── .env # 托管环境层（胜过 ~/.hermes/.env + shell）
````

目录和文件由“root”拥有（目录模式“0755”，文件
`0644`)：所有人可读，仅管理员可写。 **那个
文件系统权限是强制机制**——标准用户可以读取
管理的文件，但无法编辑它们。

任一文件都是可选的。丢失的托管目录或丢失的文件
意味着“无托管范围”，并且配置的解析与没有托管范围时完全相同
该功能。

### 重新定位目录

可以使用“HERMES_MANAGED_DIR”环境变量重新定位该位置
（对于容器或非“/etc”部署）。这是部署/引导路径
旋钮 - 就像“HERMES_HOME” - 由拥有托管的同一管理员设置
文件。 OpenClaw **从未将其持久化**到任何“.env”。

````bash
# 将托管范围指向自定义目录（由 IT/部署设置，而不是用户设置）
导出 HERMES_MANAGED_DIR=/opt/org/hermes-policy
````

:::警告
可以设置“HERMES_MANAGED_DIR”的用户可以将托管范围重新指向目录
他们控制并击败它。在实际部署中，应该修复此变量
由管理员（例如，烘焙到服务单元/容器映像中），而不是
左用户可设置。 `hermes doctor` 报告*已解析的*托管目录，因此
重定向是可见的。
:::

## 优先级

对于管理层指定的键，顺序为（最高者获胜）：

|等级 |配置.yaml | .env |
|---|---|---|
| 1 | `/etc/hermes/config.yaml`（托管）| `/etc/hermes/.env`（托管）|
| 2 | `~/.hermes/config.yaml`（用户）| `~/.hermes/.env`（用户）|
| 3 |内置默认值 |预先存在的 shell 环境 |

合并是**叶级**：固定“model.default”不会冻结其余部分
`模型。*`。托管的“config.yaml”：

````yaml
型号：
  默认值：组织/标准模型
````

为每个用户强制使用“model.default”，同时保留“model.fallback”（以及每个用户）
其他键）在用户控制下。

:::note 优先级注释
对于它所固定的键，托管作用域故意胜过 shell 环境
也是如此——否则它就不会被“管理”。这是一个颠倒的地方
通常的“环境变量覆盖 config.yaml”规则，并且它仅适用
管理层指定的特定键。
:::

## 查看管理的内容

````bash
hermes config # 显示命名托管源 + 固定密钥的标头
Hermes doctor # 报告已解析的托管目录 + 固定键计数
````

如果您尝试更改托管值，OpenClaw 会拒绝并指出来源：

````bash
$ Hermes 配置集 model.default my/model
无法设置“model.default”：它由您的管理员管理
（/etc/hermes/config.yaml）并且无法更改。
````

这同样适用于托管机密 — `hermes config set` / setup 不会写入
由托管“.env”固定的 env 键的用户值。

## 设置托管范围（管理员）

````bash
sudo mkdir -p /etc/hermes

# 为这台机器上的每个用户固定一些配置值
sudo tee /etc/hermes/config.yaml >/dev/null <<'YAML'
型号：
  提供者： 诺斯
安全：
  redact_secrets：true
YAML

# 可选择固定共享的、不敏感的环境值
sudo tee /etc/hermes/.env >/dev/null <<'ENV'
OPENAI_API_BASE=https://inference.example.com/v1
环境电压

须藤 chmod 0755 /etc/hermes
须藤 chmod 0644 /etc/hermes/config.yaml /etc/hermes/.env
````

更改在下一次 OpenClaw 启动时生效（记录了格式错误的托管文件
大声并被忽略——它永远不会阻止启动，但管理员应该检查
“hermes doctor”以确认该政策正在应用）。

## 安全模型和限制 (v1)

- **仅执行文件系统权限。**如果用户具有写入权限
  托管目录（或以“root”身份运行 OpenClaw），托管范围是建议性的。
- **托管的`.env`是世界可读的**（`0644`），因此任何本地用户都可以读取
  秘密穿过它。将其用于共享的、非敏感的值（组织 API
  基本 URL、功能默认值）而不是高敏感度机密。
- **代理自己的工具不会硬阻止托管 *env* 值。** A
  托管环境变量在启动时应用，但没有什么可以阻止
  代理在其自己的子进程外壳内设置不同的值。 v1 是一个
  针对普通用户的管理便利边界，而不是不可避免的
  沙箱。

以下内容有意**超出 v1** 的范围，可能会稍后发布：

- 代理本身无法逃脱的硬边界。
- macOS 和 Windows 上的本机托管位置（v1 优先为 Linux/POSIX）。
- 用于分层策略的插入片段目录（`management.d/`）。
- 已签名/经过完整性检查的托管文件。
- 远程/设备管理 (MDM) 交付。
- 托管机密的更严格（组范围）权限。