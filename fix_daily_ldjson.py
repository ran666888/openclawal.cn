#!/usr/bin/env python3
"""Fix broken JSON-LD in dist/daily/index.html"""
import re, json

path = r'C:\Users\50148\oc-site\dist\daily\index.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the ld+json block
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
old_json = m.group(1)

# Build clean @graph
clean_graph = [
    {
        "@type": "Organization",
        "@id": "https://openclawal.cn/#organization",
        "name": "OpenClaw 中文社区",
        "url": "https://openclawal.cn/",
        "logo": "https://openclawal.cn/img/logo.png",
        "sameAs": ["https://github.com/openclaw/openclaw", "https://discord.gg/NousResearch"]
    },
    {
        "@type": "WebSite",
        "@id": "https://openclawal.cn/#website",
        "name": "OpenClaw 中文社区",
        "url": "https://openclawal.cn/",
        "inLanguage": "zh-CN",
        "description": "OpenClaw 中文文档、安装教程、使用指南与社区入口，覆盖长期记忆、Skills、MCP、消息网关和多平台接入。",
        "publisher": {"@id": "https://openclawal.cn/#organization"}
    },
    {
        "@id": "https://openclawal.cn/daily#webpage",
        "@type": "CollectionPage",
        "name": "OpenClaw 中文社区日报",
        "url": "https://openclawal.cn/daily",
        "description": "OpenClaw 中文社区日报归档：每日 AI 前沿资讯、微信群精选观察与工程实践汇总。",
        "inLanguage": "zh-CN",
        "isPartOf": {"@id": "https://openclawal.cn/#website"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": "https://openclawal.cn/img/openclaw-og.svg"}
    },
    {
        "@id": "https://openclawal.cn/daily#breadcrumbs",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "首页", "item": "https://openclawal.cn/"},
            {"@type": "ListItem", "position": 2, "name": "日报", "item": "https://openclawal.cn/daily"},
            {"@type": "ListItem", "position": 3, "name": "OpenClaw 中文社区日报 7月1日", "item": "https://openclawal.cn/daily/2026-07-01"}
        ]
    },
]

# Try to extract the ItemList from old JSON
itemlist_start = old_json.find('"@type":"ItemList"')
if itemlist_start > 0:
    brace_start = old_json.rfind('{', 0, itemlist_start)
    depth = 0
    end_pos = brace_start
    for i in range(brace_start, len(old_json)):
        if old_json[i] == '{':
            depth += 1
        elif old_json[i] == '}':
            depth -= 1
        if depth == 0:
            end_pos = i + 1
            break
    itemlist_str = old_json[brace_start:end_pos]
    try:
        itemlist = json.loads(itemlist_str)
        print(f"ItemList parsed: {len(itemlist.get('itemListElement', []))} items")
        clean_graph.append(itemlist)
    except json.JSONDecodeError as e:
        print(f"ItemList parse failed: {e}")
        clean_graph.append({
            "@type": "ItemList",
            "@id": "https://openclawal.cn/daily#archive",
            "name": "OpenClaw 中文社区日报归档",
            "itemListOrder": "https://schema.org/ItemListOrderDescending",
            "numberOfItems": 45
        })

new_ld = json.dumps({"@context": "https://schema.org", "@graph": clean_graph}, ensure_ascii=False)
new_tag = f'<script type="application/ld+json">{new_ld}</script>'

content = content.replace(m.group(0), new_tag)

# Verify
vm = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
try:
    j = json.loads(vm.group(1))
    items = j.get("@graph", [])
    print(f"✅ VALID JSON-LD ({len(items)} graph items)")
    for item in items:
        if item.get("@type") == "BreadcrumbList":
            bc = item.get("itemListElement", [])
            print(f"  BreadcrumbList: {len(bc)} items")
            for b in bc:
                print(f"    #{b['position']}: {b['name']} -> {b.get('item','')}")
        if item.get("@type") == "ItemList":
            il = item.get("itemListElement", [])
            print(f"  ItemList: {len(il)} items")
except json.JSONDecodeError as e:
    print(f"❌ STILL INVALID: {e}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ Written!")
