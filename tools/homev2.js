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

