# Report – Grafo delle Relazioni, Alberi genealogici, Arti Mistiche
Build: `20261018-1100-rel-trees-arti` (sostituire solo `index.html` nel repository)

## Cause individuate
**Relazioni**: anello unico non limitato (nodi Universo/Organizzazione con centinaia di collegamenti), etichette sotto i nodi che si sovrapponevano, nessun messaggio con zero risultati, il pannello ignorava i filtri. Il filtro «Titolo» in realtà rappresenta le co-apparizioni tra personaggi (non esistono nodi-titolo).
**Alberi**: erano solo elenchi di schede testuali (nessun diagramma).
**Arti Mistiche**: limite di *soglia* (≥3 schede) più dati effettivamente scarsi: solo Stregoneria supera la soglia; Magia oscura ha 2 schede, Magia del caos 2 personaggi; Magia runica, Magia asgardiana (seidr) e «Maestri delle Arti Mistiche» hanno 0 schede.

## Correzioni
- **Relazioni**: layout a due colonne con etichette accanto ai nodi, archi colorati per tipo (tratteggio = co-apparizione), «Mostra altri» (14 per pagina), badge con il numero di collegamenti per filtro, messaggi espliciti per zero risultati / nessun filtro, pan, pinch, pulsanti zoom e selezione nodo mantenuti. Nessuna relazione inventata.
- **Alberi**: diagrammi SVG interattivi (matrimonio = doppia linea, genitore→figlio = linea piena, adottivo = tratteggio, compagno/a = tratteggio rosa, fratelli = punteggiato), generazioni etichettate, pan/zoom, tocco su persona = dossier, continuità separate, dettagli testuali conservati sotto. Gruppi: Fantastic Four, Asgard, Wakanda, Stark.
- **Arti**: 3 discipline documentate (Stregoneria; Magia oscura e Magia del caos marcate «dati limitati»), box «cercate ma non documentate» con le 3 lacune, dossier con Definizione, personaggi, titoli, universo, artefatti associati (vuoto dichiarato).

## Test (Chromium, 390 px e altri viewport)
rel_test 0 fallimenti (filtri singoli e combinati per ognuno dei 7 tipi, zero risultati, badge, nessuna sovrapposizione di etichette, paginazione, zoom, selezione, assenza di scroll orizzontale) · tree_arti_test 0 fallimenti · leg_test, rs_test 33/33, nav_test 29/29, lm_test, a2_test, intro_single, in1_fb: 0 fallimenti · ios.py 272/288 (16 noti, solo controlli intro).

## Limiti e dati da verificare
- Alberi: solo dati MCU; le continuità Legacy/alternative non hanno dati strutturati e non sono rappresentate. FF = MCU + Earth-828 (First Steps). Il diagramma FF a vista intera è piccolo: i ruoli compaiono a zoom ≥1,5.
- Relazioni: la direzione delle relazioni familiari nei dati è ambigua («Padre» in entrambi i versi); i dati «Variante» sono sospetti (Loki ↔ Jane Foster/Mighty Thor); personaggi duplicati (Mary Jane Watson / Mary Jane / MJ).
- Arti: Magia runica, seidr asgardiano e Maestri delle Arti Mistiche non hanno schede. Proposta: aggiungere un campo «tradizione magica» nelle schede di personaggi e artefatti. Magia oscura non ha titoli verificati.
- Da verificare su Safari/iPhone reale: gesti pinch/trascinamento, touch-action, safe area (testati solo con Chromium).
- Il patch del grafo relazioni è applicato direttamente in `index.html` (blocco `RG-LAYOUT`, sorgente in `tools/relgraph_new.js`): `index.html` è la fonte di riferimento.
