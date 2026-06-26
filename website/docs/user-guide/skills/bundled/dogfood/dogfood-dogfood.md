---
title: "Dogfood — Exploratory QA of web apps: find bugs, evidence, reports"
sidebar_label: "Dogfood"
description: "Exploratory QA of web apps: find bugs, evidence, reports"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 狗食

Web 应用程序的探索性 QA：查找错误、证据、报告。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/dogfood` |
|版本 | `1.0.0` |
|平台| linux、macos、windows |
|标签 | `qa`、`测试`、`浏览器`、`web`、`dogfood` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Dogfood：系统的 Web 应用程序 QA 测试

## 概述

此技能将指导您使用浏览器工具集对 Web 应用程序进行系统的探索性 QA 测试。您将导航应用程序、与元素交互、捕获问题证据并生成结构化错误报告。

## 先决条件

- 浏览器工具集必须可用（`browser_navigate`、`browser_snapshot`、`browser_click`、`browser_type`、`browser_vision`、`browser_console`、`browser_scroll`、`browser_back`、`browser_press`）
- 用户的目标 URL 和测试范围

## 输入

用户提供：
1. **目标URL**——测试的入口点
2. **范围** — 重点关注哪些领域/功能（或用于全面测试的“完整站点”）
3. **输出目录**（可选）- 保存屏幕截图和报告的位置（默认：`./dogfood-output`）

## 工作流程

请遵循以下 5 个阶段的系统工作流程：

### 第一阶段：计划

1.创建输出目录结构：
<!-- ascii-guard-ignore -->
   ````
   {输出目录}/
   ├──截图/#证据截图
   └──report.md # 最终报告（第5阶段生成）
   ````
<!-- ascii-guard-ignore-end -->
2. 根据用户输入确定测试范围。
3. 通过规划要测试的页面和功能来构建粗略的站点地图：
   - 登陆/主页
   - 导航链接（页眉、页脚、侧边栏）
   - 关键用户流程（注册、登录、搜索、结帐等）
   - 表格和互动元素
   - 边缘情况（空状态、错误页面、404）

### 第二阶段：探索

对于计划中的每个页面或功能：

1. **导航**至页面：
   ````
   browser_navigate(url="https://example.com/page")
   ````

2. **拍个快照**来了解DOM结构：
   ````
   browser_snapshot()
   ````

3. **检查控制台**是否存在 JavaScript 错误：
   ````
   browser_console（清除= true）
   ````
   每次导航和每次重要交互后都执行此操作。无声 JS 错误是高价值的发现。

4. **截取带注释的屏幕截图**以直观地评估页面并识别交互元素：
   ````
   browser_vision(question="描述页面布局，识别任何视觉问题、损坏的元素或可访问性问题", annotate=true)
   ````
   “annotate=true”标志覆盖交互式元素上编号的“[N]”标签。每个“[N]”映射到后续浏览器命令的引用“@eN”。

5. **系统地测试交互元素**：
   - 单击按钮和链接：`browser_click(ref="@eN")`
   - 填写表格：`browser_type(ref="@eN", text="test input")`
   - 测试键盘导航：`browser_press(key="Tab")`、`browser_press(key="Enter")`
   - 滚动浏览内容：`browser_scroll(direction="down")`
   - 使用无效输入测试表单验证
   - 测试空提交

6. **每次交互后**，检查：
   - 控制台错误：`browser_console()`
   - 视觉变化：`browser_vision(question="交互后发生了什么变化？")`
   - 预期行为与实际行为

### 第三阶段：收集证据

对于发现的每个问题：

1. **截取屏幕截图**显示问题：
   ````
   browser_vision(question="捕获并描述此页面上可见的问题", annotate=false)
   ````
   保存响应中的“screenshot_path”——您将在报告中引用它。

2. **记录详细信息**：
   - 发生问题的 URL
   - 重现步骤
   - 预期行为
   - 实际行为
   - 控制台错误（如果有）
   - 截图路径

3. **使用问题分类法对问题进行分类**（请参阅 `references/issue-taxonomy.md`）：
   - 严重性：严重/高/中/低
   - 类别：功能/视觉/辅助功能/控制台/用户体验/内容

### 第 4 阶段：分类

1. 查看所有收集到的问题。
2. 去重——合并在不同地方出现的相同错误的问题。
3. 为每个问题分配最终的严重性和类别。
4. 按严重性排序（首先是严重，然后是高、中、低）。
5. 按执行摘要的严重性和类别对问题进行计数。

### 第五阶段：报告

使用“templates/dogfood-report-template.md”中的模板生成最终报告。

报告必须包括：
1. **执行摘要**，包含问题总数、按严重程度细分和测试范围
2. **每期章节**：
   - 期号和标题
   - 严重性和类别徽章
   - 观察到的 URL
   - 问题描述
   - 重现步骤
   - 预期行为与实际行为
   - 屏幕截图参考（使用“MEDIA:<screenshot_path>”作为内联图像）
   - 控制台错误（如果相关）
3. **所有问题的汇总表**
4. **测试说明** — 测试了什么，未测试什么，是否有任何阻碍

将报告保存到“{output_dir}/report.md”。

## 工具参考

|工具|目的|
|------|---------|
| `浏览器导航` |转到 URL |
| `浏览器快照` |获取 DOM 文本快照（辅助树）|
| `浏览器单击` |通过 ref (`@eN`) 或文本 | 单击元素
| `浏览器类型` |在输入字段中输入 |
| `浏览器滚动` |在页面上向上/向下滚动 |
| `浏览器返回` |返回浏览器历史记录 |
| `browser_press` |按键盘键 |
| `浏览器视觉` |截图+AI分析；对元素标签使用“annotate=true” |
| `浏览器控制台` |获取 JS 控制台输出和错误 |

## 提示

- **在导航和重要交互之后始终检查 `browser_console()`。** 无声 JS 错误是最有价值的发现之一。
- **当您需要推断交互式元素位置或快照引用不清楚时，请使用“annotate=true”和“browser_vision”**。
- **使用有效和无效输入进行测试** - 表单验证错误很常见。
- **滚动浏览长页面** - 折叠下方的内容可能存在渲染问题。
- **测试导航流程** — 单击端到端的多步骤流程。
- **通过注意屏幕截图中可见的任何布局问题来检查响应行为**。
- **不要忘记边缘情况**：空状态、很长的文本、特殊字符、快速点击。
- 向用户报告屏幕截图时，请包含“MEDIA:<screenshot_path>”，以便他们可以看到内嵌的证据。