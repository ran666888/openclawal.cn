import os
import re

dist = r'C:\Users\50148\oc-site\dist'
script = '<script defer src="/_vercel/insights/script.js"></script>'

count = 0
skipped = 0
for root, dirs, files in os.walk(dist):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8', errors='ignore') as fh:
            content = fh.read()
        
        if '/_vercel/insights/script.js' in content:
            skipped += 1
            print(f"SKIP (already has): {path}")
            continue
        
        # Insert after <head> or before </head>
        new_content = re.sub(
            r'(</head>)',
            f'  {script}\n\\1',
            content,
            count=1
        )
        
        if new_content == content:
            skipped += 1
            print(f"SKIP (no </head>): {path}")
            continue
        
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        count += 1
        print(f"OK: {path}")

print(f"\nDone: {count} files injected, {skipped} skipped")
