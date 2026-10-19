import re, json, sys
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt, (s.count(old), old[:80])
    s=s.replace(old,new)

# ---------- 1. estrai li 133 e rimuovilo dalla posizione attuale ----------
a=s.index('<li class="card-wrap" id="item-133"')
b=s.index('</li>',a)+5
li133=s[a:b]
assert '<li' not in li133[4:]
# rimuove anche il "\n" che precede
s=s[:a]+s[b:].lstrip('\n')
assert s[a-1]=='\n'

# ---------- 2. nuova scheda variante ----------
new133 = '''<li class="card-wrap card-variant" id="item-133" data-item="133" data-variant-of="089" data-tag="verde" data-studio="mcu" data-type="film" data-cats="film mcu infinity variante" data-weekend="0" data-search="avengers: endgame encore versione alternativa riedizione" data-uni="uni-earth-199999-mcu">
    <label class="watch-box" title="Segna la versione Encore come vista (non conta nel progresso)">
      <input type="checkbox" class="variant-check" data-item="133" data-variant-of="089" data-cats="film mcu infinity variante">
      <span class="watch-mark">&#10003;</span>
    </label>
    <button type="button" class="fav-star" data-item="133" title="Aggiungi ai preferiti">&#9734;</button>
    <details class="card">
      <summary>
        <span class="rec rec-var">&#8627;</span>
        <span class="ic">🎞️</span>
        <div class="item-body">
          <div class="item-top"><span class="title">Avengers: Endgame Encore</span> <span class="yr">in sala dal 25 set 2026</span>
            <span class="tag tag-variante" title="VERSIONE ALTERNATIVA di N°089 — non conta come titolo autonomo">VERSIONE ALTERNATIVA</span>
          </div>
          <div class="item-note">riedizione in sala di N&deg;089 con circa 4 minuti di scene aggiunte &middot; non conta nel progresso</div>
        </div>
        <span class="chev">&#9656;</span>
      </summary>
      <div class="detail-panel"><div class="detail-row"><span class="detail-k">VERSIONE DI</span><span class="detail-v">N&deg;089 &mdash; Avengers: Endgame (il film resta quello: stessa trama, stessi eventi)</span></div><div class="detail-row"><span class="detail-k">UNIVERSO</span><span class="detail-v">MCU</span></div><div class="detail-row lvl-light"><span class="detail-k">DURATA</span><span class="detail-v">185 min secondo AMC Theatres (l&rsquo;originale dura 181 min): circa 4 minuti in pi&ugrave;</span></div><div class="detail-row lvl-light"><span class="detail-k">DISTRIBUZIONE</span><span class="detail-v">Riedizione cinematografica (25 settembre 2026, gi&agrave; uscita in sala). Nessuna disponibilit&agrave; in streaming verificata</span></div><div class="detail-row lvl-light"><span class="detail-k">CONTEGGIO</span><span class="detail-v">Non &egrave; un titolo autonomo: non aumenta i titoli, la percentuale, gli XP n&eacute; i distintivi. Se l&rsquo;hai vista, puoi spuntarla solo come annotazione personale.</span></div><details class="sub-group">
          <summary>&#128260; Cosa cambia rispetto al film</summary>
          <div class="sub-group-body"><div class="detail-row "><span class="detail-k">FILM PRINCIPALE</span><span class="detail-v ">Invariato: la storia di Endgame (N&deg;089) &egrave; la stessa. Chi ha visto N&deg;089 non perde nulla di essenziale per capire il resto della guida.</span></div><div class="detail-row "><span class="detail-k">CONTENUTO AGGIUNTO</span><span class="detail-v ">Circa 4 minuti di materiale nuovo. Joe Russo lo ha descritto come una &laquo;critical companion story&raquo; che fa da ponte tra Endgame e Avengers: Doomsday (citazione riportata da GamesRadar).</span></div><div class="detail-hint" style="font-size:0.78rem;opacity:0.8;padding:0.3rem 0;">Fonti: AMC Theatres (durata, via GamesRadar); GamesRadar; TheWrap; Murphy&rsquo;s Multiverse. Marvel Studios non ha pubblicato una descrizione ufficiale dettagliata delle scene.</div><div class="detail-row spoiler-hint">Dettaglio delle scene aggiunte nascosto: attiva gli spoiler per vederlo.</div><div class="detail-row spoiler-row"><span class="detail-k">SCENE AGGIUNTE (RIPORTATE)</span><span class="detail-v spoiler-row">La stampa riporta una scena finale estesa in cui Loki si offre di aiutare Steve e Peggy, e tre scene a fine film: Bruce Banner prelevato da Doctor Doom, una scena della TVA su incursioni tra universi e la forgia di una maschera. Le fonti divergono sui dettagli e parte del materiale proviene da proiezioni internazionali o da formati premium (IMAX / Infinity Vision): trattalo come non confermato da Marvel e non come parte del canone verificato.</span></div></div>
        </details><details class="sub-group">
          <summary>&#128279; Ordine di visione</summary>
          <div class="sub-group-body"><div class="detail-row lvl-light"><span class="detail-k"></span><span class="detail-v lvl-light">Va vista al posto di (o dopo) N&deg;089, mai come film in pi&ugrave;: &egrave; Endgame con scene aggiunte. Per capire Doomsday (N&deg;136) basta N&deg;089; la versione Encore &egrave; un extra facoltativo.</span></div></div>
        </details></div>
      <div class="rating-widget" data-item="133">
        <span class="rating-label">Il tuo voto:</span>
        <span class="rating-stars">
          <span class="rating-star" data-value="1">&#9734;</span><span class="rating-star" data-value="2">&#9734;</span><span class="rating-star" data-value="3">&#9734;</span><span class="rating-star" data-value="4">&#9734;</span><span class="rating-star" data-value="5">&#9734;</span>
        </span>
      </div>
      <details class="note-toggle">
        <summary>&#128221; + Aggiungi una nota personale</summary>
        <div class="user-note-box">
          <textarea class="user-note" id="note-133" data-item="133" rows="2" placeholder="Scrivi qui un tuo pensiero, un ricordo, un promemoria... si salva da solo."></textarea>
        </div>
      </details>
    </details>
    </li>
'''
# inserisci subito dopo li 089
i089=s.index('<li class="card-wrap" id="item-089"')
e089=s.index('</li>',i089)+5
assert s[e089]=='\n'
s=s[:e089+1]+new133+s[e089+1:]

# ---------- 3. sezione "Versioni alternative" nella scheda 089 ----------
i089=s.index('<li class="card-wrap" id="item-089"')
e089=s.index('</li>',i089)
blk=s[i089:e089]
marker='</details></div>\n      <details class="watch-picker">'
assert blk.count(marker)==1
alt='''</details><details class="sub-group" id="altVersions-089">
          <summary>&#127902;&#65039; Versioni alternative</summary>
          <div class="sub-group-body"><div class="detail-row lvl-light"><span class="detail-k">ENDGAME ENCORE</span><span class="detail-v lvl-light">Riedizione in sala (25 set 2026) dello stesso film, con circa 4 minuti di scene aggiunte. Non &egrave; un titolo autonomo e non conta nel progresso. <a href="#item-133" class="variant-goto" data-goto="133">Apri la scheda Encore &rarr;</a></span></div></div>
        </details></div>
      <details class="watch-picker">'''
blk=blk.replace(marker,alt)
s=s[:i089]+blk+s[e089:]

# ---------- 4. CSS ----------
rep('.watch-check { display: none; }','.watch-check { display: none; }\n.variant-check { display: none; }\n.variant-check:checked ~ .watch-mark { background: var(--accent-green); border-color: var(--accent-green); color: #fff; opacity: .75; }\n.card-variant { margin-left: 1.1rem; }\n.card-variant details.card { border-left-style: dashed !important; }\n.rec-var { opacity: .7; }\n.tag-variante { color: var(--ink-soft, #888); border: 1px dashed currentColor; border-radius: 4px; padding: 0 .3rem; font-size: .66rem; white-space: nowrap; }\n.variant-goto { text-decoration: underline; cursor: pointer; }')

# ---------- 5. JS: stato con varianti ----------
rep("  var STORAGE_KEY = 'marvel-ultimate-timeline-watched';",
"""  var STORAGE_KEY = 'marvel-ultimate-timeline-watched';
  // ---- Versioni alternative: opere che NON sono titoli autonomi (es. Endgame Encore, id storico 133, variante
  // di 089). Il loro flag "visto" resta nello stesso salvataggio, sotto lo stesso id (nessuna migrazione, nessuna
  // perdita), ma loadState() lo nasconde ai calcoli di progresso/XP/badge/amici e saveState() lo preserva sempre. ----
  var VARIANT_IDS = { '133': '089' };""")
rep("""  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); } catch(e) { return {}; }
  }
  function saveState(state) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch(e) {}
  }""",
"""  function loadStateRaw() {
    try { var r = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}'); return (r && typeof r === 'object') ? r : {}; } catch(e) { return {}; }
  }
  function loadState() {
    var s = loadStateRaw();
    Object.keys(VARIANT_IDS).forEach(function(v) { delete s[v]; });
    return s;
  }
  function saveState(state) {
    try {
      var raw = loadStateRaw(), out = {};
      Object.keys(state).forEach(function(k) { if (!VARIANT_IDS[k]) out[k] = state[k]; });
      Object.keys(VARIANT_IDS).forEach(function(v) { if (raw[v]) out[v] = raw[v]; });
      localStorage.setItem(STORAGE_KEY, JSON.stringify(out));
    } catch(e) {}
  }
  function setVariantSeen(id, on) {
    try {
      var raw = loadStateRaw();
      if (on) raw[id] = true; else delete raw[id];
      localStorage.setItem(STORAGE_KEY, JSON.stringify(raw));
    } catch(e) {}
  }""")
# badge range: salta le varianti
rep("""      for (var n = b.start; n <= b.end; n++) {
        if (!d.visti[('000' + n).slice(-3)]) return false;""",
"""      for (var n = b.start; n <= b.end; n++) {
        var kRange = ('000' + n).slice(-3);
        if (VARIANT_IDS[kRange]) continue;
        if (!d.visti[kRange]) return false;""")
# handler checkbox variante: dopo il ciclo allChecks principale
rep("""      })(allChecks[i]);
    }
    updateProgress();
""","""      })(allChecks[i]);
    }
    // Checkbox delle versioni alternative: solo annotazione personale, nessun contatore/XP/missione.
    Array.prototype.slice.call(document.querySelectorAll('.variant-check')).forEach(function(vchk) {
      var vid = vchk.getAttribute('data-item');
      var vwrap = vchk.closest ? vchk.closest('.card-wrap') : null;
      if (loadStateRaw()[vid]) { vchk.checked = true; if (vwrap) vwrap.classList.add('watched'); }
      vchk.addEventListener('change', function() {
        setVariantSeen(vid, vchk.checked);
        if (vwrap) vwrap.classList.toggle('watched', vchk.checked);
      });
    });
    Array.prototype.slice.call(document.querySelectorAll('.variant-goto')).forEach(function(lk) {
      lk.addEventListener('click', function(ev) {
        ev.preventDefault();
        var t = document.getElementById('item-' + lk.getAttribute('data-goto'));
        if (!t) return;
        var d = t.querySelector('details'); if (d) d.open = true;
        try { t.scrollIntoView({ behavior: 'smooth', block: 'start' }); } catch(eSv) { t.scrollIntoView(); }
      });
    });
    updateProgress();
""")
# import: accetta id variante
rep("Array.prototype.forEach.call(document.querySelectorAll('.watch-check'), function(c) { idTitoli[c.getAttribute('data-item')] = true; });",
    "Array.prototype.forEach.call(document.querySelectorAll('.watch-check, .variant-check'), function(c) { idTitoli[c.getAttribute('data-item')] = true; });")

# ---------- 6. dati: WATCH_ORDER_JS, altTimelineData, mvMapData, atlas ----------
rep(', {"id": "133", "tag": "blu", "title": "Avengers: Endgame Encore"}','')
m=re.search(r'(id="altTimelineData">)(.*?)(</script>)',s,re.S)
arr=json.loads(m.group(2)); n0=len(arr)
arr=[x for x in arr if x['num']!=133]; assert len(arr)==n0-1
s=s[:m.start(2)]+json.dumps(arr)+s[m.end(2):]
m=re.search(r'(id="mvMapData">)(.*?)(</script>)',s,re.S)
mv=json.loads(m.group(2)); u=mv['universi']['uni-earth-199999-mcu']
assert '133' in u['titoliIds'] and u['titoli']==94 and u['film']==41
u['titoliIds'].remove('133'); u['titoli']=93; u['film']=40
if 'titoliIds' in u and isinstance(u.get('titoliIds'),list): pass
s=s[:m.start(2)]+json.dumps(mv)+s[m.end(2):]
m=re.search(r'(id="atlasData">)(.*?)(</script>)',s,re.S)
at=json.loads(m.group(2))
for o in at['opere']:
    if o['id']=='133':
        o['ruolo']='variante'; o['variantDi']='089'; o['annoCard']='in sala dal 25 set 2026'; o['ambientazione']='2012-2023'
at['nota_varianti']='Le opere con ruolo "variante" (id 133, Avengers: Endgame Encore, variante di 089) non sono titoli autonomi e non entrano nei conteggi.'
s=s[:m.start(2)]+json.dumps(at,ensure_ascii=False,separators=(',',':'))+s[m.end(2):]

# ---------- 7. testi con "139" ----------
rep('Gli stessi 139 titoli, riordinati per uscita reale','Gli stessi 138 titoli, riordinati per uscita reale')
rep('Gli stessi 139 titoli, riordinati a scelta','Gli stessi 138 titoli, riordinati a scelta')
rep('id="tesseraTitoliAssoluti">0/139<','id="tesseraTitoliAssoluti">0/138<')
rep('&mdash; 139 titoli tra film, serie e speciali','&mdash; 138 titoli tra film, serie e speciali (pi&ugrave; 1 versione alternativa)')
rep('<b>139</b>titoli numerati','<b>138</b>titoli autonomi (+1 variante)')
rep('id="progressPct">0/139<','id="progressPct">0/138<')
rep('id="dashHoloSub">0/139 titoli visti','id="dashHoloSub">0/138 titoli visti')
rep('FASCICOLO CHIUSO &middot; 139 VOCI','FASCICOLO CHIUSO &middot; 138 OPERE + 1 VARIANTE')
open(P,'w',encoding='utf-8').write(s)
print('ok')
