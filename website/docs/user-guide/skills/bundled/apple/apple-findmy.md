---
title: "Findmy — Track Apple devices/AirTags via FindMy"
sidebar_label: "Findmy"
description: "Track Apple devices/AirTags via FindMy"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 找到我

在 macOS 上通过 FindMy.app 跟踪 Apple 设备/AirTags。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/苹果/findmy` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| macOS |
|标签 | `FindMy`、`AirTag`、`位置`、`跟踪`、`macOS`、`Apple` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 查找我的（苹果）

通过 macOS 上的 FindMy.app 跟踪 Apple 设备和 AirTags。因为苹果没有
为FindMy提供CLI，该技能使用AppleScript打开应用程序并
用于读取设备位置的屏幕截图。

## 先决条件

- **macOS** 已登录“查找我的应用程序”和 iCloud
- 设备/AirTags 已在“查找我的”中注册
- 终端屏幕录制权限（系统设置→隐私→屏幕录制）
- **可选但推荐**：安装 `peekaboo` 以获得更好的 UI 自动化：
  `brew 安装 steipete/tap/peekaboo`

## 何时使用

- 用户询问“我的[设备/猫/钥匙/包]在哪里？”
- 追踪 AirTag 位置
- 检查设备位置（iPhone、iPad、Mac、AirPods）
- 监控宠物或物品随时间的移动（AirTag 巡逻路线）

## 方法一：AppleScript + 屏幕截图（基本）

### 打开 FindMy 并导航

````bash
# 打开“查找我的应用程序”
osascript -e '告诉应用程序“FindMy”激活'

# 等待加载
睡觉 3

# 截取“查找我的”窗口的屏幕截图
屏幕截图-w -o /tmp/findmy.png
````

然后使用“vision_analyze”读取屏幕截图：
````
Vision_analyze(image_url="/tmp/findmy.png", Question="显示了哪些设备/项目以及它们的位置是什么？")
````

### 在选项卡之间切换

````bash
# 切换到设备选项卡
osascript -e '
告诉应用程序“系统事件”
    告诉进程“FindMy”
        单击窗口 1 工具栏 1 的“设备”按钮
    结束告诉
结束告诉'

# 切换到项目选项卡 (AirTags)
osascript -e '
告诉应用程序“系统事件”
    告诉进程“FindMy”
        单击窗口 1 工具栏 1 的“项目”按钮
    结束告诉
结束告诉'
````

## 方法 2：Peekaboo UI 自动化（推荐）

如果安装了 `peekaboo`，请使用它来实现更可靠的 UI 交互：

````bash
# 打开“查找我的”
osascript -e '告诉应用程序“FindMy”激活'
睡觉 3

# 捕获并注释 UI
peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png

# 通过元素 ID 单击特定设备/项目
peekaboo click --on B3 --app“FindMy”

# 捕获详细视图
peekaboo 图像 --app "FindMy" --path /tmp/findmy-detail.png
````

然后用视觉来分析：
````
Vision_analyze(image_url="/tmp/findmy-detail.png", Question="此设备/项目显示的位置是什么？包括地址和坐标（如果可见）。")
````

## 工作流程：随着时间的推移跟踪 AirTag 位置

用于监控 AirTag（例如，跟踪猫的巡逻路线）：

````bash
# 1. 打开 FindMy 到 Items 选项卡
osascript -e '告诉应用程序“FindMy”激活'
睡觉 3

# 2. 单击 AirTag 项目（停留在页面上 — AirTag 仅在页面打开时更新）

# 3.定期捕捉位置
虽然真实；做
    屏幕截图 -w -o /tmp/findmy-$(日期 +%H%M%S).png
    睡眠 300 # 每 5 分钟
完成
````

用视觉分析每个屏幕截图以提取坐标，然后编译路线。

## 限制

- FindMy **没有 CLI 或 API** — 必须使用 UI 自动化
- AirTags 仅在 FindMy 页面主动显示时更新位置
- 位置精度取决于 FindMy 网络中附近的 Apple 设备
- 屏幕截图需要屏幕录制权限
- AppleScript UI 自动化可能会跨 macOS 版本崩溃

## 规则

1. 跟踪 AirTags 时将 FindMy 应用程序保持在前台（最小化时更新停止）
2.使用`vision_analyze`读取屏幕截图内容——不要尝试解析像素
3. 对于持续跟踪，请使用 cronjob 定期捕获和记录位置
4. 尊重隐私——仅跟踪用户拥有的设备/物品