import re

path = r'C:\Users\50148\projects\openclaw中文社区网站\dist\assets\js\docs-viewer.js'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find lines 333-337 and replace with correct 2 lines
lines = content.split('\n')

# Show lines 331-339
print("BEFORE:")
for i in range(330, min(339, len(lines))):
    print(f'  L{i+1}: {repr(lines[i])}')

# Lines 333-337 (indices 332-336) are broken
# Replace with the correct JS code
# In the file, we want: scm[1].replace(/\n/g,"\\n").replace(/\r/g,"\\r");
# So regex \n (backslash+n in the file) and string "\\n" (backslash+backslash+n in the file)

correct_lines = [
    '          var jsonStr = scm[1].replace(/\\n/g,"\\\\n").replace(/\\r/g,"\\\\r");',
]

# Check what we currently have as the broken block (indices 332-336 combined)
broken_combined = '\n'.join(lines[332:337])

# What we want instead
# We replace 5 broken lines with 2 correct lines
new_block = correct_lines[0] + '\n' + lines[336]  # Keep 'var mdText = JSON.parse(jsonStr);' from line 337 (index 336)

# Replace
content_before = content
content = content.replace(broken_combined, new_block, 1)

# Also remove any duplicate JSON.parse line
lines_after = content.split('\n')
seen_parse = False
for i, line in enumerate(lines_after):
    if 'var mdText = JSON.parse(jsonStr);' in line:
        if seen_parse:
            lines_after[i] = ''
            print(f'Removed duplicate at line {i+1}')
        else:
            seen_parse = True

content = '\n'.join(lines_after)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open(path, 'r', encoding='utf-8') as f:
    verify_lines = f.readlines()

print("\nAFTER:")
for i in range(330, min(339, len(verify_lines))):
    print(f'  L{i+1}: {repr(verify_lines[i].rstrip())}')

# Check JS syntax
print("\nSyntax check:")
