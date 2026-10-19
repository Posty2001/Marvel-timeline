import re,json
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:70]); s=s.replace(old,new)

# 1) mappa dipendenze di 136: nuova ripartizione
m=re.search(r'(var DEPENDENCY_MAP_JS = )(\{.*?\})(;\n)',s); d=json.loads(m.group(2))
old136=d['136']; assert old136=={"ess":["125","112","117"],"cons":["089","123"],"opz":["131"]}
d['136']={"ess":["089","112","123","125"],
          "cons":["041","051","084","095","097","099","102","108","117","121","015","016"],
          "opz":["131","104","109","094","069","085","017"]}
allids=[x for k in d['136'] for x in d['136'][k]]; assert len(allids)==len(set(allids))==23
s=s[:m.start(2)]+json.dumps(d)+s[m.end(2):]

# 2) motivi e tipi di legame (solo fatti verificati)
MOT={
'089':(['uff','narr'],"Doomsday è presentato come quinto film degli Avengers dopo Endgame (Disney+). Nel cast annunciato: Steve Rogers, Peggy Carter, Thor."),
'112':(['uff','narr'],"Loki (Hiddleston) è nel cast annunciato; la stagione 2 chiude l'arco di Loki e della TVA, a cui la guida lega il tema multiversale."),
'123':(['uff','narr'],"Nel cast annunciato: Yelena, Bucky, Red Guardian, Sentry, US Agent e Ghost, cioè il gruppo riunito in questo film."),
'125':(['uff','narr'],"Nel cast annunciato: Reed Richards, Sue Storm, Johnny Storm e Ben Grimm; è l'unico film con questa versione dei Fantastic Four."),
'041':(['uff','narr'],"Origine di Steve Rogers e Peggy Carter, entrambi nel cast annunciato."),
'051':(['uff','narr'],"Nascita della squadra degli Avengers e primo scontro con Loki."),
'084':(['uff','narr'],"Fa da ponte verso Endgame; vi compaiono Thor e Steve Rogers."),
'095':(['uff','narr'],"Necessario per capire Loki stagione 2 (prerequisito diretto)."),
'097':(['uff'],"Shang-Chi (Simu Liu) è nel cast annunciato; il film è la sua unica storia solista."),
'099':(['uff','narr'],"Mostra l'apertura del multiverso e le incursioni di altre linee. Spider-Man NON risulta nel cast annunciato."),
'102':(['uff','narr'],"Qui compare il Charles Xavier di Earth-838 (Patrick Stewart, nel cast annunciato). Non è confermato che sia lo stesso personaggio in Doomsday."),
'108':(['uff'],"Nel cast annunciato: Shuri, M'Baku, Namor e Namora, tutti legati a questo film."),
'117':(['uff','narr'],"Gambit (Channing Tatum, nel cast annunciato) appare qui. Wolverine e Deadpool NON risultano nel cast annunciato. Prima era Essenziale: declassato a Consigliato."),
'121':(['uff'],"Sam Wilson come Captain America (Anthony Mackie) e Joaquin Torres (Danny Ramirez) sono nel cast annunciato."),
'015':(['uff','ipo'],"Marvel lo include nella sua lista. Gli attori Fox sono nel cast annunciato, ma come i film Fox si colleghino a Doomsday non è dichiarato."),
'016':(['uff','ipo'],"Marvel lo include nella sua lista (Nightcrawler: Alan Cumming è nel cast annunciato). Il collegamento narrativo con Doomsday non è dichiarato."),
'131':(['ipo'],"Serie animata a continuità separata: nessun legame con Doomsday è stato confermato."),
'104':(['narr'],"Thor (Chris Hemsworth) è nel cast annunciato; qui è la sua ultima storia solista. Non è nella lista Marvel."),
'109':(['narr'],"Paul Rudd (Ant-Man) e Kathryn Newton (Cassie Lang) sono nel cast annunciato; il film li vede protagonisti. Non è nella lista Marvel."),
'094':(['narr'],"Percorso di Sam Wilson verso Captain America e di Bucky Barnes (entrambi nel cast annunciato). Non è nella lista Marvel."),
'069':(['narr'],"Origine di Yelena Belova e Red Guardian (nel cast annunciato). Non è nella lista Marvel."),
'085':(['narr'],"Introduce Ghost (Hannah John-Kamen, nel cast annunciato). Non è nella lista Marvel."),
'017':(['ipo'],"Kelsey Grammer (Beast) è nel cast annunciato; nessun collegamento narrativo dichiarato. Non è nella lista Marvel."),
}
assert set(MOT)==set(allids)
rep("  var DEPENDENCY_MAP_JS = ","  // Motivi e tipo di legame per le voci di Doomsday (N°136). uff = confermato ufficialmente (lista Marvel/Disney+ \"Countdown to Avengers: Doomsday\" e/o cast annunciato);\n  // narr = legame narrativo dimostrabile nei titoli gia' usciti; ipo = ipotesi editoriale della guida. Verificato il 15 ott 2026.\n  var DEP_MOTIVI_JS = {\"136\": "+json.dumps({k:{'lk':v[0],'why':v[1]} for k,v in MOT.items()},ensure_ascii=False)+"};\n  var DEP_LK_DEF = { uff: ['\\u2705', 'Confermato ufficialmente'], narr: ['\\uD83D\\uDD17', 'Legame narrativo dimostrabile'], ipo: ['\\uD83D\\uDCA1', 'Ipotesi editoriale'] };\n  var DEPENDENCY_MAP_JS = ")

# 3) rendering chip
rep("""            return '<button type="button" class="dep-chip" data-num="' + n + '"><span class="dep-chip-check" data-check-for="' + n + '-' + targetNum + '">&#11036;</span> ' + titolo + (viaCatena[n] ? ' <span class="dep-chip-via">(obbligatorio via ' + titoloPerDipendenza(viaCatena[n]) + ')</span>' : '') + '</button>';""",
"""            var mot = DEP_MOTIVI_JS[targetNum] && DEP_MOTIVI_JS[targetNum][n];
            var lkHtml = '', whyHtml = '';
            if (mot) {
              lkHtml = ' <span class="dep-chip-lk">' + mot.lk.map(function(k) { return '<span title="' + DEP_LK_DEF[k][1] + '" aria-label="' + DEP_LK_DEF[k][1] + '">' + DEP_LK_DEF[k][0] + '</span>'; }).join('') + '</span>';
              whyHtml = '<span class="dep-chip-why">' + mot.why.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>';
            }
            return '<button type="button" class="dep-chip' + (mot ? ' dep-chip-rich' : '') + '" data-num="' + n + '"><span class="dep-chip-row"><span class="dep-chip-check" data-check-for="' + n + '-' + targetNum + '">&#11036;</span> ' + titolo + lkHtml + (viaCatena[n] ? ' <span class="dep-chip-via">(obbligatorio via ' + titoloPerDipendenza(viaCatena[n]) + ')</span>' : '') + '</span>' + whyHtml + '</button>';""")
rep("var CAT_DEFS = [['ess', 'ESSENZIALI', '\\uD83D\\uDFE2'], ['cons', 'CONSIGLIATI', '\\uD83D\\uDD35'], ['opz', 'OPZIONALI', '\\uD83D\\uDFE1']];",
    "var CAT_DEFS = [['ess', 'ESSENZIALI', '\\uD83D\\uDFE2'], ['cons', 'CONSIGLIATI', '\\uD83D\\uDD35'], ['opz', 'FACOLTATIVI', '\\uD83D\\uDFE1']];")
rep("""'<div class="dep-map-body"><p class="dep-map-editorial-note">Selezione curata da questa guida, non una classificazione ufficiale Marvel.</p>' + catHtml + '</div></details>';""",
"""'<div class="dep-map-body"><p class="dep-map-editorial-note">Selezione curata da questa guida, non una classificazione ufficiale Marvel.</p>' + (DEP_MOTIVI_JS[targetNum] ? DEP_LEGENDA_HTML : '') + catHtml + (DEP_MOTIVI_JS[targetNum] ? DEP_FONTI_HTML : '') + '</div></details>';""")
rep("  function initDependencyMaps() {","""  var DEP_LEGENDA_HTML = '<p class="dep-map-legend"><b>Come leggere i livelli.</b> Essenziale: Doomsday ne è il seguito diretto, o è l&rsquo;unica fonte di un gruppo o arco intero presente nel cast annunciato. Consigliato: approfondisce personaggi del cast annunciato o titoli indicati da Marvel. Facoltativo: contesto in più. <span class="dep-lk-key">&#9989; confermato ufficialmente &middot; &#128279; legame narrativo dimostrabile &middot; &#128161; ipotesi editoriale</span></p>';
  var DEP_FONTI_HTML = '<p class="dep-map-sources">Marvel e Disney+ precisano che per vedere Doomsday non serve alcun ripasso: la lista &laquo;Countdown to Avengers: Doomsday&raquo; (15 titoli, che nella guida diventano le 16 schede della missione Road to Doomsday) &egrave; solo un consiglio. Il cast &egrave; quello annunciato (Disney+ avverte che una parte resta non rivelata). Personaggi solo ipotizzati o trapelati, come Wolverine, Deadpool o Spider-Man, non rendono Essenziale alcun titolo. Controllato il 15 ottobre 2026 su Marvel.com e Disney+.</p>';
  function initDependencyMaps() {""")
# CSS
rep(".dep-chip-via { font-size: 0.75rem; opacity: 0.8; }",
""".dep-chip-via { font-size: 0.75rem; opacity: 0.8; }
.dep-chip-rich { flex-direction: column; align-items: flex-start; text-align: left; width: 100%; }
.dep-chip-row { display: inline-flex; align-items: center; gap: 0.3rem; flex-wrap: wrap; }
.dep-chip-lk { font-size: 0.72rem; letter-spacing: 0.1em; }
.dep-chip-why { font-size: 0.64rem; font-family: 'IBM Plex Mono', monospace; color: var(--ink-soft); line-height: 1.35; font-weight: normal; }
.dep-map-legend, .dep-map-sources { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: var(--ink-soft); line-height: 1.45; margin: 0; }
.dep-lk-key { display: block; margin-top: 0.25rem; }
.rtd-tier { font-family: 'IBM Plex Mono', monospace; font-size: 0.5rem; letter-spacing: 0.04em; border: 1px solid var(--line); border-radius: 3px; padding: 0 0.25rem; color: var(--ink-soft); flex-shrink: 0; }""")

# 4) RTD: livello per voce + nota
rep("      var st = document.createElement('span'); st.className = 'rtd-st';\n      btn.appendChild(n); btn.appendChild(t); btn.appendChild(y); btn.appendChild(st);",
"""      var st = document.createElement('span'); st.className = 'rtd-st';
      var tierEl = null;
      try {
        var cats136 = DEPENDENCY_MAP_JS['136'], tl = null;
        if (cats136.ess.indexOf(id) !== -1) tl = 'ESSENZ.'; else if (cats136.cons.indexOf(id) !== -1) tl = antecedenteViaCatena('136', id) ? 'ESSENZ.' : 'CONSIGL.'; else if (cats136.opz.indexOf(id) !== -1) tl = 'FACOLT.';
        if (tl) { tierEl = document.createElement('span'); tierEl.className = 'rtd-tier'; tierEl.textContent = tl; tierEl.title = 'Livello nel percorso verso Doomsday (N\\u00B0136)'; }
      } catch(eRtdTier) {}
      btn.appendChild(n); btn.appendChild(t); if (tierEl) btn.appendChild(tierEl); btn.appendChild(y); btn.appendChild(st);""")
rep("16 schede gi&agrave; presenti in timeline, nell&rsquo;ordine di visione.","Le 16 schede della lista &laquo;Countdown to Avengers: Doomsday&raquo; di Marvel/Disney+ (consiglio, non obbligo), nell&rsquo;ordine di visione. Il livello (essenziale, consigliato, facoltativo) &egrave; della guida e si legge nella scheda N&deg;136.")
open(P,'w',encoding='utf-8').write(s); print('ok')
