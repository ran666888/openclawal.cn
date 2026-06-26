"""
免费翻译 OpenClaw 文档为中文 (使用 Google 免费翻译接口)
同时备份英文原版到 i18n/en/
"""
import os, sys, json, time, re
import urllib.request, urllib.parse

# 配置
BASE_DIR = r'C:\Users\50148\projects\openclaw中文社区网站'
DOCS_DIR = os.path.join(BASE_DIR, 'website', 'docs')
I18N_DIR = os.path.join(BASE_DIR, 'website', 'i18n', 'en', 'docusaurus-plugin-content-docs', 'current')
LOG_FILE = os.path.join(BASE_DIR, 'docs-system', 'translation_log.txt')

os.makedirs(I18N_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(msg):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{time.strftime("%H:%M:%S")} {msg}\n')
    print(msg)
    sys.stdout.flush()

def google_translate(text, src='en', tgt='zh-CN'):
    """调用 Google 免费翻译"""
    url = 'https://translate.googleapis.com/translate_a/single'
    params = {'client': 'gtx', 'sl': src, 'tl': tgt, 'dt': 't', 'q': text}
    url = url + '?' + urllib.parse.urlencode(params)
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                result = ''
                for part in data[0]:
                    if part[0]:
                        result += part[0]
                return result
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                return f'[翻译失败: {e}]'

def translate_markdown(content):
    """翻译 markdown 内容，保留格式"""
    # 分离 frontmatter 和正文
    fm = ''
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm = '---' + parts[1] + '---'
            body = parts[2]

    # 翻译正文
    if body.strip():
        translated = google_translate(body)
        if translated and not translated.startswith('[翻译失败'):
            # 修复一些常见翻译错误
            translated = translated.replace('纱线', 'yarn')
            translated = translated.replace('自述', 'README')
            return fm + '\n' + translated if fm else translated
    return content

# 统计
total = 0
success = 0
fail = 0
errors = []

# 遍历所有 .md 文件
for root, dirs, files in os.walk(DOCS_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        
        src_path = os.path.join(root, fname)
        rel_path = os.path.relpath(src_path, DOCS_DIR)
        
        # 计算目标路径
        dst_path = os.path.join(I18N_DIR, rel_path)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        
        total += 1
        
        # 读取原文
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 跳过已经是中文的（简单的判断）
        zh_count = len(re.findall(r'[\u4e00-\u9fff]', content))
        if zh_count > 50:  # 已经有不少中文了
            log(f'  ⏭ [{total}/351] {rel_path} — 已包含中文，跳过')
            # 仍然备份英语原文
            if not os.path.exists(dst_path):
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                with open(dst_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            success += 1
            continue
        
        # 备份英文原版
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 翻译
        log(f'  🔄 [{total}/351] 翻译中: {rel_path} ({len(content)} chars)')
        translated = translate_markdown(content)
        
        if translated and not translated.startswith('[翻译失败'):
            with open(src_path, 'w', encoding='utf-8') as f:
                f.write(translated)
            success += 1
            log(f'  ✅ [{total}/351] {rel_path} — 完成')
        else:
            fail += 1
            errors.append(rel_path)
            log(f'  ❌ [{total}/351] {rel_path} — 失败')
        
        # 限速：每次请求间隔 1 秒
        time.sleep(1)

# 报告
log(f'\n{"="*50}')
log(f'翻译完成!')
log(f'总文件: {total}')
log(f'成功: {success}')
log(f'失败: {fail}')
if errors:
    log(f'失败列表:')
    for e in errors:
        log(f'  - {e}')
log(f'英文原版备份在: {I18N_DIR}')
