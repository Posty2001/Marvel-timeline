# TVA Archives — Blocco 2.1: rifinitura navigazione Centrale TVA
**Build ID:** `20261021-2040-blocco2-1` (base `20261021-2000-blocco2`). Nessun push/deploy. Blocco 3 non avviato. In attesa di approvazione.

## Modifiche
- Ordine delle sezioni: **PANORAMICA · MISSIONI · OSSERVATORIO · OPERAZIONI**.
- «Strumenti» rinominata **Osservatorio** (etichetta, scorciatoia in Panoramica, sottotitolo) e spostata in 3ª posizione; **Operazioni** in 4ª. Anche l'ordine dei pannelli nel DOM e la navigazione a frecce seguono il nuovo ordine.
- Icona 🧰 sostituita da un'icona **radar** SVG inline (cerchi concentrici, sweep, blip; colore oro, stessa dimensione delle altre icone; `aria-hidden`).
- Contenuto dell'Osservatorio e di Operazioni invariato (stessi nodi, id, algoritmi, conferme).
- ID interni e ancore conservati (`cenTab-strumenti`, `cenPan-strumenti`, `#cen-strumenti`); aggiunto l'alias `#cen-osservatorio`.
- Etichette dei tab ridotte leggermente a 320 px (8 px) perché «OSSERVATORIO» non venisse tagliata.
- File: `tools/b2.js`, `tools/b2.css`, `tools/patch_fase1.py` (build id). Build idempotente (md5 stabile).

## Test (Chromium con emulazione touch — **NON Safari iPhone reale**; nessun test su dispositivo reale)
- `b2_test.py`: **121/121** (incluse le nuove verifiche: ordine/etichette, icona radar, scorciatoie, alias hash, Indietro, ripristino sezione, layout 320/375/390/393 senza overflow né etichette tagliate, controlli ≥44px).
- Regressione (25 script): 0 fallimenti nuovi. Preesistenti identici alla baseline: `tva_test` A8/A9, `ui_audit` Home (14), `r320` «home decor» (3). `map3b`/`cron3c` danno 0/0 con questo runner (come prima).
- `rs_test`/`stats_fix_test`: solo nuovo build id.

## Residui
- Non verificato su Safari reale; il testo dei tab a 320 px è piccolo (8 px).
- «Osservatorio» e 🎯 Missioni sono entrambe cerchi concentrici: distinguibili per lo sweep del radar, valutare se preferisci un glifo più diverso.
- Sei dei 9 checkpoint puntano ancora a `#parte3` (link originali).

## Screenshot
`screenshot_blocco2_1/{320,375,390,393}_{panoramica,missioni,strumenti,operazioni}.png` (strumenti = Osservatorio).
