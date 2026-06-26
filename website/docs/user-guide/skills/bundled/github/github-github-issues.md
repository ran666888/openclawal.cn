---
title: "Github Issues — Create, triage, label, assign GitHub issues via gh or REST"
sidebar_label: "Github Issues"
description: "Create, triage, label, assign GitHub issues via gh or REST"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# GitHub 问题

通过 gh 或 REST 创建、分类、标记、分配 GitHub 问题。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/github/github-问题` ​​|
|版本 | `1.1.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `GitHub`、`问题`、`项目管理`、`Bug 跟踪`、`分类` |
|相关技能| [`github-auth`](/docs/user-guide/skills/bundled/github/github-github-auth), [`github-pr-workflow`](/docs/user-guide/skills/bundled/github/github-github-pr-workflow) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# GitHub 问题管理

创建、搜索、分类和管理 GitHub 问题。每个部分首先显示“gh”，然后显示“curl”回退。

## 先决条件

- 通过 GitHub 进行身份验证（请参阅“github-auth”技能）
- 在具有 GitHub 远程的 git 存储库内，或显式指定存储库

### 设置

````bash
if 命令 -v gh &>/dev/null && gh auth status &>/dev/null;然后
  授权=“呃”
否则
  授权=“git”
  如果[-z“$GITHUB_TOKEN”];然后
    if _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env";然后
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null;然后
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    菲
  菲
菲

REMOTE_URL=$(git 远程 get-url 来源)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
````

---

## 1.查看问题

**与 gh:**

````bash
gh 问题列表
gh 问题列表 --state open --label "bug"
gh 问题列表--受让人@me
gh 问题列表 --search "authentication error" --state all
gh 问题视图 42
````

**带卷曲：**

````bash
# 列出未解决的问题
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  “https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20”\
  | python3-c“
导入系统，json
对于 json.load(sys.stdin) 中的 i：
    if 'pull_request' not in i: # GitHub API 也在 /issues 中返回 PR
        labels = ', '.join(l['name'] for l in i['labels'])
        print(f\"#{i['number']:5} {i['state']:6} {labels:30} {i['title']}\")"

# 按标签过滤
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  “https://api.github.com/repos/$OWNER/$REPO/issues?state=open&labels=bug&per_page=20” \
  | python3-c“
导入系统，json
对于 json.load(sys.stdin) 中的 i：
    如果“pull_request”不在 i 中：
        print(f\"#{i['number']} {i['title']}\")"

# 查看具体问题
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  | python3-c“
导入系统，json
i = json.load(sys.stdin)
labels = ', '.join(l['name'] for l in i['labels'])
受让人 = ', '.join(a['login'] for a in i['受让人'])
print(f\"#{i['number']}: {i['title']}\")
print(f\"州: {i['state']} 标签: {labels} 受让人: {受让人}\")
print(f\"作者：{i['user']['login']} 创建：{i['created_at']}\")
打印(f\"\n{i['body']}\")"

# 搜索问题
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  “https://api.github.com/search/issues?q=authentication+error+repo:$OWNER/$REPO”\
  | python3-c“
导入系统，json
对于 json.load(sys.stdin)['items'] 中的 i：
    print(f\"#{i['number']} {i['state']:6} {i['title']}\")"
````

## 2. 创建问题

**与 gh:**

````bash
gh 问题创建 \
  --title“登录重定向忽略？next=参数”\
  --body "## 描述
登录后，用户始终会登陆 /dashboard。

## 重现步骤
1. 注销时导航至 /settings
2. 重定向到/login?next=/settings
3. 登录
4.实际：重定向到/dashboard（应该转到/settings）

## 预期行为
遵守 ?next= 查询参数。” \
  --label“bug，后端”\
  --受让人“用户名”
````

**带卷曲：**

````bash
卷曲-s -X POST \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d'{
    "title": "登录重定向忽略 ?next= 参数",
    "body": "## 描述\n登录后，用户始终登陆 /dashboard。\n\n## 重现步骤\n1. 注销时导航到 /settings\n2. 重定向到 /login?next=/settings\n3. 登录\n4. 实际：重定向到 /dashboard\n\n## 预期行为\n遵守 ?next= 查询参数。",
    “标签”：[“错误”，“后端”]，
    “受让人”：[“用户名”]
  }'
````

### 错误报告模板

````
## 错误描述
<发生了什么事>

## 重现步骤
1. <步骤>
2. <步骤>

## 预期行为
<应该发生什么>

## 实际行为
<实际发生了什么>

## 环境
- 操作系统：<操作系统>
- 版本：<版本>
````

### 功能请求模板

````
## 功能描述
<你想要什么>

## 动机
<为什么这会有用>

## 建议的解决方案
<它是如何工作的>

## 考虑的替代方案
<其他方法>
````

## 3. 管理问题

### 添加/删除标签

**与 gh:**

````bash
gh 问题编辑 42 --add-label“优先级：高，bug”
gh 问题编辑 42 --remove-label "needs-triage"
````

**带卷曲：**

````bash
# 添加标签
卷曲-s -X POST \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \
  -d '{"labels": ["priority:high", "bug"]}'

# 删除标签
卷曲-s -X删除\
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels/needs-triage

# 列出存储库中可用的标签
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/labels \
  | python3-c“
导入系统，json
对于 json.load(sys.stdin) 中的 l：
    print(f\" {l['名称']:30} {l.get('描述', '')}\")"
````

### 作业

**与 gh:**

````bash
gh 问题编辑 42 --add-受让人用户名
gh 问题编辑 42 --add-assignee @me
````

**带卷曲：**

````bash
卷曲-s -X POST \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42/assignees \
  -d '{"受让人": ["用户名"]}'
````

### 评论

**与 gh:**

````bash
gh 问题评论 42 --body“已调查 - 根本原因在于 auth 中间件。正在修复。”
````

**带卷曲：**

````bash
卷曲-s -X POST \
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42/comments \
  -d '{"body": "已调查 — 根本原因在于身份验证中间件。正在修复。"}'
````

### 关闭和重新开放

**与 gh:**

````bash
gh 问题关闭 42
gh 问题关闭 42 --原因“未计划”
gh 问题重新打开 42
````

**带卷曲：**

````bash
# 关闭
卷曲-s -X 补丁\
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  -d '{"state": "已关闭", "state_reason": "已完成"}'

# 重新打开
卷曲-s -X 补丁\
  -H“授权：令牌$GITHUB_TOKEN”\
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  -d '{"状态": "打开"}'
````

### 将问题链接到 PR

当 PR 与正文中的正确关键字合并时，问题会自动关闭：

````
关闭 #42
修复 #42
解决 #42
````

要从问题创建分支：

**与 gh:**

````bash
gh 问题开发 42 --checkout
````

**使用 git （相当于手动）：**

````bash
git checkout main && git pull origin main
git checkout -b 修复/issue-42-登录重定向
````

## 4. 问题分类工作流程

当被要求对问题进行分类时：

1. **列出未分类的问题：**

````bash
# 与 gh
gh 问题列表 --label "needs-triage" --state open

# 带有卷曲
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  “https://api.github.com/repos/$OWNER/$REPO/issues?labels=needs-triage&state=open”\
  | python3-c“
导入系统，json
对于 json.load(sys.stdin) 中的 i：
    如果“pull_request”不在 i 中：
        print(f\"#{i['number']} {i['title']}\")"
````

2. **阅读并分类**每个问题（查看详细信息，了解错误/功能）

3. **应用标签和优先级**（请参阅上面的管理问题）

4. **分配**（如果所有者明确）

5. **如有需要，可评论分类注释**

## 5. 批量操作

对于批处理操作，将 API 调用与 shell 脚本结合起来：

**与 gh:**

````bash
# 关闭具有特定标签的所有问题
gh 问题列表 --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issues close {} --原因“未计划”
````

**带卷曲：**

````bash
# 列出带有标签的问题编号，然后关闭每个问题
卷曲-s \
  -H“授权：令牌$GITHUB_TOKEN”\
  “https://api.github.com/repos/$OWNER/$REPO/issues?labels=wontfix&state=open”\
  | python3 -c "导入 sys,json; [print(i['number']) for i in json.load(sys.stdin)]" \
  |同时读取数字；做
    卷曲-s -X 补丁\
      -H“授权：令牌$GITHUB_TOKEN”\
      https://api.github.com/repos/$OWNER/$REPO/issues/$num \
      -d '{"state": "已关闭", "state_reason": "not_planned"}'
    echo“已关闭#$num”
  完成
````

## 快速参考表

|行动| gh |卷曲端点 |
|--------|-----|--------------|
|列出问题 | `gh 问题列表` | `GET /repos/{o}/{r}/issues` |
|查看问题 | `gh 问题视图 N` | `GET /repos/{o}/{r}/issues/N` |
|创建问题 | `gh 问题创建...` | `POST /repos/{o}/{r}/issues` |
|添加标签 | `gh 问题编辑 N --add-label ...` | `POST /repos/{o}/{r}/issues/N/labels` |
|分配| `gh 问题编辑 N --add-受让人 ...` | `POST /repos/{o}/{r}/issues/N/受让人` |
|评论 | `gh 问题评论 N --body ...` | `POST /repos/{o}/{r}/issues/N/comments` |
|关闭 | `gh 问题关闭 N` | `PATCH /repos/{o}/{r}/issues/N` |
|搜索 | `gh 问题列表 -- 搜索“...”` | `GET /search/issues?q=...` |