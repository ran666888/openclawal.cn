---
title: "Github Pr Workflow — GitHub PR lifecycle: branch, commit, open, CI, merge"
sidebar_label: "Github Pr Workflow"
description: "GitHub PR lifecycle: branch, commit, open, CI, merge"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Github 公关工作流程

GitHub PR 生命周期：分支、提交、打开、CI、合并。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/github/github-pr-workflow` |
|版本 | `1.1.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `GitHub`、`Pull-Requests`、`CI/CD`、`Git`、`自动化`、`合并` |
|相关技能| [`github-auth`](/docs/user-guide/skills/bundled/github/github-github-auth), [`github-code-review`](/docs/user-guide/skills/bundled/github/github-github-code-review) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# GitHub 拉取请求工作流程

管理公关生命周期的完整指南。每个部分首先显示“gh”方式，然后是没有“gh”的机器的“git”+“curl”后备方式。

## 先决条件

- 通过 GitHub 进行身份验证（请参阅“github-auth”技能）
- 在带有 GitHub 远程的 git 存储库内

### 快速身份验证检测

````bash
# 确定在整个工作流程中使用哪种方法
if 命令 -v gh &>/dev/null && gh auth status &>/dev/null;然后
  授权=“呃”
否则
  授权=“git”
  # 确保我们有 API 调用的令牌
  如果[-z“$GITHUB_TOKEN”];然后
    if _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env";然后
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null;然后
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    菲
  菲
菲
回显“使用：$AUTH”
````

### 从 Git 远程提取所有者/存储库

许多“curl”命令需要“owner/repo”。从 git 远程提取它：

````bash
# 适用于 HTTPS 和 SSH 远程 URL
REMOTE_URL=$(git 远程 get-url 来源)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
echo“所有者：$OWNER，回购：$REPO”
````

---

## 1. 分支创建

这部分是纯粹的“git”——无论如何都是相同的：

````bash
# 确保您是最新的
git 获取原点
git checkout main && git pull origin main

# 创建并切换到新分支
git checkout -b feat/add-user-authentication git checkout -b feat/add-user-authentication
````

分支命名约定：
- `壮举/描述` — 新功能
- `修复/描述` — 错误修复
- `refactor/description` — 代码重组
- `docs/description` — 文档
- `ci/description` — CI/CD 更改

## 2. 做出承诺

使用代理的文件工具（`write_file`、`patch`）进行更改，然后提交：

````bash
# 阶段特定文件
git add src/auth.py src/models/user.py 测试/test_auth.py

# 使用常规提交消息进行提交
git commit -m "feat: 添加基于 JWT 的用户身份验证

- 添加登录/注册端点
- 添加带有密码哈希的用户模型
- 为受保护的路由添加身份验证中间件
- 添加身份验证流程的单元测试”
````

提交消息格式（常规提交）：
````
类型（范围）：简短描述

如果需要的话，可以提供更长的解释。 72 个字符换行。
````

类型：`feat`、`fix`、`refactor`、`docs`、`test`、`ci`、`chore`、`perf`

## 3. 推送并创建 PR

### 推送分支（两种方式都相同）

````bash
git Push -u 原点 HEAD
````

### 创建 PR

**与 gh:**

````bash
gh 公关创建\
  --title "feat: 添加基于 JWT 的用户身份验证" \
  --body "## 总结
- 添加登录和注册 API 端点
- JWT 令牌生成和验证

## 测试计划
- [ ] 单元测试通过

关闭 #42"
````

选项：`--draft`、`--reviewer user1,user2`、`--label "enhancement"`、`--basedevelopment`

**使用 git + curl：**

````bash
分支 = $(git 分支 --show-current)

卷曲-s -X POST \
  -H“授权：令牌$GITHUB_TOKEN”\
  -H“接受：application/vnd.github.v3+json”\
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d“{
    \"title\": \"功能：添加基于 JWT 的用户身份验证\",
    \"body\": \"## 摘要\n添加登录和注册 API 端点。\n\n关闭 #42\",
    \"head\": \"$BRANCH\",
    \“基础\”：“主要\”
  }”
````

响应 JSON 包含 PR“编号”——将其保存以供后续命令使用。

要创建草稿，请将 `"draft": true` 添加到 JSON 正文。

## 4. 监控 CI 状态

### 检查 CI 状态

**与 gh:**

````bash
# 一次性检查
gh 公关检查

# 观察直到所有检查完成（每 10 秒轮询一次）
gh 公关检查 --watch
````

**使用 git + curl：**

````bash
# 获取当前分支上最新的提交SHA
SHA=$(git rev-parse HEAD)

# 查询组合状态
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
  | python3-c“
导入系统，json
数据 = json.load(sys.stdin)
print(f\"总体：{data['state']}\")
for s in data.get('statuses', []):
    print(f\" {s['context']}: {s['state']} - {s.get('description', '')}\")"

# 同时检查 GitHub Actions 检查运行（单独的端点）
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/check-runs \
  | python3-c“
导入系统，json
数据 = json.load(sys.stdin)
对于 data.get('check_runs', []) 中的 cr：
    print(f\" {cr['名称']}: {cr['状态']} / {cr['结论'] 或 '待定'}\")"
````

### 轮询直至完成（git + curl）

````bash
# 简单的轮询循环 — 每 30 秒检查一次，最多 10 分钟
SHA=$(git rev-parse HEAD)
对于 $(seq 1 20) 中的 i；做
  状态=$(curl -s \
    -H“授权：令牌$GITHUB_TOKEN”\
    https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status \
    | python3 -c "导入 sys,json; print(json.load(sys.stdin)['state'])")
  echo“检查$i：$STATUS”
  if [ "$STATUS" = "成功" ] || [“$STATUS”=“失败”]|| [“$STATUS”=“错误”];然后
    打破
  菲
  睡30
完成
````

## 5. 自动修复 CI 故障

当 CI 失败时，诊断并修复。此循环适用于任一身份验证方法。

### 第 1 步：获取失败详细信息

**与 gh:**

````bash
# 列出该分支上最近运行的工作流程
gh run list --branch $(gitbranch --show-current) --limit 5

# 查看失败日志
gh run view <RUN_ID> --log-failed
````

**使用 git + curl：**

````bash
分支 = $(git 分支 --show-current)

# 列出该分支上运行的工作流
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  “https://api.github.com/repos/$OWNER/$REPO/actions/runs?branch=$BRANCH&per_page=5”\
  | python3-c“
导入系统，json
运行 = json.load(sys.stdin)['workflow_runs']
对于运行中的 r：
    print(f\"运行 {r['id']}: {r['name']} - {r['结论'] 或 r['status']}\")"

# 获取失败的作业日志（下载为 zip、解压、读取）
RUN_ID=<运行 ID>
卷曲-s-L \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/logs \
  -o /tmp/ci-logs.zip
cd /tmp && unzip -o ci-logs.zip -d ci-logs && cat ci-logs/*.txt
````

### 第 2 步：修复并推送

确定问题后，使用文件工具（`patch`、`write_file`）来修复它：

````bash
git add <固定文件>
git commit -m“修复：解决 <check_name> 中的 CI 失败”
git 推送
````

### 第 3 步：验证

使用上面第 4 节中的命令重新检查 CI 状态。

### 自动修复循环模式

当要求自动修复 CI 时，请遵循以下循环：

1. 检查 CI 状态 → 识别故障
2.阅读故障日志→理解错误
3. 使用 `read_file` + `patch`/`write_file` → 修复代码
4. `git 添加 . && git commit -m "修复：..." && git Push`
5.等待CI→重新检查状态
6. 如果仍然失败，请重复（最多尝试 3 次，然后询问用户）

## 6. 合并

**与 gh:**

````bash
# 挤压合并+删除分支（对于功能分支来说最干净）
gh pr 合并 --squash --删除分支

# 启用自动合并（所有检查通过后合并）
gh pr 合并 --auto --squash --delete-branch
````

**使用 git + curl：**

````bash
PR_NUMBER=<数字>

# 通过 API 合并 PR (squash)
卷曲-s -X PUT \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d“{
    \"merge_method\": \"挤压\",
    \"commit_title\": \"功能：添加用户身份验证 (#$PR_NUMBER)\"
  }”

# 合并后删除远程分支
分支 = $(git 分支 --show-current)
git push origin --删除 $BRANCH

# 本地切换回main
git checkout main && git pull origin main
git 分支 -d $BRANCH
````

合并方法：“merge”（合并提交）、“squash”、“rebase”

### 启用自动合并（curl）

````bash
# 自动合并需要存储库在设置中启用它。
# 这使用 GraphQL API，因为 REST 不支持自动合并。
PR_NODE_ID=$(curl -s \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c“导入sys，json;打印（json.load（sys.stdin）['node_id']）”）

卷曲-s -X POST \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/graphql \
  -d "{\"query\": \"mutation { enablePullRequestAutoMerge(input: {pullRequestId: \\\"$PR_NODE_ID\\\", mergeMethod: SQUASH}) { clientMutationId } }\"}"
````

## 7. 完整的工作流程示例

````bash
# 1. 从干净的主程序开始
git checkout main && git pull origin main

#2. 分支
git checkout -b 修复/登录重定向错误

# 3.（Agent使用文件工具进行代码更改）

# 4. 提交
git add src/auth/login.py 测试/test_login.py
git commit -m“修复：登录后正确的重定向 URL

保留 ?next= 参数，而不是始终重定向到 /dashboard。”

# 5. 推
git Push -u 原点 HEAD

# 6. 创建 PR（根据可用内容选择 gh 或 curl）
# ...（参见第 3 节）

# 7. 监控 CI（参见第 4 节）

# 8. 绿色时合并（参见第 6 节）
````

## 有用的 PR 命令参考

|行动| gh | git + 卷曲 |
|--------|-----|------------|
|列出我的 PR | `gh 公关列表 --作者@me` | `curl -s -H "授权：令牌 $GITHUB_TOKEN" "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"` |
|查看公关差异 | `gh 公关差异` | `git diff main...HEAD` (本地) 或 `curl -H "Accept: application/vnd.github.diff" ...` |
|添加评论 | `gh pr 评论 N --body "..."` | `curl -X POST .../issues/N/comments -d '{"body":"..."}'` |
|请求审查 | `gh pr edit N --add-reviewer user` | `curl -X POST .../pulls/N/requested_reviewers -d '{"reviewers":["user"]}'` |
|关闭公关 | `gh pr 关闭 N` | `curl -X PATCH .../pulls/N -d '{"state":"close"}'` |
|查看某人的公关 | `gh pr 结账 N` | `git fetch origin pull/N/head:pr-N && git checkout pr-N` |