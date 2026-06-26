---
title: "Fitness Nutrition — Gym workout planner and nutrition tracker"
sidebar_label: "Fitness Nutrition"
description: "Gym workout planner and nutrition tracker"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

#健身营养

健身房锻炼计划和营养追踪器。通过 wger 按肌肉、设备或类别搜索 690 多个练习。通过 USDA FoodData Central 查找 380,000 多种食物的宏量和卡路里。计算 BMI、TDEE、单次最大次数、宏观分割和身体脂肪 — 纯 Python，无需安装 pip。专为追求增肌、减肥或只是想吃得更好的人而设计。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/health/fitness-nutrition` 安装 |
|路径| `可选技能/健康/健身营养` |
|版本 | `1.0.0` |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “健康”、“健身”、“营养”、“健身”、“锻炼”、“饮食”、“锻炼” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 健身与营养

专业的健身教练和运动营养师技能。两个数据源
加上离线计算器——健身爱好者所需的一切都集中在一个地方。

**数据源（全部免费，无 pip 依赖）：**

- **wger** (https://wger.de/api/v2/) — 开放练习数据库，包含 690 多个肌肉、设备、图像练习。公共端点需要零身份验证。
- **USDA FoodData Central** (https://api.nal.usda.gov/fdc/v1/) — 美国政府营养数据库，包含 380,000 多种食品。 `DEMO_KEY` 立即生效；免费注册以获得更高的限额。

**离线计算器（纯stdlib Python）：**

- BMI、TDEE (Mifflin-St Jeor)、一次最大次数 (Epley/Brzycki/Lombardi)、宏观分割、体脂百分比（美国海军方法）

---

## 何时使用

当用户询问以下问题时触发此技能：
- 练习、锻炼、健身常规、肌肉群、锻炼分割
- 食物宏量、卡路里、蛋白质含量、膳食计划、卡路里计数
- 身体成分：BMI、体脂、TDEE、热量过剩/不足
- 一次最大估计、训练百分比、渐进超负荷
- 用于切割、膨化或维护的宏观比率

---

## 程序

### 练习查找（wger API）

所有 wger 公共端点都返回 JSON 并且不需要身份验证。总是添加
`format=json` 和 `language=2`（英语）用于练习查询。

**第 1 步 - 确定用户想要什么：**

- 按肌肉 → 使用 `/api/v2/exercise/?muscles={id}&language=2&status=2&format=json`
- 按类别 → 使用 `/api/v2/exercise/?category={id}&language=2&status=2&format=json`
- 按设备 → 使用 `/api/v2/exercise/?equipment={id}&language=2&status=2&format=json`
- 按名称 → 使用 `/api/v2/exercise/search/?term={query}&language=english&format=json`
- 完整详细信息 → 使用 `/api/v2/exerciseinfo/{exercise_id}/?format=json`

**第 2 步 — 参考 ID（因此您不需要额外的 API 调用）：**

运动类别：

|身份证 |类别 |
|----|-------------|
| 8 |武器 |
| 9 |腿|
| 10 | 10腹肌 |
| 11 | 11胸部|
| 12 | 12返回 |
| 13 |肩膀|
| 14 | 14小牛|
| 15 | 15有氧运动 |

肌肉：

|身份证 |肌肉|身份证 |肌肉|
|----|----------------------------------------|----|------------------------------------|
| 1 |肱二头肌 | 2 |三角肌前束|
| 3 |前锯肌 | 4 |胸大肌 |
| 5 |外斜肌 | 6 |腓肠肌 |
| 7 |腹直肌 | 8 |臀大肌 |
| 9 |斜方肌 | 10 | 10股四头肌|
| 11 | 11股二头肌 | 12 | 12背阔肌 |
| 13 |肱肌 | 14 | 14肱三头肌|
| 15 | 15比目鱼属 |    |                         |

设备：

|身份证 |设备|
|----|----------------|
| 1 |杠铃|
| 3 |哑铃|
| 4 |健身垫|
| 5 |瑞士球 |
| 6 |引体向上杆|
| 7 |无（体重）|
| 8 |长凳|
| 9 |上斜凳|
| 10 | 10壶铃|

**第 3 步 — 获取并呈现结果：**

````bash
# 按名称搜索练习
查询=“$1”
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")
卷曲-s“https://wger.de/api/v2/exercise/search/?term=${ENCODED}&language=english&format=json”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
对于 data.get('建议',[])[:10] 中的 s：
    d=s.get('数据',{})
    print(f\" ID {d.get('id','?'):>4} | {d.get('name','N/A'):<35} | 类别: {d.get('category','N/A')}\")
”
````

````bash
# 获取特定练习的完整详细信息
EXERCISE_ID="$1"
卷曲-s“https://wger.de/api/v2/exerciseinfo/${EXERCISE_ID}/?format=json”\
  | python3-c“
导入 json、sys、html、re
数据=json.load(sys.stdin)
trans=[t for t in data.get('translations',[]) if t.get('语言')==2]
t=trans[0] if trans else data.get('translations',[{}])[0]
desc=re.sub('<[^>]+>','',html.unescape(t.get('描述','N/A')))
print(f\"练习：{t.get('name','N/A')}\")
print(f\"类别: {data.get('类别',{}).get('名称','N/A')}\")
print(f\"主要：{', '.join(m.get('name_en','') for m in data.get('muscles',[])) 或 'N/A'}\")
print(f\"次要：{', '.join(m.get('name_en','') for m in data.get('muscles_secondary',[])) 或 'none'}\")
print(f\"装备: {', '.join(e.get('name','') for e in data.get('装备',[])) 或 '体重'}\")
print(f\"如何：{desc[:500]}\")
imgs=data.get('图像',[])
if imgs: print(f\"图像: {imgs[0].get('image','')}\")
”
````

````bash
# 列出按肌肉、类别或设备过滤的练习
# 根据需要组合过滤器：?muscles=4&equipment=1&language=2&status=2
FILTER="$1" # 例如“肌肉=4”或“类别=11”或“装备=3”
卷曲-s“https://wger.de/api/v2/exercise/?${FILTER}&语言=2&状态=2&限制=20&格式=json”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
print(f'找到 {data.get(\"count\",0)} 练习。')
对于 data.get('结果',[]) 中的 ex：
    print(f\" ID {ex['id']:>4} | 肌肉: {ex.get('肌肉',[])} | 装备: {ex.get('装备',[])}\")
”
````

### 营养查询（美国农业部食品数据中心）

如果设置，则使用“USDA_API_KEY”环境变量，否则回退到“DEMO_KEY”。
DEMO_KEY = 30 个请求/小时。免费注册密钥 = 1,000 个请求/小时。

````bash
# 按名称搜索食物
食物=“$1”
API_KEY="${USDA_API_KEY:-DEMO_KEY}"
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$FOOD")
卷曲-s“https://api.nal.usda.gov/fdc/v1/foods/search?api_key=${API_KEY}&query=${ENCODED}&pageSize=5&dataType=Foundation,SR%20Legacy”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
食物=data.get('食物',[])
如果不是食物： print('未找到食物。'); sys.exit()
对于食品中的 f：
    n={x[' NutritionName']:x.get('value','?') for x in f.get('foodNutrients',[])}
    cal=n.get('能量','?'); prot=n.get('蛋白质','?')
    fat=n.get('总脂质(脂肪)','?'); carb=n.get('碳水化合物，差异','?')
    print(f\"{f.get('描述','N/A')}\")
    print(f\" 每 100g: {cal} kcal | {prot}g 蛋白质 | {fat}g 脂肪 | {carb}g 碳水化合物\")
    print(f\" FDC ID: {f.get('fdcId','N/A')}\")
    打印（）
”
````

````bash
# 按 FDC ID 列出的详细营养成分
FDC_ID=“$1”
API_KEY="${USDA_API_KEY:-DEMO_KEY}"
卷曲-s“https://api.nal.usda.gov/fdc/v1/food/${FDC_ID}?api_key=${API_KEY}”\
  | python3-c“
导入 json,sys
d=json.load(sys.stdin)
print(f\"食物：{d.get('描述','N/A')}\")
print(f\"{'营养素':<40} {'数量':>8} {'单位'}\")
打印('-'*56)
for x in Sorted(d.get('foodNutrients',[]),key=lambda x:x.get(' Nutrition',{}).get('rank',9999)):
    nut=x.get('营养素',{}); amt=x.get('金额',0)
    如果 amt 且 float(amt)>0：
        print(f\" {nut.get('name',''):<38} {amt:>8} {nut.get('unitName','')}\")
”
````

### 离线计算器

使用“scripts/”中的帮助程序脚本进行批量操作，
或内联运行单个计算：

- `python3 脚本/body_calc.py bmi <体重公斤> <身高厘米>`
- `python3 脚本/body_calc.py tdee <体重公斤> <身高厘米> <年龄> <M|F> <活动 1-5>`
- `python3 脚本/body_calc.py 1rm <权重> <次数>`
- `python3 脚本/body_calc.py 宏 <tdee_kcal> <cut|maintain|bulk>`
-`python3脚本/body_calc.py体脂<M|F><颈厘米><腰厘米>[臀厘米]<身高厘米>`

请参阅“references/FORMULAS.md”了解每个公式背后的科学原理。

---

## 陷阱

- wger 练习端点返回**默认所有语言** — 始终为英语添加 `language=2`
- wger 包括**未经验证的用户提交** - 添加“status=2”以仅获得批准的练习
- USDA `DEMO_KEY` 有 **30 个请求/小时** — 在批量请求之间添加 `sleep 2` 或获取免费密钥
- 美国农业部数据为**每 100 克** — 提醒用户按实际份量调整
- BMI 无法区分肌肉和脂肪 — 肌肉发达的人体重指数高并不一定不健康
- 体脂公式为**估计值** (±3-5%) — 建议使用 DEXA 扫描以确保精确度
- 1RM 公式在超过 10 次重复后会失去准确性 — 使用 3-5 组进行最佳估计
- wger 的“exercise/search”端点使用“term”而不是“query”作为参数名称

---

## 验证

运行运动搜索后：确认结果包括运动名称、肌肉群和设备。
营养查询后：确认每 100 克宏量包含千卡、蛋白质、脂肪、碳水化合物。
计算器之后：健全性检查输出（例如，对于大多数成年人来说，TDEE 应为 1500-3500）。

---

## 快速参考

|任务|来源 |端点 |
|------|--------|----------|
|按名称搜索练习 |沃格尔 | `GET /api/v2/exercise/search/?term=&language=english` |
|锻炼详情|沃格尔 | `GET /api/v2/exerciseinfo/{id}/` |
|按肌肉过滤 |沃格尔 | `GET /api/v2/exercise/?muscles={id}&language=2&status=2` |
|按设备筛选 |沃格尔 | `GET /api/v2/exercise/?equipment={id}&language=2&status=2` |
|列表类别 |沃格尔 | `GET /api/v2/exercisecategory/` |
|列出肌肉 |沃格尔 | `获取 /api/v2/muscle/` |
|搜索食物 |美国农业部 | `GET /fdc/v1/foods/search?query=&dataType=Foundation,SR Legacy` |
|食品详情|美国农业部 | `获取 /fdc/v1/food/{fdcId}` |
| BMI / TDEE / 1RM / 宏 |离线| `python3 脚本/body_calc.py` |