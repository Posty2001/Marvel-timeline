# Marvel Multiverse — TVA Archive (PWA)

App statica a file singolo. Pubblicazione: GitHub Pages (branch `main`, cartella root).

- `index.html` — build finale (manifest e icone incorporati; CSP in `<meta>`)
- `sw.js` — service worker (network-first, cache dinamica). `SW_BUILD` e nome cache sono legati alla build (`marvel-timeline-cache-<build>`), impostati da `tools/patch_c26.py`
- `assets/` — immagini
- `tools/` — sorgenti e patch idempotenti. **Pipeline attuale:** `tools/build_4.sh` (catena di `patch_*.py` fino a `patch_c26.py`). Parte da un `index.html` già prodotto da `build_3c.sh` → `build_restyle.sh`; **non è rieseguibile da capo su una build finita**: per applicare solo l'ultima patch usare `python3 tools/patch_c26.py` (idempotente). L'identificativo di build è nel `<meta name="tva-build">`
- `tests/` — test Playwright/Chromium e runner riproducibile (vedi sotto)
- `docs/` — Registro Master (ultima sezione: E, consolidamento C2–C6), rapporti di blocco, `PROBLEMI_PREESISTENTI.md`

## Test
```
pip install playwright pillow && playwright install chromium
python3 tests/run_suites.py                 # tutte le suite, un processo alla volta (default)
python3 tests/run_suites.py --only c2_test,c3_test,c4_test,tva_test
python3 tests/run_suites.py --list
```
Il runner avvia un server locale per suite sulla radice del progetto, adatta percorsi/porte/build-id **solo nelle copie temporanee** dei test e produce `tests/results/RESULTS.md|json` con PASS / FAIL / BLOCKED / NOT RUN e le motivazioni. I FAIL noti sono in `tests/KNOWN_FAILS.json`; un FAIL non viene mai trasformato in PASS. Ultimo esito: `tests/RESULTS_C26.md`. Non occorre accesso alla rete. Con più processi paralleli (`--jobs`) alcune suite sensibili ai tempi (`f4b_test`, `map3b_test`) possono dare falsi FAIL.
Suite con dipendenze non incluse (build di riferimento `index.3c.frozen.html`, `index.pre_*.html`, backup `backups/N*.html`, server 8125–8128) risultano NOT RUN.
