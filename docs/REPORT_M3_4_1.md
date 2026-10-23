# M3.4.1 — «Prossimo titolo» e Timeline attiva (build 20261023-1700-m341)
Nessun commit/push/deploy.

**Come l'app salva la Timeline:** solo l'ordine personalizzato (`marvelGuideCustomTimelineOrder`, elenco di numeri scheda). La modalità scelta (Consigliato/Uscita/…/Personalizzato) NON era salvata: era solo una vista dell'overlay, azzerata a ogni apertura.
**Modifica:** nuova chiave locale `marvelGuideActiveTimelineMode` (`custom`|`standard`), scritta al tocco su un pulsante modalità; non entra in profilo/sync/Firebase.

- Standard (o nessuna modalità salvata): logica invariata.
- Personalizzata: primo titolo non visto nella sequenza salvata, con gli stessi vincoli (uscita disponibile, prerequisiti → suggerisce il prerequisito mancante, bloccati saltati). Titoli non presenti nell'ordine salvato in coda; numeri mancanti/duplicati/non validi ignorati.
- Sequenza vuota o corrotta → comportamento standard. Percorso completato → «Tutto visto!», CTA nascosta.
- Home aggiornata subito su: cambio modalità, riordino con le frecce, completamento titolo, evento `storage` (altra scheda).
- L'alt timeline si riapre sulla modalità salvata.
- «Inizia»/«Continua» aprono esattamente il titolo mostrato.

**Test:** m341_test 20/20 (standard, personalizzata, cambio modalità, riordino, persistenza, CTA, mancanti/vuota/corrotta/parziale, completato, storage; progressi/voti/XP invariati). Regressioni OK: m34, cap0, m32, m3, rs, stats_fix, b321, home2, leg, m21, m1.

**Da sapere:** la card «Cosa guardo dopo» della Timeline usa ancora la logica standard (fuori ambito). Una sequenza personalizzata vuota usa lo standard anziché l'ordine consigliato.
