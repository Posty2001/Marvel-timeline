# TVA ARCHIVES — Report F-A1: autenticazione email/password

Base: commit `fbf3399` (c26) · Build di lavoro: **`20261023-2355-fa1`** (solo in `/home/claude/work`, non pubblicata; md5 `index.html` 82fdf0a6197fe8ebf5b4ddf8ff9ffc08)
Stato: **IMPLEMENTATO IN LOCALE — nessun commit, push o deploy. In attesa di approvazione.**
Non toccati: regole RTDB, `sync/`, `rooms/`, dati remoti, Firebase Console, credenziali, repository `marvel-timeline`, Registro Master (da aggiornare dopo l'approvazione).

## 1. Cosa è stato implementato

| # | Richiesta | Esito |
|---|---|---|
| 1 | Registrazione email + password + conferma | ✅ Validazioni client (email, ≥ 8 caratteri, ≤ 128, ≠ email, conferma uguale), nessuna chiamata se non valide |
| 2 | Login / logout | ✅ Messaggio unico «Email o password non corretti» (nessuna enumerazione); logout non cancella nulla di locale |
| 3 | Verifica email + reinvio | ✅ `sendEmailVerification` subito dopo la registrazione; vista «Email da verificare» con «Ho verificato», «Reinvia il link» (attesa 60 s), ricontrollo automatico al ritorno sulla scheda |
| 4 | Recupero password | ✅ `sendPasswordResetEmail`; risposta **sempre neutra** (identica per email nota e sconosciuta) |
| 5 | Sessione Firebase | ✅ `onAuthStateChanged`, persistenza predefinita dell'SDK (IndexedDB), watchdog 8 s se lo stato non arriva |
| 6 | Email in italiano | ✅ `auth.languageCode = 'it'` |
| 7 | UI TVA Hybrid, responsive, iPhone | ✅ Gruppo «Account personale (facoltativo)» in Centrale TVA → Operazioni, prima di «Sincronizzazione cloud»; riusa `reset-btn`, variabili colore, tema scuro; input 16 px, bersagli ≥ 44 px, `autocomplete` corretti (email / current-password / new-password) |
| 8 | Errori, caricamento, offline | ✅ Mappa errori in italiano (+ codice per quelli sconosciuti), `aria-busy` e pulsanti disabilitati, anti doppio invio, timeout 20 s, banner offline, nessuna chiamata se offline, SDK assente → «non disponibile» |

Il login **non è mai obbligatorio**: l'archivio locale funziona senza account e senza SDK Auth.

## 2. Modifiche tecniche (tutte in `index.html` + `sw.js`, via `tools/patch_fa1.py`, idempotente)

| Elemento | Modifica |
|---|---|
| Script | `firebase-auth-compat.js` 10.13.0 da `www.gstatic.com` (stessa versione e origine degli SDK esistenti) |
| CSP | `connect-src` + `https://identitytoolkit.googleapis.com` + `https://securetoken.googleapis.com`. Nessun wildcard `googleapis`, nessun `frame-src`, `script-src` invariato |
| UI | blocco `#faAccount` + CSS `fa1-css` (isolato) |
| Logica | `<script id="fa1-js">` isolato (IIFE). Espone solo `window.tvaAuth.getStatus()` (congelato) |
| Build/SW | id build `20261023-2355-fa1`; `sw.js` aggiornato (solo identificativi; logica C3 invariata) |
| File di test | `tests/fa1_test.py` (+ voce in `SUITES.json`) |

Garanzie verificate (analisi statica + test): il modulo **non** usa `localStorage`, RTDB, `sync/`, `rooms/`, `users/`, né Google / anonimo / popup / redirect. `initializeApp` è condiviso con il guard già presente nel sync (nessuna doppia inizializzazione). Il modulo non sincronizza nulla: l'account serve solo a identificare l'utente (F-A2 in poi).

## 3. Compatibilità

| Area | Esito | Evidenza |
|---|---|---|
| Firebase SDK esistente | ✅ Stesso 10.13.0 compat; `initializeApp` unica (guard `firebase.apps.length` già in sync e live room) | CODICE + test mock |
| CSP | ✅ per la pagina (zero violazioni nei test con CSP reale attiva); ⚠️ comportamento dell'SDK reale **non provabile qui** (vedi §5 B1) | test |
| GitHub Pages | ✅ file statici, nessun nuovo percorso, nessuna build; il dominio `posty2001.github.io` è già autorizzato da te | CODICE |
| Service worker | ✅ Gestisce solo GET: le chiamate Auth (POST) non sono intercettate; lo script gstatic entra in cache come gli altri SDK | CODICE |
| Safari iOS | **BLOCKED** (nessun WebKit/iPhone in sandbox). Emulato solo viewport 390×844 in Chromium | §5 B3 |

## 4. Test locali

Tutti i test Auth usano un **MOCK** dell'SDK (rete verso gstatic/Firebase bloccata). Provano UI, logica, stati e protezione dati; **non** l'SDK reale né il server.

| Suite | Esito |
|---|---|
| `fa1_test` (nuova, mock SDK) | **PASS 54 / FAIL 0** |

Copertura `fa1_test`: pannello nel gruppo corretto; stato iniziale «out» senza login; `languageCode='it'`; un solo `initializeApp`; validazioni (email, password corta, conferma); `aria-invalid`; caricamento + anti doppio invio (1 sola creazione); email di verifica con continue URL; reinvio bloccato 60 s; password svuotate dopo l'invio; persistenza sessione al reload; «Ho verificato» prima/dopo verifica; logout; login errato e email inesistente (stesso messaggio); email già in uso; reset neutro (note/sconosciute); offline (banner, nessuna chiamata, ritorno online); errore di rete SDK; watchdog 8 s; SDK assente; invio verifica fallito (account creato, errore, reinvio disponibile); `localStorage` **identico** su tutto il flusso (watched, ratings, XP bank, badge, rewards, Timeline personalizzata + modalità attiva, nome); nessuna violazione CSP; nessun errore JS; 390 px senza scroll orizzontale, input ≥ 16 px, pulsanti ≥ 44 px; analisi statica (nessun localStorage/RTDB/Google/anonimo); CSP (2 host, no wildcard, no frame); SDK stessa versione.

Due scoperte di test (non sono difetti del modulo): l'app salva da sola `auto-backup` (con nuovo `exportedAt`) 5 s dopo ogni avvio e normalizza i dati seed al primo ricaricamento; il confronto dei dati è quindi fatto dopo l'assestamento e ignora il solo orario.

### Regressione completa
Giro completo `python3 tests/run_suites.py --jobs 1` sulla build `20261023-2355-fa1`: **PASS 33 | FAIL 6 | BLOCKED 9 | NOT RUN 10** (58 suite). Confronto con c26 (PASS 33 / FAIL 6 / BLOCKED 8 / NOT RUN 10, con 1 suite in più = `fa1_test`):

| Verifica | Esito |
|---|---|
| FAIL nuovi rispetto a `KNOWN_FAILS.json` | **0** — i 6 FAIL (b32, bl, cron3c, fx_test4, fy, ui_audit) sono gli stessi documentati e preesistenti |
| BLOCKED invariati (obsoleti/preesistenti) | cons, cop, f3, fx_test2, nav, net, uf, uf_3b — stesse cause di c26 |
| BLOCKED in più | `b322_test`: errore del *runner* (`FileNotFoundError: b321_geom.py`, prima di caricare la pagina; riscrittura del percorso `/tmp/claude-0/t/`). Eseguita direttamente: **PASS 14 / FAIL 0**. Non è una regressione dell'app; il runner va corretto (attività separata) |
| c2, c3 (SW/offline/aggiornamento), c4 (CSP/accessibilità), c4_contrast, b2, b40c, cap0, a2, assets, … | PASS |

Risultati completi: `tests/RESULTS_FA1.md` (copia in outputs non allegata; disponibile su richiesta).

## 5. Elementi BLOCKED e rischi aperti

| ID | Elemento | Stato | Cosa serve |
|---|---|---|---|
| B1 | Funzionamento dell'SDK Auth **reale** sotto la CSP: in particolare se la versione compat tenta di caricare `apis.google.com` (iframe di origin-validation) all'avvio | **BLOCKED** (SDK scaricabile solo con rete; nessuna prova da qui) | Primo test reale sul tuo dispositivo/PC con console aperta: nessun errore «Refused to load…». Se compare `apis.google.com`, **mi fermo e ti chiedo** (non allargo la CSP da solo) |
| B2 | Registrazione, email di verifica, login, recupero **reali** contro Firebase | **BLOCKED** (rete) e **non autorizzato** a creare account reali | Tua autorizzazione e un'email di test (o test tuo) |
| B3 | Safari iOS / PWA installata (sessione IndexedDB, tastiera, autofill password, ritorno dal link email) | **BLOCKED** | Prova su iPhone dopo l'approvazione |
| B4 | SRI per `firebase-auth-compat.js` | Non applicato: l'hash va calcolato sul file reale di gstatic (rete); gli altri due SDK non hanno SRI | Calcolo su macchina con rete; decisione tua se estenderlo anche agli altri due |
| B5 | Rinvio/limiti server (quota email, throttle `too-many-requests`) | Non verificabile | Test reale |
| R1 | Un'email non verificata può esistere ma non fa nulla (nessuna scrittura dati in F-A1) | Per progetto | Le regole F-A2 richiederanno `email_verified` |
| R2 | Con «protezione enumerazione email» attiva, registrando un'email esistente Firebase risponde comunque `email-already-in-use` | Accettato, messaggio chiaro | — |
| R3 | `continueUrl` usa `origin + pathname` della pagina | Richiede dominio autorizzato (fatto) | — |

## 6. Decisioni/autorizzazioni richieste

1. Approvare F-A1 così com'è (o indicare modifiche).
2. **Pubblicazione** (commit/push/deploy) della build `20261023-2355-fa1`: solo con tua autorizzazione esplicita.
3. Autorizzare test reali (B2) con un indirizzo di test e dire chi crea l'account; io non creo account reali.
4. SRI (B4): sì/no, e se estenderlo agli altri SDK.
5. Dopo la pubblicazione: prova su iPhone (B3) e controllo console CSP (B1) prima di F-A2.

Nessuno sviluppo oltre F-A1 è stato iniziato.

## 7. Artefatti
- `tools/patch_fa1.py` (patch idempotente applicata su c26), `tests/fa1_test.py`, `tests/SUITES.json`, `tests/RESULTS_FA1.md` — in `/home/claude/work`.
- Screenshot 390 px: `FA1_shot_registrazione_390.png`, `FA1_shot_account_390.png`.
- Il repository `marvel-timeline` e il Registro Master **non sono stati modificati**.
