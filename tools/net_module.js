/* ===== TVA NET — indice relazioni + router di navigazione (additivo, nessun dato riscritto) ===== */
(function () {
  'use strict';
  try {
    var D = document, W = window;
    // Numero visibile (N°, posizionale) <-> id stabile; posizione di guida. Fonte: funzioni window.marvel* del modulo principale quando sono gia' definite
    // oppure, se questo modulo parte prima, la stessa tabella ricavata dal DOM (.rec delle schede): stessa regola, nessun dato duplicato.
    var _NV = null;
    function nvTab() { if (_NV) return _NV; var a = {}, b = {}, g = {}; Array.prototype.forEach.call(D.querySelectorAll('.card-wrap[id^="item-"]'), function (n, k) { var id = n.id.slice(5), r = n.querySelector('.rec'), m = r && /(\d+)/.exec(r.textContent), v = m ? m[1] : id; a[id] = v; b[v] = id; g[id] = k; }); return (_NV = { a: a, b: b, g: g }); }
    function k3(n) { return ('000' + n).slice(-3); }
    function VN(n) { try { return W.marvelNumeroVisibile ? W.marvelNumeroVisibile(n) : (nvTab().a[k3(n)] || k3(n)); } catch (e) { return n; } }
    function FV(n) { try { return W.marvelIdDaNumeroVisibile ? W.marvelIdDaNumeroVisibile(n) : (nvTab().b[k3(n)] || k3(n)); } catch (e) { return n; } }
    function GP(n) { var m = /^(?:item-)?(\d{3})$/.exec(String(n)); if (!m) return null; try { var p = W.marvelPosizioneGuida ? W.marvelPosizioneGuida(m[1]) : nvTab().g[m[1]]; return p === undefined ? null : p; } catch (e) { return null; } }
    function byGuide(a, b) { var pa = /^([a-z0-9]+)-/.exec(String(a)), pb = /^([a-z0-9]+)-/.exec(String(b)); pa = pa ? pa[1] : 'item'; pb = pb ? pb[1] : 'item'; if (pa !== pb) return pa < pb ? -1 : 1; var x = GP(a), y = GP(b); if (x !== null && y !== null && x !== y) return x - y; return a < b ? -1 : a > b ? 1 : 0; }

    function $(id) { return D.getElementById(id); }
    function J(id) { try { return JSON.parse($(id).textContent); } catch (e) { return null; } }
    var MV = J('mvMapData') || { universi: {}, famiglie: {} };
    var ATL = J('atlasData') || { opere: [], animate: [], personaggi: [] };
    var UNI = MV.universi || {};
    var FAM = MV.famiglie || {};
    var RUOLO = {};
    (ATL.opere || []).forEach(function (o) { RUOLO[o.id] = o.ruolo || ''; });

    /* ---------- 1. INDICE DELLE RELAZIONI (derivato dai dati già presenti) ---------- */
    var TIT = {};          // li.id -> {li, id, kind, title, unis[]}
    var TITLIST = [];      // in ordine di documento (= ordine della guida)
    // Le serie animate ricevono data-uni a runtime (filtro universo, script precedente): qui l'universo si legge direttamente
    // da atlasData.animate, cosi' l'indice non dipende dall'ordine di esecuzione degli script.
    var ANIMU = {};
    (ATL.animate || []).forEach(function (x) { if (x.universi && x.universi.length) ANIMU[x.id] = x.universi.slice(); });
    Array.prototype.forEach.call(D.querySelectorAll('li.card-wrap[id]'), function (li) {
      var m = /^(item|anim|p4)-/.exec(li.id);
      if (!m || li.closest('.tva-archives-overlay')) return;
      var t = li.querySelector('.title');
      var e = { li: li, id: li.id, kind: m[1], title: t ? t.textContent.trim() : li.id,
        num: li.getAttribute('data-item') || '', variant: li.classList.contains('card-variant'),
        unis: (li.getAttribute('data-uni') || '').split(/\s+/).filter(Boolean) };
      if (!e.unis.length && ANIMU[li.id]) e.unis = ANIMU[li.id].slice();
      TIT[li.id] = e; TITLIST.push(e);
    });
    function titoliDi(uid) { return TITLIST.filter(function (e) { return !e.variant && e.unis.indexOf(uid) !== -1; }); }
    function eCross(e) { return e.kind === 'item' ? RUOLO[e.num] === 'crossover' : e.unis.length > 1; }

    var CH = {};           // char id -> {li, name, apps[]}
    var ITEMCH = {};       // item li.id -> [char id]
    Array.prototype.forEach.call(D.querySelectorAll('li.card-wrap[id^="char-"]'), function (li) {
      var t = li.querySelector('.title');
      var apps = [];
      Array.prototype.forEach.call(li.querySelectorAll('.detail-row'), function (r) {
        var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v');
        if (!k || !v || !/APP\./.test(k.textContent)) return;
        var re = /N°(\d{3})/g, mm;
        while ((mm = re.exec(v.textContent))) { var iid = 'item-' + FV(mm[1]); if (TIT[iid] && apps.indexOf(iid) === -1) apps.push(iid); }
      });
      CH[li.id] = { li: li, id: li.id, name: t ? t.textContent.trim() : li.id, apps: apps };
      apps.forEach(function (iid) { (ITEMCH[iid] = ITEMCH[iid] || []).push(li.id); });
    });
    var CHAPP = {};        // char id -> universo di appartenenza (atlas.personaggi.appartenenza)
    (ATL.personaggi || []).forEach(function (p) { if (p.appartenenza && p.appartenenza.length) CHAPP[p.id] = p.appartenenza; });
    function personaggiDi(uid) { return Object.keys(CHAPP).filter(function (id) { return CHAPP[id].indexOf(uid) !== -1 && CH[id]; }); }
    // Categorie distinte (nessun dato nuovo, solo letture dei campi gia' presenti in atlasData):
    //  - origine  = personaggi.continuitaOrigine (continuita' d'origine dichiarata)
    //  - presenza = personaggi.appartenenza (universi della riga UNIVERSI della scheda: dove il personaggio compare)
    //  - ambientazione = opere.ambientazione (luogo/epoca, testo libero: NON e' un universo)
    //  - ruolo del titolo = opere.ruolo (primario | crossover | variante)
    var CO = {};
    (ATL.personaggi || []).forEach(function (p) { if (p.continuitaOrigine && p.continuitaOrigine.length) CO[p.id] = p.continuitaOrigine.filter(function (u) { return UNI[u]; }); });
    var AMBI = {};
    (ATL.opere || []).forEach(function (o) { if (o.ambientazione) AMBI[o.id] = o.ambientazione; });
    function origineDi(uid) { return Object.keys(CO).filter(function (id) { return CO[id].indexOf(uid) !== -1 && CH[id]; }); }
    function presentiDi(uid) { return personaggiDi(uid).filter(function (id) { return (CO[id] || []).indexOf(uid) === -1; }); }
    function breve(uid) { var n = (UNI[uid] && UNI[uid].nome) || uid; var p = n.split(' — '); return p.length > 1 ? p[1] : n; }
    function ruoloDi(e) { return e.variant ? 'variante' : (eCross(e) ? 'crossover' : 'appartenenza'); }

    // alias nome-universo -> id, solo se univoci (nessuna associazione indovinata)
    var ALIAS = {}, AMB = {};
    function addAlias(a, uid) {
      a = (a || '').trim().toLowerCase(); if (!a) return;
      if (ALIAS[a] && ALIAS[a] !== uid) AMB[a] = true; else ALIAS[a] = uid;
    }
    Object.keys(UNI).forEach(function (uid) {
      var n = UNI[uid].nome || ''; addAlias(n, uid);
      var p = n.split(' — '); if (p.length > 1) { addAlias(p[0], uid); addAlias(p[1], uid); }
    });
    function uidDaTesto(t) {
      t = (t || '').trim().toLowerCase(); if (!t || AMB[t]) return null;
      if (ALIAS[t]) return ALIAS[t];
      var m = /^(earth-\w+)\s*\(([^)]+)\)$/.exec(t);               // "Earth-96283 (Raimi-Verse)"
      if (m && ALIAS[m[1]] && !AMB[m[1]]) return ALIAS[m[1]];
      return null;
    }
    W.tvaIdx = { titoli: TIT, personaggi: CH, titoliDi: titoliDi, personaggiDi: personaggiDi, uidDaTesto: uidDaTesto, itemChars: ITEMCH,
      origineDi: origineDi, presentiDi: presentiDi, origineDa: function (cid) { return (CO[cid] || []).slice(); }, ambientazione: function (num) { return AMBI[num] || ''; },
      breve: breve, ruoloDi: ruoloDi, varianti: function (uid) { return TITLIST.filter(function (e) { return e.variant && e.unis.indexOf(uid) !== -1; }); } };

    /* ---------- 2. ROUTER: stack, ripristino filtro/scorrimento, tasto Indietro ---------- */
    var stack = [], busy = false;
    function cbs() {
      var o = {};
      Array.prototype.forEach.call(D.querySelectorAll('input[type=checkbox][id$="Toggle"]'), function (c) { if (c.id !== 'sidebarToggle' && c.checked) o[c.id] = 1; });
      return o;
    }
    function snapshot() {
      var db = D.querySelector('input[id^="dbtab-"]:checked');
      var act = D.querySelector('.app-tab-active');
      var hhx = $('homeHubExited');
      return { tg: cbs(), hh: !!(hhx && hhx.checked), db: db ? db.id : null, f: W.marvelUniFiltroStato ? W.marvelUniFiltroStato() : null,
        fl: W.marvelFiltriStato ? W.marvelFiltriStato() : null,
        y: W.pageYOffset || 0, an: anchorOf(), tab: act ? act.getAttribute('data-tab') : null,
        a2: (W.tvaAtlas2 && $('atlas2Toggle') && $('atlas2Toggle').checked) ? W.tvaAtlas2.getState() : null };
    }
    function raf2(fn) { requestAnimationFrame(function () { requestAnimationFrame(fn); }); }
    // Le schede usano content-visibility:auto: l'altezza stimata delle voci non ancora disegnate cambia mentre si scorre,
    // quindi un solo scrollIntoView non arriva a destinazione. Si riprova fino a quando la posizione e' stabile.
    function topMin() {
      var b = $('mvUniversoBanner');
      return (b && !b.hidden && b.offsetParent !== null) ? Math.round(b.getBoundingClientRect().bottom) + 6 : 8;
    }
    function settle(elm, want, cb) {
      var tries = 0, stable = 0;
      function step() {
        if (!elm || !elm.isConnected) return cb && cb(false);
        var d = elm.getBoundingClientRect().top - want;
        if (Math.abs(d) < 3) stable++; else { stable = 0; W.scrollBy({ top: d, left: 0, behavior: 'instant' }); }
        if (stable >= 3 || ++tries > 60) return cb && cb(stable >= 3);
        requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    }
    function waitVisible(elm, cb, n) {
      n = n || 0;
      if (elm.offsetParent !== null) return cb(true);
      if (n > 90) return cb(false);
      requestAnimationFrame(function () { waitVisible(elm, cb, n + 1); });
    }
    function anchorOf() {
      // elemento con id sotto alcuni punti dello schermo: posizione di riferimento stabile anche se sopra cambia l'altezza
      // di altre schede. elementFromPoint e' O(1): niente scansione di migliaia di nodi (conta sui telefoni lenti).
      var x = Math.round((W.innerWidth || 390) / 2), ys = [96, 170, 260, 380];
      for (var i = 0; i < ys.length; i++) {
        var e = D.elementFromPoint(x, ys[i]);
        while (e && e !== D.body) {
          if (e.id && e.id !== 'mvUniversoBanner' && e.id !== 'tvaBackBtn' && !(e.closest && (e.closest('#appTabbar') || e.closest('.sidebar')))) {
            return { id: e.id, off: Math.round(e.getBoundingClientRect().top) };
          }
          e = e.parentElement;
        }
      }
      return null;
    }
    function restore(s) {
      busy = true;
      try {
        if (s.f && s.f.uid) W.marvelEsploraUniverso(s.f.uid, s.f.nome, { noScroll: true, keepOverlays: true });
        else if (W.marvelUniFiltroStato && W.marvelUniFiltroStato().uid) W.marvelUniFiltroReset();
        if (s.fl && W.marvelFiltriImposta) W.marvelFiltriImposta(s.fl);
        W.marvelChiudiOverlay();
        // Home Marvel (hub) o documento: lo stato di partenza fa parte dello snapshot, altrimenti Indietro la lascerebbe nascosta
        if (typeof s.hh === 'boolean') { var hx = $('homeHubExited'), hb = $('homeHub'); if (hx) hx.checked = s.hh; if (hb) hb.style.display = s.hh ? 'none' : ''; }
        Object.keys(s.tg).forEach(function (id) { var c = $(id); if (c) c.checked = true; });
        if (s.db && $(s.db)) $(s.db).checked = true;
        if (s.tab && W.marvelAggiornaTab) W.marvelAggiornaTab(s.tab);
        if (s.a2 && W.tvaAtlas2) W.tvaAtlas2.setState(s.a2);
      } catch (e) { if (W.console) console.error('tvaNet restore', e); }
      raf2(function () {
        W.scrollTo(0, s.y);
        var an = s.an && $(s.an.id);
        if (an && an.offsetParent !== null) settle(an, s.an.off, function () { busy = false; refreshProg(); });
        else { busy = false; refreshProg(); }
      });
    }
    var backBtn = null;
    function ensureBack() {
      if (backBtn) return backBtn;
      var bar = $('appTabbar'); if (!bar) return null;
      backBtn = D.createElement('button');
      backBtn.type = 'button'; backBtn.id = 'tvaBackBtn'; backBtn.className = 'tva-back'; backBtn.hidden = true;
      backBtn.setAttribute('aria-label', 'Torna alla schermata precedente');
      backBtn.innerHTML = '<span aria-hidden="true">←</span> <span class="tva-back-t">Indietro</span>';
      backBtn.addEventListener('click', function () { goBack(); });
      bar.appendChild(backBtn);
      return backBtn;
    }
    function syncBack() {
      var b = ensureBack(); if (!b) return;
      b.hidden = stack.length === 0;
      var t = b.querySelector('.tva-back-t');
      if (stack.length && t) t.textContent = 'Indietro' + (stack[stack.length - 1].lbl ? ' · ' + stack[stack.length - 1].lbl : '');
    }
    function ctxLabel(s) {
      if (s.a2) return W.tvaAtlas2 && W.tvaAtlas2.label ? W.tvaAtlas2.label(s.a2) : 'Atlante';
      if (s.tg.tvaArchivesToggle) return 'Archivio';
      if (s.tg.tesseraToggle) return 'Tessera';
      if (s.tg.friendsToggle) return 'Friends';
      if (s.tg.altTimelineToggle) return 'Timeline alt.';
      if (s.tab === 'home') return 'Home';
      return s.f && s.f.uid ? 'Timeline · ' + (s.f.nome || '').replace(/^Earth-(\w+) — /, 'E-$1 ') : 'Timeline';
    }
    // Cronologia del browser (gesto/tasto Indietro di iOS): ogni livello dello stack ha una voce history con un numero
    // di sequenza crescente {tva: seq}. Alla popstate lo stato di destinazione dice a che livello si e' arrivati:
    // si ripristinano gli snapshot con seq > destinazione (l'ultimo estratto e' quello da ripristinare). Voci rimaste
    // dopo un azzeramento (tab) o oltre il limite dello stack vengono consumate senza effetti. Un cambio di #frammento
    // (indice della guida) genera anche una popstate con stato nullo: si distingue dal confronto con l'hash noto.
    var seqN = 0, baseHash = (W.location && W.location.hash) || '';
    function push(lbl) {
      var s = snapshot(); s.lbl = ctxLabel(s); s.seq = ++seqN;
      if (!stack.length) baseHash = W.location.hash || '';
      stack.push(s); if (stack.length > 40) stack.shift();
      try { history.pushState({ tva: s.seq }, ''); } catch (e) {}
      syncBack();
    }
    function popTo(destSeq) {
      var last = null;
      while (stack.length && stack[stack.length - 1].seq > destSeq) last = stack.pop();
      return last;
    }
    function goBack(fromPop) {
      if (!stack.length) return false;
      var top = stack[stack.length - 1];
      if (!fromPop) { try { if (history.state && history.state.tva === top.seq) { history.back(); return true; } } catch (e) {} }
      var s = stack.pop(); syncBack(); restore(s); return true;
    }
    W.addEventListener('popstate', function (ev) {
      if (!stack.length) return;
      var dest = ev.state && typeof ev.state.tva === 'number' ? ev.state.tva : null;
      if (dest === null) {
        // stato nullo: voce di base (Indietro dall'ultimo livello: stesso #frammento di quando e' iniziato lo stack)
        // oppure cambio di #frammento (indice della guida): in quel caso non si tocca lo stack
        if ((W.location.hash || '') !== baseHash) return;
        dest = 0;
      }
      var s = popTo(dest); syncBack();
      if (s) restore(s);
    });
    function resetStack() { stack.length = 0; syncBack(); }

    function exitHub() {
      var x = $('homeHubExited'); if (x) x.checked = true;
      var h = $('homeHub'); if (h) h.style.display = 'none';
    }
    function flash(el) { el.classList.add('us-flash'); setTimeout(function () { el.classList.remove('us-flash'); }, 1700); }
    function ensureVisible(li, done, n) {
      n = n || 0;
      if (li.offsetParent !== null) return done(true);
      // n=0: filtro universo che non comprende il titolo; n=1: ricerca/filtri (priorita', studio, tipo, preferiti, weekend)
      // che nascondono proprio questa scheda. Si azzerano solo i filtri responsabili; nessuna scrittura su localStorage:
      // "Indietro" ripristina esattamente lo stato precedente.
      if (n === 0 && W.marvelUniFiltroStato && W.marvelUniFiltroStato().uid && li.getAttribute('data-uni') && li.getAttribute('data-uni').indexOf(W.marvelUniFiltroStato().uid) === -1) W.marvelUniFiltroReset();
      else if (n === 1 && li.style.display === 'none' && W.marvelFiltriSblocca) W.marvelFiltriSblocca(li);
      if (n > 3) return done(li.offsetParent !== null);
      setTimeout(function () { ensureVisible(li, done, n + 1); }, 160);
    }
    function goItem(id, opt) {
      var e = TIT[id]; if (!e) return false;
      if (!(opt && opt.nopush)) push(e.title.length > 22 ? e.title.slice(0, 21) + '…' : e.title);
      W.marvelChiudiOverlay(); exitHub();
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('timeline');
      ensureVisible(e.li, function (ok) {
        var det = e.li.querySelector('details'); if (det) det.setAttribute('open', '');
        raf2(function () { settle(e.li, topMin(), function () { flash(e.li); }); });
      });
      return true;
    }
    function goUni(uid, opt) {
      if (!UNI[uid] || !$(uid)) return false;
      if (!(opt && opt.nopush)) push(UNI[uid].nome ? UNI[uid].nome.replace(/^Earth-(\w+) — /, 'E-$1 ') : 'Universo');
      if (W.tvaAtlas2) { W.tvaAtlas2.openUni(uid, true); return true; }
      W.marvelChiudiOverlay();
      var t = $('tvaArchivesToggle'); if (t) t.checked = true;
      var tab = $('dbtab-uni'); if (tab) tab.checked = true;
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('atlante');
      var card = $(uid), det = card.querySelector('details'); if (det) det.setAttribute('open', ''); openAncestors(card);
      waitVisible(card, function () { raf2(function () { settle(card, 8, function () { flash(card); }); }); });
      return true;
    }
    function goChar(id) {
      var c = CH[id]; if (!c) return false;
      // scheda nativa dell'Atlante (nessun passaggio dall'archivio classico)
      if (W.tvaAtlas2 && W.tvaAtlas2.openChar) { push(c.name.length > 22 ? c.name.slice(0, 21) + '…' : c.name); return W.tvaAtlas2.openChar(id, true); }
      push(c.name.length > 22 ? c.name.slice(0, 21) + '…' : c.name);
      W.marvelChiudiOverlay();
      var t = $('tvaArchivesToggle'); if (t) t.checked = true;
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('atlante');
      inRouter = true; try { W.mvNavigateTo(id, 'char', c.name.charAt(0).toUpperCase()); } finally { inRouter = false; }
      return true;
    }
    function goFilter(uid) {
      if (!UNI[uid]) return false;
      push('Atlante');
      W.marvelEsploraUniverso(uid, UNI[uid].nome || uid);
      return true;
    }
    function openAncestors(elm) { for (var a = elm.parentElement; a; a = a.parentElement) if (a.tagName === 'DETAILS') a.setAttribute('open', ''); }
    W.tvaSettleScroll = function (elm) { openAncestors(elm); waitVisible(elm, function () { settle(elm, topMin()); }); };
    // mvNavigateTo (ricerca, link nelle schede) entra nello stack: dopo "Indietro" si torna dove si era
    var inRouter = false, origNav = W.mvNavigateTo;
    var ARCMAP = { org: 'org', art: 'art', pia: 'luo', luo: 'luo', evt: 'evt', bat: 'evt' };
    function wrapNav(orig) {
      var w = function (id, type, name) {
        // schede d'archivio: aprono sempre la scheda nativa dell'Atlante (nessun passaggio dall'archivio classico)
        if (!inRouter && W.tvaAtlas2 && W.tvaGo) {
          var ok = false;
          try {
            if (type === 'char') ok = W.tvaGo('char', id);
            else if (type === 'uni') ok = W.tvaGo('uni', id);
            else if (type === 'att') ok = W.tvaGo('att', id);
            else if (ARCMAP[type]) ok = W.tvaGo('arc', ARCMAP[type] + ':' + id);
          } catch (eM) { ok = false; }
          if (ok) return true;
        }
        if (!inRouter) { var e = $(id); var t = e && e.querySelector('.title'); push(t ? (t.textContent.length > 22 ? t.textContent.slice(0, 21) + '…' : t.textContent) : ''); }
        return orig.apply(this, arguments);
      };
      w.__tvaW = true; return w;
    }
    // mvNavigateTo puo' essere (ri)definita dopo questo blocco: l'assegnazione viene intercettata e avvolta una sola volta
    (function () {
      var cur = typeof origNav === 'function' ? wrapNav(origNav) : origNav;
      try {
        Object.defineProperty(W, 'mvNavigateTo', { configurable: true, enumerable: true,
          get: function () { return cur; }, set: function (f) { cur = (typeof f === 'function' && !f.__tvaW) ? wrapNav(f) : f; } });
      } catch (eDp) { if (typeof cur === 'function') W.mvNavigateTo = cur; }
    })();
    W.mvNavigate = function (id, type, name) { W.mvNavigateTo(id, type, name); return false; };
    // dossier degli archivi TVA (Organizzazioni, Artefatti, Eventi, Luoghi): id = «categoria:scheda»
    function goArc(id, opt) {
      var k = id.indexOf(':'), cat = id.slice(0, k), eid = id.slice(k + 1);
      if (!W.tvaAtlas2 || !W.tvaAtlas2.openArc || !$(eid) && !W.tvaAtlas2.arcModel().byId[eid]) return false;
      if (!(opt && opt.nopush)) push(eid);
      return W.tvaAtlas2.openArc(cat, eid, true);
    }
    W.tvaGo = function (kind, id, opt) {
      if (kind === 'arc') return goArc(id, opt);
      if (kind === 'item') return goItem(id, opt);
      if (kind === 'uni') return goUni(id, opt);
      if (kind === 'char') return goChar(id);
      if (kind === 'att') { if (!W.tvaAtlas2 || !W.tvaAtlas2.openAtt) return false; if (!(opt && opt.nopush)) push('Attori'); return W.tvaAtlas2.openAtt(id, true); }
      if (kind === 'filter') return goFilter(id);
      return false;
    };
    W.tvaBack = function () { return goBack(); };
    // «App Marvel» dall'Atlante immersivo: torna alla schermata da cui si e' entrati (ultimo snapshot senza Atlante),
    // scartando i livelli intermedi; la cronologia del browser viene riallineata con history.go(-k).
    W.tvaTornaApp = function () {
      var i = stack.length - 1; while (i >= 0 && stack[i].a2) i--;
      if (i < 0) return false;
      var k = stack.length - i, s = stack[i]; stack.length = i; syncBack();
      try { history.go(-k); } catch (e) {}
      restore(s); return true;
    };
    W.tvaPushNav = function (lbl) { push(lbl); };
    W.tvaNavStato = function () { return { depth: stack.length, last: stack.length ? stack[stack.length - 1] : null, labels: stack.map(function (x) { return x.lbl || ''; }) }; };

    // le sei tab in basso sono navigazione di primo livello: azzerano la cronologia interna
    D.addEventListener('click', function (ev) { if (ev.target.closest && ev.target.closest('.app-tab')) resetStack(); }, true);
    D.addEventListener('click', function (ev) {
      var a = ev.target.closest ? ev.target.closest('[data-go]') : null;
      if (!a) return;
      var p = (a.getAttribute('data-go') || '').split(':');
      if (p.length < 2) return;
      ev.preventDefault(); ev.stopPropagation();
      W.tvaGo(p[0], p.slice(1).join(':'));
    }, true);

    /* ---------- 3. COLLEGAMENTI NELLE SCHEDE ---------- */
    function el(tag, cls, txt) { var n = D.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }
    function chip(label, go, extra, cls) {
      var b = el('button', 'tva-chip' + (cls ? ' ' + cls : ''));
      b.type = 'button'; b.setAttribute('data-go', go);
      b.appendChild(el('span', 'tva-chip-t', label));
      if (extra) b.appendChild(el('small', '', extra));
      return b;
    }
    function row(k) { var r = el('div', 'detail-row tva-row'); r.appendChild(el('span', 'detail-k', k)); var v = el('span', 'detail-v'); r.appendChild(v); return { r: r, v: v }; }

    // 3a. schede personaggio: N°xxx -> scheda del titolo; UNIVERSI (solo testo semplice) -> scheda universo
    Object.keys(CH).forEach(function (cid) {
      var li = CH[cid].li;
      Array.prototype.forEach.call(li.querySelectorAll('.detail-row'), function (r) {
        var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v');
        if (!k || !v || v.getAttribute('data-tva-lk')) return;
        if (/APP\./.test(k.textContent)) {
          v.setAttribute('data-tva-lk', '1');
          var w = D.createTreeWalker(v, NodeFilter.SHOW_TEXT, null), nodes = [], n;
          while ((n = w.nextNode())) nodes.push(n);
          nodes.forEach(function (tn) {
            if (tn.parentNode.closest && tn.parentNode.closest('a')) return;
            var txt = tn.nodeValue, re = /N°(\d{3})/g, last = 0, mm, frag = D.createDocumentFragment(), any = false;
            while ((mm = re.exec(txt))) {
              var fid = FV(mm[1]); if (!TIT['item-' + fid]) continue;
              any = true;
              if (mm.index > last) frag.appendChild(D.createTextNode(txt.slice(last, mm.index)));
              var a = el('a', 'tva-lk', mm[0]); a.href = 'javascript:void(0)'; a.setAttribute('data-go', 'item:item-' + fid);
              a.title = 'Apri la scheda: ' + TIT['item-' + fid].title;
              frag.appendChild(a); last = mm.index + mm[0].length;
            }
            if (any) { if (last < txt.length) frag.appendChild(D.createTextNode(txt.slice(last))); tn.parentNode.replaceChild(frag, tn); }
          });
        } else if (/^UNIVERSI/.test(k.textContent.trim()) && !v.children.length) {
          v.setAttribute('data-tva-lk', '1');
          var parts = v.textContent.split('·'), frag2 = D.createDocumentFragment(), anyU = false;
          parts.forEach(function (p, i) {
            if (i) frag2.appendChild(D.createTextNode(' · '));
            var uid = uidDaTesto(p);
            if (uid && $(uid)) { anyU = true; var a2 = el('a', 'tva-lk', p.trim()); a2.href = 'javascript:void(0)'; a2.setAttribute('data-go', 'uni:' + uid); frag2.appendChild(a2); }
            else frag2.appendChild(D.createTextNode(p.trim()));
          });
          if (anyU) { v.textContent = ''; v.appendChild(frag2); }
        }
      });
    });

    // 3a-bis. schede personaggio: origine dichiarata e universi in cui compare (da atlasData), con link reciproco alla scheda universo
    function charChips(r, ids) { r.v.classList.add('tva-chips'); ids.forEach(function (u) { r.v.appendChild(chip(UNI[u].nome || u, 'uni:' + u)); }); }
    Object.keys(CH).forEach(function (cid) {
      var li = CH[cid].li, panel = li.querySelector('.detail-panel');
      if (!panel || li.getAttribute('data-tva-atl')) return;
      var org = (CO[cid] || []).filter(function (u) { return $(u); });
      var pres = (CHAPP[cid] || []).filter(function (u) { return UNI[u] && $(u) && org.indexOf(u) === -1; });
      if (!org.length && !pres.length) return;
      li.setAttribute('data-tva-atl', '1');
      if (org.length) {
        var r1 = row('ORIGINE (ATLANTE)'); charChips(r1, org);
        r1.v.appendChild(el('div', 'tva-note', 'Continuità d’origine dichiarata dalla guida.'));
        panel.appendChild(r1.r);
      }
      if (pres.length) {
        var r2 = row('COMPARE ANCHE IN (ATLANTE)'); charChips(r2, pres);
        r2.v.appendChild(el('div', 'tva-note', 'Universi della riga UNIVERSI in cui compare' + (org.length ? ', oltre all’origine' : '') + ': indica presenza, non appartenenza.'));
        panel.appendChild(r2.r);
      }
    });

    // 3b. schede titolo (Timeline): universi + personaggi in archivio
    TITLIST.forEach(function (e) {
      var panel = e.li.querySelector('.detail-panel'); if (!panel || e.li.getAttribute('data-tva-net')) return;
      e.li.setAttribute('data-tva-net', '1');
      var any = false;
      if (e.unis.length) {
        var rl = ruoloDi(e);
        var u = row(rl === 'crossover' ? 'CROSSOVER · UNIVERSI COINVOLTI' : (rl === 'variante' ? 'UNIVERSO (VERSIONE ALTERNATIVA)' : 'UNIVERSO DI APPARTENENZA'));
        e.unis.forEach(function (uid) { if (UNI[uid] && $(uid)) u.v.appendChild(chip(UNI[uid].nome || uid, 'uni:' + uid)); });
        if (rl === 'crossover') u.v.appendChild(el('div', 'tva-note', 'Crossover: coinvolge più universi. I dati della guida non indicano un universo principale, quindi il titolo non è assegnato a uno solo.'));
        else if (rl === 'variante') u.v.appendChild(el('div', 'tva-note', 'Versione alternativa di un titolo già presente: non è conteggiata tra i titoli dell’universo.'));
        u.v.classList.add('tva-chips'); panel.appendChild(u.r); any = true;
      }
      var amb = e.kind === 'item' ? AMBI[e.num] : '';
      if (amb) {
        var ar = row('AMBIENTAZIONE'); ar.v.textContent = amb;
        ar.v.appendChild(el('div', 'tva-note', 'Luogo ed epoca della storia (testo della guida): non indica un universo.'));
        panel.appendChild(ar.r); any = true;
      }
      var cl = ITEMCH[e.id];
      if (cl && cl.length) {
        var p = row('PERSONAGGI IN ARCHIVIO'), LIM = 10;
        p.v.classList.add('tva-chips');
        cl.forEach(function (cid, i) {
          var c = chip(CH[cid].name, 'char:' + cid); if (i >= LIM) { c.hidden = true; c.setAttribute('data-more', '1'); } p.v.appendChild(c);
        });
        if (cl.length > LIM) {
          var more = el('button', 'tva-chip tva-more', '+' + (cl.length - LIM) + ' altri'); more.type = 'button';
          more.addEventListener('click', function (ev) { ev.stopPropagation(); Array.prototype.forEach.call(p.v.querySelectorAll('[data-more]'), function (c) { c.hidden = false; }); more.remove(); });
          p.v.appendChild(more);
        }
        p.v.appendChild(el('div', 'tva-note', 'Elenco delle schede che citano questo titolo tra le apparizioni: indica la presenza, non l’appartenenza a un universo.'));
        panel.appendChild(p.r); any = true;
      }
      if (any) panel.setAttribute('data-tva-linked', '1');
    });

    // 3c. schede universo (Atlante): titoli, ordine, progresso, personaggi, collegamenti
    function progUni(uid) {
      var t = titoliDi(uid), v = 0;
      t.forEach(function (e) { var c = e.li.querySelector('.watch-check, .anim-watch-check'); if (c && c.checked) v++; });
      return { n: t.length, v: v, k: t.filter(eCross).length };
    }
    var PROGEL = [];
    function refreshProg() {
      PROGEL.forEach(function (o) {
        var p = progUni(o.uid);
        o.el.textContent = p.n ? (p.v + '/' + p.n + ' visti' + (p.k ? ' · ' + p.k + ' crossover' : '')) : 'Nessun titolo associato nei dati';
        if (o.bar) o.bar.style.width = (p.n ? Math.round(p.v / p.n * 100) : 0) + '%';
      });
    }
    Object.keys(UNI).forEach(function (uid) {
      var li = $(uid); if (!li) return;
      var panel = li.querySelector('.detail-panel'); if (!panel || li.getAttribute('data-tva-net')) return;
      li.setAttribute('data-tva-net', '1');
      var tt = titoliDi(uid);
      var r1 = row('TITOLI ASSOCIATI');
      var prog = el('div', 'tva-prog-t'); var bar = el('div', 'tva-prog'); var fill = el('i'); bar.appendChild(fill);
      r1.v.appendChild(prog); r1.v.appendChild(bar);
      PROGEL.push({ uid: uid, el: prog, bar: fill });
      if (tt.length) {
        var prim = tt.filter(function (e) { return !eCross(e); }), cro = tt.filter(eCross), vv = TITLIST.filter(function (e) { return e.variant && e.unis.indexOf(uid) !== -1; });
        if (prim.length) {
          r1.v.appendChild(el('div', 'tva-sub', 'DI APPARTENENZA (' + prim.length + ')'));
          var ch = el('div', 'tva-chips');
          prim.forEach(function (e) { ch.appendChild(chip(e.title, 'item:' + e.id, e.num ? 'N°' + VN(e.num) : '')); });
          r1.v.appendChild(ch);
        }
        if (cro.length) {
          r1.v.appendChild(el('div', 'tva-sub', 'CROSSOVER (' + cro.length + ') · coinvolgono più universi'));
          var ch2 = el('div', 'tva-chips');
          cro.forEach(function (e) { ch2.appendChild(chip(e.title, 'item:' + e.id, (e.num ? 'N°' + VN(e.num) : '') + ' ↗', 'tva-k')); });
          r1.v.appendChild(ch2);
          r1.v.appendChild(el('div', 'tva-note', 'I dati non indicano un universo principale per i crossover: compaiono in ciascun universo coinvolto, senza essere assegnati a uno solo.'));
        }
        if (vv.length) {
          r1.v.appendChild(el('div', 'tva-sub', 'VERSIONE ALTERNATIVA · non conteggiata'));
          var ch3 = el('div', 'tva-chips');
          vv.forEach(function (e) { ch3.appendChild(chip(e.title, 'item:' + e.id, e.num ? 'N°' + VN(e.num) : '')); });
          r1.v.appendChild(ch3);
        }
        r1.v.appendChild(el('div', 'tva-note', 'Ordine: quello della guida (N°).'));
        var bt = el('button', 'tva-btn', 'Mostra solo questi titoli in Timeline'); bt.type = 'button'; bt.setAttribute('data-go', 'filter:' + uid);
        r1.v.appendChild(bt);
      } else {
        r1.v.appendChild(el('div', 'tva-note', 'Nessun titolo è associato direttamente a questo universo nei dati della guida.'));
      }
      panel.appendChild(r1.r);
      // collegamenti con altre realtà (solo via titoli condivisi nei dati)
      var link = {};
      tt.forEach(function (e) { e.unis.forEach(function (o) { if (o !== uid && UNI[o]) (link[o] = link[o] || []).push(e.num || e.title); }); });
      var lk = Object.keys(link);
      if (lk.length) {
        var r2 = row('COLLEGAMENTI CON ALTRE REALTÀ'); r2.v.classList.add('tva-chips');
        lk.forEach(function (o) { r2.v.appendChild(chip(UNI[o].nome || o, 'uni:' + o, 'via ' + link[o].map(function (x) { return /^\d+$/.test(x) ? 'N°' + VN(x) : x; }).slice(0, 3).join(', '))); });
        r2.v.appendChild(el('div', 'tva-note', 'Universi che compaiono negli stessi titoli (crossover) secondo i dati.'));
        panel.appendChild(r2.r);
      }
      function charsRow(label, ids, note, showOrig) {
        if (!ids.length) return;
        var r3 = row(label + ' (' + ids.length + ')'), LIM2 = 10; r3.v.classList.add('tva-chips');
        ids.forEach(function (cid, i) {
          var o = showOrig ? (CO[cid] || []).filter(function (u) { return u !== uid; }) : [];
          var c = chip(CH[cid].name, 'char:' + cid, o.length ? 'orig.: ' + o.map(breve).slice(0, 2).join(', ') : (showOrig ? 'orig.: non indicata' : ''));
          if (i >= LIM2) { c.hidden = true; c.setAttribute('data-more', '1'); } r3.v.appendChild(c);
        });
        if (ids.length > LIM2) {
          var m2 = el('button', 'tva-chip tva-more', '+' + (ids.length - LIM2) + ' altri'); m2.type = 'button';
          m2.addEventListener('click', function (ev) { ev.stopPropagation(); Array.prototype.forEach.call(r3.v.querySelectorAll('[data-more]'), function (c) { c.hidden = false; }); m2.remove(); });
          r3.v.appendChild(m2);
        }
        r3.v.appendChild(el('div', 'tva-note', note));
        panel.appendChild(r3.r);
      }
      charsRow('PERSONAGGI ORIGINARI', origineDi(uid), 'Continuità d’origine dichiarata dalla guida per questo universo.', false);
      charsRow('PERSONAGGI PRESENTI', presentiDi(uid), 'Compaiono in questo universo secondo la riga UNIVERSI della scheda, ma la loro origine dichiarata è altrove: presenza, non appartenenza.', true);
      var fams = Object.keys(FAM).filter(function (f) { return (FAM[f].universi || []).indexOf(uid) !== -1; });
      if (fams.length) {
        var r4 = row('FAMIGLIA'); r4.v.textContent = fams.map(function (f) { return (FAM[f].ic || '') + ' ' + FAM[f].nome; }).join(' · '); panel.appendChild(r4.r);
      }
    });
    refreshProg();
    // 3d. Missioni -> titoli richiesti -> schede (solo missioni con un insieme di titoli noto; la segreta resta segreta)
    function renderMissioni() {
      var info = W.marvelMissioniInfo; if (!info) return;
      function box(rowId, ids, label) {
        var row = $(rowId); if (!row) return;
        var old = row.querySelector('.tva-mis'); if (old) old.remove();
        if (row.classList.contains('missione-completa')) return;
        var todo = ids.filter(function (id) { var e = TIT['item-' + id]; if (!e || e.variant) return false; var c = e.li.querySelector('.watch-check'); return !(c && c.checked); });
        if (!todo.length) return;
        var b = el('div', 'tva-mis'); b.appendChild(el('div', 'tva-mis-l', label + ' (' + todo.length + ')'));
        var cc = el('div', 'tva-chips'), LIM = 6;
        todo.forEach(function (id, i) { var c = chip(TIT['item-' + id].title, 'item:item-' + id, 'N°' + VN(id)); if (i >= LIM) { c.hidden = true; c.setAttribute('data-more', '1'); } cc.appendChild(c); });
        if (todo.length > LIM) { var mo = el('button', 'tva-chip tva-more', '+' + (todo.length - LIM) + ' altri'); mo.type = 'button'; mo.addEventListener('click', function () { Array.prototype.forEach.call(cc.querySelectorAll('[data-more]'), function (x) { x.hidden = false; }); mo.remove(); }); cc.appendChild(mo); }
        b.appendChild(cc); row.appendChild(b);
      }
      if (info.tematica) box('missioneTematica', info.tematica.ids || [], 'Titoli che la completano');
      if (info.saga) box('missioneSaga', info.saga.ids || [], 'Titoli ancora da vedere');
    }
    D.addEventListener('tva:missioni', renderMissioni);
    renderMissioni();
    D.addEventListener('change', function (ev) {
      var t = ev.target; if (t && t.classList && (t.classList.contains('watch-check') || t.classList.contains('anim-watch-check'))) setTimeout(refreshProg, 30);
    }, true);
    D.addEventListener('toggle', function (ev) { if (ev.target && ev.target.tagName === 'DETAILS') refreshProg(); }, true);
    W.tvaRefreshProg = refreshProg;
    ensureBack();
  } catch (eNet) { if (window.console) console.error('Marvel guide - tvaNet:', eNet); }
})();
