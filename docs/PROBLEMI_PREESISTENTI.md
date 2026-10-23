# Problemi preesistenti nei test (registrati, non nascosti)

Aggiornato il 2026-10-23, build `20261023-1520-c26`. Esito completo: `tests/RESULTS_C26.md`. Nessun test è stato modificato per ottenere PASS: dove i selettori/aspettative erano obsoleti, l'aggiornamento è motivato nel codice (commenti `C5`) e nel Registro Master §E4.

## Risolti (classificati come aspettative obsolete, nessun difetto applicativo)
Gli otto controlli storici di `tva_test` (`G arti n schede`, `G multiverso/reliquiario atlante chiuso`, `H cronologie righe 15!=10`, `H cronologie[0..2] apre sezione`, `H cronologie[6] ritorno`), l'interruzione al blocco J (`.a2-feat` rimosso) e i tre FAIL `K ricerca gemme`, `K char apre scheda`, `L scheda personaggio` sono stati analizzati e aggiornati: `tva_test` ha ora **0 FAIL** su 390×844, 320×568 e 844×390, con i blocchi J–Q eseguiti.

## FAIL ancora presenti (documentati in `tests/KNOWN_FAILS.json`; identici sulla build pre-M3.4)
| Suite | Controlli | Natura |
|---|---|---|
| `fx_test4` | 18 (R1, R2 ×9, R6, R15 ×6) | descrive il widget voto precedente a M3.2 |
| `bl_test` | 4 (stelle sotto il titolo) | idem |
| `fy_test` | 4 (`cap0 tag`) | tag Capitolo 0 cambiato |
| `b32_test` | 1 (`K2a Carriera`) | avviso Carriera, comportamento cambiato |
| `cron3c_test` | 2 (MCU 64 con anno, ordine monotono) | conteggi fissi su `tools/cron3c.js` |
| `ui_audit` | 1 (contrasto `.ud-st-ok` 4,40) | falso positivo del modello di composizione dello sfondo: misura reale sui pixel 4,97 (`c4_contrast`) |
| `cons_test` | 1 (`Back 2` scorrimento) + interruzione | flusso obsoleto (barra non visibile nella shell) |

## BLOCKED (interrotte da selettori/flussi obsoleti)
`cons_test`, `net_test`, `nav_test` (28 controlli PASS prima di `label[for=multiverseGraphToggle].home-hub-btn`, rimosso con la Home M3.4), `fx_test2` (`#homeHubMapBtn` rimosso), `cop_test` (`.a2-tiles`), `f3_test` (`.a2-all`), `uf_test`, `uf_test_3b` (`#mvUniversoBannerChiudi`).

## NOT RUN (dipendenze non incluse nel repository)
`b31_test`, `b40e_test`, `d3a_test`, `data_test`, `lm_test`, `m21_test`, `m2_test`, `m34_test`, `xm_close_test`, `xm_test`: richiedono build di riferimento (`index.3c.frozen.html`, `index.pre_*.html`, `backups/N*.html`) o server aggiuntivi.

## Altri
- Il falso positivo di contrasto indicato in passato («5,4 e 6,7:1» su `.ud-st`) non è riproducibile ed è sostituito dalla misura sui pixel (E3): era davvero insufficiente solo `.ud-st-vf` (4,10), ora corretto (5,31).
- Suite sensibili ai tempi (`f4b_test`, `map3b_test`): possibili falsi FAIL con esecuzione parallela.
