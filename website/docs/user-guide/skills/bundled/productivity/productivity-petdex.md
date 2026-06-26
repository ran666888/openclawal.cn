---
title: "Petdex — Install and select animated petdex mascots for OpenClaw"
sidebar_label: "Petdex"
description: "Install and select animated petdex mascots for OpenClaw"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 佩德克斯

为 OpenClaw 安装并选择动画 petdex 吉祥物。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/生产力/petdex` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `petdex`、`mascot`、`display`、`cli`、`tui`、`desktop` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 佩德克斯技能

浏览、安装并从公众中选择动画“宠物”吉祥物
[petdex](https://github.com/crafter-station/petdex) 画廊。已安装的宠物
对代理活动（空闲、运行工具、检查、错误、完成）做出反应
Hermes CLI、TUI 和桌面应用程序。该技能驱动“hermes pets”CLI
和“display.pet”配置 - 它不会生成精灵。

## 何时使用

- 用户想要桌面/终端吉祥物或询问“pets”/petdex。
- 用户想要更改、预览或禁用活动宠物。
- 诊断宠物不显示的原因（终端图形支持、配置）。

## 先决条件

- 对库/清单的“petdex.dev”的网络访问（只读，无身份验证）。
- 用于精灵解码的 Pillow（OpenClaw 核心依赖项）——已安装。
- 对于全保真终端渲染：具有图形功能的终端（kitty、
  Ghostty、WezTerm、iTerm2 或 Sixel）。否则为真彩色 Unicode
  自动使用半块回退。

## 如何运行

使用“terminal”工具运行“hermes pets <子命令>”。

## 快速参考

|目标|命令|
| --- | --- |
|浏览画廊 | `hermes pets list`（添加一个子字符串来过滤：`hermes pets list cat`）|
|列出已安装的宠物 | `爱马仕宠物列表--已安装` |
|安装宠物 | `hermes pets install <slug>`（添加 `--select` 以使其处于活动状态）|
|设置活跃宠物| `hermes pets select <slug>`（省略选择器的 slug）|
|随处调整宠物大小 | `hermes pets scale <factor>`（例如`0.5`，限制在 0.1–3.0）|
|在终端中预览/动画 | `爱马仕宠物秀 [slug] [--cycle] [--state run]` |
|禁用宠物 | “爱马仕宠物关闭”|
|移除宠物 | `爱马仕宠物移除 <slug>` |
|诊断设置 | 『爱马仕宠物医生』 |

## 程序

1. 找到一只宠物：“hermes pets list <query>”并记下它的“slug”。
2. 安装+激活：`hermes pets install <slug> --select`。
3. 预览：`hermes pets show`（Ctrl+C 停止）。
4. 确认设置：`hermes pets doctor` — 显示已解析的宠物，已配置
   渲染模式、检测到的终端图形协议和有效模式。

Pets 安装到 `<HERMES_HOME>/pets/<slug>/`（配置文件感知）。选择宠物
将 `display.pet.slug` + `display.pet.enabled` 写入 `config.yaml`。

## 配置

在“config.yaml”中的“display.pet”下：

- `enabled` (bool) — 主控开/关。
- `slug` (str) — 活跃宠物；空=首次安装。
- `render_mode` — `auto`（检测）| `小猫` | `iterm` | `六塞尔` | `unicode` | ‘关’。
- `scale` (float) — 原生 192×208 帧的屏幕尺寸（默认 0.33，
  夹紧0.1–3.0）。一个旋钮可调整每个表面的大小；设置为
  `hermes pets scale <factor>`、`/pet scale` 斜线命令或桌面
  外观滑块。
- `unicode_cols` (int) — Unicode 后备的列宽度。

## 陷阱

- 宠物仅在安装并选择后才会显示（“启用：true”）。
- 在管道/重定向（无 TTY）内部，终端渲染被设计为禁用。
- petdex npm CLI 安装到 `~/.codex/pets`；爱马仕用的是自己的
  相反，配置文件范围为“<HERMES_HOME>/pets/”——通过“hermes pets”安装。

## 验证

- 当安装、选择宠物时，“爱马仕宠物医生”报告“✓ 就绪”，
  启用，并且 Pillow 是可导入的。