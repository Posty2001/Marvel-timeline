/* ===== TVA ARCHIVES — L'Atlante del Multiverso (evoluzione dell'Atlante 2.0, sopra l'indice delle relazioni tvaIdx) ===== */
(function () {
  'use strict';
  try {
    var D = document, W = window;
    function $(id) { return D.getElementById(id); }
    var root = $('atlas2'), tog = $('atlas2Toggle'), IDX = W.tvaIdx;
    // Numero visibile (N°, posizionale) <-> id stabile; posizione di guida. Fonte: funzioni window.marvel* del modulo principale quando sono gia' definite
    // oppure, se questo modulo parte prima, la stessa tabella ricavata dal DOM (.rec delle schede): stessa regola, nessun dato duplicato.
    var _NV = null;
    function nvTab() { if (_NV) return _NV; var a = {}, b = {}, g = {}; Array.prototype.forEach.call(D.querySelectorAll('.card-wrap[id^="item-"]'), function (n, k) { var id = n.id.slice(5), r = n.querySelector('.rec'), m = r && /(\d+)/.exec(r.textContent), v = m ? m[1] : id; a[id] = v; b[v] = id; g[id] = k; }); return (_NV = { a: a, b: b, g: g }); }
    function k3(n) { return ('000' + n).slice(-3); }
    function VN(n) { try { return W.marvelNumeroVisibile ? W.marvelNumeroVisibile(n) : (nvTab().a[k3(n)] || k3(n)); } catch (e) { return n; } }
    function FV(n) { try { return W.marvelIdDaNumeroVisibile ? W.marvelIdDaNumeroVisibile(n) : (nvTab().b[k3(n)] || k3(n)); } catch (e) { return n; } }
    function GP(n) { var m = /^(?:item-)?(\d{3})$/.exec(String(n)); if (!m) return null; try { var p = W.marvelPosizioneGuida ? W.marvelPosizioneGuida(m[1]) : nvTab().g[m[1]]; return p === undefined ? null : p; } catch (e) { return null; } }
    function byGuide(a, b) { var pa = /^([a-z0-9]+)-/.exec(String(a)), pb = /^([a-z0-9]+)-/.exec(String(b)); pa = pa ? pa[1] : 'item'; pb = pb ? pb[1] : 'item'; if (pa !== pb) return pa < pb ? -1 : 1; var x = GP(a), y = GP(b); if (x !== null && y !== null && x !== y) return x - y; return a < b ? -1 : a > b ? 1 : 0; }
    if (!root || !tog || !IDX) return;
    var MV = JSON.parse($('mvMapData').textContent), ATL = JSON.parse($('atlasData').textContent);
    var UNI = MV.universi, FAM = MV.famiglie || {};
    var USCITA = {}; (ATL.opere || []).forEach(function (o) { if (o.uscita) USCITA[o.id] = o.uscita; });
    var PTIPO = {}, PSUB = {}; (ATL.personaggi || []).forEach(function (p) { PTIPO[p.id] = p.tipo || ''; PSUB[p.id] = p.sottotipo || ''; });
    var NAT = {
      'Continuità principale': { ic: '⭐', k: 'principale', lbl: 'Principale' },
      'Universo autonomo': { ic: '🌌', k: 'autonomo', lbl: 'Autonomo' },
      'Diramazione / universo alternativo': { ic: '🔀', k: 'diramazione', lbl: 'Diramazione' },
      'Raggruppamento editoriale': { ic: '🗂️', k: 'raggruppamento', lbl: 'Raggruppamento' },
      'Luogo narrativo (non un universo)': { ic: '⏳', k: 'luogo', lbl: 'Luogo narrativo' }
    };
    function nat(u) { return NAT[u.natura] || { ic: '🌌', k: 'altro', lbl: u.natura || 'Universo' }; }
    var ST = { screen: 'home', uid: null, sez: null, q: '', sq: '', nat: 'tutti', fam: 'tutte', ord: 'guida', pf: 'tutti', pq: '', arc: null, eid: null, af: 'tutti', aq: '', au: 'tutti' };
    var EXT = { screens: {}, label: null, search: null, uniExtra: null };
    function el(tag, cls, txt) { var n = D.createElement(tag); if (cls) n.className = cls; if (txt != null) n.textContent = txt; return n; }
    function btn(cls, txt, fn) { var b = el('button', cls, txt); b.type = 'button'; if (fn) b.addEventListener('click', fn); return b; }
    function go(kind, id, label) { var b = btn('a2-chip', label); b.setAttribute('data-go', kind + ':' + id); return b; }
    function sezChip(key, label) { var b = btn('a2-chip a2-chip-s', label); b.setAttribute('data-a2s', key); return b; }

    /* ---------- illustrazioni (SVG inline statici, nessuna immagine esterna, nessuna animazione) ---------- */
    var SV = '<svg viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">';
    var ART = {
      universi: SV + '<circle cx="32" cy="32" r="5.5"/><ellipse cx="32" cy="32" rx="26" ry="9.5" transform="rotate(28 32 32)"/><ellipse cx="32" cy="32" rx="26" ry="9.5" transform="rotate(-28 32 32)"/><circle cx="55" cy="22" r="2.6" fill="currentColor"/><circle cx="9" cy="42" r="2.6" fill="currentColor"/><circle cx="32" cy="6" r="2" fill="currentColor"/></svg>',
      personaggi: SV + '<circle cx="32" cy="21" r="9.5"/><path d="M11 57c2-15 10-21 21-21s19 6 21 21"/><path d="M32 3v4M22 8l2 3M42 8l-2 3"/></svg>',
      cronologie: SV + '<path d="M5 38h54"/><path d="M16 38V24M30 38V14M44 38V27"/><circle cx="16" cy="22" r="2.4" fill="currentColor"/><circle cx="30" cy="12" r="2.4" fill="currentColor"/><circle cx="44" cy="25" r="2.4" fill="currentColor"/><path d="M30 38c9 0 11 10 24 10"/><circle cx="55" cy="48" r="2.4" fill="currentColor"/></svg>',
      relazioni: SV + '<circle cx="32" cy="32" r="5"/><circle cx="12" cy="14" r="4"/><circle cx="54" cy="16" r="4"/><circle cx="14" cy="52" r="4"/><circle cx="52" cy="50" r="4"/><path d="M28 28L15 17M36 28l15-9M28 36L17 49M36 36l13 11"/></svg>',
      gemma: SV + '<path d="M32 5l21 12v28L32 59 11 45V17z"/><path d="M11 17l21 12 21-12M32 29v30"/></svg>',
      poteri: SV + '<path d="M32 6l27 49H5z"/><path d="M21 34h22M13.5 46h37"/></svg>',
      casa: SV + '<path d="M8 30L32 9l24 21"/><path d="M14 27v26h36V27"/><path d="M27 53V38h10v15"/></svg>',
      org: SV + '<circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="11"/><path d="M32 6v14M32 44v14M6 32h14M44 32h14"/></svg>',
      eventi: SV + '<path d="M32 5l6 17 18 1-14 11 5 18-15-10-15 10 5-18L8 23l18-1z"/></svg>',
      luoghi: SV + '<circle cx="32" cy="30" r="20"/><ellipse cx="32" cy="30" rx="20" ry="7"/><path d="M32 10c8 8 8 32 0 40M32 10c-8 8-8 32 0 40"/><path d="M32 50v10"/></svg>',
      cerca: SV + '<circle cx="27" cy="27" r="17"/><path d="M40 40l17 17"/></svg>',
      freccia: SV + '<path d="M40 10L18 32l22 22"/></svg>'
    };
    function art(name, cls) { var s = el('span', 'a2-art' + (cls ? ' ' + cls : '')); s.setAttribute('aria-hidden', 'true'); s.innerHTML = ART[name]; return s; }
    // copertina: rami della Sacra Timeline potati dalla TVA (linee sottili, nessun effetto pesante)
    var COVER = '<svg viewBox="0 0 390 230" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false" fill="none">' +
      '<defs><radialGradient id="a2cg" cx="72%" cy="8%" r="75%"><stop offset="0" stop-color="#DB777C" stop-opacity=".38"/><stop offset="1" stop-color="#101014" stop-opacity="0"/></radialGradient></defs>' +
      '<rect width="390" height="230" fill="url(#a2cg)"/>' +
      '<g stroke="#D2B184" stroke-opacity=".55" stroke-width="1.1">' +
      '<circle cx="292" cy="96" r="38"/><circle cx="292" cy="96" r="64" stroke-opacity=".35"/><circle cx="292" cy="96" r="92" stroke-opacity=".2"/>' +
      '<path d="M292 230V150C292 122 292 112 292 96"/><path d="M292 150C262 138 246 118 230 86"/><path d="M292 150C322 136 340 112 352 80"/><path d="M292 190C268 182 252 170 238 150"/><path d="M292 190C318 180 332 166 344 146"/>' +
      '</g><g fill="#D2B184"><circle cx="292" cy="96" r="4.5"/><circle cx="230" cy="86" r="3"/><circle cx="352" cy="80" r="3"/><circle cx="238" cy="150" r="2.5"/><circle cx="344" cy="146" r="2.5"/></g>' +
      '<g fill="#DB777C"><circle cx="292" cy="150" r="3.5"/><circle cx="292" cy="190" r="3"/></g>' +
      '<g fill="#F2E8D8" fill-opacity=".7"><circle cx="40" cy="30" r="1.2"/><circle cx="120" cy="58" r="1"/><circle cx="188" cy="24" r="1.3"/><circle cx="64" cy="112" r="1"/><circle cx="156" cy="132" r="1.2"/></g></svg>';

    /* ---------- scheletro: intestazione dedicata (Indietro · titolo · ricerca · App Marvel) ---------- */
    var top = el('header', 'a2-top'), body = el('div', 'a2-scroll'), back = btn('a2-back', null), ttl = el('div', 'a2-ttl'), srch = btn('a2-srch', null), ext = btn('a2-exit', null);
    back.appendChild(art('freccia')); back.setAttribute('aria-label', 'Indietro');
    srch.appendChild(art('cerca')); srch.setAttribute('aria-label', 'Ricerca universale');
    ext.appendChild(art('casa')); ext.appendChild(el('span', 'a2-exit-t', 'App Marvel')); ext.setAttribute('aria-label', 'Torna all’app Marvel');
    top.appendChild(back); top.appendChild(ttl); top.appendChild(srch); top.appendChild(ext);
    root.appendChild(top); root.appendChild(body);
    root.setAttribute('role', 'dialog'); root.setAttribute('aria-label', 'TVA Archives — L’Atlante del Multiverso');
    function setTitle(main, sub) { ttl.textContent = ''; ttl.appendChild(el('span', 'a2-eyebrow', 'TVA ARCHIVES')); if (sub) ttl.title = sub; ttl.appendChild(el('b', '', main)); }

    function prog(uid) {
      var t = IDX.titoliDi(uid), v = 0;
      t.forEach(function (e) { var c = e.li.querySelector('.watch-check, .anim-watch-check'); if (c && c.checked) v++; });
      return { n: t.length, v: v };
    }
    function tipoTitolo(e) {
      var t = e.li.getAttribute('data-type');
      if (e.kind === 'anim') return 'Serie animata';
      return t === 'serie' ? 'Serie' : (t === 'film' ? 'Film' : (t ? t.charAt(0).toUpperCase() + t.slice(1) : 'Titolo'));
    }
    // Anno di uscita da atlasData.opere.uscita (l'etichetta .yr a volte e' l'AMBIENTAZIONE, non un anno)
    function anno(e) {
      if (e.kind === 'item') return USCITA[e.num] ? 'uscita ' + String(USCITA[e.num]).slice(0, 4) : '';
      var y = e.li.querySelector('.yr'), t = y ? y.textContent.trim() : '';
      return /^\d{4}/.test(t) ? t : '';
    }
    function classicDescr(uid) {
      var li = $(uid), out = {};
      if (!li) return out;
      Array.prototype.forEach.call(li.querySelectorAll('.detail-row'), function (r) {
        var k = r.querySelector('.detail-k'), v = r.querySelector('.detail-v');
        if (k && v && !r.classList.contains('tva-row')) out[k.textContent.trim()] = v.textContent.trim();
      });
      return out;
    }

    /* ---------- testi condivisi: categorie e numerazione ---------- */
    var MCU = 'uni-earth-199999-mcu';
    var NOTA_NUM = 'Numerazione: in questa guida l’MCU è Earth-199999. «Earth-616» è la numerazione del fumetto principale Marvel e qui non è un universo: non esiste una scheda Earth-616 e nessun titolo o personaggio è associato a «616». Dove un testo originale scrive «MCU-616» (per esempio nella «Cronologia dei simbionti») intende l’MCU, non un universo a parte. Le associazioni della guida non sono state modificate.';
    function legend(open) {
      var d = D.createElement('details'); d.className = 'a2-legend'; if (open) d.open = true;
      d.appendChild(el('summary', '', 'Come leggere le schede: appartenenza, crossover, ambientazione, apparizione'));
      var dl = el('dl');
      [['Appartenenza', 'Il titolo è assegnato dai dati della guida a un solo universo.'],
       ['Crossover', 'Il titolo coinvolge più universi e la guida non indica quale sia «il suo»: compare in ciascuno, senza essere assegnato a uno solo.'],
       ['Ambientazione', 'Luogo ed epoca in cui si svolge la storia (testo libero della guida). Non è un universo.'],
       ['Origine e apparizione', 'L’origine di un personaggio è la continuità dichiarata dalla guida. «Presente» indica che compare in quell’universo (riga UNIVERSI della scheda) pur avendo l’origine altrove.']
      ].forEach(function (p) { dl.appendChild(el('dt', '', p[0])); dl.appendChild(el('dd', '', p[1])); });
      d.appendChild(dl); return d;
    }
    function info(txt) { var p = el('p', 'a2-info', txt); p.setAttribute('role', 'note'); return p; }
    // stessa nota, richiudibile (nella scheda MCU non deve dominare l'intestazione)
    function infoDet(sum, txt) { var d = D.createElement('details'); d.className = 'a2-info a2-info-d'; d.appendChild(el('summary', '', sum)); d.appendChild(el('p', '', txt)); return d; }

    /* ---------- catalogo degli archivi (modello unico: Home, catalogo e ricerca lo leggono da qui) ---------- */
    // st: dis = schermata di TVA Archives · cls = sezione dell'archivio esistente, riutilizzata · prep = solo struttura di navigazione
    var BADGE = { dis: 'Disponibile', cls: 'Archivio esistente', prep: 'In preparazione' };
    var GRP = [
      { k: 'mt', n: 'Multiverso e Tempo', items: [
        { k: 'multiverso', n: 'Multiverso', art: 'universi', st: 'cls', d: 'La mappa interattiva dei 27 universi.', kw: 'grafico mappa rami grafo', act: ['map'] },
        { k: 'universi', n: 'Universi', art: 'universi', st: 'dis', d: 'Ogni universo con titoli, personaggi e crossover.', kw: 'earth mcu terre', act: ['scr', 'universi'] },
        { k: 'cronologie', n: 'Cronologie', art: 'cronologie', st: 'dis', d: 'Timeline degli universi, alternative e cronologie tematiche.', kw: 'timeline tempo kang loki doom tva simbionti battleworld', act: ['scr', 'cronologie'] },
        { k: 'eventi', n: 'Eventi', art: 'eventi', st: 'dis', d: 'Eventi e Battaglie: cause, conseguenze e titoli.', kw: 'battaglie battaglia guerra scontri blip', act: ['arc', 'evt'] }
      ] },
      { k: 'ip', n: 'Identità e Potere', items: [
        { k: 'personaggi', n: 'Personaggi', art: 'personaggi', st: 'dis', d: 'Tutte le schede, in ordine alfabetico, con le varianti.', kw: 'varianti variante eroi cattivi', act: ['scr', 'personaggi'] },
        { k: 'relazioni', n: 'Relazioni', art: 'relazioni', st: 'dis', d: 'Grafo delle relazioni e alberi genealogici.', kw: 'alberi genealogici famiglia parentele grafo', act: ['scr', 'relazioni'] },
        { k: 'attori', n: 'Attori', art: 'personaggi', st: 'dis', d: 'Gli interpreti, con i ruoli e i titoli in cui compaiono.', kw: 'attori interpreti cast ruoli volti', act: ['scr', 'attori'] },
        { k: 'poteri', n: 'Classifica dei Poteri', art: 'poteri', st: 'dis', d: 'Archivio della Potenza TVA: sette fasce, schede di potenza e confronto tra due personaggi.', kw: 'forte piramide livelli potere confronto fasce potenza', act: ['scr', 'potenza'] },
        { k: 'cosmiche', n: 'Entità Cosmiche', art: 'poteri', st: 'dis', d: 'Entità apparse sullo schermo e quelle che la guida elenca come mai apparse.', kw: 'cosmico entità celestiali eterni galactus watcher', act: ['arc', 'cos'] }
      ] },
      { k: 'mc', n: 'Mondi e Civiltà', items: [
        { k: 'luoghi', n: 'Luoghi', art: 'luoghi', st: 'dis', d: 'Pianeti e luoghi, con i titoli in cui compaiono.', kw: 'pianeti luogo mondi', act: ['arc', 'luo'] },
        { k: 'specie', n: 'Specie e Civiltà', art: 'personaggi', st: 'dis', d: 'Specie e popoli citati in più schede, con personaggi, mondi e conflitti.', kw: 'specie razze civiltà alieni kree asgardiani mutanti', act: ['arc', 'spe'] },
        { k: 'organizzazioni', n: 'Organizzazioni', art: 'org', st: 'dis', d: 'Membri, scopo e titoli di ogni organizzazione.', kw: 'shield hydra avengers tva', act: ['arc', 'org'] }
      ] },
      { k: 'ra', n: 'Reliquie e Arti Arcane', items: [
        { k: 'artefatti', n: 'Artefatti', art: 'gemma', st: 'dis', d: 'Artefatti, Gemme dell’Infinito e il Reliquiario.', kw: 'gemme infinito guanto reliquie oggetti reliquiario', act: ['arc', 'art'] },
        { k: 'arti', n: 'Arti Mistiche', art: 'gemma', st: 'dis', d: 'Discipline mistiche documentate, con praticanti, artefatti e luoghi.', kw: 'magia mistico stregoneria incantesimi darkhold kamar-taj', act: ['arc', 'mis'] }
      ] }
    ];
    var SEZ = {}; GRP.forEach(function (g) { g.items.forEach(function (i) { i.g = g; SEZ[i.k] = i; }); });

    /* ---------- conteggi dai dati ---------- */
    function titoliBase() { return Object.keys(IDX.titoli).map(function (k) { return IDX.titoli[k]; }).filter(function (e) { return !e.variant; }); }
    function personaggiLista() { return Object.keys(IDX.personaggi).map(function (k) { return IDX.personaggi[k]; }).filter(function (c) { return PTIPO[c.id] !== 'segnaposto'; }); }
    function isVar(c) { return PTIPO[c.id] === 'variante' || PTIPO[c.id] === 'aggregata' || /incarnazion|variant/i.test(PSUB[c.id] || ''); }

    /* ---------- apertura delle sezioni esistenti (ogni uscita dall'Atlante entra nello stack: Indietro riporta qui) ---------- */
    function fire(c) { try { c.dispatchEvent(new Event('change', { bubbles: true })); } catch (e) {} }
    function leave() { if (W.tvaPushNav) W.tvaPushNav('Atlante'); if (W.marvelChiudiOverlay) W.marvelChiudiOverlay(); }
    function openToggle(id) { var t = $(id); if (!t) return; leave(); t.checked = true; fire(t); }
    function cardByTitle(txt) {
      var low = txt.toLowerCase(), all = D.querySelectorAll('#tvaArchivesOverlayEl details.card > summary .title');
      for (var i = 0; i < all.length; i++) if (all[i].textContent.trim().toLowerCase().indexOf(low) === 0) return all[i].closest('details.card');
      return null;
    }
    function openArchive(dbtab) {
      leave(); var t = $('tvaArchivesToggle'); if (!t) return false; t.checked = true; fire(t);
      if (dbtab && $(dbtab)) { $(dbtab).checked = true; fire($(dbtab)); }
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('atlante');
      return true;
    }
    function openCard(title) {
      var c = cardByTitle(title); if (!openArchive()) return;
      c = cardByTitle(title); if (c) { c.setAttribute('open', ''); if (W.tvaSettleScroll) W.tvaSettleScroll(c); }
    }
    function openChrono(target) {
      openArchive(); var host = cardByTitle('Cronologie Personaggio'); if (host) host.setAttribute('open', '');
      var b = D.querySelector('#tvaArchivesOverlayEl [data-target="' + target + '"]');
      if (b) { b.click(); var p = $(target); if (p && W.tvaSettleScroll) W.tvaSettleScroll(p); }
    }
    function openTimeline() {
      if (W.tvaPushNav) W.tvaPushNav('Atlante'); if (W.marvelChiudiOverlay) W.marvelChiudiOverlay();
      var x = $('homeHubExited'); if (x) x.checked = true; var h = $('homeHub'); if (h) h.style.display = 'none';
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('timeline');
      var p = $('parte1'); if (p && p.scrollIntoView) p.scrollIntoView({ block: 'start' });
    }
    function run(a) {
      var t = a[0];
      if (t === 'tog') openToggle(a[1]);
      else if (t === 'cls') openArchive(a[1]);
      else if (t === 'card') { if (a[1] === 'Alberi Genealogici') nav('alberi', { eid: 'tree-ff' }); else openCard(a[1]); }
      else if (t === 'chr') nav('chrono', { eid: a[1] });
      else if (t === 'doc') nav('doc', { eid: a[1] });
      else if (t === 'map') openMappa();
      else if (t === 'tl') openTimeline();
      else if (t === 'arc') nav('arch', { arc: a[1], eid: null, af: 'tutti', aq: '', au: 'tutti' });
      else if (t === 'rel') nav('reliquiario', { arc: 'art', eid: null });
      else if (t === 'scr') nav(a[1], a[1] === 'potenza' ? { arc: 'pot', eid: null, af: 'tutti', aq: '', au: 'tutti' } : a[1] === 'personaggi' ? { pf: 'tutti', pq: '' } : (a[1] === 'universi' ? { nat: 'tutti', fam: 'tutte', q: '' } : (a[1] === 'attori' ? { eid: null, aq: '' } : null)));
    }
    function openSez(k) {
      var s = SEZ[k]; if (!s) return;
      if (s.st === 'prep') return nav('soon', { sez: k });
      if (s.act[0] === 'sub') return nav('sezione', { sez: k });
      run(s.act);
    }
    function nav(screen, patch) {
      if (tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante');
      ST.screen = screen; if (patch) Object.keys(patch).forEach(function (k) { ST[k] = patch[k]; });
      draw(); setScroll(0);
    }

    /* ---------- elementi riusabili ---------- */
    function badge(st) { return el('span', 'a2-st a2-st-' + st, BADGE[st]); }
    function row(item, onclick) {
      var b = btn('a2-lrow', null, onclick);
      var ic = art(item.art || 'universi', 'a2-lrow-ic'), th = item.k ? thumb(item.k, 'a2-lrow-img') : null;
      if (th) { var imE = th.firstChild; imE.onerror = function () { if (th.parentNode) th.parentNode.replaceChild(ic, th); }; b.appendChild(th); } else b.appendChild(ic);
      var t = el('span', 'a2-lrow-t'); t.appendChild(el('b', '', item.n)); if (item.d) t.appendChild(el('small', '', item.d)); b.appendChild(t);
      if (item.st) b.appendChild(badge(item.st));
      return b;
    }
    function heading(kick, title, lead) {
      var h = el('section', 'a2-head'); if (kick) h.appendChild(el('span', 'a2-kick', kick)); h.appendChild(el('h2', '', title)); if (lead) h.appendChild(el('p', '', lead)); return h;
    }
    function searchBox(id, val, onq, ph) {
      var f = el('form', 'a2-sbox'); f.setAttribute('role', 'search'); f.addEventListener('submit', function (e) { e.preventDefault(); });
      f.appendChild(art('cerca'));
      var inp = D.createElement('input'); inp.type = 'search'; inp.id = id; inp.value = val; inp.placeholder = ph || 'Cerca nell’Atlante…';
      inp.setAttribute('aria-label', 'Ricerca universale'); inp.autocomplete = 'off'; inp.setAttribute('enterkeyhint', 'search'); f.appendChild(inp);
      var tm = null; inp.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(function () { onq(inp.value); }, 120); });
      return f;
    }
    // ricerca universale: archivi, universi, titoli, personaggi (stessi indici dei collegamenti: nessun dato duplicato)
    function drawResults(box, raw) {
      box.textContent = '';
      if (EXT.drawResults && EXT.drawResults(box, raw)) return;   /* F4: ricerca tollerante (dossier4.js) */
      var q = (raw || '').trim().toLowerCase();
      if (q.length < 2) return;
      var any = false;
      function group(titolo, n) { var g = el('div', 'a2-resbox'); g.appendChild(el('h3', '', titolo + ' (' + n + ')')); box.appendChild(g); any = true; return g; }
      var sz = []; GRP.forEach(function (g) { g.items.forEach(function (i) { if ((i.n + ' ' + (i.kw || '') + ' ' + g.n).toLowerCase().indexOf(q) !== -1) sz.push(i); }); });
      if (sz.length) { var g0 = group('Archivi', sz.length); sz.forEach(function (i) { g0.appendChild(row(i, function () { openSez(i.k); })); }); }
      var us = Object.keys(UNI).filter(function (u) { return (UNI[u].nome || '').toLowerCase().indexOf(q) !== -1; });
      if (us.length) { var g1 = group('Universi', us.length), c1 = el('div', 'a2-chips'); us.slice(0, 12).forEach(function (u) { c1.appendChild(go('uni', u, UNI[u].nome)); }); g1.appendChild(c1); if (us.length > 12) g1.appendChild(el('p', 'a2-more', '+' + (us.length - 12) + ' altri: affina la ricerca')); }
      if (/616/.test(q)) box.appendChild(info(NOTA_NUM));
      if (EXT.search) { var ar = EXT.search(q); if (ar.length) { var gA = group('Schede degli archivi', ar.length), cA = el('div', 'a2-chips'); ar.slice(0, 12).forEach(function (x) { var ch = go('arc', x.cat + ':' + x.id, x.name); ch.appendChild(el('small', '', x.catLbl)); cA.appendChild(ch); }); gA.appendChild(cA); if (ar.length > 12) gA.appendChild(el('p', 'a2-more', '+' + (ar.length - 12) + ' altre: affina la ricerca')); } }
      var tit = titoliBase().filter(function (e) { return e.title.toLowerCase().indexOf(q) !== -1; });
      if (tit.length) { var g2 = group('Titoli', tit.length), c2 = el('div', 'a2-chips'); tit.slice(0, 10).forEach(function (e) { var ch = go('item', e.id, e.title); if (e.num) ch.appendChild(el('small', '', 'N°' + VN(e.num))); c2.appendChild(ch); }); g2.appendChild(c2); if (tit.length > 10) g2.appendChild(el('p', 'a2-more', '+' + (tit.length - 10) + ' altri: affina la ricerca')); }
      var chs = personaggiLista().filter(function (c) { return c.name.toLowerCase().indexOf(q) !== -1; });
      if (chs.length) { var g3 = group('Personaggi', chs.length), c3 = el('div', 'a2-chips'); chs.slice(0, 12).forEach(function (c) { c3.appendChild(go('char', c.id, c.name)); }); g3.appendChild(c3); if (chs.length > 12) g3.appendChild(el('p', 'a2-more', '+' + (chs.length - 12) + ' altri: affina la ricerca')); }
      if (!any && !/616/.test(q)) box.appendChild(el('p', 'a2-empty', 'Nessun risultato per «' + raw.trim() + '». Prova con il nome di un personaggio, di un universo o di un titolo.'));
    }

    /* ---------- schermata: Home TVA Archives (Fase 2 — «Osservatorio»; blocco sostituito da patch_home2.py) ---------- */
    /* Asset sostituibili (nessuna modifica al codice): copiare il file in assets/images/tva/ con il nome indicato, verra' caricato da solo.
       Home: home_hero.webp · universi.webp · attori.webp · reliquiario.webp · eventi.webp · luoghi.webp · specie_civilta.webp · organizzazioni.webp
       Se il file manca resta la copertina condivisa (se esiste) oppure la composizione SVG originale. */
    /* Statistiche: UNICA sorgente per Home e introduzione (tvaAtlas2.stats()). Nessun valore statico. */
    function hmStats() {
      var T = Object.keys(IDX.titoli).map(function (k) { return IDX.titoli[k]; });
      return { universi: Object.keys(UNI).length, personaggi: personaggiLista().length,
        titoliTimeline: titoliBase().filter(function (e) { return e.kind === 'item'; }).length,
        opereTotali: T.filter(function (e) { return e.kind === 'item' || e.kind === 'variant' || e.kind === 'anim'; }).length };
    }
    var HM_DIR = 'assets/images/tva/';
    var HM_HERO = [HM_DIR + 'home_hero.webp', HM_DIR + 'multiverso.webp'];
    var hmSeq = 0;
    // composizioni SVG originali per le 4 sezioni senza copertina (nessun elemento ufficiale Marvel)
    function hmScene(kind) {
      var g = 'hs' + (hmSeq++), c = '#D2B184', r = '#DB777C', s = '', i;
      var defs = '<defs><radialGradient id="' + g + 'a" cx=".72" cy=".32" r=".9"><stop offset="0" stop-color="#7a2433" stop-opacity=".95"/><stop offset=".55" stop-color="#2a1218" stop-opacity=".9"/><stop offset="1" stop-color="#0b0a0e"/></radialGradient>' +
        '<radialGradient id="' + g + 'b" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="' + c + '" stop-opacity=".55"/><stop offset="1" stop-color="' + c + '" stop-opacity="0"/></radialGradient></defs>';
      if (kind === 'eventi') {
        for (i = 0; i < 28; i++) { var a = i * Math.PI / 14, l = i % 2 ? 46 : 78; s += '<line x1="' + (150 + 14 * Math.cos(a)).toFixed(1) + '" y1="' + (60 + 14 * Math.sin(a)).toFixed(1) + '" x2="' + (150 + l * Math.cos(a)).toFixed(1) + '" y2="' + (60 + l * Math.sin(a) * 0.8).toFixed(1) + '" stroke="' + (i % 3 ? c : r) + '" stroke-opacity="' + (i % 2 ? '.35' : '.7') + '" stroke-width="' + (i % 2 ? 1 : 1.6) + '"/>'; }
        s += '<circle cx="150" cy="60" r="34" fill="url(#' + g + 'b)"/><circle cx="150" cy="60" r="12" fill="none" stroke="' + c + '"/><circle cx="150" cy="60" r="4" fill="' + c + '"/><circle cx="150" cy="60" r="52" fill="none" stroke="' + r + '" stroke-opacity=".4" stroke-dasharray="2 5"/>';
      } else if (kind === 'luoghi') {
        s += '<circle cx="120" cy="88" r="66" fill="#1a0f14" stroke="' + c + '" stroke-opacity=".75"/><circle cx="120" cy="88" r="66" fill="url(#' + g + 'b)" opacity=".5"/><ellipse cx="120" cy="88" rx="104" ry="14" fill="none" stroke="' + c + '" stroke-opacity=".6" transform="rotate(-18 120 88)"/>' +
          '<path d="M54 100Q90 70 120 94T186 82" fill="none" stroke="' + r + '" stroke-opacity=".6"/><path d="M60 118Q100 96 130 112T182 106" fill="none" stroke="' + c + '" stroke-opacity=".35"/><circle cx="196" cy="34" r="7" fill="' + c + '" fill-opacity=".85"/><circle cx="40" cy="30" r="2" fill="' + c + '"/><circle cx="64" cy="16" r="1.4" fill="' + c + '"/>';
      } else if (kind === 'specie') {
        var P = [[60, 82], [118, 46], [176, 78], [232, 40], [150, 112]];
        s += '<path d="M60 82L118 46 176 78 232 40M118 46L150 112 176 78" fill="none" stroke="' + c + '" stroke-opacity=".5"/>';
        P.forEach(function (p, j) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (14 + (j % 3) * 3) + '" fill="url(#' + g + 'b)"/><circle cx="' + p[0] + '" cy="' + (p[1] - 4) + '" r="4.2" fill="none" stroke="' + c + '"/><path d="M' + (p[0] - 8) + ' ' + (p[1] + 10) + 'Q' + p[0] + ' ' + (p[1] - 2) + ' ' + (p[0] + 8) + ' ' + (p[1] + 10) + '" fill="none" stroke="' + (j % 2 ? r : c) + '"/>'; });
      } else {
        s += '<path d="M150 14L204 44V92L150 122 96 92V44Z" fill="#1a0f14" fill-opacity=".7" stroke="' + c + '" stroke-width="1.6"/><path d="M150 32L188 54V84L150 106 112 84V54Z" fill="none" stroke="' + r + '" stroke-opacity=".7"/><path d="M150 50L172 63V79L150 92 128 79V63Z" fill="' + c + '" fill-opacity=".18" stroke="' + c + '"/><circle cx="150" cy="68" r="4" fill="' + c + '"/><circle cx="150" cy="68" r="62" fill="url(#' + g + 'b)" opacity=".45"/>' +
          '<path d="M30 118L96 92M270 118L204 92M30 10L96 44M270 10L204 44" stroke="' + c + '" stroke-opacity=".35"/>';
      }
      var vb = { luoghi: '46 -8 148 176', specie: '36 18 224 100' }[kind] || '0 0 300 130';
      return '<svg class="hm-scene" xmlns="http://www.w3.org/2000/svg" viewBox="' + vb + '" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">' + defs + '<rect x="-50" y="-50" width="500" height="250" fill="url(#' + g + 'a)"/>' + s + '</svg>';
    }
    // carica la prima immagine disponibile fra le candidate; se nessuna carica chiama none()
    /* Asset opzionali (dedicati) non ancora prodotti: dopo il primo 404 l'assenza viene ricordata (per build, in localStorage + memoria)
       e non si ripete la richiesta. Un asset nuovo viene rilevato alla prima apertura con un nuovo build id, oppure con tvaAtlas2.img.reprobe(). */
    var HM_OPT = { 'home_hero': 1, 'universi': 1, 'attori': 1, 'reliquiario': 1, 'eventi': 1, 'luoghi': 1, 'specie_civilta': 1, 'organizzazioni': 1, 'uni_mcu': 1, 'uni_sony': 1, 'uni_fox': 1, 'uni_spiderverse': 1, 'uni_legacy': 1, 'uni_whatif': 1, 'uni_animazione': 1, 'mappa_sfondo': 1 };
    var HM_MISS = {}, HM_BUILD = (function () { var m = D.querySelector('meta[name="tva-build"]'); return m ? m.content : 'x'; })(), HM_KEY = 'tvaHomeMiss:' + HM_BUILD;
    try { HM_MISS = JSON.parse(W.localStorage.getItem(HM_KEY) || '{}') || {}; Object.keys(W.localStorage).forEach(function (k) { if (k.indexOf('tvaHomeMiss:') === 0 && k !== HM_KEY) W.localStorage.removeItem(k); }); } catch (eM) { HM_MISS = {}; }
    function hmOpt(src) { var m = /([^\/]+)\.webp$/.exec(src); return !!(m && HM_OPT[m[1]]); }
    function hmMiss(src) { HM_MISS[src] = 1; try { W.localStorage.setItem(HM_KEY, JSON.stringify(HM_MISS)); } catch (eS) { } }
    function hmLoad(host, list, cls, none) {
      list = list.filter(function (u) { return !(hmOpt(u) && HM_MISS[u]); });
      if (!list.length) { if (none) none(); return D.createElement('img'); }
      var i = 0, im = new Image(); im.alt = ''; im.className = cls; im.decoding = 'async';
      im.onerror = function () { if (hmOpt(list[i])) hmMiss(list[i]); i++; if (i < list.length) { im.src = list[i]; } else { im.remove(); if (none) none(); } };
      im.onload = function () { host.classList.add('hm-has-img'); host.setAttribute('data-src', list[i]); };
      im.src = list[0]; host.insertBefore(im, host.firstChild); return im;
    }
    // definizione dei portali: ordine e grid-area scelti per capitolo (nessun dato Marvel qui: conteggi dai dati reali)
    function hmPortals(nU, nC, nT) {
      var A = function (n) { return { src: [HM_DIR + n + '.webp'] }; };
      return [
        { ch: 'mt', k: 'multiverso', n: 'Multiverso', sub: 'La mappa dei rami', go: ['sez', 'multiverso'], cls: 'hm-p-hero', img: [HM_DIR + 'multiverso.webp'], pos: '50% 42%' },
        { ch: 'mt', k: 'universi', n: 'Universi', sub: nU + ' universi e la loro mappa', go: ['sez', 'universi'], img: [HM_DIR + 'universi.webp', HM_DIR + 'multiverso.webp'], pos: '12% 30%', zoom: 1.9 },
        { ch: 'mt', k: 'cronologie', n: 'Cronologie', sub: 'Timeline e percorsi', go: ['sez', 'cronologie'], img: [HM_DIR + 'cronologie.webp'], pos: '50% 50%' },
        { ch: 'mt', k: 'eventi', n: 'Eventi', sub: 'Battaglie, cause e conseguenze', go: ['sez', 'eventi'], cls: 'hm-p-strip', img: [HM_DIR + 'eventi.webp'], scene: 'eventi', dpos: '50% 50%' },
        { ch: 'ip', k: 'personaggi', n: 'Personaggi', sub: nC + ' schede, con le varianti', go: ['sez', 'personaggi'], cls: 'hm-p-wide', img: [HM_DIR + 'personaggi.webp'], pos: '50% 30%' },
        { ch: 'ip', k: 'poteri', n: 'Classifica dei Poteri', sub: 'Sette fasce di potenza', go: ['sez', 'poteri'], cls: 'hm-p-tall', img: [HM_DIR + 'classifica_poteri.webp'], pos: '50% 50%' },
        { ch: 'ip', k: 'relazioni', n: 'Relazioni', sub: 'Grafo e alberi', go: ['sez', 'relazioni'], img: [HM_DIR + 'relazioni.webp'], pos: '50% 50%' },
        { ch: 'ip', k: 'attori', n: 'Attori', sub: 'Interpreti e ruoli', go: ['sez', 'attori'], img: [HM_DIR + 'attori.webp', HM_DIR + 'personaggi.webp'], pos: '90% 40%', zoom: 1.7 },
        { ch: 'ip', k: 'cosmiche', n: 'Entità Cosmiche', sub: 'Presenze oltre i mondi', go: ['sez', 'cosmiche'], cls: 'hm-p-strip', img: [HM_DIR + 'entita_cosmiche.webp'], pos: '50% 40%' },
        { ch: 'mc', k: 'luoghi', n: 'Luoghi', sub: 'Pianeti e luoghi', go: ['sez', 'luoghi'], cls: 'hm-p-tall', img: [HM_DIR + 'luoghi.webp'], scene: 'luoghi', dpos: '50% 30%' },
        { ch: 'mc', k: 'specie', n: 'Specie e Civiltà', sub: 'Popoli e specie', go: ['sez', 'specie'], img: [HM_DIR + 'specie_civilta.webp'], scene: 'specie' },
        { ch: 'mc', k: 'organizzazioni', n: 'Organizzazioni', sub: 'Membri, scopo e titoli', go: ['sez', 'organizzazioni'], img: [HM_DIR + 'organizzazioni.webp'], scene: 'organizzazioni' },
        { ch: 'ra', k: 'artefatti', n: 'Artefatti', sub: 'Oggetti e reliquie', go: ['sez', 'artefatti'], cls: 'hm-p-wide', img: [HM_DIR + 'artefatti.webp'], pos: '50% 50%' },
        { ch: 'ra', k: 'reliquiario', n: 'Reliquiario', sub: 'Le sei Gemme', go: ['rel'], img: [HM_DIR + 'reliquiario.webp', HM_DIR + 'artefatti.webp'], pos: '85% 30%', zoom: 1.8, gems: true },
        { ch: 'ra', k: 'arti', n: 'Arti Mistiche', sub: 'Discipline arcane', go: ['sez', 'arti'], img: [HM_DIR + 'arti_mistiche.webp'], pos: '50% 50%' }
      ];
    }
    var HM_CH = [
      { k: 'mt', n: 'Multiverso e Tempo', num: 'I', t: 'Dove i rami si separano' },
      { k: 'ip', n: 'Identità e Potere', num: 'II', t: 'Chi sono, quanto possono' },
      { k: 'mc', n: 'Mondi e Civiltà', num: 'III', t: 'Pianeti, popoli, organizzazioni' },
      { k: 'ra', n: 'Reliquie e Arti Arcane', num: 'IV', t: 'Ciò che resta e ciò che si evoca' }
    ];
    function hmPortal(p) {
      var b = btn('hm-p ' + (p.cls || ''), null, function () { if (p.go[0] === 'rel') run(['rel']); else openSez(p.go[1]); });
      b.setAttribute('data-tile', p.k); b.setAttribute('data-portal', p.k);
      var bg = el('span', 'hm-p-bg'); bg.setAttribute('aria-hidden', 'true'); b.appendChild(bg);
      var fb = function () { if (p.scene) bg.insertAdjacentHTML('afterbegin', hmScene(p.scene)); };
      var im = hmLoad(bg, p.img, 'hm-p-img', function () { b.classList.add('hm-p-noimg'); fb(); });
      im.loading = 'lazy';
      // inquadratura: ritaglio di una copertina condivisa (pos/zoom) solo se manca l'asset dedicato; l'asset dedicato si mostra intero (cover)
      im.addEventListener('load', function () {
        if (hmOpt(bg.getAttribute('data-src') || '')) { im.style.transform = ''; im.style.objectPosition = p.dpos || '50% 40%'; var gm = b.querySelector('.hm-gems'); if (gm) gm.remove(); /* l'illustrazione dedicata contiene gia' le sei Gemme */ }
        else { if (p.pos) im.style.objectPosition = p.pos; if (p.zoom) { im.style.transform = 'scale(' + p.zoom + ')'; im.style.transformOrigin = p.pos || '50% 50%'; } }
      });
      if (p.pos) im.style.objectPosition = p.pos;
      if (p.zoom) im.style.transform = 'scale(' + p.zoom + ')', im.style.transformOrigin = p.pos || '50% 50%';
      b.appendChild(el('span', 'hm-p-shade'));
      var tx = el('span', 'hm-p-t'); tx.appendChild(el('b', '', p.n)); tx.appendChild(el('small', '', p.sub)); b.appendChild(tx);
      if (p.gems) { var dots = el('span', 'hm-gems'); dots.setAttribute('aria-hidden', 'true'); ['#3a7dd6', '#e8c93a', '#d6483a', '#8f5bd0', '#4fae6a', '#f0954a'].forEach(function (c) { var i = el('i'); i.style.background = c; dots.appendChild(i); }); b.appendChild(dots); }
      b.appendChild(el('span', 'hm-p-go', 'Entra')); b.lastChild.setAttribute('aria-hidden', 'true');
      b.setAttribute('aria-label', p.n + ' — ' + p.sub);
      return b;
    }
    function renderHome() {
      body.className = 'a2-scroll a2-home hm'; body.textContent = '';
      setTitle('Home');
      var S0 = hmStats(), nU = S0.universi, nC = S0.personaggi, nT = S0.titoliTimeline;
      /* ① Osservatorio */
      var hero = el('section', 'hm-hero'); hero.setAttribute('aria-labelledby', 'hmH1');
      var sky = el('div', 'hm-sky'); sky.setAttribute('aria-hidden', 'true');
      var fx = el('div', 'hm-fx'); for (var q = 0; q < 14; q++) { var pt = el('i', 'hm-pt'); pt.style.left = (6 + (q * 37) % 88) + '%'; pt.style.top = (8 + (q * 53) % 70) + '%'; pt.style.animationDelay = ((q * 0.7) % 6).toFixed(1) + 's'; pt.style.animationDuration = (7 + q % 5) + 's'; fx.appendChild(pt); }
      var himg = el('div', 'hm-orb'); hmLoad(himg, HM_HERO, 'hm-orb-img', function () { himg.classList.add('hm-orb-none'); himg.innerHTML = hmScene('luoghi'); });
      sky.appendChild(himg); sky.appendChild(el('div', 'hm-beam')); sky.appendChild(fx); hero.appendChild(sky);
      var ht = el('div', 'hm-hero-t');
      ht.appendChild(el('span', 'a2-kick hm-kick', 'TVA ARCHIVES · OSSERVATORIO'));
      var h1 = el('h1', '', 'L’Atlante del Multiverso'); h1.id = 'hmH1'; ht.appendChild(h1);
      ht.appendChild(el('p', 'hm-lead', 'Un archivio dimensionale di universi, identità, cronologie e relazioni della Sacra Timeline, catalogati dalla TVA.'));
      var st = el('ul', 'hm-stats'); st.setAttribute('aria-label', 'Contenuti dell’archivio');
      [[nU, 'universi'], [nC, 'personaggi'], [nT, 'titoli della Timeline']].forEach(function (p) { var li = el('li'); li.appendChild(el('b', '', String(p[0]))); li.appendChild(el('span', '', p[1])); st.appendChild(li); });
      ht.appendChild(st); hero.appendChild(ht); body.appendChild(hero);
      /* ③ Console (sopra i portali: la ricerca e' sempre raggiungibile) */
      var con = el('section', 'hm-console'); con.setAttribute('aria-label', 'Console di ricerca');
      var res = el('div', 'a2-res hm-res');
      con.appendChild(searchBox('a2HomeSearch', ST.sq, function (v) { ST.sq = v; drawResults(res, v); }, 'Cerca personaggi, universi, titoli…'));
      var qa = el('div', 'hm-quick');
      var b1 = btn('hm-q', null, function () { nav('confronto', { arc: 'pot', eid: '|', au: 'tutti', aq: '' }); }); b1.appendChild(art('poteri', 'hm-q-ic')); b1.appendChild(el('span', '', 'Confronta poteri')); b1.setAttribute('data-quick', 'confronto');
      var b2 = btn('hm-q', null, function () { nav('catalogo'); }); b2.appendChild(art('casa', 'hm-q-ic')); b2.appendChild(el('span', '', 'Indice completo')); b2.setAttribute('data-quick', 'indice');
      qa.appendChild(b1); qa.appendChild(b2); con.appendChild(qa); con.appendChild(res); body.appendChild(con); drawResults(res, ST.sq);
      /* ② Portali per capitolo */
      var P = hmPortals(nU, nC, nT);
      HM_CH.forEach(function (c) {
        var sec = el('section', 'hm-ch hm-ch-' + c.k); sec.setAttribute('aria-labelledby', 'hmc-' + c.k);
        var hd = el('header', 'hm-ch-h'); hd.appendChild(el('span', 'hm-ch-n', 'Capitolo ' + c.num)); var h2 = el('h2', '', c.n); h2.id = 'hmc-' + c.k; hd.appendChild(h2); hd.appendChild(el('p', '', c.t)); sec.appendChild(hd);
        var gr = el('div', 'hm-grid');
        P.filter(function (p) { return p.ch === c.k; }).forEach(function (p) { gr.appendChild(hmPortal(p)); });
        sec.appendChild(gr); body.appendChild(sec);
      });
      var ft = el('section', 'a2-foot hm-foot');
      var bx = btn('a2-ghost', 'Torna all’app Marvel', function () { exitApp(); }); ft.appendChild(bx);
      ft.appendChild(el('p', 'a2-note', 'Progressi, XP e badge restano quelli dell’app: TVA Archives li legge senza modificarli.')); body.appendChild(ft);
    }

    /* ---------- schermata: catalogo ---------- */
    function renderCatalogo() {
      body.className = 'a2-scroll'; body.textContent = ''; setTitle('Tutti gli archivi', 'Catalogo');
      body.appendChild(heading('CATALOGO', 'Tutti gli archivi', 'Quattro aree. Le voci «In preparazione» mostrano soltanto la struttura: non contengono ancora schede.'));
      GRP.forEach(function (g, gi) {
        var s = el('section', 'a2-cat'); var h = el('h3'); h.appendChild(el('span', 'a2-cat-n', String(gi + 1))); h.appendChild(D.createTextNode(g.n)); s.appendChild(h);
        g.items.forEach(function (i) { var r = row(i, function () { openSez(i.k); }); r.setAttribute('data-sez', i.k); s.appendChild(r); });
        body.appendChild(s);
      });
      var n = el('p', 'a2-note', 'Integrati: Varianti → Personaggi · Alberi Genealogici → Relazioni · Battaglie → Eventi · Gemme dell’Infinito → Artefatti.'); body.appendChild(n);
    }
    function renderSezione() {
      var s = SEZ[ST.sez]; if (!s || !s.subs) { ST.screen = 'catalogo'; return renderCatalogo(); }
      body.className = 'a2-scroll'; body.textContent = ''; setTitle(s.n, s.g.n);
      body.appendChild(heading(s.g.n.toUpperCase(), s.n, s.d));
      var box = el('section', 'a2-cat'); s.subs.forEach(function (x) { box.appendChild(row({ n: x.n, d: x.d, art: s.art }, function () { run(x.act); })); }); body.appendChild(box);
    }
    function renderSoon() {
      var s = SEZ[ST.sez]; if (!s) { ST.screen = 'catalogo'; return renderCatalogo(); }
      body.className = 'a2-scroll'; body.textContent = ''; setTitle(s.n, s.g.n);
      body.appendChild(heading(s.g.n.toUpperCase(), s.n, null));
      var c = el('section', 'a2-soon'); c.appendChild(badge('prep'));
      c.appendChild(el('p', '', 'Questa sezione è prevista nelle prossime fasi di TVA Archives. Per ora non contiene schede: nessun contenuto è stato inventato.'));
      if (s.extra) { c.appendChild(el('p', 'a2-note', s.extra.txt)); c.appendChild(btn('a2-primary', s.extra.n, function () { run(s.extra.act); })); }
      c.appendChild(btn('a2-ghost', 'Torna al catalogo', function () { nav('catalogo'); }));
      body.appendChild(c);
    }

    /* ---------- schermata: Cronologie ---------- */
    function renderCronologie() {
      body.className = 'a2-scroll'; body.textContent = ''; setTitle('Cronologie', 'Multiverso e Tempo');
      body.appendChild(heading('MULTIVERSO E TEMPO', 'Cronologie', 'Percorsi già presenti nell’app, raccolti in un unico punto.'));
      var s0 = el('section', 'a2-cat'); s0.appendChild(el('h3', '', 'Esplora il tempo'));
      [['Cronologia di un universo', 'Il percorso dei titoli di un universo, con date certe, approssimative e mancanti distinte.', 'uni'], ['Cronologie parallele', 'Confronta due universi senza inventare corrispondenze fra epoche.', 'par'],
       ['Esplora nel tempo', 'Cerca un titolo e filtra per universo, periodo, saga e tipo.', 'exp']].forEach(function (p) { var r0 = row({ n: p[0], d: p[1], art: 'cronologie' }, function () { crOpen(p[2]); }); r0.setAttribute('data-cr', p[2]); s0.appendChild(r0); });
      body.appendChild(s0);
      var s1 = el('section', 'a2-cat'); s1.appendChild(el('h3', '', 'Timeline'));
      [['Ordine di visione', 'La Timeline Marvel con i tuoi progressi.', ['tl']], ['Timeline degli Universi', 'I titoli disposti per universo.', ['tog', 'universeTimelineToggle']],
       ['Timeline alternativa', 'Un secondo ordine di visione.', ['tog', 'altTimelineToggle']]].forEach(function (p) { s1.appendChild(row({ n: p[0], d: p[1], art: 'cronologie' }, function () { run(p[2]); })); });
      body.appendChild(s1);
      var s2 = el('section', 'a2-cat'); s2.appendChild(el('h3', '', 'Cronologie tematiche'));
      [['chrono-kang', 'Kang', 'Le identità di Nathaniel Richards.'], ['chrono-loki', 'Loki', 'Le versioni e le linee di Loki.'], ['chrono-doom', 'Doom', 'Victor Von Doom attraverso i titoli.'],
       ['chrono-simbionte-venom', 'Simbionti', 'I simbionti della saga.'], ['chrono-tva', 'TVA', 'La Time Variance Authority.'], ['chrono-gemme-dell-infinito', 'Gemme dell’Infinito', 'Dove compare ogni Gemma.'],
       ['chrono-battleworld', 'Battleworld', 'Secret Wars e Battleworld.']].forEach(function (p) {
        if (!D.querySelector('#tvaArchivesOverlayEl [data-target="' + p[0] + '"]')) return;
        s2.appendChild(row({ n: p[1], d: p[2], art: 'cronologie' }, function () { run(['chr', p[0]]); }));
      });
      body.appendChild(s2);
      var s3 = el('section', 'a2-cat'); s3.appendChild(el('h3', '', 'Eventi e percorsi'));
      [['Timeline delle Incursioni', 'Quando due universi si toccano: cos’è un’incursione e dove la guida la mostra.', 'inc'], ['Maratona Weekend', 'Dieci film per l’arco narrativo essenziale della saga.', 'mar']].forEach(function (p) {
        s3.appendChild(row({ n: p[0], d: p[1], art: 'cronologie' }, function () { run(['doc', p[2]]); }));
      });
      body.appendChild(s3);
    }
    /* ---------- schermata: Relazioni ---------- */
    function renderRelazioni() {
      body.className = 'a2-scroll'; body.textContent = ''; setTitle('Relazioni', 'Identità e Potere');
      body.appendChild(heading('IDENTITÀ E POTERE', 'Relazioni', 'Collegamenti tra titoli, personaggi e universi, e le famiglie dei personaggi.'));
      var s = el('section', 'a2-cat');
      [['Grafo delle Relazioni', 'Titoli, personaggi e universi collegati.', ['tog', 'relationshipGraphToggle']], ['Alberi Genealogici', 'Le famiglie dei personaggi.', ['card', 'Alberi Genealogici']],
       ['Kang e la TVA', 'Il grafo delle varianti di Kang e della TVA.', ['tog', 'kangTvaGraphToggle']]].forEach(function (p) { s.appendChild(row({ n: p[0], d: p[1], art: 'relazioni' }, function () { run(p[2]); })); });
      s.appendChild(row({ n: 'Varianti', d: 'Le varianti e le incarnazioni, tra i Personaggi.', art: 'personaggi' }, function () { nav('personaggi', { pf: 'varianti' }); }));
      body.appendChild(s);
    }
    /* ---------- schermata: ricerca ---------- */
    function renderSearch() {
      body.className = 'a2-scroll'; body.textContent = ''; setTitle('Ricerca universale', 'Ricerca');
      var res = el('div', 'a2-res');
      body.appendChild(searchBox('a2Search', ST.sq, function (v) { ST.sq = v; drawResults(res, v); }));
      body.appendChild(res); drawResults(res, ST.sq);
      if (!ST.sq.trim()) body.appendChild(el('p', 'a2-note', 'Cerca tra archivi, universi, titoli e personaggi. Esempi: «gemme», «Loki», «battaglie», «616».'));
    }

    /* ---------- schermata: Personaggi ---------- */
    function renderPersonaggi() {
      body.className = 'a2-scroll'; body.textContent = ''; setTitle('Personaggi', 'Identità e Potere');
      var all = personaggiLista(), nVar = all.filter(isVar).length;
      body.appendChild(heading('IDENTITÀ E POTERE', 'Personaggi', all.length + ' schede in ordine alfabetico. Le voci generiche (segnaposto) non sono elencate.'));
      var stick = el('div', 'a2-stick');
      var list = el('div', 'a2-plist'), jump = el('div', 'a2-jump');
      stick.appendChild(searchBox('a2PSearch', ST.pq, function (v) { ST.pq = v; draw2(); }, 'Cerca un personaggio…'));
      var f = el('div', 'a2-filters'); f.setAttribute('role', 'group'); f.setAttribute('aria-label', 'Filtra i personaggi');
      [['tutti', 'Tutti ' + all.length], ['varianti', 'Varianti e incarnazioni ' + nVar]].forEach(function (p) {
        var b = btn('a2-f' + (ST.pf === p[0] ? ' on' : ''), p[1], function () { ST.pf = p[0]; Array.prototype.forEach.call(f.children, function (x) { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); }); b.classList.add('on'); b.setAttribute('aria-pressed', 'true'); draw2(); });
        b.setAttribute('aria-pressed', ST.pf === p[0] ? 'true' : 'false'); f.appendChild(b);
      });
      stick.appendChild(f); stick.appendChild(jump); body.appendChild(stick); body.appendChild(list);
      function draw2() {
        list.textContent = ''; jump.textContent = '';
        var q = ST.pq.trim().toLowerCase();
        var arr = all.filter(function (c) { return (ST.pf !== 'varianti' || isVar(c)) && (!q || c.name.toLowerCase().indexOf(q) !== -1); })
          .sort(function (a, b) { return a.name.localeCompare(b.name, 'it', { sensitivity: 'base' }); });
        var groups = {}, order = [];
        arr.forEach(function (c) { var L = c.name.charAt(0).toUpperCase(); if (!/[A-Z]/.test(L.normalize('NFD').charAt(0))) L = '#'; else L = L.normalize('NFD').charAt(0); if (!groups[L]) { groups[L] = []; order.push(L); } groups[L].push(c); });
        order.forEach(function (L) {
          var jb = btn('a2-jl', L, function () { var t = list.querySelector('[data-l="' + L + '"]'); if (t) body.scrollTop = Math.max(0, t.offsetTop - stick.offsetHeight - 4); });
          jb.setAttribute('aria-label', 'Vai alla lettera ' + L); jump.appendChild(jb);
          var g = el('section', 'a2-pgrp'); g.setAttribute('data-l', L); g.appendChild(el('h3', '', L));
          groups[L].forEach(function (c) {
            var b = btn('a2-prow', null); b.setAttribute('data-go', 'char:' + c.id); b.appendChild(cover('chr', c.id, c.name, 'a2-cov-xs'));
            var t = el('span', 'a2-lrow-t'); t.appendChild(el('b', '', c.name));
            var o = IDX.origineDa(c.id).filter(function (u) { return UNI[u]; }).map(IDX.breve);
            t.appendChild(el('small', '', (isVar(c) ? 'Variante · ' : '') + (o.length ? 'origine: ' + o.slice(0, 2).join(', ') : 'origine non indicata'))); b.appendChild(t); g.appendChild(b);
          });
          list.appendChild(g);
        });
        if (!arr.length) list.appendChild(el('p', 'a2-empty', 'Nessun personaggio corrisponde. Cambia ricerca o filtro.'));
        else list.appendChild(el('p', 'a2-note', arr.length + (arr.length === 1 ? ' scheda' : ' schede') + '. Tocca un nome per aprire la scheda.'));
      }
      draw2();
    }

    /* ---------- schermata: Universi (ex panoramica dell'Atlante 2.0) ---------- */
    function renderUniversi() {
      body.className = 'a2-scroll'; body.textContent = '';
      var uids = Object.keys(UNI);
      setTitle('Multiverso', uids.length + ' universi');
      body.appendChild(heading('MULTIVERSO E TEMPO', 'Il multiverso, universo per universo', 'Ogni scheda mostra solo i titoli e i personaggi che i dati della guida associano a quell’universo. Dove un dato non c’è, non viene inventato.'));
      var mp = btn('a2-primary a2-map', 'Apri la mappa del Multiverso', function () { openMappa(); }); mp.id = 'a2OpenMap'; body.appendChild(mp);
      var mp2 = btn('a2-ghost a2-map2', 'Grafo classico', function () { run(['tog', 'multiverseGraphToggle']); }); mp2.id = 'a2OpenClassic'; body.appendChild(mp2);
      body.appendChild(legend(false));
      var sb = el('div', 'a2-search'); var inp = D.createElement('input'); inp.type = 'search'; inp.id = 'a2UniSearch'; inp.placeholder = 'Filtra gli universi per nome…'; inp.value = ST.q;
      inp.setAttribute('aria-label', 'Filtra gli universi'); inp.autocomplete = 'off'; inp.setAttribute('enterkeyhint', 'search'); sb.appendChild(inp); body.appendChild(sb);
      var f1 = el('div', 'a2-filters'); f1.setAttribute('role', 'group'); f1.setAttribute('aria-label', 'Filtra per tipologia');
      var natKeys = ['tutti'].concat(Object.keys(NAT).map(function (k) { return NAT[k].k; }));
      natKeys.forEach(function (k) {
        var lbl = k === 'tutti' ? 'Tutti' : (Object.keys(NAT).map(function (n) { return NAT[n]; }).filter(function (x) { return x.k === k; })[0] || {}).lbl;
        var n = k === 'tutti' ? uids.length : uids.filter(function (u) { return nat(UNI[u]).k === k; }).length;
        if (!n) return;
        var b = btn('a2-f' + (ST.nat === k ? ' on' : ''), lbl + ' ' + n, function () { ST.nat = k; renderUniversi(); });
        b.setAttribute('aria-pressed', ST.nat === k ? 'true' : 'false'); f1.appendChild(b);
      });
      body.appendChild(f1);
      var f2 = el('div', 'a2-filters a2-fam'); f2.setAttribute('role', 'group'); f2.setAttribute('aria-label', 'Filtra per famiglia');
      [['tutte', 'Tutte le famiglie']].concat(Object.keys(FAM).map(function (k) { return [k, (FAM[k].ic || '') + ' ' + FAM[k].nome]; })).forEach(function (p) {
        var b = btn('a2-f' + (ST.fam === p[0] ? ' on' : ''), p[1], function () { ST.fam = p[0]; renderUniversi(); });
        b.setAttribute('aria-pressed', ST.fam === p[0] ? 'true' : 'false'); f2.appendChild(b);
      });
      body.appendChild(f2);
      var gridWrap = el('div', 'a2-grid'); body.appendChild(gridWrap);
      function drawGrid() {
        gridWrap.textContent = '';
        var q = ST.q.trim().toLowerCase();
        var list = uids.filter(function (u) {
          if (ST.nat !== 'tutti' && nat(UNI[u]).k !== ST.nat) return false;
          if (ST.fam !== 'tutte' && (FAM[ST.fam].universi || []).indexOf(u) === -1) return false;
          if (q && (UNI[u].nome || '').toLowerCase().indexOf(q) === -1) return false;
          return true;
        });
        list.forEach(function (u) {
          var d = UNI[u], n = nat(d), p = prog(u);
          var c = btn('a2-card a2-n-' + n.k, null, function () { openUni(u); });
          c.setAttribute('data-uid', u);
          var h = el('div', 'a2-card-h'); h.appendChild(el('span', 'a2-card-ic', n.ic)); h.appendChild(el('span', 'a2-card-n', d.nome)); c.appendChild(h);
          c.appendChild(el('span', 'a2-badge', n.lbl));
          c.appendChild(el('span', 'a2-card-m', p.n ? (p.n + (p.n === 1 ? ' titolo' : ' titoli') + ' · ' + p.v + ' visti') : 'Nessun titolo associato'));
          var bar = el('span', 'a2-bar'); var fi = el('i'); fi.style.width = (p.n ? Math.round(p.v / p.n * 100) : 0) + '%'; bar.appendChild(fi); c.appendChild(bar);
          gridWrap.appendChild(c);
        });
        if (!list.length) gridWrap.appendChild(el('p', 'a2-empty', 'Nessun universo corrisponde ai filtri. Rimuovi un filtro o cambia ricerca.'));
      }
      var tm = null;
      inp.addEventListener('input', function () { clearTimeout(tm); tm = setTimeout(function () { ST.q = inp.value; drawGrid(); }, 120); });
      drawGrid();
    }
    /* ---------- schermata: scheda universo = DOSSIER (FASE 3A) ----------
       Costruito esclusivamente sul modello condiviso tvaUniverse (sola lettura). Un modulo compare solo se ha dati: nessun evento o collegamento viene inventato. */
    var UM = W.tvaUniverse;
    function sec(titleTxt) { var s = el('section', 'a2-sec'); s.appendChild(el('h3', '', titleTxt)); return s; }
    var UD_FAM = { sony: 'uni_sony', fox: 'uni_fox', spiderverse: 'uni_spiderverse', legacy: 'uni_legacy', whatif: 'uni_whatif', animazione: 'uni_animazione' };
    var UD_STATO = { confermato: { ic: '●', cls: 'ok' }, legacy: { ic: '○', cls: 'lg' }, verificare: { ic: '◇', cls: 'vf' } };
    function udAsset(uid) { var f = (UM.get(uid).famiglie[0]); return uid === MCU ? 'uni_mcu' : (f && UD_FAM[f]) || null; }
    // ambiente procedurale (SVG statico, ~1 KB) usato finché non esiste l'illustrazione dedicata della famiglia: stesso schema per famiglia, variazione per universo
    function udScene(uid, fam) {
      var h = hsh(uid), k = function (m, s) { return (h >>> (s * 3)) % m; }, g = '', i, G = '#D2B184', R = '#DB777C';
      var cx = 250 + k(60, 1), cy = 82 + k(40, 2);
      if (fam === 'spiderverse') { for (i = 0; i < 9; i++) { var a = i * Math.PI / 4.5; g += '<line x1="' + cx + '" y1="' + cy + '" x2="' + (cx + 260 * Math.cos(a)).toFixed(0) + '" y2="' + (cy + 260 * Math.sin(a)).toFixed(0) + '" stroke="' + G + '" stroke-opacity=".28"/>'; } for (i = 1; i < 6; i++) g += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (i * 26) + '" fill="none" stroke="' + R + '" stroke-opacity="' + (0.5 - i * 0.07).toFixed(2) + '" stroke-dasharray="' + (i * 5) + ' 7"/>'; }
      else if (fam === 'sony') { for (i = 0; i < 7; i++) g += '<path d="M' + (40 + i * 52) + ' 0Q' + (60 + k(80, i % 5)) + ' 110 ' + (cx - 60 + i * 20) + ' 220" fill="none" stroke="' + G + '" stroke-opacity=".3"/>'; g += '<circle cx="' + cx + '" cy="' + cy + '" r="22" fill="none" stroke="' + R + '" stroke-opacity=".6"/>'; }
      else if (fam === 'fox') { for (i = 0; i < 5; i++) g += '<path d="M' + (i * 90 - 40) + ' 0L' + (i * 90 + 130) + ' 220M' + (i * 90 + 130) + ' 0L' + (i * 90 - 40) + ' 220" stroke="' + (i % 2 ? G : R) + '" stroke-opacity=".22" fill="none"/>'; }
      else if (fam === 'legacy') { for (i = 0; i < 5; i++) g += '<rect x="' + (14 + i * 78) + '" y="' + (40 + k(30, i % 4)) + '" width="62" height="100" rx="3" fill="none" stroke="' + G + '" stroke-opacity=".3"/><circle cx="' + (45 + i * 78) + '" cy="' + (28 + k(10, i % 3)) + '" r="3" fill="' + R + '" fill-opacity=".6"/>'; }
      else if (fam === 'whatif') { for (i = 0; i < 6; i++) g += '<path d="M' + cx + ' 220C' + (cx - 90 + i * 36) + ' 150 ' + (60 + i * 60) + ' 100 ' + (30 + i * 66) + ' ' + (10 + k(40, i % 5)) + '" fill="none" stroke="' + (i % 2 ? G : R) + '" stroke-opacity=".4"/><circle cx="' + (30 + i * 66) + '" cy="' + (10 + k(40, i % 5)) + '" r="3" fill="' + G + '"/>'; }
      else if (fam === 'animazione') { for (i = 0; i < 4; i++) g += '<rect x="' + (30 + i * 28) + '" y="' + (20 + i * 14) + '" width="' + (300 - i * 40) + '" height="' + (150 - i * 22) + '" rx="10" fill="none" stroke="' + (i % 2 ? R : G) + '" stroke-opacity="' + (0.5 - i * 0.08).toFixed(2) + '"/>'; }
      else { for (i = 1; i < 5; i++) g += '<ellipse cx="' + cx + '" cy="' + cy + '" rx="' + (i * 48) + '" ry="' + (i * 17) + '" fill="none" stroke="' + G + '" stroke-opacity="' + (0.55 - i * 0.1).toFixed(2) + '" transform="rotate(' + (-24 + i * 6) + ' ' + cx + ' ' + cy + ')"/>'; g += '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="' + G + '"/>'; }
      for (i = 0; i < 12; i++) g += '<circle cx="' + ((h >>> (i % 7)) % 380 + 10) + '" cy="' + ((h >>> ((i + 3) % 9)) % 200 + 8) + '" r="' + (0.8 + (i % 3) * 0.5) + '" fill="#F2E8D8" fill-opacity=".5"/>';
      return '<svg viewBox="0 0 400 220" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">' + g + '</svg>';
    }
    function udRiga(e, i, uid, conAltri) {
      var c = e.li.querySelector('.watch-check, .anim-watch-check'), seen = !!(c && c.checked);
      var li = el('li'); var b = btn('a2-row' + (seen ? ' seen' : '') + (conAltri ? ' a2-row-x' : ''), null);
      b.setAttribute('data-go', 'item:' + e.id);
      b.appendChild(el('span', 'a2-row-n', String(i + 1)));
      var tx = el('span', 'a2-row-t'); tx.appendChild(el('b', '', e.title));
      tx.appendChild(el('small', '', [tipoTitolo(e), anno(e), e.num ? 'N°' + VN(e.num) : ''].filter(Boolean).join(' · ')));
      if (conAltri) {
        var altri = e.unis.filter(function (o) { return o !== uid && UNI[o]; }).map(IDX.breve);
        if (altri.length) tx.appendChild(el('small', 'a2-row-x-l', '↗ insieme a: ' + altri.join(', ')));
      }
      var am = e.kind === 'item' ? IDX.ambientazione(e.num) : '';
      if (am) {
        var ya = ST.ord === 'ambientazione' ? UM.annoAmbientazione(am) : null;
        tx.appendChild(el('small', 'a2-row-amb', 'Ambientazione: ' + am + (ya && ya.y !== null && ya.approx ? ' (data approssimativa)' : '') + (ya && ya.y === null ? ' (non datata)' : '')));
      }
      b.appendChild(tx);
      b.appendChild(el('span', 'a2-row-s', seen ? '✓' : '○')); b.setAttribute('aria-label', e.title + (conAltri ? ', crossover' : '') + (seen ? ', visto' : ', da vedere'));
      li.appendChild(b); return li;
    }
    function udBadge(stato) { var s = UD_STATO[stato]; return el('span', 'ud-st ud-st-' + s.cls, s.ic + ' ' + UM.stati[stato]); }
    function udTitoliChips(nums) {
      var box = el('div', 'ud-refs');
      nums.slice().sort(byGuide).forEach(function (n) { var t = IDX.titoli['item-' + n]; if (!t) return; var c = go('item', t.id, 'N°' + VN(n) + ' · ' + t.title); c.classList.add('ud-ref'); box.appendChild(c); });
      return box.childNodes.length ? box : null;
    }
    function udLegendaStati() {
      var d = D.createElement('details'); d.className = 'a2-legend ud-leg'; d.appendChild(el('summary', '', 'Come si leggono i tre stati'));
      var dl = el('dl');
      [['confermato', 'Documentato nella guida', 'Almeno un titolo (N°) è citato sia dai dati dell’Atlante sia dal grafo storico, e le due fonti concordano. Entrambe derivano dalla guida: non è una verifica canonica indipendente.'],
       ['legacy', 'Legacy', 'Presente nel grafo storico (crossover o cameo) con un titolo esistente, ma l’Atlante non lo riscontra né lo contraddice. Non ancora verificato.'],
       ['verificare', 'Da verificare', 'Dati ambigui, contraddittori o insufficienti: un collegamento «previsto», un titolo assegnato altrove o una relazione presente solo nei dati. La sola presenza nel database non è una conferma canonica.']
      ].forEach(function (p) { var dt = el('dt'); dt.appendChild(udBadge(p[0])); dl.appendChild(dt); dl.appendChild(el('dd', '', p[2])); });
      d.appendChild(dl); return d;
    }
    function udProvenienza(c) {
      var d = D.createElement('details'); d.className = 'ud-prov'; d.appendChild(el('summary', '', 'Provenienza e motivo'));
      var ul = el('ul', 'ud-fonti');
      c.fonti.forEach(function (f) {
        ul.appendChild(el('li', '', f.fonte + (f.tipo ? ' · ' + (UM.tipi[f.tipo] || f.tipo) : '') + (f.titoli && f.titoli.length ? ' · N°' + f.titoli.slice().sort(byGuide).map(VN).join(', N°') : '')));
      });
      d.appendChild(ul); if (c.motivo) d.appendChild(el('p', 'a2-note', c.motivo)); return d;
    }
    function renderUni(uid) {
      var d = UNI[uid]; if (!d || !UM) { ST.screen = 'universi'; return renderUniversi(); }
      body.className = 'a2-scroll a2-dossier'; body.textContent = '';
      var m = UM.get(uid), n = nat(d), p = prog(uid), tt = m.titoli, cd = classicDescr(uid), fk = m.famiglie[0], famNome = fk && FAM[fk] ? FAM[fk].nome : (uid === MCU ? 'Continuità principale' : '');
      setTitle(d.nome, n.lbl);
      var mods = []; // indice dei moduli: solo quelli con dati
      function modulo(key, lbl, s) { s.setAttribute('data-mod', key); s.id = 'ud-' + key; mods.push([key, lbl]); body.appendChild(s); return s; }

      /* --- hero: illustrazione di famiglia (se esiste) oppure ambiente procedurale --- */
      var hero = el('section', 'a2-hero ud-hero a2-n-' + n.k); hero.setAttribute('data-fam', fk || (uid === MCU ? 'mcu' : 'altro'));
      var bg = el('div', 'ud-bg'); bg.setAttribute('aria-hidden', 'true');
      var fall = function () { bg.classList.add('ud-bg-proc'); bg.innerHTML = udScene(uid, fk); };
      var asset = udAsset(uid);
      if (asset) hmLoad(bg, [HM_DIR + asset + '.webp'], 'ud-bg-img', fall); else fall();
      hero.appendChild(bg); hero.appendChild(el('div', 'ud-shade'));
      var hc = el('div', 'ud-hero-c');
      hc.appendChild(el('span', 'ud-kick', [famNome, n.lbl].filter(Boolean).join(' · ').toUpperCase()));
      hc.appendChild(el('h2', '', d.nome));
      if (d.naturaNota) hc.appendChild(el('p', 'ud-nota', d.naturaNota));
      if (cd.DESCRIZIONE) hc.appendChild(el('p', 'a2-descr', cd.DESCRIZIONE));
      if (cd['COMPARE IN']) hc.appendChild(el('p', 'a2-note', 'Nella guida: ' + cd['COMPARE IN']));
      if (uid === MCU) hc.appendChild(infoDet('Nota sulla numerazione: Earth-199999 e «616»', NOTA_NUM));
      hero.appendChild(hc);
      var st = el('ul', 'ud-stats'); var nOrig = m.origine.length + m.presenti.length;
      [[m.appartenenza.length, 'titoli propri'], [m.crossover.length, 'crossover'], [nOrig, 'personaggi'], [m.collegamenti.length, 'collegamenti']].forEach(function (x) {
        if (!x[0]) return; var li = el('li'); li.appendChild(el('b', '', String(x[0]))); li.appendChild(el('span', '', x[1])); st.appendChild(li);
      });
      if (st.childNodes.length) hero.appendChild(st);
      body.appendChild(hero);
      var hAct = el('div', 'ud-hacts'); var hCr = btn('a2-ghost', 'Cronologia di questo universo', function () { crOpen('uni', { uid: uid }); }); hCr.id = 'udOpenCron'; hAct.appendChild(hCr); body.appendChild(hAct);
      var navSlot = el('nav', 'ud-index a2-jump'); navSlot.setAttribute('aria-label', 'Moduli del dossier'); body.appendChild(navSlot);
      if (tt.length) body.appendChild(legend(false));

      /* --- progresso --- */
      var nCross = m.crossover.length;
      if (p.n) {
        var s1 = sec('Il tuo progresso'); s1.appendChild(el('div', 'a2-prog-t', p.v + ' di ' + p.n + ' titoli visti' + (nCross ? ' · di cui ' + nCross + ' crossover' : '')));
        var bar = el('div', 'a2-bar a2-bar-lg'); var fi = el('i'); fi.style.width = Math.round(p.v / p.n * 100) + '%'; bar.appendChild(fi); s1.appendChild(bar); body.appendChild(s1);
      }

      /* --- titoli: tre ordini --- */
      if (tt.length) {
        var okU = tt.filter(function (e) { return USCITA[e.num]; }).length >= 2, okA = tt.filter(function (e) { return e.kind === 'item' && UM.annoAmbientazione(IDX.ambientazione(e.num)).y !== null; }).length >= 2;
        if (ST.ord === 'uscita' && !okU) ST.ord = 'guida'; if (ST.ord === 'ambientazione' && !okA) ST.ord = 'guida';
        var s2 = sec('Titoli di appartenenza (' + m.appartenenza.length + ')'); s2.classList.add('a2-sec-prim');
        var modi = [['guida', 'Ordine della guida']]; if (okU) modi.push(['uscita', 'Per data di uscita']); if (okA) modi.push(['ambientazione', 'Per ambientazione']);
        function riordina(k) { var y = body.scrollTop; ST.ord = k; renderUni(uid); body.scrollTop = y; }
        if (modi.length > 1) {
          var ordBox = el('div', 'a2-filters ud-ord'); ordBox.setAttribute('role', 'group'); ordBox.setAttribute('aria-label', 'Ordine dei titoli');
          modi.forEach(function (o) { var b = btn('a2-f' + (ST.ord === o[0] ? ' on' : ''), o[1], function () { riordina(o[0]); }); b.setAttribute('aria-pressed', ST.ord === o[0] ? 'true' : 'false'); ordBox.appendChild(b); });
          s2.appendChild(ordBox);
        }
        var oinfo = null;
        function elenco(list, conAltri) { var o = UM.ordina(list, ST.ord); oinfo = o; var ol = el('ol', 'a2-list'); o.lista.forEach(function (e, i) { ol.appendChild(udRiga(e, i, uid, conAltri)); }); return ol; }
        if (m.appartenenza.length) {
          s2.appendChild(elenco(m.appartenenza, false));
          var nota = ST.ord === 'uscita' ? 'Ordinati per data di uscita' + (oinfo.senzaDato ? ' (' + oinfo.senzaDato + (oinfo.senzaDato === 1 ? ' titolo senza data in coda' : ' titoli senza data in coda') + ')' : '') + '. '
            : ST.ord === 'ambientazione' ? 'Ordinati per anno di ambientazione ricavato dal testo della guida' + (oinfo.approx ? ' (alcune date sono approssimative)' : '') + (oinfo.senzaDato ? '; ' + oinfo.senzaDato + (oinfo.senzaDato === 1 ? ' titolo non datato in coda' : ' titoli non datati in coda') : '') + '. '
            : 'Ordine consigliato dalla guida (N°). ';
          s2.appendChild(el('p', 'a2-note', nota + 'Assegnati dalla guida a questo universo.'));
        } else s2.appendChild(el('p', 'a2-empty', 'Nessun titolo è assegnato in via esclusiva a questo universo dai dati della guida.' + (m.crossover.length ? ' Compare soltanto nei crossover qui sotto.' : '')));
        var acts = el('div', 'ud-acts');
        var tb = btn('a2-primary', 'Mostra solo questi titoli in Timeline'); tb.setAttribute('data-go', 'filter:' + uid); acts.appendChild(tb);
        acts.appendChild(btn('a2-ghost', 'Apri le Cronologie', function () { run(['scr', 'cronologie']); }));
        s2.appendChild(acts);
        modulo('titoli', 'Titoli', s2);
        if (m.crossover.length) {
          var s2c = sec('Crossover (' + m.crossover.length + ')'); s2c.classList.add('a2-sec-cro');
          s2c.appendChild(el('p', 'a2-note', 'Coinvolgono questo universo e almeno un altro. La guida non indica un universo principale: non sono attribuiti a uno solo e non contano come «appartenenza».'));
          s2c.appendChild(elenco(m.crossover, true)); modulo('crossover', 'Crossover', s2c);
        }
        if (m.varianti.length) {
          var s2v = sec('Versione alternativa (non conteggiata)'); s2v.classList.add('a2-sec-var');
          s2v.appendChild(el('p', 'a2-note', 'Riedizione di un titolo già presente: non è un titolo autonomo e non aumenta i conteggi.'));
          var olv = el('ol', 'a2-list'); m.varianti.forEach(function (e, i) { olv.appendChild(udRiga(e, i, uid, false)); }); s2v.appendChild(olv); modulo('varianti', 'Varianti', s2v);
        }
      }

      /* --- personaggi --- */
      if (m.have.personaggi) {
        var s3 = sec('Personaggi (' + nOrig + ')');
        if (m.principali.length) s3.appendChild(el('p', 'a2-note', 'Principali: ' + m.principali.join(', ') + '.'));
        var gruppo = function (titolo, ids, nota, conOrig) {
          if (!ids.length) return;
          s3.appendChild(el('h4', 'a2-sub', titolo + ' (' + ids.length + ')'));
          var cc = el('div', 'a2-chips'); var LIM = 12;
          ids.forEach(function (cid, i) {
            var c = go('char', cid, IDX.personaggi[cid].name);
            if (conOrig) { var o = IDX.origineDa(cid).filter(function (u) { return u !== uid; }); c.appendChild(el('small', '', o.length ? 'orig.: ' + o.map(IDX.breve).slice(0, 2).join(', ') : 'orig.: non indicata')); }
            if (i >= LIM) { c.hidden = true; c.setAttribute('data-more', '1'); } cc.appendChild(c);
          });
          if (ids.length > LIM) { var mb = btn('a2-chip a2-moreb', '+' + (ids.length - LIM) + ' altri', function () { Array.prototype.forEach.call(cc.querySelectorAll('[data-more]'), function (x) { x.hidden = false; }); mb.remove(); }); cc.appendChild(mb); }
          s3.appendChild(cc); s3.appendChild(el('p', 'a2-note', nota));
        };
        gruppo('Originari di questo universo', m.origine, 'Continuità d’origine dichiarata dalla guida.', false);
        gruppo('Presenti, con origine altrove', m.presenti, 'Compaiono qui secondo la riga UNIVERSI della scheda: presenza (apparizione), non appartenenza.', true);
        if (!m.origine.length && !m.presenti.length) s3.appendChild(el('p', 'a2-empty', 'Nessuna scheda personaggio è associata a questo universo nei dati: restano solo i nomi indicati come principali.'));
        modulo('personaggi', 'Personaggi', s3);
      }

      /* --- eventi chiave: soltanto quelli dichiarati nei dati; archivi derivati dai titoli --- */
      if (m.eventiChiave.length) { var s4 = sec('Eventi chiave'); var ul = el('ul', 'a2-ul'); m.eventiChiave.forEach(function (x) { ul.appendChild(el('li', '', x)); }); s4.appendChild(ul); modulo('eventi', 'Eventi', s4); }
      var haArch = false;
      if (EXT.uniExtra) { var sx = EXT.uniExtra(uid, sec); if (sx) { modulo('archivi', 'Archivi', sx); haArch = true; } }

      /* --- collegamenti con stato e provenienza --- */
      if (m.have.collegamenti) {
        var s5 = sec('Collegamenti del Multiverso');
        s5.appendChild(el('p', 'a2-note', 'Unione dei dati dell’Atlante e del grafo storico. Ogni collegamento riporta lo stato e la fonte: un collegamento non documentato o dubbio non viene mai presentato come documentato.'));
        s5.appendChild(udLegendaStati());
        var cnt = m.conteggi, ris = el('p', 'ud-sum');
        var PL = { confermato: 'documentati nella guida', legacy: 'legacy', verificare: 'da verificare' }; ris.textContent = ['confermato', 'legacy', 'verificare'].map(function (k) { return cnt[k] + ' ' + PL[k]; }).join(' · '); s5.appendChild(ris);
        ['confermato', 'legacy', 'verificare'].forEach(function (k) {
          var lst = m.collegamenti.filter(function (c) { return c.stato === k; }); if (!lst.length) return;
          s5.appendChild(el('h4', 'a2-sub', UM.stati[k] + ' (' + lst.length + ')'));
          lst.forEach(function (c) {
            var card = el('div', 'ud-lk ud-lk-' + UD_STATO[k].cls);
            var top2 = el('div', 'ud-lk-h'); var ch = go('uni', c.con, UNI[c.con].nome); top2.appendChild(ch); top2.appendChild(udBadge(k)); card.appendChild(top2);
            card.appendChild(el('small', 'ud-lk-t', c.tipi.map(function (t) { return UM.tipi[t]; }).join(' · ')));
            var refs = udTitoliChips(c.titoli); if (refs) card.appendChild(refs);
            card.appendChild(udProvenienza(c)); s5.appendChild(card);
          });
        });
        // elementi speciali collegati dal grafo storico (non sono universi: restano separati)
        var sp = m.speciali.filter(function (x) { return x.stato; });
        if (sp.length) {
          s5.appendChild(el('h4', 'a2-sub', 'Luoghi e realtà speciali nel grafo storico (' + sp.length + ')'));
          s5.appendChild(el('p', 'a2-note', 'Non sono universi e non rientrano nei 27: sono elementi del grafo classico. Lo stato indica quanto il collegamento è verificato.'));
          sp.forEach(function (x) {
            var card = el('div', 'ud-lk ud-lk-' + UD_STATO[x.stato].cls); var top3 = el('div', 'ud-lk-h');
            top3.appendChild(el('b', 'ud-lk-n', x.entita.nome + ' · ' + x.entita.classeLbl)); top3.appendChild(udBadge(x.stato)); card.appendChild(top3);
            card.appendChild(el('small', 'ud-lk-t', UM.tipi[x.tipo] || x.tipo));
            var rf = udTitoliChips(x.titoli); if (rf) card.appendChild(rf);
            card.appendChild(el('p', 'a2-note', x.motivo)); s5.appendChild(card);
          });
        }
        var cvi = btn('a2-ghost', 'Apri il grafo classico del Multiverso', function () { run(['tog', 'multiverseGraphToggle']); }); s5.appendChild(cvi);
        modulo('collegamenti', 'Collegamenti', s5);
      }
      /* --- raggruppamenti e affinità editoriale (non sono collegamenti narrativi) --- */
      var gr = m.speciali.filter(function (x) { return !x.stato; }); var fams = m.famiglie;
      var sibl = []; fams.forEach(function (f) { (FAM[f].universi || []).forEach(function (o) { if (o !== uid && sibl.indexOf(o) === -1) sibl.push(o); }); });
      if (gr.length || sibl.length) {
        var s6 = sec('Raggruppamenti e famiglia editoriale');
        gr.forEach(function (x) { s6.appendChild(el('p', 'a2-note', x.incerto ? 'Appartenenza ambigua al raggruppamento «' + x.entita.nome + '» (' + x.entita.classeLbl.toLowerCase() + ') del grafo classico: ' + x.motivo + '.' : 'Nel grafo classico questo universo è elencato esplicitamente nel raggruppamento «' + x.entita.nome + '» (' + x.entita.classeLbl.toLowerCase() + '). Base: ' + x.motivo + '.')); });
        if (sibl.length) {
          s6.appendChild(el('p', 'a2-note', 'Stessa famiglia editoriale (' + fams.map(function (f) { return FAM[f].nome; }).join(', ') + '). È un’affinità di catalogo, non un collegamento narrativo:'));
          var c6 = el('div', 'a2-chips'); sibl.forEach(function (o) { c6.appendChild(go('uni', o, UNI[o].nome)); }); s6.appendChild(c6);
        }
        modulo('famiglia', 'Famiglia', s6);
      }

      /* --- sezioni senza dati: dichiarate, mai riempite --- */
      var vuoti = [];
      if (!tt.length) vuoti.push('film e serie'); if (!m.have.personaggi) vuoti.push('personaggi'); if (!m.have.eventi) vuoti.push('eventi chiave');
      if (!haArch) vuoti.push('schede d’archivio'); if (!m.have.collegamenti) vuoti.push('collegamenti del Multiverso');
      if (vuoti.length) {
        var s7 = sec('Non documentato'); s7.classList.add('ud-empty');
        s7.appendChild(el('p', 'a2-empty', 'I dati della guida non contengono ' + vuoti.join(', ') + ' per questo universo. Non vengono inventati.')); body.appendChild(s7);
      }

      /* --- indice dei moduli (solo quelli presenti) --- */
      mods.forEach(function (x) {
        var b = btn('ud-ix', x[1], function () {
          var t = $('ud-' + x[0]); if (!t) return; var ih = navSlot.getBoundingClientRect().height || 44;
          body.scrollTop = t.getBoundingClientRect().top - body.getBoundingClientRect().top + body.scrollTop - ih - 6;
        });
        b.setAttribute('data-ix', x[0]); navSlot.appendChild(b);
      });
      if (!mods.length) navSlot.remove();
    }


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

    /* ---------- apertura / stato ---------- */
    var RENDER = { home: renderHome, universi: renderUniversi, uni: function () { renderUni(ST.uid); }, personaggi: renderPersonaggi, cronologie: renderCronologie,
      relazioni: renderRelazioni, mappa: renderMappa, cron: renderCron, catalogo: renderCatalogo, sezione: renderSezione, soon: renderSoon, search: renderSearch };
    function updateBack() {
      var s = W.tvaNavStato ? W.tvaNavStato() : { depth: 0 };
      back.setAttribute('aria-label', s.depth > 0 ? ('Indietro' + (s.last && s.last.lbl ? ' · ' + s.last.lbl : '')) : 'Esci da TVA Archives');
    }
    function draw() { (RENDER[ST.screen] || EXT.screens[ST.screen] || renderHome)(); updateBack(); }
    function show() {
      if (W.marvelChiudiOverlay) W.marvelChiudiOverlay(); tog.checked = true;
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('atlante');
    }
    function setScroll(y) { body.scrollTop = y || 0; }
    function openHome() { ST.screen = 'home'; ST.uid = null; show(); draw(); setScroll(0); }
    function openUniversi() { ST.screen = 'universi'; ST.uid = null; show(); draw(); setScroll(0); }
    // ingresso dall'app Marvel: lo snapshot della schermata di partenza entra nello stack, quindi Indietro / «App Marvel» la ripristinano
    function enter() {
      var sb = $('sidebarToggle'); if (sb) sb.checked = false;
      if (!tog.checked && W.tvaPushNav) W.tvaPushNav('Home');
      ST.screen = 'home'; ST.uid = null; show(); draw(); setScroll(0);
    }
    function exitApp() {
      if (W.tvaTornaApp && W.tvaTornaApp()) return;
      var h = $('appTabHome'); if (h) h.click();
    }
    function openUni(uid, fromRouter) {
      if (!fromRouter && tog.checked && W.tvaPushNav) W.tvaPushNav('Atlante');
      ST.screen = 'uni'; ST.uid = uid; ST.ord = 'guida'; if (!tog.checked) show(); draw(); setScroll(0);
    }
    function openClassicCard(uid) {
      if (W.tvaPushNav) W.tvaPushNav('Atlante');
      W.marvelChiudiOverlay(); var t = $('tvaArchivesToggle'); if (t) t.checked = true; var tab = $('dbtab-uni'); if (tab) tab.checked = true;
      if (W.marvelAggiornaTab) W.marvelAggiornaTab('atlante');
      var card = $(uid); if (card) { var det = card.querySelector('details'); if (det) det.setAttribute('open', ''); W.tvaSettleScroll && W.tvaSettleScroll(card); }
    }
    back.addEventListener('click', function () {
      var s = W.tvaNavStato ? W.tvaNavStato() : { depth: 0 };
      if (s.depth > 0 && W.tvaBack) W.tvaBack(); else exitApp();
    });
    ext.addEventListener('click', exitApp);
    srch.addEventListener('click', function () {
      if (ST.screen === 'home' || ST.screen === 'search') {
        var i = $(ST.screen === 'home' ? 'a2HomeSearch' : 'a2Search'); if (i) { body.scrollTop = 0; i.focus(); }
      } else nav('search');
    });
    root.addEventListener('click', function (ev) {
      var a = ev.target.closest ? ev.target.closest('[data-a2s]') : null;
      if (a) { ev.preventDefault(); openSez(a.getAttribute('data-a2s')); }
    });
    // aggiornamento progressi quando cambia una spunta di visione
    D.addEventListener('change', function (ev) {
      var t = ev.target; if (tog.checked && (ST.screen === 'uni' || ST.screen === 'universi') && t && t.classList && (t.classList.contains('watch-check') || t.classList.contains('anim-watch-check'))) {
        var y = body.scrollTop; setTimeout(function () { draw(); body.scrollTop = y; }, 40);
      }
    }, true);

    /* ---------- accesso ibrido: card cinematografica nella Home Marvel + voce nel menu generale ---------- */
    function mountEntry() {
      var nv = D.querySelector('.home-hub-nav'); if (!nv || $('a2Entry')) return;
      var c = btn('a2-entry', null, enter); c.id = 'a2Entry'; c.setAttribute('aria-label', 'Apri TVA Archives — L’Atlante del Multiverso');
      var bg = el('span', 'a2-entry-bg'); bg.innerHTML = COVER.replace(/a2cg/g, 'a2cgE'); bg.setAttribute('aria-hidden', 'true'); c.appendChild(bg);
      var t = el('span', 'a2-entry-t'); t.appendChild(el('small', '', 'TVA ARCHIVES')); t.appendChild(el('b', '', 'L’Atlante del Multiverso'));
      t.appendChild(el('span', '', 'Universi, personaggi, cronologie e relazioni in un unico archivio.')); t.appendChild(el('em', '', 'Entra nell’Atlante →')); c.appendChild(t);
      nv.parentNode.insertBefore(c, nv);
    }
    D.addEventListener('click', function (ev) {
      var a = ev.target.closest ? ev.target.closest('label.sidebar-archive-link[for="atlas2Toggle"]') : null;
      if (a) { ev.preventDefault(); enter(); }
    }, true);
    mountEntry();
    // la Home del Multiverso puo' essere (ri)costruita: la card viene riagganciata, mai duplicata
    try { new MutationObserver(function () { if (!$('a2Entry')) mountEntry(); }).observe(D.body, { childList: true, subtree: true }); } catch (eMo) {}

    function lab(s) {
      var sc = s && s.screen;
      if (sc === 'uni') return UNI[s.uid] ? (UNI[s.uid].nome || 'Atlante').replace(/^Earth-(\w+) — /, 'E-$1 ') : 'Atlante';
      if (sc === 'universi') return 'Multiverso';
      if (sc === 'mappa') return 'Mappa';
      if (sc === 'cron') return 'Cronologia';
      if (sc === 'personaggi') return 'Personaggi';
      if (sc === 'cronologie') return 'Cronologie';
      if (sc === 'relazioni') return 'Relazioni';
      if (sc === 'catalogo') return 'Archivi';
      if (sc === 'search') return 'Ricerca';
      if ((sc === 'sezione' || sc === 'soon') && SEZ[s.sez]) return SEZ[s.sez].n;
      if (EXT.label) { var xl = EXT.label(s); if (xl) return xl; }
      return 'TVA Archives';
    }
    W.tvaAtlas2 = {
      onOpen: function () { draw(); setScroll(0); },
      enter: enter, exit: exitApp, openUni: openUni, openHome: openHome, openUniversi: openUniversi, label: lab,
      getState: function () { return { screen: ST.screen, uid: ST.uid, sez: ST.sez, q: ST.q, sq: ST.sq, pq: ST.pq, pf: ST.pf, nat: ST.nat, fam: ST.fam, ord: ST.ord, arc: ST.arc, eid: ST.eid, af: ST.af, aq: ST.aq, au: ST.au, mp: mpSnap(), cr: crSnap(), y: body.scrollTop }; },
      setState: function (s) {
        if (!s) return;
        ['screen', 'uid', 'sez', 'q', 'sq', 'pq', 'pf', 'nat', 'fam', 'ord', 'arc', 'eid', 'af', 'aq', 'au'].forEach(function (k) { if (s[k] !== undefined) ST[k] = s[k]; });
        if (s.mp) ST.mp = JSON.parse(JSON.stringify(s.mp));
        if (s.cr) ST.cr = JSON.parse(JSON.stringify(s.cr));
        draw(); requestAnimationFrame(function () { requestAnimationFrame(function () { setScroll(s.y); }); });
      },
      stato: function () { return ST; }, catalogo: function () { return GRP; }
    };
    /* ---------- immagini: registro centralizzato + illustrazioni originali ----------
       L'app non contiene immagini raster. Le foto/still cinematografici NON sono incluse: nessuna fonte con diritti d'uso e' verificabile da qui.
       IMGM e' l'unico punto in cui registrare un'immagine reale: { 'kind:id': { src, w, h, credit, licence, verified:true } } (file locali in assets/img/,
       dimensioni dichiarate, caricamento lazy). Una voce senza licence + verified non viene mai usata. Senza immagine: emblema SVG originale (generato, ~0,7 KB). */
    var IMGM = (W.TVA_IMG_MANIFEST = W.TVA_IMG_MANIFEST || {});
    var PALE = { uni: ['#2b2332', '#101014', '#D2B184'], chr: ['#2a2630', '#101014', '#D2B184'], cos: ['#4a3340', '#14121a', '#D2B184'], spe: ['#3d3226', '#14121a', '#E3C9A0'], mis: ['#4a2a33', '#12101a', '#DB777C'],
      org: ['#3a2328', '#101014', '#DB777C'], art: ['#3b3224', '#101014', '#D2B184'], evt: ['#40282c', '#101014', '#F2E8D8'], luo: ['#2e2a24', '#101014', '#D2B184'], pot: ['#46362a', '#14101a', '#D2B184'] };
    /* Copertine di sezione (WebP locali in assets/images/tva/, illustrazioni originali generate con AI, non immagini ufficiali Marvel). Chiave: 'sez:<chiave>'. */
    [['multiverso', 1280, 720], ['personaggi', 1280, 720], ['cronologie', 1280, 720], ['relazioni', 1280, 720], ['artefatti', 1280, 720], ['entita_cosmiche', 1280, 720], ['arti_mistiche', 1280, 720], ['classifica_poteri', 1280, 720]].forEach(function (p) {
      if (!IMGM['sez:' + p[0]]) IMGM['sez:' + p[0]] = { src: 'assets/images/tva/' + p[0] + '.webp', w: p[1], h: p[2], licence: 'original_ai_generated', verified: true, credit: 'Illustrazione originale generata per TVA Archives (non e\u2019 un\u2019immagine ufficiale Marvel)' };
    });
    var SEZIMG = { multiverso: 'multiverso', universi: 'multiverso', personaggi: 'personaggi', cronologie: 'cronologie', relazioni: 'relazioni', artefatti: 'artefatti', art: 'artefatti', cosmiche: 'entita_cosmiche', cos: 'entita_cosmiche', arti: 'arti_mistiche', mis: 'arti_mistiche', poteri: 'classifica_poteri', pot: 'classifica_poteri', attori: 'personaggi' };
    function sezImg(k) { var n = SEZIMG[k]; var m = n && IMGM['sez:' + n]; return (m && m.src && (m.licence || m.license) && m.verified === true) ? m : null; }
    /* Aggiunge la copertina come sfondo di un contenitore (hero/tile); se il file manca o non carica, resta l'emblema SVG. Il titolo resta testo HTML sopra una sfumatura scura. */
    function imgLayer(host, k) {
      var m = sezImg(k); if (!m) return false;
      var im = new Image(); im.alt = ''; im.className = 'a2-bgimg'; im.width = m.w || 1280; im.height = m.h || 720; im.loading = 'lazy'; im.decoding = 'async';
      im.onerror = function () { im.remove(); host.classList.remove('a2-has-img'); if (host.__fb) { var f = host.__fb; host.__fb = null; f(); } };
      im.src = m.src; host.classList.add('a2-has-img'); host.insertBefore(im, host.firstChild); return true;
    }
    function thumb(k, cls) {
      var m = sezImg(k); if (!m) return null; var d = el('span', 'a2-cov ' + (cls || '')); d.setAttribute('aria-hidden', 'true');
      var im = new Image(); im.alt = ''; im.width = 64; im.height = 64; im.loading = 'lazy'; im.decoding = 'async'; d.setAttribute('data-img', '1'); d.appendChild(im);
      im.onerror = function () { d.remove(); d.__bad = true; }; im.src = m.src; return d;
    }
    var emSeq = 0;
    function hsh(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
    function emblem(kind, id, name, n) {
      var h = hsh(kind + ':' + id), p = PALE[kind] || PALE.uni, c = p[2], gid = 'em' + (emSeq++), g = '', i, k = function (m, s) { return (h >>> (s * 4)) % m; };
      if (kind === 'cos') { for (i = 0; i < 4; i++) g += '<circle cx="32" cy="29" r="' + (6 + i * 6) + '" fill="none" stroke="' + c + '" stroke-opacity="' + (0.9 - i * 0.2).toFixed(2) + '"/>'; g += '<circle cx="' + (26 + k(12, 1)) + '" cy="' + (23 + k(12, 2)) + '" r="2.6" fill="' + c + '"/>'; }
      else if (kind === 'spe') { g += '<path d="M12 42Q32 ' + (4 + k(12, 1)) + ' 52 42" fill="none" stroke="' + c + '" stroke-width="2"/><path d="M19 42Q32 ' + (16 + k(8, 2)) + ' 45 42" fill="none" stroke="' + c + '" stroke-opacity=".6"/><circle cx="32" cy="' + (24 + k(8, 3)) + '" r="4" fill="' + c + '"/>'; }
      else if (kind === 'mis') { var m = 5 + 2 * k(2, 1), pts = []; for (i = 0; i < m; i++) { var a2 = -Math.PI / 2 + ((i * 2) % m) * 2 * Math.PI / m; pts.push((32 + 19 * Math.cos(a2)).toFixed(1) + ',' + (29 + 19 * Math.sin(a2)).toFixed(1)); } g += '<circle cx="32" cy="29" r="21" fill="none" stroke="' + c + '" stroke-opacity=".5"/><polygon points="' + pts.join(' ') + '" fill="none" stroke="' + c + '"/>'; }
      else if (kind === 'org') { g += '<path d="M32 8L50 18V40L32 51 14 40V18Z" fill="none" stroke="' + c + '" stroke-width="1.6"/><path d="M32 17L43 23V36L32 43 21 36V23Z" fill="' + c + '" fill-opacity=".18" stroke="' + c + '" stroke-opacity=".7"/>'; }
      else if (kind === 'art') { g += '<path d="M32 8L50 29 32 50 14 29Z" fill="' + c + '" fill-opacity=".14" stroke="' + c + '" stroke-width="1.6"/><path d="M14 29H50M32 8L24 29 32 50 40 29Z" fill="none" stroke="' + c + '" stroke-opacity=".6"/>'; }
      else if (kind === 'evt') { var r = 8 + k(5, 1); for (i = 0; i < r; i++) { var b = i * 2 * Math.PI / r; g += '<line x1="' + (32 + 8 * Math.cos(b)).toFixed(1) + '" y1="' + (29 + 8 * Math.sin(b)).toFixed(1) + '" x2="' + (32 + (i % 2 ? 17 : 24) * Math.cos(b)).toFixed(1) + '" y2="' + (29 + (i % 2 ? 17 : 24) * Math.sin(b)).toFixed(1) + '" stroke="' + c + '" stroke-opacity=".85"/>'; } g += '<circle cx="32" cy="29" r="5" fill="' + c + '"/>'; }
      else if (kind === 'luo') { g += '<circle cx="' + (40 + k(10, 1)) + '" cy="' + (16 + k(6, 2)) + '" r="6" fill="' + c + '" fill-opacity=".85"/><path d="M4 44Q16 ' + (28 + k(8, 3)) + ' 28 38T52 36 64 42V64H4Z" fill="' + c + '" fill-opacity=".18"/><path d="M4 50Q20 ' + (36 + k(6, 4)) + ' 34 46T64 46" fill="none" stroke="' + c + '" stroke-opacity=".7"/>'; }
      else if (kind === 'pot') { var t = n || 1 + k(7, 1); for (i = 0; i < t; i++) g += '<path d="M16 ' + (44 - i * 6) + 'L32 ' + (36 - i * 6) + ' 48 ' + (44 - i * 6) + '" fill="none" stroke="' + c + '" stroke-width="2" stroke-opacity="' + (0.45 + 0.55 * (i + 1) / t).toFixed(2) + '"/>'; }
      else { var rot = k(6, 1) * 30; g += '<g transform="rotate(' + rot + ' 32 29)"><ellipse cx="32" cy="29" rx="22" ry="9" fill="none" stroke="' + c + '"/><ellipse cx="32" cy="29" rx="22" ry="9" fill="none" stroke="' + c + '" stroke-opacity=".5" transform="rotate(60 32 29)"/><circle cx="32" cy="29" r="3" fill="' + c + '"/></g>'; }
      var L = ((name || '').match(/[A-Za-zÀ-ÿ0-9]/) || ['·'])[0].toUpperCase();
      return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="' + p[0] + '"/><stop offset="1" stop-color="' + p[1] + '"/></linearGradient></defs><rect width="64" height="64" fill="url(#' + gid + ')"/>' + g + '<text x="32" y="60" text-anchor="middle" font-size="11" fill="' + c + '" fill-opacity=".85" font-family="Special Elite,monospace">' + L + '</text></svg>';
    }
    function cover(kind, id, name, cls, n) {
      var d = el('span', 'a2-cov' + (cls ? ' ' + cls : '')); d.setAttribute('aria-hidden', 'true'); d.setAttribute('data-kind', kind);
      var m = IMGM[kind + ':' + id];
      if (m && m.src && m.licence && m.verified === true) {
        var im = new Image(); im.alt = ''; im.width = m.w || 64; im.height = m.h || 64; im.loading = 'lazy'; im.decoding = 'async'; im.onerror = function () { im.remove(); d.removeAttribute('data-img'); d.innerHTML = emblem(kind, id, name, n); }; im.src = m.src; d.setAttribute('data-img', '1'); d.appendChild(im);
      } else d.innerHTML = emblem(kind, id, name, n);
      return d;
    }
    var DECOR = {
      universi: '<path d="M6 74C36 66 52 34 114 8M6 74C40 70 76 58 114 40M6 74C34 76 76 74 114 70" fill="none" stroke="#D2B184" stroke-opacity=".55"/><circle cx="114" cy="8" r="3" fill="#D2B184"/><circle cx="114" cy="40" r="2.5" fill="#DB777C"/><circle cx="114" cy="70" r="2.5" fill="#D2B184" fill-opacity=".6"/>',
      personaggi: '<circle cx="84" cy="26" r="13" fill="none" stroke="#D2B184" stroke-opacity=".6"/><path d="M48 78Q84 34 120 78" fill="none" stroke="#D2B184" stroke-opacity=".5"/><circle cx="84" cy="26" r="22" fill="none" stroke="#DB777C" stroke-opacity=".3"/>',
      cronologie: '<path d="M6 52H116" stroke="#D2B184" stroke-opacity=".55"/><path d="M20 52V38M44 52V30M70 52V42M96 52V26" stroke="#D2B184" stroke-opacity=".5"/><circle cx="44" cy="30" r="3" fill="#DB777C"/><circle cx="96" cy="26" r="3" fill="#D2B184"/><path d="M70 52Q82 64 108 66" fill="none" stroke="#DB777C" stroke-opacity=".5"/>',
      relazioni: '<path d="M30 56L62 24 96 50 74 72ZM62 24L74 72" fill="none" stroke="#D2B184" stroke-opacity=".5"/><circle cx="30" cy="56" r="4" fill="#D2B184"/><circle cx="62" cy="24" r="4" fill="#DB777C"/><circle cx="96" cy="50" r="4" fill="#D2B184"/><circle cx="74" cy="72" r="4" fill="#D2B184" fill-opacity=".7"/>'
    };
    function decor(key) { var d = el('span', 'a2-tile-bg'); d.setAttribute('aria-hidden', 'true'); d.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 80" focusable="false">' + (DECOR[key] || '') + '</svg>'; return d; }
    W.tvaAtlas2.stats = hmStats;
    W.tvaAtlas2.img = { reprobe: function () { HM_MISS = {}; try { Object.keys(W.localStorage).forEach(function (k) { if (k.indexOf('tvaHomeMiss:') === 0) W.localStorage.removeItem(k); }); } catch (e) { } }, stats: hmStats, sezImg: sezImg, manifest: IMGM, emblem: emblem, cover: cover, verified: function () { return Object.keys(IMGM).filter(function (k) { var m = IMGM[k]; return m && m.src && m.licence && m.verified === true; }).length; } };

    EXT.api = { cover: cover, heroImg: imgLayer, $: $, el: el, btn: btn, go: go, art: art, ART: ART, heading: heading, row: row, badge: badge, searchBox: searchBox, nav: nav, setTitle: setTitle, body: body, ST: ST,
      UNI: UNI, IDX: IDX, USCITA: USCITA, personaggiLista: personaggiLista, titoliBase: titoliBase, tipoTitolo: tipoTitolo, anno: anno, prog: prog, info: info, sec: sec, draw: draw, show: show,
      setScroll: setScroll, NOTA_NUM: NOTA_NUM, openMappa: openMappa, crOpen: crOpen, openUni: openUni, openArchive: openArchive, openChrono: openChrono, nat: nat, PTIPO: PTIPO, PSUB: PSUB, tog: tog, cardByTitle: cardByTitle, run: run, fire: fire, leave: leave, SEZ: SEZ, GRP: GRP, updateBack: updateBack };
    W.tvaAtlas2.ext = EXT;
  } catch (eA2) { if (window.console) console.error('Marvel guide - TVA Archives:', eA2); }
})();
