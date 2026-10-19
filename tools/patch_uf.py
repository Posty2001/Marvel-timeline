import re
p='/home/claude/work/index.html'
s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old)); s=s.replace(old,new)

# ---------- 1) CSS: banner compatto + regole del filtro ----------
a=s.index(".mv-universo-banner {\n  position: sticky;")
b=s.index(".mv-map-old-link {")
css='''/* ---- Filtro universo (Esplora Multiverso -> Timeline) ----
   Banner compatto su una riga: lascia libero il menu circolare fisso in alto a sinistra (2.6rem, a 1rem dal bordo)
   e allinea il proprio contenuto al suo centro, cosi' non si sovrappongono. */
.mv-universo-banner {
  position: sticky; top: 0; z-index: 90; display: flex; align-items: center; justify-content: space-between; gap: 0.6rem;
  background: var(--marvel-red); color: #fff; font-family: 'IBM Plex Mono', monospace; box-sizing: border-box;
  padding: calc(var(--sat) + 0.75rem) calc(var(--sar) + 0.7rem) 0.5rem calc(var(--sal) + 4.1rem);
  min-height: calc(var(--sat) + 3.65rem); box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
@media (min-width: 1180px) { .mv-universo-banner { padding-left: 1.2rem; min-height: 0; padding-top: calc(var(--sat) + 0.6rem); } }
.mv-universo-banner[hidden] { display: none; }
.mv-ub-txt { min-width: 0; flex: 1 1 auto; text-align: left; }
.mv-ub-name { font-size: 0.8rem; line-height: 1.25; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mv-ub-name b { color: #ffe9a8; }
.mv-ub-meta { font-size: 0.64rem; line-height: 1.3; opacity: 0.92; margin-top: 0.1rem; overflow-wrap: anywhere; }
.mv-universo-banner button {
  flex: 0 0 auto; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.5); color: #fff;
  font-family: inherit; font-size: 0.68rem; padding: 0 0.7rem; border-radius: 4px; cursor: pointer;
  min-height: 2.75rem; white-space: nowrap; touch-action: manipulation;
}
.mv-universo-banner button:hover { background: rgba(255,255,255,0.28); }
.mv-universo-vuoto {
  margin: 1rem; padding: 1.1rem 1rem; border: 1px dashed rgba(200,39,42,0.6); border-radius: 6px; text-align: center;
  background: rgba(200,39,42,0.06); color: var(--ink); font-family: 'Spectral', Georgia, serif; font-size: 0.95rem; line-height: 1.5;
}
.mv-universo-vuoto[hidden] { display: none; }
.mv-universo-vuoto b { color: var(--marvel-red); }
.mv-universo-vuoto .mv-uv-small { display: block; margin-top: 0.5rem; font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; opacity: 0.75; }
.mv-universo-vuoto.mv-uv-nota { border-style: solid; border-color: rgba(200,39,42,0.35); font-size: 0.85rem; padding: 0.7rem 0.9rem; }
/* Durante il filtro: restano solo banner, ricerca/filtri e i titoli dell'universo. Tutto il resto (copertina, bollettino,
   indice, legenda, note editoriali, dashboard, database, grafico, piede) non appartiene a nessun universo e si nasconde. */
html.uf-on #cover, html.uf-on #bollettinoBox, html.uf-on #indice, html.uf-on .legend-wrap,
html.uf-on #dashboard, html.uf-on #modalita-confronto, html.uf-on #database, html.uf-on #gtimeline,
html.uf-on footer.closing, html.uf-on .foot-mark,
html.uf-on .controlbar .progress-row, html.uf-on #resetBtn,
html.uf-on .part-head .part-sub, html.uf-on .dopo-sw > .part-sub,
html.uf-on .part > .note-clip, html.uf-on .part > .innesto, html.uf-on .dopo-sw > .note-clip { display: none !important; }
[data-uf-hide] { display: none !important; }
/* etichetta sui titoli crossover (ruolo "crossover" nei dati dell'Atlante) */
li.card-wrap[data-uf-rel]::before {
  content: attr(data-uf-rel-txt); display: block; margin: 0 0 0.25rem; padding: 0.3rem 0.6rem; border-radius: 4px;
  font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; line-height: 1.35; color: #5a3a00; background: #ffe9a8;
}
'''
s=s[:a]+css+s[b:]

# ---------- 2) refreshVisibility: filtro universo ----------
rep("""        var uniAttr = li.getAttribute('data-uni') || '';
        var passUniverso = !filtroUniversoAttivo || !uniAttr || (' ' + uniAttr + ' ').indexOf(' ' + filtroUniversoAttivo + ' ') !== -1;""",
"""        var uniAttr = li.getAttribute('data-uni') || '';
        // Filtro universo: vale solo per le schede della Timeline. Una scheda SENZA data-uni non e' associata a nessun
        // universo nei dati e quindi NON passa (prima passava sempre). Le schede dell'Atlante non vengono toccate.
        var passUniverso = true;
        if (filtroUniversoAttivo && !ufInAtlante(li)) {
          passUniverso = uniAttr !== '' && (' ' + uniAttr + ' ').indexOf(' ' + filtroUniversoAttivo + ' ') !== -1;
        }""")
rep("""          if (letterGroup) letterGroup.setAttribute('open', '');
        }
      }
    } catch(e) {
      if (window.console) console.error('Marvel guide - refreshVisibility:', e);
    }
  }
""","""          if (letterGroup) letterGroup.setAttribute('open', '');
        }
      }
      ufApplicaStruttura();
    } catch(e) {
      if (window.console) console.error('Marvel guide - refreshVisibility:', e);
    }
  }
""")

# ---------- 3) mvEsploraUniverso riscritta + helper ----------
a=s.index("  // ---- \"Esplora questo universo\" dalla Mappa Multiverso")
b=s.index("  window.marvelEsploraUniverso = mvEsploraUniverso;")
js=r'''  // ---- "Esplora questo universo" dalla Mappa Multiverso: filtra la Timeline reale mostrando SOLO i titoli associati a
  // quell'universo nei dati (data-uni == mvMapData.titoliIds == atlasData.opere[].universi), riusando le schede esistenti
  // (checkbox, note, rating invariati). Intestazioni di sezione, note e blocchi editoriali senza titoli visibili vengono
  // nascosti; i titoli con ruolo "crossover" (atlasData) restano visibili ma etichettati; se non c'e' nulla, stato vuoto.
  // Nessuna scrittura su localStorage: e' solo una vista. ----
  var ufNome = '';
  var ufCacheRuoli = null, ufCacheUni = null;
  function ufInAtlante(li) {
    if (li.__ufDb === undefined) li.__ufDb = !!(li.closest && li.closest('.tva-archives-overlay'));
    return li.__ufDb;
  }
  function ufRuoli() {
    if (ufCacheRuoli) return ufCacheRuoli;
    ufCacheRuoli = {};
    try {
      var a = JSON.parse(document.getElementById('atlasData').textContent);
      (a.opere || []).forEach(function(o) { ufCacheRuoli[o.id] = o.ruolo || ''; });
    } catch(eUfR) {}
    return ufCacheRuoli;
  }
  function ufUniversi() {
    if (ufCacheUni) return ufCacheUni;
    ufCacheUni = {};
    try { ufCacheUni = JSON.parse(document.getElementById('mvMapData').textContent).universi || {}; } catch(eUfU) {}
    return ufCacheUni;
  }
  function ufEAssociata(li, uid) {
    var a = li.getAttribute('data-uni') || '';
    return a !== '' && (' ' + a + ' ').indexOf(' ' + uid + ' ') !== -1;
  }
  function ufEcrossover(li) {
    var r = ufRuoli()[li.getAttribute('data-item')];
    if (r) return r === 'crossover';
    return (li.getAttribute('data-uni') || '').split(/\s+/).filter(Boolean).length > 1;
  }
  function ufConta(uid) {
    var c = { n: 0, k: 0, v: 0, m: 0 };
    for (var i = 0; i < allWraps.length; i++) {
      var li = allWraps[i];
      if (ufInAtlante(li) || !ufEAssociata(li, uid)) continue;
      c.n++;
      var chk = li.querySelector('.watch-check');
      if (chk && chk.checked) c.v++;
      if (ufEcrossover(li)) c.k++;
      if (li.style.display !== 'none') c.m++;
    }
    return c;
  }
  function ufAssicuraBanner() {
    var banner = document.getElementById('mvUniversoBanner');
    if (!banner) {
      banner = document.createElement('div');
      banner.id = 'mvUniversoBanner';
      banner.className = 'mv-universo-banner';
      banner.setAttribute('role', 'status');
      banner.innerHTML = '<div class="mv-ub-txt"><div class="mv-ub-name">🌌 Stai vedendo solo: <b></b></div><div class="mv-ub-meta"></div></div>' +
        '<button type="button" id="mvUniversoBannerChiudi" aria-label="Rimuovi il filtro e torna a tutti i titoli">✕ Rimuovi filtro</button>';
      var parte1El = document.getElementById('parte1');
      if (parte1El && parte1El.parentNode) parte1El.parentNode.insertBefore(banner, parte1El);
      banner.querySelector('#mvUniversoBannerChiudi').addEventListener('click', function() { mvUniFiltroReset(); });
      var vuoto = document.createElement('div');
      vuoto.id = 'mvUniversoVuoto';
      vuoto.className = 'mv-universo-vuoto';
      vuoto.hidden = true;
      banner.parentNode.insertBefore(vuoto, banner.nextSibling);
    }
    return banner;
  }
  function ufAggiornaBanner() {
    var banner = document.getElementById('mvUniversoBanner');
    var vuoto = document.getElementById('mvUniversoVuoto');
    if (!banner) return;
    if (!filtroUniversoAttivo) { banner.hidden = true; if (vuoto) vuoto.hidden = true; return; }
    var u = ufUniversi()[filtroUniversoAttivo] || {};
    var c = ufConta(filtroUniversoAttivo);
    banner.hidden = false;
    banner.querySelector('.mv-ub-name b').textContent = ufNome || u.nome || filtroUniversoAttivo;
    var meta = [];
    meta.push(c.n + (c.n === 1 ? ' titolo' : ' titoli'));
    meta.push(c.v + (c.v === 1 ? ' visto' : ' visti'));
    if (c.k) meta.push(c.k + ' crossover');
    if (c.n && c.m !== c.n) meta.push(c.m + ' mostrati con la ricerca/i filtri attuali');
    if (u.natura) meta.push(u.natura);
    banner.querySelector('.mv-ub-meta').textContent = meta.join(' · ');
    if (!vuoto) return;
    var nome = (ufNome || u.nome || filtroUniversoAttivo);
    vuoto.classList.remove('mv-uv-nota');
    if (c.n === 0) {
      vuoto.innerHTML = '<b></b> non ha titoli associati direttamente nella Timeline.<span class="mv-uv-small"></span>';
      vuoto.querySelector('b').textContent = nome;
      vuoto.querySelector('.mv-uv-small').textContent = (u.naturaNota ? u.naturaNota + ' ' : '') +
        'I titoli senza un universo verificato nei dati (capitolo 0, Parte 4, serie animate) non vengono attribuiti per ipotesi. Puoi consultare questo universo nella Mappa Multiverso e nell’Atlante.';
      vuoto.hidden = false;
    } else if (c.m === 0) {
      vuoto.innerHTML = 'Nessun titolo di <b></b> corrisponde alla ricerca o ai filtri attuali.<span class="mv-uv-small"></span>';
      vuoto.querySelector('b').textContent = nome;
      vuoto.querySelector('.mv-uv-small').textContent = c.n + (c.n === 1 ? ' titolo associato' : ' titoli associati') + ': svuota la ricerca o riattiva i filtri per vederli.';
      vuoto.hidden = false;
    } else if (c.k === c.n) {
      vuoto.classList.add('mv-uv-nota');
      vuoto.textContent = 'Nessun titolo appartiene esclusivamente a questo universo: qui sotto i crossover / titoli multi-universo che lo coinvolgono (ruolo “crossover” nei dati).';
      vuoto.hidden = false;
    } else {
      vuoto.hidden = true;
    }
  }
  function ufPulisciBadge() {
    for (var i = 0; i < allWraps.length; i++) {
      var li = allWraps[i];
      if (li.hasAttribute('data-uf-rel')) { li.removeAttribute('data-uf-rel'); li.removeAttribute('data-uf-rel-txt'); }
    }
  }
  function ufApplicaStruttura() {
    try {
      var root = document.documentElement;
      var marcati = document.querySelectorAll('[data-uf-hide]');
      for (var m = 0; m < marcati.length; m++) marcati[m].removeAttribute('data-uf-hide');
      if (!filtroUniversoAttivo) {
        root.classList.remove('uf-on');
        ufPulisciBadge();
        ufAggiornaBanner();
        return;
      }
      root.classList.add('uf-on');
      var uni = ufUniversi();
      for (var i = 0; i < allWraps.length; i++) {
        var li = allWraps[i];
        if (ufInAtlante(li)) continue;
        if (ufEAssociata(li, filtroUniversoAttivo) && ufEcrossover(li)) {
          var nomi = (li.getAttribute('data-uni') || '').split(/\s+/).filter(Boolean).map(function(id) { return (uni[id] && uni[id].nome) || id; });
          li.setAttribute('data-uf-rel', 'crossover');
          li.setAttribute('data-uf-rel-txt', '↗ CROSSOVER · coinvolge più universi: ' + nomi.join(' + '));
        } else if (li.hasAttribute('data-uf-rel')) {
          li.removeAttribute('data-uf-rel'); li.removeAttribute('data-uf-rel-txt');
        }
      }
      var secs = document.querySelectorAll('section.part, section.dopo-sw, #serieanimate');
      for (var s1 = 0; s1 < secs.length; s1++) {
        var sec = secs[s1];
        if (sec.closest && sec.closest('.tva-archives-overlay')) continue;
        var cards = sec.querySelectorAll('.card-wrap'), vis = 0;
        for (var k = 0; k < cards.length; k++) if (cards[k].style.display !== 'none') vis++;
        if (!vis) { sec.setAttribute('data-uf-hide', '1'); continue; }
        var pend = null, kids = sec.children;
        for (var j = 0; j < kids.length; j++) {
          var el = kids[j];
          if (el.matches && el.matches('h3.sec-h')) { pend = el; }
          else if (el.matches && el.matches('ul.items')) {
            var cs = el.querySelectorAll('.card-wrap'), v2 = 0;
            for (var q2 = 0; q2 < cs.length; q2++) if (cs[q2].style.display !== 'none') v2++;
            if (!v2) { el.setAttribute('data-uf-hide', '1'); if (pend) pend.setAttribute('data-uf-hide', '1'); }
            pend = null;
          }
        }
      }
      ufAggiornaBanner();
    } catch(eUfStr) {
      if (window.console) console.error('Marvel guide - filtro universo:', eUfStr);
    }
  }
  function mvUniFiltroReset() {
    if (!filtroUniversoAttivo) return;
    filtroUniversoAttivo = null;
    ufNome = '';
    refreshVisibility();
  }
  window.marvelUniFiltroReset = mvUniFiltroReset;
  function mvEsploraUniverso(uid, nomeUniverso) {
    try {
      filtroUniversoAttivo = uid;
      ufNome = nomeUniverso || '';
      chiudiTuttiGliOverlay();
      var exitCb = document.getElementById('homeHubExited');
      if (exitCb) exitCb.checked = true;
      var hub = document.getElementById('homeHub');
      if (hub) hub.style.display = 'none';
      var banner = ufAssicuraBanner();
      refreshVisibility();
      if (banner && banner.scrollIntoView) banner.scrollIntoView({ behavior: 'auto', block: 'start' });
      if (typeof aggiornaTabAttiva === 'function') aggiornaTabAttiva('timeline');
    } catch(eMvEsplora) {
      if (window.console) console.error('Marvel guide - esplora universo:', eMvEsplora);
    }
  }
'''
s=s[:a]+js+s[b:]

# ---------- 4) bottone Esplora anche per universi senza titoli (porta allo stato vuoto) ----------
rep("""    var esploraHtml = '';
    if (u.titoliIds && u.titoliIds.length) {
      esploraHtml = '<button type="button" class="mv-map-esplora-btn" id="mvMapEsploraBtn" data-uni="' + uid + '">' +
        '\\uD83E\\uDDED Esplora questo universo</button>';
    }""","""    var esploraHtml = '';
    var nTitoliUni = (u.titoliIds && u.titoliIds.length) || 0;
    esploraHtml = '<button type="button" class="mv-map-esplora-btn" id="mvMapEsploraBtn" data-uni="' + uid + '">' +
      '\\uD83E\\uDDED Esplora questo universo' + (nTitoliUni ? '' : ' (nessun titolo associato)') + '</button>';""")

# ---------- 5) ganci: uscita dalla vista filtrata ----------
rep("""      appTabHome.addEventListener('click', function() {
        chiudiTuttiGliOverlay();""","""      appTabHome.addEventListener('click', function() {
        try { mvUniFiltroReset(); } catch(eUfH) {}
        chiudiTuttiGliOverlay();""")
rep("""      appTabMissioni.addEventListener('click', function() {
        chiudiTuttiGliOverlay();""","""      appTabMissioni.addEventListener('click', function() {
        try { mvUniFiltroReset(); } catch(eUfM) {}
        chiudiTuttiGliOverlay();""")
rep("""        link.addEventListener('click', function() {
          chiudiTuttiGliOverlay();
          var exitCb = document.getElementById('homeHubExited');""","""        link.addEventListener('click', function() {
          try { mvUniFiltroReset(); } catch(eUfS) {}
          chiudiTuttiGliOverlay();
          var exitCb = document.getElementById('homeHubExited');""")
# contatori del banner aggiornati quando si spunta/toglie un titolo
rep("""  function updateProgress() {
    try {
      var checked = document.querySelectorAll('.watch-check:checked').length;""","""  function updateProgress() {
    try { if (filtroUniversoAttivo) ufAggiornaBanner(); } catch(eUfUp) {}
    try {
      var checked = document.querySelectorAll('.watch-check:checked').length;""")
open(p,'w',encoding='utf-8').write(s); print('ok')
