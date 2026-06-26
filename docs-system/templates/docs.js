/**
 * OpenClaw 文档侧边栏渲染器
 * 从 SIDEBAR_DATA 渲染侧边栏，支持搜索过滤和激活状态
 */
(function() {
  'use strict';

  const root = document.getElementById('sidebarRoot');
  if (!root) return;

  function renderSidebar(data, currentPath) {
    let html = '';
    for (const item of data) {
      if (item.type === 'category') {
        html += renderCategory(item, currentPath);
      } else if (item.type === 'link') {
        html += renderSingleLink(item, currentPath);
      }
    }
    root.innerHTML = html;

    // 展开当前路径所在的分类
    const activeLink = root.querySelector('.sidebar-link.active');
    if (activeLink) {
      let parent = activeLink.closest('.sidebar-items');
      while (parent) {
        parent.classList.remove('collapsed');
        const header = parent.previousElementSibling;
        if (header && header.classList.contains('sidebar-category-header')) {
          const arrow = header.querySelector('.arrow');
          if (arrow) arrow.classList.add('open');
        }
        parent = parent.parentElement?.closest('.sidebar-items');
      }
      activeLink.scrollIntoView({ block: 'nearest' });
    }
  }

  function renderCategory(cat, currentPath) {
    const isExpanded = isCategoryActive(cat, currentPath);
    const arrowClass = isExpanded ? 'arrow open' : 'arrow';
    const itemsClass = isExpanded ? 'sidebar-items' : 'sidebar-items collapsed';

    let html = `<div class="sidebar-category">
      <div class="sidebar-category-header" onclick="toggleCategory(this)">
        ${cat.label}
        <span class="${arrowClass}">▶</span>
      </div>
      <ul class="${itemsClass}">`;

    for (const item of cat.items) {
      if (item.type === 'category') {
        html += `<li>${renderCategory(item, currentPath)}</li>`;
      } else {
        const isActive = item.href === currentPath;
        const activeClass = isActive ? 'sidebar-link active' : 'sidebar-link';
        html += `<li><a class="${activeClass}" href="${item.href}">${item.label}</a></li>`;
      }
    }

    html += `</ul></div>`;
    return html;
  }

  function renderSingleLink(link, currentPath) {
    const isActive = link.href === currentPath;
    const activeClass = isActive ? 'sidebar-single-link active' : 'sidebar-single-link';
    return `<a class="${activeClass}" href="${link.href}">${link.label}</a>`;
  }

  function isCategoryActive(cat, currentPath) {
    for (const item of cat.items) {
      if (item.type === 'category') {
        if (isCategoryActive(item, currentPath)) return true;
      } else if (item.href === currentPath) {
        return true;
      }
    }
    return false;
  }

  // 切换分类展开/折叠
  window.toggleCategory = function(header) {
    const items = header.nextElementSibling;
    if (!items || !items.classList.contains('sidebar-items')) return;
    items.classList.toggle('collapsed');
    const arrow = header.querySelector('.arrow');
    if (arrow) arrow.classList.toggle('open');
  };

  // 搜索过滤
  window.filterSidebar = function(query) {
    const allLinks = root.querySelectorAll('.sidebar-link, .sidebar-single-link');
    const allCats = root.querySelectorAll('.sidebar-category');

    if (!query.trim()) {
      allLinks.forEach(el => el.classList.remove('sidebar-hidden'));
      allCats.forEach(el => el.classList.remove('sidebar-hidden'));
      // 恢复默认折叠状态
      root.querySelectorAll('.sidebar-items.collapsed').forEach(el => {
        // 保持折叠，但不清除active展开
      });
      return;
    }

    const q = query.toLowerCase();
    allLinks.forEach(link => {
      const text = link.textContent.toLowerCase();
      link.classList.toggle('sidebar-hidden', !text.includes(q));
    });

    // 展开所有包含匹配结果的分类
    allCats.forEach(cat => {
      const hasVisible = cat.querySelector('.sidebar-link:not(.sidebar-hidden), .sidebar-single-link:not(.sidebar-hidden)');
      cat.classList.toggle('sidebar-hidden', !hasVisible);
      if (hasVisible) {
        const items = cat.querySelector('.sidebar-items');
        if (items) items.classList.remove('collapsed');
        const arrow = cat.querySelector('.arrow');
        if (arrow) arrow.classList.add('open');
      }
    });
  };

  // 初始化
  if (typeof SIDEBAR_DATA !== 'undefined' && typeof CURRENT_PATH !== 'undefined') {
    renderSidebar(SIDEBAR_DATA, CURRENT_PATH);
  }
})();
