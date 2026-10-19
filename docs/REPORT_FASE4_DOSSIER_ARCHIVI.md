# Fase 4 — Dossier e Archivi Marvel: report finale

Build: `20261019-1030-fase4-dossier` (base: `20261019-0900-xmen-chiusura`). Fase 5 non avviata.

## 1. Cosa è stato fatto (sprint A→D, nell'ordine deciso)
**A. Base `tvaXref` + ricerca.** Facciata di sola lettura (`tools/xref.js`) sopra i dati esistenti: opere, personaggi, attori, archivi, saghe, dipendenze. Ricerca tollerante a punteggiatura, accenti e varianti (S.H.I.E.L.D./shield, Jackman, x men/xmen, spiderman, realta/realtà, deadpool e/and wolverine), risultati divisi per tipo con filtri; 0 risultati persi rispetto alla vecchia ricerca (961 query confrontate).
**B. Dossier Opera** (`tools/dossier4.js`). Il chip N° negli Atlanti apre il Dossier Opera (D1). Da lì: «Scheda in guida» (apre la card originale della Timeline), Indietro coerente (pila + scorrimento), segna Visto/Non visto (D2) con **lo stesso click sulla casella della Timeline**: stessa persistenza, progressi, XP; nessuno stato parallelo. Tre assi sempre separati (guida / uscita / ambientazione), trama senza spoiler, personaggi, interpreti, saga, opere collegate, archivi, ponti verso Dossier universo / Mappa / Cronologie. Nessuna sezione o tab vuota.
**C. Dossier Personaggio adattivo + indice attori.** 49 attori indicizzati, filmografia in ordine di guida, link bidirezionali opera↔attore↔personaggio; sezione «Stesso individuo, secondo la guida» solo dai gruppi `identita` già presenti.
**D. Identità visiva e dossier secondari.** Skin per categoria sui 93 dossier archivio (organizzazioni, artefatti, eventi, luoghi, ecc.), barra salti, etichette fonte G/D/N, grafica di ripiego coerente con il design system (D6: nessun asset definitivo).
**D3.** `CANDIDATI_IDENTITA_D3.md/.csv`: 13 gruppi candidati (30 confronti, livelli dichiarato/forte/possibile/debole) + 8 «probabili distinti». Nessuna unificazione, nessun ID toccato, nessuna relazione inventata.
**D4.** Sezione «Titoli con il nome nel titolo» nei dossier organizzazione, etichettata come corrispondenza sul titolo (non apparizione né relazione narrativa); 30 titoli mostrati, solo non già confermati.

## 2. File
Nuovi: `tools/xref.js`, `tools/dossier4.js`, `tools/dossier4.css`, `tools/patch_dossier4.py`, `tools/build_4.sh`, `tools/d3_candidati.py`, `CANDIDATI_IDENTITA_D3.md/.csv`, test `f4a…f4e*`.
Modificati: `index.html`; `tools/atlas2.js` (hook `drawResults`, 4 funzioni in `EXT.api`), `tools/net_module.js` (`labels` in `tvaNavStato`), `tools/patch_fase1.py` (build id). In `index.html` un getter di sola lettura `marvelDipendenzeLettura`.
**Non modificati:** Home Marvel, Home TVA, logica Mappa 3B e Cronologie 3C (il loro click su un titolo apre ancora la card Timeline), ID, progressi, XP, badge, missioni, Firebase, Amici, Live Room.
Pipeline: `bash tools/build_4.sh` (verificata idempotente: stesso hash a ogni esecuzione).

## 3. Test eseguiti (Chromium, touch emulato)
- Nuovi: ricerca 21/0 · Dossier Opera 15/0 + tutti i 139 titoli e 37 anim 7/0 · personaggi (tutti i 304) 8/0 · attori 7/0 · dossier archivio (93) 9/0 · integrità/Indietro/viewport 20/0 (vedi sotto).
- **Sola lettura:** navigare in tutti i dossier, ricerche e funzioni D3 esegue 0 scritture su localStorage. Il Visto scrive solo le chiavi già usate dalla Timeline.
- **Indietro:** personaggio → opera → universo → opera → Indietro ×3 ripercorre il percorso e ripristina lo scorrimento; funziona anche il gesto Indietro del browser; il breadcrumb riflette la pila.
- **Viewport 320 / 375 / 390 / 393:** 95 schermate ciascuno, nessun overflow orizzontale, nessun errore JS; `prefers-reduced-motion` senza animazioni attive. Screenshot a 320 e 390 in `screenshot_fase4/` (20 file).
- Difetto trovato e corretto: chip con nota lunga (Avengers: Doomsday) usciva dalla colonna.
- **Regressione:** `d3a_test`, `a2_test`, `cons_test`, `net_test`, `tva_test`, `ui_audit` aggiornati solo nelle aspettative del flusso voluto da D1 (il N° ora porta al Dossier Opera, poi «Scheda in guida» alla card; un Indietro in più). Nessun controllo rimosso. `xm_*`, `g3`, `data_test`, cronologie 3C: invariati e verdi.

## 4. Fallimenti preesistenti (identici alla baseline X-Men, non causati dalla Fase 4)
in1/in2 (intro schermi piccoli), tva_test A8/A9, r320 «home decor» (3), ui_audit controlli della Home (14: testi <11px, hm-orb/hm-beam overflow, input 42px), g2 (tessera; supera il tempo limite del runner), d3.py instabile.

## 5. Limiti e punti aperti — da leggere
- **Prestazioni:** apertura dossier a CPU rallentata 4×: da pagina appena avviata ≈ 70–85 ms (mediana), il personaggio è più rapido della baseline 3C (p95 106 vs 127–141 ms). In una sessione di test con centinaia di navigazioni consecutive la mediana sale a ≈ 115–145 ms (Opera). L'obiettivo <100 ms non è dimostrato per tutti i casi: in questi test l'ho lasciato come misura, non come soglia. Non ho indagato la causa (probabile accumulo di pila/stato di navigazione).
- Link inline nel testo (`tva-lk`, `mv-inline-link`, ~30 px) sotto i 44 px: preesistenti, non cambiati.
- **Non verificati:** Safari su iPhone reale; Firebase/Live Room reali.
- Le relazioni D3 restano solo candidate: servono tue decisioni caso per caso.
