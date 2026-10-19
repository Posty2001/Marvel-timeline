# TVA ARCHIVES — Fase 4: Dossier e Archivi Marvel · Documento di progetto

Build analizzata: `20261019-0900-xmen-chiusura`. **Nessun codice del prodotto è stato modificato.** Fermo qui, in attesa della tua approvazione. Non ho iniziato la Fase 5.

Tutte le cifre sotto sono state lette dal codice e dai dati della build (non da memoria): schermate aperte a 390×844 e conteggi estratti dal DOM e dai blocchi JSON.

---

## 0. Sintesi

**Il punto di partenza è più avanzato di quanto la roadmap suggerisca.** L'Atlante ha già 14 sezioni, dossier nativi per organizzazioni, artefatti, eventi, luoghi, specie, arti mistiche e entità cosmiche, la Classifica dei Poteri con 156 schede, il Reliquiario, il confronto fra personaggi, e i collegamenti inversi verso le schede della Timeline. La Fase 4 non deve rifare questo: deve **unificare, approfondire e collegare**.

**Cosa manca davvero (verificato):**
1. **Non esiste un dossier nativo delle opere.** Titoli e serie vivono solo nella scheda della Timeline; dall'Atlante ogni chip «N°» porta fuori, nella Timeline. Non c'è un punto che riunisca cast, universo, saga, posizione in guida, uscita, ambientazione e opere collegate.
2. **La ricerca ha buchi reali.** «shield» non trova S.H.I.E.L.D. (la ricerca è sottostringa esatta, con punteggiatura e accenti). «jackman» non trova nulla perché i 49 attori non sono indicizzati.
3. **Le pagine personaggio sono tutte uguali.** 304 pagine con la stessa struttura a elenco; 188 (62 %) hanno **una sola apparizione**, quindi vanno trattate con una scheda breve, non con tab vuoti.
4. **Dossier secondari piatti.** Artefatti, luoghi e pianeti hanno due soli campi (descrizione + «compare in»; 210–409 caratteri). Eventi: solo 7 schede.
5. **Identità sparse.** Solo 5 gruppi «stesso individuo» sono dichiarati nei dati; altre pagine sembrano duplicati (es. Ross ×3, MJ ×3, Phil Coulson/Coulson) ma **nessun dato lo dichiara** (la somiglianza è solo nel nome della pagina: alcune potrebbero essere versioni distinte, come Coulson LMD): non verranno unite né presentate come identiche.
6. **Nessun contesto di percorso visibile.** Lo stack «Indietro» esiste ed è solido, ma l'utente non vede da dove arriva.

**Cosa propongo:** un livello condiviso di sola lettura (`tvaXref`) per i collegamenti, un piccolo «Dossier Kit» di componenti riusabili, un nuovo **Dossier Opera**, un **Dossier Personaggio 2** adattivo, un restyling per identità degli archivi esistenti (cornice, motivo, componente-firma — stessa palette), e la ricerca corretta. Nessun nuovo archivio. Nessun dato nuovo. Nessun ID, progresso, XP, badge, missione, Firebase, Friends o Live Room toccato.

**Decisioni che ti chiedo** sono al §10 (sei, con una raccomandazione ciascuna).

---

## 1. Inventario completo degli archivi esistenti

### 1.1 Portali dell'Atlante (home → capitoli → 14 voci di catalogo)

| Area | Voce | Schermata / sorgente | Stato |
|---|---|---|---|
| Multiverso e Tempo | Multiverso | Mappa 3B (`map3b.js`, `mvMapData`) | completo |
| | Universi | Dossier 3A (`dossier.js`, `universe_model.js`, `atlasData`) — 27 universi | completo |
| | Cronologie | 3C (blocco `CRON3C` in `atlas2.js`) + cronologie tematiche (`scheda.js`) | completo |
| | Eventi | `archivi.js`, schede `evt-`/`bat-` | **superficiale (7)** |
| Identità e Potere | Personaggi | `renderPersonaggi/renderChar` in `atlas2.js` — 304 pagine | completo ma uniforme |
| | Relazioni | grafo (`relationshipGraphData`), alberi (`famtree.js`), Kang/TVA | completo, dati radi |
| | Attori | `scheda.js` — 49 schede | **sottile** |
| | Classifica dei Poteri | `archivi.js` — 156 schede di potenza, confronto | completo |
| | Entità Cosmiche | `archivi.js` — 26 voci | buono |
| Mondi e Civiltà | Luoghi | `pia-`/`luo-` → 16 voci | **superficiale** |
| | Specie e Civiltà | aggregate dal testo — 8 voci | buono (voci derivate, dichiarate) |
| | Organizzazioni | `org-` — 17 schede | buono, copertura titoli limitata dalla guida |
| Reliquie e Arti | Artefatti | `art-` — 16 + Reliquiario | **superficiale** (2 campi) |
| | Arti Mistiche | aggregate — 3 voci | buono, dati limitati dichiarati |

### 1.2 Famiglie di schede nel DOM (sorgente dati)

`char` 304 · `item` 139 (138 titoli + 1 variante) · `att` 49 · `anim` 37 · `uni` 27 · `org` 17 · `art` 16 · `pia` 7 · `luo` 9 · `evt` 3 · `bat` 4 · altre (`p-`) 10.

### 1.3 Fonti dati condivise

| Fonte | Contenuto | Note |
|---|---|---|
| Schede della guida (DOM) | testo, campi PRIMA/ULTIMA/ALTRE APP., POTERI, CORRELATI, COMPARE IN | sorgente primaria |
| `atlasData` (148 KB) | 27 universi, 139 opere (uscita, ambientazione, ruolo, precisione), 37 animate, 304 personaggi (tipo, appartenenza, crossover, dubbio, collegamenti multiverso), 5 identità | sola lettura |
| `altTimelineData` | saga, release, tag, studio dei 138 titoli | data/saga |
| `relationshipGraphData` (318 KB) | 386 nodi; relazioni: titolo 1522, universo 692, attore 106, organizzazione 98, famiglia 28, relazione 4, variante 4 | **legami personaggio↔personaggio quasi assenti** |
| `mvMapData` | 27 universi per la mappa | 3B |
| `tvaIdx` (runtime, `net_module.js`) | indici titoli↔personaggi↔universi | già condiviso |
| Modello archivi (`archivi.js` `M`) | voci org/art/evt/luo/cos/spe/mis, `byTitle`, `charOrg`, `charCited`, `charExtra` | già condiviso, lazy |

---

## 2. Analisi: cosa c'è, cosa manca

### 2.1 Già presente (non va rifatto)

- Router unico `tvaGo(kind,id)` con stack «Indietro» e «App Marvel» (`net_module.js`); i tipi: item, char, uni, att, arc, filter.
- Collegamenti inversi iniettati nelle schede della Timeline: «ARCHIVI COLLEGATI» (32 titoli), «ORGANIZZAZIONI», «CITATO IN», «ENTITÀ, SPECIE E ARTI», «POTENZA TVA».
- Pagina personaggio: Apparizioni · Universi e origine · Poteri e natura · Legami · Nei fumetti (3–5 sezioni su 297 pagine su 304).
- Dossier archivio con provenienza dichiarata («dato derivato dai titoli», «riferimenti non confermati», «solo i nomi che corrispondono a una scheda»). **Questo principio va esteso, non sostituito.**
- Dependency Map (ESSENZIALI / CONSIGLIATI / FACOLTATIVI) già visibile nella scheda Timeline per 9 titoli crossover.
- Ordine editoriale, uscita e ambientazione già separati nei dati (`atlasData.opere`, `altTimelineData`) e nelle cronologie 3C.

### 2.2 Lacune e problemi verificati

| # | Evidenza | Impatto | Azione proposta |
|---|---|---|---|
| L1 | Nessuna schermata `opera` nell'Atlante; `tvaGo('item')` apre la scheda Timeline | alto: manca il perno fra personaggi, universi, 3B, 3C | **Dossier Opera** (P1) |
| L2 | Ricerca: `shield` → nessuna scheda per S.H.I.E.L.D.; `jackman`, `nyong` → nulla; `città` ≠ `citta` | alto, correzione piccola | Normalizzazione + attori (P2) |
| L3 | 188/304 personaggi con 1 sola apparizione; solo 158 hanno 5 sezioni | medio: un dossier «ricco» per tutti sarebbe vuoto | Layout adattivo (P3) |
| L4 | Artefatti 16, luoghi 16, pianeti, eventi 7: 2–4 campi | medio | Restyling + backlinks, **senza** inventare campi (P4) |
| L5 | Solo 5 gruppi `identita` (Xavier, 4× Peter Parker); altre pagine verosimilmente duplicate non dichiarate | medio: confusione, ma l'unione richiede una tua conferma | Lista di candidati da confermare (D3) |
| L6 | Varianti documentate: 4 `variante` + 2 `aggregata` + 5 «incarnazioni» + 14 con `collegamentiMultiversoMCU`; `crossover` = 0 | l'area «varianti multiversali» è piccola per natura | Mostrare solo dove i dati esistono, stato vuoto altrove |
| L7 | Legami personaggio↔personaggio: 28 «famiglia», 4 «relazione», 4 «variante»; il resto è testo CORRELATI | «Collegamenti ad altri personaggi» resta in gran parte testo | Chip dai CORRELATI **solo** se il nome coincide con una scheda; nessuna relazione inventata |
| L8 | S.H.I.E.L.D.: «1 titolo» confermato (la guida dice «e successive»); esistono 7 serie «Agents of S.H.I.E.L.D.» | limite del dato | Facoltativo: voce «per nome nel titolo», dichiarata derivata (D4) |
| L9 | Il contesto di percorso non è mostrato all'utente | medio, UX | Breadcrumb di sessione (P0) |
| L10 | Dopo la modifica X-Men il N° è posizionale: i moduli devono usare `marvelNumeroVisibile` | rischio di regressione | Test dedicati (§8) |

Archivi **che non vanno creati**: «Poteri» (esiste già come Classifica e campo POTERI), «Oggetti» (coperti da Artefatti), «Fazioni» (coperte da Organizzazioni). Nessun archivio nuovo.

---

## 3. Architettura condivisa

```
 DATI (sola lettura, invariati)          LIVELLO CONDIVISO NUOVO              UI
 schede DOM · atlasData · altTimeline    ┌─────────────────────┐   ┌──────────────────────────┐
 relationshipGraph · mvMapData  ───────► │ tvaXref (facciata)  │──►│ Dossier Kit (componenti) │
 tvaIdx · modello archivi M              │  rel(id) → vicini   │   │ hero · assi · percorso   │
                                         │  con fonte G/D/N    │   │ chip · stato vuoto ·     │
                                         └─────────────────────┘   │ breadcrumb · fonte       │
                                                    │               └────────────┬─────────────┘
                                         tvaGo / stack «Indietro» (esistenti)    ▼
                                                                    Schermate: opera · personaggio 2 ·
                                                                    archivi (skin) · ricerca
```

### 3.1 `tvaXref` — facciata di lettura (nuovo, senza dati propri)
Un'unica funzione `tvaXref.rel(id)` che restituisce i vicini di una scheda (personaggi, opere, universi, organizzazioni, eventi, luoghi, artefatti, attori), ciascuno con:
- `via`: da quale fonte nasce il legame;
- `fonte`: **G** scritto nella guida · **D** derivato (nome esatto nel testo, universo dei titoli, ecc.) · **N** non documentato.

Oggi questa logica è sparsa in `net_module.js` (`tvaIdx`), `archivi.js` (`M`), `universe_model.js`, `scheda.js` e `atlas2.js`. `tvaXref` non sostituisce niente: li **interroga** e rende uniforme la presentazione e i test. **Nessuna sorgente duplicata.**

### 3.2 Dossier Kit (componenti UI condivisi)
Hero con motivo per tipo · **striscia dei tre assi** (in guida / uscita / ambientazione, sempre separati) · «Percorso» ordinato per posizione di guida · riga di chip con etichetta di fonte · stato vuoto onesto · breadcrumb di percorso · barra di sezioni (mostra solo sezioni con dati). Stile in `atlas2.css`/un nuovo `dossier4.css`, stesse variabili di colore.

### 3.3 Regole vincolanti
1. **Nessun dato nuovo.** Un blocco compare solo se esiste la fonte; altrimenti stato vuoto.
2. **Tre assi mai fusi.** N° = posizione di guida (editoriale); uscita = `atlasData.opere.uscita`; ambientazione = `atlasData.opere.ambientazione`. Le etichette lo dicono ogni volta.
3. **ID stabili.** Si usano ID delle schede; il N° visibile passa sempre da `marvelNumeroVisibile`/`marvelPosizioneGuida`.
4. **Sola lettura.** Visto/XP/missioni mostrati ma mai scritti dai dossier.
5. **Bidirezionalità solo dove supportata.** Se A→B è nei dati, B→A viene mostrato con la stessa etichetta di fonte.
6. **Contesto di percorso.** Ogni navigazione aggiorna lo stack già esistente (`tvaPushNav`); il breadcrumb lo legge.
7. **Prestazioni.** Costruzione lazy come oggi (`build()`), nessun pre-calcolo all'avvio; budget: apertura di un dossier < 100 ms su CPU 4× più lenta (stessa metrica dei test esistenti).

---

## 4. Priorità di sviluppo (motivate)

| Pri. | Intervento | Perché adesso | Sforzo | Rischio |
|---|---|---|---|---|
| **P0** | `tvaXref` + Dossier Kit + breadcrumb | Fondazione: evita di duplicare la logica nelle prossime tre voci | M | basso (sola lettura) |
| **P1** | **Dossier Opera** (film, serie, animate) | Lacuna maggiore (L1); perno fra personaggi, universi, 3A/3B/3C | L | medio: tocca il router |
| **P2** | **Ricerca**: normalizzazione, attori, filtri per tipo | Bug reali, correzione piccola, beneficio immediato | S | basso |
| **P3** | **Dossier Personaggio 2** adattivo | 304 pagine; valore alto ma dati radi, quindi dopo P0/P1 | M | basso |
| **P4** | **Identità visiva** degli archivi esistenti (org, eventi, luoghi, artefatti) + backlinks | Fa sentire «archivi diversi, stesso sistema» | M | basso |
| **P5** | Attori: filmografia in ordine di guida | Piccolo, riusa P0/P1 | S | basso |
| — | Candidati identità duplicate (D3), voce «per nome nel titolo» (D4) | Solo se approvati | S | — |

Sequenza consigliata: **Sprint A** (P0+P2) → **B** (P1) → **C** (P3+P5) → **D** (P4). Ogni sprint è consegnabile e testabile da solo.

---

## 5. Wireframe mobile 390×844

File in `wf4/` (generati da `src4/wireframes_build.py` con dati reali; `wf4/f4_wireframe_sheet.png` è l'insieme). Etichette: **G** guida · **D** derivato · **N** non documentato.

| # | File | Mostra | Punti chiave |
|---|---|---|---|
| W1 | `w1_dossier_personaggio.png` | **Charles Xavier** (3 pagine dichiarate come stesso individuo, 8 titoli) | ① hero con universo · ② sezioni solo se hanno dati · ③ «Percorso nella guida» in ordine editoriale con uscita accanto · ④ identità dichiarate in `atlasData.identita` · stato vuoto «varianti» |
| W2 | `w2_dossier_opera.png` | **Logan N°023** | ① **tre assi separati**: in guida 12ª dei 13 Fox · uscita 3 mar 2017 · ambientazione 2029 · ② prima/dopo nella guida (Deadpool · Deadpool 2) · ③ cast · ④ universo e saga · ⑤ «opere collegate» con stato vuoto · ⑥ ponti verso scheda in guida, Cronologia 3C, Mappa 3B, Dossier universo 3A |
| W3 | `w3_identita_archivi.png` | Identità visiva dei sei tipi | cornice/motivo/componente-firma per tipo; palette invariata; animazioni leggere |
| W4 | `w4_dossier_evento.png` | **Il Blip** | motivo a raggiera · Prima/Dopo dal campo «Cause/Conseguenze» · titoli con uscita e ambientazione separate · «non confermati» restano separati |
| W5 | `w5_dossier_organizzazione.png` | **S.H.I.E.L.D.** | emblema esagonale · roster leader/membri (solo nomi con scheda) · limite «e successive» dichiarato |
| W6 | `w6_ricerca.png` | ricerca «shield» | filtri per tipo con conteggi · ricerca senza punteggiatura/accenti · attori indicizzati |

Il breadcrumb compare sotto la barra in W1, W2, W4, W5. I wireframe sono la prima schermata scorrevole: il resto segue la stessa griglia.

---

## 6. Piano dei collegamenti fra archivi

Legenda stato: **E** esiste · **N** nuovo · **P** parziale. Fonte: G/D come sopra.

| Da → A | Oggi | Fase 4 | Fonte | Ritorno |
|---|---|---|---|---|
| Personaggio → Opera | **E** chip N° → scheda Timeline | **N** apre il Dossier Opera (D1); «Scheda in guida» resta | G (PRIMA/ULTIMA/ALTRE APP.) | Opera → personaggio **N** |
| Opera → Personaggio | **E** solo nella scheda Timeline | **N** nel dossier | G (PERSONAGGI IN ARCHIVIO) | sì |
| Opera → Universo | **E** chip nella scheda | **N** | G (`atlasData.opere.universi`) | Universo → opera **E** (3A) |
| Opera → Saga | testo | **N** chip | G (`altTimelineData.saga`) | Cronologie 3C per saga **E** |
| Opera → Posizione in guida / precedente-successivo | N° visibile | **N** «prima/dopo» | G (ordine DOM) | — |
| Opera → Cronologia 3C / Mappa 3B / Dossier 3A | non diretto | **N** ponti contestuali | G | back via stack |
| Opera → Opere collegate | **P** la Dependency Map è mostrata nella scheda Timeline solo per 9 titoli crossover curati; i prerequisiti diretti (sequel) sono usati solo dai suggerimenti, non mostrati | **N** «richiede / consigliato» per tutte le opere che hanno dato; la Dependency Map esistente resta com'è | G (`PREREQ_DIRETTI_JS`, `DEPENDENCY_MAP_JS`) | simmetrico: «è richiesto da» |
| Opera → Archivi (evento, luogo, artefatto, org) | **P** 32/138 schede | **N** per tutte le opere con dato | G/D | Archivio → opera **E** |
| Personaggio → Organizzazione | **E** (46) | **E** + skin | G | Org → personaggio **E** (roster) |
| Personaggio → Evento/Luogo/Artefatto | **E** «CITATO IN» (16) | **E** | D (nome esatto) | Archivio → «personaggi citati» **E** |
| Personaggio → Varianti/altre pagine | solo 5 identità | **N** dove dichiarato (`identita`, `tipo`, `collegamentiMultiversoMCU`) | G | simmetrico |
| Personaggio → Attore | **E** nel testo | **N** chip diretto verso la scheda attore (49) | G | Attore → personaggi **E** |
| Attore → Filmografia | ruoli | **N** ordinata per guida | G | — |
| Ricerca → qualsiasi scheda | titoli, personaggi, archivi, universi | + attori; normalizzazione | — | — |

**Contesto di navigazione:** il breadcrumb riflette lo stack esistente («Da: Dossier Fox-Verse › Personaggi › Charles Xavier»); «torna a» riporta alla schermata esatta (stato `tvaAtlas2.getState/setState` già usato dai test).

---

## 7. Brief degli asset grafici

Tutti **opzionali**: senza file, il sistema usa i motivi SVG di W3 (come la Home). Percorso e naming nello stile dei file esistenti (`assets/images/tva/`).

| Asset | Uso | Specifica | Fallback |
|---|---|---|---|
| `dossier_personaggio.webp` | banda hero personaggio | 1170×420, nero cosmico con velo bordeaux, figure in silhouette, nessun volto reale/logo | gradiente + ovale SVG |
| `dossier_opera.webp` | hero opera | 1170×420, pellicola/proiettore dorato, tre punti luminosi | motivo pellicola SVG |
| `archivio_organizzazioni.webp` | hero org | 1170×420, esagono bordeaux inciso, trama a griglia | esagono SVG |
| `archivio_eventi.webp` | hero evento | 1170×420, raggiera in oro, filo tratteggiato crepuscolare | raggiera SVG |
| `archivio_luoghi.webp` | hero luoghi | 1170×420, orizzonte planetario, stelle rade | arco SVG |
| `archivio_artefatti.webp` | hero artefatti | 1170×420, reliquiario con angoli oro | cornice SVG |
| `cornice_ritratto.svg` | ovale personaggio | vettoriale 1 colore (oro), 160×200 | SVG inline |

Vincoli: niente volti di attori, loghi Marvel/Disney o personaggi riconoscibili; WebP ≤ 120 KB ciascuno; testo non incorporato nell'immagine. Il brief di dettaglio verrà consegnato con l'approvazione, come per le fasi precedenti.

---

## 8. Piano di implementazione e test

### 8.1 Sprint

| Sprint | Contenuto | Uscita consegnabile |
|---|---|---|
| **A** | `tvaXref`, Dossier Kit, breadcrumb, ricerca (normalizzazione, attori, filtri per tipo) | ricerca corretta + componenti riusabili |
| **B** | Dossier Opera (film, serie, animate), ponti 3A/3B/3C, router `item` (D1) | nuova schermata |
| **C** | Dossier Personaggio 2 adattivo, collegamento attore↔personaggio, filmografia attori | pagine personaggio/attore |
| **D** | Skin per tipo di archivio, backlinks opere→archivi per tutte le opere con dato | identità visiva completa |

Build: nuovo `patch_dossier4.py` (idempotente) nella pipeline `build_3c.sh` → rinominata `build_4.sh`; build id dedicato; rapporto dedicato per sprint.

### 8.2 Test (nuovi) e protezioni

1. **Fonte:** ogni chip del dossier ha `data-src` ∈ {G,D,N}; test che nessun blocco compare senza dato e che nessuna relazione è presente in `tvaXref` senza `via`.
2. **Tre assi:** per tutte le 138 opere il dossier mostra posizione, uscita e ambientazione uguali a DOM/`atlasData`; ordinamenti per uscita e per ambientazione invariati (confronto con la build corrente).
3. **Bidirezionalità:** per ogni coppia A→B nei dati il ritorno B→A esiste e punta alla stessa scheda.
4. **Contesto:** apri personaggio → opera → universo → Indietro ×3 riporta alla pagina di partenza con stesso scroll/stato.
5. **Ricerca:** casi `shield`, `S.H.I.E.L.D.`, `jackman`, `nyong`, `città/citta`, `wakanda`; nessuna regressione sui risultati attuali.
6. **N° posizionale:** test dopo la modifica X-Men (013 → X-Men Origins, ecc.) su tutti i nuovi blocchi.
7. **Integrità:** ID schede, `localStorage` (watched/favorites/notes/ratings), XP/badge/missioni, gruppi Amici, Live Room: byte-identici prima/dopo; nessuna scrittura da parte dei dossier (spia su `localStorage.setItem`).
8. **Regressione:** suite completa esistente (3A/3B/3C, home, nav, import/export, ios, ecc.) con confronto contro questa baseline; i fallimenti preesistenti restano elencati a parte.
9. **Viewport/touch:** 320, 375, 390, 393 px; bersagli ≥ 44 px; nessun overflow orizzontale; `prefers-reduced-motion`.
10. **Prestazioni:** apertura dossier < 100 ms (CPU 4×), scroll p95 < 50 ms (metrica attuale).
11. **Limite dichiarato:** Chromium + touch emulato; iPhone reale e Firebase restano a tua verifica.

---

## 9. Moduli da modificare (elenco preciso)

**Da creare**
- `tools/xref.js` — `tvaXref` (sola lettura).
- `tools/dossier4.js`, `tools/dossier4.css` — Dossier Kit e schermate nuove (`opera`, skin archivi).
- `tools/patch_dossier4.py`, `tools/build_4.sh` — iniezione e build.

**Da modificare**
| Modulo | Modifica |
|---|---|
| `tools/atlas2.js` | registrazione schermata `opera`; `renderChar` adattivo; `drawResults` (normalizzazione, attori, filtri); `GRP`/portali: nessuna voce nuova |
| `tools/net_module.js` | `tvaGo('item')`: aggiunta di un'opzione per il Dossier Opera (comportamento attuale mantenuto come predefinito finché non decidi D1); breadcrumb dallo stack |
| `tools/archivi.js` | skin per tipo, backlinks opere→archivi per tutte le opere con dato, chip personaggio→attore |
| `tools/scheda.js` | filmografia attore; link dalla scheda attore |
| `tools/dossier.js` / `universe_model.js` | solo ponti «Opera» dai titoli del dossier universo (senza cambiare ordine/dati) |
| `tools/atlas2.css` | variabili/skin condivise |
| `tools/patch_fase1.py` | build id |

**Da NON toccare:** `map3b.js`, blocco `CRON3C`, `cron3c.js`, `homev2.js`, `home2.css`, la Home Marvel e la Home TVA; dati canonici (`atlasData`, `altTimelineData`, `relationshipGraphData`, `mvMapData`); logica di progressi, XP, badge, missioni, Firebase, Friends, Live Room; `WATCH_ORDER_JS`/dipendenze. Ponti verso 3B/3C usano le API esistenti (`openMappa`, `crOpen`/`tvaTime`).

---

## 10. Decisioni che ti chiedo

| # | Decisione | Raccomandazione |
|---|---|---|
| **D1** | Il chip «N°» da un personaggio apre il **Dossier Opera** (con «Scheda in guida» a portata) o continua ad aprire la scheda Timeline? | Dossier Opera di default, scheda in guida come pulsante primario sempre visibile |
| **D2** | Il Dossier Opera mostra lo stato **Visto** (sola lettura) e il pulsante di spunta, o solo il rimando alla scheda in guida? | Solo lettura + rimando: la spunta resta in un unico posto, niente doppia scrittura |
| **D3** | Candidati «stesso individuo» (somiglianza dei nomi di pagina, es. Ross ×3, MJ ×3, Phil Coulson/Coulson, Janet/Janet Van Dyne): vuoi che ti prepari un elenco da confermare, con le prove presenti nelle schede? | Sì, elenco a parte; nessuna unione senza tua conferma (e senza toccare gli ID) |
| **D4** | Voce «titoli con il nome dell'organizzazione nel titolo» (es. 7 serie *Agents of S.H.I.E.L.D.*), dichiarata **derivata** | Sì, ma separata dai titoli confermati della guida |
| **D5** | Ordine degli sprint: A → B → C → D come proposto, oppure prima l'identità visiva (D)? | A → B → C → D |
| **D6** | Gli asset grafici (§7): li produci tu/un tool esterno oppure partiamo con i soli motivi SVG? | Partire con SVG; asset in un secondo momento |

---

## 11. Rischi e cosa non farà la Fase 4

- **Rischio principale:** il router (`tvaGo('item')`) è il cuore della navigazione; ogni modifica è dietro opzione e con test di stack (§8, punto 4).
- **Dati radi:** molte schede resteranno brevi; è corretto così e verrà dichiarato nell'interfaccia.
- **Non farà:** nuovi archivi, nuovi dati, relazioni dedotte, unione di personaggi, modifiche a Home, Mappa 3B, Cronologie 3C, progressi, XP, badge, missioni, Firebase, Friends o Live Room.

**In attesa della tua approvazione (e delle decisioni D1–D6) prima di scrivere codice.**
