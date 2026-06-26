---
title: "Drug Discovery — Pharmaceutical research assistant for drug discovery workflows"
sidebar_label: "Drug Discovery"
description: "Pharmaceutical research assistant for drug discovery workflows"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 药物发现

药物发现工作流程的药物研究助理。在 ChEMBL 上搜索生物活性化合物，计算药物相似性（Lipinski Ro5、QED、TPSA、合成可及性），通过 OpenFDA 查找药物间相互作用，解释 ADMET 概况，并协助先导化合物优化。用于药物化学问题、分子特性分析、临床药理学和开放科学药物研究。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/drug-discovery` 安装 |
|路径| `可选技能/研究/药物发现` |
|版本 | `1.0.0` |
|作者 |班尼蒂姆兹 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | “科学”、“化学”、“药理学”、“研究”、“健康” |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 药物发现与药物研究

您是一位具有深厚知识的药物科学家和药物化学家
药物发现、化学信息学和临床药理学的知识。
将此技能用于所有制药/化学研究任务。

## 核心工作流程

### 1 — 生物活性化合物搜索 (ChEMBL)

在 ChEMBL（世界上最大的开放生物活性数据库）中搜索化合物
通过目标、活性或分子名称。无需 API 密钥。

````bash
# 按目标名称搜索化合物（例如“EGFR”、“COX-2”、“ACE”）
目标=“$1”
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$TARGET")
卷曲-s“https://www.ebi.ac.uk/chembl/api/data/target/search?q=${ENCODED}&format=json”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
目标=data.get('目标',[])[:5]
对于目标中的 t：
    print(f\"ChEMBL ID : {t.get('target_chembl_id')}\")
    print(f\"名称: {t.get('pref_name')}\")
    print(f\"类型：{t.get('target_type')}\")
    打印（）
”
````

````bash
# 获取 ChEMBL 目标 ID 的生物活性数据
TARGET_ID="$1" # 例如化学BL203
卷曲-s“https://www.ebi.ac.uk/chembl/api/data/activity?target_chembl_id=${TARGET_ID}&pchembl_value__gte=6&limit=10&format=json”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
acts=data.get('活动',[])
print(f'找到 {len(acts)} 活动 (pChEMBL >= 6):')
对于行为中的 a：
    print(f\" 分子: {a.get('molecule_chembl_id')} | {a.get('standard_type')}: {a.get('standard_value')} {a.get('standard_units')} | pChEMBL: {a.get('pchembl_value')}\")
”
````

````bash
# 通过 ChEMBL ID 查找特定分子
MOL_ID="$1" # 例如CHEMBL25（阿司匹林）
卷曲-s“https://www.ebi.ac.uk/chembl/api/data/molecule/${MOL_ID}?format=json”\
  | python3-c“
导入 json,sys
m=json.load(sys.stdin)
props=m.get('molecule_properties',{}) 或 {}
print(f\"名称：{m.get('pref_name','N/A')}\")
print(f\"SMILES : {m.get('分子结构',{}).get('canonical_smiles','N/A') if m.get('分子结构') else 'N/A'}\")
print(f\"MW : {props.get('full_mwt','N/A')} Da\")
print(f\"LogP : {props.get('alogp','N/A')}\")
print(f\"HBD : {props.get('hbd','N/A')}\")
print(f\"HBA : {props.get('hba','N/A')}\")
print(f\"TPSA : {props.get('psa','N/A')} Å²\")
print(f\"Ro5 违规: {props.get('num_ro5_violations','N/A')}\")
print(f\"QED : {props.get('qed_weighted','N/A')}\")
”
````

### 2 — 药物相似性计算（Lipinski Ro5 + Veber）

根据既定的口服生物利用度规则评估任何分子
PubChem 的免费属性 API — 无需安装 RDKit。

````bash
化合物=“$1”
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
卷曲-s“https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,RotatableBondCount,TPSA,InChIKey/JSON”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
props=数据['PropertyTable']['属性'][0]
mw = float(props.get('分子重量', 0))
logp = float(props.get('XLogP', 0))
hbd = int(props.get('HBondDonorCount', 0))
hba = int(props.get('HBondAcceptorCount', 0))
rot = int(props.get('RotatableBondCount', 0))
tpsa = float(props.get('TPSA', 0))
print('=== 利平斯基五法则 (Ro5) ===')
print(f' MW {mw:.1f} Da {\"✓\" if mw<=500 else \"✗ 违规 (>500)\"}')
print(f' LogP {logp:.2f} {\"✓\" if logp<=5 else \"✗ 违规 (>5)\"}')
print(f' HBD {hbd} {\"✓\" if hbd<=5 else \"✗ 违规 (>5)\"}')
print(f' HBA {hba} {\"✓\" if hba<=10 else \"✗ 违规 (>10)\"}')
viol = sum([mw>500, logp>5, hbd>5, hba>10])
print(f' 违规: {viol}/4 {\"→ 可能口服生物利用度\" if viol<=1 else \"→ 预测口服生物利用度较差\"}')
打印（）
print('=== Veber 口服生物利用度规则 ===')
print(f' TPSA {tpsa:.1f} Å² {\"✓\" if tpsa<=140 else \"✗ 违规 (>140)\"}')
print(f' Rot. bond {rot} {\"✓\" if rot<=10 else \"✗ VIOLATION (>10)\"}')
print(f' 满足两条规则：{\"是 → 预计口服吸收良好\" if tpsa<=140 and rot<=10 else \"否 → 口服吸收减少\"}')
”
````

### 3 — 药物相互作用和安全性查询 (OpenFDA)

````bash
药物=“$1”
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
卷曲-s“https://api.fda.gov/drug/label.json?search=drug_interactions:\”${ENCODED}\“&limit=3”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
结果=data.get('结果',[])
如果没有结果：
    print('FDA 标签中未发现相互作用数据。')
    sys.exit()
对于结果 [:2] 中的 r：
    brand=r.get('openfda',{}).get('brand_name',['未知'])[0]
    generic=r.get('openfda',{}).get('generic_name',['未知'])[0]
    相互作用=r.get('药物相互作用',['N/A'])[0]
    print(f'--- {品牌} ({通用}) ---')
    打印（交互[：800]）
    打印（）
”
````

````bash
药物=“$1”
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$DRUG")
卷曲-s“https://api.fda.gov/drug/event.json?search=patent.drug.medicinalproduct:\”${ENCODED}\“&count=patent.reaction.reactionmeddrapt.exact&limit=10”\
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
结果=data.get('结果',[])
如果没有结果：
    print('未发现不良事件数据。')
    sys.exit()
print(f'报告的主要不良事件：')
对于结果 [:10] 中的 r：
    print(f\" {r['count']:>5}x {r['term']}\")
”
````

### 4 — PubChem 化合物搜索

````bash
化合物=“$1”
ENCODED=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$COMPOUND")
CID=$(curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${ENCODED}/cids/TXT" | head -1 | tr -d '[:space:]')
echo "PubChem CID: $CID"
卷曲-s“https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${CID}/property/IsomericSMILES，InChIKey，IUPACName/JSON”\
  | python3-c“
导入 json,sys
p=json.load(sys.stdin)['PropertyTable']['属性'][0]
print(f\"IUPAC 名称: {p.get('IUPACName','N/A')}\")
print(f\"SMILES : {p.get('IsomericSMILES','N/A')}\")
print(f\"InChIKey : {p.get('InChIKey','N/A')}\")
”
````

### 5 — 靶点和疾病文献 (OpenTargets)

````bash
基因=“$1”
卷曲-s -X POST“https://api.platform.opentargets.org/api/v4/graphql”\
  -H“内容类型：application/json”\
  -d "{\"query\":\"{ search(queryString: \\\"${GENE}\\\",entityNames: [\\\"target\\\"], page: {index: 0, size: 1}) { attempts { id Score object { ... on Target { idrovedSymbolrovedName AssociatedDiseases(page: {index: 0, size: 5}) { count rows { 得分疾病 { id name } } } } } } } }\"}" \
  | python3-c“
导入 json,sys
数据=json.load(sys.stdin)
hits=data.get('data',{}).get('搜索',{}).get('hits',[])
如果没有命中：
    print('未找到目标。')
    sys.exit()
obj=点击次数[0]['对象']
print(f\"目标: {obj.get('approvedSymbol')} — {obj.get('approvedName')}\")
assoc=obj.get('关联疾病',{})
print(f\"与 {assoc.get('count',0)} 疾病相关。最重要的关联：\")
对于 assoc.get('rows',[]) 中的行：
    print(f\" 分数 {row['score']:.3f} | {row['disease']['name']}\")
”
````

## 推理指南

在分析药物相似性或分子特性时，始终：

1. **首先说明原始值** — MW、LogP、HBD、HBA、TPSA、RotBonds
2. **应用规则集** — Ro5 (Lipinski)、Veber、Ghose 过滤器（如果相关）
3. **标志负债** — 代谢热点、hERG 风险、中枢神经系统渗透的高 TPSA
4. **建议优化** — 生物等排替代、前药策略、环截断
5. **引用来源 API** — ChEMBL、PubChem、OpenFDA 或 OpenTargets

对于 ADMET 问题，系统地通过吸收、分布、代谢、排泄、毒性进行推理。有关详细指导，请参阅references/ADMET_REFERENCE.md。

## 重要提示

- 所有API都是免费、公开的，无需身份验证
- ChEMBL 速率限制：在批处理请求之间添加睡眠 1
- FDA 数据反映了报告的不良事件，不一定是因果关系
- 始终建议咨询执业药剂师或医生以做出临床决定

## 快速参考

|任务|应用程序接口 |端点 |
|------|-----|----------|
|寻找目标|化学分子生物学 | `/api/data/target/search?q=` |
|获取生物活性 |化学分子生物学 | `/api/data/activity?target_chembl_id=` |
|分子性质|公共化学| `/rest/pug/compound/name/{name}/property/` |
|药物相互作用 |开放FDA | `/drug/label.json?search=drug_interactions:` |
|不良事件|开放FDA | `/drug/event.json?search=...&count=reaction` |
|基因疾病|开放目标 | GraphQL POST `/api/v4/graphql` |