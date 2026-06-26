"""Normalize article paths to use forward slashes"""
import json, os
os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/docs-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# Count backslash keys
bs_keys = [k for k in articles if '\\' in k]
print(f"含反斜杠的 key: {len(bs_keys)}")
for k in bs_keys[:5]:
    print(f"  {repr(k)}")

# Normalize: replace all backslashes with forward slashes
normalized = {}
for k, v in articles.items():
    new_k = k.replace('\\', '/')
    normalized[new_k] = v

# Write back
with open('dist/docs-articles.json', 'w', encoding='utf-8') as f:
    json.dump(normalized, f, ensure_ascii=False)

print(f"\n已修复 {len(bs_keys)} 个路径")
print(f"总文章数: {len(normalized)}")

# Verify
with open('dist/docs-articles.json', 'r', encoding='utf-8') as f:
    verify = json.load(f)
bs_left = [k for k in verify if '\\' in k]
print(f"剩余反斜杠: {len(bs_left)}")
