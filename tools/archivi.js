/* ===== TVA ARCHIVES — ARCHIVI (Organizzazioni, Artefatti e Gemme, Eventi e Battaglie, Luoghi) =====
   Nessun dato duplicato: il modello e' letto dalle schede dell'archivio classico (unica fonte). Le relazioni mostrate sono
   soltanto quelle presenti nel testo della guida: numeri di scheda (N°/#), e nomi citati per esteso. I nomi ambigui non si collegano. */
(function () {
  'use strict';
  try {
    var W = window, D = document, A = W.tvaAtlas2, X = A && A.ext, a = X && X.api;
    // Numero visibile (N°, posizionale) <-> id stabile; posizione di guida. Fonte: funzioni window.marvel* del modulo principale quando sono gia' definite
    // oppure, se questo modulo parte prima, la stessa tabella ricavata dal DOM (.rec delle schede): stessa regola, nessun dato duplicato.
    var _NV = null;
    function nvTab() { if (_NV) return _NV; var a = {}, b = {}, g = {}; Array.prototype.forEach.call(D.querySelectorAll('.card-wrap[id^="item-"]'), function (n, k) { var id = n.id.slice(5), r = n.querySelector('.rec'), m = r && /(\d+)/.exec(r.textContent), v = m ? m[1] : id; a[id] = v; b[v] = id; g[id] = k; }); return (_NV = { a: a, b: b, g: g }); }
    function k3(n) { return ('000' + n).slice(-3); }
    function VN(n) { try { return W.marvelNumeroVisibile ? W.marvelNumeroVisibile(n) : (nvTab().a[k3(n)] || k3(n)); } catch (e) { return n; } }
    function FV(n) { try { return W.marvelIdDaNumeroVisibile ? W.marvelIdDaNumeroVisibile(n) : (nvTab().b[k3(n)] || k3(n)); } catch (e) { return n; } }
    function GP(n) { var m = /^(?:item-)?(\d{3})$/.exec(String(n)); if (!m) return null; try { var p = W.marvelPosizioneGuida ? W.marvelPosizioneGuida(m[1]) : nvTab().g[m[1]]; return p === undefined ? null : p; } catch (e) { return null; } }
    function byGuide(a, b) { var pa = /^([a-z0-9]+)-/.exec(String(a)), pb = /^([a-z0-9]+)-/.exec(String(b)); pa = pa ? pa[1] : 'item'; pb = pb ? pb[1] : 'item'; if (pa !== pb) return pa < pb ? -1 : 1; var x = GP(a), y = GP(b); if (x !== null && y !== null && x !== y) return x - y; return a < b ? -1 : a > b ? 1 : 0; }

    if (!a) return;
    var $ = a.$, el = a.el, btn = a.btn, ST = a.ST, UNI = a.UNI, IDX = a.IDX, body = a.body;
    var CATS = {
      org: { n: 'Organizzazioni', one: 'Organizzazione', art: 'org', kick: 'IDENTITÀ E POTERE', lead: 'Chi le guida, chi ne fa parte e dove compaiono.' },
      art: { n: 'Artefatti', one: 'Artefatto', art: 'gemma', kick: 'RELIQUIE E ARTI ARCANE', lead: 'Reliquie, armi e le sei Gemme dell’Infinito.' },
      evt: { n: 'Eventi', one: 'Evento', art: 'eventi', kick: 'MULTIVERSO E TEMPO', lead: 'Gli eventi della guida e le Battaglie, che ne sono una categoria.' },
      luo: { n: 'Luoghi', one: 'Luogo', art: 'luoghi', kick: 'MONDI E CIVILTÀ', lead: 'Pianeti e luoghi, con i titoli in cui compaiono.' },
      cos: { n: 'Entità Cosmiche', one: 'Entità', art: 'poteri', kick: 'IDENTITÀ E POTERE', lead: 'Fumetti e schermo restano separati: nessuna versione è fusa con l’altra.', unit: 'entità',
        note: 'Sullo schermo: le entità che la guida stessa descrive come Celestiale, entità cosmica, Osservatore o Araldo cosmico. Mai apparse: l’elenco «Chi manca ancora» della guida, con i suoi raggruppamenti. Le versioni dei fumetti sono indicate a parte.' },
      spe: { n: 'Specie e Civiltà', one: 'Specie', art: 'personaggi', kick: 'MONDI E CIVILTÀ', lead: 'Voci aggregate dal TVA: specie, popolazioni e civiltà citate in più schede.', unit: 'voci',
        note: 'La guida non ha schede dedicate alle specie: ogni voce raccoglie le schede che la citano (almeno 3). Il tipo (Specie, Popolazione, Civiltà) è una classificazione editoriale TVA. Origini e caratteristiche sono riportate solo se scritte nella guida.' },
      mis: { n: 'Arti Mistiche', one: 'Disciplina', art: 'gemma', kick: 'RELIQUIE E ARTI ARCANE', lead: 'Discipline mistiche che la guida documenta in più schede.', unit: 'discipline',
        note: 'Solo discipline che la guida nomina esplicitamente: tre o più schede, oppure due schede se la disciplina ha un nome proprio (segnalate come «dati limitati»). Non ogni potere soprannaturale è una disciplina mistica: poteri innati, tecnologia e forze cosmiche restano fuori.' }
    };
    var SPEC = { org: [['org-', 'Organizzazione', 'dbtab-org']], art: [['art-', '', 'dbtab-art']], evt: [['evt-', 'Evento', 'dbtab-evt'], ['bat-', 'Battaglia', 'dbtab-bat']], luo: [['pia-', 'Pianeta', 'dbtab-pia'], ['luo-', 'Luogo', 'dbtab-luo']] };
    var SKIP = { 'COMPARE IN': 1, 'TITOLI': 1 };

    /* ---------- modello (lazy, letto dal DOM classico) ---------- */
    var M = null;
    function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
    function toks(name, isArc) {
      var out = [], base = name.replace(/\s*\([^)]*\)/g, '').trim();
      function add(t) { t = (t || '').trim(); if (t.length >= 4 && /^[A-ZÀ-Ý0-9]/.test(t) && out.indexOf(t) === -1) out.push(t); }
      add(base); base.split('/').forEach(add); add(base.replace(/^(Il|I|La|Le|Lo|Gli|L')\s*/i, ''));
      (name.match(/\(([^)]*)\)/g) || []).forEach(function (p) { add(p.slice(1, -1)); });
      return out;
    }

    /* ---------- verifica dei riferimenti ai titoli ----------
       I campi «COMPARE IN» / «TITOLI» delle schede usano numerazioni diverse: a volte «#083» (solo numero), a volte «N°083 — Avengers: Infinity War».
       Per molte schede il numero è sfasato di 1 rispetto alla numerazione attuale dei titoli (es. «N°083 — Avengers: Infinity War», che oggi è N°084).
       Regola: un riferimento è VERIFICATO se (1) il titolo è nominato accanto al numero, (2) la cronologia delle Gemme della guida lo conferma con lo stesso numero,
       (3) il nome del titolo compare per esteso nel testo della scheda, oppure (4) un personaggio collegato alla scheda ha davvero quel titolo tra le sue apparizioni.
       Altrimenti resta «non confermato»: viene mostrato a parte e non conta come collegamento. Nessuna associazione viene inventata. */
    function NN(t) { return (t || '').replace(/&amp;/g, '&').toLowerCase().replace(/&/g, 'and').replace(/[’‘`]/g, '').replace(/[^a-z0-9]/g, ''); }
    function titleByName(nm) {
      if (!M._tn) { M._tn = {}; Object.keys(IDX.titoli).forEach(function (k) { var t = IDX.titoli[k]; if (t.kind === 'item' && !t.variant && !M._tn[NN(t.title)]) M._tn[NN(t.title)] = k; }); }
      return M._tn[NN((nm || '').replace(/\s*\(\d{4}\)\s*$/, ''))] || null;
    }
    function appsOf(cid) {
      M._ap = M._ap || {}; if (M._ap[cid]) return M._ap[cid];
      var out = {}, c = IDX.personaggi[cid], li = c && c.li;
      if (li) Array.prototype.forEach.call(li.querySelectorAll('.detail-row'), function (r) {
        if (r.classList.contains('tva-row')) return;
        var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v'); if (!k || !v || !/APP\.|COMPARE ANCHE IN/.test(k.textContent)) return;
        var m, re = /N°\s*(\d{3})/g, tx = v.textContent; while ((m = re.exec(tx))) out['item-' + FV(m[1])] = 1;
      });
      return (M._ap[cid] = out);
    }
    function gemChrono() {
      if (M._gc) return M._gc; M._gc = {};
      var host = D.getElementById('chrono-gemme-dell-infinito'); if (!host) return M._gc;
      var tx = host.textContent.replace(/\s+/g, ' ').replace(/[’‘]/g, "'"), parts = tx.split(/(?=Gemma (?:dello|della|del|dell')|Tutte e sei)/);
      M.cat.art.forEach(function (e) {
        var base = e.name.replace(/\s*\([^)]*\)/, '').replace(/[’‘]/g, "'").trim(), isG = /^Guanto/.test(e.name);
        var part = parts.filter(function (p) { return isG ? /^Tutte e sei/.test(p) : p.indexOf(base) === 0; })[0]; if (!part) return;
        var t = {}, m, re = /N°\s*(\d{3})/g; while ((m = re.exec(part))) if (IDX.titoli['item-' + FV(m[1])]) t['item-' + FV(m[1])] = 1;
        M._gc[e.id] = { titles: t, text: part };
      });
      return M._gc;
    }
    function refineTitles(scan) {
      var GC = gemChrono();
      M.list.forEach(function (e) {
        var stated = [], named = {}, any = false;
        ['COMPARE IN', 'TITOLI'].forEach(function (k) {
          var v = e.f[k]; if (!v) return;
          var m = v.match(/^((?:N°\s*\d{3}\s*,?\s*)+)—\s*(.+)$/);
          if (m) {
            var nums = (m[1].match(/\d{3}/g) || []), names = m[2].split(/,\s*(?=[A-Z0-9])/);
            if (nums.length === names.length) nums.forEach(function (n, i) { var tid = titleByName(names[i]); if (tid) named['item-' + FV(n)] = tid; });
          }
          var re = /(?:N°|#)\s*(\d{3})/g, mm; while ((mm = re.exec(v))) { var id = 'item-' + FV(mm[1]); if (IDX.titoli[id] && stated.indexOf(id) === -1) stated.push(id); }
        });
        var txt = NN(Object.keys(e.f).filter(function (k) { return !SKIP[k]; }).map(function (k) { return e.f[k]; }).join(' '));
        var ver = {}, un = [], why = {};
        stated.forEach(function (id) { if (named[id]) { ver[named[id]] = 1; why[named[id]] = 'nome'; if (named[id] !== id) e.mism = (e.mism || []).concat([[id.slice(5), named[id]]]); } });
        Object.keys(named).forEach(function (id) { if (!(named[id] in ver)) { ver[named[id]] = 1; why[named[id]] = 'nome'; } });
        var gc = GC[e.id];
        if (gc) {
          Object.keys(gc.titles).forEach(function (id) { ver[id] = 1; why[id] = why[id] || 'cronologia'; });
          scan(gc.text, e.id).forEach(function (key) {
            var id = key.slice(2);
            if (key[0] === 'c') { if (e.cited.indexOf(id) === -1) { e.cited.push(id); (M.charCited[id] = M.charCited[id] || []).push(e.id); } }
            else if (e.arcs.indexOf(id) === -1) { e.arcs.push(id); (M.citedBy[id] = M.citedBy[id] || []).push(e.id); }
          });
        }
        var chars = e.members.concat(e.leader, e.cited);
        stated.forEach(function (id) {
          if (id in ver) return;
          var t = IDX.titoli[id], nm = t && NN(t.title);
          if (nm && nm.length >= 9 && txt.indexOf(nm) !== -1) { ver[id] = 1; why[id] = 'testo'; return; }
          if (chars.some(function (c) { return appsOf(c)[id]; })) { ver[id] = 1; why[id] = 'personaggio'; return; }
          un.push(id);
        });
        // titoli nominati per esteso nel testo della scheda (es. «distrutto in Thor: Ragnarok»)
        Object.keys(IDX.titoli).forEach(function (id) {
          if (id in ver) return; var t = IDX.titoli[id]; if (t.kind !== 'item' || t.variant) return;
          var nm = NN(t.title); if (nm.length >= 11 && txt.indexOf(nm) !== -1) { ver[id] = 1; why[id] = 'testo'; }
        });
        var prev = e.titles.slice(); e.titles = Object.keys(ver).sort(byGuide); e.unconf = un.filter(function (id) { return !(id in ver); }).sort(byGuide); e.why = why; e.statedTitles = prev;
      });
      M.byTitle = {}; M.byUni = {};
      M.list.forEach(function (e) {
        var us = {}; e.titles.forEach(function (tid) { (M.byTitle[tid] = M.byTitle[tid] || []).push(e.id); (IDX.titoli[tid].unis || []).forEach(function (u) { if (UNI[u]) us[u] = 1; }); });
        e.unis = Object.keys(us); e.unis.forEach(function (u) { (M.byUni[u] = M.byUni[u] || []).push(e.id); });
      });
    }
    function build() {
      if (M) return M;
      M = { list: [], byId: {}, cat: { org: [], art: [], evt: [], luo: [], cos: [], spe: [], mis: [] }, charExtra: {}, scan: null, byUni: {}, byTitle: {}, charOrg: {}, charCited: {}, citedBy: {} };
      Object.keys(SPEC).forEach(function (cat) {
        SPEC[cat].forEach(function (sp) {
          D.querySelectorAll('#tvaArchivesOverlayEl li[id^="' + sp[0] + '"]').forEach(function (li) {
            var t = li.querySelector('.title'); if (!t) return;
            var e = { id: li.id, cat: cat, pre: sp[0], dbtab: sp[2], name: t.textContent.trim(), sub: sp[1], f: {}, titles: [], vago: false, unis: [], members: [], leader: [], cited: [], arcs: [], li: li };
            Array.prototype.forEach.call(li.querySelectorAll('.detail-row'), function (r) {
              if (r.classList.contains('tva-row')) return;
              var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v'); if (k && v) e.f[k.textContent.trim()] = v.textContent.trim();
            });
            if (cat === 'art') e.sub = /^Gemma /.test(e.name) ? 'Gemma dell’Infinito' : (/^Guanto/.test(e.name) ? 'Guanto' : 'Artefatto');
            ['COMPARE IN', 'TITOLI'].forEach(function (k) {
              var v = e.f[k]; if (!v) return; var m, re = /(?:N°|#)\s*(\d{3})/g;
              while ((m = re.exec(v))) { var id = 'item-' + FV(m[1]); if (IDX.titoli[id] && e.titles.indexOf(id) === -1) e.titles.push(id); }
              if (/successiv|\baltri\b|\becc\b|\.\.\./i.test(v)) e.vago = true;
            });
            e.titles.sort(byGuide);
            var us = {}; e.titles.forEach(function (tid) { (IDX.titoli[tid].unis || []).forEach(function (u) { if (UNI[u]) us[u] = 1; }); }); e.unis = Object.keys(us);
            M.list.push(e); M.byId[e.id] = e; M.cat[cat].push(e);
            e.titles.forEach(function (tid) { (M.byTitle[tid] = M.byTitle[tid] || []).push(e.id); });
            e.unis.forEach(function (u) { (M.byUni[u] = M.byUni[u] || []).push(e.id); });
          });
        });
      });
      // indice dei nomi: scheda personaggio (c:) o altra scheda d'archivio (a:); un nome che indica piu' schede e' ambiguo e non si collega
      var index = {};
      function put(tok, key) { (index[tok] = index[tok] || []); if (index[tok].indexOf(key) === -1) index[tok].push(key); }
      a.personaggiLista().forEach(function (c) { toks(c.name).forEach(function (t) { put(t, 'c:' + c.id); }); });
      M.list.forEach(function (e) { toks(e.name, true).forEach(function (t) { put(t, 'a:' + e.id); }); });
      var TK = Object.keys(index).filter(function (t) { return index[t].length === 1; }).map(function (t) { return { t: t, k: index[t][0], re: new RegExp('(?<![\\p{L}\\p{N}])' + esc(t) + '(?![\\p{L}\\p{N}])', 'u') }; });
      function scan(text, selfId) {
        var hits = [];
        TK.forEach(function (x) { var m = x.re.exec(text); if (m && x.k !== 'a:' + selfId) hits.push({ s: m.index, e: m.index + x.t.length, k: x.k, l: x.t.length }); });
        hits.sort(function (p, q) { return q.l - p.l; });
        var acc = [], keys = [];
        hits.forEach(function (h) { if (!acc.some(function (o) { return h.s < o.e && h.e > o.s; })) { acc.push(h); if (keys.indexOf(h.k) === -1) keys.push(h.k); } });
        return keys;
      }
      M.list.forEach(function (e) {
        var memb = {}, cit = {}, arcs = {};
        Object.keys(e.f).forEach(function (k) {
          if (SKIP[k]) return;
          scan(e.f[k], e.id).forEach(function (key) {
            var id = key.slice(2);
            if (key[0] === 'a') { arcs[id] = 1; return; }
            if (e.cat === 'org' && k === 'MEMBRI') memb[id] = 1; else if (e.cat === 'org' && k === 'LEADER') { e.leader.push(id); } else cit[id] = 1;
          });
        });
        e.members = Object.keys(memb); e.cited = Object.keys(cit).filter(function (c) { return !memb[c] && e.leader.indexOf(c) === -1; }); e.arcs = Object.keys(arcs);
        e.members.concat(e.leader).forEach(function (c) { if (e.cat === 'org') { (M.charOrg[c] = M.charOrg[c] || []); if (M.charOrg[c].indexOf(e.id) === -1) M.charOrg[c].push(e.id); } });
        e.cited.forEach(function (c) { (M.charCited[c] = M.charCited[c] || []).push(e.id); });
        e.arcs.forEach(function (o) { (M.citedBy[o] = M.citedBy[o] || []).push(e.id); });
      });
      M.scan = scan; M._index = index; M._TK = TK;
      try { refineTitles(scan); } catch (eR) { if (W.console) console.error('TVA Archives - verifica dei riferimenti ai titoli:', eR); }
      try { build3(); } catch (e3) { if (W.console) console.error('TVA Archives - Fase 3 (modello):', e3); }
      return M;
    }
    function catOf(id) { var e = build().byId[id]; return e ? e.cat : null; }
    function short(n, k) { return n.length > k ? n.slice(0, k - 1) + '…' : n; }
    function firstSentence(t, k) { if (!t) return ''; var m = t.match(/^.{20,}?[.;](\s|$)/); var s = m ? m[0].trim() : t; return s.length > k ? s.slice(0, k - 1).trim() + '…' : s; }
    function seenOf(e) { var v = 0; e.titles.forEach(function (tid) { var c = IDX.titoli[tid].li.querySelector('.watch-check, .anim-watch-check'); if (c && c.checked) v++; }); return v; }

    /* ---------- navigazione ---------- */
    function openDossier(cat, id, fromRouter) {
      if (!fromRouter && a.tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante');
      ST.screen = 'dossier'; ST.arc = cat; ST.eid = id;
      if (!a.tog.checked) a.show();
      a.draw(); a.setScroll(0);
    }
    A.openArc = function (cat, id, fromRouter) { build(); if (!M.byId[id]) return false; openDossier(M.byId[id].cat, id, fromRouter); return true; };
    A.arcLabel = function (id) { var e = build().byId[id]; return e ? short(e.name, 22) : 'Archivio'; };
    function goArc(cat, id) { return a.nav('dossier', { arc: cat, eid: id }); }
    function classic(e) {
      a.openArchive(e.dbtab);
      var c = $(e.id); if (c) { var d = c.querySelector('details'); if (d) d.setAttribute('open', ''); if (W.tvaSettleScroll) W.tvaSettleScroll(c); }
    }
    function arcChip(id, extra) { var e = M.byId[id]; var c = a.go('arc', e.cat + ':' + id, e.name); if (extra !== false) c.appendChild(el('small', '', e.cat === 'evt' ? e.sub : (e.cat === 'luo' ? e.sub : CATS[e.cat].one))); return c; }
    function charChip(cid) { return a.go('char', cid, IDX.personaggi[cid].name); }
    function chipsBox(ids, mk, LIM) {
      var box = el('div', 'a2-chips'); LIM = LIM || 14;
      ids.forEach(function (x, i) { var c = mk(x); if (i >= LIM) { c.hidden = true; c.setAttribute('data-more', '1'); } box.appendChild(c); });
      if (ids.length > LIM) { var m = btn('a2-chip a2-moreb', '+' + (ids.length - LIM) + ' altri', function () { Array.prototype.forEach.call(box.querySelectorAll('[data-more]'), function (x) { x.hidden = false; }); m.remove(); }); box.appendChild(m); }
      return box;
    }

    /* ---------- schermata: catalogo di un archivio ---------- */
    function renderArch() {
      var cat = ST.arc, C = CATS[cat]; if (!C) { ST.screen = 'catalogo'; return a.draw(); }
      build(); body.className = 'a2-scroll a2-arc a2-arc-' + cat; body.textContent = '';
      var all = M.cat[cat]; a.setTitle(C.n, 'Archivio');
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, cat); hero.appendChild(a.art(C.art, 'a2-arc-ic'));
      hero.appendChild(el('span', 'a2-kick', C.kick)); hero.appendChild(el('h2', '', C.n));
      var LBL = { 'Evento': 'eventi', 'Battaglia': 'battaglie', 'Pianeta': 'pianeti', 'Luogo': 'luoghi', 'Gemma dell’Infinito': 'Gemme', 'Guanto': 'Guanto', 'Artefatto': 'altri artefatti', 'Organizzazione': '' };
      var nSub = {}; all.forEach(function (e) { nSub[e.sub] = (nSub[e.sub] || 0) + 1; });
      var parts = Object.keys(nSub).map(function (k) { return LBL[k] ? nSub[k] + ' ' + LBL[k] : ''; }).filter(Boolean);
      if (cat === 'cos') parts = [all.filter(function (e) { return e.onscreen; }).length + ' sullo schermo', all.filter(function (e) { return !e.onscreen; }).length + ' mai apparse'];
      hero.appendChild(el('p', '', all.length + ' ' + (C.unit ? C.unit : 'schede nella guida') + (parts.length > 1 ? ' (' + parts.join(', ') + ')' : '') + '. ' + C.lead));
      body.appendChild(hero);
      if (C.note) body.appendChild(el('p', 'a2-note a2-arc-note', C.note));
      if (cat === 'mis' && M.misGaps) {
        var gp = el('details', 'a2-unconf a2-gaps'); gp.appendChild(el('summary', '', 'Discipline cercate ma non documentate a sufficienza (' + M.misGaps.length + ')'));
        var gl = el('ul', 'a2-unc-l');
        M.misGaps.forEach(function (g) {
          var li = el('li'); var n = g.ids.length;
          var txt = g.name + ': ' + (n === 0 ? 'nessuna scheda della guida la nomina.' : (g.inStr === n ? n + (n === 1 ? ' scheda, già compresa' : ' schede, già comprese') + ' in «Stregoneria e Arti Mistiche» (non è una disciplina separata nei dati).' : n + (n === 1 ? ' sola scheda' : ' schede') + ': dati insufficienti per una voce.'));
          li.appendChild(D.createTextNode(txt + ' ')); if (n && g.inStr !== n) g.ids.slice(0, 3).forEach(function (id) { var c = M.byId[id] ? arcChip(id, false) : charChip(id); li.appendChild(c); });
          gl.appendChild(li);
        });
        gp.appendChild(gl); gp.appendChild(el('p', 'a2-note', 'Per integrarle servono schede o frasi della guida che le nominino (es. un campo «Tradizione magica» nei personaggi). Finché mancano, non vengono create categorie artificiali.')); body.appendChild(gp);
      }
      if (cat === 'art') { var rb = btn('a2-primary a2-rel-btn', 'Apri il Reliquiario delle sei Gemme', function () { a.nav('reliquiario', { arc: 'art', eid: null }); }); body.appendChild(rb); }
      var extra = cat === 'art' ? ['Cronologia delle Gemme', 'chrono-gemme-dell-infinito'] : (cat === 'evt' ? ['Cronologia di Battleworld', 'chrono-battleworld'] : null);
      var res = el('div', 'a2-gridwrap');
      var inp;
      body.appendChild(a.searchBox('a2ArcSearch', ST.aq, function (v) { ST.aq = v; draw2(); }, 'Cerca in ' + C.n.toLowerCase() + '…'));
      var fl = el('div', 'a2-filters'); fl.setAttribute('role', 'group'); fl.setAttribute('aria-label', 'Filtra');
      var subs = []; all.forEach(function (e) { if (subs.indexOf(e.sub) === -1) subs.push(e.sub); });
      var fopts = [['tutti', 'Tutti ' + all.length]];
      if (subs.length > 1) subs.forEach(function (s) { fopts.push([s, (cat === 'evt' && s === 'Battaglia' ? 'Battaglie' : (cat === 'evt' ? 'Eventi' : (cat === 'luo' ? (s === 'Pianeta' ? 'Pianeti' : 'Luoghi') : (s === 'Gemma dell’Infinito' ? 'Gemme' : s === 'Artefatto' ? 'Altri artefatti' : s)))) + ' ' + all.filter(function (e) { return e.sub === s; }).length]); });
      if (cat === 'art') { var g = all.filter(function (e) { return e.cat === 'art'; }); }
      fopts.forEach(function (p) { var b = btn('a2-f' + (ST.af === p[0] ? ' on' : ''), p[1], function () { ST.af = p[0]; Array.prototype.forEach.call(fl.children, function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('on'); b.setAttribute('aria-pressed', 'true'); draw2(); }); b.setAttribute('aria-pressed', ST.af === p[0] ? 'true' : 'false'); fl.appendChild(b); });
      if (fopts.length > 1) body.appendChild(fl);
      var us = {}; all.forEach(function (e) { e.unis.forEach(function (u) { us[u] = (us[u] || 0) + 1; }); });
      var uk = Object.keys(us);
      if (uk.length >= 2) {
        var fu = el('div', 'a2-filters a2-fam'); fu.setAttribute('role', 'group'); fu.setAttribute('aria-label', 'Filtra per universo dei titoli');
        [['tutti', 'Tutti gli universi']].concat(uk.sort(function (x, y) { return us[y] - us[x]; }).map(function (u) { return [u, IDX.breve(u) + ' ' + us[u]]; })).forEach(function (p) {
          var b = btn('a2-f' + (ST.au === p[0] ? ' on' : ''), p[1], function () { ST.au = p[0]; Array.prototype.forEach.call(fu.children, function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('on'); b.setAttribute('aria-pressed', 'true'); draw2(); }); b.setAttribute('aria-pressed', ST.au === p[0] ? 'true' : 'false'); fu.appendChild(b);
        });
        body.appendChild(fu); body.appendChild(el('p', 'a2-note', 'Universo = quello dei titoli in cui la scheda compare (dato derivato dai titoli).'));
      }
      body.appendChild(res);
      if (extra && D.querySelector('#tvaArchivesOverlayEl [data-target="' + extra[1] + '"]')) { var xb = btn('a2-ghost', extra[0], function () { a.nav('chrono', { eid: extra[1] }); }); body.appendChild(xb); }
      function draw2() {
        res.textContent = '';
        var q = ST.aq.trim().toLowerCase(), grid = el('div', 'a2-grid');
        var list = all.filter(function (e) { return (ST.af === 'tutti' || e.sub === ST.af) && (ST.au === 'tutti' || e.unis.indexOf(ST.au) !== -1) && (!q || e.name.toLowerCase().indexOf(q) !== -1); });
        list.forEach(function (e) {
          var c = btn('a2-card a2-arcard', null, function () { goArc(cat, e.id); }); c.setAttribute('data-arc', e.id);
          var h = el('div', 'a2-card-h'); h.appendChild(a.cover(cat, e.id, e.name, 'a2-cov-s')); h.appendChild(el('span', 'a2-card-n', e.name)); c.appendChild(h);
          c.appendChild(el('span', 'a2-badge', e.sub || C.one));
          c.appendChild(el('span', 'a2-card-m', firstSentence(e.f.DESCRIZIONE, 110) || e.sintesi || ''));
          var meta = []; if (e.meta) { } else if (e.titles.length) meta.push(e.titles.length + (e.titles.length === 1 ? ' titolo' : ' titoli')); if (e.members.length) meta.push(e.members.length + ' membri con scheda');
          c.appendChild(el('span', 'a2-card-m a2-card-m2', e.meta || (meta.length ? meta.join(' · ') : (e.vuoto || 'Nessun titolo indicato'))));
          var bar = el('span', 'a2-bar'), fi = el('i'); fi.style.width = (e.titles.length ? Math.round(seenOf(e) / e.titles.length * 100) : 0) + '%'; bar.appendChild(fi); c.appendChild(bar);
          grid.appendChild(c);
        });
        if (!list.length) grid.appendChild(el('p', 'a2-empty', 'Nessuna scheda corrisponde ai filtri.'));
        res.appendChild(grid);
      }
      draw2();
    }

    /* ---------- schermata: dossier ---------- */
    var WHY = { nome: 'titolo indicato dalla guida', cronologia: 'confermato dalla cronologia', testo: 'citato nel testo della scheda', personaggio: 'confermato da un personaggio collegato' };
    function titleRow(tid, i, why) {
      var e = IDX.titoli[tid], c = e.li.querySelector('.watch-check, .anim-watch-check'), seen = !!(c && c.checked);
      var li = el('li'), b = btn('a2-row' + (seen ? ' seen' : ''), null); b.setAttribute('data-go', 'item:' + tid);
      b.appendChild(el('span', 'a2-row-n', String(i + 1)));
      var tx = el('span', 'a2-row-t'); tx.appendChild(el('b', '', e.title)); tx.appendChild(el('small', '', [a.tipoTitolo(e), a.anno(e), e.num ? 'N°' + VN(e.num) : '', why ? WHY[why] : ''].filter(Boolean).join(' · '))); b.appendChild(tx);
      b.appendChild(el('span', 'a2-row-s', seen ? '✓' : '○')); b.setAttribute('aria-label', e.title + (seen ? ', visto' : ', da vedere'));
      li.appendChild(b); return li;
    }
    function unconfBox(e) {
      if (!e.unconf || !e.unconf.length) return null;
      var d = D.createElement('details'); d.className = 'a2-unconf'; d.appendChild(el('summary', '', 'Riferimenti della guida non confermati (' + e.unconf.length + ')'));
      d.appendChild(el('p', 'a2-note', 'La guida indica questi numeri di scheda, ma il titolo che oggi porta quel numero non è confermato né dal testo della scheda né dai personaggi collegati (molti numeri derivano da una numerazione precedente, sfasata di 1). Non vengono trattati come collegamenti.'));
      var ul = el('ul', 'a2-unc-l'); e.unconf.forEach(function (tid) { ul.appendChild(el('li', '', '#' + tid.slice(5) + ' → ' + IDX.titoli[tid].title + ' (non confermato)')); }); d.appendChild(ul); return d;
    }
    function dl(pairs) { var d = el('dl', 'a2-dl'); pairs.forEach(function (p) { if (!p[1]) return; d.appendChild(el('dt', '', p[0])); d.appendChild(el('dd', '', p[1])); }); return d; }
    function renderDossier() {
      build(); var e = M.byId[ST.eid]; if (!e) { ST.screen = 'arch'; return renderArch(); }
      if (e.cat === 'cos' || e.cat === 'spe' || e.cat === 'mis') return renderDossier3(e);
      var C = CATS[e.cat]; body.className = 'a2-scroll a2-dossier a2-arc-' + e.cat; body.textContent = '';
      a.setTitle(e.name, C.n);
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, e.cat); hero.appendChild(a.cover(e.cat, e.id, e.name, 'a2-cov-hero'));
      hero.appendChild(el('span', 'a2-kick', (C.one + (e.sub && e.sub !== C.one ? ' · ' + e.sub : '')).toUpperCase())); hero.appendChild(el('h2', '', e.name));
      if (e.f.DESCRIZIONE) hero.appendChild(el('p', 'a2-descr', e.f.DESCRIZIONE));
      body.appendChild(hero);
      var rows = [];
      if (e.cat === 'org') rows = [['Fondata', e.f.FONDATA], ['Leader', e.f.LEADER], ['Scopo', e.f.SCOPO]];
      if (e.cat === 'evt') rows = [['Cause e conseguenze', e.f['CAUSE/CONSEG.']]];
      if (rows.some(function (r) { return r[1]; })) { var s0 = a.sec('Scheda'); s0.appendChild(dl(rows)); body.appendChild(s0); }
      if (e.cat === 'org') {
        var sm = a.sec('Membri e leader'); if (e.f.MEMBRI) sm.appendChild(dl([['Membri citati', e.f.MEMBRI]]));
        if (e.leader.length) { sm.appendChild(el('h4', 'a2-sub', 'Leader con scheda (' + e.leader.length + ')')); sm.appendChild(chipsBox(e.leader, charChip)); }
        if (e.members.length) { sm.appendChild(el('h4', 'a2-sub', 'Membri con scheda (' + e.members.length + ')')); sm.appendChild(chipsBox(e.members, charChip)); }
        if (!e.members.length && !e.leader.length) sm.appendChild(el('p', 'a2-empty', 'Nessun membro citato corrisponde a una scheda personaggio.'));
        else sm.appendChild(el('p', 'a2-note', 'Solo i nomi che corrispondono esattamente a una scheda sono collegati; gli altri restano testo della guida.'));
        body.appendChild(sm);
      }
      var st = a.sec(e.cat === 'evt' ? 'Titoli (in ordine della guida)' : 'Compare nei titoli (' + e.titles.length + ')'); st.classList.add('a2-sec-prim');
      if (e.titles.length) { var ol = el('ol', 'a2-list'); e.titles.forEach(function (t, i) { ol.appendChild(titleRow(t, i, e.why && e.why[t])); }); st.appendChild(ol); st.appendChild(el('p', 'a2-note', 'Solo i titoli verificati (indicati per nome, confermati dalla cronologia, citati nel testo o confermati da un personaggio collegato).' + (e.vago ? ' La guida accenna anche ad altri titoli («e successive») senza elencarli.' : ''))); }
      else st.appendChild(el('p', 'a2-empty', e.unconf && e.unconf.length ? 'Nessun titolo è confermato per questa scheda.' : 'La guida non indica titoli per questa scheda.'));
      var ub = unconfBox(e); if (ub) st.appendChild(ub);
      body.appendChild(st);
      if (e.unis.length) { var su = a.sec('Universi'); su.appendChild(chipsBox(e.unis, function (u) { return a.go('uni', u, UNI[u].nome); })); su.appendChild(el('p', 'a2-note', 'Universi dei titoli elencati sopra (dato derivato dai titoli, non una classificazione della guida).')); body.appendChild(su); }
      if (e.cited.length) { var sc = a.sec((e.cat === 'evt' ? 'Personaggi citati (partecipanti)' : 'Personaggi citati') + ' (' + e.cited.length + ')'); sc.appendChild(chipsBox(e.cited, charChip)); sc.appendChild(el('p', 'a2-note', 'Nomi che compaiono per esteso nel testo della scheda' + (e.cat === 'art' ? ' (anche i possessori)' : '') + '. La guida non li elenca in un campo dedicato.')); body.appendChild(sc); }
      var by = (M.citedBy[e.id] || []);
      if (e.arcs.length || by.length) {
        var sl = a.sec('Altre schede collegate');
        if (e.arcs.length) { sl.appendChild(el('h4', 'a2-sub', 'Citate in questa scheda')); sl.appendChild(chipsBox(e.arcs, arcChip)); }
        if (by.length) { sl.appendChild(el('h4', 'a2-sub', 'Che citano questa scheda')); sl.appendChild(chipsBox(by, arcChip)); }
        body.appendChild(sl);
      }
      var foot = el('section', 'a2-sec a2-foot');
      if (e.cat === 'art' && /^Gemma|^Guanto/.test(e.name)) foot.appendChild(btn('a2-primary', 'Apri il Reliquiario delle Gemme', function () { a.nav('reliquiario', { arc: 'art', eid: e.id }); }));
      body.appendChild(foot);
    }

    /* ---------- schermata: Reliquiario delle sei Gemme ---------- */
    function renderReliquiario() {
      build(); body.className = 'a2-scroll a2-dossier a2-arc-art a2-reliq'; body.textContent = '';
      a.setTitle('Reliquiario', 'Artefatti');
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, 'art'); hero.appendChild(a.art('gemma', 'a2-arc-ic')); hero.appendChild(el('span', 'a2-kick', 'ARTEFATTI · ESPERIENZA SPECIALE'));
      hero.appendChild(el('h2', '', 'Il Reliquiario delle sei Gemme')); hero.appendChild(el('p', '', 'Tocca una Gemma per leggerne la scheda, i titoli e i personaggi citati. Al centro, il Guanto dell’Infinito.'));
      body.appendChild(hero);
      var gems = []; Array.prototype.forEach.call(D.querySelectorAll('.stone-gem'), function (g) {
        var nm = (g.getAttribute('title') || '').toLowerCase(), ent = M.cat.art.filter(function (e) { return /^Gemma /.test(e.name) && e.name.toLowerCase().indexOf(nm) !== -1; })[0];
        if (nm && ent) gems.push({ e: ent, col: g.style.background || g.style.backgroundColor, lbl: g.getAttribute('title') });
      });
      var glove = M.cat.art.filter(function (e) { return /^Guanto/.test(e.name); })[0];
      var stage = el('div', 'a2-stage'), N = gems.length;
      var ring = D.createElementNS('http://www.w3.org/2000/svg', 'svg'); ring.setAttribute('viewBox', '0 0 100 100'); ring.setAttribute('class', 'a2-ring'); ring.setAttribute('aria-hidden', 'true');
      ring.innerHTML = '<circle cx="50" cy="50" r="36" fill="none" stroke="#D2B184" stroke-opacity=".45"/><circle cx="50" cy="50" r="22" fill="none" stroke="#D2B184" stroke-opacity=".25"/>';
      stage.appendChild(ring);
      var panel = el('section', 'a2-sec a2-rel-panel');
      function place(node, ang) { node.style.left = (50 + 36 * Math.cos(ang)) + '%'; node.style.top = (50 + 36 * Math.sin(ang)) + '%'; }
      gems.forEach(function (g, i) {
        var b = btn('a2-gem' + (ST.eid === g.e.id ? ' on' : ''), null, function () { ST.eid = g.e.id; Array.prototype.forEach.call(stage.querySelectorAll('.a2-gem,.a2-glove'), function (x) { x.classList.remove('on'); }); b.classList.add('on'); drawPanel(); });
        b.setAttribute('data-gem', g.e.id); b.setAttribute('aria-label', 'Gemma ' + g.lbl); var d = el('i'); d.style.background = g.col; b.appendChild(d); b.appendChild(el('span', '', g.lbl));
        place(b, -Math.PI / 2 + i * 2 * Math.PI / N); stage.appendChild(b);
      });
      if (glove) { var gb = btn('a2-glove' + (ST.eid === glove.id ? ' on' : ''), null, function () { ST.eid = glove.id; Array.prototype.forEach.call(stage.querySelectorAll('.a2-gem,.a2-glove'), function (x) { x.classList.remove('on'); }); gb.classList.add('on'); drawPanel(); }); gb.setAttribute('data-gem', glove.id); gb.setAttribute('aria-label', 'Guanto dell’Infinito'); gb.appendChild(a.art('gemma')); gb.appendChild(el('span', '', 'Guanto')); stage.appendChild(gb); }
      body.appendChild(stage); body.appendChild(panel);
      function drawPanel() {
        panel.textContent = ''; var e = M.byId[ST.eid];
        if (!e) { panel.appendChild(el('p', 'a2-empty', 'Seleziona una Gemma o il Guanto per aprirne la scheda.')); return; }
        panel.appendChild(el('h3', '', e.name)); if (e.f.DESCRIZIONE) panel.appendChild(el('p', 'a2-descr2', e.f.DESCRIZIONE));
        if (e.titles.length) { panel.appendChild(el('h4', 'a2-sub', 'Compare nei titoli · verificati (' + e.titles.length + ')')); var ol = el('ol', 'a2-list'); e.titles.forEach(function (t, i) { ol.appendChild(titleRow(t, i, e.why && e.why[t])); }); panel.appendChild(ol); }
        else panel.appendChild(el('p', 'a2-empty', 'Nessun titolo confermato.'));
        var ub = unconfBox(e); if (ub) panel.appendChild(ub);
        if (e.cited.length) { panel.appendChild(el('h4', 'a2-sub', 'Citati nel testo della guida (' + e.cited.length + ')')); panel.appendChild(chipsBox(e.cited, charChip)); panel.appendChild(el('p', 'a2-note', 'Nomi che compaiono nella scheda o nella cronologia delle Gemme: non indicano necessariamente chi la possiede.')); }
        if (e.arcs.length) { panel.appendChild(el('h4', 'a2-sub', 'Schede collegate')); panel.appendChild(chipsBox(e.arcs, arcChip)); }
        panel.appendChild(btn('a2-primary', 'Apri il dossier completo', function () { goArc('art', e.id); }));
      }
      drawPanel();
      var foot = el('section', 'a2-sec a2-foot');
      if (D.querySelector('#tvaArchivesOverlayEl [data-target="chrono-gemme-dell-infinito"]')) foot.appendChild(btn('a2-ghost', 'Cronologia delle Gemme (tutti i titoli)', function () { a.nav('chrono', { eid: 'chrono-gemme-dell-infinito' }); }));
      foot.appendChild(btn('a2-ghost', 'Tutti gli artefatti', function () { a.nav('arch', { arc: 'art', af: 'tutti', aq: '', au: 'tutti' }); }));
      body.appendChild(foot);
    }

    X.screens.arch = renderArch; X.screens.dossier = renderDossier; X.screens.reliquiario = renderReliquiario;
    X.label = function (s) {
      if (s.screen === 'arch' && CATS[s.arc]) return CATS[s.arc].n;
      if (s.screen === 'dossier') { var e = build().byId[s.eid]; return e ? short(e.name, 22) : 'Archivio'; }
      if (s.screen === 'reliquiario') return 'Reliquiario';
      return null;
    };
    X.search = function (q) {
      build(); return M.list.filter(function (e) { return e.name.toLowerCase().indexOf(q) !== -1; }).map(function (e) { return { cat: e.cat, id: e.id, name: e.name, catLbl: CATS[e.cat].one }; });
    };
    X.uniExtra = function (uid, sec) {
      build(); var ids = M.byUni[uid]; if (!ids || !ids.length) return null;
      var s = sec('Archivi nei suoi titoli (' + ids.length + ')');
      ['org', 'art', 'evt', 'luo'].forEach(function (cat) {
        var l = ids.filter(function (id) { return M.byId[id].cat === cat; }); if (!l.length) return;
        s.appendChild(el('h4', 'a2-sub', CATS[cat].n + ' (' + l.length + ')')); s.appendChild(chipsBox(l, function (id) { return arcChip(id, false); }, 10));
      });
      s.appendChild(el('p', 'a2-note', 'Schede d’archivio che compaiono in titoli di questo universo (derivato dai titoli: la guida non assegna le schede a un universo).'));
      return s;
    };

    /* ====================== FASE 3: Entità Cosmiche, Specie e Civiltà, Arti Mistiche, Potenza TVA ======================
       Nessun dato inventato: le voci sono lette dalle schede della guida. Le voci aggregate (Specie, Arti) esistono solo se citate in >= 3 schede
       e riportano soltanto frasi della guida con la scheda di provenienza; il tipo/la fascia sono classificazioni editoriali TVA dichiarate come tali. */
    var LIM_RE = /\blimit|vulnerab|\bdebol|non può|non è in grado|\bdipend|a costo|\bprezzo|corrom|incapace|\bmortal|proibit|solo se|soltanto se|sconfitt|imprigionat/i;
    var TXT_CH = ['POTERI', '📚 NEI FUMETTI', 'RELAZIONI'];
    var ONSCREEN = ['char-arishem', 'char-ego', 'char-galactus', 'char-knull', 'char-the-watcher', 'char-silver-surfer'];
    var SPE = [['spe-asgardiani', 'Asgardiani', 'Civiltà', /Asgardian|\bAsgard\b/i], ['spe-celestiali', 'Celestiali', 'Specie', /Celestial/i], ['spe-chitauri', 'Chitauri', 'Specie', /Chitauri/i],
      ['spe-deviants', 'Deviants', 'Specie', /Deviant/i], ['spe-eterni', 'Eterni', 'Specie', /\bEterni\b|\bEternals\b/i], ['spe-inumani', 'Inumani', 'Popolazione', /Inumani|Inhuman/i],
      ['spe-kree', 'Kree', 'Specie', /\bKree\b/i], ['spe-mutanti', 'Mutanti', 'Popolazione', /\bmutant/i], ['spe-simbionti', 'Simbionti', 'Specie', /simbio|symbio/i],
      ['spe-skrull', 'Skrull', 'Specie', /\bSkrull/i], ['spe-talokanil', 'Talokanil', 'Civiltà', /Talokan/i], ['spe-vampiri', 'Vampiri', 'Specie', /vampir/i],
      ['spe-wakandiani', 'Wakandiani', 'Civiltà', /Wakand/i], ['spe-xandariani', 'Xandariani', 'Civiltà', /Xandar/i]];
    var MIS = [['mis-stregoneria', 'Stregoneria e Arti Mistiche', 'Disciplina', /stregon|arti mistiche|Kamar-Taj|Sorcerer Supreme/i, 3],
      ['mis-magia-oscura', 'Magia oscura', 'Disciplina', /magia oscura|Darkhold|Chthon/i, 2],
      ['mis-magia-del-caos', 'Magia del caos', 'Disciplina', /magia del caos|chaos magic/i, 2]];
    // discipline cercate nella guida ma non (ancora) documentate a sufficienza: non diventano voci, compaiono come lacune dichiarate
    var MIS_GAPS = [['Magia runica', /magia runica|\brune\b|\brunic/i], ['Magia asgardiana (seidr)', /seidr|magia asgardian|magia di Asgard|Asgardian magic/i], ['Maestri delle Arti Mistiche', /Maestr[oi] delle Arti Mistiche|Master of the Mystic Arts/i]];
    var chF = {};
    function cf(cid) {
      if (!chF[cid]) { var f = {}; Array.prototype.forEach.call(IDX.personaggi[cid].li.querySelectorAll('.detail-row'), function (r) { if (r.classList.contains('tva-row')) return; var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v'); if (k && v) f[k.textContent.trim()] = v.textContent.trim(); }); chF[cid] = f; }
      return chF[cid];
    }
    function chTexts(cid) { var f = cf(cid); return TXT_CH.map(function (k) { return f[k] || ''; }).filter(Boolean); }
    function arTexts(e) { return Object.keys(e.f).filter(function (k) { return !SKIP[k]; }).map(function (k) { return e.f[k]; }); }
    function sents(t) { return t.split(/(?<=[.;!?])\s+/).map(function (x) { return x.trim(); }).filter(Boolean); }
    function pick(texts, re) { for (var i = 0; i < texts.length; i++) { var ss = sents(texts[i]); for (var j = 0; j < ss.length; j++) if (re.test(ss[j])) return ss[j].length > 230 ? ss[j].slice(0, 229) + '…' : ss[j]; } return null; }
    function slug(n) { return n.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
    function uniq(arr) { var o = []; arr.forEach(function (x) { if (o.indexOf(x) === -1) o.push(x); }); return o; }
    function finishTU(e) {
      e.titles = uniq(e.titles).filter(function (t) { return IDX.titoli[t]; }).sort(byGuide);
      var us = {}; e.titles.forEach(function (tid) { (IDX.titoli[tid].unis || []).forEach(function (u) { if (UNI[u]) us[u] = 1; }); }); e.unis = Object.keys(us);
      e.unis.forEach(function (u) { (M.byUni3[u] = M.byUni3[u] || []).push(e.id); });
    }
    function mk3(o) { return { id: o.id, cat: o.cat, pre: o.cat + '-', dbtab: null, name: o.name, sub: o.sub, f: o.f || {}, titles: o.titles || [], vago: false, unis: [], members: [], leader: [], cited: [], arcs: [], li: o.li || null, charId: o.charId || null, onscreen: !!o.onscreen, vuoto: o.vuoto, sintesi: o.sintesi, limiti: [], chars: [], byChars: [], byArcs: [], ex: [] }; }
    function add3(e) { M.list.push(e); M.byId[e.id] = e; M.cat[e.cat].push(e); }
    function build3() {
      M.byUni3 = {}; var chars = a.personaggiLista();
      // --- Entità Cosmiche: sullo schermo (la guida le descrive come Celestiale / entità / Osservatore / Araldo cosmico) ---
      ONSCREEN.forEach(function (cid) {
        var c = IDX.personaggi[cid]; if (!c) return; var f = cf(cid);
        var e = mk3({ id: 'cos-' + cid.slice(5), cat: 'cos', name: c.name, sub: 'Sullo schermo', li: c.li, charId: cid, onscreen: true, titles: (c.apps || []).slice(), f: { DESCRIZIONE: f['POTERI'] || '', 'NEI FUMETTI': f['📚 NEI FUMETTI'] || '', 'DA LEGGERE': f['📖 DA LEGGERE'] || '' } });
        finishTU(e);
        [['schermo', f['POTERI']], ['fumetti', f['📚 NEI FUMETTI']]].forEach(function (p) { if (p[1]) sents(p[1]).forEach(function (s) { if (LIM_RE.test(s)) e.limiti.push({ k: p[0], txt: s.length > 230 ? s.slice(0, 229) + '…' : s }); }); });
        add3(e);
      });
      D.querySelectorAll('.cosmic-card').forEach(function (cc) {
        var n = cc.querySelector('.cosmic-card-name'), d = cc.querySelector('.cosmic-card-desc'), t = cc.closest('.cosmic-tier'), tl = t && t.querySelector('.cosmic-tier-label'); if (!n || !d) return;
        var id = 'cos-' + slug(n.textContent); if (M.byId[id]) return;
        var e = mk3({ id: id, cat: 'cos', name: n.textContent.trim(), sub: tl ? tl.textContent.trim() : 'Mai apparse', onscreen: false, vuoto: 'Mai apparsa sullo schermo', f: { DESCRIZIONE: d.textContent.trim() } });
        finishTU(e); add3(e);
      });
      M.cat.cos.sort(function (p, q) { return (q.onscreen ? 1 : 0) - (p.onscreen ? 1 : 0) || (p.onscreen ? p.name.localeCompare(q.name, 'it') : 0); });
      // menzioni verso/da le altre schede (stessi nomi esatti, ambigui esclusi). I nomi delle entità «mai apparse» sono unici solo se non coincidono con altre schede.
      var never = M.cat.cos.filter(function (e) { return !e.onscreen; }), T3 = [], seen = {};
      var STOP3 = { Maestro: 1, Nova: 1 };
      never.forEach(function (e) { toks(e.name).forEach(function (t) { if (STOP3[t]) return; if (!M._index[t] && !seen[t]) { seen[t] = e.id; T3.push({ t: t, k: 'x:' + e.id, re: new RegExp('(?<![\\p{L}\\p{N}"])' + esc(t) + (t === 'Death' ? '(?! of\\b)' : '') + '(?![\\p{L}\\p{N}])', 'u') }); } else if (seen[t]) { seen[t] = null; } }); });
      T3 = T3.filter(function (x) { return seen[x.t]; });
      var ALL = M._TK.concat(T3);
      function scanAll(text, selfKey) {
        var hits = []; ALL.forEach(function (x) { var m = x.re.exec(text); if (m && x.k !== selfKey) hits.push({ s: m.index, e: m.index + x.t.length, k: x.k, l: x.t.length }); });
        hits.sort(function (p, q) { return q.l - p.l; }); var acc = [], keys = [];
        hits.forEach(function (h) { if (!acc.some(function (o) { return h.s < o.e && h.e > o.s; })) { acc.push(h); if (keys.indexOf(h.k) === -1) keys.push(h.k); } });
        return keys;
      }
      function pre(t) { return T3.some(function (x) { return t.indexOf(x.t) !== -1; }); }
      M.cat.cos.forEach(function (e) {
        var cit = {}, arc = {}, texts = e.charId ? chTexts(e.charId) : [e.f.DESCRIZIONE];
        texts.forEach(function (t) { scanAll(t, e.charId ? 'c:' + e.charId : 'x:' + e.id).forEach(function (k) { if (k[0] === 'c') cit[k.slice(2)] = 1; else if (k[0] === 'a') arc[k.slice(2)] = 1; }); });
        e.cited = Object.keys(cit); e.arcs = Object.keys(arc);
      });
      var byId = {}; never.forEach(function (e) { byId[e.id] = e; });
      chars.forEach(function (c) { chTexts(c.id).forEach(function (t) { if (!pre(t)) return; scanAll(t, 'c:' + c.id).forEach(function (k) { if (k[0] === 'x' && byId[k.slice(2)] && byId[k.slice(2)].byChars.indexOf(c.id) === -1) byId[k.slice(2)].byChars.push(c.id); }); }); });
      M.list.forEach(function (o) { if (o.cat === 'cos' || o.cat === 'spe' || o.cat === 'mis') return; arTexts(o).forEach(function (t) { if (!pre(t)) return; scanAll(t, 'a:' + o.id).forEach(function (k) { if (k[0] === 'x' && byId[k.slice(2)] && byId[k.slice(2)].byArcs.indexOf(o.id) === -1) byId[k.slice(2)].byArcs.push(o.id); }); }); });
      // --- Specie e Arti Mistiche: voci aggregate (>= 3 schede) ---
      var base = M.list.filter(function (o) { return o.cat === 'org' || o.cat === 'art' || o.cat === 'evt' || o.cat === 'luo'; });
      function aggregate(seed, cat) {
        var re = seed[3], e = mk3({ id: seed[0], cat: cat, name: seed[1], sub: seed[2] }), ts = [], exA = [], exC = [];
        base.forEach(function (o) { var tx = arTexts(o), s = pick(tx, re); if (s) { e.arcs.push(o.id); exA.push({ kind: 'a', id: o.id, txt: s }); ts = ts.concat(o.titles); } });
        chars.forEach(function (c) { var tx = chTexts(c.id), s = pick(tx, re); if (s) { e.chars.push(c.id); exC.push({ kind: 'c', id: c.id, txt: s }); ts = ts.concat(IDX.personaggi[c.id].apps || []); } });
        var need = seed[4] || 3; if (e.arcs.length + e.chars.length < need) return null; e.limited = (e.arcs.length + e.chars.length) < 3; e.re = re;
        e.ex = exA.concat(exC); e.titles = ts; finishTU(e);
        if (cat === 'mis') e.ex.forEach(function (x) { var tx = x.kind === 'a' ? arTexts(M.byId[x.id]) : chTexts(x.id); tx.forEach(function (t) { sents(t).forEach(function (s) { if (re.test(s) && LIM_RE.test(s) && !e.limiti.some(function (l) { return l.txt === s; })) e.limiti.push({ kind: x.kind, id: x.id, txt: s.length > 230 ? s.slice(0, 229) + '…' : s }); }); }); });
        e.sintesi = e.chars.length + (e.chars.length === 1 ? ' personaggio' : ' personaggi') + ' · ' + e.arcs.length + (e.arcs.length === 1 ? ' scheda d’archivio' : ' schede d’archivio') + ' che la citano' + (e.limited ? ' · dati limitati (solo ' + (e.arcs.length + e.chars.length) + ' schede)' : '');
        return e;
      }
      SPE.forEach(function (s) { var e = aggregate(s, 'spe'); if (e) add3(e); });
      MIS.forEach(function (s) { var e = aggregate(s, 'mis'); if (e) add3(e); });
      // lacune dichiarate: cosa è stato cercato e quante schede lo documentano davvero
      M.misGaps = MIS_GAPS.map(function (g) {
        var ids = []; base.forEach(function (o) { if (pick(arTexts(o), g[1])) ids.push(o.id); }); chars.forEach(function (c) { if (pick(chTexts(c.id), g[1])) ids.push(c.id); });
        var inStr = M.byId['mis-stregoneria'] ? ids.filter(function (id) { var st = M.byId['mis-stregoneria']; return st.arcs.indexOf(id) > -1 || st.chars.indexOf(id) > -1; }).length : 0;
        return { name: g[0], ids: ids, inStr: inStr };
      });
      M.cat.spe.sort(function (p, q) { return p.name.localeCompare(q.name, 'it'); });
      // collegamenti inversi verso le schede classiche dei personaggi
      M.list.forEach(function (e) {
        var who = e.cat === 'cos' ? (e.charId ? [e.charId] : []) : (e.cat === 'spe' || e.cat === 'mis' ? e.chars : []);
        who.forEach(function (cid) { (M.charExtra[cid] = M.charExtra[cid] || []).push(e.id); });
      });
    }
    function moreList(ol, n) { var items = Array.prototype.slice.call(ol.children); if (items.length <= n) return; items.forEach(function (li, i) { if (i >= n) li.hidden = true; }); var b = btn('a2-chip a2-moreb', '+' + (items.length - n) + ' altri titoli', function () { items.forEach(function (li) { li.hidden = false; }); b.remove(); }); ol.parentNode.insertBefore(b, ol.nextSibling); }
    function srcChip(x) { return x.kind === 'a' ? arcChip(x.id, false) : charChip(x.id); }
    function quotes(list, empty) {
      if (!list.length) return el('p', 'a2-empty', empty); var ul = el('ul', 'a2-ul a2-quotes');
      list.forEach(function (x) { var li = el('li'); li.appendChild(el('q', '', x.txt)); var s = el('span', 'a2-src'); s.appendChild(el('small', '', 'da: ')); s.appendChild(srcChip(x)); li.appendChild(s); ul.appendChild(li); });
      return ul;
    }
    function renderDossier3(e) {
      var C = CATS[e.cat]; body.className = 'a2-scroll a2-dossier a2-arc-' + e.cat; body.textContent = ''; a.setTitle(e.name, C.n);
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, e.cat); hero.appendChild(a.cover(e.cat, e.id, e.name, 'a2-cov-hero'));
      hero.appendChild(el('span', 'a2-kick', (e.cat === 'cos' ? 'ENTITÀ COSMICA · ' + e.sub : (C.one === e.sub ? e.sub : C.one + ' · ' + e.sub)).toUpperCase())); hero.appendChild(el('h2', '', e.name));
      var hp = e.cat === 'cos' ? (e.onscreen ? 'Versione dello schermo e versione dei fumetti sono tenute separate.' : 'Mai apparsa sullo schermo nei titoli di questa guida: scheda dai fumetti.') : e.sintesi + '.';
      hero.appendChild(el('p', 'a2-descr', hp)); body.appendChild(hero);
      if (e.cat === 'cos') {
        if (e.onscreen) {
          var s1 = a.sec('Sullo schermo (titoli della guida)'); s1.appendChild(el('p', 'a2-descr2', e.f.DESCRIZIONE || 'La guida non descrive i poteri.')); body.appendChild(s1);
          var s2 = a.sec('Nei fumetti'); s2.appendChild(el('p', 'a2-descr2', e.f['NEI FUMETTI'] || 'La guida non riporta la versione dei fumetti.')); s2.appendChild(el('p', 'a2-note', 'Versione fumettistica: non coincide necessariamente con quella cinematografica.')); if (e.f['DA LEGGERE']) s2.appendChild(dl([['Da leggere', e.f['DA LEGGERE']]])); body.appendChild(s2);
        } else {
          var s0 = a.sec('Solo nei fumetti'); s0.appendChild(dl([['Gruppo (secondo la guida)', e.sub], ['Natura e poteri', e.f.DESCRIZIONE]])); s0.appendChild(el('p', 'a2-note', 'Elencata dalla guida in «Chi manca ancora»: mai comparsa sullo schermo nei titoli coperti. Nessun universo dei titoli.')); body.appendChild(s0);
        }
        var sl = a.sec('Limiti documentati');
        if (e.limiti.length) { e.limiti.forEach(function (l) { sl.appendChild(el('p', 'a2-descr2', (l.k === 'fumetti' ? 'Fumetti: ' : 'Schermo: ') + l.txt)); }); }
        else sl.appendChild(el('p', 'a2-empty', 'La guida non documenta limiti specifici per questa entità.'));
        body.appendChild(sl);
      } else {
        if (e.cat === 'mis') {
          var sdf = a.sec('Definizione (dalla guida)'); if (e.ex.length) { var dfx = e.ex.filter(function (x) { return e.re && x.txt.search(e.re) >= 0 && x.txt.search(e.re) <= 3; })[0] || e.ex[0]; sdf.appendChild(quotes([dfx], '')); sdf.appendChild(el('p', 'a2-note', 'Formulazione della guida: nessuna definizione editoriale aggiunta.')); } else sdf.appendChild(el('p', 'a2-empty', 'La guida non offre una definizione.')); body.appendChild(sdf);
          if (e.limited) body.appendChild(el('p', 'a2-note a2-unconf', 'Dati limitati: la disciplina è citata solo in ' + (e.arcs.length + e.chars.length) + ' schede. Personaggi, titoli e artefatti mostrati sono solo quelli documentati.'));
        }
        var sg = a.sec('Cosa dice la guida (' + Math.min(e.ex.length, 8) + ' di ' + e.ex.length + ' schede)'); sg.classList.add('a2-sec-prim'); sg.appendChild(quotes(e.ex.slice(0, 8), 'Nessuna frase.')); sg.appendChild(el('p', 'a2-note', 'Frasi tratte dalle schede indicate. La guida non ha una scheda dedicata: origini e caratteristiche non descritte restano non documentate.')); body.appendChild(sg);
        var who = a.sec((e.cat === 'mis' ? 'Praticanti documentati' : 'Personaggi collegati') + ' (' + e.chars.length + ')');
        if (e.chars.length) { who.appendChild(chipsBox(e.chars, charChip)); who.appendChild(el('p', 'a2-note', 'Personaggi la cui scheda cita ' + (e.cat === 'mis' ? 'questa disciplina' : 'questa voce') + ' (nei poteri, nei fumetti o nelle relazioni).')); } else who.appendChild(el('p', 'a2-empty', 'Nessuna scheda personaggio la cita.'));
        body.appendChild(who);
        [['luo', e.cat === 'mis' ? 'Luoghi associati' : 'Mondi associati'], ['org', 'Organizzazioni'], ['evt', 'Eventi e conflitti'], ['art', 'Artefatti associati']].forEach(function (g) {
          var l = e.arcs.filter(function (id) { return M.byId[id].cat === g[0]; }); if (!l.length) { if (e.cat === 'mis' && g[0] === 'art') { var sn = a.sec('Artefatti associati (0)'); sn.appendChild(el('p', 'a2-empty', 'Nessun artefatto documentato dalla guida per questa disciplina.')); body.appendChild(sn); } return; } var s = a.sec(g[1] + ' (' + l.length + ')'); s.appendChild(chipsBox(l, arcChip)); body.appendChild(s);
        });
        if (e.cat === 'mis') { var sm = a.sec('Limiti e condizioni d’uso'); if (e.limiti.length) sm.appendChild(quotes(e.limiti.slice(0, 6), '')); else sm.appendChild(el('p', 'a2-empty', 'La guida non documenta limiti o condizioni specifici per questa disciplina.')); body.appendChild(sm); }
      }
      var st = a.sec(e.onscreen || e.cat !== 'cos' ? 'Apparizioni nei titoli (' + e.titles.length + ')' : 'Apparizioni nei titoli');
      if (e.titles.length) { var ol = el('ol', 'a2-list'); e.titles.forEach(function (t, i) { ol.appendChild(titleRow(t, i)); }); st.appendChild(ol); moreList(ol, 10); if (e.cat !== 'cos') st.appendChild(el('p', 'a2-note', 'Titoli delle schede che citano la voce (dato derivato).')); }
      else st.appendChild(el('p', 'a2-empty', e.cat === 'cos' ? 'Mai apparsa sullo schermo nei titoli di questa guida.' : 'Nessun titolo collegato.'));
      body.appendChild(st);
      if (e.unis.length) { var su = a.sec('Universo di riferimento'); su.appendChild(chipsBox(e.unis, function (u) { return a.go('uni', u, UNI[u].nome); })); su.appendChild(el('p', 'a2-note', 'Universi dei titoli elencati (dato derivato dai titoli).')); body.appendChild(su); }
      if (e.cat === 'cos') {
        if (e.cited.length) { var sc = a.sec('Personaggi collegati (' + e.cited.length + ')'); sc.appendChild(chipsBox(e.cited, charChip)); sc.appendChild(el('p', 'a2-note', 'Nomi che compaiono per esteso nel testo della scheda.')); body.appendChild(sc); }
        if (e.arcs.length) { var sa = a.sec('Eventi, artefatti e altre schede citate'); sa.appendChild(chipsBox(e.arcs, arcChip)); body.appendChild(sa); }
        if (e.byChars.length || e.byArcs.length) { var sb = a.sec('Citata da'); if (e.byChars.length) { sb.appendChild(el('h4', 'a2-sub', 'Personaggi')); sb.appendChild(chipsBox(e.byChars, charChip)); } if (e.byArcs.length) { sb.appendChild(el('h4', 'a2-sub', 'Altre schede')); sb.appendChild(chipsBox(e.byArcs, arcChip)); } body.appendChild(sb); }
      }
      var foot = el('section', 'a2-sec a2-foot');
      if (e.charId) { foot.appendChild(a.go('char', e.charId, 'Scheda personaggio completa')); if (pot().of[e.charId]) foot.appendChild(a.go('arc', 'pot:' + e.charId, 'Scheda di potenza TVA')); }
      body.appendChild(foot);
    }

    /* ---------- Potenza TVA ---------- */
    var POT = null;
    function pot() {
      if (POT) return POT; POT = { tiers: [], of: {} };
      D.querySelectorAll('#tvaArchivesOverlayEl .pyramid-tier').forEach(function (t) {
        var m = /pyramid-tier-(\d)/.exec(t.className), lab = t.querySelector('.pyramid-tier-label'); if (!m || !lab) return;
        var ic = (lab.querySelector('.pyramid-tier-icon') || {}).textContent || '', dd = (lab.querySelector('.pyramid-tier-desc') || {}).textContent || '';
        var nm = lab.textContent.replace(ic, '').replace(dd, '').replace('▸', '').replace(/^\s*\d+\s*·\s*/, '').trim(), dm = /^\(([\s\S]*)\)\s*—\s*\d+/.exec(dd.trim());
        var ids = []; t.querySelectorAll('.power-chip').forEach(function (c) { var mm = /'(char-[^']+)'/.exec(c.getAttribute('onclick') || ''); if (mm && IDX.personaggi[mm[1]]) ids.push(mm[1]); });
        var tier = { n: +m[1], name: nm, ic: ic.trim(), desc: dm ? dm[1] : dd, ids: ids }; POT.tiers.push(tier); ids.forEach(function (id) { POT.of[id] = tier; });
      });
      POT.tiers.sort(function (p, q) { return q.n - p.n; }); return POT;
    }
    function facts(cid) {
      var c = IDX.personaggi[cid], f = cf(cid), t = pot().of[cid], apps = uniq((c.apps || []).filter(function (x) { return IDX.titoli[x]; })).sort(byGuide), us = {};
      apps.forEach(function (x) { (IDX.titoli[x].unis || []).forEach(function (u) { if (UNI[u]) us[u] = 1; }); });
      var lim = []; [['schermo', f['POTERI']], ['fumetti', f['📚 NEI FUMETTI']]].forEach(function (p) { if (p[1]) sents(p[1]).forEach(function (s) { if (LIM_RE.test(s)) lim.push({ k: p[0], txt: s.length > 230 ? s.slice(0, 229) + '…' : s }); }); });
      var ev = (M.charCited[cid] || []).filter(function (id) { return M.byId[id] && (M.byId[id].cat === 'evt'); });
      return { id: cid, name: c.name, tier: t, pow: f['POTERI'] || '', fum: f['📚 NEI FUMETTI'] || '', apps: apps, unis: Object.keys(us), lim: lim, ev: ev, orgs: M.charOrg[cid] || [], extra: M.charExtra[cid] || [] };
    }
    var DISC = 'Le fasce sono valutazioni editoriali TVA su quanto mostrato sullo schermo, ancorate alla scala Marvel (Classe 1–100+): non sono classifiche ufficiali Marvel né fatti oggettivi come date o cast.';
    function renderPotenza() {
      build(); var P = pot(); body.className = 'a2-scroll a2-arc a2-arc-pot'; body.textContent = ''; a.setTitle('Potenza TVA', 'Archivio');
      var tot = 0; P.tiers.forEach(function (t) { tot += t.ids.length; });
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, 'pot'); hero.appendChild(a.art('poteri', 'a2-arc-ic')); hero.appendChild(el('span', 'a2-kick', 'IDENTITÀ E POTERE')); hero.appendChild(el('h2', '', 'Archivio della Potenza TVA'));
      hero.appendChild(el('p', '', tot + ' personaggi con poteri reali in ' + P.tiers.length + ' fasce. Capacità, apparizioni, limiti documentati e confronto tra due personaggi.')); body.appendChild(hero);
      body.appendChild(el('p', 'a2-note a2-arc-note a2-disc', DISC));
      body.appendChild(btn('a2-primary a2-rel-btn', 'Confronta due personaggi', function () { a.nav('confronto', { arc: 'pot', eid: '|', au: 'tutti', aq: '' }); }));
      body.appendChild(a.searchBox('a2PotSearch', ST.aq, function (v) { ST.aq = v; draw2(); }, 'Cerca un personaggio…'));
      var fl = el('div', 'a2-filters'); fl.setAttribute('role', 'group'); fl.setAttribute('aria-label', 'Filtra per fascia');
      [['tutti', 'Tutte ' + tot]].concat(P.tiers.map(function (t) { return [String(t.n), t.ic + ' ' + t.n + ' · ' + t.name + ' ' + t.ids.length]; })).forEach(function (p) {
        var b = btn('a2-f' + (ST.af === p[0] ? ' on' : ''), p[1], function () { ST.af = p[0]; Array.prototype.forEach.call(fl.children, function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('on'); b.setAttribute('aria-pressed', 'true'); draw2(); }); b.setAttribute('aria-pressed', ST.af === p[0] ? 'true' : 'false'); fl.appendChild(b);
      });
      body.appendChild(fl); var res = el('div', 'a2-gridwrap'); body.appendChild(res);
      function draw2() {
        res.textContent = ''; var q = ST.aq.trim().toLowerCase(), n = 0;
        P.tiers.forEach(function (t) {
          if (ST.af !== 'tutti' && ST.af !== String(t.n)) return;
          var ids = t.ids.filter(function (id) { return !q || IDX.personaggi[id].name.toLowerCase().indexOf(q) !== -1; }); if (!ids.length) return;
          var h = el('div', 'a2-tier-h'); h.appendChild(el('b', '', t.ic + ' Fascia ' + t.n + ' · ' + t.name)); h.appendChild(el('small', '', t.desc)); res.appendChild(h);
          var ul = el('ul', 'a2-list a2-list-pot');
          ids.forEach(function (id) {
            var li = el('li'), b = btn('a2-row', null, function () { a.nav('potscheda', { arc: 'pot', eid: id }); }); b.setAttribute('data-pot', id); b.insertBefore(a.cover('pot', id, IDX.personaggi[id].name, 'a2-cov-s', t.n), b.firstChild); var tx = el('span', 'a2-row-t'); tx.appendChild(el('b', '', IDX.personaggi[id].name)); tx.appendChild(el('small', '', firstSentence(cf(id)['POTERI'], 96))); b.appendChild(tx); li.appendChild(b); ul.appendChild(li); n++;
          });
          res.appendChild(ul);
        });
        if (!n) res.appendChild(el('p', 'a2-empty', 'Nessun personaggio corrisponde ai filtri.'));
      }
      draw2();
    }
    function renderPotScheda() {
      build(); var cid = ST.eid, P = pot(); if (!cid || !P.of[cid]) { ST.screen = 'potenza'; return renderPotenza(); }
      var f = facts(cid), t = f.tier; body.className = 'a2-scroll a2-dossier a2-arc-pot'; body.textContent = ''; a.setTitle(f.name, 'Potenza TVA');
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, 'pot'); hero.appendChild(a.cover('pot', cid, f.name, 'a2-cov-hero', t.n)); hero.appendChild(el('span', 'a2-kick', ('Fascia ' + t.n + ' · ' + t.name).toUpperCase())); hero.appendChild(el('h2', '', f.name)); hero.appendChild(el('p', 'a2-descr', t.desc)); body.appendChild(hero);
      body.appendChild(el('p', 'a2-note a2-arc-note a2-disc', DISC));
      var s1 = a.sec('Capacità principali (schermo)'); s1.appendChild(el('p', 'a2-descr2', f.pow || 'La guida non descrive i poteri.')); body.appendChild(s1);
      var s2 = a.sec('Nei fumetti'); s2.appendChild(el('p', 'a2-descr2', f.fum || 'La guida non riporta la versione dei fumetti.')); s2.appendChild(el('p', 'a2-note', 'Versione a parte: non coincide necessariamente con quella dello schermo.')); body.appendChild(s2);
      var s3 = a.sec('Imprese e apparizioni'); s3.classList.add('a2-sec-prim');
      if (f.apps.length) { var ol = el('ol', 'a2-list'); f.apps.forEach(function (x, i) { ol.appendChild(titleRow(x, i)); }); s3.appendChild(ol); moreList(ol, 8); } else s3.appendChild(el('p', 'a2-empty', 'Nessun titolo indicato dalla guida.'));
      if (f.ev.length) { s3.appendChild(el('h4', 'a2-sub', 'Eventi e Battaglie che citano il personaggio')); s3.appendChild(chipsBox(f.ev, arcChip)); s3.appendChild(el('p', 'a2-note', 'Il nome compare per esteso nel testo di queste schede.')); }
      body.appendChild(s3);
      var s4 = a.sec('Limiti e vulnerabilità documentati');
      if (f.lim.length) { f.lim.forEach(function (l) { s4.appendChild(el('p', 'a2-descr2', (l.k === 'fumetti' ? 'Fumetti: ' : 'Schermo: ') + l.txt)); }); } else s4.appendChild(el('p', 'a2-empty', 'La guida non documenta limiti o vulnerabilità per questo personaggio: non vanno presupposti.'));
      body.appendChild(s4);
      var s5 = a.sec('Collegamenti'); s5.appendChild(a.go('char', cid, 'Scheda personaggio completa'));
      if (f.orgs.length) { s5.appendChild(el('h4', 'a2-sub', 'Organizzazioni')); s5.appendChild(chipsBox(f.orgs, arcChip)); }
      if (f.extra.length) { s5.appendChild(el('h4', 'a2-sub', 'Entità, specie e arti')); s5.appendChild(chipsBox(f.extra, arcChip)); }
      if (f.unis.length) { s5.appendChild(el('h4', 'a2-sub', 'Universi')); s5.appendChild(chipsBox(f.unis, function (u) { return a.go('uni', u, UNI[u].nome); })); }
      body.appendChild(s5);
      var foot = el('section', 'a2-sec a2-foot'); foot.appendChild(btn('a2-primary', 'Confronta con un altro personaggio', function () { a.nav('confronto', { arc: 'pot', eid: cid + '|', au: 'B', aq: '' }); })); body.appendChild(foot);
    }
    function renderConfronto() {
      build(); var P = pot(), ids = (ST.eid || '|').split('|'), S = { A: ids[0] || '', B: ids[1] || '' };
      body.className = 'a2-scroll a2-dossier a2-arc-pot a2-cmp'; body.textContent = ''; a.setTitle('Confronto', 'Potenza TVA');
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, 'pot'); hero.appendChild(a.art('poteri', 'a2-arc-ic')); hero.appendChild(el('span', 'a2-kick', 'POTENZA TVA')); hero.appendChild(el('h2', '', 'Confronto tra due personaggi'));
      hero.appendChild(el('p', '', 'Mette accanto capacità, imprese, limiti e incertezze. Non indica un vincitore.')); body.appendChild(hero);
      body.appendChild(el('p', 'a2-note a2-arc-note a2-disc', DISC));
      var slots = el('div', 'a2-slots'); body.appendChild(slots);
      function setSlot(k, id) { S[k] = id; ST.eid = S.A + '|' + S.B; ST.au = 'tutti'; ST.aq = ''; a.draw(); }
      ['A', 'B'].forEach(function (k) {
        var box = el('div', 'a2-slot' + (ST.au === k ? ' on' : '')); box.appendChild(el('small', '', 'Personaggio ' + k));
        var nm = S[k] && P.of[S[k]] ? IDX.personaggi[S[k]].name : 'Da scegliere'; box.appendChild(el('b', '', nm));
        if (S[k] && P.of[S[k]]) box.appendChild(el('span', 'a2-badge', 'Fascia ' + P.of[S[k]].n + ' · ' + P.of[S[k]].name));
        box.appendChild(btn('a2-ghost a2-slot-b', S[k] ? 'Cambia' : 'Scegli', function () { ST.au = ST.au === k ? 'tutti' : k; ST.aq = ''; a.draw(); })); slots.appendChild(box);
      });
      if (ST.au === 'A' || ST.au === 'B') {
        var slot = ST.au, other = S[slot === 'A' ? 'B' : 'A'], pick2 = el('div', 'a2-picker'), lst = el('div', 'a2-gridwrap');
        pick2.appendChild(a.searchBox('a2CmpSearch', ST.aq, function (v) { ST.aq = v; dr(); }, 'Cerca nelle ' + Object.keys(P.of).length + ' schede…')); pick2.appendChild(lst); body.appendChild(pick2);
        var dr = function () {
          lst.textContent = ''; var q = ST.aq.trim().toLowerCase(), ul = el('ul', 'a2-list a2-list-pot'), n = 0;
          P.tiers.forEach(function (t) { t.ids.forEach(function (id) { if (id === other || n >= 40) return; if (q && IDX.personaggi[id].name.toLowerCase().indexOf(q) === -1) return; n++; var li = el('li'), b = btn('a2-row', null, function () { setSlot(slot, id); }); b.setAttribute('data-pick', id); var tx = el('span', 'a2-row-t'); tx.appendChild(el('b', '', IDX.personaggi[id].name)); tx.appendChild(el('small', '', 'Fascia ' + t.n + ' · ' + t.name)); b.appendChild(tx); li.appendChild(b); ul.appendChild(li); }); });
          lst.appendChild(ul); if (!n) lst.appendChild(el('p', 'a2-empty', 'Nessun personaggio corrisponde.')); else if (n >= 40) lst.appendChild(el('p', 'a2-note', 'Primi 40 risultati: continua a digitare per restringere.'));
        }; dr();
      }
      if (!(P.of[S.A] && P.of[S.B])) { body.appendChild(el('p', 'a2-empty', 'Scegli due personaggi per vedere il confronto.')); return; }
      var A = facts(S.A), B = facts(S.B);
      function two(title, fa, fb, note) {
        var s = a.sec(title), g = el('div', 'a2-cmp-g');
        [[A, fa], [B, fb]].forEach(function (p) { var c = el('div', 'a2-cmp-c'); c.appendChild(el('b', '', p[0].name)); if (typeof p[1] === 'string') c.appendChild(el('p', p[1] ? 'a2-descr2' : 'a2-empty', p[1] || 'Non documentato dalla guida.')); else c.appendChild(p[1]); g.appendChild(c); });
        s.appendChild(g); if (note) s.appendChild(el('p', 'a2-note', note)); body.appendChild(s);
      }
      two('Fascia TVA (valutazione editoriale)', 'Fascia ' + A.tier.n + ' · ' + A.tier.name + ' — ' + A.tier.desc, 'Fascia ' + B.tier.n + ' · ' + B.tier.name + ' — ' + B.tier.desc);
      two('Capacità principali (schermo)', A.pow, B.pow);
      two('Nei fumetti (versione a parte)', A.fum, B.fum, 'Le versioni dei fumetti non sono fuse con quelle dello schermo.');
      function imp(f) { var d = el('div'); d.appendChild(el('p', 'a2-descr2', f.apps.length + (f.apps.length === 1 ? ' titolo' : ' titoli') + ' nella guida' + (f.ev.length ? ' · ' + f.ev.length + ' tra eventi e battaglie che lo citano' : '') + '.')); if (f.ev.length) d.appendChild(chipsBox(f.ev, arcChip, 6)); return d; }
      two('Imprese documentate', imp(A), imp(B));
      function lim(f) { if (!f.lim.length) return ''; var d = el('div'); f.lim.forEach(function (l) { d.appendChild(el('p', 'a2-descr2', (l.k === 'fumetti' ? 'Fumetti: ' : 'Schermo: ') + l.txt)); }); return d; }
      two('Limiti e vulnerabilità documentati', lim(A), lim(B), 'Un limite non documentato non significa assenza di limiti.');
      var common = A.apps.filter(function (x) { return B.apps.indexOf(x) !== -1; });
      var sc = a.sec('Titoli in comune (' + common.length + ')');
      if (common.length) { var ol = el('ol', 'a2-list'); common.forEach(function (x, i) { ol.appendChild(titleRow(x, i)); }); sc.appendChild(ol); moreList(ol, 6); sc.appendChild(el('p', 'a2-note', 'Comparire nello stesso titolo non significa che i due si affrontino.')); }
      else sc.appendChild(el('p', 'a2-empty', 'Nessun titolo in comune: la guida non documenta incontri tra i due sullo schermo.'));
      body.appendChild(sc);
      var rd = a.sec('Lettura TVA'); rd.classList.add('a2-sec-prim'); var ul = el('ul', 'a2-ul');
      var dn = Math.abs(A.tier.n - B.tier.n);
      ul.appendChild(el('li', '', dn === 0 ? 'Stessa fascia (' + A.tier.n + '): la classificazione non distingue i due personaggi.' : (A.tier.n > B.tier.n ? A.name : B.name) + ' è in una fascia più alta (' + Math.max(A.tier.n, B.tier.n) + ' contro ' + Math.min(A.tier.n, B.tier.n) + '): indica la scala di potenza mostrata sullo schermo, non l’esito di uno scontro.'));
      ul.appendChild(el('li', '', 'Nessun risultato ipotetico: la guida non documenta un confronto o uno scontro diretto tra i due' + (common.length ? ' (compaiono insieme in ' + common.length + (common.length === 1 ? ' titolo' : ' titoli') + ').' : '.')));
      var unk = []; if (!A.lim.length) unk.push(A.name); if (!B.lim.length) unk.push(B.name);
      ul.appendChild(el('li', '', 'Incertezze: ' + (unk.length ? 'limiti non documentati per ' + unk.join(' e ') + '; ' : '') + 'equipaggiamento, alleati, contesto e versioni (schermo/fumetti) non sono valutati dalla fascia.'));
      rd.appendChild(ul); body.appendChild(rd);
      var foot = el('section', 'a2-sec a2-foot'); foot.appendChild(a.go('arc', 'pot:' + S.A, 'Scheda di ' + A.name)); foot.appendChild(a.go('arc', 'pot:' + S.B, 'Scheda di ' + B.name)); body.appendChild(foot);
    }
    var prevOpen = A.openArc;
    A.openArc = function (cat, id, fromRouter) {
      if (cat === 'pot') { if (!IDX.personaggi[id] || !pot().of[id]) return false; if (!fromRouter && a.tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante'); ST.screen = 'potscheda'; ST.arc = 'pot'; ST.eid = id; if (!a.tog.checked) a.show(); a.draw(); a.setScroll(0); return true; }
      return prevOpen(cat, id, fromRouter);
    };
    A.potTier = function (cid) { var t = pot().of[cid]; return t ? t.n : null; };
    X.screens.potenza = renderPotenza; X.screens.potscheda = renderPotScheda; X.screens.confronto = renderConfronto;
    var prevLabel = X.label;
    X.label = function (s) {
      if (s.screen === 'potenza') return 'Potenza TVA'; if (s.screen === 'potscheda') { var t = IDX.personaggi[s.eid]; return t ? short(t.name, 22) : 'Potenza TVA'; } if (s.screen === 'confronto') return 'Confronto';
      return prevLabel ? prevLabel(s) : null;
    };

    /* ---------- collegamenti inversi nelle schede classiche (titoli e personaggi) ---------- */
    function rowEl(k) { var r = el('div', 'detail-row tva-row'); r.appendChild(el('span', 'detail-k', k)); var v = el('span', 'detail-v tva-chips'); r.appendChild(v); return { r: r, v: v }; }
    function tchip(label, goTo, extra) { var b = el('button', 'tva-chip'); b.type = 'button'; b.setAttribute('data-go', goTo); b.appendChild(el('span', 'tva-chip-t', label)); if (extra) b.appendChild(el('small', '', extra)); return b; }
    function injectBack() {
      build();
      Object.keys(M.byTitle).forEach(function (tid) {
        var li = IDX.titoli[tid] && IDX.titoli[tid].li, panel = li && li.querySelector('.detail-panel'); if (!panel || li.getAttribute('data-tva-arc')) return;
        li.setAttribute('data-tva-arc', '1');
        var r = rowEl('ARCHIVI COLLEGATI (ATLANTE)');
        M.byTitle[tid].forEach(function (id) { var e = M.byId[id]; r.v.appendChild(tchip(e.name, 'arc:' + e.cat + ':' + id, CATS[e.cat].one)); });
        r.v.appendChild(el('div', 'tva-note', 'Schede di Organizzazioni, Artefatti, Eventi e Luoghi che elencano questo titolo.'));
        panel.appendChild(r.r);
      });
      Object.keys(IDX.personaggi).forEach(function (cid) {
        var li3 = IDX.personaggi[cid].li, p3 = li3 && li3.querySelector('.detail-panel'); if (p3 && !li3.getAttribute('data-tva-arc3')) {
          var tt = A.potTier(cid), ex3 = M.charExtra[cid];
          if (tt || (ex3 && ex3.length)) {
            li3.setAttribute('data-tva-arc3', '1');
            if (ex3 && ex3.length) { var r3 = rowEl('ENTITÀ, SPECIE E ARTI (ATLANTE)'); ex3.forEach(function (id) { r3.v.appendChild(tchip(M.byId[id].name, 'arc:' + M.byId[id].cat + ':' + id, CATS[M.byId[id].cat].one)); }); r3.v.appendChild(el('div', 'tva-note', 'Voci che citano o descrivono questo personaggio.')); p3.appendChild(r3.r); }
            if (tt) { var r4 = rowEl('POTENZA TVA (ATLANTE)'); r4.v.appendChild(tchip('Scheda di potenza', 'arc:pot:' + cid, 'fascia ' + tt)); r4.v.appendChild(el('div', 'tva-note', 'Valutazione editoriale TVA, non una classifica ufficiale Marvel.')); p3.appendChild(r4.r); }
          }
        }
        var li = IDX.personaggi[cid].li, panel = li && li.querySelector('.detail-panel'); if (!panel || li.getAttribute('data-tva-arc')) return;
        var o = M.charOrg[cid], c = M.charCited[cid]; if (!(o && o.length) && !(c && c.length)) return;
        li.setAttribute('data-tva-arc', '1');
        if (o && o.length) { var r1 = rowEl('ORGANIZZAZIONI (ATLANTE)'); o.forEach(function (id) { r1.v.appendChild(tchip(M.byId[id].name, 'arc:org:' + id, M.byId[id].leader.indexOf(cid) !== -1 ? 'leader' : 'membro')); }); r1.v.appendChild(el('div', 'tva-note', 'Citato tra i membri o i leader nella scheda dell’organizzazione.')); panel.appendChild(r1.r); }
        if (c && c.length) { var r2 = rowEl('CITATO IN (ATLANTE)'); c.forEach(function (id) { var e = M.byId[id]; r2.v.appendChild(tchip(e.name, 'arc:' + e.cat + ':' + id, CATS[e.cat].one)); }); r2.v.appendChild(el('div', 'tva-note', 'Il nome compare per esteso nel testo di queste schede.')); panel.appendChild(r2.r); }
      });
    }
    A.arcModel = function () { return build(); };
    var kick = function () { try { injectBack(); } catch (eI) { if (W.console) console.error('TVA Archives - collegamenti inversi:', eI); } };
    if (W.requestIdleCallback) W.requestIdleCallback(kick, { timeout: 1500 }); else setTimeout(kick, 400);
  } catch (eAr) { if (window.console) console.error('Marvel guide - TVA Archives (archivi):', eAr); }
})();
