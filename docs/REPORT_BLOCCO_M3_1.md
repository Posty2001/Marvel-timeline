# TVA Archives — Blocco M3.1 · Locandine TMDB (build 20261023-1100-m31)

Nessun commit/push/deploy. Firebase, dati Marvel, ordini, progressi e ricompense non toccati.

## Cosa è pronto
| # | Richiesta | Implementazione |
|---|---|---|
| 1 | Associazione catalogo → TMDB (film / serie / stagioni) | `tools/tmdb_sync.py` → `assets/images/catalog/tmdb_map.json` (`t` movie\|tv, `id`, `s` stagione, `p` poster_path). Stagioni (S1, S2…) usano il poster della stagione, con ripiego su quello della serie. Abbinamento solo se titolo esatto (film: anno ±1); ambigui → `tmdb_review.json`; correzioni a mano in `tmdb_overrides.json`. |
| 2 | Locandine in Opera e Timeline | Dossier Opera: locandina nell'hero. Scheda Timeline: miniatura (92×138) alla prima apertura, solo se esiste una locandina. |
| 3–4 | Priorità | immagine personalizzata (licence + verified:true) → TMDB → emblema. Se la personalizzata non carica, ripiega su TMDB; se anche TMDB fallisce, resta l'emblema. Controlli di licenza dei file locali invariati. |
| 5 | Caricamento | Hero: `srcset` w342 (1x) / w500 (2x); miniature: w154 / w342 (lazy); larghezza/altezza dichiarate (niente salti di layout); `referrerPolicy=no-referrer`; nessuna immagine rotta in caso di errore. Offline: TMDB saltato. |
| 6 | Segreti | Nessuna chiave nel codice o nella build: l'API serve solo al sync (offline, sul tuo PC); l'app a runtime usa solo gli URL immagine pubblici di `image.tmdb.org`. Verificato da test (nessun `api_key`/token nella build). |
| 7 | Condizioni TMDB | Attribuzione sotto la locandina: «This product uses the TMDB API but is not endorsed or certified by TMDB» con link a themoviedb.org. Immagini mostrate intere, senza ritocchi. |

## Cosa devi configurare tu (non ho inventato credenziali né ID)
1. Crea un account TMDB e richiedi la chiave API (gratuita, uso non commerciale/attribuzione).
2. Sul tuo PC: imposta `TMDB_READ_TOKEN` (o `TMDB_API_KEY`) nella shell — mai nel repository — ed esegui `python3 tools/tmdb_sync.py`, poi `bash tools/build_4.sh`.
3. Controlla `tmdb_review.json` e risolvi i titoli non riconosciuti in `tmdb_overrides.json`.
4. Logo TMDB: i termini lo richiedono nei crediti. Scarica il logo ufficiale e aggiungilo dove preferisci (non l'ho ridisegnato); l'attribuzione testuale è già presente.
5. Verifica che l'uso dell'app rientri nei termini TMDB (uso non commerciale). Se l'app diventasse commerciale serve accordo con TMDB.

Finora `tmdb_map.json` è **vuoto**: in questa build non compare nessuna locandina TMDB finché non esegui il sync. Qui non potevo farlo (rete non consentita, nessuna chiave).

## Note
- Privacy: con le locandine attive il browser contatta `image.tmdb.org` (IP visibile a TMDB). Interruttore tecnico: `localStorage.tvaTmdbOff='1'`. Non ho aggiunto un'opzione nelle impostazioni: decisione di prodotto tua.
- Il service worker non mette in cache le immagini cross-origin: offline restano gli emblemi.
- Prima apertura offline di una scheda con locandina: emblema.

## File
`index.html`, `tools/patch_m31.py`, `tools/tmdb_sync.py`, `tools/build_4.sh`, `assets/images/catalog/tmdb_map.json`, `tmdb_overrides.json`.

## Test mirati
`m31_test.py` 15/15 (default senza richieste TMDB; locandina+attribuzione; srcset; priorità custom>TMDB; custom rotta→TMDB; non verificata ignorata; TMDB in errore→emblema; interruttore; miniatura Timeline; nessun errore JS; nessuna chiave nel codice; logica del sync con API simulata: match esatto, ambiguo rifiutato, anno lontano rifiutato). Regressioni: m3 16/16, m21 15/15, m1 14/14, data 5, rs 33, stats_fix 12, b321 38, lm 87, home2 49, leg 37, b31 67 — nessun fallimento.
