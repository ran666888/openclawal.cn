"""Extract and inject announcement banner"""
import os, re
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')
with open('dist/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find banner
start = html.find('theme-announcement-bar')
before = html.rfind('>', start-200, start)
end = html.find('</nav>', start)
banner = html[before+1:end]
# Clean up - keep only the banner div and its content
banner = banner[:banner.find('</div></div><nav')]
print("Banner extracted:", len(banner), "chars")
print(banner[:200])
