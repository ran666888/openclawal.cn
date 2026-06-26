---
title: "Maps — Geocode, POIs, routes, timezones via OpenStreetMap/OSRM"
sidebar_label: "Maps"
description: "Geocode, POIs, routes, timezones via OpenStreetMap/OSRM"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 地图

通过 OpenStreetMap/OSRM 进行地理编码、POI、路线、时区。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/生产力/地图` |
|版本 | `1.2.0` |
|作者 |米巴伊 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `地图`、`地理编码`、`地点`、`路线`、`距离`、`方向`、`附近`、`位置`、`openstreetmap`、`nominatim`、`立交桥`、`osrm` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 地图技能

使用免费、开放数据源的位置智能。 8 个命令，44 个 POI
类别、零依赖关系（仅限 Python stdlib）、无需 API 密钥。

数据来源：OpenStreetMap/Nominatim、Overpass API、OSRM、TimeAPI.io。

该技能取代了旧的“查找附近”技能——所有“查找附近”的技能
下面的“nearby”命令涵盖了功能，具有相同的功能
`--near "<place>"` 快捷方式和多类别支持。

## 何时使用

- 用户发送 Telegram 位置图钉（消息中的纬度/经度）→“附近”
- 用户想要一个地名的坐标→“搜索”
- 用户有坐标并想要地址 → `reverse`
- 用户询问附近的餐馆、医院、药店、酒店等→“附近”
- 用户想要驾驶/步行/骑自行车的距离或旅行时间→“距离”
- 用户想要两个地点之间的路线导航 → `directions`
- 用户想要某个位置的时区信息 → `timezone`
- 用户想要搜索某个地理区域内的 POI → `area` + `bbox`

## 先决条件

Python 3.8+（仅限 stdlib — 无需安装 pip）。

脚本路径：`~/.hermes/skills/maps/scripts/maps_client.py`

## 命令

````bash
MAPS=~/.hermes/skills/maps/scripts/maps_client.py
````

### 搜索 — 对地名进行地理编码

````bash
python3 $MAPS 搜索“埃菲尔铁塔”
python3 $MAPS 搜索“1600 宾夕法尼亚大道，华盛顿特区”
````

返回：纬度、经度、显示名称、类型、边界框、重要性分数。

### 反向 — 要地址的坐标

````bash
python3 $MAPS 反向 48.8584 2.2945
````

返回：完整地址细分（街道、城市、州、国家、邮政编码）。

### 附近 — 按类别查找地点

````bash
# 通过坐标（例如，来自 Telegram 位置图钉）
python3 $MAPS 附近 48.8584 2.2945 餐厅 --limit 10
python3 $MAPS 附近 40.7128 -74.0060 医院 --radius 2000

# 按地址/城市/邮政编码/地标 — --near auto-geocodes
python3 $MAPS附近--“纽约时代广场”附近--类别咖啡馆
python3 $MAPS附近--“90210”附近--类别药房

# 多个类别合并到一个查询中
python3 $MAPS附近--“奥斯汀市中心”附近--类别餐厅--类别酒吧--limit 10
````

46个类别：餐厅、咖啡馆、酒吧、医院、药房、酒店、宾馆、
营地、超市、自动取款机、加油站、停车场、博物馆、公园、学校、
大学、银行、警察、消防站、图书馆、机场、火车站、
巴士站、教堂、清真寺、犹太教堂、牙医、医生、电影院、剧院、健身房、
游泳池、邮局、便利店、面包店、书店、洗衣房、
洗车、汽车租赁、自行车租赁、出租车、兽医、动物园、游乐场、
体育场、夜总会。

每个结果包括：`name`、`address`、`lat`/`lon`、`distance_m`、
`maps_url`（可点击的 Google 地图链接），`directions_url`（Google 地图
从搜索点出发的方向），以及可用的促销标签 -
“美食”、“营业时间”（营业时间）、“电话”、“网站”。

### distance — 行驶距离和时间

````bash
python3 $MAPS 距离“巴黎”--到“里昂”
python3 $MAPS距离“纽约”--到“波士顿”--模式驾驶
python3 $MAPS距离“大本钟”--到“塔桥”--步行模式
````

模式：驾驶（默认）、步行、骑行。返回道路距离、持续时间、
和直线距离进行比较。

### 路线 — 路线规划导航

````bash
python3 $MAPS 方向“埃菲尔铁塔”--到“卢浮宫博物馆”--步行模式
python3 $MAPS 指示“肯尼迪机场”--到“时代广场”--模式驾驶
````

返回带编号的步骤以及说明、距离、持续时间、道路名称和
机动类型（转弯、出发、到达等）。

### timezone — 坐标时区

````bash
python3 $MAPS 时区 48.8584 2.2945
python3 $MAPS 时区 35.6762 139.6503
````

返回时区名称、UTC 偏移量和当前本地时间。

### area — 某个地点的边界框和区域

````bash
python3 $MAPS 区域“曼哈顿，纽约”
python3 $MAPS 区域“伦敦”
````

返回边界框坐标、宽度/高度（以公里为单位）以及近似面积。
可用作 bbox 命令的输入。

### bbox — 在边界框内搜索

````bash
python3 $MAPS bbox 40.75 -74.00 40.77 -73.98 餐厅 --limit 20
````

查找地理矩形内的 POI。首先使用“area”来获取
指定地点的边界框坐标。

## 使用 Telegram 位置图钉

当用户发送位置图钉时，消息包含“纬度：”和
`经度：` 字段。提取这些并将它们直接传递到“附近”：

````bash
# 用户在 36.17,-115.14 发送了一个 pin 并询问“寻找附近的咖啡馆”
python3 $MAPS 附近 36.17 -115.14 咖啡馆 --radius 1500
````

将结果显示为编号列表，其中包含名称、距离和
`maps_url` 字段，以便用户在聊天中获得点击打开的链接。对于“开
现在？”如有问题，请检查“小时”字段；如果缺失或不清楚，请验证
使用“web_search”，因为 OSM 时间由社区维护，但并不总是如此
当前。

## 工作流程示例

**“查找罗马斗兽场附近的意大利餐厅”：**
1.`附近--“罗马斗兽场”附近--类别餐厅--半径500`
   — 一条命令，自动地理编码

**“他们发送的这个位置图钉附近有什么？”：**
1. 从 Telegram 消息中提取经纬度
2.`附近的LAT LON咖啡馆--半径1500`

**“如何从酒店步行到会议中心？”：**
1.`路线“酒店名称”--到“会议中心”--步行方式`

**“西雅图市中心有哪些餐厅？”：**
1. `区域“西雅图市中心”` → 获取边界框
2.`bbox SW N E餐厅--限30个`

## 陷阱

- Nominatim ToS：最大 1 req/s（由脚本自动处理）
- `nearby` 需要纬度/经度或 `--near "<address>"` — 需要两者之一
- OSRM 路由覆盖范围最适合欧洲和北美
- Overpass API 在高峰时段可能会很慢；脚本自动执行
  在镜像之间回退（overpass-api.de → overpass.kumi.systems）
- `distance` 和 `direction` 使用 `--to` 标志作为目的地（不是位置）
- 如果仅邮政编码在全球范围内给出不明确的结果，请包括国家/州

## 验证

````bash
python3 ~/.hermes/skills/maps/scripts/maps_client.py 搜索“自由女神像”
# 应该返回 lat ~40.689, lon ~-74.044

python3 ~/.hermes/skills/maps/scripts/maps_client.py 附近 --“时代广场”附近 --类别餐厅 --limit 3
# 应返回时代广场约 500m 范围内的餐厅列表
````