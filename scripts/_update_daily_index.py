"""
Update openclawal.cn daily index page to include 2026-06-28.
1. Create dist/daily/2026-06-28/index.html
2. Update dist/daily/index.html (calendar, chips, JSON-LD, main content)
"""
import os, re, shutil

BASE = "C:/Users/50148/projects/openclaw中文社区网站"
DAILY_INDEX = os.path.join(BASE, "dist/daily/index.html")
JUNE22_DIR = os.path.join(BASE, "dist/daily/2026-06-22")
JUNE28_DIR = os.path.join(BASE, "dist/daily/2026-06-28")

# ── Step 1: Create 2026-06-28 page ──
print("=== Step 1: Creating dist/daily/2026-06-28/index.html ===")
if not os.path.exists(JUNE22_DIR):
    print(f"ERROR: {JUNE22_DIR} not found!")
    exit(1)

os.makedirs(JUNE28_DIR, exist_ok=True)

with open(os.path.join(JUNE22_DIR, "index.html"), "r", encoding="utf-8") as f:
    html_28 = f.read()

# Replace date-specific content
html_28 = html_28.replace("2026-06-22", "2026-06-28")
html_28 = html_28.replace("6月22日", "6月28日")
html_28 = html_28.replace("6月22日日报", "6月28日日报")
# Fix title - only the specific page title
html_28 = html_28.replace(
    'title>OpenClaw 中文社区日报 6月28日 | OpenClaw 中文社区',
    'title>OpenClaw 中文社区日报 6月28日 | OpenClaw 中文社区'
)
# Update OG image URL
html_28 = html_28.replace("/reports/daily/2026-06-22.png", "/reports/daily/2026-06-28.png")
# Update canonical URL
html_28 = re.sub(r'canonical[^>]+href="[^"]+"', 'link rel="canonical" href="https://openclawal.cn/daily/2026-06-28"', html_28, count=1)
# Update iframe src  
html_28 = html_28.replace('src="/reports/daily/2026-06-22.html', 'src="/reports/daily/2026-06-28.html')
# Update download PNG link
html_28 = html_28.replace("/reports/daily/2026-06-22.png", "/reports/daily/2026-06-28.png")

# Fix the JSON-LD published date
html_28 = re.sub(r'"datePublished": "[^"]*"', '"datePublished": "2026-06-28T09:00:00+08:00"', html_28)
html_28 = re.sub(r'"dateModified": "[^"]*"', '"dateModified": "2026-06-28T18:00:00+08:00"', html_28)

# Update keywords
html_28 = html_28.replace('OpenClaw 6月22日日报', 'OpenClaw 6月28日日报')
html_28 = html_28.replace('OpenClaw 中文社区日报 6月22日', 'OpenClaw 中文社区日报 6月28日')

# Update the download filename
html_28 = re.sub(
    r'download="[^"]*"',
    'download="openclaw-agent-daily-2026-06-28.png"',
    html_28
)

with open(os.path.join(JUNE28_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_28)
print("✅ dist/daily/2026-06-28/index.html created")

# ── Step 2: Update dist/daily/index.html ──
print("\n=== Step 2: Updating dist/daily/index.html ===")

with open(DAILY_INDEX, "r", encoding="utf-8") as f:
    html = f.read()

# 2a. Update "已归档 42 期" → "已归档 43 期"
html = html.replace("已归档 <strong>42</strong> 期 · 最近更新 <strong>6月22日</strong>",
                     "已归档 <strong>43</strong> 期 · 最近更新 <strong>6月28日</strong>")

# 2b. JSON-LD: numberOfItems 42 → 43
html = html.replace('"numberOfItems":42', '"numberOfItems":43')

# 2c. JSON-LD: shift positions, add June 28 as position 1
# Find the itemListElement array pattern
# Current: "position":1,"url":"https://openclawal.cn/daily/2026-06-22"
# Need to: add June 28 as new position 1, shift all others by 1
old_json_item = '"position":1,"url":"https://openclawal.cn/daily/2026-06-22","name":"OpenClaw 中文社区日报 6月22日"'
new_json_item = '"position":1,"url":"https://openclawal.cn/daily/2026-06-28","name":"OpenClaw 中文社区日报 6月28日"'
html = html.replace(old_json_item, new_json_item)

# Update position 2 (was 1 pos 1)
# The old position 1 is now position 2 (June 22)
# Find: "position":2,"url":"https://openclawal.cn/daily/2026-06-18"
# The June 22 was pos 1, now it moves elsewhere in the list
# Actually I need to insert a new element at position 1 and update all positions

# Let me find the itemListElement pattern and reconstruct it
match = re.search(r'"itemListElement":\[(.*?)\]', html, re.DOTALL)
if match:
    items_str = match.group(1)
    # Parse existing items by position
    items = re.findall(r'\{([^}]+)\}', items_str)
    print(f"Found {len(items)} items in JSON-LD")
    
    # Shift all positions by 1 (add 1 to each)
    new_items = []
    new_items.append('"position":1,"url":"https://openclawal.cn/daily/2026-06-28","name":"OpenClaw 中文社区日报 6月28日"')
    
    for item in items:
        # Extract the position number
        pos_match = re.search(r'"position":(\d+)', item)
        if pos_match:
            old_pos = int(pos_match.group(1))
            new_pos = old_pos + 1
            # Replace the position
            new_item = item.replace(f'"position":{old_pos}', f'"position":{new_pos}')
            new_items.append(new_item)
    
    new_items_str = ",".join(new_items)
    html = html.replace(f'"itemListElement":[{items_str}]', f'"itemListElement":[{new_items_str}]')
    print("✅ JSON-LD itemListElement updated")

# 2d. Calendar: change June 28 from disabled to active
# Old: buttons for June 28
# Find the 28th day button pattern
old_day_28 = re.search(
    r'<button[^>]*aria-label="2026-06-28 无日报"[^>]*>28</button>',
    html
)
if old_day_28:
    new_day_28 = '<button type="button" class="oc-daily-cal__day oc-daily-cal__day--has" title="" aria-label="查看 2026-06-28 的日报">28</button>'
    html = html.replace(old_day_28.group(0), new_day_28)
    print("✅ Calendar: June 28 enabled")

# 2e. Add the recent chip for June 28 as the FIRST chip
# The chips are in order: 6-22, 6-18, 6-17, 6-16, 6-15...
# I need to insert 6-28 before 6-22
chip_6_22 = re.search(
    r'<button type="button" class="oc-daily-chip oc-daily-chip--on" aria-pressed="true"><span class="oc-daily-chip__m">6<!-- -->月</span><span class="oc-daily-chip__d">22</span></button>',
    html
)
if chip_6_22:
    new_chip_6_28 = '<button type="button" class="oc-daily-chip oc-daily-chip--on" aria-pressed="true"><span class="oc-daily-chip__m">6<!-- -->月</span><span class="oc-daily-chip__d">28</span></button>'
    html = html.replace(chip_6_22.group(0), new_chip_6_28)
    
    # Also need to add 6-22 as the second chip
    chip_6_18 = re.search(
        r'<button type="button" class="oc-daily-chip" aria-pressed="false"><span class="oc-daily-chip__m">6<!-- -->月</span><span class="oc-daily-chip__d">18</span></button>',
        html
    )
    if chip_6_18:
        new_chip_6_22 = '<button type="button" class="oc-daily-chip" aria-pressed="false"><span class="oc-daily-chip__m">6<!-- -->月</span><span class="oc-daily-chip__d">22</span></button>\n<button type="button" class="oc-daily-chip" aria-pressed="false"><span class="oc-daily-chip__m">6<!-- -->月</span><span class="oc-daily-chip__d">18</span></button>'
        html = html.replace(chip_6_18.group(0), new_chip_6_22)
    print("✅ Recent chips updated")

# 2f. Update the "最近" sidebar navigation
# Old: <a href="/daily/2026-06-22" class="oc-daily-recent__item oc-daily-recent__item--on">6月22日 · 周一</a>
# Need to add 6-28 as first item
old_recent_6_22 = re.search(
    r'<a href="/daily/2026-06-22"[^>]*class="oc-daily-recent__item oc-daily-recent__item--on"[^>]*><span class="oc-daily-recent__label">6月22日 · 周一</span></a>',
    html
)
if old_recent_6_22:
    new_recent_6_28 = f'<a href="/daily/2026-06-28" class="oc-daily-recent__item oc-daily-recent__item--on"><span class="oc-daily-recent__label">6月28日 · 周日</span></a>'
    html = html.replace(old_recent_6_22.group(0), new_recent_6_28)
    
    # Add 6-22 as second
    old_recent_6_18 = re.search(
        r'<a href="/daily/2026-06-18"[^>]*class="oc-daily-recent__item"[^>]*><span class="oc-daily-recent__label">6月18日 · 周四</span></a>',
        html
    )
    if old_recent_6_18:
        new_recent_6_22 = f'<a href="/daily/2026-06-22" class="oc-daily-recent__item"><span class="oc-daily-recent__label">6月22日 · 周一</span></a><a href="/daily/2026-06-18" class="oc-daily-recent__item"><span class="oc-daily-recent__label">6月18日 · 周四</span></a>'
        html = html.replace(old_recent_6_18.group(0), new_recent_6_22)
    print("✅ Recent sidebar updated")

# 2g. Update main content section - date pill, title, iframe
html = html.replace('2026-06-22 · 周一', '2026-06-28 · 周日')
html = html.replace('OpenClaw 中文社区日报 6月22日', 'OpenClaw 中文社区日报 6月28日')
html = html.replace('每天 1 分钟，了解 AI Agent 最新资讯。', '每天 1 分钟，了解 AI Agent 最新资讯。')

# Update iframe to point to 6-28 report
html = html.replace('src="/reports/daily/2026-06-22.html', 'src="/reports/daily/2026-06-28.html')

# Update download PNG
html = html.replace('/reports/daily/2026-06-22.png', '/reports/daily/2026-06-28.png')

# Update JSON-LD for the main page (dailypage feed)
html = html.replace(
    '"position":1,"url":"https://openclawal.cn/daily/2026-06-22"',
    '"position":1,"url":"https://openclawal.cn/daily/2026-06-28"'
)
html = html.replace(
    '"name":"OpenClaw 中文社区日报 6月22日"',
    '"name":"OpenClaw 中文社区日报 6月28日"'
)

# Update NEXT/PREV buttons - disable "后一期"
html = html.replace(
    '<button type="button" disabled="">后一期',
    '<button type="button" disabled="">后一期'
)

# Update the "下一期" button (currently disabled for 6-22 which was the latest)
# For 6-28, it's the latest so "后一期" stays disabled
# But "前一期" should work (point to 6-22)
html = html.replace(
    'aria-label="前一期">前一期',
    'aria-label="前一期">前一期'
)

# Update the calendar active day
html = html.replace(
    'oc-daily-cal__day--active" title="" aria-label="查看 2026-06-22 的日报">22',
    'oc-daily-cal__day--active" title="" aria-label="查看 2026-06-28 的日报">28'
)

print("✅ Main content updated")

# ── Write ──
with open(DAILY_INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print("✅ dist/daily/index.html saved")
print("\nDone! Run git commit + push to deploy.")
