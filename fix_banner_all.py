#!/usr/bin/env python3
"""Apply banner fix (enterprise section moved to right) to all HTML files."""

import os
import glob

DIST = r'C:\Users\50148\projects\openclaw中文社区网站\dist'

# Files to exclude (already fixed or backups)
exclude = [
    '/forum/',        # already fixed
    '/docs_old_bak/', # old backup
    '/daily/2026-',   # historical dailies
]

# Files to include (main pages + zh-Hant)
files = []
for root, dirs, fnames in os.walk(DIST):
    # Skip excluded paths
    skip = False
    for ex in exclude:
        if ex in root:
            skip = True
            break
    if skip:
        continue
    
    for fname in fnames:
        if fname.endswith('.html'):
            fpath = os.path.join(root, fname)
            files.append(fpath)

files.sort()
print(f"Found {len(files)} HTML files to check")

# The old enterprise span line (with margin-left:12px)
old_enterprise_span = (
    '<span style="font-size:.78rem;color:rgba(255,230,203,.5);'
    'margin-left:12px;display:inline-block">'
    '企业服务·UCloud '
    '<a href="https://passport.ucloud.cn?cps_code=BFkfQaBnaZJGEO75O5x4SY"'
    ' target="_blank" rel="noreferrer" style="color:#ffd700;text-decoration:underline">'
    '了解详情 →</a></span>'
)

new_enterprise_span = old_enterprise_span.replace('margin-left:12px', 'margin-left:auto')

old_slide_div = '<div class="oc-announcement-slide">'
new_slide_div = '<div class="oc-announcement-slide" style="display:flex;flex-direction:row;align-items:center">'

count_modified = 0

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Add style to slide div
    content = content.replace(old_slide_div, new_slide_div)
    
    # 2. Change margin-left:12px to margin-left:auto
    content = content.replace(old_enterprise_span, new_enterprise_span)
    
    # 3. Move </a> from after enterprise span to after chips span
    # Old: ...</span>\n    \n\n    <span ...企业服务...</span>\n</a>\n</div>
    # New: ...</span>\n    </a>\n\n    <span ...企业服务...</span>\n</div>
    
    # The unique marker: the chips closing </span> followed by whitespace then enterprise span
    old_tail = (
        '      </span>\n    \n\n    <span style="font-size:.78rem;'
        'color:rgba(255,230,203,.5);margin-left:auto;display:inline-block">'
        '企业服务·UCloud '
        '<a href="https://passport.ucloud.cn?cps_code=BFkfQaBnaZJGEO75O5x4SY"'
        ' target="_blank" rel="noreferrer" style="color:#ffd700;text-decoration:underline">'
        '了解详情 →</a></span>\n</a>\n</div>'
    )
    new_tail = (
        '      </span>\n    </a>\n\n    <span style="font-size:.78rem;'
        'color:rgba(255,230,203,.5);margin-left:auto;display:inline-block">'
        '企业服务·UCloud '
        '<a href="https://passport.ucloud.cn?cps_code=BFkfQaBnaZJGEO75O5x4SY"'
        ' target="_blank" rel="noreferrer" style="color:#ffd700;text-decoration:underline">'
        '了解详情 →</a></span>\n</div>'
    )
    
    content = content.replace(old_tail, new_tail)
    
    if content != original:
        count_modified += 1
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✅ Fixed: {fpath[len(DIST)+1:]}")
    else:
        # Check if already had the fix
        if 'style="display:flex;flex-direction:row;align-items:center"' in content:
            print(f"  ⏭️ Already fixed: {fpath[len(DIST)+1:]}")
        else:
            print(f"  ❌ No match: {fpath[len(DIST)+1:]}")

print(f"\nDone! Modified {count_modified} files.")
