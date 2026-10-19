#!/usr/bin/env python3
"""Consolidamento: esportazioni filtri/ricerca per il router, nota naturaNota (niente 'MCU/Earth-616'), prova estensione tabbar, build."""
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:80])
    s=s.replace(old,new)
# 1) nota natura SSU: la guida usa Earth-199999 per l'MCU; 616 non e' un universo della guida
rep("Il legame con il MCU/Earth-616 non è mai stato chiarito del tutto.","Il legame con l’MCU non è mai stato chiarito del tutto.",2)
rep("Il legame con il MCU/Earth-616 non \\u00e8 mai stato chiarito del tutto.","Il legame con l’MCU non \\u00e8 mai stato chiarito del tutto.")
# 2) esportazioni stato Timeline (ricerca + filtri), solo in memoria
rep("""  window.marvelUniFiltroStato = function() { return { uid: filtroUniversoAttivo, nome: ufNome }; };
""","""  window.marvelUniFiltroStato = function() { return { uid: filtroUniversoAttivo, nome: ufNome }; };
  // ---- Stato della vista Timeline (ricerca + filtri priorita'/studio/tipo/preferiti/weekend) per il tasto "Indietro":
  // lettura/scrittura solo in memoria. NIENTE scritture su localStorage (FILTERS_KEY resta quello salvato dall'utente). ----
  function tvCopia(o) { var r = {}, k; for (k in o) r[k] = o[k]; return r; }
  function tvFiltriUi() {
    Array.prototype.forEach.call(document.querySelectorAll('.filter-btn[data-tag]'), function(b) { b.classList.toggle('off', !activeFilters[b.getAttribute('data-tag')]); });
    Array.prototype.forEach.call(document.querySelectorAll('.filter-btn[data-studio]'), function(b) { b.classList.toggle('off', !activeStudios[b.getAttribute('data-studio')]); });
    Array.prototype.forEach.call(document.querySelectorAll('.filter-btn[data-type]'), function(b) { b.classList.toggle('off', !activeTypes[b.getAttribute('data-type')]); });
    var fb = document.getElementById('favFilterBtn'); if (fb) fb.classList.toggle('off', !favOnly);
    var wb = document.getElementById('weekendFilterBtn'); if (wb) wb.classList.toggle('off', !weekendOnly);
  }
  function tvRicerca(v) {
    if (!searchBox || searchBox.value === v) return;
    searchBox.value = v;
    try { searchBox.dispatchEvent(new Event('input', { bubbles: true })); } catch(eEv) {}
  }
  window.marvelFiltriStato = function() {
    return { q: searchBox ? searchBox.value : '', tag: tvCopia(activeFilters), studio: tvCopia(activeStudios), type: tvCopia(activeTypes), fav: !!favOnly, wk: !!weekendOnly };
  };
  window.marvelFiltriImposta = function(st) {
    if (!st) return;
    try {
      var k;
      if (st.tag) for (k in st.tag) activeFilters[k] = st.tag[k];
      if (st.studio) for (k in st.studio) activeStudios[k] = st.studio[k];
      if (st.type) for (k in st.type) activeTypes[k] = st.type[k];
      favOnly = !!st.fav; weekendOnly = !!st.wk;
      tvFiltriUi();
      if (typeof st.q === 'string') tvRicerca(st.q);
      refreshVisibility();
    } catch(eFiltImp) { if (window.console) console.error('Marvel guide - imposta filtri:', eFiltImp); }
  };
  // Azzera SOLO i filtri che nascondono questa scheda (usato quando un collegamento porta a un titolo nascosto).
  window.marvelFiltriSblocca = function(li) {
    var cleared = [];
    try {
      var tag = li.getAttribute('data-tag'), studio = li.getAttribute('data-studio'), ity = li.getAttribute('data-type'), id = li.getAttribute('data-item');
      if (tag && activeFilters[tag] === false) { activeFilters[tag] = true; cleared.push('priorita'); }
      if (studio && activeStudios[studio] === false) { activeStudios[studio] = true; cleared.push('studio'); }
      if (ity && activeTypes[ity] === false) { activeTypes[ity] = true; cleared.push('tipo'); }
      if (favOnly && id && !loadFavs()[id]) { favOnly = false; cleared.push('preferiti'); }
      if (weekendOnly && li.getAttribute('data-weekend') !== '1') { weekendOnly = false; cleared.push('weekend'); }
      var q = searchBox ? searchBox.value.trim().toLowerCase() : '';
      if (q && (li.getAttribute('data-search') || '').indexOf(q) === -1) { tvRicerca(''); cleared.push('ricerca'); }
      if (cleared.length) { tvFiltriUi(); refreshVisibility(); }
    } catch(eFiltSbl) { if (window.console) console.error('Marvel guide - sblocca filtri:', eFiltSbl); }
    return cleared;
  };
""")
# 3) prova estensione tabbar (A/B sul dispositivo) + misure
rep("""/* Tastiera aperta (campo di testo a fuoco)""","""/* Solo diagnostica (pannello debugLayout, tasto ESTENS.SOTTO): disattiva il prolungamento per verificare sul dispositivo se serve ancora. */
html.tva-no-ext .app-tabbar::after { display: none; }
/* Tastiera aperta (campo di testo a fuoco)""")
rep("""    zb.textContent='ZOOMFIX '+((window.__tvaTabbar&&window.__tvaTabbar.zoomFix)?'ON':'OFF');
""","""    zb.textContent='ZOOMFIX '+((window.__tvaTabbar&&window.__tvaTabbar.zoomFix)?'ON':'OFF');
    var eb=btn('ESTENS.SOTTO',function(){ root.classList.toggle('tva-no-ext'); eb.textContent='ESTENS.SOTTO '+(root.classList.contains('tva-no-ext')?'OFF':'ON'); aggiorna(); });
    eb.textContent='ESTENS.SOTTO '+(root.classList.contains('tva-no-ext')?'OFF':'ON');
""")
rep("""      L.push('classi: '+b.className+' | html: '+root.className);""","""      L.push('classi: '+b.className+' | html: '+root.className);
      var ca=getComputedStyle(b,'::after');
      L.push('estensione ::after: '+(ca.display==='none'?'DISATTIVATA (prova)':'attiva')+' | h '+ca.height+' | top '+ca.top+' | bg '+ca.backgroundColor+' | overflow documento (scrollHeight-clientHeight): '+(root.scrollHeight-root.clientHeight));""")
# 4) build
rep('<meta name="tva-build" content="20261017-1800-net-a2">','<meta name="tva-build" content="20261017-1600-consolidation1">')
open(P,'w',encoding='utf-8').write(s)
print('patch ok')
