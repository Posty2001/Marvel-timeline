# FASE 3A — Dati condivisi e dossier degli universi · Report (rev. 1)

**Rev. 1 (correzioni richieste):** lo stato «Confermato» è ora **«Documentato nella guida»** (Atlante e grafo storico derivano entrambi dalla guida: la concordanza non è una verifica canonica indipendente; testo di legenda e motivazioni aggiornati, fonti conservate). «Legacy isolati» distingue i **4 membri elencati esplicitamente** (Blade, Daredevil/Elektra, Ghost Rider, Spider-Noir) da **Hulk (2003)**, la cui appartenenza è ambigua e dichiarata come tale nel suo dossier; nessun universo cancellato o modificato. Test 3A: 0 fallimenti (aggiunti: etichetta, 4+1 membri, Hulk).

Build: `20261018-1930-uni-dossier`. Fermo qui, come richiesto: **mappa 3B e cronologie 3C non sono state avviate**; il portale «Multiverso» della Home punta ancora al grafo classico.

## 1. Cosa è stato fatto
1. **Modello dati condiviso `tvaUniverse`** (`tools/universe_model.js`, sola lettura). Non copia dati: legge `mvMapData`, `atlasData`, l'indice `tvaIdx` e gli archi del grafo storico dell'overlay Multiverso, e li riconcilia. Espone i 27 universi (titoli per appartenenza/crossover/varianti, personaggi di origine/presenti, eventi dichiarati, collegamenti con stato e provenienza, famiglie, raggruppamenti) e un `audit()` usato dai test.
2. **Normalizzazione non distruttiva dei collegamenti**: le due sorgenti restano intatte (verificato byte-per-byte); ogni relazione conserva le fonti originali (Atlante / grafo storico, tipo d'arco, N° dei titoli) e il motivo dello stato.
3. **Elementi speciali** (Void, Battleworld, Legacy isolati, Animazione): classificati a parte (luogo · realtà speciale · 2 raggruppamenti editoriali), **non contati fra i 27**, restano nella vista classica. I loro archi non sono stati trasformati in relazioni fra universi.
4. **Dossier immersivo** per i 27 universi (`renderUni`), costruito solo sul modello. Moduli presenti solo se hanno dati; il resto è dichiarato in un riquadro «Non documentato».
5. **Brief** per le 7 ambientazioni di famiglia + sfondo mappa opzionale (`BRIEF_ASSET_DOSSIER_UNIVERSI_TVA.md`), `prepara_asset.py` esteso (`--set uni|all`).

## 2. Criterio dei tre stati (documentato anche nel codice e nella legenda in app)
| Stato | Regola |
|---|---|
| **Documentato nella guida** (ex Confermato) | Riferimento narrativo verificabile: almeno un titolo (N°) citato da **due fonti indipendenti** — le opere dell'Atlante che assegnano il titolo a entrambi gli universi **e** un arco «crossover/cameo» del grafo storico che cita lo stesso N° — senza contraddizioni. |
| **Legacy** | Presente nel grafo storico (crossover/cameo) con N° esistente; l'Atlante non lo riscontra né lo contraddice. Non verificato. |
| **Da verificare** | Dati ambigui, contraddittori o insufficienti: (a) arco «previsto, non ancora mostrato»; (b) arco «crossover» il cui N° l'Atlante assegna ad altri universi; (c) coppia presente **solo** nei dati dell'Atlante (la sola presenza nel database non è conferma canonica). |

Esito sui dati reali (9 relazioni fra universi + 4 elementi speciali):

| Relazione | Stato | Motivo (visibile in app, «Provenienza e motivo») |
|---|---|---|
| MCU – Raimi-Verse (N°099) | Confermato | N°099 in entrambe le fonti |
| MCU – Garfield-Verse (N°099) | Confermato | idem |
| MCU – Fox-Verse (N°117) | Confermato | N°117 in entrambe le fonti |
| MCU – TVA (N°095, N°112) | Confermato | in entrambe le fonti |
| MCU – SSU (cameo, N°007/099) | Legacy | solo grafo storico; l'Atlante non lo riscontra né lo contraddice |
| MCU – Earth-828 (N°125/136) | Da verificare | grafo: «previsto»; Atlante: titolo condiviso N°125 → fonti in disaccordo |
| MCU – Earth-838 (N°102) | Da verificare | il grafo indica crossover, ma l'Atlante assegna il N°102 al solo MCU |
| MCU – Rami di What If…? (N°096/114/119) | Da verificare | solo Atlante; manca il riscontro nel grafo storico |
| Raimi – Garfield (N°099) | Da verificare | solo Atlante (derivata dal titolo a tre universi; non è nel grafo storico) |
| Void ↔ MCU/Fox/Legacy (N°117) | Legacy | solo grafo storico (elemento speciale) |
| Battleworld (N°139) | Da verificare | «previsto, non ancora mostrato» |
| Legacy isolati ↔ MCU/Fox (cameo, N°117) | Legacy | solo grafo storico (raggruppamento) |

Totale universi: **4 confermati · 1 legacy · 4 da verificare**. Nessun collegamento dubbio è mostrato come confermato (test automatico).

**Decisioni che ho preso e che puoi rivedere** (tutte reversibili modificando una regola):
- «What If» e Raimi–Garfield finiscono in *Da verificare* perché sono solo nei dati dell'Atlante: segue alla lettera «la sola presenza nel database non è conferma». Se vuoi considerare confermato un titolo che il database assegna a due universi, basta cambiare la regola (c).
- L'appartenenza dei membri a «Legacy isolati» è ambigua nella fonte (la nota elenca 4 universi, la descrizione aggiunge Hulk 2003): ho incluso 5 membri e **lo dichiaro nel dossier**. Per «Animazione» il nodo non elenca i membri: uso la famiglia editoriale di `mvMapData` (9 universi) e lo dichiaro.

## 3. Dossier — struttura (mobile 390×844)
Hero (illustrazione di famiglia se presente, altrimenti ambiente procedurale), famiglia + natura, descrizione e note dalla guida, **4 statistiche reali** (zeri omessi) → indice moduli sticky → progresso → **Titoli** con 3 ordini (Ordine della guida · Per data di uscita · Per ambientazione; ogni ordine compare solo se ≥2 titoli hanno il dato; i titoli senza dato vanno in coda con nota; le date approssimative sono segnalate) → Crossover → Varianti → Personaggi (origine / presenti) → Eventi chiave (solo quelli dichiarati) → Archivi derivati → **Collegamenti** (stato, tipo, titoli di riferimento cliccabili, provenienza, motivo; luoghi e realtà speciali separati) → Raggruppamenti e famiglia (affinità editoriale dichiarata *non* narrativa) → «Non documentato».
Navigazione: collegamento → altro dossier; titolo → scheda; personaggio → scheda; «Mostra solo questi titoli in Timeline»; «Apri le Cronologie»; «Apri il grafo classico». Ogni passaggio usa lo stack esistente: Indietro riporta al dossier.
Moduli presenti nei 27 dossier: titoli 22 · personaggi 22 · collegamenti 9 · crossover 7 · archivi 7 · varianti 1 · eventi 1 (solo l'MCU ha eventi dichiarati: negli altri 26 **non ne sono stati inventati**) · famiglia 24.

## 4. Test (Chromium/Playwright, touch emulato; **non** su iPhone reale)
- `d3a_test.py` — integrità: `mvMapData`, `atlasData`, `relationshipGraphData`, `altTimelineData` **identici byte-per-byte** alla build precedente; 1297 occorrenze `mvNavigate`, `card-wrap`, 3 toggle overlay e HTML del grafo storico invariati; 27 universi; 13/13 archi del grafo mappati; 12 nodi; aspettative esplicite sullo stato di ciascuna relazione; speciali fuori dai 27; nei 27 dossier: titolo = nome, collegamenti resi = modello, righe titoli = dati, nessuna sezione vuota, indice = sezioni, nessun universo condiviso nei titoli perso dai collegamenti; navigazione avanti/indietro (altro universo, titolo, personaggio, Timeline filtrata, Cronologie, grafo classico); i 3 ordini monotoni e con gli stessi titoli; 3 overlay legacy ancora apribili; overflow orizzontale 0 a 320/360/390/430 px con `prefers-reduced-motion`. **0 fallimenti.**
- `d3a_img_test.py` — slot illustrazione: senza file → ambiente procedurale; con file (finto, solo test) → caricato da solo; nessun errore; **una sola richiesta per asset mancante** (cache negativa).
- Copertura dei contenuti classici (`uni_par.py`): tutte le righe originali delle 27 schede sono nel dossier; differiscono solo due righe *generate* della scheda classica (conteggi/collegamenti), riformulate.
- Regressioni: vedi §5.

## 5. Regressioni
Eseguite sulla build finale, in sequenza; per ogni fallimento ho confrontato con la build precedente (`20261018-1800-home-assets`).

**Passano:** home2 (15 portali) · assets · stats_fix · rs_test (33/33) · intro_scenes · nav_test (29/29) · ios (0 fallimenti su 288) · perf (scorrimento p95 16,8 ms con CPU 4× più lenta) · rtd3 · imp (33) · enc (19) · modes (15) · links (13) · final (10) · tb2b · uf_test · data_test · f2_test · f2_links · lm_test · a2_test · cons_test · ui_audit sui dossier (MCU, E-828, Raimi, 6 viewport incl. landscape e safe area).

**Corretti perché la 3A li aveva toccati (non nascosti):**
- `a2_test` pretendeva un paragrafo di stato vuoto nei dossier senza titoli → ora «Non documentato» usa la stessa classe `a2-empty`.
- `ui_audit`: testi <11 px e strip dell'indice trattata come overflow → font ≥11,5 px e la strip usa la classe di scorrimento orizzontale già prevista (`a2-jump`).
- `cons_test` segnalava la chiave `tvaHomeMiss:<build>` (cache degli asset opzionali assenti, già introdotta nella Fase 2) come scrittura in localStorage: l'apertura di un dossier la crea al primo mancato asset. **Nessuna chiave di progresso, XP, badge, filtri o ordine personalizzato viene scritta**; ho escluso solo questa chiave dal confronto e lo dichiaro qui.

**Falliscono identicamente sulla build precedente (già presenti, non causati dalla 3A; test obsoleti dopo la Home della Fase 2, non aggiornati):** `in1`/`in2` (layout intro a 320×480/568: Atto I non entra senza scroll — anche prima), `tva_test` A8/A9, `r320_test` «home decor», `ui_audit` sui controlli della **Home** (testi <11 px, overflow decorativo `hm-beam`), `g2` (tessera: apertura per lettera), `net_test` e `f3_test` (si interrompono al primo click perché cercano elementi della vecchia Home). Li lascio da riallineare in un intervento dedicato; non li ho considerati «passati».
Una singola esecuzione di `c.py` (profili casuali del picker) ha dato un fallimento non riproducibile: 5 riesecuzioni successive, anche dentro `reg.py`, sono pulite.

## 6. Limiti dichiarati
- Nessuna illustrazione prodotta: **sono bloccati solo i brief, non il codice**. Gli ambienti di famiglia procedurali sono un fallback onesto (SVG ~1 KB), non asset finali.
- Verifica solo su Chromium con touch emulato: **la verifica su iPhone/Safari è tua** (sticky dell'indice, scorrimento, riduzione movimento).
- Le date di ambientazione sono ricavate dal testo libero della guida (periodi, «anni '90», a.C.) e marcate come approssimative; i titoli senza data stanno in coda. L'ordinamento per ambientazione nelle Cronologie (3C) userà la stessa funzione.
- La classificazione di Void/Battleworld come «luogo» / «realtà speciale» è editoriale (la guida non le classifica); è dichiarata come tale.

## 7. File
`index.html` (build `20261018-1930-uni-dossier`) · sorgenti: `tools/universe_model.js`, `tools/dossier.js`, `tools/dossier.css`, `tools/patch_dossier.py`, `tools/inject_net.py` · screenshot `fase3a_01…11` · `BRIEF_ASSET_DOSSIER_UNIVERSI_TVA.md` · `asset_tools/prepara_asset.py`.
Deploy: sostituire `index.html` (nessun nuovo asset richiesto). Rollback: ripristinare l'`index.html` della build `20261018-1800-home-assets`.
