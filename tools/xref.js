/* ===== TVA XREF — facciata di LETTURA per i collegamenti fra archivi (FASE 4, sprint A) =====
   Nessun dato proprio, nessuna scrittura. Interroga gli indici gia' esistenti (tvaIdx, modello archivi, atlasData, altTimelineData,
   schede degli attori) e restituisce ogni legame con la sua FONTE:
     G = scritto nella guida (campi delle schede, atlasData);   D = derivato (nome esatto nel testo, corrispondenza del titolo);   N = non documentato.
   Nessuna relazione viene dedotta oltre questi due livelli; i nomi ambigui non si collegano. */
(function () {
  'use strict';
  try {
    var W = window, D = document, A = W.tvaAtlas2, X = A && A.ext, a = X && X.api;
    if (!a || W.tvaXref) return;
    var IDX = a.IDX, UNI = a.UNI;
    function $(id) { return D.getElementById(id); }
    function J(id) { try { return JSON.parse($(id).textContent); } catch (e) { return null; } }
    var ATL = J('atlasData') || { opere: [], personaggi: [], identita: [] }, ALT = J('altTimelineData') || [];
    function k3(n) { return ('000' + n).slice(-3); }
    function VN(n) { try { return W.marvelNumeroVisibile ? W.marvelNumeroVisibile(n) : n; } catch (e) { return n; } }
    function FV(n) { try { return W.marvelIdDaNumeroVisibile ? W.marvelIdDaNumeroVisibile(n) : k3(n); } catch (e) { return k3(n); } }
    function GP(id) { var m = /^(?:item-)?(\d{3})$/.exec(String(id)); if (!m) return null; try { var p = W.marvelPosizioneGuida ? W.marvelPosizioneGuida(m[1]) : null; return p === undefined ? null : p; } catch (e) { return null; } }
    function byGuide(x, y) { var px = GP(x), py = GP(y); if (px !== null && py !== null && px !== py) return px - py; return x < y ? -1 : x > y ? 1 : 0; }
    function uniq(l) { var o = [], s = {}; l.forEach(function (x) { if (!s[x]) { s[x] = 1; o.push(x); } }); return o; }

    /* ---------- normalizzazione e confronto tollerante ---------- */
    var STOP = { and: 1, e: 1, ed: 1, the: 1, il: 1, lo: 1, la: 1, le: 1, i: 1, gli: 1, l: 1, of: 1, di: 1, del: 1, della: 1, dei: 1, delle: 1, un: 1, una: 1, a: 1 };
    // punteggiatura, accenti, maiuscole e «&»/«e»/«and» non cambiano l'esito; i punti si uniscono («S.H.I.E.L.D.» = «SHIELD»)
    function norm(s) {
      s = String(s == null ? '' : s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/&/g, ' and ');
      return s.replace(/[’'`´]/g, ' ').replace(/[^a-z0-9]+/g, ' ').replace(/\s+/g, ' ').trim();
    }
    function normD(s) {   // come norm, ma i punti si fondono con le lettere vicine
      s = String(s == null ? '' : s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/&/g, ' and ').replace(/\./g, '');
      return s.replace(/[’'`´]/g, ' ').replace(/[^a-z0-9]+/g, ' ').replace(/\s+/g, ' ').trim();
    }
    function compact(s) { return s.replace(/ /g, ''); }
    function toks(n) { var t = n.split(' ').filter(Boolean), c = t.filter(function (x) { return !STOP[x]; }); return c.length ? c : t; }
    // punteggio 0 = nessuna corrispondenza; piu' alto = piu' pertinente
    function prep(q) { var n = normD(q); return { n: n, c: compact(n), t: toks(n), raw: norm(q) }; }
    function score(P, hay) {
      if (!P.n) return 0;
      var h = normD(hay), hc = compact(h); if (!h) return 0;
      if (h === P.n) return 100;
      if (hc === P.c) return 96;
      if (h.indexOf(P.n) === 0 || hc.indexOf(P.c) === 0) return 80;
      if ((' ' + h).indexOf(' ' + P.n) !== -1) return 70;
      if (P.c.length >= 2 && hc.indexOf(P.c) !== -1) return 50;
      if (P.t.length > 1 || P.t.length === 1) {
        var ok = P.t.every(function (w) { return (' ' + h).indexOf(' ' + w) !== -1; });
        if (ok) return P.t.length > 1 ? 40 : 30;
      }
      return 0;
    }
    function best(P, list) { var m = 0; for (var i = 0; i < list.length; i++) { var s = score(P, list[i]); if (s > m) m = s; } return m; }

    /* ---------- attori (schede att-*): ruoli e titoli indicati dalla guida ---------- */
    var ATT = null;
    function attori() {
      if (ATT) return ATT;
      ATT = { list: [], byId: {}, byTitle: {}, byChar: {} };
      var M = A.arcModel ? A.arcModel() : null;
      Array.prototype.forEach.call(D.querySelectorAll('li[id^="att-"]'), function (li) {
        if (li.closest('.tva-archives-overlay') && false) return;
        var t = li.querySelector('.title'); if (!t) return;
        var e = { id: li.id, name: t.textContent.trim(), roles: [], titles: [], chars: [] };
        Array.prototype.forEach.call(li.querySelectorAll('.readings-list li'), function (r) {
          var ref = r.querySelector('.us-result-ref'), nm = '';
          Array.prototype.forEach.call(r.childNodes, function (n) { if (n.nodeType === 3) nm += n.nodeValue; });
          nm = nm.replace(/\s+/g, ' ').trim();
          var tid = [], re = /N°\s*(\d{3})/g, m, txt = ref ? ref.textContent : '';
          while ((m = re.exec(txt))) { var id = 'item-' + FV(m[1]); if (IDX.titoli[id] && tid.indexOf(id) === -1) tid.push(id); }
          // personaggio: solo se il nome del ruolo coincide con una scheda (M.scan = nome esatto, ambigui esclusi)
          var ch = []; if (M && M.scan && nm) { try { M.scan(nm, '').forEach(function (k) { if (k[0] === 'c' && IDX.personaggi[k.slice(2)]) ch.push(k.slice(2)); }); } catch (e2) {} }
          e.roles.push({ nome: nm, titoli: tid, personaggi: ch.slice(0, 3), rif: txt.replace(/^\s*[—\-]\s*/, '').trim() });
          tid.forEach(function (x) { if (e.titles.indexOf(x) === -1) e.titles.push(x); });
          ch.slice(0, 3).forEach(function (c) { if (e.chars.indexOf(c) === -1) e.chars.push(c); });
        });
        e.titles.sort(byGuide);
        ATT.list.push(e); ATT.byId[e.id] = e;
        e.titles.forEach(function (x) { (ATT.byTitle[x] = ATT.byTitle[x] || []).push(e.id); });
        e.chars.forEach(function (c) { (ATT.byChar[c] = ATT.byChar[c] || []).push(e.id); });
      });
      return ATT;
    }

    /* ---------- opere ---------- */
    var OPE = null, ALTN = null;
    function opereIdx() {
      if (OPE) return OPE; OPE = {}; ALTN = {};
      (ATL.opere || []).forEach(function (o) { OPE[o.id] = o; });
      (ALT || []).forEach(function (x) { ALTN[k3(x.num)] = x; });
      return OPE;
    }
    var SAGAIDX = null;
    function saga(id) {
      opereIdx(); var m = /^item-(\d{3})$/.exec(id); if (!m) return null;
      var x = ALTN[m[1]]; if (!x) return null;
      if (!SAGAIDX) {
        SAGAIDX = {};
        Object.keys(IDX.titoli).filter(function (k) { return /^item-\d{3}$/.test(k) && !IDX.titoli[k].variant && ALTN[k.slice(5)]; }).sort(byGuide).forEach(function (k) {
          var sg = ALTN[k.slice(5)].saga; (SAGAIDX[sg] = SAGAIDX[sg] || []).push(k);
        });
      }
      var lst = SAGAIDX[x.saga] || [];
      return { nome: x.saga, pos: lst.indexOf(id) + 1, di: lst.length, studio: x.studio, tag: x.tag, release: x.release };
    }
    var GUIDA = null;
    function guida() {   // titoli (non varianti) in ordine di guida: unica sequenza editoriale
      if (!GUIDA) GUIDA = Object.keys(IDX.titoli).filter(function (k) { return /^item-\d{3}$/.test(k) && !IDX.titoli[k].variant; }).sort(byGuide);
      return GUIDA;
    }
    function chk(id) { var e = IDX.titoli[id]; return e && e.li ? e.li.querySelector('.watch-check, .anim-watch-check, .variant-check') : null; }
    function visto(id) { var c = chk(id); return !!(c && c.checked); }
    function dipendenze() { try { return W.marvelDipendenzeLettura ? W.marvelDipendenzeLettura() : null; } catch (e) { return null; } }
    function linkDip(id) {
      var d = dipendenze(), m = /^item-(\d{3})$/.exec(id); if (!d || !m) return { richiede: [], consigliati: [], facoltativi: [], dipendeDa: [], mappa: false };
      var n = m[1], mp = d.map[n], dirT = (d.prereq[n] || []).map(function (x) { return 'item-' + x; }).filter(function (x) { return IDX.titoli[x]; });
      var ess = mp ? mp.ess.map(function (x) { return 'item-' + x; }) : [];
      var out = { richiede: uniq(dirT.concat(ess.filter(function (x) { return IDX.titoli[x]; }))), consigliati: mp ? mp.cons.map(function (x) { return 'item-' + x; }).filter(function (x) { return IDX.titoli[x]; }) : [],
        facoltativi: mp ? mp.opz.map(function (x) { return 'item-' + x; }).filter(function (x) { return IDX.titoli[x]; }) : [], dipendeDa: [], mappa: !!mp, motivi: (d.motivi && d.motivi[n]) || {} };
      // inverso: titoli che richiedono questo (stessa fonte, letta al contrario)
      Object.keys(d.prereq).forEach(function (k) { if (d.prereq[k].indexOf(n) !== -1 && IDX.titoli['item-' + k]) out.dipendeDa.push('item-' + k); });
      Object.keys(d.map).forEach(function (k) { var v = d.map[k]; if ((v.ess.indexOf(n) !== -1 || v.cons.indexOf(n) !== -1 || v.opz.indexOf(n) !== -1) && IDX.titoli['item-' + k] && out.dipendeDa.indexOf('item-' + k) === -1) out.dipendeDa.push('item-' + k); });
      out.richiede.sort(byGuide); out.consigliati.sort(byGuide); out.facoltativi.sort(byGuide); out.dipendeDa.sort(byGuide);
      return out;
    }
    function archiviDi(id) {
      var M = A.arcModel ? A.arcModel() : null; if (!M) return [];
      return (M.byTitle[id] || []).map(function (x) { var e = M.byId[x]; return e ? { id: e.id, cat: e.cat, nome: e.name, sub: e.sub, fonte: 'G' } : null; }).filter(Boolean);
    }
    // D4 — organizzazioni il cui nome compare nel titolo dell'opera (corrispondenza del TITOLO, non apparizione ne' relazione narrativa)
    function orgVariants(e) {
      var base = e.name.replace(/\s*\([^)]*\)/g, '').trim(), out = [];
      function add(t) { t = normD(t); if (t.length >= 4 && out.indexOf(t) === -1) out.push(t); }
      add(base); base.split('/').forEach(add); (e.name.match(/\(([^)]*)\)/g) || []).forEach(function (p) { add(p.slice(1, -1)); });
      return out;
    }
    function titoloContiene(titolo, v) { var h = ' ' + normD(titolo) + ' '; return h.indexOf(' ' + v + ' ') !== -1; }
    function orgNelTitolo(titleId) {
      var M = A.arcModel ? A.arcModel() : null, e = IDX.titoli[titleId]; if (!M || !e) return [];
      var out = [];
      M.cat.org.forEach(function (o) { var hit = orgVariants(o).filter(function (v) { return titoloContiene(e.title, v); }); if (hit.length) out.push({ id: o.id, nome: o.name, corrispondenza: hit[0], confermato: (o.titles || []).indexOf(titleId) !== -1, fonte: 'D' }); });
      return out;
    }
    function titoliConNomeOrg(orgId) {
      var M = A.arcModel ? A.arcModel() : null, o = M && M.byId[orgId]; if (!o) return [];
      var vs = orgVariants(o), out = [];
      guida().concat(Object.keys(IDX.titoli).filter(function (k) { return /^anim-/.test(k); })).forEach(function (tid) {
        var t = IDX.titoli[tid]; if (!t || t.variant) return;
        var hit = vs.filter(function (v) { return titoloContiene(t.title, v); }); if (hit.length) out.push({ id: tid, titolo: t.title, corrispondenza: hit[0], confermato: (o.titles || []).indexOf(tid) !== -1, fonte: 'D' });
      });
      return out;
    }

    function opera(id) {
      var e = IDX.titoli[id]; if (!e) return null; opereIdx();
      var m = /^item-(\d{3})$/.exec(id), o = m ? OPE[m[1]] : null, sg = saga(id);
      var gi = guida(), ix = gi.indexOf(id);
      var chars = uniq((IDX.itemChars && IDX.itemChars[id]) || []).filter(function (c) { return IDX.personaggi[c]; });
      var att = attori().byTitle[id] || [];
      var c = chk(id), lv = e.li.querySelector('.detail-panel');
      function row(k) { var rr = null; if (lv) Array.prototype.forEach.call(lv.querySelectorAll(':scope > .detail-row'), function (r) { var kk = r.querySelector('.detail-k'); if (kk && kk.textContent.trim().toUpperCase() === k) rr = r.querySelector('.detail-v'); }); return rr; }
      function sub(titolo, key) {
        var res = null; if (!lv) return null;
        Array.prototype.forEach.call(lv.querySelectorAll('details.sub-group'), function (d) {
          var s = d.querySelector('summary'); if (!s || s.textContent.indexOf(titolo) === -1) return;
          Array.prototype.forEach.call(d.querySelectorAll('.detail-row'), function (r) { var kk = r.querySelector('.detail-k'); if (kk && kk.textContent.trim().toUpperCase() === key) res = r.querySelector('.detail-v'); });
        });
        return res;
      }
      var tr = sub('Trama', 'SPOILER-FREE'), du = row('DURATA'), pers = row('PERSONAGGI');
      return {
        id: id, titolo: e.title, kind: e.kind, variante: !!e.variant, num: e.num || null, vis: e.kind === 'item' ? VN(e.num) : null,
        tipo: a.tipoTitolo(e), anno: a.anno(e), icona: (e.li.querySelector('.ic') || {}).textContent || '',
        guida: m && ix !== -1 ? { pos: ix + 1, tot: gi.length, vis: VN(m[1]), prec: ix > 0 ? gi[ix - 1] : null, succ: ix < gi.length - 1 ? gi[ix + 1] : null, fonte: 'G' } : null,
        uscita: o && o.uscita ? { iso: o.uscita, prec: o.precisioneUscita || '', fonte: 'G' } : null,
        ambientazione: o && o.ambientazione ? { testo: o.ambientazione, fonte: 'G' } : null,
        ruolo: o ? o.ruolo : null, universi: (e.unis || []).filter(function (u) { return UNI[u]; }), saga: sg,
        personaggi: chars, attori: att, trama: tr ? tr.textContent.trim() : '', durata: du ? du.textContent.trim() : '', personaggiTesto: pers ? pers.textContent.trim() : '',
        dip: linkDip(id), archivi: archiviDi(id), orgTitolo: orgNelTitolo(id),
        visto: !!(c && c.checked), puoVisto: !!c, prioritaTag: saga(id) ? saga(id).tag : (e.li.getAttribute('data-tag') || '')
      };
    }

    /* ---------- personaggi: percorso nella guida, attori, archivi ---------- */
    function personaggio(cid) {
      var c = IDX.personaggi[cid]; if (!c) return null; var M = A.arcModel ? A.arcModel() : null;
      var apps = (c.apps || []).slice().sort(byGuide);
      return { id: cid, nome: c.name, percorso: apps, attori: (attori().byChar[cid] || []).slice(), orgs: M ? (M.charOrg[cid] || []) : [], citato: M ? (M.charCited[cid] || []) : [], extra: M ? (M.charExtra[cid] || []) : [] };
    }
    function filmografia(attId) {
      var e = attori().byId[attId]; if (!e) return [];
      var out = [];
      e.roles.forEach(function (r) { r.titoli.forEach(function (t) { out.push({ titolo: t, ruolo: r.nome, personaggi: r.personaggi, rif: r.rif }); }); });
      out.sort(function (x, y) { return byGuide(x.titolo, y.titolo); });
      return out;
    }

    function breve(id) {
      var e = IDX.titoli[id]; if (!e) return null; opereIdx(); var m = /^item-(\d{3})$/.exec(id), o = m ? OPE[m[1]] : null;
      return { id: id, titolo: e.title, vis: e.kind === 'item' ? VN(e.num) : null, tipo: a.tipoTitolo(e), uscita: o && o.uscita ? o.uscita : null, anno: a.anno(e), visto: visto(id) };
    }
    function identita(cid) {
      var out = []; (ATL.identita || []).forEach(function (g) { if ((g.pagine || []).indexOf(cid) !== -1) out.push(g); }); return out;
    }
    function incarnazioni(cid) {
      var p = null; (ATL.personaggi || []).forEach(function (x) { if (x.id === cid) p = x; }); if (!p) return null;
      var inc = (p.incarnazioni || []).map(function (i) { return { id: i.id, universi: (i.universi || []).filter(function (u) { return UNI[u]; }), titoli: (i.opere || []).map(function (n) { return 'item-' + k3(n); }).filter(function (t) { return IDX.titoli[t]; }), stato: i.stato || '' }; });
      var col = (p.collegamentiMultiversoMCU || []).map(function (c) { return { universo: UNI[c.universo] ? c.universo : null, tipo: c.tipo || '', origine: c.origine || '' }; });
      if (!inc.length && !col.length) return null; return { incarnazioni: inc, collegamenti: col, sottotipo: p.sottotipo || '' };
    }
    /* ---------- D3: candidati «stesso individuo» (solo elenco; nessuna unione) ---------- */
    function duplicati() {
      var chars = Object.keys(IDX.personaggi), ident = {};
      (ATL.identita || []).forEach(function (g) { (g.pagine || []).forEach(function (p) { (ident[p] = ident[p] || []).push(g.id); }); });
      var groups = {};
      chars.forEach(function (id) {
        var nm = IDX.personaggi[id].name.replace(/\s*\([^)]*\)/g, ''), toks2 = normD(nm).split(' ').filter(Boolean);
        if (!toks2.length) return;
        var keys = [normD(nm)]; if (toks2.length > 1) keys.push(toks2[toks2.length - 1] + '|' + toks2[0].charAt(0));
        keys.forEach(function (k) { (groups[k] = groups[k] || []).push(id); });
      });
      return { gruppi: groups, dichiarati: ident };
    }

    /* ---------- ricerca tipizzata ---------- */
    var TIPI = [
      { k: 'sez', lbl: 'Sezioni' }, { k: 'uni', lbl: 'Universi' }, { k: 'tit', lbl: 'Titoli' }, { k: 'chr', lbl: 'Personaggi' }, { k: 'att', lbl: 'Attori' },
      { k: 'org', lbl: 'Organizzazioni' }, { k: 'evt', lbl: 'Eventi' }, { k: 'luo', lbl: 'Luoghi' }, { k: 'art', lbl: 'Artefatti' }, { k: 'cos', lbl: 'Entità cosmiche' }, { k: 'spe', lbl: 'Specie e civiltà' }, { k: 'mis', lbl: 'Arti mistiche' }
    ];
    var SIDX = null;
    function ricIdx() {
      if (SIDX) return SIDX; SIDX = [];
      var M = A.arcModel ? A.arcModel() : null;
      (a.GRP || []).forEach(function (g) { g.items.forEach(function (i) { SIDX.push({ t: 'sez', id: i.k, name: i.n, sub: g.n, hay: [i.n, i.kw || '', g.n + ' ' + i.n], item: i }); }); });
      Object.keys(UNI).forEach(function (u) { var n = UNI[u].nome || u, p = n.split(' — '); SIDX.push({ t: 'uni', id: u, name: n, sub: '', hay: [n].concat(p.length > 1 ? p : []).concat(['earth ' + (/Earth-(\w+)/.exec(n) || [])[1] || '']) }); });
      a.titoliBase().forEach(function (e) {
        var al = [e.title]; var sd = e.li && e.li.getAttribute('data-search'); if (sd) al.push(sd);
        SIDX.push({ t: 'tit', id: e.id, name: e.title, sub: [a.tipoTitolo(e), e.num ? 'N°' + VN(e.num) : '', a.anno(e)].filter(Boolean).join(' · '), hay: al });
      });
      a.personaggiLista().forEach(function (c) {
        var al = [c.name]; c.name.split('/').forEach(function (p) { al.push(p.replace(/\s*\([^)]*\)/g, '')); }); (c.name.match(/\(([^)]*)\)/g) || []).forEach(function (p) { al.push(p.slice(1, -1)); });
        SIDX.push({ t: 'chr', id: c.id, name: c.name, sub: '', hay: al });
      });
      attori().list.forEach(function (e) { SIDX.push({ t: 'att', id: e.id, name: e.name, sub: e.roles.length + (e.roles.length === 1 ? ' ruolo' : ' ruoli'), hay: [e.name] }); });
      if (M) M.list.forEach(function (e) {
        var al = [e.name]; e.name.split('/').forEach(function (p) { al.push(p.replace(/\s*\([^)]*\)/g, '')); }); (e.name.match(/\(([^)]*)\)/g) || []).forEach(function (p) { al.push(p.slice(1, -1)); });
        SIDX.push({ t: e.cat, id: e.id, name: e.name, sub: e.sub || '', hay: al });
      });
      return SIDX;
    }
    function cerca(q) {
      var P = prep(q), res = {}; if (P.n.length < 2) return { q: q, gruppi: [], n: 0, prep: P };
      ricIdx().forEach(function (it) { var s = best(P, it.hay); if (s > 0) (res[it.t] = res[it.t] || []).push({ it: it, s: s }); });
      var gr = [], n = 0;
      TIPI.forEach(function (T) {
        var l = res[T.k]; if (!l || !l.length) return;
        l.sort(function (x, y) { return y.s - x.s || x.it.name.localeCompare(y.it.name, 'it'); }); n += l.length;
        gr.push({ tipo: T.k, lbl: T.lbl, voci: l.map(function (x) { return x.it; }) });
      });
      return { q: q, gruppi: gr, n: n, prep: P };
    }

    W.tvaXref = { norm: norm, normD: normD, prep: prep, score: score, opera: opera, personaggio: personaggio, attori: attori, filmografia: filmografia, archiviDi: archiviDi, orgNelTitolo: orgNelTitolo,
      titoliConNomeOrg: titoliConNomeOrg, dipendenze: linkDip, saga: saga, guida: guida, visto: visto, chk: chk, breve: breve, identita: identita, incarnazioni: incarnazioni, cerca: cerca, tipi: TIPI, duplicati: duplicati, byGuide: byGuide, VN: VN, FV: FV, GP: GP, uniq: uniq,
      fonti: { G: 'scritto nella guida', D: 'derivato', N: 'non documentato' } };
  } catch (eX) { if (window.console) console.error('tvaXref:', eX); }
})();
