  /* ---------- COMPOSIZIONI (3.2.2) ---------- */
  var SIZE = { wide: [1000, 630], compact: [560, 400], vertical: [720, 1200] };
  var LEG_FRAME = 'cornice-nexus-supremo', LEG_THEME = 'tema-fine-del-tempo', LEG_TITLE = 'titolo-colui-che-rimane', LEG_FX = 'effetto-aura-leggendaria';
  function bar(x, y, w, h, p, col) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + h / 2 + '" fill="rgba(0,0,0,.4)" stroke="#fff" stroke-opacity=".12"/><rect x="' + x + '" y="' + y + '" width="' + n1(Math.max(h, w * p)) + '" height="' + h + '" rx="' + h / 2 + '" fill="' + col + '"/><rect x="' + x + '" y="' + y + '" width="' + n1(Math.max(h, w * p)) + '" height="' + n1(h * 0.4) + '" rx="' + h / 4 + '" fill="#fff" fill-opacity=".28"/>'; }
  /* a capo per parole: nessun testo troncato finche' entra in maxLines; solo l'ultima riga puo' avere l'ellissi */
  function wrap(text, weight, family, size, maxW, maxLines) {
    var words = String(text).split(/\s+/), lines = [], cur = '', i, f = weight + ' ' + size + 'px ' + family;
    for (i = 0; i < words.length; i++) {
      var t = cur ? cur + ' ' + words[i] : words[i];
      if (measure(t, f) <= maxW || !cur) cur = t; else { lines.push(cur); cur = words[i]; }
    }
    if (cur) lines.push(cur);
    if (lines.length > maxLines) { var rest = lines.slice(maxLines - 1).join(' '); lines = lines.slice(0, maxLines - 1); lines.push(clip(rest, weight, '', family, size, maxW)); }
    return lines.map(function (l) { return measure(l, f) > maxW ? clip(l, weight, '', family, size, maxW) : l; });
  }
  function codeBars(x, y, w, h, seedStr, col, op) {
    var r = rng(seedStr.split('').reduce(function (a, c) { return (a * 31 + c.charCodeAt(0)) >>> 0; }, 7)), s = '', cx = x, k;
    while (cx < x + w - 3) { k = 1 + Math.floor(r() * 3) * 1.4; s += '<rect x="' + n1(cx) + '" y="' + y + '" width="' + n1(k) + '" height="' + h + '"/>'; cx += k + 1.2 + r() * 2.6; }
    return '<g fill="' + col + '" fill-opacity="' + (op || 0.55) + '">' + s + '</g>';
  }
  /* pannello dati: ogni tema ha un proprio trattamento (materiale, bordo, sagoma) */
  function pan(x, y, w, h, th, u, r) {
    r = r === undefined ? 12 : r; var bg = th.bg, a = th.acc, k = th.pn, sh = '<rect x="' + x + '" y="' + (y + 4) + '" width="' + w + '" height="' + h + '" rx="' + r + '" fill="#000" fill-opacity=".28"/>', s = '', x2 = x + w, y2 = y + h, i;
    var fill = function (c, o, rr) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + (rr === undefined ? r : rr) + '" fill="' + c + '" fill-opacity="' + o + '"/>'; };
    var line = function (d, c, wd, o, ex) { return '<path d="' + d + '" fill="none" stroke="' + c + '" stroke-width="' + wd + '" stroke-opacity="' + o + '"' + (ex || '') + '/>'; };
    var gl = '<defs>' + lg(u + 'pg', [[0, '#fff', 0.1], [0.5, '#fff', 0.02], [1, '#000', 0.18]], 0, 0, 0.3, 1) + '</defs>';
    if (k === 'paper') {
      s = fill(mix(bg, '#000000', 0.5), 0.5) + fill('#efe4c9', 0.06) + '<rect x="' + (x + 6) + '" y="' + (y + 6) + '" width="' + (w - 12) + '" height="' + (h - 12) + '" rx="' + Math.max(2, r - 5) + '" fill="none" stroke="' + a + '" stroke-opacity=".5"/>' + line('M' + (x + 14) + ' ' + (y + 1.5) + 'H' + (x2 - 14), a, 2, 0.8);
    } else if (k === 'steel') {
      s = fill(mix(bg, '#000000', 0.55), 0.62) + line('M' + x + ' ' + (y + 22) + 'H' + x2, a, 1, 0.35) + line('M' + (x + 10) + ' ' + (y + 11) + 'h26M' + (x2 - 36) + ' ' + (y + 11) + 'h26', a, 2, 0.5) + '<path d="M' + x + ' ' + (y + 14) + 'V' + y + 'H' + (x + 14) + 'M' + (x2 - 14) + ' ' + y + 'H' + x2 + 'V' + (y + 14) + 'M' + x2 + ' ' + (y2 - 14) + 'V' + y2 + 'H' + (x2 - 14) + 'M' + (x + 14) + ' ' + y2 + 'H' + x + 'V' + (y2 - 14) + '" fill="none" stroke="' + th.accT + '" stroke-width="2"/>';
    } else if (k === 'brass') {
      s = '<defs>' + lg(u + 'pb', [[0, a, 0.2], [0.5, a, 0.07], [1, '#000', 0.25]], 0, 0, 1, 1) + '</defs>' + fill(mix(bg, '#000000', 0.4), 0.55) + fill('url(#' + u + 'pb)', 1) + '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + r + '" fill="none" stroke="' + a + '" stroke-opacity=".55" stroke-width="1.6"/>';
      [[x + 9, y + 9], [x2 - 9, y + 9], [x + 9, y2 - 9], [x2 - 9, y2 - 9]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="3" fill="' + a + '" fill-opacity=".8" stroke="#000" stroke-opacity=".5"/>'; });
    } else if (k === 'cracked') {
      s = fill(mix(bg, '#000000', 0.55), 0.66) + line('M' + (x2 - 70) + ' ' + y + 'L' + (x2 - 52) + ' ' + (y + 16) + 'L' + (x2 - 60) + ' ' + (y + 26) + 'L' + (x2 - 36) + ' ' + (y + 44), '#ff5a74', 1.6, 0.85) + line('M' + x + ' ' + (y2 - 30) + 'L' + (x + 18) + ' ' + (y2 - 20) + 'L' + (x + 12) + ' ' + (y2 - 8) + 'L' + (x + 30) + ' ' + y2, '#ff5a74', 1.4, 0.7) + '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + r + '" fill="none" stroke="#D82C48" stroke-opacity=".5" stroke-width="1.4"/>';
    } else if (k === 'hud') {
      s = fill(mix(bg, '#000000', 0.45), 0.62) + fill('#24B4C5', 0.05, 2) + '<path d="M' + x + ' ' + (y + 20) + 'V' + y + 'H' + (x + 20) + 'M' + (x2 - 20) + ' ' + y + 'H' + x2 + 'V' + (y + 20) + 'M' + x2 + ' ' + (y2 - 20) + 'V' + y2 + 'H' + (x2 - 20) + 'M' + (x + 20) + ' ' + y2 + 'H' + x + 'V' + (y2 - 20) + '" fill="none" stroke="' + th.accT + '" stroke-width="2"/>';
      for (i = 0; i < 12; i++) s += '<path d="M' + (x + 40 + i * 7) + ' ' + (y + 5) + 'v' + (i % 4 ? 3 : 6) + '" stroke="' + a + '" stroke-opacity=".6"/>';
      s += line('M' + (x + 30) + ' ' + y2 + 'H' + (x2 - 30), a, 1, 0.4);
    } else if (k === 'indus') {
      var c = Math.min(26, h * 0.12), pts = [[x + c, y], [x2, y], [x2, y2 - c], [x2 - c, y2], [x, y2], [x, y + c]];
      s = poly(pts, mix(bg, '#000000', 0.5), '#c9bdff', 1.2, ' fill-opacity=".66" stroke-opacity=".45"') + '<path d="M' + (x + c) + ' ' + (y + 5) + 'H' + (x2 - 10) + '" stroke="' + a + '" stroke-width="3" stroke-opacity=".7"/><path d="M' + (x + 8) + ' ' + (y2 - 5) + 'h' + (w * 0.3) + '" stroke="#c9bdff" stroke-width="1.4" stroke-opacity=".5" stroke-dasharray="6 4"/>';
    } else if (k === 'sigil') {
      s = fill(mix(bg, '#000000', 0.4), 0.55, r + 8) + '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + (r + 8) + '" fill="none" stroke="' + a + '" stroke-opacity=".7" stroke-width="1.4"/><rect x="' + (x + 6) + '" y="' + (y + 6) + '" width="' + (w - 12) + '" height="' + (h - 12) + '" rx="' + (r + 3) + '" fill="none" stroke="#EBC8FF" stroke-opacity=".25" stroke-dasharray="2 5"/>';
      [[x + w / 2, y], [x + w / 2, y2], [x, y + h / 2], [x2, y + h / 2]].forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="4.4" fill="' + bg + '" stroke="' + th.accT + '" stroke-width="1.4"/>'; });
    } else if (k === 'void') {
      var cc = Math.min(34, h * 0.16);
      s = poly([[x, y], [x2 - cc, y], [x2, y + cc], [x2, y2], [x + cc, y2], [x, y2 - cc]], '#000', '#9a96a8', 1, ' fill-opacity=".66" stroke-opacity=".34" stroke-dasharray="14 7"') + '<path d="M' + (x2 - cc + 6) + ' ' + (y + 2) + 'L' + (x2 - 4) + ' ' + (y + cc - 6) + '" stroke="#9a96a8" stroke-opacity=".4" transform="translate(5 5)"/>';
    } else if (k === 'cosmic') {
      s = '<defs>' + lg(u + 'pc', [[0, '#477BEB', 0.18], [1, '#7a3fc0', 0.14]], 0, 0, 1, 1) + '</defs>' + fill(mix(bg, '#000000', 0.45), 0.6) + fill('url(#' + u + 'pc)', 1) + '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + r + '" fill="none" stroke="#8fb0ff" stroke-opacity=".5"/><path d="M' + (x2 - 70) + ' ' + y + 'A70 70 0 0 1 ' + x2 + ' ' + (y + 70) + '" fill="none" stroke="#d8b5ff" stroke-opacity=".6" stroke-width="1.4"/>' + stars(w, h, 12, 4, '#fff', 1).replace(/<circle cx="([\d.]+)" cy="([\d.]+)"/g, function (m0, cx, cy) { return '<circle cx="' + n1(+cx + x) + '" cy="' + n1(+cy + y) + '"'; });
    } else {   // monument (Fine del Tempo): marmo pallido, architrave e fusti
      s = fill(mix(bg, '#000000', 0.35), 0.56) + fill('#fff2b8', 0.07, 2) + '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="6" fill="' + a + '" fill-opacity=".55"/><rect x="' + (x - 3) + '" y="' + (y - 2) + '" width="' + (w + 6) + '" height="3" fill="' + a + '" fill-opacity=".7"/><rect x="' + x + '" y="' + (y2 - 4) + '" width="' + w + '" height="4" fill="' + a + '" fill-opacity=".45"/>';
      for (i = 0; i < 3; i++) s += '<path d="M' + (x + 7 + i * 4) + ' ' + (y + 10) + 'V' + (y2 - 8) + 'M' + (x2 - 7 - i * 4) + ' ' + (y + 10) + 'V' + (y2 - 8) + '" stroke="' + a + '" stroke-opacity=".18"/>';
    }
    return gl + sh + s + '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + r + '" fill="url(#' + u + 'pg)"/>';
  }
  /* ritratto a strati: sfondo del tema, fascio di luce, avatar, vignettatura, riflesso, bordo metallico */
  function portrait(m, x, y, w, h, shape, u, th, o) {
    o = o || {}; var cx = x + w / 2, a = th.acc, id = u + 'pt', clipEl, bord, s = '';
    var arch = function (xx, yy, ww, hh, inset) { var r = ww / 2 - inset; return 'M' + (xx + inset) + ' ' + (yy + hh - inset) + 'V' + (yy + r + inset) + 'A' + r + ' ' + r + ' 0 0 1 ' + (xx + ww - inset) + ' ' + (yy + r + inset) + 'V' + (yy + hh - inset) + 'Z'; };
    if (shape === 'arch') clipEl = '<path d="' + arch(x, y, w, h, 0) + '"/>'; else clipEl = '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="8"/>';
    s += '<defs><clipPath id="' + id + '">' + clipEl + '</clipPath>' + rg(u + 'pv', 0.5, 0.42, 0.75, '#000', 0, 0.62) + rg(u + 'pb', 0.5, 0.3, 0.6, mix(a, '#ffffff', 0.35), 0.5, 0) + lg(u + 'pr', [[0, '#fff', 0.18], [0.45, '#fff', 0], [1, '#fff', 0]], 0, 0, 1, 1) + lg(u + 'pf', [[0, '#000', 0], [1, mix(th.bg, '#000000', 0.5), 0.92]], 0, 0, 0, 1) + '</defs>';
    s += '<g transform="translate(0 ' + (o.sh === 0 ? 0 : 6) + ')" opacity=".35"><path d="' + (shape === 'arch' ? arch(x, y, w, h, 0) : 'M' + x + ' ' + y + 'h' + w + 'v' + h + 'h' + (-w) + 'Z') + '" fill="#000"/></g>';
    s += '<g clip-path="url(#' + id + ')"><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="' + mix(th.bg, a, 0.14) + '"/><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#' + u + 'pb)"/>';
    if (o.rays) { var i, rays = ''; for (i = -5; i <= 5; i++) rays += '<path d="M' + cx + ' ' + (y + h * 0.3) + 'L' + n1(cx + i * w * 0.22 - w * 0.03) + ' ' + y + 'H' + n1(cx + i * w * 0.22 + w * 0.03) + 'Z"/>'; s += '<g fill="' + mix(a, '#ffffff', 0.4) + '" fill-opacity="' + (o.leg ? 0.16 : 0.07) + '">' + rays + '</g>'; }
    s += avatarPiece(m, x, y, w, h, shape === 'arch' ? 'rect' : 'rect', u + 'q').replace(/rx="10"/, 'rx="0"');
    s += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#' + u + 'pv)"/>';
    if (o.fade) s += '<rect x="' + x + '" y="' + (y + h * 0.62) + '" width="' + w + '" height="' + n1(h * 0.38) + '" fill="url(#' + u + 'pf)"/>';
    s += '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#' + u + 'pr)"/></g>';
    var path = shape === 'arch' ? arch(x, y, w, h, 0) : 'M' + (x + 4) + ' ' + y + 'H' + (x + w - 4) + 'Q' + (x + w) + ' ' + y + ' ' + (x + w) + ' ' + (y + 4) + 'V' + (y + h - 4) + 'Q' + (x + w) + ' ' + (y + h) + ' ' + (x + w - 4) + ' ' + (y + h) + 'H' + (x + 4) + 'Q' + x + ' ' + (y + h) + ' ' + x + ' ' + (y + h - 4) + 'V' + (y + 4) + 'Q' + x + ' ' + y + ' ' + (x + 4) + ' ' + y + 'Z';
    s += '<defs>' + lg(u + 'pm', [[0, mix(a, '#ffffff', 0.55)], [0.5, a], [1, mix(a, '#000000', 0.55)]], 0, 0, 1, 1) + '</defs><path d="' + path + '" fill="none" stroke="url(#' + u + 'pm)" stroke-width="' + (o.bw || 4) + '"/>';
    if (shape === 'arch') s += '<path d="' + arch(x, y, w, h, 9) + '" fill="none" stroke="' + a + '" stroke-opacity=".5" stroke-width="1.4"/>' + (o.leg ? '<path d="' + arch(x, y, w, h, 17) + '" fill="none" stroke="' + mix(a, '#ffffff', 0.5) + '" stroke-opacity=".6" stroke-width="1"/><path d="M' + (cx - 20) + ' ' + y + 'L' + cx + ' ' + (y - 16) + 'L' + (cx + 20) + ' ' + y + 'Z" fill="#12070a" stroke="' + mix(a, '#ffffff', 0.5) + '" stroke-width="2"/><circle cx="' + cx + '" cy="' + (y - 5) + '" r="4" fill="#d4283f"/>' : '');
    else s += '<path d="M' + (x + 8) + ' ' + (y + 8) + 'h14M' + (x + 8) + ' ' + (y + 8) + 'v14M' + (x + w - 8) + ' ' + (y + h - 8) + 'h-14M' + (x + w - 8) + ' ' + (y + h - 8) + 'v-14" fill="none" stroke="' + mix(a, '#ffffff', 0.4) + '" stroke-opacity=".7" stroke-width="1.6"/>';
    return s;
  }
  function holo(cx, cy, r, u, a) {
    return '<defs>' + lg(u + 'ho', [[0, '#7fe8f0', 0.6], [0.35, '#d8a0ff', 0.55], [0.7, '#ffd890', 0.6], [1, '#7fe8f0', 0.5]], 0, 0, 1, 1) + '</defs><circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="url(#' + u + 'ho)"/><circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="' + a + '" stroke-opacity=".7" stroke-width="1.4"/><circle cx="' + cx + '" cy="' + cy + '" r="' + n1(r * 0.72) + '" fill="none" stroke="#fff" stroke-opacity=".4" stroke-dasharray="2 3"/>' + emblem(cx, cy, r * 0.5, '#fff', 1.4).replace('<g ', '<g stroke-opacity=".75" ');
  }
  function laurel(cx, y, side, col) {
    var s = '', i; for (i = 0; i < 4; i++) s += '<path d="M' + (cx + side * i * 8) + ' ' + (y - i * 2.4) + 'q' + (side * 9) + ' -8 ' + (side * 17) + ' -3q' + (side * -8) + ' 7 ' + (side * -17) + ' 3Z" fill="' + col + '" fill-opacity=".85"/>'; return s;
  }
  function build(m, layout, o) {
    o = o || {}; var sz = SIZE[layout], Wd = sz[0], Ht = sz[1], u = (o.uid || 'tc') + '_', th = THEMES[m.theme] || THEMES['tema-tva-classico'], fr = FRAMES[m.frame] || FRAMES['cornice-standard-tva'];
    var p = m.xpNeed > 0 ? Math.max(0, Math.min(1, m.xpCur / m.xpNeed)) : 0, g = '', a, nm = m.name || 'Variante', fxId = m.fx;
    var inkO = th.ink, sub = th.sub, acc = th.acc, accT = th.accT, legF = m.frame === LEG_FRAME, legT = m.theme === LEG_THEME, legTi = m.titleId === LEG_TITLE, leg = legF || legT;
    CUR_LT = th.lt;
    var med = function (b, cx, cy, r) { return medal(b.id, cx, cy, r, acc); };
    if (layout === 'wide') {
      a = { cx: 205, cy: 325, r: 120 };
      g += th.draw(Wd, Ht, u);
      if (fxId && FX[fxId]) g += FX[fxId](Wd, Ht, a, u);
      g += pan(352, 150, 598, 448, th, u, 14);
      g += emblem(96, 98, 26, acc, 2.2) + T(136, 96, 'TIME VARIANCE AUTHORITY', { size: 24, fill: inkO, mono: 1, ls: 3, weight: 700 }) + T(136, 122, 'ARCHIVI TEMPORALI · CARTA D’IDENTITÀ DELL’AGENTE', { size: 14, fill: sub, mono: 1, ls: 1.5 });
      g += holo(884, 94, 30, u, acc) + codeBars(640, 80, 190, 30, m.id, acc, 0.4);
      g += '<path d="M70 140H930" stroke="' + acc + '" stroke-opacity=".5"/><path d="M70 143H930" stroke="' + acc + '" stroke-opacity=".18"/>';
      g += portrait(m, 70, 160, 270, 330, 'rect', u, th, { leg: leg, bw: 4 });
      var nw = 558, fs = fit(nm, 700, '', SERIF, nw, 84, 30), nmW = clip(nm, 700, '', SERIF, fs, nw);
      g += T(372, 186, 'AGENTE', { size: 16, fill: accT, mono: 1, ls: 4 }) + T(372, 186 + fs * 0.95, nmW, { size: fs, weight: 700, fill: inkO });
      var ty = 186 + fs * 0.95 + 38, tsz = fit(m.title, 400, 'italic', SERIF, nw - (legTi ? 70 : 0), 30, 22);
      g += T(372 + (legTi ? 36 : 0), ty, clip(m.title, 400, 'italic', SERIF, tsz, nw - (legTi ? 70 : 0)), { size: tsz, italic: 1, fill: inkO, op: 0.88 }) + (legTi ? '<g transform="translate(372 ' + (ty - 8) + ')">' + laurel(0, 0, 1, mix(acc, '#ffffff', 0.4)) + '</g>' : '');
      g += T(372, ty + 44, 'VARIANT ID', { size: 14, fill: sub, mono: 1, ls: 3 }) + '<rect x="368" y="' + (ty + 50) + '" width="226" height="40" rx="5" fill="#000" fill-opacity=".35" stroke="' + acc + '" stroke-opacity=".55"/>' + T(380, ty + 80, m.id, { size: 28, fill: accT, mono: 1, weight: 700, ls: 3 });
      var by = 428;
      g += T(372, by, 'LV ' + m.level, { size: 40, fill: inkO, weight: 700 }) + T(930, by - 2, m.xp + ' XP', { size: 24, fill: inkO, mono: 1, anchor: 'end' });
      g += bar(372, by + 14, 558, 10, p, th.bar) + T(372, by + 46, m.xpCur + ' / ' + m.xpNeed + ' XP AL LIVELLO ' + (m.level + 1), { size: 16, fill: sub, mono: 1, ls: 1 });
      m.badges.slice(0, 3).forEach(function (b, i) { g += med(b, 404 + i * 90, 534, 32); });
      if (!m.badges.length) g += T(372, 540, 'NESSUN DISTINTIVO ANCORA', { size: 15, fill: sub, mono: 1, ls: 2 });
      g += T(930, 548, 'AUTORIZZATO · TVA', { size: 14, fill: sub, mono: 1, anchor: 'end', ls: 2 }) + codeBars(740, 556, 190, 16, m.id + 'b', acc, 0.4);
    } else if (layout === 'compact') {
      a = { cx: 108, cy: 184, r: 76 };
      g += th.draw(Wd, Ht, u);
      if (fxId && FX[fxId]) g += FX[fxId](Wd, Ht, a, u);
      g += pan(194, 92, 346, 262, th, u, 10);
      g += emblem(58, 56, 18, acc, 2) + T(86, 62, 'TIME VARIANCE AUTHORITY', { size: 20, fill: inkO, mono: 1, ls: 1.2, weight: 700 });
      g += '<path d="M36 82H524" stroke="' + acc + '" stroke-opacity=".5"/>';
      g += portrait(m, 36, 96, 146, 176, 'rect', u, th, { leg: leg, bw: 3, sh: 1 });
      var nw2 = 318, fs2 = fit(nm, 700, '', SERIF, nw2, 46, 24), nmW2 = clip(nm, 700, '', SERIF, fs2, nw2);
      g += T(204, 114, 'AGENTE', { size: 20, fill: accT, mono: 1, ls: 3 }) + T(204, 114 + fs2 * 0.95, nmW2, { size: fs2, weight: 700, fill: inkO });
      var ty2 = 114 + fs2 * 0.95 + 28, tsz2 = fit(m.title, 400, 'italic', SERIF, nw2, 24, 20);
      g += T(204, ty2, clip(m.title, 400, 'italic', SERIF, tsz2, nw2), { size: tsz2, italic: 1, fill: inkO, op: 0.88 });
      g += T(204, ty2 + 32, m.id, { size: 24, fill: accT, mono: 1, weight: 700, ls: 2 });
      g += T(204, 262, 'LV ' + m.level, { size: 30, fill: inkO, weight: 700 }) + T(524, 260, m.xp + ' XP', { size: 21, fill: inkO, mono: 1, anchor: 'end' });
      g += bar(204, 270, 320, 8, p, th.bar);
      g += T(204, 298, m.xpCur + ' / ' + m.xpNeed, { size: 20, fill: sub, mono: 1 });
      m.badges.slice(0, 3).forEach(function (b, i) { g += med(b, 66 + i * 64, 332, 25); });
      if (!m.badges.length) g += T(36, 338, 'NESSUN DISTINTIVO', { size: 20, fill: sub, mono: 1, ls: 1 });
    } else {   // vertical: carta da collezione, composizione autonoma (arco ritratto, targa nome, pannello progressione)
      a = { cx: 360, cy: 400, r: 170 };
      g += th.draw(Wd, Ht, u);
      // stelo decorativo e dettagli narrativi in testata
      g += '<g stroke="' + acc + '" stroke-opacity=".5" fill="none"><path d="M80 98H300M420 98H640"/><path d="M80 98l8-6v12zM640 98l-8-6v12z" fill="' + acc + '" fill-opacity=".5" stroke="none"/><path d="M110 108H290M430 108H610" stroke-opacity=".2"/></g>';
      g += emblem(360, 92, 34, acc, 2.8) + holo(124, 150, 0.01, u, acc).replace(/.*/, '');
      g += T(360, 168, 'TIME VARIANCE AUTHORITY', { size: 28, fill: inkO, mono: 1, ls: 4, weight: 700, anchor: 'middle' }) + T(360, 196, 'ARCHIVI TEMPORALI · SEZIONE VARIANTI', { size: 20, fill: sub, mono: 1, ls: 2, anchor: 'middle' });
      if (fxId && FX[fxId]) g += FX[fxId](Wd, Ht, { cx: 360, cy: 420, r: 200 }, u);
      g += portrait(m, 140, 222, 440, 420, 'arch', u, th, { leg: leg, rays: 1, fade: 1, bw: 6 });
      // targa identita': nome, titolo, Variant ID
      var nw3 = 560, fs3 = fit(nm, 700, '', SERIF, nw3, 84, 36), nmW3 = clip(nm, 700, '', SERIF, fs3, nw3), nby = 700;
      g += T(360, nby, nmW3, { size: fs3, weight: 700, fill: inkO, anchor: 'middle' });
      var tw = legTi ? 500 : 560, tsz3 = fit(m.title, 400, 'italic', SERIF, tw, 34, 24);
      g += T(360, nby + 44, clip(m.title, 400, 'italic', SERIF, tsz3, tw), { size: tsz3, italic: 1, fill: inkO, op: 0.9, anchor: 'middle' });
      if (legTi) { var tl = measure(clip(m.title, 400, 'italic', SERIF, tsz3, tw), 'italic 400 ' + tsz3 + 'px ' + SERIF) / 2 + 14; g += '<g transform="translate(' + (360 - tl) + ' ' + (nby + 38) + ')">' + laurel(0, 0, -1, mix(acc, '#ffffff', 0.4)) + '</g><g transform="translate(' + (360 + tl) + ' ' + (nby + 38) + ')">' + laurel(0, 0, 1, mix(acc, '#ffffff', 0.4)) + '</g>'; }
      g += '<rect x="170" y="' + (nby + 62) + '" width="380" height="48" rx="8" fill="#000" fill-opacity=".4" stroke="' + acc + '" stroke-opacity=".6"/>' + T(188, nby + 94, 'VARIANT ID', { size: 20, fill: sub, mono: 1, ls: 1 }) + T(532, nby + 95, m.id, { size: 31, fill: accT, mono: 1, weight: 700, ls: 2, anchor: 'end' });
      // progressione
      var py = 828;
      g += pan(70, py, 580, 258, th, u, 16);
      g += T(98, py + 66, 'LV ' + m.level, { size: 60, fill: inkO, weight: 700 }) + T(622, py + 58, m.xp + ' XP', { size: 32, fill: inkO, mono: 1, anchor: 'end' });
      g += bar(98, py + 80, 524, 14, p, th.bar) + T(98, py + 120, m.xpCur + ' / ' + m.xpNeed + ' XP AL LIVELLO ' + (m.level + 1), { size: 22, fill: sub, mono: 1 });
      g += '<path d="M98 ' + (py + 136) + 'H622" stroke="' + acc + '" stroke-opacity=".3"/>';
      m.badges.slice(0, 3).forEach(function (b, i) {
        var bx = 168 + i * 192, lines = wrap(b.name, 400, SERIF, 22, 176, 3);
        g += med(b, bx, py + 176, 30) + lines.map(function (l, k) { return T(bx, py + 226 + k * 25, l, { size: 22, fill: sub, anchor: 'middle' }); }).join('');
      });
      if (!m.badges.length) g += T(360, py + 192, 'NESSUN DISTINTIVO ANCORA', { size: 22, fill: sub, mono: 1, ls: 2, anchor: 'middle' });
      // autenticazione e firma
      g += codeBars(150, 1104, 420, 20, m.id, acc, 0.5) + T(360, 1150, 'TVA ARCHIVES', { size: 22, fill: sub, mono: 1, ls: 8, anchor: 'middle', weight: 700 });
    }
    var fs_ = Wd / 560;   // le cornici sono disegnate su una base di 560 unita' e scalate: stesso peso visivo in tutte le composizioni
    g += '<g transform="scale(' + n1(fs_ * 1000) / 1000 + ')">' + fr(Wd / fs_, Ht / fs_, u) + '</g>';
    var aria = 'Tessera TVA. Agente ' + nm + ', ' + m.id + '. Titolo: ' + m.title + '. Livello ' + m.level + ', ' + m.xp + ' XP.';
    return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ' + Wd + ' ' + Ht + '" width="' + Wd + '" height="' + Ht + '" role="img" aria-label="' + esc(aria) + '" class="tc-svg tc-' + layout + '" data-layout="' + layout + '">' + g + '</svg>';
  }
