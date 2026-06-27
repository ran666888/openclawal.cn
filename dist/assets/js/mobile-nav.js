(function(){
  'use strict';

  // Only run on mobile
  if (window.innerWidth > 996) return;

  var btn = document.querySelector('.navbar__toggle');
  if (!btn) return;

  // === Inject CSS ===
  var style = document.createElement('style');
  style.textContent = '.navbar-sidebar{display:none}@media(max-width:996px){' +
    '.navbar-sidebar{position:fixed;top:var(--ifm-navbar-height,4rem);bottom:0;left:-100%;width:280px;max-width:80vw;background:var(--ifm-navbar-background-color,#1b1b1d);border-right:1px solid var(--ifm-toc-border-color,#333);transition:left .25s ease;z-index:calc(var(--ifm-z-index-fixed,200)-1);overflow-y:auto;box-shadow:2px 0 12px rgba(0,0,0,.2);display:block;height:calc(100vh - 60px)!important;opacity:1!important;visibility:visible!important;transform:none!important}' +
    '.navbar-sidebar--show{left:0}' +
    '.navbar-sidebar__brand{padding:.75rem 1rem;border-bottom:1px solid var(--ifm-toc-border-color,#333);display:flex;align-items:center}' +
    '.navbar-sidebar__menu{padding:.25rem 0}' +
    '.navbar-sidebar__menu .navbar__link{display:block;padding:.7rem 1rem;font-size:.9375rem;color:var(--ifm-navbar-link-color,#dadde1);text-decoration:none;border-left:3px solid transparent;transition:all .12s ease}' +
    '.navbar-sidebar__menu .navbar__link:hover,.navbar-sidebar__menu .navbar__link:focus{background:var(--ifm-menu-color-background-active,rgba(0,188,212,.08));color:var(--ifm-link-color,#00bcd4);border-left-color:var(--ifm-link-color,#00bcd4)}' +
    '.navbar-sidebar__backdrop--show{opacity:1!important;visibility:visible!important}' +
    'body.navbar-sidebar-open{overflow:hidden}' +
  '}';
  document.head.appendChild(style);

  // === Inject sidebar HTML ===
  var nav = document.querySelector('.navbar');
  if (!nav) return;

  var sidebar = document.createElement('div');
  sidebar.className = 'navbar-sidebar';
  sidebar.innerHTML =
    '<div class="navbar-sidebar__brand">' +
      '<a class="navbar__brand" href="/">' +
        '<div class="navbar__logo">' +
          '<img src="/img/logo.png?v=20260608-logo" alt="OpenClaw 中文社区" class="themedComponent_hcyy themedComponent--light_lVmn">' +
          '<img src="/img/logo.png?v=20260608-logo" alt="OpenClaw 中文社区" class="themedComponent_hcyy themedComponent--dark_qXEE">' +
        '</div>' +
        '<b class="navbar__title text--truncate">OpenClaw 中文社区</b>' +
      '</a>' +
    '</div>' +
    '<div class="navbar-sidebar__menu">' +
      '<a class="navbar__link" href="/#docs">文档</a>' +
      '<a class="navbar__link" href="/community">社区</a>' +
      '<a class="navbar__link" href="/forum">论坛</a>' +
      '<a class="navbar__link" href="/#skills">技能</a>' +
      '<a class="navbar__link" href="/daily">日报</a>' +
      '<a class="navbar__link" href="/practice-guides">生态</a>' +
      '<a class="navbar__link" href="/releases">版本</a>' +
    '</div>';

  nav.appendChild(sidebar);
  // Close sidebar when any nav link is clicked
  sidebar.querySelectorAll('.navbar-sidebar__menu .navbar__link').forEach(function(el) {
    el.addEventListener('click', function() {
      btn.setAttribute('aria-expanded', 'false');
      sidebar.classList.remove('navbar-sidebar--show');
      if (backdrop) backdrop.classList.remove('navbar-sidebar__backdrop--show');
      document.body.classList.remove('navbar-sidebar-open');
    });
  });
  var backdrop = nav.querySelector('.navbar-sidebar__backdrop');

  // === Toggle handler ===
  function toggle() {
    var expanded = btn.getAttribute('aria-expanded') === 'true';
    btn.setAttribute('aria-expanded', !expanded);
    sidebar.classList.toggle('navbar-sidebar--show', !expanded);
    if (backdrop) backdrop.classList.toggle('navbar-sidebar__backdrop--show', !expanded);
    document.body.classList.toggle('navbar-sidebar-open', !expanded);
  }

  btn.addEventListener('click', toggle);
  if (backdrop) backdrop.addEventListener('click', toggle);

  // Re-check on resize (going from mobile to desktop and back)
  var resizeTimer;
  window.addEventListener('resize', function() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function() {
      if (window.innerWidth > 996) {
        sidebar.classList.remove('navbar-sidebar--show');
        if (backdrop) backdrop.classList.remove('navbar-sidebar__backdrop--show');
        document.body.classList.remove('navbar-sidebar-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    }, 200);
  });
})();
