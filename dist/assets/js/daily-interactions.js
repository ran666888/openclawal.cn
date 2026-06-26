/**
 * daily-interactions.js — 日报页交互功能（v2）
 * 功能：前一期/后一期导航、公众号弹窗、下载图片
 * 修正：弹窗布局全新设计、下载直接截取当前 iframe 内容
 */
(function() {
  'use strict';

  var AVAILABLE_DATES = [
    "2026-06-22","2026-06-23",
    "2026-06-24","2026-06-25","2026-06-26"
  ];

  /* ──────── 工具函数 ──────── */
  function getCurrentDateStr() {
    var iframe = document.querySelector('.oc-daily-frame');
    if (!iframe) return 'today';
    var m = iframe.src.match(/daily\/(\d{4}-\d{2}-\d{2})\.html/);
    return m ? m[1] : 'today';
  }

  /* ──────── 1. 前一期/后一期导航 ──────── */
  function initNavigation() {
    var prevBtn = document.querySelector('.oc-daily-step button:first-child');
    var nextBtn = document.querySelector('.oc-daily-step button:last-child');
    var iframe = document.querySelector('.oc-daily-frame');
    var headDate = document.querySelector('.oc-daily-date-pill');
    var headTitle = document.querySelector('.oc-daily-main__head h2');

    if (!prevBtn || !nextBtn || !iframe) return;

    function getCurrentDate() {
      var m = iframe.src.match(/daily\/(\d{4}-\d{2}-\d{2})\.html/);
      return m ? m[1] : null;
    }

    function updateDateUI(dateStr) {
      var d = new Date(dateStr + 'T00:00:00+08:00');
      var weekdays = ['周日','周一','周二','周三','周四','周五','周六'];
      var wd = weekdays[d.getDay()];
      var month = parseInt(dateStr.slice(5,7));
      var day = parseInt(dateStr.slice(8,10));

      var pill = document.querySelector('.oc-daily-date-pill');
      if (pill) pill.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 2v4"></path><path d="M16 2v4"></path><rect width="18" height="18" x="3" y="4" rx="2"></rect><path d="M3 10h18"></path><path d="M8 14h.01"></path><path d="M12 14h.01"></path><path d="M16 14h.01"></path><path d="M8 18h.01"></path><path d="M12 18h.01"></path><path d="M16 18h.01"></path></svg>' + dateStr + ' · ' + wd;

      var title = document.querySelector('.oc-daily-main__head h2');
      if (title) title.textContent = 'OpenClaw 中文社区日报 ' + month + '月' + day + '日';

      // Update download button filename
      var dl = document.querySelector('.oc-daily-cta__secondary');
      if (dl) {
        dl.dataset.date = dateStr;
      }
    }

    function loadHighlights(dateStr) {
      var xhr = new XMLHttpRequest();
      xhr.open('GET', '/reports/daily/' + dateStr + '.html', true);
      xhr.onload = function() {
        if (xhr.status !== 200) return;
        var html = xhr.responseText;
        var communityCount = (html.match(/<li class="community-item">/g) || []).length;
        var headlinesCount = (html.match(/<li class="headline">/g) || []).length;

        var hh = document.querySelector('.oc-daily-highlights__head');
        if (hh && communityCount > 0) {
          var total = headlinesCount + communityCount;
          hh.innerHTML = '本期社区摘录 · 共 ' + total + ' 条';
        }

        var hl = document.querySelector('.oc-daily-highlights__list');
        if (!hl) return;

        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var items = doc.querySelectorAll('.community-item');
        var headlines = doc.querySelectorAll('.headline');

        var h = '';
        if (headlines.length > 0) {
          headlines.forEach(function(item, i) {
            var num = (i + 1).toString().padStart(2, '0');
            var titleEl = item.querySelector('.headline-title');
            var tagEl = item.querySelector('.tag-headline');
            var title = titleEl ? titleEl.textContent : '';
            var tag = tagEl ? tagEl.textContent : '';
            if (title) {
              h += '<li class="oc-daily-highlights__item"><span class="oc-daily-highlights__num">' + num + '</span><span class="oc-daily-highlights__body"><span class="oc-daily-highlights__title">' + title + '</span><span class="oc-daily-highlights__tag">' + tag + '</span></span></li>';
            }
          });
        }
        if (items.length > 0) {
          items.forEach(function(item, i) {
            var idx = headlines.length + i;
            var num = (idx + 1).toString().padStart(2, '0');
            var titleEl = item.querySelector('.community-title');
            var tagEl = item.querySelector('.tag-community');
            var title = titleEl ? titleEl.textContent : '';
            var tag = tagEl ? tagEl.textContent : '';
            if (title) {
              h += '<li class="oc-daily-highlights__item"><span class="oc-daily-highlights__num">' + num + '</span><span class="oc-daily-highlights__body"><span class="oc-daily-highlights__title">' + title + '</span><span class="oc-daily-highlights__tag">' + tag + '</span></span></li>';
            }
          });
        }
        hl.innerHTML = h || '<li class="oc-daily-highlights__item" style="opacity:0.6">暂无社区摘录数据</li>';
      };
      xhr.send();
    }

    function updateLinks(dateStr) {
      // placeholder for any link updates needed
    }

    function navigate(dir) {
      var current = getCurrentDate();
      if (!current) return;
      var idx = AVAILABLE_DATES.indexOf(current);
      if (idx === -1) return;
      var newIdx = idx + dir;
      if (newIdx < 0 || newIdx >= AVAILABLE_DATES.length) return;
      var newDate = AVAILABLE_DATES[newIdx];

      iframe.src = '/reports/daily/' + newDate + '.html';
      // 高度调整由统一的 load 监听器自动完成
      iframe.onload = function() {
        loadHighlights(newDate);
        updateLinks(newDate);
        updateDateUI(newDate);
      };

      updateDateUI(newDate);
      prevBtn.disabled = (newIdx === 0);
      nextBtn.disabled = (newIdx === AVAILABLE_DATES.length - 1);
    }

    prevBtn.addEventListener('click', function() { navigate(-1); });
    nextBtn.addEventListener('click', function() { navigate(1); });

    // 高度自适应：临时展开 overflow 拿到真实内容高度
    function adjustHeight() {
      try {
        var doc = iframe.contentDocument || iframe.contentWindow.document;
        var b = doc.body;
        if (!b) return;
        var wasOverflow = b.style.overflow;
        b.style.overflow = 'visible';
        var realH = b.scrollHeight;
        b.style.overflow = wasOverflow;
        iframe.style.height = realH + 'px';
      } catch(e) {}
    }

    // 每次 iframe 加载后自动调整高度（初始 + 导航 + 未来新日期）
    function onIframeLoad() {
      setTimeout(adjustHeight, 50);
    }
    iframe.addEventListener('load', onIframeLoad);

    // 加时间戳防缓存：确保 iframe 总是加载最新的 report HTML
    var ts = Date.now();
    iframe.src = iframe.src.split('?')[0] + '?t=' + ts;

    // 如果 iframe 已经加载完，马上算一次（也等 load 事件走完）
    if (iframe.contentDocument && iframe.contentDocument.readyState === 'complete') {
      setTimeout(adjustHeight, 150);
    }
  }

  /* ──────── 2. 公众号弹窗（重新设计布局） ──────── */
  function initModal() {
    // ===== 创建弹窗结构 =====
    var overlay = document.createElement('div');
    overlay.id = 'oc-daily-modal';

    // 注入完整 CSS
    var style = document.createElement('style');
    style.textContent =
      '#oc-daily-modal{' +
        'display:none;position:fixed;top:0;left:0;width:100%;height:100%;' +
        'z-index:99999;background:rgba(0,0,0,0.75);' +
        'justify-content:center;align-items:center;' +
        'backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);' +
        'animation:ocModalFadeIn 0.25s ease-out;' +
      '}' +
      '#oc-daily-modal.show{display:flex;}' +
      '@keyframes ocModalFadeIn{' +
        'from{opacity:0}' +
        'to{opacity:1}' +
      '}' +
      '#oc-daily-modal .oc-modal-card{' +
        'background:linear-gradient(145deg,#0d312d 0%,#082121 100%);' +
        'border:1px solid rgba(255,230,203,0.12);' +
        'border-radius:24px;padding:0;max-width:480px;width:92%;' +
        'box-shadow:0 32px 96px rgba(0,0,0,0.6);' +
        'position:relative;overflow:hidden;' +
        'animation:ocModalSlideUp 0.3s ease-out;' +
      '}' +
      '@keyframes ocModalSlideUp{' +
        'from{transform:translateY(30px);opacity:0}' +
        'to{transform:translateY(0);opacity:1}' +
      '}' +
      '#oc-daily-modal .oc-modal-close{' +
        'position:absolute;top:16px;right:18px;' +
        'width:32px;height:32px;border-radius:50%;' +
        'background:rgba(255,255,255,0.06);' +
        'border:1px solid rgba(255,230,203,0.10);' +
        'color:rgba(255,230,203,0.5);font-size:20px;' +
        'cursor:pointer;z-index:10;' +
        'display:flex;align-items:center;justify-content:center;' +
        'transition:all 0.2s;line-height:1;' +
      '}' +
      '#oc-daily-modal .oc-modal-close:hover{' +
        'background:rgba(255,230,203,0.12);' +
        'color:#ffe6cb;' +
      '}' +
      '#oc-daily-modal .oc-modal-header{' +
        'padding:40px 32px 0 32px;' +
        'text-align:center;' +
      '}' +
      '#oc-daily-modal .oc-modal-badge{' +
        'display:inline-block;' +
        'background:linear-gradient(135deg,rgba(251,146,60,0.20),rgba(251,146,60,0.08));' +
        'border:1px solid rgba(251,146,60,0.20);' +
        'border-radius:20px;padding:4px 14px;' +
        'font-size:13px;color:#fb923c;letter-spacing:1px;font-weight:700;' +
        'text-transform:uppercase;margin-bottom:12px;' +
      '}' +
      '#oc-daily-modal .oc-modal-title{' +
        'color:#ffe6cb;font-size:22px;margin:0 0 6px;font-weight:700;' +
      '}' +
      '#oc-daily-modal .oc-modal-desc{' +
        'color:rgba(255,230,203,0.7);font-size:16px;font-weight:600;' +
        'line-height:1.7;margin:0 0 24px;' +
      '}' +
      '#oc-daily-modal .oc-modal-body{' +
        'padding:0 32px 32px;' +
        'display:flex;flex-direction:column;align-items:center;' +
      '}' +
      '#oc-daily-modal .oc-modal-qr-wrapper{' +
        'position:relative;' +
        'padding:16px;' +
        'background:rgba(255,230,203,0.03);' +
        'border:1px solid rgba(255,230,203,0.08);' +
        'border-radius:16px;' +
        'margin-bottom:20px;' +
      '}' +
      '#oc-daily-modal .oc-modal-qr{' +
        'width:200px;height:200px;' +
        'border-radius:10px;display:block;' +
      '}' +
      '#oc-daily-modal .oc-modal-label{' +
        'color:rgba(255,230,203,0.4);font-size:12px;' +
        'text-align:center;margin:0 0 4px;letter-spacing:0.5px;' +
      '}' +
      '#oc-daily-modal .oc-modal-cta{' +
        'color:#ffd700;font-size:17px;font-weight:700;' +
        'margin:0;text-align:center;' +
      '}' +
      '#oc-daily-modal .oc-modal-footer{' +
        'background:rgba(0,0,0,0.15);' +
        'padding:14px 32px;' +
        'border-top:1px solid rgba(255,230,203,0.05);' +
      '}' +
      '#oc-daily-modal .oc-modal-footer p{' +
        'color:rgba(255,230,203,0.35);font-size:14px;font-weight:600;' +
        'margin:0;text-align:center;' +
      '}' +
      '';

    document.head.appendChild(style);

    // ===== 创建卡片 =====
    var card = document.createElement('div');
    card.className = 'oc-modal-card';

    // 关闭按钮
    var closeBtn = document.createElement('button');
    closeBtn.className = 'oc-modal-close';
    closeBtn.innerHTML = '&times;';
    closeBtn.setAttribute('aria-label', '关闭');

    // 头部
    var header = document.createElement('div');
    header.className = 'oc-modal-header';

    var badge = document.createElement('div');
    badge.className = 'oc-modal-badge';
    badge.textContent = 'WECHAT · 公众号';

    var title = document.createElement('h3');
    title.className = 'oc-modal-title';
    title.textContent = '订阅公众号获取每日日报';

    var desc = document.createElement('p');
    desc.className = 'oc-modal-desc';
    desc.innerHTML = '微信扫码关注 <strong style="color:#ffd700">「阿茅的数字大厦」</strong>，<br>每日日报上线立刻推送，公众号内可查看含链接详细版。';

    header.appendChild(badge);
    header.appendChild(title);
    header.appendChild(desc);

    // 身体（二维码）
    var body = document.createElement('div');
    body.className = 'oc-modal-body';

    var qrWrapper = document.createElement('div');
    qrWrapper.className = 'oc-modal-qr-wrapper';

    var qrImg = document.createElement('img');
    // 获取页面上的二维码图片源
    var pageQr = document.querySelector('img[alt*="二维码"]');
    qrImg.src = pageQr ? pageQr.src : '/img/daily/wechat-official-qr.jpg';
    qrImg.alt = '微信公众号「阿茅的数字大厦」二维码';
    qrImg.className = 'oc-modal-qr';

    qrWrapper.appendChild(qrImg);
    body.appendChild(qrWrapper);

    var ctaText = document.createElement('p');
    ctaText.className = 'oc-modal-cta';
    ctaText.textContent = '微信扫一扫 · 关注公众号';

    body.appendChild(ctaText);

    // 底部
    var footer = document.createElement('div');
    footer.className = 'oc-modal-footer';
    var footerP = document.createElement('p');
    footerP.textContent = '已归档 ' + AVAILABLE_DATES.length + ' 期 · 每日更新';
    footer.appendChild(footerP);

    card.appendChild(closeBtn);
    card.appendChild(header);
    card.appendChild(body);
    card.appendChild(footer);
    overlay.appendChild(card);
    document.body.appendChild(overlay);

    // ===== 事件 =====
    function openModal() {
      overlay.classList.add('show');
      overlay.style.display = 'flex';
    }

    function closeModal() {
      overlay.classList.remove('show');
      overlay.style.display = 'none';
    }

    closeBtn.addEventListener('click', closeModal);
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) closeModal();
    });
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && overlay.classList.contains('show')) closeModal();
    });

    // 绑定按钮：capture-phase 防止 Docusaurus 路由拦截
    // 1. 去公众号文字版链接
    var linksBtn = document.querySelector('.oc-daily-links');
    if (linksBtn) {
      linksBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        openModal();
      }, true);
    }

    // 2. 关注公众号每日推送按钮
    var subBtn = document.querySelector('.oc-daily-sub-bar');
    if (subBtn) {
      subBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        openModal();
      }, true);
    }

    // 3. 侧边栏 CTA 按钮（如果有）
    var sidebarCta = document.querySelector('.oc-daily-cta__primary');
    if (sidebarCta) {
      sidebarCta.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopImmediatePropagation();
        openModal();
      }, true);
    }
  }

  /* ──────── 3. 下载图片 ──────── */
  function initDownload() {
    var dlLink = document.querySelector('.oc-daily-cta__secondary');
    if (!dlLink) return;

    dlLink.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopImmediatePropagation();

      var iframe = document.querySelector('.oc-daily-frame');
      if (!iframe) return;

      var dateStr = dlLink.dataset.date || getCurrentDateStr();
      downloadViaCanvas(iframe, dateStr);
    }, true);
  }

  function downloadViaCanvas(iframe, dateStr) {
    // 加载 html2canvas
    if (typeof html2canvas === 'undefined') {
      var script = document.createElement('script');
      script.src = 'https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';
      script.onload = function() {
        doCapture(iframe, dateStr);
      };
      document.head.appendChild(script);
    } else {
      doCapture(iframe, dateStr);
    }
  }

  function doCapture(iframe, dateStr) {
    try {
      var doc = iframe.contentDocument || iframe.contentWindow.document;
      if (!doc) { console.error('Cannot access iframe document'); return; }

      var body = doc.body;
      if (!body) return;

      // 临时展开 iframe body 以完整截图
      var origOverflow = body.style.overflow;
      body.style.overflow = 'visible';

      // 获取完整的滚动宽高
      var fullHeight = body.scrollHeight;
      var fullWidth = body.scrollWidth;

      html2canvas(body, {
        scale: 2,
        useCORS: true,
        allowTaint: true,
        backgroundColor: '#041c1c',
        logging: false,
        width: fullWidth,
        height: fullHeight,
        windowWidth: fullWidth,
        windowHeight: fullHeight
      }).then(function(canvas) {
        // 恢复 overflow
        body.style.overflow = origOverflow;

        var link = document.createElement('a');
        link.download = 'openclaw-daily-' + dateStr + '.png';
        link.href = canvas.toDataURL('image/png');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }).catch(function(err) {
        console.error('html2canvas capture failed:', err);
        body.style.overflow = origOverflow;
      });
    } catch(e) {
      console.error('Download capture failed:', e);
    }
  }

  /* ──────── 初始化 ──────── */
  function init() {
    initNavigation();
    initModal();
    initDownload();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
