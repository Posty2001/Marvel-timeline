(function () {
  'use strict';
  try {
    var intro = document.getElementById('intro');
    var scroller = document.getElementById('lmScroll');
    if (!intro || !scroller || !intro.hasAttribute('data-lm')) return;
    var scenes = [intro.querySelector('.lm-act1')].concat(Array.prototype.slice.call(intro.querySelectorAll('.lm-lower .lm-act')));
    if (scenes.length !== 4 || !scenes[0]) return;
    var NAMES = ['Copertina', 'Il Multiverso si espande', 'Il futuro del Multiverso', 'Il portale TVA'];
    var NUM = ['I', 'II', 'III', 'IV'];
    var rm = function () { return !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); };
    var NS = 'http://www.w3.org/2000/svg';
    function el(tag, cls, attrs) { var e = document.createElement(tag); if (cls) e.className = cls; if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]); return e; }
    function chev(dir) { var s = document.createElementNS(NS, 'svg'); s.setAttribute('viewBox', '0 0 24 24'); s.setAttribute('aria-hidden', 'true'); s.setAttribute('focusable', 'false'); var p = document.createElementNS(NS, 'path'); p.setAttribute('d', dir < 0 ? 'M15 5l-7 7 7 7' : 'M9 5l7 7-7 7'); p.setAttribute('fill', 'none'); p.setAttribute('stroke', 'currentColor'); p.setAttribute('stroke-width', '2'); p.setAttribute('stroke-linecap', 'round'); p.setAttribute('stroke-linejoin', 'round'); s.appendChild(p); return s; }

    /* sfondo */
    var bg = el('div', 'lm-bg', { 'aria-hidden': 'true' }); ['lm-b1', 'lm-b2', 'lm-b3', 'lm-bp'].forEach(function (c) { var x = document.createElement('i'); x.className = c; bg.appendChild(x); }); scroller.insertBefore(bg, scroller.firstChild);
    /* rivelazione a cascata (solo classi: i contenuti restano quelli originali) */
    scenes[1].querySelectorAll('.lm-kick, .lm-h2, .intro-stat, .intro-honest-note').forEach(function (n, i) { n.classList.add('lm-rv'); n.style.setProperty('--i', i); });
    scenes[2].querySelectorAll('.lm-kick, .lm-h2, .intro-cd').forEach(function (n, i) { n.classList.add('lm-rv'); n.style.setProperty('--i', i); });
    scenes[3].querySelectorAll('.lm-kick, .lm-h2, .lm-portal, .lm-flicker, .lm-foot').forEach(function (n, i) { n.classList.add('lm-rv'); n.style.setProperty('--i', i); });

    /* barra di avanzamento + navigazione + annuncio per screen reader */
    var prog = el('nav', 'lm-prog', { 'aria-label': 'Avanzamento dell’introduzione' });
    var segs = NAMES.map(function (n, i) { var b = el('button', 'lm-seg', { type: 'button', 'aria-label': 'Atto ' + NUM[i] + ' — ' + n }); b.appendChild(document.createElement('i')); b.addEventListener('click', function () { go(i, 'ui'); }); prog.appendChild(b); return b; });
    var nav = el('div', 'lm-nav');
    var prev = el('button', 'lm-nb lm-prev', { type: 'button', 'aria-label': 'Atto precedente' }); prev.appendChild(chev(-1));
    var next = el('button', 'lm-nb lm-next', { type: 'button', 'aria-label': 'Atto successivo' }); next.appendChild(chev(1));
    var skip = el('button', 'lm-skip', { type: 'button' }); var sl = el('span'); sl.textContent = 'Inizia il viaggio'; skip.appendChild(sl); skip.appendChild(chev(1));
    nav.appendChild(prev); nav.appendChild(skip); nav.appendChild(next);
    var live = el('div', 'lm-live', { 'aria-live': 'polite', 'aria-atomic': 'true', role: 'status' });
    intro.appendChild(prog); intro.appendChild(nav); intro.appendChild(live);
    prev.addEventListener('click', function () { go(cur - 1, 'ui'); });
    next.addEventListener('click', function () { go(cur + 1, 'ui'); });
    skip.addEventListener('click', function () { var b = document.getElementById('journeyStartBtn'); if (b) b.click(); });

    /* statistiche: stessa sorgente della Home (tvaAtlas2.stats()); il testo statico resta come riserva se i dati non sono disponibili */
    function hydrate() {
      try {
        var A = window.tvaAtlas2, st = A && A.stats && A.stats(); if (!st) return;
        var map = { universi: st.universi, personaggi: st.personaggi, timeline: st.titoliTimeline, opere: st.opereTotali };
        scenes[1].querySelectorAll('.intro-stat-num[data-stat]').forEach(function (e) { var v = map[e.getAttribute('data-stat')]; if (typeof v === 'number' && v > 0) { e.textContent = String(v); e.setAttribute('data-final', String(v)); } });
      } catch (eH) { }
    }
    hydrate();
    /* contatori animati (il valore finale resta sempre nel testo) */
    var counters = [];
    scenes[1].querySelectorAll('.intro-stat-num').forEach(function (e) { counters.push(e); });
    scenes[2].querySelectorAll('.intro-cd > span[id]').forEach(function (e) { counters.push(e); });
    var rafs = new Map();
    function count(e) {
      var fin = e.getAttribute('data-final'); if (fin === null) { fin = (e.textContent || '').trim(); e.setAttribute('data-final', fin); }
      var m = /^(\D*)(\d+)(.*)$/.exec(fin); if (!m || rm()) { e.textContent = fin; return; }
      var to = parseInt(m[2], 10), t0 = 0, dur = Math.min(1500, 600 + to * 3);
      if (rafs.has(e)) cancelAnimationFrame(rafs.get(e));
      function step(t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), v = Math.round(to * (1 - Math.pow(1 - p, 3))); e.textContent = m[1] + v + m[3]; if (p < 1) rafs.set(e, requestAnimationFrame(step)); else { e.textContent = fin; rafs.delete(e); } }
      e.textContent = m[1] + '0' + m[3]; rafs.set(e, requestAnimationFrame(step));
    }
    function settle() { counters.forEach(function (e) { var f = e.getAttribute('data-final'); if (f !== null) { if (rafs.has(e)) cancelAnimationFrame(rafs.get(e)); rafs.delete(e); e.textContent = f; } }); }

    var cur = 0;
    function go(i, why) {
      i = Math.max(0, Math.min(scenes.length - 1, i));
      var first = why === 'init' || why === 'reset';
      if (first) { intro.classList.add('lm-instant'); }
      var changed = i !== cur || first;
      cur = i; intro.setAttribute('data-sc', String(i));
      scenes.forEach(function (s, k) {
        s.classList.add('lm-sc'); s.classList.toggle('is-on', k === i); s.classList.toggle('is-past', k < i);
        if (k === i) { s.removeAttribute('inert'); s.removeAttribute('aria-hidden'); } else { s.setAttribute('inert', ''); s.setAttribute('aria-hidden', 'true'); }
        if (k === i) s.scrollTop = 0;
      });
      segs.forEach(function (b, k) { b.classList.toggle('is-done', k < i); b.classList.toggle('is-cur', k === i); if (k === i) b.setAttribute('aria-current', 'step'); else b.removeAttribute('aria-current'); });
      prev.disabled = i === 0; next.disabled = i === scenes.length - 1;
      if (i === 1) hydrate();
      if (i === 1 || i === 2) { settle(); counters.forEach(function (e) { if (scenes[i].contains(e)) count(e); }); } else if (!first) { settle(); }
      if (changed && why !== 'init') live.textContent = 'Atto ' + NUM[i] + ' di IV: ' + NAMES[i];
      if (first) { void intro.offsetWidth; requestAnimationFrame(function () { intro.classList.remove('lm-instant'); }); }
    }
    intro.classList.add('lm-scenes');
    go(0, 'init');

    /* input: tocco, rotella, tastiera */
    function canScroll(dir) { var s = scenes[cur]; if (!s || s.scrollHeight <= s.clientHeight + 1) return false; return dir > 0 ? s.scrollTop + s.clientHeight < s.scrollHeight - 1 : s.scrollTop > 0; }
    var tx = 0, ty = 0, tt = 0, tOn = false;
    intro.addEventListener('touchstart', function (e) { if (e.touches.length !== 1) { tOn = false; return; } tOn = true; tx = e.touches[0].clientX; ty = e.touches[0].clientY; tt = Date.now(); }, { passive: true });
    intro.addEventListener('touchcancel', function () { tOn = false; }, { passive: true });
    intro.addEventListener('touchend', function (e) {
      if (!tOn) return; tOn = false; var t = e.changedTouches[0]; var dx = t.clientX - tx, dy = t.clientY - ty, ax = Math.abs(dx), ay = Math.abs(dy);
      if (Date.now() - tt > 900 || Math.max(ax, ay) < 46) return;
      if (ay >= ax) { var d = dy < 0 ? 1 : -1; if (canScroll(d)) return; go(cur + d, 'ui'); }
      else go(cur + (dx < 0 ? 1 : -1), 'ui');
    }, { passive: true });
    var wAcc = 0, wLast = 0;
    intro.addEventListener('wheel', function (e) {
      var d = e.deltaY || e.deltaX; if (!d || canScroll(d > 0 ? 1 : -1)) return;
      var n = Date.now(); if (n - wLast < 750) return; wAcc += d; if (Math.abs(wAcc) < 24) return; wLast = n; var dir = wAcc > 0 ? 1 : -1; wAcc = 0; go(cur + dir, 'ui');
    }, { passive: true });
    function visible() { var o = document.getElementById('onboardingScreen'); return intro.getClientRects().length > 0 && !(o && !o.hidden); }
    document.addEventListener('keydown', function (e) {
      if (!visible() || e.altKey || e.ctrlKey || e.metaKey) return;
      var k = e.key, t = e.target;
      if (t && t.closest && t.closest('details.intro-quiz') && (k === 'ArrowDown' || k === 'ArrowUp')) return;
      if (k === 'ArrowRight' || k === 'PageDown' || (k === 'ArrowDown' && !canScroll(1))) { e.preventDefault(); go(cur + 1, 'ui'); }
      else if (k === 'ArrowLeft' || k === 'PageUp' || (k === 'ArrowUp' && !canScroll(-1))) { e.preventDefault(); go(cur - 1, 'ui'); }
      else if (k === 'Home') { e.preventDefault(); go(0, 'ui'); }
      else if (k === 'End') { e.preventDefault(); go(scenes.length - 1, 'ui'); }
    });
    /* ritorno dalla Home alla copertina: si riparte dalla scena I */
    ['journeyStarted', 'homeHubExited'].forEach(function (id) { var c = document.getElementById(id); if (c) c.addEventListener('change', function () { if (!c.checked) go(0, 'reset'); }); });
    window.tvaIntroScenes = { go: function (i) { go(i, 'ui'); }, current: function () { return cur; }, count: scenes.length };
  } catch (err) { if (window.console) console.error('Marvel guide - intro a scene:', err); }
})();
