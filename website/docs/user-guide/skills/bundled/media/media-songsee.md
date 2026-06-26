---
title: "Songsee — Audio spectrograms/features (mel, chroma, MFCC) via CLI"
sidebar_label: "Songsee"
description: "Audio spectrograms/features (mel, chroma, MFCC) via CLI"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#松西

通过 CLI 的音频频谱图/功能（梅尔、色度、MFCC）。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/媒体/songsee` |
|版本 | `1.0.0` |
|作者 |社区 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `音频`、`可视化`、`频谱图`、`音乐`、`分析` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 歌见

从音频文件生成频谱图和多面板音频特征可视化。

## 先决条件

需要 [Go](https://go.dev/doc/install)：
````bash
去安装 github.com/steipete/songsee/cmd/songsee@latest
````

可选：“ffmpeg”适用于 WAV/MP3 以外的格式。

## 快速入门

````bash
# 基本频谱图
歌见曲目.mp3

# 保存到指定文件
Songsee track.mp3 -o 频谱图.png

# 多面板可视化网格
Songsee track.mp3 --viz 频谱图、mel、色度、hpss、selfsim、响度、tempogram、mfcc、flux

# 时间片（从12.5秒开始，持续8秒）
Songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg

# 来自标准输入
猫的踪迹.mp3 | Songsee - --format png -o out.png
````

## 可视化类型

使用带有逗号分隔值的“--viz”：

|类型 |描述 |
|------|-------------|
| `频谱图` |标准频谱图 |
| `梅尔` |梅尔标度谱图 |
| `色度` |音高等级分布 |
| `hpss` |和声/打击乐分离 |
| `selfsim` |自相似矩阵|
| `响度` |随时间变化的响度 |
| `温度图` |节奏估计 |
| `mfcc` |梅尔频率倒谱系数 |
| `通量` |光谱通量（起始检测）|

多个“--viz”类型在单个图像中呈现为网格。

## 常用标志

|旗帜|描述 |
|------|-------------|
| `--即` |可视化类型（逗号分隔）|
| `--风格` |调色板：“经典”、“岩浆”、“地狱”、“绿色”、“灰色” |
| `--width` / `--height` |输出图像尺寸 |
| `--window` / `--hop` | FFT 窗口和跳跃大小 |
| `--最小频率` / `--最大频率` |频率范围滤波器|
| `--start` / `--duration` |音频的时间片|
| `--格式` |输出格式：`jpg` 或 `png` |
| `-o` |输出文件路径 |

## 注释

- WAV 和 MP3 本地解码；其他格式需要`ffmpeg`
- 可以使用“vision_analyze”检查输出图像以进行自动音频分析
- 用于比较音频输出、调试合成或记录音频处理管道