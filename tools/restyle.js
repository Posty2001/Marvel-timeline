/* RS-JS-BEGIN: restyling — solo presentazione. Non modifica dati, ID, logica o storage (eccetto la preferenza tema v2). */
(function () {
  'use strict';
  var D = document, W = window;
  if (W.__rsSkin) return; W.__rsSkin = true;
  var MAP = /*RS_MAP*/{}/*RS_MAP_END*/;
  var cps = Object.keys(MAP).map(function (k) { return parseInt(k, 10); });
  var RE = null;
  try {
    RE = new RegExp('(' + cps.map(function (c) { return '\\u{' + c.toString(16) + '}'; }).join('|') + ')[\\uFE0E\\uFE0F]?', 'gu');
  } catch (e) { RE = null; }
  var SKIP = { SCRIPT: 1, STYLE: 1, TEXTAREA: 1, OPTION: 1, SELECT: 1, TITLE: 1, INPUT: 1, NOSCRIPT: 1, SVG: 1, svg: 1, CANVAS: 1 };

  function skipEl(el) {
    for (; el && el !== D.body; el = el.parentNode) {
      if (el.nodeType !== 1) continue;
      if (SKIP[el.nodeName]) return true;
      var c = el.classList;
      if (c && (c.contains('rs-i') || c.contains('a2') || c.contains('intro-screen') || c.contains('lm-scene'))) return true;
      if (el.isContentEditable) return true;
    }
    return false;
  }
  function wrapText(tn) {
    var t = tn.nodeValue;
    if (!t || t.length > 600) return;
    RE.lastIndex = 0; if (!RE.test(t)) return;
    if (skipEl(tn.parentNode)) return;
    RE.lastIndex = 0;
    var pe = tn.parentNode;
    if (pe.nodeName === 'SPAN' && pe.hasAttribute('title') && pe.childNodes.length === 1) {
      var mm = RE.exec(t); RE.lastIndex = 0;
      if (mm && mm[0].length === t.trim().length && !pe.className) { var nm = MAP[mm[0].codePointAt(0)]; if (nm && nm.indexOf('dot') !== 0) { pe.className = 'rs-i'; pe.setAttribute('data-ic', nm); return; } }
    }
    var frag = D.createDocumentFragment(), last = 0, m;
    while ((m = RE.exec(t))) {
      var cp = m[0].codePointAt(0), name = MAP[cp]; if (!name) continue;
      if (m.index > last) frag.appendChild(D.createTextNode(t.slice(last, m.index)));
      var s = D.createElement('span'); s.className = 'rs-i'; s.setAttribute('data-ic', name); s.setAttribute('aria-hidden', 'true');
      s.textContent = m[0];
      if (name.indexOf('dot') === 0) s.style.background = DOT[name] || 'currentColor';
      frag.appendChild(s); last = m.index + m[0].length;
    }
    if (last === 0) return;
    if (last < t.length) frag.appendChild(D.createTextNode(t.slice(last)));
    var par = tn.parentNode;
    if (t.replace(RE, '').trim().length) { var wr = D.createElement('span'); wr.className = 'rs-w'; wr.appendChild(frag); par.replaceChild(wr, tn); }
    else par.replaceChild(frag, tn);
  }
  var DOT = { dot1f534: '#DB777C', dot1f535: '#8fb8d8', dot1f7e0: '#E2A46B', dot1f7e1: '#D2B184', dot1f7e2: '#8cc3a0', dot1f7e3: '#b79be0', dot1f7e4: '#a58468', dot1f7ec: '#a58468' };
  function walk(root) {
    if (!RE || !root) return;
    if (root.nodeType === 3) { wrapText(root); return; }
    if (root.nodeType !== 1 || skipEl(root)) return;
    var w = D.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), n, list = [];
    while ((n = w.nextNode())) { if (n.nodeValue && n.nodeValue.length < 600 && n.nodeValue.charCodeAt(0) !== undefined) list.push(n); }
    for (var i = 0; i < list.length; i++) wrapText(list[i]);
  }
  var pend = [], raf = 0;
  function flush() { raf = 0; var l = pend; pend = []; for (var i = 0; i < l.length; i++) { try { if (l[i].isConnected !== false) walk(l[i]); } catch (e) {} } syncHome(); }
  function queue(n) { pend.push(n); if (!raf) raf = W.requestAnimationFrame ? W.requestAnimationFrame(flush) : setTimeout(flush, 16); }

  /* ---- Home: barra progresso + scheda missioni (sola lettura, ricavata dal DOM esistente) ---- */
  function q(s, r) { return (r || D).querySelector(s); }
  function syncHome() {
    var hub = q('#homeHub'); if (!hub) return;
    var line = q('.home-hub-pct-line', hub), pct = q('#hhgPct');
    if (line && pct) {
      var bar = q('.rs-prog', hub);
      if (!bar) { bar = D.createElement('div'); bar.className = 'rs-prog'; bar.setAttribute('aria-hidden', 'true'); bar.appendChild(D.createElement('i')); line.parentNode.appendChild(bar); }
      var v = parseFloat(String(pct.textContent).replace(',', '.')) || 0; bar.firstChild.style.width = Math.max(0, Math.min(100, v)) + '%';
    }
    var inner = q('.home-hub-inner', hub); if (!inner) return;
    var card = q('#rsHomeMis', inner);
    var st = q('#dashboard .stagione-tva-card');
    if (!st) { if (card) card.style.display = 'none'; return; }
    if (!card) { card = D.createElement('button'); card.type = 'button'; card.id = 'rsHomeMis'; card.setAttribute('aria-label', 'Apri Missioni'); card.addEventListener('click', function () { var t = D.getElementById('appTabMissioni'); if (t) t.click(); }); inner.appendChild(card); }
    var rows = [], seen = 0, mr = D.querySelectorAll('#dashboard .stagione-tva-card, #dashboard .missione-row');
    for (var i = 0; i < mr.length && rows.length < 3; i++) {
      var e = mr[i], nm = q('.stagione-tva-nome, .missione-testo', e), fr = q('.stagione-tva-frac, .missione-frac', e), fl = q('.stagione-tva-fill, .missione-fill', e);
      if (!nm || !fr || e.querySelector('.missione-segreta')) continue;
      var f = String(fr.textContent).match(/(\d+)\s*\/\s*(\d+)/); if (!f) continue;
      if (e.classList.contains('missione-row') && +f[1] >= +f[2] && seen >= 0) continue;
      var name = (q('b', nm) || nm).textContent.replace(/\s+/g, ' ').trim().slice(0, 60);
      rows.push({ n: name, f: f[1] + '/' + f[2], w: (+f[2] ? Math.round(100 * f[1] / f[2]) : 0) });
    }
    var html = '<div class="rs-mh"><span>Missioni</span><span>Apri &rsaquo;</span></div>';
    for (var j = 0; j < rows.length; j++) html += '<div class="rs-mr"><b></b><span>' + rows[j].f + '</span></div><div class="rs-prog"><i style="width:' + rows[j].w + '%"></i></div>';
    var sig = JSON.stringify(rows); if (card.__sig === sig) return; card.__sig = sig;
    card.innerHTML = html; var bs = card.querySelectorAll('.rs-mr b'); for (var k = 0; k < bs.length; k++) bs[k].textContent = rows[k].n;
    card.style.display = rows.length ? '' : 'none';
    walk(card);
  }

  /* ---- Menu circolare: si ritrae scorrendo verso il basso, ricompare risalendo ---- */
  function menuHide() {
    var b = q('.sidebar-open-btn'); if (!b) return; var last = W.pageYOffset || 0, tk = 0;
    function onS(e) {
      var y = (e && e.target && e.target !== D && e.target.scrollTop != null) ? e.target.scrollTop : (W.pageYOffset || 0);
      var d = y - last; if (Math.abs(d) < 6) return; last = y;
      b.classList.toggle('rs-away', d > 0 && y > 80);
    }
    W.addEventListener('scroll', onS, { passive: true }); D.addEventListener('scroll', onS, { passive: true, capture: true });
  }

  function init() {
    if (!D.body) return;
    try { walk(D.body); } catch (e) {}
    try {
      var mo = new MutationObserver(function (ms) {
        for (var i = 0; i < ms.length; i++) {
          var m = ms[i];
          if (m.type === 'childList') { for (var j = 0; j < m.addedNodes.length; j++) { var n = m.addedNodes[j]; if (n.nodeType === 1 && n.classList && n.classList.contains('rs-i')) continue; queue(n); } }
          else if (m.type === 'characterData') { if (m.target.parentNode && !(m.target.parentNode.classList && m.target.parentNode.classList.contains('rs-i'))) queue(m.target); }
        }
      });
      mo.observe(D.body, { childList: true, subtree: true, characterData: true });
    } catch (e) {}
    menuHide(); syncHome(); setTimeout(syncHome, 800); setTimeout(syncHome, 2500);
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', init); else init();
})();
/* RS-JS-END */
