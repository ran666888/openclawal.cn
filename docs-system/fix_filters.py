"""Fix filter buttons on skills page"""
import os
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/skills/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# New categories in order
new_cats = [
    ('全部', 62),
    ('开发工具', 13),
    ('GitHub', 2),
    ('笔记与知识', 5),
    ('日常工具', 11),
    ('密码与安全', 2),
    ('媒体与创意', 11),
    ('通信与消息', 6),
    ('邮件与文档', 2),
    ('MCP 与集成', 2),
    ('智能硬件', 4),
    ('扩展技能', 5),
]

# Build new filter bar HTML
filters_html = '<div class="oc-skill-filters" role="tablist" aria-label="按分类筛选">'
filters_html += f'<button type="button" role="tab" aria-selected="true" class="oc-skill-filter is-active">全部 <span>{62}</span></button>'
for cat, cnt in new_cats[1:]:
    filters_html += f'<button type="button" role="tab" aria-selected="false" class="oc-skill-filter">{cat} <span>{cnt}</span></button>'
filters_html += '</div></header>'

# Find old filter section
old_marker = 'class="oc-skill-filters"'
idx = html.find(old_marker)
if idx > 0:
    end_idx = html.find('</div></header>', idx)
    if end_idx > idx:
        old = html[idx:end_idx + len('</div></header>')]
        html = html.replace(old, filters_html)
        print(f"✅ Filters replaced")

# Also update the heading text
html = html.replace(
    '好用的 Skill 去哪找?',
    'OpenClaw Skill Atlas'
)

html = html.replace(
    'OpenClaw 出厂自带 62 个 Skill，覆盖开发工具、日常效率、媒体处理、AI 集成等场景。点击分类筛选，或往下翻查看全部。',
    'OpenClaw 出厂自带 62 个 Skill，覆盖开发工具、日常效率、媒体处理、AI 集成等场景。点击分类筛选快速定位。'
)

with open('dist/skills/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
with open('dist/skills/index.html', 'r', encoding='utf-8') as f2:
    verify = f2.read()
    
import re
filters = re.findall(r'oc-skill-filter">([^<]+)', verify)
print(f"Filter buttons: {len(filters)}")
for f in filters:
    print(f"  {f}")
    
# Check no old categories remain
old_cats = ['Apple 系统', '自主 Agent', '创意设计', 'DevOps', 'Dogfood', 
            '游戏', 'Inference.sh', 'MLOps', '红队', '智能家居', '效率工具']
for oc in old_cats:
    if oc in verify:
        print(f"⚠️  Still has: {oc}")
