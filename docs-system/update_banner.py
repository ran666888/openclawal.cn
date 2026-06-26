"""Batch update banner links and add UCloud"""
import os, re

BASE = r'C:\Users\50148\projects\openclaw中文社区网站\dist'
DIST_DIR = BASE

UCLOUD_HTML = '\n\n    <span style="font-size:.78rem;color:rgba(252,229,221,.5);margin-left:12px;display:inline-block">企业服务·UCloud <a href="https://passport.ucloud.cn?cps_code=BFkfQaBnaZJGEO75O5x4SY" target="_blank" rel="noreferrer" style="color:#fb923c;text-decoration:underline">了解详情 →</a></span>\n'

old_url = 'https://passport.compshare.cn/register?referral_code=K50gMvv85OmEJ5T9ZDUtDE&ytag=GPU_YY_YX_openclaw.cn'
new_url = 'https://passport.compshare.cn/register?referral_code=HdzDF41Ry3BGN49EFalbN4'

count = 0
ucloud_count = 0

for root, dirs, files in os.walk(DIST_DIR):
    if 'docs_old_bak' in root:
        continue
    for fname in files:
        if not fname.endswith('.html'):
            continue
        path = os.path.join(root, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        
        # Replace old URL with new URL
        if old_url in content:
            content = content.replace(old_url, new_url)
            modified = True
        
        # Add UCloud after the banner link
        # Look for oc-announcement-link that already has the new URL
        if new_url in content and 'ucloud' not in content.lower():
            # Find </a> right after the banner chips
            marker = '立即抢购 &gt;'
            if marker in content:
                idx = content.find(marker)
                end_a = content.find('</a>', idx)
                if end_a > 0:
                    content = content[:end_a] + UCLOUD_HTML + content[end_a:]
                    modified = True
                    ucloud_count += 1
        
        if modified:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1

print(f"修改了 {count} 个文件")
print(f"添加 UCloud 链接: {ucloud_count} 个文件")
