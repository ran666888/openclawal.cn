#!/usr/bin/env python3
"""Enhance homepage JSON-LD: add SearchAction + SiteNavigationElement"""
import re, json

with open('/c/Users/50148/projects/openclaw中文社区网站/dist/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find first JSON-LD block
pattern = r'(<script type="application/ld\+json">)(.*?)(</script>)'
def enhance_ldjson(match):
    prefix = match.group(1)
    raw = match.group(2)
    suffix = match.group(3)
    
    try:
        data = json.loads(raw)
    except:
        return match.group(0)
    
    if '@graph' not in data:
        return match.group(0)
    
    graph = data['@graph']
    
    # 1. Add SearchAction to WebSite entry
    for item in graph:
        if item.get('@type') == 'WebSite':
            item['potentialAction'] = {
                "@type": "SearchAction",
                "target": {
                    "@type": "EntryPoint",
                    "urlTemplate": "https://openclawal.cn/search?q={search_term_string}"
                },
                "query-input": "required name=search_term_string"
            }
            break
    
    # 2. Add SiteNavigationElement (critical for Sitelinks)
    nav_entry = {
        "@id": "https://openclawal.cn/#sitenavigation",
        "@type": "SiteNavigationElement",
        "name": "主导航",
        "description": "OpenClaw 中文社区网站导航",
        "hasPart": [
            {"@type": "SiteNavigationElement", "name": "安装教程", "url": "https://openclawal.cn/openclaw-installation/"},
            {"@type": "SiteNavigationElement", "name": "文档", "url": "https://openclawal.cn/docs-index.html"},
            {"@type": "SiteNavigationElement", "name": "技能", "url": "https://openclawal.cn/skills/"},
            {"@type": "SiteNavigationElement", "name": "生态系统", "url": "https://openclawal.cn/practice-guides/"},
            {"@type": "SiteNavigationElement", "name": "社区", "url": "https://openclawal.cn/community/"},
            {"@type": "SiteNavigationElement", "name": "日报", "url": "https://openclawal.cn/daily/"},
            {"@type": "SiteNavigationElement", "name": "消息网关", "url": "https://openclawal.cn/openclaw-messaging/"},
            {"@type": "SiteNavigationElement", "name": "MCP", "url": "https://openclawal.cn/openclaw-mcp/"},
            {"@type": "SiteNavigationElement", "name": "关于", "url": "https://openclawal.cn/about/"}
        ]
    }
    graph.append(nav_entry)
    
    new_raw = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return prefix + new_raw + suffix

new_content = re.sub(pattern, enhance_ldjson, content, count=1)

with open('/c/Users/50148/projects/openclaw中文社区网站/dist/index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ JSON-LD enhanced: SearchAction + SiteNavigationElement added")
