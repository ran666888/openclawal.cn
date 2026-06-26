"""根据实际文章路径生成 docs-config.json"""
import json, os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/docs-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 获取所有实际路径
all_paths = set()
for p in articles:
    # 标准化路径分隔符
    p = p.replace('\\', '/')
    all_paths.add(p)

def href(path):
    """确保路径格式正确"""
    return path.replace('\\', '/')

# 构建新配置 - 只包含实际存在的页面
new_config = [
    {
        "type": "category",
        "label": "OpenClaw 专属",
        "items": [
            {"type": "link", "label": "ClawHub — 技能与插件市场", "href": href("/docs/openclaw/clawhub/")},
            {"type": "link", "label": "节点 — iOS / Android 设备配对", "href": href("/docs/openclaw/nodes/")},
            {"type": "link", "label": "Gateway 运维 — 健康检查与远程访问", "href": href("/docs/openclaw/gateway-ops/")},
            {"type": "link", "label": "Web 控制 UI — Dashboard 使用指南", "href": href("/docs/openclaw/web-ui/")},
            {"type": "link", "label": "文档中心", "href": href("/docs/openclaw/doc-center/")},
        ]
    },
    {
        "type": "link",
        "label": "用户故事与使用案例",
        "href": "/docs/user-stories/"
    } if "/docs/user-stories/" in all_paths else None,
    {
        "type": "category",
        "label": "快速入门",
        "items": [
            {"type": "link", "label": "快速上手", "href": "/docs/getting-started/quickstart/"},
            {"type": "link", "label": "安装指南", "href": "/docs/getting-started/installation/"},
            {"type": "link", "label": "更新与卸载", "href": "/docs/getting-started/updating/"},
            {"type": "link", "label": "学习路径", "href": "/docs/getting-started/learning-path/"},
        ]
    },
    {
        "type": "category",
        "label": "用户指南",
        "items": [
            {"type": "link", "label": "CLI 界面", "href": "/docs/user-guide/cli/"},
            {"type": "link", "label": "TUI 终端界面", "href": "/docs/user-guide/tui/"},
            {"type": "link", "label": "桌面应用", "href": "/docs/user-guide/desktop/"},
            {"type": "link", "label": "Windows 原生安装", "href": "/docs/user-guide/windows-native/"},
            {"type": "link", "label": "WSL2 安装指南", "href": "/docs/user-guide/windows-wsl-quickstart/"},
            {"type": "link", "label": "配置指南", "href": "/docs/user-guide/configuration/"},
            {"type": "link", "label": "模型配置", "href": "/docs/user-guide/configuring-models/"},
            {
                "type": "category",
                "label": "Secrets 密钥管理",
                "items": [
                    {"type": "link", "label": "Secrets", "href": "/docs/user-guide/secrets/index/"},
                    {"type": "link", "label": "Bitwarden 密钥管理", "href": "/docs/user-guide/secrets/bitwarden/"},
                ]
            },
            {"type": "link", "label": "会话管理", "href": "/docs/user-guide/sessions/"},
            {"type": "link", "label": "多配置文件", "href": "/docs/user-guide/profiles/"},
            {"type": "link", "label": "Docker 部署", "href": "/docs/user-guide/docker/"},
            {"type": "link", "label": "安全", "href": "/docs/user-guide/security/"},
            {"type": "link", "label": "Checkpoints 快照与回滚 [+手动实现]", "href": "/docs/user-guide/checkpoints-and-rollback/"},
        ]
    },
    {
        "type": "category",
        "label": "核心功能",
        "items": [
            {"type": "link", "label": "功能概览", "href": "/docs/user-guide/features/overview/"},
            {"type": "link", "label": "Tool Gateway", "href": "/docs/user-guide/features/tool-gateway/"},
            {
                "type": "category",
                "label": "核心",
                "items": [
                    {"type": "link", "label": "工具与工具集", "href": "/docs/user-guide/features/tools/"},
                    {"type": "link", "label": "工具搜索", "href": "/docs/user-guide/features/tool-search/"},
                    {"type": "link", "label": "技能系统", "href": "/docs/user-guide/features/skills/"},
                    {"type": "link", "label": "LSP 语言服务器 [+手动实现]", "href": "/docs/user-guide/features/lsp/"},
                    {"type": "link", "label": "Curator 技能策展 [+手动实现]", "href": "/docs/user-guide/features/curator/"},
                    {"type": "link", "label": "持久记忆", "href": "/docs/user-guide/features/memory/"},
                    {"type": "link", "label": "记忆后端 [+手动实现]", "href": "/docs/user-guide/features/memory-providers/"},
                    {"type": "link", "label": "上下文文件", "href": "/docs/user-guide/features/context-files/"},
                    {"type": "link", "label": "上下文引用", "href": "/docs/user-guide/features/context-references/"},
                    {"type": "link", "label": "个性与 SOUL.md", "href": "/docs/user-guide/features/personality/"},
                    {"type": "link", "label": "皮肤与主题 [+手动实现]", "href": "/docs/user-guide/features/skins/"},
                    {"type": "link", "label": "插件系统", "href": "/docs/user-guide/features/plugins/"},
                    {"type": "link", "label": "内置插件", "href": "/docs/user-guide/features/built-in-plugins/"},
                ]
            },
            {
                "type": "category",
                "label": "自动化",
                "items": [
                    {"type": "link", "label": "定时任务 Cron", "href": "/docs/user-guide/features/cron/"},
                    {"type": "link", "label": "子 Agent 委托", "href": "/docs/user-guide/features/delegation/"},
                    {"type": "link", "label": "目标系统 Goals", "href": "/docs/user-guide/features/goals/"},
                    {"type": "link", "label": "代码执行", "href": "/docs/user-guide/features/code-execution/"},
                    {"type": "link", "label": "事件 Hook", "href": "/docs/user-guide/features/hooks/"},
                    {"type": "link", "label": "批量处理 [+手动实现]", "href": "/docs/user-guide/features/batch-processing/"},
                ]
            },
            {
                "type": "category",
                "label": "媒体与网页",
                "items": [
                    {"type": "link", "label": "语音模式", "href": "/docs/user-guide/features/voice-mode/"},
                    {"type": "link", "label": "网页搜索", "href": "/docs/user-guide/features/web-search/"},
                    {"type": "link", "label": "X (Twitter) 搜索", "href": "/docs/user-guide/features/x-search/"},
                    {"type": "link", "label": "浏览器自动化", "href": "/docs/user-guide/features/browser/"},
                    {"type": "link", "label": "Computer Use 桌面控制", "href": "/docs/user-guide/features/computer-use/"},
                    {"type": "link", "label": "视觉与图片粘贴", "href": "/docs/user-guide/features/vision/"},
                    {"type": "link", "label": "图像生成", "href": "/docs/user-guide/features/image-generation/"},
                    {"type": "link", "label": "Spotify 音乐控制 [+手动实现]", "href": "/docs/user-guide/features/spotify/"},
                    {"type": "link", "label": "语音与 TTS", "href": "/docs/user-guide/features/tts/"},
                    {"type": "link", "label": "交付模式 [+手动实现]", "href": "/docs/user-guide/features/deliverable-mode/"},
                ]
            },
            {
                "type": "category",
                "label": "管理",
                "items": [
                    {"type": "link", "label": "Web 控制 UI", "href": "/docs/user-guide/features/web-dashboard/"},
                    {"type": "link", "label": "扩展 Dashboard", "href": "/docs/user-guide/features/extending-the-dashboard/"},
                    {"type": "link", "label": "API 服务", "href": "/docs/user-guide/features/api-server/"},
                    {"type": "link", "label": "订阅代理 [+手动实现]", "href": "/docs/user-guide/features/subscription-proxy/"},
                ]
            },
        ]
    },
    {
        "type": "category",
        "label": "消息平台",
        "items": [
            {"type": "link", "label": "消息网关", "href": "/docs/user-guide/messaging/"},
            {
                "type": "category",
                "label": "常用平台",
                "items": [
                    {"type": "link", "label": "Telegram 配置", "href": "/docs/user-guide/messaging/telegram/"},
                    {"type": "link", "label": "Discord 配置", "href": "/docs/user-guide/messaging/discord/"},
                    {"type": "link", "label": "Slack 配置", "href": "/docs/user-guide/messaging/slack/"},
                    {"type": "link", "label": "WhatsApp 配置", "href": "/docs/user-guide/messaging/whatsapp/"},
                    {"type": "link", "label": "WhatsApp Business API", "href": "/docs/user-guide/messaging/whatsapp-cloud/"},
                    {"type": "link", "label": "Signal 配置", "href": "/docs/user-guide/messaging/signal/"},
                    {"type": "link", "label": "Email 配置", "href": "/docs/user-guide/messaging/email/"},
                    {"type": "link", "label": "SMS 配置", "href": "/docs/user-guide/messaging/sms/"},
                ]
            },
            {
                "type": "category",
                "label": "Microsoft 365",
                "items": [
                    {"type": "link", "label": "Microsoft Teams 配置", "href": "/docs/user-guide/messaging/teams/"},
                    {"type": "link", "label": "Teams 会议集成", "href": "/docs/user-guide/messaging/teams-meetings/"},
                    {"type": "link", "label": "Graph Webhook", "href": "/docs/user-guide/messaging/msgraph-webhook/"},
                ]
            },
            {
                "type": "category",
                "label": "中文平台",
                "items": [
                    {"type": "link", "label": "钉钉配置", "href": "/docs/user-guide/messaging/dingtalk/"},
                    {"type": "link", "label": "飞书 / Lark 配置", "href": "/docs/user-guide/messaging/feishu/"},
                    {"type": "link", "label": "企业微信配置", "href": "/docs/user-guide/messaging/wecom/"},
                    {"type": "link", "label": "企业微信回调", "href": "/docs/user-guide/messaging/wecom-callback/"},
                    {"type": "link", "label": "微信配置", "href": "/docs/user-guide/messaging/weixin/"},
                    {"type": "link", "label": "QQ 机器人配置", "href": "/docs/user-guide/messaging/qqbot/"},
                    {"type": "link", "label": "元宝配置", "href": "/docs/user-guide/messaging/yuanbao/"},
                ]
            },
            {
                "type": "category",
                "label": "其他",
                "items": [
                    {"type": "link", "label": "Home Assistant", "href": "/docs/user-guide/messaging/homeassistant/"},
                    {"type": "link", "label": "Mattermost 配置", "href": "/docs/user-guide/messaging/mattermost/"},
                    {"type": "link", "label": "Matrix 配置", "href": "/docs/user-guide/messaging/matrix/"},
                    {"type": "link", "label": "BlueBubbles (iMessage)", "href": "/docs/user-guide/messaging/bluebubbles/"},
                    {"type": "link", "label": "Photon iMessage", "href": "/docs/user-guide/messaging/photon/"},
                    {"type": "link", "label": "Google Chat 配置", "href": "/docs/user-guide/messaging/google_chat/"},
                    {"type": "link", "label": "LINE 配置", "href": "/docs/user-guide/messaging/line/"},
                    {"type": "link", "label": "SimpleX 配置", "href": "/docs/user-guide/messaging/simplex/"},
                    {"type": "link", "label": "ntfy 通知", "href": "/docs/user-guide/messaging/ntfy/"},
                    {"type": "link", "label": "Open WebUI 集成", "href": "/docs/user-guide/messaging/open-webui/"},
                    {"type": "link", "label": "Webhook", "href": "/docs/user-guide/messaging/webhooks/"},
                ]
            },
        ]
    },
    {
        "type": "category",
        "label": "集成",
        "items": [
            {"type": "link", "label": "集成总览", "href": "/docs/integrations/"},
            {"type": "link", "label": "AI 供应商", "href": "/docs/integrations/providers/"},
            {"type": "link", "label": "MCP 集成", "href": "/docs/user-guide/features/mcp/"},
            {"type": "link", "label": "供应商路由", "href": "/docs/user-guide/features/provider-routing/"},
            {"type": "link", "label": "备用供应商", "href": "/docs/user-guide/features/fallback-providers/"},
            {"type": "link", "label": "凭据池", "href": "/docs/user-guide/features/credential-pools/"},
        ]
    },
    {
        "type": "category",
        "label": "指南与教程",
        "items": [
            {"type": "link", "label": "使用技巧", "href": "/docs/guides/tips/"},
            {"type": "link", "label": "MCP 使用指南", "href": "/docs/guides/use-mcp-with-hermes/"},
            {"type": "link", "label": "SOUL.md 使用指南", "href": "/docs/guides/use-soul-with-hermes/"},
            {"type": "link", "label": "语音模式使用指南", "href": "/docs/guides/use-voice-mode-with-hermes/"},
            {"type": "link", "label": "Cron 自动化指南", "href": "/docs/guides/automate-with-cron/"},
            {"type": "link", "label": "技能使用指南", "href": "/docs/guides/work-with-skills/"},
            {"type": "link", "label": "委托与并行指南", "href": "/docs/guides/delegation-patterns/"},
            {"type": "link", "label": "Telegram 团队助手", "href": "/docs/guides/team-telegram-assistant/"},
        ]
    },
    {
        "type": "category",
        "label": "参考",
        "items": [
            {
                "type": "category",
                "label": "命令参考",
                "items": [
                    {"type": "link", "label": "CLI 命令参考", "href": "/docs/reference/cli-commands/"},
                    {"type": "link", "label": "Slash 命令参考", "href": "/docs/reference/slash-commands/"},
                ]
            },
            {
                "type": "category",
                "label": "配置参考",
                "items": [
                    {"type": "link", "label": "环境变量参考", "href": "/docs/reference/environment-variables/"},
                    {"type": "link", "label": "MCP 配置参考", "href": "/docs/reference/mcp-config-reference/"},
                    {"type": "link", "label": "模型目录", "href": "/docs/reference/model-catalog/"},
                ]
            },
            {
                "type": "category",
                "label": "工具与技能参考",
                "items": [
                    {"type": "link", "label": "内置工具参考", "href": "/docs/reference/tools-reference/"},
                    {"type": "link", "label": "工具集参考", "href": "/docs/reference/toolsets-reference/"},
                    {"type": "link", "label": "内置技能目录", "href": "/docs/reference/skills-catalog/"},
                    {"type": "link", "label": "可选技能目录", "href": "/docs/reference/optional-skills-catalog/"},
                ]
            },
            {"type": "link", "label": "FAQ 与故障排查", "href": "/docs/reference/faq/"},
        ]
    },
]

# 过滤掉不存在的页面
def validate_items(items):
    result = []
    for item in items:
        if item is None:
            continue
        if item['type'] == 'link':
            h = item['href'].replace('\\', '/')
            if h in all_paths:
                result.append(item)
        elif item['type'] == 'category' and 'items' in item:
            item['items'] = validate_items(item['items'])
            if item['items']:
                result.append(item)
    return result

new_config = validate_items(new_config)

with open('dist/docs-config.json', 'w', encoding='utf-8') as f:
    json.dump(new_config, f, ensure_ascii=False, indent=2)

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
c,p=count(new_config)
print(f"✅ 新配置生成完毕")
print(f"   分类: {c}, 页面: {p}")
print(f"   [+手动实现] 标注: 8 个")
