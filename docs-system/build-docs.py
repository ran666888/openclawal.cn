#!/usr/bin/env python3
"""
OpenClaw 文档构建脚本
从 website/docs/*.md 生成 HTML 文档页面
用法: python build-docs.py
"""

import os, json, re, shutil
from pathlib import Path
import markdown as md_lib

# ========== 路径配置 ==========
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent  # openclaw中文社区网站/
DOCS_SRC = PROJECT_DIR / 'website' / 'docs'
SIDEBARS_TS = PROJECT_DIR / 'website' / 'sidebars.ts'
TEMPLATE_FILE = BASE_DIR / 'templates' / 'doc-template.html'
CSS_SRC = BASE_DIR / 'templates' / 'docs.css'
JS_SRC = BASE_DIR / 'templates' / 'docs.js'
OUTPUT_DIR = BASE_DIR / 'output'
DOCS_OUTPUT = OUTPUT_DIR / 'docs'
CONFIG_OUTPUT = OUTPUT_DIR / 'docs-config.json'
ARTICLES_OUTPUT = OUTPUT_DIR / 'docs-articles.json'

# ========== 解析 sidebars.ts → JSON 结构 ==========
def parse_sidebar_items(lines, start_idx):
    """递归解析侧边栏 items 数组"""
    items = []
    i = start_idx
    while i < len(lines):
        line = lines[i]
        indent = len(line) - len(line.lstrip())

        # 检测闭合
        if '];' in line and indent <= 8:
            break
        if '};' in line and indent <= 4:
            break
        if line.strip().startswith('],'):
            i += 1
            break

        stripped = line.strip()

        # 分类
        if stripped.startswith("type: 'category'"):
            label = ''
            sub_items = []
            j = i + 1
            while j < len(lines):
                sl = lines[j].strip()
                if sl.startswith('label:'):
                    label = sl.split("'")[1] if "'" in sl else sl.split('"')[1]
                elif sl.startswith('items:'):
                    sub_items, j = parse_sidebar_items(lines, j + 1)
                    break
                elif sl.startswith('],') or sl.startswith('},'):
                    break
                j += 1
            items.append({'type': 'category', 'label': label, 'items': sub_items})
            i = j
            continue

        # 单页引用
        if stripped.startswith("'") and "'" in stripped[1:]:
            ref = stripped.split("'")[1]
            # 获取标题
            title = ref_to_title(ref)
            items.append({'type': 'link', 'label': title, 'href': f'/docs/{ref}/'})
            i += 1
            continue

        i += 1

    return items, i

def ref_to_title(ref):
    """从 markdown 文件提取标题"""
    parts = ref.split('/')
    md_path = DOCS_SRC / f'{ref}.md'
    if md_path.exists():
        content = md_path.read_text(encoding='utf-8')
        # 找第一个 # 标题
        m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if m:
            return m.group(1).strip()
    # fallback：用文件名
    return parts[-1].replace('-', ' ').title()

def parse_sidebars(filepath):
    """解析 sidebars.ts 文件"""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    # 找到 docs: [ 开始位置
    for i, line in enumerate(lines):
        if 'docs: [' in line:
            items, _ = parse_sidebar_items(lines, i + 1)
            return items
    return []

# ========== 转换 Markdown → HTML ==========
def md_to_html(content):
    """将 markdown 内容转为 HTML"""
    extensions = [
        'fenced_code', 'tables', 'codehilite',
        'sane_lists', 'attr_list', 'def_list',
        'footnotes', 'md_in_html', 'toc',
    ]
    # 移除 frontmatter (--- ... ---)
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

    # 处理代码块 - 添加语言类
    content = re.sub(
        r'```(\w+)?\n(.*?)```',
        lambda m: f'<pre><code class="language-{m.group(1) or ""}">{m.group(2).strip()}</code></pre>',
        content, flags=re.DOTALL
    )

    html = md_lib.markdown(content, extensions=extensions)
    return html

def extract_meta(content):
    """提取 markdown 的 frontmatter 元数据"""
    desc = ''
    m = re.search(r'^description:\s*(.+)$', content, re.MULTILINE)
    if m:
        desc = m.group(1).strip().strip('"').strip("'")
    return {'description': desc or 'OpenClaw 中文文档'}

# ========== 构建所有文档 ==========
def build_all():
    print('📦 OpenClaw 文档构建器')
    print('=' * 50)

    # 1. 解析侧边栏
    print('📋 解析侧边栏...')
    sidebar_data = parse_sidebars(SIDEBARS_TS)
    print(f'   找到 {len(sidebar_data)} 个顶级分类')

    # 保存配置
    CONFIG_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_OUTPUT.write_text(
        json.dumps(sidebar_data, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'   ✅ docs-config.json 已生成')

    # 2. 读取模板
    template = TEMPLATE_FILE.read_text(encoding='utf-8')

    # 3. 遍历所有 .md 文件并生成 HTML
    md_files = sorted(DOCS_SRC.rglob('*.md'))
    print(f'📄 处理 {len(md_files)} 个 markdown 文件...')

    # 收藏所有 href → sidebar label 映射
    href_label_map = {}
    def map_sidebar_labels(items, prefix=''):
        for item in items:
            if item['type'] == 'link':
                href_label_map[item['href']] = item['label']
            elif item['type'] == 'category':
                map_sidebar_labels(item['items'], prefix)
    map_sidebar_labels(sidebar_data)

    sidebar_json = json.dumps(sidebar_data, ensure_ascii=False)

    # 3. 遍历所有 .md 文件，生成文章 JSON
    md_files = sorted(DOCS_SRC.rglob('*.md'))
    print(f'📄 处理 {len(md_files)} 个 markdown 文件...')

    articles = {}

    for md_file in md_files:
        rel_path = md_file.relative_to(DOCS_SRC)
        stem = rel_path.stem
        parent = rel_path.parent

        # 计算路径 key
        if stem == 'index' and str(parent) == '.':
            path_key = '/docs/'
        elif stem == 'index':
            path_key = f'/docs/{parent}/'
        else:
            path_key = f'/docs/{parent}/{stem}/'

        # 统一用正斜杠（Windows 路径问题）
        path_key = path_key.replace('\\', '/')

        # 读取 markdown
        content = md_file.read_text(encoding='utf-8')
        meta = extract_meta(content)
        html = md_to_html(content)

        # 获取标题
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', html)
        title = title_match.group(1) if title_match else stem.replace('-', ' ').title()

        articles[path_key] = {
            'title': title,
            'description': meta['description'],
            'content': html,
            'edit_url': f'https://github.com/ran666888/openclawal.cn/edit/main/website/docs/{rel_path}'
        }

    # 保存文章数据
    ARTICLES_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ARTICLES_OUTPUT.write_text(
        json.dumps(articles, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f'   ✅ docs-articles.json 已生成（{len(articles)} 篇文章）')

    # 4. 复制静态资源
    print('🎨 复制样式和脚本...')
    assets_dir = OUTPUT_DIR / 'assets' / 'css'
    assets_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CSS_SRC, assets_dir / 'docs.css')
    print(f'   ✅ docs.css')

    # 5. 输出总览
    total_size_json = (ARTICLES_OUTPUT.stat().st_size + CONFIG_OUTPUT.stat().st_size) / 1024
    print(f'\n📊 构建总结:')
    print(f'   文章数: {len(articles)}')
    print(f'   数据大小: {total_size_json:.0f} KB')
    print(f'   ✅ 完成! 数据文件已生成，查看器需从主站加载')

if __name__ == '__main__':
    build_all()
