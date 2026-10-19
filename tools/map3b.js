    /* ==== MAP3B:BEGIN ====
       Mappa interattiva del Multiverso (FASE 3B). Costruita esclusivamente sul modello condiviso tvaUniverse (sola lettura):
       nessun dato, collegamento o attribuzione viene aggiunto. Layout fisso e curato (nessuna simulazione), scena SVG unica,
       un solo attributo transform aggiornato durante i gesti. Le nebulose sono raggruppamenti visivi per famiglia editoriale, NON relazioni. */
    var MP_POS = {
      'uni-earth-199999-mcu': [430, 700],
      'uni-tva-fuori-dal-tempo': [430, 490], 'uni-rami-di-what-if': [280, 390], 'uni-earth-838': [580, 390], 'uni-earth-828': [430, 300],
      'uni-earth-10005-fox-verse': [700, 620],
      'uni-earth-96283-raimi-verse': [240, 590], 'uni-earth-120703-garfield-verse': [130, 720], 'uni-spider-noir-verse': [85, 450], 'uni-spider-verse-sony-animato': [90, 590],
      'uni-sony-s-spider-man-universe-ssu': [240, 870],
      'uni-blade-verse': [100, 1040], 'uni-daredevil-elektra-verse': [240, 1020], 'uni-ghost-rider-verse': [370, 1070], 'uni-hulk-2003-verse': [90, 1180],
      'uni-fantastic-four-1994': [225, 1180], 'uni-earth-121698': [350, 1200], 'uni-earth-trn123': [170, 1310],
      'uni-x-men-97-verse': [490, 1040], 'uni-your-friendly-neighborhood-spider-man-verse': [650, 990], 'uni-marvel-productions-universe-anni-80': [770, 1070],
      'uni-marvel-productions-universe-anni-90': [770, 1200], 'uni-marvel-animation-universe-2006-2017': [730, 1330], 'uni-continuity-animate-isolate-minori': [540, 1340],
      'uni-legion-verse': [500, 1180], 'uni-the-gifted-verse': [640, 1160], 'uni-marvel-zombies-verse': [790, 900]
    };
    // etichette abbreviate: usate solo quando il nome completo non entra; il nome completo e' sempre in selezione, anteprima, elenco e dossier
    var MP_SH = {
      'uni-earth-199999-mcu': 'MCU', 'uni-earth-96283-raimi-verse': 'Raimi', 'uni-earth-120703-garfield-verse': 'Garfield', 'uni-sony-s-spider-man-universe-ssu': 'SSU',
      'uni-earth-10005-fox-verse': 'Fox', 'uni-fantastic-four-1994': 'FF ’94', 'uni-earth-121698': 'E-121698', 'uni-earth-trn123': 'TRN123', 'uni-blade-verse': 'Blade',
      'uni-daredevil-elektra-verse': 'Daredevil', 'uni-ghost-rider-verse': 'Ghost Rider', 'uni-spider-noir-verse': 'Spider-Noir', 'uni-hulk-2003-verse': 'Hulk ’03',
      'uni-earth-828': 'E-828', 'uni-earth-838': 'E-838', 'uni-tva-fuori-dal-tempo': 'TVA', 'uni-rami-di-what-if': 'What If', 'uni-x-men-97-verse': 'X-Men ’97',
      'uni-your-friendly-neighborhood-spider-man-verse': 'Friendly Spidey', 'uni-marvel-productions-universe-anni-80': 'Prod. ’80', 'uni-marvel-productions-universe-anni-90': 'Prod. ’90',
      'uni-marvel-animation-universe-2006-2017': 'Animation ’06-17', 'uni-continuity-animate-isolate-minori': 'Animate minori', 'uni-spider-verse-sony-animato': 'Spider-Verse',
      'uni-legion-verse': 'Legion', 'uni-the-gifted-verse': 'Gifted', 'uni-marvel-zombies-verse': 'Zombies'
    };
    var MP_ACC = { mcu: '#D2B184', whatif: '#DB777C', fox: '#E3C9A0', spiderverse: '#C2566B', sony: '#F2E8D8', legacy: '#B08968', animazione: '#E8A598' };
    var MP_FN = { whatif: 'WHAT IF · TVA', fox: 'FOX', spiderverse: 'SPIDER-VERSE', sony: 'SONY', legacy: 'LEGACY', animazione: 'ANIMAZIONE' };
    var MP_CAP = { whatif: [430, 235], fox: [700, 565], spiderverse: [150, 380], sony: [240, 815], legacy: [215, 955], animazione: [640, 935] };
    var MP_FAMORD = ['mcu', 'whatif', 'fox', 'spiderverse', 'sony', 'legacy', 'animazione'];
    var MP_NATORD = ['principale', 'autonomo', 'diramazione', 'raggruppamento', 'luogo'];
    var MP_NATLBL = { principale: 'Continuità principale', autonomo: 'Universo autonomo', diramazione: 'Diramazione / alternativo', raggruppamento: 'Raggruppamento editoriale', luogo: 'Luogo narrativo' };
    var MP_ST = { confermato: { col: '#D2B184', da: '', w: 2.4, ic: '●', cls: 'ok' }, legacy: { col: '#F2E8D8', da: '6 5', w: 1.6, ic: '○', cls: 'lg' }, verificare: { col: '#DB777C', da: '1.5 5', w: 1.9, ic: '◇', cls: 'vf' } };
    var MP_CW = 860, MP_CH = 1500, MP_BB = { x0: 60, y0: 215, x1: 830, y1: 1405 }, MP_ZMAX = 6;
    function mpFresh() { return { mode: 'map', v: null, sel: null, focus: null, hl: null, panel: null, q: '', rel: { confermato: 1, legacy: 1, verificare: 1 }, fam: 'tutte', nat: 'tutti', onlyLinks: false }; }
    ST.mp = mpFresh();
    var MPD = null; // dati derivati dal modello, costruiti una sola volta
    function mpNorm(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
    function mpEsc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
    function mpData() {
      if (MPD) return MPD;
      var ids = UM.ids(), nodes = {}, order = [], spare = 0;
      ids.forEach(function (id) {
        var m = UM.get(id), d = UNI[id] || {}, p = MP_POS[id];
        if (!p) { p = [120 + (spare % 5) * 150, 1450 + Math.floor(spare / 5) * 90]; spare++; } // un universo futuro senza coordinate non si perde mai
        var nk = nat(d).k, fam = m.famiglie && m.famiglie[0] ? m.famiglie[0] : 'mcu';
        nodes[id] = { id: id, nome: m.nome, breve: m.breve, short: MP_SH[id] || m.breve || m.nome, natura: m.natura, nk: nk, fam: fam, x: p[0], y: p[1],
          nt: m.titoli.length, np: d.personaggi || 0, cnt: m.conteggi, nlink: (m.conteggi.confermato || 0) + (m.conteggi.legacy || 0) + (m.conteggi.verificare || 0), spec: m.speciali || [],
          titles: m.titoli.map(function (t) { return mpNorm(t.title); }), famNome: fam === 'mcu' ? 'MCU' : ((FAM[fam] && FAM[fam].nome) || fam) };
        order.push(id);
      });
      var links = UM.links().filter(function (l) { return nodes[l.a] && nodes[l.b]; });
      var cent = {}; // baricentro e raggio delle nebulose (solo grafica)
      MP_FAMORD.forEach(function (f) {
        var arr = order.filter(function (i) { return nodes[i].fam === f; }); if (!arr.length) return;
        var cx = 0, cy = 0; arr.forEach(function (i) { cx += nodes[i].x; cy += nodes[i].y; }); cx /= arr.length; cy /= arr.length;
        var r = 0; arr.forEach(function (i) { r = Math.max(r, Math.hypot(nodes[i].x - cx, nodes[i].y - cy)); });
        cent[f] = { x: cx, y: cy, r: Math.max(110, r + 95) };
      });
      var stars = []; for (var i = 0; i < 96; i++) stars.push([Math.abs(Math.sin(i * 12.9898) * 43758.5453) % 1 * MP_CW, 120 + Math.abs(Math.sin(i * 78.233) * 43758.5453) % 1 * (MP_CH - 120), 0.7 + (i % 3) * 0.45, 0.25 + (i % 4) * 0.1]);
      var md = 1e9; order.forEach(function (a, i) { order.slice(i + 1).forEach(function (b2) { md = Math.min(md, Math.hypot(nodes[a].x - nodes[b2].x, nodes[a].y - nodes[b2].y)); }); });
      MPD = { nodes: nodes, order: order, links: links, cent: cent, stars: stars, minD: md };
      return MPD;
    }
    function mpOpen(extra) {
      if (tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante');
      ST.mp = mpFresh(); if (extra) Object.keys(extra).forEach(function (k) { ST.mp[k] = extra[k]; });
      ST.screen = 'mappa'; ST.uid = null; if (!tog.checked) show(); draw(); setScroll(0);
    }
    function openMappa(uid) { mpOpen(uid ? { sel: uid } : null); }
    function mpSnap() { try { return JSON.parse(JSON.stringify(ST.mp)); } catch (e) { return mpFresh(); } }
    var MPR = { ro: null, cleanup: null, reduce: false };
    try { MPR.reduce = !!(W.matchMedia && W.matchMedia('(prefers-reduced-motion: reduce)').matches); } catch (eRm) {}

    /* ---- forme dei nodi (stesso linguaggio nella mappa, nella legenda e nell'elenco): forma = natura, anello = famiglia ---- */
    function mpShape(nk, r, acc, o) {
      o = o || {}; var sw = o.sel ? 3 : 1.9, fill = o.sel ? '#2a1417' : '#1b1b20', dot = '<circle r="' + Math.max(1.8, r * 0.26).toFixed(1) + '" fill="' + acc + '" fill-opacity=".85"/>';
      if (nk === 'principale') return '<circle r="' + (r + 8) + '" fill="none" stroke="' + acc + '" stroke-opacity=".45" stroke-width="1.2"/><circle r="' + (r + 3.5) + '" fill="none" stroke="' + acc + '" stroke-opacity=".25" stroke-width="1" stroke-dasharray="2 3"/><circle r="' + r + '" fill="' + fill + '" stroke="' + acc + '" stroke-width="' + (sw + 0.4) + '"/>' + dot;
      if (nk === 'diramazione') return '<path d="M0 ' + (-r - 1) + 'L' + (r + 1) + ' 0L0 ' + (r + 1) + 'L' + (-r - 1) + ' 0Z" fill="' + fill + '" stroke="' + acc + '" stroke-width="' + sw + '" stroke-linejoin="round"/>' + dot;
      if (nk === 'raggruppamento') return '<rect x="' + (-r * 0.92) + '" y="' + (-r * 0.92) + '" width="' + (r * 1.84) + '" height="' + (r * 1.84) + '" rx="4" fill="' + fill + '" stroke="' + acc + '" stroke-width="' + sw + '" stroke-dasharray="3.5 2.5"/>' + dot;
      if (nk === 'luogo') { var pts = []; for (var i = 0; i < 6; i++) pts.push((r * 1.06 * Math.cos(Math.PI / 3 * i + Math.PI / 6)).toFixed(1) + ',' + (r * 1.06 * Math.sin(Math.PI / 3 * i + Math.PI / 6)).toFixed(1)); return '<polygon points="' + pts.join(' ') + '" fill="' + fill + '" stroke="' + acc + '" stroke-width="' + sw + '" stroke-linejoin="round"/>' + dot; }
      return '<circle r="' + r + '" fill="' + fill + '" stroke="' + acc + '" stroke-width="' + sw + '"/>' + dot;
    }
    function mpIcon(nk, acc, size) {
      var s = el('span', 'mp-ic'); s.setAttribute('aria-hidden', 'true'); size = size || 26;
      s.innerHTML = '<svg width="' + size + '" height="' + size + '" viewBox="-17 -17 34 34" focusable="false"><g>' + mpShape(nk, nk === 'principale' ? 6.5 : 8, acc) + '</g></svg>'; return s;
    }
    function mpLineSample(stato) {
      var c = MP_ST[stato], s = el('span', 'mp-ln'); s.setAttribute('aria-hidden', 'true');
      s.innerHTML = '<svg width="38" height="12" viewBox="0 0 38 12" focusable="false"><line x1="2" y1="6" x2="36" y2="6" stroke="' + c.col + '" stroke-width="' + c.w + '"' + (c.da ? ' stroke-dasharray="' + c.da + '"' : '') + ' stroke-linecap="round"/></svg>'; return s;
    }
    function mpStBadge(stato, n) {
      var c = MP_ST[stato], b = el('span', 'mp-b mp-b-' + c.cls, c.ic + ' ' + (n != null ? n + ' ' : '') + UM.stati[stato]);
      return b;
    }
    // filtri condivisi da mappa ed elenco
    function mpVis(n) {
      var f = ST.mp;
      if (f.fam !== 'tutte' && n.fam !== f.fam) return false;
      if (f.nat !== 'tutti' && n.nk !== f.nat) return false;
      if (f.onlyLinks && !mpLinksOf(n.id).length) return false;
      return true;
    }
    function mpLinksOf(id) { var D2 = mpData(); return D2.links.filter(function (l) { return (l.a === id || l.b === id) && ST.mp.rel[l.stato]; }); }
    function mpFiltersOn() { var f = ST.mp, n = 0; if (f.fam !== 'tutte') n++; if (f.nat !== 'tutti') n++; if (f.onlyLinks) n++; if (!(f.rel.confermato && f.rel.legacy && f.rel.verificare)) n++; return n; }
    function mpMatch(q) {
      var D2 = mpData(), nq = mpNorm(q).trim(); if (!nq) return [];
      var out = [];
      D2.order.forEach(function (id) {
        var n = D2.nodes[id]; if (!mpVis(n)) return;
        var hay = mpNorm(n.nome + ' ' + n.breve + ' ' + n.short + ' ' + n.famNome), sc = 0, via = '';
        if (hay.indexOf(nq) !== -1) sc = mpNorm(n.short).indexOf(nq) === 0 || mpNorm(n.breve).indexOf(nq) === 0 ? 3 : 2;
        else { for (var i = 0; i < n.titles.length; i++) if (n.titles[i].indexOf(nq) !== -1) { sc = 1; via = UM.get(id).titoli[i].title; break; } }
        if (sc) out.push({ id: id, sc: sc, via: via });
      });
      out.sort(function (a, b) { return b.sc - a.sc; }); return out;
    }
    function mpCountsTxt(n) { return n.nt + (n.nt === 1 ? ' titolo' : ' titoli') + ' · ' + n.np + (n.np === 1 ? ' personaggio' : ' personaggi'); }

    /* ---------- schermata ---------- */
    function renderMappa() {
      if (MPR.cleanup) { MPR.cleanup(); MPR.cleanup = null; }
      var D2 = mpData(), M = ST.mp, NS = 'http://www.w3.org/2000/svg';
      body.className = 'a2-scroll a2-mapscr'; body.textContent = ''; setTitle('Mappa del Multiverso', '27 universi');
      /* barra: ricerca · filtri · Mappa/Elenco */
      var bar = el('div', 'mp-bar'), sb = el('form', 'mp-search'); sb.setAttribute('role', 'search'); sb.addEventListener('submit', function (e) { e.preventDefault(); if (M.mode === 'map') { var r = mpMatch(inp.value); if (r.length) pickSearch(r[0].id); } });
      sb.appendChild(art('cerca'));
      var inp = D.createElement('input'); inp.type = 'search'; inp.id = 'mpSearch'; inp.value = M.q || ''; inp.placeholder = 'Cerca…'; inp.autocomplete = 'off';
      inp.setAttribute('aria-label', 'Cerca un universo, un titolo o una famiglia'); inp.setAttribute('enterkeyhint', 'search'); sb.appendChild(inp);
      var fb = btn('mp-fbtn', null, function () { mpPanel(M.panel === 'filtri' ? null : 'filtri'); }); fb.id = 'mpFiltri';
      fb.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M4 7h16M7 12h10M10 17h4"/></svg>';
      fb.setAttribute('aria-label', 'Filtri'); var fbDot = el('i', 'mp-dot'); fbDot.hidden = true; fb.appendChild(fbDot);
      var seg = el('div', 'mp-seg'); seg.setAttribute('role', 'group'); seg.setAttribute('aria-label', 'Vista');
      var sbM = btn('mp-sg', null, function () { setMode('map'); }), sbL = btn('mp-sg', null, function () { setMode('list'); });
      sbM.id = 'mpModeMap'; sbL.id = 'mpModeList';
      sbM.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="3"/><circle cx="5" cy="6" r="1.8"/><circle cx="19" cy="7" r="1.8"/><circle cx="18" cy="18" r="1.8"/><path d="M10 10.5L6.2 7.2M14.5 11l3-2.6M13.5 14.2l3.4 2.6"/></svg><span>Mappa</span>';
      sbL.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><path d="M9 6h11M9 12h11M9 18h11M4.5 6h.01M4.5 12h.01M4.5 18h.01"/></svg><span>Elenco</span>';
      sbM.setAttribute('aria-label', 'Vista mappa'); sbL.setAttribute('aria-label', 'Vista elenco');
      seg.appendChild(sbM); seg.appendChild(sbL);
      bar.appendChild(sb); bar.appendChild(fb); bar.appendChild(seg); body.appendChild(bar);

      var wrap = el('div', 'mp-wrap'); body.appendChild(wrap);
      var live = el('div', 'mp-vh'); live.setAttribute('role', 'status'); live.setAttribute('aria-live', 'polite'); wrap.appendChild(live);
      var sugg = el('div', 'mp-sugg'); sugg.hidden = true; sugg.setAttribute('role', 'listbox'); sugg.setAttribute('aria-label', 'Risultati'); wrap.appendChild(sugg);
      var mapBox = el('div', 'mp-mapbox'), listBox = el('div', 'mp-list'); wrap.appendChild(mapBox); wrap.appendChild(listBox);
      var panelHost = el('div', 'mp-panelhost'); wrap.appendChild(panelHost);

      /* sfondo: procedurale; se esiste l'illustrazione opzionale mappa_sfondo.webp viene adottata da sola */
      var bg = el('div', 'mp-bg'); bg.setAttribute('aria-hidden', 'true'); mapBox.appendChild(bg);
      try { hmLoad(bg, [HM_DIR + 'mappa_sfondo.webp'], 'mp-bg-img', null); } catch (eBg) {}
      var svg = D.createElementNS(NS, 'svg'); svg.setAttribute('class', 'mp-stage'); svg.setAttribute('role', 'group'); svg.setAttribute('tabindex', '0');
      svg.setAttribute('aria-label', 'Mappa del Multiverso: 27 universi. Trascina per spostare, pizzica per ingrandire. La vista Elenco offre le stesse informazioni in forma di testo.');
      var defs = '<defs>'; MP_FAMORD.forEach(function (f) { defs += '<radialGradient id="mpn_' + f + '"><stop offset="0" stop-color="' + MP_ACC[f] + '" stop-opacity=".2"/><stop offset=".55" stop-color="' + MP_ACC[f] + '" stop-opacity=".07"/><stop offset="1" stop-color="' + MP_ACC[f] + '" stop-opacity="0"/></radialGradient><radialGradient id="mpg_' + f + '"><stop offset="0" stop-color="' + MP_ACC[f] + '" stop-opacity=".34"/><stop offset="1" stop-color="' + MP_ACC[f] + '" stop-opacity="0"/></radialGradient>'; });
      defs += '<radialGradient id="mpn_core"><stop offset="0" stop-color="#7a2a34" stop-opacity=".30"/><stop offset="1" stop-color="#7a2a34" stop-opacity="0"/></radialGradient></defs>';
      svg.innerHTML = defs + '<g class="mp-world"><g class="mp-bgl"></g><g class="mp-dyn"></g></g>';
      mapBox.appendChild(svg);
      var world = svg.querySelector('.mp-world'), bgl = svg.querySelector('.mp-bgl'), dyn = svg.querySelector('.mp-dyn');
      /* strato statico: nebulose (gradienti radiali, nessun filtro), polvere di stelle, portali dimensionali dell'MCU e della TVA */
      var sh = '<circle cx="430" cy="640" r="520" fill="url(#mpn_core)"/>';
      MP_FAMORD.forEach(function (f) { var c = D2.cent[f]; if (c) sh += '<circle cx="' + c.x.toFixed(0) + '" cy="' + c.y.toFixed(0) + '" r="' + (c.r * 1.55).toFixed(0) + '" fill="url(#mpn_' + f + ')"/>'; });
      D2.stars.forEach(function (t) { sh += '<circle cx="' + t[0].toFixed(0) + '" cy="' + t[1].toFixed(0) + '" r="' + t[2] + '" fill="#F2E8D8" fill-opacity="' + t[3] + '"/>'; });
      var mc = D2.nodes[MCU], tv = D2.nodes['uni-tva-fuori-dal-tempo'];
      if (mc) sh += '<g fill="none" stroke="#D2B184" stroke-opacity=".16"><circle cx="' + mc.x + '" cy="' + mc.y + '" r="78"/><circle cx="' + mc.x + '" cy="' + mc.y + '" r="118" stroke-dasharray="2 7"/><circle cx="' + mc.x + '" cy="' + mc.y + '" r="165" stroke-opacity=".09"/></g>';
      if (tv) sh += '<g fill="none" stroke="#DB777C" stroke-opacity=".18"><circle cx="' + tv.x + '" cy="' + tv.y + '" r="52" stroke-dasharray="1.5 6"/></g>';
      bgl.innerHTML = sh;

      /* ---- vista: z relativo al fit, centro in coordinate del mondo (stabile con rotazione e resize) ---- */
      var vw = 0, vh = 0, padB = 72, fit = 1, s = 1, tx = 0, ty = 0, paintedS = -1, tween = null, raf = 0;
      function measure() {
        var r = mapBox.getBoundingClientRect(); vw = Math.max(1, r.width); vh = Math.max(1, r.height);
        var bw = MP_BB.x1 - MP_BB.x0, bh = MP_BB.y1 - MP_BB.y0, padx = 30, pady = 26; // i bersagli dei nodi estremi restano interamente nell'area
        padB = 72; // fascia in basso riservata a Legenda, Fuori mappa e Adatta: a vista d'insieme non coprono nodi
        fit = Math.min((vw - padx * 2) / bw, (vh - pady - padB) / bh);
      }
      function clampView(ns, ntx, nty) {
        ns = Math.max(fit * 0.98, Math.min(fit * MP_ZMAX, ns));
        var minx = vw * 0.28 - MP_BB.x1 * ns, maxx = vw * 0.72 - MP_BB.x0 * ns, miny = vh * 0.28 - MP_BB.y1 * ns, maxy = vh * 0.62 - MP_BB.y0 * ns;
        return { s: ns, x: Math.min(maxx, Math.max(minx, ntx)), y: Math.min(maxy, Math.max(miny, nty)) };
      }
      function setView(ns, ntx, nty) { var c = clampView(ns, ntx, nty); s = c.s; tx = c.x; ty = c.y; applyView(); }
      function applyView() {
        world.setAttribute('transform', 'translate(' + tx.toFixed(2) + ' ' + ty.toFixed(2) + ') scale(' + s.toFixed(4) + ')');
        M.v = { z: +(s / fit).toFixed(4), cx: +((vw / 2 - tx) / s).toFixed(1), cy: +((vh / 2 - ty) / s).toFixed(1) };
      }
      function viewFromState() {
        if (M.v) { var ns = M.v.z * fit; setView(ns, vw / 2 - M.v.cx * ns, vh / 2 - M.v.cy * ns); }
        else fitView(false);
      }
      function fitView(anim) {
        var ns = fit, cx = (MP_BB.x0 + MP_BB.x1) / 2, cy = (MP_BB.y0 + MP_BB.y1) / 2; goTo(ns, cx, cy, anim, padB - 26);
      }
      function goTo(ns, wx, wy, anim, dy) { // centra (wx,wy) con scala ns; dy sposta il centro verso l'alto (spazio per l'anteprima)
        var c = clampView(ns, vw / 2 - wx * ns, (vh - (dy || 0)) / 2 - wy * ns);
        if (!anim || MPR.reduce) { cancelTween(); s = c.s; tx = c.x; ty = c.y; applyView(); settle(); return; }
        cancelTween(); var f = { s: s, x: tx, y: ty }, t0 = performance.now(), dur = 320;
        tween = function (now) {
          var p = Math.min(1, (now - t0) / dur), e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
          s = f.s + (c.s - f.s) * e; tx = f.x + (c.x - f.x) * e; ty = f.y + (c.y - f.y) * e; applyView();
          if (p < 1) raf = requestAnimationFrame(tween); else { tween = null; settle(); }
        };
        raf = requestAnimationFrame(tween);
      }
      function cancelTween() { if (tween) { cancelAnimationFrame(raf); tween = null; } }
      function zoomAt(px, py, factor, anim) {
        var ns = Math.max(fit, Math.min(fit * MP_ZMAX, s * factor)); if (ns === s) return;
        var wx = (px - tx) / s, wy = (py - ty) / s;
        var c = clampView(ns, px - wx * ns, py - wy * ns);
        if (!anim || MPR.reduce) { cancelTween(); s = c.s; tx = c.x; ty = c.y; applyView(); settle(); return; }
        cancelTween(); var f = { s: s, x: tx, y: ty }, t0 = performance.now(), dur = 240;
        tween = function (now) { var p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3); s = f.s + (c.s - f.s) * e; tx = f.x + (c.x - f.x) * e; ty = f.y + (c.y - f.y) * e; applyView(); if (p < 1) raf = requestAnimationFrame(tween); else { tween = null; settle(); } };
        raf = requestAnimationFrame(tween);
      }

      /* ---- scena dinamica: archi, aloni, nodi, etichette (ricostruita solo a fine gesto o al cambio di stato) ---- */
      function nodeScale() { var z = s / fit; return (1 / s) * Math.min(1.9, 1 + 0.3 * Math.log2(Math.max(1, z))); }
      function radius(n) { return n.nk === 'principale' ? 14 : (n.nt >= 12 ? 12 : (n.nt >= 5 ? 10 : 8)); }
      function related(sel) {
        var set = {}; if (!sel) return set; set[sel] = 1;
        D2.links.forEach(function (l) { if (!M.rel[l.stato]) return; if (l.a === sel) set[l.b] = 1; else if (l.b === sel) set[l.a] = 1; });
        return set;
      }
      function paint() {
        paintedS = s; var k = nodeScale(), g = k * s, hitR = Math.max(9, Math.min(23, (D2.minD * s / 2 - 0.5) / g)), rel = related(M.sel), focusSet = M.focus ? rel : null, out = '';
        // archi: pieni (documentato nella guida), tratteggiati (legacy), puntinati (da verificare)
        D2.links.forEach(function (l) {
          if (!M.rel[l.stato]) return; var a = D2.nodes[l.a], b = D2.nodes[l.b], c = MP_ST[l.stato];
          if (!mpVis(a) && !mpVis(b)) return;
          var mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2, dx = b.x - a.x, dy = b.y - a.y, cx = mx - dy * 0.12, cy = my + dx * 0.12;
          var on = !M.sel || (l.a === M.sel || l.b === M.sel), op = M.sel ? (on ? 1 : 0.1) : (l.stato === 'confermato' ? 0.9 : 0.78);
          if (focusSet && !on) op = 0;
          var d = 'M' + a.x + ' ' + a.y + 'Q' + cx.toFixed(1) + ' ' + cy.toFixed(1) + ' ' + b.x + ' ' + b.y, w = c.w * (on && M.sel ? 1.25 : 1) / s;
          if (l.stato === 'confermato') out += '<path d="' + d + '" fill="none" stroke="' + c.col + '" stroke-opacity="' + (op * 0.13).toFixed(2) + '" stroke-width="' + (w * 4).toFixed(3) + '" stroke-linecap="round"/>';
          out += '<path class="mp-arc mp-arc-' + c.cls + '" data-a="' + l.a + '" data-b="' + l.b + '" d="' + d + '" fill="none" stroke="' + c.col + '" stroke-opacity="' + op + '" stroke-width="' + w.toFixed(3) + '"' +
            (c.da ? ' stroke-dasharray="' + c.da.split(' ').map(function (v) { return (v / s * 1.0).toFixed(3); }).join(' ') + '"' : '') + ' stroke-linecap="round"/>';
        });
        // aloni punteggiati (Fuori mappa: evidenziazione di universi in relazione con un elemento speciale)
        var hl = M.hl ? M.hl.ids || [] : [], hlx = M.hl ? M.hl.incerti || [] : [];
        hl.concat(hlx).forEach(function (id) { var n = D2.nodes[id]; if (!n) return; out += '<circle class="mp-halo' + (hlx.indexOf(id) !== -1 ? ' mp-halo-q' : '') + '" cx="' + n.x + '" cy="' + n.y + '" r="' + (31 * k).toFixed(3) + '" fill="none" stroke="#E3C9A0" stroke-width="' + (1.8 * k).toFixed(3) + '" stroke-dasharray="' + (1.5 * k).toFixed(3) + ' ' + (5.5 * k).toFixed(3) + '" stroke-linecap="round"/>'; });
        // nodi
        D2.order.forEach(function (id) {
          var n = D2.nodes[id], vis = mpVis(n), isSel = M.sel === id, acc = MP_ACC[n.fam], dim = (M.sel && !rel[id]) || (focusSet && !focusSet[id]);
          var cls = 'mp-n' + (isSel ? ' sel' : '') + (!vis ? ' off' : (dim ? ' dim' : ''));
          out += '<g class="' + cls + '" data-u="' + id + '" transform="translate(' + n.x + ' ' + n.y + ') scale(' + k.toFixed(5) + ')" role="button" tabindex="' + (vis ? 0 : -1) + '" aria-pressed="' + (isSel ? 'true' : 'false') + '"' + (vis ? '' : ' aria-hidden="true"') +
            ' aria-label="' + mpEsc(n.nome + ', ' + n.natura + (n.fam !== 'mcu' ? ', famiglia ' + n.famNome : '') + ', ' + mpCountsTxt(n) + ', ' + n.nlink + (n.nlink === 1 ? ' collegamento' : ' collegamenti')) + '">' +
            '<circle r="' + (radius(n) * 3.1) + '" fill="url(#mpg_' + n.fam + ')" class="mp-glow"/>' + mpShape(n.nk, radius(n) + (isSel ? 2 : 0), acc, { sel: isSel }) +
            (isSel ? '<circle r="' + (radius(n) + (n.nk === 'principale' ? 17 : 13)) + '" fill="none" stroke="' + acc + '" stroke-opacity=".7" stroke-dasharray="2 4" class="mp-selring"/>' : '') +
            '<circle r="' + hitR.toFixed(2) + '" fill="transparent" class="mp-hit"/></g>';
        });
        // didascalie di famiglia (decorative) ed etichette dei nodi con rilevamento delle collisioni
        MP_FAMORD.forEach(function (f) {
          if (f === 'mcu' || !MP_CAP[f]) return; var p = MP_CAP[f];
          out += '<text class="mp-cap" aria-hidden="true" x="' + p[0] + '" y="' + p[1] + '" text-anchor="middle" font-size="' + (11 / s).toFixed(3) + '" letter-spacing="' + (2.2 / s).toFixed(3) + '" fill="' + MP_ACC[f] + '" fill-opacity="' + (M.sel ? 0.4 : 0.88) + '">' + MP_FN[f] + '</text>';
        });
        out += labels(g, rel, focusSet);
        dyn.innerHTML = out;
      }
      function labels(g, rel, focusSet) {
        var placed = [], res = '', fs = 12.5;
        MP_FAMORD.forEach(function (f) { if (f === 'mcu' || !MP_CAP[f]) return; var w = MP_FN[f].length * 9.6 + 8, X = MP_CAP[f][0] * s, Y = MP_CAP[f][1] * s; placed.push([X - w / 2, Y - 14, X + w / 2, Y + 5]); });
        // i comandi fissi (zoom, legenda) sono ostacoli: nessuna etichetta viene piazzata sotto di loro
        try { var mb = mapBox.getBoundingClientRect(); [ctl, pills].forEach(function (c) { if (!c || c.hidden) return; Array.prototype.forEach.call(c.children, function (k2) { var r = k2.getBoundingClientRect(); if (r.width) placed.push([r.left - mb.left - tx - 3, r.top - mb.top - ty - 3, r.right - mb.left - tx + 3, r.bottom - mb.top - ty + 3]); }); }); } catch (eO) {}
        var order0 = null, order = D2.order.filter(function (id) { return mpVis(D2.nodes[id]); });
        var prio = function (id) { return (id === M.sel ? 1000 : 0) + (rel[id] && M.sel ? 500 : 0) + (M.hl && (M.hl.ids || []).indexOf(id) !== -1 ? 300 : 0) + (id === MCU ? 200 : 0) + D2.nodes[id].nt; };
        order.sort(function (a, b) { return prio(b) - prio(a); });
        // ostacoli: i dischi di tutti i nodi
        var obst = D2.order.map(function (id) { var n = D2.nodes[id], r = (radius(n) + (n.nk === 'principale' ? 9 : 2)) * g + 3; return [n.x * s - r, n.y * s - r, n.x * s + r, n.y * s + r]; });
        function hit(r) { for (var i = 0; i < placed.length; i++) { var p = placed[i]; if (r[0] < p[2] && r[2] > p[0] && r[1] < p[3] && r[3] > p[1]) return true; } return false; }
        function hitObs(r, own) { for (var i = 0; i < obst.length; i++) { if (i === own) continue; var p = obst[i]; if (r[0] < p[2] && r[2] > p[0] && r[1] < p[3] && r[3] > p[1]) return true; } return false; }
        order.forEach(function (id) {
          var n = D2.nodes[id], idx = D2.order.indexOf(id), isSel = id === M.sel, dimmed = (M.sel && !rel[id]) || (focusSet && !focusSet[id]);
          if (dimmed && !isSel) return;
          var rs = (radius(n) + (n.nk === 'principale' ? 9 : 2)) * g, X = n.x * s, Y = n.y * s, cands = [];
          var full = n.nome, sh2 = n.short;
          // etichetta abbreviata a vista d'insieme; il nome completo compare quando l'ingrandimento lo consente o per l'universo selezionato
          if (isSel || s / fit >= 1.9) cands.push(full); if (!isSel && (sh2 !== full || !cands.length)) cands.push(sh2);
          var done = false;
          cands.forEach(function (t) {
            if (done) return; var w = t.length * (isSel ? 7.5 : 7.1) + 8, h = 17;
            [['b', X - w / 2, Y + rs + 3], ['t', X - w / 2, Y - rs - 3 - h], ['r', X + rs + 4, Y - h / 2], ['l', X - rs - 4 - w, Y - h / 2]].forEach(function (c) {
              if (done) return; var r = [c[1], c[2], c[1] + w, c[2] + h];
              if (hit(r) || hitObs(r, idx)) return;
              if (X + tx > 0 && X + tx < vw && (r[0] + tx < 4 || r[2] + tx > vw - 4)) return; // a vista d'insieme nessuna etichetta esce dall'area
              done = true; placed.push(r); res += mpLab(n, t, c[0], X, Y, rs, w, h, isSel);
            });
          });
          if (!done && isSel) { // il nome completo dell'universo selezionato ha la precedenza: puo' sfiorare altri nodi, mai altre etichette
            var wf = full.length * 7.5 + 8, hf = 17;
            [['b', X - wf / 2, Y + rs + 3], ['t', X - wf / 2, Y - rs - 3 - hf], ['r', X + rs + 4, Y - hf / 2], ['l', X - rs - 4 - wf, Y - hf / 2]].forEach(function (c) { if (done) return; var r = [c[1], c[2], c[1] + wf, c[2] + hf]; if (hit(r) || r[0] + tx < 4 || r[2] + tx > vw - 4) return; done = true; placed.push(r); res += mpLab(n, full, c[0], X, Y, rs, wf, hf, true); });
          }
          if (!done && (isSel || id === MCU)) { var t2 = sh2, w2 = t2.length * 7.1 + 8; placed.push([X - w2 / 2, Y + rs + 3, X + w2 / 2, Y + rs + 20]); res += mpLab(n, t2, 'b', X, Y, rs, w2, 17, isSel); }
        });
        return res;
      }
      function mpLab(n, t, pos, X, Y, rs, w, h, isSel) {
        var x, y, anc = 'middle';
        if (pos === 'b') { x = X; y = Y + rs + 3 + 13; } else if (pos === 't') { x = X; y = Y - rs - 3 - 4; } else if (pos === 'r') { x = X + rs + 4 + 2; y = Y + 4.5; anc = 'start'; } else { x = X - rs - 4 - 2; y = Y + 4.5; anc = 'end'; }
        return '<text class="mp-lb' + (isSel ? ' sel' : '') + '" aria-hidden="true" x="' + (x / s).toFixed(2) + '" y="' + (y / s).toFixed(2) + '" text-anchor="' + anc + '" font-size="' + (12.5 / s).toFixed(3) + '" stroke-width="' + (3.6 / s).toFixed(3) + '">' + mpEsc(t) + '</text>';
      }
      function settle(soft) { if (cancelled) return; if (soft === true && Math.abs(s - paintedS) < 1e-6) { syncCtl(); return; } paint(); syncCtl(); } // le etichette non dipendono dalla traslazione: dopo un pan la scena non si ridisegna
      var cancelled = false;

      /* ---- selezione ---- */
      function say(t) { live.textContent = ''; setTimeout(function () { live.textContent = t; }, 30); }
      function select(id, o) {
        o = o || {}; M.sel = id; if (!id) M.focus = null; renderSheet(); sheetMetrics();
        if (id && o.center) {
          var n = D2.nodes[id], z = Math.max(s / fit, o.z || 2.2); goTo(fit * z, n.x, n.y, true, sheetH());
        } else if (id) { keepVisible(id); settle(); } else settle();
        if (id) say('Selezionato: ' + D2.nodes[id].nome);
      }
      function sheetH() { var sh1 = wrap.querySelector('.mp-sheet'); return sh1 && M.sel && !M.panel ? sh1.offsetHeight : 0; }
      function keepVisible(id) {
        var n = D2.nodes[id], sy = n.y * s + ty, sx = n.x * s + tx, h = sheetH(), lim = vh - h - 104, dyv = 0, dxv = 0;
        if (sy > lim) dyv = lim - sy; if (sy < 44) dyv = 44 - sy; if (sx < 30) dxv = 30 - sx; if (sx > vw - 30) dxv = vw - 30 - sx;
        if (dyv || dxv) goTo(s, (vw / 2 - (tx + dxv)) / s, ((vh - h) / 2 - (ty + dyv)) / s + 0, true, h);
      }
      function pickSearch(id) {
        var n = D2.nodes[id]; M.q = ''; inp.value = ''; sugg.hidden = true; inp.blur();
        if (M.fam !== 'tutte' || M.nat !== 'tutti' || M.onlyLinks) { /* il risultato e' gia' filtrato come visibile */ }
        if (M.mode !== 'map') setMode('map'); M.panel = null; renderPanel(); select(id, { center: true, z: 2.4 });
      }

      /* ---- anteprima dal basso (dati reali del modello) ---- */
      var sheetEl = null;
      function renderSheet() {
        if (sheetEl) { sheetEl.remove(); sheetEl = null; }
        if (!M.sel || M.panel || M.mode !== 'map') { wrap.style.setProperty('--mpsh', '0px'); return; }
        var n = D2.nodes[M.sel], m = UM.get(M.sel), acc = MP_ACC[n.fam], p = prog(M.sel);
        var sh1 = el('section', 'mp-sheet'); sh1.setAttribute('aria-label', 'Anteprima: ' + n.nome); sheetEl = sh1; sh1.style.setProperty('--acc', acc);
        var shb = el('div', 'mp-shb'); sh1.appendChild(shb);
        var head = el('div', 'mp-sh-h'); head.appendChild(mpIcon(n.nk, acc, 30));
        var tt = el('div', 'mp-sh-t'); tt.appendChild(el('span', 'mp-k', (n.natura + (n.fam !== 'mcu' ? ' · ' + n.famNome : '')).toUpperCase())); tt.appendChild(el('h3', '', n.nome)); head.appendChild(tt);
        var x = btn('mp-x', '✕', function () { select(null); }); x.setAttribute('aria-label', 'Chiudi anteprima'); head.appendChild(x); shb.appendChild(head);
        var st = el('p', 'mp-sh-s', mpCountsTxt(n) + (p.n ? ' · visti ' + p.v + ' su ' + p.n : '')); shb.appendChild(st);
        var lk = mpLinksOf(M.sel), all = m.conteggi.confermato + m.conteggi.legacy + m.conteggi.verificare;
        var lrow = el('div', 'mp-sh-l');
        if (lk.length) {
          var parts = []; [['confermato', 'documentat' + 'i nella guida'], ['legacy', 'legacy'], ['verificare', 'da verificare']].forEach(function (q) { var c = lk.filter(function (l) { return l.stato === q[0]; }).length; if (c) parts.push(MP_ST[q[0]].ic + ' ' + c + ' ' + q[1]); });
          lrow.appendChild(el('p', 'mp-sh-c', (lk.length === 1 ? '1 collegamento: ' : lk.length + ' collegamenti: ') + parts.join(' · ')));
          var chips = el('div', 'mp-chips mp-chips-s'); chips.setAttribute('aria-label', 'Universi collegati');
          lk.forEach(function (l) { var o = l.a === M.sel ? l.b : l.a, on = D2.nodes[o]; var c = btn('mp-chip mp-chip-' + MP_ST[l.stato].cls, MP_ST[l.stato].ic + ' ' + on.short, function () { select(o, { center: true, z: Math.max(1.6, s / fit) }); }); c.setAttribute('aria-label', on.nome + ' — ' + UM.stati[l.stato] + '. Seleziona'); chips.appendChild(c); });
          lrow.appendChild(chips);
        } else lrow.appendChild(el('span', 'mp-none', all ? 'Collegamenti nascosti dal filtro di affidabilità attivo.' : 'Nessun collegamento con altri universi nei dati della guida.'));
        shb.appendChild(lrow);
        var spn = []; n.spec.forEach(function (e) { var nm = e.entita && e.entita.nome; if (nm && spn.indexOf(nm) === -1) spn.push(nm); });
        if (spn.length) shb.appendChild(el('p', 'mp-sh-sp', 'Compare anche in: ' + spn.join(', ') + ' (fuori mappa).'));
        var acts = el('div', 'mp-acts');
        var op = btn('mp-go', 'Apri il dossier', function () { openUni(M.sel); }); op.id = 'mpOpenDossier'; acts.appendChild(op);
        var oc = btn('mp-sec', 'Cronologia', function () { crOpen('uni', { uid: M.sel }); }); oc.id = 'mpOpenCron'; oc.setAttribute('aria-label', 'Apri la cronologia di ' + n.nome); acts.appendChild(oc);
        if (lk.length) { var fo = btn('mp-sec', M.focus ? 'Mostra tutto' : 'Solo i suoi collegamenti', function () { M.focus = M.focus ? null : M.sel; if (M.focus) { var set = related(M.sel), xs = [], ys = []; Object.keys(set).forEach(function (i) { xs.push(D2.nodes[i].x); ys.push(D2.nodes[i].y); }); var x0 = Math.min.apply(0, xs), x1 = Math.max.apply(0, xs), y0 = Math.min.apply(0, ys), y1 = Math.max.apply(0, ys); var h = sheetH(), ns = Math.min((vw - 110) / Math.max(60, x1 - x0), (vh - h - 110) / Math.max(60, y1 - y0)); renderSheet(); goTo(Math.max(fit, Math.min(fit * 3.2, ns)), (x0 + x1) / 2, (y0 + y1) / 2, true, sheetH()); } else { renderSheet(); fitView(true); } }); fo.id = 'mpFocus'; fo.setAttribute('aria-pressed', M.focus ? 'true' : 'false'); acts.appendChild(fo); }
        sh1.appendChild(acts); wrap.appendChild(sh1);
      }
      function sheetMetrics() { wrap.style.setProperty('--mpsh', (M.sel && !M.panel && M.mode === 'map' && sheetEl ? sheetEl.offsetHeight : 0) + 'px'); }

      /* ---- comandi sulla mappa: zoom, adatta, legenda, fuori mappa ---- */
      var ctl = el('div', 'mp-ctl'), zin = btn('mp-rb', '＋', function () { zoomBtn(1.7); }), zout = btn('mp-rb', '−', function () { zoomBtn(1 / 1.7); }), zfit = btn('mp-rb mp-fit', null, function () { M.focus = null; fitView(true); if (M.focus === null) renderSheet(); });
      zin.setAttribute('aria-label', 'Ingrandisci'); zout.setAttribute('aria-label', 'Riduci'); zfit.setAttribute('aria-label', 'Adatta la mappa allo schermo'); zin.id = 'mpZin'; zout.id = 'mpZout'; zfit.id = 'mpFit';
      zfit.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg><small>Adatta</small>';
      ctl.appendChild(zin); ctl.appendChild(zout); ctl.appendChild(zfit); mapBox.appendChild(ctl);
      var pills = el('div', 'mp-pills'), pl = btn('mp-pill', null, function () { mpPanel(M.panel === 'legenda' ? null : 'legenda'); }), pf = btn('mp-pill', null, function () { mpPanel(M.panel === 'fuori' ? null : 'fuori'); });
      pl.id = 'mpLegenda'; pf.id = 'mpFuori'; pl.innerHTML = '<span aria-hidden="true">◧</span> Legenda'; pf.innerHTML = '<span aria-hidden="true">◌</span> Fuori mappa · ' + UM.special().length;
      pills.appendChild(pl); pills.appendChild(pf); wrap.appendChild(pills);
      var hlBar = el('div', 'mp-hlbar'); hlBar.hidden = true; wrap.appendChild(hlBar);
      function syncCtl() {
        zin.disabled = s >= fit * MP_ZMAX - 0.001; zout.disabled = s <= fit * 1.001;
        if (M.hl) { hlBar.hidden = false; hlBar.textContent = ''; var t = el('span', '', 'In evidenza: ' + M.hl.nome); var c = btn('mp-hlx', '✕ Rimuovi', function () { M.hl = null; hlBar.hidden = true; settle(); }); hlBar.appendChild(t); hlBar.appendChild(c); } else hlBar.hidden = true;
        var fc = mpFiltersOn(); fbDot.hidden = !fc; fb.setAttribute('aria-label', fc ? 'Filtri (' + fc + ' attivi)' : 'Filtri');
      }

      function zoomBtn(f) { // con un universo selezionato lo zoom resta centrato su di lui (nell'area libera sopra l'anteprima)
        var ns = Math.max(fit, Math.min(fit * MP_ZMAX, s * f)); if (ns === s) return;
        if (M.sel) goTo(ns, D2.nodes[M.sel].x, D2.nodes[M.sel].y, true, sheetH()); else zoomAt(vw / 2, vh / 2, f, true);
      }
      /* ---- pannelli: legenda · filtri · fuori mappa ---- */
      var panelEl = null, lastFocus = null;
      function mpPanel(name) {
        var prev = M.panel; M.panel = name;
        if (name) lastFocus = D.activeElement;
        renderPanel(); renderSheet(); sheetMetrics();
        if (!name && lastFocus && lastFocus.focus && prev) { try { lastFocus.focus(); } catch (e) {} }
      }
      function renderPanel() {
        panelHost.textContent = ''; panelEl = null; wrap.classList.toggle('mp-has-panel', !!M.panel);
        if (!M.panel) return;
        var foot, P = el('section', 'mp-panel'); P.setAttribute('role', 'dialog'); panelEl = P;
        var head = el('div', 'mp-ph'), ttl2 = el('h3', '', M.panel === 'legenda' ? 'Legenda' : (M.panel === 'filtri' ? 'Filtri' : 'Fuori mappa · ' + UM.special().length));
        var cx = btn('mp-x', '✕', function () { mpPanel(null); }); cx.setAttribute('aria-label', 'Chiudi'); cx.id = 'mpPanelX';
        head.appendChild(ttl2); head.appendChild(cx); P.appendChild(head); P.setAttribute('aria-label', ttl2.textContent);
        var bd = el('div', 'mp-pb'); P.appendChild(bd), foot = null;
        if (M.panel === 'filtri') { foot = el('div', 'mp-pf'); }
        if (M.panel === 'legenda') panelLegenda(bd); else if (M.panel === 'filtri') panelFiltri(bd, foot); else panelFuori(bd);
        if (foot) P.appendChild(foot);
        var back2 = el('div', 'mp-pback'); back2.addEventListener('click', function () { mpPanel(null); });
        panelHost.appendChild(back2); panelHost.appendChild(P); cx.focus({ preventScroll: true });
      }
      function sectionH(t) { return el('h4', 'mp-h4', t); }
      function panelLegenda(bd) {
        bd.appendChild(sectionH('COLLEGAMENTI'));
        [['confermato', 'Atlante e grafo storico concordano su almeno un titolo. Entrambi derivano dalla guida: non è una verifica canonica indipendente.'],
         ['legacy', 'Presente solo nel grafo storico; l’Atlante non lo riscontra né lo contraddice. Non verificato.'],
         ['verificare', 'Dati ambigui, contraddittori o presenti solo nell’Atlante.']].forEach(function (p) {
          var r = el('div', 'mp-lg'); r.appendChild(mpLineSample(p[0])); var t = el('div', ''); t.appendChild(el('b', '', UM.stati[p[0]])); t.appendChild(el('span', '', p[1])); r.appendChild(t); bd.appendChild(r);
        });
        bd.appendChild(sectionH('NODI · LA FORMA È LA TIPOLOGIA'));
        var cnt = {}; D2.order.forEach(function (i) { cnt[D2.nodes[i].nk] = (cnt[D2.nodes[i].nk] || 0) + 1; });
        MP_NATORD.forEach(function (k) { if (!cnt[k]) return; var r = el('div', 'mp-lg'); r.appendChild(mpIcon(k, '#D2B184', 30)); var t = el('div', ''); t.appendChild(el('b', '', MP_NATLBL[k] + ' · ' + cnt[k])); r.appendChild(t); bd.appendChild(r); });
        bd.appendChild(el('p', 'mp-note', 'La dimensione del nodo dipende dal numero di titoli associati dalla guida.'));
        bd.appendChild(sectionH('COLORE DELL’ANELLO · FAMIGLIA EDITORIALE'));
        var sw = el('div', 'mp-sw'); MP_FAMORD.forEach(function (f) { if (!D2.order.some(function (i) { return D2.nodes[i].fam === f; })) return; var c = el('span', 'mp-swi'); var d = el('i', ''); d.style.background = MP_ACC[f]; d.setAttribute('aria-hidden', 'true'); c.appendChild(d); c.appendChild(D.createTextNode(f === 'mcu' ? 'MCU' : (FAM[f] ? FAM[f].nome : f))); sw.appendChild(c); }); bd.appendChild(sw);
        bd.appendChild(el('p', 'mp-note', 'Le nebulose sullo sfondo raggruppano gli universi per famiglia editoriale: sono un aiuto visivo, non relazioni canoniche. La mappa non aggiunge collegamenti: mostra solo quelli presenti nei dati della guida.'));
        bd.appendChild(sectionH('GESTI'));
        bd.appendChild(el('p', 'mp-note', 'Trascina per spostare · pizzica o tocca due volte per ingrandire · tocca un universo per l’anteprima · tocca lo sfondo per deselezionare. Con la tastiera: frecce, + / − e 0 per adattare.'));
        var c2 = btn('mp-sec mp-wide', 'Apri il grafo classico', function () { run(['tog', 'multiverseGraphToggle']); }); c2.id = 'mpClassic1'; bd.appendChild(c2);
      }
      function panelFiltri(bd, foot) {
        bd.appendChild(sectionH('AFFIDABILITÀ DEI COLLEGAMENTI'));
        ['confermato', 'legacy', 'verificare'].forEach(function (k) {
          var b = btn('mp-tg' + (M.rel[k] ? ' on' : ''), null, function () { M.rel[k] = M.rel[k] ? 0 : 1; renderPanel(); settle(); renderSheet(); sheetMetrics(); }); b.setAttribute('aria-pressed', M.rel[k] ? 'true' : 'false'); b.setAttribute('data-rel', k);
          b.appendChild(mpLineSample(k)); b.appendChild(el('span', 'mp-tg-t', UM.stati[k])); b.appendChild(el('span', 'mp-tg-s', M.rel[k] ? 'Visibili' : 'Nascosti')); bd.appendChild(b);
        });
        bd.appendChild(sectionH('FAMIGLIA'));
        var fr = el('div', 'mp-fr'); function chip(lbl, on, fn, val) { var b = btn('mp-fc' + (on ? ' on' : ''), lbl, fn); b.setAttribute('aria-pressed', on ? 'true' : 'false'); if (val) b.setAttribute('data-v', val); return b; }
        var fc = { tutte: D2.order.length }; D2.order.forEach(function (i) { fc[D2.nodes[i].fam] = (fc[D2.nodes[i].fam] || 0) + 1; });
        fr.appendChild(chip('Tutte ' + fc.tutte, M.fam === 'tutte', function () { M.fam = 'tutte'; applyFilters(); }, 'tutte'));
        MP_FAMORD.forEach(function (f) { if (!fc[f]) return; fr.appendChild(chip((f === 'mcu' ? 'MCU' : (FAM[f] ? FAM[f].nome : f)) + ' ' + fc[f], M.fam === f, function () { M.fam = f; applyFilters(); }, f)); }); bd.appendChild(fr);
        bd.appendChild(sectionH('TIPOLOGIA'));
        var tr = el('div', 'mp-fr'), nc = { tutti: D2.order.length }; D2.order.forEach(function (i) { nc[D2.nodes[i].nk] = (nc[D2.nodes[i].nk] || 0) + 1; });
        tr.appendChild(chip('Tutte ' + nc.tutti, M.nat === 'tutti', function () { M.nat = 'tutti'; applyFilters(); }, 'tutti'));
        MP_NATORD.forEach(function (k) { if (!nc[k]) return; tr.appendChild(chip(MP_NATLBL[k] + ' ' + nc[k], M.nat === k, function () { M.nat = k; applyFilters(); }, k)); }); bd.appendChild(tr);
        var ol = btn('mp-tg' + (M.onlyLinks ? ' on' : ''), null, function () { M.onlyLinks = !M.onlyLinks; applyFilters(); }); ol.id = 'mpOnlyLinks'; ol.setAttribute('aria-pressed', M.onlyLinks ? 'true' : 'false');
        ol.appendChild(el('span', 'mp-tg-t', 'Solo universi con collegamenti')); ol.appendChild(el('span', 'mp-tg-s', M.onlyLinks ? 'Attivo' : 'Disattivo')); bd.appendChild(ol);
        var shown = D2.order.filter(function (i) { return mpVis(D2.nodes[i]); }).length;
        bd.appendChild(el('p', 'mp-note', shown + ' di ' + D2.order.length + ' universi visibili con i filtri attuali.'));
        var row2 = foot, rs2 = btn('mp-sec', 'Azzera i filtri', function () { M.rel = { confermato: 1, legacy: 1, verificare: 1 }; M.fam = 'tutte'; M.nat = 'tutti'; M.onlyLinks = false; applyFilters(); }); rs2.id = 'mpReset';
        var ok = btn('mp-go', 'Mostra ' + shown + ' universi', function () { mpPanel(null); }); row2.appendChild(rs2); row2.appendChild(ok);
        var c3 = btn('mp-link', 'Apri il grafo classico', function () { run(['tog', 'multiverseGraphToggle']); }); c3.id = 'mpClassic2'; bd.appendChild(c3);
      }
      function applyFilters() {
        if (M.sel && !mpVis(D2.nodes[M.sel])) { M.sel = null; M.focus = null; }
        renderPanel(); settle(); drawList(); renderSheet(); sheetMetrics();
      }
      function panelFuori(bd) {
        bd.appendChild(el('p', 'mp-note', 'Non sono universi e non rientrano nei 27: luoghi, realtà speciali e raggruppamenti editoriali. Sono tenuti separati per non confonderli con continuità canoniche.'));
        UM.special().forEach(function (e) {
          var card = el('article', 'mp-sp'), h = el('div', 'mp-sp-h'); h.appendChild(el('span', 'mp-tag', e.classeLbl.toUpperCase())); card.appendChild(h);
          card.appendChild(el('h4', 'mp-sp-n', e.nome));
          var tx2 = String(e.testo || ''); if (tx2.indexOf(e.nome) === 0) tx2 = tx2.slice(e.nome.length); var ci = tx2.indexOf('Collegamenti:'); if (ci !== -1) tx2 = tx2.slice(0, ci);
          if (tx2.trim()) card.appendChild(el('p', 'mp-sp-t', tx2.trim()));
          var halo = [], haloQ = [];
          if (e.membri && e.membri.length) {
            card.appendChild(el('p', 'mp-sp-s', 'Membri elencati dalla guida (' + e.membri.length + '):')); var mr = el('div', 'mp-chips mp-chips-w');
            e.membri.forEach(function (u) { if (!D2.nodes[u]) return; halo.push(u); var c = btn('mp-chip', D2.nodes[u].short, function () { M.panel = null; M.hl = null; renderPanel(); if (M.mode !== 'map') setMode('map'); select(u, { center: true, z: 2 }); }); c.setAttribute('aria-label', D2.nodes[u].nome + '. Mostra sulla mappa'); mr.appendChild(c); });
            (e.membriIncerti || []).forEach(function (u) { if (!D2.nodes[u]) return; haloQ.push(u); var c = btn('mp-chip mp-chip-q', '? ' + D2.nodes[u].short, function () { M.panel = null; M.hl = null; renderPanel(); if (M.mode !== 'map') setMode('map'); select(u, { center: true, z: 2 }); }); c.setAttribute('aria-label', D2.nodes[u].nome + ': appartenenza ambigua. Mostra sulla mappa'); mr.appendChild(c); });
            card.appendChild(mr);
            if (e.base) card.appendChild(el('p', 'mp-sp-b', 'Base: ' + e.base + '.'));
            if (e.baseIncerta) card.appendChild(el('p', 'mp-sp-b mp-sp-q', '? ' + e.baseIncerta.charAt(0).toUpperCase() + e.baseIncerta.slice(1) + '.'));
          }
          if (e.relazioni && e.relazioni.length) {
            card.appendChild(el('p', 'mp-sp-s', 'Collegamenti nei dati:'));
            e.relazioni.forEach(function (r) {
              var rw = el('div', 'mp-rl'); var spN = null; UM.special().forEach(function (z) { if (z.id === r.conSpecial) spN = z.nome; }); var who = r.con && D2.nodes[r.con] ? D2.nodes[r.con].nome : (spN || '—'); if (r.con && D2.nodes[r.con] && halo.indexOf(r.con) === -1) halo.push(r.con);
              rw.appendChild(el('span', 'mp-rl-w', who)); rw.appendChild(mpStBadge(r.stato)); var tt2 = (UM.tipi[r.tipo] || r.tipo) + (r.titoli && r.titoli.length ? ' · ' + r.titoli.slice().sort(byGuide).map(function (n) { return 'N°' + VN(n); }).join(', ') : ''); rw.appendChild(el('span', 'mp-rl-t', tt2)); card.appendChild(rw);
            });
          } else card.appendChild(el('p', 'mp-sp-s', 'Nessun incrocio diretto mostrato nei dati.'));
          if (halo.length || haloQ.length) { var hb = btn('mp-sec mp-wide', 'Evidenzia sulla mappa', function () { M.hl = { nome: e.nome, ids: halo, incerti: haloQ }; M.panel = null; renderPanel(); if (M.mode !== 'map') setMode('map'); select(null); fitView(true); }); hb.setAttribute('data-sp', e.id); card.appendChild(hb); }
          bd.appendChild(card);
        });
      }

      /* ---- elenco: stessa ricerca, stessi filtri, stessi dati ---- */
      function drawList() {
        listBox.textContent = ''; var q = M.q, byFam = {}, shown = 0, rows = D2.order.filter(function (i) { return mpVis(D2.nodes[i]); });
        if (q.trim()) { var ms = {}; mpMatch(q).forEach(function (r) { ms[r.id] = r; }); rows = rows.filter(function (i) { return ms[i]; }); }
        rows.forEach(function (i) { (byFam[D2.nodes[i].fam] = byFam[D2.nodes[i].fam] || []).push(i); });
        listBox.appendChild(el('p', 'mp-lc', rows.length === D2.order.length ? D2.order.length + ' universi' : rows.length + ' di ' + D2.order.length + ' universi'));
        MP_FAMORD.forEach(function (f) {
          var arr = byFam[f]; if (!arr) return; var sec2 = el('section', 'mp-lsec'), h = el('h3', 'mp-lh'); var dot = el('i', ''); dot.style.background = MP_ACC[f]; dot.setAttribute('aria-hidden', 'true'); h.appendChild(dot);
          h.appendChild(D.createTextNode((f === 'mcu' ? 'MCU · continuità principale' : (FAM[f] ? FAM[f].nome : f)) + ' · ' + arr.length)); sec2.appendChild(h);
          arr.sort(function (a, b) { return (b === MCU) - (a === MCU) || D2.nodes[b].nt - D2.nodes[a].nt; }).forEach(function (id) {
            var n = D2.nodes[id], r = el('div', 'mp-row'), b = btn('mp-rmain', null, function () { openUni(id); }); b.setAttribute('data-u', id); b.setAttribute('aria-label', n.nome + '. Apri il dossier');
            b.appendChild(mpIcon(n.nk, MP_ACC[n.fam], 30)); var t = el('span', 'mp-rt'); t.appendChild(el('b', '', n.nome)); t.appendChild(el('small', '', n.natura + ' · ' + mpCountsTxt(n)));
            var lk = mpLinksOf(id); var br = el('span', 'mp-rbs');
            if (lk.length) ['confermato', 'legacy', 'verificare'].forEach(function (k) { var c = lk.filter(function (l) { return l.stato === k; }).length; if (c) { var bb = mpStBadge(k, c); bb.setAttribute('title', c + ' · ' + UM.stati[k]); br.appendChild(bb); } });
            else br.appendChild(el('span', 'mp-none', 'Nessun collegamento nei dati'));
            t.appendChild(br); b.appendChild(t); r.appendChild(b);
            var mb = btn('mp-rmap', null, function () { setMode('map'); select(id, { center: true, z: 2.2 }); }); mb.setAttribute('aria-label', 'Mostra ' + n.nome + ' sulla mappa'); mb.setAttribute('data-map', id);
            mb.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>'; r.appendChild(mb);
            sec2.appendChild(r); shown++;
          });
          listBox.appendChild(sec2);
        });
        if (!shown) { var em = el('div', 'a2-empty'); em.appendChild(el('p', '', 'Nessun universo corrisponde a ricerca e filtri attuali.')); var rz = btn('mp-sec', 'Azzera ricerca e filtri', function () { M.q = ''; inp.value = ''; M.rel = { confermato: 1, legacy: 1, verificare: 1 }; M.fam = 'tutte'; M.nat = 'tutti'; M.onlyLinks = false; drawList(); syncCtl(); }); em.appendChild(rz); listBox.appendChild(em); }
        var ft = el('div', 'mp-lf'), a = btn('mp-pill', null, function () { mpPanel('legenda'); }), b2 = btn('mp-pill', null, function () { mpPanel('fuori'); }), c = btn('mp-pill', 'Grafo classico', function () { run(['tog', 'multiverseGraphToggle']); });
        a.innerHTML = '<span aria-hidden="true">◧</span> Legenda'; b2.innerHTML = '<span aria-hidden="true">◌</span> Fuori mappa · ' + UM.special().length; c.id = 'mpClassic3';
        ft.appendChild(a); ft.appendChild(b2); ft.appendChild(c); listBox.appendChild(ft);
      }
      function setMode(md) {
        M.mode = md; wrap.classList.toggle('mp-listmode', md === 'list'); sbM.classList.toggle('on', md === 'map'); sbL.classList.toggle('on', md === 'list');
        sbM.setAttribute('aria-pressed', md === 'map' ? 'true' : 'false'); sbL.setAttribute('aria-pressed', md === 'list' ? 'true' : 'false');
        pills.hidden = md === 'list'; sugg.hidden = true;
        if (md === 'list') { drawList(); renderSheet(); } else { measure(); viewFromState(); settle(); renderSheet(); sheetMetrics(); }
        sheetMetrics(); syncCtl();
      }

      /* ---- ricerca ---- */
      function drawSugg() {
        var q = inp.value; M.q = q;
        if (M.mode === 'list') { drawList(); return; }
        sugg.textContent = ''; if (!q.trim()) { sugg.hidden = true; return; }
        var r = mpMatch(q).slice(0, 6); sugg.hidden = false;
        if (!r.length) { sugg.appendChild(el('p', 'mp-none mp-sg-none', 'Nessun universo trovato' + (mpFiltersOn() ? ' (filtri attivi)' : '') + '.')); return; }
        r.forEach(function (x) {
          var n = D2.nodes[x.id], b = btn('mp-sg-i', null, function () { pickSearch(x.id); }); b.setAttribute('role', 'option'); b.setAttribute('data-u', x.id);
          b.appendChild(mpIcon(n.nk, MP_ACC[n.fam], 26)); var t = el('span', 'mp-rt'); t.appendChild(el('b', '', n.nome)); t.appendChild(el('small', '', x.via ? 'tramite il titolo «' + x.via + '»' : n.natura + (n.fam !== 'mcu' ? ' · ' + n.famNome : ''))); b.appendChild(t); sugg.appendChild(b);
        });
      }
      var stm = null; inp.addEventListener('input', function () { clearTimeout(stm); stm = setTimeout(drawSugg, 90); });
      inp.addEventListener('focus', function () { if (M.mode === 'map' && inp.value.trim()) drawSugg(); });
      inp.addEventListener('keydown', function (e) { if (e.key === 'Escape') { sugg.hidden = true; inp.blur(); } });

      /* ---- gesti: un dito = pan, due dita = pinch, doppio tocco = zoom; touch-action:none solo sull'area della mappa ---- */
      var ptrs = {}, G = null, lastTap = null;
      function cnt() { return Object.keys(ptrs).length; }
      function pts() { return Object.keys(ptrs).map(function (k) { return ptrs[k]; }); }
      function local(e) { var r = svg.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
      svg.addEventListener('pointerdown', function (e) {
        if (e.pointerType === 'mouse' && e.button !== 0) return;
        cancelTween(); var p = local(e); ptrs[e.pointerId] = { x: p.x, y: p.y };
        try { svg.setPointerCapture(e.pointerId); } catch (eC) {}
        if (cnt() === 1) G = { type: 'pan', sx: p.x, sy: p.y, tx0: tx, ty0: ty, moved: false, tgt: e.target.closest ? e.target.closest('[data-u]') : null, t0: performance.now() };
        else if (cnt() === 2) { var a = pts(), d = Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) || 1; G = { type: 'pinch', d0: d, mx0: (a[0].x + a[1].x) / 2, my0: (a[0].y + a[1].y) / 2, s0: s, tx0: tx, ty0: ty, moved: true }; }
      });
      svg.addEventListener('pointermove', function (e) {
        if (!ptrs[e.pointerId] || !G) return; var p = local(e); ptrs[e.pointerId] = { x: p.x, y: p.y };
        if (G.type === 'pan' && cnt() === 1) {
          var dx = p.x - G.sx, dy = p.y - G.sy; if (!G.moved && Math.hypot(dx, dy) < 7) return; G.moved = true;
          setViewLive(s, G.tx0 + dx, G.ty0 + dy);
        } else if (G.type === 'pinch' && cnt() >= 2) {
          var a = pts(), d = Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) || 1, mx = (a[0].x + a[1].x) / 2, my = (a[0].y + a[1].y) / 2;
          var ns = Math.max(fit * 0.98, Math.min(fit * MP_ZMAX, G.s0 * d / G.d0)), wx = (G.mx0 - G.tx0) / G.s0, wy = (G.my0 - G.ty0) / G.s0;
          setViewLive(ns, mx - wx * ns, my - wy * ns);
        }
      });
      function setViewLive(ns, ntx, nty) { var c = clampView(ns, ntx, nty); s = c.s; tx = c.x; ty = c.y; if (!raf2) raf2 = requestAnimationFrame(function () { raf2 = 0; applyView(); }); }
      var raf2 = 0;
      function endPtr(e, cancel) {
        if (!ptrs[e.pointerId]) return; var wasTwo = G && G.type === 'pinch', g0 = G; delete ptrs[e.pointerId];
        try { svg.releasePointerCapture(e.pointerId); } catch (eR) {}
        if (cnt() === 0) {
          G = null; if (raf2) { cancelAnimationFrame(raf2); raf2 = 0; } applyView();
          if (g0 && g0.type === 'pan' && !g0.moved && !cancel) onTap(local(e), g0.tgt); else settle(true);
        } else if (wasTwo && cnt() === 1) { var q = pts()[0]; G = { type: 'pan', sx: q.x, sy: q.y, tx0: tx, ty0: ty, moved: true, tgt: null }; }
      }
      svg.addEventListener('pointerup', function (e) { endPtr(e, false); });
      svg.addEventListener('pointercancel', function (e) { endPtr(e, true); });
      // dopo un tocco sulla mappa il click sintetico del browser non deve attivare un comando che nel frattempo si e' spostato sotto il dito (pillole e anteprima)
      var tapGuard = 0;
      wrap.addEventListener('click', function (e) { if (performance.now() - tapGuard < 500 && !(e.target.closest && e.target.closest('.mp-stage'))) { e.stopPropagation(); e.preventDefault(); } }, true);
      function onTap(p, tgt) {
        var now = performance.now(); tapGuard = now;
        if (lastTap && now - lastTap.t < 330 && Math.hypot(p.x - lastTap.x, p.y - lastTap.y) < 30) { lastTap = null; zoomAt(p.x, p.y, 2, true); return; }
        lastTap = { t: now, x: p.x, y: p.y };
        if (tgt) { var id = tgt.getAttribute('data-u'); if (id && mpVis(D2.nodes[id])) { select(id === M.sel ? id : id); } } else if (M.sel) select(null); else settle();
      }
      svg.addEventListener('wheel', function (e) { e.preventDefault(); var p = local(e); zoomAt(p.x, p.y, Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)), false); }, { passive: false });
      ['gesturestart', 'gesturechange', 'gestureend'].forEach(function (n) { svg.addEventListener(n, function (e) { e.preventDefault(); }); });
      svg.addEventListener('contextmenu', function (e) { e.preventDefault(); });
      svg.addEventListener('keydown', function (e) {
        var u = e.target.closest && e.target.closest('[data-u]');
        if (u && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); var id = u.getAttribute('data-u'); select(id, { center: false }); var again = svg.querySelector('[data-u="' + id + '"]'); if (again) again.focus({ preventScroll: true }); return; }
        var st2 = 56, mv = { ArrowLeft: [st2, 0], ArrowRight: [-st2, 0], ArrowUp: [0, st2], ArrowDown: [0, -st2] }[e.key];
        if (mv && !u) { e.preventDefault(); setView(s, tx + mv[0], ty + mv[1]); settle(); }
        else if (e.key === '+' || e.key === '=') { zoomAt(vw / 2, vh / 2, 1.5, false); } else if (e.key === '-') { zoomAt(vw / 2, vh / 2, 1 / 1.5, false); } else if (e.key === '0') { fitView(false); }
        else if (e.key === 'Escape') { if (M.panel) mpPanel(null); else if (M.sel) { var was = M.sel; select(null); var nd = svg.querySelector('[data-u="' + was + '"]'); if (nd) nd.focus({ preventScroll: true }); } }
      });
      // dopo un ridisegno il focus resta sul nodo selezionato (navigazione da tastiera)
      var oldPaint = paint; paint = function () { var ae = D.activeElement, keep = ae && ae.getAttribute && svg.contains(ae) ? ae.getAttribute('data-u') : null; oldPaint(); if (keep) { var nd = svg.querySelector('[data-u="' + keep + '"]'); if (nd) try { nd.focus({ preventScroll: true }); } catch (eF) {} } };

      /* ---- ciclo di vita ---- */
      var onKey = function (e) { if (ST.screen !== 'mappa') return; if (e.key === 'Escape' && M.panel) { mpPanel(null); } };
      D.addEventListener('keydown', onKey);
      var onRz = function () { measure(); viewFromState(); settle(); sheetMetrics(); };
      var ro = null; try { ro = new ResizeObserver(function () { if (mapBox.offsetWidth) onRz(); }); ro.observe(mapBox); } catch (eRo) { W.addEventListener('resize', onRz); }
      MPR.cleanup = function () { cancelled = true; cancelTween(); D.removeEventListener('keydown', onKey); if (ro) ro.disconnect(); else W.removeEventListener('resize', onRz); };

      // primo disegno
      setMode(M.mode === 'list' ? 'list' : 'map');
      if (M.mode === 'map') {
        measure(); viewFromState(); settle();
        if (M.sel && !M.v) { goTo(Math.max(s, fit * 2.2), D2.nodes[M.sel].x, D2.nodes[M.sel].y, false, sheetH()); }
        else if (M.sel) keepVisible(M.sel);
        renderSheet(); sheetMetrics(); renderPanel();
      } else renderPanel();
      if (M.panel && M.mode === 'map') renderPanel();
      // dopo il layout (font, safe area) la misura viene riallineata una volta
      requestAnimationFrame(function () { if (cancelled || M.mode !== 'map') return; if (Math.abs(mapBox.getBoundingClientRect().height - vh) > 1) onRz(); });
    }
    /* ==== MAP3B:END ==== */
