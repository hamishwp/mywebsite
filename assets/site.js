/* Shared site behaviour: header/footer injection, mobile nav, dropdown,
   work-card rendering (science/art), expand toggles, font sampler. */
(function () {
  "use strict";

  var NAV = [
    { label: "Home",       href: "index.html",       key: "home" },
    { label: "CV",         href: "cv.html",          key: "cv" },
    { label: "Science",    href: "science.html",     key: "science" },
    { label: "Visual Art", href: "visual-art.html",  key: "visual-art" },
    { label: "Claywork",   href: "claywork.html",    key: "claywork" },
    { label: "Literature", key: "literature", children: [
        { label: "Short Stories", href: "short-stories.html", key: "short-stories" },
        { label: "Poetry",        href: "poetry.html",        key: "poetry" }
      ] },
    { label: "Contact",    href: "contact.html",     key: "contact" }
  ];

  var SOCIAL = [
    { label: "LinkedIn",       href: "https://linkedin.com/in/hamishpatten" },
    { label: "GitHub",         href: "https://github.com/hamishwp" },
    { label: "Google Scholar", href: "https://scholar.google.com/citations?user=mwVQuFIAAAAJ&hl=en" },
    { label: "ORCID",          href: "https://orcid.org/0000-0001-5600-2097" }
  ];

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function buildHeader(active) {
    var items = NAV.map(function (item) {
      if (item.children) {
        var isActive = item.children.some(function (c) { return c.key === active; });
        var sub = item.children.map(function (c) {
          return '<a href="' + c.href + '"' + (c.key === active ? ' class="active"' : '') + '>' + esc(c.label) + '</a>';
        }).join('');
        return '<div class="dropdown' + (isActive ? ' is-active' : '') + '">' +
               '<button class="dropbtn' + (isActive ? ' active' : '') + '" aria-expanded="false">' + esc(item.label) + '</button>' +
               '<div class="dropdown-menu">' + sub + '</div></div>';
      }
      return '<a href="' + item.href + '"' + (item.key === active ? ' class="active"' : '') + '>' + esc(item.label) + '</a>';
    }).join('');

    return '<header class="site-header"><div class="nav-wrap">' +
           '<a class="brand" href="index.html">Hamish Patten</a>' +
           '<button class="nav-toggle" aria-label="Menu" aria-expanded="false">&#9776;</button>' +
           '<nav class="nav">' + items + '</nav>' +
           '</div></header>';
  }

  function buildFooter() {
    var links = SOCIAL.map(function (s) {
      return '<a href="' + s.href + '" target="_blank" rel="noopener">' + esc(s.label) + '</a>';
    }).join('');
    return '<footer class="site-footer"><div class="footer-wrap">' +
           '<span class="footer-note">&copy; Hamish Patten — statistician, physicist &amp; artist, Lausanne.</span>' +
           '<nav class="social-row">' + links + '</nav>' +
           '</div></footer>';
  }

  function wireNav() {
    var toggle = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.nav');
    if (toggle && nav) {
      toggle.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    }
    // Dropdown: hover handles desktop via CSS; click handles touch/mobile.
    document.querySelectorAll('.dropdown .dropbtn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var dd = btn.parentElement;
        var open = dd.classList.toggle('open');
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      });
    });
  }

  /* ---- Lightbox (maximise a card / photo to fill the page) ---- */
  var lightbox;
  function ensureLightbox() {
    if (lightbox) return lightbox;
    lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.setAttribute('hidden', '');
    lightbox.innerHTML =
      '<div class="lightbox-backdrop"></div>' +
      '<button class="lightbox-close" type="button" aria-label="Close">&times;</button>' +
      '<div class="lightbox-panel" role="dialog" aria-modal="true" tabindex="-1">' +
        '<div class="lightbox-content"></div></div>';
    document.body.appendChild(lightbox);
    function close() { lightbox.setAttribute('hidden', ''); document.body.style.overflow = ''; }
    lightbox.querySelector('.lightbox-backdrop').addEventListener('click', close);
    lightbox.querySelector('.lightbox-close').addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !lightbox.hasAttribute('hidden')) close();
    });
    return lightbox;
  }
  function openLightbox(html, imageOnly) {
    var lb = ensureLightbox();
    var panel = lb.querySelector('.lightbox-panel');
    lb.querySelector('.lightbox-content').innerHTML = html;
    panel.classList.toggle('image-only', !!imageOnly);
    panel.scrollTop = 0;
    lb.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';      // lock background scroll
    lb.querySelector('.lightbox-close').focus();
  }
  function imageLightboxHTML(src, alt) {
    return '<div class="lb-frame"><img src="' + src + '" alt="' + esc(alt || '') + '"></div>';
  }
  // Build the maximised view from a card's EXISTING DOM (content is server-rendered).
  function cardLightboxFromEl(card) {
    var img = card.querySelector('.card-frame img');
    var title = card.querySelector('.card-title');
    var sub = card.querySelector('.card-subtitle');
    var textEl = card.querySelector('.card-full') || card.querySelector('.card-teaser') || card.querySelector('.card-body p');
    return '<div class="lb-frame"><img src="' + (img ? img.getAttribute('src') : '') + '" alt="' + esc(img ? img.getAttribute('alt') : '') + '"></div>' +
           '<h2 class="lb-title">' + (title ? title.innerHTML : '') + '</h2>' +
           (sub ? '<p class="card-subtitle">' + sub.innerHTML + '</p>' : '') +
           '<div class="lb-text"><p>' + (textEl ? textEl.innerHTML : '') + '</p></div>';
  }

  /* ---- Responsive round-robin masonry over existing children ---- */
  var masonryFns = [];
  function masonryLayout(container, itemSel, colClass, colsFn) {
    if (!container._items) container._items = Array.prototype.slice.call(container.querySelectorAll(itemSel));
    var ncols = colsFn();
    if (container._cols === ncols) return;            // only rebuild when column count changes
    container._cols = ncols;
    container.innerHTML = '';
    var cols = [];
    for (var c = 0; c < ncols; c++) {
      var col = document.createElement('div');
      col.className = colClass;
      container.appendChild(col);
      cols.push(col);
    }
    // Round-robin: item i -> column (i % ncols), so row r holds items r*ncols..+ncols-1.
    container._items.forEach(function (it, i) { cols[i % ncols].appendChild(it); });
  }
  function registerMasonry(container, itemSel, colClass, colsFn) {
    masonryFns.push(function () { masonryLayout(container, itemSel, colClass, colsFn); });
  }
  function runMasonry() { masonryFns.forEach(function (fn) { fn(); }); }

  /* ---- Enhance server-rendered work cards: expand toggle + lightbox + keyboard ---- */
  function enhanceCards(container) {
    Array.prototype.slice.call(container.querySelectorAll('.card')).forEach(function (card) {
      var btn = card.querySelector('.expand-btn');
      if (btn) {
        btn.addEventListener('click', function () {
          var teaser = card.querySelector('.card-teaser');
          var full = card.querySelector('.card-full');
          if (full.hasAttribute('hidden')) {
            full.removeAttribute('hidden'); teaser.setAttribute('hidden', ''); btn.textContent = 'Show less';
          } else {
            full.setAttribute('hidden', ''); teaser.removeAttribute('hidden'); btn.textContent = 'Read more';
          }
        });
      }
      function maximise() { openLightbox(cardLightboxFromEl(card)); }
      card.addEventListener('click', function (e) { if (e.target.closest('a, button')) return; maximise(); });
      card.tabIndex = 0;
      card.setAttribute('role', 'button');
      card.addEventListener('keydown', function (e) {
        if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('a, button')) { e.preventDefault(); maximise(); }
      });
    });
  }

  /* ---- Enhance server-rendered gallery figures: lightbox + keyboard ---- */
  function enhanceGallery(gal) {
    Array.prototype.slice.call(gal.querySelectorAll('figure')).forEach(function (fig) {
      var img = fig.querySelector('img');
      if (!img) return;
      function open() { openLightbox(imageLightboxHTML(img.getAttribute('src'), img.getAttribute('alt')), true); }
      fig.tabIndex = 0;
      fig.setAttribute('role', 'button');
      fig.addEventListener('click', open);
      fig.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
  }

  /* ---- Font sampler (home page, first build only) ---- */
  var SAMPLE_FONTS = [
    "Playfair Display", "Cormorant Garamond", "EB Garamond", "Lora", "Cardo",
    "Crimson Pro", "Libre Baskerville", "Spectral", "Source Serif 4", "Marcellus",
    "Cinzel", "Bodoni Moda", "Prata", "Italiana", "Frank Ruhl Libre"
  ];
  function renderSampler(containerId) {
    var host = document.getElementById(containerId);
    if (!host) return;
    var heading = "Hamish Patten";
    var para = "Statistician and physicist, with paintings, pottery and writing kept alongside the science.";
    host.innerHTML = SAMPLE_FONTS.map(function (f) {
      var fam = '"' + f + '", serif';
      return '<div class="sample">' +
               '<span class="label">' + esc(f) + '</span>' +
               '<p class="h" style="font-family:' + fam + '">' + esc(heading) + '</p>' +
               '<p class="p" style="font-family:' + fam + '">' + esc(para) + '</p>' +
             '</div>';
    }).join('');
  }

  /* ---- Init ---- */
  document.addEventListener('DOMContentLoaded', function () {
    var active = document.body.getAttribute('data-page') || '';
    var h = document.getElementById('site-header');
    var f = document.getElementById('site-footer');
    if (h) h.innerHTML = buildHeader(active);
    if (f) f.innerHTML = buildFooter();
    wireNav();

    // Work cards (science / visual art) — content is server-rendered; just enhance it.
    ['science-cards', 'art-cards'].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      enhanceCards(el);
      registerMasonry(el, '.card', 'work-col', function () {
        return window.matchMedia('(min-width: 1000px)').matches ? 2 : 1;
      });
    });

    // Claywork gallery — server-rendered figures; enhance + masonry.
    document.querySelectorAll('.gallery').forEach(function (gal) {
      gal.classList.add('masonry-js');
      enhanceGallery(gal);
      registerMasonry(gal, 'figure', 'gallery-col', function () {
        return window.matchMedia('(min-width: 1000px)').matches ? 3
             : window.matchMedia('(min-width: 640px)').matches ? 2 : 1;
      });
    });

    runMasonry();
    window.addEventListener('resize', runMasonry);

    renderSampler('font-sampler');
  });
})();
