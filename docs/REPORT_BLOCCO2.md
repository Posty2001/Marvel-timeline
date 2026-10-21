# TVA Archives — Blocco 2: Centrale TVA, Missioni, Operazioni e Strumenti
**Build ID:** `20261021-2000-blocco2` (base `20261021-1900-blocco1`). Nessun push eseguito. Blocco 3 non avviato.

## Completato
- **Centrale TVA in 4 sezioni on-demand** (tablist accessibile, frecce da tastiera, contesto e scroll conservati per sezione; barra inferiore invariata):
  - **Panoramica**: agente/grado/livello/XP (letti dalla Tessera reale, nessuna seconda Tessera), progresso, prossimo titolo con link alla scheda, anteprima 4 missioni + stagione, scorciatoie.
  - **Missioni** → Attive / Stagioni / Speciali / Archivio. Dossier apribile per ogni missione (descrizione, requisiti, stato, ricompensa, scadenza reale = domenica ISO, opere con link). Stagioni: «La Guerra delle Incursioni» 0/10, +500 XP e titolo. Speciali: Road to Doomsday 0/16, +300 XP, distinzione watchlist ufficiale / classificazioni editoriali. Archivio in sola lettura dal registro ricompense (nessuna voce duplicata). Missione segreta: nessun titolo rivelato.
  - **Operazioni**: segna tutti visti/non visti (nuova conferma solo per «non visti»), reset progresso e reset totale (conferme originali, in «Zona pericolosa»), backup/ripristino, sincronizzazione, modalità scura.
  - **Strumenti**: «Cosa guardo stasera?», statistiche dettagliate, Modalità Confronto (usabilità mobile corretta: niente tabella orizzontale, selettori 16px/44px).
- **Timeline ripulita**: senza reset/segna tutti/confronto/statistiche/backup/sync; «Timeline Riassuntiva» ridotta a un indice compatto dei 9 checkpoint (una sola volta, solo in Timeline, subito dopo l'indice capitoli).
- **Navigazione**: Indietro ripristina sezione, sotto-sezione e dossier aperti; ancore `#cen-*`; `openMission(key)`; `scrollIntoView` e ricerca commutano la vista; link Atlante → Atlante esistente.
- Predisposizione Blocco 3: solo `tvaCentrale.getState/setState` e dati missione in sola lettura (`marvelMissioniInfo`, evento `tva:missioni2`). Nessun nuovo XP/contatore.

## Preservato
138 opere + variante, Capitolo 0 (5), serie animate, ID/ordine/classificazioni, voti, preferiti, XP (30/20, retroattivi), missioni, stagioni, RTD, Atlante, Friends, Live Room, Firebase/sync. Registro ricompense e chiavi localStorage invariati; la sola navigazione non scrive in localStorage (test D1).

## Test (Chromium con emulazione touch — **NON Safari reale**)
- `b2_test.py` (nuovo): **117/117**: navigazione 4 sezioni, apertura/ritorno titoli (Indietro), missioni/stagione/RTD, nessun XP duplicato e persistenza dopo reload, operazioni con conferme, unicità id/componenti, Timeline senza strumenti admin, 9 checkpoint, layout 320/375/390/393 (no overflow, controlli ≥44px, confronto), nessun errore JS.
- Regressione: bl, fy, fx1-4, rel, nav, a2, home2, cons, net, rs, stats_fix, lm, imp, data, xm, xm_close, tree_arti, leg → **0 fallimenti**.
- **Fallimenti preesistenti (identici alla baseline, non regressioni)**: tva_test A8/A9, ui_audit Home (14), r320 «home decor» (3). map3b/cron3c riportano 0 pass/0 fail con questo runner (come prima).
- **Modifiche intenzionali ai test**: `bl_test` (2 asserzioni × 4 viewport): la Centrale non mostra più `.controlbar` né il database/Atlante; strumenti ora in Operazioni. `rs_test`/`stats_fix_test`: nuovo build id.
- Nota: in un test il XP differiva di 5 dopo reload solo se un voto veniva scritto direttamente in localStorage; riprodotto identico sulla baseline Blocco 1 (non dipende da Blocco 2).

## Problemi residui / note
- 6 dei 9 checkpoint puntano ancora allo stesso `#parte3` (collegamenti originali mantenuti come richiesto).
- Non verificato su Safari/iPhone reale.
- ui_audit/Home: problemi preesistenti (testo <11px, overflow decorativi) non toccati.

## PWA
Service worker **network-first** per l'HTML: nessun bump necessario (resta `marvel-timeline-cache-v8`).

## File modificati
`index.html` (generato), `tools/patch_b2.py`, `tools/b2.js`, `tools/b2.css` (nuovi), `tools/b1.css`, `tools/b1.js`, `tools/patch_fase1.py`, `tools/build_4.sh`. Build idempotente (md5 stabile su build ripetute).
