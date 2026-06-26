#!/usr/bin/env python3
"""Batch fetch OpenClaw Chinese docs and build articles.json + config.json"""
import json, re, sys, time, os
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import concurrent.futures

# Configuration
SITEMAP = "https://docs.openclaw.ai/zh-CN"
URLS_FILE = Path("zhcn_urls.txt")
OUTPUT_DIR = Path("docs-system/output")
MAX_WORKERS = 10

def fetch_url(url):
    """Fetch a URL and return (url, html)"""
    try:
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })
        with urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='replace')
        return (url, html)
    except Exception as e:
        return (url, None)

def extract_article(html):
    """Extract article title, description, and content from HTML"""
    if not html:
        return None
    
    # Extract title from <title> tag
    title_m = re.search(r'<title[^>]*>([^<]+)', html)
    title = title_m.group(1).strip() if title_m else ""
    # Clean title - remove site name suffix
    title = re.sub(r'\s*[-–—|]\s*OpenClaw.*', '', title).strip()
    
    # Extract description from meta tag
    desc_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', html, re.IGNORECASE)
    description = desc_m.group(1).strip() if desc_m else ""
    
    # Extract article content
    article_m = re.search(r'<article class="article">(.*?)</article>', html, re.DOTALL)
    content = article_m.group(1) if article_m else ""
    
    if not content:
        return None
    
    return {
        'title': title,
        'description': description,
        'content': '<article class="markdown">' + content + '</article>',
    }

def url_to_path_key(url):
    """Convert URL to path key like /docs/getting-started/quickstart/"""
    # Remove base URL
    path = url.replace('https://docs.openclaw.ai/zh-CN', '')
    if not path:
        path = '/'
    # Ensure starts with /docs/
    path_key = f'/docs{path}'
    if not path_key.endswith('/'):
        path_key += '/'
    return path_key

def main():
    # Read URLs
    urls = [u.strip() for u in URLS_FILE.read_text().splitlines() if u.strip()]
    print(f'总 URL 数: {len(urls)}')
    print(f'并行线程: {MAX_WORKERS}')
    
    # Batch fetch
    articles = {}
    failed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_url, url): url for url in urls}
        done = 0
        for future in concurrent.futures.as_completed(futures):
            url, html = future.result()
            done += 1
            result = extract_article(html)
            if result:
                key = url_to_path_key(url)
                articles[key] = result
            else:
                failed += 1
            
            if done % 50 == 0 or done == len(urls):
                print(f'  进度: {done}/{len(urls)}, 成功: {len(articles)}, 失败: {failed}')
    
    print(f'\n抓取完成')
    print(f'成功: {len(articles)}, 失败: {failed}')
    
    # Save articles
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    articles_json = json.dumps(articles, ensure_ascii=False, indent=None)
    (OUTPUT_DIR / 'docs-articles.json').write_text(articles_json, encoding='utf-8')
    print(f'docs-articles.json 已生成 ({len(articles)} 篇文章, {len(articles_json)//1024} KB)')
    
    # Build a flat sidebar config (we'll refine later)
    # Generate category structure from URL paths
    categories = {}
    for key in articles:
        parts = key.strip('/').split('/')
        if len(parts) >= 2:
            cat = parts[1]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(key)
    
    sidebar = []
    for cat_name, items in sorted(categories.items()):
        sidebar.append({
            'type': 'category',
            'label': cat_name,
            'items': [{'type': 'link', 'label': articles[item]['title'], 'href': item} for item in sorted(items)]
        })
    
    (OUTPUT_DIR / 'docs-config.json').write_text(
        json.dumps(sidebar, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f'docs-config.json 已生成 ({len(sidebar)} 个分类)')
    
    print('\n分类概览:')
    for cat, items in sorted(categories.items()):
        print(f'  {cat}: {len(items)} 页')

if __name__ == '__main__':
    main()
