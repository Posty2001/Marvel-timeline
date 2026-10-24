# TVA Archives — Registro Master (ricognizione, sola lettura) · 22/10/2026
> **Aggiornato il 23/10/2026** con i blocchi M3.2 → M3.4.2 (sezione D) e con il consolidamento C2–C6 (sezione E, in fondo). Le sezioni A–C restano la ricognizione del 22/10 (build 4.0E) e non sono state riscritte: dove D o E contraddicono A–C, vale la più recente (E > D > A–C). Le righe di A che sono state superate portano la nota «→ E».
Build di riferimento: `20261022-2100-blocco4-0e` · Nessuna modifica a codice/Firebase/database · nessun commit/push/deploy.
**Stati:** COMPLETATA = implementata + test automatici passati (Chromium/Playwright; *nessun test su iPhone/Safari reale è registrato in nessun rapporto*, salvo dove indicato) · PARZIALE · DA SVILUPPARE · DA VERIFICARE · SOLO PROPOSTA · ESCLUSA.

## 0. Fonti mancanti (dichiarato)
- **Non reperiti:** il documento originale della roadmap **F1–F6** e l'eventuale **roadmap in 10 fasi**; i prompt delle Fasi 2 (parte progettuale), 4 e dei fix intermedi non sono tutti conservati. La Fase 1 (prompt `db0204c7`) dice solo «il progetto è già definito e approvato». **Contenuto di Fase 5 e Fase 6 non recuperabile**: i rapporti dicono solo «Fase 5 non avviata»; dopo lo sprint pre-Fase 5 il lavoro è proseguito per «Blocchi» (1, 2, 3.1, 3.2.x, 4.x). Non so se Blocchi 1–3 coprano F5/F6: **da confermare da te**.
- **Disponibili:** prompt/brief Fase 1, Home, Fase 3, X-Men, restyling, Blocchi 1–3.2.5, 4.0B/D/E; audit del 15/10 (`981e2fcf`); 36 rapporti in `outputs/` e `docs/`; memoria utente; repository (7 commit locali dal 19/10); build/test.
- Le decisioni di «fusione degli archivi» le ricavo dai rapporti (legacy→nativo, Fase 3B/4); non esiste un elenco unico approvato: **non invento altre fusioni**.

## A. Registro Master
Fonti: **P**=prompt/brief · **R**=rapporto · **C**=codice (file/funzione) · **T**=test.

### A1. Home, introduzione, navigazione
| Funzionalità | Fase/blocco | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Struttura TVA Archives, accesso ibrido (card Home + voce menu), modalità immersiva, Indietro coerente | F1 (P db0204c7) | COMPLETATA | R legacy_integration; T nav_test 28/28, a2_test 24/24 | iPhone reale |
| Home «Living Multiverse» con 15 portali e 8 asset definitivi | F2 (P 4f448229) | COMPLETATA | R home_assets; T home2_test 49/49 (15 portali → destinazione→ritorno) | Home: ui_audit ×14 e r320 ×3 falliscono (preesistenti) |
| Introduzione cinematografica a vista singola + statistiche reali (27/300/138/176) | F2 | COMPLETATA | R intro_vista_singola, stats_fix; T stats_fix 12/12, lm_test 87/87 | «~527 ore» sorgente non verificata |
| Barra a 6 voci, ATLANTE → home, Timeline compatta, overlay iOS | pre-F5, B1 | COMPLETATA | R SPRINT_PRE_FASE5, BLOCCO1; T fy_test 133/133, b2_test 121/121 | iPhone reale (rapporto stesso lo chiede); SW cache v9 deciso |
| Pubblicazione GitHub Pages | — | DA VERIFICARE (→ E: verificata, deploy riuscito per `65617fc` e `32a570b`) | Repo locale 7 commit; remoto/online non raggiungibile da qui; nulla pubblicato in questa sessione | Versione online probabilmente ≤ pre-4.0C |
| PWA: manifest inline, service worker v9 (font/avatar), tema | — | PARZIALE (→ E/C3: SW versionato per build, aggiornamento e offline provati in Chromium) | C index.html `rel=manifest` (data-URI), `sw.js` v9 | Offline reale e installazione iOS mai verificati |

### A2. Timeline, ordine di visione, filtri
| Funzionalità | Fase | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Timeline Marvel 138 schede (+1 variante, 37 animate), ID stabili | base | COMPLETATA | T data_test 5/5, b2_test | — |
| Ordine di visione X-Men (Fox) + audit chiusura (categoria `xmen`) | X-Men (P 6d14d126) | COMPLETATA | R XMEN_ORDINE/CHIUSURA; T xm_test 53/53, xm_close 134/134 | — |
| Filtri, modalità spoiler (soglia), ordine personalizzato (5 viste timeline) | base | PARZIALE | C `spoilerCutoffInput`; memoria utente | ~~Ordine personalizzato escluso da export/backup/sync~~ **superato (→ E/C2):** `customOrder` è in export/import/sync dal blocco M1; la modalità Timeline attiva resta solo locale |
| Prerequisiti/Dependency Map, suggerimenti rispettano dipendenze | audit 15/10 | DA VERIFICARE | C `initDependencyMaps` ("una sola volta"); nessun rapporto/test dedicato letto | Verificare duplicazione pannelli e suggerimenti |
| Road to Doomsday (16 titoli, +300 XP) e distinzione watchlist ufficiale / editoriale | audit, B2 | COMPLETATA | R BLOCCO2; C `roadToDoomsday`, `DEP_FONTI_HTML` | Peso contestuale N°069/073/094 non deciso |
| «Modalità Prima di Doomsday» come funzione autonoma | citata dall'utente | DA VERIFICARE | Nel codice 0 occorrenze di «Prima di Doomsday»; esistono Road to Doomsday e countdown | **Chiedi: coincide con Road to Doomsday o è una modalità a sé?** |
| Correzioni di dati certi dell'audit (sinossi/continuità N°046, 091–092, 119–120/134, post-credit 094/121/123; schema anno/ambientazione) | audit §10 p.2–3 | DA VERIFICARE | Solo X-Men documentato come chiuso; altro non tracciato | Riconciliare audit ↔ build |
| Dati da aggiornare con fonte (date uscita 027/131/135–139, cast 132, streaming IT, Earth-199999) | audit §9 | DA SVILUPPARE | R FASE3C: 12 titoli «Prevista», 6 da verificare | Servono fonti datate |

### A3. Atlante / Multiverso / 15 aree
| Funzionalità | Fase | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Aree: Universi, Personaggi, Relazioni, Cronologie, Poteri, Ricerca, Artefatti, Organizzazioni, Luoghi, Eventi, Specie e Civiltà, Entità Cosmiche, Arti Mistiche (+Home, Multiverso) | F1–F4 | COMPLETATA (a livello di portale e schede) | T home2_test 15 portali, leg_test 37/37, tree_arti 48/48; R legacy_integration | Profondità dei contenuti per area non misurata |
| Fusioni legacy→nativo (Personaggi, Cronologie tematiche, Alberi, Attori 49, Incursioni/Maratona→Eventi e percorsi) | F2/legacy | COMPLETATA | R legacy_integration | — |
| Dossier Universi (3 stati dei dati, ambientazione approssimata) | F3A | COMPLETATA | R FASE3A | Asset illustrati: solo brief, fallback SVG |
| Mappa interattiva del Multiverso | F3B | COMPLETATA | R FASE3B; T map3b | map3b_test 0/0 controlli (da riscrivere); target 12–20 px in landscape basso |
| Cronologie del Multiverso (hub, esploratore, parallele) | F3C | COMPLETATA | R FASE3C; T cron3c | cron3c_test 0/0 controlli; 5 universi senza titoli |
| Dossier Opera/Personaggio/Attore, `tvaXref`, ricerca tollerante (961 query) | F4 A–C | COMPLETATA | R FASE4; T xm, lm, rs | Tempo apertura <100 ms non dimostrato in uso prolungato |
| 93 dossier archivio con skin per categoria | F4 D | PARZIALE | R FASE4 (D6: nessun asset definitivo) | Illustrazioni definitive |
| Candidati identità (13 gruppi) / fusioni di personaggi | F4 D3 | DA VERIFICARE | `CANDIDATI_IDENTITA_D3.md`: nessuna unificazione eseguita | **Attendono tue decisioni caso per caso** |
| Grafo Relazioni (302 nodi), Alberi genealogici, Arti Mistiche | pre-F3 | COMPLETATA | R relazioni_alberi_arti; B1 (etichette 6,4 px) | Etichette piccole su 320 px |
| Immagini: 8 copertine + hero + intro (WebP) | F2 | COMPLETATA | C assets/images/tva (16 file) | — |
| Locandine/poster **per titolo** | — | SOLO PROPOSTA | Nessun documento di approvazione; 1 sola `<img>` nel DOM; nessun asset | Decidere se serve (e licenze) |
| Ambientazioni (asse «ambientazione» per opera) | F3A/F4 | COMPLETATA | R FASE3A/F4 | Date da testo libero, approssimate |

### A4. Centrale TVA, missioni, strumenti, progressione
| Funzionalità | Fase | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Centrale TVA (Panoramica, Missioni, Operazioni, Strumenti), 2.1 rifinitura | B2, B2.1 (P 38f2a810) | COMPLETATA | R BLOCCO2/2.1; T b2_test | 6/9 checkpoint → `#parte3`; testo tab 8 px a 320 |
| Missioni (attive/stagioni/speciali/archivio) + XP, stagione «Guerra delle Incursioni» | B2 | COMPLETATA | R BLOCCO2 | — |
| «Cosa guardo stasera», statistiche, Modalità Confronto | B2 | COMPLETATA | R BLOCCO2; C stringhe presenti | — |
| Quiz «da dove inizio» (`quizGoBtn`) | base | DA VERIFICARE | C presente; fuori dal flusso visibile dopo l'intro a vista singola (display:none) | Decidere se riesporlo |
| Quiz/Duelli tra amici | Friends | vedi A7 | — | — |
| Backup/ripristino manuale validato, copia di sicurezza, reset | audit §8, 4.0C | COMPLETATA | C `normalizzaProfilo`/`sostituisciProfilo`; T imp 33/33 | Ordine personalizzato fuori dal profilo |

### A5. Tessera Variante
| Funzionalità | Fase | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Tessera (livelli/ranghi, 14 distintivi, XP) | base/B3 | COMPLETATA | C `updateTessera`; T b31 66/66 | — |
| Ricompense cosmetiche (48), migrazione dati | B3.1 | COMPLETATA | R BLOCCO3_1; `tools/rw.js` | Unione multi-dispositivo testata come funzione, non su Firebase reale |
| Avatar (8), cornici (12), temi (10), effetti (6), 3 layout, editor, PNG, Variant ID `VAR-XXXXXX` | B3.2–3.2.6 | COMPLETATA | R BLOCCO3_2…3_2_6; battery Tessera 13/13 suite PASS (22/10) | Safari reale non provato; foto solo locale (non nel profilo) |
| Unicità dei Variant ID | — | DA SVILUPPARE | C `getTesseraId`: `Math.random`, nessuna garanzia | Indice server (blocco Friends) |

### A6. Backup, sincronizzazione, autenticazione
| Funzionalità | Fase | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Client sync: stati reali, conflitti espliciti, validazione, retry limitati | 4.0C | COMPLETATA (client) | R 4.0C; T b40c 41/41 | **Cloud NON VERIFICATO** |
| Barriera di inizializzazione, niente falsi conflitti | 4.0E | COMPLETATA (con limitazioni) | R 4.0E; T b40e 24/24 | Grafo instabile; sync reale non provata |
| Funzionamento reale di `sync/<codice>` | — | DA VERIFICARE / probabile BLOCCATA | Regole utente: solo `rooms` | Verifiche manuali 4.0D §6 |
| Backup storici (nodo `sync`) | — | DA VERIFICARE | Esportati manualmente dall'utente; non letti | Non accedere/modificare |
| Firebase Authentication / App Check | 4.0B | DA SVILUPPARE | Decisioni 4.0B (anonimo → e-mail verificata); C: nessun SDK Auth | Blocco Friends F-A |
| Regole di sicurezza per-utente, Variant ID↔UID | 4.0B/D | DA SVILUPPARE | Solo regole `rooms` | idem |
| Spark 0 €/mese | 4.0B | Vincolo | Pagina prezzi 22/10 | Cloud Functions non disponibili |

### A7. TVA Friends
| Funzionalità | Stato | Evidenza | Residuo |
|---|---|---|---|
| TVA Live Room (classifica real-time) | PARZIALE | C `rooms/*`; memoria: bug regole risolto ad agosto | Impersonificazione/quote (regole attuali); senza Auth |
| TVA Group (gruppi con codice, confronto manuale), amici legacy | PARZIALE | C `friends-group-*`, `friends-lb-*` | Manuale, nessun server |
| Varianti (profilo pubblico minimo), Legame Nexus, Squadre TVA, Serate Marvel, Quiz/Duelli, Archivio, Centro Comunicazioni | DA SVILUPPARE | Direzione approvata in 4.0/4.0B; proposta 4.1–4.7 in R 3.2.6 «da approvare»; **nessuna specifica scritta trovata per Quiz/Duelli, Archivio, Centro Comunicazioni** (citati nel tuo elenco) | 0 occorrenze nel codice |
| Notifiche (inbox, poi Web Push) | SOLO PROPOSTA | R 3.2.6 F5, non approvata; Web Push richiede server (non Spark-compatibile se server-side) | Decidere ridimensionamento |
| Privacy (default privato, consensi espliciti) | Vincolo approvato | 4.0B | Da tradurre in regole |

### A8. Qualità trasversale
| Funzionalità | Stato | Evidenza | Residuo |
|---|---|---|---|
| Accessibilità (ARIA 320 occorrenze, reduced-motion ×21, target 44 px) | PARZIALE | C; test mirati nei blocchi | Nessun audit VoiceOver/contrasto globale; ui_audit Home ×14 |
| Responsive 320–430 | COMPLETATA (Chromium) | fy_test, home2_test | Landscape basso |
| Test su iPhone reale | DA VERIFICARE | Tutti i rapporti: «non verificato su Safari reale» | Checklist da eseguire dall'utente |
| Baseline test pulita | PARZIALE (→ E/C5: runner riproducibile `tests/run_suites.py`, `tva_test` 0 FAIL con J–Q, riepilogo PASS/FAIL/BLOCKED/NOT RUN in `tests/RESULTS_C26.md`) | Falliscono da sempre: tva_test A8/A9, ui_audit Home ×14, r320 ×3; map3b/cron3c 0/0; leg_test instabile (causa ignota) | Aggiornare/riscrivere test obsoleti |
| ESCLUSA | — | **Nessuna funzionalità risulta esplicitamente esclusa** nei documenti disponibili | — |

**Riepilogo:** COMPLETATA ≈ 32 · PARZIALE ≈ 9 · DA VERIFICARE ≈ 9 · DA SVILUPPARE ≈ 7 · SOLO PROPOSTA ≈ 2 · ESCLUSA 0.

## B. Roadmap residua (dipendenze rispettate)
**App principale (nessun Firebase remoto)**
| Blocco | Contenuto | Dipende da |
|---|---|---|
| **M1 Baseline di rilascio** | Riportare i test a verde (Home ×16, tva_test, map3b/cron3c, causa del grafo); inserire l'ordine personalizzato nel profilo con retrocompatibilità; checklist iPhone | — |
| **M2 Qualità dei dati** | Audit §9–10 residuo: date/stati, cast, ambientazione, post-credit; Dependency Map | M1; tue fonti/decisioni |
| **M3 Archivi e contenuti** | Decisioni D3 (13 gruppi), asset illustrati dei dossier, scelta su locandine, quiz «da dove inizio» | decisioni tue |
| **M4 Verifica reale e rilascio** | Prova su iPhone, PWA offline, accessibilità (VoiceOver), pubblicazione | M1–M3; tua autorizzazione push/deploy |

**Espansione TVA Friends (dopo l'app principale, in parallelo solo la parte locale)**
| Blocco | Contenuto | Dipende da |
|---|---|---|
| **F-A Fondamenta** | Verifiche manuali Console; regole in Emulator; Anonymous Auth dietro flag; indice Variant ID; e-mail verificata; pubblicazione regole additive (**remoto, da autorizzare**); `sync` storico congelato | 4.0D §6, build ≥4.0E online |
| **F-B Multiverso privato** | Gruppi 2–6, inviti, ruoli, Legame Nexus, Squadre TVA, privacy per campo | F-A |
| **F-C Serate, sfide, comunicazioni** | Serate Marvel, Quiz/Duelli, Archivio/ricordi, Centro Comunicazioni (in-app) | F-B; specifica da scrivere |
| **F-D Hardening** | Test accesso incrociato, XSS, quote Spark, iPhone | F-C |

## C. Prossimo intervento (uno solo, dopo il 4.0E): **M1 — Baseline di rilascio**
- **Obiettivo:** avere una baseline di test affidabile e un backup davvero completo prima di costruirci sopra Friends.
- **Modifiche:** (1) aggiornare/riscrivere i test obsoleti (Home ×16, tva_test A8/A9, map3b/cron3c) senza alterare il prodotto, e correggere la Home solo dove il difetto è reale (testi <11 px, overflow decorativi) — **previa tua autorizzazione**; (2) individuare la causa dell'instabilità di `leg_test` (riproduzione con carico controllato); (3) includere `marvelGuideCustomTimelineOrder` in export/import/sync con retrocompatibilità dei vecchi backup; (4) checklist iPhone da eseguire da parte tua.
- **Test essenziali:** suite attuali (generale + Tessera + b40c/b40e) senza nuovi fallimenti; import di un vecchio backup senza il nuovo campo; `leg_test` 10/10 sotto CPU rallentata; ID/progressi invariati.
- **Perché questo:** Friends è bloccato dalle tue verifiche Console e da decisioni; M1 è locale, a basso rischio e rende individuabili le regressioni dei blocchi successivi.

*Mi fermo qui in attesa di autorizzazione. Nessuna modifica effettuata.*

## D. Aggiornamento 23/10/2026 — M3.2 → M3.4.2 (build 20261023-1730-m342)
**Legenda stati.** *Implementato* = nel codice della build. *Testato* = test automatici Chromium/Playwright (emulazione iPhone 320/360/390 px) passati. *Verificato su iPhone* = prova su dispositivo reale: **per nessun blocco di questa sezione è stata registrata una verifica su iPhone reale** (la esegui tu: M3.2 e successivi sono «da verificare»).
**Pubblicazione.** M3.2 → commit `248b1b6`; M3.3 + M3.4 → `65617fc` (deploy Pages riuscito); M3.4.1 + M3.4.2 → commit di questa consegna (vedi rapporto). Precursore: M3.1 (locandine TMDB, 131 abbinamenti, workflow manuale `tmdb-sync`, commit `c7706e3` e precedenti).

| Blocco | Implementato | Testato (esito) | Verificato su iPhone |
|---|---|---|---|
| **M3.2** Scheda Opera mobile | Voto a 5 stelle nella riga principale (nessun duplicato nel pannello; 1° tocco intero, 2° stessa stella −0,5, 3° ripristino; persistenza; a11y); locandina nella riga principale (manifest autorizzato → TMDB → emblema); Reliquiario raggiungibile dall'Atlante (accesso dalla Home mantenuto); attribuzione TMDB in Crediti/Privacy; allineamento intestazioni | `m32_test` 33/33; overflow 390/360/320 senza regressioni (`home2_test` 49/49) | **NO** (da fare: stelle, locandine, apertura schede, navigazione) |
| **M3.3** Capitolo 0 | Singola card «Prologo — Prima del Tempo», chiusa di default, 5 letture 0.1–0.5 espandibili, ID/testi/link invariati, Parte 1 subito dopo; i link a `#cap0` aprono la card | `cap0_test` 37/37 (nessun salto, nessun overflow 390/360/320) | **NO** |
| **M3.4** Home «TVA Hybrid» | Header + barra; card Prossimo titolo con locandina, anno · universo, Inizia/Continua; 3 statistiche (completati, ore, voto medio); accessi Atlante/Tessera; una missione attiva + Centrale TVA, con stati vuoti; rimosse dalla Home le scorciatoie ridondanti (funzioni ancora nelle sezioni). **Fix alla fonte:** (1) voto medio vuoto al caricamento/dopo import (chiave voti inizializzata dopo la prima lettura); (2) missioni tematica/saga con «—» (la prima `updateMissioni` usciva prima che i dati esistessero), ora ripetuta in sola lettura | `m34_test` 35/35 (14 settimane simulate senza descrizioni vuote; localStorage identico alla build precedente: nessuna ricompensa/XP/snapshot al caricamento) | **NO** |
| **M3.4.1** Prossimo titolo e Timeline attiva | Modalità attiva salvata in locale (`marvelGuideActiveTimelineMode`); personalizzata = primo non visto dell'ordine salvato con gli stessi vincoli; sequenza vuota/corrotta → standard; Home aggiornata su cambio modalità/riordino/completamento/storage; Inizia/Continua aprono il titolo mostrato | `m341_test` 20/20 | **NO** |
| **M3.4.2** «Cosa guardo dopo» | La card Timeline usa la stessa funzione della Home (`trovaProssimoHome`), si aggiorna con modalità/ordine | `m342_test` 15/15 | **NO** |

**Regressioni eseguite sulla build finale:** m34, m341, m342, rs, stats_fix (ultimo giro); nel giro precedente anche cap0, m32, m31, m3, b321, home2, leg, m21, m1, data (tutti OK). `rs_test` è stato **aggiornato di proposito** alla nuova gerarchia della Home (copia originale `rs_test.pre_m34.py`, solo nell'ambiente di lavoro).

### D1. Problemi NON risolti (nessuno è stato nascosto o modificato per ottenere PASS)
**Otto controlli storici di `tva_test.py` ancora FALLITI** (identici sulla build pre-M3 → preesistenti; non attribuibili a M3.x):
1. `G multiverso atlante chiuso`
2. `G reliquiario atlante chiuso`
3. `G arti n schede`
4. `H cronologie righe 15!=10`
5. `H cronologie[0] apre sezione`
6. `H cronologie[1] apre sezione`
7. `H cronologie[2] apre sezione`
8. `H cronologie[6] ritorno`
*(Superato in E/C5: i controlli sono stati classificati e i selettori obsoleti aggiornati; `tva_test` ora ha 0 FAIL e i blocchi J–Q vengono eseguiti.)* Inoltre, fino a M3.4.2, `tva_test` si interrompeva con un'eccezione al blocco J (`.a2-feat` assente: `Cannot read properties of undefined (reading 'click')`), anch'essa identica sulla build precedente: i controlli oltre quel punto **non vengono eseguiti**. Dettagli in `docs/PROBLEMI_PREESISTENTI.md`. Noto anche il falso positivo di contrasto `.ud-st` in `ui_audit`.

### D2. Altri aperti / decisioni
| Voce | Stato |
|---|---|
| Logo TMDB ufficiale per i Crediti | Mancante: va fornito come `assets/images/tmdb-logo.svg` (compare da solo); testo+link già presenti |
| 7 titoli senza locandina TMDB | 073 The Defenders, 074/086 Punisher S1/S2 (poster mancante), 077 Team Thor, 107 Holiday Special, 115 I Am Groot, 125 Fantastic Four: First Steps → fallback emblema |
| Modalità Timeline attiva | Solo locale (non in profilo/export/sync/Firebase), come concordato fino alla fase Firebase; l'ordine personalizzato è invece in backup/sync (→ E/C2; il «resta escluso» di questa riga è superato) |
| Missioni: effetto collaterale del fix | Ora il rendering iniziale delle missioni esiste al caricamento; la prima scrittura dello snapshot settimanale resta al primo tocco (come prima) |
| Testo voto medio | «Ancora nessun voto» → «Nessun voto» (3 colonne) |
| Verifica iPhone | Tutti i blocchi M3.2–M3.4.2 + PWA/offline: da eseguire sul dispositivo reale |
| Dati Marvel, ordini di visione, progressi, XP, ricompense, Firebase, TVA Friends | Non modificati in nessun blocco M3.x; nessuna credenziale nel repository (scansione ripetuta) |

## E. Aggiornamento 23/10/2026 — Consolidamento C2–C6 (build `20261023-1520-c26`, base `32a570b`)
**Stato di pubblicazione:** modifiche **solo locali** (nessun commit, push o deploy; in attesa di approvazione). **Nessuna modifica** a Firebase, regole, credenziali, dati remoti, catalogo Marvel, ordini di visione, progressi, voti, XP, ricompense; nessuna funzionalità TVA Friends; nessun refactoring generale di `index.html`.

**Verifica su iPhone reale — M3.4.2 (build `20261023-1730-m342`): 6/6 PASS, dichiarata dall'utente** (esito riferito dall'utente il 23/10/2026; l'elenco dei sei controlli non è stato fornito e non è registrato qui). La verifica **non** copre la build c26 (CSP, SW per build, menu da tastiera, contrasto): da ripetere sul dispositivo prima della pubblicazione. Per M3.2, M3.3, M3.4 e M3.4.1 non è registrata una verifica separata.

### E1. C2 — Timeline e backup
| Elemento | Stato |
|---|---|
| `customOrder` (`marvelGuideCustomTimelineOrder`) | In profilo, export, import (validato, transazionale), sync, copia di sicurezza automatica del Reset totale. Immutato |
| `marvelGuideActiveTimelineMode` (`custom`/`standard`) | Solo locale, mai in profilo/export/sync (come concordato fino alla fase Firebase). Immutato |
| `preferredMode` (`marvel-ultimate-timeline-preferred-mode`, `uscita`/`cronologico`) | Preferenza **dichiarata** nel quiz d'ingresso; resta nel profilo e nei backup per compatibilità; non è mai letta. **Non fusa** con la modalità attiva: domini diversi (ordine uscita/cronologico ≠ personalizzato/standard); una fusione richiederebbe una migrazione o un cambio di comportamento → **non applicata, serve decisione** |
| Difetto 1 (corretto) | «Cancella tutto» rimuoveva l'ordine ma lasciava la modalità `custom`; ora rimuove anche la modalità locale |
| Difetto 2 (corretto) | `custom` con ordine vuoto (Reset totale, import con `customOrder: []`) riapriva «Personalizzato» mentre la Home usava il percorso standard; ora la Timeline riparte da «Consigliato» (stessa regola della Home) |
| Test | `c2_test` 29/29: export, import (vecchio backup senza i campi, completo, ordine vuoto, 4 casi invalidi senza scritture), cambio modalità, ricarica, reset progresso (ordine/modalità intatti), Reset totale |

### E2. C3 — PWA e cache
| Elemento | Stato |
|---|---|
| `sw.js` | `SW_BUILD` e nome cache legati alla build (`marvel-timeline-cache-<build>`, impostati da `tools/patch_c26.py`); `activate` elimina **solo** le cache `marvel-timeline-cache-*` diverse dalla corrente (prima: tutte le cache dell'origine); `install` mette in cache anche `./` e `./index.html` (offline subito dopo un aggiornamento); la navigazione offline ignora la query; **(C3b)** la pagina entra nella cache solo se il suo `tva-build` coincide con `SW_BUILD` (deploy a metà con `sw.js` nuovo e `index.html` vecchio: nessun HTML di altra build sotto una cache nuova) |
| Aggiornamento in pagina | Meccanismo esistente invariato (confronto build via Range + una sola ricarica per build). Nessun avviso nuovo, nessun cambio di interfaccia |
| Dati utente | `localStorage` non viene mai toccato dal SW; verificati ordine, modalità, voti e progressi dopo installazione, offline, aggiornamento |
| Test | `c3_test` 22/22 con service worker reale in Chromium: installazione, cache obsoleta `v9` rimossa, cache di un'altra app preservata, precache pagina, offline, aggiornamento a una nuova build, offline dopo l'aggiornamento (serve la build nuova), ritorno online, **deploy a metà** (index vecchio + sw nuovo: non salvato; a deploy completo la build coerente entra in cache alla navigazione online) |
| Non verificato | Safari/iOS reale; installazione da «Aggiungi a Home» |

### E3. C4 — Sicurezza e accessibilità
| Elemento | Protezione | Stato |
|---|---|---|
| Contrasto `.ud-st` | Misura sui **pixel** (testo reso trasparente, sfondo reale) su 27 universi: `ok` 4,97 (PASS), `lg` 11,98 (PASS), `vf` 4,10 (**insufficiente**). Corretto solo `.ud-st-vf` (testo `#EA9195`, 5,31). `ui_audit` stima 4,40 su `ok`: falso positivo del suo modello di composizione (documentato). Le misure «5,4/6,7» citate in precedenza non sono riproducibili e sono **superate** | IMPLEMENTATA |
| CSP (meta) | `default-src 'self'`; `script-src 'self' 'unsafe-inline' https://www.gstatic.com`; `style-src 'self' 'unsafe-inline' https://fonts.googleapis.com`; `font-src` fonts.gstatic.com; `img-src 'self' data: blob: https://image.tmdb.org`; `connect-src` `'self'`, Firebase (`*.firebaseio.com`, `*.firebasedatabase.app`, https/wss), fonts, TMDB; `manifest-src 'self' data:`; `worker-src 'self'`; `object-src 'none'`; `base-uri 'self'`; `form-action 'self'`. Nessuna violazione nei flussi principali (`c4_test`); uno script da origine esterna viene bloccato | IMPLEMENTATA (limitata) |
| Limiti della CSP | `'unsafe-inline'` resta (app a file singolo con script inline): la CSP **non** protegge da XSS inline. `frame-ancestors` non è impostabile con `<meta>` (serve header HTTP, non disponibile su GitHub Pages). **La connessione Firebase reale non è verificabile dalla sandbox** → da provare con una sync vera prima della pubblicazione | RACCOMANDATA: nonce/hash (refactoring), header HTTP |
| SRI | I due script `firebase-*-compat.js` 10.13.0 su gstatic non sono scaricabili da qui (403): un hash non calcolato sui byte reali bloccherebbe l'app. CSS Google Fonts non è soggetto a SRI | NON IMPLEMENTATA, **raccomandata** (calcolare `sha384` da una macchina con rete) |
| Tastiera | Il menu laterale chiuso era nell'ordine Tab (link fuori schermo): ora `visibility:hidden` finché chiuso; pulsanti apri/chiudi raggiungibili con Tab, Invio/Spazio, Esc chiude, `aria-expanded` aggiornato; la funzione al tocco è invariata | IMPLEMENTATA |
| Etichette/focus | 0 controlli visibili senza nome accessibile; 0 immagini visibili senza `alt`; indicatore di focus presente sui controlli attraversati; skip-link presente | VERIFICATA (Chromium) |
| Non verificato | VoiceOver reale, Dynamic Type, navigazione da tastiera in ogni overlay | APERTO |

### E4. C5 — Test automatici
- **Runner riproducibile:** `tests/run_suites.py` (+ `SUITES.json`, `KNOWN_FAILS.json`). Avvia un server per suite sulla radice del progetto, sostituisce percorsi/porte/build-id solo nelle copie temporanee, classifica PASS / FAIL / BLOCKED / NOT RUN e confronta i FAIL con quelli documentati. Un FAIL non diventa PASS.
- **Esito (`tests/RESULTS_C26.md`):** 57 suite — **PASS 33, FAIL 6, BLOCKED 8, NOT RUN 10**; 1511 asserzioni PASS, 32 FAIL, **tutti documentati e identici alla build pre-M3.4 (nessun FAIL nuovo)**. Le suite sensibili ai tempi (`f4b`, `map3b`) hanno mostrato falsi FAIL con 3 processi paralleli e PASS in isolamento (`--jobs 1` è il default).
- **`tva_test`:** blocchi J–Q ripristinati (J usava `.a2-feat`, rimosso: ora i portali `.hm-p[data-tile=reliquiario|poteri]`); 0 FAIL su 390×844, 320×568, 844×390. Otto FAIL storici e tre FAIL K/L classificati **tutti come aspettative/selettori obsoleti, nessun difetto applicativo** (il comportamento reale è stato riprodotto e verificato):
  | Controllo | Causa | Aggiornamento |
  |---|---|---|
  | `G multiverso/reliquiario atlante chiuso` | ora schermate native `mappa`/`reliquiario` dentro l'Atlante | aspettativa: resta nell'Atlante, Indietro → catalogo |
  | `G arti n schede` | Arti Mistiche = 3 schede (Stregoneria, Magia oscura, Magia del caos; `docs/REPORT_relazioni_alberi_arti.md`, `tree_arti_test`) | atteso 3 (era 1) |
  | `H cronologie righe 15!=10` | il catalogo ha 15 voci | atteso 15 |
  | `H cronologie[0..2] apre sezione` | aprono schermate native (`cron`), non overlay | «overlay chiuso **oppure** schermata diversa» |
  | `H cronologie[6] ritorno` | a cascata: le voci 3–5 aprono overlay classici ma il test le trattava come «Varianti» e saltava il Back, lasciando overlay e stack sporchi | il salto vale solo se resta nella stessa schermata **e** nell'Atlante |
  | `K ricerca gemme -> archivi` | i risultati sono chip `.a2-chip`, non righe `.a2-lrow` | selettore |
  | `K char apre scheda`, `L scheda personaggio` | il dossier personaggio è la schermata nativa `char` | `sc=='char' && on` |
  | `Q localStorage modificato` | `tvaHomeMiss:<build>` = cache di locandine non caricate (non dato utente) | escluso dal confronto |
- **Altri aggiornamenti:** `a2_test` (il percorso passa dal Dossier Opera: due Indietro) → 40/40; `b324_test` (nome cache dinamico invece di `v9`) → 27/27.
- **BLOCKED (8):** `cons_test`, `net_test`, `nav_test`, `fx_test2`, `cop_test`, `f3_test`, `uf_test`, `uf_test_3b`: selettori/flussi obsoleti (elementi rimossi da Fase 4/M3.4); non riscritti perché richiedono una specifica attuale. **NOT RUN (10):** richiedono build di riferimento (`index.3c.frozen.html`, `index.pre_*.html`, `backups/N*.html`) o server aggiuntivi (8125–8128) non inclusi nel repository.

### E5. Problemi ancora aperti e rischi residui
| Voce | Nota |
|---|---|
| Verifica iPhone della build c26 | Da eseguire (CSP, SW per build, menu da tastiera, contrasto) |
| Firebase live con la CSP | Non verificabile dalla sandbox; verificare sync reale prima del push |
| SRI Firebase; CSP senza `unsafe-inline` | Raccomandate, non implementate |
| `preferredMode` | Mantenuto per compatibilità; decisione di prodotto richiesta se deve diventare il default iniziale |
| Attribuzione TMDB | Testo e link presenti nei Crediti; **logo ufficiale mancante** (`assets/images/tmdb-logo.svg`, va fornito) |
| Locandine TMDB | **7 titoli senza locandina** (073, 074, 077, 086, 107, 115, 125) → fallback emblema |
| Test BLOCKED/NOT RUN | 8 + 10 (vedi E4) |
| `fx_test4`, `bl_test`, `fy_test`, `b32_test`, `cron3c_test`, `ui_audit` | FAIL documentati, preesistenti, non corretti per ottenere PASS |
| Metadati catalogo `multiverso` (`st:'cls'`, azione `map`) | Segnalato, non modificato (contenuto) |
| Cache SW: gli utenti con la vecchia `v9` la perdono all'attivazione della nuova | Intenzionale; la pagina della nuova build entra in cache già all'installazione del SW |

## F. Aggiornamento 24/10/2026 — F-A1 Autenticazione email/password (build `20261023-2355-fa1`, base `fbf3399`, tag `pre-fa1`)
| Voce | Nota |
|---|---|
| Funzione | Account personale **facoltativo** (Centrale TVA → Operazioni): registrazione, verifica email + reinvio, login, logout, recupero password, sessione Firebase, email in italiano. Nessuna sincronizzazione dati, nessuna scrittura su RTDB/`sync/`/`rooms/`/`users/`, nessuna lettura/modifica del profilo |
| CSP | Solo `connect-src` +`identitytoolkit.googleapis.com` +`securetoken.googleapis.com` (motivazione completa in `docs/REPORT_F-A1_RIFINITURA.md` §3) |
| Test | `fa1_test` (SDK **simulato**) 64 PASS; `b322_test` risolto (helper `tests/b321_geom.py` mancante nel repo) |
| **ATTIVITA' APERTA — SRI** | Hash SRI Firebase 10.13.0 **non calcolati** (rete bloccata nel sandbox). Script pronti: `tools/sri_firebase.sh|ps1`, `tools/apply_sri.py`. **F-A1 non è chiusa finché l'SRI non è risolto** |
| **ATTIVITA' APERTA — collaudo reale** | Test su iPhone con Firebase reale (`docs/PROCEDURA_TEST_REALE_IPHONE_F-A1.md`): SDK reale sotto CSP (verificare assenza di `apis.google.com`), email, Safari/PWA. Rollback: `docs/STRATEGIA_ROLLBACK_F-A1.md` (`git revert`, tag `pre-fa1`) |
| Non iniziato | F-A2 (regole `users/{uid}`), migrazione, sync account |
