"""Restore all guides to config"""
import json, os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/docs-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('dist/docs-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

paths = set(k.replace('\\', '/') for k in articles)

# All guide pages with Chinese labels
all_guides = [
    ("使用技巧", "/docs/guides/tips/"),
    ("MCP 使用指南", "/docs/guides/use-mcp-with-hermes/"),
    ("SOUL.md 使用指南", "/docs/guides/use-soul-with-hermes/"),
    ("语音模式使用指南", "/docs/guides/use-voice-mode-with-hermes/"),
    ("Cron 自动化指南", "/docs/guides/automate-with-cron/"),
    ("技能使用指南", "/docs/guides/work-with-skills/"),
    ("委托与并行指南", "/docs/guides/delegation-patterns/"),
    ("Automation Blueprints", "/docs/guides/automation-blueprints/"),
    ("Cron 脚本模式", "/docs/guides/cron-script-only/"),
    ("Cron 故障排查", "/docs/guides/cron-troubleshooting/"),
    ("每日简报机器人教程", "/docs/guides/daily-briefing-bot/"),
    ("GitHub PR 审查 Agent", "/docs/guides/github-pr-review-agent/"),
    ("Webhook GitHub PR 评论", "/docs/guides/webhook-github-pr-review/"),
    ("Google Gemini 集成", "/docs/guides/google-gemini/"),
    ("Azure Foundry", "/docs/guides/azure-foundry/"),
    ("本地 Ollama 部署", "/docs/guides/local-ollama-setup/"),
    ("本地 LLM (Mac)", "/docs/guides/local-llm-on-mac/"),
    ("MiniMax OAuth", "/docs/guides/minimax-oauth/"),
    ("xAI Grok OAuth", "/docs/guides/xai-grok-oauth/"),
    ("OAuth over SSH", "/docs/guides/oauth-over-ssh/"),
    ("AWS Bedrock", "/docs/guides/aws-bedrock/"),
    ("Microsoft Graph 注册", "/docs/guides/microsoft-graph-app-registration/"),
    ("Teams 会议流水线", "/docs/guides/operate-teams-meeting-pipeline/"),
    ("Telegram 团队助手", "/docs/guides/team-telegram-assistant/"),
    ("Python 库方式使用", "/docs/guides/python-library/"),
    ("脚本输出到消息平台", "/docs/guides/pipe-script-output/"),
    ("从 OpenClaw 迁移", "/docs/guides/migrate-from-openclaw/"),
    ("构建 Hermes 插件", "/docs/guides/build-a-hermes-plugin/"),
    ("Hermes + Nous Portal", "/docs/guides/run-hermes-with-nous-portal/"),
    ("Nemotron 3 Ultra 免费运行", "/docs/guides/run-nemotron-3-ultra-free/"),
]

# 找到 指南与教程  section
for item in config:
    if item.get('label') == '指南与教程' and item['type'] == 'category':
        item['items'] = []
        for label, href in all_guides:
            if href in paths:
                item['items'].append({"type": "link", "label": label, "href": href})
        print(f"指南与教程: {len(item['items'])} 项")
        break

with open('dist/docs-config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

def count(items):
    c,p=0,0
    for i in items:
        if i['type']=='category':
            c+=1
            cc,pp=count(i.get('items',[]))
            c+=cc;p+=pp
        else:
            p+=1
    return c,p
c,p=count(config)
print(f"✅ 完成: 分类={c}, 页面={p}")
