# FASE 3B — Mappa interattiva del Multiverso · Report

Build: `20261018-2100-multiverse-map` · Deploy: sostituire `index.html` (nessun nuovo asset obbligatorio). Rollback: `index.html` della 3A rev. 1 (`20261018-1930-uni-dossier`). **La 3C non è stata avviata.**

## 1. Cosa è stato realizzato
- **Nuova schermata «Mappa del Multiverso»** (scena SVG unica, layout fisso e curato dei 27 universi, nessuna simulazione a forze), costruita *solo* sul modello `tvaUniverse` della 3A: nessun dato, ID, collegamento o attribuzione aggiunto o modificato.
- **Linguaggio visivo**: sfondo nero/bordeaux con nebulose per famiglia (gradienti radiali, nessun filtro), polvere di stelle, anelli concentrici attorno all'MCU (fulcro) e alla TVA. Forma = tipologia (◉ continuità principale, ● autonomo, ◆ diramazione, quadrato tratteggiato raggruppamento, esagono luogo); colore dell'anello = famiglia; dimensione = n° titoli. Le nebulose sono dichiarate in legenda come raggruppamento visivo, non relazione.
- **Archi** dai 9 collegamenti del modello: pieno oro (Documentato nella guida), tratteggio lungo avorio (Legacy), puntinato cremisi (Da verificare). L'MCU non riceve archi non documentati.
- **Gesti**: pan a un dito, pinch, doppio tocco (×2), pulsanti ＋ − e «Adatta», rotella/tastiera su desktop. `touch-action:none` solo sull'area mappa; la pagina non scorre. Durante il gesto si aggiorna un solo `transform`.
- **Etichette**: abbreviate a vista d'insieme (es. «Raimi», «E-828»), nome completo quando l'ingrandimento lo consente e **sempre** per l'universo selezionato, in anteprima, elenco e dossier. Collisioni gestite (nessuna sovrapposizione fra etichette, né con comandi, né fuori area).
- **Ricerca** (nome, famiglia, titolo): centra, ingrandisce e seleziona; nell'Elenco filtra la lista.
- **Filtri**: affidabilità (3 stati), famiglia, tipologia, «solo universi con collegamenti», Azzera; indicatore di filtri attivi.
- **Anteprima dal basso** con dati reali (titoli, personaggi, progresso visione, collegamenti per stato con chip navigabili), «Apri il dossier» e «Solo i suoi collegamenti».
- **Ritorno dal dossier** (e dal grafo classico): selezione, zoom, posizione, filtri, modalità e ricerca preservati (stato incluso in `getState/setState`).
- **Elenco** completo: 27 righe per famiglia, stessi dati, ricerca e filtri condivisi; riga → dossier, pulsante → «mostra sulla mappa».
- **Legenda** sempre accessibile (stati con la precisazione che la concordanza non è verifica canonica indipendente, forme, famiglie, gesti).
- **Fuori mappa · 4**: pannello separato (Void luogo, Battleworld realtà speciale, Legacy isolati e Animazione raggruppamenti), «non rientrano nei 27»; Hulk 2003 marcato come appartenenza ambigua; «Evidenzia sulla mappa» con aloni puntinati (nessun arco creato).
- **Grafo classico**: accesso secondario da Legenda, Filtri, Elenco e dalla schermata Universi (invariato).
- **Fallback asset**: sfondo procedurale; se in futuro esiste `assets/images/tva/mappa_sfondo.webp` (1170×1600, ≤120 KB) viene adottato da solo (cache negativa, una sola richiesta).
- **Accessibilità**: nodi `role=button` con aria-label (nome completo, tipologia, famiglia, conteggi), annunci `aria-live`, tastiera (Tab/Invio/frecce/+/−/0/Esc), focus gestito nei pannelli, `prefers-reduced-motion` (nessun movimento animato), safe area per sheet e comandi.

## 2. Modifiche autorizzate fuori dalla mappa (circoscritte)
- Destinazione del portale Home TVA «Multiverso» → nuova mappa (`SEZ.multiverso` ora usa l'azione `map`). **Unico ritocco di testo**: il sottotitolo del portale era «Il grafo dei rami», ora «La mappa dei rami», per coerenza con la destinazione. Se preferisci l'etichetta precedente è una riga in `homev2.js`.
- Schermata Universi: il pulsante principale apre la mappa; «Grafo classico» è secondario. Catalogo: descrizione di «Multiverso» aggiornata.
- Invariati: intro, Home (layout), dossier 3A, dati/ID, progressi, XP, missioni, badge, Friends, Firebase, Live Room. Nei dossier **non** ho aggiunto «Apri sulla mappa» (avrebbe toccato i dossier 3A); si può aggiungere in seguito.

## 3. Test (Chromium/Playwright, touch emulato via CDP; **non** su iPhone reale)
- `map3b_test.py`: **81 controlli, 0 fallimenti** — 27 nodi = 27 universi; 9 archi = 9 relazioni con stato/stile corretti; speciali fuori mappa; gesti reali (pan, pinch, doppio tocco, zoom min/max, Adatta); selezione e attenuazione; anteprima ≤40% e nodo visibile; ricerca per nome/titolo; filtri; legenda; Fuori mappa e aloni; ritorno da dossier/grafo classico con stato; elenco con ricerca+filtri; tastiera; nessun click fantasma sotto il dito; nessuna chiave localStorage nuova (oltre la cache asset già esistente); nessun errore JS.
- `map3b_vp.py`: **211 controlli, 0 fallimenti** su 320×568, 320×480, 360×640, 375×667, 390×844, 430×932, 844×390, 1024×768 — nessun overflow, comandi ≥44 px, testi leggibili, etichette senza sovrapposizioni e dentro l'area, nodi interamente nell'area, anteprima con pulsante dossier sempre visibile, pannelli dentro lo schermo; reduced-motion.
- `map3b_perf.py`: con CPU 4× più lenta p50 16,7 ms / p95 16,8 ms in pan e pinch (2 frame lunghi su ~1000 alla fine del pinch, quando le etichette vengono ricalcolate); scena ~340 elementi, nessun `filter`/`backdrop-filter`.
- **Regressioni** (suite completa, confronto con la build precedente): passano d3a (0), d3a_img, home2 (15 portali, aspettativa «Multiverso → mappa» aggiornata), assets, stats_fix, rs_test (33/33), intro_scenes, nav_test (31/31, aggiornato: il Multiverso passa ora dalla mappa e dal grafo classico), rel/tree_arti, ios (0/288), rtd3, imp, enc, modes, links, final, tb2b, uf_test, a2_test, data_test, cons_test, f2_test, f2_links, lm_test. `c.py`: un fallimento non riproducibile in `reg.py`, pulito alla riesecuzione isolata (come già nella 3A).
- **Falliscono come prima della 3B** (test obsoleti dopo la Home della Fase 2, non aggiornati): in1/in2 (layout intro 320×480/568), tva_test A8/A9, r320_test «home decor», ui_audit sui controlli della Home, g2 (tessera per lettera), net_test e f3_test (si interrompono al primo click sulla vecchia Home).

## 4. Limiti dichiarati
- Verifica solo su Chromium con touch emulato: **Safari/iPhone da verificare da te** (gesti a due dita, rubber-band, safe area, riduzione movimento).
- A vista d'insieme in **landscape/viewport molto bassi** (es. 844×390, 320×480) i bersagli dei nodi si riducono per non sovrapporsi (~12–20 px): lì conviene ingrandire o usare Elenco/ricerca. Su portrait 320–430 i bersagli sono ≥44 px.
- A vista d'insieme non tutti i nodi hanno etichetta (collisioni): il nome è sempre disponibile con selezione, ricerca ed Elenco.
- Layout fisso: un nuovo universo aggiunto ai dati verrebbe collocato in una fascia di riserva sotto la mappa finché non gli si assegnano coordinate.
- Nessuna illustrazione prodotta (`mappa_sfondo.webp` opzionale, vedi brief 3A).
- Le coordinate sono un'impaginazione editoriale: la vicinanza sulla mappa non indica relazione canonica.

## 5. File
`index.html` · `TVA_Fase3B_deploy.zip` · sorgenti in `src3b/` (`map3b.js`, `map3b.css`, `patch_map3b.py`, `build_3b.sh`, test) · screenshot in `3b_screenshots/` (320 e 390: portale Home, mappa, selezione+anteprima, ricerca, zoom, legenda, filtri, mappa filtrata, Fuori mappa, Void evidenziato, Elenco; più `contact_320.png` / `contact_390.png`).
