# TVA Archives — correzioni iPhone, navigazione Multiverso e voto a mezze stelle

Build: `20261019-1130-fix-ios-voti` (base `20261019-1030-fase4-dossier`). Fase 5 non avviata.
**Limite dichiarato:** nessun Safari/iPhone reale disponibile. Tutti i test sono su Chromium con touch emulato, che NON è equivalente a Safari. I due difetti iOS (sovrapposizione, area scura del grafo) non sono riproducibili in Chromium: ho individuato la causa nel codice e applicato i rimedi già adottati nel progetto, ma la conferma finale va fatta sul tuo iPhone.

## 1. Cause
1. **Sovrapposizione dopo la registrazione.** Causa reale (verificata): mentre l'onboarding è attivo, `journeyStarted` non è ancora spuntato, quindi la regola `#journeyStarted:checked ~ .intro-screen {display:none}` non scatta e l'introduzione resta **montata e `display:block`** sotto la registrazione (misurato: intro a 844 px di altezza sotto l'onboarding). L'onboarding la copriva solo grazie a un overlay `position:fixed; height:100dvh`, che su iOS può restare più corto del viewport visibile (barra Safari, standalone): sotto compare l'intro con «Inizia il viaggio». Problema di stato, non di z-index.
2. **«Esplora il Multiverso».** Il pulsante della Home era un `<label for="multiverseGraphToggle">`: apriva direttamente il vecchio grafo. Stesso collegamento nella scheda «Grafico del Multiverso» della guida.
3. **Grafo classico con area scura.** `.multiverse-graph-overlay` era `position:fixed; height:100dvh; overflow-y:auto; transform:translateZ(0); will-change:transform`: esattamente il pattern che il file stesso documenta come bug iOS (area scoperta in basso) e che era già stato rimosso per Tessera, Friends e Database, ma non per questo overlay. In Chromium lo scorrimento interno funziona, per questo non si riproduce.
4. **Voto.** Cinque stelle intere salvate come interi 1–5, widget in fondo alla scheda dopo «Guarda» e «File locale»; la validazione dell'import e l'«ultimo titolo visto» accettavano/mostravano solo interi.

## 2. Correzioni applicate
- **Registrazione:** classe di stato `tva-onb` sull'`<html>`, impostata all'avvio dell'onboarding e rimossa a «Inizia la timeline» e nel ripiego d'errore: l'introduzione viene smontata finché la registrazione è attiva. In più l'onboarding ora copre il viewport con `bottom:0` invece di una sola altezza in dvh.
- **Multiverso:** Home e scheda guida aprono la **Mappa 3B** (`tvaAtlas2.ext.api.openMappa`); il grafo classico resta come opzione secondaria (guida: «Grafo classico»; Atlante/Universi e pannelli della Mappa invariati). Se l'Atlante non fosse disponibile c'è un ripiego sul grafo classico. La Mappa 3B non è stata modificata.
- **Grafo classico:** l'overlay è ora contenuto normale della pagina (`position:static`, `min-height:100dvh`, niente transform/will-change), come Tessera/Friends/Database; tolto lo spazio riservato alla barra inferiore. Contenuto, dati e logica invariati; nessun contenuto nascosto via CSS.
- **Voto** (stessa chiave `marvel-ultimate-timeline-ratings`, stesso oggetto, nessuna seconda sorgente):
  - Posizione: subito sotto titolo e informazioni principali, prima di Trama e descrizioni (139 schede).
  - Blocco unico compatto (~82 px): «LA TUA VALUTAZIONE», 5 stelle oro #D2B184 con riempimento a mezza stella, voto «3,5 / 5» a destra, «Azzera» visibile solo con un voto; bordi bordeaux, microanimazione disattivata con `prefers-reduced-motion`.
  - Ogni stella ha due zone di tocco (sinistra = mezzo voto, destra = intero) come elementi veri: nessuna coordinata né hover.
  - Tastiera/AT: `role="slider"` (0–5), frecce ±0,5, PageUp/PageDown ±1, End = 5, Home/Canc = azzera, cifre 1–5, `aria-valuetext` («3,5 su 5»), annuncio vocale.
  - Il voto conta come salvato solo se rileggibile; altrimenti la UI non lo mostra e avvisa.
  - Voti interi esistenti invariati. Aggiornati: validazione import profilo (multipli di 0,5 da 0,5 a 5), «ultimo titolo visto» (miniatura a mezze stelle). Le medie (Home, Dashboard, Tessera) funzionavano già con i decimali.
  - Note personali e altre chiavi: non toccate.

## 3. File modificati
Build: `index.html`. Nuovi: `tools/patch_fix_ios.py`, `tools/fix_ios.css`, `tools/fix_rating_block.js`. Modificati: `tools/build_4.sh` (aggiunge il patch, pipeline idempotente verificata), `tools/patch_fase1.py` (build id). Test: nuovi `fx_test1–4`; aggiornati solo nelle aspettative `a2_test`, `cons_test`, `d3a_test`, `net_test`, `tva_test`, `ui_audit` (flusso N° → Dossier Opera, già della Fase 4), `data_test` (il widget voto cambia testo/posizione), `imp.py` (3,5 ora valido; 3,3 e 0,25 rifiutati), `rs_test`, `stats_fix_test` (build id).

## 4. Screenshot
`screenshot_fix_ios/` — prima/dopo a 390×844 e 320×568: onboarding (step 1 e 2), home, scheda con voto, grafo classico (alto/centro/basso). Nota: i «prima» del grafo in Chromium sembrano uguali ai «dopo» perché il difetto è specifico di iOS.

## 5. Test (Chromium, touch emulato)
- Registrazione `fx_test1` 40/0 (390, 320, 430): primo accesso, step 1 e 2 con hit-test su 15 punti (solo onboarding), viewport dinamica, «Inizia la timeline» col tocco, refresh, accessi successivi, reduced-motion.
- Multiverso `fx_test2` 26/0 (390, 320): Home → Mappa → Indietro → Home; Mappa → grafo classico → Indietro → Mappa; Universi → grafo classico → Indietro → Universi; scheda guida.
- Grafo `fx_test3` 20/0: contenuto finale raggiungibile, area vuota sotto ≤ 120 px, comandi zoom colpibili, tocco su un nodo, viewport dinamica senza area scoperta.
- Voto `fx_test4` 35/0: 10 valori col tocco, mezza stella verificata sui pixel, salvataggio/caricamento, modifica, azzeramento, refresh, voti interi preesistenti, media (4,1,5,3,5 → 3,3), tastiera, errore di salvataggio, note intatte, 6 viewport 320–430 (zone di tocco ≥ 44 px di altezza, nessun overflow).
- Regressione completa: nessun nuovo fallimento. Verdi: `imp.py` 33/0, `cron3c_test` 113/0, `cron3c_vp` 372/0, `cron3c_touch` 25/0, `map3b_test` 81/0, `xm_test` 53/0, `xm_close_test` 134/0, test Fase 4 (`f4*`) tutti 0 fallimenti.
- **Preesistenti, invariati:** in1/in2, `tva_test` A8/A9, r320 «home decor», `ui_audit` controlli della Home (14), g2.

## 6. Limiti residui
- **Safari/iPhone reale non verificato** (in particolare i punti 1 e 3: confermare che sparisca l'introduzione sotto la registrazione e l'area scura nel grafo).
- Zone di mezzo voto larghe 11–16 px (altezza 44 px): è la precisione intrinseca di un tocco su mezza stella; per la precisione assoluta servono tastiera/AT.
- A 320 px il blocco di voto estende il margine fino ai bordi della scheda perché lo spazio della scheda è già stretto.
- Gli altri overlay a schermo intero (Kang/TVA, Relazioni, Timeline Universi, Timeline alternativa) usano ancora lo stesso schema fixed+dvh del grafo classico: potrebbero soffrire dello stesso difetto su iPhone, non li ho modificati perché fuori dal perimetro richiesto.
- Le medie mostrano il punto decimale come prima («3.3»), non la virgola.
