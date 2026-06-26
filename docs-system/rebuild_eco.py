import os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open("dist/practice-guides/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# OpenClaw Web Control UI section
webui = '<article id="openclaw-web-control-ui" class="oc-cell oc-eco-featured" data-featured="true"><div class="oc-eco-featured__media"><span class="oc-eco-featured__caption">仪表板 · 聊天界面</span><img class="oc-eco-featured__image" src="/img/practice/openclaw-webui-cn.png" alt="OpenClaw Web Control UI 聊天界面" loading="lazy"><span class="oc-eco-featured__caption">技能管理</span><img class="oc-eco-featured__image" src="/img/practice/openclaw-webui-cn2.png" alt="OpenClaw Web Control UI 技能管理" loading="lazy"><span class="oc-eco-featured__capfoot">内置仪表板 · 无需安装 · openclaw dashboard</span></div><div class="oc-eco-featured__body"><div class="oc-eco-pills"><span class="oc-eco-pill oc-eco-pill--type">WebUI</span><span class="oc-eco-pill oc-eco-pill--stable">● 稳定</span><span class="oc-eco-pill">官方内置</span></div><h2 class="oc-eco-featured__title">OpenClaw Web Control UI</h2><p class="oc-eco-featured__tagline">OpenClaw 内置的浏览器仪表板，<code>openclaw dashboard</code> 一键启动。聊天、配置、会话管理、节点配对，一个界面管所有。</p><ul class="oc-eco-bullets"><li><code>openclaw dashboard</code> 一键启动，无需额外安装</li><li>浏览器内直接对话，多 Agent 会话统一管理</li><li>节点配对 + Canvas + 移动端支持</li><li>Tailscale 远程访问，随时随地连接</li></ul><div class="oc-eco-meta"><div class="oc-eco-meta__cell"><span class="oc-eco-meta__k">上手难度</span><span class="oc-eco-meta__v">⭐ · 极简</span></div><div class="oc-eco-meta__cell"><span class="oc-eco-meta__k">启动方式</span><span class="oc-eco-meta__v">openclaw dashboard</span></div><div class="oc-eco-meta__cell"><span class="oc-eco-meta__k">端口</span><span class="oc-eco-meta__v">18789</span></div></div><div class="oc-eco-actions"><a class="oc-button oc-eco-btn oc-eco-btn--primary" href="https://github.com/openclaw/openclaw" target="_blank" rel="noreferrer"><span class="oc-eco-btn__label">GitHub 仓库</span><span class="oc-eco-btn__arrow" aria-hidden="true">↗</span></a><a class="oc-button oc-eco-btn" href="http://localhost:3003/#docs" target="_blank" rel="noreferrer"><span class="oc-eco-btn__label">官方文档</span><span class="oc-eco-btn__arrow" aria-hidden="true">↗</span></a></div><div class="agent-prompt-card oc-eco-prompt"><div class="agent-prompt-header"><span class="agent-prompt-icon" aria-hidden="true">💬</span><span class="agent-prompt-title">复制提示词发给你的 OpenClaw，一键配置 Web 控制面板</span></div><div class="agent-prompt-body">OpenClaw 自带浏览器仪表板，请帮我启动：\n\n请帮我启动 OpenClaw Web 控制面板：运行 openclaw dashboard，等它启动后检查 http://127.0.0.1:18789/ 是否正常响应，确认后告诉我「已启动，可以正常访问」。</div><button class="agent-prompt-copy" type="button"><span class="agent-prompt-copy-icon" aria-hidden="true">📋</span><span>复制提示词</span></button></div></div></article>'

# Insert 1: After Hermes WebUI CN - unique marker: the MCP URL + prompt close + scale-os start
# Find: MCP URL through prompt close through scale-os start
marker1_old = 'https://mcp.openclaw.cn/v1 （Streamable HTTP，无需 API Key，无需登录）</div><button class="agent-prompt-copy" type="button"><span class="agent-prompt-copy-icon" aria-hidden="true">📋</span><span>复制提示词</span></button></div></div></article><article id="scale-os"'

marker1_new = 'https://mcp.openclaw.cn/v1 （Streamable HTTP，无需 API Key，无需登录）</div><button class="agent-prompt-copy" type="button"><span class="agent-prompt-copy-icon" aria-hidden="true">📋</span><span>复制提示词</span></button></div></div></article>\n\n' + webui + '\n\n<article id="scale-os"'

if marker1_old in html:
    html = html.replace(marker1_old, marker1_new, 1)
    print("Insert 1 (OpenClaw Web Control UI): SUCCESS")
else:
    print("Insert 1: FAILED - marker not found")

# Langfuse section  
langfuse = '<article id="langfuse" class="oc-cell oc-eco-featured-wide" data-featured="true"><div class="oc-eco-featured-wide__head"><div class="oc-eco-pills"><span class="oc-eco-pill oc-eco-pill--type">Observability · 可观测性</span><span class="oc-eco-pill oc-eco-pill--stable">● 稳定</span></div><h2 class="oc-eco-featured-wide__title">Langfuse</h2><p class="oc-eco-featured-wide__tagline">用了 OpenClaw 之后，想知道它每步在干嘛、花了多少 Token、有没有出问题？Langfuse 就是干这个的。</p><p style="color:rgba(255,230,203,.65);font-size:.85rem;line-height:1.7;margin:0 auto 1rem;max-width:660px">Langfuse 是一款开源的可观测性工具，专门用来监控和分析 AI Agent 的运行情况。把它接入 OpenClaw 后，你能看到每一次对话、每一步工具调用的完整追踪——从用户问了什么、Agent 调用了哪些工具、用了哪个模型、花了多少 Token、到响应花了多久。一句话说：<strong style="color:gold">装上它，AI 干活的全过程你都能看得清清楚楚</strong>。</p><div class="oc-eco-actions"><a class="oc-button oc-eco-btn oc-eco-btn--primary" href="https://langfuse.com" target="_blank" rel="noreferrer"><span class="oc-eco-btn__label">访问官网</span><span class="oc-eco-btn__arrow" aria-hidden="true">↗</span></a></div></div><div class="oc-eco-featured-wide__embed"><div style="padding:1rem"><div class="oc-lf-promo"><div class="oc-lf-promo-head"><div class="oc-lf-promo-logo">Lf</div><div class="oc-lf-promo-name"><span>Lang</span>fuse</div></div><div class="oc-lf-promo-body"><div class="oc-lf-promo-visual"><div class="oc-lf-promo-visual-inner"><div class="oc-lf-promo-dots"><div class="oc-lf-promo-dot"></div><div class="oc-lf-promo-dot"></div><div class="oc-lf-promo-dot"></div></div><div class="oc-lf-promo-line w60"></div><div class="oc-lf-promo-line w80"></div><div class="oc-lf-promo-line w100"></div><div class="oc-lf-promo-panel"><div class="oc-lf-promo-panel-row"><span class="key">TRACE</span><span class="val">chat_completion_openai</span></div><div class="oc-lf-promo-panel-row"><span class="key">TOKENS</span><span class="val">1,847 · ↑0.42s · $0.0083</span></div><div class="oc-lf-promo-panel-row"><span class="key">MODEL</span><span class="val">gpt-4o · agent: code-assist</span></div><div class="oc-lf-promo-panel-row"><span class="key">EVAL</span><span class="val">hallucination · 0.94</span></div></div></div></div><div class="oc-lf-promo-right"><h3>看得见的 LLM 质量</h3><p>Trace · 评估 · Prompt 管理 — 一个平台闭环</p><ul class="oc-lf-promo-feats"><li>🔍 完整 Trace 追踪</li><li>📊 在线评估</li><li>📝 Prompt 版本管理</li></ul><ul class="oc-lf-promo-steps"><li>注册</li><li>安装</li><li>配置</li><li>使用</li></ul></div></div></div></div><div class="oc-eco-featured-wide__embedfoot"><span>开源 · MIT</span><span><a href="https://langfuse.com" target="_blank" rel="noreferrer" style="color:gold;text-decoration:none">langfuse.com ↗</a></span></div></div></article>'

# Insert 2: After SCALE OS - unique marker: embedfoot of scale-os + submit section
marker2_old = '</span><span>src: /promos/scale-os.html</span></div></div></article><aside class="oc-cell oc-eco-submit"'
marker2_new = '</span><span>src: /promos/scale-os.html</span></div></div></article>\n\n' + langfuse + '\n\n<aside class="oc-cell oc-eco-submit"'

if marker2_old in html:
    html = html.replace(marker2_old, marker2_new, 1)
    print("Insert 2 (Langfuse): SUCCESS")
else:
    print("Insert 2: FAILED - marker not found")
    # Try shorter marker
    marker2b = '</span></div></div></article><aside class="oc-cell oc-eco-submit"'
    if marker2b in html:
        html = html.replace(marker2b, '</span></div></div></article>\n\n' + langfuse + '\n\n<aside class="oc-cell oc-eco-submit"', 1)
        print("Insert 2 (fallback): SUCCESS")
    else:
        print("Insert 2 fallback: FAILED")

# Insert 3: Full CSS + terminal script
css_block = '''
<script>
(function(){
  var c=document.getElementById("oc-terminal-body"),z=document.getElementById("oc-cursor");if(!c)return;
  var t=['<span style="color:#fb923c">openclaw setup</span>','  选择模型供应商：智谱 / DeepSeek / Qwen / Kimi / MiniMax','  配置工具集：终端、文件、浏览器、记忆、技能、MCP','\\u2713 OpenClaw \\u5df2\\u51c6\\u5907\\u5c31\\u7eea','','<span style="color:#fb923c">openclaw</span>','  \\u5e2e\\u6211\\u6574\\u7406\\u672c\\u5468\\u9879\\u76ee\\u8fdb\\u5c55','  session_search \\u201c\\u9879\\u76ee\\u8fdb\\u5c55\\u201d','  read_file ./AGENTS.md','  web_search \\u201c\\u76f8\\u5173\\u4f9d\\u8d56\\u6700\\u65b0\\u7248\\u672c\\u201d','  feishu_send \\u201c\\u672c\\u5468\\u7b80\\u62a5\\u5df2\\u751f\\u6210\\u201d','','Done.'];
  var h='',i=0,j=0,s=25;
  function n(){if(i>=t.length){if(z)z.style.animation="oc-blink 1s step-end infinite";return}
  var l=t[i];if(j<=l.length){var d=l.substring(0,j),u=\'<span class="oc-cursor" style="animation:oc-blink 1s step-end infinite;display:inline-block;width:8px;height:1em;background:#fb923c;vertical-align:text-bottom"></span>\';c.innerHTML=h+d+u;j++;setTimeout(n,s)}else{h+=l+"\\n";i++;j=0;setTimeout(n,s*3)}}
  c.innerHTML="";n()})();
</script>
<style>
:root{--oc-bg:#041c1c;--oc-cream:#ffe6cb;--oc-cream-muted:rgba(255,230,203,.84);--oc-cream-faint:rgba(255,230,203,.3);--oc-gold:gold;--oc-green:#6ee7b7;--oc-line:rgba(255,230,203,.28);--oc-line-strong:rgba(255,215,0,.52);--oc-font-serif:ui-serif,"Songti SC","STSong","SimSun","Noto Serif CJK SC",serif;--oc-font-mono:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,"Liberation Mono","Courier New",monospace}
html{background:var(--oc-bg)!important}
body{background:0 0!important;color:var(--oc-cream)!important;font-weight:480;letter-spacing:.02em}
.oc-shell{margin:0 auto;padding:2rem;width:min(100%,1600px)}
.oc-eco-grid{border-left:1px solid var(--oc-line);border-top:1px solid var(--oc-line);display:grid;grid-template-columns:repeat(6,minmax(0,1fr))}
.oc-cell{border-bottom:1px solid var(--oc-line);border-right:1px solid var(--oc-line);padding:1.5rem}
.oc-kicker,.oc-eco-hero__kicker{color:var(--oc-cream-muted);font-family:var(--oc-font-mono);font-size:.78rem;letter-spacing:.18em;text-transform:uppercase}
.oc-eco-hero{align-items:center;display:flex;flex-direction:column;grid-column:1/-1;justify-content:center;min-height:74vh;padding:max(3rem,min(8vw,7rem)) 1.5rem;position:relative;text-align:center}
.oc-eco-hero::before{content:"";position:absolute;border-radius:999px;filter:blur(72px);mix-blend-mode:screen;opacity:.56;background:radial-gradient(ellipse at 46% 50%,rgba(255,240,120,.34) 0,rgba(255,224,102,.22) 26%,rgba(181,255,132,.12) 52%,rgba(181,255,132,.04) 68%,transparent 82%);height:min(24vw,18rem);right:-8rem;top:-9rem;width:min(44vw,34rem)}
.oc-eco-hero::after{content:"";position:absolute;border-radius:999px;filter:blur(72px);mix-blend-mode:screen;opacity:.56;background:radial-gradient(ellipse at 54% 48%,rgba(126,247,196,.26) 0,rgba(126,247,196,.16) 28%,rgba(196,255,112,.1) 54%,rgba(196,255,112,.04) 70%,transparent 84%);bottom:-10rem;height:min(26vw,20rem);left:-10rem;width:min(46vw,36rem)}
.oc-eco-hero>*{position:relative;z-index:1}
.oc-eco-hero__title{color:var(--oc-cream);font-family:var(--oc-font-serif);font-size:max(3.2rem,min(8vw,8.2rem));font-weight:900;letter-spacing:-.05em;line-height:.88}
.oc-eco-hero__title em{color:var(--oc-gold);font-style:normal}
.oc-eco-hero__lede{color:var(--oc-cream-muted);font-size:max(1rem,min(1.7vw,1.28rem));line-height:1.8;margin:1.25rem auto 0;max-width:680px}
.oc-eco-section{grid-column:span 2;min-height:250px}
.oc-eco-section__title{color:var(--oc-gold);font-family:var(--oc-font-serif);font-size:1.3rem}
.oc-eco-triage{display:grid;grid-template-columns:repeat(3,1fr);grid-column:1/-1}
.oc-eco-triage__card{display:flex;flex-direction:column;padding:1.5rem;border-right:1px solid var(--oc-line);border-bottom:1px solid var(--oc-line);text-decoration:none!important;color:inherit;min-height:200px}
.oc-eco-triage__num{color:var(--oc-cream-faint);font-family:var(--oc-font-mono);font-size:2rem;font-weight:900}
.oc-eco-triage__card h3{color:var(--oc-gold);font-size:1.08rem;letter-spacing:.08em;text-transform:uppercase}
.oc-eco-triage__card p{color:var(--oc-cream-muted);line-height:1.78;font-size:.92rem}
.oc-eco-triage__jump{color:var(--oc-gold);font-family:var(--oc-font-mono);font-size:.78rem;letter-spacing:.12em;margin-top:auto;text-transform:uppercase}
.oc-eco-pills{display:flex;flex-wrap:wrap;gap:.6rem;margin-bottom:1rem}
.oc-eco-pill{align-items:center;background:rgba(255,215,0,.04);border:1px solid var(--oc-line-strong);border-radius:999px;color:var(--oc-cream);display:inline-flex;font-family:var(--oc-font-mono);font-size:.72rem;padding:.35rem .7rem}
.oc-eco-pill--type{color:var(--oc-gold)}
.oc-eco-pill--stable{color:var(--oc-green);border-color:rgba(110,231,183,.35)}
.oc-eco-actions{display:flex;flex-wrap:wrap;gap:.8rem;margin-top:2rem}
.oc-eco-btn{align-items:center;background:rgba(255,215,0,.04);border:1px solid var(--oc-line-strong);color:var(--oc-gold);display:inline-flex;font-family:var(--oc-font-mono);font-size:.82rem;letter-spacing:.12em;min-height:44px;padding:.72rem 1rem;text-transform:uppercase;text-decoration:none!important}
.oc-eco-btn:hover{border-color:var(--oc-gold);background:rgba(255,215,0,.08)}
.oc-eco-btn--primary{background:var(--oc-gold);border-color:var(--oc-gold);color:var(--oc-bg)}
.oc-eco-btn--survey{background:var(--oc-green);border-color:var(--oc-green);color:var(--oc-bg)}
.oc-eco-bullets{list-style:none;padding:0;color:var(--oc-cream-muted)}
.oc-eco-bullets li{padding:.35rem 0 .35rem 1.5rem;position:relative;font-size:.92rem}
.oc-eco-bullets li::before{content:"\\u25cf";position:absolute;left:0;color:var(--oc-gold);font-size:.6rem;top:.5rem}
.oc-eco-meta{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem}
.oc-eco-meta__k{color:var(--oc-cream-faint);font-family:var(--oc-font-mono);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase}
.oc-eco-meta__v{color:var(--oc-cream-muted);font-size:.9rem}
.oc-eco-featured{grid-column:span 3;min-height:350px;display:flex;flex-wrap:wrap}
.oc-eco-featured__media{flex:1 1 45%;padding:1rem}
.oc-eco-featured__body{flex:1 1 55%;padding:1rem}
.oc-eco-featured__title{color:var(--oc-gold);font-family:var(--oc-font-serif);font-size:1.6rem;font-weight:900}
.oc-eco-featured__tagline{color:var(--oc-cream-muted);font-size:.95rem;line-height:1.78;max-width:520px}
.oc-eco-featured__caption{display:block;color:var(--oc-cream-faint);font-size:.78rem;font-family:var(--oc-font-mono);text-transform:uppercase}
.oc-eco-featured__image{width:100%;border-radius:8px;border:1px solid var(--oc-line);display:block}
.oc-eco-featured-wide{grid-column:1/-1;background:rgba(255,215,0,.025);border-color:var(--oc-line-strong)}
.oc-eco-featured-wide__head{border-bottom:1px solid var(--oc-line);padding:2.4rem 2rem 1.6rem;text-align:center}
.oc-eco-featured-wide__title{color:var(--oc-cream);font-family:var(--oc-font-serif);font-size:2rem;font-weight:900}
.oc-eco-featured-wide__tagline{color:var(--oc-cream-muted);font-size:1rem;line-height:1.78;max-width:72ch;margin:0 auto}
.oc-eco-featured-wide__embed{background:var(--oc-bg);border:1px solid var(--oc-line);border-radius:12px}
.oc-eco-upcoming{background:repeating-linear-gradient(135deg,rgba(255,230,203,.04) 0 12px,transparent 12px 24px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);padding:0}
.oc-eco-upcoming::before{background:var(--oc-cream);color:var(--oc-bg);content:"Public Beta";font-family:var(--oc-font-mono);font-size:.7rem;font-weight:700;padding:.34rem .8rem;position:absolute;top:0}
.oc-eco-desktop{background:radial-gradient(circle at 16% 18%,rgba(255,122,45,.13),transparent 30%),radial-gradient(circle at 84% 12%,rgba(110,231,183,.12),transparent 32%),linear-gradient(135deg,rgba(0,26,24,.96),rgba(1,18,22,.96));border-color:rgba(255,215,0,.34);overflow:hidden}
.oc-eco-desktop__hero{border-bottom:1px solid rgba(255,230,203,.14);display:grid;grid-template-columns:minmax(0,1.08fr) minmax(0,.92fr)}
.oc-eco-desktop__copy{background:linear-gradient(180deg,rgba(255,215,0,.07),transparent 48%),rgba(0,0,0,.1);border-right:1px solid rgba(255,230,203,.14);padding:max(2.6rem,min(4vw,3.4rem)) max(1.8rem,min(3vw,2.6rem)) 2rem}
.oc-eco-desktop .oc-eco-featured__title{font-size:max(2.2rem,min(4vw,3.25rem))}
.oc-eco-desktop__gallery{display:grid;gap:1rem;padding:2rem}
.oc-eco-desktop__image{border-color:rgba(255,230,203,.18);border-radius:10px;width:100%}
.oc-eco-desktop__progress-row{display:grid;grid-template-columns:minmax(300px,.82fr) minmax(0,1.18fr);gap:1rem;background:rgba(0,0,0,.08);padding:1.25rem}
.oc-eco-survey{background:rgba(110,231,183,.06);border:1px solid rgba(110,231,183,.18);border-radius:8px;margin-top:1.2rem;padding:1rem}
.oc-eco-survey-impact{background:rgba(0,0,0,.12);border:1px solid rgba(255,230,203,.14);border-radius:10px;margin-top:1rem;padding:1.15rem}
.oc-eco-survey-impact__grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem}
.oc-eco-survey-impact__item{background:rgba(0,0,0,.14);border:1px solid rgba(255,230,203,.13);border-radius:8px;padding:.8rem .9rem}
.oc-eco-progress{background:radial-gradient(circle at top right,rgba(255,215,0,.12),transparent 38%),linear-gradient(135deg,rgba(255,215,0,.08),rgba(110,231,183,.055) 48%,rgba(0,0,0,.18));border:1px solid rgba(255,215,0,.28);border-radius:10px;padding:1.1rem}
.oc-eco-submit{background:linear-gradient(135deg,rgba(110,231,183,.08),transparent 70%);grid-column:span 3;display:flex;align-items:center}
.oc-eco-submit__body{padding:3rem 2rem;text-align:center}
.oc-eco-submit__title{color:var(--oc-cream);font-family:var(--oc-font-serif);font-size:1.6rem;font-weight:900}
.oc-eco-check-list li::before{color:var(--oc-green);content:"\\u2713"}
.oc-eco-email{color:var(--oc-gold);font-family:var(--oc-font-mono);font-size:.95rem;border-bottom:1px dashed rgba(255,215,0,.5);text-decoration:none!important}
.oc-lf-promo{max-width:720px;margin:0 auto;padding:2rem;text-align:center}
.oc-lf-promo-logo{width:48px;height:48px;background:linear-gradient(135deg,gold,#e6c200);border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:20px;color:#041c1c}
.oc-lf-promo-name{font-size:28px;font-weight:800;color:var(--oc-cream);font-family:var(--oc-font-serif)}
.oc-lf-promo-name span{color:gold}
.oc-footer{background:linear-gradient(180deg,rgba(4,28,28,0),rgba(2,17,17,.85) 22%,#021111 62%,#010808);border-top:1px solid rgba(255,215,0,.42);padding:48px 0 28px}
.oc-footer__epigraph-zh{color:var(--oc-cream);font-family:var(--oc-font-serif);font-size:max(28px,min(4.6vw,58px));font-weight:700}
.oc-footer__cta-btn--primary{background:var(--oc-gold);border:1px solid var(--oc-gold);color:#0b0b0b;padding:12px 24px}
.oc-footer__cta-btn--ghost{background:0 0;border:1px solid rgba(255,230,203,.42);color:var(--oc-cream);padding:12px 24px}
.oc-footer__link{color:var(--oc-cream-muted);font-size:15px;text-decoration:none!important}
code,pre{font-weight:500}
</style>
'''

# Replace the last script+style block
last_script = html.rfind('<script>')
if last_script > 0:
    before = html[:last_script]
    # Keep everything before the old script, add new content
    html = before + css_block
    print("CSS replacement: SUCCESS")
else:
    print("CSS replacement: FAILED")

# Write
with open("dist/practice-guides/index.html", "w", encoding="utf-8") as f:
    f.write(html)

size = os.path.getsize("dist/practice-guides/index.html")
print(f"\nWritten: {size} bytes")

# Verify - count sections
sections = ['oc-eco-hero', 'oc-eco-desktop', 'hermes-webui-cn', 'openclaw-web-control-ui', 'scale-os', 'langfuse', 'oc-eco-submit', 'oc-footer']
for s in sections:
    count = html.count(s)
    ok = "OK" if count == 1 else "DUPLICATE!"
    print(f"  {s}: {count} {ok}")

print(f"CSS vars: {'--oc-bg:#041c1c' in html}")
print(f"Terminal: {'oc-terminal-body' in html}")
