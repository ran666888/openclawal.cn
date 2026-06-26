"""Replace skill cards using precise byte positions"""
import os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/skills/index_original.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Precise positions found earlier
# wall at 19190, foot at 44052
start_marker = '<div class="oc-skill-wall">'
end_marker = '</div></section><footer class="oc-skill-foot">'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

print(f'Start: {start_idx}, End: {end_idx}')

def card(cat, name, desc):
    return f'<article class="oc-skill-card"><span class="oc-skill-card-cat">{cat}</span><h3 class="oc-skill-card-name">{name}</h3><p class="oc-skill-card-desc">{desc}</p></article>'

descriptions = {
    'coding-agent':'AI 编码助手，自动生成代码、调试、重构',
    'python-debugpy':'Python 远程调试，支持断点、变量检查',
    'node-inspect-debugger':'Node.js 调试器，支持 Chrome DevTools 协议',
    'spike':'快速原型验证，用 Demo 验证想法',
    'tmux':'终端复用器管理，多窗口/面板操作',
    'gog':'Go 语言开发工具箱',
    'taskflow':'工作流编排引擎，多步骤任务管理',
    'skill-creator':'可视化 Skill 创建向导',
    'pyproject.toml':'Python 项目配置管理',
    'node-connect':'Node 远程连接管理',
    'peekaboo':'屏幕截图工具',
    'blucli':'蓝牙设备管理 CLI',
    'sag':'AWS Systems Manager 操作',
    'github':'GitHub 全功能集成：PR、Issue、Code Review',
    'gh-issues':'GitHub Issue 管理，搜索/创建/分配',
    'notion':'Notion 集成，创建/读取/更新页面和数据库',
    'obsidian':'Obsidian 仓库管理，笔记搜索与整理',
    'bear-notes':'Bear 笔记集成',
    'apple-notes':'Apple Notes 笔记管理',
    'apple-reminders':'Apple 提醒事项管理',
    'weather':'天气查询，支持城市搜索和天气预报',
    'canvas':'实时画布，支持绘图、图表、白板协作',
    'trello':'Trello 看板管理，卡片/列表操作',
    'taskflow-inbox-triage':'Inbox 邮件整理，自动分类与归档',
    'things-mac':'Things 3 任务管理集成 (macOS)',
    'goplaces':'周边地点搜索，导航与路线规划',
    'ordercli':'命令行点餐助手',
    'healthcheck':'系统健康检查，监控 CPU/内存/磁盘',
    'session-logs':'会话日志管理，搜索和导出',
    'summarize':'文本/网页/视频自动摘要',
    'camsnap':'摄像头拍照与图像采集',
    '1password':'1Password 密码管理，搜索/填充凭证',
    'model-usage':'API 用量查询，各模型消耗统计',
    'meme-maker':'表情包生成器，文字+模板合成图片',
    'diagram-maker':'图表/流程图/架构图自动生成',
    'video-frames':'视频帧提取/分析，逐帧处理',
    'gifgrep':'GIF 动图搜索与下载',
    'songsee':'音频频谱可视化',
    'sherpa-onnx-tts':'本地离线 TTS 语音合成',
    'openai-whisper':'OpenAI Whisper 语音转文字',
    'openai-whisper-api':'Whisper API 版语音识别',
    'spotify-player':'Spotify 音乐播放控制',
    'sonoscli':'Sonos 音响系统控制',
    'blogwatcher':'RSS/博客订阅监控',
    'discord':'Discord 消息通知与频道管理',
    'slack':'Slack 消息发送与频道管理',
    'voice-call':'语音通话技能，拨打电话',
    'imsg':'iMessage 消息发送与接收',
    'xurl':'URL 分享与预览',
    'gemini':'Google Gemini AI 助手',
    'himalaya':'邮件客户端，命令行收发邮件',
    'nano-pdf':'PDF 编辑，合并/拆分/提取/转换',
    'mcporter':'MCP 服务器转换桥接工具',
    'clawhub':'ClawHub 技能市场接入',
    'openhue':'Philips Hue 智能灯控',
    'eightctl':'智能温控器控制',
    'wacli':'WiFi 设备控制',
    'oracle':'数据库查询与运维工具',
    'browser-automation':'浏览器自动化，表单填写/网页操作/数据抓取',
    'tavily':'网页搜索增强 (Tavily 引擎)',
    'obsidian-vault-maintainer':'Obsidian 仓库自动化维护',
    'wiki-maintainer':'Wiki 知识库自动维护',
    'prose':'写作风格优化与润色',
}

categories = [
    ('开发工具', ['coding-agent','python-debugpy','node-inspect-debugger','spike','tmux','gog','taskflow','skill-creator','pyproject.toml','node-connect','peekaboo','blucli','sag']),
    ('GitHub', ['github','gh-issues']),
    ('笔记与知识', ['notion','obsidian','bear-notes','apple-notes','apple-reminders']),
    ('日常工具', ['weather','canvas','trello','taskflow-inbox-triage','things-mac','goplaces','ordercli','healthcheck','session-logs','summarize','camsnap']),
    ('密码与安全', ['1password','model-usage']),
    ('媒体与创意', ['meme-maker','diagram-maker','video-frames','gifgrep','songsee','sherpa-onnx-tts','openai-whisper','openai-whisper-api','spotify-player','sonoscli','blogwatcher']),
    ('通信与消息', ['discord','slack','voice-call','imsg','xurl','gemini']),
    ('邮件与文档', ['himalaya','nano-pdf']),
    ('MCP 与集成', ['mcporter','clawhub']),
    ('智能硬件', ['openhue','eightctl','wacli','oracle']),
    ('扩展技能', ['browser-automation','tavily','obsidian-vault-maintainer','wiki-maintainer','prose']),
]

total_skills = sum(len(s) for _, s in categories)
new_cards_html = ''
for cat, skills in categories:
    for name in skills:
        desc = descriptions.get(name, name)
        new_cards_html += card(cat, name, desc)

# Replace cards section
old_section = html[start_idx:end_idx + len(end_marker)]
new_section = f'<div class="oc-skill-wall">{new_cards_html}</div></section><footer class="oc-skill-foot">'
html = html.replace(old_section, new_section)

# Update numbers
html = html.replace('<!-- -->95<!-- --> 个 Skill', f'<!-- -->{total_skills}<!-- --> 个 Skill')

# Update URL references that mention old skills
html = html.replace('href="/en/skills"', 'href="/skills"')
html = html.replace('lang="zh-CN"', 'lang="zh-CN"')

with open('dist/skills/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
count = html.count('oc-skill-card')
print(f'✅ 完成')
print(f'   技能卡片: {count//4} 个')
print(f'   分类: {len(categories)}')
print(f'   文件大小: {len(html)} bytes')
