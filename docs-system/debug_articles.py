"""Debug article paths"""
import json, os
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')
with open('dist/docs-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

keys = list(articles.keys())
print(f"总文章数: {len(keys)}")
print(f"\n前5个 key:")
for k in keys[:5]:
    print(f"  repr: {repr(k)}")

print(f"\n检查关键路径:")
checks = [
    "/docs/getting-started/installation/",
    "/docs/user-guide/features/tools/",
    "/docs/openclaw/clawhub/",
    "/docs/user-guide/messaging/telegram/",
]
for p in checks:
    found = False
    for k in keys:
        # Normalize both for comparison
        knorm = k.replace('\\', '/')
        if knorm == p:
            found = True
            break
    print(f"  {p}: {'✅' if found else '❌'}")
    if not found:
        # Find similar
        for k in keys:
            if p.split('/')[-2] in k:
                print(f"    类似: {repr(k[:80])}")
