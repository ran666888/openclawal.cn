import json, os
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')
with open('dist/docs-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Fix 1: labels
old_new = {
    "在 Hermes 中使用 MCP": "MCP 使用指南",
    "使用 SOUL.md": "SOUL.md 使用指南",
    "使用语音模式": "语音模式使用指南",
    "使用 Cron 自动化": "Cron 自动化指南",
    "使用技能": "技能使用指南",
    "委托与并行工作": "委托与并行指南",
    "设置团队 Telegram 助手": "Telegram 团队助手",
    "技巧与最佳实践": "使用技巧",
}

def fix(item):
    if item['type'] == 'link' and item.get('label') in old_new:
        item['label'] = old_new[item['label']]
    if item['type'] == 'category' and 'items' in item:
        for s in item['items']:
            fix(s)

for item in config:
    fix(item)

# Fix 2: releases
for item in config:
    if item.get('label') == '版本发布' and item['type'] == 'category':
        keep = []
        for v in item['items']:
            l = v.get('label','')
            if l in ('v2026.6.10','v2026.6.9','v2026.6.8','v2026.6.7 Beta.1','v2026.6.6','v2026.6.5'):
                keep.append(v)
        item['items'] = keep

# Fix 3: guides
for item in config:
    if item.get('label') == '指南与教程':
        keep = ['MCP 使用指南','SOUL.md 使用指南','语音模式使用指南','Cron 自动化指南','技能使用指南','委托与并行指南','Telegram 团队助手','使用技巧']
        item['items'] = [i for i in item['items'] if i.get('label') in keep]

with open('dist/docs-config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

def count(items):
    c,p=0,0
    for i in items:
        if i['type']=='category':
            c+=1
            cc,pp=count(i.get('items',[]))
            c+=cc;p+=pp
        else:
            p+=1
    return c,p
c,p=count(config)
print(f'✅ 完成: 分类={c}, 页面={p}')
