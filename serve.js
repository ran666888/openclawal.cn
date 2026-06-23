const http = require('http');
const fs = require('fs');
const path = require('path');

const SITE_DIR = path.join(__dirname, 'site');
const PORT = 3000;
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.gif': 'image/gif', '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon', '.webp': 'image/webp',
  '.woff': 'font/woff', '.woff2': 'font/woff2',
  '.ttf': 'font/ttf', '.eot': 'application/vnd.ms-fontobject',
  '.xml': 'application/xml',
  '.webmanifest': 'application/manifest+json',
  '.sh': 'text/plain', '.ps1': 'text/plain',
};

function resolvePath(urlPath) {
  if (urlPath === '/') return path.join(SITE_DIR, 'index.html');
  const filePath = path.join(SITE_DIR, urlPath);
  try {
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) return path.join(filePath, 'index.html');
    return filePath;
  } catch (e) {
    const indexPath = path.join(SITE_DIR, urlPath, 'index.html');
    if (fs.existsSync(indexPath)) return indexPath;
    const htmlPath = filePath + '.html';
    if (fs.existsSync(htmlPath)) return htmlPath;
    return null;
  }
}

const server = http.createServer((req, res) => {
  const urlPath = req.url.split('?')[0];
  const resolved = resolvePath(urlPath);
  if (!resolved) {
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`<h1>404 - ${urlPath} 未找到</h1>`);
    return;
  }
  const ext = path.extname(resolved).toLowerCase();
  fs.readFile(resolved, (err, data) => {
    if (err) { res.writeHead(500); res.end('Error'); return; }
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

server.listen(PORT, () => {
  console.log('═══════════════════════════════');
  console.log('  OpenClaw 中文社区 - 本地镜像');
  console.log('═══════════════════════════════');
  console.log(`  打开: http://localhost:${PORT}`);
  console.log('  按 Ctrl+C 停止');
});
