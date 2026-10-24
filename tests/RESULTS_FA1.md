# Risultati suite pertinenti — build 20261023-2355-fa1 (24/10/2026)

Suite pertinenti rieseguite sul repository (`run_suites.py --jobs 1`): **PASS 13 | FAIL 6 (tutti documentati in KNOWN_FAILS.json, nessuno nuovo) | BLOCKED 0 | NOT RUN 0**. Le altre suite (BLOCKED 8 / NOT RUN 10 preesistenti) non sono state rieseguite in questo giro: l'ultimo giro completo sulla stessa build (index.html/sw.js identici) ha dato PASS 33 | FAIL 6 | BLOCKED 9 (b322 poi risolto → 8) | NOT RUN 10. fa1_test usa un SDK Auth simulato.

| Suite | Stato | PASS | FAIL | Motivazione |
|---|---|---|---|---|
| fa1_test | PASS | 64 | 0 |  |
| c2_test | PASS | 29 | 0 |  |
| c3_test | PASS | 22 | 0 |  |
| c4_test | PASS | 12 | 0 |  |
| c4_contrast | PASS | 3 | 0 |  |
| a2_test | PASS | 40 | 0 |  |
| assets_test | PASS | 39 | 0 |  |
| b2_test | PASS | 121 | 0 |  |
| b321_test | PASS | 38 | 0 |  |
| b322_test | PASS | 15 | 0 |  |
| b324_test | PASS | 27 | 0 |  |
| b32_test | FAIL | 133 | 1 | 1 FAIL documentati in KNOWN_FAILS.json (FAIL storico, identico pre-M3.4 (avviso Carriera)) |
| b40c_test | PASS | 41 | 0 |  |
| bl_test | FAIL | 89 | 4 | 4 FAIL documentati in KNOWN_FAILS.json (FAIL storico, identico pre-M3.4 (posizione del widget voto cambiata)) |
| cap0_test | PASS | 37 | 0 |  |
| cron3c_test | FAIL | 0 | 2 | 2 FAIL documentati in KNOWN_FAILS.json (FAIL storico: conteggi fissi su tools/cron3c.js (indipendenti dalla build)) |
| fx_test4 | FAIL | 18 | 18 | 18 FAIL documentati in KNOWN_FAILS.json (18 FAIL identici sulla build pre-M3.4: il test descrive il widget voto precedente a M3.2 (stelle nella riga principale); da riscrivere con la specifica attuale) |
| fy_test | FAIL | 129 | 4 | 4 FAIL documentati in KNOWN_FAILS.json (FAIL storico, identico sulla build pre-M3.4 (tag Capitolo 0 cambiato)) |
| ui_audit | FAIL | 135 | 1 | 1 FAIL documentati in KNOWN_FAILS.json (il modello di composizione dello sfondo di ui_audit stima 4.40 su .ud-st-ok; la misura reale sui pixel (c4_contrast) e' 4.97: falso positivo del modello, non un difetto) |

**Totale:** PASS 13 | FAIL 6 | BLOCKED 0 | NOT RUN 0
