# Intro a vista singola (build 20261018-0930-intro-single)

## Elementi della vecchia introduzione
ATTO I = copertina (resta, ora è l'illustrazione). Fuori dal flusso visibile (display:none, DOM e ID intatti):
- ATTO II «Il Multiverso si espande»: 4 statistiche + nota (valori calcolati dai dati reali)
- ATTO III «Il futuro del Multiverso»: countdown #icdDoomsday / #icdSecretWars
- ATTO IV «Il portale TVA»: pulsante #lmTvaPortal + quiz «da dove inizio» (#quizGoBtn)
- indicatore di scroll (lm-cue)
Nessun dato o logica è stato cancellato; countdown e statistiche continuano a essere calcolati.

## Correzione (mirata, solo #intro)
- `#intro .lm-lower, .lm-cue { display:none }` → niente contenuto sotto la copertina, niente focus da tastiera nei contenuti nascosti.
- Con illustrazione attiva: `#intro .lm-scroll { overflow:hidden; overscroll-behavior:none }` e `touch-action:none` solo su #intro; scrollTop forzato a 0.
- Nessun overflow:hidden globale su html/body: Home e TVA Archives scorrono come prima.
- Se l'immagine non carica: fallback SVG, sempre senza atti II–IV (scroll interno solo se lo schermo è troppo basso).

## Test (Chromium, touch emulato)
intro_single (110 controlli, 0 fallimenti) su 320×568, 360×640, 375×667, 390×844, 430×932, ciascuno anche con safe area simulata (top 59 / bottom 34): copertina unica; Atti II–IV non visibili; scrollHeight = clientHeight; dopo wheel, swipe touch, PageDown/End/Space e scrollTop forzato nulla si sposta; Tab non entra nei contenuti nascosti; un solo pulsante visibile; «Inizia il viaggio» → onboarding → Home; Home e TVA Archives scorrono; riapertura della copertina da Home/Atlante: vista singola, scroll 0, scroll bloccato, pulsante di nuovo funzionante; nessun errore JS.
Regressione: rs_test 33/33, nav_test 29/29, leg_test 0 fail, a2_test 0 fail, lm_test 0 fail, in1_fb ALL_PASS, ios.py 272/288 (16 = vecchi controlli sull'intro già noti, invariati).
Test aggiornati perché descrivevano comportamenti ora superati: lm_test (portale, quiz, parallasse da scroll ora verificati come «nascosti/bloccati»), in1/in1_fb (griglia statistiche), rs_test (build id). Nota: in in1/in1_fb il controllo sulle statistiche è ora solo informativo; la verifica vera è in intro_single.

## Da verificare su iPhone reale
Gesto di swipe sulla copertina (rimbalzo elastico/overscroll), barra di Safari che cambia altezza, PWA a schermo intero con la safe area reale.

## Conseguenza da sapere
Il portale «Esplora TVA Archives» e il quiz «da dove inizio» non sono più visibili dall'ingresso. L'Atlante resta raggiungibile da Home e dalla tab; il quiz non ha al momento un'altra entrata (logica conservata, si può riproporre in Home).

Deploy: sostituisci solo `index.html` nel repository (stesso nome); build id atteso 20261018-0930-intro-single.
