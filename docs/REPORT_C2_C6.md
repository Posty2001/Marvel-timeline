# TVA Archives — Rapporto consolidamento C2–C6
**Build:** `20261023-1520-c26` · base `32a570b` (M3.4.2) · **solo locale: nessun commit, push o deploy** · nessuna modifica a Firebase, regole, credenziali, dati remoti, catalogo Marvel, progressi/voti/XP/ricompense · nessuna funzionalità TVA Friends.
`index.html` md5 `73ed07167ca5c197fd01c2346f597d99` · `sw.js` md5 `b76146704ba055d64aad183b9307c31c` (include la correzione C3b).
Verifica iPhone M3.4.2: **6/6 PASS (dichiarata dall'utente)**, registrata nel Registro Master §E; non copre la build c26.

## File modificati
| File | Modifica |
|---|---|
| `index.html` | C2: Reset totale rimuove anche la modalità Timeline locale; `custom` con ordine vuoto riapre su «Consigliato»; commento su `preferredMode`. C4: `.ud-st-vf` contrasto; CSP `<meta>`; menu laterale chiuso fuori dal focus + tastiera (Invio/Spazio/Esc, `aria-expanded`). Build id |
| `sw.js` | C3: build e cache legate alla build; pulizia solo cache `marvel-timeline-cache-*`; precache pagina solo se la build coincide (C3b); navigazione offline ignora la query |
| `tools/patch_c26.py`, `tools/build_4.sh` | patch idempotente (doppia esecuzione = stesso md5) agganciata alla catena |
| `tests/` | nuovi: `run_suites.py`, `SUITES.json`, `KNOWN_FAILS.json`, `RESULTS_C26.md`, `c2_test`, `c3_test`, `c4_test`, `c4_contrast`; aggiornati: `tva_test` (J–Q), `a2_test`, `b324_test`; incluse le librerie e le suite storiche eseguite |
| `docs/`, `README.md` | Registro Master (§E, note «→ E» sulle righe superate), `PROBLEMI_PREESISTENTI.md`, README, questo rapporto |

## Problemi risolti
| Fase | Problema | Evidenza |
|---|---|---|
| C2 | «Cancella tutto» lasciava la modalità `custom` senza ordine | `c2_test` 29/29 |
| C2 | `custom` + ordine vuoto: Timeline in «Personalizzato», Home in standard | idem |
| C3 | Cache fissa `v9`, cancellazione di tutte le altre cache, pagina fuori dalla precache | `c3_test` 22/22 (SW reale: install, update, offline, ritorno online, deploy a metà; dati intatti) |
| C4 | `.ud-st-vf` 4,10:1 (pixel, 27 universi) → 5,31:1 | `c4_contrast` |
| C4 | Menu chiuso nell'ordine Tab (link fuori schermo); pulsanti menu non azionabili da tastiera | `c4_test` 12/12 |
| C4 | Nessuna CSP | CSP attiva, 0 violazioni nei flussi, script esterno bloccato |
| C5 | `tva_test` interrotto al blocco J | 0 FAIL su 3 viewport, blocchi J–Q eseguiti |
| C5 | 8 FAIL storici + 3 K/L: tutti aspettative/selettori obsoleti (comportamento reale riprodotto), aggiornati con motivazione; nessuna aspettativa valida toccata | tabella in Registro §E4 |
| C5 | Esecuzione non riproducibile (porte, percorsi, build fissate) | `tests/run_suites.py` |

## Contrasto `.ud-st` — riconciliazione
Misura sui pixel: `ok` 4,97 (PASS), `lg` 11,98, `vf` 4,10 (insufficiente, corretto). `ui_audit` dà 4,40 su `ok` per il suo modello di composizione: falso positivo, documentato. Le misure «5,4 / 6,7» del giro precedente non sono riproducibili e sono superate.

## Sicurezza: implementato vs raccomandato
| Implementato | Solo raccomandato |
|---|---|
| CSP con origini limitate (script, stile, font, immagini TMDB, connect Firebase), `object-src 'none'`, `base-uri`, `form-action`; menu fuori dal focus | CSP senza `unsafe-inline` (nonce/hash: refactoring); SRI sui 2 script Firebase (hash non calcolabile da qui, rete bloccata); `frame-ancestors`/header HTTP (non disponibili su Pages); audit VoiceOver |

## Test eseguiti (`tests/RESULTS_C26.md`)
57 suite: **PASS 33 · FAIL 6 · BLOCKED 8 · NOT RUN 10**; 1511 asserzioni PASS, 32 FAIL, tutti documentati e identici alla build pre-M3.4 (nessun FAIL nuovo).
FAIL (documentati): `fx_test4` 18, `bl_test` 4, `fy_test` 4, `cron3c_test` 2, `b32_test` 1, `ui_audit` 1. BLOCKED (selettori/flussi obsoleti): `cons`, `net`, `nav`, `fx_test2`, `cop`, `f3`, `uf`, `uf_3b`. NOT RUN (riferimenti/server non nel repo): `b31`, `b40e`, `d3a`, `data`, `lm`, `m21`, `m2`, `m34`, `xm_close`, `xm`.
`f4b_test` e `map3b_test` hanno dato falsi FAIL con 3 processi paralleli e PASS in isolamento (default del runner: 1 processo).

## Problemi rimasti e rischi residui
1. **Firebase con la CSP:** la connessione reale non è verificabile dalla sandbox. Se `connect-src` fosse troppo stretta la sync fallirebbe (i dati locali non sono a rischio). **Va provata una sync reale prima del push.**
2. **iPhone:** build c26 non verificata (CSP, SW per build, menu da tastiera, contrasto).
3. **`preferredMode`:** mantenuto (compatibilità backup), non fuso con la modalità attiva; se deve diventare il default iniziale serve una decisione (cambio di comportamento).
4. Utenti con la vecchia cache `v9`: viene eliminata all'attivazione del nuovo SW (intenzionale).
5. Aperti: logo TMDB mancante (`assets/images/tmdb-logo.svg`), 7 locandine mancanti (073, 074, 077, 086, 107, 115, 125), metadati catalogo `multiverso`, 8 test BLOCKED da riscrivere con la specifica attuale, SRI/CSP stretta.
6. Il rapporto non copre le suite NOT RUN (richiedono build di riferimento).

**Attendo approvazione prima di commit/push/deploy.**
