---
title: "Gitnexus Explorer"
sidebar_label: "Gitnexus Explorer"
description: "Index a codebase with GitNexus and serve an interactive knowledge graph via web UI + Cloudflare tunnel"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# GitNexus 浏览器

使用 GitNexus 索引代码库，并通过 Web UI + Cloudflare 隧道提供交互式知识图。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/research/gitnexus-explorer` 安装 |
|路径| `可选技能/研究/gitnexus-explorer` |
|版本 | `1.0.0` |
|作者 | OpenClaw代理+Teknium|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `gitnexus`、`代码智能`、`知识图谱`、`可视化` |
|相关技能| `native-mcp`，[`codebase-inspection`](/docs/user-guide/skills/bundled/github/github-codebase-inspection) |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# GitNexus 资源管理器

将任何代码库索引到知识图谱中，并提供交互式 Web UI 以供探索
符号、调用链、集群和执行流。通过 Cloudflare 建立隧道以进行远程访问。

## 何时使用

- 用户想要直观地探索代码库的架构
- 用户请求存储库的知识图/依赖图
- 用户想要与某人共享交互式代码库浏览器

## 先决条件

- **Node.js** (v18+) — GitNexus 和代理所需
- **git** — 仓库必须有一个 `.git` 目录
- **cloudflared** — 用于隧道（如果缺少，自动安装到 ~/.local/bin）

## 尺寸警告

Web UI 在浏览器中呈现所有节点。大约 5,000 个文件下的存储库运行良好。大号
存储库（30k+ 节点）将变得缓慢或使浏览器选项卡崩溃。 CLI/MCP 工具可以工作
任何规模——只有网络可视化有这个限制。

## 步骤

### 1. 克隆并构建 GitNexus（一次性安装）

````bash
GITNEXUS_DIR="${GITNEXUS_DIR:-$HOME/.local/share/gitnexus}"

如果[！ -d“$GITNEXUS_DIR/gitnexus-web/dist”];然后
  git克隆 https://github.com/abhigyanpatwari/GitNexus.git“$GITNEXUS_DIR”
  cd "$GITNEXUS_DIR/gitnexus-shared" && npm install && npm run build
  cd "$GITNEXUS_DIR/gitnexus-web" && npm install
菲
````

### 2. 修补 Web UI 以进行远程访问

对于 API 调用，Web UI 默认为“localhost:4747”。修补它以使用同源
所以它通过隧道/代理工作：

**文件：`$GITNEXUS_DIR/gitnexus-web/src/config/ui-constants.ts`**
改变：
``打字稿
导出常量 DEFAULT_BACKEND_URL = 'http://localhost:4747';
````
致：
``打字稿
导出常量 DEFAULT_BACKEND_URL = typeof window !== '未定义' && window.location.hostname !== 'localhost' ? window.location.origin : 'http://localhost:4747';
````

**文件：`$GITNEXUS_DIR/gitnexus-web/vite.config.ts`**
在 `server: { }` 块中添加 `allowedHosts: true` （仅在运行 dev 时需要）
模式而不是生产构建）：
``打字稿
服务器：{
    允许的主机：true，
    // ...现有配置
},
````

然后构建生产包：
````bash
cd "$GITNEXUS_DIR/gitnexus-web" && npx vite 构建
````

### 3. 为目标存储库建立索引

````bash
cd /路径/到/目标仓库
npx gitnexus 分析 --skip-agents-md
rm -rf .claude/ # 删除 Claude 代码特定的工件
````

添加“--embeddings”进行语义搜索（较慢 - 分钟而不是秒）。

该索引位于存储库内的“.gitnexus/”中（自动 gitignored）。

### 4. 创建代理脚本

将其写入文件（例如“$GITNEXUS_DIR/proxy.mjs”）。它服务于生产
Web UI 和代理 `/api/*` 到 GitNexus 后端 — 同源，没有 CORS 问题，
没有 sudo，没有 nginx。

```javascript
从 'node:http' 导入 http；
从“节点：fs”导入 fs；
从“节点：路径”导入路径；

const API_PORT = parseInt(process.env.API_PORT || '4747');
const DIST_DIR = process.argv[2] || './dist';
const PORT = parseInt(process.argv[3] || '8888');

常量 MIME = {
  '.html': '文本/html', '.js': '应用程序/javascript', '.css': '文本/css',
  '.json': 'application/json', '.png': '图像/png', '.svg': '图像/svg+xml',
  '.ico': '图像/x-图标', '.woff2': '字体/woff2', '.woff': '字体/woff',
  '.wasm': '应用程序/wasm',
};

函数 proxyToApi(req, res) {
  常量选项 = {
    主机名：'127.0.0.1'，端口：API_PORT，
    路径：req.url，方法：req.method，标题：req.headers，
  };
  const proxy = http.request(opts, (upstream) => {
    res.writeHead(upstream.statusCode,upstream.headers);
    上游.pipe(res, { end: true });
  });
  proxy.on('error', () => { res.writeHead(502); res.end('后端不可用'); });
  req.pipe(代理, { end: true });
}

函数serveStatic(req, res) {
  let filePath = path.join(DIST_DIR, req.url === '/' ? 'index.html' : req.url.split('?')[0]);
  if (!fs.existsSync(filePath)) filePath = path.join(DIST_DIR, 'index.html');
  const ext = path.extname(filePath);
  const mime = MIME[ext] || '应用程序/八位字节流'；
  尝试{
    const data = fs.readFileSync(filePath);
    res.writeHead(200, { 'Content-Type': mime, 'Cache-Control': 'public, max-age=3600' });
    res.end(数据);
  } catch { res.writeHead(404); res.end('未找到'); }
}

http.createServer((req, res) => {
  if (req.url.startsWith('/api')) proxyToApi(req, res);
  否则serveStatic(req, res);
}).listen(PORT, () => console.log(`http://localhost:${PORT}` 上的 GitNexus 代理));
````

### 5.启动服务

````bash
# 终端 1：GitNexus 后端 API
npx gitnexus 服务 &

# 终端 2：代理（一个端口上的 Web UI + API）
节点“$GITNEXUS_DIR/proxy.mjs”“$GITNEXUS_DIR/gitnexus-web/dist”8888&
````

验证：“curl -s http://localhost:8888/api/repos”应该返回索引的存储库。

### 6. Cloudflare 隧道（可选 — 用于远程访问）

````bash
# 如果需要，安装 cloudflared（无需 sudo）
如果！命令 -v cloudflared &>/dev/null;然后
  mkdir -p ~/.local/bin
  curl -sL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o ~/.local/bin/cloudflared
  chmod +x ~/.local/bin/cloudflared
  导出 PATH="$HOME/.local/bin:$PATH"
菲

# 启动隧道（--config /dev/null 避免与现有命名隧道发生冲突）
cloudflared 隧道 --config /dev/null --url http://localhost:8888 --no-autoupdate --protocol http2
````

隧道 URL（例如，`https://random-words.trycloudflare.com`）被打印到 stderr。
分享它——任何知道链接的人都可以探索该图。

### 7. 清理

````bash
# 停止服务
pkill -f“gitnexus 服务”
pkill -f“代理.mjs”
pkill -f cloudflared

# 从目标仓库中删除索引
cd /路径/到/目标仓库
npx gitnexus 干净
rm -rf .克劳德/
````

## 陷阱

- **`--config /dev/null` 对于 cloudflared** 是必需的，如果用户有现有的
  命名隧道配置位于“~/.cloudflared/config.yml”。没有它，包罗万象
  配置中的入口规则对于所有快速隧道请求返回 404。

- **生产构建对于隧道是强制性的。** Vite 开发服务器块
  默认情况下非本地主机主机（“allowedHosts”）。生产构建+节点
  proxy 完全避免了这种情况。

- **Web UI 不会创建 `.claude/` 或 `CLAUDE.md`。** 这些是由
  `npx gitnexus 分析`。使用 `--skip-agents-md` 抑制 markdown 文件，
  然后 `rm -rf .claude/` 剩下的。这些是克劳德代码集成
  hermes-agent 用户不需要。

- **浏览器内存限制。** Web UI 将整个图表加载到浏览器内存中。
  具有 5k+ 文件的存储库可能会很缓慢。超过 30k 个文件可能会使选项卡崩溃。

- **嵌入是可选的。** `--embeddings` 启用语义搜索，但需要
  大型回购协议的分钟数。跳过它以进行快速探索；如果需要的话可以添加
  通过人工智能聊天面板进行自然语言查询。

- **多个存储库。** `gitnexusserve` 提供所有索引存储库。索引几个
  存储库、启动服务一次，Web UI 允许您在它们之间切换。