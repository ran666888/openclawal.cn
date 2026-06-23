# OpenClaw 中文社区网站 — 项目转接文档

## 项目概况

| 项目 | 内容 |
|------|------|
| 项目名 | OpenClaw 中文社区网站 |
| 位置 | `C:\Users\50148\projects\openclaw中文社区网站\` |
| 原始来源 | [hermesagent.org.cn](https://hermesagent.org.cn/) (Hermes Agent 中文社区) |
| 框架 | Docusaurus v3.9.2 (静态构建，无源码) |
| 当前状态 | 品牌改造中，已完成约 85% |

---

## 目录结构

```
openclaw中文社区网站/
├── HANDOVER.md          ← 本文档
├── transform.js         ← 一键改造脚本（核心！）
├── create-logo.js       ← Logo/品牌图片生成器
├── start.js             ← 本地 HTTP 服务器
├── site/                ← 原始 Hermes 站点（备份，勿动）
└── dist/                ← 改造后的 OpenClaw 站点（运行产物）
```

---

## 改造工具说明

### transform.js — 核心改造脚本

读取 `site/` → 输出 `dist/`。**每次修改规则后都必须重新运行。**

运行方式：
```bash
cd "C:\Users\50148\projects\openclaw中文社区网站"
node transform.js
node create-logo.js
```

#### 里面的替换规则

| 位置 | 说明 |
|------|------|
| `TEXT_RULES` (约 60 行) | 全站通用文本替换：Hermes Agent → OpenClaw、域名、GitHub 链接等 |
| `COLOR_MAP` (约 80 行) | 颜色值映射：旧色 → 新配色 |
| `CSS_CLASS_RULES` (约 70 行) | CSS 类名替换：`.hermes-` → `.oc-` |
| `JS_SAFE_RULES` (约 62 行) | JS 中等长字符串替换（不影响代码逻辑） |
| `processHtml()` | HTML 文件处理：属性替换、类名同步、对比区块删除、终端动画注入 |
| `processCss()` | CSS 处理：类名替换 + 颜色替换 + gold 安全替换 |
| `processJs()` | JS 处理：等长替换 + 颜色替换 + Unicode 品牌名替换 |

> ⚠️ **重要**：规则顺序影响结果！长匹配必须放在短匹配之前（例如 `res1.hermesagent.org.cn` 必须在 `hermesagent.org.cn` 之前）。

### create-logo.js — 品牌图片

生成 logo.svg、favicon.svg、openclaw-og.svg 等。用户自定义的 `logo.png` 会优先使用。

---

## 当前配色方案（第⑥组）

```
背景     #2a2520    暖深灰（暗色主题）
卡片     #35302b    暖中灰
主文字   #fce5dd    暖白
高亮色   #fb923c    亮橙（文字高亮、边框、按钮）
强调色   #5496a2    青蓝（UI 强调、部分边框）
成功色   #80abb1    青灰
亮色底   #dfd7d3    暖灰
```

---

## 已完成的工作

- [x] 全站品牌名替换：Hermes Agent → OpenClaw（HTML + CSS + JS）
- [x] CSS 类名替换：hermes- → oc-（含 HTML 中的 class 属性同步）
- [x] logo 替换为用户提供的图片（logo.png + logo.svg）
- [x] 配色方案改为第⑥组 + 亮橙高亮
- [x] 删除迁移指南页面（migrate-from-openclaw）
- [x] 删除 Hermes vs OpenClaw 对比区域
- [x] GitHub 链接指向 openclaw/openclaw
- [x] 域名替换：hermesagent.org.cn → openclaw.cn
- [x] 安装镜像地址：res.agthub.tech（国内加速）
- [x] GA / AdSense 清除
- [x] 终端打字动画（从 Hermes 改为 OpenClaw 操作演示）
- [x] meta theme-color 更新
- [x] site.webmanifest 更新
- [x] 多语言版本同步改造（繁中/英文）
- [x] sitemap.xml 域名替换
- [x] 所有旧 rgba 背景色清除（35 处 → 暖深灰）
- [x] community-v3-* 独立变量体系替换
- [x] CSS content:"HERMES" → "OPENCLAW"

---

## 未完成/需要注意的事项

### 1. 安装脚本仍是 Hermes Agent（需你自己处理）
`res.agthub.tech/install.sh` 里写的是 `# Hermes Agent 安装`。如果你希望用户装的是独立的 OpenClaw 版本，需要：
- 替换 `res.agthub.tech` 上的 install.sh 和 install.ps1
- 或者在服务器上放 OpenClaw 自己的安装包

### 2. 外部链接有的是原来的
- Discord 链接仍指向 NousResearch 的 Discord
- 如果需要 OpenClaw 自己的社区链接，替换 `discord.gg/NousResearch`
- 页脚的 "Enzo Li" 设计署名等，如果需要调整

### 3. JS 中仍有大量 "Hermes" 引用（文档内容）
主 JS 包 (main.68955185.js) 里嵌入了所有文档的正文内容，这些文本中仍有 "Hermes" 出现（约 149+ 处）。因为它们存在于文档内容的 JSON 数据中，替换可能破坏文档结构，目前谨慎保留。

### 4. 图片替换未完成
- `logo.png` 已替换为用户图片 ✅
- `apple-touch-icon.png`、`favicon-*.png` 等仍是旧图标（需要制作新 PNG 图标）
- `assets/images/` 下的功能截图仍然是 Hermes Agent 的

### 5. 搜索功能
DocSearch 配置仍在，但搜索索引可能还是 Hermes 的内容，需要重新配置。

### 6. 一键重跑命令
```bash
cd "C:\Users\50148\projects\openclaw中文社区网站"
node transform.js && node create-logo.js
# 然后 cp logo 图片：
copy "C:\Users\50148\Desktop\photo_2026-06-23_20-05-43_rounded.png" dist\img\logo.png
# 启动本地查看：
PORT=3002 node start.js
# 打开 http://localhost:3002
```

---

## 本地运行方式

```bash
cd "C:\Users\50148\projects\openclaw中文社区网站"
PORT=3002 node start.js
# 浏览器打开 http://localhost:3002
```

注意：3000 和 3001 端口可能有旧服务残留，建议用 3002。

---

## 关键联系人信息

| 项目 | 内容 |
|------|------|
| Logo 源文件 | `C:\Users\50148\Desktop\photo_2026-06-23_20-05-43_rounded.png` |
| 镜像服务器 | `res.agthub.tech` (Cloudflare) |
| 目标域名 | openclaw.cn（未解析） |

---

文档更新时间：2026-06-23
