# TVA ARCHIVES — F-A1: report di rifinitura

Build: `20261023-2355-fa1` (invariata: `index.html` md5 `82fdf0a6197fe8ebf5b4ddf8ff9ffc08`, `sw.js` md5 `c64333d50488bf9909e482b81b27ff44`). Solo lavoro locale: **nessun commit, push, deploy**; nessuna modifica a Firebase, regole RTDB, `sync/`, `rooms/`; nessun account creato; F-A2 non iniziata.

| # | Richiesta | Esito |
|---|---|---|
| 1 | Runner / `b322_test` | **RISOLTO** |
| 2 | Integrità/SRI Firebase 10.13.0 | **BLOCKED** (nessun hash inventato) — script pronti |
| 3 | CSP restrittiva | **CONFERMATA** (diff verificato) |
| 4 | Nessuna lettura/modifica/sync dei dati | **CONFERMATO** (statico + 64 test) |
| 5 | Uso senza login; logout/cambio account | **CONFERMATO** |
| 6 | Procedura test reale iPhone | **PRONTA** |
| 7 | Rollback senza toccare Firebase | **PRONTA** |

## 1. Runner e b322_test
- **Causa reale:** `b322_test` legge l'helper `b321_geom.py` che esisteva solo in `/tmp/claude-0/t/` (fuori dal repository). Il runner riscrive il percorso in relativo e copia gli helper solo se presenti in `tests/`: il file mancava → `FileNotFoundError` prima ancora di aprire la pagina. Non era un difetto dell'app.
- **Correzione:** aggiunto `tests/b321_geom.py`, copia **byte per byte** dell'originale (verificato con `cmp`). Né `b322_test.py` né il runner sono stati alterati; nessuna asserzione toccata.
- **Esito:** `b322_test` via runner **PASS 15 / FAIL 0** (come c26). Torna quindi BLOCKED 8 (le stesse cause preesistenti, non nascoste).
- Nota: il file `b321_geom.py` entrerà nel repository solo con il commit autorizzato.

## 2. Integrità script Firebase 10.13.0 — BLOCKED
- Rete verso `gstatic.com`, `cdn.jsdelivr.net` e `registry.npmjs.org`: **403 / host non risolvibile** dal proxy del sandbox (riprovato). Impossibile scaricare i file ufficiali → **nessun hash calcolato né riportato**.
- Pronti (non eseguiti qui): `tools/sri_firebase.sh` e `tools/sri_firebase.ps1` (Windows) scaricano dagli **stessi URL** di `index.html` i tre file (`app`, `database`, `auth` compat) e stampano `sha384-…`, SHA-256 e dimensione in JSON. `tools/apply_sri.py` applica `integrity` + `crossorigin="anonymous"` **solo** con hash validi (formato `sha384-` + 64 base64), rifiuta il resto, è idempotente. Provato su copia temporanea con valori fittizi (esplicitamente di prova): rifiuta l'hash malformato, applica 3 tag una sola volta; **il file di lavoro non è stato modificato**.
- Rischi da valutare prima di attivare SRI: (a) l'hash blocca l'SDK se gstatic aggiorna il file (sync e Auth degradano ma l'archivio resta); (b) serve CORS da gstatic (atteso, non verificabile qui) — provare su iPhone/PC prima del deploy; (c) il service worker mette in cache la risposta CORS (stessa richiesta della pagina): nessun problema atteso, da confermare nel test reale.
- Raccomandazione: eseguire lo script sul tuo PC, incollarmi il JSON, applico e ritesto; SRI come **commit separato** da F-A1.

## 3. CSP
Diff rispetto a c26 (`fbf3399`): una sola direttiva cambiata, `connect-src`, **+2 host, −0**: `https://identitytoolkit.googleapis.com`, `https://securetoken.googleapis.com`. Invariate le altre 10 direttive; `script-src` invariato; **nessun** `unsafe-eval`, nessun `frame-src` (iframe/popup bloccati da `default-src 'self'`), nessun wildcard nuovo. Restano i wildcard preesistenti `*.firebaseio.com` / `*.firebasedatabase.app` (stringerli può rompere le connessioni RTDB a shard diversi: non toccati).
Motivazioni verificabili:
- `identitytoolkit.googleapis.com`: endpoint dell'accesso email/password — citato nella checklist di sicurezza ufficiale Firebase come host le cui quote proteggono dal brute force dell'accesso con email/password ([firebase.google.com/support/guides/security-checklist](https://firebase.google.com/support/guides/security-checklist?hl=de)). Il dettaglio per-operazione (signUp, signIn, sendOobCode) non è stato leggibile dalle pagine REST (troncate): **[INFERITO]**.
- `securetoken.googleapis.com`: rinnovo del token di sessione. **[INFERITO]**: non confermato da una fonte letta in questa sessione.
- Verifica empirica obbligatoria nel test reale (§6 Procedura, sezione B): solo questi due host per l'Auth; **qualsiasi altro host o `apis.google.com` → STOP**, nessuna CSP allargata senza tua decisione.

## 4. Il modulo non legge, modifica o sincronizza i dati utente — CONFERMATO
- Analisi statica (nel test, a ogni esecuzione): il codice del modulo non contiene `localStorage`, `setItem/removeItem`, `cookie`, `.database(`, `.ref(`, `sync/`, `rooms/`, `users/`, né riferimenti a `marvel-ultimate-timeline`, `marvelGuide`, `PROFILE_*`, `esportaProfilo`, `sostituisciProfilo`, `normalizzaProfilo`, `AUTO_BACKUP`, `costruisciProfilo`; nessun Google/anonimo/popup/redirect.
- Dinamica: su flusso completo (registrazione, verifica, logout, login errato/corretto, reset, offline) l'intero `localStorage` è identico (progressi, voti, XP bank, badge, ricompense, nome, Timeline personalizzata `[3,1,2]` + modalità attiva `custom`).
- Unica differenza osservabile, **preesistente e indipendente dal modulo** (dimostrata con controllo senza Auth): l'app riscrive da sola `auto-backup` con nuovo `exportedAt` 5 s dopo ogni avvio, e normalizza i dati al primo ricaricamento. Il test lo isola e lo dichiara.
- L'account non sincronizza nulla (nessun accesso al database dal modulo): F-A2 non iniziata.

## 5. Uso senza login; logout; cambio account — CONFERMATO (mock SDK)
| Scenario | Esito |
|---|---|
| Archivio usato senza account (segno un titolo come visto, salvato) | PASS |
| Con account verificato: nuovi progressi salvati, precedenti intatti | PASS |
| Logout: dati locali identici; archivio ancora usabile | PASS |
| Cambio account A→B (registrazione) e B→A (login): dati identici, nessuna fusione tra account | PASS |
| Riavvio con sessione attiva: dati identici (salvo la copia di sicurezza riscritta dall'app) | PASS |
| SDK Auth non caricato / sessione che non risponde (8 s) | PASS: «non disponibile», archivio operativo, nessun errore JS |
| Nessun errore JS / violazione CSP nel flusso | PASS |
**Limite:** prove con **SDK simulato**; il comportamento con Firebase reale resta da provare con la procedura iPhone.

## 6. Procedura test reale iPhone
`PROCEDURA_TEST_REALE_IPHONE_F-A1.md`: prerequisiti, verifica build, controlli CSP/rete con **criterio di stop** (`apis.google.com`, host extra), backup del profilo prima di iniziare, 19 casi (registrazione, verifica email, reinvio, login, logout, reset, offline, tastiera iOS, tema, PWA, integrità dati finale), esito e pulizia. L'account lo crei tu con un'email tua.

## 7. Rollback
`STRATEGIA_ROLLBACK_F-A1.md`: punto di ritorno `fbf3399`/c26 (md5 annotati) + zip; F-A1 in **un solo commit** con tag `pre-fa1` (da autorizzare) → `git revert`; alternative (ripristino file, rimozione del solo tag Auth); effetto su service worker (cache per build, pulizia solo cache dell'app), sessioni e account; verifica post-rollback in 4 passi. **Nessuna modifica a Firebase necessaria.**

## Test (stato finale)
| Suite | Esito |
|---|---|
| `fa1_test` (mock SDK) | **PASS 64 / FAIL 0** (era 54: +10 su integrità dati, uso senza login, logout, cambio account) |
| `b322_test` | **PASS 15 / FAIL 0** |
| Giro completo sulla build (invariata) | PASS 33 / FAIL 6 documentati / BLOCKED 9 → ora 8 con b322 risolto / NOT RUN 10 |

## Da autorizzare / decidere
1. Pubblicazione F-A1 (commit unico + tag `pre-fa1`): **non autorizzata**.
2. SRI: eseguire lo script sul tuo PC; inserimento come commit separato.
3. Test reali con tuo account di prova, con la procedura allegata.
