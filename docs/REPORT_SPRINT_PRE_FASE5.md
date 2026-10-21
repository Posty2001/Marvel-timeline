# TVA Archives — Sprint di rifinitura pre-Fase 5

**Build ID:** `20261021-1630-pre5-rifinitura` (partenza: `20261019-1130-fix-ios-voti`)
Pipeline: `tools/build_4.sh` + nuovo `tools/patch_pre5.py` (idempotente: due build consecutive producono lo stesso md5).

## 1. Modifiche per area
**Atlante / navigazione.** Il tasto ATLANTE della barra inferiore apre sempre la schermata principale (`tvaAtlas2.openHome`). Indietro interno ai dossier invariato (stack di navigazione, ricerca/filtri preservati). Verificati HOME, TIMELINE, MISSIONI, TESSERA, FRIENDS: nessun overlay/dossier residuo.
**Timeline.** Intestazione compatta (279 px a 390/393; 292 px a 320), titolo «Marvel Ultimate Timeline», sottotitolo breve, 4 statistiche in riga, pulsante «Continua il percorso» (solo lettura: nessuna scrittura in localStorage), nota editoriale discreta «Include titoli annunciati fino a Secret Wars (dic 2027)». Rimossi «Scorri per iniziare» e il timbro gigante. Kicker spostato per non sovrapporsi all'hamburger, safe area rispettata.
**Capitolo 0.** I 5 contenuti restano integri; solo presentazione: spaziature ridotte, bordi più leggeri, righe da 44 px, etichetta «Lettura editoriale · nessun titolo da guardare», filetto oro antico a sinistra.
**Overlay iOS.** Kang/TVA, Relazioni, Timeline degli Universi, Timeline alternativa: stesso rimedio del Grafo classico (flusso normale, `position:static`, `transform:none`, `min-height:100dvh`, padding inferiore della barra azzerato). `.info-overlay` non toccato. Grafi, relazioni, dati e cronologie invariati.
**Voti.** Eliminate le zone da 11–16 px. Interazione a due passaggi: un tocco = voto intero, secondo tocco sulla stessa stella = k−0,5, terzo = torna a k. Stelle ≥ 22 px × 44 px, suggerimento «Tocca 2 volte per ½» finché non c'è un voto, valore numerico visibile, tastiera (frecce ±0,5, PgSu/Giù ±1, Home/Canc azzera, cifre), ARIA slider con step 0,5, live region. Chiavi, interi salvati, XP invariati.

## 2. Cause tecniche
- ATLANTE: il gestore della tab chiamava `onOpen()`, che ridisegna lo stato corrente (il dossier) senza tornare alla home.
- Overlay: `position:fixed` + `height:100dvh` + `transform/will-change` + contenuto più alto del viewport (confermato strutturalmente sui quattro, scrollHeight 1072–9561 px); è lo schema già documentato come causa dell'area scura su iOS.
- Intestazione: `min-height:100dvh` centrata + sigillo assoluto.
- Mezze stelle: aree di tocco larghe 11–16 px.

## 3. Test
- Nuovo `fy_test.py`: 133/133 (320, 375, 390, 393): flussi Atlante richiesti, cover ≤ 300 px, niente sovrapposizione hamburger, Continua senza scritture, Capitolo 0, quattro overlay (statici, nessun vuoto, fondo raggiungibile, niente overflow orizzontale), nessun errore JS.
- `fx_test4` (voti, aggiornato per l'interazione a due passaggi, cambiamento funzionale intenzionale): tutti PASS, 10 valori, persistenza, import, note intatte, reduced-motion, 320–430 px.
- Regressione completa: a2, an, assets, c, cons, cron3c (113/113), d3a, g, g3, home2, imp, inc, leg, lm, map3b (81/81), min2, nav, net, r, rel, rs, stats_fix, t, tree_arti, xm (53), xm_close (134), xm_extra: tutti senza fallimenti. X-Men: ordine invariato.
- `data_test`: 1 fallimento iniziale causato solo dal testo del nuovo suggerimento del widget; aggiornato il normalizzatore (modifica funzionale intenzionale), poi 0 fallimenti. Nessuna aspettativa sui contenuti modificata.

## 4. Problemi preesistenti ancora aperti (identici alla baseline)
in1/in2, tva_test A8/A9, r320 (3), ui_audit controlli Home (14), g2 (1; nell'ultimo rilancio isolato è andato in timeout). Non toccati e non risolti.

## 5. Limiti non verificabili
Chromium con touch emulato **non equivale a Safari reale**: i difetti iOS (area scura, dvh, transform) non sono riproducibili qui; il rimedio deriva dall'analisi del codice e dal bug iOS già documentato. Serve conferma su iPhone reale (rotazione, barra Safari dinamica, safe area). Il tempo di apertura dossier sotto uso prolungato non è dimostrato. Service worker ancora a `marvel-timeline-cache-v8` (non incrementato).

## 6. Prontezza per la Fase 5
Pronti con riserva: navigazione, intestazione, overlay e voti sono coperti da test automatici senza nuove regressioni e senza modifiche a dati, ID, ordine titoli, Firebase/XP/PWA. Prima di procedere consiglio: (1) un controllo rapido su un iPhone reale dei quattro overlay, della Timeline e dei voti; (2) decidere se incrementare la cache del service worker a v9; (3) valutare se sistemare i fallimenti preesistenti per avere una baseline pulita.
