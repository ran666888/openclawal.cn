// 生成 sitemap.xml
const fs = require('fs');
const path = require('path');
const dist = path.join(__dirname, 'dist');

const urls = [];

function walk(dir) {
  for (const f of fs.readdirSync(dir)) {
    const fp = path.join(dir, f);
    if (f.startsWith('.') || f === 'node_modules') continue;
    if (fs.statSync(fp).isDirectory()) walk(fp);
    else if (f === 'index.html') {
      const rel = path.relative(dist, path.dirname(fp)).replace(/\\/g, '/');
      urls.push('https://openclawal.cn/' + (rel || ''));
    }
  }
}

walk(dist);

let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
for (const url of urls.sort()) {
  xml += '  <url><loc>' + url + '</loc></url>\n';
}
xml += '</urlset>\n';

fs.writeFileSync(path.join(dist, 'sitemap.xml'), xml, 'utf-8');
console.log('✅ sitemap.xml 已生成: ' + urls.length + ' 个 URL');
