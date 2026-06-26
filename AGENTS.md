# OpenClaw 中文社区网站 — 项目规范

## 身份

本站（openclaw.cn）是 OpenClaw 的中文社区站点。文档区内容来自 docs.openclaw.ai 中文版（VitePress 抓取，609 篇）。

---

## 核心铁律（从翻车中总结）

### 第一条：1:1 复制，不创新
用户说「复制官网」就是复制官网。不能：
- 改 Tab 名称（「代理」不能改成「核心概念」）
- 加设计元素（折叠/展开、额外动画）
- 删内容（VitePress 组件标签是设计的一部分）
- 改样式（颜色、间距、字体）
- 改命名、加功能、自作主张「优化」
- 改设计文件（主样式表、HTML 结构）
- 如果内容不显示，只改查看器的提取/渲染逻辑，不动页面本身

### 第二条：动手前先确认方案
任何文件/配置修改前，先展示具体改动内容，等用户回复「执行」「确认」再动手。

### 第三条：改完就全量验证
改完一个功能点后必须用全套工具交叉验证，再改下一个。不能攒一堆一起验证。

**全量验证 5 层流程：**
1. **服务层**（`curl`）— 遍历所有页面，全部返回 200。关键文件（`docs-articles.json`、`docs-viewer.js`、**`docs-site.css`**）无 404
2. **浏览器层**（`browser_navigate` + `browser_snapshot`）— 页面正常打开，元素树完整
3. **JS 引擎层**（`browser_console`）— 0 个 JS 错误
4. **视觉层**（`browser_vision` 截图）— 无视觉异常（失败时靠其他层替代）
5. **DOM 样式**（`browser_console` 跑 JS，用 `getComputedStyle` / `getBoundingClientRect`）— CSS 实际生效

**常见故障：** `docs-site.css` 容易被误删，返回 404 时文档区样式全丢

### 第四条：提前检查边界
- JSON 文件大小：30MB+ 的内容要提前评估加载时间，加 gzip 压缩
- CSS 作用域：官网 CSS 的 `:root` 和 `body` 规则必须作用域化到 `#oc-docs-viewer`
- 数据一致性：抓取的内容要确保路径匹配
- Python 代码替换操作前先确认实际文件内容，避免替换模式不匹配

### 第五条：不改设计
- 不能修改网站的设计、排版、位置、HTML 结构
- 只改文字内容时也要先问方案再执行

---

## 当前项目状态（2026-06-26）

### 关键 Skill
- `openclaw-site-collaboration-protocol` 已升级为 **v2.0**（master skill），涵盖：站点架构、4种修改模型、文档系统、Skill页面、设计组件库、翻车铁律大全、常见操作速查、用户极端厌恶清单
- 所有修改前必须先加载此 skill

### 已完成
1. ✅ 文档区从 Hermes Agent 文档全面换成 docs.openclaw.ai 中文版（609 篇）
2. ✅ 文档查看器重写为三栏 VitePress 布局（左目录 + 内容 + 右侧大纲）
3. ✅ 侧边栏从官网实时抓取，10 个 Tab 对应正确分类
4. ✅ gzip 压缩加速 JSON 加载
5. ✅ 官网 CSS 作用域化到 `#oc-docs-viewer`
6. ✅ 技能页数据改为真实 OpenClaw 内置 57 个技能（从本地包 SKILL.md 读取）
7. ✅ 技能页分类和描述翻译为中文
8. ✅ 验证流程升级为 5 层全量验证（curl + browser_snapshot + browser_console + browser_vision + DOM 检查）
9. ✅ `openclaw-site-collaboration-protocol` skill 升级到 v2.0，验证流程从三步改为全量 5 层
10. ✅ AGENTS.md 同步更新验证铁律
11. ✅ 最新完整备份已创建

### 最近一次全量验证结果（2026-06-26）
| 页面 | HTTP 状态 | 大小 |
|------|----------|------|
| `/` | 200 | 56,866 bytes |
| `/about/` | 200 | 28,041 bytes |
| `/community/` | 200 | 30,038 bytes |
| `/skills/` | 200 | 40,499 bytes |
| `/daily/` | 200 | 47,132 bytes |
| `/practice-guides/` | 200 | 64,906 bytes |
| `/releases/` | 200 | 28,394 bytes |
| JS 错误 | 0 个 | ✅ |

### 已知问题（待排查/修复）
1. ❌ **`dist/assets/css/docs-site.css` 返回 404** — 文件被误删。文档区如果没有此 CSS，所有 VitePress 样式丢失（背景变白、布局崩坏）。需要从备份恢复或重新从 docs.openclaw.ai 下载并作用域化。
2. ❌ **`docs-viewer.js` 中 `convertCards()` 嵌套结构 bug** — 空的 `<a>` 和包裹 `<div>` 导致 Card 组件可能渲染异常。用户尚未下达修复指令。

### 最新备份
- ✅ **`dist-backup-20260626_030257`** — 265MB，2026-06-26 最新完整 dist/ 备份
- 旧备份：`color-backup-20260625_161822`（配色备份）、`dist_backup2`（6月24日旧版）

---

## 2026-06-26 会话记录

### 做了什么
1. **Chrome DevTools MCP 安装尝试** — 在 `~/.hermes/config.yaml` 添加了 `chrome-devtools` MCP 服务器（`npx chrome-devtools-mcp@latest --browserUrl http://localhost:9222`），包已安装但不显示在工具列表中。需要完全重启 Hermes 后新会话才能加载。
2. **Skill 升级** — `openclaw-site-collaboration-protocol` 全面重写为 master skill，涵盖所有网站修改知识
3. **验证流程升级** — 从简单「三步验证」改为「5 层全量验证」，写入 skill + AGENTS.md
4. **发现 docs-site.css 404** — 验证时发现文档区 CSS 文件缺失
5. **完整备份** — `dist-backup-20260626_030257`

### 用户偏好确认
- 极度重视验证准确性，要求「所有命令和工具都用上去确保」
- 要求 skill 足够细致，「到时候直接读内容」
- 要求项目文件（AGENTS.md）保持最新状态，确保第二天工作无缝衔接

### 未完成/待办
- 🔴 Chrome DevTools MCP 工具仍未出现在工具列表中（需用户执行 `hermes stop` + `hermes start` 完全重启后在新会话中生效）
- 🔴 `docs-site.css` 404 待修复
- 🔴 卡片网格布局嵌套 bug 待修复

---

## 2026-06-24 全线翻车复盘

### 翻车 1：Tab 名称擅自修改
- **问题**：把官方 Tab「代理」写成了「核心概念」
- **教训**：官网叫啥就写啥，不要自己觉得

### 翻车 2：删 VitePress 组件标签
- **问题**：为了压缩文件大小，删了 `<Tabs>`、`<Card>`、`<Note>` 等标签
- **教训**：VitePress 的组件标签是页面视觉元素，不能删

### 翻车 3：侧边栏加折叠功能
- **问题**：子分类默认折叠，要点才展开
- **教训**：官网所有链接直接展开显示，不要加交互

### 翻车 4：CSS 污染全站
- **问题**：官网 CSS 的 `:root{--bg}` 把整个页面背景改黑了
- **教训**：第三方 CSS 必须先作用域化到容器内

### 翻车 5：30MB JSON 加载慢
- **问题**：609 篇文章 30MB，浏览器加载超时
- **教训**：大 JSON 加 gzip 压缩

### 翻车 6：侧边栏混入其他分类
- **问题**：「代理」分类下的链接因为路径匹配被混入了「快速开始」
- **教训**：直接取当前 Tab 对应的分类，不做跨分类过滤

### 翻车 7：多渲染一层分类标题
- **问题**：侧边栏多了「快速开始」标题，官网没有
- **教训**：只渲染子分类标题+链接，不渲染顶层分类

### 翻车 8：Python 替换没匹配到代码
- **问题**：多次修改后代码变了，替换模式没跟着更新
- **教训**：替换前先 grep 确认实际内容

### 翻车 9：技能页内容空白
- **问题**：技能卡片不显示，因为 CSS 在 `<head>` 里，`loadSection` 提取 `<main>` 时丢掉
- **教训**：只改查看器的提取逻辑（让 `<style>` 也带上），不动页面本身

### 翻车 10：改主样式表
- **问题**：往主样式表追加 CSS，导致全站设计变化
- **教训**：死都不能动主样式表，内容不显示就修加载方式

---

## 文档系统架构

### 数据源
- `dist/docs-articles.json` — 所有文章内容（从 docs.openclaw.ai/zh-CN/ 抓取，609 篇，~30MB）
- `dist/docs-config.json` — 侧边栏结构（从官网 HTML 的 `<aside class="sidebar">` 实时提取）
- `docs-system/fetch-chinese-docs.py` — 批量抓取脚本
- `docs-system/build-exact-sidebar.py` — 从官网重新生成侧边栏配置
- `docs-system/build-docs.py` — .md → docs-articles.json

### 查看器
- `dist/assets/js/docs-viewer.js` — 文档查看器 v4.2，三栏 VitePress 布局
- `dist/assets/css/docs-site.css` — ⚠️ 官网 CSS（**当前返回 404，文件丢失**），需要作用域化到 `#oc-docs-viewer`
- `start.js` — 本地服务器（Node.js http + zlib gzip）
- 端口通过 `PORT` 环境变量配置，默认 3003

### 技能页
- `dist/skills/index.html` — 独立静态 HTML，57 个真实 OpenClaw 内置技能
- 数据来源：本地 OpenClaw 包的 `skills/*/SKILL.md` 文件
- 分类：开发工具(15)、效率工具(14)、媒体与创意(8)、通信与消息(7)、AI 助手(7)、系统运维(4)、智能家居(2)
- 加载方式：`loadSection('skills')` fetch `/skills/index.html`，提取 `#oc-skills-viewer` 或 `<main>` 并保留 `<style>`

### 社区二维码小部件
- `dist/index.html` 中 `<aside class="oc-community-widget">`
- 折叠按钮：`<button class="oc-community-widget-toggle">`

### 文档区布局
```
[网站原有顶栏 — Logo、文档、社区、技能...]
[Tab 导航 — 快速开始、安装、消息渠道、代理、工具、模型、平台、网关与运维、参考、帮助]
.doc-shell (grid: 340px + 1fr; gap:72px)
  ├── .sidebar (sticky, 宽度340px → 站点主题覆盖260px)
  └── .main (grid: minmax(0,760px) + 250px; gap:76px)
       ├── .article → #ocs-content（文章正文）
       └── aside.toc → 本页内容（从 h2 自动生成）
```

### Tab 与侧边栏对照
| Tab 名 | Section 标识 | 抓取来源 |
|--------|-------------|---------|
| 快速开始 | start | /zh-CN/start/showcase |
| 安装 | install | /zh-CN/install |
| 消息渠道 | channels | /zh-CN/channels |
| 代理 | concepts | /zh-CN/concepts/architecture |
| 工具 | tools | /zh-CN/tools |
| 模型 | providers | /zh-CN/providers |
| 平台 | platforms | /zh-CN/platforms |
| 网关与运维 | gateway | /zh-CN/gateway |
| 参考 | cli | /zh-CN/cli |
| 帮助 | help | /zh-CN/help |

### 侧边栏渲染规则
- `renderSidebar()` 根据 `currentSection` 找到对应的 Tab 分类
- **直接取该分类的 `items` 渲染，不做跨分类过滤**
- `buildSidebar()` **不渲染顶层分类标题**，只渲染子分类 `<h2>` + 链接
- 所有链接**默认展开显示**，不加折叠
- 路径映射 `sectionPathMap` 处理 `/docs/vps/` → install、`/docs/install/node/` → help 等特殊情况

### docs-viewer.js 核心函数
| 函数 | 作用 |
|------|------|
| `showDocs(path)` | hash 路由入口 `#docs/...` |
| `navigateTo(path)` | 侧边栏链接点击导航 |
| `renderSidebar()` | 渲染侧边栏 |
| `loadContent(path)` | 从 JSON 加载并渲染文章 |
| `updateTabs()` | 更新 Tab 高亮 |
| `convertCards()` | VitePress CardGroup/Card → 标准 HTML |
| `hrefToSection(path)` | 路径→版块映射（含 sectionPathMap） |
| `normalizePath(path)` | 确保路径带尾部斜杠 |

---

## 用户极端厌恶清单

| 行为 | 后果 |
|------|------|
| 搞混品牌（OpenClaw ≠ Hermes） | 直接骂傻逼 |
| 自作主张做决定 | 暴怒 |
| 画蛇添足（加没要求的功能） | 「你为什么又画蛇添足？」 |
| 不改问题分析技术原因 | 「认错不是过关，改才是」 |
| 说「可能」「大概」 | 「不能用可能来评判」 |
| 不看页面就改视觉 | 「你每次能不能看着页面改？」 |
| 改设计/排版/结构 | 直接发火 |
| 自行决定改 locales 跳过构建 | 「你为什么要这样做？」 |

---

## 全站规则

### 外部链接行为
所有指向站外（非 openclaw.cn）的链接必须使用 `target="_blank" rel="noopener noreferrer"`，在新标签页打开，不覆盖本站页面。

### Docusaurus SPA 路由绕过（docs-viewer.js）
Docusaurus 用 capture-phase 事件监听拦截内部链接点击。Bubble-phase 的点击处理器无法阻止它。
- Fix 1（start.js）：服务端 SPA fallback — `/docs/*` 路径匹配不到真实文件时，返回 index.html 而非 404
- Fix 2（docs-viewer.js init）：页面加载时如果 `pathname.startsWith('/docs/')`，重定向到 `/#docs`
- Fix 3（docs-viewer.js init）：capture-phase click listener 拦截所有 `/docs/` 链接点击，用 `e.stopImmediatePropagation()` + `window.location.href` 强制全页导航
- Fix 4：docs-viewer.js 必须在所有包含 `/docs/` 链接的页面加载，不只 index.html
- 关键：Docusaurus 编译页用 React SPA router，在 capture phase 运行，bubble-phase handlers 无法阻止

---

## 当前配色方案

- 页面背景：`#0f0f1a` 深蓝紫
- 卡片底色：`rgba(10, 48, 48, 0.72)` 半透明深绿
- 强调色：`#fb923c` 暖橙
- 标签文字：`#5eead4` 青绿
- 文字主色：`#ffe6cb` 奶油色（文档区）/ `#e4e4f0` 暖白（其他页面）
- 标题渐变：橙→琥珀（`#fb923c` → `#fbbf24`）
- 面板底：带 blur 的半透明深色

---

## 已知坑

1. `/docs/vps/`（Linux 服务器）属于「安装」版块，但路径不匹配 `/docs/install/` 前缀
2. `/docs/install/node/`（Node 运行时）属于「帮助」版块，不在「安装」里
3. `write_file` 工具在 Windows 下路径会多出 `/c/` 前缀，写完后需 `cp` 修复
4. 侧边栏配置必须从官网 HTML 实时抓取，不能用路径自动生成
5. 内容包含 VitePress 组件标签（Tabs、Card、Note 等），这些是设计的一部分，不能删
6. 查看器加载 `docs-articles.json`（~30MB）需要时间，要考虑加载状态
7. 技能页 CSS 通过 `loadSection` 的 style 提取逻辑带上，不能写在主样式表
8. 真实 OpenClaw 内置技能 57 个（非 95/62 个），数据在 openclaw npm 包的 `skills/` 目录
9. `docs-site.css` 容易被误删，删除后文档区样式全丢（当前状态：⚠️ 文件缺失，返回 404）
10. Docusaurus 编译 HTML 的属性引号用 `\"`，`patch` 工具难以匹配，需用 Python `str.replace()` 替换
