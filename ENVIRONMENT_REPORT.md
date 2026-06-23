# OpenClaw 中文社区 — 环境总览报告

> 生成时间：2026-06-23 21:41 CST  
> 生成人：Hermes (Wahhra's AI Agent)  
> 接收人：Claude Code（接手续作）

---

## 一、项目目录结构

```
C:\Users\50148\projects\
├── openclaw中文社区网站\          ← 🔴 OpenClaw 主项目（当前活跃）
│   ├── dist\                      ← Vercel 部署源目录（已上线）
│   ├── site\                      ← 原始 Hermes 备份（勿动）
│   ├── scripts\                   ← 安装脚本
│   │   ├── install.sh             ← Linux/macOS 安装脚本
│   │   └── install.ps1            ← Windows 安装脚本
│   ├── transform.js               ← 品牌改造核心脚本
│   ├── create-logo.js             ← Logo 生成器
│   ├── start.js / serve.js        ← 本地 HTTP 服务器
│   ├── HANDOVER.md                ← 上一任转接文档
│   ├── .gitignore                 ← git 忽略规则
│   ├── index.html                 ← ⚠️ Hermes 误放，描述性页
│   ├── vercel.json                ← ⚠️ Hermes 误放
│   └── .vercelignore              ← ⚠️ Hermes 误放
│
└── openclaw-community-site\       ← 旧项目（已废弃）
    └── site\                      ← 同内容的另一版本
```

> **清理建议：** 根目录下的 `index.html`、`vercel.json`、`.vercelignore` 三个文件是 Hermes 误放的，建议 Claude Code 接手后删除。

---

## 二、Vercel 状态

### Vercel Account
- **Team:** `wahhra-s-projects` (orgId: `team_gtsmcbv7u3ls0t2R2rpKY8U6`)
- **User:** `ran666888`

### 项目列表

| 项目名 | 域名 | 最新部署 | 备注 |
|--------|------|---------|------|
| **openclaw** | `openclawal.cn` | 刚刚恢复部署 | 🔴 OpenClaw 中文社区站 |
| **agent-hub-cn** | `www.agthub.tech` | ~12h前 | agthub.tech 日报站，独立项目，**不要混用** |

### openclaw 项目详情

| 项目 | 内容 |
|------|------|
| Project ID | `prj_HaVxRISyAU1AR93H85dYWsCUY60l` |
| 部署目录 | `C:\Users\50148\projects\openclaw中文社区网站\dist\` |
| 最新 Production | `openclaw-nkerqnudu`（刚刚恢复，原站已还原） |
| 无环境变量 | 该项目没有任何 env vars |
| 构建时间 | ~9s |

### ⚠️ 历史部署杂讯（需要清理）
最近 40 分钟内（2026-06-23 21:00~21:40），Hermes 进行了若干次错误部署：

| 部署 | 内容 | 状态 | 说明 |
|------|------|------|------|
| `openclaw-7gz7z3rot` (2s) | 仅 `index.html` + `vercel.json` + `scripts/` | ✅ 已覆盖 | Hermes 的 placeholder |
| `openclaw-o4nd3p3dm` (27s) | 同上 + scripts 调整 | ✅ 已覆盖 | Hermes 调整 |
| `openclaw-600r8d2yp` (16s) | 同上 | ✅ 已覆盖 | Hermes 再调整 |
| `openclaw-nkerqnudu` (9s) | **✅ 当前Production** `dist/` 网站恢复 | ✅ 当前线上 | 正确版本 |

另有两个更旧的 `dist` 项目部署（40分钟前），来自当时代码，现项目已整合到 openclaw。

### 域名 DNS
- **`openclawal.cn`** → CNAME → `cname.vercel-dns.com` → Vercel
- **DNS 托管方:** 第三方域名注册商（非 Cloudflare）
- **Vercel 自动绑定**：域名已通过 Vercel 面板绑定到 openclaw 项目

---

## 三、GitHub 仓库

| 仓库 | 链接 | 可见性 | 默认分支 | 说明 |
|------|------|--------|---------|------|
| **openclawal.cn** | `github.com/ran666888/openclawal.cn` | 🔓 **Public** | `main` | OpenClaw 中文社区仓库 |
| agent-hub-cn | `github.com/ran666888/agent-hub-cn` | 🔒 Private | `master` | agthub.tech 独立项目 |

### openclawal.cn 仓库内容

- 语言占比：PowerShell 51% / Shell 44% / HTML 5%
- 包含文件：`install.sh`, `install.ps1`, `index.html`（Hermes 误放）, `vercel.json`（Hermes 误放）, `.vercelignore`（Hermes 误放）, `.gitignore`
- **注意：** `dist/` 目录未 push 到 GitHub。当前 Vercel 直接从本地 `dist/` 部署，不是从 GitHub auto-deploy。
- **GitHub Pages 未启用**

### Release
- **`v0.1.0-mirror`**（Latest）— 安装镜像
  - 附件：`install.sh` (13KB)、`install.ps1` (15KB)
  - 下载量：0
  - 标签：`v0.1.0-mirror`

---

## 四、Cloudflare 状态

### agthub.tech 使用 Cloudflare（与 OpenClaw 无关 🔴）
- Zone ID: `d2180810d9d15c68e24b75d46d1a2a72`
- 认证：Global API Key（存于 `~/.hermes/.env`）
- **这是 agent-hub-cn 项目的 CDN，OpenClaw 项目不经过 Cloudflare**

### openclawal.cn DNS
- 托管在第三方域名注册商
- 直接 CNAME 到 `cname.vercel-dns.com`
- **没有 Cloudflare 代理**

---

## 五、本地构建工具

### 核心脚本（均在 `openclaw中文社区网站\` 根目录）

| 脚本 | 作用 |
|------|------|
| `transform.js` | 读取 `site/` → 规则替换 → 输出 `dist/`（约60条文本规则+颜色映射+类名替换+JS安全替换） |
| `create-logo.js` | 生成 logo.svg / favicon.svg / og-image.svg |
| `start.js` / `serve.js` | 本地 HTTP 服务器（推荐 PORT=3002） |

### 一键重跑命令
```bash
cd "C:\Users\50148\projects\openclaw中文社区网站"
node transform.js && node create-logo.js
```

### 本地启动
```bash
PORT=3002 node start.js
# 浏览器访问 http://localhost:3002
```

### 部署命令
```bash
cd dist
npx vercel --prod
```
当前 Vercel 项目绑定到 `wahhra-s-projects/openclaw`，部署源为 `dist/` 目录。

---

## 六、重要的 ⚠️ 注意给 Claude Code

### 1. 两个项目完全隔离
- **OpenClaw 中文社区** = `openclawal.cn` / `ran666888/openclawal.cn` / Vercel 项目 `openclaw`
- **Agent Hub 中文站** = `www.agthub.tech` / `ran666888/agent-hub-cn` / Vercel 项目 `agent-hub-cn`
- **绝对不要混在一起操作！** 每一件事情只属于一个项目。

### 2. 网站内容来源
- 当前网站内容来自 `dist/` 目录（已被 transform.js 品牌改造为 OpenClaw）
- 原始备份在 `site/`（Hermes Agent 原站，只有 Hermes→OpenClaw 替换脚本依赖它，不要手动修改）
- 网站是纯静态 HTML，非 SSG/SSR

### 3. 安装镜像
- 安装脚本已上传到 GitHub Release `v0.1.0-mirror`
- Vercel 线上也能访问 `https://openclawal.cn/scripts/install.sh`
- 注意：脚本安装的是真正的 `npm install -g openclaw@latest`（OpenClaw），不是 Hermes

### 4. 需要删除的垃圾文件
根目录下这三个文件是 Hermes 误放的，应该删除：
- `index.html`（描述性 placeholder）
- `vercel.json`（与 `dist/` 中的 vercel 配置冲突）
- `.vercelignore`
- 同时从 git 仓库中移除它们（`git rm` 并提交）

### 5. Vercel 部署注意
- Vercel CLI 需在 `dist/` 目录下运行
- 部署前确认 `dist/` 是最新构建结果
- 当前无任何环境变量，如后续需要请通过 `vercel env add` 设置

---

*本报告由 Hermes Agent 自动生成，供 Claude Code 接手参考。部分数据可能因时序变化略有差异，建议以实际工具输出为准。*
