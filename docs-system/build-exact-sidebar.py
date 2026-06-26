#!/usr/bin/env python3
"""Fetch official sidebar from each section and build exact docs-config.json"""
import json, re
from urllib.request import urlopen, Request

SECTIONS = {
    'start': '/zh-CN/start/showcase',
    'install': '/zh-CN/install',
    'channels': '/zh-CN/channels',
    'concepts': '/zh-CN/concepts/architecture',
    'tools': '/zh-CN/tools',
    'providers': '/zh-CN/providers',
    'platforms': '/zh-CN/platforms',
    'gateway': '/zh-CN/gateway',
    'cli': '/zh-CN/cli',
    'help': '/zh-CN/help',
}

# Tab names matching official site
TAB_NAMES = {
    'start': '快速开始',
    'install': '安装',
    'channels': '消息渠道',
    'concepts': '代理',
    'tools': '工具',
    'providers': '模型',
    'platforms': '平台',
    'gateway': '网关与运维',
    'cli': '参考',
    'help': '帮助',
}

def fetch(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')

def extract_sidebar(html):
    """Extract sidebar sections from official HTML"""
    # Find the sidebar nav content
    m = re.search(r'<aside class="sidebar">.*?<nav>(.*?)</nav>', html, re.DOTALL)
    if not m:
        return []
    nav_html = m.group(1)
    
    sections = []
    # Find each section
    for sec_m in re.finditer(r'<section class="nav-section">(.*?)</section>', nav_html, re.DOTALL):
        sec_html = sec_m.group(1)
        
        # Get h2 heading
        h2_m = re.search(r'<h2>(.*?)</h2>', sec_html)
        heading = h2_m.group(1).strip() if h2_m else ''
        
        # Get all links
        links = []
        for link_m in re.finditer(r'<a class="nav-link[^"]*"\s+href="([^"]*)">(.*?)</a>', sec_html):
            href = link_m.group(1)
            label = link_m.group(2).strip()
            links.append({'href': href, 'label': label})
        
        if heading or links:
            sections.append({'heading': heading, 'links': links})
    
    return sections

def official_to_local_href(official_href):
    """Convert /zh-CN/path to /docs/path/"""
    # Remove /zh-CN prefix
    path = official_href.replace('/zh-CN', '', 1)
    if not path.endswith('/'):
        path += '/'
    return '/docs' + path

def main():
    sidebar_config = []
    
    for section_key, section_path in SECTIONS.items():
        url = f'https://docs.openclaw.ai{section_path}'
        print(f'Fetching {url}...')
        
        try:
            html = fetch(url)
            sidebar = extract_sidebar(html)
            
            if not sidebar:
                print(f'  WARNING: No sidebar found for {section_key}')
                continue
            
            tab_name = TAB_NAMES[section_key]
            
            # Build category items
            items = []
            for sec in sidebar:
                sub_items = []
                for link in sec['links']:
                    local_href = official_to_local_href(link['href'])
                    sub_items.append({
                        'type': 'link',
                        'label': link['label'],
                        'href': local_href
                    })
                items.append({
                    'type': 'subcategory',
                    'label': sec['heading'],
                    'items': sub_items
                })
            
            sidebar_config.append({
                'type': 'category',
                'label': tab_name,
                'items': items
            })
            
            print(f'  ✅ {tab_name}: {len(items)} subcategories')
            
        except Exception as e:
            print(f'  ❌ Error: {e}')
    
    # Write config
    output_path = 'dist/docs-config.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sidebar_config, f, ensure_ascii=False, indent=2)
    
    print(f'\n✅ docs-config.json saved ({len(sidebar_config)} categories)')
    
    # Print summary
    for cat in sidebar_config:
        total_links = sum(len(sub['items']) for sub in cat['items'])
        print(f'  {cat["label"]}: {len(cat["items"])} sections, {total_links} links')

if __name__ == '__main__':
    main()
