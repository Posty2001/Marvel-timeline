# TVA Archives — M3.4 Home «TVA Hybrid»
Build 20261023-1600-m34. Nessun commit/push/deploy.

| Punto | Esito |
|---|---|
| Header: «Bentornato, Variante», % complessiva, barra | OK |
| Prossimo titolo: locandina TMDB a sinistra, titolo, anno · universo, CTA (Inizia/Continua) | OK, dati reali; fallback emblema se manca/TMDB off |
| 3 statistiche: titoli completati (n/138), ore viste, voto medio | OK |
| 2 accessi: Atlante, Tessera TVA | OK |
| 1 missione attiva + «Centrale TVA →»; stati vuoti (tutte completate / nessuna valida) | OK |
| Rimossi dalla Home: Rango, Prossimo badge, Serie attiva, Continua, 7 pulsanti, card Atlante grande, vecchia scheda missioni | funzioni ancora in Timeline/Tessera/Atlante/menu |
| 320/360/390 px: niente overflow, Home tutta sopra la tab bar | OK |

## Correzioni alla fonte
1. **Voto medio vuoto al caricamento** (e dopo import profilo): la prima `updateHomeHubSummary()` girava prima che `RATINGS_KEY` fosse inizializzata → leggeva 0 voti. Ora si ricalcola subito dopo. Verificato: aggiornamento al caricamento, dopo un voto, azzeramento, altro profilo.
2. **Missioni «—»**: la prima `updateMissioni()` usciva perché `marvelGetAltTimelineData` non esisteva ancora (tematica e saga restavano «—», 14 settimane su 14). Ora viene richiamata a dati pronti **in sola lettura**: nessuna ricompensa/XP/snapshot/celebrazione al caricamento (localStorage identico alla build precedente). Nessun testo inventato.

## Test
m34_test 35/35 (incl. prossimo titolo su 8 avanzamenti: mai già visto, obbligatori prima, aggiornamento Home). Regressioni OK: cap0, m32, m31, m3, rs, stats_fix, b321, home2, leg, m21, m1.
`rs_test` aggiornato di proposito alla nuova gerarchia Home (copia originale: rs_test.pre_m34.py). `tva_test`: stessi 8 FAIL preesistenti + stesso stop al blocco J (identico alla build precedente).

## Note / da verificare
- «Prossimo titolo» usa la logica esistente (priorità obbligatorio→consigliato→…, prerequisiti, uscita dei titoli); non legge l'ordine personalizzato della Timeline alternativa (comportamento già presente, non modificato).
- Universo mostrato = studio della scheda (MCU, Sony's Spider-Man, Fox-Verse, Legacy, Animazione).
- Il voto medio ora mostra «Nessun voto» (prima «Ancora nessun voto», troppo lungo in 3 colonne).
- Da provare su iPhone reale: tap su locandina/CTA, Atlante, Tessera, Centrale TVA.
