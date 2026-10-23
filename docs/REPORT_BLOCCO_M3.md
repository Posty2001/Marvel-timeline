# TVA Archives — Blocco M3 (build 20261023-1000-m3)

Nessun commit/push/deploy. Firebase e dati remoti non toccati. Progressi, valutazioni, ricompense e ordini personalizzati non modificati.

## 1. Atlante — verifica delle sezioni e dei collegamenti
| Verifica | Esito |
|---|---|
| Catalogo Atlante: 14 sezioni nel catalogo + portale «Reliquiario» (15°) solo in Home | invariato, nessuna sezione nuova |
| 93 dossier d'archivio (org 17, art 16, evt 7, luo 16, cos 26, spe 8, mis 3) | tutti apribili, nessun errore JS |
| Titoli collegati non risolvibili | 0 |
| Voci senza alcun collegamento | 7, tutte entità cosmiche solo-fumetti (L'Uno al di sopra di tutti, Molecule Man, Immortus, Shuma-Gorath, The Stranger, Hyperion, Nova) |
| Messaggio mostrato sulle 7 voci | già esplicito: «Mai apparsa sullo schermo nei titoli di questa guida» |

**Decisione:** nessun collegamento aggiunto. Per quelle 7 voci la guida non contiene titoli, universi o citazioni; collegarle sarebbe inventare dati. Lo stato attuale (dossier onesto + nota) è il comportamento corretto.

## 2. Cronologie — titoli post-Endgame senza anno
- Nell'ordinamento per ambientazione i titoli senza anno ufficiale seguono ora l'ordine della timeline Disney+ (`posizioneDisney`), non più l'ordine di guida.
- Etichetta: «· pos. N/18 timeline Disney+ (ordine)» al posto di «(senza anno)»; stessa etichetta nelle colonne di confronto.
- Anno di uscita, ambientazione e ordine di visione restano tre campi distinti; gli ordini personalizzati non sono toccati.
- Dossier Opera: sotto l'ambientazione compare «posizione N di 18 tra i titoli post-Endgame (timeline Disney+: ordine, non data)».

## 3. Homecoming (N°075)
- Ambientazione: «New York, dopo la battaglia di New York (post-Avengers; anno non determinabile)».
- Nuova riga scheda «NOTA DI CONTINUITÀ» + campo `notaContinuita`: la didascalia «otto anni dopo» è un'incongruenza di continuità, non un riferimento cronologico, e non viene usata per datare il titolo (anno = nessuno).

## 4. Immagini — sistema ID → file (nessuna immagine scelta)
- Cartella: `assets/images/catalog/<kind>__<id>.webp` (es. `item__075.webp`, `chr__char-thanos.webp`). kind: item, anim, chr, uni, evt, luo, org, art, cos, spe, mis.
- Registro: `assets/images/catalog/manifest.json` (vuoto), incorporato nella build come `imageManifest` e fuso nel registro già esistente `TVA_IMG_MANIFEST` (usato da personaggi/universi/archivi).
- Regola di sicurezza invariata: una voce è usata solo con `licence` e `verified:true`; se il file manca resta l'emblema.
- Nuovo aggancio: locandina nel Dossier Opera (chiave `item:<ID>` / `anim:<ID>`).
- Strumento: `tools/img_catalog.py list|scan|register` (legge w/h dal file; `verified` solo con `--verify`).
- **Decisione tua:** per ogni immagine che fornirai servono licenza/credito (e conferma dei diritti). Finché non li indichi la voce resta non verificata e non compare.

## 5. UI
Nessun problema grafico reale emerso: nessuna modifica oltre al CSS della locandina (`.m3-poster`).

## File modificati
`index.html` (build), `tools/patch_m3.py` (nuovo), `tools/build_4.sh` (+patch_m3), `tools/img_catalog.py` (nuovo), `assets/images/catalog/manifest.json` (nuovo).

## Test mirati
`m3_test.py` 16/16 (build id, 075 testo/nota/anno null, ordine pos Disney+ nel gruppo senza anno, posizione nel dossier, locandina: assente senza voce / non verificata / verificata OK / file mancante con fallback, blob vuoto, nessun errore JS, tool scan/list). Regressioni: m21 15/15 (aggiornato per la modifica voluta di 075), m1 14/14, rs 33/33, stats_fix 12/12, b321 38/38, home2 49/49, leg 37/37, lm 87/87, data_test OK (le righe «FAILS 0» sono il riepilogo, non errori). Patch idempotente (doppia esecuzione = stesso md5).

## Non fatto / aperto
- Locandine e illustrazioni: in attesa dei tuoi file e della licenza.
- Reliquiario resta solo-Home (non nel catalogo Atlante): decisione di prodotto se aggiungerlo al catalogo.
- Test su iPhone/Safari reali e sync cloud: non eseguiti.
Non avviati M4 / TVA Friends.
