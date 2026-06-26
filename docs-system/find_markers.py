"""Find exact marker positions in skills page"""
import os
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')
with open('dist/skills/index_original.html', 'r', encoding='utf-8') as f:
    data = f.read()

print(f'File length: {len(data)}')
print(f'wall found: {"oc-skill-wall" in data} → idx={data.find("oc-skill-wall")}')
print(f'foot found: {"oc-skill-foot" in data} → idx={data.find("oc-skill-foot")}')
print(f'card found: {"oc-skill-card" in data} → count={data.count("oc-skill-card")}')
print(f'end section: {data.rfind("</section>")}')
