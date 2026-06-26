#!/usr/bin/env python3
"""Translate OpenClaw skills to Chinese and update the skills page."""
import json, re
from pathlib import Path

skills = json.load(open('openclaw_skills.json', 'r', encoding='utf-8'))

cat_trans = {
    'Development': '\u5f00\u53d1\u5de5\u5177',
    'Productivity': '\u6548\u7387\u5de5\u5177',
    'Media': '\u5a92\u4f53\u4e0e\u521b\u610f',
    'Communication': '\u901a\u4fe1\u4e0e\u6d88\u606f',
    'AI': 'AI \u52a9\u624b',
    'System': '\u7cfb\u7edf\u8fd0\u7ef4',
    'Home Automation': '\u667a\u80fd\u5bb6\u5c45',
}

trans = {
    "Set up and use 1Password CLI for sign-in, desktop integration, and reading or injecting secrets.": "\u914d\u7f6e\u548c\u4f7f\u7528 1Password CLI\uff0c\u7ba1\u7406\u767b\u5f55\u3001\u684c\u9762\u96c6\u6210\u548c\u5bc6\u94a5\u8bfb\u5199\u3002",
    "Create, view, edit, delete, search, move, or export Apple Notes via the memo CLI on macOS.": "\u901a\u8fc7 macOS \u4e0a\u7684 memo CLI \u7ba1\u7406 Apple \u5907\u5fd8\u5f55\u3002",
    "List, add, edit, complete, or delete Apple Reminders and reminder lists via remindctl.": "\u7ba1\u7406 Apple \u63d0\u9192\u4e8b\u9879\uff0c\u652f\u6301\u5217\u51fa\u3001\u6dfb\u52a0\u3001\u7f16\u8f91\u3001\u5b8c\u6210\u548c\u5220\u9664\u3002",
    "Create, search, and manage Bear notes via grizzly CLI.": "\u901a\u8fc7 grizzly CLI \u521b\u5efa\u3001\u641c\u7d22\u548c\u7ba1\u7406 Bear \u7b14\u8bb0\u3002",
    "Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI.": "\u76d1\u63a7\u535a\u5ba2\u548c RSS/Atom \u8ba2\u9605\u6e90\u66f4\u65b0\u3002",
    "BluOS CLI (blu) for discovery, playback, grouping, and volume.": "BluOS CLI \u63a7\u5236\u97f3\u7bb1\u8bbe\u5907\u7684\u53d1\u73b0\u3001\u64ad\u653e\u3001\u5206\u7ec4\u548c\u97f3\u91cf\u3002",
    "Capture frames or clips from RTSP/ONVIF cameras.": "\u4ece RTSP/ONVIF \u6444\u50cf\u5934\u62bd\u53d6\u5e27\u6216\u7247\u6bb5\u3002",
    "Present HTML on connected OpenClaw node canvases, navigate/eval/snapshot, and debug canvas host URLs.": "\u5728\u8fde\u63a5\u7684 OpenClaw \u8282\u70b9\u753b\u5e03\u4e0a\u5c55\u793a HTML\uff0c\u652f\u6301\u5bfc\u822a\u3001\u6267\u884c\u548c\u8c03\u8bd5\u3002",
    "Search, install, update, sync, or publish agent skills with the ClawHub CLI and registry.": "\u901a\u8fc7 ClawHub CLI \u641c\u7d22\u3001\u5b89\u88c5\u3001\u66f4\u65b0\u3001\u540c\u6b65\u6216\u53d1\u5e03 Agent \u6280\u80fd\u3002",
    "Delegate coding work to Codex, Claude Code, or OpenCode as background workers.": "\u5c06\u7f16\u7801\u4efb\u52a1\u59d4\u6d3e\u7ed9 Codex\u3001Claude Code \u6216 OpenCode \u4f5c\u4e3a\u540e\u53f0\u5de5\u4f5c\u8fdb\u7a0b\u6267\u884c\u3002",
    "Create SVG/HTML or Excalidraw diagrams for concepts, architecture, flows, and whiteboards.": "\u521b\u5efa SVG/HTML \u6216 Excalidraw \u56fe\u8868\uff0c\u7528\u4e8e\u6982\u5ff5\u8bf4\u660e\u3001\u67b6\u6784\u56fe\u3001\u6d41\u7a0b\u56fe\u3002",
    "Discord message-tool ops: send/read/edit/delete, react, poll, pin, thread, search, presence, media/components.": "Discord \u6d88\u606f\u64cd\u4f5c\uff1a\u53d1\u9001\u3001\u8bfb\u53d6\u3001\u7f16\u8f91\u3001\u5220\u9664\u3001\u53cd\u5e94\u3001\u6295\u7968\u3001\u56fa\u5b9a\u3001\u56de\u590d\u3001\u641c\u7d22\u7b49\u3002",
    "Control Eight Sleep pods (status, temperature, alarms, schedules).": "\u63a7\u5236 Eight Sleep \u667a\u80fd\u5e8a\u57ab\uff08\u72b6\u6001\u3001\u6e29\u5ea6\u3001\u95f9\u949f\u3001\u5b9a\u65f6\uff09\u3002",
    "Gemini CLI one-shot prompts, summaries, generation, skills, hooks, MCP, or Gemma routing.": "Gemini CLI \u5355\u6b21\u63d0\u793a\u3001\u6458\u8981\u3001\u751f\u6210\u3001\u6280\u80fd\u3001\u94a9\u5b50\u3001MCP \u6216 Gemma \u8def\u7531\u3002",
    "Fetch GitHub issues, select candidates, spawn background fix agents, open PRs.": "\u83b7\u53d6 GitHub Issue\uff0c\u9009\u62e9\u5019\u9009\uff0c\u542f\u52a8\u540e\u53f0\u4fee\u590d Agent\uff0c\u6253\u5f00 PR\u3002",
    "Search GIF providers with CLI/TUI, download results, and extract stills/sheets.": "\u901a\u8fc7 CLI/TUI \u641c\u7d22 GIF\uff0c\u4e0b\u8f7d\u7ed3\u679c\u5e76\u63d0\u53d6\u9759\u6001\u5e27\u3002",
    "GitHub CLI for issues, PRs, CI/check logs, comments, reviews, releases, repos, and gh api queries.": "GitHub CLI \u7ba1\u7406 Issue\u3001PR\u3001CI \u65e5\u5fd7\u3001\u8bc4\u8bba\u3001\u5ba1\u67e5\u3001\u53d1\u5e03\u548c\u4ed3\u5e93\u3002",
    "Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.": "Google Workspace CLI \u7ba1\u7406 Gmail\u3001\u65e5\u5386\u3001\u4e91\u7aef\u786c\u76d8\u3001\u8054\u7cfb\u4eba\u3001\u8868\u683c\u548c\u6587\u6863\u3002",
    "Query Google Places for text search, place details, resolve, reviews, or scriptable JSON via goplaces.": "\u67e5\u8be2 Google Places\uff0c\u652f\u6301\u6587\u672c\u641c\u7d22\u3001\u5730\u70b9\u8be6\u60c5\u3001\u89e3\u6790\u3001\u8bc4\u8bba\u548c JSON \u8f93\u51fa\u3002",
    "Audit/harden OpenClaw hosts: SSH, firewall, updates, exposure, backups, disk encryption, gateway security.": "\u5ba1\u8ba1\u548c\u52a0\u56fa OpenClaw \u4e3b\u673a\uff1aSSH\u3001\u9632\u706b\u5899\u3001\u66f4\u65b0\u3001\u66b4\u9732\u9762\u3001\u5907\u4efd\u3001\u78c1\u76d8\u52a0\u5bc6\u3001\u7f51\u5173\u5b89\u5168\u3002",
    "Himalaya CLI for IMAP/SMTP mail: list, read, search, compose, reply, forward, copy, move, delete.": "Himalaya CLI \u7ba1\u7406 IMAP/SMTP \u90ae\u4ef6\uff1a\u5217\u51fa\u3001\u9605\u8bfb\u3001\u641c\u7d22\u3001\u64b0\u5199\u3001\u56de\u590d\u3001\u8f6c\u53d1\u3001\u590d\u5236\u3001\u79fb\u52a8\u3001\u5220\u9664\u3002",
    "iMessage/SMS CLI for listing chats, history, and sending messages via Messages.app.": "iMessage/SMS CLI \u67e5\u770b\u804a\u5929\u5217\u8868\u3001\u5386\u53f2\u8bb0\u5f55\u548c\u53d1\u9001\u6d88\u606f\u3002",
    "List, configure, authenticate, call, and inspect MCP servers/tools with mcporter over HTTP or stdio.": "\u7ba1\u7406\u3001\u914d\u7f6e\u3001\u8ba4\u8bc1\u548c\u8c03\u7528 MCP \u670d\u52a1\u5668/\u5de5\u5177\uff0c\u652f\u6301 HTTP \u6216 stdio\u3002",
    "Search meme templates, suggest formats, and generate local or hosted image memes.": "\u641c\u7d22\u8868\u60c5\u5305\u6a21\u677f\uff0c\u5efa\u8bae\u683c\u5f0f\uff0c\u751f\u6210\u672c\u5730\u6216\u5728\u7ebf\u8868\u60c5\u5305\u3002",
    "Summarize CodexBar local cost logs by model for Codex or Claude, including current or full breakdowns.": "\u6c47\u603b CodexBar \u672c\u5730\u8d39\u7528\u65e5\u5fd7\uff0c\u6309\u6a21\u578b\u7edf\u8ba1 Codex \u6216 Claude \u7684\u6d88\u8017\u3002",
    "Edit PDFs with natural-language instructions using the nano-pdf CLI.": "\u901a\u8fc7\u81ea\u7136\u8bed\u8a00\u6307\u4ee4\u7f16\u8f91 PDF\u3002",
    "Diagnose OpenClaw Android, iOS, or macOS node pairing issues.": "\u8bca\u65ad OpenClaw \u8282\u70b9\u914d\u5bf9\u3001\u4e8c\u7ef4\u7801\u3001\u8def\u7531\u3001\u8ba4\u8bc1\u548c\u8fde\u63a5\u6545\u969c\u3002",
    "Debug Node.js with node inspect, --inspect, breakpoints, CDP, heap, and CPU profiles.": "\u8c03\u8bd5 Node.js\uff0c\u652f\u6301 node inspect\u3001\u65ad\u70b9\u3001CDP\u3001\u5806\u5feb\u7167\u548c CPU \u5206\u6790\u3002",
    "Notion CLI/API for pages, Markdown content, data sources, files, comments, search, Workers, and raw API calls.": "Notion CLI/API \u7ba1\u7406\u9875\u9762\u3001Markdown \u5185\u5bb9\u3001\u6570\u636e\u6e90\u3001\u6587\u4ef6\u3001\u8bc4\u8bba\u548c\u641c\u7d22\u3002",
    "Work with Obsidian vaults using the official obsidian CLI.": "\u7ba1\u7406 Obsidian \u4ed3\u5e93\uff0c\u652f\u6301\u8bfb\u5199\u641c\u7d22\u521b\u5efa\u7f16\u8f91\u7b14\u8bb0\u3001\u4efb\u52a1\u548c\u94fe\u63a5\u3002",
    "Local speech-to-text with the Whisper CLI (no API key).": "\u672c\u5730 Whisper CLI \u8bed\u97f3\u8f6c\u6587\u5b57\uff0c\u65e0\u9700 API Key\u3002",
    "OpenAI Audio Transcriptions API via curl; gpt-4o-transcribe, mini, diarize, or whisper-1.": "\u8c03\u7528 OpenAI \u97f3\u9891\u8f6c\u5f55 API\uff0c\u652f\u6301 gpt-4o-transcribe \u7b49\u6a21\u578b\u3002",
    "Control Philips Hue lights and scenes via the OpenHue CLI.": "\u901a\u8fc7 OpenHue CLI \u63a7\u5236 Philips Hue \u706f\u5177\u548c\u573a\u666f\u3002",
    "Oracle CLI second-model review/debug/refactor/design with selected files.": "Oracle CLI \u7b2c\u4e8c\u6a21\u578b\u5ba1\u67e5/\u8c03\u8bd5/\u91cd\u6784/\u8bbe\u8ba1\uff0c\u652f\u6301\u9009\u5b9a\u6587\u4ef6\u3002",
    "Foodora-only CLI for checking past orders and active order status.": "Foodora CLI \u67e5\u770b\u5386\u53f2\u8ba2\u5355\u548c\u5f53\u524d\u8ba2\u5355\u72b6\u6001\u3002",
    "Capture and automate macOS UI with the Peekaboo CLI.": "\u4f7f\u7528 Peekaboo CLI \u6355\u83b7\u548c\u81ea\u52a8\u5316 macOS \u754c\u9762\u3002",
    "Debug Python with pdb, breakpoint(), post-mortem inspection, and debugpy remote attach.": "\u8c03\u8bd5 Python\uff0c\u652f\u6301 pdb\u3001\u65ad\u70b9\u3001\u4e8b\u540e\u68c0\u67e5\u548c debugpy \u8fdc\u7a0b\u9644\u52a0\u3002",
    "ElevenLabs text-to-speech with mac-style say UX.": "ElevenLabs \u6587\u5b57\u8f6c\u8bed\u97f3\uff0cmacOS say \u98ce\u683c\u4f53\u9a8c\u3002",
    "Search and analyze your own session logs (older/parent conversations) using jq.": "\u4f7f\u7528 jq \u641c\u7d22\u548c\u5206\u6790\u81ea\u5df1\u7684\u4f1a\u8bdd\u65e5\u5fd7\uff08\u5386\u53f2\u5bf9\u8bdd\uff09\u3002",
    "Local text-to-speech via sherpa-onnx (offline, no cloud)": "\u901a\u8fc7 sherpa-onnx \u672c\u5730\u6587\u5b57\u8f6c\u8bed\u97f3\uff0c\u79bb\u7ebf\u8fd0\u884c\uff0c\u65e0\u9700\u4e91\u7aef\u3002",
    "Create, edit, audit, tidy, validate, or restructure AgentSkills and SKILL.md files.": "\u521b\u5efa\u3001\u7f16\u8f91\u3001\u5ba1\u8ba1\u3001\u6574\u7406\u3001\u9a8c\u8bc1\u6216\u91cd\u6784 AgentSkills \u548c SKILL.md \u6587\u4ef6\u3002",
    "Slack tool actions: send/read/edit/delete messages, react, pin/unpin, list pins/reactions/emoji, member info.": "Slack \u5de5\u5177\u64cd\u4f5c\uff1a\u53d1\u9001\u3001\u8bfb\u53d6\u3001\u7f16\u8f91\u3001\u5220\u9664\u6d88\u606f\uff0c\u53cd\u5e94\uff0c\u56fa\u5b9a\uff0c\u67e5\u770b\u6210\u5458\u4fe1\u606f\u3002",
    "Generate spectrograms and feature-panel visualizations from audio with the songsee CLI.": "\u4ece\u97f3\u9891\u751f\u6210\u9891\u8c31\u56fe\u548c\u7279\u5f81\u53ef\u89c6\u5316\u3002",
    "Control Sonos speakers (discover/status/play/volume/group).": "\u63a7\u5236 Sonos \u97f3\u7bb1\uff08\u53d1\u73b0\u3001\u72b6\u6001\u3001\u64ad\u653e\u3001\u97f3\u91cf\u3001\u5206\u7ec4\uff09\u3002",
    "Run throwaway prototypes to validate feasibility, compare approaches, and report a verdict.": "\u8fd0\u884c\u5feb\u901f\u539f\u578b\u9a8c\u8bc1\u53ef\u884c\u6027\uff0c\u5bf9\u6bd4\u65b9\u6848\u5e76\u62a5\u544a\u7ed3\u8bba\u3002",
    "Terminal Spotify playback/search via spogo (preferred) or spotify_player.": "\u7ec8\u7aef Spotify \u64ad\u653e/\u641c\u7d22\uff0c\u4f18\u5148\u4f7f\u7528 spogo\u3002",
    "Summarize or transcribe URLs, YouTube/videos, podcasts, articles, transcripts, PDFs, and local files.": "\u6458\u8981\u6216\u8f6c\u5f55 URL\u3001YouTube \u89c6\u9891\u3001\u64ad\u5ba2\u3001\u6587\u7ae0\u3001PDF \u548c\u672c\u5730\u6587\u4ef6\u3002",
    "Coordinate multi-step detached tasks as one durable TaskFlow job.": "\u534f\u8c03\u591a\u6b65\u5206\u79bb\u4efb\u52a1\u4e3a\u6301\u4e45\u5316 TaskFlow \u4f5c\u4e1a\u3002",
    "Example TaskFlow pattern for inbox triage, intent routing, waiting on replies, and later summaries.": "TaskFlow \u793a\u4f8b\uff1a\u6536\u4ef6\u7bb1\u5206\u7c7b\u3001\u610f\u56fe\u8def\u7531\u3001\u7b49\u5f85\u56de\u590d\u548c\u540e\u7eed\u6458\u8981\u3002",
    "Add, update, list, search, or inspect Things 3 todos, inbox, today, projects, areas, and tags on macOS.": "\u7ba1\u7406 Things 3 \u5f85\u529e\u4e8b\u9879\uff1a\u6dfb\u52a0\u3001\u66f4\u65b0\u3001\u5217\u51fa\u3001\u641c\u7d22\u548c\u68c0\u67e5\u3002",
    "Control tmux sessions/panes for interactive CLIs: list, capture output, send keys, paste text, monitor prompts.": "\u63a7\u5236 tmux \u4f1a\u8bdd/\u7a97\u683c\uff1a\u5217\u51fa\u3001\u6355\u83b7\u8f93\u51fa\u3001\u53d1\u9001\u6309\u952e\u3001\u7c98\u8d34\u6587\u672c\u3002",
    "Manage Trello boards, lists, and cards via the Trello REST API.": "\u901a\u8fc7 Trello REST API \u7ba1\u7406\u770b\u677f\u3001\u5217\u8868\u548c\u5361\u7247\u3002",
    "Extract frames or short clips from videos using ffmpeg.": "\u4f7f\u7528 ffmpeg \u4ece\u89c6\u9891\u63d0\u53d6\u5e27\u6216\u77ed\u7247\u6bb5\u3002",
    "Start voice calls via the OpenClaw voice-call plugin.": "\u901a\u8fc7 OpenClaw \u8bed\u97f3\u901a\u8bdd\u63d2\u4ef6\u53d1\u8d77\u8bed\u97f3\u901a\u8bdd\u3002",
    "Send third-party WhatsApp messages or sync/search WhatsApp history via wacli.": "\u901a\u8fc7 wacli \u53d1\u9001\u7b2c\u4e09\u65b9 WhatsApp \u6d88\u606f\u6216\u540c\u6b65/\u641c\u7d22\u804a\u5929\u8bb0\u5f55\u3002",
    "Current weather and forecasts with web_fetch, falling back to wttr.in curl.": "\u5f53\u524d\u5929\u6c14\u548c\u9884\u62a5\uff0c\u652f\u6301\u5730\u70b9\u3001\u964d\u96e8\u3001\u6e29\u5ea6\u548c\u51fa\u884c\u89c4\u5212\u3002",
    "xurl CLI for authenticated X posts, replies, reads/search, DMs, media upload, followers, auth status, or raw v2 API calls.": "xurl CLI \u7ba1\u7406 X/Twitter\uff1a\u53d1\u5e16\u3001\u56de\u590d\u3001\u641c\u7d22\u3001\u79c1\u4fe1\u3001\u5a92\u4f53\u4e0a\u4f20\u548c API \u8c03\u7528\u3002",
}

# Apply translations
for s in skills:
    if s['cat'] in cat_trans:
        s['cat'] = cat_trans[s['cat']]
    if s['desc'] in trans:
        s['desc'] = trans[s['desc']]

# Save
json.dump(skills, open('openclaw_skills.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# Generate HTML
cats = {}
for s in skills:
    cats[s['cat']] = cats.get(s['cat'], 0) + 1
cat_names = sorted(cats.keys(), key=lambda c: -cats[c])

btns = '<button type="button" role="tab" aria-selected="true" class="oc-skill-filter is-active">\u5168\u90e8 <span>' + str(len(skills)) + '</span></button>'
for c in cat_names:
    btns += '<button type="button" role="tab" aria-selected="false" class="oc-skill-filter">' + c + ' <span>' + str(cats[c]) + '</span></button>'

cards = ''
for s in skills:
    cards += '<article class="oc-skill-card"><span class="oc-skill-card-cat">' + s['cat'] + '</span><h3 class="oc-skill-card-name">' + s['name'] + '</h3><p class="oc-skill-card-desc">' + s['desc'] + '</p></article>'

html = Path('dist/skills/index.html').read_text(encoding='utf-8')
html = re.sub(r'<div class="oc-skill-filters[^"]*"[^>]*>.*?</div>',
              '<div class="oc-skill-filters" role="tablist" aria-label="\u6309\u5206\u7c7b\u7b5b\u9009">' + btns + '</div>',
              html, flags=re.DOTALL)
html = re.sub(r'<div class="oc-skill-wall">.*?</div>\s*</section>',
              '<div class="oc-skill-wall">' + cards + '</div>\n</section>',
              html, flags=re.DOTALL)

# Update header count
html = re.sub(r'\u81ea\u5e26.*?(\d+).*?\u4e2a Skill', '\u81ea\u5e26 ' + str(len(skills)) + ' \u4e2a Skill', html)

Path('dist/skills/index.html').write_text(html, encoding='utf-8')
print('\u2705 Skills page updated with Chinese categories and descriptions')
print(f'\u5171 {len(skills)} \u4e2a\u6280\u80fd')
for c in cat_names:
    print(f'  {c}: {cats[c]}')
