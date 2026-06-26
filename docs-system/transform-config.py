"""
OpenClaw 文档目录重构脚本
读取当前 docs-config.json → 应用新结构 → 写入
"""
import json, os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/docs-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# ===== 中文标签映射表 =====
LABEL_MAP = {
    # OpenClaw 专属
    "ClawHub — Skills & Plugins Marketplace": "ClawHub — 技能与插件市场",
    "Nodes — iOS / Android Device Pairing": "节点 — iOS / Android 设备配对",
    "Gateway Operations — Health, Remote Access & Tailscale": "Gateway 运维 — 健康检查与远程访问",
    "Web Control UI — Dashboard Guide": "Web 控制 UI — Dashboard 使用指南",
    "Documentation Center": "文档中心",
    "User Stories": "用户故事与使用案例",
    
    # 快速入门
    "Quickstart": "快速上手",
    "Installation": "安装指南",
    "Updating & Uninstalling": "更新与卸载",
    "Learning Path": "学习路径",
    
    # 用户指南
    "CLI Interface": "CLI 界面",
    "TUI": "TUI 终端界面",
    "Desktop App": "桌面应用",
    "Windows (Native) Guide": "Windows 原生安装",
    "Windows (WSL2) Guide": "WSL2 安装指南",
    "Configuration": "配置指南",
    "Configuring Models": "模型配置",
    "Sessions": "会话管理",
    "Profiles: Running Multiple Agents": "多配置文件",
    "Hermes Agent — Docker": "Docker 部署",
    "Security": "安全",
    "Checkpoints and `/rollback`": "Checkpoints 快照与回滚 [+手动实现]",
    
    # 核心功能
    "Features Overview": "功能概览",
    "Nous Tool Gateway": "Tool Gateway",
    "Tools & Toolsets": "工具与工具集",
    "Tool Search": "工具搜索",
    "Skills System": "技能系统",
    "Language Server Protocol (LSP)": "LSP 语言服务器 [+手动实现]",
    "Curator": "Curator 技能策展 [+手动实现]",
    "Persistent Memory": "持久记忆",
    "Memory Providers": "记忆后端 [+手动实现]",
    "Context Files": "上下文文件",
    "Context References": "上下文引用",
    "Personality & SOUL.md": "个性与 SOUL.md",
    "Skins & Themes": "皮肤与主题 [+手动实现]",
    "Plugins": "插件系统",
    "Built-in Plugins": "内置插件",
    "Scheduled Tasks (Cron)": "定时任务 Cron",
    "Subagent Delegation": "子 Agent 委托",
    "Persistent Goals (`/goal`)": "目标系统 Goals",
    "Code Execution (Programmatic Tool Calling)": "代码执行",
    "Event Hooks": "事件 Hook",
    "Batch Processing": "批量处理 [+手动实现]",
    "Voice Mode": "语音模式",
    "Web Search & Extract": "网页搜索",
    "X (Twitter) Search": "X (Twitter) 搜索",
    "Browser Automation": "浏览器自动化",
    "Computer Use": "Computer Use 桌面控制",
    "Vision & Image Paste": "视觉与图片粘贴",
    "Image Generation": "图像生成",
    "Spotify": "Spotify 音乐控制 [+手动实现]",
    "Voice & TTS": "语音与 TTS",
    "Deliverable Mode": "交付模式 [+手动实现]",
    "Web Dashboard": "Web 控制 UI",
    "Extending the Dashboard": "扩展 Dashboard",
    "API Server": "API 服务",
    "Subscription Proxy": "订阅代理 [+手动实现]",
    
    # 集成分类
    "Integrations": "集成总览",
    "AI Providers": "AI 供应商",
    "MCP (Model Context Protocol)": "MCP 集成",
    "Provider Routing": "供应商路由",
    "Fallback Providers": "备用供应商",
    "Credential Pools": "凭据池",
    
    # 开发者指南
    "Contributing": "贡献指南",
    "Architecture": "架构",
    "Extending": "扩展开发",
    "Internals": "内部机制",
    
    # Secrets
    "Secrets": "Secrets 密钥管理",
    "Bitwarden Secrets Manager": "Bitwarden 密钥管理",
    
    # 指南分类
    "Guides & Tutorials": "指南与教程",
    "Guides": "指南与教程",
    "Using Hermes": "使用指南",
    
    # 参考
    "CLI Commands Reference": "CLI 命令参考",
    "Slash Commands Reference": "Slash 命令参考",
    "Environment Variables Reference": "环境变量参考",
    "MCP Config Reference": "MCP 配置参考",
    "Model Catalog": "模型目录",
    "Built-in Tools Reference": "内置工具参考",
    "Toolsets Reference": "工具集参考",
    "Bundled Skills Catalog": "内置技能目录",
    "Optional Skills Catalog": "可选技能目录",
    "FAQ & Troubleshooting": "FAQ 与故障排查",
    "Command Reference": "命令参考",
    "Configuration Reference": "配置参考",
    "Tools & Skills Reference": "工具与技能参考",
    
    # Release versions
    "V2026.6.10": "v2026.6.10",
    "V2026.6.9": "v2026.6.9",
    "V2026.6.8": "v2026.6.8",
    "V2026.6.7 Beta.1": "v2026.6.7 Beta.1",
    "V2026.6.6 Beta.2": "v2026.6.6 Beta.2",
    "V2026.6.5": "v2026.6.5",
    "V2026.6.1 Beta.3": "v2026.6.1 Beta.3",
    "V2026.5.31 Beta.4": "v2026.5.31 Beta.4",
    
    # 消息平台
    "Messaging Gateway": "消息网关",
    "Telegram Setup": "Telegram 配置",
    "Discord Setup": "Discord 配置",
    "Slack Setup": "Slack 配置",
    "WhatsApp Setup": "WhatsApp 配置",
    "WhatsApp Business Cloud API Setup": "WhatsApp Business API 配置",
    "Signal Setup": "Signal 配置",
    "Email Setup": "Email 配置",
    "SMS Setup (Twilio)": "SMS 配置 (Twilio)",
    "DingTalk Setup": "钉钉配置",
    "Feishu / Lark Setup": "飞书 / Lark 配置",
    "WeCom (Enterprise WeChat)": "企业微信配置",
    "WeCom Callback (Self-Built App)": "企业微信回调配置",
    "Weixin (WeChat)": "微信配置",
    "QQ Bot": "QQ 机器人配置",
    "Microsoft Teams Setup": "Microsoft Teams 配置",
    "Microsoft Teams Meetings": "Teams 会议集成",
    "Microsoft Graph Webhook Listener": "Microsoft Graph Webhook",
    "Home Assistant Integration": "Home Assistant 集成",
    "Mattermost Setup": "Mattermost 配置",
    "Matrix Setup": "Matrix 配置",
    "BlueBubbles (iMessage)": "BlueBubbles (iMessage)",
    "Photon iMessage": "Photon iMessage",
    "Google Chat Setup": "Google Chat 配置",
    "LINE Setup": "LINE 配置",
    "SimpleX Chat": "SimpleX 配置",
    "ntfy": "ntfy 通知",
    "Open WebUI Integration": "Open WebUI 集成",
    "Webhooks": "Webhook",
    "Yuanbao": "元宝配置",
    
    # 指南
    "Tips & Best Practices": "技巧与最佳实践",
    "Working with Skills": "使用技能",
    "Delegation & Parallel Work": "委托与并行工作",
    "Automate Anything with Cron": "使用 Cron 自动化",
    "Use MCP with Hermes": "在 Hermes 中使用 MCP",
    "Use Voice Mode with Hermes": "使用语音模式",
    "Use SOUL.md with Hermes": "使用 SOUL.md",
    "Set Up a Team Telegram Assistant": "设置团队 Telegram 助手",
    
    # 分类名称
    "Core": "核心",
    "Automation": "自动化",
    "Media & Web": "媒体与网页",
    "Management": "管理",
    "Release Notes": "版本发布",
    "Popular": "常用平台",
    "Microsoft 365": "Microsoft 365",
    "Chinese platforms": "中文平台",
    "Other": "其他",
    "Messaging Platforms": "消息平台",
    "Features": "功能特性",
}

def translate_label(label):
    return LABEL_MAP.get(label, label)

def transform_items(items):
    """递归遍历并转换标签"""
    for item in items:
        item['label'] = translate_label(item['label'])
        if item['type'] == 'category' and 'items' in item:
            transform_items(item['items'])

transform_items(config)

# 写入新配置
with open('dist/docs-config-new.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("新配置已生成: dist/docs-config-new.json")

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
print(f"分类: {cats}, 页面: {pages}")
