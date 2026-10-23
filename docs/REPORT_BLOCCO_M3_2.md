# TVA Archives — M3.2 · UI Timeline mobile (build 20261023-1400-m32)

**Non pubblicata:** nessun commit, push o deploy. Firebase, dati, progressi, XP, ricompense, cronologia, ordine X-Men, Deadpool & Wolverine e TVA Friends non toccati.

## Modifiche applicate
| # | Richiesta | Esito |
|---|---|---|
| 1 | Stelle sempre visibili, anche a scheda chiusa | Fatto: il controllo è nella riga principale, sotto titolo/anno/badge. |
| 2 | Comportamento del voto | Logica invariata (nessuna riga di salvataggio toccata): 1° tocco = intero, 2° sulla stessa stella = −0,5, 3° = ripristino intero, stella diversa = intero. Verificati anche persistenza dopo ricarica, tastiera (frecce, cifre), Azzera, ruolo `slider` con `aria-valuenow/valuetext/labelledby`. |
| 3 | Un solo riquadro | Fatto: 139 schede = 139 controlli, 0 nel pannello. Stessa istanza, stessi listener: nessun doppio salvataggio. I gesti sulle stelle (tocco, tastiera, Azzera) non aprono/chiudono la scheda. |
| 4 | Locandina nella riga principale | Fatto per le 131 schede con locandina: a sinistra del titolo, 52×78 px (2:3), caricamento lazy, srcset 1x/2x, priorità personalizzata → TMDB → emblema. Tap sulla locandina apre/chiude. Rimossa la miniatura dal pannello. |
| 5 | Funzioni esistenti | Checkbox, preferiti, badge, numero opera, anno, apertura/chiusura verificati. |
| 6 | Sezioni | Verificato: la Timeline contiene solo percorso di visione (copertina, indice, filtri, schede). «Cosa guardo stasera», dashboard e missioni sono in **Centrale TVA** (Strumenti/Missioni); Confronta in Atlante e Friends; statistiche e voto medio in Home. Nessuno spostamento necessario. |
| 7 | Reliquiario nell'Atlante | Aggiunta la voce «Reliquiario» (15ª) in «Reliquie e Arti Arcane», che apre la schermata già esistente; nessun contenuto duplicato; il portale in Home Atlante resta. |
| 8 | Allineamento / overflow | Audit a 390/360/320 px: trovata e corretta una mia regressione a 320 px (stelle oltre il bordo → pagina allargata); ora nessun overflow. A ≤360 px locandina 42×63 e stelle a tutta larghezza. Intestazioni invariate. Applicato un riordino di riga anno + badge sulla stessa linea per schede più compatte. |

## Senza locandina
Il fallback è il layout originale (emblema), senza spazi vuoti: 7 titoli (The Defenders, Punisher S1/S2, Team Thor, Holiday Special, I Am Groot, FF First Steps).

## Test
`m32_test.py` 33/33 (voto, a11y, persistenza, overflow 390/360/320, fallback, Reliquiario). Regressioni (tutte verdi): m3 16/16, m31 15/15, m21 15/15, m1 14/14, rs 33, stats_fix 12, b321 38, home2 49, leg 37, lm 87, data 5, r320 0 fallimenti. Il test legacy `tva_test` ha 3+ controlli obsoleti (sezione Cronologie, Atlante chiuso) che falliscono identici anche sulla build precedente: non collegati a M3.2. Aggiornati test obsoleti per modifiche volute: tva_test G1 (14→15 voci Atlante), m31 (miniatura ora nella riga principale).

## Da verificare su iPhone reale
- Tocco vero sulle stelle (nessuna apertura accidentale) e scorrimento con il dito sopra le stelle.
- Resa delle locandine TMDB su rete mobile e con «Risparmio dati».
- Altezza schede con testo grande (Dynamic Type) e Safari con barra in basso.
- Attribuzione TMDB: resta nel dossier Opera; nella Timeline non compare per spazio (valuta una nota nei crediti).
