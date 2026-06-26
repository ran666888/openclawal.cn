// 生成 sitemap.xml — 带优先级 + 每日报告
const fs = require('fs');
const path = require('path');
const dist = path.join(__dirname, 'dist');

const urls = [];

const priorityMap = {
  '/': '1.0',
  '/openclaw-installation': '0.9',
  '/docs-index': '0.9',
  '/skills': '0.9',
  '/practice-guides': '0.9',
  '/community': '0.9',
  '/daily': '0.8',
  '/openclaw-messaging': '0.8',
  '/openclaw-mcp': '0.8',
  '/about': '0.7',
  '/forum': '0.7',
  '/releases': '0.7',
  '/privacy': '0.5',
  '/terms': '0.5',
  '/en': '0.6',
  '/zh-Hant': '0.6',
};

function getPriority(rel) {
  return priorityMap[rel] || '0.5';
}

function walk(dir) {
  for (const f of fs.readdirSync(dir)) {
    const fp = path.join(dir, f);
    if (f.startsWith('.') || f === 'node_modules' || f.includes('_old_bak') || f.includes('backup')) continue;
    if (fs.statSync(fp).isDirectory()) walk(fp);
    else if (f === 'index.html') {
      const rel = path.relative(dist, path.dirname(fp)).replace(/\\/g, '/');
      urls.push({
        loc: 'https://openclawal.cn/' + (rel || ''),
        priority: getPriority('/' + rel)
      });
    }
  }
}

walk(dist);

if (fs.existsSync(path.join(dist, 'docs-index.html'))) {
  urls.push({
    loc: 'https://openclawal.cn/docs-index.html',
    priority: '0.9'
  });
}

const reportsDir = path.join(dist, 'reports', 'daily');
if (fs.existsSync(reportsDir)) {
  for (const f of fs.readdirSync(reportsDir)) {
    if (f.endsWith('.html')) {
      const name = f.replace('.html', '');
      urls.push({
        loc: 'https://openclawal.cn/reports/daily/' + name,
        priority: '0.6'
      });
    }
  }
}

urls.sort((a, b) => {
  if (a.loc === 'https://openclawal.cn/') return -1;
  if (b.loc === 'https://openclawal.cn/') return 1;
  return a.loc.localeCompare(b.loc);
});

let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const url of urls) {
  xml += '  <url><loc>' + url.loc + '</loc><priority>' + url.priority + '</priority></url>\n';
}
xml += '</urlset>\n';

fs.writeFileSync(path.join(dist, 'sitemap.xml'), xml, 'utf-8');
console.log('sitemap.xml generated: ' + urls.length + ' URLs');
