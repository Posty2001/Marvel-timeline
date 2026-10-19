# TVA Archives — integrazione sezioni legacy (build 20261018-0400-legacy-integration)

## Mappa percorsi legacy → destinazione moderna
| Partenza | Prima (legacy) | Ora |
|---|---|---|
| Personaggi, ricerca, chip dei dossier, link incrociati (mvNavigateTo/goChar) | scheda classica | scheda personaggio nativa (Apparizioni, Universi e origine, Poteri, Legami, Fumetti, Altro) |
| Cronologie → cronologie tematiche | card classica | schermata "Cronologie" con tab e linea del tempo |
| Relazioni → Alberi genealogici | card classica | schermata "Alberi genealogici" |
| Attori (49) | solo archivio classico | elenco + scheda attore nativi |
| Incursioni, Maratona Weekend | solo archivio classico | schermate "Eventi e percorsi" |
| Reliquiario → Cronologia delle Gemme | pannello classico | cronologia nativa |
| Dossier / Universo → "Apri nell'archivio classico" | bottone | rimosso (la scheda nativa contiene tutti i campi, incl. "Nella guida: …") |
| Toggle archivio classico (Home, menu) | overlay classico | reindirizzato all'Atlante (`?legacy=1` lo riabilita per debug) |
| Grafi Kang/TVA, Relazioni, Multiverso | SVG fisso, tagliato | viewport con pan/pinch/zoom, vista intera centrata, testi ingranditi |
| Timeline degli Universi | nomi disallineati, solo scroll | nomi allineati, salti rapidi ai capitoli |

L'overlay classico resta nel DOM come sorgente dati (nulla è stato cancellato), ma non è più raggiungibile dall'utente.

## Gemme: dati verificati vs non confermati
Scoperta: i campi «COMPARE IN»/«TITOLI» della guida usano una numerazione sfalsata di +1 in molti casi (es. Gemma del Tempo → «#069 Black Widow», ma è Doctor Strange N°070). Un riferimento è **verificato** solo se: titolo nominato accanto al numero, confermato dalla cronologia delle Gemme, nome completo nel testo, o apparizione di un personaggio collegato. Il resto è in «Riferimenti della guida non confermati» (sezione richiudibile). Nessuna associazione inventata. Esempi: Mente 051/062/084 verificati, 061 non confermato; Mjolnir 050/076 verificati, 075 non confermato. I personaggi citati sono etichettati «Citati nel testo della guida» (non indicano il possessore).

## Test (Chromium, 390 px e altri viewport)
- leg_test (nuovo): 0 fallimenti — schede native, back, guardia, gemme, grafici (nessun nodo tagliato, pan/zoom, tap≠drag, fit), allineamento timeline.
- rs_test 33/33, nav_test 29/29, a2_test 0 fail, lm_test 0 fail.
- ios.py 272/288: i 16 fallimenti sono i vecchi controlli sull'intro (titolo/eyebrow HTML nascosti perché ora nell'illustrazione) — invariati, attesi.
- Test aggiornati perché obsoleti: nav_test (non apre più l'archivio classico), a2_test (nessun bottone classico nel dossier), rs_test (build id).

## Da verificare su Safari/iPhone reale (non verificabile con Chromium)
Pinch-zoom e trascinamento dei grafi (touch-action, gesti a due dita), scroll verticale della pagina attorno ai grafi, font Spectral caricati, safe area, comportamento del tasto Indietro di sistema, PWA/service worker dopo l'aggiornamento.

## Note
- Gli screenshot indicati nel messaggio non sono arrivati.
- Piccoli difetti noti: in alcune voci di cronologia «( N°102 )» va a capo; «Altre apparizioni —» vuoto su alcuni personaggi.
- Deploy: carica `index.html` (e, se non già presente, `assets/images/intro/living-multiverse.webp`). `sw.js` invariato.
