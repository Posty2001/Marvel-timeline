# Report Fase 3C — Cronologie del Multiverso
Build `20261019-0200-cronologie` · file unico `index.html` (+ `sw.js` invariato)

## Cosa è stato consegnato
- Hub «Cronologie» → nuova sezione «Esplora il tempo» (3 ingressi), nessun nuovo portale in Home TVA.
- **Cronologia universo**: spina temporale per ambientazione / uscita / ordine guida, nodi «anno certo», «approssimativo», «senza dato», «Prevista», eventi chiave dai dati 3A. Selettore universo (27).
- **Cronologie parallele**: «Corsie · uscita» (default), «Corsie proprie», «A | B»; riepilogo e collegamenti confermati dai dati 3A.
- **Esploratore**: ricerca, filtri (universo, tipo, stato uscita, ambientazione, ruolo), 4 ordinamenti, sezione «Non assegnate» (16 animazioni, mai attribuite in automatico).
- Pulsante «Cronologia» nei dossier 3A e nella scheda anteprima della mappa 3B (modifiche minime).
- Stato filtri e navigazione conservati tra Cronologie ↔ dossier ↔ mappa ↔ schede.
- Uscite future: «Prevista» (ufficiale / annunciata / da verificare); mai considerate uscite perché la data è passata.
- Le 37 animazioni usano il periodo di messa in onda come uscita, non come ambientazione.
- Le sei modalità Timeline alternative e «La mia timeline» sono intatte; progressi/XP/missioni/Firebase/Friends/Live Room non toccati.

## File modificati / nuovi
Nuovi: `tools/cron3c.js`, `tools/cron3c.css`, `tools/patch_cron3c.py`, `tools/build_3c.sh`.
Modificati: `tools/dossier.js` (pulsante), `tools/map3b.js` (pulsante), `tools/patch_map3b.py` (guardia idempotenza), `tools/patch_fase1.py` (build id), `rs_test.py`, `stats_fix_test.py` (build id) → `index.html`.

## Test superati
| Suite | Esito |
|---|---|
| Funzionale cron3c_test | 113 / 0 falliti |
| Viewport cron3c_vp (320–430, orientamenti) | 372 / 0 |
| Touch cron3c_touch (emulazione touch) | 25 / 0 |
| Coerenza Timeline Eventi vs tvaTime | 138 righe, 0 differenze |
| map3b_test / map3b_vp | 81 / 0 · 211 / 0 |
| d3a_test (dossier, 4 larghezze) | 0 falliti |
| nav_test, home2_test, map3b_perf | 31/0 · 0 · 5/0 |
| reg.py: an, g3, m3, m4, xm | OK |

## Nuovi difetti
Nessuno aperto. Corretti in corso d'opera: pulsante dossier che rompeva d3a (classe `ud-acts`), marcatori di lacuna fuorvianti, font <11px, input ricerca 42px, sovrapposizione footer sheet, N° mostrato come ID invece del numero visibile.

## Fallimenti preesistenti (identici sulla baseline 3B)
in1/in2, tva_test A8/A9, f3_test, r320 «home decor», ui_audit controlli Home, g2 (→ «REGRESSIONE FALLITA» di reg.py), net_test, uf_test (la modale `#missioneCelebrazione` intercetta i click: dipende dalla nuova settimana ISO, fallisce uguale sulla 3B salvata).

## Test non eseguiti
- Safari/iPhone reale (solo Chromium con touch emulato): verifica a cura tua.
- Test con account Firebase reali / Live Room multiutente.

## Limiti dichiarati sui dati
1. Animazioni: solo periodo di messa in onda («In onda»).
2. Stato «Prevista»: euristica data ≥ 2026-01-01; 12 titoli: 027, 134, 136, 139 ufficiali; 137, 138 annunciati; 039, 127, 128, 129, 132, 133 da verificare.
3. L'Esploratore conta la variante 133 sotto MCU (94); la cronologia universo (dati 3A) ne mostra 93.
4. 5 universi senza titoli associati → stato vuoto informativo.
5. Nei dossier 3A il «N°» per ID 022/023/024 differisce dal numero visibile della scheda (sistemato nella modifica X-Men successiva).

## Screenshot
`3c_screenshots/390x844/` e `3c_screenshots/320px/` (14 viste ciascuno: hub, cronologia universo ×3 modi, stati dati insufficienti/vuoto, parallele ×4, esploratore ×3, selettore).
