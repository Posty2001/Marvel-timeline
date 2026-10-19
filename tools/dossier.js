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

