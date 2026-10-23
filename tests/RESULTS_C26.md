# Risultati suite — build 20261023-1520-c26

Esecuzione con `python3 tests/run_suites.py` (Chromium/Playwright, senza rete). Giro completo a 3 processi paralleli + riesecuzione in isolamento delle suite sensibili ai tempi (f4b, map3b, b324, m342, a2, b32, cons, net, nav, cop, f3, fx_test2, uf, ui_audit, fx_test4, bl). Dopo il giro l'unica modifica a `sw.js` e' la correzione C3b (HTML in cache solo se la build coincide); `c3_test` e le suite SW-sensibili (`b324`, `b321`, `c2`, `c4`, `m342`) sono state rieseguite dopo di essa. `index.html` invariato.

**Totale suite: 57 — BLOCKED 8 | FAIL 6 | NOT RUN 10 | PASS 33**  
Asserzioni: 1511 PASS, 32 FAIL (tutti i FAIL sono documentati in `tests/KNOWN_FAILS.json`: nessun FAIL nuovo).

| Suite | Stato | PASS | FAIL | Motivazione |
|---|---|---|---|---|
| c2_test | PASS | 29 | 0 |  |
| c3_test | PASS | 22 | 0 |  |
| c4_test | PASS | 12 | 0 |  |
| c4_contrast | PASS | 3 | 0 |  |
| tva_test | PASS | 0 | 0 |  |
| a2_test | PASS | 40 | 0 |  |
| assets_test | PASS | 39 | 0 |  |
| b2_test | PASS | 121 | 0 |  |
| b31_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: server aggiuntivo (porte 8125-8129: altra build/cartella di riferimento) |
| b321_test | PASS | 38 | 0 |  |
| b322_test | PASS | 15 | 0 |  |
| b324_test | PASS | 27 | 0 |  |
| b32_test | FAIL | 133 | 1 | 1 FAIL documentati in KNOWN_FAILS.json (FAIL storico, identico pre-M3.4 (avviso Carriera)) |
| b40c_test | PASS | 41 | 0 |  |
| b40e_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: server aggiuntivo (porte 8125-8129: altra build/cartella di riferimento) |
| bl_test | FAIL | 89 | 4 | 4 FAIL documentati in KNOWN_FAILS.json (FAIL storico, identico pre-M3.4 (posizione del widget voto cambiata)) |
| cap0_test | PASS | 37 | 0 |  |
| cons_test | BLOCKED | 40 | 1 | esecuzione interrotta: playwright._impl._errors.TimeoutError: Page.click: Timeout 10000ms exceeded. / causa: flusso obsoleto: dopo tvaGo(item) la barra .app-tab non e' visibile (shell immersiva); identico pre-M3.4 |
| cop_test | BLOCKED | 0 | 0 | esecuzione interrotta: playwright._impl._errors.Error: Page.evaluate: TypeError: Cannot read properties of null (reading 'scrollIntoView') / causa: selettore obsoleto: .a2-tiles (Home Atlante ridisegnata con .hm-p) |
| cron3c_test | FAIL | 0 | 2 | 2 FAIL documentati in KNOWN_FAILS.json (FAIL storico: conteggi fissi su tools/cron3c.js (indipendenti dalla build)) |
| d3a_img_test | PASS | 5 | 0 |  |
| d3a_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: build di riferimento index.3c.frozen.html |
| data_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: backup storico backups/N*.html |
| f2_test | PASS | 0 | 0 |  |
| f3_test | BLOCKED | 0 | 0 | esecuzione interrotta: playwright._impl._errors.Error: Page.evaluate: TypeError: Cannot read properties of null (reading 'click') / causa: selettore obsoleto: .a2-all (Home Atlante ridisegnata) |
| f4b_test | PASS | 16 | 0 |  |
| f4e_test | PASS | 13 | 0 |  |
| fx_test1 | PASS | 41 | 0 |  |
| fx_test2 | BLOCKED | 0 | 1 | esecuzione interrotta: playwright._impl._errors.Error: Page.evaluate: TypeError: Cannot read properties of null (reading 'getBoundingClientRect') / causa: selettore obsoleto: #homeHubMapBtn rimosso dalla Home (M3.4) |
| fx_test3 | PASS | 21 | 0 |  |
| fx_test4 | FAIL | 18 | 18 | 18 FAIL documentati in KNOWN_FAILS.json (18 FAIL identici sulla build pre-M3.4: il test descrive il widget voto precedente a M3.2 (stelle nella riga principale); da riscrivere con la specifica attuale) |
| fy_test | FAIL | 129 | 4 | 4 FAIL documentati in KNOWN_FAILS.json (FAIL storico, identico sulla build pre-M3.4 (tag Capitolo 0 cambiato)) |
| home2_test | PASS | 49 | 0 |  |
| leg_test | PASS | 37 | 0 |  |
| lm_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: backup storico backups/N*.html |
| m1_test | PASS | 14 | 0 |  |
| m21_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: build di riferimento index.pre_*.html |
| m2_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: build di riferimento index.pre_*.html |
| m31_test | PASS | 15 | 0 |  |
| m32_test | PASS | 33 | 0 |  |
| m341_test | PASS | 20 | 0 |  |
| m342_test | PASS | 15 | 0 |  |
| m34_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: server aggiuntivo (porte 8125-8129: altra build/cartella di riferimento) |
| m3_test | PASS | 16 | 0 |  |
| map3b_test | PASS | 81 | 0 |  |
| nav_test | BLOCKED | 28 | 0 | esecuzione interrotta: playwright._impl._errors.Error: Page.evaluate: TypeError: Cannot read properties of null (reading 'click') / causa: selettore obsoleto: label[for=multiverseGraphToggle].home-hub-btn rimosso dalla Home (M3.4: |
| net_test | BLOCKED | 12 | 0 | esecuzione interrotta: playwright._impl._errors.TimeoutError: ElementHandle.scroll_into_view_if_needed: Timeout 8000ms exceeded. / causa: selettore obsoleto: il link #char-peter-parker a.tva-lk[data-go=item:item-089] non e' piu' v |
| r320_test | PASS | 0 | 0 |  |
| rel_test | PASS | 35 | 0 |  |
| rs_test | PASS | 32 | 0 |  |
| stats_fix_test | PASS | 12 | 0 |  |
| tree_arti_test | PASS | 48 | 0 |  |
| uf_test | BLOCKED | 0 | 0 | esecuzione interrotta: playwright._impl._errors.TimeoutError: Page.click: Timeout 30000ms exceeded. / causa: selettore obsoleto/flusso: #mvUniversoBannerChiudi non cliccabile (banner non presente nel flusso) |
| uf_test_3b | BLOCKED | 0 | 0 | esecuzione interrotta: playwright._impl._errors.TimeoutError: Page.click: Timeout 30000ms exceeded. / causa: idem uf_test |
| ui_audit | FAIL | 135 | 1 | 1 FAIL documentati in KNOWN_FAILS.json (il modello di composizione dello sfondo di ui_audit stima 4.40 su .ud-st-ok; la misura reale sui pixel (c4_contrast) e' 4.97: falso positivo del modello, non un difetto) |
| xm_close_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: build di riferimento index.3c.frozen.html |
| xm_test | NOT RUN | 0 | 0 | dipendenza esterna non inclusa nel repo: build di riferimento index.3c.frozen.html |

*PASS = completata senza FAIL. FAIL = completata con FAIL (tutti documentati e identici alla build pre-M3.4 salvo dove indicato). BLOCKED = interrotta da selettore/flusso obsoleto o timeout, non attribuibile a un difetto dimostrato. NOT RUN = richiede build di riferimento o altri server non inclusi nel repository. `tva_test` stampa solo i FAIL: 0 FAIL su 390x844, 320x568, 844x390 con i blocchi J-Q eseguiti.*
