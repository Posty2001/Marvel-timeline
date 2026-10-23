/* TCART-JS-BEGIN: Blocco 3.2 - motore grafico della Tessera TVA (SVG puro, senza immagini esterne): avatar originali, 12 cornici, 10 temi, 6 effetti, 3 composizioni (wide, compact, vertical). */
(function () {
  'use strict';
  var W = window;
  if (W.tvaCardArt) return;
  var SERIF = "Georgia, 'Times New Roman', serif", MONO = "ui-monospace, Menlo, Consolas, 'Courier New', monospace";
  var GOLD = '#D2B184', IVORY = '#efe4c9';
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function n1(v) { return Math.round(v * 10) / 10; }
  function rng(seed) { var a = seed >>> 0; return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

  /* ---------- misura testo (stesso font in anteprima ed esportazione) ---------- */
  var mctx = null;
  function measure(text, font) { try { if (!mctx) mctx = document.createElement('canvas').getContext('2d'); mctx.font = font; return mctx.measureText(text).width; } catch (e) { return text.length * 0.6 * parseFloat(font.match(/(\d+(\.\d+)?)px/)[1]); } }
  function fit(text, weight, style, family, maxW, max, min, ls) {
    var size = max; ls = ls || 0;
    for (; size > min; size -= 1) { if (measure(text, style + ' ' + weight + ' ' + size + 'px ' + family) + ls * Math.max(0, text.length - 1) <= maxW) return size; }
    return min;
  }
  function clip(text, weight, style, family, size, maxW) {
    if (measure(text, style + ' ' + weight + ' ' + size + 'px ' + family) <= maxW) return text;
    var t = text; while (t.length > 1 && measure(t + '…', style + ' ' + weight + ' ' + size + 'px ' + family) > maxW) t = t.slice(0, -1);
    return t + '…';
  }
  function T(x, y, s, o) {
    o = o || {};
    return '<text x="' + n1(x) + '" y="' + n1(y) + '" font-family="' + (o.mono ? MONO : SERIF) + '" font-size="' + n1(o.size || 20) + '" fill="' + (o.fill || IVORY) + '"' +
      (o.weight ? ' font-weight="' + o.weight + '"' : '') + (o.italic ? ' font-style="italic"' : '') + (o.anchor ? ' text-anchor="' + o.anchor + '"' : '') +
      (o.ls ? ' letter-spacing="' + o.ls + '"' : '') + (o.op ? ' fill-opacity="' + o.op + '"' : '') + '>' + esc(s) + '</text>';
  }

  /* ---------- emblema TVA (geometria originale: esagono, quadrante, clessidra) ---------- */
  function emblem(cx, cy, r, col, sw) {
    var pts = [], i; for (i = 0; i < 6; i++) { var a = Math.PI / 3 * i - Math.PI / 6; pts.push(n1(cx + r * Math.cos(a)) + ',' + n1(cy + r * Math.sin(a))); }
    var k = r * 0.42;
    return '<g fill="none" stroke="' + col + '" stroke-width="' + sw + '" stroke-linejoin="round"><polygon points="' + pts.join(' ') + '"/><circle cx="' + cx + '" cy="' + cy + '" r="' + n1(r * 0.64) + '"/>' +
      '<path d="M' + n1(cx - k) + ' ' + n1(cy - k) + 'H' + n1(cx + k) + 'L' + cx + ' ' + cy + 'L' + n1(cx + k) + ' ' + n1(cy + k) + 'H' + n1(cx - k) + 'L' + cx + ' ' + cy + 'Z"/></g>';
  }

  /* ---------- AVATAR (8 ritratti, 100x100, PROPOSTA illustrata a mano in SVG: ombreggiatura a 3 toni, luce di taglio, costumi propri) ----------
     Limite dichiarato: non e' arte generata da un'IA di immagini; e' una proposta visiva con le risorse disponibili. */
  function skin(u, a, b) { return '<linearGradient id="' + u + 'sk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="' + a + '"/><stop offset="1" stop-color="' + b + '"/></linearGradient>'; }
  function lgd(id, a, b, x2, y2) { return '<linearGradient id="' + id + '" x1="0" y1="0" x2="' + (x2 || 0) + '" y2="' + (y2 || 1) + '"><stop offset="0" stop-color="' + a + '"/><stop offset="1" stop-color="' + b + '"/></linearGradient>'; }
  function rim(d, col, w, op) { return '<path d="' + d + '" fill="none" stroke="' + col + '" stroke-width="' + (w || 0.9) + '" stroke-linecap="round" stroke-opacity="' + (op || 0.85) + '"/>'; }
  function head(u, cx, cy, rx, ry, shade) { return '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + rx + '" ry="' + ry + '" fill="url(#' + u + 'sk)"/><path d="M' + (cx + 1) + ' ' + (cy - ry + 1) + 'A' + rx + ' ' + ry + ' 0 0 1 ' + (cx + 1) + ' ' + (cy + ry) + 'Q' + (cx + rx * 0.3) + ' ' + cy + ' ' + (cx + 1) + ' ' + (cy - ry + 1) + 'Z" fill="' + (shade || '#3a1a10') + '" fill-opacity=".28"/>'; }
  var AVATARS = [
    { id: 'agente', nome: 'Agente temporale', bg: ['#4a1620', '#0f0508'], svg: function (u) {
      return '<defs>' + skin(u, '#e8b890', '#b57a52') + lgd(u + 'su', '#c4682c', '#5e2c12', 0.3, 1) + rg(u + 'hl', 0.3, 0.3, 0.6, '#ffd9a0', 0.55, 0) + '</defs>' +
        '<circle cx="50" cy="40" r="35" fill="none" stroke="#D2B184" stroke-width=".8" stroke-opacity=".5"/><circle cx="50" cy="40" r="30" fill="none" stroke="#D2B184" stroke-width="1.6" stroke-opacity=".28" stroke-dasharray="1.2 3.4"/>' +
        '<path d="M6 100C6 76 24 68 41 64H59C76 68 94 76 94 100Z" fill="url(#' + u + 'su)"/><path d="M41 64L50 83L59 64L68 100H32Z" fill="#efe4c9"/><path d="M41 64L50 83L30 100H12C12 80 26 70 41 64ZM59 64L50 83L70 100H88C88 80 74 70 59 64Z" fill="#6e3314"/><path d="M41 64L50 83L30 100" fill="none" stroke="#e0a060" stroke-width=".8"/>' +
        '<path d="M50 72L46.6 77L50 94L53.4 77Z" fill="#9c1c22"/><path d="M47.6 70.5H52.4L53.4 76H46.6Z" fill="#b8262c"/>' +
        '<rect x="63" y="80" width="9" height="6.4" rx="1" fill="#D2B184"/><rect x="64.4" y="81.4" width="3" height="3.6" fill="#3a1a10"/><path d="M69 82h2M69 84h2" stroke="#3a1a10" stroke-width=".7"/>' +
        '<path d="M43 52H57L58 66Q50 70 42 66Z" fill="#a8704a"/><path d="M43 60Q50 64 57 60V66Q50 70 43 66Z" fill="#000" fill-opacity=".25"/>' +
        head(u, 50, 39, 12.6, 15.4, '#2a0e08') + '<ellipse cx="37.6" cy="41" rx="2" ry="3.4" fill="#c98a62"/><ellipse cx="62.4" cy="41" rx="2" ry="3.4" fill="#9a6040"/>' +
        '<path d="M37.6 36C36 24 44 20 52 21C60 21.5 64 27 62.6 36C61 31 58 28.6 52 28.4C46 28.2 40 30 37.6 36Z" fill="#2c1810"/><path d="M39 29C42 23 52 21 60 24" fill="none" stroke="#7a4a2a" stroke-width="1" stroke-linecap="round"/>' +
        '<path d="M42 37.4L47.4 36.8M52.6 36.8L58 37.4" stroke="#2a1208" stroke-width="1.5" stroke-linecap="round"/><ellipse cx="44.6" cy="40.2" rx="2.1" ry="1.1" fill="#f6efe0"/><ellipse cx="55.4" cy="40.2" rx="2.1" ry="1.1" fill="#f6efe0"/><circle cx="44.8" cy="40.2" r=".95" fill="#20120a"/><circle cx="55.6" cy="40.2" r=".95" fill="#20120a"/>' +
        '<path d="M50 41.5L48.6 47.4Q50 48.4 51.4 47.4" fill="none" stroke="#7e4a30" stroke-width=".9" stroke-linecap="round"/><path d="M45.4 51.6Q50 53.4 54.6 51.6" fill="none" stroke="#6a2a22" stroke-width="1.2" stroke-linecap="round"/>' +
        rim('M38 28C41 22 48 20 55 21', '#ffe2b0', 0.9) + rim('M10 96C11 80 24 71 38 66', '#ffd2a0', 1) + '<rect width="100" height="100" fill="url(#' + u + 'hl)"/>'; } },
    { id: 'variante', nome: 'Variante misteriosa', bg: ['#2a1634', '#07040b'], svg: function (u) {
      return '<defs>' + lgd(u + 'cl', '#3a2a52', '#0a0710', 0.4, 1) + rg(u + 'gl', 0.5, 0.42, 0.5, '#c8a0ff', 0.5, 0) + '</defs>' +
        '<circle cx="50" cy="40" r="34" fill="url(#' + u + 'gl)"/><path d="M50 4C70 4 80 24 80 44C80 52 86 60 94 100H6C14 60 20 52 20 44C20 24 30 4 50 4Z" fill="url(#' + u + 'cl)"/>' +
        '<path d="M50 4C70 4 80 24 80 44C80 52 86 60 94 100H72C70 78 64 66 50 64C36 66 30 78 28 100H6C14 60 20 52 20 44C20 24 30 4 50 4Z" fill="#000" fill-opacity=".25"/>' +
        '<path d="M30 40C30 24 38 16 50 16C62 16 70 24 70 40C70 56 62 66 50 66C38 66 30 56 30 40Z" fill="#05030a"/>' +
        '<path d="M34 32C34 22 41 18 50 18C59 18 66 22 66 32" fill="none" stroke="#8a6cc0" stroke-width=".8" stroke-opacity=".6"/>' +
        '<path d="M38 42L46 40.4L46.6 43.6L38.6 44.4Z" fill="#e8c46a"/><path d="M62 42L54 40.4L53.4 43.6L61.4 44.4Z" fill="#e8c46a"/><path d="M38 42L46 40.4" stroke="#fff4c8" stroke-width=".6"/><path d="M62 42L54 40.4" stroke="#fff4c8" stroke-width=".6"/>' +
        '<path d="M50 15L55 23L50 31L45 23Z" fill="#e8c46a" fill-opacity=".9"/><path d="M50 18L52.6 23L50 28L47.4 23Z" fill="#05030a"/>' +
        '<path d="M42 54Q50 58 58 54" fill="none" stroke="#6a548a" stroke-width=".8" stroke-opacity=".7"/>' +
        rim('M22 46C21 28 30 8 50 5', '#c8a8ff', 1.1) + rim('M7 98C12 66 20 56 21 48', '#b898f0', 0.9, 0.6) + '<path d="M20 100C22 84 28 76 36 72M80 100C78 84 72 76 64 72" stroke="#8a6cc0" stroke-width=".7" fill="none" stroke-opacity=".5"/>'; } },
    { id: 'esploratore', nome: 'Esploratore del Multiverso', bg: ['#0e3a42', '#031014'], svg: function (u) {
      return '<defs>' + skin(u, '#f0c8a0', '#a8704c') + lgd(u + 'co', '#2c6a70', '#0c2a30', 0.3, 1) + rg(u + 'po', 0.7, 0.35, 0.55, '#5fe8f0', 0.6, 0) + '</defs>' +
        '<circle cx="66" cy="34" r="30" fill="url(#' + u + 'po)"/><circle cx="68" cy="32" r="27" fill="none" stroke="#7fe8f0" stroke-width="1.6" stroke-opacity=".7"/><circle cx="68" cy="32" r="21" fill="none" stroke="#7fe8f0" stroke-width=".8" stroke-opacity=".5" stroke-dasharray="3 2.4"/><circle cx="68" cy="32" r="15" fill="none" stroke="#bff8fb" stroke-width=".7" stroke-opacity=".5"/>' +
        '<path d="M4 100C4 78 20 68 38 64H62C80 68 96 78 96 100Z" fill="url(#' + u + 'co)"/><path d="M38 64L44 100H30C26 80 28 70 38 64ZM62 64L56 100H70C74 80 72 70 62 64Z" fill="#14363c" stroke="#5fe0e8" stroke-width=".7" stroke-opacity=".7"/>' +
        '<path d="M30 66L36 100M70 66L64 100" stroke="#a87a3a" stroke-width="3" stroke-opacity=".9"/><rect x="31.4" y="76" width="4.6" height="5" fill="#d2a860"/><rect x="64" y="76" width="4.6" height="5" fill="#d2a860"/>' +
        '<path d="M43 52H57L58 66L50 70L42 66Z" fill="#a8704c"/><path d="M42 62L50 70L58 62" stroke="#14363c" stroke-width="3" fill="none"/>' +
        head(u, 50, 38, 12.4, 14.6, '#2a1008') + '<ellipse cx="37.8" cy="40" rx="1.8" ry="3" fill="#c88a64"/><ellipse cx="62.2" cy="40" rx="1.8" ry="3" fill="#9a6444"/>' +
        '<path d="M37 33C36 22 44 18 52 19C60 20 64 26 63 33C61 29 58 27 51 27C45 27 40 29 37 33Z" fill="#5a2a14"/><path d="M38 26C42 20 54 19 61 24" fill="none" stroke="#b86a34" stroke-width="1" stroke-linecap="round"/>' +
        '<path d="M36 31H64" stroke="#2a1c10" stroke-width="3.4" stroke-linecap="round"/><circle cx="43" cy="31" r="4.6" fill="#0c2a30" stroke="#d2a860" stroke-width="1.4"/><circle cx="57" cy="31" r="4.6" fill="#0c2a30" stroke="#d2a860" stroke-width="1.4"/><circle cx="43" cy="31" r="3" fill="#4ad8e4" fill-opacity=".75"/><circle cx="57" cy="31" r="3" fill="#4ad8e4" fill-opacity=".75"/><path d="M41.4 29.6L43.4 29.2M55.4 29.6L57.4 29.2" stroke="#fff" stroke-width=".7"/>' +
        '<path d="M42 38.4L47 38M53 38L58 38.4" stroke="#2a1208" stroke-width="1.3" stroke-linecap="round"/><circle cx="44.6" cy="41.4" r=".9" fill="#20120a"/><circle cx="55.4" cy="41.4" r=".9" fill="#20120a"/>' +
        '<path d="M50 42L48.8 47Q50 48 51.2 47" fill="none" stroke="#7e4a30" stroke-width=".8"/><path d="M45.6 51Q50 52.4 54.4 51" fill="none" stroke="#7a3a2a" stroke-width="1.1" stroke-linecap="round"/><path d="M46 49.6l.8.6M53 49.6l-.8.6" stroke="#7a3a2a" stroke-width=".4"/>' +
        rim('M38 24C42 19 50 18 56 19', '#bff8fb', .9) + rim('M8 94C10 80 22 70 36 66', '#7fe8f0', 1, .7); } },
    { id: 'tecnologico', nome: 'Figura tecnologica', bg: ['#16262e', '#04080a'], svg: function (u) {
      return '<defs>' + lgd(u + 'ti', '#aebcc6', '#3a4a54', 1, 1) + lgd(u + 'ti2', '#6a7c88', '#222e36', 0.4, 1) + rg(u + 'vz', 0.5, 0.45, 0.5, '#35d0e8', 0.7, 0) + '</defs>' +
        '<g stroke="#35d0e8" stroke-opacity=".25" stroke-width=".5" fill="none"><path d="M0 20H30V34H14M100 30H74V44H88M0 62H20V74"/><circle cx="14" cy="34" r="1.4"/><circle cx="88" cy="44" r="1.4"/></g>' +
        '<path d="M2 100C2 80 14 70 30 66L38 62H62L70 66C86 70 98 80 98 100Z" fill="url(#' + u + 'ti2)"/><path d="M2 100C2 82 10 74 22 70L30 76L26 100Z" fill="url(#' + u + 'ti)" stroke="#d6e2ea" stroke-width=".7"/><path d="M98 100C98 82 90 74 78 70L70 76L74 100Z" fill="url(#' + u + 'ti)" stroke="#d6e2ea" stroke-width=".7"/>' +
        '<path d="M36 64L50 80L64 64" fill="#0a1216" stroke="#35d0e8" stroke-width=".8"/><path d="M42 70H58M44 76H56" stroke="#35d0e8" stroke-width=".7" stroke-opacity=".8"/><circle cx="50" cy="86" r="4" fill="#0a1216" stroke="#35d0e8" stroke-width="1"/><circle cx="50" cy="86" r="1.8" fill="#8ff3ff"/>' +
        '<path d="M40 54H60L62 66H38Z" fill="#26343c" stroke="#8a9ca6" stroke-width=".6"/><path d="M42 58H58M42 62H58" stroke="#000" stroke-opacity=".5" stroke-width=".7"/>' +
        '<path d="M28 40C28 20 38 10 50 10C62 10 72 20 72 40V52C72 58 66 62 60 62H40C34 62 28 58 28 52Z" fill="url(#' + u + 'ti)"/><path d="M50 10C62 10 72 20 72 40V52C72 58 66 62 60 62H50Z" fill="#000" fill-opacity=".28"/>' +
        '<path d="M50 10V30" stroke="#2a3a44" stroke-width="2.4"/><path d="M34 36H66C68 36 69 38 69 41V44C69 48 66 50 63 50H37C34 50 31 48 31 44V41C31 38 32 36 34 36Z" fill="#04090c"/><rect x="35" y="39.6" width="30" height="4.2" rx="2.1" fill="url(#' + u + 'vz)" /><rect x="35" y="39.6" width="30" height="4.2" rx="2.1" fill="#35d0e8"/><rect x="40" y="40.4" width="12" height="1.2" fill="#d8ffff"/>' +
        '<path d="M30 30C32 20 40 13 50 12" fill="none" stroke="#e8f2f8" stroke-width="1" stroke-linecap="round"/><path d="M33 52L40 60M67 52L60 60" stroke="#2a3a44" stroke-width="1"/><path d="M26 44V34M74 44V34" stroke="#d6e2ea" stroke-width="2.4" stroke-linecap="round"/>' +
        rim('M8 96C9 84 14 76 22 72', '#9ff0ff', 1, .8); } },
    { id: 'mistico', nome: 'Figura mistica', bg: ['#34163f', '#0a0410'], svg: function (u) {
      return '<defs>' + skin(u, '#d8b8d8', '#8a608e') + lgd(u + 'ro', '#6a2a8a', '#1c0a2a', 0.2, 1) + rg(u + 'ar', 0.5, 0.3, 0.55, '#d890ff', 0.6, 0) + '</defs>' +
        '<circle cx="50" cy="34" r="38" fill="url(#' + u + 'ar)"/>' +
        '<g fill="none" stroke="#e8c4ff"><circle cx="50" cy="32" r="31" stroke-width=".9" stroke-opacity=".7"/><circle cx="50" cy="32" r="26" stroke-width=".6" stroke-opacity=".5" stroke-dasharray="1.5 2.5"/><path d="M50 3L77 49H23Z" stroke-width=".7" stroke-opacity=".55"/><path d="M50 61L23 15H77Z" stroke-width=".7" stroke-opacity=".55"/></g>' +
        '<path d="M2 100C6 76 22 66 38 62H62C78 66 94 76 98 100Z" fill="url(#' + u + 'ro)"/><path d="M38 62L50 100L62 62L58 100H42Z" fill="#12061c"/><path d="M38 62L48 96M62 62L52 96" stroke="#d890ff" stroke-width=".8" stroke-opacity=".8"/><path d="M44 78H56M45 84H55" stroke="#e8c4ff" stroke-width=".6"/>' +
        '<path d="M44 52H56L57 63Q50 68 43 63Z" fill="#9a6a9a"/>' +
        '<path d="M26 56C24 34 30 12 50 10C70 12 76 34 74 56C70 44 66 34 60 30L40 30C34 34 30 44 26 56Z" fill="url(#' + u + 'ro)"/>' +
        head(u, 50, 40, 11.8, 14.4, '#2a0a30') + '<path d="M38 34C44 28 56 28 62 34C58 30 54 29 50 29C46 29 42 30 38 34Z" fill="#1c0a2a"/>' +
        '<path d="M42 38.6Q45 37 48 38.6M52 38.6Q55 37 58 38.6" fill="none" stroke="#2a0a30" stroke-width="1.2" stroke-linecap="round"/><path d="M43.4 40.2Q45.5 41.2 47.6 40.2M52.4 40.2Q54.5 41.2 56.6 40.2" stroke="#e8a0ff" stroke-width="1" fill="none" stroke-linecap="round"/>' +
        '<path d="M50 41L49 46Q50 47 51 46" fill="none" stroke="#6a3a6a" stroke-width=".8"/><path d="M46.4 50Q50 51 53.6 50" fill="none" stroke="#7a2a5a" stroke-width="1.1" stroke-linecap="round"/>' +
        '<path d="M50 30L52 33L50 36L48 33Z" fill="#ffd8ff" stroke="#e8a0ff" stroke-width=".5"/>' +
        '<circle cx="24" cy="30" r="1.4" fill="#f0d0ff"/><circle cx="78" cy="22" r="1" fill="#f0d0ff"/><circle cx="84" cy="52" r="1.6" fill="#f0d0ff"/>' +
        rim('M26 54C24 34 30 14 48 10', '#f0d0ff', 1) + rim('M6 96C9 80 20 70 34 65', '#e8a0ff', .9, .7); } },
    { id: 'astratto', nome: 'Silhouette astratta', bg: ['#2c261c', '#0a0806'], svg: function (u) {
      return '<defs>' + lgd(u + 'f1', '#f2d9a8', '#9a7440', 1, 1) + lgd(u + 'f2', '#b08a54', '#4a3418', 0.2, 1) + lgd(u + 'f3', '#6a4c26', '#1e140a', 0.5, 1) + '</defs>' +
        '<path d="M0 100L50 4L100 100" fill="none" stroke="#D2B184" stroke-width=".5" stroke-opacity=".25"/><circle cx="50" cy="40" r="36" fill="none" stroke="#D2B184" stroke-width=".5" stroke-opacity=".3"/>' +
        '<path d="M50 14L66 24L70 42L60 58L50 62L40 58L30 42L34 24Z" fill="url(#' + u + 'f2)"/>' +
        '<path d="M50 14L66 24L50 36Z" fill="url(#' + u + 'f1)"/><path d="M34 24L50 14L50 36Z" fill="#f8e6c0"/><path d="M66 24L70 42L50 36Z" fill="#b8905a"/><path d="M34 24L50 36L30 42Z" fill="#d8b478"/><path d="M30 42L50 36L40 58Z" fill="#9a7440"/><path d="M70 42L60 58L50 36Z" fill="#6a4c26"/><path d="M40 58L50 36L60 58L50 62Z" fill="#3a2812"/>' +
        '<path d="M42 58L58 58L62 72L38 72Z" fill="#7a5a30"/><path d="M42 58L50 66L58 58" fill="#d8b478" fill-opacity=".6"/>' +
        '<path d="M4 100L22 78L38 70L50 100Z" fill="url(#' + u + 'f1)"/><path d="M50 100L38 70L62 70Z" fill="url(#' + u + 'f3)"/><path d="M96 100L78 78L62 70L50 100Z" fill="url(#' + u + 'f3)"/><path d="M22 78L38 70L30 100L4 100Z" fill="#f2d9a8" fill-opacity=".5"/><path d="M96 100L78 78L84 100Z" fill="#000" fill-opacity=".35"/>' +
        '<path d="M50 14V62M30 42H70M34 24L60 58M66 24L40 58" stroke="#fff4d8" stroke-width=".35" stroke-opacity=".5" fill="none"/>' +
        rim('M34 24L50 14L66 24', '#fff4d8', 1) + '<path d="M44 40H56" stroke="#1e140a" stroke-width="1.6" stroke-linecap="round" stroke-opacity=".0"/>'; } },
    { id: 'cronista', nome: 'Cronista degli Archivi', bg: ['#17382f', '#040e0b'], svg: function (u) {
      return '<defs>' + skin(u, '#f0d0a8', '#b08258') + lgd(u + 'jk', '#3f7a66', '#10302a', 0.3, 1) + rg(u + 'la', 0.8, 0.5, 0.45, '#ffc060', 0.55, 0) + '</defs>' +
        '<circle cx="80" cy="46" r="26" fill="url(#' + u + 'la)"/><path d="M70 36H92V74H70Z" fill="#1c1208" stroke="#D2B184" stroke-width=".7"/><path d="M74 42H88M74 48H88M74 54H84M74 60H88" stroke="#D2B184" stroke-width=".6" stroke-opacity=".8"/>' +
        '<g fill="#0e2a24" stroke="#D2B184" stroke-width=".5"><rect x="4" y="52" width="9" height="30"/><rect x="13" y="58" width="7" height="24"/><rect x="20" y="48" width="8" height="34"/></g>' +
        '<path d="M2 100C4 78 20 68 38 64H62C80 68 96 78 98 100Z" fill="url(#' + u + 'jk)"/><path d="M38 64L50 100L62 64L74 70L66 100H34L26 70Z" fill="#2c1c0c"/><path d="M30 68C40 80 60 80 70 68L72 78C60 88 40 88 28 78Z" fill="#a8362a"/><path d="M34 78L32 100H44L42 84Z" fill="#8a2a20"/><path d="M30 68C40 80 60 80 70 68" fill="none" stroke="#e08a6a" stroke-width=".7"/>' +
        '<path d="M43 52H57L58 66Q50 72 42 66Z" fill="#a8784c"/>' +
        head(u, 50, 39, 12.6, 15, '#2a1008') + '<ellipse cx="37.6" cy="41" rx="1.9" ry="3.2" fill="#c8946a"/><ellipse cx="62.4" cy="41" rx="1.9" ry="3.2" fill="#9a6a44"/>' +
        '<path d="M37 36C34 24 42 17 51 17C60 17 66 24 63 36C61 30 58 26 51 26C45 26 40 30 37 36Z" fill="#a8a8b0"/><path d="M38 24C44 18 56 17 62 22" fill="none" stroke="#e8e8f0" stroke-width="1" stroke-linecap="round"/><path d="M37 36C35 40 36 46 38 48" fill="none" stroke="#a8a8b0" stroke-width="1.6"/>' +
        '<path d="M41 36.6L46.4 36.2M53.6 36.2L59 36.6" stroke="#6a6a72" stroke-width="1.4" stroke-linecap="round"/>' +
        '<circle cx="44.6" cy="40.4" r="5" fill="#fff" fill-opacity=".1" stroke="#D2B184" stroke-width="1.1"/><circle cx="55.4" cy="40.4" r="5" fill="#fff" fill-opacity=".1" stroke="#D2B184" stroke-width="1.1"/><path d="M49.6 40H50.4" stroke="#D2B184" stroke-width="1"/><path d="M39.6 39.6L37.6 38.8M60.4 39.6L62.4 38.8" stroke="#D2B184" stroke-width=".9"/><circle cx="44.8" cy="40.6" r=".9" fill="#20120a"/><circle cx="55.6" cy="40.6" r=".9" fill="#20120a"/><path d="M42 38.4L45 37.6" stroke="#fff" stroke-width=".6" stroke-opacity=".8"/>' +
        '<path d="M50 42L48.8 47Q50 48 51.2 47" fill="none" stroke="#7e4a30" stroke-width=".8"/><path d="M45 50.6Q50 54.4 55 50.6" fill="none" stroke="#7a3a2a" stroke-width="1.1" stroke-linecap="round"/><path d="M46 52Q50 57 54 52Q50 55 46 52Z" fill="#c8c8d0"/>' +
        '<path d="M14 98L24 74" stroke="#efe4c9" stroke-width="1.6" stroke-linecap="round"/><path d="M24 74L27 70L25 76Z" fill="#efe4c9"/><path d="M14 98C16 92 18 88 20 84" stroke="#a8362a" stroke-width="1.2" stroke-linecap="round"/>' +
        rim('M38 22C44 17 52 16 58 17', '#fff0d0', .9) + rim('M6 96C9 80 22 70 36 66', '#ffc060', 1, .7); } },
    { id: 'sentinella', nome: 'Sentinella', bg: ['#3a1018', '#0b0305'], svg: function (u) {
      return '<defs>' + lgd(u + 'ar', '#c9a35a', '#5a3e18', 1, 1) + lgd(u + 'ar2', '#8a2a32', '#2a0a10', 0.3, 1) + rg(u + 'cr', 0.5, 0.5, 0.5, '#ff5060', 0.45, 0) + '</defs>' +
        '<circle cx="50" cy="42" r="36" fill="url(#' + u + 'cr)"/>' +
        '<path d="M0 100C0 82 8 72 22 66L34 62H66L78 66C92 72 100 82 100 100Z" fill="url(#' + u + 'ar2)"/>' +
        '<path d="M0 100C0 86 6 76 16 70L30 74L32 100Z" fill="url(#' + u + 'ar)" stroke="#2a1a08" stroke-width=".8"/><path d="M100 100C100 86 94 76 84 70L70 74L68 100Z" fill="url(#' + u + 'ar)" stroke="#2a1a08" stroke-width=".8"/><path d="M6 86H28M72 86H94M8 92H30M70 92H92" stroke="#2a1a08" stroke-width=".7"/>' +
        '<path d="M38 64L50 98L62 64" fill="#1a080c" stroke="#c9a35a" stroke-width=".8"/><path d="M50 70V92M44 78H56" stroke="#e8c46a" stroke-width="1.1"/><path d="M50 72L54 78L50 84L46 78Z" fill="#d83a48"/>' +
        '<path d="M40 56H60L62 66L50 70L38 66Z" fill="url(#' + u + 'ar)" stroke="#2a1a08" stroke-width=".7"/>' +
        '<path d="M50 2C54 2 56 8 56 14L58 22H42L44 14C44 8 46 2 50 2Z" fill="url(#' + u + 'ar2)" stroke="#2a1a08" stroke-width=".6"/><path d="M50 4V20" stroke="#e8c46a" stroke-width="1.2"/>' +
        '<path d="M30 40C30 22 38 14 50 14C62 14 70 22 70 40V54C70 60 64 64 58 64H42C36 64 30 60 30 54Z" fill="url(#' + u + 'ar)" stroke="#2a1a08" stroke-width=".9"/><path d="M50 14C62 14 70 22 70 40V54C70 60 64 64 58 64H50Z" fill="#000" fill-opacity=".3"/>' +
        '<path d="M32 38H68V46L50 52L32 46Z" fill="#12060a"/><path d="M32 38H68" stroke="#e8c46a" stroke-width="1"/><path d="M50 38V52" stroke="#c9a35a" stroke-width="1.6"/><path d="M37 42L46 43.4L46 45.6L38 45Z" fill="#ff4a5a"/><path d="M63 42L54 43.4L54 45.6L62 45Z" fill="#ff4a5a"/>' +
        '<path d="M42 54L46 62M50 54V63M58 54L54 62" stroke="#2a1a08" stroke-width="1.2"/>' +
        '<path d="M31 36C32 24 38 17 47 15" fill="none" stroke="#fff0c0" stroke-width="1" stroke-linecap="round"/>' + rim('M3 96C5 84 10 76 18 71', '#ffd890', 1, .8); } }
  ];
  var AV_BY = {}; AVATARS.forEach(function (a) { AV_BY[a.id] = a; });

  /* ---------- glifi dei distintivi (geometrici, non emoji) ---------- */
  var GL = {
    'primo-passo': '<path d="M-6 6L0-6L6 6M-6 12L0 0L6 12"/>', 'linea-sacra': '<path d="M-10 0H10"/><circle cx="0" cy="0" r="3.6"/>',
    'cacciatore-varianti': '<circle r="7"/><path d="M0-11V-4M0 4V11M-11 0H-4M4 0H11"/>', 'archivista': '<path d="M-9-7H0V8H-9ZM0-7H9V8H0Z"/>',
    'essenziale': '<path d="M0-10L8 0L0 10L-8 0Z"/><path d="M0-4V4M-4 0H4"/>', 'nessuna-divergenza': '<path d="M0 0C-4-7-10-7-10 0C-10 7-4 7 0 0C4-7 10-7 10 0C10 7 4 7 0 0Z"/>',
    'cinefilo': '<rect x="-10" y="-7" width="20" height="14" rx="1.5"/><path d="M-5-7V7M5-7V7M-10-2H-5M-10 2H-5M5-2H10M5 2H10"/>', 'maratoneta': '<path d="M-5-8L8 0L-5 8Z"/>',
    'collezionista': '<rect x="-8" y="-8" width="12" height="12"/><path d="M-4 8H8V-4"/>', 'weekend-guerriero': '<circle r="4.2"/><path d="M0-10V-7M0 7V10M-10 0H-7M7 0H10M-7-7L-5-5M5 5L7 7M7-7L5-5M-5 5L-7 7"/>',
    'meta-strada': '<path d="M-10 5A10 10 0 0 1 10 5M-10 5H10M0 5L5-5"/>', 'critico': '<path d="M0-10L3 -3L10-3L4.5 2L6.5 9L0 5L-6.5 9L-4.5 2L-10-3L-3-3Z"/>',
    'preferiti': '<path d="M0 9C-12-1-8-9 0-4C8-9 12-1 0 9Z"/>', 'cronista': '<path d="M-7 9L-3 8L8-4L5-8L-6 4Z"/><path d="M-3 8L-7 9"/>'
  };
  function glyph(id) { return GL[id] || '<circle r="6"/>'; }
  function medal(id, cx, cy, r, acc) {
    return '<g transform="translate(' + n1(cx) + ' ' + n1(cy) + ')"><circle r="' + r + '" fill="rgba(0,0,0,0.35)" stroke="' + acc + '" stroke-width="' + n1(Math.max(1.6, r / 14)) + '"/><circle r="' + n1(r - r / 7) + '" fill="none" stroke="' + acc + '" stroke-opacity=".35" stroke-width="1"/>' +
      '<g transform="scale(' + n1(r / 17) + ')" fill="none" stroke="' + acc + '" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">' + glyph(id) + '</g></g>';
  }

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
  function corners(W_, H_, m, fn, sc) { sc = sc || 1; var s = '', i, c = [[1, 1], [-1, 1], [1, -1], [-1, -1]]; for (i = 0; i < 4; i++) s += '<g transform="translate(' + (c[i][0] > 0 ? m : W_ - m) + ' ' + (c[i][1] > 0 ? m : H_ - m) + ') scale(' + c[i][0] * sc + ' ' + c[i][1] * sc + ')">' + fn(i) + '</g>'; return s; }
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
      /* 3.2.5: identita' istituzionale: filo interno, targhetta centrale con rivetti, tacche di registro agli angoli */
      var inst = rr(W_, H_, 19.5, 0.7, g, 4, ' stroke-opacity=".5"');
      [[W_ / 2, 14, 1], [W_ / 2, H_ - 14, -1]].forEach(function (q) { inst += '<g transform="translate(' + q[0] + ' ' + q[1] + ') scale(1 ' + q[2] + ')"><path d="M-30 0H30L24 9H-24Z" fill="#1a1308" stroke="' + g + '" stroke-width="1.4"/><circle cx="-16" cy="3.4" r="1.3" fill="' + g + '"/><circle cx="16" cy="3.4" r="1.3" fill="' + g + '"/><path d="M-6 3.4H6" stroke="' + g + '" stroke-width="1.6" stroke-linecap="round"/></g>'; });
      return inst + plate(W_, H_, 14, 7, 0.35, 7) + rr(W_, H_, 14, 1.8, g, 7) + corners(W_, H_, 14, function () { return '<path d="M0 22V7a7 7 0 0 1 7-7H22" fill="none" stroke="' + g + '" stroke-width="3.6"/>'; });
    },
    /* 02 - bronzo scuro lavorato: sagoma smussata massiccia, bordo largo satinato, giunti e placche meccaniche, ingranaggi */
    'cornice-bronzo-temporale': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'br', [[0, '#d68a40'], [0.5, '#8e5420'], [1, '#4a280e']], 0, 0, 1, 1) + '</defs>', hi = '#f0b878', s = d;
      s += poly(cham(W_, H_, 17, 26), 'none', '#000', 20, ' stroke-opacity=".55"') + poly(cham(W_, H_, 17, 26), 'none', 'url(#' + u + 'br)', 15);
      s += poly(cham(W_, H_, 24, 22), 'none', hi, 1, ' stroke-opacity=".6"') + poly(cham(W_, H_, 10, 30), 'none', '#2a1406', 1, ' stroke-opacity=".7"');
      s += edgeRun(W_, H_, 17, 46, function (x, y, v, e) { return '<rect x="' + n1(x - 7) + '" y="' + n1(y - 3.4) + '" width="14" height="6.8" rx="1.5" transform="' + (v ? 'rotate(90 ' + n1(x) + ' ' + n1(y) + ')' : '') + '" fill="#2a1406" stroke="' + hi + '" stroke-width=".8"/>'; }, 64);
      s += corners(W_, H_, 14, function () { return '<rect x="-3" y="-3" width="34" height="34" rx="3" fill="url(#' + u + 'br)" stroke="#2c1706" stroke-width="1.4"/><path d="M4 4H24V24" fill="none" stroke="' + hi + '" stroke-width=".9" stroke-opacity=".6"/><circle cx="8" cy="8" r="2.2" fill="#2c1706"/><circle cx="24" cy="8" r="2.2" fill="#2c1706"/><circle cx="8" cy="24" r="2.2" fill="#2c1706"/><circle cx="24" cy="24" r="2.2" fill="#2c1706"/>';; }, 0.8);
      return s + gear(W_ / 2, 17, 9, 8, hi, '#3a2008') + gear(W_ / 2, H_ - 17, 9, 8, hi, '#3a2008') + gear(17, H_ / 2, 7, 8, hi, '#3a2008') + gear(W_ - 17, H_ / 2, 7, 8, hi, '#3a2008');
    },
    /* 03 - acciaio argentato di precisione: ghiera cronografica a blocchi alternati (alta frequenza), anelli concentrici, quadranti agli angoli */
    'cornice-argento-cronologico': function (W_, H_, u) {
      var a = '#d3dde8', a2 = '#7f8da0', d = '<defs>' + lg(u + 'ag', [[0, '#f4f8fc'], [0.5, '#aab7c7'], [1, '#5d6b7c']], 0, 0, 1, 1) + '</defs>';
      var s = d + plate(W_, H_, 17, 24, 0.45, 22) + rr(W_, H_, 17, 11, 'url(#' + u + 'ag)', 22) + rr(W_, H_, 17, 11, '#0d1218', 22, ' stroke-dasharray="4.5 4.5" stroke-opacity=".62"') + rr(W_, H_, 11, 1.2, a, 26) + rr(W_, H_, 23.5, 1.2, a, 17) + rr(W_, H_, 27.5, 0.7, a2, 15, ' stroke-dasharray="1 3"');
      s += corners(W_, H_, 0, function () { var t = '', k; for (k = 0; k < 12; k++) { var an = Math.PI / 6 * k; t += '<path d="M' + n1(18 + Math.cos(an) * 10) + ' ' + n1(18 + Math.sin(an) * 10) + 'L' + n1(18 + Math.cos(an) * 13) + ' ' + n1(18 + Math.sin(an) * 13) + '" stroke="' + a + '" stroke-width="1"/>'; } return '<circle cx="18" cy="18" r="14.5" fill="#0d1218" stroke="url(#' + u + 'ag)" stroke-width="2.6"/>' + t + '<path d="M18 18V9M18 18L24 21" stroke="' + a + '" stroke-width="1.6" stroke-linecap="round"/><circle cx="18" cy="18" r="1.6" fill="' + a + '"/>'; });
      return s;
    },
    /* 04 - oro inciso con filigrana: doppio bordo, tralcio continuo a volute tra i fili, fioroni a spirale agli angoli, cartigli centrali */
    'cornice-oro-archivista': function (W_, H_, u) {
      var g = 'url(#' + u + 'go)', d = '<defs>' + lg(u + 'go', [[0, '#fbe9ae'], [0.5, '#d9ad4e'], [1, '#98702a']], 0, 0, 1, 1) + '</defs>', s = d + plate(W_, H_, 16, 15, 0.4, 6) + rr(W_, H_, 12, 4.4, g, 6) + rr(W_, H_, 25, 1.3, '#f3d98b', 3);
      var vine = function (x1, y1, x2, y2) { var len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len, dd = 'M' + n1(x1) + ' ' + n1(y1), t, o = ''; for (t = 0; t <= len; t += 2) { var off = Math.sin(t / 4.6) * 3.4; dd += 'L' + n1(x1 + ux * t - uy * off) + ' ' + n1(y1 + uy * t + ux * off); } for (t = 10; t < len - 6; t += 29) { o += '<circle cx="' + n1(x1 + ux * t + uy * 4.2) + '" cy="' + n1(y1 + uy * t - ux * 4.2) + '" r="1.6" fill="#f3d98b"/>'; } return '<path d="' + dd + '" fill="none" stroke="#f3d98b" stroke-width="1.15"/>' + o; };
      s += vine(46, 18.5, W_ - 46, 18.5) + vine(46, H_ - 18.5, W_ - 46, H_ - 18.5) + vine(18.5, 46, 18.5, H_ - 46) + vine(W_ - 18.5, 46, W_ - 18.5, H_ - 46);
      s += corners(W_, H_, 12, function () { return '<path d="M2 36C2 16 16 2 36 2" fill="none" stroke="' + g + '" stroke-width="3.6"/><path d="M9 30C9 18 18 9 30 9" fill="none" stroke="#f3d98b" stroke-width="1.2"/><path d="M13 13m-5 0a5 5 0 1 1 10 0a3.4 3.4 0 1 1-6.8 0a1.8 1.8 0 1 1 3.6 0" fill="none" stroke="' + g + '" stroke-width="1.5"/><path d="M24 6c5 1 8 4 8 9-4-1-7-4-8-9zM6 24c1 5 4 8 9 8-1-4-4-7-9-8z" fill="' + g + '" stroke="#5a4012" stroke-width=".5"/>'; }, 0.82);
      [[W_ / 2, 12, 1], [W_ / 2, H_ - 12, -1]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ') scale(1 ' + q[2] + ')"><path d="M-26 0C-16 0-12 9 0 9C12 9 16 0 26 0" fill="none" stroke="' + g + '" stroke-width="2.6"/><path d="M0 3C-6 3-6 12 0 12C6 12 6 3 0 3" fill="#1a1006" stroke="#f3d98b" stroke-width="1.1"/></g>'; });
      return s;
    },
    /* 05 - acciaio scuro e graffiato: angoli asimmetrici, tre incisioni diagonali evidenti */
    'cornice-acciaio-mutante': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'st', [[0, '#8c97a2'], [0.5, '#3a4149'], [1, '#6c7782']], 0, 0, 1, 1) + '</defs>', r = rng(5), s = d + rr(W_, H_, 14, 12, '#000', 1, ' stroke-opacity=".5"') + rr(W_, H_, 14, 8, 'url(#' + u + 'st)', 1) + rr(W_, H_, 9.8, 0.8, '#c3ccd5', 0, ' stroke-opacity=".5"'), i;
      for (i = 0; i < 38; i++) { var x = 30 + r() * (W_ - 60), y = r() > 0.5 ? 12 + r() * 4 : H_ - 16 + r() * 4, l = 5 + r() * 12; s += pth('M' + n1(x) + ' ' + n1(y) + 'l' + n1(l) + ' ' + n1(-l * 0.5), '#dfe5ea', 0.7, ' stroke-opacity="' + n1(0.15 + r() * 0.3) + '"'); }
      s += '<path d="M14 62V26L26 14H62" fill="none" stroke="#000" stroke-width="15" stroke-opacity=".45"/><path d="M14 62V26L26 14H62" fill="none" stroke="url(#' + u + 'st)" stroke-width="10" stroke-linejoin="miter"/>';
      s += '<path d="M' + (W_ - 14) + ' ' + (H_ - 40) + 'V' + (H_ - 14) + 'H' + (W_ - 40) + '" fill="none" stroke="url(#' + u + 'st)" stroke-width="10"/>';
      /* 3.2.5: materiale: venature di spazzolatura sulle staffe, bulloni a testa esagonale e linee di giunzione */
      var hxb = function (x, y) { var q = [], j; for (j = 0; j < 6; j++) q.push([x + Math.cos(Math.PI / 3 * j) * 4.6, y + Math.sin(Math.PI / 3 * j) * 4.6]); return poly(q, '#2b333b', '#d9e1e8', 0.9) + '<circle cx="' + x + '" cy="' + y + '" r="1.3" fill="#9aa6b1"/>'; };
      s += hxb(22, 22) + hxb(W_ - 22, H_ - 22) + hxb(22, 54) + hxb(W_ - 54, H_ - 22) + hxb(54, 22) + hxb(W_ - 22, H_ - 54);
      [[0, 3.4], [15, 2.6], [30, 1.8]].forEach(function (k) { s += pth('M' + (W_ - 56 + k[0]) + ' 4L' + (W_ - 4) + ' ' + (56 - k[0] + 0) + '', '#000', k[1] + 3, ' stroke-opacity=".5"').replace('L' + (W_ - 4), 'L' + (W_ - 4 - 0)); });
      [[0, 3.4], [15, 2.6], [30, 1.8]].forEach(function (k) { s += pth('M' + n1(W_ - 74 + k[0]) + ' 6L' + n1(W_ - 18 + k[0] * 0.0) + ' ' + n1(62 - 0 + 0) + '', '#eef3f7', k[1], ' stroke-linecap="round"').replace(/M[^L]*L[^"]*/, 'M' + n1(W_ - 20 - k[0] * 0.9) + ' 6L' + n1(W_ - 80 - k[0] * 0.9) + ' 66'); });
      return s;
    },
    /* 06 - cristallo mistico: banda di vetro viola sfaccettato, schegge-cristallo agli angoli, rune, sigilli a esagramma */
    'cornice-energia-arcana': function (W_, H_, u) {
      var v = '#b57ef0', p = '#e2cbff', d = '<defs>' + lg(u + 'c1', [[0, '#d8b4ff'], [1, '#6a34b8']], 0, 0, 1, 1) + lg(u + 'c2', [[0, '#9a64e0'], [1, '#2a1052']], 1, 0, 0, 1) + '</defs>', s = d + plate(W_, H_, 17, 20, 0.4, 4) + rr(W_, H_, 17, 12, v, 4, ' stroke-opacity=".18"') + rr(W_, H_, 14, 1.8, v, 4) + rr(W_, H_, 21, 1.4, p, 2, ' stroke-dasharray="7 3 2 3" stroke-opacity=".85"');
      var rune = ['M0 -4V4M0 -1L3 -4M0 2L3 -1', 'M-2 -4L2 0L-2 4M2 -4V4', 'M-3 -4L3 4M3 -4L-3 4', 'M-2 4V-4L2 0L-2 0', 'M0 -4L3 0L0 4L-3 0Z', 'M-3 -3H3L-3 3H3'];
      s += edgeRun(W_, H_, 17.5, 15, function (x, y, v2, e, k) { return '<path transform="translate(' + n1(x) + ' ' + n1(y) + ')" d="' + rune[Math.round(k / 15) % 6] + '" fill="none" stroke="' + p + '" stroke-width="1.1" stroke-linecap="round"/>'; }, 62);
      s += corners(W_, H_, 10, function () { return '<path d="M0 0L34 4L22 22Z" fill="url(#' + u + 'c1)" stroke="' + p + '" stroke-width=".9"/><path d="M0 0L22 22L4 34Z" fill="url(#' + u + 'c2)" stroke="' + p + '" stroke-width=".9"/><path d="M22 22L34 4L38 24Z" fill="' + v + '" fill-opacity=".55" stroke="' + p + '" stroke-width=".7"/><path d="M22 22L4 34L24 38Z" fill="#4a2086" fill-opacity=".8" stroke="' + p + '" stroke-width=".7"/><path d="M0 0L22 22" stroke="#fff" stroke-width=".8" stroke-opacity=".7"/>'; }, 0.8);
      [[W_ / 2, 17], [W_ / 2, H_ - 17], [17, H_ / 2], [W_ - 17, H_ / 2]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ')"><path d="M0-14L11 0 0 14-11 0Z" fill="#12081c" stroke="' + v + '" stroke-width="1.6"/><path d="M0-8L6.9 4H-6.9ZM0 8L6.9-4H-6.9Z" fill="none" stroke="' + p + '" stroke-width="1.1"/></g>'; });
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
    /* 09 - monumentale e solenne: fascia d'oro antico chiaro con intreccio nordico, merlatura continua, torri angolari, archi */
    'cornice-asgard': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'as', [[0, '#f6e4a2'], [0.5, '#c9a352'], [1, '#7c5a26']], 0, 0, 1, 1) + '</defs>', a = '#e8cf86', s = d + plate(W_, H_, 17, 16, 0.5, 0) + rr(W_, H_, 17, 9, 'url(#' + u + 'as)', 0) + rr(W_, H_, 12.8, 0.9, '#fff0c0', 0, ' stroke-opacity=".8"');
      var wave = function (x1, y1, x2, y2) { var len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len, o = '', k; for (k = 0; k < 2; k++) { var dd = 'M' + n1(x1) + ' ' + n1(y1), t; for (t = 0; t <= len; t += 3) { var off = Math.sin((t / 9) + (k ? Math.PI : 0)) * 2.6; dd += 'L' + n1(x1 + ux * t - uy * off) + ' ' + n1(y1 + uy * t + ux * off); } o += '<path d="' + dd + '" fill="none" stroke="' + (k ? '#2a1c08' : '#fff6cc') + '" stroke-width="1.3"/>'; } return o; };
      s += wave(46, 17, W_ - 46, 17) + wave(46, H_ - 17, W_ - 46, H_ - 17) + wave(17, 46, 17, H_ - 46) + wave(W_ - 17, 46, W_ - 17, H_ - 46);
      var mer = '', x, y; for (x = 52; x < W_ - 52; x += 15) { mer += '<rect x="' + x + '" y="22" width="9" height="7"/><rect x="' + x + '" y="' + (H_ - 29) + '" width="9" height="7"/>'; } for (y = 52; y < H_ - 52; y += 15) { mer += '<rect x="22" y="' + y + '" width="7" height="9"/><rect x="' + (W_ - 29) + '" y="' + y + '" width="7" height="9"/>'; }
      s += '<g fill="url(#' + u + 'as)" stroke="#2a1c08" stroke-width=".7">' + mer + '</g>';
      s += corners(W_, H_, 8, function () { return '<rect x="0" y="8" width="32" height="26" fill="url(#' + u + 'as)" stroke="#2a1c08" stroke-width="1.2"/><path d="M0 8V0H6V4H10V0H16V4H20V0H26V4H30V0H32V8Z" fill="url(#' + u + 'as)" stroke="#2a1c08" stroke-width="1"/><path d="M10 14L16 28L22 14M10 24H22" fill="none" stroke="#2a1c08" stroke-width="2"/>'; }, 0.9);
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
      var cr = '#ff3d57', dk = '#6b2e36', s = '<defs>' + rg(u + 'rg', 0.5, 0.5, 0.5, '#ff2d4a', 0.5, 0) + '</defs>', cps = [[24, 22], [W_ - 22, H_ * 0.55], [W_ * 0.86, H_ - 15], [W_ - 24, 24]];
      cps.forEach(function (q) { s += '<circle cx="' + q[0] + '" cy="' + q[1] + '" r="34" fill="url(#' + u + 'rg)"/>'; });
      var seg = function (x1, y1, x2, y2, cuts) { var len = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / len, uy = (y2 - y1) / len, pts = [0].concat(cuts.map(function (c) { return c * len; })).concat([len]), o = '', i; for (i = 0; i < pts.length - 1; i++) { var a = pts[i] + (i ? 5 : 0), b2 = pts[i + 1] - (i < pts.length - 2 ? 5 : 0), off = i % 2 ? 4 : -2; o += '<path d="M' + n1(x1 + ux * a - uy * off) + ' ' + n1(y1 + uy * a + ux * off) + 'L' + n1(x1 + ux * b2 - uy * off) + ' ' + n1(y1 + uy * b2 + ux * off) + '" stroke="#000" stroke-width="12" stroke-opacity=".5" fill="none"/><path d="M' + n1(x1 + ux * a - uy * off) + ' ' + n1(y1 + uy * a + ux * off) + 'L' + n1(x1 + ux * b2 - uy * off) + ' ' + n1(y1 + uy * b2 + ux * off) + '" stroke="' + dk + '" stroke-width="7" fill="none"/><path d="M' + n1(x1 + ux * a - uy * off - uy * 3.4) + ' ' + n1(y1 + uy * a + ux * off + ux * 3.4) + 'L' + n1(x1 + ux * b2 - uy * off - uy * 3.4) + ' ' + n1(y1 + uy * b2 + ux * off + ux * 3.4) + '" stroke="#c07a82" stroke-width=".9" stroke-opacity=".7" fill="none"/>'; } return o; };
      s += seg(14, 15, W_ - 14, 15, [0.18, 0.62]) + seg(W_ - 15, 14, W_ - 15, H_ - 14, [0.5]) + seg(W_ - 14, H_ - 15, 14, H_ - 15, [0.3, 0.7]) + seg(15, H_ - 14, 15, 14, [0.4]);
      var crack = function (x, y, sx, sy, sc) { return '<g transform="translate(' + x + ' ' + y + ') scale(' + sx * sc + ' ' + sy * sc + ')" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M-14 -6L-2 4L4 -8L14 6L22 -2L36 12" stroke="' + cr + '" stroke-opacity=".3" stroke-width="9"/><path d="M-14 -6L-2 4L4 -8L14 6L22 -2L36 12M-2 4L-6 18M14 6L18 22M22 -2L30 -14" stroke="' + cr + '" stroke-width="2.6"/><path d="M-14 -6L-2 4L4 -8L14 6L22 -2L36 12" stroke="#ffd6dc" stroke-width=".9"/></g>'; };
      s += crack(14, 14, 1, 1, 0.7) + crack(W_ - 15, H_ * 0.55 - 20, 0, 0, 1).replace('scale(0 0)', 'rotate(90) scale(1 -1)') + crack(W_ * 0.86, H_ - 17, 1, -1, 0.7).replace(/translate\(([^ ]+) ([^)]+)\) scale\(([^)]+)\)/, 'translate($1 $2) rotate(-12) scale($3)') + crack(W_ - 14, 14, -1, 1, 0.6);
      return s;
    },
    /* 12 - leggendaria: sagoma a portale ottagonale, strati d'oro, filo cremisi, ghost dimensionali, medaglioni a gemma sugli smussi, archi */
    'cornice-nexus-supremo': function (W_, H_, u) {
      var d = '<defs>' + lg(u + 'nx', [[0, '#fff0bd'], [0.45, '#e2b556'], [1, '#9a6f22']], 0, 0, 1, 1) + rg(u + 'gm', 0.35, 0.3, 0.8, '#ff9aa8', 1, 0.2) + '</defs>', g = 'url(#' + u + 'nx)', cr = '#d4283f';
      var s = d + poly(cham(W_, H_, 8, 30), 'none', '#a78bfa', 0.9, ' stroke-opacity=".75" transform="translate(-2 -2)"') + poly(cham(W_, H_, 8, 30), 'none', '#52d6e6', 0.9, ' stroke-opacity=".75" transform="translate(2 2)"');
      s += poly(cham(W_, H_, 17, 26), 'none', '#000', 20, ' stroke-opacity=".5"') + poly(cham(W_, H_, 14, 28), 'none', g, 5.4) + poly(cham(W_, H_, 21, 24), 'none', cr, 1.6) + poly(cham(W_, H_, 25.5, 22), 'none', '#fff0bd', 1.1) + poly(cham(W_, H_, 28.5, 20), 'none', g, 0.7, ' stroke-dasharray="3 3" stroke-opacity=".8"');
      s += edgeRun(W_, H_, 14, 44, function (x, y, v) { return '<path transform="translate(' + n1(x) + ' ' + n1(y) + ')" d="M0-5L4 0 0 5-4 0Z" fill="#12070a" stroke="#fff0bd" stroke-width="1.2"/><circle r="1.4" fill="' + cr + '"/>'; }, 82);
      var med = function (cx, cy) { var rays = '', k; for (k = 0; k < 8; k++) { var an = Math.PI / 4 * k; rays += '<path d="M' + n1(Math.cos(an) * 9) + ' ' + n1(Math.sin(an) * 9) + 'L' + n1(Math.cos(an) * 18) + ' ' + n1(Math.sin(an) * 18) + '" stroke="#fff0bd" stroke-width="1.2"/>'; } var oct = [], j; for (j = 0; j < 8; j++) { var a2 = Math.PI / 4 * j + Math.PI / 8; oct.push([Math.cos(a2) * 13, Math.sin(a2) * 13]); } return '<g transform="translate(' + cx + ' ' + cy + ')">' + rays + poly(oct, g, '#2a1a05', 1.4) + '<circle r="8" fill="#12070a" stroke="#fff0bd" stroke-width="1.2"/><circle r="4.8" fill="url(#' + u + 'gm)" stroke="' + cr + '" stroke-width="1"/></g>'; };
      var cc = 14 + 28 * 0.5; s += med(14 + 7, 14 + 7) + med(W_ - 21, 21) + med(21, H_ - 21) + med(W_ - 21, H_ - 21);
      [[W_ / 2, 14, 1], [W_ / 2, H_ - 14, -1]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ') scale(1 ' + q[2] + ')"><path d="M-34 0Q-16 17 0 17Q16 17 34 0" fill="none" stroke="' + g + '" stroke-width="3"/><path d="M-22 0Q-9 11 0 11Q9 11 22 0" fill="none" stroke="' + cr + '" stroke-width="1.2"/><path d="M0 3L6.5 10 0 17-6.5 10Z" fill="#12070a" stroke="#fff0bd" stroke-width="1.4"/><circle cy="10" r="2.4" fill="url(#' + u + 'gm)"/></g>'; });
      [[10, H_ / 2], [W_ - 10, H_ / 2]].forEach(function (q) { s += '<g transform="translate(' + q[0] + ' ' + q[1] + ')"><path d="M0-17L9 0 0 17-9 0Z" fill="#12070a" stroke="' + g + '" stroke-width="2.2"/><circle r="2.8" fill="url(#' + u + 'gm)"/></g>'; });
      /* 3.2.5: prestigio: alone cremisi/dorato interno, filigrana a diamanti sul filo interno, raggi dai medaglioni */
      s += poly(cham(W_, H_, 33, 18), 'none', '#d4283f', 3, ' stroke-opacity=".12"') + poly(cham(W_, H_, 31, 19), 'none', '#fff0bd', 0.8, ' stroke-opacity=".38"');
      s += edgeRun(W_, H_, 31, 41, function (x, y) { return '<path transform="translate(' + n1(x) + ' ' + n1(y) + ')" d="M0-2.6L2.6 0 0 2.6-2.6 0Z" fill="#fff0bd" fill-opacity=".55"/>'; }, 100);
      return s;
    }
  };
  /* distintivi di colore principali delle cornici (per i test di contrasto) */
  var FRAME_COLORS = { 'cornice-standard-tva': ['#D2B184'], 'cornice-bronzo-temporale': ['#e2a566', '#a86a2c'], 'cornice-argento-cronologico': ['#d3dde8'], 'cornice-oro-archivista': ['#fbe9ae', '#d9ad4e'], 'cornice-acciaio-mutante': ['#8c97a2', '#eef3f7'], 'cornice-energia-arcana': ['#b57ef0', '#e2cbff'], 'cornice-tecnologia-stark': ['#35d0e8'], 'cornice-wakanda': ['#8d6be0', '#c9ccd8'], 'cornice-asgard': ['#e2c77f', '#fbeab4'], 'cornice-vuoto-temporale': ['#aaa5bb', '#7a6a9c'], 'cornice-incursione-rossa': ['#ff3d57', '#c07a82'], 'cornice-nexus-supremo': ['#fff0bd', '#e2b556'] };

  /* ---------- TEMI (10): sfondo, palette, testi, motivi, texture, luce e superfici propri ----------
     palette di riferimento: bg / accento / testo. Il testo-accento (ID, intestazioni) viene portato a contrasto >= 4,5 sul fondo. */
  var CUR_LT = null;
  function lighting(W_, H_, u, bg, k) {
    var l = CUR_LT || { x: 0.18, y: 0.08, c: '#ffffff', o: 0.1, r: 0.95, vx: 0.85, vy: 1 };
    return '<defs>' + rg(u + 'l1', l.x, l.y, l.r || 0.95, l.c, l.o * (k || 1), 0) + rg(u + 'l2', l.vx, l.vy, 0.8, '#000000', 0.5, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'l1)"/><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'l2)"/>';
  }
  function base(W_, H_, u, bg, lo) { return '<defs>' + lg(u + 'tb', [[0, mix(bg, '#ffffff', lo || 0.07)], [0.55, bg], [1, mix(bg, '#000000', 0.5)]], 0, 0, 1, 1) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'tb)"/>'; }
  function hatch(W_, H_, col, op, step, ang) { var s = '', i, d = Math.max(W_, H_) * 1.5; for (i = -d; i < d; i += step) s += '<path d="M' + n1(i) + ' ' + H_ + 'L' + n1(i + (ang || 1) * H_) + ' 0"/>'; return '<g stroke="' + col + '" stroke-opacity="' + op + '" stroke-width=".8">' + s + '</g>'; }
  var THEMES = {
    /* istituzionale: bordeaux scuro, guilloche, clessidra filigranata */
    'tema-tva-classico': { pn: 'paper', lt: { x: 0.12, y: 0.05, c: '#ffe2a8', o: 0.16, r: 0.9, vx: 0.9, vy: 1 }, bg: '#211016', acc: '#D2B184', ink: '#F2E8D5', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#211016', 0.1) + hatch(W_, H_, '#D2B184', 0.05, 11, 0.45), cx = W_ * 0.76, cy = H_ * 0.52, R = Math.min(W_, H_) * 0.4, i;
      var ring = ''; for (i = 1; i <= 5; i++) ring += '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * i / 5) + '" fill="none" stroke="#D2B184" stroke-opacity="' + n1(0.05 + i * 0.012) + '"/>';
      var hg = '<path d="M' + n1(cx - R * 0.28) + ' ' + n1(cy - R * 0.4) + 'H' + n1(cx + R * 0.28) + 'L' + cx + ' ' + cy + 'L' + n1(cx + R * 0.28) + ' ' + n1(cy + R * 0.4) + 'H' + n1(cx - R * 0.28) + 'L' + cx + ' ' + cy + 'Z" fill="none" stroke="#D2B184" stroke-opacity=".16" stroke-width="2.4"/>';
      return s + ring + hg + lighting(W_, H_, u, '#211016');
    } },
    /* documentazione riservata: blu profondo, righe da registro, barre di oscuramento, timbro */
    'tema-archivio-notturno': { pn: 'steel', lt: { x: 0.5, y: 0, c: '#a8c8ff', o: 0.14, r: 0.8, vx: 0.5, vy: 1.1 }, bg: '#0A1425', acc: '#6885A7', ink: '#DCE7F1', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#0A1425', 0.1), y, r = rng(2), st = '';
      for (y = 34; y < H_; y += 30) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#6885A7" stroke-opacity=".12"/>';
      s += '<path d="M' + n1(W_ * 0.07) + ' 0V' + H_ + '" stroke="#c85a6a" stroke-opacity=".22"/>';
      for (y = 0; y < 5; y++) st += '<rect x="' + n1(W_ * (0.55 + r() * 0.3)) + '" y="' + n1(H_ * (0.15 + y * 0.17)) + '" width="' + n1(W_ * (0.08 + r() * 0.16)) + '" height="' + n1(H_ * 0.022) + '" fill="#02050b" fill-opacity=".6"/>';
      var cx = W_ * 0.8, cy = H_ * 0.6, R = Math.min(W_, H_) * 0.2;
      s += st + '<g transform="rotate(-14 ' + n1(cx) + ' ' + n1(cy) + ')" fill="none" stroke="#6885A7" stroke-opacity=".28"><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R) + '" stroke-width="2.4"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.82) + '" stroke-width="1"/><path d="M' + n1(cx - R * 0.6) + ' ' + n1(cy) + 'H' + n1(cx + R * 0.6) + '" stroke-width="2"/></g>';
      /* 3.2.5: dettagli archivistici discreti: fori da raccoglitore, linguette di schedario, etichette di catalogo */
      var k;
      for (k = 0; k < 3; k++) s += '<circle cx="' + n1(W_ * 0.032) + '" cy="' + n1(H_ * (0.22 + k * 0.28)) + '" r="' + n1(Math.min(W_, H_) * 0.012) + '" fill="#02050b" fill-opacity=".55" stroke="#6885A7" stroke-opacity=".3"/>';
      for (k = 0; k < 6; k++) s += '<path d="M' + n1(W_ - 2) + ' ' + n1(H_ * (0.1 + k * 0.13)) + 'h' + n1(-W_ * 0.028) + 'v' + n1(H_ * 0.07) + 'h' + n1(W_ * 0.028) + '" fill="#6885A7" fill-opacity="' + (k % 2 ? 0.1 : 0.17) + '" stroke="#6885A7" stroke-opacity=".3"/>';
      s += '<g fill="none" stroke="#6885A7" stroke-opacity=".22"><rect x="' + n1(W_ * 0.1) + '" y="' + n1(H_ * 0.9) + '" width="' + n1(W_ * 0.16) + '" height="' + n1(H_ * 0.05) + '" rx="2"/><path d="M' + n1(W_ * 0.115) + ' ' + n1(H_ * 0.925) + 'h' + n1(W_ * 0.1) + '"/></g>';
      return s + lighting(W_, H_, u, '#0A1425', 0.8);
    } },
    /* bronzo e oro: superfici calde spazzolate, raggi, ingranaggio e scala cronologica */
    'tema-cronologia-dorata': { pn: 'brass', lt: { x: 0.74, y: 0.5, c: '#ffd890', o: 0.2, r: 0.7, vx: 0.05, vy: 1 }, bg: '#2C2115', acc: '#D9AE4D', ink: '#FFF0BD', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#2C2115', 0.12), i, cx = W_ * 0.74, cy = H_ * 0.5, y;
      for (y = 3; y < H_; y += 5) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#ffe6a8" stroke-opacity="' + (y % 15 === 3 ? 0.05 : 0.025) + '"/>';
      for (i = 0; i < 32; i++) { var a = Math.PI * 2 / 32 * i; s += '<path d="M' + n1(cx + Math.cos(a) * 70) + ' ' + n1(cy + Math.sin(a) * 70) + 'L' + n1(cx + Math.cos(a) * Math.max(W_, H_)) + ' ' + n1(cy + Math.sin(a) * Math.max(W_, H_)) + '" stroke="#D9AE4D" stroke-opacity=".05" stroke-width="7"/>'; }
      var R = Math.min(W_, H_) * 0.34, tp = [], t; for (t = 0; t < 36; t++) { var an = Math.PI / 18 * t, rad = t % 2 ? R * 0.9 : R; tp.push([cx + Math.cos(an) * rad, cy + Math.sin(an) * rad]); }
      s += poly(tp, 'none', '#D9AE4D', 1.6, ' stroke-opacity=".2"') + '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.55) + '" fill="none" stroke="#D9AE4D" stroke-opacity=".18" stroke-width="2"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.12) + '" fill="#D9AE4D" fill-opacity=".2"/>';
      for (y = 28; y < H_ - 20; y += 22) s += '<path d="M' + n1(W_ * 0.035) + ' ' + y + 'h' + ((y / 22 | 0) % 4 === 0 ? 20 : 10) + '" stroke="#D9AE4D" stroke-opacity=".3" stroke-width="1.4"/>';
      return s + lighting(W_, H_, u, '#2C2115');
    } },
    /* tensione dimensionale: frammenti di realta' sfalsati con fratture rosse */
    'tema-multiverso-cremisi': { pn: 'cracked', lt: { x: 0.45, y: 1, c: '#ff3a52', o: 0.26, r: 0.85, vx: 0.5, vy: -0.1 }, bg: '#29090F', acc: '#D82C48', ink: '#F5B1BC', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#29090F', 0.08), r = rng(23), sh = [[0, 0, 0.42, 0, 0.3, 1, 0, 1], [0.42, 0, 0.74, 0, 0.62, 1, 0.3, 1], [0.74, 0, 1, 0, 1, 1, 0.62, 1]], k;
      sh.forEach(function (q, i) { var pts = ''; for (k = 0; k < 8; k += 2) pts += n1(q[k] * W_) + ',' + n1(q[k + 1] * H_) + ' '; s += '<polygon points="' + pts + '" fill="' + (i === 1 ? '#6a1020' : i === 2 ? '#150307' : '#ffffff') + '" fill-opacity="' + (i === 0 ? 0.03 : 0.3) + '"/>'; });
      var f = function (x0, w) { var d = 'M' + n1(x0 * W_) + ' 0', y = 0; while (y < H_) { y += 20 + r() * 40; d += 'L' + n1(x0 * W_ + (r() - 0.5) * w) + ' ' + n1(Math.min(y, H_)); } return d; };
      [[0.42, 40], [0.7, 50]].forEach(function (q) { var d = f(q[0], q[1]); s += '<path d="' + d + '" fill="none" stroke="#D82C48" stroke-opacity=".25" stroke-width="9" stroke-linejoin="round"/><path d="' + d + '" fill="none" stroke="#ff6b83" stroke-opacity=".7" stroke-width="1.6" stroke-linejoin="round"/>'; });
      for (k = 0; k < 6; k++) s += '<circle cx="' + n1(r() * W_) + '" cy="' + n1(r() * H_) + '" r="' + n1(Math.min(W_, H_) * (0.1 + r() * 0.2)) + '" fill="none" stroke="#D82C48" stroke-opacity=".08" stroke-width="2"/>';
      return s + lighting(W_, H_, u, '#29090F');
    } },
    /* petrolio scuro e ciano: griglia tecnica, circuiti, pannelli smussati */
    'tema-tecnologia-futuristica': { pn: 'hud', lt: { x: 1, y: 0.4, c: '#35e0f0', o: 0.2, r: 0.8, vx: 0, vy: 1 }, bg: '#071D25', acc: '#24B4C5', ink: '#B8F5F0', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#071D25', 0.1), x, y, r = rng(5), g = Math.round(W_ / 21);
      for (x = g; x < W_; x += g) s += '<path d="M' + x + ' 0V' + H_ + '" stroke="#24B4C5" stroke-opacity=".06"/>';
      for (y = g; y < H_; y += g) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#24B4C5" stroke-opacity=".06"/>';
      for (x = 0; x < 11; x++) { var px = g * (1 + Math.floor(r() * (W_ / g - 3))), py = g * (1 + Math.floor(r() * (H_ / g - 3))), l = g * (1 + Math.floor(r() * 3)); s += '<path d="M' + px + ' ' + py + 'h' + l + 'v' + g + 'h' + l + '" fill="none" stroke="#24B4C5" stroke-opacity=".3" stroke-width="1.4"/><circle cx="' + (px + 2 * l) + '" cy="' + (py + g) + '" r="3" fill="#071D25" stroke="#24B4C5" stroke-opacity=".6"/>'; }
      var pw = W_ * 0.3, ph = H_ * 0.34, c = 14; s += '<polygon points="' + [[W_ * 0.64 + c, H_ * 0.18], [W_ * 0.64 + pw, H_ * 0.18], [W_ * 0.64 + pw, H_ * 0.18 + ph - c], [W_ * 0.64 + pw - c, H_ * 0.18 + ph], [W_ * 0.64, H_ * 0.18 + ph], [W_ * 0.64, H_ * 0.18 + c]].map(function (p) { return n1(p[0]) + ',' + n1(p[1]); }).join(' ') + '" fill="#24B4C5" fill-opacity=".05" stroke="#24B4C5" stroke-opacity=".3"/>';
      return s + lighting(W_, H_, u, '#071D25');
    } },
    /* indaco e viola: diagonali, riflessi metallici */
    'tema-universo-mutante': { pn: 'indus', lt: { x: 0.9, y: 0.1, c: '#c9bdff', o: 0.16, r: 1, vx: 0.1, vy: 1 }, bg: '#17132D', acc: '#7863D7', ink: '#E0D7FF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#17132D', 0.09) + '<defs>' + lg(u + 'ms', [[0, '#ffffff', 0], [0.5, '#c9bdff', 0.16], [1, '#ffffff', 0]], 0, 0, 1, 0) + '</defs>', i, d = Math.max(W_, H_);
      for (i = -3; i < 16; i++) { var x = i * W_ * 0.14; s += '<polygon points="' + [[x, H_], [x + d * 0.55, H_ - d * 0.55], [x + d * 0.55 + W_ * (i % 3 ? 0.03 : 0.07), H_ - d * 0.55], [x + W_ * (i % 3 ? 0.03 : 0.07), H_]].map(function (p) { return n1(p[0]) + ',' + n1(p[1]); }).join(' ') + '" fill="#7863D7" fill-opacity="' + (i % 3 ? 0.15 : 0.3) + '"/>'; }
      for (i = 0; i < H_; i += 5) s += '<path d="M0 ' + i + 'H' + W_ + '" stroke="#c9bdff" stroke-opacity=".035"/>';
      s += '<polygon points="0,' + n1(H_ * 0.7) + ' ' + n1(W_) + ',' + n1(H_ * 0.1) + ' ' + n1(W_) + ',' + n1(H_ * 0.24) + ' 0,' + n1(H_ * 0.84) + '" fill="url(#' + u + 'ms)"/>';
      s += '<path d="M0 ' + n1(H_ * 0.7) + 'L' + W_ + ' ' + n1(H_ * 0.1) + 'M0 ' + n1(H_ * 0.84) + 'L' + W_ + ' ' + n1(H_ * 0.24) + '" stroke="#c9bdff" stroke-opacity=".28"/>';
      /* 3.2.5: geometrie molecolari, elica genetica, anomalia energetica discreta (sfondo, bassa opacita') */
      var hx = W_ * 0.9, hy0 = H_ * 0.06, hl = H_ * 0.88, amp = Math.min(W_, H_) * 0.035, pa = '', pb = '', k, yy;
      for (k = 0; k <= 40; k++) { yy = hy0 + hl * k / 40; pa += (k ? 'L' : 'M') + n1(hx + Math.sin(k * 0.5) * amp) + ' ' + n1(yy); pb += (k ? 'L' : 'M') + n1(hx - Math.sin(k * 0.5) * amp) + ' ' + n1(yy); }
      s += '<g fill="none" stroke="#c9bdff" stroke-width="1.4" stroke-opacity=".24"><path d="' + pa + '"/><path d="' + pb + '"/>';
      for (k = 1; k < 40; k += 2) { yy = hy0 + hl * k / 40; s += '<path d="M' + n1(hx + Math.sin(k * 0.5) * amp) + ' ' + n1(yy) + 'L' + n1(hx - Math.sin(k * 0.5) * amp) + ' ' + n1(yy) + '" stroke-opacity=".16"/>'; }
      s += '</g>';
      var mx = W_ * 0.5, my = H_ * 0.93, mr = Math.min(W_, H_) * 0.04, mp = [], mj;
      for (mj = 0; mj < 6; mj++) mp.push([mx + Math.cos(Math.PI / 3 * mj) * mr, my + Math.sin(Math.PI / 3 * mj) * mr]);
      s += poly(mp, 'none', '#c9bdff', 1.2, ' stroke-opacity=".26"');
      for (mj = 0; mj < 6; mj++) s += '<circle cx="' + n1(mp[mj][0]) + '" cy="' + n1(mp[mj][1]) + '" r="' + n1(mr * 0.2) + '" fill="#17132D" stroke="#c9bdff" stroke-opacity=".5"/><path d="M' + n1(mp[mj][0]) + ' ' + n1(mp[mj][1]) + 'L' + n1(mx + (mp[mj][0] - mx) * 1.9) + ' ' + n1(my + (mp[mj][1] - my) * 1.9) + '" stroke="#c9bdff" stroke-opacity=".16"/>';
      var ax = W_ * 0.07, ay = H_ * 0.1;
      s += '<g fill="none" stroke="#c9bdff"><circle cx="' + n1(ax) + '" cy="' + n1(ay) + '" r="' + n1(mr * 0.9) + '" stroke-opacity=".3" stroke-dasharray="5 4"/><circle cx="' + n1(ax) + '" cy="' + n1(ay) + '" r="' + n1(mr * 0.4) + '" stroke-opacity=".5"/><path d="M' + n1(ax - mr * 1.6) + ' ' + n1(ay) + 'h' + n1(mr * 0.5) + 'M' + n1(ax + mr * 1.1) + ' ' + n1(ay) + 'h' + n1(mr * 0.5) + 'M' + n1(ax) + ' ' + n1(ay - mr * 1.6) + 'v' + n1(mr * 0.5) + '" stroke-opacity=".3"/></g>';
      return s + lighting(W_, H_, u, '#17132D');
    } },
    /* sigilli e geometrie arcane: cerchi concentrici con rune, esagrammi, alone viola */
    'tema-energia-mistica': { pn: 'sigil', lt: { x: 0.5, y: 0.5, c: '#d070ff', o: 0.24, r: 0.65, vx: 0.9, vy: 1 }, bg: '#25122E', acc: '#B15BE1', ink: '#EBC8FF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#25122E', 0.09) + '<defs>' + rg(u + 'mg', 0.72, 0.5, 0.62, '#C77CF0', 0.62, 0) + rg(u + 'mv', 0.5, 0.5, 0.85, '#000000', 0, 0.55) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'mg)"/><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'mv)"/>', cx = W_ * 0.74, cy = H_ * 0.5, R = Math.min(W_, H_) * 0.46, i;
      for (i = 1; i <= 4; i++) s += '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * i / 4) + '" fill="none" stroke="#B15BE1" stroke-opacity="' + n1(0.12 + i * 0.03) + '" stroke-width="' + (i === 4 ? 2 : 1) + '"' + (i % 2 ? ' stroke-dasharray="3 5"' : '') + '/>';
      for (i = 0; i < 24; i++) { var a = Math.PI / 12 * i; s += '<path d="M' + n1(cx + Math.cos(a) * R * 0.97) + ' ' + n1(cy + Math.sin(a) * R * 0.97) + 'L' + n1(cx + Math.cos(a) * R * (i % 2 ? 1.04 : 1.1)) + ' ' + n1(cy + Math.sin(a) * R * (i % 2 ? 1.04 : 1.1)) + '" stroke="#EBC8FF" stroke-opacity=".3"/>'; }
      var hex = function (k, rot) { var p = [], j; for (j = 0; j < 3; j++) { var an = rot + Math.PI * 2 / 3 * j; p.push([cx + Math.cos(an) * R * k, cy + Math.sin(an) * R * k]); } return poly(p, 'none', '#EBC8FF', 1.4, ' stroke-opacity=".3"'); };
      /* 3.2.5: anello di rune, cerchio rituale interno, stella a 12 punte e linee di energia a spirale */
      var RUNE = ['M0 -5V5M0 -5L4 -1L0 3', 'M-3 -5L3 5M3 -5L-3 5', 'M0 -5V5M-3 -2H3M-3 2H3', 'M-3 5L0 -5L3 5M-2 1H2', 'M-3 -5H3L-3 5H3', 'M0 -5L4 0L0 5L-4 0Z'], k;
      s += '<g fill="none" stroke="#EBC8FF" stroke-width="1.3" stroke-linecap="round" stroke-opacity=".5">';
      for (k = 0; k < 18; k++) { var ra = Math.PI / 9 * k - Math.PI / 2, ura = Math.cos(ra) > 0.15 && Math.sin(ra) < 0.1; if (ura && k % 2) continue; s += '<path' + (ura ? ' stroke-opacity=".26"' : (k % 3 === 2 ? ' stroke-opacity=".34"' : '')) + ' transform="translate(' + n1(cx + Math.cos(ra) * R * 0.86) + ' ' + n1(cy + Math.sin(ra) * R * 0.86) + ') rotate(' + n1(ra * 180 / Math.PI + 90) + ') scale(' + n1(R / 58) + ')" d="' + RUNE[k % 6] + '"/>'; }
      s += '</g><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.34) + '" fill="none" stroke="#EBC8FF" stroke-opacity=".4" stroke-width="1.6"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.12) + '" fill="#B15BE1" fill-opacity=".35" stroke="#EBC8FF" stroke-opacity=".6"/>';
      s += hex(0.5, 0) + hex(0.5, Math.PI);
      s += '<g fill="none" stroke="#d070ff" stroke-opacity=".34" stroke-width="1.4" stroke-dasharray="6 5" stroke-linecap="round">';
      for (k = 0; k < 6; k++) { var sa = Math.PI / 3 * k; s += '<path d="M' + n1(cx + Math.cos(sa) * R * 0.14) + ' ' + n1(cy + Math.sin(sa) * R * 0.14) + 'Q' + n1(cx + Math.cos(sa + 0.7) * R * 0.7) + ' ' + n1(cy + Math.sin(sa + 0.7) * R * 0.7) + ' ' + n1(cx + Math.cos(sa + 0.25) * R * 1.3) + ' ' + n1(cy + Math.sin(sa + 0.25) * R * 1.3) + '"/>'; }
      s += '</g>';
      return s + hex(0.72, -Math.PI / 2) + hex(0.72, Math.PI / 2) + lighting(W_, H_, u, '#25122E');
    } },
    /* quasi monocromatico: frammenti, vuoti, asimmetria */
    'tema-ombre-del-vuoto': { pn: 'void', lt: { x: 0.02, y: 0.3, c: '#b9b4cc', o: 0.12, r: 0.45, vx: 0.7, vy: 0.9 }, bg: '#08080E', acc: '#686477', ink: '#D4D0DD', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#08080E', 0.1), r = rng(31), i;
      s += '<defs>' + rg(u + 'vd', 0.78, 0.62, 0.34, '#000000', 1, 0) + '</defs><circle cx="' + n1(W_ * 0.78) + '" cy="' + n1(H_ * 0.62) + '" r="' + n1(Math.min(W_, H_) * 0.42) + '" fill="url(#' + u + 'vd)"/><circle cx="' + n1(W_ * 0.78) + '" cy="' + n1(H_ * 0.62) + '" r="' + n1(Math.min(W_, H_) * 0.24) + '" fill="#020204"/><circle cx="' + n1(W_ * 0.78) + '" cy="' + n1(H_ * 0.62) + '" r="' + n1(Math.min(W_, H_) * 0.24) + '" fill="none" stroke="#9a96a8" stroke-opacity=".3" stroke-width="1.4" stroke-dasharray="14 9"/>';
      for (i = 0; i < 16; i++) { var x = r() * W_, y = r() * H_, sz = Math.min(W_, H_) * (0.03 + r() * 0.09), an = r() * 6.28; s += '<polygon points="' + [0, 2.2, 4.1].map(function (o, k) { return n1(x + Math.cos(an + o) * sz * (k === 2 ? 0.55 : 1)) + ',' + n1(y + Math.sin(an + o) * sz * (k === 2 ? 0.55 : 1)); }).join(' ') + '" fill="#686477" fill-opacity="' + n1(0.08 + r() * 0.14) + '" stroke="#9a96a8" stroke-opacity=".3" stroke-width=".8"/>'; }
      s += '<defs>' + rg(u + 'vl', 0.15, 0.1, 0.6, '#b9b4cc', 0.14, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'vl)"/>';
      for (i = 6; i < H_; i += 7) s += '<path d="M0 ' + i + 'H' + W_ + '" stroke="#fff" stroke-opacity=".018"/>';
      return s + lighting(W_, H_, u, '#08080E', 0.4);
    } },
    /* blu cosmico: nebulosa viola, orbite, stelle */
    'tema-nexus-cosmico': { pn: 'cosmic', lt: { x: 0.85, y: 0.1, c: '#b080ff', o: 0.22, r: 0.8, vx: 0.1, vy: 1 }, bg: '#101C39', acc: '#477BEB', ink: '#D8B5FF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#101C39', 0.08) + '<defs>' + rg(u + 'nb', 0.74, 0.3, 0.55, '#a45be0', 0.42, 0) + rg(u + 'nc', 0.2, 0.85, 0.5, '#477BEB', 0.3, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'nb)"/><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'nc)"/>' + stars(W_, H_, 70, 21, '#ffffff', 1.5), cx = W_ * 0.68, cy = H_ * 0.52, i;
      for (i = 0; i < 3; i++) s += '<ellipse cx="' + n1(cx) + '" cy="' + n1(cy) + '" rx="' + n1(W_ * (0.3 + i * 0.12)) + '" ry="' + n1(H_ * (0.12 + i * 0.07)) + '" transform="rotate(' + (-22 + i * 6) + ' ' + n1(cx) + ' ' + n1(cy) + ')" fill="none" stroke="#8fb0ff" stroke-opacity="' + n1(0.26 - i * 0.05) + '" stroke-width="1.2"/>';
      s += '<circle cx="' + n1(cx + W_ * 0.25) + '" cy="' + n1(cy - H_ * 0.34) + '" r="' + n1(Math.min(W_, H_) * 0.025) + '" fill="#d8b5ff"/><circle cx="' + n1(cx + W_ * 0.2) + '" cy="' + n1(cy + H_ * 0.42) + '" r="' + n1(Math.min(W_, H_) * 0.018) + '" fill="#8fb0ff"/>';
      /* 3.2.5: profondita' stellare a piu' livelli, connessioni dimensionali tra stelle, bagliori a quattro punte */
      var r3 = rng(77), px = [], k;
      s += stars(W_, H_, 90, 41, '#c9d8ff', 0.7);
      for (k = 0; k < 9; k++) px.push([W_ * (0.08 + r3() * 0.84), H_ * (0.06 + r3() * 0.88)]);
      s += '<g fill="none" stroke="#8fb0ff" stroke-opacity=".26" stroke-width="1.1">';
      for (k = 1; k < px.length; k++) s += '<path d="M' + n1(px[k - 1][0]) + ' ' + n1(px[k - 1][1]) + 'L' + n1(px[k][0]) + ' ' + n1(px[k][1]) + '"/>';
      s += '<path d="M' + n1(px[0][0]) + ' ' + n1(px[0][1]) + 'L' + n1(px[4][0]) + ' ' + n1(px[4][1]) + '" stroke-dasharray="4 5"/></g>';
      var sp = Math.min(W_, H_) * 0.022;
      for (k = 0; k < px.length; k++) s += '<circle cx="' + n1(px[k][0]) + '" cy="' + n1(px[k][1]) + '" r="' + n1(sp * 0.28) + '" fill="#e6ecff" fill-opacity=".8"/>' + (k % 3 === 0 ? '<path d="M' + n1(px[k][0] - sp * 1.6) + ' ' + n1(px[k][1]) + 'h' + n1(sp * 3.2) + 'M' + n1(px[k][0]) + ' ' + n1(px[k][1] - sp * 1.6) + 'v' + n1(sp * 3.2) + '" stroke="#d8b5ff" stroke-opacity=".6" stroke-width="1"/>' : '');
      s += '<ellipse cx="' + n1(W_ * 0.2) + '" cy="' + n1(H_ * 0.8) + '" rx="' + n1(W_ * 0.22) + '" ry="' + n1(H_ * 0.05) + '" transform="rotate(-18 ' + n1(W_ * 0.2) + ' ' + n1(H_ * 0.8) + ')" fill="none" stroke="#d8b5ff" stroke-opacity=".2" stroke-dasharray="2 6"/>';
      return s + lighting(W_, H_, u, '#101C39', 0.6);
    } },
    /* oro pallido, solenne e monumentale: orologio spezzato, colonne, orizzonte (tema leggendario, il piu' elaborato) */
    'tema-fine-del-tempo': { pn: 'monument', lt: { x: 0.6, y: -0.05, c: '#fff2b8', o: 0.3, r: 0.9, vx: 0.05, vy: 1.1 }, bg: '#242018', acc: '#E5C879', ink: '#FFF8DF', draw: function (W_, H_, u) {
      var s = base(W_, H_, u, '#242018', 0.1) + '<defs>' + lg(u + 'cl', [[0, '#fff2b8', 0.32], [1, '#E5C879', 0.04]], 0, 0, 0, 1) + rg(u + 'sn', 0.72, 0.9, 0.7, '#fff2b8', 0.5, 0) + '</defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'sn)"/>', cx = W_ * 0.74, cy = H_ * 0.58, R = Math.min(W_, H_) * 0.42, i;
      for (i = 0; i < 5; i++) { var x = W_ * (0.48 + i * 0.105); s += '<rect x="' + n1(x) + '" y="' + n1(H_ * 0.1) + '" width="' + n1(W_ * 0.05) + '" height="' + n1(H_ * 0.8) + '" fill="url(#' + u + 'cl)"/><rect x="' + n1(x - 3) + '" y="' + n1(H_ * 0.1) + '" width="' + n1(W_ * 0.05 + 6) + '" height="6" fill="#E5C879" fill-opacity=".14"/>'; }
      s += '<circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R) + '" fill="#242018" fill-opacity=".7" stroke="#E5C879" stroke-opacity=".38" stroke-width="2.4"/><circle cx="' + n1(cx) + '" cy="' + n1(cy) + '" r="' + n1(R * 0.9) + '" fill="none" stroke="#E5C879" stroke-opacity=".2"/>';
      for (i = 0; i < 12; i++) { var a = Math.PI / 6 * i; s += '<path d="M' + n1(cx + Math.cos(a) * R * 0.78) + ' ' + n1(cy + Math.sin(a) * R * 0.78) + 'L' + n1(cx + Math.cos(a) * R * 0.9) + ' ' + n1(cy + Math.sin(a) * R * 0.9) + '" stroke="#E5C879" stroke-opacity=".5" stroke-width="2.4"/>'; }
      s += '<path d="M' + n1(cx) + ' ' + n1(cy) + 'L' + n1(cx + R * 0.5) + ' ' + n1(cy - R * 0.36) + 'M' + n1(cx) + ' ' + n1(cy) + 'L' + n1(cx - R * 0.12) + ' ' + n1(cy - R * 0.66) + '" stroke="#E5C879" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/><path d="M' + n1(cx - R * 1.05) + ' ' + n1(cy + R * 0.2) + 'L' + n1(cx - R * 0.2) + ' ' + n1(cy - R * 0.04) + 'L' + n1(cx + R * 0.14) + ' ' + n1(cy + R * 0.44) + 'L' + n1(cx + R * 1.05) + ' ' + n1(cy + R * 0.14) + '" fill="none" stroke="#d42a3a" stroke-opacity=".45" stroke-width="2"/><path d="M0 ' + n1(H_ * 0.9) + 'H' + W_ + '" stroke="#E5C879" stroke-opacity=".3"/>';
      /* 3.2.5: cronologia in dissoluzione: frammenti che si staccano dal quadrante, righello temporale che sfuma, polvere, architravi monumentali */
      var r4 = rng(91), k;
      for (k = 0; k < 14; k++) {
        var fa = -0.9 + r4() * 1.9, fd = R * (1.02 + r4() * 0.55), fx = cx + Math.cos(fa) * fd, fy = cy + Math.sin(fa - 0.5) * fd * 0.9, fs = Math.min(W_, H_) * (0.012 + r4() * 0.028), rot = r4() * 6.28;
        s += '<polygon points="' + [0, 2.1, 4.2].map(function (o, j) { return n1(fx + Math.cos(rot + o) * fs * (j === 2 ? 0.6 : 1)) + ',' + n1(fy + Math.sin(rot + o) * fs * (j === 2 ? 0.6 : 1)); }).join(' ') + '" fill="#E5C879" fill-opacity="' + n1(0.34 - k * 0.019) + '" stroke="#FFF8DF" stroke-opacity="' + n1(0.4 - k * 0.025) + '" stroke-width=".8"/>';
      }
      for (k = 0; k < 26; k++) s += '<rect x="' + n1(W_ * (0.04 + r4() * 0.5)) + '" y="' + n1(H_ * (0.05 + r4() * 0.9)) + '" width="' + n1(1.2 + r4() * 2.2) + '" height="' + n1(1.2 + r4() * 2.2) + '" fill="#E5C879" fill-opacity="' + n1(0.12 + r4() * 0.2) + '"/>';
      s += '<g stroke="#E5C879" stroke-width="1.2">';
      for (k = 0; k < 22; k++) s += '<path d="M' + n1(W_ * 0.03 + k * W_ * 0.02) + ' ' + n1(H_ * 0.96) + 'v' + (k % 5 === 0 ? -9 : -5) + '" stroke-opacity="' + n1(Math.max(0.04, 0.42 - k * 0.019)) + '"/>';
      s += '</g>';
      for (k = 0; k < 5; k++) s += '<path d="M' + n1(W_ * (0.48 + k * 0.105) + 3) + ' ' + n1(H_ * 0.1) + 'l' + n1(W_ * 0.012) + ' ' + n1(H_ * 0.03) + 'l' + n1(-W_ * 0.006) + ' ' + n1(H_ * 0.025) + 'l' + n1(W_ * 0.016) + ' ' + n1(H_ * 0.02) + '" fill="none" stroke="#FFF8DF" stroke-opacity=".3"/>';
      return s + lighting(W_, H_, u, '#242018', 0.7);
    } }
  };
  Object.keys(THEMES).forEach(function (k) { var t = THEMES[k]; var ref = mix(t.bg, '#ffffff', 0.24); t.sub = ensure(mix(t.ink, t.bg, 0.22), ref, 5); t.accT = ensure(t.acc, ref, 5.2); t.bar = ensure(t.acc, t.bg, 3); });

  /* ---------- EFFETTI (6): resa statica sempre presente; l'animazione e' solo CSS (disattivata con reduced-motion) ---------- */
  var FX = {
    'effetto-scansione-temporale': function (W_, H_, a, u) { var s = '', y; for (y = 4; y < H_; y += 6) s += '<path d="M0 ' + y + 'H' + W_ + '" stroke="#fff" stroke-opacity=".025"/>'; return '<g>' + s + '</g><g class="tc-fx tc-fx-scan"><rect x="0" y="' + n1(H_ * 0.3) + '" width="' + W_ + '" height="' + n1(H_ * 0.07) + '" fill="url(#' + u + 'scan)"/></g><defs><linearGradient id="' + u + 'scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + GOLD + '" stop-opacity="0"/><stop offset=".5" stop-color="' + GOLD + '" stop-opacity=".36"/><stop offset="1" stop-color="' + GOLD + '" stop-opacity="0"/></linearGradient></defs>'; },
    'effetto-bagliore-dorato': function (W_, H_, a, u) { return '<defs><radialGradient id="' + u + 'gl" cx="' + n1(a.cx / W_) + '" cy="' + n1(a.cy / H_) + '" r=".55"><stop offset="0" stop-color="#f0cf8a" stop-opacity=".34"/><stop offset=".6" stop-color="#f0cf8a" stop-opacity=".08"/><stop offset="1" stop-color="#f0cf8a" stop-opacity="0"/></radialGradient></defs><rect class="tc-fx tc-fx-glow" width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'gl)"/>'; },
    'effetto-energia-cremisi': function (W_, H_, a) { var s = '', i; for (i = 0; i < 4; i++) s += '<path class="tc-fx tc-fx-arc" d="M' + n1(a.cx - a.r * (1.1 + i * 0.28)) + ' ' + n1(a.cy + a.r * 0.4) + 'A' + n1(a.r * (1.15 + i * 0.28)) + ' ' + n1(a.r * (1.15 + i * 0.28)) + ' 0 0 1 ' + n1(a.cx + a.r * 0.3) + ' ' + n1(a.cy - a.r * (1.1 + i * 0.28)) + '" fill="none" stroke="#e23a4a" stroke-width="' + (3.6 - i * 0.5) + '" stroke-opacity="' + n1(0.85 - i * 0.1) + '" stroke-dasharray="' + (10 + i * 6) + ' ' + (8 + i * 4) + '"/>'; return s; },
    'effetto-distorsione-nexus': function (W_, H_, a) { var r = rng(13), s = '', i; for (i = 0; i < 7; i++) { var y = n1(r() * H_), h = n1(3 + r() * 9), x = r() > 0.5 ? 0 : W_ * 0.7; s += '<rect class="tc-fx tc-fx-gl" x="' + n1(x + r() * 20) + '" y="' + y + '" width="' + n1(W_ * (0.1 + r() * 0.2)) + '" height="' + h + '" fill="' + (i % 2 ? '#e23a4a' : '#7fd3d6') + '" opacity=".16"/>'; } return s + '<g class="tc-fx tc-fx-ghost" opacity=".18" fill="none" stroke="#7fd3d6" stroke-width="2"><rect x="' + n1(a.cx - a.r - 5) + '" y="' + n1(a.cy - a.r) + '" width="' + n1(a.r * 2) + '" height="' + n1(a.r * 2) + '" rx="8"/></g>'; },
    'effetto-particelle-cosmiche': function (W_, H_) { var r = rng(17), s = '', i; for (i = 0; i < 46; i++) { var x = r() * W_, y = r() * H_, rr = 0.8 + r() * 2.4; s += '<circle class="' + (i % 3 === 0 ? 'tc-fx tc-fx-tw' : 'tc-fx-st') + '" cx="' + n1(x) + '" cy="' + n1(y) + '" r="' + n1(rr) + '" fill="' + (i % 5 === 0 ? GOLD : '#fff') + '" opacity="' + n1(0.3 + r() * 0.5) + '"/>'; } return s; },
    'effetto-aura-leggendaria': function (W_, H_, a, u) { var s = '', i; for (i = 0; i < 16; i++) { var an = Math.PI * 2 / 16 * i; s += '<path d="M' + n1(a.cx + Math.cos(an) * a.r * 1.05) + ' ' + n1(a.cy + Math.sin(an) * a.r * 1.05) + 'L' + n1(a.cx + Math.cos(an) * a.r * (i % 2 ? 1.9 : 2.4)) + ' ' + n1(a.cy + Math.sin(an) * a.r * (i % 2 ? 1.9 : 2.4)) + '" stroke="#f0cf8a" stroke-opacity="' + (i % 2 ? 0.1 : 0.16) + '" stroke-width="' + (i % 2 ? 4 : 7) + '" stroke-linecap="round"/>'; } return '<defs><radialGradient id="' + u + 'au" cx="' + n1(a.cx / W_) + '" cy="' + n1(a.cy / H_) + '" r=".5"><stop offset="0" stop-color="#f6dc9c" stop-opacity=".3"/><stop offset="1" stop-color="#f6dc9c" stop-opacity="0"/></radialGradient></defs><rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'au)"/><g class="tc-fx tc-fx-rot" style="transform-origin:' + a.cx + 'px ' + a.cy + 'px">' + s + '</g><circle cx="' + a.cx + '" cy="' + a.cy + '" r="' + n1(a.r * 1.08) + '" fill="none" stroke="#f6dc9c" stroke-opacity=".5" stroke-width="2.4"/>'; }
  };

  /* ---------- avatar nelle carte ---------- */
  /* ---------- illustrazioni esterne degli avatar (opzionali, con fallback agli SVG) ----------
     W.TVA_AVATAR_ART = { 'agente': 'assets/avatars/agente.webp', ... } (vuota di default: nessuna richiesta di rete).
     Ogni file viene scaricato, validato (tipo, peso, decodifica) e convertito in data URL, cosi' la Tessera e il PNG non dipendono da risorse esterne.
     Se un file manca o e' corrotto, quell'avatar resta lo SVG: nessun errore visibile. */
  /* 3.2.4: otto ritratti approvati (WebP 768x960, ritaglio senza cornice/scritte); gli SVG restano come fallback se un file manca o e' corrotto. */
  W.TVA_AVATAR_ART = W.TVA_AVATAR_ART || { agente: 'assets/avatars/agente.webp', variante: 'assets/avatars/variante.webp', esploratore: 'assets/avatars/esploratore.webp', tecnologico: 'assets/avatars/tecnologico.webp', mistico: 'assets/avatars/mistico.webp', astratto: 'assets/avatars/astratto.webp', cronista: 'assets/avatars/cronista.webp', sentinella: 'assets/avatars/sentinella.webp' };
  var AV_TH = {}, AV_TS = {}, SMALL_ART = false;   /* AV_TH 160x200 (griglia avatar), AV_TS 96x120 (miniature dei temi) */
  var AV_IMG = {};
  function loadAvatarArt() {
    var map = W.TVA_AVATAR_ART || {}, ids = Object.keys(map).filter(function (id) { return AV_BY[id] && map[id] && !AV_IMG[id]; });
    if (!ids.length || !W.fetch) return Promise.resolve([]);
    return Promise.all(ids.map(function (id) {
      return fetch(map[id]).then(function (r) { if (!r.ok) throw 0; return r.blob(); }).then(function (b) {
        if (!/^image\/(webp|png|jpeg)$/.test(b.type) || b.size > 400000) throw 0;
        return new Promise(function (res, rej) { var f = new FileReader(); f.onload = function () { res(f.result); }; f.onerror = rej; f.readAsDataURL(b); });
      }).then(function (url) {
        return new Promise(function (res, rej) { var im = new Image(); im.onload = function () {
          if (!(im.naturalWidth > 0)) return res(null);
          try { var cv = document.createElement('canvas'); cv.width = 160; cv.height = 200; cv.getContext('2d').drawImage(im, 0, 0, 160, 200); var t = cv.toDataURL('image/jpeg', 0.8); if (/^data:image\/jpeg/.test(t)) AV_TH[id] = t; var c2 = document.createElement('canvas'); c2.width = 96; c2.height = 120; c2.getContext('2d').drawImage(im, 0, 0, 96, 120); var t2 = c2.toDataURL('image/jpeg', 0.7); if (/^data:image\/jpeg/.test(t2)) AV_TS[id] = t2; } catch (e) { delete AV_TH[id]; delete AV_TS[id]; }
          res(url); }; im.onerror = rej; im.src = url; });
      }).then(function (url) { if (!url) throw 0; AV_IMG[id] = url; return id; }).catch(function () { delete AV_IMG[id]; delete AV_TH[id]; delete AV_TS[id]; return null; });
    })).then(function (r) { r = r.filter(Boolean); if (r.length) { try { document.dispatchEvent(new CustomEvent('tva:avatarart', { detail: r })); } catch (e) {} } return r; });
  }
  function avatarPiece(m, x, y, w, h, shape, u, bgOp, small) {
    var id = u + 'av', clipEl = shape === 'circle' ? '<circle cx="' + n1(x + w / 2) + '" cy="' + n1(y + h / 2) + '" r="' + n1(w / 2) + '"/>' : '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="10"/>';
    var def = '<defs><clipPath id="' + id + '">' + clipEl + '</clipPath>', body;
    if (m.avatar && m.avatar.kind === 'photo' && m.avatar.url) {
      body = '<image x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" preserveAspectRatio="xMidYMid slice" href="' + m.avatar.url + '" xlink:href="' + m.avatar.url + '"/>';
    } else {
      var av = AV_BY[(m.avatar && m.avatar.id) || 'agente'] || AVATARS[0];
      if (AV_IMG[av.id]) { var iu = (small && AV_TH[av.id]) || (SMALL_ART && AV_TS[av.id]) || AV_IMG[av.id], lite = iu !== AV_IMG[av.id]; body = '<image x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" preserveAspectRatio="xMidYMin slice" href="' + iu + '"' + (lite ? '' : ' xlink:href="' + iu + '"') + '/>'; }
      else {
      def += grad(u + 'ag', av.bg[0], av.bg[1], 'v');
      var k = Math.max(w, h) / 100;   // 'slice' calcolato a mano (allineamento centro/basso): evita differenze di <svg> annidati tra browser
      body = '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#' + u + 'ag)"' + (bgOp !== undefined ? ' fill-opacity="' + bgOp + '"' : '') + '/><g transform="translate(' + n1(x + (w - 100 * k) / 2) + ' ' + n1(y + h - 100 * k) + ') scale(' + n1(k * 1000) / 1000 + ')">' + av.svg(u) + '</g>';
      }
    }
    return def + '</defs><g clip-path="url(#' + id + ')">' + body + '</g>';
  }
  function avFrame(shape, x, y, w, h, col, sw) { return shape === 'circle' ? '<circle cx="' + n1(x + w / 2) + '" cy="' + n1(y + h / 2) + '" r="' + n1(w / 2) + '" fill="none" stroke="' + col + '" stroke-width="' + sw + '"/>' : '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="10" fill="none" stroke="' + col + '" stroke-width="' + sw + '"/>'; }

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
  /* velo di lettura: attenua texture e motivi dietro intestazione e nome (la grafica non attraversa i dati) */
  function scrim(u, y, h, bg, op, mid) { var id = u + 'sc' + y; return '<defs><linearGradient id="' + id + '" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + mix(bg, '#000000', 0.5) + '" stop-opacity="' + (mid ? 0 : op) + '"/>' + (mid ? '<stop offset=".3" stop-color="' + mix(bg, '#000000', 0.5) + '" stop-opacity="' + op + '"/><stop offset=".75" stop-color="' + mix(bg, '#000000', 0.5) + '" stop-opacity="' + op + '"/>' : '') + '<stop offset="1" stop-color="' + mix(bg, '#000000', 0.5) + '" stop-opacity="0"/></linearGradient></defs><rect x="0" y="' + y + '" width="720" height="' + h + '" fill="url(#' + id + ')"/>'; }
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
    s += '<defs><clipPath id="' + id + '">' + clipEl + '</clipPath>' + rg(u + 'pv', 0.5, 0.42, 0.8, '#000', 0, 0.5) + rg(u + 'pb', 0.5, 0.3, 0.6, mix(a, '#ffffff', 0.35), 0.5, 0) + lg(u + 'pr', [[0, '#fff', 0.18], [0.45, '#fff', 0], [1, '#fff', 0]], 0, 0, 1, 1) + lg(u + 'pf', [[0, '#000', 0], [1, mix(th.bg, '#000000', 0.5), 0.92]], 0, 0, 0, 1) + '</defs>';
    s += '<g transform="translate(0 ' + (o.sh === 0 ? 0 : 6) + ')" opacity=".35"><path d="' + (shape === 'arch' ? arch(x, y, w, h, 0) : 'M' + x + ' ' + y + 'h' + w + 'v' + h + 'h' + (-w) + 'Z') + '" fill="#000"/></g>';
    s += '<g clip-path="url(#' + id + ')"><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="' + mix(th.bg, a, 0.3) + '"/><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#' + u + 'pb)"/>';
    if (o.rays) { var i, rays = ''; for (i = -5; i <= 5; i++) rays += '<path d="M' + cx + ' ' + (y + h * 0.3) + 'L' + n1(cx + i * w * 0.22 - w * 0.03) + ' ' + y + 'H' + n1(cx + i * w * 0.22 + w * 0.03) + 'Z"/>'; s += '<g fill="' + mix(a, '#ffffff', 0.4) + '" fill-opacity="' + (o.leg ? 0.3 : 0.07) + '">' + rays + '</g>'; }
    if (o.leg) s += '<defs>' + rg(u + 'lg', 0.5, 0.45, 0.6, '#fff2b8', 0.7, 0) + '</defs><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="url(#' + u + 'lg)"/>';
    s += avatarPiece(m, x, y, w, h, 'rect', u + 'q', 0.5).replace(/rx="10"/, 'rx="0"');
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
  /* 3.2.5: cornice leggendaria: sfondo con velo cremisi/violetto ai margini (portale) e fascio d'oro dall'alto, solo decorazione di fondo */
  function legBg(W_, H_, u) {
    var vg = '<defs>' + '<radialGradient id="' + u + 'lv" cx="0.5" cy="0.5" r="0.75"><stop offset="0" stop-color="#7a1f4a" stop-opacity="0"/><stop offset="0.6" stop-color="#7a1f4a" stop-opacity="0"/><stop offset="1" stop-color="#7a1f4a" stop-opacity="0.8"/></radialGradient>' + '</defs>';
    return vg + '<rect width="' + W_ + '" height="' + H_ + '" fill="url(#' + u + 'lv)"/><path d="M' + n1(W_ * 0.5 - W_ * 0.07) + ' 0H' + n1(W_ * 0.5 + W_ * 0.07) + 'L' + n1(W_ * 0.5 + W_ * 0.3) + ' ' + n1(H_ * 0.55) + 'H' + n1(W_ * 0.5 - W_ * 0.3) + 'Z" fill="#fff0bd" fill-opacity=".05"/>';
  }
  function build(m, layout, o) {
    o = o || {}; SMALL_ART = !!o.small; var sz = SIZE[layout], Wd = sz[0], Ht = sz[1], u = (o.uid || 'tc') + '_', th = THEMES[m.theme] || THEMES['tema-tva-classico'], fr = FRAMES[m.frame] || FRAMES['cornice-standard-tva'];
    var p = m.xpNeed > 0 ? Math.max(0, Math.min(1, m.xpCur / m.xpNeed)) : 0, g = '', a, nm = m.name || 'Variante', fxId = m.fx;
    var inkO = th.ink, sub = th.sub, acc = th.acc, accT = th.accT, legF = m.frame === LEG_FRAME, legT = m.theme === LEG_THEME, legTi = m.titleId === LEG_TITLE, leg = legF || legT;
    CUR_LT = th.lt;
    var med = function (b, cx, cy, r) { return medal(b.id, cx, cy, r, acc); };
    if (layout === 'wide') {
      a = { cx: 205, cy: 325, r: 120 };
      g += th.draw(Wd, Ht, u) + (legF ? legBg(Wd, Ht, u) : '');
      if (fxId && FX[fxId]) g += FX[fxId](Wd, Ht, a, u);
      g += pan(352, 150, 598, 448, th, u, 14);
      g += emblem(96, 98, 26, acc, 2.2) + T(136, 96, 'TIME VARIANCE AUTHORITY', { size: 24, fill: inkO, mono: 1, ls: 3, weight: 700 }) + T(136, 122, 'ARCHIVI TEMPORALI · CARTA D’IDENTITÀ DELL’AGENTE', { size: 14, fill: sub, mono: 1, ls: 1.5 });
      g += holo(790, 92, 28, u, acc) + codeBars(560, 78, 190, 30, m.id, acc, 0.4);
      g += '<path d="M70 140H930" stroke="' + acc + '" stroke-opacity=".5"/><path d="M70 143H930" stroke="' + acc + '" stroke-opacity=".18"/>';
      g += portrait(m, 70, 160, 270, 330, 'rect', u, th, { leg: leg, bw: 4 });
      var nw = 558, fs = fit(nm, 700, '', SERIF, nw, 70, 30), nmW = clip(nm, 700, '', SERIF, fs, nw);
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
      g += th.draw(Wd, Ht, u) + (legF ? legBg(Wd, Ht, u) : '');
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
      g += th.draw(Wd, Ht, u) + (legF ? legBg(Wd, Ht, u) : '');
      // stelo decorativo e dettagli narrativi in testata
      g += '<g stroke="' + acc + '" stroke-opacity=".5" fill="none"><path d="M80 98H300M420 98H640"/><path d="M80 98l8-6v12zM640 98l-8-6v12z" fill="' + acc + '" fill-opacity=".5" stroke="none"/><path d="M110 108H290M430 108H610" stroke-opacity=".2"/></g>';
      g += emblem(360, 92, 34, acc, 2.8);
      g += T(360, 168, 'TIME VARIANCE AUTHORITY', { size: 28, fill: inkO, mono: 1, ls: 4, weight: 700, anchor: 'middle' }) + T(360, 196, 'ARCHIVI TEMPORALI · SEZIONE VARIANTI', { size: 20, fill: sub, mono: 1, ls: 2, anchor: 'middle' });
      if (fxId && FX[fxId]) g += FX[fxId](Wd, Ht, { cx: 360, cy: 420, r: 200 }, u);
      g += scrim(u, 0, 215, th.bg, 0.72) + scrim(u, 628, 200, th.bg, 0.88, 1);
      g += portrait(m, 120, 214, 480, 432, 'arch', u, th, { leg: leg, rays: 1, fade: 1, bw: 6 });
      // targa identita': nome, titolo, Variant ID
      var nw3 = 560, fs3 = fit(nm, 700, '', SERIF, nw3, 84, 36), nmW3 = clip(nm, 700, '', SERIF, fs3, nw3), nby = 734;   /* 3.2.5: ritratto -12, nome +10: respiro ritratto/nome/titolo */
      g += T(360, nby, nmW3, { size: fs3, weight: 700, fill: inkO, anchor: 'middle' });
      var tw = legTi ? 500 : 560, tsz3 = fit(m.title, 400, 'italic', SERIF, tw, 34, 24);
      g += T(360, nby + 46, clip(m.title, 400, 'italic', SERIF, tsz3, tw), { size: tsz3, italic: 1, fill: inkO, op: 0.9, anchor: 'middle' });
      if (legTi) { var tl = measure(clip(m.title, 400, 'italic', SERIF, tsz3, tw), 'italic 400 ' + tsz3 + 'px ' + SERIF) / 2 + 14; g += '<g transform="translate(' + (360 - tl) + ' ' + (nby + 40) + ')">' + laurel(0, 0, -1, mix(acc, '#ffffff', 0.4)) + '</g><g transform="translate(' + (360 + tl) + ' ' + (nby + 40) + ')">' + laurel(0, 0, 1, mix(acc, '#ffffff', 0.4)) + '</g>'; }
      g += '<rect x="170" y="' + (nby + 66) + '" width="380" height="44" rx="8" fill="#000" fill-opacity=".4" stroke="' + acc + '" stroke-opacity=".6"/>' + T(188, nby + 95, 'VARIANT ID', { size: 20, fill: sub, mono: 1, ls: 1 }) + T(532, nby + 96, m.id, { size: 31, fill: accT, mono: 1, weight: 700, ls: 2, anchor: 'end' });
      // progressione
      var py = 856;
      g += '<g opacity=".58">' + pan(70, py, 580, 254, th, u, 16) + '</g>';   /* 3.2.4: pannello alleggerito, la carta resta protagonista */
      g += T(98, py + 62, 'LV ' + m.level, { size: 60, fill: inkO, weight: 700 }) + T(622, py + 54, m.xp + ' XP', { size: 32, fill: inkO, mono: 1, anchor: 'end' });
      g += bar(98, py + 74, 524, 14, p, th.bar) + T(98, py + 112, m.xpCur + ' / ' + m.xpNeed + ' XP AL LIVELLO ' + (m.level + 1), { size: 22, fill: sub, mono: 1 });
      g += '<path d="M98 ' + (py + 126) + 'H622" stroke="' + acc + '" stroke-opacity=".3"/>';
      m.badges.slice(0, 3).forEach(function (b, i) {
        var bx = 168 + i * 192, lines = wrap(b.name, 400, SERIF, 22, 176, 3);
        g += med(b, bx, py + 164, 30) + lines.map(function (l, k) { return T(bx, py + 212 + k * 24, l, { size: 22, fill: sub, anchor: 'middle' }); }).join('');
      });
      if (!m.badges.length) g += T(360, py + 180, 'NESSUN DISTINTIVO ANCORA', { size: 22, fill: sub, mono: 1, ls: 2, anchor: 'middle' });
      // autenticazione e firma
      g += codeBars(150, 1117, 420, 12, m.id, acc, 0.5) + T(360, 1150, 'TVA ARCHIVES', { size: 22, fill: sub, mono: 1, ls: 8, anchor: 'middle', weight: 700 });
    }
    var fs_ = Wd / 560;   // le cornici sono disegnate su una base di 560 unita' e scalate: stesso peso visivo in tutte le composizioni
    g += '<g transform="scale(' + n1(fs_ * 1000) / 1000 + ')">' + fr(Wd / fs_, Ht / fs_, u) + '</g>';
    var aria = 'Tessera TVA. Agente ' + nm + ', ' + m.id + '. Titolo: ' + m.title + '. Livello ' + m.level + ', ' + m.xp + ' XP.';
    return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 ' + Wd + ' ' + Ht + '" width="' + Wd + '" height="' + Ht + '" role="img" aria-label="' + esc(aria) + '" class="tc-svg tc-' + layout + '" data-layout="' + layout + '">' + g + '</svg>';
  }
  /* miniature per l'editor: stessa grafica della Tessera (stesse definizioni), su una carta semplificata senza testo */
  function miniCard(frameId, themeId, uid, fxId) {
    var W_ = 560, H_ = 400, u = (uid || 'mc') + '_', th = THEMES[themeId] || THEMES['tema-tva-classico'], fr = FRAMES[frameId] || FRAMES['cornice-standard-tva'], acc = th.acc, i, s = th.draw(W_, H_, u);
    if (fxId && FX[fxId]) s += FX[fxId](W_, H_, { cx: 110, cy: 200, r: 70 }, u);
    s += pan(196, 96, 330, 250, th, u, 10) + emblem(60, 62, 18, acc, 2) + '<rect x="90" y="56" width="150" height="9" rx="4" fill="' + th.ink + '" fill-opacity=".8"/><path d="M40 86H520" stroke="' + acc + '" stroke-opacity=".5"/>';
    s += '<rect x="40" y="100" width="124" height="176" rx="3" fill="#2a1219" stroke="' + acc + '" stroke-width="2.4"/><circle cx="102" cy="162" r="26" fill="' + th.sub + '"/><path d="M58 274c0-34 20-52 44-52s44 18 44 52z" fill="' + th.sub + '"/>';
    s += '<rect x="214" y="112" width="250" height="26" rx="5" fill="' + th.ink + '"/><rect x="214" y="150" width="170" height="12" rx="5" fill="' + th.ink + '" fill-opacity=".6"/><rect x="214" y="176" width="130" height="14" rx="5" fill="' + th.accT + '"/><rect x="214" y="216" width="70" height="20" rx="5" fill="' + th.ink + '"/><rect x="214" y="250" width="290" height="9" rx="4.5" fill="#fff" fill-opacity=".14"/><rect x="214" y="250" width="70" height="9" rx="4.5" fill="' + th.bar + '"/>';
    for (i = 0; i < 3; i++) s += '<circle cx="' + (80 + i * 58) + '" cy="322" r="21" fill="rgba(0,0,0,.35)" stroke="' + acc + '" stroke-width="2.2"/>';
    var fs_ = 1; return s + fr(W_, H_, u);
  }
  function thumb(kind, id, uid, ctx) {
    var w = 280, h = 200, u = (uid || 'th') + '_', body; ctx = ctx || {};
    if (kind === 'tema' && ctx.model) {   /* 3.2.5: anteprima reale del tema = la stessa composizione compatta della Tessera (stessi componenti), con ritratto leggero */
      var tm = {}, k2; for (k2 in ctx.model) tm[k2] = ctx.model[k2]; tm.theme = id; tm.fx = null; tm.titleId = null; if (ctx.frame) tm.frame = ctx.frame;
      return build(tm, 'compact', { uid: uid, small: true }).replace(/ width="560" height="400"/, '').replace(/ role="img" aria-label="[^"]*"/, '').replace('class="tc-svg tc-compact"', 'class="tc-thumb tc-thumb-real" aria-hidden="true" focusable="false"');
    }
    if (kind === 'tema') body = '<g transform="scale(' + n1(w / 560) + ')">' + miniCard('cornice-standard-tva', id, uid, null) + '</g>';
    else if (kind === 'cornice') body = '<g transform="scale(' + n1(w / 560) + ')">' + miniCard(id, ctx.theme || 'tema-tva-classico', uid, null) + '</g>';
    else { var t = THEMES[ctx.theme || 'tema-tva-classico']; body = '<g transform="scale(' + n1(w / 560) + ')">' + miniCard(ctx.frame || 'cornice-standard-tva', ctx.theme || 'tema-tva-classico', uid, id) + '</g>'; }
    return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + w + ' ' + h + '" class="tc-thumb" aria-hidden="true" focusable="false"><g class="tc-still">' + body + '</g></svg>';
  }
  function avatarThumb(model, uid) {
    var u = (uid || 'av') + '_';
    return '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 100" class="tc-thumb tc-thumb-av" aria-hidden="true" focusable="false">' + avatarPiece(model, 0, 0, 100, 100, 'circle', u, undefined, true) + '</svg>';
  }
  W.tvaCardArt = { themeBg: function (id) { return (THEMES[id] || THEMES['tema-tva-classico']).bg; }, avatarArt: { load: loadAvatarArt, loaded: function () { return Object.keys(AV_IMG); }, _inject: function (id, url) { if (url) AV_IMG[id] = url; else delete AV_IMG[id]; } }, build: build, thumb: thumb, avatarThumb: avatarThumb, avatars: AVATARS, sizes: SIZE, frames: Object.keys(FRAMES), themes: Object.keys(THEMES), fx: Object.keys(FX), glyph: glyph, SERIF: SERIF, MONO: MONO };
})();
/* TCART-JS-END */
