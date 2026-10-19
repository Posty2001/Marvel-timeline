/* ===== TVA UNIVERSE MODEL — modello dati condiviso dei 27 universi (FASE 3A, sola lettura) =====
   Nessun dato viene copiato o inventato: il modello LEGGE le fonti esistenti (mvMapData, atlasData, indice tvaIdx, grafo storico dell'overlay Multiverso)
   e le riconcilia. Le fonti non vengono modificate. Unica tabella scritta a mano: la corrispondenza nodo-del-grafo-storico -> universo (NODE_MAP).

   CRITERIO DEI COLLEGAMENTI (un collegamento = coppia di universi, con provenienza di ogni fonte):
     Documentato nella guida (chiave interna 'confermato'): almeno un titolo (N°) citato sia dalle opere dell'Atlante (che lo assegnano a entrambi gli
                     universi) sia da un arco «crossover»/«cameo» del grafo storico, senza contraddizioni. ATTENZIONE: entrambe le fonti derivano dalla
                     guida; la concordanza NON e' una verifica canonica indipendente.
     Legacy        : presente nel grafo storico (crossover/cameo) con N° esistente, ma l'Atlante non lo riscontra e non lo contraddice. Non verificato.
     Da verificare : dati ambigui, contraddittori o insufficienti: (a) arco «previsto, non ancora mostrato»; (b) arco «crossover» del grafo il cui N° l'Atlante
                     assegna ad altri universi; (c) coppia presente SOLO nei dati dell'Atlante (la sola presenza nel database non e' una conferma canonica).
   Gli archi che toccano i nodi speciali (Void, Battleworld, Legacy isolati, Animazione) NON diventano relazioni tra universi: restano sull'entita' speciale. */
(function () {
  'use strict';
  try {
    var D = document, W = window, IDX = W.tvaIdx;
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
    if (!IDX || !$('mvMapData') || !$('atlasData')) return;
    var MV = JSON.parse($('mvMapData').textContent), ATL = JSON.parse($('atlasData').textContent);
    var UNI = MV.universi, FAM = MV.famiglie || {};
    var UIDS = Object.keys(UNI);

    /* ---- corrispondenza nodi del grafo storico -> universi (12 nodi: 8 universi + 4 entita' speciali) ---- */
    var NODE_MAP = {
      mcu: { uid: 'uni-earth-199999-mcu' }, tva: { uid: 'uni-tva-fuori-dal-tempo' }, fox: { uid: 'uni-earth-10005-fox-verse' },
      e838: { uid: 'uni-earth-838' }, e828: { uid: 'uni-earth-828' }, ssu: { uid: 'uni-sony-s-spider-man-universe-ssu' },
      garfield: { uid: 'uni-earth-120703-garfield-verse' }, raimi: { uid: 'uni-earth-96283-raimi-verse' }
    };
    /* ---- elementi speciali: NON sono tra i 27 universi; la classificazione e' editoriale e dichiarata come tale ---- */
    var SPECIAL = {
      void: { id: 'void', nome: 'Void', classe: 'luogo', classeLbl: 'Luogo', membri: [], base: '' },
      battleworld: { id: 'battleworld', nome: 'Battleworld', classe: 'realta', classeLbl: 'Realtà speciale', membri: [], base: '' },
      legacy: { id: 'legacy', nome: 'Legacy isolati', classe: 'raggruppamento', classeLbl: 'Raggruppamento editoriale',
        membri: ['uni-blade-verse', 'uni-daredevil-elektra-verse', 'uni-ghost-rider-verse', 'uni-spider-noir-verse'],
        membriIncerti: ['uni-hulk-2003-verse'],
        base: 'elencati esplicitamente nella nota del grafo storico: Blade, Daredevil/Elektra, Ghost Rider, Spider-Noir', baseIncerta: 'la descrizione del nodo cita Hulk (2003), ma la nota del grafo non lo elenca: appartenenza ambigua, non confermata' },
      animazione: { id: 'animazione', nome: 'Animazione', classe: 'raggruppamento', classeLbl: 'Raggruppamento editoriale',
        membri: (FAM.animazione && FAM.animazione.universi || []).slice(), base: 'famiglia editoriale «Animazione» di mvMapData (il nodo storico non elenca i membri)' }
    };
    Object.keys(SPECIAL).forEach(function (k) { NODE_MAP[k] = { special: k }; SPECIAL[k].membri = SPECIAL[k].membri.filter(function (u) { return UNI[u]; }); SPECIAL[k].membriIncerti = (SPECIAL[k].membriIncerti || []).filter(function (u) { return UNI[u]; }); });

    function pairKey(a, b) { return a < b ? a + '|' + b : b + '|' + a; }
    function nodeText(id) {
      var n = $('mgInfo-' + id); if (!n) return '';
      var t = n.textContent.replace(/\s+/g, ' ').trim(); return t;
    }

    /* ---- evidenze: Atlante (opere e animate con >= 2 universi) ---- */
    var OPERA = {}; (ATL.opere || []).forEach(function (o) { OPERA[o.id] = o; });
    var EV = {}; // pairKey -> { a, b, atl: {num: ruolo}, lg: [{tipo, items, nodeA, nodeB}] }
    function ev(a, b) { var k = pairKey(a, b); return EV[k] || (EV[k] = { a: a < b ? a : b, b: a < b ? b : a, atl: {}, lg: [] }); }
    (ATL.opere || []).forEach(function (o) {
      var u = (o.universi || []).filter(function (x) { return UNI[x]; });
      for (var i = 0; i < u.length; i++) for (var j = i + 1; j < u.length; j++) ev(u[i], u[j]).atl[o.id] = o.ruolo || 'crossover';
    });
    (ATL.animate || []).forEach(function (o) {
      var u = (o.universi || []).filter(function (x) { return UNI[x]; });
      for (var i = 0; i < u.length; i++) for (var j = i + 1; j < u.length; j++) ev(u[i], u[j]).atl[o.id] = 'animata';
    });

    /* ---- evidenze: grafo storico (archi dell'overlay Multiverso, letti dal DOM) ---- */
    var EDGES = [];
    Array.prototype.forEach.call(D.querySelectorAll('.multiverse-graph-overlay .mg-edge[data-node-a][data-node-b][data-items]'), function (e) {
      var tipo = /mg-edge-futuro/.test(e.getAttribute('class')) ? 'futuro' : (/mg-edge-cameo/.test(e.getAttribute('class')) ? 'cameo' : 'crossover');
      EDGES.push({ a: e.getAttribute('data-node-a'), b: e.getAttribute('data-node-b'), tipo: tipo, items: e.getAttribute('data-items').split(',').map(function (x) { return x.trim(); }).filter(Boolean) });
    });
    var SPREL = {}; Object.keys(SPECIAL).forEach(function (k) { SPREL[k] = []; });
    EDGES.forEach(function (g) {
      var A = NODE_MAP[g.a], B = NODE_MAP[g.b];
      if (!A || !B) return;
      if (A.uid && B.uid) { ev(A.uid, B.uid).lg.push({ tipo: g.tipo, items: g.items, nodi: [g.a, g.b] }); return; }
      // arco con un nodo speciale: resta sull'entita' speciale (nessuna relazione inventata tra universi)
      [[A, B, g.b], [B, A, g.a]].forEach(function (p) {
        if (p[0].special) SPREL[p[0].special].push({ con: p[1].uid || null, conSpecial: p[1].special || null, conNodo: p[2], tipo: g.tipo, items: g.items });
      });
    });

    function titoloEsiste(num) { return !!IDX.titoli['item-' + num]; }
    var STATI = { confermato: 'Documentato nella guida', legacy: 'Legacy', verificare: 'Da verificare' };
    var TIPI = { crossover: 'Crossover mostrato', cameo: 'Cameo / sfondo', futuro: 'Previsto, non ancora mostrato', atlante: 'Titolo condiviso (dati dell’Atlante)' };

    function valuta(x) {
      var lgTutti = x.lg, atlNums = Object.keys(x.atl);
      var fonti = [];
      if (atlNums.length) fonti.push({ fonte: 'Atlante (opere)', titoli: atlNums.slice().sort(byGuide), nota: 'Titoli che i dati assegnano a entrambi gli universi' });
      lgTutti.forEach(function (g) { fonti.push({ fonte: 'Grafo storico', tipo: g.tipo, titoli: g.items.slice(), nota: TIPI[g.tipo] }); });
      var r = { a: x.a, b: x.b, fonti: fonti, tipi: [], titoli: [], stato: 'verificare', motivo: '' };
      lgTutti.forEach(function (g) { if (r.tipi.indexOf(g.tipo) === -1) r.tipi.push(g.tipo); g.items.forEach(function (n) { if (r.titoli.indexOf(n) === -1) r.titoli.push(n); }); });
      atlNums.forEach(function (n) { if (r.titoli.indexOf(n) === -1) r.titoli.push(n); });
      r.titoli = r.titoli.filter(titoloEsiste).sort(byGuide);
      if (!lgTutti.length) { // solo Atlante
        r.tipi = ['atlante'];
        r.motivo = 'Presente solo nei dati dell’Atlante: manca il riscontro nel grafo storico. La presenza nel database non è una conferma canonica.';
        return r;
      }
      var vivi = lgTutti.filter(function (g) { return g.tipo !== 'futuro'; });
      if (!vivi.length) {
        r.motivo = 'Il grafo storico lo segna come «previsto, non ancora mostrato»' + (atlNums.length ? ', mentre l’Atlante registra un titolo condiviso (N°' + atlNums.slice().sort(byGuide).map(VN).join(', N°') + '): fonti in disaccordo.' : '.');
        return r;
      }
      var citati = []; vivi.forEach(function (g) { g.items.forEach(function (n) { if (citati.indexOf(n) === -1) citati.push(n); }); });
      var riscontri = citati.filter(function (n) { return x.atl[n] && titoloEsiste(n); });
      if (riscontri.length) {
        r.stato = 'confermato'; r.titoli = r.titoli.filter(function (n) { return riscontri.indexOf(n) !== -1; });
        r.motivo = 'Titolo/i N°' + riscontri.slice().sort(byGuide).map(VN).join(', N°') + ' citato/i sia dal grafo storico sia dalle opere dell’Atlante: le due fonti concordano. Entrambe derivano dalla guida, quindi non è una verifica canonica indipendente.';
        return r;
      }
      var tipoCross = vivi.some(function (g) { return g.tipo === 'crossover'; });
      var contraddetto = tipoCross && citati.some(function (n) {
        var o = OPERA[n]; return o && (o.universi || []).length && !((o.universi || []).indexOf(x.a) !== -1 && (o.universi || []).indexOf(x.b) !== -1);
      });
      if (contraddetto) {
        var dett = citati.filter(function (n) { return OPERA[n]; }).map(function (n) { return 'N°' + VN(n) + ' → ' + (OPERA[n].universi || []).map(function (u) { return (UNI[u] || {}).nome || u; }).join(' + '); });
        r.motivo = 'Il grafo storico indica un crossover, ma nei dati dell’Atlante il titolo risulta assegnato altrove (' + dett.join('; ') + ').';
        return r;
      }
      r.stato = 'legacy';
      r.motivo = 'Presente nel grafo storico (' + r.tipi.map(function (t) { return TIPI[t].toLowerCase(); }).join(', ') + '), non riscontrato né contraddetto dall’Atlante. Non ancora verificato.';
      return r;
    }
    var RELS = Object.keys(EV).map(function (k) { return valuta(EV[k]); });
    RELS.sort(function (p, q) { return (UIDS.indexOf(p.a) - UIDS.indexOf(q.a)) || (UIDS.indexOf(p.b) - UIDS.indexOf(q.b)); });

    /* relazioni dell'entita' speciale: stato per regola (non e' un universo, l'Atlante non puo' riscontrarla) */
    function statoSpeciale(r) { return r.tipo === 'futuro' ? 'verificare' : 'legacy'; }
    function motivoSpeciale(r) {
      return r.tipo === 'futuro' ? 'Il grafo storico lo segna come «previsto, non ancora mostrato».'
        : 'Presente solo nel grafo storico: un elemento speciale non ha riscontro nei dati dell’Atlante.';
    }

    /* ---- anno di ambientazione (approssimato, mai inventato): derivato dal testo libero opere.ambientazione ---- */
    var MESE_RE = /^\d{1,2}\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+\d{4}$/i;
    function annoAmb(txt) {
      var t = String(txt || '').trim(), out = { y: null, approx: false, txt: t };
      if (!t || /^TBD$/i.test(t) || MESE_RE.test(t)) return out;
      if (/contemporanea|atemporale|fuori dal tempo|Battleworld|gotica/i.test(t) && !/\b(1\d{3}|20\d{2})\b/.test(t)) return out;
      var m;
      if ((m = t.match(/(?:^|dal\s+)(\d{3,4})\s*a\.C\./i))) { out.y = -parseInt(m[1], 10); out.approx = true; }
      else if ((m = t.match(/\b(1\d{3}|20\d{2})\b/))) out.y = parseInt(m[1], 10);
      else if ((m = t.match(/(inizio|primi|metà|meta)\s+anni\s+2000/i))) { out.y = /inizio/i.test(m[1]) ? 2000 : (/primi/i.test(m[1]) ? 2001 : 2005); out.approx = true; }
      else if ((m = t.match(/anni\s+'(\d)0/))) { out.y = 1900 + parseInt(m[1], 10) * 10; out.approx = true; }
      if (out.y !== null && (/\d{4}\s*[-–]\s*\d{2,4}|dal |dagli |a\.C\./i.test(t) || /dibattut|alt\.|universo alt|multiplo|\/ futuro|circa|ca\./i.test(t))) out.approx = true;
      return out;
    }

    function breve(uid) { return IDX.breve(uid); }
    function famDi(uid) { return Object.keys(FAM).filter(function (f) { return (FAM[f].universi || []).indexOf(uid) !== -1; }); }
    function gruppiDi(uid) { return Object.keys(SPECIAL).filter(function (k) { return SPECIAL[k].classe === 'raggruppamento' && (SPECIAL[k].membri.indexOf(uid) !== -1 || SPECIAL[k].membriIncerti.indexOf(uid) !== -1); }).map(function (k) { return SPECIAL[k]; }); }

    function collegamenti(uid) {
      var out = [];
      RELS.forEach(function (r) {
        if (r.a !== uid && r.b !== uid) return;
        out.push({ con: r.a === uid ? r.b : r.a, stato: r.stato, tipi: r.tipi, titoli: r.titoli, fonti: r.fonti, motivo: r.motivo });
      });
      var ord = { confermato: 0, legacy: 1, verificare: 2 };
      out.sort(function (p, q) { return ord[p.stato] - ord[q.stato] || UIDS.indexOf(p.con) - UIDS.indexOf(q.con); });
      return out;
    }
    function specialiDi(uid) { // entita' speciali collegate a questo universo dal grafo storico (relazioni dell'entita', non dell'universo)
      var out = [];
      Object.keys(SPECIAL).forEach(function (k) {
        var s = SPECIAL[k];
        SPREL[k].forEach(function (r) {
          if (r.con === uid) out.push({ entita: s, tipo: r.tipo, titoli: r.items.filter(titoloEsiste), stato: statoSpeciale(r), motivo: motivoSpeciale(r) });
        });
        var esp = s.membri.indexOf(uid) !== -1, inc = s.membriIncerti.indexOf(uid) !== -1;
        if (s.classe === 'raggruppamento' && (esp || inc) && !out.some(function (o) { return o.entita === s; })) out.push({ entita: s, tipo: 'membro', incerto: inc, titoli: [], stato: null, motivo: inc ? s.baseIncerta : s.base });
      });
      return out;
    }

    function get(uid) {
      var d = UNI[uid]; if (!d) return null;
      var tt = IDX.titoliDi(uid);
      var prim = tt.filter(function (e) { return IDX.ruoloDi(e) === 'appartenenza'; }), cro = tt.filter(function (e) { return IDX.ruoloDi(e) === 'crossover'; });
      var vv = IDX.varianti(uid), orig = IDX.origineDi(uid), pres = IDX.presentiDi(uid), col = collegamenti(uid), spec = specialiDi(uid);
      var cnt = { confermato: 0, legacy: 0, verificare: 0 }; col.forEach(function (c) { cnt[c.stato]++; });
      var evChiave = (d.eventiChiave || []).slice();
      var have = {
        titoli: tt.length > 0, personaggi: orig.length + pres.length > 0 || (d.personaggiPrincipali || []).length > 0, eventi: evChiave.length > 0,
        collegamenti: col.length > 0 || spec.some(function (s) { return s.stato; }), gruppi: spec.some(function (s) { return !s.stato; }), varianti: vv.length > 0
      };
      return { id: uid, nome: d.nome, breve: breve(uid), natura: d.natura, naturaNota: d.naturaNota || '', famiglie: famDi(uid), titoli: tt, appartenenza: prim, crossover: cro, varianti: vv,
        origine: orig, presenti: pres, principali: (d.personaggiPrincipali || []).slice(), eventiChiave: evChiave, collegamenti: col, speciali: spec, conteggi: cnt, have: have,
        gruppi: gruppiDi(uid) };
    }
    function ordinaTitoli(list, modo) {
      var arr = list.slice();
      if (modo === 'uscita') {
        var us = function (e) { var o = OPERA[e.num]; return o && o.uscita ? o.uscita : null; };
        return { lista: arr.sort(function (a, b) { return (us(a) || '9999').localeCompare(us(b) || '9999'); }), senzaDato: arr.filter(function (e) { return !us(e); }).length, approx: false };
      }
      if (modo === 'ambientazione') {
        var ay = function (e) { var o = OPERA[e.num]; return annoAmb(o && o.ambientazione); };
        var withY = arr.filter(function (e) { return ay(e).y !== null; }), noY = arr.filter(function (e) { return ay(e).y === null; });
        withY.sort(function (a, b) { return ay(a).y - ay(b).y; });
        return { lista: withY.concat(noY), senzaDato: noY.length, approx: withY.some(function (e) { return ay(e).approx; }) };
      }
      return { lista: arr, senzaDato: 0, approx: false };
    }

    W.tvaUniverse = {
      version: '3A', ids: function () { return UIDS.slice(); }, get: get, stati: STATI, tipi: TIPI,
      links: function () { return RELS.map(function (r) { return { a: r.a, b: r.b, stato: r.stato, tipi: r.tipi.slice(), titoli: r.titoli.slice(), motivo: r.motivo, fonti: r.fonti }; }); },
      special: function () { return Object.keys(SPECIAL).map(function (k) {
        var s = SPECIAL[k]; return { id: s.id, nome: s.nome, classe: s.classe, classeLbl: s.classeLbl, membri: s.membri.slice(), membriIncerti: s.membriIncerti.slice(), base: s.base, baseIncerta: s.baseIncerta || '', testo: nodeText(k),
          relazioni: SPREL[k].map(function (r) { return { con: r.con, conSpecial: r.conSpecial, tipo: r.tipo, titoli: r.items.filter(titoloEsiste), stato: statoSpeciale(r), motivo: motivoSpeciale(r) }; }) };
      }); },
      nodeMap: function () { return JSON.parse(JSON.stringify(NODE_MAP)); },
      ordina: ordinaTitoli, annoAmbientazione: annoAmb, ambientazione: function (num) { var o = OPERA[num]; return o ? o.ambientazione || '' : ''; },
      uscita: function (num) { var o = OPERA[num]; return o ? { data: o.uscita || null, precisione: o.precisioneUscita || null } : null; },
      audit: function () {
        var c = { confermato: 0, legacy: 0, verificare: 0 }; RELS.forEach(function (r) { c[r.stato]++; });
        var archiGrafo = EDGES.length, mappati = 0; EDGES.forEach(function (g) { if (NODE_MAP[g.a] && NODE_MAP[g.b]) mappati++; });
        return { universi: UIDS.length, relazioni: RELS.length, perStato: c, archiGrafoStorico: archiGrafo, archiMappati: mappati, speciali: Object.keys(SPECIAL).length,
          nodiMappati: Object.keys(NODE_MAP).length };
      }
    };
  } catch (eUM) { if (window.console) console.error('Marvel guide - TVA Universe Model:', eUM); }
})();
