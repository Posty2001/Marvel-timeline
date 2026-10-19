# Chiusura audit X-Men — report finale

Build: `20261019-0900-xmen-chiusura` (precedente `20261019-0600-xmen-ordine`). Nessuna Fase 4, nessuna nuova funzionalità.

## 1. Problemi effettivamente trovati

| # | Problema | Effetto reale |
|---|---|---|
| P1 | **Categoria `xmen` mancante** su X2 (016), Dark Phoenix (020), The New Mutants (021). | La categoria è usata da: contatore «X-Men» della dashboard, DNA Marvel (% per categoria), pool della missione tematica settimanale («Guarda un titolo degli X-Men»). Quei 3 film non venivano contati né validi per la missione. Il denominatore statico era anche sbagliato (13 invece di 14 prima, 17 ora). Non c'era alcun impatto su filtri, ricerche, dossier, archivi e suggerimenti (non leggono `data-cats`). |
| P2 | Test che fallivano solo per la vecchia numerazione/ordine | `d3a_test` (3 sorgenti dati + conteggio `card-wrap`), `data_test`, `xm.py` (12), `g3.py` (1), `xm_test` (2, dovute a P1), `rs_test`/`stats_fix_test` (build id). Nessun difetto del prodotto. |
| — | «Prossimo titolo» e «Cosa guardo stasera» | **Nessuna incoerenza trovata.** Vedi punto 2. |
| — | «Prossimo titolo comune» (Amici) | **Nessuna incoerenza trovata.** Vedi punto 3. |

## 2. Correzioni applicate e file modificati
- `tools/patch_xmen_cat.py` (nuovo, idempotente): aggiunge la categoria **già esistente** `xmen` a 016/020/021 sia sul `<li data-cats>` sia sulla checkbox, e allinea il denominatore statico (=17: 13 Fox + D&W + X-Men '97 S1/S2/S3). Nessuna categoria nuova o duplicata; le altre appartenenze non cambiano (verificato per tutte le 138 schede).
- `index.html`: 7 modifiche (6 attributi `data-cats`, 1 denominatore) + build id.
- `tools/patch_fase1.py`: build id.
- Effetto sulle missioni: la missione tematica «X-Men» ora accetta anche X2, Dark Phoenix, New Mutants. Ricompense già assegnate, XP, badge, progressi non vengono toccati.
- Test aggiornati (nessun controllo eliminato o disattivato): `d3a_test.py`, `data_test.py`, `xm.py`, `g3.py`, `xm_test.py`, `rs_test.py`, `stats_fix_test.py`. Nuovo: `xm_close_test.py`.

## 3. Verifica dei suggerimenti (nessuna modifica necessaria)
Codice: entrambi i sistemi scorrono `WATCH_ORDER_JS` (= ordine della guida, già nel nuovo ordine) per livello verde→blu→giallo→rosso, con prerequisiti diretti e Dependency Map. A parità di livello «Prossimo titolo» sceglie il primo in ordine di guida, quindi la sequenza editoriale. «Cosa guardo stasera» sceglie **a caso** nel pool del livello attivo: è la regola esistente, non una scelta d'ordine, e non è stata cambiata.

Test funzionali (`xm_close_test.py`, browser, dati simulati, confronto con un algoritmo indipendente):
- 15 scenari mirati (nulla visto, progressi parziali, solo Logan, solo Deadpool 2, vecchio ordine, verdi completi, rimasti solo rossi, ecc.) + 14 scenari casuali con seed fisso: «Prossimo titolo» identico all'atteso in tutti; ogni proposta di «Stasera» appartiene al pool atteso (60 estrazioni) e il pool viene esplorato per intero.
- Priorità Fox: verdi 012, 015, 016, 022, 024, 023 · blu 019, 013 · gialli 018, 017, 014 · rossi 020, 021. Ne risulta, ad esempio: First Class → X-Men → X2 → Deadpool → Logan → Deadpool 2 → The Wolverine → DOFP → …; un livello inferiore non anticipa mai uno superiore (comportamento esistente, invariato).

## 4. Prossimo titolo comune — Amici/Gruppi (test funzionale)
Il confronto Amici/Gruppo e la Live Room condividono `renderCompareResultGenerica`. I gruppi vivono in localStorage del browser: ho creato gruppi simulati in contesti browser isolati (nessun dato reale, nessun Firebase) con 8 casi: nessuno ha visto nulla; due utenti con progressi diversi; Logan vs Deadpool 2; un utente col vecchio ordine e uno col nuovo; tutti i Fox visti da uno solo; tutto visto da entrambi.
- Il titolo «che nessuno dei due ha ancora visto» è il primo non visto da nessuno dei due nell'ordine della guida (quindi nel nuovo ordine X-Men; dopo i Fox, D&W al suo posto).
- Gli elenchi «solo A / solo B» sono corretti; i dati dei due utenti (localStorage) non vengono modificati dal confronto; nessun errore JS.
- Verificato in locale: la logica condivisa. **Non verificato:** sincronizzazione Firebase della Live Room (nessun ambiente Firebase di test). La logica di confronto è la stessa funzione, ma la lettura dei dati remoti non è stata eseguita.
- Limite noto (preesistente, non modificato): il «prossimo comune» segue solo l'ordine di guida, senza priorità per livello né controllo di uscita. Non l'ho cambiato perché la regola attuale è documentata nel codice e non riguarda l'ordine X-Men.

## 5. Test
**Superati (nuovi/aggiornati):** `xm_close_test.py` 134/0 · `xm_test.py` 122/0 · `xm.py` 32/0 · `g3.py` 0 fallimenti · `data_test.py` 0 · `d3a_test` aggiornato (sorgenti confrontate in forma canonica, N° normalizzati; l'ordine è coperto da `xm_test`) · cronologie 3C: `cron3c_test` 113/0, `cron3c_vp` 372/0, `cron3c_touch` 25/0, consistenza Timeline Eventi 138 righe, 0 differenze · `rs_test` 33/0 e `stats_fix_test` 0 fallimenti (build id aggiornato).

**Test aggiornati per la nuova sequenza** (solo aspettative): numerazione e ordine in `xm.py`/`g3.py`; sorgenti dati e conteggio `card-wrap` (ora elementi `<li class="card-wrap">`, le stringhe JS aggiunte nei moduli non contano) in `d3a_test`; `data_test` ammette solo variazioni dichiarate (solo N°, stesse parole in ordine diverso, 13 schede Fox, 7 personaggi ricalcolati); data-cats 016/020/021 in `xm_test`; build id in `rs_test`/`stats_fix_test`.

**Fallimenti preesistenti (identici alla baseline 3C):** in1/in2 (intro su schermi piccoli), tva_test A8/A9, r320 «home decor», ui_audit controlli Home, g2 (tessera, in reg.py → «REGRESSIONE FALLITA» come prima), net_test, uf_test (dipende dall'ora).

**Nuovi difetti:** nessuno. Un test (`d3.py`, scenario A) è fallito una volta nella suite completa (preparazione dello stato a campione casuale) e passa 3 volte su 3 alla riesecuzione: instabile per costruzione, non collegato alla modifica.

**Non eseguibili:** Firebase/Live Room reali; iPhone reale (solo Chromium con touch emulato).

## 6. Regressione finale
Invariati (verificati dai test sopra e dalla suite completa): ID schede; progressi, preferiti, note, voti (localStorage identico tra 3C e nuova build); XP/badge/missioni (nessun premio ritirato o duplicato); ordine per uscita e per ambientazione (identico su tutti i 27 universi e nella Timeline alternativa); altre saghe e MCU; posizione di D&W (indice DOM e N° 117); Dossier 3A, Mappa 3B, Cronologie 3C (nessuna modifica in questa fase).

## 7. Limiti residui
- Firebase/Live Room e iPhone reale non verificati (vedi sopra).
- «Cosa guardo stasera» resta casuale dentro il livello di priorità (regola esistente).
- «Prossimo comune» in Amici ignora priorità e uscita (regola esistente).
- Nessuna funzione Precedente/Successivo esplicita nella guida.

## 8. Conferma
**La modifica X-Men è conclusa.** Non restano incoerenze note derivanti dal nuovo ordine; i limiti elencati sono comportamenti preesistenti o verifiche non eseguibili in questo ambiente.
