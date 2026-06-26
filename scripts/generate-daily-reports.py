#!/usr/bin/env python3
"""从 agthub.tech 的 daily-data.js 生成 openclawal.cn 的日报独立页面"""

import subprocess, json, os, re
from datetime import datetime
from collections import defaultdict

# ── 路径 ──
DAILY_JS = "C:/Users/50148/agent-hub-cn/daily-data.js"
OUT_DIR  = "C:/Users/50148/projects/openclaw中文社区网站/dist/reports/daily"

os.makedirs(OUT_DIR, exist_ok=True)

# ── 1. 用 Node 解析 daily-data.js → JSON ──
node_script = """
const fs = require('fs');
let code = fs.readFileSync(process.argv[1], 'utf-8');
code = code.replace('var articles', 'globalThis.articles');
eval(code);
process.stdout.write(JSON.stringify(globalThis.articles));
"""

result = subprocess.run(
    ["node", "-e", node_script, DAILY_JS],
    capture_output=True, text=True, timeout=15
)
if result.returncode != 0:
    print(f"❌ Node 解析失败:\n{result.stderr}")
    exit(1)

articles = json.loads(result.stdout)
print(f"✅ 从 daily-data.js 解析到 {len(articles)} 篇文章")

# ── 2. 按日期分组 ──
by_date = defaultdict(list)
for a in articles:
    by_date[a["date"]].append(a)

print(f"📅 共 {len(by_date)} 期日报")

# ── 3. 辅助函数 ──
WEEKDAYS_ZH = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
WEEKDAYS_EN = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

def date_to_path(d):
    """2026.06.26 → 2026-06-26"""
    return d.replace(".", "-")

def get_weekday(d_str):
    dt = datetime.strptime(d_str, "%Y.%m.%d")
    return WEEKDAYS_ZH[dt.weekday()], WEEKDAYS_EN[dt.weekday()]

def parse_body(body_html):
    """从 body 中提取摘要纯文本和来源链接"""
    # 去掉所有 HTML 标签，取前 200 字作为摘要
    clean = re.sub(r'<[^>]+>', '', body_html)
    # 去掉来源行
    parts = clean.split("来源：")
    summary = parts[0].strip()
    source = ""
    if len(parts) > 1:
        source = "来源：" + parts[1].strip()
    # 截断太长
    if len(summary) > 280:
        summary = summary[:280] + "…"
    return summary, source

TAG_COLORS = {
    "AI 行业":   {"bg": "rgba(251,146,60,0.15)", "border": "rgba(251,146,60,0.35)", "text": "#fb923c"},
    "实用技巧": {"bg": "rgba(94,234,212,0.15)",  "border": "rgba(94,234,212,0.35)",  "text": "#5eead4"},
    "热门推荐": {"bg": "rgba(251,191,36,0.15)",  "border": "rgba(251,191,36,0.35)",  "text": "#fbbf24"},
    "开源项目": {"bg": "rgba(196,181,253,0.15)", "border": "rgba(196,181,253,0.35)", "text": "#c4b5fd"},
}

# ── 4. 生成 HTML ──
def generate_html(date_str, items):
    weekday_zh, weekday_en = get_weekday(date_str)
    parts = date_str.split(".")
    year, month, day = parts[0], parts[1], parts[2]
    path_date = date_to_path(date_str)
    item_count = len(items)

    articles_html = ""
    for i, item in enumerate(items):
        tag = item.get("tag", "AI 行业")
        title = item.get("title", "")
        body = item.get("body", "")
        summary, source = parse_body(body)

        tc = TAG_COLORS.get(tag, TAG_COLORS["AI 行业"])

        # 前 3 篇用金色大卡片，其余用白底列表
        if i < 3:
            articles_html += f"""
            <li class="headline">
              <div class="headline-meta">
                <span class="tag-headline">{tag}</span>
                <span class="item-source">{source}</span>
              </div>
              <h3 class="headline-title">{title}</h3>
              <p class="headline-detail">{summary}</p>
            </li>"""
        else:
            articles_html += f"""
            <li class="community-item">
              <div class="community-meta">
                <span class="tag-community" style="--tag-bg:{tc['bg']};--tag-border:{tc['border']};--tag-text:{tc['text']}">{tag}</span>
                <span class="item-source">{source}</span>
              </div>
              <h3 class="community-title">{title}</h3>
              <p class="community-detail">{summary}</p>
            </li>"""

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenClaw 中文社区日报 {year}年{month}月{int(day)}日</title>
  <meta name="description" content="每天 1 分钟，了解 AI Agent 最新资讯。" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="https://openclawal.cn/daily/{path_date}" />
  <meta property="og:url" content="https://openclawal.cn/daily/{path_date}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="OpenClaw 中文社区日报 {year}年{month}月{int(day)}日" />
  <meta property="og:description" content="每天 1 分钟，了解 AI Agent 最新资讯。" />
  <meta property="og:site_name" content="OpenClaw 中文社区" />
  <meta property="article:published_time" content="{path_date}T09:00:00+08:00" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="OpenClaw 中文社区日报 {year}年{month}月{int(day)}日" />
  <meta name="twitter:description" content="每天 1 分钟，了解 AI Agent 最新资讯。" />
  <script type="application/ld+json">{json.dumps({{
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": f"OpenClaw 中文社区日报 {year}年{month}月{int(day)}日",
    "name": f"OpenClaw 中文社区日报 {year}年{month}月{int(day)}日",
    "description": "每天 1 分钟，了解 AI Agent 最新资讯。",
    "inLanguage": "zh-CN",
    "datePublished": f"{path_date}T09:00:00+08:00",
    "dateModified": f"{path_date}T18:00:00+08:00",
    "mainEntityOfPage": f"https://openclawal.cn/daily/{path_date}",
    "url": f"https://openclawal.cn/daily/{path_date}",
    "isAccessibleForFree": True,
    "author": {{"@type": "Organization", "name": "OpenClaw 中文社区", "url": "https://openclawal.cn"}},
    "publisher": {{"@type": "Organization", "name": "OpenClaw 中文社区", "url": "https://openclawal.cn"}},
  }}, ensure_ascii=False)}</script>
  <style>
    :root {{
      --bg-deep: #0f0f1a;
      --bg-soft: #1a1a2e;
      --bg-mid: #16213e;
      --paper: #f6efdb;
      --paper-strong: #fdf6e8;
      --paper-line: rgba(23,48,47,0.10);
      --paper-line-strong: rgba(23,48,47,0.18);
      --ink: #17302f;
      --ink-soft: rgba(23,48,47,0.74);
      --ink-faint: rgba(23,48,47,0.5);
      --cream: #ffe6cb;
      --cream-soft: rgba(255,230,203,0.78);
      --cream-faint: rgba(255,230,203,0.5);
      --gold: #b97f0b;
      --gold-soft: #e0a93a;
      --gold-bright: #ffd96b;
      --gold-deep: #6b4500;
      --green: #155d4d;
      --green-deep: #0d4641;
      --accent: #fb923c;
      --accent-glow: rgba(251,146,60,0.25);
      --shadow: 0 28px 80px rgba(0,0,0,0.32);
      --radius: 28px;
      --font-sans: 'PingFang SC','Hiragino Sans GB','Noto Sans SC','Microsoft YaHei',system-ui,sans-serif;
      --font-serif: 'Noto Serif SC','Source Han Serif SC','Songti SC','STSong',serif;
      --font-mono: 'Courier Prime','SFMono-Regular','Menlo',monospace;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; padding: 0; }}
    body {{
      min-height: 100vh;
      font-family: var(--font-serif);
      color: var(--cream);
      background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
    }}
    .shot-root {{
      width: min(760px, 100%);
      margin: 0 auto;
      padding: 36px 28px 44px;
    }}
    .poster {{
      position: relative;
      overflow: hidden;
      width: 100%;
      border-radius: var(--radius);
      border: 1px solid rgba(255,230,203,0.18);
      box-shadow: var(--shadow);
      background: var(--paper);
    }}
    .poster-shell {{ padding: 14px; }}
    .poster-frame {{
      border-radius: calc(var(--radius) - 8px);
      overflow: hidden;
      border: 1px solid var(--paper-line);
      background: var(--paper-strong);
    }}
    .hero {{
      position: relative;
      padding: 32px 32px 26px;
      background:
        radial-gradient(circle at 88% 0%, rgba(251,146,60,0.14), transparent 38%),
        radial-gradient(circle at 0% 100%, rgba(94,234,212,0.10), transparent 36%),
        linear-gradient(135deg, #16213e 0%, #1a1a2e 60%, #0f0f1a 100%);
      color: var(--cream);
    }}
    .hero-row {{
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
    }}
    .hero-weekday {{
      font-family: var(--font-serif);
      font-size: 64px;
      line-height: 0.95;
      font-weight: 800;
      letter-spacing: -0.04em;
      color: var(--cream);
    }}
    .hero-slogan-sub {{
      margin-top: 10px;
      font-size: 15px;
      font-weight: 500;
      letter-spacing: 0.04em;
      color: var(--cream-faint);
    }}
    .hero-eyebrow {{
      display: block;
      margin-bottom: 6px;
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.32em;
      text-transform: uppercase;
      color: var(--cream-faint);
    }}
    .hero-date {{ text-align: right; color: var(--cream-soft); }}
    .hero-date .y {{
      display: block;
      font-size: 13px;
      letter-spacing: 0.16em;
      color: var(--cream-faint);
    }}
    .hero-date .md {{
      display: block;
      margin-top: 4px;
      font-size: 26px;
      font-weight: 700;
      color: var(--cream);
      letter-spacing: 0.04em;
    }}
    .hero-foot {{
      margin-top: 22px;
      padding-top: 16px;
      border-top: 1px solid rgba(255,230,203,0.18);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
    }}
    .hero-brand {{
      font-size: 17px;
      font-weight: 700;
      color: var(--cream);
      letter-spacing: 0.02em;
    }}
    .hero-stats {{
      font-family: var(--font-mono);
      font-size: 12px;
      letter-spacing: 0.06em;
      color: var(--cream-soft);
    }}
    .hero-stats strong {{
      color: var(--gold-bright);
      font-weight: 700;
      font-size: 15px;
    }}
    .section-head {{
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 22px 26px 6px;
    }}
    .section-head .bar {{
      width: 4px;
      height: 18px;
      border-radius: 2px;
      background: var(--gold);
    }}
    .section-head .bar-headline {{ background: var(--gold); }}
    .section-head .bar-community {{ background: var(--green); }}
    .section-head .label {{
      font-size: 16px;
      font-weight: 800;
      color: var(--ink);
      letter-spacing: 0.02em;
    }}
    .section-head .meta {{
      margin-left: auto;
      font-family: var(--font-mono);
      font-size: 10px;
      letter-spacing: 0.18em;
      color: var(--ink-faint);
      text-transform: uppercase;
    }}
    .headlines {{ list-style: none; margin: 0; padding: 6px 22px 6px; }}
    .headline {{
      position: relative;
      margin: 0 0 12px;
      padding: 18px 18px 18px 22px;
      border-radius: 14px;
      background: linear-gradient(180deg, rgba(251,146,60,0.11), rgba(251,146,60,0.04));
      border: 1px solid rgba(251,146,60,0.28);
    }}
    .headline::before {{
      content: '';
      position: absolute;
      left: 8px; top: 20px; bottom: 20px;
      width: 3px;
      border-radius: 2px;
      background: var(--accent);
    }}
    .headline-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }}
    .tag-headline {{
      display: inline-flex;
      align-items: center;
      height: 22px;
      padding: 0 10px;
      border-radius: 4px;
      background: var(--accent);
      color: #fff8e5;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.08em;
    }}
    .item-source {{
      display: inline-flex;
      align-items: center;
      min-height: 22px;
      color: var(--ink-faint);
      font-size: 12px;
      font-weight: 600;
      line-height: 1.35;
    }}
    .headline .item-source {{ color: rgba(107,69,0,0.72); }}
    .headline-title {{
      margin: 0 0 10px;
      font-size: 32px;
      line-height: 1.4;
      font-weight: 800;
      color: var(--ink);
    }}
    .headline-detail {{
      margin: 0;
      font-size: 17px;
      line-height: 1.78;
      color: var(--ink-soft);
    }}
    .community {{ list-style: none; margin: 0; padding: 4px 26px 14px; }}
    .community-item {{
      padding: 14px 0 15px;
      border-bottom: 1px solid var(--paper-line-strong);
    }}
    .community-item:last-child {{ border-bottom: none; }}
    .community-meta {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      flex-wrap: wrap;
    }}
    .tag-community {{
      display: inline-flex;
      align-items: center;
      height: 22px;
      padding: 0 9px;
      border-radius: 4px;
      border: 1px solid var(--tag-border, rgba(21,93,77,0.32));
      background: var(--tag-bg, rgba(21,93,77,0.08));
      color: var(--tag-text, var(--green));
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.02em;
    }}
    .community-title {{
      margin: 0 0 8px;
      font-size: 28px;
      line-height: 1.38;
      font-weight: 700;
      color: var(--ink);
    }}
    .community-detail {{
      margin: 0;
      font-size: 17px;
      line-height: 1.78;
      color: var(--ink-soft);
    }}
  </style>
</head>
<body>
  <div class="shot-root">
    <article class="poster">
      <div class="poster-shell">
        <div class="poster-frame">
          <div class="hero">
            <div class="hero-row">
              <div>
                <span class="hero-eyebrow">{weekday_en} · DAILY DIGEST</span>
                <div class="hero-weekday">{weekday_zh}</div>
                <div class="hero-slogan-sub">1 分钟了解每日 AI 最新动态</div>
              </div>
              <div class="hero-date">
                <span class="y">{year} 年</span>
                <span class="md">{int(month)} 月 {int(day)} 日</span>
              </div>
            </div>
            <div class="hero-foot">
              <span class="hero-brand">OpenClaw 中文社区日报</span>
              <span class="hero-stats">共 <strong>{item_count}</strong> 条 · 第 {len(by_date)} 期</span>
            </div>
          </div>

          <div class="section-head">
            <span class="bar bar-headline"></span>
            <span class="label">要闻速览</span>
            <span class="meta">HEADLINES · {min(3, item_count)}</span>
          </div>
          <ul class="headlines">
            {"".join(articles_html.split("</ul>")[0].split("<ul")[-1].split(">", 1)[1:]) if False else ""}
          </ul>

          <div class="section-head">
            <span class="bar bar-community"></span>
            <span class="label">社区摘录</span>
            <span class="meta">COMMUNITY · {item_count}</span>
          </div>
          <ul class="community">
            {articles_html}
          </ul>
        </div>
      </div>
    </article>
  </div>
</body>
</html>"""

    # 修正：前3条headlines和后4+条community分离
    return html

def generate_html_v2(date_str, items):
    """生成日报 HTML — 正确分离 headlines 和 community"""
    weekday_zh, weekday_en = get_weekday(date_str)
    parts = date_str.split(".")
    year, month, day = parts[0], parts[1], parts[2]
    path_date = date_to_path(date_str)
    item_count = len(items)

    headlines_html = ""
    community_html = ""

    ld_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": f"OpenClaw 中文社区日报 {year}年{month}月{int(day)}日",
        "description": "每天 1 分钟，了解 AI Agent 最新资讯。",
        "inLanguage": "zh-CN",
        "datePublished": f"{path_date}T09:00:00+08:00",
        "mainEntityOfPage": f"https://openclawal.cn/daily/{path_date}",
        "url": f"https://openclawal.cn/daily/{path_date}",
        "author": {"@type": "Organization", "name": "OpenClaw 中文社区", "url": "https://openclawal.cn"},
        "publisher": {"@type": "Organization", "name": "OpenClaw 中文社区", "url": "https://openclawal.cn"},
    }, ensure_ascii=False)

    for i, item in enumerate(items):
        tag = item.get("tag", "AI 行业")
        title = item.get("title", "")
        body = item.get("body", "")
        summary, source = parse_body(body)

        if i < 3:
            headlines_html += f"""
            <li class="headline">
              <div class="headline-meta">
                <span class="tag-headline">{tag}</span>
                <span class="item-source">{source}</span>
              </div>
              <h3 class="headline-title">{title}</h3>
              <p class="headline-detail">{summary}</p>
            </li>"""
        else:
            tc = TAG_COLORS.get(tag, TAG_COLORS["AI 行业"])
            community_html += f"""
            <li class="community-item">
              <div class="community-meta">
                <span class="tag-community" style="--tag-bg:{tc['bg']};--tag-border:{tc['border']};--tag-text:{tc['text']}">{tag}</span>
                <span class="item-source">{source}</span>
              </div>
              <h3 class="community-title">{title}</h3>
              <p class="community-detail">{summary}</p>
            </li>"""

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>OpenClaw 中文社区日报 {year}年{month}月{int(day)}日</title>
  <meta name="description" content="每天 1 分钟，了解 AI Agent 最新资讯。" />
  <meta name="robots" content="index,follow" />
  <link rel="canonical" href="https://openclawal.cn/daily/{path_date}" />
  <meta property="og:url" content="https://openclawal.cn/daily/{path_date}" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="OpenClaw 中文社区日报 {year}年{month}月{int(day)}日" />
  <meta property="og:description" content="每天 1 分钟，了解 AI Agent 最新资讯。" />
  <meta property="og:site_name" content="OpenClaw 中文社区" />
  <meta property="article:published_time" content="{path_date}T09:00:00+08:00" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="OpenClaw 中文社区日报 {year}年{month}月{int(day)}日" />
  <meta name="twitter:description" content="每天 1 分钟，了解 AI Agent 最新资讯。" />
  <script type="application/ld+json">{ld_json}</script>
  <style>
    :root {{
      --bg-deep: #0f0f1a; --bg-soft: #1a1a2e; --bg-mid: #16213e;
      --paper: #f6efdb; --paper-strong: #fdf6e8;
      --paper-line: rgba(23,48,47,0.10); --paper-line-strong: rgba(23,48,47,0.18);
      --ink: #17302f; --ink-soft: rgba(23,48,47,0.74); --ink-faint: rgba(23,48,47,0.5);
      --cream: #ffe6cb; --cream-soft: rgba(255,230,203,0.78); --cream-faint: rgba(255,230,203,0.5);
      --gold: #b97f0b; --gold-soft: #e0a93a; --gold-bright: #ffd96b;
      --green: #155d4d; --green-deep: #0d4641;
      --accent: #fb923c;
      --shadow: 0 28px 80px rgba(0,0,0,0.32); --radius: 28px;
      --font-sans: 'PingFang SC','Hiragino Sans GB','Noto Sans SC','Microsoft YaHei',system-ui,sans-serif;
      --font-serif: 'Noto Serif SC','Source Han Serif SC','Songti SC','STSong',serif;
      --font-mono: 'Courier Prime','SFMono-Regular','Menlo',monospace;
    }}
    *{{box-sizing:border-box}} html,body{{margin:0;padding:0}}
    body{{min-height:100vh;font-family:var(--font-serif);color:var(--cream);background:linear-gradient(180deg,#1a1a2e 0%,#0f0f1a 100%)}}
    .shot-root{{width:min(760px,100%);margin:0 auto;padding:36px 28px 44px}}
    .poster{{position:relative;overflow:hidden;width:100%;border-radius:var(--radius);border:1px solid rgba(255,230,203,0.18);box-shadow:var(--shadow);background:var(--paper)}}
    .poster-shell{{padding:14px}}
    .poster-frame{{border-radius:calc(var(--radius)-8px);overflow:hidden;border:1px solid var(--paper-line);background:var(--paper-strong)}}
    .hero{{position:relative;padding:32px 32px 26px;background:radial-gradient(circle at 88% 0%,rgba(251,146,60,0.14),transparent 38%),radial-gradient(circle at 0% 100%,rgba(94,234,212,0.10),transparent 36%),linear-gradient(135deg,#16213e 0%,#1a1a2e 60%,#0f0f1a 100%);color:var(--cream)}}
    .hero-row{{display:flex;align-items:flex-end;justify-content:space-between;gap:16px}}
    .hero-weekday{{font-family:var(--font-serif);font-size:64px;line-height:0.95;font-weight:800;letter-spacing:-0.04em;color:var(--cream)}}
    .hero-slogan-sub{{margin-top:10px;font-size:15px;font-weight:500;letter-spacing:0.04em;color:var(--cream-faint)}}
    .hero-eyebrow{{display:block;margin-bottom:6px;font-family:var(--font-mono);font-size:11px;letter-spacing:0.32em;text-transform:uppercase;color:var(--cream-faint)}}
    .hero-date{{text-align:right;color:var(--cream-soft)}}
    .hero-date .y{{display:block;font-size:13px;letter-spacing:0.16em;color:var(--cream-faint)}}
    .hero-date .md{{display:block;margin-top:4px;font-size:26px;font-weight:700;color:var(--cream);letter-spacing:0.04em}}
    .hero-foot{{margin-top:22px;padding-top:16px;border-top:1px solid rgba(255,230,203,0.18);display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}}
    .hero-brand{{font-size:17px;font-weight:700;color:var(--cream);letter-spacing:0.02em}}
    .hero-stats{{font-family:var(--font-mono);font-size:12px;letter-spacing:0.06em;color:var(--cream-soft)}}
    .hero-stats strong{{color:var(--gold-bright);font-weight:700;font-size:15px}}
    .section-head{{display:flex;align-items:center;gap:10px;padding:22px 26px 6px}}
    .section-head .bar{{width:4px;height:18px;border-radius:2px}}
    .section-head .bar-headline{{background:var(--accent)}}
    .section-head .bar-community{{background:var(--green)}}
    .section-head .label{{font-size:16px;font-weight:800;color:var(--ink);letter-spacing:0.02em}}
    .section-head .meta{{margin-left:auto;font-family:var(--font-mono);font-size:10px;letter-spacing:0.18em;color:var(--ink-faint);text-transform:uppercase}}
    .headlines{{list-style:none;margin:0;padding:6px 22px 6px}}
    .headline{{position:relative;margin:0 0 12px;padding:18px 18px 18px 22px;border-radius:14px;background:linear-gradient(180deg,rgba(251,146,60,0.11),rgba(251,146,60,0.04));border:1px solid rgba(251,146,60,0.28)}}
    .headline::before{{content:'';position:absolute;left:8px;top:20px;bottom:20px;width:3px;border-radius:2px;background:var(--accent)}}
    .headline-meta{{display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap}}
    .tag-headline{{display:inline-flex;align-items:center;height:22px;padding:0 10px;border-radius:4px;background:var(--accent);color:#fff8e5;font-size:12px;font-weight:800;letter-spacing:0.08em}}
    .item-source{{display:inline-flex;align-items:center;min-height:22px;color:var(--ink-faint);font-size:12px;font-weight:600;line-height:1.35}}
    .headline .item-source{{color:rgba(107,69,0,0.72)}}
    .headline-title{{margin:0 0 10px;font-size:30px;line-height:1.38;font-weight:800;color:var(--ink)}}
    .headline-detail{{margin:0;font-size:17px;line-height:1.78;color:var(--ink-soft)}}
    .community{{list-style:none;margin:0;padding:4px 26px 14px}}
    .community-item{{padding:14px 0 15px;border-bottom:1px solid var(--paper-line-strong)}}
    .community-item:last-child{{border-bottom:none}}
    .community-meta{{display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap}}
    .tag-community{{display:inline-flex;align-items:center;height:22px;padding:0 9px;border-radius:4px;border:1px solid var(--tag-border,rgba(21,93,77,0.32));background:var(--tag-bg,rgba(21,93,77,0.08));color:var(--tag-text,var(--green));font-size:12px;font-weight:700;letter-spacing:0.02em}}
    .community-title{{margin:0 0 8px;font-size:27px;line-height:1.38;font-weight:700;color:var(--ink)}}
    .community-detail{{margin:0;font-size:17px;line-height:1.78;color:var(--ink-soft)}}
  </style>
</head>
<body>
  <div class="shot-root">
    <article class="poster">
      <div class="poster-shell">
        <div class="poster-frame">
          <div class="hero">
            <div class="hero-row">
              <div>
                <span class="hero-eyebrow">{weekday_en} · DAILY DIGEST</span>
                <div class="hero-weekday">{weekday_zh}</div>
                <div class="hero-slogan-sub">1 分钟了解每日 AI 最新动态</div>
              </div>
              <div class="hero-date">
                <span class="y">{year} 年</span>
                <span class="md">{int(month)} 月 {int(day)} 日</span>
              </div>
            </div>
            <div class="hero-foot">
              <span class="hero-brand">OpenClaw 中文社区日报</span>
              <span class="hero-stats">共 <strong>{item_count}</strong> 条</span>
            </div>
          </div>

          {f'''<div class="section-head"><span class="bar bar-headline"></span><span class="label">要闻速览</span><span class="meta">HEADLINES · {min(3, item_count)}</span></div>
          <ul class="headlines">{headlines_html}</ul>''' if headlines_html else ''}

          <div class="section-head">
            <span class="bar bar-community"></span>
            <span class="label">社区摘录</span>
            <span class="meta">COMMUNITY · {item_count}</span>
          </div>
          <ul class="community">
            {headlines_html + community_html if not headlines_html else community_html}
          </ul>
        </div>
      </div>
    </article>
  </div>
</body>
</html>"""
    return html

# ── 5. 执行生成 ──
count = 0
total_articles = 0
for date_str in sorted(by_date.keys()):
    items = by_date[date_str]
    path_date = date_to_path(date_str)
    output_path = os.path.join(OUT_DIR, f"{path_date}.html")

    html = generate_html_v2(date_str, items)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✅ {path_date}.html — {len(items)} 篇文章")
    count += 1
    total_articles += len(items)

print(f"\n📊 完成！生成 {count} 期日报，共 {total_articles} 篇文章")
print(f"📁 输出目录: {OUT_DIR}")
