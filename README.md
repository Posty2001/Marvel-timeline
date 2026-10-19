# Marvel Multiverse — TVA Archive (PWA)

App statica a file singolo. Pubblicazione: GitHub Pages (branch `main`, cartella root).

- `index.html` — build finale (manifest e icone incorporati)
- `sw.js` — service worker (network-first, cache dinamica)
- `assets/` — immagini
- `tools/` — sorgenti e patch idempotenti; pipeline: `tools/build_3c.sh` → `build_restyle.sh`
- `tests/` — test Playwright/Chromium (richiedono un server locale, es. `python3 -m http.server 8124`)
- `docs/` — report di audit e progetto Fase 4
