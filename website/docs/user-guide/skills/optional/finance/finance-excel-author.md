---
title: "Excel Author"
sidebar_label: "Excel Author"
description: "Build auditable Excel workbooks headless with openpyxl — blue/black/green cell conventions, formulas over hardcodes, named ranges, balance checks, sensitivit..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Excel 写作

使用 openpyxl 构建可无头的可审计 Excel 工作簿 — 蓝/黑/绿单元格约定、硬编码公式、命名范围、余额检查、敏感度表。用于财务模型、审计输出、对账。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/finance/excel-author` 安装 |
|路径| `可选技能/财务/excel-作者` |
|版本 | `1.0.0` |
|作者 |人择（由 Nous Research 改编）|
|许可证|阿帕奇-2.0 |
|平台| linux、macos、windows |
|标签 | `excel`、`openpyxl`、`财务`、`电子表格`、`建模` |
|相关技能| [`pptx-author`](/docs/user-guide/skills/optional/finance/finance-pptx-author)、[`dcf-model`](/docs/user-guide/skills/optional/finance/finance-dcf-model)、[`comps-analysis`](/docs/user-guide/skills/Optional/finance/finance-comps-analysis), [`lbo-model`](/docs/user-guide/skills/optional/finance/finance-lbo-model), [`3-statement-model`](/docs/user-guide/skills/optional/finance/finance-3-statement-model) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# excel-作者

使用“openpyxl”在磁盘上生成 .xlsx 文件。遵循下面的银行家级约定，以便该模型是可审计的、灵活的，并且可由构建该模型的人以外的其他人进行审查。

改编自 [anthropics/financial-services](https://github.com/anthropics/financial-services) 存储库中 Anthropic 的“xlsx-author”和“audit-xls”技能。原始版本的 MCP / Office-JS / Cowork 特定分支被删除 - 该技能假设无头 Python。

## 输出合约

- 写入`./out/<name>.xlsx`。如果`./out/`不存在，则创建它。
- 返回最终消息中的相对路径，以便下游工具可以拾取它。
- 每个文件一个逻辑模型。除非明确要求，否则不要附加到现有工作簿。

## 设置

````bash
pip 安装“openpyxl>=3.0”
````

## 核心约定（不可协商）

### 蓝/黑/绿单元格颜色
- **Blue** (`Font(color="0000FF")`) — 人类输入的硬编码输入。收入驱动因素、WACC 投入、码头增长、市场数据。
- **黑色**（默认）— 公式。每个派生单元格都是一个实时 Excel 公式。
- **绿色** (`Font(color="006100")`) — 链接到另一个工作表或外部文件。

然后，审阅者可以扫描该工作表并立即查看假设与计算结果。

### 公式优于硬编码
每个计算单元格必须是公式字符串，而不是在 Python 中计算并粘贴为值的数字。

````蟒蛇
# 错误 — 等待发生的无声错误
ws["D20"] = 前年收入 * (1 + 增长)

# CORRECT — 当用户改变假设时进行调整
ws["D20"] = "=D19*(1+$B$8)"
````

唯一允许的硬编码数字：
1. 原始历史输入（实际收入、报告的 EBITDA 等）
2. 用户要灵活运用的假设驱动因素（增长率、WACC 输入、终端 g）
3. 当前市场数据（股价、债务余额）——带有记录来源+日期的单元格注释

如果您发现自己在 Python 中计算一个值并写入结果，请停止。

### 跨表引用的命名范围
对从另一张工作表、幻灯片或备忘录引用的任何图形使用命名范围。

````蟒蛇
从 openpyxl.workbook.define_name 导入 DefinedName
wb.define_names["WACC"] = DefinedName("WACC", attr_text="输入！$C$8")
# 然后在其他地方：
计算[“D30”] =“=D29/WACC”
````

### 余额检查选项卡
包括一个“检查”选项卡，将所有内容联系起来并显示 TRUE/FALSE：
- 资产负债表余额（资产=负债+权益）
- 现金流量与 BS 上的同期现金变化相关
- 各部分总和与合并总数的关系
- 计算范围内没有恶意硬编码

示例：
````蟒蛇
检查 = wb.create_sheet("检查")
支票["A2"] = "BS 余额"
检查["B2"] = "=IS!D20-IS!D21-IS!D22"
检查["C2"] = "=ABS(B2)<0.01" # 对/错
````

### 每个硬编码输入的单元格注释
在创建单元格时添加注释，而不是稍后添加。

````蟒蛇
从 openpyxl.comments 导入评论
ws["C2"] = 1_250_000_000
ws["C2"].font = 字体(color="0000FF")
ws["C2"].comment = Comment("来源：10-K FY2024，第 47 页，收入线"，"分析师")
````

格式：`来源：[系统/文档]、[日期]、[参考]、[URL（如果适用）]`。

切勿推迟采购。切勿写“TODO：添加源”。

## 骨架：典型的财务模型

````蟒蛇
从 openpyxl 导入工作簿
从 openpyxl.styles 导入字体、图案填充、对齐方式、边框、侧面
从 openpyxl.comments 导入评论
从 openpyxl.utils 导入 get_column_letter
从 pathlib 导入路径

蓝色=字体（颜色=“0000FF”）
黑色=字体（颜色=“000000”）
绿色=字体（颜色=“006100”）
粗体=字体（粗体=真）
HEADER_FILL = PatternFill("实心", fgColor="1F4E79")
HEADER_FONT = 字体（颜色=“FFFFFF”，粗体=True）

wb = 工作簿()

# --- 输入选项卡 ---
inp = wb.活动
inp.title = "输入"
inp["A1"] = "市场数据和关键输入"
inp["A1"].font = HEADER_FONT
inp["A1"].fill = HEADER_FILL
inp.merge_cells("A1:C1")

inp["B3"] = "2024 财年收入"
inp["C3"] = 1_250_000_000
inp["C3"].font = 蓝色
inp["C3"].comment = Comment("来源：10-K FY2024 p.47", "模型")

inp["B4"] = "增长率"
输入[“C4”] = 0.12
inp["C4"].font = 蓝色

# --- 计算选项卡 ---
计算 = wb.create_sheet("DCF")
calc["B2"] = "预计收入"
calc["C2"] = "=Inputs!C3*(1+Inputs!C4)" # 公式，黑色

# --- 检查选项卡 ---
chk = wb.create_sheet("检查")
chk["A2"] = "BS 余额"
chk["B2"] = "=ABS(BS!D20-BS!D21-BS!D22)<0.01"

路径("./out").mkdir(exist_ok=True)
wb.save("./out/model.xlsx")
````

## 带有合并单元格的节标题

openpyxl 怪癖：合并时，在左上角单元格上设置值并单独设置整个范围的样式。

````蟒蛇
ws["A7"] = "现金流量预测"
ws["A7"].font = HEADER_FONT
ws.merge_cells("A7:H7")
for col in range(1, 9): # A..H
    ws.cell(行=7，列=列).fill = HEADER_FILL
````

## 灵敏度表

使用循环构建，而不是每个单元格硬编码公式。规则：

- **奇数行/列**（5×5 或 7×7）— 保证真正的中心单元格。
- **中心单元 = 基本情况。** 中间行/列标题必须等于模型的实际 WACC 和终端 g，以便中心输出等于基本情况隐含股价。这就是健全性检查。
- **使用中蓝色填充（“BDD7EE”）和粗体突出显示中心单元格。
- 用完整的重新计算公式填充每个单元格 - 绝不是近似值。

````蟒蛇
# 5x5 WACC（行）x 终端生长（列）敏感性
wacc_axis = [0.08, 0.085, 0.09, 0.095, 0.10] # 中心行 = 基数 9.0%
term_axis = [0.02, 0.025, 0.03, 0.035, 0.04] # 中心 col = 基数 3.0%

起始行 = 40
ws.cell(row=start_row, column=1).value = "隐含股价 ($)"
ws.cell(行=开始行，列=1).font = BOLD

对于 enumerate(term_axis) 中的 j、g：
    ws.cell(行=start_row+1,列=2+j).value = g
    ws.cell(行=start_row+1,列=2+j).font = 蓝色

对于 enumerate(wacc_axis) 中的 i、w：
    r = 起始行 + 2 + i
    ws.cell(行=r,列=1).value = w
    ws.cell(行=r,列=1).font = 蓝色
    对于 enumerate(term_axis) 中的 j、g：
        c = 2 + j
        # 完整的 DCF 重新计算公式（为了说明而简化）。
        # 在真实模型中，这引用了完整的投影块。
        ws.cell(行=r,列=c).value = (
            f"=SUMPRODUCT(FCF_range,1/(1+{w})^year_offset) + "
            f"FCF_terminal*(1+{g})/({w}-{g})/(1+{w})^terminal_year"
        ）

# 突出显示中心单元格（基本情况）
center = ws.cell(row=start_row+2+len(wacc_axis)//2,
                 列=2+len(term_axis)//2)
center.fill = PatternFill("solid", fgColor="BDD7EE")
center.font = 粗体
````

## 发货前重新计算

openpyxl 写入公式字符串但不计算它们。 Excel 在打开时重新计算，但下游使用者（自动检查脚本、CI）需要计算值。

在交付前运行 LibreOffice 或专用的重新计算步骤：

````bash
# LibreOffice 无头重新计算
libreoffice --headless --calc --convert-to xlsx ./out/model.xlsx --outdir ./out/
````

或者使用 Python 重新计算助手（请参阅本技能中的“scripts/recalc.py”）。

## 模型布局规划

在编写任何公式之前：
1. 定义所有部分行位置
2. 编写所有标题和标签
3. 写入所有节分隔线和空白行
4. 然后使用锁定的行位置编写公式

这可以防止级联公式破坏模式，即在写入公式后插入标题行会移动每个下游引用。

## 与用户逐步验证

对于大型模型（DCF、三语句、LBO），请在继续之前停止并向用户显示中间工件。在构建下游敏感度表之前发现错误的裕度假设可以节省一个小时。

检查点模式：
- 输入块之后 → 显示原始输入，在投影前确认
- 收入预测后 → 确认营收 + 增长
- FCF建成后→确认完整的时间表
- WACC之后→确认输入
- 估值后→确认股权桥
- 然后建立敏感度表

## 何时不使用此技能

- 使用 Office MCP 进行实时 Excel 会话的用户 — 改为驱动他们的实时工作簿。
- 没有公式的纯表格数据导出 - `csv` 或 `pandas.to_excel` 更简单。
- 具有很强交互性的仪表板/图表——使用真正的 BI 工具。

## 归因

约定（蓝/黑/绿、硬编码公式、命名范围、敏感度规则）改编自 Anthropic 的 Claude for Financial Services 插件套件，已获得 Apache-2.0 许可。原文：https://github.com/anthropics/financial-services/tree/main/plugins/vertical-plugins/financial-analysis/skills/xlsx-author