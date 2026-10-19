    /* ==== CRON3C:BEGIN — FASE 3C: Cronologie del Multiverso ====
       Esperienza di sola lettura costruita sul modello condiviso tvaUniverse + indice tvaIdx + dati Timeline (marvelGetAltTimelineData).
       Non scrive nulla (progressi, XP, localStorage, «La mia timeline»): lo stato UI vive in ST.cr e nello stack di navigazione. */
    var CR_FUT = '2026-01-01';          // dalle uscite da questa data in poi la guida non permette di dedurre l'avvenuta uscita senza un marcatore esplicito
    var CR_MESI = ['gen', 'feb', 'mar', 'apr', 'mag', 'giu', 'lug', 'ago', 'set', 'ott', 'nov', 'dic'];
    var CR_MESI_L = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
    var CR_BINS = [['b0', '< 1950', function (y) { return y < 1950; }], ['b1', '1950–1999', function (y) { return y >= 1950 && y < 2000; }], ['b2', '2000–2009', function (y) { return y >= 2000 && y < 2010; }],
      ['b3', '2010–2019', function (y) { return y >= 2010 && y < 2020; }], ['b4', '2020–2029', function (y) { return y >= 2020 && y < 2030; }], ['b5', '2030 e oltre', function (y) { return y >= 2030; }], ['bn', 'Senza data', null]];
    var CR_STATE = { 'prev-uff': 'Prevista · data ufficiale', 'prev-ann': 'Prevista · annunciata', 'prev-ver': 'Prevista · da verificare' };
    var CR_TIPO = { film: 'Film', serie: 'Serie', speciale: 'Speciale', animazione: 'Animazione' };
    var CRD = null, CRS = null;
    function crFmtY(y) { return y < 0 ? (-y) + ' a.C.' : String(y); }
    function crFmtDate(iso) { var p = String(iso || '').split('-'); if (p.length < 3) return iso || ''; return (+p[2]) + ' ' + CR_MESI[+p[1] - 1] + ' ' + p[0]; }
    function crNorm(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
    function crCut(s, n) { s = String(s || '').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n - 1).replace(/[\s,;(]+$/, '') + '…' : s; }
    function crPlural(n, one, many) { return n + ' ' + (n === 1 ? one : many); }

    /* ---- livello dati: una voce per titolo, quattro informazioni temporali sempre separate ---- */
    function crData() {
      if (CRD) return CRD;
      var OP = {}, ALT = {}, sagas = [];
      try { var atl = JSON.parse((D.getElementById('atlasData') || {}).textContent || '{}'); (atl.opere || []).forEach(function (o) { OP[o.id] = o; }); } catch (e1) {}
      try { (W.marvelGetAltTimelineData() || []).forEach(function (a, i) { var k = ('000' + a.num).slice(-3); ALT[k] = { saga: a.saga || null, idx: i }; if (a.saga && sagas.indexOf(a.saga) === -1) sagas.push(a.saga); }); } catch (e2) {}
      var E = {}, order = [], seq = 0;
      Object.keys(IDX.titoli).forEach(function (id) {
        var t = IDX.titoli[id]; if (t.kind !== 'item' && t.kind !== 'anim') return;   // le altre voci (p4-…) non fanno parte del modello 3A
        var e = { id: id, kind: t.kind, num: t.num, title: t.title, variant: !!t.variant, li: t.li, seq: seq++ };
        e.unis = (t.unis || []).filter(function (o) { return UNI[o]; });
        if (t.kind === 'item') {
          var op = OP[t.num] || {}, u = (UM.uscita(t.num) || {}), raw = UM.ambientazione(t.num) || '', ya = raw ? UM.annoAmbientazione(raw) : { y: null, approx: false };
          var mv = /^[\s\u2713\u2606]*N°(\d+)/.exec(t.li.textContent || ''); e.vn = mv ? mv[1] : null;   // numero VISIBILE della scheda (posizionale; l'ID resta quello originale)
          var al = ALT[t.num]; e.tipo = op.tipo || null; e.ruolo = op.ruolo || null; e.saga = al ? al.saga : null; e.gi = al ? al.idx : 5000 + e.seq;
          var head = (t.li.textContent || '').slice(0, 260), stg = t.li.querySelector('.status-tag'), st = null, iso = u.data || null;
          if (stg && /status-confermato/.test(stg.className)) st = 'prev-uff'; else if (stg && /status-annunciato/.test(stg.className)) st = 'prev-ann';
          else if (/già uscita/i.test(head)) st = 'uscito'; else if (iso && iso >= CR_FUT) st = 'prev-ver'; else if (iso) st = 'uscito';
          var rk = null, y0 = null; if (iso) { var p = iso.split('-'); y0 = +p[0]; rk = y0 * 12 + (+p[1] - 1) + (+p[2]) / 32; }
          e.rel = { iso: iso, prec: u.precisione || null, state: st, y0: y0, y1: y0, rk: rk, raw: null };
          var y = ya.y === undefined ? null : ya.y, lab = '';
          if (y !== null) { var rg = /(-?\d{3,4})\s*[-–]\s*(\d{2,4})/.exec(raw); lab = ya.approx && rg ? rg[1] + '–' + rg[2] : (ya.approx ? '~' : '') + crFmtY(y); }
          e.set = { raw: raw, y: y, approx: !!(ya.approx && y !== null), kind: y === null ? 'assente' : (ya.approx ? 'approssimata' : 'certa'), lab: lab };
        } else {
          var am = ''; Array.prototype.forEach.call(t.li.querySelectorAll('.detail-row'), function (r) { var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v'); if (k && v && /^AMBIENTAZIONE/i.test(k.textContent.trim())) am = v.textContent.replace(/\s+/g, ' ').trim(); });
          var ys = am.match(/\b(?:19|20)\d\d\b/g) || [], yy0 = ys.length ? +ys[0] : null, open = /in conclusione|in corso|annunciat/i.test(am), yy1 = ys.length ? (open ? null : +ys[ys.length - 1]) : null, mm = 0;
          var low = am.toLowerCase(); for (var q = 0; q < 12; q++) { var ix = low.indexOf(CR_MESI_L[q]); if (ix !== -1 && (!mm || ix < mm.ix)) mm = { ix: ix, m: q }; }
          e.tipo = 'animazione'; e.ruolo = null; e.saga = null; e.gi = 5000 + e.seq;
          e.rel = { iso: null, prec: yy0 ? 'periodo' : null, state: 'uscito', y0: yy0, y1: yy1, rk: yy0 === null ? null : yy0 * 12 + (mm ? mm.m : 0), raw: am };
          e.set = { raw: '', y: null, approx: false, kind: 'assente', lab: '', na: true };   // la serie animata non ha un'ambientazione datata: il periodo è di MESSA IN ONDA
        }
        E[id] = e; order.push(id);
      });
      CRD = { E: E, order: order, sagas: sagas, OP: OP };
      return CRD;
    }
    function crUniList(uid) { var D0 = crData(); return UM.get(uid).titoli.map(function (t) { return D0.E[t.id]; }).filter(Boolean); }
    function crCov(list) {
      var c = { n: list.length, amb: 0, ap: 0, rel: 0, prev: 0, anim: 0 };
      list.forEach(function (e) { if (e.set.y !== null) { c.amb++; if (e.set.approx) c.ap++; } if (e.rel.rk !== null) c.rel++; if (/^prev/.test(e.rel.state || '')) c.prev++; if (e.kind === 'anim') c.anim++; });
      return c;
    }
    function crKey(e, ord) { if (ord === 'ambientazione') return e.set.y; if (ord === 'uscita') return e.rel.rk; return null; }
    function crSort(list, ord) {
      var a = list.slice(), cmpG = function (x, y) { return x.gi - y.gi; };
      if (ord === 'az') { a.sort(function (x, y) { return crNorm(x.title).localeCompare(crNorm(y.title)) || cmpG(x, y); }); return { lista: a, senza: [] }; }
      if (ord === 'guida') { a.sort(cmpG); return { lista: a, senza: [] }; }
      var has = [], no = []; a.forEach(function (e) { (crKey(e, ord) === null ? no : has).push(e); });
      has.sort(function (x, y) { return crKey(x, ord) - crKey(y, ord) || cmpG(x, y); }); no.sort(cmpG); return { lista: has, senza: no };
    }
    function crAvail(cov) { return { ambientazione: cov.amb >= 2, uscita: cov.rel >= 2, guida: true }; }
    function crDefOrd(av) { return av.ambientazione ? 'ambientazione' : av.uscita ? 'uscita' : 'guida'; }
    function crRelLab(e) {
      var r = e.rel; if (r.iso) return String(r.y0); if (r.y0 === null) return '—';
      if (r.y1 === null || r.y1 === r.y0) return String(r.y0); var s = String(r.y1); return r.y0 + '–' + (String(r.y0).slice(0, 2) === s.slice(0, 2) ? s.slice(2) : s);
    }
    function crRelTxt(e) {
      var r = e.rel; if (r.iso) return 'Uscita: ' + crFmtDate(r.iso) + (r.state && /^prev/.test(r.state) ? ' (prevista)' : '');
      if (r.raw) return 'In onda: ' + crCut(r.raw, 58); return 'Uscita: data non disponibile';
    }
    function crSetTxt(e) {
      if (e.kind === 'anim') return ''; var s = e.set;
      if (s.y !== null) return 'Ambientazione: ' + crCut(s.raw, 64); if (s.raw) return 'Ambientazione: ' + crCut(s.raw, 50) + ' (senza anno)'; return 'Ambientazione: informazione non disponibile';
    }
    function crSeen(e) { var c = e.li && e.li.querySelector('.watch-check, .anim-watch-check'); return !!(c && c.checked); }
    function crShort(uid) { return IDX.breve ? IDX.breve(uid) : (UNI[uid] ? UNI[uid].nome : uid); }

    /* ---- stato (nello snapshot di navigazione: tornando da dossier/mappa/scheda si ritrova tutto) ---- */
    function crFresh() {
      var fox = (UM.ids().filter(function (i) { return /10005/.test(i); })[0]) || UM.ids()[1];
      return { mode: 'uni', uid: MCU, ord: null, und: false, lim: 40, pA: MCU, pB: fox, pm: 'uscita', ps: 'A', q: '', fu: [], fb: 'amb', fp: [], fs: [], ft: [], fr: false, xo: 'uscita', xl: 30, na: false };
    }
    function crSnap() { try { return JSON.parse(JSON.stringify(ST.cr || crFresh())); } catch (e) { return crFresh(); } }
    function crOpen(mode, extra) {
      if (tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante');
      var c = crFresh(); c.mode = mode || 'uni'; if (extra) Object.keys(extra).forEach(function (k) { c[k] = extra[k]; });
      ST.cr = c; ST.screen = 'cron'; ST.uid = null; if (!tog.checked) show(); draw(); setScroll(0);
    }
    function crRedraw(keep) { var y = body.scrollTop; draw(); if (keep) body.scrollTop = y; }

    /* ---- bottom-sheet accessibile (Esc, backdrop, focus gestito) ---- */
    function crCloseSheet(ret) {
      if (!CRS) return; var s = CRS; CRS = null; if (s.ov.parentNode) s.ov.parentNode.removeChild(s.ov);
      if (ret !== false && s.op && D.body.contains(s.op)) try { s.op.focus(); } catch (e) {}
    }
    function crSheet(title, build, opener) {
      crCloseSheet(false);
      var ov = el('div', 'cr-ov'), sh = el('div', 'cr-sheet'); sh.setAttribute('role', 'dialog'); sh.setAttribute('aria-modal', 'true'); sh.setAttribute('aria-label', title);
      var hd = el('div', 'cr-sh-h'); hd.appendChild(el('b', '', title)); var x = btn('cr-x', '✕', function () { crCloseSheet(); }); x.setAttribute('aria-label', 'Chiudi'); hd.appendChild(x);
      var bd = el('div', 'cr-sh-b'); sh.appendChild(el('div', 'cr-grab')); sh.appendChild(hd); sh.appendChild(bd); ov.appendChild(sh);
      ov.addEventListener('click', function (e) { if (e.target === ov) crCloseSheet(); });
      sh.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') { e.stopPropagation(); crCloseSheet(); return; }
        if (e.key === 'Tab') { var f = sh.querySelectorAll('button:not([disabled]),input,[tabindex="0"]'); if (!f.length) return; var a = f[0], z = f[f.length - 1]; if (e.shiftKey && D.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && D.activeElement === z) { e.preventDefault(); a.focus(); } }
      });
      body.appendChild(ov); CRS = { ov: ov, op: opener || null, bd: bd, sh: sh }; build(bd);
      var f0 = sh.querySelector('.cr-opt.on, .cr-opt, button:not(.cr-x)') || x; try { f0.focus({ preventScroll: true }); } catch (e3) {}
      return CRS;
    }
    function crPickUni(title, cur, excl, onPick, opener) {
      crSheet(title, function (bd) {
        var ul = el('ul', 'cr-pick');
        UM.ids().forEach(function (u) {
          var n = UM.get(u).titoli.length, li = el('li'), b = btn('cr-opt' + (u === cur ? ' on' : ''), null, function () { crCloseSheet(false); onPick(u); });
          b.appendChild(el('span', 'cr-opt-n', UNI[u].nome)); b.appendChild(el('small', '', n ? crPlural(n, 'titolo', 'titoli') : 'nessun titolo associato'));
          if (u === excl) { b.disabled = true; b.appendChild(el('small', 'cr-opt-x', 'già scelto nell’altra corsia')); }
          b.setAttribute('aria-pressed', u === cur ? 'true' : 'false'); li.appendChild(b); ul.appendChild(li);
        });
        bd.appendChild(ul);
      }, opener);
    }

    /* ---- elementi comuni ---- */
    function crTag(cls, txt) { return el('span', 'cr-tag ' + cls, txt); }
    function crTags(e, ord, ctx) {
      var t = el('div', 'cr-tags');
      if (e.kind === 'item') {
        if (ord === 'ambientazione' || ord === 'az' || ord === 'exp-a') t.appendChild(e.set.kind === 'certa' ? crTag('c', 'anno certo') : e.set.kind === 'approssimata' ? crTag('a', 'approssimativo') : crTag('n', 'senza anno'));
      } else t.appendChild(crTag('n', 'periodo di messa in onda'));
      if (ord === 'uscita' && e.kind === 'item') t.appendChild(e.rel.iso ? crTag('c', 'data certa') : crTag('n', 'data non disponibile'));
      if (CR_STATE[e.rel.state]) t.appendChild(crTag('p', CR_STATE[e.rel.state]));
      if (e.variant) t.appendChild(crTag('n', 'variante'));
      if (ctx && ctx.key) t.appendChild(crTag('k', '★ evento chiave'));
      if (ctx && ctx.cross) t.appendChild(crTag('x', 'crossover'));
      return t.childNodes.length ? t : null;
    }
    function crTitle(e) {
      var b = btn('cr-t', null); b.setAttribute('data-go', 'item:' + e.id);
      if (e.vn) b.appendChild(el('span', 'cr-n', 'N°' + e.vn)); b.appendChild(el('span', 'cr-tt', e.title));
      b.setAttribute('aria-label', e.title + (e.vn ? ', N°' + e.vn : '') + '. Apri la scheda'); return b;
    }
    function crUniBtns(uid, cls) {
      var r = el('div', 'cr-links ' + (cls || ''));
      var b1 = btn('cr-lk', 'Dossier', function () { openUni(uid); }); b1.setAttribute('aria-label', 'Apri il dossier di ' + UNI[uid].nome);
      var b2 = btn('cr-lk', '◎ Mappa', function () { openMappa(uid); }); b2.setAttribute('aria-label', 'Mostra ' + UNI[uid].nome + ' sulla mappa del Multiverso');
      r.appendChild(b1); r.appendChild(b2); return r;
    }
    function crSeg(items, cur, onPick, label) {
      var s = el('div', 'cr-seg'); s.setAttribute('role', 'group'); s.setAttribute('aria-label', label);
      items.forEach(function (o) { var b = btn('cr-sg' + (cur === o[0] ? ' on' : ''), o[1], function () { if (!b.disabled) onPick(o[0]); }); b.setAttribute('aria-pressed', cur === o[0] ? 'true' : 'false'); if (o[2]) { b.disabled = true; b.title = o[2]; b.setAttribute('aria-label', o[1] + ' — non disponibile: ' + o[2]); } s.appendChild(b); });
      return s;
    }
    function crLegend() {
      var d = D.createElement('details'); d.className = 'a2-legend cr-leg'; d.appendChild(el('summary', '', 'Come si leggono le date'));
      var dl = el('dl');
      [['● Anno certo', 'riportato come anno unico nella scheda.'], ['◌ Approssimativo', 'intervallo o data incerta (es. «2013-14»): mostrato come tale.'], ['◇ Senza data', 'la guida non indica un anno: il titolo resta nell’elenco «senza data».'],
       ['◍ Prevista', 'uscita non ancora confermata come avvenuta: ufficiale, annunciata o da verificare.'], ['★ Evento chiave', 'solo dove il dossier dell’universo lo documenta.'],
       ['Uscita ≠ ambientazione', 'l’anno di uscita è reale; l’ambientazione è quella della storia. Sono separati e non si convertono.']].forEach(function (r) { dl.appendChild(el('dt', '', r[0])); dl.appendChild(el('dd', '', r[1])); });
      d.appendChild(dl); return d;
    }
    function crTabs(C) {
      var t = el('div', 'cr-tabs'); t.setAttribute('role', 'tablist'); t.setAttribute('aria-label', 'Modalità delle Cronologie');
      [['uni', 'Universo'], ['par', 'Parallele'], ['exp', 'Esplora']].forEach(function (o) {
        var b = btn('cr-tab' + (C.mode === o[0] ? ' on' : ''), o[1], function () { if (C.mode === o[0]) return; C.mode = o[0]; C.lim = 40; crCloseSheet(false); draw(); setScroll(0); });
        b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', C.mode === o[0] ? 'true' : 'false'); b.id = 'crTab-' + o[0]; t.appendChild(b);
      });
      return t;
    }

    /* ---- MODALITÀ 1: cronologia di un universo ---- */
    function crBanner(cov, ord, nSenza) {
      var p = el('p', 'cr-note');
      if (ord === 'ambientazione') p.textContent = 'Ordinati per anno di ambientazione riportato nella scheda: ' + cov.amb + ' con anno' + (cov.ap ? ' (' + cov.ap + ' approssimativi)' : '') + ', ' + nSenza + ' senza anno in fondo. Non è una cronologia canonica.';
      else if (ord === 'uscita') p.textContent = 'Ordinati per data di uscita reale: ' + cov.rel + ' con data' + (nSenza ? ', ' + nSenza + ' senza data in fondo' : '') + (cov.prev ? ' · ' + cov.prev + ' previste (non confermate come avvenute)' : '') + '. La data di uscita non indica quando si svolge la storia.';
      else p.textContent = 'Sequenza editoriale della guida (N°): è l’ordine consigliato per la visione, non una cronologia.' + (cov.amb < 2 && cov.rel < 2 ? ' Per questo universo i dati non bastano per un ordine temporale.' : '');
      return p;
    }
    function crEvent(e, ord, m, ctxKey) {
      var li = el('li', 'cr-ev' + (crSeen(e) ? ' seen' : '')), lab, sub = '', nd = 'n';
      if (ord === 'ambientazione') { lab = e.set.lab || '—'; nd = e.set.kind === 'certa' ? 'c' : e.set.kind === 'approssimata' ? 'a' : 'n'; }
      else if (ord === 'uscita') { lab = crRelLab(e); nd = /^prev/.test(e.rel.state || '') ? 'p' : e.rel.iso ? 'c' : e.rel.rk !== null ? 'a' : 'n'; if (e.rel.iso) sub = CR_MESI[+e.rel.iso.split('-')[1] - 1]; }
      else { lab = e.vn ? 'N°' + e.vn : 'AN'; nd = 'e'; }
      var key = !!ctxKey; if (key) nd += ' k';
      var yl = el('div', 'cr-yr'); yl.appendChild(el('b', '', lab)); if (sub) yl.appendChild(el('small', '', sub)); li.appendChild(yl);
      var dot = el('span', 'cr-nd cr-nd-' + nd.replace(' ', ' cr-nd-')); dot.setAttribute('aria-hidden', 'true'); li.appendChild(dot);
      var cd = el('div', 'cr-cd' + (key ? ' key' : '')); cd.appendChild(crTitle(e));
      var l1 = crSetTxt(e), l2 = crRelTxt(e), first = ord === 'uscita' ? [l2, l1] : [l1, l2];
      first.forEach(function (tx, i) { if (tx) cd.appendChild(el('div', 'cr-m' + (i ? ' sec' : ''), tx)); });
      var cross = e.unis.length > 1, tg = crTags(e, ord, { key: key, cross: cross }); if (tg) cd.appendChild(tg);
      if (cross) { var oth = e.unis.filter(function (o) { return o !== m.uid; }).map(crShort); if (oth.length) cd.appendChild(el('div', 'cr-m sec', '↗ anche in: ' + oth.join(', '))); }
      if (crSeen(e)) cd.appendChild(el('span', 'cr-seen', '✓ visto'));
      li.appendChild(cd); return li;
    }
    function crTimeline(parent, uid, C) {
      var m = UM.get(uid), mm = { uid: uid }, list = crUniList(uid), cov = crCov(list), nm = UNI[uid].nome;
      var head = el('div', 'cr-uhead'); head.appendChild(el('h3', '', nm));
      head.appendChild(el('p', 'cr-sub', list.length ? crPlural(list.length, 'titolo', 'titoli') + (m.crossover.length ? ' (' + m.appartenenza.length + ' propri + ' + m.crossover.length + ' crossover)' : '') + ' associati dai dati della guida' : 'Nessun titolo associato nei dati della guida'));
      head.appendChild(crUniBtns(uid)); parent.appendChild(head);
      if (!list.length) {
        var em = el('div', 'cr-empty'); em.appendChild(el('b', '', 'Nessuna cronologia disponibile'));
        em.appendChild(el('p', '', 'Per questo universo la guida non associa titoli, quindi non c’è nulla da ordinare nel tempo. Non vengono inventati eventi o date: il dossier mostra cosa è documentato (personaggi, collegamenti).'));
        parent.appendChild(em); return;
      }
      var av = crAvail(cov), ord = C.ord && av[C.ord] ? C.ord : crDefOrd(av);
      var motivo = function (k) { return k === 'ambientazione' ? 'meno di 2 titoli con anno di ambientazione' : 'meno di 2 titoli con data di uscita'; };
      parent.appendChild(crSeg([['ambientazione', 'Ambientazione', av.ambientazione ? null : motivo('ambientazione')], ['uscita', 'Uscita', av.uscita ? null : motivo('uscita')], ['guida', 'Guida']], ord, function (k) { C.ord = k; C.lim = 40; crRedraw(true); }, 'Ordine dei titoli'));
      var s = crSort(list, ord); parent.appendChild(crBanner(cov, ord, s.senza.length));
      parent.appendChild(crLegend());
      var keys = (m.eventiChiave || []).map(crNorm), ol = el('ol', 'cr-tl'); ol.setAttribute('aria-label', 'Titoli di ' + nm + ' in ordine ' + (ord === 'guida' ? 'editoriale' : ord === 'uscita' ? 'di uscita' : 'di ambientazione'));
      var shown = s.lista.slice(0, C.lim), prev = null, prevE = null;
      shown.forEach(function (e) {
        var k = crKey(e, ord);
        if (prev !== null && k !== null && ord !== 'guida' && (ord === 'uscita' || (e.set.kind === 'certa' && prevE.set.kind === 'certa'))) { var d = ord === 'uscita' ? (k - prev) / 12 : k - prev; if (d >= 15) { var g = el('li', 'cr-gap'); g.setAttribute('aria-hidden', 'true'); g.appendChild(el('span', '', '⋮ ' + (ord === 'uscita' ? Math.floor(prev / 12) + ' → ' + Math.floor(k / 12) + ' · nessuna uscita nell’intervallo' : crFmtY(prev) + ' → ' + crFmtY(k) + ' · nessun titolo datato nell’intervallo'))); ol.appendChild(g); } }
        if (k !== null) { prev = k; prevE = e; }
        ol.appendChild(crEvent(e, ord, mm, keys.indexOf(crNorm(e.title)) !== -1));
      });
      parent.appendChild(ol);
      if (s.lista.length > C.lim) { var mo = btn('cr-more', 'Mostra altri ' + Math.min(40, s.lista.length - C.lim) + ' · restano ' + (s.lista.length - C.lim), function () { C.lim += 40; crRedraw(true); }); mo.id = 'crMore'; parent.appendChild(mo); }
      if (s.senza.length) {
        var bl = ord === 'ambientazione' ? 'Senza anno di ambientazione' : 'Senza data di uscita';
        var bb = btn('cr-band', null, function () { C.und = !C.und; crRedraw(true); }); bb.id = 'crBand'; bb.setAttribute('aria-expanded', C.und ? 'true' : 'false');
        bb.appendChild(el('span', '', bl + ' · ' + s.senza.length)); bb.appendChild(el('span', 'cr-band-c', C.und ? 'Nascondi ▴' : 'Mostra ▾')); parent.appendChild(bb);
        if (C.und) { var ol2 = el('ol', 'cr-tl cr-tl-n'); s.senza.slice(0, 120).forEach(function (e) { ol2.appendChild(crEvent(e, 'guida', mm, keys.indexOf(crNorm(e.title)) !== -1)); }); parent.appendChild(ol2); parent.appendChild(el('p', 'cr-note', 'In questo blocco i titoli seguono l’ordine editoriale della guida (N°): non indicano una successione temporale.')); }
      }
    }
    function crUni(main, C) {
      if (!UNI[C.uid]) C.uid = MCU;
      var row = el('div', 'cr-pickrow'), pb = btn('cr-sel', null, function () { crPickUni('Scegli l’universo', C.uid, null, function (u) { C.uid = u; C.ord = null; C.lim = 40; C.und = false; crRedraw(false); setScroll(0); }, pb); });
      pb.id = 'crUniSel'; pb.appendChild(el('span', 'cr-sel-k', 'Universo')); pb.appendChild(el('span', 'cr-sel-v', UNI[C.uid].nome)); pb.appendChild(el('span', 'cr-sel-c', '▾')); pb.setAttribute('aria-haspopup', 'dialog');
      row.appendChild(pb); main.appendChild(row); crTimeline(main, C.uid, C);
    }

    /* ---- MODALITÀ 2: cronologie parallele (nessuna corrispondenza temporale inventata) ---- */
    function crRange(vals, fmt) { if (!vals.length) return 'non disponibile'; var a = Math.min.apply(0, vals), b = Math.max.apply(0, vals); return a === b ? fmt(a) : fmt(a) + ' → ' + fmt(b); }
    function crSummary(A, B, uA, uB) {
      var t = D.createElement('table'); t.className = 'cr-cmp'; var cap = D.createElement('caption'); cap.className = 'cr-vh'; cap.textContent = 'Confronto fra i due universi'; t.appendChild(cap);
      var cA = crCov(A), cB = crCov(B), shared = A.filter(function (e) { return B.indexOf(e) !== -1; }).length;
      var hr = D.createElement('tr'); ['', 'A · ' + crShort(uA), 'B · ' + crShort(uB)].forEach(function (x, i) { var h = D.createElement('th'); h.scope = i ? 'col' : 'row'; h.textContent = x; if (i) h.className = i === 1 ? 'a' : 'b'; hr.appendChild(h); }); t.appendChild(hr);
      var ry = function (L) { return crRange(L.filter(function (e) { return e.rel.y0 !== null; }).map(function (e) { return e.rel.y0; }), String); };
      var ra = function (L) { return crRange(L.filter(function (e) { return e.set.y !== null; }).map(function (e) { return e.set.y; }), crFmtY); };
      [['Titoli', String(A.length), String(B.length)], ['Uscite', ry(A), ry(B)], ['Ambientazione', ra(A) + (cA.amb ? ' (' + cA.amb + ' con anno)' : ''), ra(B) + (cB.amb ? ' (' + cB.amb + ' con anno)' : '')],
       ['Previste', String(cA.prev), String(cB.prev)]].forEach(function (r) { var tr = D.createElement('tr'); r.forEach(function (x, i) { var c = D.createElement(i ? 'td' : 'th'); if (!i) c.scope = 'row'; c.textContent = x; tr.appendChild(c); }); t.appendChild(tr); });
      var w = el('div', 'cr-cmpw'); w.appendChild(t); if (shared) w.appendChild(el('p', 'cr-note', 'Titoli presenti in entrambe: ' + shared + '.')); return w;
    }
    function crLinks(uA, uB) {
      var box = el('div', 'cr-lkbox'), ls = UM.links().filter(function (l) { return (l.a === uA && l.b === uB) || (l.a === uB && l.b === uA); });
      if (!ls.length) { box.appendChild(el('p', 'cr-note', 'Nessun collegamento documentato tra questi due universi nei dati della guida: il confronto mostra solo il periodo e i titoli di ciascuno.')); return box; }
      ls.forEach(function (l) {
        var r = el('div', 'cr-lkrow'); r.appendChild(el('span', 'cr-lk-h', 'Collegamento nei dati della guida:')); r.appendChild(udBadge(l.stato)); box.appendChild(r);
        var ch = l.titoli && l.titoli.length ? udTitoliChips(l.titoli) : null; if (ch) { box.appendChild(el('span', 'cr-lk-t', 'Titoli citati:')); box.appendChild(ch); }
      });
      box.appendChild(el('p', 'cr-note cr-warn', 'Un collegamento tra universi non indica che gli eventi siano contemporanei né che le due linee si svolgano nello stesso periodo.')); return box;
    }
    function crLaneCard(e, side) {
      var d = el('div', 'cr-lc cr-lc-' + side + (crSeen(e) ? ' seen' : '')); d.appendChild(crTitle(e));
      d.appendChild(el('div', 'cr-m', e.rel.iso ? crFmtDate(e.rel.iso) : (e.rel.raw ? crCut(e.rel.raw, 34) : 'data non disponibile')));
      if (CR_STATE[e.rel.state]) d.appendChild(crTag('p', CR_STATE[e.rel.state])); return d;
    }
    function crPar(main, C) {
      if (!UNI[C.pA]) C.pA = MCU; if (!UNI[C.pB] || C.pB === C.pA) C.pB = UM.ids().filter(function (u) { return u !== C.pA; })[0];
      var uA = C.pA, uB = C.pB, A = crUniList(uA), B = crUniList(uB), pk = el('div', 'cr-pickrow cr-pk2');
      var ba = btn('cr-sel cr-sel-a', null, function () { crPickUni('Universo A', uA, uB, function (u) { C.pA = u; C.lim = 40; crRedraw(true); }, ba); }), bb = btn('cr-sel cr-sel-b', null, function () { crPickUni('Universo B', uB, uA, function (u) { C.pB = u; C.lim = 40; crRedraw(true); }, bb); });
      [[ba, 'A', uA], [bb, 'B', uB]].forEach(function (x) { x[0].appendChild(el('span', 'cr-sel-k', x[1])); x[0].appendChild(el('span', 'cr-sel-v', crShort(x[2]))); x[0].appendChild(el('span', 'cr-sel-c', '▾')); x[0].setAttribute('aria-haspopup', 'dialog'); x[0].setAttribute('aria-label', 'Universo ' + x[1] + ': ' + UNI[x[2]].nome + '. Cambia'); });
      ba.id = 'crSelA'; bb.id = 'crSelB';
      var sw = btn('cr-swap', '⇄', function () { var t = C.pA; C.pA = C.pB; C.pB = t; crRedraw(true); }); sw.id = 'crSwap'; sw.setAttribute('aria-label', 'Scambia A e B');
      pk.appendChild(ba); pk.appendChild(sw); pk.appendChild(bb); main.appendChild(pk);
      main.appendChild(crSeg([['uscita', 'Corsie · uscita'], ['proprie', 'Corsie proprie'], ['ab', 'A | B']], C.pm, function (k) { C.pm = k; C.lim = 40; crRedraw(false); }, 'Modalità di confronto'));
      main.appendChild(crSummary(A, B, uA, uB)); main.appendChild(crLinks(uA, uB));
      var nt = el('p', 'cr-note cr-axis');
      nt.textContent = C.pm === 'uscita' ? 'Asse comune = anno di uscita (data reale, uguale per tutti). Le corsie non indicano contemporaneità narrativa né ambientazione.'
        : C.pm === 'proprie' ? 'Due sequenze indipendenti: nessun allineamento tra le colonne. Ogni colonna usa il proprio ordine (ambientazione, uscita o guida, in base ai dati disponibili).' : 'Una corsia alla volta, con la stessa lettura della cronologia di un universo.';
      main.appendChild(nt);
      if (C.pm === 'uscita') {
        var M = {}; A.forEach(function (e) { M[e.id] = { e: e, a: 1 }; }); B.forEach(function (e) { (M[e.id] || (M[e.id] = { e: e })).b = 1; });
        var rows = Object.keys(M).map(function (k) { return M[k]; }), has = rows.filter(function (r) { return r.e.rel.rk !== null; }), no = rows.filter(function (r) { return r.e.rel.rk === null; });
        has.sort(function (x, y) { return x.e.rel.rk - y.e.rel.rk || x.e.gi - y.e.gi; }); no.sort(function (x, y) { return x.e.gi - y.e.gi; });
        if (!rows.length) { main.appendChild(el('div', 'cr-empty', 'Nessun titolo associato a nessuno dei due universi.')); return; }
        var lh = el('div', 'cr-lh'); lh.appendChild(el('span', 'cr-lh-a', 'A · ' + crShort(uA))); lh.appendChild(el('span', 'cr-lh-m', 'uscita')); lh.appendChild(el('span', 'cr-lh-b', 'B · ' + crShort(uB))); main.appendChild(lh);
        var ol = el('ol', 'cr-lanes'), py = null;
        function lrow(r, showY) {
          var li = el('li', 'cr-lr ' + (r.a && r.b ? 'ab' : r.a ? 'a' : 'b')), mid = el('span', 'cr-ly'); mid.setAttribute('aria-hidden', 'true'); if (showY) mid.textContent = crRelLab(r.e); li.appendChild(mid);
          if (r.a && r.b) { var c = crLaneCard(r.e, 'ab'); c.insertBefore(el('span', 'cr-both', 'In entrambe le corsie'), c.firstChild); li.appendChild(c); }
          else li.appendChild(crLaneCard(r.e, r.a ? 'a' : 'b'));
          li.setAttribute('aria-label', (r.a && r.b ? 'Entrambi gli universi' : r.a ? 'Universo A' : 'Universo B') + ': ' + r.e.title); return li;
        }
        has.slice(0, C.lim).forEach(function (r) { var yl = crRelLab(r.e), same = (yl === py); py = yl; ol.appendChild(lrow(r, !same)); });
        main.appendChild(ol);
        if (has.length > C.lim) { var mo = btn('cr-more', 'Mostra altri ' + Math.min(40, has.length - C.lim) + ' · restano ' + (has.length - C.lim), function () { C.lim += 40; crRedraw(true); }); mo.id = 'crMore'; main.appendChild(mo); }
        if (no.length) {
          var nb = btn('cr-band', null, function () { C.und = !C.und; crRedraw(true); }); nb.id = 'crBand'; nb.setAttribute('aria-expanded', C.und ? 'true' : 'false'); nb.appendChild(el('span', '', 'Senza data di uscita · ' + no.length)); nb.appendChild(el('span', 'cr-band-c', C.und ? 'Nascondi ▴' : 'Mostra ▾')); main.appendChild(nb);
          if (C.und) { var o2 = el('ol', 'cr-lanes'); no.forEach(function (r) { o2.appendChild(lrow(r, false)); }); main.appendChild(o2); }
        }
      } else if (C.pm === 'proprie') {
        var cols = el('div', 'cr-cols');
        [[uA, 'a', A], [uB, 'b', B]].forEach(function (x) {
          var col = el('section', 'cr-col cr-col-' + x[1]), cov = crCov(x[2]), av = crAvail(cov), ord = crDefOrd(av);
          col.appendChild(el('h4', '', (x[1].toUpperCase()) + ' · ' + crShort(x[0]))); col.appendChild(el('p', 'cr-sub', x[2].length ? 'Ordine: ' + (ord === 'ambientazione' ? 'ambientazione' : ord === 'uscita' ? 'uscita' : 'guida (editoriale)') : 'Nessun titolo associato'));
          var s = crSort(x[2], ord), ul = el('ol', 'cr-colist');
          s.lista.slice(0, C.lim).concat(ord === 'guida' ? [] : s.senza.slice(0, 5)).forEach(function (e) {
            var li = el('li', 'cr-lc cr-lc-' + x[1]); li.appendChild(crTitle(e)); var sk = e.rel.iso ? crFmtDate(e.rel.iso) : crRelLab(e);
            li.appendChild(el('div', 'cr-m', ord === 'ambientazione' ? (e.set.y !== null ? 'Amb. ' + e.set.lab : 'senza anno') : ord === 'uscita' ? 'Uscita ' + sk : (e.vn ? 'N°' + e.vn : 'guida'))); if (CR_STATE[e.rel.state]) li.appendChild(crTag('p', CR_STATE[e.rel.state])); ul.appendChild(li);
          });
          col.appendChild(ul); if (s.lista.length > C.lim || s.senza.length > 5) col.appendChild(el('p', 'cr-note', 'Elenco abbreviato: apri «A | B» per la cronologia completa.')); col.appendChild(crUniBtns(x[0], 'cr-links-c')); cols.appendChild(col);
        });
        main.appendChild(cols);
      } else {
        main.appendChild(crSeg([['A', 'A · ' + crShort(uA)], ['B', 'B · ' + crShort(uB)]], C.ps, function (k) { C.ps = k; C.ord = null; C.lim = 40; C.und = false; crRedraw(true); }, 'Quale universo mostrare'));
        crTimeline(main, C.ps === 'B' ? uB : uA, C);
      }
    }

    /* ---- MODALITÀ 3: esploratore temporale ---- */
    function crFilterN(C) { return (C.fu.length ? 1 : 0) + (C.fp.length ? 1 : 0) + (C.fs.length ? 1 : 0) + (C.ft.length ? 1 : 0) + (C.fr ? 1 : 0); }
    function crMatch(C) {
      var d = crData(), q = crNorm(C.q).trim(), out = [];
      d.order.forEach(function (id) {
        var e = d.E[id];
        if (q && crNorm(e.title).indexOf(q) === -1 && (e.vn ? ('n' + e.vn + ' ' + e.vn).indexOf(q.replace('°', '')) === -1 : true)) return;
        if (C.fu.length && !(e.unis.length ? e.unis.some(function (u) { return C.fu.indexOf(u) !== -1; }) : C.fu.indexOf('_na') !== -1)) return;
        if (C.ft.length && C.ft.indexOf(e.tipo) === -1) return;
        if (C.fs.length && C.fs.indexOf(e.saga) === -1) return;
        if (C.fr && !/^prev/.test(e.rel.state || '')) return;
        if (C.fp.length) { var y = C.fb === 'amb' ? e.set.y : e.rel.y0, ok = C.fp.some(function (b) { if (b === 'bn') return y === null; var B0 = CR_BINS.filter(function (x) { return x[0] === b; })[0]; return y !== null && B0[2](y); }); if (!ok) return; }
        out.push(e);
      });
      return out;
    }
    function crResRow(e, ord) {
      var li = el('li', 'cr-res' + (crSeen(e) ? ' seen' : '')); li.appendChild(crTitle(e));
      var l1 = crSetTxt(e), l2 = crRelTxt(e), ln = ord === 'uscita' ? [l2, l1] : [l1, l2]; ln.forEach(function (tx, i) { if (tx) li.appendChild(el('div', 'cr-m' + (i ? ' sec' : ''), tx)); });
      var tg = crTags(e, ord === 'ambientazione' ? 'ambientazione' : ord === 'uscita' ? 'uscita' : 'exp-a', {}) || el('div', 'cr-tags');
      if (e.tipo) tg.insertBefore(crTag('t', CR_TIPO[e.tipo] || e.tipo), tg.firstChild);
      if (e.unis.length) { var uu = e.unis.slice(0, 2).map(crShort).join(' · ') + (e.unis.length > 2 ? ' +' + (e.unis.length - 2) : ''); tg.appendChild(crTag('u', uu)); } else tg.appendChild(crTag('n', 'non assegnata'));
      li.appendChild(tg);
      var ac = el('div', 'cr-acts'); ac.appendChild(btn('cr-lk', 'Scheda ›', null)); ac.firstChild.setAttribute('data-go', 'item:' + e.id); ac.firstChild.setAttribute('aria-label', 'Apri la scheda di ' + e.title);
      if (e.unis.length === 1) {
        var u = e.unis[0]; ac.appendChild(btn('cr-lk', 'Dossier', function () { openUni(u); })); ac.appendChild(btn('cr-lk', '◎ Mappa', function () { openMappa(u); })); ac.appendChild(btn('cr-lk', 'Cronologia', function () { crOpen('uni', { uid: u }); }));
      } else if (e.unis.length > 1) {
        var mb = btn('cr-lk', 'Universi (' + e.unis.length + ') ▾', null); mb.addEventListener('click', function () {
          crSheet(e.title, function (bd) { bd.appendChild(el('p', 'cr-note', 'Presente in più universi: scegli dove proseguire.')); e.unis.forEach(function (u) { var g = el('div', 'cr-ugrp'); g.appendChild(el('b', '', UNI[u].nome)); var r = el('div', 'cr-acts'); r.appendChild(btn('cr-lk', 'Dossier', function () { crCloseSheet(false); openUni(u); })); r.appendChild(btn('cr-lk', '◎ Mappa', function () { crCloseSheet(false); openMappa(u); })); r.appendChild(btn('cr-lk', 'Cronologia', function () { crCloseSheet(false); crOpen('uni', { uid: u }); })); g.appendChild(r); bd.appendChild(g); }); }, mb);
        }); ac.appendChild(mb);
      }
      li.appendChild(ac); return li;
    }
    function crFilterSheet(C, repaint, opener) {
      crSheet('Filtri · Esplora', function (bd) {
        var cnt = btn('cr-go', null, function () { crCloseSheet(); }); cnt.id = 'crFgo';
        function upd() { cnt.textContent = 'Mostra ' + crPlural(crMatch(C).length, 'risultato', 'risultati'); repaint(); }
        function group(title, hint) { var g = el('section', 'cr-fg'); g.appendChild(el('h4', '', title)); if (hint) g.appendChild(el('p', 'cr-note', hint)); bd.appendChild(g); return g; }
        function chips(g, items, arr, multiUpdate) {
          var box = el('div', 'cr-fchips cr-fw'); items.forEach(function (o) { var on = arr.indexOf(o[0]) !== -1, b = btn('a2-f' + (on ? ' on' : ''), o[1], function () { var i = arr.indexOf(o[0]); if (i === -1) arr.push(o[0]); else arr.splice(i, 1); b.classList.toggle('on', i === -1); b.setAttribute('aria-pressed', i === -1 ? 'true' : 'false'); C.xl = 30; upd(); }); b.setAttribute('aria-pressed', on ? 'true' : 'false'); box.appendChild(b); }); g.appendChild(box);
        }
        var g1 = group('Il periodo si riferisce a', 'Ambientazione e anno di uscita sono dati distinti: scegli quale usare.');
        g1.appendChild(crSeg([['amb', 'Ambientazione'], ['rel', 'Anno di uscita']], C.fb, function (k) { C.fb = k; C.xl = 30; var y = bd.scrollTop; crCloseSheet(false); crFilterSheet(C, repaint, opener); CRS.bd.scrollTop = y; repaint(); }, 'Base del periodo'));
        chips(g1, CR_BINS.map(function (b) { return [b[0], b[1]]; }), C.fp);
        g1.appendChild(el('p', 'cr-note', C.fb === 'amb' ? '«Senza data» include i titoli senza anno di ambientazione e le animazioni (il loro periodo è di messa in onda).' : '«Senza data» include i titoli per cui la guida non indica la data di uscita.'));
        var g2 = group('Universo'); chips(g2, UM.ids().map(function (u) { return [u, crShort(u)]; }).concat([['_na', 'Non assegnate']]), C.fu);
        var g3 = group('Saga della guida', 'Le saghe sono quelle della Timeline alternativa (solo titoli della guida, non animazioni).'); chips(g3, crData().sagas.map(function (s) { return [s, s]; }), C.fs);
        var g4 = group('Tipo di contenuto'); chips(g4, [['film', 'Film'], ['serie', 'Serie'], ['speciale', 'Speciale'], ['animazione', 'Animazione']], C.ft);
        var g5 = group('Stato di uscita'); chips(g5, [['p', 'Solo previste']], { indexOf: function () { return C.fr ? 0 : -1; }, push: function () { C.fr = true; }, splice: function () { C.fr = false; } });
        var ft = el('div', 'cr-fa'); ft.appendChild(btn('cr-lk cr-clr', 'Azzera', function () { C.fu = []; C.fp = []; C.fs = []; C.ft = []; C.fr = false; C.xl = 30; var y = bd.scrollTop; crCloseSheet(false); crFilterSheet(C, repaint, opener); repaint(); })); ft.appendChild(cnt); bd.appendChild(ft); upd();
      }, opener);
    }
    function crExp(main, C) {
      crData();
      var bar = el('div', 'cr-bar'), f = el('form', 'cr-search'); f.setAttribute('role', 'search'); f.addEventListener('submit', function (e) { e.preventDefault(); });
      f.appendChild(el('span', 'cr-s-i', '⌕')); var inp = D.createElement('input'); inp.type = 'search'; inp.id = 'crQ'; inp.value = C.q; inp.placeholder = 'Cerca un titolo…'; inp.setAttribute('aria-label', 'Cerca un titolo'); inp.autocomplete = 'off'; f.appendChild(inp);
      var fb = btn('cr-fbtn', null, function () { crFilterSheet(C, paint, fb); }); fb.id = 'crFbtn'; fb.setAttribute('aria-haspopup', 'dialog'); fb.appendChild(el('span', '', '☰')); var dot = el('i', 'cr-dot'); fb.appendChild(dot);
      bar.appendChild(f); bar.appendChild(fb); main.appendChild(bar);
      var chipsBox = el('div', 'cr-fchips cr-act'); main.appendChild(chipsBox);
      main.appendChild(crSeg([['uscita', 'Uscita'], ['ambientazione', 'Ambientaz.'], ['guida', 'Guida'], ['az', 'A–Z']], C.xo, function (k) { C.xo = k; C.xl = 30; crRedraw(true); }, 'Ordinamento dei risultati'));
      var info = el('div', 'cr-info'); info.setAttribute('aria-live', 'polite'); main.appendChild(info); var res = el('div', 'cr-resbox'); main.appendChild(res);
      function chipX(lbl, fn) { var b = btn('a2-f on cr-x2', lbl + ' ✕', fn); b.setAttribute('aria-label', 'Rimuovi filtro: ' + lbl); chipsBox.appendChild(b); }
      function paint() {
        var n = crFilterN(C); dot.style.display = n ? '' : 'none'; fb.setAttribute('aria-label', 'Filtri' + (n ? ', ' + n + ' attivi' : ''));
        chipsBox.textContent = '';
        if (C.fu.length) chipX('Universo: ' + (C.fu.length === 1 ? (C.fu[0] === '_na' ? 'Non assegnate' : crShort(C.fu[0])) : C.fu.length + ' selezionati'), function () { C.fu = []; C.xl = 30; paint(); });
        if (C.fp.length) chipX((C.fb === 'amb' ? 'Ambientaz. ' : 'Uscita ') + C.fp.map(function (b) { return CR_BINS.filter(function (x) { return x[0] === b; })[0][1]; }).join(', '), function () { C.fp = []; C.xl = 30; paint(); });
        if (C.fs.length) chipX('Saga: ' + C.fs.length, function () { C.fs = []; C.xl = 30; paint(); });
        if (C.ft.length) chipX('Tipo: ' + C.ft.map(function (t) { return CR_TIPO[t]; }).join(', '), function () { C.ft = []; C.xl = 30; paint(); });
        if (C.fr) chipX('Solo previste', function () { C.fr = false; C.xl = 30; paint(); });
        chipsBox.style.display = chipsBox.childNodes.length ? '' : 'none';
        var all = crMatch(C), asg = all.filter(function (e) { return e.unis.length; }), na = all.filter(function (e) { return !e.unis.length; });
        info.textContent = ''; var t = el('span', 'cr-cnt'); t.appendChild(el('b', '', String(all.length))); t.appendChild(D.createTextNode(' risultati' + (n ? ' · ' + crPlural(n, 'filtro', 'filtri') : ''))); info.appendChild(t);
        if (n || C.q) info.appendChild(btn('cr-lk cr-clr', 'Azzera', function () { C.q = ''; inp.value = ''; C.fu = []; C.fp = []; C.fs = []; C.ft = []; C.fr = false; C.xl = 30; paint(); }));
        if (na.length && C.fu.indexOf('_na') === -1) { var nb = btn('cr-lk', 'Non assegnate · ' + na.length, function () { C.fu = ['_na']; C.xl = 30; paint(); }); nb.setAttribute('aria-label', 'Mostra solo le ' + na.length + ' non assegnate'); info.appendChild(nb); }
        res.textContent = '';
        if (!all.length) { var em = el('div', 'cr-empty'); em.appendChild(el('b', '', 'Nessun risultato')); em.appendChild(el('p', '', 'Prova a togliere un filtro o a cambiare la ricerca.')); res.appendChild(em); return; }
        var s = crSort(asg, C.xo), shown = 0, ol = el('ol', 'cr-reslist'); ol.setAttribute('aria-label', 'Risultati');
        var lim = C.xl; s.lista.slice(0, lim).forEach(function (e) { ol.appendChild(crResRow(e, C.xo)); shown++; });
        if (shown < lim && s.senza.length) { var dv = el('li', 'cr-sepli'); dv.textContent = (C.xo === 'ambientazione' ? 'Senza anno di ambientazione' : 'Senza data di uscita') + ' · ' + s.senza.length; ol.appendChild(dv); s.senza.slice(0, lim - shown).forEach(function (e) { ol.appendChild(crResRow(e, C.xo)); shown++; }); }
        if (asg.length) res.appendChild(ol);
        if (asg.length > shown) { var mo = btn('cr-more', 'Mostra altri ' + Math.min(30, asg.length - shown) + ' · restano ' + (asg.length - shown), function () { C.xl += 30; var y = body.scrollTop; paint(); body.scrollTop = y; }); mo.id = 'crMore'; res.appendChild(mo); }
        if (na.length) {
          var sec = el('section', 'cr-na'), nh = btn('cr-band', null, function () { C.na = !C.na; paint(); }); nh.id = 'crNaBtn'; nh.setAttribute('aria-expanded', (C.na || C.fu.indexOf('_na') !== -1) ? 'true' : 'false');
          nh.appendChild(el('span', '', 'Non assegnate · ' + na.length)); nh.appendChild(el('span', 'cr-band-c', (C.na || C.fu.indexOf('_na') !== -1) ? 'Nascondi ▴' : 'Mostra ▾')); sec.appendChild(nh);
          if (C.na || C.fu.indexOf('_na') !== -1) { sec.appendChild(el('p', 'cr-note', 'Titoli di animazione presenti nella guida ma non classificati in alcun universo. Non sono attribuiti automaticamente a nessun universo esistente.')); var o3 = el('ol', 'cr-reslist'); crSort(na, C.xo).lista.concat(crSort(na, C.xo).senza).forEach(function (e) { o3.appendChild(crResRow(e, C.xo)); }); sec.appendChild(o3); }
          res.appendChild(sec);
        }
      }
      inp.addEventListener('input', function () { C.q = inp.value; C.xl = 30; paint(); });
      paint();
    }

    /* ---- schermata ---- */
    function renderCron() {
      var C = ST.cr || (ST.cr = crFresh()); crData(); crCloseSheet(false);
      body.className = 'a2-scroll a2-cron'; body.textContent = ''; setTitle('Cronologie', 'Esplora il tempo');
      var hd = el('section', 'cr-head'); hd.appendChild(el('span', 'a2-kick', 'MULTIVERSO E TEMPO')); hd.appendChild(el('h2', '', C.mode === 'uni' ? 'Cronologia di un universo' : C.mode === 'par' ? 'Cronologie parallele' : 'Esplora nel tempo')); body.appendChild(hd);
      body.appendChild(crTabs(C)); var main = el('div', 'cr-main'); main.setAttribute('role', 'tabpanel'); main.setAttribute('aria-labelledby', 'crTab-' + C.mode); body.appendChild(main);
      if (C.mode === 'uni') crUni(main, C); else if (C.mode === 'par') crPar(main, C); else crExp(main, C);
    }
    W.tvaTime = { data: function () { return crData(); }, list: crUniList, cov: crCov, sort: crSort, avail: crAvail, state: function () { return JSON.parse(JSON.stringify(ST.cr || null)); }, bins: CR_BINS.map(function (b) { return b[0]; }) };
    /* ==== CRON3C:END ==== */
