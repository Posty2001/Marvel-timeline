/* ===== TVA ARCHIVES — Visualizzatore dei grafici (pan / pinch-zoom / pulsanti, centratura iniziale) =====
   Avvolge gli SVG dei grafici legacy (Kang/TVA, Relazioni, Multiverso) in un viewport: all'apertura l'intero grafico è visibile e centrato
   (nessun nodo tagliato ai lati); si ingrandisce con pizzico, rotella o pulsanti, ci si sposta trascinando. Un trascinamento non apre i nodi. */
(function () {
  'use strict';
  try {
    var D = document, W = window;
    var SEL = '.multiverse-graph-overlay .mg-scroll > svg, .relationship-graph-overlay .mg-scroll > svg, .kang-tva-overlay .mg-scroll > svg';
    function num(v) { return parseFloat(v); }
    function mk(tag, cls, txt) { var e = D.createElement(tag); if (cls) e.className = cls; if (txt) e.textContent = txt; return e; }

    function wrapLabels(svg, B, dense) {
      // grafici radi (Kang/TVA): testo più grande e su due righe, così resta leggibile già alla vista intera
      var cw = (svg.closest('.a2-vp-stage') || svg.parentNode).clientWidth || 360, px = (dense ? 9 : 10.5) / (cw / B.w); var fs = Math.max(12, Math.min(dense ? 26 : 20, px));
      Array.prototype.forEach.call(svg.querySelectorAll('text.mg-node-label'), function (t) {
        if (t.__wrapped || t.classList.contains('rg-nm') || t.classList.contains('rg-hub-label')) return; t.__wrapped = true;
        var txt = t.textContent.trim(), x = t.getAttribute('x'), words = txt.split(/\s+/);
        var cur = parseFloat(t.style.fontSize || t.getAttribute('font-size')) || 0; t.style.fontSize = Math.max(cur, fs) + 'px';
        if (words.length < 2 && !/\//.test(txt) || txt.length <= 11) return;
        if (words.length < 2) words = txt.split(/(?<=\/)/);
        var best = 1, bd = 1e9; for (var i = 1; i < words.length; i++) { var d = Math.abs(words.slice(0, i).join(' ').length - words.slice(i).join(' ').length); if (d < bd) { bd = d; best = i; } }
        t.textContent = '';
        [words.slice(0, best).join(' '), words.slice(best).join(' ')].forEach(function (ln, k) {
          var ts = D.createElementNS('http://www.w3.org/2000/svg', 'tspan'); ts.setAttribute('x', x); ts.setAttribute('dy', k ? '1.12em' : '0'); ts.textContent = ln; t.appendChild(ts);
        });
      });
    }

    function computeBase(vbs, sparse, fixedAspect) {
      var aspect = fixedAspect || (sparse ? vbs[2] / vbs[3] : 0.92);   // grafici densi: area più alta per usare lo schermo verticale
      var pad = vbs[2] * 0.04, W0 = vbs[2] + pad * 2, H0 = W0 / aspect, cy0 = vbs[1] + vbs[3] / 2;
      var B = { x: vbs[0] - pad, y: cy0 - H0 / 2, w: W0, h: H0 };
      if (H0 < vbs[3] + pad * 2) { H0 = vbs[3] + pad * 2; B.h = H0; B.y = cy0 - H0 / 2; }
      return B;
    }
    function attach(svg, opts) {
      if (svg.__vp) return; var o = opts || {};
      var vbs = (svg.getAttribute('data-vb') || svg.getAttribute('viewBox') || '').split(/[\s,]+/).map(num); if (vbs.length !== 4 || vbs.some(isNaN)) return;
      var sparse = o.sparse !== undefined ? !!o.sparse : !!svg.closest('.kang-tva-overlay');
      var B = computeBase(vbs, sparse, o.aspect);
      var host = svg.parentNode, wrap = mk('div', 'a2-vp'), stage = mk('div', 'a2-vp-stage');
      host.insertBefore(wrap, svg); wrap.appendChild(stage); stage.appendChild(svg); stage.style.aspectRatio = (B.w / B.h).toFixed(4);
      svg.style.width = '100%'; svg.style.height = '100%'; svg.style.maxWidth = 'none'; svg.removeAttribute('width'); svg.removeAttribute('height'); svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
      var MAXZ = o.maxZ || (sparse ? 4 : 7), v = { cx: B.x + B.w / 2, cy: B.y + B.h / 2, z: 1 };
      if (!o.noLabels) wrapLabels(svg, B, !sparse);
      function apply() {
        var w = B.w / v.z, h = B.h / v.z;
        v.cx = Math.min(B.x + B.w - w / 2, Math.max(B.x + w / 2, v.cx)); v.cy = Math.min(B.y + B.h - h / 2, Math.max(B.y + h / 2, v.cy));
        svg.setAttribute('viewBox', (v.cx - w / 2).toFixed(2) + ' ' + (v.cy - h / 2).toFixed(2) + ' ' + w.toFixed(2) + ' ' + h.toFixed(2));
        wrap.setAttribute('data-z', v.z.toFixed(2)); wrap.classList.toggle('a2-vp-zoomed', v.z > 1.01); wrap.classList.toggle('a2-vp-z2', v.z >= 1.5);
      }
      function upp() { return (B.w / v.z) / (stage.clientWidth || 360); }          // unità SVG per pixel
      function zoomAt(f, px, py) {                                                  // px/py: punto fisso in coordinate stage
        var nz = Math.min(MAXZ, Math.max(1, v.z * f)); if (nz === v.z) return;
        var r = stage.getBoundingClientRect(), u = upp(), w = B.w / v.z, h = B.h / v.z;
        var ux = v.cx - w / 2 + (px - r.left) * u, uy = v.cy - h / 2 + (py - r.top) * u;
        v.z = nz; var w2 = B.w / v.z, h2 = B.h / v.z, u2 = upp();
        v.cx = ux - (px - r.left) * u2 + w2 / 2; v.cy = uy - (py - r.top) * u2 + h2 / 2; apply();
      }
      function fit() { v.z = 1; v.cx = B.x + B.w / 2; v.cy = B.y + B.h / 2; apply(); }
      apply();

      var ptr = {}, drag = false, suppress = false, last = null, pinch = null;
      function cnt() { return Object.keys(ptr).length; }
      stage.addEventListener('pointerdown', function (e) {
        ptr[e.pointerId] = { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY };
        if (cnt() === 2) { var k = Object.keys(ptr), p1 = ptr[k[0]], p2 = ptr[k[1]]; pinch = { d: Math.hypot(p1.x - p2.x, p1.y - p2.y), mx: (p1.x + p2.x) / 2, my: (p1.y + p2.y) / 2 }; drag = true; }
      });
      stage.addEventListener('pointermove', function (e) {
        var p = ptr[e.pointerId]; if (!p) return;
        if (cnt() >= 2 && pinch) {
          p.x = e.clientX; p.y = e.clientY; var k = Object.keys(ptr), p1 = ptr[k[0]], p2 = ptr[k[1]];
          var d = Math.hypot(p1.x - p2.x, p1.y - p2.y), mx = (p1.x + p2.x) / 2, my = (p1.y + p2.y) / 2;
          if (pinch.d > 0) zoomAt(d / pinch.d, mx, my);
          var u = upp(); v.cx -= (mx - pinch.mx) * u; v.cy -= (my - pinch.my) * u; apply(); pinch = { d: d, mx: mx, my: my }; e.preventDefault(); return;
        }
        var dx = e.clientX - p.x, dy = e.clientY - p.y;
        if (!drag && Math.hypot(e.clientX - p.sx, e.clientY - p.sy) > 7) { drag = true; try { stage.setPointerCapture(e.pointerId); } catch (x) {} }
        if (drag) { var uu = upp(); v.cx -= dx * uu; v.cy -= dy * uu; apply(); e.preventDefault(); }
        p.x = e.clientX; p.y = e.clientY;
      });
      function up(e) {
        if (!ptr[e.pointerId]) return; delete ptr[e.pointerId]; pinch = null;
        if (drag) { suppress = true; setTimeout(function () { suppress = false; }, 80); }
        if (!cnt()) drag = false;
      }
      stage.addEventListener('pointerup', up); stage.addEventListener('pointercancel', up);
      stage.addEventListener('click', function (e) { if (suppress) { e.stopPropagation(); e.preventDefault(); } }, true);
      stage.addEventListener('wheel', function (e) { e.preventDefault(); zoomAt(e.deltaY < 0 ? 1.25 : 0.8, e.clientX, e.clientY); }, { passive: false });

      var ctl = mk('div', 'a2-vp-ctl');
      [['+', 'Ingrandisci', function () { var r = stage.getBoundingClientRect(); zoomAt(1.5, r.left + r.width / 2, r.top + r.height / 2); }],
       ['−', 'Riduci', function () { var r = stage.getBoundingClientRect(); zoomAt(1 / 1.5, r.left + r.width / 2, r.top + r.height / 2); }],
       ['⤢', 'Adatta alla schermata', fit]].forEach(function (c) {
        var b = mk('button', 'a2-vp-b', c[0]); b.type = 'button'; b.setAttribute('aria-label', c[1]); b.title = c[1]; b.addEventListener('click', function (e) { e.stopPropagation(); c[2](); }); ctl.appendChild(b);
      });
      var bar = mk('div', 'a2-vp-bar'); bar.appendChild(mk('p', 'a2-vp-hint', o.hint || 'Pizzica per ingrandire · trascina per spostarti · tocca un nodo per i dettagli')); bar.appendChild(ctl); wrap.appendChild(bar);
      // il grafo delle relazioni viene ridisegnato a ogni ricerca: si torna alla vista intera, centrata
      function rebase() {                                                           // il disegno può cambiare altezza (es. grafo delle relazioni): nuova base e vista intera
        var nv = (svg.getAttribute('data-vb') || '').split(/[\s,]+/).map(num);
        if (nv.length === 4 && !nv.some(isNaN)) { var nb = computeBase(nv, sparse, o.aspect); B.x = nb.x; B.y = nb.y; B.w = nb.w; B.h = nb.h; stage.style.aspectRatio = (B.w / B.h).toFixed(4); }
      }
      if (svg.id) new MutationObserver(function () { rebase(); if (!o.noLabels) wrapLabels(svg, B, !sparse); fit(); }).observe(svg, { childList: true });
      svg.__vp = { fit: fit, zoomAt: zoomAt, state: v, base: B, rebase: rebase };
    }

    /* Timeline degli Universi: nomi allineati alle righe, salto rapido ai capitoli, indicazione dello scorrimento laterale */
    function utFix() {
      var ov = D.querySelector('.universe-timeline-overlay'); if (!ov) return;
      var body = ov.querySelector('.ut-body'), svg = ov.querySelector('.ut-svg'), lab = ov.querySelector('.ut-labels-fixed'), sc = ov.querySelector('.mg-scroll'); if (!body || !svg || !lab || !sc) return;
      if (svg.getClientRects().length) { lab.style.transform = ''; var dy = svg.getBoundingClientRect().top - lab.getBoundingClientRect().top; if (Math.abs(dy) > 0.5) lab.style.transform = 'translateY(' + dy.toFixed(1) + 'px)'; }
      if (body.__utBar) return; body.__utBar = true;
      if (W.ResizeObserver) { var ro = new W.ResizeObserver(function () { utFix(); }); ro.observe(svg); ro.observe(ov); }
      var bar = mk('div', 'a2-ut-bar'); bar.appendChild(mk('span', 'a2-ut-l', 'Scorri di lato · salta a'));
      Array.prototype.forEach.call(svg.querySelectorAll('.ut-marker-label'), function (t) {
        var b = mk('button', 'a2-ut-j', t.textContent.trim()); b.type = 'button'; b.setAttribute('aria-label', 'Vai al titolo ' + t.textContent.trim());
        b.addEventListener('click', function () { var x = parseFloat(t.getAttribute('x')) || 0, k = svg.getBoundingClientRect().width / (svg.viewBox.baseVal.width || 1); try { sc.scrollTo({ left: Math.max(0, x * k - sc.clientWidth / 2), behavior: 'smooth' }); } catch (e) { sc.scrollLeft = Math.max(0, x * k - sc.clientWidth / 2); } });
        bar.appendChild(b);
      });
      body.parentNode.insertBefore(bar, body);
    }
    function scan() { utFix(); Array.prototype.forEach.call(D.querySelectorAll(SEL), attach); }
    W_init();
    function W_init() {
      if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', scan); else scan();
      D.addEventListener('change', function (e) { if (e.target && /Toggle$/.test(e.target.id || '')) setTimeout(function () { scan(); utFix(); Array.prototype.forEach.call(D.querySelectorAll(SEL), function (s) { if (s.__vp && e.target.checked) s.__vp.fit(); }); }, 60); });
    }
    window.addEventListener('resize', function () { utFix(); });
    window.tvaGraphVP = { scan: scan, utFix: utFix, attach: attach };
  } catch (err) { try { console.error('graphvp', err); } catch (x) {} }
})();
