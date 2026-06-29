# OpenClaw 中文社区网站 — 项目规范

## 身份

本站（openclawal.cn）是 OpenClaw 的中文社区站点。文档区内容来自 docs.openclaw.ai 中文版（VitePress 抓取，609 篇）。

**⚠️ 域名是 openclawal.cn，不是 openclaw.cn。openclaw.cn 不是本项目的域名，不要在任何场景提及或引用它。**

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

## 项目部署信息

### 技术栈
- 静态站点，Docusaurus 构建产物放在 `dist/` 目录
- 部署到 Vercel（项目名：`oc-site`，团队：`wahhra-s-projects`）
- GitHub 仓库：`ran666888/openclawal.cn`（main 分支）
- 域名：`openclawal.cn`（由 ran666888 注册，绑定到 wahhra-s-projects 团队）
- Vercel CLI 已登录，可通过 CLI 操作部署和 alias

### 工作目录（唯一）
- 本地：`~/oc-site/`（即 `C:\Users\50148\oc-site`）
- ⚠️ 旧目录 `~/projects/openclaw中文社区网站/` 已废弃，不可使用
- 本地预览：Python http.server port 3003
- 本地服务器：`start.js`（Node.js http + zlib gzip）

### 部署流程（只走 git push，不用手动 vercel deploy）
1. 修改 `dist/` 下的文件（只在 `~/oc-site/` 下操作）
2. `git add` + `git commit` + `git push` → Vercel 自动构建
3. 如果自动 alias 失败，手动执行：
   ```
   npx vercel alias set <deployment-url> openclawal.cn --scope wahhra-s-projects
   ```
4. ⛔ 绝对不要从旧目录 `~/projects/openclaw中文社区网站/` 部署——它会重新创建已删除的 openclaw 项目

---

## 当前项目状态（2026-06-27）

### 已完成
1. ✅ 文档区从 Hermes Agent 文档全面换成 docs.openclaw.ai 中文版（609 篇）
2. ✅ 文档查看器重写为三栏 VitePress 布局（左目录 + 内容 + 右侧大纲）
3. ✅ 侧边栏从官网实时抓取，10 个 Tab 对应正确分类
4. ✅ gzip 压缩加速 JSON 加载
5. ✅ 官网 CSS 作用域化到 `#oc-docs-viewer`
6. ✅ 技能页数据改为真实 OpenClaw 内置 57 个技能
7. ✅ 技能页分类和描述翻译为中文
8. ✅ 验证流程升级为 5 层全量验证
9. ✅ 完整备份（`dist-backup-20260626_030257`，265MB）
10. ✅ 全站域名替换：JS bundle 中 `openclaw.cn` → `openclawal.cn`（解决 React Hydrate 覆盖）
11. ✅ 全站安全头配置（X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, CSP）
12. ✅ 结构化数据增强（Organization, SoftwareApplication, Article, FAQPage, SiteNavigationElement, hreflang）
13. ✅ SEO 基础强化（唯一 h1, 优化 title/description, canonical）
14. ✅ 创建 404 友好页面
15. ✅ favicon 全套生成（svg, 16x16, 32x32, apple-touch-icon, ico）
16. ✅ robots.txt 优化（含 Crawl-delay）
17. ✅ sitemap 增加 lastmod
18. ✅ Vercel Alias 修复（域名重新绑定到最新部署）
19. ✅ Logo 替换为桌面照片（928×928 PNG）
20. ✅ 首页 Title 改为「OpenClaw 中文社区：OpenClaw 中文文档、安装教程与指南」
21. ✅ 首页 Description 改为「OpenClaw 是一个开源、自托管、支持长期记忆与 Skills 的 AI Agent。它既能在终端中完成复杂任务，也能通过消息网关在微信、飞书、QQ 等平台上持续工作。」
22. ✅ OG/Twitter 标签全部同步（title, description, image）
23. ✅ JSON-LD 描述同步更新
24. ✅ 所有改动已推送 GitHub 并部署到 Vercel，线上验证通过
25. ✅ 日报正文页 `dist/reports/daily/2026-06-27.html` 已生成（20篇）

### 最近一次全量验证结果（2026-06-27）
| 页面 | HTTP 状态 | 备注 |
|------|----------|------|
| `https://openclawal.cn/` | 200 ✅ | Title/Desc/OG 均更新 |
| `https://openclawal.cn/img/logo.png` | 200 ✅ | 新照片替换 928×928 |
| `https://openclawal.cn/img/openclaw-og.png` | 200 ✅ | 新 OG 图 |
| 安全头 | 全部到位 ✅ | X-Frame/X-Content/Referrer/CSP/Permissions |
| 域名引用 | 0 个 `openclaw.cn` ✅ | 56 个 `openclawal.cn` |

### 已知问题（待排查/修复）
1. ❌ **`dist/assets/css/docs-site.css` 返回 404** — 文件被误删。文档区如果没有此 CSS，所有 VitePress 样式丢失。
2. ❌ **`docs-viewer.js` 中 `convertCards()` 嵌套结构 bug** — 空的 `<a>` 和包裹 `<div>` 导致 Card 组件可能渲染异常。
3. ⏳ **Google 尚未收录** — 需要提交 Google Search Console。
4. ⏳ **Sitelinks 未生成** — Google 收录后自动生成，不能手动设置。

### 最新备份
- ✅ `dist-backup-20260626_030257` — 265MB，2026-06-26 最新完整备份
- 旧备份：`color-backup-20260625_161822`、`dist_backup2`

---

## 2026-06-27 完整会话记录

### 做了什么

#### 1. Vercel 部署故障修复
- **问题**：之前部署新代码后，`openclawal.cn` 域名指向了旧部署，手动删除 alias 后导致域名 404
- **修复**：使用 `npx vercel alias set` 将域名重新绑定到最新部署（`openclaw-a78504cx4-wahhra-s-projects.vercel.app`）
- **验证**：curl 确认 200 ✅，全部安全头到位 ✅

#### 2. Logo 替换
- 从桌面照片 `photo_2026-06-27_03-07-15.jpg`（928×928）替换为所有图标：
  - `dist/img/logo.png` — 导航栏 Logo
  - `dist/img/favicon-16x16.png` — 16px 图标
  - `dist/img/favicon-32x32.png` — 32px 图标
  - `dist/img/apple-touch-icon.png` — 180px Apple 图标
  - `dist/img/openclaw-og.png` — 1200×630 OG 分享图
- **使用工具**：Python PIL（Pillow）生成所有尺寸

#### 3. 首页 SEO 元数据更新
- **Title**：`OpenClaw 中文社区：OpenClaw 中文文档、安装教程与指南`
- **Meta Description**：`OpenClaw 是一个开源、自托管、支持长期记忆与 Skills 的 AI Agent。它既能在终端中完成复杂任务，也能通过消息网关在微信、飞书、QQ 等平台上持续工作。`
- **OG/Twitter**：title、description、image 全部同步更新
- **JSON-LD**：WebSite、WebPage 的描述同步更新
- **OG Image URL**：从 `.svg` 改为 `.png`

#### 4. 子页面 SEO 准备（为 sitelinks）
- `SiteNavigationElement` 结构化数据已在 JSON-LD 中，包含所有导航项（安装教程、文档、技能、生态、社区、日报、消息网关、MCP、关于）
- 子页面 title/description 将在 Google 收录后自然展现为 sitelinks

#### 5. 部署验证
- git push 到 `ran666888/openclawal.cn` main 分支
- Vercel 自动构建（`openclaw-ph79mne2a`，用时 18s）
- 手动 alias 到 `openclawal.cn`
- 线上 curl 验证：Title、Description、OG Image、Logo 全部正确 ✅

### Vercel 操作备忘
- 项目在团队 `wahhra-s-projects` 下，域名 `openclawal.cn` 注册在个人账号后在团队下管理
- `npx vercel alias set <deployment-url> openclawal.cn --scope wahhra-s-projects` — 手动绑定域名
- ⚠️ 删除 alias 会导致域名 404，恢复方法同上
- 部署后如果域名没自动指到新版，需要手动 alias

### 用户偏好（新增/确认）
- 极度厌恶别人替用户做决定（删 alias 没问用户，直接导致问题）
- 说「恢复」时要列出所有版本让用户选，不能自己动手
- 改完后必须线上验证（curl 检查 meta），不能只报「推成功了」
- 这个站只是 openclawal.cn，和 openclaw.cn 或其他网站没有关系
- 提交到 Google Search Console 是下一步的关键动作

### 未完成/待办（明天继续）
1. 🔴 **提交 Google Search Console** — 让 Google 收录 `openclawal.cn`
2. 🔴 `docs-site.css` 404 待修复
3. 🔴 卡片网格布局嵌套 bug 待修复
4. ⏳ 等待 Google 收录后检查 sitelinks 展现效果
5. ⏳ 如需要，进一步优化子页面 title/description

---

## 2026-06-26 会话记录

### 做了什么
1. **Chrome DevTools MCP 安装尝试** — 在 `~/.hermes/config.yaml` 添加了 `chrome-devtools` MCP 服务器。需要完全重启 Hermes 后新会话才能加载。
2. **Skill 升级** — `openclaw-site-collaboration-protocol` 全面重写为 master skill
3. **验证流程升级** — 从简单「三步验证」改为「5 层全量验证」
4. **发现 docs-site.css 404** — 验证时发现文档区 CSS 文件缺失
5. **完整备份** — `dist-backup-20260626_030257`

---

## 文档系统架构

### 数据源
- `dist/docs-articles.json` — 所有文章内容（609 篇，~30MB）
- `dist/docs-config.json` — 侧边栏结构
- `docs-system/fetch-chinese-docs.py` — 批量抓取脚本
- `docs-system/build-exact-sidebar.py` — 从官网重新生成侧边栏配置
- `docs-system/build-docs.py` — .md → docs-articles.json

### 查看器
- `dist/assets/js/docs-viewer.js` — 文档查看器 v4.2，三栏 VitePress 布局
- `dist/assets/css/docs-site.css` — ⚠️ 当前返回 404，文件丢失
- `start.js` — 本地服务器（Node.js http + zlib gzip）
- 端口通过 `PORT` 环境变量配置，默认 3003

### 技能页
- `dist/skills/index.html` — 独立静态 HTML，57 个真实 OpenClaw 内置技能
- 数据来源：本地 OpenClaw 包的 `skills/*/SKILL.md` 文件
- 分类：开发工具(15)、效率工具(14)、媒体与创意(8)、通信与消息(7)、AI 助手(7)、系统运维(4)、智能家居(2)

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

---

## 用户极端厌恶清单

| 行为 | 后果 |
|------|------|
| 替用户做决定 / 自作主张 | 暴怒 |
| 搞混品牌（OpenClaw ≠ Hermes） | 直接骂傻逼 |
| 搞混域名（openclawal.cn ≠ openclaw.cn） | 极其愤怒 |
| 画蛇添足（加没要求的功能） | 「你为什么又画蛇添足？」 |
| 不改问题分析技术原因 | 「认错不是过关，改才是」 |
| 说「可能」「大概」 | 「不能用可能来评判」 |
| 不看页面就改视觉 | 「你每次能不能看着页面改？」 |
| 改设计/排版/结构 | 直接发火 |
| 改完不验证就报完成 | 「你必须打开页面看一看呀」 |
| 删 alias 不问用户 | 导致域名 404 |

---

## 全站规则

### 外部链接行为
所有指向站外（非 openclawal.cn）的链接必须使用 `target="_blank" rel="noopener noreferrer"`，在新标签页打开。

### Docusaurus SPA 路由绕过（docs-viewer.js）
Docusaurus 用 capture-phase 事件监听拦截内部链接点击。Bubble-phase 的点击处理器无法阻止它。
- 关键：Docusaurus 编译页用 React SPA router，在 capture phase 运行

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
3. Vercel alias 删除后会导致域名 404，需用 `npx vercel alias set` 重新绑定
4. 侧边栏配置必须从官网 HTML 实时抓取，不能用路径自动生成
5. 内容包含 VitePress 组件标签（Tabs、Card、Note 等），不能删除
6. `docs-site.css` 易被误删，返回 404 时文档区样式全丢
