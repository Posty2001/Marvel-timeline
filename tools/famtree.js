/* ===== TVA ARCHIVES — Alberi genealogici come diagrammi (SVG) =====
   I legami vengono letti dalle frasi delle schede della guida («sposato con», «padre di», «figlia di», «fratello di», «compagna di»):
   un legame esiste solo se una frase lo afferma. Nessun nodo o linea è aggiunto per completare la simmetria. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function se(tag, attrs, parent) { var e = document.createElementNS(NS, tag); if (attrs) for (var k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.appendChild(e); return e; }
  function norm(s) { return (s || '').replace(/[’‘`]/g, "'").toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/\s+/g, ' ').trim(); }

  /* ---------- 1) lettura dei dati ---------- */
  function parse(host, resolveChar) {
    var nodes = [], gens = host.querySelectorAll('.tree-gen');
    Array.prototype.forEach.call(gens, function (g, gi) {
      Array.prototype.forEach.call(g.querySelectorAll('.tree-node'), function (n) {
        var nm = n.querySelector('.tree-node-name'), an = nm && nm.querySelector('a'), oc = an && an.getAttribute('onclick') || '', mm = oc.match(/mvNavigate\('([^']+)','char'/);
        var name = nm ? nm.textContent.trim() : '', role = (n.querySelector('.tree-node-role') || {}).textContent || '', rel = (n.querySelector('.tree-node-rel') || {}).textContent || '';
        var base = name.split('/')[0].trim(), keys = [norm(name), norm(base), norm(base.split(' ')[0])];
        name.split('/').forEach(function (p) { keys.push(norm(p)); });
        var o = { i: nodes.length, gen: gi, name: name, short: base, role: role.trim(), rel: rel.trim(), keys: keys, id: mm ? mm[1] : null };
        if (!o.id && resolveChar) o.id = resolveChar(name) || null;
        nodes.push(o);
      });
    });
    function find(ref) { var k = norm(ref.replace(/^(?:il|lo|la|l')\s*/i, '')); for (var i = 0; i < nodes.length; i++) if (nodes[i].keys.indexOf(k) > -1) return nodes[i]; return null; }
    function list(seg) { return seg.split(/\s+e\s+|,\s*/).map(function (x) { return find(x.trim()); }).filter(Boolean); }
    var marriages = [], partners = [], parents = [], sibs = [], seen = {};
    function once(k) { if (seen[k]) return false; seen[k] = 1; return true; }
    nodes.forEach(function (n) {
      var t = n.rel + '. ' + n.role, m, re;
      if (/nessun legame di sangue/i.test(n.rel)) n.nonblood = true;
      re = /spos(?:ato|ata)\s+con\s+([^,.;]+)/gi; while ((m = re.exec(t))) list(m[1]).forEach(function (o) { if (o !== n && once('m' + Math.min(n.i, o.i) + '-' + Math.max(n.i, o.i))) marriages.push([n, o]); });
      re = /compagn[oa]\s+di\s+([^,.;]+)/gi; while ((m = re.exec(t))) list(m[1]).forEach(function (o) { if (o !== n && once('p' + Math.min(n.i, o.i) + '-' + Math.max(n.i, o.i))) partners.push([n, o]); });
      re = /(padre|madre)(\s+adottiv[oa])?\s+di\s+([^,.;]+)/gi; while ((m = re.exec(t))) list(m[3]).forEach(function (c) { if (c !== n && once('c' + n.i + '>' + c.i)) parents.push({ p: n, c: c, adopt: !!m[2] }); });
      re = /(?:figli[oa]|primogenit[oa])(\s+(?:segret[oa]|adottiv[oa]))?\s+di\s+([^,.;]+)/gi; while ((m = re.exec(t))) list(m[2]).forEach(function (p) { if (p !== n && once('c' + p.i + '>' + n.i)) parents.push({ p: p, c: n, adopt: /adottiv/i.test(m[1] || ''), secret: /segret/i.test(m[1] || '') }); });
      re = /(?:fratell[oi]|sorell[ae])\s+di\s+([^,.;]+)/gi; while ((m = re.exec(t))) list(m[1]).forEach(function (o) { if (o !== n && once('s' + Math.min(n.i, o.i) + '-' + Math.max(n.i, o.i))) sibs.push([n, o]); });
    });
    // se una frase dice «adottivo» per un figlio, la sua linea è tratteggiata; i figli di una stessa coppia sono fratelli solo se la guida lo afferma
    return { nodes: nodes, marriages: marriages, partners: partners, parents: parents, sibs: sibs };
  }

  /* ---------- 2) disposizione ---------- */
  var W = 104, H = 58, GX = 20, CG = 30, RG = 96, PAD = 14, TOP = 18, GUT = 20;
  function layout(M) {
    var nodes = M.nodes, unitOf = {}, units = [];
    function mkUnit(ms) { var u = { m: ms, kids: [], par: null, w: 0, x: 0, ties: [] }; ms.forEach(function (n) { unitOf[n.i] = u; }); units.push(u); return u; }
    var cp = M.marriages.map(function (e) { return { e: e, t: 'm' }; }).concat(M.partners.map(function (e) { return { e: e, t: 'p' }; }));
    cp.forEach(function (c) {
      var a = c.e[0], b = c.e[1]; if (unitOf[a.i] || unitOf[b.i]) return;
      var ms = a.i < b.i ? [a, b] : [b, a]; var u = mkUnit(ms); u.tie = c.t;
    });
    nodes.forEach(function (n) { if (!unitOf[n.i]) mkUnit([n]); });
    // genitori di ogni unità: l'unità dei genitori del primo membro che ha genitori
    units.forEach(function (u) {
      for (var k = 0; k < u.m.length && !u.par; k++) {
        var ps = M.parents.filter(function (r) { return r.c === u.m[k]; }); if (!ps.length) continue;
        // il discendente si appende all'unità del primo genitore (i genitori in coppia condividono la stessa unità)
        var pu = unitOf[ps[0].p.i]; if (pu !== u) { u.par = pu; pu.kids.push(u); }
      }
    });
    function sw(u) { return u.m.length * W + (u.m.length - 1) * CG; }
    function mw(u) { var k = u.kids; if (!k.length) { u.w = sw(u); return u.w; } var s = 0; k.forEach(function (c) { s += mw(c); }); s += (k.length - 1) * GX; u.w = Math.max(sw(u), s); return u.w; }
    // ordine dei figli: ordine dei nodi nei dati
    units.forEach(function (u) { u.kids.sort(function (a, b) { return a.m[0].i - b.m[0].i; }); });
    var roots = units.filter(function (u) { return !u.par; }).sort(function (a, b) { return a.m[0].i - b.m[0].i; });
    // fratelli senza genitori nei dati (es. Sue e Johnny): le radici vengono affiancate nell'ordine che li rende adiacenti
    var order = []; roots.forEach(function (r) { order.push(r); });
    var changed = true, guard = 0;
    while (changed && guard++ < 10) { changed = false; M.sibs.forEach(function (s) { var a = unitOf[s[0].i], b = unitOf[s[1].i]; if (a.par || b.par) return; var ia = order.indexOf(a), ib = order.indexOf(b); if (ia < 0 || ib < 0 || Math.abs(ia - ib) === 1) return; order.splice(ib, 1); order.splice(ia + (ib > ia ? 1 : 0), 0, b); changed = true; }); }
    var x0 = PAD + GUT, total = 0;
    function place(u, left) {
      var w = mw(u), cx;
      if (u.kids.length) { var kw = -GX; u.kids.forEach(function (c) { kw += c.w + GX; }); var l = left + Math.max(0, (w - kw) / 2); u.kids.forEach(function (c) { place(c, l); l += c.w + GX; }); var first = u.kids[0], lastK = u.kids[u.kids.length - 1]; cx = (first.cx + lastK.cx) / 2; }
      else cx = left + w / 2;
      u.cx = cx; u.left = cx - sw(u) / 2; u.m.forEach(function (n, i) { n.x = u.left + i * (W + CG); });
    }
    var cur = x0; order.forEach(function (r) { place(r, cur); cur += r.w + GX * 1.4; });
    // normalizza: sposta tutto a sinistra a PAD e calcola l'estensione
    var minX = 1e9, maxX = -1e9; nodes.forEach(function (n) { if (n.x < minX) minX = n.x; if (n.x + W > maxX) maxX = n.x + W; });
    nodes.forEach(function (n) { n.x += PAD + GUT - minX; });
    var gmax = 0; nodes.forEach(function (n) { n.y = TOP + n.gen * (H + RG); if (n.gen > gmax) gmax = n.gen; });
    return { units: units, unitOf: unitOf, width: maxX - minX + PAD * 2 + GUT, height: TOP + (gmax + 1) * H + gmax * RG + PAD + 8, gens: gmax + 1 };
  }

  /* ---------- 3) disegno ---------- */
  function lines(s) { // nome su una o due righe
    var t = s; if (t.length <= 9) return [t]; var w = t.split(/(?<=\/)|\s+/), best = 1, bd = 1e9; if (w.length < 2) return [t.length > 12 ? t.slice(0, 11) + '…' : t];
    for (var i = 1; i < w.length; i++) { var d = Math.abs(w.slice(0, i).join(' ').length - w.slice(i).join(' ').length); if (d < bd) { bd = d; best = i; } }
    return [w.slice(0, best).join(' '), w.slice(best).join(' ')];
  }
  function render(M, opts) {
    var L = layout(M), svg = se('svg', { 'class': 'ft-svg', viewBox: '0 0 ' + Math.ceil(L.width) + ' ' + Math.ceil(L.height), xmlns: NS, role: 'group', 'aria-label': opts && opts.label || 'Albero genealogico' });
    svg.setAttribute('data-vb', '0 0 ' + Math.ceil(L.width) + ' ' + Math.ceil(L.height));
    var gL = se('g', { 'class': 'ft-gen' }, svg), gE = se('g', { 'class': 'ft-edges' }, svg), gN = se('g', { 'class': 'ft-nodes' }, svg);
    for (var g = 0; g < L.gens; g++) { var y = TOP + g * (H + RG); var t = se('text', { x: 0, y: 0, 'class': 'ft-genl', transform: 'translate(11 ' + (y + H / 2) + ') rotate(-90)', 'text-anchor': 'middle' }, gL); t.textContent = 'GEN. ' + (g + 1); se('line', { x1: GUT - 4, x2: GUT - 4, y1: y - 4, y2: y + H + 4, 'class': 'ft-genline' }, gL); }
    var unitOf = L.unitOf, midY = function (n) { return n.y + H / 2; };
    // coppie
    M.marriages.concat(M.partners).forEach(function (e, idx) {
      var a = e[0].x < e[1].x ? e[0] : e[1], b = a === e[0] ? e[1] : e[0], isM = idx < M.marriages.length, y = midY(a), x1 = a.x + W, x2 = b.x;
      if (x2 - x1 < 4) return;
      if (isM) { se('line', { x1: x1, x2: x2, y1: y - 3, y2: y - 3, 'class': 'ft-e ft-marr' }, gE); se('line', { x1: x1, x2: x2, y1: y + 3, y2: y + 3, 'class': 'ft-e ft-marr' }, gE); }
      else se('line', { x1: x1, x2: x2, y1: y, y2: y, 'class': 'ft-e ft-partner' }, gE);
    });
    // genitori → figli: bus per unità
    var byChild = {}; M.parents.forEach(function (r) { (byChild[r.c.i] = byChild[r.c.i] || []).push(r); });
    L.units.forEach(function (u) {
      if (!u.kids.length) return;
      // punto di partenza: centro della coppia (se entrambi i membri sono genitori) o del singolo genitore
      var pm = u.m.filter(function (n) { return M.parents.some(function (r) { return r.p === n; }); }); if (!pm.length) pm = [u.m[0]];
      var sx = pm.length === 2 ? (pm[0].x + W + pm[1].x) / 2 : pm[0].x + W / 2, sy = pm.length === 2 ? midY(pm[0]) : pm[0].y + H, busY = u.m[0].y + H + RG / 2;
      var kids = []; u.kids.forEach(function (k) { k.m.forEach(function (n) { if (byChild[n.i] && byChild[n.i].some(function (r) { return u.m.indexOf(r.p) > -1; })) kids.push(n); }); });
      if (!kids.length) return;
      var xs = kids.map(function (n) { return n.x + W / 2; }).concat([sx]), mn = Math.min.apply(null, xs), mx = Math.max.apply(null, xs);
      se('line', { x1: sx, x2: sx, y1: sy, y2: busY, 'class': 'ft-e ft-par' }, gE);
      if (mx - mn > 1) se('line', { x1: mn, x2: mx, y1: busY, y2: busY, 'class': 'ft-e ft-par' }, gE);
      kids.forEach(function (n) {
        var adopt = byChild[n.i].some(function (r) { return r.adopt && u.m.indexOf(r.p) > -1; });
        se('line', { x1: n.x + W / 2, x2: n.x + W / 2, y1: busY, y2: n.y, 'class': 'ft-e ft-par' + (adopt ? ' ft-adopt' : '') }, gE);
      });
    });
    // fratelli: tratteggio puntinato tra le caselle adiacenti, arco sopra se non adiacenti
    M.sibs.forEach(function (s) {
      var a = s[0].x < s[1].x ? s[0] : s[1], b = a === s[0] ? s[1] : s[0];
      if (a.gen !== b.gen) return;
      var between = M.nodes.some(function (n) { return n.gen === a.gen && n !== a && n !== b && n.x > a.x && n.x < b.x; });
      if (!between && b.x - (a.x + W) >= 4) { var y = a.y + H - 9; se('line', { x1: a.x + W, x2: b.x, y1: y, y2: y, 'class': 'ft-e ft-sib' }, gE); }
      else { var x1 = a.x + W / 2, x2 = b.x + W / 2, y0 = a.y; se('path', { d: 'M' + x1 + ' ' + y0 + 'C' + x1 + ' ' + (y0 - 22) + ' ' + x2 + ' ' + (y0 - 22) + ' ' + x2 + ' ' + y0, 'class': 'ft-e ft-sib', fill: 'none' }, gE); }
    });
    // nodi
    M.nodes.forEach(function (n) {
      var linked = !!n.id, g = se('g', { 'class': 'ft-node' + (linked ? ' ft-link' : '') + (n.nonblood ? ' ft-nb' : ''), transform: 'translate(' + n.x + ' ' + n.y + ')', 'data-node': n.i }, gN);
      if (linked) { g.setAttribute('data-char', n.id); g.setAttribute('tabindex', '0'); g.setAttribute('role', 'button'); g.setAttribute('aria-label', 'Apri la scheda di ' + n.name); }
      se('rect', { width: W, height: H, rx: 12, 'class': 'ft-box' }, g);
      var ls = lines(n.short || n.name), fy = ls.length === 1 ? 26 : 20;
      var tn = se('text', { x: W / 2, y: fy, 'text-anchor': 'middle', 'class': 'ft-name' }, g); ls.forEach(function (l, k) { var ts = se('tspan', { x: W / 2, dy: k ? '1.12em' : '0' }, tn); ts.textContent = l; });
      var r = (n.role || '').length > 19 ? n.role.slice(0, 18) + '…' : n.role;
      var tr = se('text', { x: W / 2, y: H - 9, 'text-anchor': 'middle', 'class': 'ft-role' }, g); tr.textContent = r;
      var ti = se('title', null, g); ti.textContent = n.name + (n.role ? ' — ' + n.role : '') + (n.rel ? ' · ' + n.rel : '');
    });
    return { svg: svg, layout: L };
  }
  window.tvaFamTree = { parse: parse, layout: layout, render: render, size: { W: W, H: H } };
})();
