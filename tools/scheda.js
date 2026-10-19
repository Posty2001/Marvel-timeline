/* ===== TVA ARCHIVES — Schede native: Personaggi, Cronologie tematiche, Alberi genealogici, Attori, Percorsi =====
   Sostituisce i passaggi verso l'«Archivio classico». Nessun dato duplicato: le schede della guida (nel DOM classico, ora solo sorgente dati)
   vengono lette e presentate nell'interfaccia TVA; ogni campo, ID e collegamento viene conservato. */
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
    var $ = a.$, el = a.el, btn = a.btn, ST = a.ST, IDX = a.IDX, body = a.body, PTIPO = a.PTIPO || {}, PSUB = a.PSUB || {};
    var ATLP = {};
    try { (JSON.parse($('atlasData').textContent).personaggi || []).forEach(function (p) { ATLP[p.id] = p; }); } catch (eAt) {}

    /* ---------- utilità ---------- */
    function strip(t) { return (t || '').replace(/[\u{1F000}-\u{1FFFF}←-➿️‍]/gu, '').replace(/\s+/g, ' ').trim(); }
    function cloneInto(dst, src) { Array.prototype.forEach.call(src.childNodes, function (n) { dst.appendChild(n.cloneNode(true)); }); return dst; }
    function goBtn(kind, id, label, cls) { var b = btn(cls || 'a2-chip', label); b.setAttribute('data-go', kind + ':' + id); return b; }
    // «N°095» nel testo -> pulsante che apre la scheda del titolo (solo se il titolo esiste)
    function linkN(root) {
      var w = D.createTreeWalker(root, NodeFilter.SHOW_TEXT, null), nodes = [], n;
      while ((n = w.nextNode())) if (/N°\s*\d{3}/.test(n.nodeValue) && !(n.parentNode.closest && n.parentNode.closest('a,button'))) nodes.push(n);
      nodes.forEach(function (t) {
        var txt = t.nodeValue, frag = D.createDocumentFragment(), last = 0, m, re = /N°\s*(\d{3})/g;
        while ((m = re.exec(txt))) {
          var id = 'item-' + FV(m[1]); if (!IDX.titoli[id]) continue;
          frag.appendChild(D.createTextNode(txt.slice(last, m.index)));
          var b = el('button', 'a2-n', 'N°' + m[1]); b.type = 'button'; b.setAttribute('data-go', 'item:' + id); b.title = IDX.titoli[id].title; b.setAttribute('aria-label', 'Apri ' + IDX.titoli[id].title);
          frag.appendChild(b); last = m.index + m[0].length;
        }
        if (!last) return; frag.appendChild(D.createTextNode(txt.slice(last))); t.parentNode.replaceChild(frag, t);
      });
      return root;
    }
    function model() { return A.arcModel ? A.arcModel() : null; }
    function charName(id) { var c = IDX.personaggi[id]; return c ? c.name : id; }
    function openScreen(screen, patch, fromRouter) {
      if (!fromRouter && a.tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante');
      ST.screen = screen; Object.keys(patch || {}).forEach(function (k) { ST[k] = patch[k]; });
      if (!a.tog.checked) a.show(); a.draw(); a.setScroll(0); return true;
    }

    /* ---------- Scheda personaggio ---------- */
    var KEYS = {
      'PRIMA APP.': ['Prima apparizione', 0], 'ULTIMA APP.': ['Ultima apparizione', 0], 'ALTRE APP.': ['Altre apparizioni', 0], 'COMPARE ANCHE IN (ATLANTE)': ['Compare anche in', 0],
      'UNIVERSI': ['Universi', 1], 'ORIGINE (ATLANTE)': ['Origine', 1],
      'POTERI': ['Poteri', 2], 'POTENZA TVA (ATLANTE)': ['Potenza TVA', 2], 'ENTITÀ, SPECIE E ARTI (ATLANTE)': ['Entità, specie e arti', 2],
      'CORRELATI': ['Correlati', 3], 'RELAZIONI': ['Relazioni', 3], 'COLLEGAMENTI': ['Collegamenti', 3], 'ORGANIZZAZIONI (ATLANTE)': ['Organizzazioni', 3], 'CITATO IN (ATLANTE)': ['Citato in', 3],
      'NEI FUMETTI': ['Nei fumetti', 4], 'DA LEGGERE': ['Da leggere', 4]
    };
    var GTIT = ['Apparizioni', 'Universi e origine', 'Poteri e natura', 'Legami', 'Nei fumetti'];
    function kv(label, vNode) {
      var d = el('div', 'a2-kv'); d.appendChild(el('span', 'a2-k', label)); var v = el('div', 'a2-v'); cloneInto(v, vNode); linkN(v); d.appendChild(v); return d;
    }
    function renderChar() {
      var id = ST.eid, c = IDX.personaggi[id];
      if (!c || !c.li) { ST.screen = 'personaggi'; return a.draw(); }
      body.className = 'a2-scroll a2-dossier a2-char'; body.textContent = ''; a.setTitle(c.name, 'Personaggi');
      var tipo = PTIPO[id] || 'personaggio', sub = PSUB[id] || '';
      var hero = el('section', 'a2-hero a2-arc-hero a2-char-hero'); a.heroImg(hero, 'personaggi'); hero.appendChild(a.cover('chr', id, c.name, 'a2-cov-hero'));
      hero.appendChild(el('span', 'a2-kick', (tipo === 'variante' ? 'VARIANTE' : tipo === 'aggregata' ? 'VOCE AGGREGATA' : tipo === 'segnaposto' ? 'VOCE GENERICA' : 'PERSONAGGIO')));
      hero.appendChild(el('h2', '', c.name));
      var rows = Array.prototype.filter.call(c.li.querySelectorAll('.detail-panel > .detail-row'), function (r) { return r.querySelector('.detail-k') && r.querySelector('.detail-v'); });
      var by = {}, other = [], first = null;
      rows.forEach(function (r) {
        var k = strip(r.querySelector('.detail-k').textContent).toUpperCase(), m = KEYS[k];
        if (k === 'PRIMA APP.') first = r.querySelector('.detail-v');
        if (m) (by[m[1]] = by[m[1]] || []).push([m[0], r]); else other.push([strip(r.querySelector('.detail-k').textContent), r]);
      });
      if (first) { var fl = el('p', 'a2-descr'); fl.appendChild(D.createTextNode('Prima apparizione: ')); cloneInto(fl, first); linkN(fl); hero.appendChild(fl); }
      body.appendChild(hero);
      var at = ATLP[id];
      if (sub && /^(incarnazion|versione|ambiguo|jolly|elenco)/.test(sub) || tipo === 'variante' || tipo === 'aggregata') {
        body.appendChild(a.info('Voce speciale della guida (' + sub.replace(/-/g, ' ') + '): raccoglie più versioni o incarnazioni; non sono fuse in un unico personaggio.'));
      }
      if (at && at.dubbio && at.dubbio.length) body.appendChild(a.info('Dato non confermato: ' + at.dubbio.map(function (d) { return typeof d === 'string' ? d : (d.nota || d.motivo || JSON.stringify(d)); }).join('; ') + '.'));
      for (var g = 0; g < GTIT.length; g++) {
        if (!by[g] || !by[g].length) continue;
        var s = a.sec(GTIT[g]); if (g === 0 && !by[0].filter(function (p) { return p[0] !== 'Prima apparizione'; }).length) continue;
        by[g].forEach(function (p) { if (g === 0 && p[0] === 'Prima apparizione') return; s.appendChild(kv(p[0], p[1].querySelector('.detail-v'))); });
        body.appendChild(s);
      }
      if (other.length) { var so = a.sec('Altro dalla guida'); other.forEach(function (p) { so.appendChild(kv(p[0], p[1].querySelector('.detail-v'))); }); body.appendChild(so); }
      var foot = el('section', 'a2-sec a2-foot');
      foot.appendChild(btn('a2-ghost', 'Tutti i personaggi', function () { a.nav('personaggi', { pf: 'tutti', pq: '' }); }));
      body.appendChild(foot);
    }
    A.openChar = function (id, fromRouter) { if (!IDX.personaggi[id]) return false; return openScreen('char', { eid: id }, fromRouter); };

    /* ---------- Cronologie tematiche ---------- */
    function chronoList() {
      var o = [], seen = {};
      Array.prototype.forEach.call(D.querySelectorAll('#tvaArchivesOverlayEl [data-target^="chrono-"]'), function (b) { var t = b.getAttribute('data-target'); if (!seen[t] && $(t)) { seen[t] = 1; o.push([t, strip(b.textContent)]); } });
      return o;
    }
    function tabs(list, cur, onPick, label) {
      var fl = el('div', 'a2-filters a2-tabs'); fl.setAttribute('role', 'group'); fl.setAttribute('aria-label', label);
      list.forEach(function (p) {
        var b = btn('a2-f' + (p[0] === cur ? ' on' : ''), p[1], function () { onPick(p[0]); }); b.setAttribute('aria-pressed', p[0] === cur ? 'true' : 'false'); fl.appendChild(b);
      });
      return fl;
    }
    function timeline(ol) {
      var out = el('ol', 'a2-tl');
      Array.prototype.forEach.call(ol.children, function (li) {
        var n = el('li', 'a2-tl-i'); cloneInto(n, li);
        var b = n.firstElementChild;
        if (b && b.tagName === 'B') {
          // «Titolo — testo»: il titolo diventa intestazione del passaggio, il trattino iniziale e il <br> si tolgono
          var nx = b.nextSibling; if (nx && nx.nodeType === 1 && nx.tagName === 'BR') { n.removeChild(nx); nx = b.nextSibling; }
          if (nx && nx.nodeType === 3) nx.nodeValue = nx.nodeValue.replace(/^\s*[—–-]\s*/, '');
        }
        linkN(n); out.appendChild(n);
      });
      return out;
    }
    function togButton(lab) {
      var f = lab.getAttribute('for'), t = f && $(f); if (!t) return null;
      return btn('a2-primary a2-tl-go', strip(lab.textContent).replace(/\s*[→▸›]+$/, ''), function () { a.run(['tog', f]); });
    }
    function renderChrono() {
      var list = chronoList(), cur = ST.eid && $(ST.eid) && /^chrono-/.test(ST.eid) ? ST.eid : (list[0] && list[0][0]), host = cur && $(cur);
      body.className = 'a2-scroll a2-doc a2-chrono'; body.textContent = ''; a.setTitle('Cronologie', 'Multiverso e Tempo');
      if (!host) { body.appendChild(a.heading('CRONOLOGIE', 'Cronologie tematiche', 'Nessuna cronologia disponibile.')); return; }
      body.appendChild(tabs(list, cur, function (id) { ST.eid = id; a.draw(); a.setScroll(0); }, 'Cronologia'));
      var kids = Array.prototype.slice.call(host.children), title = kids.filter(function (k) { return k.classList.contains('chrono-panel-title'); })[0];
      body.appendChild(a.heading('CRONOLOGIE TEMATICHE', title ? title.textContent : 'Cronologia', 'Passaggi nell’ordine della guida; tocca un N° per aprire il titolo.'));
      var first = true;
      kids.forEach(function (k) {
        if (k.classList.contains('chrono-panel-title')) { if (first) { first = false; return; } body.appendChild(el('h3', 'a2-h3', k.textContent)); return; }
        if (k.tagName === 'OL') { var s = el('section', 'a2-sec a2-sec-tl'); s.appendChild(timeline(k)); body.appendChild(s); return; }
        if (k.tagName === 'LABEL') { var b = togButton(k); if (b) { var w = el('div', 'a2-tl-act'); w.appendChild(b); body.appendChild(w); } return; }
        if (k.tagName === 'P' || k.tagName === 'DIV') { var p = el('p', 'a2-note'); cloneInto(p, k); linkN(p); body.appendChild(p); }
      });
    }

    /* ---------- Alberi genealogici ---------- */
    function treeList() {
      var o = [], seen = {};
      Array.prototype.forEach.call(D.querySelectorAll('#tvaArchivesOverlayEl [data-target^="tree-"]'), function (b) { var t = b.getAttribute('data-target'); if (!seen[t] && $(t)) { seen[t] = 1; o.push([t, strip(b.textContent)]); } });
      return o;
    }
    function resolveCharByName(name) {
      var n = (name || '').trim().toLowerCase(), hit = [];
      Object.keys(IDX.personaggi).forEach(function (id) { var p = IDX.personaggi[id], nm = (p.name || '').toLowerCase(); if (nm === n || nm.indexOf(n + '/') === 0) hit.push(id); });
      return hit.length === 1 ? hit[0] : null;
    }
    function titlesFromNote(note) {
      var m = (note || '').match(/\(([^()]*)\)\.?\s*$/) || (note || '').match(/\(([^()]*)\)/); if (!m) return [];
      var out = [];
      m[1].split(/,\s*/).forEach(function (raw) {
        var nm = raw.replace(/\s*(?:\d{4}(?:-\d{2})?)\s*$/, '').replace(/^universo\s+\S+\s*,?\s*/i, '').trim().toLowerCase(); if (!nm) return;
        var hit = Object.keys(IDX.titoli).map(function (k) { return IDX.titoli[k]; }).filter(function (t) { var tt = t.title.toLowerCase(); return tt === nm || tt.slice(-nm.length - 2) === ': ' + nm; });
        if (hit.length === 1) out.push(hit[0]);
      });
      return out;
    }
    function continuityBox(note) {
      var head = el('div', 'a2-ft-cont'), nt = el('p', 'a2-note'), ts = titlesFromNote(note), us = {};
      ts.forEach(function (t) { (t.unis || []).forEach(function (u) { us[u] = 1; }); });
      var ks = Object.keys(us);
      head.appendChild(el('span', 'a2-ft-contl', 'CONTINUITÀ'));
      if (ks.length) { var row = el('div', 'a2-chips'); ks.forEach(function (u) { row.appendChild(goBtn('uni', u, IDX.breve ? IDX.breve(u) : u, 'tva-chip')); }); head.appendChild(row); nt.textContent = 'Continuità = universi dei titoli in cui la guida mostra questi legami (' + ts.map(function (t) { return t.title; }).join(', ') + '). Altre continuità (Legacy o alternative) non vengono mescolate.'; }
      else { head.appendChild(el('span', 'a2-note', ' non indicata dalla guida per questo gruppo.')); nt.textContent = ''; }
      return { head: head, note: nt };
    }
    function legendBox() {
      var lg = el('div', 'a2-ft-legend'); lg.setAttribute('aria-label', 'Legenda delle linee');
      var items = [['ft-marr2', 'Matrimonio'], ['ft-partner2', 'Compagno/a'], ['ft-par2', 'Genitore → figlio'], ['ft-adopt2', 'Figlio adottivo'], ['ft-sib2', 'Fratelli']];
      items.forEach(function (it) { var s = el('span', 'a2-ft-li'); var sv = D.createElementNS('http://www.w3.org/2000/svg', 'svg'); sv.setAttribute('viewBox', '0 0 34 12'); sv.setAttribute('width', '34'); sv.setAttribute('height', '12'); sv.setAttribute('aria-hidden', 'true');
        if (it[0] === 'ft-marr2') { [3, 9].forEach(function (y) { var l = D.createElementNS('http://www.w3.org/2000/svg', 'line'); l.setAttribute('x1', 1); l.setAttribute('x2', 33); l.setAttribute('y1', y); l.setAttribute('y2', y); l.setAttribute('class', 'ft-e ft-marr'); sv.appendChild(l); }); }
        else { var l2 = D.createElementNS('http://www.w3.org/2000/svg', 'line'); l2.setAttribute('x1', 1); l2.setAttribute('x2', 33); l2.setAttribute('y1', 6); l2.setAttribute('y2', 6); l2.setAttribute('class', 'ft-e ' + ({ 'ft-partner2': 'ft-partner', 'ft-par2': 'ft-par', 'ft-adopt2': 'ft-par ft-adopt', 'ft-sib2': 'ft-sib' })[it[0]]); sv.appendChild(l2); }
        s.appendChild(sv); s.appendChild(D.createTextNode(it[1])); lg.appendChild(s); });
      return lg;
    }
    function renderAlberi() {
      var list = treeList(), cur = ST.eid && $(ST.eid) && /^tree-/.test(ST.eid) ? ST.eid : (list[0] && list[0][0]), host = cur && $(cur);
      body.className = 'a2-scroll a2-doc a2-trees'; body.textContent = ''; a.setTitle('Alberi genealogici', 'Relazioni');
      body.appendChild(a.heading('IDENTITÀ E POTERE', 'Alberi genealogici', 'Le famiglie dei personaggi, limitate ai legami mostrati o confermati nella guida.'));
      if (!host) return;
      body.appendChild(tabs(list, cur, function (id) { ST.eid = id; a.draw(); a.setScroll(0); }, 'Famiglia'));
      var intro = host.querySelector(':scope > p');
      var ft = W.tvaFamTree, drawn = false;
      if (ft) {
        try {
          var M = ft.parse(host, resolveCharByName), R = ft.render(M, { label: 'Albero genealogico: ' + (list.filter(function (x) { return x[0] === cur; })[0] || [])[1] });
          var cont = continuityBox(intro ? intro.textContent : ''); body.appendChild(cont.head);
          var holder = el('div', 'a2-ft'); holder.appendChild(R.svg); body.appendChild(holder);
          if (W.tvaGraphVP) W.tvaGraphVP.attach(R.svg, { sparse: true, noLabels: true, maxZ: 4, hint: 'Pizzica per ingrandire · trascina per spostarti · tocca una persona per aprire il dossier' });
          function openNode(g) { var id = g && g.getAttribute('data-char'); if (id && A.openChar) A.openChar(id, true); }
          holder.addEventListener('click', function (ev) { var g = ev.target.closest && ev.target.closest('.ft-node.ft-link'); if (g) openNode(g); });
          holder.addEventListener('keydown', function (ev) { if (ev.key !== 'Enter' && ev.key !== ' ') return; var g = ev.target.closest && ev.target.closest('.ft-node.ft-link'); if (g) { ev.preventDefault(); openNode(g); } });
          body.appendChild(legendBox());
          body.appendChild(cont.note);
          if (intro) body.appendChild(el('p', 'a2-note', intro.textContent));
          drawn = true;
          body.appendChild(el('p', 'a2-note', 'Il diagramma rappresenta solo i legami che le schede della guida affermano esplicitamente (' + M.marriages.length + ' matrimoni, ' + M.partners.length + ' relazioni, ' + M.parents.length + ' legami genitore–figlio, ' + M.sibs.length + ' fratellanze).'));
        } catch (eFt) { if (W.console) console.error('Alberi:', eFt); }
      }
      if (!drawn && intro) body.appendChild(el('p', 'a2-note', intro.textContent));
      var det = el('details', 'a2-unconf a2-ft-det'); if (!drawn) det.open = true;
      det.appendChild(el('summary', '', 'Dettagli per persona (' + host.querySelectorAll('.tree-node').length + ')'));
      var wrap = el('div', 'a2-tree');
      Array.prototype.forEach.call(host.querySelectorAll('.tree-gen'), function (gen, gi) {
        if (gi) { var sp = el('div', 'a2-tree-link'); sp.setAttribute('aria-hidden', 'true'); wrap.appendChild(sp); }
        var g = el('div', 'a2-tgen'); g.appendChild(el('span', 'a2-tgen-l', 'Generazione ' + (gi + 1)));
        Array.prototype.forEach.call(gen.querySelectorAll('.tree-node'), function (n) {
          var card = el('div', 'a2-tnode'), nm = n.querySelector('.tree-node-name'), an = nm && nm.querySelector('a'), oc = an && an.getAttribute('onclick') || '', mm = oc.match(/mvNavigate\('([^']+)','char'/);
          if (mm && IDX.personaggi[mm[1]]) card.appendChild(goBtn('char', mm[1], nm.textContent.trim(), 'a2-tn-name'));
          else card.appendChild(el('span', 'a2-tn-name a2-tn-plain', nm ? nm.textContent.trim() : ''));
          var role = n.querySelector('.tree-node-role'), rel = n.querySelector('.tree-node-rel');
          if (role) card.appendChild(el('span', 'a2-tn-role', role.textContent.trim()));
          if (rel) card.appendChild(el('span', 'a2-tn-rel', rel.textContent.trim()));
          g.appendChild(card);
        });
        wrap.appendChild(g);
      });
      det.appendChild(wrap); body.appendChild(det);
    }

    /* ---------- Attori ---------- */
    function attLis() { return Array.prototype.slice.call(D.querySelectorAll('#tvaArchivesOverlayEl li[id^="att-"]')); }
    function attName(li) { var t = li.querySelector('.title'); return t ? t.textContent.trim() : li.id; }
    function renderAttori() {
      body.className = 'a2-scroll a2-doc a2-att'; body.textContent = ''; a.setTitle('Attori', 'Identità e Potere');
      var all = attLis().sort(function (x, y) { return attName(x).localeCompare(attName(y), 'it'); });
      body.appendChild(a.heading('IDENTITÀ E POTERE', 'Attori', all.length + ' interpreti con i ruoli e i titoli indicati dalla guida.'));
      var res = el('div', 'a2-gridwrap');
      body.appendChild(a.searchBox('a2AttSearch', ST.aq || '', function (v) { ST.aq = v; draw2(); }, 'Cerca un attore o un ruolo…'));
      body.appendChild(res);
      function draw2() {
        res.textContent = ''; var q = (ST.aq || '').trim().toLowerCase(), n = 0, list = el('div', 'a2-plist');
        all.forEach(function (li) {
          var nm = attName(li), roles = li.querySelectorAll('.readings-list li'), txt = (nm + ' ' + li.textContent).toLowerCase(); if (q && txt.indexOf(q) === -1) return; n++;
          var b = btn('a2-prow', null); b.setAttribute('data-go', 'att:' + li.id); b.appendChild(a.cover('chr', li.id, nm, 'a2-cov-xs'));
          var t = el('span', 'a2-prow-t'); t.appendChild(el('b', '', nm)); t.appendChild(el('small', '', roles.length + (roles.length === 1 ? ' ruolo' : ' ruoli'))); b.appendChild(t); list.appendChild(b);
        });
        if (!n) list.appendChild(el('p', 'a2-empty', 'Nessun attore corrisponde alla ricerca.'));
        res.appendChild(list);
      }
      draw2();
    }
    function renderAttore() {
      var li = ST.eid && $(ST.eid); if (!li || !/^att-/.test(ST.eid)) { ST.screen = 'attori'; return a.draw(); }
      var nm = attName(li); body.className = 'a2-scroll a2-dossier a2-att'; body.textContent = ''; a.setTitle(nm, 'Attori');
      var hero = el('section', 'a2-hero a2-arc-hero'); a.heroImg(hero, 'personaggi'); hero.appendChild(a.cover('chr', li.id, nm, 'a2-cov-hero'));
      hero.appendChild(el('span', 'a2-kick', 'ATTORE')); hero.appendChild(el('h2', '', nm)); body.appendChild(hero);
      var M = model(), roles = li.querySelectorAll('.readings-list li'), s = a.sec('Ruoli (' + roles.length + ')');
      Array.prototype.forEach.call(roles, function (r) {
        var d = el('div', 'a2-role'), ref = r.querySelector('.us-result-ref'), nameTxt = '';
        Array.prototype.forEach.call(r.childNodes, function (n) { if (n.nodeType === 3) nameTxt += n.nodeValue; });
        nameTxt = nameTxt.replace(/\s+/g, ' ').trim(); d.appendChild(el('b', '', nameTxt));
        if (ref) { var rf = el('span', 'a2-role-ref', ref.textContent.replace(/^\s*—\s*/, '')); linkN(rf); d.appendChild(rf); }
        if (M && M.scan) { var ks = M.scan(nameTxt, ''), cs = ks.filter(function (k) { return k[0] === 'c'; }); if (cs.length) { var ch = el('div', 'a2-chips'); cs.slice(0, 3).forEach(function (k) { ch.appendChild(goBtn('char', k.slice(2), charName(k.slice(2)))); }); d.appendChild(ch); } }
        s.appendChild(d);
      });
      body.appendChild(s);
      var foot = el('section', 'a2-sec a2-foot'); foot.appendChild(btn('a2-ghost', 'Tutti gli attori', function () { a.nav('attori', { eid: null, aq: '' }); })); body.appendChild(foot);
    }
    A.openAtt = function (id, fromRouter) { if (!$(id)) return false; return openScreen('attore', { eid: id }, fromRouter); };

    /* ---------- Incursioni e Percorsi ---------- */
    function cardByTitle(t) { return a.cardByTitle ? a.cardByTitle(t) : null; }
    function renderDoc() {
      var key = ST.eid === 'mar' ? 'mar' : 'inc', card = cardByTitle(key === 'mar' ? 'Percorso: Maratona Weekend' : 'Timeline delle Incursioni');
      body.className = 'a2-scroll a2-doc a2-' + key; body.textContent = ''; a.setTitle(key === 'mar' ? 'Maratona Weekend' : 'Incursioni', 'Cronologie');
      if (!card) { body.appendChild(a.heading('CRONOLOGIE', 'Contenuto non disponibile', '')); return; }
      var panel = card.querySelector('.detail-panel');
      if (key === 'inc') {
        var cap = panel.querySelector('.incursion-caption');
        body.appendChild(a.heading('EVENTI', 'Timeline delle Incursioni', cap ? cap.textContent : ''));
        var d = el('div', 'a2-incur'); d.setAttribute('aria-hidden', 'true'); d.innerHTML = '<span class="a2-in-a">Universo A</span><i></i><span class="a2-in-b">Universo B</span>'; body.appendChild(d);
        var ol = panel.querySelector('ol'); if (ol) { var s = el('section', 'a2-sec a2-sec-tl'); s.appendChild(timeline(ol)); body.appendChild(s); }
      } else {
        var p = panel.querySelector('p');
        body.appendChild(a.heading('PERCORSI', 'Maratona Weekend', 'Dieci film per l’arco narrativo essenziale della saga.'));
        if (p) body.appendChild(el('p', 'a2-note', strip(p.textContent)));
        var ol2 = panel.querySelector('ol'), s2 = a.sec('I dieci film'), ul = el('ol', 'a2-list');
        if (ol2) Array.prototype.forEach.call(ol2.children, function (li, i) {
          var m = li.textContent.match(/N°\s*(\d{3})/), id = m && 'item-' + FV(m[1]), e = id && IDX.titoli[id]; if (!e) { ul.appendChild(el('li', '', li.textContent)); return; }
          var c = e.li.querySelector('.watch-check, .anim-watch-check'), seen = !!(c && c.checked), li2 = el('li'), b = btn('a2-row' + (seen ? ' seen' : ''), null); b.setAttribute('data-go', 'item:' + id);
          b.appendChild(el('span', 'a2-row-n', String(i + 1))); var tx = el('span', 'a2-row-t'); tx.appendChild(el('b', '', e.title)); tx.appendChild(el('small', '', [a.tipoTitolo(e), a.anno(e), 'N°' + VN(e.num)].filter(Boolean).join(' · '))); b.appendChild(tx);
          b.appendChild(el('span', 'a2-row-s', seen ? '✓' : '○')); b.setAttribute('aria-label', e.title + (seen ? ', visto' : ', da vedere')); li2.appendChild(b); ul.appendChild(li2);
        });
        s2.appendChild(ul); body.appendChild(s2);
        var w = el('div', 'a2-tl-act'); w.appendChild(btn('a2-primary a2-tl-go', 'Apri la Timeline', function () { a.run(['tl']); })); body.appendChild(w);
      }
    }

    /* ---------- registrazione schermate, etichette ---------- */
    X.screens.char = renderChar; X.screens.chrono = renderChrono; X.screens.alberi = renderAlberi; X.screens.attori = renderAttori; X.screens.attore = renderAttore; X.screens.doc = renderDoc;
    var prevLabel = X.label;
    X.label = function (s) {
      if (s.screen === 'char') return IDX.personaggi[s.eid] ? IDX.personaggi[s.eid].name.slice(0, 22) : 'Personaggio';
      if (s.screen === 'chrono') return 'Cronologie';
      if (s.screen === 'alberi') return 'Alberi';
      if (s.screen === 'attori') return 'Attori';
      if (s.screen === 'attore') { var l = $(s.eid); return l ? attName(l).slice(0, 22) : 'Attore'; }
      if (s.screen === 'doc') return s.eid === 'mar' ? 'Maratona' : 'Incursioni';
      return prevLabel ? prevLabel(s) : null;
    };

    /* ---------- l'archivio classico non si apre più dall'interfaccia ----------
       Resta nel DOM come sorgente dei dati. Qualsiasi apertura residua (pulsanti della Home, menu, link) porta all'Atlante.
       Per i test: ?legacy=1 lo riabilita. */
    var allowLegacy = /[?&]legacy=1\b/.test(W.location.search || ''); W.__tvaLegacy = allowLegacy;
    var ct = $('tvaArchivesToggle');
    if (ct) {
      ct.addEventListener('change', function (ev) {
        if (!ct.checked || W.__tvaLegacy) return;
        ev.stopImmediatePropagation(); ct.checked = false; if (A.enter) A.enter();
      }, true);
    }
    // etichette: nessun «Database classico» nel menu; il pulsante della Home parla di Archivi TVA
    try {
      Array.prototype.forEach.call(D.querySelectorAll('label[for="tvaArchivesToggle"]'), function (l) {
        if (l.classList.contains('sidebar-archive-link')) l.style.display = 'none';
        else if (l.classList.contains('home-hub-btn')) Array.prototype.forEach.call(l.childNodes, function (n) { if (n.nodeType === 3 && /Apri Database/.test(n.nodeValue)) n.nodeValue = n.nodeValue.replace('Apri Database', 'Apri gli Archivi'); });
        else if (/Apri gli Archivi TVA/.test(l.textContent)) l.setAttribute('data-tva-redirect', '1');
      });
    } catch (eLb) {}
  } catch (eSc) { if (window.console) console.error('Marvel guide - TVA Archives (schede native):', eSc); }
})();
