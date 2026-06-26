---
title: "Meme Generation — Generate real meme images by picking a template and overlaying text with Pillow"
sidebar_label: "Meme Generation"
description: "Generate real meme images by picking a template and overlaying text with Pillow"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 模因一代

通过选择模板并用 Pillow 覆盖文本来生成真实的 meme 图像。生成实际的 .png meme 文件。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用“hermes Skills installficial/creative/meme- Generation”进行安装 |
|路径| `可选技能/创意/模因生成` |
|版本 | `2.0.0` |
|作者 |阿达纳莱西奥 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “创意”、“模因”、“幽默”、“图像” |
|相关技能| [`ascii-art`](/docs/user-guide/skills/bundled/creative/creative-ascii-art)，`生成小部件` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 模因一代

从主题生成实际的模因图像。选择一个模板，编写标题，并渲染带有文本叠加的真实 .png 文件。

## 何时使用

- 用户要求您制作或生成模因
- 用户想要一个关于特定主题、情况或挫折的表情包
- 用户说“meme this”或类似内容

## 可用模板

该脚本按名称或 ID 支持 **任何约 100 个流行的 imgflip 模板**，以及 10 个带有手动调整文本定位的精选模板。

### 策划模板（自定义文本放置）

|身份证 |名称 |领域 |最适合 |
|----|------|--------|----------|
| `这很好` |这很好|顶部、底部|混乱、否认|
| `德雷克` |德雷克热线珠宝 |拒绝、批准 |拒绝/偏好|
| '心烦意乱的男朋友' |心烦意乱的男朋友|分心、当前、人|诱惑，改变优先事项|
| `两个按钮` |两个按钮|左，右，人|不可能的选择|
| “扩展大脑” |拓展大脑 | 4 级 |讽刺不断升级|
| `改变我的想法` |改变我的想法 |声明|热门话题 |
|女人对着猫大喊大叫女人对猫大喊大叫女人，猫|论据 |
| “一个不简​​单” |一个人不只是简单地 |顶部、底部 |看似困难的事情|
| `鹤计划` |格鲁的计划|步骤1-3，实现|适得其反的计划|
|蝙蝠侠打罗宾蝙蝠侠打罗宾耳光|罗宾, 蝙蝠侠 |关闭坏主意|

### 动态模板（来自 imgflip API）

任何不在策划列表中的模板都可以通过名称或 imgflip ID 来使用。这些获得智能默认文本定位（2 字段的顶部/底部，3+ 的均匀间隔）。搜索方式：
````bash
python“$SKILL_DIR/scripts/generate_meme.py”--搜索“灾难”
````

## 程序

### 模式1：经典模板（默认）

1. 阅读用户的主题并识别核心动态（混乱、困境、偏好、讽刺等）
2. 选择最匹配的模板。使用“最适合”列，或使用“--search”进行搜索。
3. 为每个字段编写简短的标题（每个字段最多 8-12 个单词，越短越好）。
4.找到技能的脚本目录：
   ````
   SKILL_DIR=$(目录名“$(find ~/.hermes/skills -path '*/meme- Generation/SKILL.md' 2>/dev/null | head -1)”)
   ````
5. 运行生成器：
   ````bash
   python "$SKILL_DIR/scripts/generate_meme.py" <template_id> /tmp/meme.png "标题 1" "标题 2" ...
   ````
6. 使用`MEDIA:/tmp/meme.png`返回图像

### 模式 2：自定义 AI 图像（当 image_generate 可用时）

当不适合经典模板或用户想要原创内容时，请使用此选项。

1.先写出标题。
2. 使用“image_generate”创建一个与 meme 概念相匹配的场景。不要在图像提示中包含任何文本 - 文本将由脚本添加。仅描述视觉场景。
3. 从image_generate结果URL中找到生成的图片路径。如果需要，将其下载到本地路径。
4. 使用“--image”运行脚本来覆盖文本，选择一种模式：
   - **叠加**（文本直接在图像上，白色，黑色轮廓）：
     ````bash
     python "$SKILL_DIR/scripts/generate_meme.py" --image /path/to/scene.png /tmp/meme.png “顶部文本” “底部文本”
     ````
   - **条**（上面/下面的黑色条带白色文本 - 更干净，始终可读）：
     ````bash
     python "$SKILL_DIR/scripts/generate_meme.py" --image /path/to/scene.png --bars /tmp/meme.png “顶部文本” “底部文本”
     ````
   当图像很复杂/很详细并且上面的文本难以阅读时，请使用“--bars”。
5. **用视觉验证**（如果 `vision_analyze` 可用）：检查结果看起来不错：
   ````
   Vision_analyze(image_url="/tmp/meme.png", Question="文本清晰且位置合适吗？模因在视觉上有效吗？")
   ````
   如果视觉模型标记问题（文本难以阅读、放置不当等），请尝试其他模式（在覆盖和条形之间切换）或重新生成场景。
6. 使用`MEDIA:/tmp/meme.png`返回图像

## 示例

**“凌晨2点调试生产”：**
````bash
pythongenerate_meme.py this-is-fine /tmp/meme.png“服务器着火了”“这很好”
````

**“在睡觉和再看一集之间做出选择”：**
````bash
pythongenerate_meme.py drake /tmp/meme.png“睡8小时”“凌晨3点再看一集”
````

**“周一早上的各个阶段”：**
````bash
pythongenerate_meme.pyexpanding-brain/tmp/meme.png“设置闹钟”“设置 5 个闹钟”“在所有闹钟响起时睡觉”“在床上工作”
````

## 列表模板

要查看所有可用模板：
````bash
pythongenerate_meme.py--列表
````

## 陷阱

- 保持字幕简短。长文本的模因看起来很糟糕。
- 将文本参数的数量与模板的字段计数相匹配。
- 选择适合笑话结构的模板，而不仅仅是主题。
- 请勿生成仇恨、辱骂或针对个人的内容。
- 首次下载后，脚本将模板图像缓存在“scripts/.cache/”中。

## 验证

如果满足以下条件，则输出正确：
- 在输出路径中创建了一个 .png 文件
- 模板上的文本清晰（白色，黑色轮廓）
- 笑话落地 — 标题与模板的预期结构相匹配
- 文件可以通过 MEDIA: 路径传送