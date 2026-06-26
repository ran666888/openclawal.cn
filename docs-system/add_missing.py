"""Add missing sections to docs-config.json"""
import json, os

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist/docs-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

with open('dist/docs-config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# All article paths (normalized)
paths = set(k.replace('\\', '/') for k in articles)

def href(p):
    return p.replace('\\', '/')

# Developer Guide section
dev_guide = {
    "type": "category",
    "label": "开发者指南",
    "items": [
        {"type": "link", "label": "贡献指南", "href": "/docs/developer-guide/contributing/"},
        {
            "type": "category",
            "label": "架构",
            "items": [
                {"type": "link", "label": "Architecture", "href": "/docs/developer-guide/architecture/"},
                {"type": "link", "label": "Agent Loop", "href": "/docs/developer-guide/agent-loop/"},
                {"type": "link", "label": "Prompt Assembly", "href": "/docs/developer-guide/prompt-assembly/"},
                {"type": "link", "label": "Context Compression", "href": "/docs/developer-guide/context-compression-and-caching/"},
                {"type": "link", "label": "Gateway Internals", "href": "/docs/developer-guide/gateway-internals/"},
                {"type": "link", "label": "Session Storage", "href": "/docs/developer-guide/session-storage/"},
                {"type": "link", "label": "Provider Runtime", "href": "/docs/developer-guide/provider-runtime/"},
                {"type": "link", "label": "Programmatic Integration", "href": "/docs/developer-guide/programmatic-integration/"},
            ]
        },
        {
            "type": "category",
            "label": "扩展",
            "items": [
                {"type": "link", "label": "Adding Tools", "href": "/docs/developer-guide/adding-tools/"},
                {"type": "link", "label": "Adding Providers", "href": "/docs/developer-guide/adding-providers/"},
                {"type": "link", "label": "Platform Adapters", "href": "/docs/developer-guide/adding-platform-adapters/"},
                {"type": "link", "label": "Memory Provider Plugin", "href": "/docs/developer-guide/memory-provider-plugin/"},
                {"type": "link", "label": "Context Engine Plugin", "href": "/docs/developer-guide/context-engine-plugin/"},
                {"type": "link", "label": "Model Provider Plugin", "href": "/docs/developer-guide/model-provider-plugin/"},
                {"type": "link", "label": "Image Gen Provider Plugin", "href": "/docs/developer-guide/image-gen-provider-plugin/"},
                {"type": "link", "label": "Video Gen Provider Plugin", "href": "/docs/developer-guide/video-gen-provider-plugin/"},
                {"type": "link", "label": "Web Search Provider Plugin", "href": "/docs/developer-guide/web-search-provider-plugin/"},
                {"type": "link", "label": "Plugin LLM Access", "href": "/docs/developer-guide/plugin-llm-access/"},
                {"type": "link", "label": "Creating Skills", "href": "/docs/developer-guide/creating-skills/"},
                {"type": "link", "label": "Extending the CLI", "href": "/docs/developer-guide/extending-the-cli/"},
            ]
        },
        {
            "type": "category",
            "label": "内部机制",
            "items": [
                {"type": "link", "label": "Tools Runtime", "href": "/docs/developer-guide/tools-runtime/"},
                {"type": "link", "label": "Browser CDP Supervisor", "href": "/docs/developer-guide/browser-supervisor/"},
                {"type": "link", "label": "Cron Internals", "href": "/docs/developer-guide/cron-internals/"},
                {"type": "link", "label": "Trajectory Format", "href": "/docs/developer-guide/trajectory-format/"},
            ]
        },
    ]
}

# Add more guides
more_guides = [
    {"type": "link", "label": "Automation Blueprints", "href": "/docs/guides/automation-blueprints/"},
    {"type": "link", "label": "Google Gemini 集成", "href": "/docs/guides/google-gemini/"},
    {"type": "link", "label": "Azure Foundry", "href": "/docs/guides/azure-foundry/"},
    {"type": "link", "label": "MiniMax OAuth", "href": "/docs/guides/minimax-oauth/"},
    {"type": "link", "label": "本地 Ollama 部署", "href": "/docs/guides/local-ollama-setup/"},
]

# Filter to only existing paths
def filter_existing(items):
    result = []
    for item in items:
        if item['type'] == 'link':
            if href(item['href']) in paths:
                result.append(item)
        elif item['type'] == 'category':
            item['items'] = filter_existing(item['items'])
            if item['items']:
                result.append(item)
    return result

dev_guide['items'] = filter_existing(dev_guide['items'])
more_guides = [g for g in more_guides if href(g['href']) in paths]

# Insert developer guide before 参考
insert_before = "参考"
insert_idx = None
for i, item in enumerate(config):
    if item.get('label') == insert_before:
        insert_idx = i
        break

if insert_idx is not None:
    config.insert(insert_idx, dev_guide)

# Add more guides to 指南与教程
for item in config:
    if item.get('label') == '指南与教程':
        item['items'].extend(more_guides)
        break

# Write back
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
print(f"✅ 新增开发者指南 + 补充教程")
print(f"   分类: {c}, 页面: {p}")
