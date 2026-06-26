"""
OpenClaw 目录重构 v2 — 完整变换
"""
import json, os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/docs-config-new.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# ===== 1. 删除技能系统分类 =====
config = [item for item in config if item.get('label') not in ('技能系统', '内置技能', '可选技能')]

# ===== 2. 删除 Hermes 特有的指南 =====
hermes_guides = [
    "Run Nemotron 3 Ultra free in Hermes Agent",
    "Run Hermes Agent with Nous Portal",
    "Run Local LLMs on Mac",
    "Tutorial: Build a Daily Briefing Bot",
    "Using Hermes as a Python Library",
    "Use SOUL.md with Hermes",
    "Use Voice Mode with Hermes",
    "Build a Hermes Plugin",
    "Tutorial: Build a GitHub PR Review Agent",
    "Automated GitHub PR Comments with Webhooks",
    "AWS Bedrock",
    "Microsoft Foundry",
    "xAI Grok OAuth (SuperGrok / X Premium+)",
    "OAuth over SSH / Remote Hosts",
    "Register a Microsoft Graph Application",
    "Operate the Teams Meeting Pipeline",
    "Script-Only Cron Jobs",
    "Cron Troubleshooting",
    "Set Up a Team Telegram Assistant",
    "Tips & Best Practices",
    "Working with Skills",
    "Delegation & Parallel Work",
    "Automate Anything with Cron",
    "Use MCP with Hermes",
    "Run Hermes Locally with Ollama",
    "Migrate from OpenClaw",
    "Pipe Script Output to Messaging Platforms",
]

def remove_hermes_items(items, depth=0):
    """递归删除 Hermes 特有页面"""
    result = []
    for item in items:
        if item['type'] == 'link' and item.get('label') in hermes_guides:
            continue
        if item['type'] == 'category':
            label = item.get('label', '')
            if label in ('Guides & Tutorials', '指南与教程'):
                item['items'] = remove_hermes_items(item['items'], depth+1)
            elif 'items' in item:
                item['items'] = remove_hermes_items(item['items'], depth+1)
        result.append(item)
    return result

config = remove_hermes_items(config)

# ===== 3. 替换版本发布为 OpenClaw 版本 =====
openclaw_versions = [
    {"type": "link", "label": "v2026.6.10", "href": "/docs/releases/v2026.6.10/"},
    {"type": "link", "label": "v2026.6.9", "href": "/docs/releases/v2026.6.9/"},
    {"type": "link", "label": "v2026.6.8", "href": "/docs/releases/v2026.6.8/"},
    {"type": "link", "label": "v2026.6.7 Beta.1", "href": "/docs/releases/v2026.6.7-beta.1/"},
    {"type": "link", "label": "v2026.6.6", "href": "/docs/releases/v2026.6.6/"},
    {"type": "link", "label": "v2026.6.5", "href": "/docs/releases/v2026.6.5/"},
]

for item in config:
    if item.get('label') in ('版本发布', 'Release Notes') and item['type'] == 'category':
        # 保留 Hermes 版本中能对应到 OpenClaw 的
        filtered = []
        for sub in item.get('items', []):
            label = sub.get('label', '')
            # 只保留名字匹配的版本
            for ov in openclaw_versions:
                if ov['label'] == label:
                    filtered.append(ov)
                    break
        item['items'] = filtered

# ===== 4. 添加 OpenClaw 技能分类 =====
openclaw_skills = [
    {"type": "link", "label": "ClawHub 市场指南", "href": "/docs/skills/clawhub/"},
    {"type": "link", "label": "GitHub 代码管理", "href": "/docs/skills/github/"},
    {"type": "link", "label": "Coding Agent 编码助手", "href": "/docs/skills/coding-agent/"},
    {"type": "link", "label": "GitHub Issues 管理", "href": "/docs/skills/gh-issues/"},
    {"type": "link", "label": "1Password 密码管理", "href": "/docs/skills/1password/"},
    {"type": "link", "label": "Notion 笔记", "href": "/docs/skills/notion/"},
    {"type": "link", "label": "Obsidian 笔记", "href": "/docs/skills/obsidian/"},
    {"type": "link", "label": "Bear Notes", "href": "/docs/skills/bear-notes/"},
    {"type": "link", "label": "Apple Notes", "href": "/docs/skills/apple-notes/"},
    {"type": "link", "label": "Apple Reminders", "href": "/docs/skills/apple-reminders/"},
    {"type": "link", "label": "Canvas 画布", "href": "/docs/skills/canvas/"},
    {"type": "link", "label": "Meme Maker 表情包制作", "href": "/docs/skills/meme-maker/"},
    {"type": "link", "label": "Spotify 音乐播放", "href": "/docs/skills/spotify-player/"},
    {"type": "link", "label": "Discord 通知", "href": "/docs/skills/discord/"},
    {"type": "link", "label": "Slack 通知", "href": "/docs/skills/slack/"},
    {"type": "link", "label": "Voice Call 语音通话", "href": "/docs/skills/voice-call/"},
    {"type": "link", "label": "天气查询", "href": "/docs/skills/weather/"},
    {"type": "link", "label": "待办事项管理", "href": "/docs/skills/trello/"},
    {"type": "link", "label": "任务流 Taskflow", "href": "/docs/skills/taskflow/"},
    {"type": "link", "label": "Inbox 邮件整理", "href": "/docs/skills/taskflow-inbox-triage/"},
    {"type": "link", "label": "Nano PDF 编辑", "href": "/docs/skills/nano-pdf/"},
    {"type": "link", "label": "终端复用 Tmux", "href": "/docs/skills/tmux/"},
    {"type": "link", "label": "Node 远程连接", "href": "/docs/skills/node-connect/"},
    {"type": "link", "label": "Node 调试器", "href": "/docs/skills/node-inspect-debugger/"},
    {"type": "link", "label": "Python 调试", "href": "/docs/skills/python-debugpy/"},
    {"type": "link", "label": "Spike 原型验证", "href": "/docs/skills/spike/"},
    {"type": "link", "label": "Himalaya 邮件", "href": "/docs/skills/himalaya/"},
    {"type": "link", "label": "OpenAI Whisper 语音转文字", "href": "/docs/skills/openai-whisper/"},
    {"type": "link", "label": "Sherpa TTS 语音合成", "href": "/docs/skills/sherpa-onnx-tts/"},
    {"type": "link", "label": "Diagram Maker 图表制作", "href": "/docs/skills/diagram-maker/"},
    {"type": "link", "label": "视频帧提取", "href": "/docs/skills/video-frames/"},
    {"type": "link", "label": "GIF 搜索", "href": "/docs/skills/gifgrep/"},
    {"type": "link", "label": "Blogwatcher RSS 监控", "href": "/docs/skills/blogwatcher/"},
    {"type": "link", "label": "健康检查", "href": "/docs/skills/healthcheck/"},
    {"type": "link", "label": "会话日志", "href": "/docs/skills/session-logs/"},
    {"type": "link", "label": "Skill 创建器", "href": "/docs/skills/skill-creator/"},
    {"type": "link", "label": "Browser Automation 浏览器自动化", "href": "/docs/skills/browser-automation/"},
    {"type": "link", "label": "Tavily 网页搜索", "href": "/docs/skills/tavily/"},
]

# 插入到 OpenClaw 专属后面（第2个位置）
config.insert(1, {
    "type": "category",
    "label": "技能与插件",
    "collapsed": False,
    "items": openclaw_skills
})

# ===== 5. 写入最终配置 =====
with open('dist/docs-config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# 统计
def count_items(items):
    cats = 0
    pages = 0
    for item in items:
        if item['type'] == 'category':
            cats += 1
            c, p = count_items(item.get('items', []))
            cats += c
            pages += p
        else:
            pages += 1
    return cats, pages

cats, pages = count_items(config)
print(f"✅ 最终目录已生成: dist/docs-config.json")
print(f"   分类: {cats}, 页面: {pages}")
print(f"   包含 OpenClaw 技能: {len(openclaw_skills)} 个")
print(f"   保留 Hermes 特有标注: 8 个 [+手动实现]")
