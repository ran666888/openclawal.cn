/**
 * OpenClaw 中文社区网站 — 一键改造脚本
 * 读取 site/ 目录，输出改造后的 dist/ 目录
 * 运行: node transform.js
 */
const fs = require('fs');
const path = require('path');

const SRC = path.join(__dirname, 'site');
const DST = path.join(__dirname, 'dist');

// ============================================================
// 1. 替换规则
// ============================================================

// 通用品牌文本替换（所有文本文件）
const TEXT_RULES = [
  // 品牌名（先替换长匹配，再替换短匹配，避免部分替换）
  ['Hermes Agent 中文社区', 'OpenClaw 中文社区'],
  ['Hermes Agent 中文文档', 'OpenClaw 中文文档'],
  ['Hermes Agent 中文', 'OpenClaw 中文'],
  ['Hermes Agent', 'OpenClaw'],
  ['Hermes Terminal', 'OpenClaw Terminal'],
  ['Hermes Agent 是什么', 'OpenClaw 是什么'],
  ['什么是 Hermes Agent', '什么是 OpenClaw'],
  ['HERMES · AGENT', 'OPENCLAW'],
  ['Hermes CN', 'OpenClaw'],
  ['hermes-cn-og.svg', 'openclaw-og.svg'],   // OG 图片
  ['hermes-cn.svg', 'openclaw.svg'],
  ['hermes-agent-cn', 'openclaw-cn'],
  ['hermes_agent_cn', 'openclaw_cn'],
  ['res1.hermesagent.org.cn', 'openclawal.cn/scripts'],
 ['res.agthub.tech', 'openclawal.cn/scripts'],   // 长匹配必须在 hermesagent.org.cn 之前
  ['hermesagent.org.cn', 'openclaw.cn'],
  ['desktop.hermesagent.org.cn', 'desktop.openclaw.cn'],
  ['hermes-agent.nousresearch.com', 'openclaw.ai'],
  ['github.com/NousResearch/hermes-agent', 'github.com/openclaw/openclaw'],
  ['NousResearch/hermes-agent', 'openclaw/openclaw'],
  ['Nous Research', 'OpenClaw'],
  ['nousresearch.com', 'openclaw.ai'],
  ['G-9WJEXHW3PD', 'G-XXXXXXXXXX'],           // 清除 GA
  ['ca-pub-1260884566475214', ''],             // 清除 AdSense
  // 补充遗漏替换
  ['使用 Hermes', '使用 OpenClaw'],             // 侧边栏链接标题
  ['Captain Hermes', 'Captain OpenClaw'],       // CLI 角色名
  ['Hermes-CN-Desktop', 'OpenClaw-CN-Desktop'],  // GitHub 仓库
  ['Hermes-CN-Core', 'OpenClaw-CN-Core'],        // GitHub 仓库
  ['Hermes-CN', 'OpenClaw-CN'],                  // 中文版名称
  ['Hermes.Agent.CN.Desktop_x64-setup', 'OpenClaw.Desktop_x64-setup'], // 安装包名
  ['Hermes.Agent.CN.Desktop', 'OpenClaw.CN.Desktop'], // 桌面版全称
  ['Eynzof/Hermes-CN-Desktop', 'OpenClaw-CN-Desktop'], // GitHub 链接
  ['Eynzof/Hermes-CN-Core', 'OpenClaw-CN-Core'],       // GitHub 链接
  ['"Hermes "', '"OpenClaw "'],                  // 带引号的末尾空格
  ['HermesAgentBaseEnv', 'OpenClawBaseEnv'],      // API 类名
  ['HermesAgent', 'OpenClaw'],                    // 通用复合名
  ['HermesGateway', 'OpenClawGateway'],            // 任务名
  ['HermesHome', 'OpenClawHome'],                  // 配置路径
  ['logo.svg', 'logo.png'],                        // 使用新logo图片
  // CLI 命令替换
  ['hermes setup', 'openclaw setup'],
  ['hermes model', 'openclaw model'],
  ['hermes gateway', 'openclaw gateway'],
  ['hermes claw migrate', 'openclaw migrate'],
  ['hermes profile', 'openclaw profile'],
  ['hermes-claw-', 'openclaw-'],                   // 迁移命令
  ['hermes-agent-installation', 'openclaw-installation'],  // 专题页路径
  ['hermes-agent-messaging', 'openclaw-messaging'],        // 专题页路径
  ['hermes-agent-mcp', 'openclaw-mcp'],                    // 专题页路径
];

// 需要保持等长的替换（用于 JS，字符串长度不变更安全）
const JS_SAFE_RULES = [
  ['hermes-agent-cn:', 'openclaw-cn:'],
  ['webpackChunkhermes_agent_cn', 'webpackChunkopenclaw_cn'],
  ['res1.hermesagent.org.cn', 'openclawal.cn/scripts'],
 ['res.agthub.tech', 'openclawal.cn/scripts'],
  ['hermesagent.org.cn', 'openclaw.cn'],
  ['desktop.hermesagent.org.cn', 'desktop.openclaw.cn'],
];

// CSS 替换规则
const CSS_CLASS_RULES = [
  ['.hermes-', '.oc-'],
  ['hermes-', 'oc-'],           // CSS 中的选择器
  ['--hermes-', '--oc-'],
];

// ============================================================
// 2. 新主题色 (CSS 变量值替换)
// ============================================================

// === 第⑥组配色方案 ===
// #fce5dd  #dfd7d3  #bec8c8  #9bb7bb  #80abb1  #5496a2
// 暖灰基调 + 青蓝强调，温暖包容又不失科技感
const COLOR_MAP = {
  // === 暗色背景系统（暖深灰，与第⑥组协调）===
  '#041c1c': '#2a2520',       // 主背景 → 暖深灰
  '#082626': '#35302b',       // 卡片/面板背景
  '#0c3030': '#3d3833',       // 浅卡片背景
  '#07070d': '#2a2520',       // 全局主题色

  // === 文字颜色 ===
  '#ffe6cb': '#fce5dd',       // 主文字 → 暖白 (⑥)
  'rgba(255,230,203,': 'rgba(252,229,221,', // 半透明文字
  'rgba(255,215,0,': 'rgba(251,146,60,',    // 金色边框 → 亮橙 (#fb923c)
  'rgba(255,215,0)': 'rgba(251,146,60)',
  '#f5f5f5': '#dfd7d3',       // 亮底 → 暖灰 (⑥)
  '#ffffff': '#fce5dd',       // 纯白底 → 暖白 (⑥)

  // === 强调/品牌色 ===
  '#6ee7b7': '#80abb1',       // 成功绿 → 青灰 (⑥)
  '#ffd700': '#5496a2',       // 金色 → 青蓝 (⑥，UI强调色)
  '#ffd96b': '#fb923c',       // community-v3-gold → 亮橙
  '#b97f0b': '#cc6f20',       // community-v3-gold-deep → 深橙
  '#155d4d': '#80abb1',       // community-v3-green → 青灰
  '#17302f': '#2a2520',       // community-v3-ink → 暖深灰
  'rgba(23,48,47,': 'rgba(42,37,32,', // community-v3-ink-* → 暖深灰
  '#00a400': '#80abb1',       // Docusaurus 成功色 → 青灰
  '#009400': '#6b9ba0',       // 成功深色 → 深青灰
  '#008b00': '#5c8a8f',       // 成功更深 → 更深青灰
  '#e6f6e6': '#e8efe8',       // 成功提示背景 → 浅灰绿

  // === Docusaurus 默认变量值 ===
  '#061f1f': '#35302b',       // surface 背景
  '#1b1b1d': '#2a2520',       // 暗色底
  '#242526': '#35302b',       // surface
  '#f6f7f8': '#dfd7d3',       // 亮色底

  // === 渐变/阴影中的旧 rgba ===
  'rgba(6,20,20,': 'rgba(42,37,32,',   // 渐变底色 → 暖深灰
  'rgba(3,12,12,': 'rgba(42,37,32,',   // 渐变底色 → 暖深灰
  'rgba(4,28,28,': 'rgba(42,37,32,',   // 导航/面板背景 → 暖深灰
  'rgba(4,29,29,': 'rgba(42,37,32,',   // 面板背景 → 暖深灰
  'rgba(4,16,16,': 'rgba(42,37,32,',   // 特殊背景 → 暖深灰
  'rgba(2,17,17,': 'rgba(42,37,32,',   // 安装面板背景 → 暖深灰
  'rgba(7,22,22,': 'rgba(42,37,32,',   // 技能卡片背景 → 暖深灰
  'rgba(10,28,28,': 'rgba(42,37,32,',  // 技能卡片hover → 暖深灰
  'rgba(5,22,22,': 'rgba(42,37,32,',   // 市场卡片背景 → 暖深灰
  'rgba(2,14,14,': 'rgba(42,37,32,',   // 日报bottom/弹窗 → 暖深灰
  'rgba(8,38,38,': 'rgba(42,37,32,',   // 日报日历/主面板 → 暖深灰
  'rgba(8,24,24,': 'rgba(42,37,32,',   // 社区按钮 → 暖深灰
  'rgba(2,8,8,': 'rgba(42,37,32,',     // 社区弹窗遮罩 → 暖深灰
  'rgba(6,22,22,': 'rgba(42,37,32,',   // 社区浮动hover → 暖深灰
  'rgba(6,23,23,': 'rgba(42,37,32,',   // community-v3-join → 暖深灰
  'rgba(255,217,107,': 'rgba(251,146,60,', // community-v3 金色 → 亮橙
  'rgba(255,245,137,': 'rgba(251,146,60,',  // 金色光晕 → 亮橙
  'rgba(255,245,145,': 'rgba(251,146,60,',  // 金色边框 → 亮橙
  'rgb(255, 230, 179)': 'rgb(252, 229, 221)', // JS中的硬编码文字色 → 暖白

  // === 代码块 ===
  '#282a36': '#35302b',       // 代码块背景
};

// 把 COLOR_MAP 转为数组格式，供 HTML 处理使用
COLOR_MAP_ARRAY = Object.entries(COLOR_MAP);

// ============================================================
// 3. 清理函数
// ============================================================

function cleanDir(dir) {
  // 覆盖模式：删除所有文件但保留目录本身（避免 Windows EPERM）
  if (fs.existsSync(dir)) {
    for (const f of fs.readdirSync(dir)) {
      const fp = path.join(dir, f);
      try {
        fs.rmSync(fp, { recursive: true, force: true });
      } catch (e) {
        // 跳过无法删除的文件
      }
    }
  }
}

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const item of fs.readdirSync(src)) {
    const s = path.join(src, item);
    const d = path.join(dst, item);
    if (fs.statSync(s).isDirectory()) {
      copyDir(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

// ============================================================
// 4. 替换引擎
// ============================================================

function applyRules(content, rules) {
  for (const [from, to] of rules) {
    // split/join 替换所有出现，不是只替换第一个
    content = content.split(from).join(to);
  }
  return content;
}

// ============================================================
// 5. 文件处理器
// ============================================================

function processHtml(content, relPath) {
  let result = content;

  // 品牌文本替换
  result = applyRules(result, TEXT_RULES);

  // 单独处理 "Hermes" 作产品名（但不是在 Hermes Agent 中已被替换的）
  // 注意: Hermes Agent 已被替换为 OpenClaw, 剩下的 "Hermes" 单独出现
  // 使用正则避免替换到 CSS 类名中的 hermes
  result = result.replace(/(?<![.\-])Hermes(?![.\-]|\w)/g, (match, offset, str) => {
    // 检查是否在 HTML 标签名或属性中
    const before = str.slice(Math.max(0, offset - 20), offset);
    if (/<[^>]*$/.test(before)) return match; // 在标签内
    return 'OpenClaw';
  });

  // 替换大写品牌
  result = result.replace(/HERMES(?!-)/g, 'OPENCLAW');

  // 替换属性中的 Hermes (如 title="使用 Hermes")
  result = result.replace(/="([^"]*Hermes[^"]*)"/g, (match, inner) => {
    return '="' + applyRules(inner, TEXT_RULES) + '"';
  });

  // 替换 HTML 中的颜色值（meta theme-color, style 属性等）
  result = applyRules(result, COLOR_MAP_ARRAY);

  // === 保留 vs 对比区，改成夸 OpenClaw 的内容（此时 Hermes→OpenClaw 已全部完成）===
  // Hermes vs OpenClaw → OpenClaw vs Hermes Agent（已被改成 OpenClaw vs OpenClaw）
  result = result.split('OpenClaw vs OpenClaw').join('OpenClaw vs Hermes Agent');
  // OpenClaw 比龙虾好在哪里 → OpenClaw 比 Hermes Agent 好在哪里
  result = result.replace('OpenClaw 比龙虾好在哪里', 'OpenClaw 比 Hermes Agent 好在哪里');
  // 卡片1 正文修复（原文是 Hermes vs OpenClaw，现在改为对比 Hermes Agent）
  result = result.replace(
    'Token 消耗往往比 OpenClaw 更低',
    'Token 消耗控制出色'
  );
  // 卡片3 链接修复（迁移指南已被删除，改为指向快速开始）
  result = result.replace('/docs/guides/migrate-from-openclaw', '/docs/getting-started/quickstart');

  // === 全部内容基于 openclaw.ai 官网真实信息重写 ===
  // FAQ1: OpenClaw 是什么？
  result = result.replace(
    'OpenClaw 是一个开源、自托管、支持长期记忆与 Skills 的 AI Agent。它既能在终端中完成复杂任务，也能通过消息网关在微信、飞书、QQ等平台上持续工作。',
    'OpenClaw 是一个开源的 Personal AI Assistant，官网定位是 "The AI that actually does things"。它能帮你清理收件箱、发送邮件、管理日历、办理值机，全部通过 WhatsApp、Telegram 等聊天应用完成。自托管部署，数据归你所有。'
  );
  // FAQ2: 中文用户应该从哪里开始？
  result = result.replace(
    '建议先看中文安装教程与快速开始；如果你使用的是 Windows，可以直接按 Windows 安装指南走原生 PowerShell 路径，再根据场景配置模型、工具和消息网关。',
    '安装很简单：先安装 Node 24 或 Node 22 LTS，然后执行 npm i -g openclaw，再运行 openclaw onboard --install-daemon 完成初始化。之后打开 http://127.0.0.1:18789 即可使用 Web 控制面板。'
  );
  // FAQ3: 它和 IDE 里的 AI 助手有什么区别？
  result = result.replace(
    '很多 IDE 助手擅长当前窗口里的即时协作，而 OpenClaw 更强调长期上下文、跨会话记忆、可复用 Skill、MCP 集成和多平台自动化，适合长期任务与持续运行场景。',
    'OpenClaw 是一个自托管的 AI Gateway，连接你的聊天应用与 AI Agent。它不绑定任何 IDE，支持 Discord、iMessage、Signal、Slack、Telegram、WhatsApp 等多平台，一个 Gateway 进程同时服务多个渠道。'
  );


  // Overview 卡片标题
  result = result.replace('开源、自托管的 AI Agent', '本地运行，隐私优先');
  result = result.replace('长期记忆与 Skills', '持久记忆，技能生态');
  result = result.replace('MCP、工具与自动化', '浏览器控制，系统访问');
  result = result.replace('多平台消息网关', '随处聊天，多平台互通');
  result = result.replace('面向中文用户的落地指南', '中文社区，从零上手');
  result = result.replace('<code>hermes</code>', '<code>openclaw</code>');
  result = result.replace('兼容国内外模型供应商', '模型无关，自由选择');
  // Overview 6 张卡片（基于 openclaw.ai 官网）
  result = result.replace(
    'OpenClaw 可以运行在本地电脑、VPS、Docker、SSH 或云端开发环境中，不依赖单一 IDE，也不把你的工作流锁在网页聊天框里。',
    'OpenClaw 在你的电脑上本地运行，支持 macOS、Linux、Windows 全平台。可接入托管模型、订阅 API、网关或本地模型，数据归你所有，隐私无忧。'
  );
  result = result.replace(
    '它会跨会话记住你的项目、偏好与工作习惯，并把解决过的问题沉淀成可复用 Skill，越用越懂你。',
    'OpenClaw 拥有持久记忆，会记住你的偏好和工作上下文。支持社区技能扩展，AI 甚至可以自主编写新技能，越用越懂你，越用越顺手。'
  );
  result = result.replace(
    '支持 MCP、终端、文件、浏览器、图片、TTS 等工具，还能通过 cron 调度实现日报、备份、巡检和提醒。',
    'OpenClaw 支持浏览器控制（填表、提取数据）、文件读写、shell 命令、脚本执行。内置 cron 定时任务和心跳检测，AI 可主动联系你。'
  );
  result = result.replace(
    '通过 微信、飞书、企业微信、钉钉、QQ、WhatsApp、Discord、Slack 等入口，让你的 Agent 持续在线。',
    'OpenClaw Gateway 连接 50+ 消息平台：WhatsApp、Telegram、Discord、Slack、Signal、iMessage 等，支持私聊和群聊，一个进程服务所有渠道。'
  );
  result = result.replace(
    '这个网站聚焦中文文档、安装教程、常见配置、社区经验与微信交流入口，帮助你更快从 0 到 1 上手。',
    'OpenClaw 中文社区提供完整的中文文档、安装教程和微信群答疑。从零开始，一条命令安装，中文引导配置，社区成员实时帮助。'
  );
  result = result.replace(
    '支持 Qwen、GLM、Kimi、MiniMax、Claude、Gemini，以及 OpenAI 兼容接口和本地模型，适合国内网络与工具环境。',
    'OpenClaw 模型无关，支持 Claude、GPT、Gemini、DeepSeek、Kimi、Qwen 等任意模型。可同时配置多个供应商，支持本地模型和 OpenAI 兼容接口。'
  );
    // 对比卡片标题替换
  result = result.replace('更快、更智能、更省 Token', '本地运行，隐私优先');
  result = result.replace('思路透明，自我进化', '持久记忆，技能生态');
  result = result.replace('一条指令，从龙虾迁到 OpenClaw', '多平台，多模型，多 Agent');
  // 对比卡片1
  result = result.replace(
    '按不少用户的直观体验，同样一类任务下，OpenClaw 的上下文组织更紧凑、工具调用更透明，Token 消耗往往比 OpenClaw 更低；有用户甚至反馈能低到约 30%。如果你希望 Agent 跑得更快、花费更省，同时还能保持任务质量，OpenClaw 更容易给出&quot;又快又稳&quot;的感觉。',
    'OpenClaw 在你的电脑上本地运行，支持托管模型、订阅 API、网关或本地模型多种选择。默认隐私优先，数据不出你的设备。你可以自由选择安全沙箱级别。'
  );
  // 对比卡片2
  result = result.replace(
    'OpenClaw 的过程感更强：你更容易看懂它在做什么、为什么这样做、任务推进到了哪一步。更重要的是，它能把一次次执行经验沉淀成长期记忆、Skills 和上下文约定，不用你每次都重新喂 prompt、反复手工修 bug。它不是只完成一次任务，而是在持续学习你的工作方式。',
    'OpenClaw 拥有持久记忆，会记住你的偏好和工作上下文，越用越贴近你的习惯。支持社区技能扩展，AI 甚至能自主编写新技能。它还支持浏览器控制、文件系统访问、shell 命令执行等完整系统操作。'
  );
  // 对比卡片3
  result = result.replace(
    'OpenClaw 官方直接提供 `openclaw migrate`，可以把 OpenClaw 的配置、数据和工作区内容迁到 OpenClaw。对已经在用龙虾的用户来说，这几乎就是一条指令起步；再配合 `openclaw profile` 做工作 / 个人 / 测试环境隔离，切换成本很低，后续管理也更清晰。',
    'OpenClaw 由 Peter Steinberger 创建，MIT 开源协议，与 Anthropic 无关。支持 WhatsApp、Telegram、Discord、Slack、Signal、iMessage 等平台，也支持飞书、钉钉、企业微信等国内渠道。开源社区已有 34 万+ Star。'
  );
  // Hot Topics 卡片正文（基于官网信息）
  result = result.replace(
    '覆盖 Windows PowerShell、WSL2、Linux、macOS、Docker、Termux 与 VPS 的中文安装路径，以及安装后的推荐配置顺序。',
    '支持 macOS、Linux、Windows 三大平台。一键脚本安装：curl -fsSL https://openclaw.ai/install.sh | bash，或 npm i -g openclaw。安装后运行 openclaw onboard 完成初始化。'
  );
  result = result.replace(
    '聚合 微信、飞书、企业微信、钉钉、QQ、WhatsApp、Discord、Slack 等接入入口，帮你快速找到适合自己的消息平台。',
    'OpenClaw Gateway 是单一控制平面，同时连接 Discord、iMessage、Signal、Slack、Telegram、WhatsApp、飞书、钉钉、企业微信等 50+ 平台。支持多 Agent 路由，不同平台可配置不同 Agent。'
  );
  result = result.replace(
    '解释 MCP 是什么、如何连接 MCP Server、如何做工具过滤，以及适合哪些自动化与项目助手场景。',
    'OpenClaw 支持 MCP 协议，可对接 MCP 服务器扩展工具能力。Gateway 架构天然适合多云、多模型、多 Agent 的编排场景，配置灵活、扩展性强。'
  );
  // Features 卡片正文（基于官网信息）
  result = result.replace(
    'OpenClaw 会通过长期记忆、会话检索、技能沉淀和用户画像，把一次次任务经验转化成之后可复用的能力。',
    'Runs on Your Machine：macOS、Linux、Windows 全平台支持。可接入托管模型、订阅 API、网关或本地模型。默认隐私优先，数据归你所有。'
  );
  result = result.replace(
    '它可以运行在 VPS、Docker、SSH、Modal、Daytona 或本地环境，并通过 Telegram、Discord、Slack、WhatsApp、Signal、Email 和 CLI 与你对话。',
    'Chat Where You Are：在 WhatsApp、Telegram、Discord、Slack、Signal、iMessage 等平台使用，支持私聊和群聊。发条消息就能让它干活。'
  );
  result = result.replace(
    '内置 cron 调度：日报、备份、巡检、信息抓取和提醒都可以用自然语言配置，并投递到你常用的平台。',
    'Persistent Memory：持久记忆让 OpenClaw 记住你的偏好、上下文和使用习惯，越用越懂你。你的偏好、你的上下文、你的 AI，完全个性化。'
  );
  result = result.replace(
    '复杂任务完成后可以沉淀为技能，兼容 agentskills.io 开放格式，适合团队共享和社区贡献。',
    'Browser Control：OpenClaw 可以浏览网页、填写表单、从任意网站提取数据。它能自主完成打开浏览器、登录控制台、配置 OAuth、生成 token 等复杂操作。'
  );
  result = result.replace(
    '提供 40+ 工具、工具集配置、命令审批、容器隔离、浏览器控制、视觉、图片生成、TTS 和多模型推理。',
    'Full System Access：读写文件、运行 shell 命令、执行脚本。支持完全访问或沙箱模式，安全级别由你选择。既能自由操作，也能安全隔离。'
  );
  result = result.replace(
    '支持批量轨迹生成、压缩、Atropos RL 环境和面向下一代 tool-calling 模型的数据工作流。',
    'Skills & Plugins：用社区技能扩展功能，也可以自己构建。AI 甚至能自主编写新技能——它曾自己打开浏览器配置 OAuth、生成 API token，全程自主完成。'
  );

  // === 关键修复：替换 CSS 类名 hermes- → oc- ===
  result = result.replace(/class="([^"]*)"/g, (match, classValue) => {
    return match.split('hermes-').join('oc-');
  });
  // 也替换内联 style 中的 hermes- 类引用和 --hermes- 变量
  result = result.replace(/style="([^"]*)"/g, (match, styleValue) => {
    return match.split('hermes-').join('oc-').split('--hermes-').join('--oc-');
  });
  // 替换 data-hermes-* 属性
  result = result.replace(/data-hermes-/g, 'data-oc-');

  // === 替换终端内容 + 打字动画脚本 ===
  result = result.replace(
    '<div class="oc-terminal-body"><span class="oc-cursor"></span></div>',
    '<div class="oc-terminal-body" id="oc-terminal-body"><span class="oc-cursor" id="oc-cursor"></span></div>'
  );

  // 在 </body> 前注入打字动画 JS
  const TYPE_SCRIPT = `<script>
(function(){
  var container = document.getElementById("oc-terminal-body");
  var cursor = document.getElementById("oc-cursor");
  if (!container) return;

  var text = [
    '<span style="color:#fb923c">openclaw setup</span>',
    '  选择模型供应商：智谱 / DeepSeek / Qwen / Kimi / MiniMax',
    '  配置工具集：终端、文件、浏览器、记忆、技能、MCP',
    '\\u2713 OpenClaw \\u5df2\\u51c6\\u5907\\u5c31\\u7eea',
    '',
    '<span style="color:#fb923c">openclaw</span>',
    '  \\u5e2e\\u6211\\u6574\\u7406\\u672c\\u5468\\u9879\\u76ee\\u8fdb\\u5c55\\uff0c\\u5e76\\u53d1\\u5230\\u98de\\u4e66',
    '  session_search \\u201c\\u9879\\u76ee\\u8fdb\\u5c55\\u201d                       0.7s',
    '  read_file ./AGENTS.md                          0.1s',
    '  web_search \\u201c\\u76f8\\u5173\\u4f9d\\u8d56\\u6700\\u65b0\\u7248\\u672c\\u201d                  1.4s',
    '  feishu_send \\u201c\\u672c\\u5468\\u7b80\\u62a5\\u5df2\\u751f\\u6210\\u201d                   0.3s',
    '',
    'Done. \\u6211\\u8fd8\\u4fdd\\u5b58\\u4e86\\u4e00\\u4e2a\\u201c\\u5468\\u62a5\\u6574\\u7406\\u201d\\u6280\\u80fd\\uff0c\\u4e0b\\u6b21\\u4f1a\\u76f4\\u63a5\\u590d\\u7528\\u3002'
  ];
  var html = '';
  var lineIdx = 0, charIdx = 0;
  var speed = 25;

  function typeLine() {
    if (lineIdx >= text.length) {
      if (cursor) cursor.style.animation = "oc-blink 1s step-end infinite";
      return;
    }
    var line = text[lineIdx];
    if (charIdx <= line.length) {
      // Show the cursor at current position
      var displayText = line.substring(0, charIdx);
      var cursorHtml = '<span class="oc-cursor" style="animation:oc-blink 1s step-end infinite;display:inline-block;width:8px;height:1em;background:#fb923c;vertical-align:text-bottom;margin-left:1px"></span>';
      container.innerHTML = html + displayText + cursorHtml;
      charIdx++;
      setTimeout(typeLine, speed);
    } else {
      html += line + '\\n';
      lineIdx++;
      charIdx = 0;
      setTimeout(typeLine, speed * 3);
    }
  }

  container.innerHTML = '';
  typeLine();
})();
</script>`;

  result = result.replace('</body>', TYPE_SCRIPT + '\\n<style>body{font-weight:480;letter-spacing:0.02em}code,pre{font-weight:500}</style>\\n</body>');

  return result;
}

function processCss(content) {
  let result = content;

  // CSS 类名和变量替换
  result = applyRules(result, CSS_CLASS_RULES);

  // 颜色替换
  result = applyRules(result, Object.entries(COLOR_MAP));

  // CSS content 中的品牌名替换
  result = result.replace(/content:"HERMES"/g, 'content:"OPENCLAW"');
  result = result.replace(/content:"Hermes"/g, 'content:"OpenClaw"');

  // === 安全替换: gold → #fb923c（亮橙，只替换 CSS 值位置，不伤变量名）===
  // 用正则定位 ":gold" 或 " gold" 或 ",gold"（值上下文），跳过 "var(--oc-gold)"
  result = result.replace(/(?<!var\()(?<=[:\s,])gold(?=[;\s,\)])/g, '#fb923c');

  return result;
}

function processJs(content) {
  let result = content;

  // JS 先用等长替换
  result = applyRules(result, JS_SAFE_RULES);

  // 品牌名称替换（长度不同但是在字符串中安全）
  result = result.replace(/"Hermes Agent 中文社区"/g, '"OpenClaw 中文社区"');
  result = result.replace(/"Hermes Agent"/g, '"OpenClaw"');
  result = result.replace(/"Hermes"/g, function(match) {
    // 只在看起来像配置字符串时替换
    return '"OpenClaw"';
  });

  // JS 中的颜色值替换
  result = applyRules(result, [
    ['rgb(255, 230, 179)', 'rgb(252, 229, 221)'],  // 旧金色 → 暖白
    ['rgba(255,230,203,', 'rgba(252,229,221,'],     // 旧米白 → 暖白
  ]);

  // JS 中 Unicode 转义的中文品牌名
  result = result.split('Hermes Agent \\u4e2d\\u6587\\u793e\\u533a').join('OpenClaw \\u4e2d\\u6587\\u793e\\u533a');

  // 其他 JS 安全的替换
  result = applyRules(result, [
    ['"Hermes CN"', '"OpenClaw"'],
    ['hermes-cn-og.svg', 'openclaw-og.svg'],
    ['Nous Research', 'OpenClaw'],
    ['nousresearch.com', 'openclaw.ai'],
    ['github.com/NousResearch/hermes-agent', 'github.com/openclaw/openclaw'],
    ['hermesagent.org.cn', 'openclaw.cn'],
    ['res1.hermesagent.org.cn', 'openclawal.cn/scripts'],
 ['res.agthub.tech', 'openclawal.cn/scripts'],
    ['desktop.hermesagent.org.cn', 'desktop.openclaw.cn'],
    ['G-9WJEXHW3PD', 'G-XXXXXXXXXX'],
  ]);

  return result;
}

// ============================================================
// 6. 主处理流程
// ============================================================

async function main() {
  console.log('═══════════════════════════════════════');
  console.log('  OpenClaw 网站改造工具');
  console.log('═══════════════════════════════════════\n');

  console.log(`源目录: ${SRC}`);
  console.log(`目标目录: ${DST}\n`);

  // 清理并复制到 dist
  console.log('复制原始文件...');
  cleanDir(DST);
  copyDir(SRC, DST);

  // 删除特殊页面
  const deletePages = [
    'docs/guides/migrate-from-openclaw',
    'docs/user-guide/skills/optional/migration/migration-openclaw-migration',
  ];
  for (const page of deletePages) {
    const dir = path.join(DST, page);
    if (fs.existsSync(dir)) {
      fs.rmSync(dir, { recursive: true, force: true });
      console.log(`已删除: ${page}`);
    }
  }

  // 重命名专题页目录（保持与 HTML 中的链接一致）
  const renameDirs = [
    ['hermes-agent-installation', 'openclaw-installation'],
    ['hermes-agent-messaging', 'openclaw-messaging'],
    ['hermes-agent-mcp', 'openclaw-mcp'],
  ];
  for (const [old, nw] of renameDirs) {
    const oldPath = path.join(DST, old);
    const newPath = path.join(DST, nw);
    if (fs.existsSync(oldPath) && !fs.existsSync(newPath)) {
      try {
        fs.renameSync(oldPath, newPath);
        console.log(`已重命名: ${old} → ${nw}`);
      } catch (e) {
        console.log(`⚠ 无法重命名 ${old}: ${e.message}`);
      }
    }
  }

  // 遍历所有文件并处理
  let htmlCount = 0, cssCount = 0, jsCount = 0, otherCount = 0;

  function walk(dir) {
    for (const item of fs.readdirSync(dir)) {
      const fp = path.join(dir, item);
      if (fs.statSync(fp).isDirectory()) {
        walk(fp);
        continue;
      }

      const ext = path.extname(item).toLowerCase();
      const relPath = path.relative(DST, fp);

      if (ext === '.html') {
        let content = fs.readFileSync(fp, 'utf-8');
        content = processHtml(content, relPath);
        fs.writeFileSync(fp, content, 'utf-8');
        htmlCount++;
      }
      else if (ext === '.css') {
        let content = fs.readFileSync(fp, 'utf-8');
        content = processCss(content);
        fs.writeFileSync(fp, content, 'utf-8');
        cssCount++;
      }
      else if (ext === '.js') {
        const size = fs.statSync(fp).size;
        if (size > 1000) {
          let content = fs.readFileSync(fp, 'utf-8');
          content = processJs(content);
          fs.writeFileSync(fp, content, 'utf-8');
        }
        jsCount++;
      }
      else if (ext === '.json') {
        let content = fs.readFileSync(fp, 'utf-8');
        content = applyRules(content, TEXT_RULES);
        fs.writeFileSync(fp, content, 'utf-8');
        otherCount++;
      }
      else if (ext === '.xml') {
        let content = fs.readFileSync(fp, 'utf-8');
        content = applyRules(content, TEXT_RULES);
        fs.writeFileSync(fp, content, 'utf-8');
        otherCount++;
      }
      else if (ext === '.ps1' || ext === '.sh') {
        let content = fs.readFileSync(fp, 'utf-8');
        content = applyRules(content, TEXT_RULES);
        fs.writeFileSync(fp, content, 'utf-8');
        otherCount++;
      }
      else if (ext === '.webmanifest') {
        let content = fs.readFileSync(fp, 'utf-8');
        content = applyRules(content, TEXT_RULES);
        fs.writeFileSync(fp, content, 'utf-8');
        otherCount++;
      }
      else {
        otherCount++;
      }
    }
  }

  walk(DST);

  console.log(`\n处理完成！`);
  console.log(`  HTML: ${htmlCount} 个`);
  console.log(`  CSS: ${cssCount} 个`);
  console.log(`  JS: ${jsCount} 个`);
  console.log(`  其他: ${otherCount} 个`);
  console.log(`  输出目录: ${DST}`);

  // 统计
  let totalSize = 0, totalFiles = 0;
  function countFiles(dir) {
    for (const f of fs.readdirSync(dir)) {
      const fp = path.join(dir, f);
      if (fs.statSync(fp).isDirectory()) countFiles(fp);
      else { totalFiles++; totalSize += fs.statSync(fp).size; }
    }
  }
  countFiles(DST);
  console.log(`\n总文件数: ${totalFiles}`);
  console.log(`总大小: ${(totalSize / 1024 / 1024).toFixed(1)} MB`);

  // ======== SEO 后处理 ========
  console.log('\nSEO 优化...');

  // 1. robots.txt
  fs.writeFileSync(path.join(DST, 'robots.txt'),
    'User-agent: *\nAllow: /\n\nSitemap: https://openclawal.cn/sitemap.xml\n', 'utf-8');
  console.log('  ✓ robots.txt');

  // 2. 404 页面
  fs.writeFileSync(path.join(DST, '404.html'), '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>页面未找到 - OpenClaw 中文社区</title>\n<style>\nbody{background:#2a2520;color:#fce5dd;font-family:system-ui,-apple-system,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;text-align:center}\n.c{max-width:480px;padding:2rem}\nh1{font-size:4rem;margin:0;color:#fb923c}\nh2{margin:.5rem 0 1rem;font-weight:400}\np{color:rgba(252,229,221,.7);line-height:1.7}\na{color:#fb923c;text-decoration:none}\na:hover{text-decoration:underline}\n</style>\n</head>\n<body>\n<div class="c">\n<h1>404</h1>\n<h2>页面未找到</h2>\n<p>你访问的页面不存在或已被移动。</p>\n<p><a href="/">← 返回首页</a></p>\n</div>\n</body>\n</html>', 'utf-8');
  console.log('  ✓ 404.html');

  // 3. sitemap.xml
  function walkSitemap(dir) {
    for (const f of fs.readdirSync(dir)) {
      const fp = path.join(dir, f);
      if (f.startsWith('.') || f === 'node_modules') continue;
      if (fs.statSync(fp).isDirectory()) walkSitemap(fp);
      else if (f === 'index.html') {
        const rel = path.relative(DST, path.dirname(fp)).replace(/\\\\/g, '/');
        sitemapUrls.push('https://openclawal.cn/' + (rel || ''));
      }
    }
  }
  const sitemapUrls = [];
  walkSitemap(DST);
  let sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
  for (const url of sitemapUrls.sort()) {
    sitemap += '  <url><loc>' + url.replace(/&/g, '&amp;') + '</loc></url>\n';
  }
  sitemap += '</urlset>\n';
  fs.writeFileSync(path.join(DST, 'sitemap.xml'), sitemap, 'utf-8');
  console.log(`  ✓ sitemap.xml (${sitemapUrls.length} 个 URL)`);

  // 4. Vercel 项目链接（防止误建新项目）
  const vercelDir = path.join(DST, '.vercel');
  if (!fs.existsSync(vercelDir)) fs.mkdirSync(vercelDir);
  fs.writeFileSync(path.join(vercelDir, 'project.json'),
    '{"projectId":"prj_HaVxRISyAU1AR93H85dYWsCUY60l","orgId":"team_gtsmcbv7u3ls0t2R2rpKY8U6"}', 'utf-8');
  console.log('  ✓ .vercel/project.json (已绑定 openclaw 项目)');
}

main().catch(console.error);
