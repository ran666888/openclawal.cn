---
title: "Openhue — Control Philips Hue lights, scenes, rooms via OpenHue CLI"
sidebar_label: "Openhue"
description: "Control Philips Hue lights, scenes, rooms via OpenHue CLI"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 开放色调

通过 OpenHue CLI 控制 Philips Hue 灯光、场景、房间。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/智能家居/openhue` |
|版本 | `1.0.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “智能家居”、“色调”、“灯光”、“物联网”、“自动化”|

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# OpenHue CLI

从终端通过 Hue 桥控制 Philips Hue 灯光和场景。

## 先决条件

````bash
# Linux（预构建的二进制文件）
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew 安装 openhue/cli/openhue-cli
````

首次运行需要按下 Hue Bridge 上的按钮进行配对。网桥必须位于同一本地网络上。

## 何时使用

- “打开/关闭灯”
- “调暗客厅的灯光”
- “设置场景”或“电影模式”
- 控制特定的 Hue 房间、区域或单个灯泡
- 调整亮度、颜色或色温

## 常用命令

### 列出资源

````bash
openhue get light # 列出所有灯光
openhue get room # 列出所有房间
openhue get scene # 列出所有场景
````

### 控制灯

````bash
# 打开/关闭
openhue 设置灯“卧室灯”--on
openhue 设置灯“卧室灯”--关闭

# 亮度 (0-100)
openhue 设置灯“卧室灯” --on --brightness 50

# 色温（暖色到冷色：153-500 mirek）
openhue设置灯“卧室灯”--on--温度300

# 颜色（按名称或十六进制）
openhue 设置灯“卧室灯”--on--颜色红色
openhue 设置灯“卧室灯”--on --rgb“#FF5500”
````

### 控制室

````bash
# 关闭整个房间
openhue 设置房间“卧室”--off

# 设置房间亮度
openhue 设置房间“Bedroom” --on --brightness 30
````

### 场景

````bash
openhue设置场景“Relax”--room“Bedroom”
openhue设置场景“集中”--房间“办公室”
````

## 快速预设

````bash
# 就寝时间（昏暗温暖）
openhue 设置房间“Bedroom” --on --brightness 20 --Temperature 450

# 工作模式（亮酷）
openhue 设置房间“Office” --on --brightness 100 --Temperature 250

# 电影模式（暗淡）
openhue 设置房间“Living Room” --on --brightness 10

#一切都关闭
openhue 设置房间“卧室”--off
openhue 设置房间“Office”--off
openhue 设置房间“Living Room”--off
````

## 注释

- Bridge 必须与运行 OpenClaw 的机器位于同一本地网络上
- 首次运行需要按下 Hue Bridge 上的按钮进行授权
- 颜色仅适用于支持颜色的灯泡（不适用于纯白色型号）
- 灯光和房间名称区分大小写 - 使用“openhue get light”检查确切的名称
- 与计划照明的 cron 作业配合得很好（例如，就寝时变暗，醒来时变亮）