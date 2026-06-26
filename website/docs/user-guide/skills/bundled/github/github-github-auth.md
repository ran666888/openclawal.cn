---
title: "Github Auth — GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login"
sidebar_label: "Github Auth"
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# GitHub 授权

GitHub 身份验证设置：HTTPS 令牌、SSH 密钥、gh CLI 登录。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/github/github-auth` |
|版本 | `1.1.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `GitHub`、`身份验证`、`Git`、`gh-cli`、`SSH`、`设置` |
|相关技能| [`github-pr-workflow`](/docs/user-guide/skills/bundled/github/github-github-pr-workflow)、[`github-code-review`](/docs/user-guide/skills/bundled/github/github-github-code-review)、[`github-issues`](/docs/user-guide/skills/bundled/github/github-github-issues)、 [`github-repo-management`](/docs/user-guide/skills/bundled/github/github-github-repo-management) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# GitHub 身份验证设置

此技能设置身份验证，以便代理可以使用 GitHub 存储库、PR、问题和 CI。它涵盖两条路径：

- **`git`（始终可用）** — 使用 HTTPS 个人访问令牌或 SSH 密钥
- **`gh` CLI（如果已安装）** — 更丰富的 GitHub API 访问以及更简单的身份验证流程

## 检测流程

当用户要求您使用 GitHub 时，请首先运行此检查：

````bash
# 检查可用的内容
git --版本
gh --版本 2>/dev/null || echo "gh 未安装"

# 检查是否已经通过身份验证
gh 身份验证状态 2>/dev/null || echo "gh 未经过身份验证"
git config --global credential.helper 2>/dev/null || echo“没有 git 凭证助手”
````

**决策树：**
1. 如果 `gh auth status` 显示已通过身份验证 → 没问题，请使用 `gh` 进行所有操作
2. 如果安装了`gh`但未经过身份验证→使用下面的“gh auth”方法
3. 如果没有安装 `gh` → 使用下面的“git-only”方法（不需要 sudo）

---

## 方法 1：仅 Git 身份验证（无 gh、无 sudo）

这适用于任何安装了“git”的机器。无需 root 访问权限。

### 选项 A：带有个人访问令牌的 HTTPS（推荐）

这是最便携的方法——适用于任何地方，无需 SSH 配置。

**第 1 步：创建个人访问令牌**

告诉用户转到：**https://github.com/settings/tokens**

- 点击“生成新令牌（经典）”
- 给它起一个名字，比如“openclaw”
- 选择范围：
  - `repo`（完整的存储库访问 - 读取、写入、推送、PR）
  - `workflow`（触发和管理 GitHub Actions）
  - `read:org` （如果使用组织存储库）
- 设置有效期（90 天是一个很好的默认值）
- 复制令牌 - 它不会再次显示

**步骤2：配置git来存储令牌**

````bash
# 设置凭证助手来缓存凭证
# “store”以明文形式保存到 ~/.git-credentials （简单、持久）
git config --global credential.helper 存储

# 现在执行一个触发 auth 的测试操作 - git 将提示输入凭据
# 用户名：<他们的 github 用户名>
# 密码：<粘贴个人访问令牌，而不是他们的 GitHub 密码>
git ls-remote https://github.com/<their-username>/<any-repo>.git
````

输入一次凭据后，它们将被保存并重复用于将来的所有操作。

**替代方案：缓存助手（凭证从内存中过期）**

````bash
# 在内存中缓存8小时（28800秒）而不是保存到磁盘
git config --global credential.helper 'cache --timeout=28800'
````

**替代方案：直接在远程 URL 中设置令牌（每个存储库）**

````bash
# 在远程 URL 中嵌入令牌（完全避免凭据提示）
git Remote set-url origin https://<用户名>:<令牌>@github.com/<所有者>/<repo>.git
````

**步骤3：配置git身份**

````bash
# 提交所需 — 设置名称和电子邮件
git config --global user.name“他们的名字”
git config --global user.email“their-email@example.com”
````

**第 4 步：验证**

````bash
# 测试推送访问（现在应该可以在没有任何提示的情况下工作）
git ls-remote https://github.com/<their-username>/<any-repo>.git

# 验证身份
git config --全局用户名
git config --全局用户.email
````

### 选项 B：SSH 密钥身份验证

适合喜欢 SSH 或已设置密钥的用户。

**第 1 步：检查现有 SSH 密钥**

````bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo“未找到 SSH 密钥”
````

**第 2 步：根据需要生成密钥**

````bash
# 生成 ed25519 密钥（现代、安全、快速）
ssh-keygen -t ed25519 -C “他们的电子邮件@example.com” -f ~/.ssh/id_ed25519 -N “”

# 显示公钥供他们添加到 GitHub
猫 ~/.ssh/id_ed25519.pub
````

告诉用户添加公钥：**https://github.com/settings/keys**
- 单击“新 SSH 密钥”
- 粘贴公钥内容
- 给它一个标题，如“openclaw-<机器名称>”

**步骤 3：测试连接**

````bash
ssh -T git@github.com
# 预期：“嗨 <用户名>！您已成功通过身份验证...”
````

**步骤 4：配置 git 以对 GitHub 使用 SSH**

````bash
# 自动将 HTTPS GitHub URL 重写为 SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"
````

**第5步：配置git身份**

````bash
git config --global user.name“他们的名字”
git config --global user.email“their-email@example.com”
````

---

## 方法 2：gh CLI 身份验证

如果安装了“gh”，它会一步处理 API 访问和 git 凭证。

### 交互式浏览器登录（桌面）

````bash
gh 验证登录
# 选择：GitHub.com
# 选择：HTTPS
# 通过浏览器进行身份验证
````

### 基于令牌的登录（无头/SSH 服务器）

````bash
回声“<THEIR_TOKEN>”| gh 身份验证登录 --with-token

# 通过 gh 设置 git 凭证
gh auth 设置-git
````

### 验证

````bash
gh 身份验证状态
````

---

## 在没有 gh 的情况下使用 GitHub API

当“gh”不可用时，您仍然可以使用“curl”和个人访问令牌访问完整的 GitHub API。这就是其他 GitHub 技能实施其后备措施的方式。

### 设置 API 调用的令牌

````bash
# 选项 1：导出为 env var（首选 - 使其远离命令）
导出 GITHUB_TOKEN="<令牌>"

# 然后在curl调用中使用：
curl -s -H "授权：令牌 $GITHUB_TOKEN" \
  https://api.github.com/user
````

### 从 Git 凭证中提取令牌

如果已经配置了 git 凭证（通过 credential.helper store），则可以提取令牌：

````bash
# 从 git 凭证存储中读取
grep "github.com" ~/.git-credentials 2>/dev/null | grep "github.com" ~/.git-credentials 2>/dev/null |头-1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
````

### Helper：检测身份验证方法

在任何 GitHub 工作流程开始时使用此模式：

````bash
# 首先尝试 gh，然后再使用 git + curl
if 命令 -v gh &>/dev/null && gh auth status &>/dev/null;然后
  回显“AUTH_METHOD=gh”
elif [ -n "$GITHUB_TOKEN" ];然后
  回声“AUTH_METHOD =卷曲”
elif _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env";然后
  导出 GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\n\r')
  回声“AUTH_METHOD =卷曲”
elif grep -q "github.com" ~/.git-credentials 2>/dev/null;然后
  导出 GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  回声“AUTH_METHOD =卷曲”
否则
  回显“AUTH_METHOD=无”
  echo "需要先设置身份验证"
菲
````

---

## 故障排除

|问题 |解决方案 |
|---------|----------|
| `git push` 要求输入密码 | GitHub 禁用密码验证。使用个人访问令牌作为密码，或切换到 SSH |
| `远程：对 X 的权限被拒绝` |令牌可能缺少“repo”范围 - 使用正确的范围重新生成 |
| `致命：身份验证失败` |缓存的凭据可能已过时 - 运行“git credentialject”然后重新进行身份验证 |
| `ssh：连接到主机 github.com 端口 22：连接被拒绝` |尝试通过 HTTPS 端口进行 SSH：将 `Host github.com` 与 `Port 443` 和 `Hostname ssh.github.com` 添加到 `~/.ssh/config` |
|凭证不持久 |检查 `git config --global credential.helper` — 必须是 `store` 或 `cache` |
|多个 GitHub 帐户 |在 `~/.ssh/config` 或每个存储库凭证 URL 中使用具有不同密钥的 SSH |
| `gh：找不到命令` + 没有 sudo |使用上面的 git-only 方法 1 — 无需安装 |