# TVA Archives — Registro Master (ricognizione, sola lettura) · 22/10/2026
> **Aggiornato il 23/10/2026** con i blocchi M3.2 → M3.4.2 (sezione D, in fondo). Le sezioni A–C restano la ricognizione del 22/10 (build 4.0E) e non sono state riscritte: dove la sezione D contraddice A–C, vale la D.
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
| Pubblicazione GitHub Pages | — | DA VERIFICARE | Repo locale 7 commit; remoto/online non raggiungibile da qui; nulla pubblicato in questa sessione | Versione online probabilmente ≤ pre-4.0C |
| PWA: manifest inline, service worker v9 (font/avatar), tema | — | PARZIALE | C index.html `rel=manifest` (data-URI), `sw.js` v9 | Offline reale e installazione iOS mai verificati |

### A2. Timeline, ordine di visione, filtri
| Funzionalità | Fase | Stato | Evidenza | Residuo |
|---|---|---|---|---|
| Timeline Marvel 138 schede (+1 variante, 37 animate), ID stabili | base | COMPLETATA | T data_test 5/5, b2_test | — |
| Ordine di visione X-Men (Fox) + audit chiusura (categoria `xmen`) | X-Men (P 6d14d126) | COMPLETATA | R XMEN_ORDINE/CHIUSURA; T xm_test 53/53, xm_close 134/134 | — |
| Filtri, modalità spoiler (soglia), ordine personalizzato (5 viste timeline) | base | PARZIALE | C `spoilerCutoffInput`; memoria utente | **Ordine personalizzato escluso da export/backup/sync** (audit §8; C: assente da PROFILE keys) |
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
| Baseline test pulita | PARZIALE | Falliscono da sempre: tva_test A8/A9, ui_audit Home ×14, r320 ×3; map3b/cron3c 0/0; leg_test instabile (causa ignota) | Aggiornare/riscrivere test obsoleti |
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
Inoltre `tva_test` si interrompe con un'eccezione al blocco J (`.a2-feat` assente: `Cannot read properties of undefined (reading 'click')`), anch'essa identica sulla build precedente: i controlli oltre quel punto **non vengono eseguiti**. Dettagli in `docs/PROBLEMI_PREESISTENTI.md`. Noto anche il falso positivo di contrasto `.ud-st` in `ui_audit`.

### D2. Altri aperti / decisioni
| Voce | Stato |
|---|---|
| Logo TMDB ufficiale per i Crediti | Mancante: va fornito come `assets/images/tmdb-logo.svg` (compare da solo); testo+link già presenti |
| 7 titoli senza locandina TMDB | 073 The Defenders, 074/086 Punisher S1/S2 (poster mancante), 077 Team Thor, 107 Holiday Special, 115 I Am Groot, 125 Fantastic Four: First Steps → fallback emblema |
| Modalità Timeline attiva | Solo locale (non in profilo/export/sync/Firebase), come concordato fino alla fase Firebase; l'ordine personalizzato resta escluso da backup/sync (aperto da A2) |
| Missioni: effetto collaterale del fix | Ora il rendering iniziale delle missioni esiste al caricamento; la prima scrittura dello snapshot settimanale resta al primo tocco (come prima) |
| Testo voto medio | «Ancora nessun voto» → «Nessun voto» (3 colonne) |
| Verifica iPhone | Tutti i blocchi M3.2–M3.4.2 + PWA/offline: da eseguire sul dispositivo reale |
| Dati Marvel, ordini di visione, progressi, XP, ricompense, Firebase, TVA Friends | Non modificati in nessun blocco M3.x; nessuna credenziale nel repository (scansione ripetuta) |
