/**
 * 生成 OpenClaw 品牌图片资源
 * 运行: node create-logo.js
 */
const fs = require('fs');
const path = require('path');

const DIST = path.join(__dirname, 'dist', 'img');
const SRC = path.join(__dirname, 'site', 'img');

// 复制用户提供的 logo.png（优先于自动生成的 SVG）
const userLogo = path.join(__dirname, '..', 'Desktop', 'photo_2026-06-23_20-05-43_rounded.png');
if (fs.existsSync(userLogo)) {
  fs.copyFileSync(userLogo, path.join(DIST, 'logo.png'));
  console.log('  ✓ logo.png (用户提供)');
} else if (fs.existsSync(path.join(SRC, 'logo.png'))) {
  fs.copyFileSync(path.join(SRC, 'logo.png'), path.join(DIST, 'logo.png'));
  console.log('  ✓ logo.png (从site复制)');
}

// 主 logo SVG — 第⑥组配色: #80abb1 → #5496a2 渐变
const LOGO_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" fill="none">
  <defs>
    <linearGradient id="oc-grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#80abb1"/>
      <stop offset="100%" stop-color="#5496a2"/>
    </linearGradient>
  </defs>
  <text x="4" y="32" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="700" fill="url(#oc-grad)">OpenClaw</text>
  <text x="4" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#9bb7bb" letter-spacing="3">中文社区</text>
</svg>`;

// 简化版 logo（暗色底用）
const LOGO_WHITE_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" fill="none">
  <text x="4" y="32" font-family="system-ui, -apple-system, sans-serif" font-size="22" font-weight="700" fill="#fce5dd">OpenClaw</text>
  <text x="4" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="9" fill="#9bb7bb" letter-spacing="3">中文社区</text>
</svg>`;

// Favicon SVG
const FAVICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <defs>
    <linearGradient id="fg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#6366f1"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="6" fill="#2a2520"/>
  <text x="16" y="22" font-family="system-ui, sans-serif" font-size="18" font-weight="bold" fill="url(#fg)" text-anchor="middle">OC</text>
</svg>`;

// OG 图片 SVG — 第⑥组配色
const OG_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" fill="none">
  <rect width="1200" height="630" fill="#2a2520"/>
  <rect x="60" y="60" width="1080" height="510" rx="16" fill="#35302b" stroke="#5496a2" stroke-width="2"/>
  <text x="600" y="280" font-family="system-ui, sans-serif" font-size="64" font-weight="bold" fill="#fce5dd" text-anchor="middle">OpenClaw</text>
  <text x="600" y="350" font-family="system-ui, sans-serif" font-size="32" fill="#80abb1" text-anchor="middle" letter-spacing="8">中文社区</text>
  <text x="600" y="420" font-family="system-ui, sans-serif" font-size="22" fill="#9bb7bb" text-anchor="middle">开源 · 自托管 · 越用越聪明的 AI Agent</text>
  <text x="600" y="520" font-family="system-ui, sans-serif" font-size="14" fill="#bec8c8" text-anchor="middle">openclaw.cn</text>
</svg>`;

console.log('生成 OpenClaw 品牌图片...\n');

// 确保目录存在
const imgDirs = [DIST, path.join(DIST, 'daily'), path.join(DIST, 'banner'), path.join(DIST, 'community')];
for (const d of imgDirs) {
  if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
}

// 写入 SVG 文件
const svgFiles = [
  { name: 'logo.svg', content: LOGO_SVG },
  { name: 'logo-white.svg', content: LOGO_WHITE_SVG },
  { name: 'favicon.svg', content: FAVICON_SVG },
  { name: 'openclaw-og.svg', content: OG_SVG },
  { name: 'hermes-cn-og.svg', content: OG_SVG },  // 覆盖旧的
];

for (const { name, content } of svgFiles) {
  const fp = path.join(DIST, name);
  fs.writeFileSync(fp, content, 'utf-8');
  console.log(`  ✓ ${name} (${content.length} bytes)`);
}

// 更新 site.webmanifest
const manifestPath = path.join(__dirname, 'dist', 'site.webmanifest');
if (fs.existsSync(manifestPath)) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  manifest.name = 'OpenClaw 中文社区';
  manifest.short_name = 'OpenClaw';
  manifest.theme_color = '#2a2520';
  manifest.background_color = '#2a2520';
  manifest.icons = [
    { src: '/img/android-chrome-192x192.png', sizes: '192x192', type: 'image/png' },
    { src: '/img/android-chrome-512x512.png', sizes: '512x512', type: 'image/png' },
  ];
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), 'utf-8');
  console.log('  ✓ site.webmanifest (已更新)');
}

// 复制 logo.svg 作为 logo.png 的占位（实际使用 SVG）
const pngFiles = ['logo.png', 'favicon-16x16.png', 'favicon-32x32.png', 'apple-touch-icon.png'];
for (const name of pngFiles) {
  // 简单复制 SVG 作为占位
  const src = path.join(DIST, name);
  if (!fs.existsSync(src)) {
    // 创建一个 1x1 透明 PNG 作占位（实际应替换为真实 PNG）
    console.log(`  ⚠ ${name} — 需要替换为真实 PNG 图标`);
  }
}

console.log('\n品牌图片生成完成！');
