# Report — Nuovo ordine di visione editoriale X-Men (Fox)

Build id: `20261019-0600-xmen-ordine` (base: 3C `20261019-0200-cronologie`). Fase separata, nessuna nuova fase avviata.

## 1. Sequenza definitiva (ordine di visione editoriale, NON cronologia canonica)

| Pos. guida | N° visibile | ID stabile | Titolo |
|---|---|---|---|
| 1 | 012 | item-012 | X-Men: First Class |
| 2 | 013 | item-018 | X-Men Origins: Wolverine |
| 3 | 014 | item-015 | X-Men |
| 4 | 015 | item-016 | X2 |
| 5 | 016 | item-017 | X-Men: The Last Stand |
| 6 | 017 | item-019 | The Wolverine |
| 7 | 018 | item-013 | X-Men: Days of Future Past |
| 8 | 019 | item-014 | X-Men: Apocalypse |
| 9 | 020 | item-020 | Dark Phoenix |
| 10 | 021 | item-021 | The New Mutants |
| 11 | 022 | item-022 | Deadpool |
| 12 | 023 | item-024 | Logan |
| 13 | 024 | item-023 | Deadpool 2 |

Deadpool & Wolverine (ID 117) resta nella sua posizione nella guida generale (non toccato; solo l'ordine interno della sua lista di dipendenze Fox segue il nuovo ordine).
Gli ID delle schede non sono mai cambiati: cambia solo la posizione e il N° visibile (derivato dalla posizione).

## 2. Fonte di verità
- `tools/xmen_order.json` (13 ID in ordine) usato da `patch_xmen_order.py` e dai test.
- A runtime: l'ordine DOM della guida; helper globale `marvelPosizioneGuida(id)` più `marvelNumeroVisibile/IdDaNumeroVisibile`. I moduli (atlas2, dossier, map3b, universe_model, archivi, scheda, net_module) usano questi helper, con fallback derivato dal DOM perché eseguiti prima dello script principale. Nessuna copia divergente della sequenza.

## 3. File modificati
- `index.html` (build finale)
- Nuovi: `tools/patch_xmen_order.py`, `tools/xmen_order.json`
- Modificati: `tools/atlas2.js`, `dossier.js`, `map3b.js`, `universe_model.js`, `archivi.js`, `scheda.js`, `net_module.js` (backup `*.pre_xm.js`), `tools/patch_fase1.py` (build id)

## 4. Sezioni e dipendenze verificate/aggiornate
Aggiornate automaticamente:
- Guida principale: riordino dei 13 `<li>` Fox (nessuna scheda cancellata/ricreata; attributi e ID identici sulle 138 schede statiche).
- 62 riferimenti «N°» rimappati (28 invariati, 1 tick d'asse UT volutamente escluso); 2 correzioni di etichette attore (Alan Cumming → N°015, Beast → N°016).
- Schede personaggio: righe PRIMA/ULTIMA/ALTRE APP. ricalcolate (modello riprodotto su tutte le 109 schede originali); 7 riordinate: Ciclope, Jean Grey/Fenice, Magneto, Sabretooth, William Stryker, Wolverine, Xavier.
- «Prossimo titolo» / «Cosa guardo stasera»: `WATCH_ORDER_JS`, `DEPENDENCY_MAP_JS` (liste Fox ordinate), priorità e prerequisiti invariati.
- Timeline alternativa (modalità consigliato/saga/studio seguono la guida); `atlasData.opere`, `altTimelineData`, `mvMapData`.
- Dossier 3A «Ordine della guida», mappa 3B (scheda “visti N su 14”, pulsante Cronologia), cronologie 3C e Esploratore temporale (chip e ricerca N°), pagine personaggio, archivi, scheda.
- Note editoriali: blocco «Perché questo ordine» di Logan riscritto, note di Deadpool/Deadpool 2/Logan, nuovo blocco su DOFP, nota «ORDINE DI VISIONE» dopo la sezione Fox (ordine editoriale, non cronologia canonica; D&W resta nella sezione MCU).
- Collegamenti N°: ora risolti per ID (corretto anche un bug 3C preesistente per cui Logan/Deadpool mostravano l'ID come N° o aprivano la scheda sbagliata).

Verificate e NON modificate (per progettazione): ordinamenti per uscita e per ambientazione (identici su tutte le 27 universi e nella Timeline alternativa), progressi, preferiti, note, voti, XP/badge/missioni, Firebase, Amici/Live Room, relazioni canoniche tra universi, classificazioni/priorità.

## 5. Test
- `xm_test.py`: 122 PASS / 0 FAIL — copre i 10 test richiesti: (1) 13 titoli in ordine; (2) nessun duplicato/mancante; (3) adiacenze precedente/successivo (la guida non ha una funzione Prev/Next esplicita: testata l'adiacenza dei prerequisiti e dei link); (4) etichette, numerazione, suggerimenti; (5) coerenza 3A/3B/3C; (6) sort per uscita/ambientazione identici; (7) 11 scenari «Prossimo titolo» con utente che ha visto film X-Men, confrontati con algoritmo indipendente; (8) progressi legati agli stessi ID (localStorage identico tra 3C e nuova build); (9) regressione; (10) D&W invariato.
- `xm_extra.py`: soglia spoiler segue il N° visibile (posizione), nessun errore JS.
- Regressione completa (suite 3C, 3B, 3A, home, nav, import/export, crittografia, modalità, link, ui, ecc.) confrontata con la baseline 3C: nessun nuovo fallimento funzionale. Nuovi “fail” solo nei test che per costruzione verificano l'ordine/numerazione precedente: sorgenti invariate `atlasData`/`altTimelineData`/`mvMapData`, «card-wrap/622 schede invariate» (cambiano 10 schede item e 24 schede personaggio, come previsto), `xm.py` (12, attendeva solo Logan spostato), `g3.py` (Patrick Stewart ora N°014 invece di N°015: corretto col nuovo ordine).
- Fallimenti preesistenti, invariati: in1/in2 (intro su schermi piccoli), tva_test A8/A9, r320 «home decor», ui_audit controlli Home, g2 (tessera, reg.py), net_test, uf_test (dipendente dall'ora).
- Suite cronologie 3C sulla nuova build: cron3c_test 113/0, cron3c_vp 372/0, cron3c_touch 25/0, consistenza Timeline Eventi vs tvaTime 138 righe, 0 differenze.

## 6. Incoerenze residue / limiti
- Le categorie `xmen` mancano su X2, Dark Phoenix e New Mutants (preesistente, non toccata).
- «Prossimo titolo» usa priorità per livello (verde→blu→giallo→rosso), quindi non è strettamente sequenziale (preesistente).
- Nessuna funzione esplicita Precedente/Successivo: verificata l'adiacenza.
- La ricerca Atlante non cerca per numero.
- «Prossimo titolo comune» in Amici verificato solo per lettura del codice (usa l'ordine DOM).
- La soglia spoiler è basata sulla posizione per scelta.
- Testato solo Chromium con touch emulato: verifica su iPhone a carico tuo.
