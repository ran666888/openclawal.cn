#!/usr/bin/env python3
"""Fix the body background issue in docs-viewer.js"""
from pathlib import Path

p = Path('/c/Users/50148/projects/openclaw中文社区网站/dist/assets/js/docs-viewer.js')
content = p.read_text(encoding='utf-8')

old = "    // \u4fee\u590d: \u5b98\u7f51 CSS \u6539\u4e86 :root {--bg} \u548c body {background}, \u628a\u5168\u9875\u80cc\u666f\u53d8\u9ed1\u4e86\n    var style = document.createElement('style');\n    style.id = 'oc-docs-body-fix';\n    style.textContent = ':root{--bg:#07070d!important}#oc-docs-viewer{background:#0d0b0b!important}#oc-docs-viewer .tabs{position:sticky;top:52px;z-index:60}';\n    document.head.appendChild(style);"

new = "    // Fix: restore page bg, keep docs viewer dark\n    var style = document.createElement('style');\n    style.id = 'oc-docs-body-fix';\n    style.textContent = ':root{--bg:#111!important}#oc-docs-viewer{--bg:#0d0b0b}#oc-docs-viewer .tabs{position:sticky;top:52px;z-index:60}';\n    document.head.appendChild(style);"

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed: root bg restored, docs viewer keeps dark bg')
else:
    print('Old string not found, trying search...')
    if 'oc-docs-body-fix' in content:
        print('Found oc-docs-body-fix in content')
        # Find the exact block and print it
        idx = content.find('oc-docs-body-fix')
        print(content[idx-50:idx+200])
