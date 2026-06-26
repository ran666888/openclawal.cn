"""Add swap script with capture-phase click interception"""
import os, json

os.chdir(r'C:\Users\50148\projects\openclaw中文社区网站')

with open('dist_backup2/skills/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

skills_data = {
    '开发工具': ['coding-agent','python-debugpy','node-inspect-debugger','spike','tmux','gog','taskflow','skill-creator','pyproject.toml','node-connect','peekaboo','blucli','sag'],
    'GitHub': ['github','gh-issues'],
    '笔记与知识': ['notion','obsidian','bear-notes','apple-notes','apple-reminders'],
    '日常工具': ['weather','canvas','trello','taskflow-inbox-triage','things-mac','goplaces','ordercli','healthcheck','session-logs','summarize','camsnap'],
    '密码与安全': ['1password','model-usage'],
    '媒体与创意': ['meme-maker','diagram-maker','video-frames','gifgrep','songsee','sherpa-onnx-tts','openai-whisper','openai-whisper-api','spotify-player','sonoscli','blogwatcher'],
    '通信与消息': ['discord','slack','voice-call','imsg','xurl','gemini'],
    '邮件与文档': ['himalaya','nano-pdf'],
    'MCP 与集成': ['mcporter','clawhub'],
    '智能硬件': ['openhue','eightctl','wacli','oracle'],
    '扩展技能': ['browser-automation','tavily','obsidian-vault-maintainer','wiki-maintainer','prose'],
}
descs = {
    'coding-agent':'AI 编码助手','python-debugpy':'Python 远程调试','node-inspect-debugger':'Node.js 调试器','spike':'快速原型验证','tmux':'终端复用器','gog':'Go 工具箱','taskflow':'工作流引擎','skill-creator':'Skill 创建向导','pyproject.toml':'Python 配置','node-connect':'Node 连接','peekaboo':'截图工具','blucli':'蓝牙 CLI','sag':'AWS 操作',
    'github':'GitHub 全功能集成','gh-issues':'Issue 管理','notion':'Notion 集成','obsidian':'Obsidian 仓库','bear-notes':'Bear 笔记','apple-notes':'Apple Notes','apple-reminders':'Apple 提醒',
    'weather':'天气查询','canvas':'实时画布','trello':'Trello 看板','taskflow-inbox-triage':'邮件整理','things-mac':'Things 任务','goplaces':'地点搜索','ordercli':'点餐助手','healthcheck':'系统检查','session-logs':'会话日志','summarize':'自动摘要','camsnap':'拍照',
    '1password':'密码管理','model-usage':'API 用量','meme-maker':'表情包制作','diagram-maker':'图表生成','video-frames':'视频帧','gifgrep':'GIF 搜索','songsee':'音频频谱','sherpa-onnx-tts':'本地 TTS','openai-whisper':'语音转文字','openai-whisper-api':'Whisper API','spotify-player':'Spotify 控制','sonoscli':'Sonos 控制','blogwatcher':'RSS 监控',
    'discord':'Discord 通知','slack':'Slack 通知','voice-call':'语音通话','imsg':'iMessage','xurl':'URL 分享','gemini':'Gemini 助手','himalaya':'邮件客户端','nano-pdf':'PDF 编辑',
    'mcporter':'MCP 桥接','clawhub':'ClawHub 接入','openhue':'Hue 灯控','eightctl':'温控器','wacli':'WiFi 控制','oracle':'数据库工具',
    'browser-automation':'浏览器自动化','tavily':'网页搜索','obsidian-vault-maintainer':'仓库维护','wiki-maintainer':'Wiki 维护','prose':'写作优化',
}

data_json = json.dumps(skills_data, ensure_ascii=False)
descs_json = json.dumps(descs, ensure_ascii=False)

script = f"""<script>
(function(){{
var D={data_json};
var E={descs_json};
var T=0;for(var k in D)T+=D[k].length;
var K=Object.keys(D);
var C=[];for(var i=0;i<K.length;i++){{for(var j=0;j<D[K[i]].length;j++){{C.push({{cat:K[i],name:D[K[i]][j],desc:E[D[K[i]][j]]||D[K[i]][j]}})}}}}

function replaceContent(){{
var cards=document.querySelectorAll('.oc-skill-card');
if(!cards||!cards.length){{setTimeout(replaceContent,500);return}}
var idx=0;
cards.forEach(function(c){{
if(idx>=C.length)return;
var ce=c.querySelector('.oc-skill-card-cat');
var ne=c.querySelector('.oc-skill-card-name');
var de=c.querySelector('.oc-skill-card-desc');
if(ce)ce.textContent=C[idx].cat;
if(ne)ne.textContent=C[idx].name;
if(de)de.textContent=C[idx].desc;
if(ce&&ne&&de)c.setAttribute('data-swapped','1');
idx++
}});
while(idx<cards.length){{cards[idx].style.display='none';idx++}}

// replace numbers
document.body.innerHTML=document.body.innerHTML.replace(/>95</g,'>'+T+'<');
document.body.innerHTML=document.body.innerHTML.replace(/95(?= 个 Skill)/g,String(T));
}}

function captureFilter(e){{
var btn=e.target.closest('.oc-skill-filter');
if(!btn)return;
e.preventDefault();
e.stopImmediatePropagation();
var fb=btn.closest('.oc-skill-filters');
if(!fb)return;
fb.querySelectorAll('.oc-skill-filter').forEach(function(b){{b.classList.remove('is-active')}});
btn.classList.add('is-active');

// Use data attribute to track category
var span=btn.querySelector('span');
var txt=btn.textContent.replace(span?span.textContent:'','').trim();
btn.setAttribute('data-oc-cat',txt);

var cards=document.querySelectorAll('.oc-skill-card');
cards.forEach(function(c){{
if(c.style.display==='none')return;
var cc=c.querySelector('.oc-skill-card-cat');
if(!cc)return;
c.style.display=(txt==='全部'||cc.textContent.trim()===txt)?'':'none';
}});
return false;
}}

function init(){{
replaceContent();
document.querySelector('.oc-skill-filters').addEventListener('click',captureFilter,true);
}}

if(document.readyState==='complete'){{setTimeout(init,1200)}}else{{window.addEventListener('load',function(){{setTimeout(init,1200)}})}}
}})();
</script>"""

html = html.replace('</body>', script + '</body>')

with open('dist/skills/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done')
