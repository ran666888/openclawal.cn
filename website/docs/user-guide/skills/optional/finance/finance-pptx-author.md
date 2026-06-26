---
title: "Pptx Author — Build PowerPoint decks headless with python-pptx"
sidebar_label: "Pptx Author"
description: "Build PowerPoint decks headless with python-pptx"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# PPT 写作

使用 python-pptx 构建无头 PowerPoint 幻灯片。与 excel-author 配合使用模型支持的套牌，其中每个数字都追溯到工作簿单元格。用于宣传材料、IC 备忘录、收益说明。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/finance/pptx-author` 安装 |
|路径| `可选技能/财务/pptx-作者` |
|版本 | `1.0.0` |
|作者 |人择（由 Nous Research 改编）|
|许可证|阿帕奇-2.0 |
|平台| linux、macos、windows |
|标签 | `powerpoint`、`pptx`、`python-pptx`、`演示文稿`、`财务` |
|相关技能| [`excel-author`](/docs/用户指南/技能/可选/finance/finance-excel-author)，[`powerpoint`](/docs/user-guide/skills/bundled/productivity/productivity-powerpoint) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# pptx-作者

使用“python-pptx”在磁盘上生成 .pptx 文件。当您需要将演示文稿作为文件工件提供而不是驱动实时 PowerPoint 会话时使用。

改编自 Anthropic 在 [anthropics/financial-services](https://github.com/anthropics/financial-services) 中的“pptx-author”和“pitch-deck”技能。原始版本的 MCP / Office-JS 分支被删除——这假设是无头 Python。

对于更广泛的、已提供的 PowerPoint 创作技能（幻灯片、演讲者笔记、嵌入、媒体），请参阅内置的“powerpoint”技能。这项技能是一种轻量级模式，针对模型支持的平台（推介平台、IC 备忘录、收益说明）进行了调整，其中每个数字都必须追溯到源工作簿。

## 输出合约

- 写入`./out/<name>.pptx`。如果`./out/`不存在，则创建它。
- 返回最终消息中的相对路径。

## 设置

````bash
pip 安装“python-pptx>=0.6”
````

## 核心约定

### 每张幻灯片一个想法
标题说明了要点；身体支撑它。标题为“第三季度收入”的幻灯片表现疲弱； “第三季度收入同比增速加速至 14%”强劲。

### 每个数字都可以追溯到型号
如果幻灯片上的图形来自“./out/model.xlsx”，请为工作表和单元格添加脚注。

````
收入：12.5 亿美元（来源：model.xlsx，输入！C3）
````

切勿从内存或摘要中转录数字 - 打开工作簿，读取命名范围，并尽可能以编程方式将牌组值与其绑定。

### 安装时使用坚固模板
如果 `./templates/firm-template.pptx` 存在，则加载它，以便幻灯片继承品牌颜色、字体和主布局。

````蟒蛇
从 pptx 导入演示文稿
从 pathlib 导入路径

模板 = Path("./templates/firm-template.pptx")
prs = 演示文稿(str(模板)) 如果 template.exists() else 演示文稿()
````

### 图表：PNG-from-model 击败原生 pptx 图表
当保真度很重要时（模型的图表样式必须与平台完全匹配），将图表从源工作簿渲染为 PNG 并嵌入图像。原生的“pptx.chart”图表很脆弱，并且通常不符合严格的惯例。

````蟒蛇
从 pptx.util 导入英寸
Slide.shapes.add_picture("./out/charts/football_field.png",
                         英寸(1)、英寸(2)、
                         宽度=英寸(8))
````

### 没有外部发送
该技能写入文件。它从不发送电子邮件、上传或发帖。编排层处理交付。

## 骷髅

````蟒蛇
从 pptx 导入演示文稿
from pptx.util import 英寸、Pt
从 pptx.dml.color 导入 RGBColor
从 pathlib 导入路径

模板 = Path("./templates/firm-template.pptx")
prs = 演示文稿(str(模板)) 如果 template.exists() else 演示文稿()

# 标题幻灯片
幻灯片 = prs.slides.add_slide(prs.slide_layouts[0])
Slide.shapes.title.text = "极光计划 — 战略替代方案"
Slide.placeholders[1].text = "初步讨论材料"

# 估值摘要幻灯片（仅标题布局）
幻灯片 = prs.slides.add_slide(prs.slide_layouts[5])
Slide.shapes.title.text = "估值意味着在不同方法中每股 38-52 美元"

# 添加一个绑定到模型输出的表
行、列 = 5、4
tbl_shape = slip.shapes.add_table(行、列、
                                   英寸(0.5)、英寸(1.5)、
                                   英寸(9)、英寸(3))
tbl = tbl_shape.table
headers = [“方法”、“低 ($)”、“中 ($)”、“高 ($)”]
对于 enumerate(headers) 中的 c、h：
    tbl.cell(0, c).text = h

# 在真实的套牌中，使用 openpyxl 从模型工作簿中读取这些内容
数据 = [
    （“交易比较”，“35”，“41”，“48”），
    （“先例并购”、“39”、“45”、“52”）、
    （“DCF（基础）”、“36”、“43”、“51”）、
    （“杠杆收购（10% IRR）”、“33”、“38”、“44”）、
]
对于 r，枚举中的行（数据，开始 = 1）：
    对于 c，枚举（行）中的 val：
        tbl.cell(r, c).text = val

# 嵌入从模型渲染的图表
幻灯片 = prs.slides.add_slide(prs.slide_layouts[5])
Slide.shapes.title.text = "足球场 — 当前价格 42 美元"
Slide.shapes.add_picture("./out/charts/football_field.png",
                         英寸(1)、英寸(1.8)、宽度=英寸(8))

路径("./out").mkdir(exist_ok=True)
prs.save("./out/pitch-aurora.pptx")
````

## 将牌组编号绑定到源工作簿

从 Excel 模型中读取命名范围或特定单元格，这样甲板编号就不会漂移。

````蟒蛇
从 openpyxl 导入 load_workbook

wb = load_workbook("./out/model.xlsx", data_only=True)
def 编号（名称）：
    """将命名范围解析为其当前计算值。"""
    rng = wb.define_names[名称]
    工作表，坐标 = 下一个（rng.destinations）
    返回wb[工作表][坐标].值

Revenue_fy24 = nr("RevenueFY24")
implied_mid = nr("ImpliedSharePriceBase")
````

然后使用这些值构建牌组内容：
````蟒蛇
Slide.shapes.title.text = f“${implied_mid:.2f} 的隐含股价（基本情况）”
````

请记住在阅读工作簿之前重新计算它 - openpyxl 仅在已经计算工作表的情况下才能看到计算值。首先在“excel-author”技能中运行重新计算助手，或通过真正的 Excel 会话打开/保存。

## 融资演讲稿的幻灯片式清单

典型的银行业融资演讲稿遵循这种结构。不是规定性的，但作为起始框架很有用：

1. 封面/标题
2. 免责声明
3. 目录
四、情况概述
5. 公司快照（目标）
6. 市场/行业背景
7. 估值总结（足球场）——资金滑坡
8. 交易补偿详情
9. 过往交易详情
10.贴现现金流总结
11. 杠杆收购/保荐人案例说明
12. 流程注意事项
13. 附录

## 何时不使用此技能

- 使用 Office MCP 进行实时 PowerPoint 会话的用户 — 改为驾驶他们的实时文档。
- 非财务幻灯片（季度全体会议、营销幻灯片）——使用更广泛的“powerpoint”技能。
- 带有大量动画、过渡或演讲者注释的幻灯片 — 使用更广泛的“powerpoint”技能。

## 归因

约定改编自 Anthropic 的 Claude for Financial Services 插件套件，已获得 Apache-2.0 许可。原文：https://github.com/anthropics/financial-services/tree/main/plugins/agent-plugins/pitch-agent/skills/pptx-author