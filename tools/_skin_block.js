  /* ---------- colore: miscela e contrasto (WCAG) ---------- */
  function hex2(c) { c = c.replace('#', ''); if (c.length === 3) c = c[0] + c[0] + c[1] + c[1] + c[2] + c[2]; return [parseInt(c.substr(0, 2), 16), parseInt(c.substr(2, 2), 16), parseInt(c.substr(4, 2), 16)]; }
  function rgb2(a) { return '#' + a.map(function (v) { v = Math.max(0, Math.min(255, Math.round(v))); return (v < 16 ? '0' : '') + v.toString(16); }).join(''); }
  function mix(a, b, t) { var x = hex2(a), y = hex2(b); return rgb2([x[0] + (y[0] - x[0]) * t, x[1] + (y[1] - x[1]) * t, x[2] + (y[2] - x[2]) * t]); }
  function lum(c) { var v = hex2(c).map(function (q) { q /= 255; return q <= 0.03928 ? q / 12.92 : Math.pow((q + 0.055) / 1.055, 2.4); }); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; }
  function contrast(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function ensure(c, bg, min) { var t = 0, o = c; while (contrast(o, bg) < min && t < 1) { t += 0.05; o = mix(c, '#ffffff', t); } return o; }
  function lg(id, stops, x1, y1, x2, y2) { return '<linearGradient id="' + id + '" x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '">' + stops.map(function (s) { return '<stop offset="' + s[0] + '" stop-color="' + s[1] + '"' + (s[2] !== undefined ? ' stop-opacity="' + s[2] + '"' : '') + '/>'; }).join('') + '</linearGradient>'; }
  function rg(id, cx, cy, r, c, o0, o1) { return '<radialGradient id="' + id + '" cx="' + cx + '" cy="' + cy + '" r="' + r + '"><stop offset="0" stop-color="' + c + '" stop-opacity="' + o0 + '"/><stop offset="1" stop-color="' + c + '" stop-opacity="' + (o1 || 0) + '"/></radialGradient>'; }
  function grad(id, a, b, ang) { var x2 = ang === 'v' ? 0 : 1; return lg(id, [[0, a], [1, b]], 0, 0, x2, 1); }
  function stars(W_, H_, n, seed, col, rmax) { var r = rng(seed), s = '', i; for (i = 0; i < n; i++) s += '<circle cx="' + n1(r() * W_) + '" cy="' + n1(r() * H_) + '" r="' + n1(0.6 + r() * rmax) + '" fill="' + col + '" opacity="' + n1(0.25 + r() * 0.55) + '"/>'; return s; }

  /* ---------- CORNICI (12): ognuna con propria silhouette, materiale, bordo e angoli ----------
     Le funzioni disegnano su una base virtuale larga 560 (poi scalata). Regole di contrasto: ogni cornice ha un sottofondo scuro
     (plate) e un filo chiaro sul bordo, quindi resta visibile su qualunque tema; i colori della cornice NON dipendono dal tema.
     Tutto il disegno sta entro 36 unita' dal bordo (le composizioni lasciano libera quella fascia). */
  function corners(W_, H_, m, fn) { var s = '', i, c = [[1, 1], [-1, 1], [1, -1], [-1, -1]]; for (i = 0; i < 4; i++) s += '<g transform="translate(' + (c[i][0] > 0 ? m : W_ - m) + ' ' + (c[i][1] > 0 ? m : H_ - m) + ') scale(' + c[i][0] + ' ' + c[i][1] + ')">' + fn(i) + '</g>'; return s; }
  function rr(W_, H_, m, sw, stroke, rx, extra) { return '<rect x="' + m + '" y="' + m + '" width="' + n1(W_ - 2 * m) + '" height="' + n1(H_ - 2 * m) + '" rx="' + (rx || 0) + '" fill="none" stroke="' + stroke + '" stroke-width="' + sw + '"' + (extra || '') + '/>'; }
  function poly(pts, fill, stroke, sw, extra) { return '<polygon points="' + pts.map(function (p) { return n1(p[0]) + ',' + n1(p[1]); }).join(' ') + '" fill="' + (fill || 'none') + '"' + (stroke ? ' stroke="' + stroke + '" stroke-width="' + sw + '" stroke-linejoin="miter"' : '') + (extra || '') + '/>'; }
  function cham(W_, H_, m, c) { return [[m + c, m], [W_ - m - c, m], [W_ - m, m + c], [W_ - m, H_ - m - c], [W_ - m - c, H_ - m], [m + c, H_ - m], [m, H_ - m - c], [m, m + c]]; }
  function pth(d, stroke, sw, extra) { return '<path d="' + d + '" fill="none" stroke="' + stroke + '" stroke-width="' + sw + '"' + (extra || '') + '/>'; }
  function edgeRun(W_, H_, m, step, fn, skip) { var s = '', x, y; skip = skip || 34; for (x = skip; x <= W_ - skip + 0.1; x += step) { s += fn(x, m, 0, 0, x) + fn(x, H_ - m, 0, 1, x); } for (y = skip; y <= H_ - skip + 0.1; y += step) { s += fn(m, y, 1, 0, y) + fn(W_ - m, y, 1, 1, y); } return s; }
  function plate(W_, H_, m, t, op, rx) { return rr(W_, H_, m, t, '#000', rx || 0, ' stroke-opacity="' + op + '"'); }
  function gear(cx, cy, r, n, fill, stroke) { var p = [], i; for (i = 0; i < n * 2; i++) { var a = Math.PI / n * i, rad = i % 2 ? r * 0.78 : r; p.push([cx + Math.cos(a) * rad, cy + Math.sin(a) * rad]); } return poly(p, fill, stroke, 1) + '<circle cx="' + cx + '" cy="' + cy + '" r="' + n1(r * 0.3) + '" fill="#2a1608"/>'; }
  var FRAMES = {
    /* 01 - istituzionale minimale: filo d'oro sottile, angoli puliti, nessuna decorazione */
    'cornice-standard-tva': function (W_, H_, u) {
      var g = '#D2B184';
      return plate(W_, H_, 14, 7, 0.35, 7) + rr(W_, H_, 14, 1.8, g, 7) + corners(W_, H_, 14, function () { return '<path d="M0 22V7a7 7 0 0 1 7-7H22" fill="none" stroke="' + g + '" stroke-width="3.6"/>'; });
    },
    /* 02 - bronzo satinato: sagoma smussata, bordo massiccio, piastre angolari con viti, ingranaggi */
    'cornice-bronzo-temporale': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'br', [[0, '#e2a566'], [0.5, '#a86a2c'], [1, '#6b3f17']], 0, 0, 1, 1) + '</defs>', hi = '#f0c28a', s = d;
      s += poly(cham(W_, H_, 16, 20), 'none', '#000', 17, ' stroke-opacity=".5"') + poly(cham(W_, H_, 16, 20), 'none', 'url(#' + u + 'br)', 12);
      s += poly(cham(W_, H_, 22.5, 16), 'none', hi, 0.9, ' stroke-opacity=".7"') + poly(cham(W_, H_, 9.5, 24), 'none', hi, 0.8, ' stroke-opacity=".45"');
      s += edgeRun(W_, H_, 16, 62, function (x, y) { return '<circle cx="' + n1(x) + '" cy="' + n1(y) + '" r="2.3" fill="' + hi + '" stroke="#3a2008" stroke-width=".8"/>'; }, 56);
      s += corners(W_, H_, 14, function () { return '<rect x="-4" y="-4" width="30" height="30" rx="2" fill="url(#' + u + 'br)" stroke="#2c1706" stroke-width="1.2"/><circle cx="5" cy="5" r="2" fill="#2c1706"/><circle cx="17" cy="5" r="2" fill="#2c1706"/><circle cx="5" cy="17" r="2" fill="#2c1706"/><circle cx="17" cy="17" r="2" fill="#2c1706"/>'; });
      return s + gear(W_ / 2, 16, 8, 8, hi, '#3a2008') + gear(W_ / 2, H_ - 16, 8, 8, hi, '#3a2008');
    },
    /* 03 - argento freddo: anelli concentrici, scala cronologica, quadranti agli angoli */
    'cornice-argento-cronologico': function (W_, H_, u) {
      var a = '#d3dde8', a2 = '#8a98aa', s = plate(W_, H_, 17, 22, 0.38, 20) + rr(W_, H_, 10, 1.6, a, 24) + rr(W_, H_, 17, 0.9, a2, 18) + rr(W_, H_, 25, 1.4, a, 12), i = 0;
      s += edgeRun(W_, H_, 13.5, 9, function (x, y, v, e, k) { var L = Math.round(k / 9) % 5 === 0 ? 6 : 3, d = e ? -1 : 1; return v ? pth('M' + n1(x) + ' ' + n1(y) + 'h' + (e ? -L : L), a, 0.9) : pth('M' + n1(x) + ' ' + n1(y) + 'v' + (e ? -L : L), a, 0.9); }, 38);
      s += corners(W_, H_, 0, function () { var t = '', k; for (k = 0; k < 12; k++) { var an = Math.PI / 6 * k; t += '<path d="M' + n1(18 + Math.cos(an) * 10) + ' ' + n1(18 + Math.sin(an) * 10) + 'L' + n1(18 + Math.cos(an) * 13) + ' ' + n1(18 + Math.sin(an) * 13) + '" stroke="' + a + '" stroke-width="1"/>'; } return '<circle cx="18" cy="18" r="14.5" fill="#0d1218" stroke="' + a + '" stroke-width="1.8"/>' + t + '<path d="M18 18V9M18 18L24 21" stroke="' + a + '" stroke-width="1.6" stroke-linecap="round"/><circle cx="18" cy="18" r="1.6" fill="' + a + '"/>'; });
      return s;
    },
    /* 04 - oro luminoso: doppio bordo, catena di losanghe, angoli a volute (filigrana) */
    'cornice-oro-archivista': function (W_, H_, u) {
      var g = 'url(#' + u + 'go)', d = '<defs>' + lg(u + 'go', [[0, '#fbe9ae'], [0.5, '#d9ad4e'], [1, '#98702a']], 0, 0, 1, 1) + '</defs>', s = d + plate(W_, H_, 16, 14, 0.4, 6) + rr(W_, H_, 12, 4.4, g, 6) + rr(W_, H_, 24, 1.3, '#f3d98b', 3) + rr(W_, H_, 18, 0.8, '#f3d98b', 4, ' stroke-opacity=".6"');
      s += edgeRun(W_, H_, 18, 16, function (x, y) { return '<path d="M' + n1(x) + ' ' + n1(y - 3) + 'l3 3-3 3-3-3z" fill="#1a1006" stroke="#f3d98b" stroke-width=".9"/>'; }, 48);
      s += corners(W_, H_, 12, function () { return '<path d="M2 34C2 16 16 2 34 2" fill="none" stroke="' + g + '" stroke-width="3.2"/><path d="M8 28C8 18 18 8 28 8" fill="none" stroke="#f3d98b" stroke-width="1.2"/><circle cx="13" cy="13" r="5" fill="#1a1006" stroke="' + g + '" stroke-width="1.8"/><path d="M13 9a4 4 0 1 1-4 4" fill="none" stroke="#f3d98b" stroke-width="1"/><path d="M30 12c4-2 7 0 8 3M12 30c-2 4 0 7 3 8" fill="none" stroke="#f3d98b" stroke-width="1.3"/>'; });
      return s;
    },
    /* 05 - acciaio scuro e graffiato: angoli asimmetrici, tre incisioni diagonali evidenti */
    'cornice-acciaio-mutante': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'st', [[0, '#8c97a2'], [0.5, '#3a4149'], [1, '#6c7782']], 0, 0, 1, 1) + '</defs>', r = rng(5), s = d + rr(W_, H_, 14, 12, '#000', 1, ' stroke-opacity=".5"') + rr(W_, H_, 14, 8, 'url(#' + u + 'st)', 1) + rr(W_, H_, 9.8, 0.8, '#c3ccd5', 0, ' stroke-opacity=".5"'), i;
      for (i = 0; i < 38; i++) { var x = 30 + r() * (W_ - 60), y = r() > 0.5 ? 12 + r() * 4 : H_ - 16 + r() * 4, l = 5 + r() * 12; s += pth('M' + n1(x) + ' ' + n1(y) + 'l' + n1(l) + ' ' + n1(-l * 0.5), '#dfe5ea', 0.7, ' stroke-opacity="' + n1(0.15 + r() * 0.3) + '"'); }
      s += '<path d="M14 62V26L26 14H62" fill="none" stroke="#000" stroke-width="15" stroke-opacity=".45"/><path d="M14 62V26L26 14H62" fill="none" stroke="url(#' + u + 'st)" stroke-width="10" stroke-linejoin="miter"/>';
      s += '<path d="M' + (W_ - 14) + ' ' + (H_ - 40) + 'V' + (H_ - 14) + 'H' + (W_ - 40) + '" fill="none" stroke="url(#' + u + 'st)" stroke-width="10"/>';
      [[0, 3.4], [15, 2.6], [30, 1.8]].forEach(function (k) { s += pth('M' + (W_ - 56 + k[0]) + ' 4L' + (W_ - 4) + ' ' + (56 - k[0] + 0) + '', '#000', k[1] + 3, ' stroke-opacity=".5"').replace('L' + (W_ - 4), 'L' + (W_ - 4 - 0)); });
      [[0, 3.4], [15, 2.6], [30, 1.8]].forEach(function (k) { s += pth('M' + n1(W_ - 74 + k[0]) + ' 6L' + n1(W_ - 18 + k[0] * 0.0) + ' ' + n1(62 - 0 + 0) + '', '#eef3f7', k[1], ' stroke-linecap="round"').replace(/M[^L]*L[^"]*/, 'M' + n1(W_ - 20 - k[0] * 0.9) + ' 6L' + n1(W_ - 80 - k[0] * 0.9) + ' 66'); });
      return s;
    },
    /* 06 - sigillo arcano: doppio filo viola tratteggiato (rune), esagrammi, archi luminosi agli angoli */
    'cornice-energia-arcana': function (W_, H_, u) {
      var v = '#b57ef0', p = '#e2cbff', s = plate(W_, H_, 17, 18, 0.35, 4) + rr(W_, H_, 17, 12, v, 4, ' stroke-opacity=".12"') + rr(W_, H_, 14, 1.8, v, 4) + rr(W_, H_, 21, 1.4, p, 2, ' stroke-dasharray="7 3 2 3" stroke-opacity=".85"');
      var rune = ['M0 -4V4M0 -1L3 -4M0 2L3 -1', 'M-2 -4L2 0L-2 4M2 -4V4', 'M-3 -4L3 4M3 -4L-3 4', 'M-2 4V-4L2 0L-2 0', 'M0 -4L3 0L0 4L-3 0Z', 'M-3 -3H3L-3 3H3'];
      s += edgeRun(W_, H_, 17.5, 15, function (x, y, v2, e, k) { var gI = Math.round(k / 15) % 6; return '<path transform="translate(' + n1(x) + ' ' + n1(y) + ')" d="' + rune[gI] + '" fill="none" stroke="' + p + '" stroke-width="1.1" stroke-linecap="round"/>'; }, 62);
      s += corners(W_, H_, 14, function () { return '<path d="M0 36A36 36 0 0 0 36 0M0 27A27 27 0 0 0 27 0M0 18A18 18 0 0 0 18 0" fill="none" stroke="' + v + '" stroke-width="1.6" stroke-opacity=".9"/><circle cx="7" cy="7" r="3" fill="' + p + '"/><path d="M16 4l3 5h-6zM4 16l5 3v-6z" fill="' + p + '"/>'; });
      [[W_ / 2, 17], [W_ / 2, H_ - 17], [17, H_ / 2], [W_ - 17, H_ / 2]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ')"><circle r="11.5" fill="#12081c" stroke="' + v + '" stroke-width="1.6"/><path d="M0-8L6.9 4H-6.9ZM0 8L6.9-4H-6.9Z" fill="none" stroke="' + p + '" stroke-width="1.2"/></g>'; });
      return s;
    },
    /* 07 - modulare futuristica: segmenti separati da giunti, staffe con circuiti, prese esagonali, accenti ciano */
    'cornice-tecnologia-stark': function (W_, H_, u) {
      var c = '#35d0e8', m = '#3c4c58', m2 = '#1d2830', s = plate(W_, H_, 15, 15, 0.45, 0), seg = function (x1, y1, x2, y2) { var len = Math.hypot(x2 - x1, y2 - y1), n = Math.round(len / 62), i, o = '', ux = (x2 - x1) / len, uy = (y2 - y1) / len, sl = len / n; for (i = 0; i < n; i++) { var a = i * sl + 2.5, b2 = (i + 1) * sl - 2.5; o += '<path d="M' + n1(x1 + ux * a) + ' ' + n1(y1 + uy * a) + 'L' + n1(x1 + ux * b2) + ' ' + n1(y1 + uy * b2) + '" stroke="' + m + '" stroke-width="9" stroke-linecap="butt" fill="none"/><path d="M' + n1(x1 + ux * a) + ' ' + n1(y1 + uy * a) + 'L' + n1(x1 + ux * b2) + ' ' + n1(y1 + uy * b2) + '" stroke="' + c + '" stroke-width="1" stroke-opacity=".8" fill="none" transform="translate(' + n1(-uy * 2.6) + ' ' + n1(ux * 2.6) + ')"/>'; if (i) o += '<rect x="' + n1(x1 + ux * i * sl - 3) + '" y="' + n1(y1 + uy * i * sl - 3) + '" width="6" height="6" fill="' + m2 + '" stroke="' + c + '" stroke-width="1"/>'; } return o; };
      s += seg(40, 15, W_ - 40, 15) + seg(40, H_ - 15, W_ - 40, H_ - 15) + seg(15, 40, 15, H_ - 40) + seg(W_ - 15, 40, W_ - 15, H_ - 40);
      s += corners(W_, H_, 0, function (i) { var cut = i === 0 || i === 3; return '<path d="M4 38V' + (cut ? 14 : 8) + 'L' + (cut ? 14 : 8) + ' 4H38" fill="none" stroke="#000" stroke-width="12" stroke-opacity=".45"/><path d="M4 38V' + (cut ? 14 : 8) + 'L' + (cut ? 14 : 8) + ' 4H38" fill="none" stroke="' + m + '" stroke-width="8"/><path d="M10 34V20L20 10H34" fill="none" stroke="' + c + '" stroke-width="1.4"/><circle cx="10" cy="34" r="2.6" fill="' + m2 + '" stroke="' + c + '" stroke-width="1"/><circle cx="34" cy="10" r="2.6" fill="' + m2 + '" stroke="' + c + '" stroke-width="1"/><path d="M20 20h14v7" fill="none" stroke="' + c + '" stroke-width="1" stroke-opacity=".7"/>'; });
      [W_ / 2 - 26, W_ / 2, W_ / 2 + 26].forEach(function (x) { var h = '', k; for (k = 0; k < 6; k++) { var an = Math.PI / 3 * k; h += n1(x + 8.5 * Math.cos(an)) + ',' + n1(15 + 8.5 * Math.sin(an)) + ' '; } s += '<polygon points="' + h + '" fill="' + m2 + '" stroke="' + c + '" stroke-width="1.2"/><circle cx="' + x + '" cy="15" r="2" fill="' + c + '"/>'; });
      return s;
    },
    /* 08 - angolare/cerimoniale: fascia viola profondo con denti triangolari, angoli a gradini, metallo scuro */
    'cornice-wakanda': function (W_, H_, u) {
      var pv = '#4b2c8c', pl = '#8d6be0', sv = '#c9ccd8', mt = '#26232e', s = plate(W_, H_, 16, 24, 0.42, 0) + rr(W_, H_, 16, 10, pv, 0) + rr(W_, H_, 10.6, 1, sv, 0, ' stroke-opacity=".8"');
      s += edgeRun(W_, H_, 16, 14, function (x, y, v, e) { var d = e ? -1 : 1; return v ? '<path d="M' + n1(x < 40 ? x : x) + ' ' + n1(y - 6) + 'l' + (d * 12) + ' 6l' + (-d * 12) + ' 6z" fill="' + mt + '" stroke="' + sv + '" stroke-width=".8"/>' : '<path d="M' + n1(x - 6) + ' ' + n1(y) + 'l6 ' + (d * 12) + 'l6 ' + (-d * 12) + 'z" fill="' + mt + '" stroke="' + sv + '" stroke-width=".8"/>'; }, 54);
      s += edgeRun(W_, H_, 16, 28, function (x, y, v, e) { return '<circle cx="' + n1(x + (v ? 0 : 14)) + '" cy="' + n1(y + (v ? 14 : 0)) + '" r="1.8" fill="' + pl + '"/>'; }, 54);
      s += corners(W_, H_, 10, function () { return '<path d="M0 0H30V9H21V18H12V27H0Z" fill="' + mt + '" stroke="' + sv + '" stroke-width="1.4" stroke-linejoin="miter"/><path d="M5 5H25V6H16V15H7V22H5Z" fill="' + pv + '"/><path d="M4 4l6 0-6 6z" fill="' + pl + '"/>'; });
      return s;
    },
    /* 09 - monumentale e solenne: fascia d'oro antico a intreccio nordico, torri angolari con merli, archi centrali */
    'cornice-asgard': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'as', [[0, '#e2c77f'], [0.5, '#b08a43'], [1, '#6f5122']], 0, 0, 1, 1) + '</defs>', a = '#d8bb72', s = d + plate(W_, H_, 17, 18, 0.45, 0) + rr(W_, H_, 17, 12, 'url(#' + u + 'as)', 0) + rr(W_, H_, 10.6, 0.9, '#f0dc9c', 0, ' stroke-opacity=".7"') + rr(W_, H_, 23.4, 0.9, '#f0dc9c', 0, ' stroke-opacity=".7"');
      var wave = function (x1, y1, x2, y2, ph) { var len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len, o = '', k; for (k = 0; k < 2; k++) { var dd = 'M' + n1(x1) + ' ' + n1(y1), t; for (t = 0; t <= len; t += 3) { var off = Math.sin((t / 9) + (k ? Math.PI : 0) + ph) * 3.2; dd += 'L' + n1(x1 + ux * t - uy * off) + ' ' + n1(y1 + uy * t + ux * off); } o += '<path d="' + dd + '" fill="none" stroke="' + (k ? '#2a1c08' : '#fbeab4') + '" stroke-width="1.5"/>'; } return o; };
      s += wave(46, 17, W_ - 46, 17, 0) + wave(46, H_ - 17, W_ - 46, H_ - 17, 0) + wave(17, 46, 17, H_ - 46, 0) + wave(W_ - 17, 46, W_ - 17, H_ - 46, 0);
      s += corners(W_, H_, 8, function () { return '<path d="M0 0H32V10H28V6H22V10H18V6H12V10H8V6H4V10H0Z" fill="#000" fill-opacity=".35" transform="translate(1 1)"/><rect x="0" y="8" width="32" height="26" fill="url(#' + u + 'as)" stroke="#2a1c08" stroke-width="1.2"/><path d="M0 8V0H6V4H10V0H16V4H20V0H26V4H30V0H32V8Z" fill="url(#' + u + 'as)" stroke="#2a1c08" stroke-width="1"/><path d="M10 14L16 28L22 14M10 24H22" fill="none" stroke="#2a1c08" stroke-width="2"/>'; });
      [[W_ / 2, 17, 1], [W_ / 2, H_ - 17, -1]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ') scale(1 ' + q[2] + ')"><path d="M-20 5V-1A20 17 0 0 1 20 -1V5Z" fill="#1a1206" stroke="' + a + '" stroke-width="1.6"/><path d="M0-9V4M-4-4L0-9L4-4" stroke="' + a + '" stroke-width="1.4" fill="none"/></g>'; });
      return s;
    },
    /* 10 - bordo discontinuo, frammenti sospesi, angolo mancante: nero, grigio, viola spento */
    'cornice-vuoto-temporale': function (W_, H_, u) {
      var g = '#aaa5bb', v = '#7a6a9c', r = rng(9), s = '', i;
      var run = function (x1, y1, x2, y2, skipMid) { var len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len, t = 0, o = ''; while (t < len) { var l = 22 + r() * 60, gp = 8 + r() * 22, e = Math.min(len, t + l), off = (r() - 0.5) * 11, w = r() > 0.55 ? 6 : 2.6; o += '<path d="M' + n1(x1 + ux * t - uy * off) + ' ' + n1(y1 + uy * t + ux * off) + 'L' + n1(x1 + ux * e - uy * off) + ' ' + n1(y1 + uy * e + ux * off) + '" stroke="#000" stroke-width="' + (w + 4) + '" stroke-opacity=".5" fill="none"/><path d="M' + n1(x1 + ux * t - uy * off) + ' ' + n1(y1 + uy * t + ux * off) + 'L' + n1(x1 + ux * e - uy * off) + ' ' + n1(y1 + uy * e + ux * off) + '" stroke="' + (r() > 0.5 ? g : v) + '" stroke-width="' + w + '" fill="none"/>'; t = e + gp; } return o; };
      s += run(60, 15, W_ - 20, 15) + run(W_ - 15, 20, W_ - 15, H_ - 20) + run(W_ - 60, H_ - 15, 20, H_ - 15) + run(15, H_ - 60, 15, 40);
      s += pth('M16 16H50M16 16V44', g, 0.8, ' stroke-opacity=".5" stroke-dasharray="2 5"') + pth('M' + (W_ - 16) + ' ' + (H_ - 16) + 'H' + (W_ - 50), g, 0.8, ' stroke-opacity=".5" stroke-dasharray="2 5"');
      for (i = 0; i < 16; i++) { var side = i % 4, px, py, sz = 3 + r() * 8; if (side === 0) { px = r() * W_; py = 3 + r() * 9; } else if (side === 1) { px = W_ - 3 - r() * 9; py = r() * H_; } else if (side === 2) { px = r() * W_; py = H_ - 3 - r() * 9; } else { px = 3 + r() * 9; py = r() * H_; } var an = r() * 6.28; s += '<path d="M' + n1(px + Math.cos(an) * sz) + ' ' + n1(py + Math.sin(an) * sz) + 'L' + n1(px + Math.cos(an + 2.3) * sz * 0.9) + ' ' + n1(py + Math.sin(an + 2.3) * sz * 0.9) + 'L' + n1(px + Math.cos(an + 4.1) * sz * 0.6) + ' ' + n1(py + Math.sin(an + 4.1) * sz * 0.6) + 'Z" fill="' + (i % 3 ? '#15121c' : v) + '" stroke="' + g + '" stroke-width=".9" stroke-opacity=".85"/>'; }
      return s;
    },
    /* 11 - realta' che si rompe: bordo spezzato con segmenti disallineati, fratture cremisi, luce rossa localizzata */
    'cornice-incursione-rossa': function (W_, H_, u) {
      var cr = '#ff3d57', dk = '#6b2e36', s = '<defs>' + rg(u + 'rg', 0.5, 0.5, 0.5, '#ff2d4a', 0.5, 0) + '</defs>', cps = [[24, 22], [W_ - 22, H_ * 0.55], [W_ * 0.34, H_ - 15], [W_ - 24, 24]];
      cps.forEach(function (q) { s += '<circle cx="' + q[0] + '" cy="' + q[1] + '" r="34" fill="url(#' + u + 'rg)"/>'; });
      var seg = function (x1, y1, x2, y2, cuts) { var len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len, pts = [0].concat(cuts.map(function (c) { return c * len; })).concat([len]), o = '', i; for (i = 0; i < pts.length - 1; i++) { var a = pts[i] + (i ? 5 : 0), b2 = pts[i + 1] - (i < pts.length - 2 ? 5 : 0), off = i % 2 ? 4 : -2; o += '<path d="M' + n1(x1 + ux * a - uy * off) + ' ' + n1(y1 + uy * a + ux * off) + 'L' + n1(x1 + ux * b2 - uy * off) + ' ' + n1(y1 + uy * b2 + ux * off) + '" stroke="#000" stroke-width="12" stroke-opacity=".5" fill="none"/><path d="M' + n1(x1 + ux * a - uy * off) + ' ' + n1(y1 + uy * a + ux * off) + 'L' + n1(x1 + ux * b2 - uy * off) + ' ' + n1(y1 + uy * b2 + ux * off) + '" stroke="' + dk + '" stroke-width="7" fill="none"/><path d="M' + n1(x1 + ux * a - uy * off - uy * 3.4) + ' ' + n1(y1 + uy * a + ux * off + ux * 3.4) + 'L' + n1(x1 + ux * b2 - uy * off - uy * 3.4) + ' ' + n1(y1 + uy * b2 + ux * off + ux * 3.4) + '" stroke="#c07a82" stroke-width=".9" stroke-opacity=".7" fill="none"/>'; } return o; };
      s += seg(14, 15, W_ - 14, 15, [0.18, 0.62]) + seg(W_ - 15, 14, W_ - 15, H_ - 14, [0.5]) + seg(W_ - 14, H_ - 15, 14, H_ - 15, [0.3, 0.7]) + seg(15, H_ - 14, 15, 14, [0.4]);
      var crack = function (x, y, sx, sy, sc) { return '<g transform="translate(' + x + ' ' + y + ') scale(' + sx * sc + ' ' + sy * sc + ')" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M-14 -6L-2 4L4 -8L14 6L22 -2L36 12" stroke="' + cr + '" stroke-opacity=".3" stroke-width="9"/><path d="M-14 -6L-2 4L4 -8L14 6L22 -2L36 12M-2 4L-6 18M14 6L18 22M22 -2L30 -14" stroke="' + cr + '" stroke-width="2.6"/><path d="M-14 -6L-2 4L4 -8L14 6L22 -2L36 12" stroke="#ffd6dc" stroke-width=".9"/></g>'; };
      s += crack(14, 14, 1, 1, 0.95) + crack(W_ - 15, H_ * 0.55 - 20, 0, 0, 1).replace('scale(0 0)', 'rotate(90) scale(1 -1)') + crack(W_ * 0.34, H_ - 17, 1, -1, 0.9).replace(/translate\(([^ ]+) ([^)]+)\) scale\(([^)]+)\)/, 'translate($1 $2) rotate(-12) scale($3)') + crack(W_ - 14, 14, -1, 1, 0.8);
      return s;
    },
    /* 12 - leggendaria: quattro strati (ghost dimensionali, oro stratificato, filo cremisi, filo interno), medaglioni a gemma, archi, gemme di bordo */
    'cornice-nexus-supremo': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'nx', [[0, '#fff0bd'], [0.45, '#e2b556'], [1, '#9a6f22']], 0, 0, 1, 1) + rg(u + 'gm', 0.35, 0.3, 0.8, '#ff9aa8', 1, 0.2) + '</defs>', g = 'url(#' + u + 'nx)', cr = '#d4283f';
      var s = d + rr(W_, H_, 8, 0.9, '#a78bfa', 0, ' stroke-opacity=".7" transform="translate(-2 -2)"') + rr(W_, H_, 8, 0.9, '#52d6e6', 0, ' stroke-opacity=".7" transform="translate(2 2)"');
      s += plate(W_, H_, 17, 20, 0.45, 3) + rr(W_, H_, 14, 5.4, g, 3) + rr(W_, H_, 21, 1.6, cr, 1) + rr(W_, H_, 25.5, 1.1, '#fff0bd', 0) + rr(W_, H_, 28.5, 0.7, g, 0, ' stroke-dasharray="3 3" stroke-opacity=".8"');
      s += edgeRun(W_, H_, 14, 44, function (x, y, v) { return '<path transform="translate(' + n1(x) + ' ' + n1(y) + ')" d="M0-5L4 0 0 5-4 0Z" fill="#12070a" stroke="#fff0bd" stroke-width="1.2"/><circle r="1.4" fill="' + cr + '"/>'; }, 82);
      s += corners(W_, H_, 6, function () { var rays = '', k; for (k = 0; k < 8; k++) { var an = Math.PI / 4 * k; rays += '<path d="M' + n1(Math.cos(an) * 9) + ' ' + n1(Math.sin(an) * 9) + 'L' + n1(Math.cos(an) * 19) + ' ' + n1(Math.sin(an) * 19) + '" stroke="#fff0bd" stroke-width="1.2"/>'; } var oct = [], j; for (j = 0; j < 8; j++) { var a2 = Math.PI / 4 * j + Math.PI / 8; oct.push([Math.cos(a2) * 15, Math.sin(a2) * 15]); } return '<g transform="translate(18 18)">' + rays + poly(oct, g, '#2a1a05', 1.4) + '<circle r="9" fill="#12070a" stroke="#fff0bd" stroke-width="1.2"/><circle r="5.4" fill="url(#' + u + 'gm)" stroke="' + cr + '" stroke-width="1"/></g>'; });
      [[W_ / 2, 14, 1], [W_ / 2, H_ - 14, -1]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ') scale(1 ' + q[2] + ')"><path d="M-34 0Q-16 17 0 17Q16 17 34 0" fill="none" stroke="' + g + '" stroke-width="3"/><path d="M-22 0Q-9 11 0 11Q9 11 22 0" fill="none" stroke="' + cr + '" stroke-width="1.2"/><path d="M0 3L8 13 0 23-8 13Z" fill="#12070a" stroke="#fff0bd" stroke-width="1.6"/><circle cy="13" r="2.8" fill="url(#' + u + 'gm)"/></g>'; });
      [[10, H_ / 2], [W_ - 10, H_ / 2]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ')"><path d="M0-17L9 0 0 17-9 0Z" fill="#12070a" stroke="' + g + '" stroke-width="2.2"/><circle r="2.8" fill="url(#' + u + 'gm)"/></g>'; });
      return s;
    }
  };
  /* distintivi di colore principali delle cornici (per i test di contrasto) */
  var FRAME_COLORS = { 'cornice-standard-tva': ['#D2B184'], 'cornice-bronzo-temporale': ['#e2a566', '#a86a2c'], 'cornice-argento-cronologico': ['#d3dde8'], 'cornice-oro-archivista': ['#fbe9ae', '#d9ad4e'], 'cornice-acciaio-mutante': ['#8c97a2', '#eef3f7'], 'cornice-energia-arcana': ['#b57ef0', '#e2cbff'], 'cornice-tecnologia-stark': ['#35d0e8'], 'cornice-wakanda': ['#8d6be0', '#c9ccd8'], 'cornice-asgard': ['#e2c77f', '#fbeab4'], 'cornice-vuoto-temporale': ['#aaa5bb', '#7a6a9c'], 'cornice-incursione-rossa': ['#ff3d57', '#c07a82'], 'cornice-nexus-supremo': ['#fff0bd', '#e2b556'] };

  /* ---------- TEMI (10): sfondo, palette, testi, motivi, texture, luce e superfici propri ----------
     palette di riferimento: bg / accento / testo. Il testo-accento (ID, intestazioni) viene portato a contrasto >= 4,5 sul fondo. */
  function lighting(W_, H_, u, bg, k) {
    return '<defs>' + rg(u + 'l1', 0.18, 0.08, 0.95, '#ffffff', 0.10 * (k || 1), 0) + rg(u + 'l2', 0.85, 1, 0.8, '#000000', 0.5, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'l1)"/><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'l2)"/>';
  }
  function base(W_, H_, u, bg, lo) { return '<defs>' + lg(u + 'tb', [[0, mix(bg, '#ffffff', lo || 0.07)], [0.55, bg], [1, mix(bg, '#000000', 0.5)]], 0, 0, 1, 1) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'tb)"/>'; }
  function hatch(W_, H_, col, op, step, ang) { var s = '', i, d = Math.max(W_, H_) * 1.5; for (i = -d; i < d; i += step) s += '<path d="M' + n1(i) + ' ' + H_ + 'L' + n1(i + (ang || 1) * H_) + ' 0"/>'; return '<g stroke="' + col + '" stroke-opacity="' + op + '" stroke-width=".8">' + s + '</g>'; }
  var THEMES = {
    /* istituzionale: bordeaux scuro, guilloche, clessidra filigranata */
    'tema-tva-classico': { bg: '#211016', acc: '#D2B184', ink: '#F2E8D5', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#211016', 0.1) + hatch(W_, H_, '#D2B184', 0.05, 11, 0.45), cx = W_ * 0.76, cy = H_ * 0.52, R = Math.min(W_, H_) * 0.4, i;
      var ring = ''; for (i = 1; i <= 5; i++) ring += '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * i / 5) + '" fill="none" stroke="#D2B184" stroke-opacity="' + n1(0.05 + i * 0.012) + '"/>';
      var hg = '<path d="M' + n1(cx - R * 0.28) + ' ' + n1(cy - R * 0.4) + 'H' + n1(cx + R * 0.28) + 'L' + cx + ' ' + cy + 'L' + n1(cx + R * 0.28) + ' ' + n1(cy + R * 0.4) + 'H' + n1(cx - R * 0.28) + 'L' + cx + ' ' + cy + 'Z" fill="none" stroke="#D2B184" stroke-opacity=".16" stroke-width="2.4"/>';
      return s + ring + hg + lighting(W_, H_, u, '#211016');
    } },
    /* documentazione riservata: blu profondo, righe da registro, barre di oscuramento, timbro */
    'tema-archivio-notturno': { bg: '#0A1425', acc: '#6885A7', ink: '#DCE7F1', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#0A1425', 0.1), y, r = rng(2), st = '';
      for (y = 34; y < H_; y += 30) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#6885A7" stroke-opacity=".12"/>';
      s += '<path d="M' + n1(W_ * 0.07) + ' 0V' + H_ + '" stroke="#c85a6a" stroke-opacity=".22"/>';
      for (y = 0; y < 5; y++) st += '<rect x="' + n1(W_ * (0.55 + r() * 0.3)) + '" y="' + n1(H_ * (0.15 + y * 0.17)) + '" width="' + n1(W_ * (0.08 + r() * 0.16)) + '" height="' + n1(H_ * 0.022) + '" fill="#02050b" fill-opacity=".6"/>';
      var cx = W_ * 0.8, cy = H_ * 0.6, R = Math.min(W_, H_) * 0.2;
      s += st + '<g transform="rotate(-14 ' + n1(cx) + ' ' + n1(cy) + ')" fill="none" stroke="#6885A7" stroke-opacity=".28"><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R) + '" stroke-width="2.4"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.82) + '" stroke-width="1"/><path d="M' + n1(cx - R * 0.6) + ' ' + n1(cy) + 'H' + n1(cx + R * 0.6) + '" stroke-width="2"/></g>';
      return s + lighting(W_, H_, u, '#0A1425', 0.8);
    } },
    /* bronzo e oro: superfici calde spazzolate, raggi, ingranaggio e scala cronologica */
    'tema-cronologia-dorata': { bg: '#2C2115', acc: '#D9AE4D', ink: '#FFF0BD', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#2C2115', 0.12), i, cx = W_ * 0.74, cy = H_ * 0.5, y;
      for (y = 3; y < H_; y += 5) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#ffe6a8" stroke-opacity="' + (y % 15 === 3 ? 0.05 : 0.025) + '"/>';
      for (i = 0; i < 32; i++) { var a = Math.PI * 2 / 32 * i; s += '<path d="M' + n1(cx + Math.cos(a) * 70) + ' ' + n1(cy + Math.sin(a) * 70) + 'L' + n1(cx + Math.cos(a) * Math.max(W_, H_)) + ' ' + n1(cy + Math.sin(a) * Math.max(W_, H_)) + '" stroke="#D9AE4D" stroke-opacity=".05" stroke-width="7"/>'; }
      var R = Math.min(W_, H_) * 0.34, tp = [], t; for (t = 0; t < 36; t++) { var an = Math.PI / 18 * t, rad = t % 2 ? R * 0.9 : R; tp.push([cx + Math.cos(an) * rad, cy + Math.sin(an) * rad]); }
      s += poly(tp, 'none', '#D9AE4D', 1.6, ' stroke-opacity=".2"') + '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.55) + '" fill="none" stroke="#D9AE4D" stroke-opacity=".18" stroke-width="2"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.12) + '" fill="#D9AE4D" fill-opacity=".2"/>';
      for (y = 28; y < H_ - 20; y += 22) s += '<path d="M' + n1(W_ * 0.035) + ' ' + y + 'h' + ((y / 22 | 0) % 4 === 0 ? 20 : 10) + '" stroke="#D9AE4D" stroke-opacity=".3" stroke-width="1.4"/>';
      return s + lighting(W_, H_, u, '#2C2115');
    } },
    /* tensione dimensionale: frammenti di realta' sfalsati con fratture rosse */
    'tema-multiverso-cremisi': { bg: '#29090F', acc: '#D82C48', ink: '#F5B1BC', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#29090F', 0.08), r = rng(23), sh = [[0, 0, 0.42, 0, 0.3, 1, 0, 1], [0.42, 0, 0.74, 0, 0.62, 1, 0.3, 1], [0.74, 0, 1, 0, 1, 1, 0.62, 1]], k;
      sh.forEach(function (q, i) { var pts = ''; for (k = 0; k < 8; k += 2) pts += n1(q[k] * W_) + ',' + n1(q[k + 1] * H_) + ' '; s += '<polygon points="' + pts + '" fill="' + (i === 1 ? '#6a1020' : i === 2 ? '#150307' : '#ffffff') + '" fill-opacity="' + (i === 0 ? 0.03 : 0.3) + '"/>'; });
      var f = function (x0, w) { var d = 'M' + n1(x0 * W_) + ' 0', y = 0; while (y < H_) { y += 20 + r() * 40; d += 'L' + n1(x0 * W_ + (r() - 0.5) * w) + ' ' + n1(Math.min(y, H_)); } return d; };
      [[0.42, 40], [0.7, 50]].forEach(function (q) { var d = f(q[0], q[1]); s += '<path d="' + d + '" fill="none" stroke="#D82C48" stroke-opacity=".25" stroke-width="9" stroke-linejoin="round"/><path d="' + d + '" fill="none" stroke="#ff6b83" stroke-opacity=".7" stroke-width="1.6" stroke-linejoin="round"/>'; });
      for (k = 0; k < 6; k++) s += '<circle cx="' + n1(r() * W_) + '" cy="' + n1(r() * H_) + '" r="' + n1(Math.min(W_, H_) * (0.1 + r() * 0.2)) + '" fill="none" stroke="#D82C48" stroke-opacity=".08" stroke-width="2"/>';
      return s + lighting(W_, H_, u, '#29090F');
    } },
    /* petrolio scuro e ciano: griglia tecnica, circuiti, pannelli smussati */
    'tema-tecnologia-futuristica': { bg: '#071D25', acc: '#24B4C5', ink: '#B8F5F0', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#071D25', 0.1), x, y, r = rng(5), g = Math.round(W_ / 21);
      for (x = g; x < W_; x += g) s += '<path d="M' + x + ' 0V' + H_ + '" stroke="#24B4C5" stroke-opacity=".06"/>';
      for (y = g; y < H_; y += g) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#24B4C5" stroke-opacity=".06"/>';
      for (x = 0; x < 11; x++) { var px = g * (1 + Math.floor(r() * (W_ / g - 3))), py = g * (1 + Math.floor(r() * (H_ / g - 3))), l = g * (1 + Math.floor(r() * 3)); s += '<path d="M' + px + ' ' + py + 'h' + l + 'v' + g + 'h' + l + '" fill="none" stroke="#24B4C5" stroke-opacity=".3" stroke-width="1.4"/><circle cx="' + (px + 2 * l) + '" cy="' + (py + g) + '" r="3" fill="#071D25" stroke="#24B4C5" stroke-opacity=".6"/>'; }
      var pw = W_ * 0.3, ph = H_ * 0.34, c = 14; s += '<polygon points="' + [[W_ * 0.64 + c, H_ * 0.18], [W_ * 0.64 + pw, H_ * 0.18], [W_ * 0.64 + pw, H_ * 0.18 + ph - c], [W_ * 0.64 + pw - c, H_ * 0.18 + ph], [W_ * 0.64, H_ * 0.18 + ph], [W_ * 0.64, H_ * 0.18 + c]].map(function (p) { return n1(p[0]) + ',' + n1(p[1]); }).join(' ') + '" fill="#24B4C5" fill-opacity=".05" stroke="#24B4C5" stroke-opacity=".3"/>';
      return s + lighting(W_, H_, u, '#071D25');
    } },
    /* indaco e viola: diagonali, riflessi metallici */
    'tema-universo-mutante': { bg: '#17132D', acc: '#7863D7', ink: '#E0D7FF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#17132D', 0.09) + '<defs>' + lg(u + 'ms', [[0, '#ffffff', 0], [0.5, '#c9bdff', 0.16], [1, '#ffffff', 0]], 0, 0, 1, 0) + '</defs>', i, d = Math.max(W_, H_);
      for (i = -3; i < 16; i++) { var x = i * W_ * 0.14; s += '<polygon points="' + [[x, H_], [x + d * 0.55, H_ - d * 0.55], [x + d * 0.55 + W_ * (i % 3 ? 0.03 : 0.07), H_ - d * 0.55], [x + W_ * (i % 3 ? 0.03 : 0.07), H_]].map(function (p) { return n1(p[0]) + ',' + n1(p[1]); }).join(' ') + '" fill="#7863D7" fill-opacity="' + (i % 3 ? 0.07 : 0.14) + '"/>'; }
      s += '<polygon points="0,' + n1(H_ * 0.7) + ' ' + n1(W_) + ',' + n1(H_ * 0.1) + ' ' + n1(W_) + ',' + n1(H_ * 0.24) + ' 0,' + n1(H_ * 0.84) + '" fill="url(#' + u + 'ms)"/>';
      s += '<path d="M0 ' + n1(H_ * 0.7) + 'L' + W_ + ' ' + n1(H_ * 0.1) + 'M0 ' + n1(H_ * 0.84) + 'L' + W_ + ' ' + n1(H_ * 0.24) + '" stroke="#c9bdff" stroke-opacity=".28"/>';
      return s + lighting(W_, H_, u, '#17132D');
    } },
    /* sigilli e geometrie arcane: cerchi concentrici con rune, esagrammi, alone viola */
    'tema-energia-mistica': { bg: '#25122E', acc: '#B15BE1', ink: '#EBC8FF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#25122E', 0.09) + '<defs>' + rg(u + 'mg', 0.72, 0.5, 0.6, '#B15BE1', 0.34, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'mg)"/>', cx = W_ * 0.74, cy = H_ * 0.5, R = Math.min(W_, H_) * 0.46, i;
      for (i = 1; i <= 4; i++) s += '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * i / 4) + '" fill="none" stroke="#B15BE1" stroke-opacity="' + n1(0.12 + i * 0.03) + '" stroke-width="' + (i === 4 ? 2 : 1) + '"' + (i % 2 ? ' stroke-dasharray="3 5"' : '') + '/>';
      for (i = 0; i < 24; i++) { var a = Math.PI / 12 * i; s += '<path d="M' + n1(cx + Math.cos(a) * R * 0.97) + ' ' + n1(cy + Math.sin(a) * R * 0.97) + 'L' + n1(cx + Math.cos(a) * R * (i % 2 ? 1.04 : 1.1)) + ' ' + n1(cy + Math.sin(a) * R * (i % 2 ? 1.04 : 1.1)) + '" stroke="#EBC8FF" stroke-opacity=".3"/>'; }
      var hex = function (k, rot) { var p = [], j; for (j = 0; j < 3; j++) { var an = rot + Math.PI * 2 / 3 * j; p.push([cx + Math.cos(an) * R * k, cy + Math.sin(an) * R * k]); } return poly(p, 'none', '#EBC8FF', 1.4, ' stroke-opacity=".3"'); };
      return s + hex(0.72, -Math.PI / 2) + hex(0.72, Math.PI / 2) + lighting(W_, H_, u, '#25122E');
    } },
    /* quasi monocromatico: frammenti, vuoti, asimmetria */
    'tema-ombre-del-vuoto': { bg: '#08080E', acc: '#686477', ink: '#D4D0DD', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#08080E', 0.1), r = rng(31), i;
      s += '<defs>' + rg(u + 'vd', 0.78, 0.62, 0.34, '#000000', 1, 0) + '</defs><circle cx="' + n1(W_ * 0.78) + '" cy="' + n1(H_ * 0.62) + '" r="' + n1(Math.min(W_, H_) * 0.42) + '" fill="url(#' + u + 'vd)"/><circle cx="' + n1(W_ * 0.78) + '" cy="' + n1(H_ * 0.62) + '" r="' + n1(Math.min(W_, H_) * 0.24) + '" fill="#020204"/><circle cx="' + n1(W_ * 0.78) + '" cy="' + n1(H_ * 0.62) + '" r="' + n1(Math.min(W_, H_) * 0.24) + '" fill="none" stroke="#9a96a8" stroke-opacity=".3" stroke-width="1.4" stroke-dasharray="14 9"/>';
      for (i = 0; i < 16; i++) { var x = r() * W_, y = r() * H_, sz = Math.min(W_, H_) * (0.03 + r() * 0.09), an = r() * 6.28; s += '<polygon points="' + [0, 2.2, 4.1].map(function (o, k) { return n1(x + Math.cos(an + o) * sz * (k === 2 ? 0.55 : 1)) + ',' + n1(y + Math.sin(an + o) * sz * (k === 2 ? 0.55 : 1)); }).join(' ') + '" fill="#686477" fill-opacity="' + n1(0.08 + r() * 0.14) + '" stroke="#9a96a8" stroke-opacity=".3" stroke-width=".8"/>'; }
      s += '<defs>' + rg(u + 'vl', 0.15, 0.1, 0.6, '#b9b4cc', 0.14, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'vl)"/>';
      for (i = 6; i < H_; i += 7) s += '<path d="M0 ' + i + 'H' + W_ + '" stroke="#fff" stroke-opacity=".018"/>';
      return s + lighting(W_, H_, u, '#08080E', 0.4);
    } },
    /* blu cosmico: nebulosa viola, orbite, stelle */
    'tema-nexus-cosmico': { bg: '#101C39', acc: '#477BEB', ink: '#D8B5FF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#101C39', 0.08) + '<defs>' + rg(u + 'nb', 0.74, 0.3, 0.55, '#a45be0', 0.42, 0) + rg(u + 'nc', 0.2, 0.85, 0.5, '#477BEB', 0.3, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'nb)"/><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'nc)"/>' + stars(W_, H_, 70, 21, '#ffffff', 1.5), cx = W_ * 0.68, cy = H_ * 0.52, i;
      for (i = 0; i < 3; i++) s += '<ellipse cx="' + n1(cx) + '" cy="' + n1(cy) + '" rx="' + n1(W_ * (0.3 + i * 0.12)) + '" ry="' + n1(H_ * (0.12 + i * 0.07)) + '" transform="rotate(' + (-22 + i * 6) + ' ' + n1(cx) + ' ' + n1(cy) + ')" fill="none" stroke="#8fb0ff" stroke-opacity="' + n1(0.26 - i * 0.05) + '" stroke-width="1.2"/>';
      s += '<circle cx="' + n1(cx + W_ * 0.22) + '" cy="' + n1(cy - H_ * 0.12) + '" r="' + n1(Math.min(W_, H_) * 0.025) + '" fill="#d8b5ff"/><circle cx="' + n1(cx - W_ * 0.18) + '" cy="' + n1(cy + H_ * 0.15) + '" r="' + n1(Math.min(W_, H_) * 0.018) + '" fill="#8fb0ff"/>';
      return s + lighting(W_, H_, u, '#101C39', 0.6);
    } },
    /* oro pallido, solenne e monumentale: orologio spezzato, colonne, orizzonte (tema leggendario, il piu' elaborato) */
    'tema-fine-del-tempo': { bg: '#242018', acc: '#E5C879', ink: '#FFF8DF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#242018', 0.1) + '<defs>' + lg(u + 'cl', [[0, '#E5C879', 0.2], [1, '#E5C879', 0.02]], 0, 0, 0, 1) + rg(u + 'sn', 0.72, 0.9, 0.55, '#fff2b8', 0.32, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'sn)"/>', cx = W_ * 0.74, cy = H_ * 0.58, R = Math.min(W_, H_) * 0.42, i;
      for (i = 0; i < 5; i++) { var x = W_ * (0.48 + i * 0.105); s += '<rect x="' + n1(x) + '" y="' + n1(H_ * 0.1) + '" width="' + n1(W_ * 0.05) + '" height="' + n1(H_ * 0.8) + '" fill="url(#' + u + 'cl)"/><rect x="' + n1(x - 3) + '" y="' + n1(H_ * 0.1) + '" width="' + n1(W_ * 0.05 + 6) + '" height="6" fill="#E5C879" fill-opacity=".14"/>'; }
      s += '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R) + '" fill="#242018" fill-opacity=".7" stroke="#E5C879" stroke-opacity=".38" stroke-width="2.4"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.9) + '" fill="none" stroke="#E5C879" stroke-opacity=".2"/>';
      for (i = 0; i < 12; i++) { var a = Math.PI / 6 * i; s += '<path d="M' + n1(cx + Math.cos(a) * R * 0.78) + ' ' + n1(cy + Math.sin(a) * R * 0.78) + 'L' + n1(cx + Math.cos(a) * R * 0.9) + ' ' + n1(cy + Math.sin(a) * R * 0.9) + '" stroke="#E5C879" stroke-opacity=".5" stroke-width="2.4"/>'; }
      s += '<path d="M' + n1(cx) + ' ' + n1(cy) + 'L' + n1(cx + R * 0.5) + ' ' + n1(cy - R * 0.36) + 'M' + n1(cx) + ' ' + n1(cy) + 'L' + n1(cx - R * 0.12) + ' ' + n1(cy - R * 0.66) + '" stroke="#E5C879" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/><path d="M' + n1(cx - R * 1.05) + ' ' + n1(cy + R * 0.2) + 'L' + n1(cx - R * 0.2) + ' ' + n1(cy - R * 0.04) + 'L' + n1(cx + R * 0.14) + ' ' + n1(cy + R * 0.44) + 'L' + n1(cx + R * 1.05) + ' ' + n1(cy + R * 0.14) + '" fill="none" stroke="#d42a3a" stroke-opacity=".45" stroke-width="2"/><path d="M0 ' + n1(H_ * 0.9) + 'H' + W_ + '" stroke="#E5C879" stroke-opacity=".3"/>';
      return s + lighting(W_, H_, u, '#242018', 0.7);
    } }
  };
  Object.keys(THEMES).forEach(function (k) { var t = THEMES[k]; t.sub = mix(t.ink, t.bg, 0.34); t.accT = ensure(t.acc, mix(t.bg, '#000000', 0.2), 4.6); t.bar = ensure(t.acc, t.bg, 3); });

