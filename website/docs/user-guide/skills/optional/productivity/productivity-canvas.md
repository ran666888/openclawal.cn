---
title: "Canvas — Canvas LMS integration — fetch enrolled courses and assignments using API token authentication"
sidebar_label: "Canvas"
description: "Canvas LMS integration — fetch enrolled courses and assignments using API token authentication"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 画布

Canvas LMS 集成 — 使用 API 令牌身份验证获取已注册的课程和作业。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/productivity/canvas` 安装 |
|路径| `可选技能/生产力/画布` |
|版本 | `1.0.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `Canvas`、`LMS`、`教育`、`课程`、`作业` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Canvas LMS — 课程和作业访问

对 Canvas LMS 的只读访问权限，用于列出课程和作业。

## 脚本

- `scripts/canvas_api.py` — 用于 Canvas API 调用的 Python CLI

## 设置

1. 在浏览器中登录您的Canvas实例
2. 转到 **帐户 → 设置**（单击您的个人资料图标，然后单击“设置”）
3. 滚动到 **批准的集成** 并单击 **+ 新访问令牌**
4. 命名令牌（例如“OpenClaw”），设置可选的到期时间，然后单击 **生成令牌**
5. 复制令牌并添加到`${HERMES_HOME:-~/.hermes}/.env`：

````
CANVAS_API_TOKEN=your_token_here
CANVAS_BASE_URL=https://yourschool.instruction.com
````

基本 URL 是您登录 Canvas 时浏览器中显示的任何内容（无尾部斜杠）。

## 用法

````bash
CANVAS =“python $HERMES_HOME/skills/productivity/canvas/scripts/canvas_api.py”

# 列出所有活跃课程
$CANVAS list_courses --注册状态活跃

# 列出所有课程（任何州）
$CANVAS 列表_课程

# 列出特定课程的作业
$CANVAS list_assignments 12345

# 列出按截止日期排序的作业
$CANVAS list_assignments 12345 --order-by due_at
````

## 输出格式

**list_courses** 返回：
```json
[{"id": 12345, "name": "CS 简介", "course_code": "CS101", "workflow_state": "可用", "start_at": "...", "end_at": "..."}]
````

**列表分配** 返回：
```json
[{"id": 67890, "name": "作业 1", "due_at": "2025-02-15T23:59:00Z", "points_possible": 100, "submission_types": ["online_upload"], "html_url": "...", "description": "...", "course_id": 12345}]
````

注意：作业描述被截断为 500 个字符。 `html_url` 字段链接到 Canvas 中的完整作业页面。

## API 参考 (curl)

````bash
# 列出课程
curl -s -H "授权：持有者 $CANVAS_API_TOKEN" \
  “$CANVAS_BASE_URL/api/v1/courses?enrollment_state=active&per_page=10”

# 列出课程作业
curl -s -H "授权：持有者 $CANVAS_API_TOKEN" \
  “$CANVAS_BASE_URL/api/v1/courses/COURSE_ID/作业？per_page=10&order_by=due_at”
````

Canvas 使用“Link”标题进行分页。 Python 脚本自动处理分页。

## 规则

- 此技能是**只读** - 它仅获取数据，从不修改课程或作业
- 首次使用时，通过运行“$CANVAS list_courses”来验证身份验证 - 如果失败并显示 401，则引导用户完成设置
- Canvas 速率限制为每 10 分钟约 700 个请求；如果达到限制，请检查“X-Rate-Limit-Remaining”标头

## 故障排除

|问题 |修复 |
|---------|-----|
| 401 未经授权 |令牌无效或过期 - 在 Canvas 设置中重新生成 |
| 403 禁止令牌缺乏此课程的权限 |
|空课程列表 |尝试“--enrollment-state active”或省略该标志以查看所有状态 |
|错误机构|验证“CANVAS_BASE_URL”与浏览器中的 URL 匹配 |
|超时错误 |检查 Canvas 实例的网络连接 |