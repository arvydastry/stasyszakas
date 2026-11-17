/* Stasys Zakas demo: bendras JS. Kiekvienas blokas atitinka natyvų Salient elgesį (žr. README). */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Split Line Heading: žodžiai ir raidės išnyra iš apačios */
  $$('[data-split]').forEach(function (h) {
    var n = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (ch) {
        if (ch.nodeType === 3) {
          var frag = document.createDocumentFragment();
          ch.textContent.split(/(\s+)/).forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(' ')); return; }
            var w = document.createElement('span'); w.className = 'w';
            part.split('').forEach(function (c) {
              var s = document.createElement('span'); s.className = 'c'; s.textContent = c;
              s.style.transitionDelay = Math.min(n++ * 28, 900) + 'ms'; w.appendChild(s);
            });
            frag.appendChild(w);
          });
          node.replaceChild(frag, ch);
        } else if (ch.nodeType === 1 && ch.tagName !== 'BR') walk(ch);
      });
    })(h);
    h.setAttribute('aria-label', h.textContent);
  });

  /* Stulpelių ir linijų atsiradimas */
  var targets = $$('[data-reveal], [data-split]');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, d = +el.getAttribute('data-delay') || 0;
        setTimeout(function () { el.classList.add('is-in'); }, d);
        io.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (t) { io.observe(t); });
  } else targets.forEach(function (t) { t.classList.add('is-in'); });

  /* Hero slaideris (Nectar Slider: fade + Ken Burns, autoplay) */
  var hero = $('[data-hero]');
  if (hero) {
    var slides = $$('.hero__slide', hero), dots = $$('.hero__dot', hero), cur = 0, timer = null, DUR = 6000;
    hero.style.setProperty('--dur', DUR / 1000 + 's');
    var restart = function () { clearTimeout(timer); if (!reduce && !hero.hasAttribute('data-paused')) timer = setTimeout(function () { go(cur + 1); }, DUR); };
    var go = function (n) {
      n = (n + slides.length) % slides.length;
      if (n === cur) return;
      var old = cur;
      slides[old].classList.remove('is-active'); slides[old].classList.add('is-leaving');
      setTimeout(function () { slides[old].classList.remove('is-leaving'); }, 1700);
      cur = n;
      $('img', slides[cur]).loading = 'eager';
      slides[cur].classList.add('is-active');
      dots.forEach(function (d, i) { d.classList.toggle('is-active', i === cur); });
      restart();
    };
    dots.forEach(function (d, i) {
      d.addEventListener('click', function (e) { if (e.target.closest('a') && i === cur) return; e.preventDefault(); go(i); });
    });
    hero.addEventListener('mouseenter', function () { hero.setAttribute('data-paused', ''); clearTimeout(timer); });
    hero.addEventListener('mouseleave', function () { hero.removeAttribute('data-paused'); restart(); });
    document.addEventListener('visibilitychange', function () { if (document.hidden) clearTimeout(timer); else restart(); });
    dots[0].classList.add('is-active'); restart();
  }

  /* Ilgi pavadinimai sluoksniuotose kortelėse */
  $$('.stack__title').forEach(function (t) {
    var len = t.textContent.trim().length;
    if (len > 14) t.classList.add('is-xlong'); else if (len > 8) t.classList.add('is-long');
  });

  /* Antraštė: slepiasi slenkant žemyn; hero parallax; kortelių „blurred scale“ */
  var header = $('.site-header'), heroBg = $('.hero__slides'), cards = $$('.stack__item');
  var lastY = 0, ticking = false;
  function frame() {
    ticking = false;
    var y = window.scrollY;
    if (header) {
      header.classList.toggle('is-hidden', y > lastY && y > 300 && !$('.nav.is-open'));
    }
    lastY = y;
    if (reduce) return;
    if (heroBg && y < window.innerHeight) heroBg.style.transform = 'translateY(' + (y * 0.18).toFixed(1) + 'px)';
    cards.forEach(function (item, i) {
      var next = cards[i + 1], card = item.firstElementChild;
      if (!next) return;
      var r = item.getBoundingClientRect(), n = next.getBoundingClientRect();
      var p = Math.max(0, Math.min(1, (r.bottom - n.top) / r.height)); /* kiek kita kortelė jau uždengė */
      card.style.transform = p ? 'scale(' + (1 - 0.2 * p).toFixed(3) + ')' : '';
      card.style.filter = p ? 'blur(' + (5 * p).toFixed(1) + 'px)' : '';
    });
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }, { passive: true });
  frame();

  /* Mobilus meniu */
  var burger = $('.burger'), nav = $('.nav');
  if (burger) burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });

  /* Žymeklio piliulė „Žiūrėti“ */
  var ind = $('.view-indicator');
  if (ind && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.addEventListener('mousemove', function (e) {
      var on = e.target.closest && e.target.closest('[data-view]');
      ind.classList.toggle('is-on', !!on);
      if (on) ind.style.transform = 'translate(' + (e.clientX + 14) + 'px,' + (e.clientY + 14) + 'px)';
    }, { passive: true });
  }

  /* Paveikslo padidinimas */
  var lb = $('.lightbox');
  if (lb) {
    var lbImg = $('img', lb), opener = null;
    var close = function () { lb.hidden = true; lb.classList.remove('is-zoom'); document.body.style.overflow = ''; if (opener) opener.focus(); };
    $$('[data-lightbox]').forEach(function (b) {
      b.addEventListener('click', function () {
        opener = b; lbImg.src = b.getAttribute('data-lightbox'); lbImg.alt = ($('img', b) || {}).alt || '';
        lb.hidden = false; document.body.style.overflow = 'hidden'; $('.lightbox__close', lb).focus();
      });
    });
    lbImg.addEventListener('click', function (e) { e.stopPropagation(); lb.classList.toggle('is-zoom'); });
    lb.addEventListener('click', close);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  /* Galerija: filtrai, „Rodyti daugiau“ */
  var grid = $('#galerija');
  if (grid) {
    var all = $$('.card', grid), filters = $$('.filter'), more = $('.btn-more'), count = $('.gallery__count');
    var STEP = 24, shown = STEP, cat = 'all';
    var apply = function () {
      var match = all.filter(function (c) { return cat === 'all' || c.getAttribute('data-cat') === cat; });
      all.forEach(function (c) { c.hidden = true; });
      match.slice(0, shown).forEach(function (c) { c.hidden = false; });
      more.hidden = shown >= match.length;
      count.textContent = 'Rodoma ' + Math.min(shown, match.length) + ' iš ' + match.length;
      filters.forEach(function (f) {
        var on = f.getAttribute('data-filter') === cat;
        f.classList.toggle('is-active', on); f.setAttribute('aria-pressed', on);
      });
    };
    filters.forEach(function (f) { f.addEventListener('click', function () { cat = f.getAttribute('data-filter'); shown = STEP; apply(); }); });
    more.addEventListener('click', function () { shown += STEP; apply(); });
    var q = new URLSearchParams(location.search).get('tema');
    if (q && filters.some(function (f) { return f.getAttribute('data-filter') === q; })) cat = q;
    apply();
  }

  /* Kontaktų forma: nieko nesiunčia, rodo sėkmės būseną; ?darbas=<slug> parodo dominantį darbą */
  var form = $('.form');
  if (form) {
    var slug = new URLSearchParams(location.search).get('darbas');
    if (slug && /^[a-z0-9-]+$/.test(slug)) {
      var box = $('.form__work', form), img = $('img', box);
      img.onload = function () { box.hidden = false; };
      img.src = 'assets/img/works/' + slug + '-480.jpg';
      fetch('kuryba/' + slug + '.html').then(function (r) { return r.text(); }).then(function (t) {
        var m = t.match(/<title>([^|<]+)/); if (m) { $('b', box).textContent = m[1].trim(); img.alt = m[1].trim(); }
      }).catch(function () { $('b', box).textContent = slug; });
    }
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true;
      $$('.field', form).forEach(function (f) {
        var i = $('input,textarea', f); if (!i) return;
        var bad = !i.checkValidity(); f.classList.toggle('is-bad', bad); if (bad) ok = false;
      });
      var chk = $('.check input', form); if (!chk.checked) { ok = false; chk.focus(); }
      if (ok) { $('.form__ok', form).hidden = false; $('button[type=submit]', form).disabled = true; }
    });
  }
})();
