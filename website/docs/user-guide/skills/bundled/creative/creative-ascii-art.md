---
title: "Ascii Art — ASCII art: pyfiglet, cowsay, boxes, image-to-ascii"
sidebar_label: "Ascii Art"
description: "ASCII art: pyfiglet, cowsay, boxes, image-to-ascii"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# ASCII 艺术

ASCII 艺术：pyfiglet、cowsay、boxes、image-to-ascii。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/创意/ascii-art` |
|版本 | `4.0.0` |
|作者 | 0xbyt4，爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `ASCII`、`Art`、`Banners`、`Creative`、`Unicode`、`Text-Art`、`pyfiglet`、`figlet`、`cowsay`、`boxes` |
|相关技能| [`excalidraw`](/docs/user-guide/skills/bundled/creative/creative-excalidraw) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# ASCII 艺术技巧

满足不同 ASCII 艺术需求的多种工具。所有工具都是本地 CLI 程序或免费的 REST API — 无需 API 密钥。

## 工具 1：文本横幅（pyfiglet — 本地）

将文本渲染为大型 ASCII 艺术横幅。 571 种内置字体。

### 设置

````bash
pip install pyfiglet --break-system-packages -q
````

### 用法

````bash
python3 -m pyfiglet“您的文本”-f 倾斜
python3 -m pyfiglet "TEXT" -f doom -w 80 # 设置宽度
python3 -m pyfiglet --list_fonts # 列出所有 571 种字体
````

### 推荐字体

|风格|字体|最适合 |
|--------|------|----------|
|干净、现代 | `倾斜` |项目名称、标题 |
|大胆而块状| `厄运` |标题、徽标|
|大且可读 | ‘大’ |横幅|
|经典横幅| `横幅3` |宽屏显示器 |
|紧凑| `小` |字幕|
|赛博朋克 | `网络大` |科技主题 |
| 3D效果| `3-d` |启动画面 |
|哥特式| `哥特式` |戏剧性的文字|

### 提示

- 预览 2-3 种字体并让用户选择自己喜欢的
- 短文本（1-8 个字符）最适合使用“doom”或“block”等详细字体
- 长文本与“小”或“迷你”等紧凑字体配合使用效果更好

## 工具 2：文本横幅（asciified API — 远程，无需安装）

免费的 REST API，可将文本转换为 ASCII 艺术。 250 多种 Figlet 字体。直接返回纯文本——无需解析。当未安装 pyfiglet 时使用此选项或作为快速替代方案。

### 用法（通过终端curl）

````bash
# 基本文本横幅（默认字体）
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=Hello+World”

# 使用特定字体
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant”
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Doom”
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Star+Wars”
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=3-D”
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Banner3”

# 列出所有可用字体（返回 JSON 数组）
卷曲-s“https://asciified.thelicato.io/api/v2/fonts”
````

### 提示

- URL 将文本参数中的空格编码为“+”
- 响应是纯文本 ASCII art — 无 JSON 包装，可以显示
- 字体名称区分大小写；使用字体端点来获取确切的名称
- 使用curl在任何终端上工作——不需要Python或pip

## 工具 3：Cowsay（消息艺术）

使用 ASCII 字符将文本包装在对话气泡中的经典工具。

### 设置

````bash
sudo apt installowsay -y # Debian/Ubuntu
#brew安装cowsay#macOS
````

### 用法

````bash
牛说“你好世界”
owsay -f tux "Linux 规则" # Tux 企鹅
owsay -f 龙“Rawr！”          #龙
owsay -f 剑龙“咆哮！”     # 剑龙
Cowthink “嗯……”# 思想泡泡
owsay -l # 列出所有字符
````

### 可用字符（50+）

`beavis.zen`、`bong`、`bunny`、`cheese`、`daemon`、`default`、`dragon`、
“龙牛”、“大象”、“眼睛”、“火焰骷髅”、“捉鬼敢死队”、
`hellokitty`、`kiss`、`kitty`、`koala`、`luke-koala`、`mech-and-cow`、
`meow`、`moofasa`、`驼鹿`、`ren`、`羊`、`骨架`、`小`、
“剑龙”、“刺激”、“超级挤奶者”、“手术”、“三眼”、
`火鸡`、`乌龟`、`燕尾服`、`乳房`、`vader`、`vader-koala`、`www`

### 眼睛/舌头修饰符

````bash
owsay -b“博格”# =_= 眼睛
owsay -d“死”# x_x 眼睛
owsay -g“贪婪”# $_$ 眼睛
owsay -p“偏执狂”#@_@眼睛
owsay -s“石头”# *_* 眼睛
owsay -w“连线”# O_O 眼睛
owsay -e "OO" "Msg" # 自定义眼睛
owsay -T "U " "Msg" # 自定义舌头
````

## 工具 4：盒子（装饰边框）

在任何文本周围绘制装饰性 ASCII 艺术边框/框架。 70 多个内置设计。

### 设置

````bash
sudo apt install box -y # Debian/Ubuntu
#brew 安装框#macOS
````

### 用法

````bash
回声“你好世界”|框 # 默认框
回声“你好世界”| box -d Stone # 石头边框
回声“你好世界”| box -d 羊皮纸 # 羊皮纸卷轴
回声“你好世界”| box -d cat # 猫边框
回声“你好世界”| box -ddog # 狗边框
回声“你好世界”|盒子 -d unicornsay # 独角兽
回声“你好世界”| Boxs -d Diamonds # 钻石图案
回声“你好世界”| box -d c-cmt # C 风格注释
回声“你好世界”| box -d html-cmt # HTML 注释
回声“你好世界”| box -a c# 居中文本
box -l # 列出所有 70 多种设计
````

### 与 pyfiglet 或 asciified 结合

````bash
python3 -m pyfiglet "HERMES" -f 倾斜|盒子-d石头
# 或者没有安装 pyfiglet:
卷曲-s“https://asciified.thelicato.io/api/v2/ascii?text=HERMES&font=Slant”|盒子-d石头
````

## 工具 5：厕所（彩色文字艺术）

与 pyfiglet 类似，但具有 ANSI 颜色效果和视觉滤镜。非常适合终端视觉糖果。

### 设置

````bash
sudo apt安装厕所厕所字体-y # Debian/Ubuntu
#brew 安装厕所#macOS
````

### 用法

````bash
厕所“Hello World”#基本文字艺术
toilet -f bigmono12 "Hello" # 特定字体
厕所——同性恋“彩虹！”                 # 彩虹色
厕所——金属“金属！”                 # 金属效果
厕所 -F border "Bordered" # 添加边框
厕所 -F 边框 --gay “太棒了！”         # 综合效果
toilet -f pagga "Block" # 块式字体（toilet独有）
厕所 -F list # 列出可用的过滤器
````

### 过滤器

`crop`、`gay`（彩虹）、`metal`、`flip`、`flop`、`180`、`left`、`right`、`border`

**注意**：厕所输出颜色的 ANSI 转义码 - 在终端中工作，但可能无法在所有上下文中呈现（例如，纯文本文件、某些聊天平台）。

## 工具 6：图像到 ASCII 艺术

将图像（PNG、JPEG、GIF、WEBP）转换为 ASCII 艺术。

### 选项 A：ascii-image-converter（推荐，现代）

````bash
# 安装
sudo snap 安装 ascii-image-converter
# 或者：安装 github.com/TheZoraiz/ascii-image-converter@latest
````

````bash
ascii-image-converter image.png # 基本
ascii-image-converter image.png -C # 颜色输出
ascii-image-converter image.png -d 60,30 # 设置尺寸
ascii-image-converter image.png -b # 盲文字符
ascii-image-converter image.png -n # 负/反转
ascii-image-converter https://url/image.jpg # 直接 URL
ascii-image-converter image.png --save-txt out # 另存为文本
````

### 选项 B：jp2a（轻量级，仅限 JPEG）

````bash
sudo apt install jp2a -y
jp2a --width=80 图像.jpg
jp2a --colors image.jpg # 彩色
````

## 工具 7：搜索预制 ASCII 艺术

从网络上搜索精选的 ASCII 艺术。将“terminal”与“curl”一起使用。

### 来源 A：ascii.co.uk（推荐用于预制艺术）

按主题组织的大量经典 ASCII 艺术作品集。艺术位于 HTML `<pre>` 标签内。使用curl 获取页面，然后使用一个小的Python 片段提取艺术作品。

**URL 模式：** `https://ascii.co.uk/art/{subject}`

**第 1 步 — 获取页面：**

````bash
卷曲 -s 'https://ascii.co.uk/art/cat' -o /tmp/ascii_art.html
````

**步骤 2 — 从预标签中提取艺术作品：**

````蟒蛇
导入重新，html
将 open('/tmp/ascii_art.html') 作为 f：
    文本 = f.read()
arts = re.findall(r'<pre[^>]*>(.*?)</pre>', text, re.DOTALL)
对于艺术中的艺术：
    clean = re.sub(r'<[^>]+>', '', art)
    干净 = html.unescape(clean).strip()
    如果长度（干净）> 30：
        打印（干净）
        打印（'\n---\n'）
````

**可用主题**（用作 URL 路径）：
- 动物：`猫`、`狗`、`马`、`鸟`、`鱼`、`龙`、`蛇`、`兔子`、`大象`、`海豚`、`蝴蝶`、`猫头鹰`、`狼`、`熊`、`企鹅`、`乌龟`
- 对象：`汽车`、`船`、`飞机`、`火箭`、`吉他`、`电脑`、`咖啡`、`啤酒`、`蛋糕`、`房子`、`城堡`、`剑`、`皇冠`、`钥匙`
- 自然：“树”、“花”、“太阳”、“月亮”、“星星”、“山”、“海洋”、“彩虹”
- 角色：‘骷髅’、‘机器人’、‘天使’、‘巫师’、‘海盗’、‘忍者’、‘外星人’
- 假期：“圣诞节”、“万圣节”、“情人节”

**提示：**
- 保留艺术家签名/缩写——重要礼仪
- 每页有多个艺术作品 - 为用户选择最好的一个
- 通过curl可靠地工作，不需要JavaScript

### 来源 B：GitHub Octocat API（有趣的复活节彩蛋）

返回带有明智引用的随机 GitHub Octocat。无需授权。

````bash
卷曲-s https://api.github.com/octocat
````

## 工具 8：有趣的 ASCII 实用程序（通过curl）

这些免费服务直接返回 ASCII 艺术 — 非常适合额外的乐趣。

### QR 码作为 ASCII 艺术

````bash
卷曲-s“qrenco.de/Hello+World”
卷曲-s“qrenco.de/https://example.com”
````

### 天气作为 ASCII 艺术

````bash
curl -s "wttr.in/London" # 带 ASCII 图形的完整天气预报
curl -s "wttr.in/Moon" # ASCII 艺术中的月相
curl -s "v2.wttr.in/London" # 详细版本
````

## 工具 9：法学硕士生成的定制艺术（后备）

当上述工具没有所需内容时，可以直接使用这些 Unicode 字符生成 ASCII 艺术作品：

### 角色调色板

**方框图：** `╔ ╗ ╚ ╝ ║ ═ ╠ ╣ ╦ ╩ ╬ ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╰ ╯`

**块元素：** `░ ▒ ▓ █ ▄ ▀ ▌ ▐ ▖ ▗ ▘ ▝ ▚ ▞`

**几何及符号：** `◆ ◇ ◈ ● ○ ◉ ■ □ ▲ △ ▼ ▽ ★ ☆ ✦ ✧ ◀ ▶ ◁ ▷ ⬡ ⬢ ⌂`

### 规则

- 最大宽度：每行 60 个字符（终端安全）
- 最大高度：横幅 15 行，场景 25 行
- 仅等宽字体：输出必须以固定宽度字体正确呈现

## 决策流程

1. **文本作为横幅** → pyfiglet（如果已安装），否则通过curl asciified API
2. **用有趣的人物艺术包裹一条信息**→cowsay
3. **添加装饰边框/框架** → 盒子（可与pyfiglet/asciified结合）
4. **特定事物的艺术**（猫、火箭、龙）→ ascii.co.uk 通过curl +解析
5. **将图像转换为 ASCII** → ascii-image-converter 或 jp2a
6. **二维码** → qrenco.de 通过curl
7. **天气/月亮艺术** → wttr.in 通过curl
8. **定制/创意的东西** → 使用 Unicode 调色板生成法学硕士
9. **任何未安装的工具** → 安装它，或退回到下一个选项