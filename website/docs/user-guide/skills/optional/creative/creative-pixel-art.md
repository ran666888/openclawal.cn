---
title: "Pixel Art — Pixel art w/ era palettes (NES, Game Boy, PICO-8)"
sidebar_label: "Pixel Art"
description: "Pixel art w/ era palettes (NES, Game Boy, PICO-8)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 像素艺术

带时代调色板的像素艺术（NES、Game Boy、PICO-8）。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/creative/pixel-art` 安装 |
|路径| `可选技能/创意/像素艺术` |
|版本 | `2.0.0` |
|作者 |渡渡鸟到达 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `创意`、`像素艺术`、`街机`、`snes`、`nes`、`gameboy`、`复古`、`图像`、`视频` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 像素艺术

将任何图像转换为复古像素艺术，然后选择将其动画化为短片
具有适合时代的效果（雨、萤火虫、雪、余烬）的 MP4 或 GIF。

有两个脚本附带此技能：

- `scripts/pixel_art.py` — 照片 → 像素艺术 PNG（Floyd-Steinberg 抖动）
- `scripts/pixel_art_video.py` — 像素艺术 PNG → 动画 MP4（+ 可选 GIF）

每个都是可导入或可直接运行的。预设捕捉到硬件调色板
当您想要时代精确的颜色（NES、Game Boy、PICO-8 等）时，或使用
街机/SNES 风格外观的自适应 N 色量化。

## 何时使用

- 用户想要从源图像中获得复古像素艺术
- 用户要求 NES / Game Boy / PICO-8 / C64 / 街机 / SNES 造型
- 用户想要一个简短的循环动画（雨景、夜空、雪景等）
- 海报、专辑封面、社交帖子、精灵、角色、头像

## 工作流程

生成前，与用户确认样式。不同的预设产生
产出差异很大，再生成本高昂。

### 第 1 步 — 提供风格

使用 4 个代表性预设调用“clarify”。根据内容选择套装
用户要求 - 不要只转储所有 14 个。

当用户意图不清楚时的默认菜单：

````蟒蛇
澄清（
    Question="您想要哪种像素艺术风格？",
    选择=[
        “街机 - 大胆、厚实的 80 年代橱柜感觉（16 种颜色，8 像素）”，
        “nes — Nintendo 8 位硬件调色板（54 色，8px）”，
        “gameboy — 4 色绿色 Game Boy DMG”,
        “snes — 更干净的 16 位外观（32 色，4 像素）”，
    ],
）
````

当用户已经命名了一个时代（例如“80s arcade”、“Gameboy”）时，跳过
`clarify`并直接使用匹配的预设。

### 第 2 步 — 提供动画（可选）

如果用户要求提供视频/GIF，或者输出可能会受益于运动，
问哪个场景：

````蟒蛇
澄清（
    Question="想要制作动画吗？选择一个场景或跳过。",
    选择=[
        “夜晚——星星+萤火虫+树叶”，
        “城市——雨+霓虹灯脉冲”，
        “雪——飘落的雪花”，
        “跳过-仅图像”，
    ],
）
````

不要连续调用“clarify”两次以上。一种用于风格，一种用于场景
动画就在桌子上。如果用户明确要求特定样式
以及他们消息中的场景，完全跳过“澄清”。

### 步骤 3 — 生成

首先运行“pixel_art()”；如果请求动画，则链接到
结果上的“pixel_art_video()”。

## 预设目录

|预设|时代|调色板|块|最适合 |
|--------|-----|---------|--------|---------|
| `街机` | 80 年代街机 |自适应 16 | 8 像素 |大胆的海报，英雄艺术|
| `斯内斯` | 16 位 |自适应 32 | 4 像素 |人物、场景细节|
| `其他` | 8 位 |红白机 (54) | 8 像素 |真正的 NES 外观 |
| `游戏男孩` | DMG 手持式 | 4 种绿色色调 | 8 像素 |单色游戏男孩 |
| `gameboy_pocket` |袖珍手持设备| 4 种灰色色调 | 8 像素 |单声道 GB 袖珍 |
| `pico8` | PICO-8 | 16 固定 | 6 像素 |幻想控制台外观|
| `c64` |准将 64 | 16 固定 | 8 像素 | 8位家用电脑|
| `苹果2` | Apple II 高分辨率 | 6 固定 | 10 像素 |极致复古，6色|
| `图文电视` | BBC 图文电视 | 8 纯 | 10 像素 |厚实的原色|
| `mspaint` | Windows MS 画图 | 24 固定 | 8 像素 |怀旧桌面|
| `mono_green` | CRT荧光粉| 2 绿色 | 6 像素 |终端/CRT美学|
| `mono_amber` | CRT 琥珀色 | 2 琥珀 | 6 像素 |琥珀色显示器外观 |
| `霓虹灯` |赛博朋克 | 10 霓虹灯 | 6 像素 |蒸汽波/网络 |
| `粉彩` |柔和的粉彩| 10 粉彩 | 6 像素 |卡哇伊/温柔|

命名调色板位于“scripts/palettes.py”中（请参阅“references/palettes.md”了解
完整列表 — 总共 28 个命名调色板）。任何预设都可以被覆盖：

````蟒蛇
Pixel_art（“in.png”，“out.png”，预设=“snes”，调色板=“PICO_8”，块= 6）
````

## 场景目录（用于视频）

|场景|效果|
|--------|---------|
| '夜晚' |闪烁的星星+萤火虫+飘零的树叶|
| `黄昏` |萤火虫+火花|
| `小酒馆` |尘埃微粒+温暖的火花|
| `室内` |尘埃微粒|
| `城市` |雨+霓虹灯脉冲|
| `自然` |树叶+萤火虫|
| ‘魔法’ |火花+萤火虫|
| ‘风暴’ |雨+闪电 |
| `水下` |气泡+闪光|
| `火` |余烬+火花|
| `雪` |雪花+火花|
| `沙漠` |热闪光+灰尘|

## 调用模式

### Python（导入）

````蟒蛇
导入系统
sys.path.insert(0, "/home/teknium/.hermes/skills/creative/pixel-art/scripts")
从像素_艺术导入像素_艺术
从像素艺术视频导入像素艺术视频

# 1. 转换为像素艺术
Pixel_art（“/path/to/photo.jpg”，“/tmp/pixel.png”，预设=“nes”）

# 2. 动画（可选）
像素艺术视频（
    “/tmp/pixel.png”，
    “/tmp/pixel.mp4”，
    场景=“夜晚”，
    持续时间=6，
    帧率=15，
    种子=42，
    导出_gif =真，
）
````

### 命令行界面

````bash
cd /home/teknium/.hermes/skills/creative/pixel-art/scripts

python Pixel_art.py in.jpg out.png --preset gameboy
python Pixel_art.py in.jpg out.png --preset snes --palette PICO_8 --block 6

python Pixel_art_video.py out.png out.mp4 --场景夜晚 --duration 6 --gif
````

## 管道原理

**像素转换：**
1. 增强对比度/颜色/清晰度（对于较小的调色板来说更强）
2. 量化前进行色调分离以简化色调区域
3.使用“Image.NEAREST”按“block”缩小尺寸（硬像素，无插值）
4. 使用 Floyd-Steinberg 抖动进行量化 — 与自适应
   N 调色板或命名硬件调色板
5. 使用“Image.NEAREST”进行升级

缩小后进行量化可保持抖动与最终像素网格对齐。
之前的量化会浪费误差扩散到消失的细节上。

**视频叠加：**
- 每个刻度复制基本框架（静态背景）
- 叠加无状态的每帧粒子绘制（每个效果一个函数）
- 通过 ffmpeg `libx264 -pix_fmt yuv420p -crf 18` 进行编码
- 通过 `palettegen` + `paletteuse` 可选 GIF

## 依赖关系

-Python 3.9+
- 枕头（`pip install Pillow`）
- PATH 上的 ffmpeg（仅视频需要 — OpenClaw 安装此软件包）

## 陷阱

- 托盘键区分大小写（“NES”、“PICO_8”、“GAMEBOY_ORIGINAL”）。
- 非常小的源（<100px 宽）会在 8-10px 块下折叠。高档的
  如果它很小，请先获取来源。
- 小数“块”或“调色板”将破坏量化 - 保持它们为正整数。
- 动画粒子计数针对约 640x480 画布进行了调整。在非常大的
  对于图像，您可能需要使用不同的密度种子进行第二遍。
- `mono_green` / `mono_amber` 强制 `color=0.0`（去饱和）。如果你覆盖
  并保持色度，2色调色板可以在平滑区域产生条纹。
- `clarify` 循环：每回合最多调用两次（样式，然后场景）。不要
  为用户提供更多选择。

## 验证

- PNG 在输出路径中创建
- 在预设的块大小下可见清晰的方形像素块
- 颜色计数与预设匹配（观察图像或运行“Image.open(p).getcolors()”）
- 视频是有效的 MP4（“ffprobe”可以打开它），大小非零

## 归因

命名硬件调色板和“pixel_art_video.py”中的程序动画循环
移植自 [pixel-art-studio](https://github.com/Synero/pixel-art-studio)
（麻省理工学院）。有关详细信息，请参阅此技能目录中的“ATTRIBUTION.md”。