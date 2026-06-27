import os
import re

dist = r'C:\Users\50148\projects\openclaw中文社区网站\dist'
script_tag = '<script defer src="/assets/js/mobile-nav.js"></script>'
count = 0

for root, dirs, files in os.walk(dist):
    for f in files:
        if not f.endswith('.html'):
            continue
        path = os.path.join(root, f)
        try:
            with open(path, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            try:
                with open(path, 'r', encoding='gbk') as fh:
                    content = fh.read()
            except:
                continue
        
        # Check if already injected
        if 'mobile-nav.js' in content:
            continue
        
        # Inject before </body>
        new_content = content.replace('</body>', script_tag + '</body>', 1)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            count += 1
            if count <= 5:
                print(f'  [{count}] {path[len(dist):]}')

print(f'\nDone: {count} files updated')
