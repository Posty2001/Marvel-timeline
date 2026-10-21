# TVA Archives — Blocco 1
**Build ID:** `20261021-1900-blocco1` (da `20261021-1630-pre5-rifinitura`). Nessun push eseguito.

## 1. Modifiche
- **Navigazione:** barra a 6 voci, «Missioni» → «CENTRALE TVA» (due righe, `aria-label="Centrale TVA"`); id e `data-tab` invariati. Atlante, Friends e Indietro non toccati.
- **Timeline / Centrale (viste CSS, nulla rimosso dal DOM):** Timeline mostra copertina, indice, legenda, controlli e i capitoli. Dashboard, database, bollettino, footer ingombrante e «fascicolo chiuso» sono nascosti. La Centrale TVA mostra gli strumenti esistenti: bollettino, controlli (progresso, filtri, backup/sync/reset), dashboard con missioni e database. Link `#dashboard`/`#database`, ricerca e scroll verso titoli cambiano vista automaticamente. Indice compatto e subito sotto la copertina, Capitolo 0 e legenda più compatti.
- **Card:** stelle (10 valori, due tocchi, azzera discreto) come primo elemento sotto il titolo, senza riquadro; l'etichetta resta solo per screen reader. Spaziature ridotte tra Universo/Ambientazione/Durata/Personaggi; Trama/Curiosità/Dietro le quinte/Collegamenti ancora espandibili. Titoli dei gruppi: nome e identificativo universo vanno su due righe solo se manca spazio.
- **Grafi:** Relazioni con etichette più grandi (min 4,5→6,4 px a 390), vista ritagliata sul contenuto (altezza da 422 a 239 px), nodi più grandi; Kang/TVA con etichette staccate dai nodi. Zoom/trascinamento invariati, grafi non ricostruiti.

## 2. Test
- `bl_test` (nuovo, 320/375/390/393): 92/92. `fy_test` 133/133. `fx_test4` 36/36. `fx_test1-3`, `rel_test` (35, nessuna sovrapposizione etichette), `nav`, `a2`, `home2`, `cons`, `net`, `rs`, `stats_fix`, `lm`, `imp`, `data_test`, `xm` (53), `xm_close` (134), `map3b`, `cron3c`, `tree_arti`, `leg`: tutti senza fallimenti.
- Aggiornamenti di test motivati: `fx_test4` R1 (widget ora primo elemento del pannello, cambio voluto); R3 esclude 2 px intorno alla linea di taglio (antialias della punta della stella; il rendering è corretto, verificato a vista); `rs_test`/`stats_fix_test` build ID; `data_test` normalizza il testo del widget.
- Controlli sintattici JS e build idempotente (stesso md5) OK.

## 3. Problemi rimasti (preesistenti, invariati)
in1/in2, tva_test A8/A9, r320 «home decor» (3), ui_audit Home (14), g2.

## 4. Rischi
- Non verificato su Safari reale (solo Chromium con touch emulato).
- La vista è un attributo CSS su `<html>`: una navigazione futura che mostri sezioni nascoste senza `scrollIntoView` o tab/link andrà agganciata a `data-tva-view`.
- Etichette dei satelliti Relazioni troncate a 24 caratteri (testo completo in aria-label/tooltip/pannello).
- Barra inferiore leggermente più alta per «CENTRALE TVA» su due righe; il service worker non è stato incrementato (cache v8).
