#!/usr/bin/env python3
"""Blocco M3.4 (idempotente, dopo patch_m33): Home «TVA Hybrid» compatta + correzioni alla fonte (voto medio al caricamento, descrizioni missioni)."""
import re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,marker):
    global s
    if marker in s: return
    assert s.count(old)==1,(old[:60],s.count(old)); s=s.replace(old,new)

# ---- A) correzioni alla fonte ----
# A1: updateMissioni() girava una sola volta prima che marvelGetAltTimelineData esistesse -> usciva subito e lasciava i segnaposto «—» nelle missioni tematica/saga
rep("window.marvelGetAltTimelineData = getAltTimelineData;",
    "window.marvelGetAltTimelineData = getAltTimelineData;\n    /* M34: la prima updateMissioni() era uscita prima che i dati esistessero (testi rimasti «—»): ora si ripete a dati pronti, in SOLA LETTURA (nessuna ricompensa, XP, snapshot o celebrazione al caricamento) */\n    try { if (typeof window.marvelUpdateMissioni === 'function') { window.marvelMissioniSoloLettura = true; try { window.marvelUpdateMissioni(); } finally { window.marvelMissioniSoloLettura = false; } } } catch (eM34m) {}",
    'eM34m')
rep("  function provaRicompensaMissione(chiave, xpValore) {",
    "  function provaRicompensaMissione(chiave, xpValore) {\n    if (window.marvelMissioniSoloLettura) return false;   /* M34: render al caricamento senza effetti collaterali */",
    'marvelMissioniSoloLettura) return false')
rep("        localStorage.setItem(MISSIONE_SNAPSHOT_KEY, JSON.stringify(dati));",
    "        if (!window.marvelMissioniSoloLettura) localStorage.setItem(MISSIONE_SNAPSHOT_KEY, JSON.stringify(dati));",
    'marvelMissioniSoloLettura) localStorage.setItem')
rep("        if (indiceStagioneAttuale > ultimaFesteggiata) {",
    "        if (indiceStagioneAttuale > ultimaFesteggiata && !window.marvelMissioniSoloLettura) {",
    'ultimaFesteggiata && !window')
# A2: la prima updateHomeHubSummary() girava prima che RATINGS_KEY fosse inizializzata (voto medio sempre vuoto al caricamento)
rep("var RATINGS_KEY = 'marvel-ultimate-timeline-ratings';",
    "var RATINGS_KEY = 'marvel-ultimate-timeline-ratings';\n  /* M34: da qui RATINGS_KEY esiste: il voto medio della Home si ricalcola dai voti salvati anche al caricamento/dopo un import profilo */\n  try { updateHomeHubSummary(); } catch (eM34r) {}",
    'eM34r')
rep("if (pctEl) pctEl.textContent = stats.pct;",
    "if (pctEl) pctEl.textContent = stats.pct;\n      var doneEl = document.getElementById('hhsDone');   /* M34 */\n      if (doneEl) doneEl.textContent = stats.checked + '/' + stats.totalChecks;\n      window.marvelHomeCount = stats.checked;",
    "getElementById('hhsDone')")
rep("'Ancora nessun voto'","'Nessun voto'","\\u2b50' : 'Nessun voto'")
rep("        var next = trovaProssimoPerPriorita();\n        if (next) {\n          nextVal.textContent = next.title;",
    "        var next = trovaProssimoPerPriorita();\n        window.marvelHomeNext = next || null;   /* M34 */\n        if (next) {\n          nextVal.textContent = next.title;",
    'marvelHomeNext = next')
rep("          nextVal.textContent = 'Tutto visto!';\n          if (nextRow) nextRow.onclick = null;\n        }\n      }",
    "          nextVal.textContent = 'Tutto visto!';\n          if (nextRow) nextRow.onclick = null;\n        }\n        try { document.dispatchEvent(new CustomEvent('tva:homenext')); } catch (eM34n) {}\n      }",
    'eM34n')
rep("  // Valuta UNA condizione badge dati i dati necessari",
    "  window.marvelUpdateHomeHub = updateHomeHubSummary;\n\n  // Valuta UNA condizione badge dati i dati necessari",'marvelUpdateHomeHub')
# A3: la vecchia scheda missioni della Home (RS) e' sostituita dalla missione in evidenza M34
rep("var inner = q('.home-hub-inner', hub); if (!inner) return;",
    "var inner = null; if (!inner) return;   /* M34: scheda missioni Home gestita da #m34Mis */",'gestita da #m34Mis')

# ---- B) markup Home ----
HTML='''<div class="home-hub-inner">
    <div class="home-hub-greeting">
      <p class="home-hub-hello" id="homeHubHello">Bentornato, Variante</p>
      <p class="home-hub-pct-line">Hai completato il <b id="hhgPct">0</b>% del Multiverso.</p>
    </div>
    <div class="home-hub-summary" id="homeHubSummary">
      <button type="button" class="m34-next" id="hhsNextRow" aria-label="Prossimo titolo">
        <span class="m34-poster" id="m34Poster" aria-hidden="true"><span class="m34-pfb" id="m34Pfb">&#127916;</span></span>
        <span class="m34-nbody">
          <span class="m34-eyebrow">Prossimo titolo</span>
          <span class="m34-ntitle" id="hhsNextValue">&mdash;</span>
          <span class="m34-nmeta" id="m34NextMeta"></span>
          <span class="m34-cta" id="m34NextCta">Inizia &#8594;</span>
        </span>
      </button>
      <div class="m34-stats" role="group" aria-label="Statistiche">
        <div class="m34-stat"><b id="hhsDone">&mdash;</b><span>Titoli completati</span></div>
        <div class="m34-stat"><b id="hhsHours">&mdash;</b><span>Ore viste</span></div>
        <div class="m34-stat"><b id="hhsRating">&mdash;</b><span>Voto medio</span></div>
      </div>
    </div>
    <nav class="home-hub-nav" aria-label="Accessi rapidi">
      <button type="button" class="m34-acc" id="m34Atl"><span class="m34-acc-ic" aria-hidden="true">&#127756;</span><span>Atlante</span></button>
      <button type="button" class="m34-acc" id="m34Tes"><span class="m34-acc-ic" aria-hidden="true">&#127894;</span><span>Tessera TVA</span></button>
    </nav>
    <section class="m34-mis" id="m34Mis" aria-label="Missione attiva">
      <span class="m34-eyebrow">Missione attiva</span>
      <span class="m34-mname" id="m34MName">&mdash;</span>
      <span class="m34-mbar" aria-hidden="true"><i id="m34MFill"></i></span>
      <span class="m34-mrow"><span class="m34-mfrac" id="m34MFrac"></span><button type="button" class="m34-mgo" id="m34MGo">Centrale TVA &#8594;</button></span>
    </section>
  </div>
</div>

'''
if 'id="m34Mis"' not in s:
    a=s.index('<div class="home-hub-inner">'); b=s.index('<div class="cover" id="cover">')
    s=s[:a]+HTML+s[b:]

# ---- C) CSS ----
CSS='''/* M34-CSS */
html:not(#rs) #homeHub { background: radial-gradient(120% 55% at 50% -8%, rgba(122,36,51,.42), transparent 62%), radial-gradient(80% 40% at 100% 40%, rgba(210,177,132,.07), transparent 60%), #0b0909; align-items: flex-start; padding-left: calc(1rem + var(--sal, 0px)); padding-right: calc(1rem + var(--sar, 0px)); }
html:not(#rs) #homeHub .home-hub-inner { display: flex; flex-direction: column; gap: .7rem; max-width: 430px; padding-top: 3.1rem; text-align: left; }
html:not(#rs) #homeHub .home-hub-greeting { order: 1; margin: 0; }
html:not(#rs) #homeHub .home-hub-hello { font-size: clamp(1.35rem, 6vw, 1.7rem); line-height: 1.15; margin: 0 0 .25rem; text-transform: none; letter-spacing: 0; }
html:not(#rs) #homeHub .home-hub-pct-line { font-size: .8rem; margin: 0; }
html:not(#rs) #homeHub .rs-prog { height: 6px; margin-top: .5rem; background: rgba(242,232,216,.1); }
html:not(#rs) #homeHub .rs-prog > i { background: linear-gradient(90deg, #7a2433, #D2B184); }
html:not(#rs) #homeHub .home-hub-summary { order: 2; display: flex; flex-direction: column; gap: .7rem; margin: 0; }
html:not(#rs) #homeHub .m34-next { display: flex; align-items: stretch; gap: .85rem; width: 100%; box-sizing: border-box; text-align: left; cursor: pointer; padding: .75rem; border-radius: 16px; border: 1px solid rgba(210,177,132,.5); background: linear-gradient(135deg, rgba(122,36,51,.55), rgba(20,12,14,.85) 70%); color: #f2e8d8; box-shadow: 0 12px 28px rgba(0,0,0,.45); font: inherit; min-height: 0; }
html:not(#rs) #homeHub .m34-next:active { transform: translateY(1px); }
html:not(#rs) #homeHub .m34-poster { position: relative; flex: 0 0 auto; width: 4.4rem; aspect-ratio: 2 / 3; border-radius: 8px; overflow: hidden; background: linear-gradient(160deg, #2a1218, #120b0d); border: 1px solid rgba(210,177,132,.35); display: grid; place-items: center; }
html:not(#rs) #homeHub .m34-poster img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; display: block; }
html:not(#rs) #homeHub .m34-pfb { font-size: 1.8rem; line-height: 1; }
html:not(#rs) #homeHub .m34-poster.m34-has .m34-pfb { display: none; }
html:not(#rs) #homeHub .m34-nbody { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; justify-content: center; gap: .2rem; }
html:not(#rs) #homeHub .m34-eyebrow { display: block; font-family: 'IBM Plex Mono', monospace; font-size: .6rem; letter-spacing: .14em; text-transform: uppercase; color: #D2B184; font-weight: 700; }
html:not(#rs) #homeHub .m34-ntitle { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: 1.2rem; line-height: 1.15; font-weight: 600; color: #f2e8d8; overflow-wrap: anywhere; }
html:not(#rs) #homeHub .m34-nmeta { display: block; font-size: .74rem; color: rgba(242,232,216,.7); min-height: 0; }
html:not(#rs) #homeHub .m34-nmeta:empty { display: none; }
html:not(#rs) #homeHub .m34-cta { align-self: flex-start; margin-top: .3rem; display: inline-flex; align-items: center; min-height: 2.25rem; padding: 0 1rem; border-radius: 999px; background: #D2B184; color: #1a0f12; font-weight: 700; font-size: .8rem; }
html:not(#rs) #homeHub .m34-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); border: 1px solid rgba(242,232,216,.12); border-radius: 14px; background: rgba(20,14,16,.7); overflow: hidden; }
html:not(#rs) #homeHub .m34-stat { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .15rem; padding: .65rem .3rem; min-height: 4rem; text-align: center; }
html:not(#rs) #homeHub .m34-stat + .m34-stat { border-left: 1px solid rgba(242,232,216,.12); }
html:not(#rs) #homeHub .m34-stat b { font-size: 1.05rem; line-height: 1.15; color: #f2e8d8; font-weight: 700; overflow-wrap: anywhere; }
html:not(#rs) #homeHub .m34-stat b * { font-size: inherit; }
html:not(#rs) #homeHub .m34-stat b .rs-i { width: 1em; height: 1em; vertical-align: -.12em; color: #D2B184; }
html:not(#rs) #homeHub .m34-stat > span { font-size: .56rem; letter-spacing: .08em; text-transform: uppercase; color: rgba(242,232,216,.55); line-height: 1.2; }
html:not(#rs) #homeHub .home-hub-nav { order: 3; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .6rem; margin: 0; }
html:not(#rs) #homeHub .m34-acc { display: flex; align-items: center; justify-content: center; gap: .5rem; min-height: 2.75rem; padding: .4rem .6rem; border-radius: 12px; border: 1px solid rgba(210,177,132,.4); background: rgba(20,14,16,.7); color: #f2e8d8; font: inherit; font-weight: 600; font-size: .85rem; cursor: pointer; width: auto; }
html:not(#rs) #homeHub .m34-acc:active { transform: translateY(1px); }
html:not(#rs) #homeHub .a2-entry, html:not(#rs) #homeHub #rsHomeMis { display: none !important; }
html:not(#rs) #homeHub .m34-mis { order: 4; display: flex; flex-direction: column; gap: .35rem; padding: .75rem .85rem; border-radius: 14px; border: 1px solid rgba(122,36,51,.7); background: rgba(122,36,51,.18); }
html:not(#rs) #homeHub .m34-mname { font-size: .95rem; font-weight: 600; line-height: 1.25; color: #f2e8d8; overflow-wrap: anywhere; }
html:not(#rs) #homeHub .m34-mbar { display: block; height: 6px; border-radius: 99px; background: rgba(242,232,216,.1); overflow: hidden; }
html:not(#rs) #homeHub .m34-mbar i { display: block; height: 100%; width: 0; background: linear-gradient(90deg, #7a2433, #D2B184); border-radius: inherit; }
html:not(#rs) #homeHub .m34-mis.m34-empty .m34-mbar { display: none; }
html:not(#rs) #homeHub .m34-mrow { display: flex; align-items: center; justify-content: space-between; gap: .6rem; }
html:not(#rs) #homeHub .m34-mfrac { font-family: 'IBM Plex Mono', monospace; font-size: .72rem; color: rgba(242,232,216,.7); }
html:not(#rs) #homeHub .m34-mgo { margin-left: auto; min-height: 2.25rem; padding: 0 .9rem; border-radius: 999px; border: 1px solid rgba(210,177,132,.6); background: transparent; color: #D2B184; font: inherit; font-weight: 700; font-size: .78rem; cursor: pointer; }
@media (max-width: 360px) {
  html:not(#rs) #homeHub { padding-left: calc(.75rem + var(--sal, 0px)); padding-right: calc(.75rem + var(--sar, 0px)); }
  html:not(#rs) #homeHub .m34-poster { width: 3.6rem; }
  html:not(#rs) #homeHub .m34-ntitle { font-size: 1.05rem; }
  html:not(#rs) #homeHub .m34-next { gap: .65rem; padding: .6rem; }
  html:not(#rs) #homeHub .m34-stat b { font-size: .95rem; }
  html:not(#rs) #homeHub .m34-acc { font-size: .8rem; padding: .4rem .4rem; }
}
@media (max-height: 640px) { html:not(#rs) #homeHub .home-hub-inner { padding-top: 2.8rem; gap: .55rem; } }
'''
s=re.sub(r'/\* M34-CSS \*/.*?(?=</style>)','',s,flags=re.S)
k=s.index('</style>'); s=s[:k]+CSS+s[k:]

# ---- D) JS ----
JS=r'''<script>/* M34 home */
(function () {
  try {
    var D = document, W = window, $ = function (i) { return D.getElementById(i); };
    var UNI = { mcu: 'MCU', sony: "Sony's Spider-Man", fox: 'Fox-Verse', legacy: 'Legacy', animazione: 'Animazione' };
    var M = W.TVA_IMG_MANIFEST || {}, T = W.tvaTmdb;
    function setPoster(num, emblem) {   /* stessa priorita' delle schede Timeline: manifest autorizzato -> TMDB -> emblema */
      var box = $('m34Poster'), fb = $('m34Pfb'); if (!box || !fb) return;
      var old = box.querySelector('img'); if (old) old.remove();
      box.classList.remove('m34-has'); fb.textContent = emblem || '🎬';
      if (!num) return;
      var m = M['item:' + num], ok = !!(m && m.src && m.licence && m.verified === true), t = T ? T.poster(num, 'thumb') : null;
      if (!ok && !t) return;
      var im = new Image(); im.alt = ''; im.decoding = 'async'; im.referrerPolicy = 'no-referrer';
      function usaT() { im.setAttribute('data-src', 'tmdb'); im.srcset = t.srcset; im.src = t.src; }
      im.onload = function () { box.classList.add('m34-has'); };
      im.onerror = function () { if (ok && t && im.getAttribute('data-src') !== 'tmdb') { ok = false; usaT(); } else { im.remove(); box.classList.remove('m34-has'); } };
      if (ok) im.src = m.src; else usaT();
      box.insertBefore(im, box.firstChild);
    }
    function fillNext() {
      var n = W.marvelHomeNext, meta = $('m34NextMeta'), cta = $('m34NextCta'), row = $('hhsNextRow'), val = $('hhsNextValue');
      if (!val) return;
      if (!n) {   /* nessun titolo disponibile: tutto visto (o nulla ancora sbloccato) */
        setPoster(null, '🏆'); if (meta) meta.textContent = 'Hai completato tutti i titoli disponibili'; if (cta) cta.style.display = 'none'; if (row) row.setAttribute('aria-label', 'Tutto visto'); return;
      }
      var li = $('item-' + n.id), yr = li && li.querySelector('.yr'), st = li && li.getAttribute('data-studio'), ic = li && li.querySelector('summary .ic');
      var parts = []; if (yr && yr.textContent.trim()) parts.push(yr.textContent.trim()); if (st && UNI[st]) parts.push(UNI[st]);
      if (meta) meta.textContent = parts.join(' · ');
      if (cta) { cta.style.display = ''; cta.textContent = (W.marvelHomeCount > 0 ? 'Continua' : 'Inizia') + ' →'; }
      if (row) row.setAttribute('aria-label', 'Prossimo titolo: ' + n.title + (parts.length ? ', ' + parts.join(', ') : ''));
      setPoster(n.id, ic ? ic.textContent.trim() : '');
    }
    D.addEventListener('tva:homenext', fillNext);
    function missSync() {   /* una sola missione attiva, da dati reali: le missioni senza descrizione valida non vengono mostrate */
      var box = $('m34Mis'); if (!box) return;
      var pick = null, valid = 0, done = 0;
      ['missioneSettimanale', 'missioneTematica', 'missioneSaga'].forEach(function (id) {
        var r = $(id); if (!r) return;
        var t = r.querySelector('.missione-testo'), f = r.querySelector('.missione-frac');
        var txt = ((t && t.textContent) || '').replace(/\s+/g, ' ').trim(), m = /(\d+)\s*\/\s*(\d+)/.exec((f && f.textContent) || '');
        if (!txt || /^[—–-]+$/.test(txt) || !m || +m[2] === 0) return;
        valid++; if (r.classList.contains('missione-completa')) { done++; return; }
        if (!pick) pick = { txt: txt, a: +m[1], b: +m[2] };
      });
      var nm = $('m34MName'), fr = $('m34MFrac'), fl = $('m34MFill');
      box.classList.toggle('m34-empty', !pick);
      if (pick) { nm.textContent = pick.txt; fr.textContent = pick.a + '/' + pick.b; fl.style.width = Math.round(100 * Math.min(pick.a, pick.b) / pick.b) + '%'; }
      else { nm.textContent = valid && done === valid ? 'Tutte le missioni di questa settimana sono completate' : 'Nessuna missione attiva al momento'; fr.textContent = ''; fl.style.width = '0%'; }
    }
    D.addEventListener('tva:missioni', missSync); missSync(); setTimeout(missSync, 800);
    function go(btnId, tabId) { var b = $(btnId); if (b) b.addEventListener('click', function () { var t = $(tabId); if (t) t.click(); }); }
    go('m34Atl', 'appTabAtlante'); go('m34Tes', 'appTabTessera'); go('m34MGo', 'appTabMissioni');
    if (typeof W.marvelUpdateHomeHub === 'function') W.marvelUpdateHomeHub(); else fillNext();
  } catch (eM34) { if (window.console) console.error('M34 home', eM34); }
})();
</script>'''
s=re.sub(r'<script>/\* M34 home \*/.*?</script>\n?','',s,flags=re.S)
k=s.rindex('</body>'); s=s[:k]+JS+'\n'+s[k:]
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+'20261023-1600-m34',s)
open(P,'w',encoding='utf-8').write(s)
