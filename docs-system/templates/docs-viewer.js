/**
 * OpenClaw 文档查看器 v2
 * 使用 hash 路由，完全绕过 Docusaurus
 */
(function() {
  var currentPath = '/docs/';
  var sidebarData = null;
  var articles = null;
  var isLoading = false;

  // ======== 注入文档容器 ========
  function injectViewer() {
    if (document.getElementById('oc-docs-viewer')) return;

    var viewer = document.createElement('div');
    viewer.id = 'oc-docs-viewer';
    viewer.style.display = 'none';
    viewer.innerHTML =
      '<div style="display:flex;max-width:1400px;margin:0 auto;min-height:calc(100vh - 60px)">' +
        '<aside style="width:300px;flex-shrink:0;border-right:1px solid rgba(252,229,221,.28);padding:16px 0;overflow-y:auto;position:sticky;top:60px;height:calc(100vh - 60px);background:#2a2520">' +
          '<div style="padding:0 12px">' +
            '<input type="text" placeholder="搜索文档..." id="ocs-search" ' +
              'style="width:100%;margin-bottom:12px;background:#35302b;border:1px solid rgba(252,229,221,.28);border-radius:8px;color:#fce5dd;font-size:13px;padding:8px 12px;outline:none">' +
            '<div id="ocs-sidebar"></div>' +
          '</div>' +
        '</aside>' +
        '<main style="flex:1;min-width:0;padding:40px 56px">' +
          '<div id="ocs-content" style="max-width:820px;margin:0 auto"></div>' +
        '</main>' +
      '</div>';

    var nav = document.querySelector('.navbar') || document.querySelector('nav');
    (nav ? nav.parentNode : document.body).insertBefore(viewer, nav ? nav.nextSibling : null);
  }

  // ======== 加载数据 ========
  function loadData(cb) {
    if (sidebarData && articles) { cb(); return; }
    var n = 0;
    function done() { n++; if (n >= 2 && sidebarData && articles) cb(); }

    var x1 = new XMLHttpRequest();
    x1.open('GET', '/docs-config.json?t=' + Date.now(), true);
    x1.onload = function() { try { sidebarData = JSON.parse(x1.responseText); } catch(e) {} done(); };
    x1.onerror = function() { done(); };
    x1.send();

    var x2 = new XMLHttpRequest();
    x2.open('GET', '/docs-articles.json?t=' + Date.now(), true);
    x2.onload = function() { try { articles = JSON.parse(x2.responseText); } catch(e) {} done(); };
    x2.onerror = function() { done(); };
    x2.send();
  }

  // ======== 显示/隐藏 ========
  function showDocs(path) {
    currentPath = path || '/docs/';
    injectViewer();

    var v = document.getElementById('oc-docs-viewer');
    if (!v) return;
    v.style.display = '';

    // 隐藏首页内容
    var main = document.querySelector('.oc-page') || document.querySelector('.main-wrapper') || document.querySelector('#__docusaurus_skipToContent_fallback');
    if (main) main.style.display = 'none';
    // 高亮"文档"按钮
    document.querySelectorAll('.navbar__link').forEach(function(el) {
      el.classList.remove('navbar__link--active');
      if (el.textContent.trim() === '文档') el.classList.add('navbar__link--active');
    });
    window.scrollTo(0, 0);

    loadData(function() {
      renderSidebar();
      loadContent(currentPath);
    });
  }

  function hideDocs() {
    var viewer = document.getElementById('oc-docs-viewer');
    if (viewer) viewer.style.display = 'none';
    var skillsFrame = document.getElementById('oc-skills-frame');
    if (skillsFrame) skillsFrame.style.display = 'none';
    var main = document.querySelector('.oc-page') || document.querySelector('.main-wrapper') || document.querySelector('#__docusaurus_skipToContent_fallback');
    if (main) main.style.display = '';
    var b = document.querySelector('.theme-announcement-bar');
    if (b) b.style.display = '';
  }

  // ======== 侧边栏 ========
  function renderSidebar() {
    var root = document.getElementById('ocs-sidebar');
    if (!root || !sidebarData) return;
    root.innerHTML = buildTree(sidebarData);

    // 绑定点击
    root.querySelectorAll('[data-href]').forEach(function(el) {
      el.onclick = function(e) {
        e.preventDefault();
        navigateTo(this.getAttribute('data-href'));
      };
    });

    // 搜索
    var s = document.getElementById('ocs-search');
    if (s) s.oninput = function() { searchDoc(this.value); };
  }

  function buildTree(items) {
    var h = '';
    for (var i = 0; i < items.length; i++) {
      var it = items[i];
      if (it.type === 'category') {
        var active = hasActive(it.items);
        h += '<div style="margin-bottom:4px">' +
          '<div onclick="ocToggle(this)" ' +
            'style="display:flex;align-items:center;justify-content:space-between;padding:8px 12px;cursor:pointer;border-radius:6px;color:#fce5dd;font-weight:700;font-size:14px;user-select:none">' +
            esc(it.label) +
            '<span style="font-size:10px;transition:.2s;' + (active ? 'transform:rotate(90deg)' : '') + '">▶</span>' +
          '</div>' +
          '<ul style="list-style:none;margin:0;padding:0;' + (active ? '' : 'display:none') + '">' +
          buildTree(it.items) + '</ul></div>';
      } else {
        var a = it.href === currentPath;
        h += '<li><a href="#" data-href="' + it.href + '" ' +
          'style="display:block;padding:6px 12px 6px 24px;color:' + (a ? '#fb923c' : 'rgba(252,229,221,.84)') + ';text-decoration:none;font-size:13.5px;border-left:2px solid ' + (a ? '#fb923c' : 'transparent') + ';background:' + (a ? 'rgba(251,146,60,.08)' : 'transparent') + '">' +
          esc(it.label) + '</a></li>';
      }
    }
    return h;
  }

  function hasActive(items) {
    for (var i = 0; i < items.length; i++) {
      if (items[i].type === 'link' && items[i].href === currentPath) return true;
      if (items[i].type === 'category' && hasActive(items[i].items)) return true;
    }
    return false;
  }

  function esc(t) {
    var d = document.createElement('div');
    d.textContent = t;
    return d.innerHTML;
  }

  function searchDoc(q) {
    var root = document.getElementById('ocs-sidebar');
    if (!root) return;
    root.querySelectorAll('[data-href]').forEach(function(el) {
      el.style.display = (!q.trim() || el.textContent.toLowerCase().includes(q.toLowerCase())) ? '' : 'none';
    });
  }

  // ======== 导航 ========
  function normalizePath(p) {
    if (!p.endsWith('/')) p += '/';
    return p;
  }

  function navigateTo(path) {
    path = normalizePath(path);
    if (isLoading || path === currentPath) return;
    currentPath = path;
    isLoading = true;
    renderSidebar();
    loadContent(path);
  }

  function loadContent(path) {
    var el = document.getElementById('ocs-content');
    if (!el) return;

    if (articles && articles[path]) {
      var a = articles[path];
      // 延迟一点等侧边栏渲染
      setTimeout(function() {
        el.innerHTML =
          '<article class="markdown">' + a.content + '</article>' +
          '<div style="display:flex;justify-content:space-between;margin-top:3rem;padding-top:1rem;border-top:1px solid rgba(252,229,221,.28);font-size:14px">' +
            '<a href="#" onclick="ocBack()" style="color:rgba(252,229,221,.84);text-decoration:none">← 返回首页</a>' +
            '<span style="color:rgba(252,229,221,.3)">发现错误？<a href="' + a.edit_url + '" style="color:#fb923c">在 GitHub 上编辑</a></span>' +
          '</div>';
        isLoading = false;
      }, 50);
    } else {
      el.innerHTML = '<div style="padding:40px;text-align:center;color:rgba(252,229,221,.6)"><p>加载中...</p></div>';
      setTimeout(function() {
        if (articles && articles[path]) {
          loadContent(path);
        } else {
          el.innerHTML = '<div style="padding:40px;text-align:center;color:rgba(252,229,221,.6)"><h2>页面未找到</h2><p>请从侧边栏选择其他页面</p></div>';
          isLoading = false;
        }
      }, 800);
    }
  }

  // ======== Hash 路由 ========
  function onHashChange() {
    var hash = window.location.hash;
    if (hash === '#docs' || hash === '#docs/') {
      showDocs('/docs/');
    } else if (hash.startsWith('#docs/')) {
      var path = hash.substring(1);
      showDocs(path);
    } else if (hash === '#skills' || hash === '#skills/') {
      var skillsFrame = document.getElementById('oc-skills-frame');
      if (!skillsFrame) {
        skillsFrame = document.createElement('div');
        skillsFrame.id = 'oc-skills-frame';
        skillsFrame.style.cssText = 'display:none;position:relative;z-index:10;';
        var nav = document.querySelector('.navbar') || document.querySelector('nav');
        (nav ? nav.parentNode : document.body).insertBefore(skillsFrame, nav ? nav.nextSibling : null);
      }
      skillsFrame.innerHTML = '<div style="padding:2rem;text-align:center;color:rgba(252,229,221,.6)">加载中...</div>';
      skillsFrame.style.display = '';
      var main = document.querySelector('.oc-page') || document.querySelector('.main-wrapper');
      if (main) main.style.display = 'none';
      document.querySelectorAll('.navbar__link').forEach(function(el) {
        el.classList.remove('navbar__link--active');
        if (el.textContent.trim() === '技能') el.classList.add('navbar__link--active');
      });
      window.scrollTo(0, 0);
      fetch('/skills/index.html?' + Date.now()).then(function(r) { return r.text(); }).then(function(html) {
        var div = document.createElement('div');
        div.innerHTML = html;
        var content = div.querySelector('#oc-skills-viewer') || div.querySelector('.oc-page') || div.querySelector('main');
        if (content) skillsFrame.innerHTML = content.outerHTML;
        var scripts = skillsFrame.querySelectorAll('script');
        scripts.forEach(function(oldScript) {
          var newScript = document.createElement('script');
          newScript.textContent = oldScript.textContent;
          oldScript.parentNode.replaceChild(newScript, oldScript);
        });
      }).catch(function() {
        skillsFrame.innerHTML = '<div style="padding:2rem;text-align:center;color:rgba(252,229,221,.6)">加载失败</div>';
      });
    } else {
      hideDocs();
    }
  }

  // ======== 全局接口 ========
  window.ocBack = function() {
    window.location.hash = '';
    hideDocs();
  };
  window.ocToggle = function(header) {
    var items = header.nextElementSibling;
    if (!items) return;
    var arrow = header.querySelector('span:last-child');
    if (items.style.display === 'none') {
      items.style.display = '';
      if (arrow) arrow.style.transform = 'rotate(90deg)';
    } else {
      items.style.display = 'none';
      if (arrow) arrow.style.transform = '';
    }
  };

  // ======== 初始化 ========
  function init() {
    injectViewer();
    window.addEventListener('hashchange', onHashChange);
    // 如果页面加载时已经有 #docs 或 #skills hash
    if (window.location.hash.startsWith('#docs') || window.location.hash.startsWith('#skills')) {
      setTimeout(onHashChange, 100);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
