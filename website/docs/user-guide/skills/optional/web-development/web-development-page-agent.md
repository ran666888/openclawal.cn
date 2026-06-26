---
title: "Page Agent"
sidebar_label: "Page Agent"
description: "Embed alibaba/page-agent into your own web application — a pure-JavaScript in-page GUI agent that ships as a single <script> tag or npm package and lets end-..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 页面代理

将 alibaba/page-agent 嵌入到您自己的 Web 应用程序中 - 一个纯 JavaScript 页内 GUI 代理，作为单个 <script> 标记或 npm 包提供，并允许站点的最终用户使用自然语言驱动 UI（“单击登录，将用户名填写为 John”）。无需 Python，无需无头浏览器，无需扩展。当用户是 Web 开发人员，想要将 AI 副驾驶添加到 SaaS/管理面板/B2B 工具、使旧版 Web 应用程序可通过自然语言访问或针对本地（Ollama）或云（Qwen/OpenAI/OpenRouter）LLM 评估页面代理时，请使用此技能。不适用于服务器端浏览器自动化 - 将这些用户指向 OpenClaw 的内置浏览器工具。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/web-development/page-agent` 安装 |
|路径| `可选技能/网络开发/页面代理` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `web`、`javascript`、`agent`、`浏览器`、`gui`、`alibaba`、`embed`、`copilot`、`saas` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 页面代理

alibaba/page-agent (https://github.com/alibaba/page-agent, 17k+ star, MIT) 是一个用 TypeScript 编写的页内 GUI 代理。它位于网页内，将 DOM 作为文本读取（无屏幕截图，无多模式 LLM），并针对当前页面执行自然语言指令，例如“单击登录按钮，然后将用户名填写为 John”。纯客户端——主机站点仅包含一个脚本并传递一个与 OpenAI 兼容的 LLM 端点。

## 什么时候使用这个技能

当用户想要执行以下操作时加载此技能：

- **在自己的网络应用程序中配备人工智能副驾驶**（SaaS、管理面板、B2B 工具、ERP、CRM）——“我的仪表板上的用户应该能够输入‘为 Acme Corp 创建发票并通过电子邮件发送’，而不是点击五个屏幕”
- **现代化旧版 Web 应用程序**，无需重写前端 - 页面代理放置在现有 DOM 之上
- **通过自然语言添加可访问性** - 语音/屏幕阅读器用户通过描述他们想要的内容来驱动 UI
- **针对本地（Ollama）或托管（Qwen、OpenAI、OpenRouter）LLM 演示或评估页面代理**
- **构建交互式培训/产品演示** - 让人工智能在真实的用户界面中引导用户“如何提交费用报告”

## 何时不使用此技能

- 用户希望 **OpenClaw 本身驱动浏览器** → 使用 OpenClaw 的内置浏览器工具 (Browserbase / Camofox)。 page-agent 是*相反*方向。
- 用户想要**跨选项卡自动化而不嵌入** → 使用 Playwright、浏览器使用或页面代理 Chrome 扩展
- 用户需求**视觉基础/屏幕截图**→页面代理仅是文本DOM；使用多模式浏览器代理代替

## 先决条件

- Node 22.13+ 或 24+，npm 10+（文档声称 11+ 但 10.9 工作正常）
- 兼容 OpenAI 的 LLM 端点：Qwen (DashScope)、OpenAI、Ollama、OpenRouter 或任何“/v1/chat/completions”
- 带有开发工具的浏览器（用于调试）

## 路径 1 — 通过 CDN 进行 30 秒演示（无需安装）

查看其工作的最快方法。使用阿里巴巴的免费测试 LLM 代理 — **仅用于评估**，但须遵守其条款。

添加到任何 HTML 页面（或作为书签粘贴到 devtools 控制台）：

````html
<script src="https://cdn.jsdelivr.net/npm/page-agent@1.8.0/dist/iife/page-agent.demo.js" crossorigin="true"></script>
````

出现一个面板。输入指令。完毕。

小书签形式（放入书签栏，单击任意页面）：

```javascript
javascript:(function(){var s=document.createElement('script');s.src='https://cdn.jsdelivr.net/npm/page-agent@1.8.0/dist/iife/page-agent.demo.js';document.head.appendChild(s);})();
````

## 路径 2 — npm 安装到您自己的 Web 应用程序中（生产使用）

在现有的 Web 项目（React / Vue / Svelte / plain）中：

````bash
npm 安装页面代理
````

将其与您自己的 LLM 端点连接起来 — **切勿将演示 CDN 发送给真实用户**：

```javascript
从 'page-agent' 导入 { PageAgent }

常量代理 = 新的 PageAgent({
    型号: 'qwen3.5-plus',
    baseURL: 'https://dashscope.aliyuncs.com/兼容模式/v1',
    apiKey: process.env.LLM_API_KEY, // 从不硬编码
    语言：“en-US”，
})

// 为最终用户显示面板：
代理.面板.show()

// 或者以编程方式驱动它：
wait agent.execute('点击提交按钮，然后将用户名填写为 John')
````

提供程序示例（任何兼容 OpenAI 的端点都可以）：

|供应商| `baseURL` | `模型` |
|----------|------------|---------|
| Qwen / DashScope | `https://dashscope.aliyuncs.com/兼容模式/v1` | `qwen3.5-plus` |
|开放人工智能 | `https://api.openai.com/v1` | `gpt-4o-mini` |
|奥拉马（本地）| `http://localhost:11434/v1` | `qwen3:14b` |
|开放路由器 | `https://openrouter.ai/api/v1` | `人类/克劳德-sonnet-4.6` |

**关键配置字段**（传递给 `new PageAgent({...})`）：

- `model`, `baseURL`, `apiKey` — LLM 连接
- `language` — UI 语言（`en-US`、`zh-CN` 等）
- 允许列表和数据屏蔽挂钩用于锁定代理可以接触的内容 - 请参阅 https://alibaba.github.io/page-agent/ 以获取完整的选项列表

**安全性。** 不要将您的“apiKey”放入客户端代码中以进行真正的部署 - 代理 LLM 调用通过您的后端并将“baseURL”指向您的代理。演示 CDN 的存在是因为阿里巴巴运行该代理进行评估。

## 路径 3 — 克隆源代码库（贡献或破解）

当用户想要修改页面代理本身、通过本地 IIFE 捆绑包针对任意站点测试它或开发浏览器扩展时，请使用此选项。

````bash
git 克隆 https://github.com/alibaba/page-agent.git
cd 页面代理
npm ci # 精确的锁定文件安装（或“npm i”以允许更新）
````

使用 LLM 端点在存储库根目录中创建“.env”。示例：

````
LLM_MODEL_NAME=gpt-4o-mini
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.openai.com/v1
````

奥拉玛口味：

````
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=NA
LLM_MODEL_NAME=qwen3:14b
````

常用命令：

````bash
npm start # 文档/网站开发服务器
npm run build # 构建每个包
npm run dev:demo # 在 http://localhost:5174/page-agent.demo.js 上提供 IIFE 包
npm run dev:ext # 开发浏览器扩展（WXT + React）
npm run build:ext # 构建扩展
````

**使用本地 IIFE 包在任何网站上进行测试**。添加此书签：

```javascript
javascript:(function(){var s=document.createElement('script');s.src=`http://localhost:5174/page-agent.demo.js?t=${Math.random()}`;s.onload=()=>console.log('PageAgent 准备就绪！');document.head.appendChild(s);})();
````

然后：`npm run dev:demo`，单击任意页面上的书签，本地构建注入。保存时自动重建。

**警告：** 您的 `.env` `LLM_API_KEY` 在开发构建期间内联到 IIFE 包中。不要共享捆绑包。别犯了。不要将 URL 粘贴到 Slack 中。 （已验证：grep 公共开发包会返回“.env”中的文字值。）

## 仓库布局（路径 3）

Monorepo 与 npm 工作区。关键包：

|套餐 |路径|目的|
|---------|------|---------|
| `页面代理` | `packages/page-agent/` |带 UI 面板的主条目 |
| `@page-agent/core` | `包/核心/` |核心代理逻辑​​，无UI |
| `@page-agent/mcp` | `包/mcp/` | MCP 服务器（测试版）|
| — | `包/llms/` |法学硕士客户|
| — | `packages/page-controller/` | DOM 操作 + 视觉反馈 |
| — | `包/ui/` |面板+i18n |
| — | `包/扩展/` | Chrome/Firefox 扩展 |
| — | `包/网站/` |文档+登陆站点|

## 验证其是否有效

路径 1 或路径 2 之后：
1.在浏览器中打开devtools打开页面
2. 您应该看到一个浮动面板。如果没有，请检查控制台是否有错误（最常见：LLM 端点上的 CORS、错误的“baseURL”或错误的 API 密钥）
3. 输入与页面上可见内容相匹配的简单说明（“单击登录链接”）
4. 观察“网络”选项卡 — 您应该会看到对“baseURL”的请求

路径 3 之后：
1. `npm run dev:demo` 打印 `Accepting Connections at http://localhost:5174`
2. `curl -I http://localhost:5174/page-agent.demo.js` 返回 `HTTP/1.1 200 OK` 和 `Content-Type: application/javascript`
3. 单击任意站点上的书签；出现面板

## 陷阱

- **生产中的演示 CDN** — 不需要。它有速率限制，使用阿里巴巴的免费代理，并且他们的条款禁止生产使用。
- **API 密钥暴露** — 传递给 `new PageAgent({apiKey: ...})` 的任何密钥都包含在您的 JS 包中。始终通过您自己的后端进行代理以进行实际部署。
- **非 OpenAI 兼容端点** 无提示地失败或出现神秘错误。如果您的提供商需要原生 Anthropic/Gemini 格式，请在前面使用 OpenAI 兼容代理（LiteLLM、OpenRouter）。
- **CSP 阻止** — 具有严格内容安全策略的站点可能拒绝加载 CDN 脚本或不允许内联评估。在这种情况下，请从您的来源进行自我托管。
- **在路径 3 中编辑`.env`后重新启动开发服务器** — Vite 仅在启动时读取 env。
- **节点版本** — 存储库声明 `^22.13.0 || >=24`。 Node 20 将因引擎错误而失败“npm ci”。
- **npm 10 与 11** — 文档说 npm 11+； npm 10.9 实际上运行得很好。

## 参考

- 仓库：https://github.com/alibaba/page-agent
- 文档：https://alibaba.github.io/page-agent/
- 许可证：MIT（基于浏览器使用的 DOM 处理内部结构构建，版权所有 2024 Gregor Zunic）