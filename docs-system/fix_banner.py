"""Remove banner-hiding from viewer and skills"""
import os
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('docs-system/templates/docs-viewer.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove banner hiding in showDocs
js = js.replace(
    "    var b = document.querySelector('.theme-announcement-bar');\n    if (b) b.style.display = 'none';\n\n    // 高亮\"文档\"按钮",
    "    // 高亮\"文档\"按钮"
)

# Remove banner hiding in skills section
js = js.replace(
    "      var banner = document.querySelector('.theme-announcement-bar');\n      if (banner) banner.style.display = 'none';\n      document.querySelectorAll('.navbar__link').forEach(function(el)",
    "      document.querySelectorAll('.navbar__link').forEach(function(el)"
)

with open('docs-system/templates/docs-viewer.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Done - banner hiding removed")

# Verify
with open('docs-system/templates/docs-viewer.js', 'r') as f:
    check = f.read()
print(f"theme-announcement-bar mentions: {check.count('theme-announcement-bar')}")
