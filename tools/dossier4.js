/* ===== TVA DOSSIER 4 — Dossier Kit, Ricerca tollerante, Dossier Opera, Personaggio 2, identita' degli archivi (FASE 4) =====
   Solo lettura: nessun dato nuovo, nessun ID cambiato, nessuna scrittura su progressi/XP/badge/missioni. L'unica azione che modifica lo stato e' il
   pulsante «Visto» del Dossier Opera, che aziona la STESSA casella della scheda in guida (stessa persistenza, stessi progressi e ricompense). */
(function () {
  'use strict';
  try {
    var W = window, D = document, A = W.tvaAtlas2, X = A && A.ext, a = X && X.api, XR = W.tvaXref;
    if (!a || !XR || W.__tvaD4) return; W.__tvaD4 = true;
    var $ = a.$, el = a.el, btn = a.btn, ST = a.ST, UNI = a.UNI, IDX = a.IDX, body = a.body, tog = a.tog;
    function VN(n) { return XR.VN(n); }
    function short(s, n) { s = String(s || ''); return s.length > (n || 22) ? s.slice(0, (n || 22) - 1) + '…' : s; }
    function goBtn(kind, id, label, sub, cls) { var b = btn(cls || 'a2-chip', null); b.setAttribute('data-go', kind + ':' + id); b.appendChild(D.createTextNode(label)); if (sub) b.appendChild(el('small', '', sub)); return b; }

    /* ================= DOSSIER KIT ================= */
    var SRC = { G: ['G', 'Scritto nella guida'], D: ['D', 'Derivato (nome esatto nel testo o corrispondenza del titolo)'], N: ['N', 'Non documentato nella guida'] };
    function src(code) { var s = SRC[code] || SRC.N, i = el('i', 'd4-src d4-src-' + s[0], s[0]); i.title = s[1]; i.setAttribute('role', 'img'); i.setAttribute('aria-label', 'Fonte: ' + s[1]); return i; }
    function sect(title, code, id, n) {
      var s = a.sec(title + (n != null ? ' (' + n + ')' : '')); s.classList.add('d4-sec'); if (id) s.setAttribute('data-d4sec', id);
      if (code) s.firstChild.appendChild(src(code)); return s;
    }
    function chipsBox(list, max, mk) {
      var box = el('div', 'a2-chips'), rest = list.slice(max || list.length);
      list.slice(0, max || list.length).forEach(function (x) { box.appendChild(mk(x)); });
      if (rest.length) {
        var more = btn('a2-chip d4-more', '+' + rest.length + ' altri', function () { rest.forEach(function (x) { box.insertBefore(mk(x), more); }); more.remove(); });
        more.setAttribute('aria-label', 'Mostra altri ' + rest.length); box.appendChild(more);
      }
      return box;
    }
    function empty(msg) { return el('p', 'a2-empty d4-empty', msg); }
    // Percorso di sessione: letto dallo stack «Indietro» esistente (nessuno stato nuovo)
    function crumb() {
      var s = W.tvaNavStato ? W.tvaNavStato() : { depth: 0, labels: [] }, l = (s.labels || []).filter(Boolean); if (!l.length) return null;
      var n = el('nav', 'd4-crumb'); n.setAttribute('aria-label', 'Percorso di navigazione');
      n.appendChild(el('span', 'd4-crumb-k', 'Da'));
      l.slice(-3).forEach(function (t, i, arr) { n.appendChild(el('span', 'd4-crumb-i', t)); if (i < arr.length - 1) n.appendChild(el('span', 'd4-crumb-s', '›')); });
      return n;
    }
    function jumpBar(list) {
      if (list.length < 3) return null;
      var n = el('div', 'd4-jump'); n.setAttribute('role', 'navigation'); n.setAttribute('aria-label', 'Sezioni della scheda');
      list.forEach(function (x) { var b = btn('d4-jump-b', x[1]); b.setAttribute('data-d4j', x[0]); n.appendChild(b); });
      return n;
    }
    D.addEventListener('click', function (ev) {
      var b = ev.target.closest ? ev.target.closest('[data-d4j]') : null; if (!b) return;
      var t = body.querySelector('[data-d4sec="' + b.getAttribute('data-d4j') + '"]'); if (t) { var y = t.getBoundingClientRect().top - body.getBoundingClientRect().top + body.scrollTop - 8; body.scrollTop = y; }
    });
    var MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
    function dataIt(iso) {
      var p = String(iso || '').split('-'); if (!/^\d{4}$/.test(p[0])) return String(iso || '');
      if (p.length >= 3 && +p[2]) return (+p[2]) + ' ' + MESI[+p[1] - 1] + ' ' + p[0];
      if (p.length >= 2 && +p[1]) return MESI[+p[1] - 1] + ' ' + p[0];
      return p[0];
    }
    function opArt(kind) {   // copertina originale (SVG) per le opere: nessun asset esterno
      var s = el('span', 'a2-cov a2-cov-hero d4-cov'); s.setAttribute('aria-hidden', 'true'); s.setAttribute('data-kind', 'opr');
      var film = '<rect x="10" y="8" width="44" height="42" rx="3" fill="none" stroke="#D2B184" stroke-width="1.6"/><path d="M10 20H54M10 38H54M20 8V50M44 8V50" stroke="#D2B184" stroke-opacity=".55"/><circle cx="32" cy="29" r="5" fill="#DB777C" fill-opacity=".9"/>';
      var tv = '<rect x="9" y="12" width="46" height="30" rx="4" fill="none" stroke="#D2B184" stroke-width="1.6"/><path d="M24 50H40M32 42V50" stroke="#D2B184" stroke-opacity=".7"/><path d="M28 21L40 27 28 33Z" fill="#DB777C" fill-opacity=".9"/>';
      s.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><defs><linearGradient id="d4og" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a2328"/><stop offset="1" stop-color="#101014"/></linearGradient></defs><rect width="64" height="64" fill="url(#d4og)"/>' + (kind === 'serie' ? tv : film) + '</svg>';
      return s;
    }

    /* ================= RICERCA TOLLERANTE, RISULTATI PER TIPOLOGIA ================= */
    var TF = 'tutti';
    function openSezione(k) {
      var s = a.SEZ[k]; if (!s) return;
      if (s.st === 'prep') return a.nav('soon', { sez: k });
      if (s.act[0] === 'sub') return a.nav('sezione', { sez: k });
      a.run(s.act);
    }
    function chipFor(it) {
      var t = it.t;
      if (t === 'sez') { var b = btn('a2-chip', null, function () { openSezione(it.id); }); b.appendChild(D.createTextNode(it.name)); if (it.sub) b.appendChild(el('small', '', it.sub)); return b; }
      if (t === 'uni') return goBtn('uni', it.id, it.name);
      if (t === 'tit') return goBtn('item', it.id, it.name, it.sub);
      if (t === 'chr') return goBtn('char', it.id, it.name);
      if (t === 'att') return goBtn('att', it.id, it.name, it.sub);
      return goBtn('arc', t + ':' + it.id, it.name, it.sub);
    }
    function drawResults(box, raw) {
      box.textContent = '';
      var q = (raw || '').trim(); if (q.length < 2) return true;
      var R = XR.cerca(q), any = R.n > 0;
      if (/616/.test(q) && a.NOTA_NUM) box.appendChild(a.info(a.NOTA_NUM));
      if (any) {
        var fl = el('div', 'd4-tf'); fl.setAttribute('role', 'group'); fl.setAttribute('aria-label', 'Filtra i risultati per tipologia');
        function tfb(k, lbl, n) { var b = btn('d4-tf-b' + (TF === k ? ' on' : ''), lbl + ' ' + n); b.setAttribute('aria-pressed', TF === k ? 'true' : 'false'); b.addEventListener('click', function () { TF = k; drawResults(box, raw); }); fl.appendChild(b); }
        if (!R.gruppi.some(function (g) { return g.tipo === TF; })) TF = 'tutti';
        if (R.gruppi.length > 1) { tfb('tutti', 'Tutti', R.n); R.gruppi.forEach(function (g) { tfb(g.tipo, g.lbl, g.voci.length); }); box.appendChild(fl); }
        R.gruppi.forEach(function (g) {
          if (TF !== 'tutti' && g.tipo !== TF) return;
          var gb = el('div', 'a2-resbox d4-res d4-res-' + g.tipo); gb.appendChild(el('h3', '', g.lbl + ' (' + g.voci.length + ')'));
          gb.appendChild(chipsBox(g.voci, TF === 'tutti' ? 12 : 60, chipFor)); box.appendChild(gb);
        });
      }
      if (!any && !/616/.test(q)) box.appendChild(el('p', 'a2-empty', 'Nessun risultato per «' + q + '». Prova con il nome di un personaggio, di un attore, di un universo o di un titolo: la ricerca ignora maiuscole, accenti e punteggiatura.'));
      return true;
    }
    X.drawResults = drawResults;

    /* ================= DOSSIER OPERA ================= */
    function typeKick(op) {
      var k = op.kind === 'anim' ? 'SERIE ANIMATA' : (op.variante ? 'VARIANTE' : (op.tipo || 'TITOLO').toUpperCase());
      return k + (op.vis ? ' · N°' + op.vis : '');
    }
    function axisTile(lbl, val, sub, code, id) {
      var t = el('div', 'd4-ax' + (val ? '' : ' d4-ax-n')); if (id) t.id = id;
      var h = el('span', 'd4-ax-k', lbl); h.appendChild(src(val ? code : 'N')); t.appendChild(h);
      t.appendChild(el('b', 'd4-ax-v', val || 'non indicata nella guida')); if (sub) t.appendChild(el('small', 'd4-ax-s', sub)); return t;
    }
    function seenButton(id) {
      var c = XR.chk(id); if (!c) return null;
      var b = btn('d4-seen', null); b.id = 'd4Seen';
      function paint() { var on = !!c.checked; b.className = 'd4-seen' + (on ? ' on' : ''); b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.textContent = on ? '✓ Visto' : '○ Segna come visto'; b.setAttribute('aria-label', on ? 'Visto. Tocca per segnare come non visto' : 'Non ancora visto. Tocca per segnare come visto'); }
      b.addEventListener('click', function () { c.click(); paint(); });   // stessa casella della Timeline: persistenza, progressi e ricompense invariati
      paint(); return b;
    }
    function renderOpera() {
      var id = ST.eid, op = XR.opera(id);
      if (!op) { ST.screen = 'search'; return a.draw(); }
      body.className = 'a2-scroll a2-dossier a2-opera'; body.textContent = ''; a.setTitle(op.titolo, 'Titoli');
      var cr = crumb(); if (cr) body.appendChild(cr);
      var hero = el('section', 'a2-hero a2-arc-hero d4-hero d4-hero-opr'); a.heroImg(hero, 'cronologie');
      hero.appendChild(opArt(op.tipo === 'Serie' || op.kind === 'anim' ? 'serie' : 'film'));
      hero.appendChild(el('span', 'a2-kick', typeKick(op))); hero.appendChild(el('h2', '', op.titolo));
      var meta = [op.uscita ? '' : op.anno, op.durata].filter(Boolean).join(' · '); if (meta) hero.appendChild(el('p', 'a2-descr d4-meta', meta));
      var acts = el('div', 'd4-acts'); var sb = seenButton(id); if (sb) acts.appendChild(sb);
      var g = btn('a2-primary d4-scheda', 'Scheda in guida ›', function () { W.tvaGo('item', id, { scheda: true }); }); g.id = 'd4Scheda'; g.setAttribute('aria-label', 'Apri la scheda originale nella Timeline: ' + op.titolo); acts.appendChild(g);
      hero.appendChild(acts); body.appendChild(hero);
      var secs = [];

      // tre assi distinti
      var ax = sect('Tre assi, mai fusi', null, 'assi'); ax.classList.add('d4-sec-ax');
      var row = el('div', 'd4-axes');
      var gtxt = op.guida ? 'N°' + op.guida.vis : null, gsub = op.guida ? 'ordine della guida' + (op.saga && op.saga.di > 1 ? ' · ' + op.saga.pos + ' di ' + op.saga.di + ' nella saga' : '') : null;
      row.appendChild(axisTile('In guida', gtxt, gsub, 'G', 'd4AxGuida'));
      row.appendChild(axisTile('Uscita', op.uscita ? dataIt(op.uscita.iso) : null, op.uscita ? ({ giorno: 'data certa', mese: 'solo mese', anno: 'solo anno' }[op.uscita.prec] || '') : null, 'G', 'd4AxUscita'));
      row.appendChild(axisTile('Ambientazione', op.ambientazione ? op.ambientazione.testo : null, op.ambientazione ? 'luogo o epoca della storia' : null, 'G', 'd4AxAmbi'));
      ax.appendChild(row); ax.appendChild(el('p', 'a2-note', 'La posizione in guida è una scelta editoriale: non coincide con la data di uscita né con la cronologia interna.')); body.appendChild(ax); secs.push(['assi', 'Assi']);

      // prima / dopo nella guida
      if (op.guida && (op.guida.prec || op.guida.succ)) {
        var pd = sect('Nella guida', 'G', 'guida'), pb = el('div', 'a2-chips');
        if (op.guida.prec) pb.appendChild(goBtn('item', op.guida.prec, IDX.titoli[op.guida.prec].title, 'prima · N°' + VN(IDX.titoli[op.guida.prec].num)));
        if (op.guida.succ) pb.appendChild(goBtn('item', op.guida.succ, IDX.titoli[op.guida.succ].title, 'dopo · N°' + VN(IDX.titoli[op.guida.succ].num)));
        pd.appendChild(pb); body.appendChild(pd); secs.push(['guida', 'Guida']);
      }
      // trama senza spoiler
      if (op.trama) { var tr = sect('Trama (senza spoiler)', 'G', 'trama'); tr.appendChild(el('p', 'd4-p', op.trama)); body.appendChild(tr); secs.push(['trama', 'Trama']); }
      // personaggi
      if (op.personaggi.length) {
        var pc = sect('Personaggi in archivio', 'G', 'personaggi', op.personaggi.length);
        pc.appendChild(chipsBox(op.personaggi, 14, function (c) { return goBtn('char', c, IDX.personaggi[c].name); }));
        body.appendChild(pc); secs.push(['personaggi', 'Personaggi']);
      } else if (op.personaggiTesto) {
        var pt = sect('Personaggi', 'G', 'personaggi'); pt.appendChild(el('p', 'd4-p', op.personaggiTesto)); pt.appendChild(el('p', 'a2-note', 'Nomi riportati dalla scheda; non hanno (ancora) una pagina nell’Atlante.')); body.appendChild(pt); secs.push(['personaggi', 'Personaggi']);
      }
      // interpreti
      if (op.attori.length) {
        var ia = sect('Interpreti', 'G', 'interpreti', op.attori.length), AT = XR.attori();
        ia.appendChild(chipsBox(op.attori, 12, function (aid) {
          var e = AT.byId[aid], ruoli = e.roles.filter(function (r) { return r.titoli.indexOf(id) !== -1; }).map(function (r) { return r.nome; }).filter(Boolean);
          return goBtn('att', aid, e.name, ruoli.slice(0, 1).join(''));
        }));
        body.appendChild(ia); secs.push(['interpreti', 'Interpreti']);
      }
      // universo e saga
      if (op.universi.length || op.saga) {
        var us = sect('Universo e saga', 'G', 'universo');
        if (op.universi.length) us.appendChild(chipsBox(op.universi, 6, function (u) { return goBtn('uni', u, UNI[u].nome || u); }));
        if (op.saga) us.appendChild(el('p', 'd4-p d4-saga', 'Saga: ' + op.saga.nome + (op.saga.di > 1 ? ' — ' + op.saga.pos + ' di ' + op.saga.di : '')));
        body.appendChild(us); secs.push(['universo', 'Universo']);
      }
      // opere collegate (prerequisiti e Dependency Map della guida)
      var dp = op.dip, dn = dp.richiede.length + dp.consigliati.length + dp.facoltativi.length + dp.dipendeDa.length;
      if (dn) {
        var dd = sect('Opere collegate', 'G', 'collegate', dn);
        [['richiede', 'Da vedere prima (essenziali)'], ['consigliati', 'Consigliati'], ['facoltativi', 'Facoltativi'], ['dipendeDa', 'Lo richiedono o lo consigliano']].forEach(function (p) {
          if (!dp[p[0]].length) return;
          dd.appendChild(el('h4', 'a2-sub', p[1] + ' (' + dp[p[0]].length + ')'));
          dd.appendChild(chipsBox(dp[p[0]], 8, function (t) { return goBtn('item', t, IDX.titoli[t].title, 'N°' + VN(IDX.titoli[t].num)); }));
        });
        dd.appendChild(el('p', 'a2-note', 'Dai prerequisiti e dalla Dependency Map della guida; la mappa completa resta nella scheda in guida.')); body.appendChild(dd); secs.push(['collegate', 'Collegate']);
      }
      // archivi collegati
      if (op.archivi.length) {
        var ar = sect('Archivi collegati', 'G', 'archivi', op.archivi.length), CL = { org: 'Organizzazioni', art: 'Artefatti', evt: 'Eventi', luo: 'Luoghi' };
        ['org', 'evt', 'luo', 'art'].forEach(function (cat) {
          var l = op.archivi.filter(function (x) { return x.cat === cat; }); if (!l.length) return;
          ar.appendChild(el('h4', 'a2-sub', CL[cat] + ' (' + l.length + ')'));
          ar.appendChild(chipsBox(l, 8, function (x) { return goBtn('arc', x.cat + ':' + x.id, x.nome, x.sub); }));
        });
        body.appendChild(ar); secs.push(['archivi', 'Archivi']);
      }
      // D4: organizzazione nel titolo (corrispondenza del titolo)
      var on = op.orgTitolo.filter(function (x) { return !x.confermato; });
      if (on.length) {
        var oo = sect('Nel titolo compare il nome di…', 'D', 'orgtitolo');
        oo.appendChild(chipsBox(on, 6, function (x) { return goBtn('arc', 'org:' + x.id, x.nome, 'corrispondenza del titolo'); }));
        oo.appendChild(el('p', 'a2-note', 'Corrispondenza del titolo: il nome dell’organizzazione è scritto nel titolo. Non è un’apparizione né una relazione narrativa documentata dalla guida.')); body.appendChild(oo); secs.push(['orgtitolo', 'Nel titolo']);
      }
      // ponti verso Universi (3A), Mappa (3B), Cronologie (3C)
      if (op.universi.length) {
        var br = sect('Apri anche', null, 'ponti');
        op.universi.slice(0, 3).forEach(function (u) {
          var r = el('div', 'd4-bridge'); r.appendChild(el('span', 'd4-bridge-n', (UNI[u].nome || u).replace(/^Earth-(\w+) — /, 'E-$1 ')));
          var bx = el('span', 'd4-bridge-b');
          bx.appendChild(btn('a2-ghost d4-bt', 'Dossier', function () { a.openUni(u); }));
          bx.appendChild(btn('a2-ghost d4-bt', 'Mappa', function () { a.openMappa(u); }));
          bx.appendChild(btn('a2-ghost d4-bt', 'Cronologia', function () { a.crOpen('uni', { uid: u }); }));
          r.appendChild(bx); br.appendChild(r);
        });
        body.appendChild(br);
      }
      var jb = jumpBar(secs); if (jb) body.insertBefore(jb, hero.nextSibling);
      var foot = el('section', 'a2-sec a2-foot d4-legend');
      foot.appendChild(el('p', 'a2-note', 'Fonti: ')); var lg = foot.firstChild; ['G', 'D', 'N'].forEach(function (k) { lg.appendChild(src(k)); lg.appendChild(D.createTextNode(' ' + SRC[k][1].split(' (')[0].toLowerCase() + ' · ')); });
      lg.lastChild.nodeValue = lg.lastChild.nodeValue.replace(/ · $/, '');
      foot.appendChild(btn('a2-ghost', 'Cerca un altro titolo', function () { a.nav('search'); })); body.appendChild(foot);
    }
    X.screens.opera = renderOpera;
    function openOpera(id, fromRouter) {
      if (!IDX.titoli[id]) return false;
      if (!fromRouter && tog.checked && W.tvaPushNav) W.tvaPushNav(short(IDX.titoli[id].title));
      ST.screen = 'opera'; ST.eid = id; if (!tog.checked) a.show(); a.draw(); a.setScroll(0); return true;
    }
    A.openOpera = openOpera;
    var prevLabel = X.label;
    X.label = function (s) { if (s.screen === 'opera') return IDX.titoli[s.eid] ? short(IDX.titoli[s.eid].title) : 'Titolo'; return prevLabel ? prevLabel(s) : null; };

    /* D1: nell'Atlante il chip «N°» / i titoli aprono il Dossier Opera; Mappa 3B e Cronologie 3C e la scheda in guida mantengono il comportamento esistente */
    var origGo = W.tvaGo;
    W.tvaGo = function (kind, id, opt) {
      if (kind === 'item' && !(opt && opt.scheda) && IDX.titoli[id] && tog.checked && ST.screen !== 'mappa' && ST.screen !== 'cron') return openOpera(id, false);
      return origGo.apply(this, arguments);
    };

    /* ================= DOSSIER PERSONAGGIO 2 (adattivo) E ATTORI ================= */
    var ATLP = {}; try { (JSON.parse($('atlasData').textContent).personaggi || []).forEach(function (p) { ATLP[p.id] = p; }); } catch (eAt) {}
    var PTIPO = a.PTIPO || {}, PSUB = a.PSUB || {};
    function strip(t) { return (t || '').replace(/[\u{1F000}-\u{1FFFF}←-➿️‍]/gu, '').replace(/\s+/g, ' ').trim(); }
    function cloneInto(dst, src) { Array.prototype.forEach.call(src.childNodes, function (n) { dst.appendChild(n.cloneNode(true)); }); return dst; }
    function linkN(root) {
      var w = D.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), nodes = [], n;
      while ((n = w.nextNode())) if (/N°\s*\d{3}/.test(n.nodeValue) && !(n.parentNode.closest && n.parentNode.closest('a,button'))) nodes.push(n);
      nodes.forEach(function (t) {
        var txt = t.nodeValue, frag = D.createDocumentFragment(), last = 0, m, re = /N°\s*(\d{3})/g;
        while ((m = re.exec(txt))) {
          var id = 'item-' + XR.FV(m[1]); if (!IDX.titoli[id]) continue;
          frag.appendChild(D.createTextNode(txt.slice(last, m.index)));
          var b = el('button', 'a2-n', 'N°' + m[1]); b.type = 'button'; b.setAttribute('data-go', 'item:' + id); b.title = IDX.titoli[id].title; b.setAttribute('aria-label', 'Apri ' + IDX.titoli[id].title);
          frag.appendChild(b); last = m.index + m[0].length;
        }
        if (!last) return; frag.appendChild(D.createTextNode(txt.slice(last))); t.parentNode.replaceChild(frag, t);
      });
      return root;
    }
    function kv(label, vNode) { var d = el('div', 'a2-kv'); d.appendChild(el('span', 'a2-k', label)); var v = el('div', 'a2-v'); cloneInto(v, vNode); linkN(v); d.appendChild(v); return d; }
    var KEYS = {
      'PRIMA APP.': ['Prima apparizione', 0], 'ULTIMA APP.': ['Ultima apparizione', 0], 'ALTRE APP.': ['Altre apparizioni', 0], 'COMPARE ANCHE IN (ATLANTE)': ['Compare anche in', 0],
      'UNIVERSI': ['Universi', 1], 'ORIGINE (ATLANTE)': ['Origine', 1],
      'POTERI': ['Poteri', 2], 'POTENZA TVA (ATLANTE)': ['Potenza TVA', 2], 'ENTITÀ, SPECIE E ARTI (ATLANTE)': ['Entità, specie e arti', 2],
      'CORRELATI': ['Correlati', 3], 'RELAZIONI': ['Relazioni', 3], 'COLLEGAMENTI': ['Collegamenti', 3], 'ORGANIZZAZIONI (ATLANTE)': ['Organizzazioni', 3], 'CITATO IN (ATLANTE)': ['Citato in', 3],
      'NEI FUMETTI': ['Nei fumetti', 4], 'DA LEGGERE': ['Da leggere', 4]
    };
    var GTIT = ['Apparizioni', 'Universi e origine', 'Poteri e natura', 'Legami', 'Nei fumetti'], GID = ['app', 'uni', 'pot', 'leg', 'fum'];
    // la riga di testo (PRIMA/ULTIMA/ALTRE APP.) e' ridondante solo se, tolti N° e titolo, non resta altro (note, cameo, universo)
    function righeRidondanti(row) {
      var t = row.querySelector('.detail-v').textContent, re = /N°\s*(\d{3})/g, m, ids = [];
      while ((m = re.exec(t))) { var id = 'item-' + XR.FV(m[1]); if (IDX.titoli[id]) ids.push(id); }
      if (!ids.length) return false;
      var left = t.replace(/N°\s*\d{3}/g, ' '); ids.forEach(function (i) { left = left.split(IDX.titoli[i].title).join(' '); });
      return left.replace(/[\s—–\-,;:·.]+/g, '') === '';
    }
    function appRow(tid, tag) {
      var br = XR.breve(tid); if (!br) return null;
      var b = btn('a2-row d4-app' + (br.visto ? ' seen' : ''), null); b.setAttribute('data-go', 'item:' + tid);
      b.appendChild(el('span', 'a2-row-n', br.vis ? 'N°' + br.vis : '·'));
      var tx = el('span', 'a2-row-t'); tx.appendChild(el('b', '', br.titolo));
      tx.appendChild(el('small', '', [tag, br.tipo, br.uscita ? dataIt(br.uscita) : br.anno].filter(Boolean).join(' · '))); b.appendChild(tx);
      b.appendChild(el('span', 'a2-row-s', br.visto ? '✓' : '○')); b.setAttribute('aria-label', br.titolo + (br.visto ? ', visto' : ', da vedere')); return b;
    }
    function renderChar2() {
      var id = ST.eid, c = IDX.personaggi[id];
      if (!c || !c.li) { ST.screen = 'personaggi'; return a.draw(); }
      body.className = 'a2-scroll a2-dossier a2-char d4-char'; body.textContent = ''; a.setTitle(c.name, 'Personaggi');
      var cr = crumb(); if (cr) body.appendChild(cr);
      var tipo = PTIPO[id] || 'personaggio', sub = PSUB[id] || '', secs = [];
      var hero = el('section', 'a2-hero a2-arc-hero a2-char-hero d4-hero'); a.heroImg(hero, 'personaggi'); hero.appendChild(a.cover('chr', id, c.name, 'a2-cov-hero'));
      hero.appendChild(el('span', 'a2-kick', (tipo === 'variante' ? 'VARIANTE' : tipo === 'aggregata' ? 'VOCE AGGREGATA' : tipo === 'segnaposto' ? 'VOCE GENERICA' : 'PERSONAGGIO')));
      hero.appendChild(el('h2', '', c.name));
      var P = XR.personaggio(id), apps = P.percorso;
      var rows = Array.prototype.filter.call(c.li.querySelectorAll('.detail-panel > .detail-row'), function (r) { return r.querySelector('.detail-k') && r.querySelector('.detail-v'); });
      var by = {}, other = [], firstRow = null;
      rows.forEach(function (r) {
        var k = strip(r.querySelector('.detail-k').textContent).toUpperCase(), m = KEYS[k];
        if (k === 'PRIMA APP.') firstRow = r.querySelector('.detail-v');
        if (m) (by[m[1]] = by[m[1]] || []).push([m[0], r, k]); else other.push([strip(r.querySelector('.detail-k').textContent), r]);
      });
      if (firstRow) { var fl = el('p', 'a2-descr'); fl.appendChild(D.createTextNode('Prima apparizione: ')); cloneInto(fl, firstRow); linkN(fl); hero.appendChild(fl); }
      body.appendChild(hero);
      var at = ATLP[id];
      if (sub && /^(incarnazion|versione|ambiguo|jolly|elenco)/.test(sub) || tipo === 'variante' || tipo === 'aggregata') body.appendChild(a.info('Voce speciale della guida (' + sub.replace(/-/g, ' ') + '): raccoglie più versioni o incarnazioni; non sono fuse in un unico personaggio.'));
      if (at && at.dubbio && at.dubbio.length) body.appendChild(a.info('Dato non confermato: ' + at.dubbio.map(function (d) { return typeof d === 'string' ? d : (d.nota || d.motivo || JSON.stringify(d)); }).join('; ') + '.'));
      var jbAt = body.lastChild;

      // 1. Percorso nella guida (apparizioni in ordine di guida)
      var s0 = by[0] || [], keep = s0.filter(function (p) { return p[0] !== 'Prima apparizione' && !(apps.length && /APP\.$/.test(p[2]) && righeRidondanti(p[1])); });
      if (apps.length || keep.length) {
        var sA = sect(apps.length > 1 ? 'Percorso nella guida' : 'Apparizione', 'G', 'app', apps.length || null);
        if (apps.length) {
          var ol = el('ul', 'a2-list d4-apps'), tagOf = {};
          function primoN(rw) { var m = rw && /N°\s*(\d{3})/.exec(rw.textContent); return m ? 'item-' + XR.FV(m[1]) : null; }
          var tp = primoN(firstRow), lastRow = null; (by[0] || []).forEach(function (q) { if (q[2] === 'ULTIMA APP.') lastRow = q[1].querySelector('.detail-v'); });
          var tu = primoN(lastRow); if (tp) tagOf[tp] = 'prima apparizione'; if (tu) tagOf[tu] = tagOf[tu] ? tagOf[tu] + ' e ultima' : 'ultima apparizione';
          apps.forEach(function (t) { var li = el('li'), r = appRow(t, apps.length > 1 ? tagOf[t] || '' : ''); if (r) { li.appendChild(r); ol.appendChild(li); } });
          sA.appendChild(ol);
          if (apps.length > 1) sA.appendChild(el('p', 'a2-note', 'Ordine della guida (scelta editoriale), non cronologia interna né data di uscita.'));
        }
        keep.forEach(function (p) { sA.appendChild(kv(p[0], p[1].querySelector('.detail-v'))); });
        body.appendChild(sA); secs.push(['app', 'Apparizioni']);
      }
      // 2. Interpreti (D: nome del ruolo = nome esatto della scheda)
      if (P.attori.length) {
        var sI = sect('Interpreti', 'D', 'att', P.attori.length), AT = XR.attori();
        sI.appendChild(chipsBox(P.attori, 6, function (aid) { return goBtn('att', aid, AT.byId[aid].name); }));
        sI.appendChild(el('p', 'a2-note', 'Dal nome del ruolo indicato nella scheda dell’attore, solo quando coincide con questa pagina.')); body.appendChild(sI); secs.push(['att', 'Interpreti']);
      }
      // 3. Identita' dichiarate e incarnazioni (solo dove i dati le dichiarano)
      var idn = XR.identita(id), inc = XR.incarnazioni(id);
      if (idn.length) {
        var sD = sect('Stesso individuo, secondo la guida', 'G', 'idn');
        idn.forEach(function (g) {
          sD.appendChild(el('h4', 'a2-sub', g.nome));
          sD.appendChild(chipsBox((g.pagine || []).filter(function (x) { return x !== id && IDX.personaggi[x]; }), 6, function (x) { return goBtn('char', x, IDX.personaggi[x].name); }));
          if (g.nota) sD.appendChild(el('p', 'a2-note', g.nota));
        });
        body.appendChild(sD); secs.push(['idn', 'Identità']);
      }
      if (inc && (inc.incarnazioni.length || inc.collegamenti.length)) {
        var sV = sect('Versioni documentate', 'G', 'var');
        inc.incarnazioni.forEach(function (i) {
          var r = el('div', 'd4-inc'); r.appendChild(chipsBox(i.universi, 3, function (u) { return goBtn('uni', u, (UNI[u].nome || u).replace(/^Earth-(\w+) — /, 'E-$1 ')); }));
          if (i.titoli.length) r.appendChild(chipsBox(i.titoli, 4, function (t) { return goBtn('item', t, IDX.titoli[t].title, 'N°' + VN(IDX.titoli[t].num)); })); sV.appendChild(r);
        });
        inc.collegamenti.forEach(function (cl) { var r = el('p', 'd4-p', 'Collegamento multiversale con l’MCU (' + (cl.tipo || 'tipo non indicato') + ')' + (cl.origine ? ': ' + cl.origine : '') + '.'); sV.appendChild(r); });
        sV.appendChild(el('p', 'a2-note', 'Le versioni non sono fuse in un unico personaggio: ognuna resta distinta nel suo universo.')); body.appendChild(sV); secs.push(['var', 'Versioni']);
      }
      // 4. sezioni della guida (solo se hanno contenuti)
      for (var g = 1; g < GTIT.length; g++) {
        if (!by[g] || !by[g].length) continue;
        var s = sect(GTIT[g], 'G', GID[g]); by[g].forEach(function (p) { s.appendChild(kv(p[0], p[1].querySelector('.detail-v'))); }); body.appendChild(s); secs.push([GID[g], ['', 'Universi', 'Poteri', 'Legami', 'Fumetti'][g]]);
      }
      if (other.length) { var so = sect('Altro dalla guida', 'G', 'alt'); other.forEach(function (p) { so.appendChild(kv(p[0], p[1].querySelector('.detail-v'))); }); body.appendChild(so); }
      var jb = jumpBar(secs); if (jb) body.insertBefore(jb, hero.nextSibling);
      var foot = el('section', 'a2-sec a2-foot'); foot.appendChild(btn('a2-ghost', 'Tutti i personaggi', function () { a.nav('personaggi', { pf: 'tutti', pq: '' }); })); body.appendChild(foot);
    }
    X.screens.char = renderChar2;

    // Attore: titoli in ordine di guida (aggiunta in testa alla scheda esistente)
    var prevAtt = X.screens.attore;
    X.screens.attore = function () {
      prevAtt(); var e = XR.attori().byId[ST.eid]; if (!e) return;
      var cr = crumb(); if (cr) body.insertBefore(cr, body.firstChild);
      if (e.titles.length > 1) {
        var s = sect('Titoli in ordine di guida', 'G', 'film', e.titles.length), hero = body.querySelector('.a2-hero');
        s.appendChild(chipsBox(e.titles, 12, function (t) { var b = XR.breve(t); return goBtn('item', t, b.titolo, b.vis ? 'N°' + b.vis : ''); }));
        s.appendChild(el('p', 'a2-note', 'Ordine della guida (scelta editoriale), non data di uscita.'));
        if (hero && hero.nextSibling) body.insertBefore(s, hero.nextSibling); else body.appendChild(s);
      }
    };

    /* ================= SPRINT D — identita' degli archivi e dossier secondari ================= */
    var SRCMAP = [[/^Scheda/, 'G'], [/^Membri e leader/, 'G'], [/^(Titoli|Compare nei titoli)/, 'G'], [/^Universi/, 'D'], [/^Personaggi citati/, 'D'], [/^Altre schede collegate/, 'D']];
    function jl(t) { var m = [[/^Scheda/, 'Scheda'], [/^Membri/, 'Membri'], [/^(Compare nei|Titoli \(in)/, 'Titoli'], [/^Titoli con/, 'Nel titolo'], [/^Universi/, 'Universi'], [/^Personaggi/, 'Personaggi'], [/^Altre schede/, 'Collegate']].filter(function (x) { return x[0].test(t); })[0]; return m ? m[1] : t.split(' ')[0]; }
    function decorateArc() {
      var M = A.arcModel ? A.arcModel() : null, e = M && M.byId[ST.eid]; if (!e) return;
      body.classList.add('d4-skin', 'd4-skin-' + e.cat);
      var cr = crumb(); if (cr && !body.querySelector('.d4-crumb')) body.insertBefore(cr, body.firstChild);
      // D4: titoli che contengono il nome dell'organizzazione (corrispondenza del titolo, separata dai titoli confermati)
      if (e.cat === 'org') {
        var tc = XR.titoliConNomeOrg(e.id).filter(function (x) { return !x.confermato; });
        if (tc.length) {
          var s = sect('Titoli con il nome nel titolo', 'D', 'nome', tc.length);
          s.appendChild(chipsBox(tc, 8, function (x) { var b = XR.breve(x.id); return goBtn('item', x.id, x.titolo, b && b.vis ? 'N°' + b.vis : 'serie animata'); }));
          s.appendChild(el('p', 'a2-note', 'Corrispondenza del titolo: il nome dell’organizzazione è scritto nel titolo. Non è un’apparizione né una relazione narrativa documentata dalla guida, ed è separata dai titoli confermati qui sopra.'));
          var prim = body.querySelector('.a2-sec-prim'); if (prim && prim.nextSibling) body.insertBefore(s, prim.nextSibling); else body.appendChild(s);
        }
      }
      var secs = []; Array.prototype.forEach.call(body.children, function (n, i) {
        if (n.tagName !== 'SECTION' || !n.classList.contains('a2-sec') || n.classList.contains('a2-foot')) return;
        var h = n.querySelector('h3'); if (!h) return; var t = h.firstChild ? h.firstChild.nodeValue || h.textContent : h.textContent; t = t.replace(/\s*\(\d+\)\s*$/, '').trim(); if (!t) return;
        if (!n.getAttribute('data-d4sec')) n.setAttribute('data-d4sec', 'x' + i);
        if (!h.querySelector('.d4-src')) SRCMAP.some(function (m) { if (m[0].test(t)) { h.appendChild(src(m[1])); return true; } });
        secs.push([n.getAttribute('data-d4sec'), jl(t)]);
      });
      var hero = body.querySelector('.a2-arc-hero'), jb = jumpBar(secs); if (jb && hero) body.insertBefore(jb, hero.nextSibling);
    }
    var prevDos = X.screens.dossier;
    if (prevDos) X.screens.dossier = function () { prevDos.apply(this, arguments); decorateArc(); };
  } catch (eD4) { if (window.console) console.error('Dossier 4:', eD4); }
})();
