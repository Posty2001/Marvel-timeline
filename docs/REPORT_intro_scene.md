# Report – Introduzione cinematografica a scene
Build `20261018-1230-intro-scenes` (sostituire solo `index.html`).

## Contenuti originali recuperati e dove sono
| Originale | Ora |
|---|---|
| Illustrazione MARVEL MULTIVERSE, «Infinite realtà. Un unico viaggio.», «Inizia il viaggio» | Scena I (invariata) |
| «TIME VARIANCE AUTHORITY · ARCHIVIO CENTRALE» | Scena I, riga editoriale in alto (sopra l'illustrazione, su scrim scuro) |
| «TVA ARCHIVE» + «The definitive interactive Marvel viewing experience.» | Scena I, riga discreta in basso, fuori dall'illustrazione |
| Statistiche 176 titoli · 26 universi · 304 personaggi · ~527 ore + icone 🎥🌐👥⏱️ + nota «Numeri calcolati dai dati reali…» | Scena II – Il Multiverso si espande (conteggio animato, valore finale invariato) |
| Contatori giorni a Doomsday (18 dic 2026) / Secret Wars (17 dic 2027), stati OGGI / USCITO | Scena III – Il futuro del Multiverso |
| Quiz «Non sai da dove iniziare?» (2 domande, 3 esiti, «Vai lì →») | Scena IV – Il portale TVA |
| «⚡ ACCESSO ARCHIVIO TVA IN CORSO… ⚡» | Scena IV (con lieve sfarfallio) |
| Portale «Esplora TVA Archives» (aggiunto nella versione Living) | Scena IV: apre direttamente TVA Archives dopo l'onboarding |

Nessun atto V: non esisteva. «THE LIVING MULTIVERSE» (aggiunto da me in precedenza, non originale) non è più visibile, resta nel DOM.

## Funzioni
Swipe (su/giù/sinistra/destra), frecce di navigazione, tocco sull'indicatore, tastiera (frecce, PagDn/PagSu, Home, End), rotella. Indicatore di avanzamento a 4 segmenti (cliccabili). «Inizia il viaggio» sempre disponibile (CTA nell'illustrazione in scena I, pulsante fisso nelle scene II–IV): onboarding → Home senza completare le scene. Ritorno dalla Home: riparte dalla scena I. Scena IV scorre internamente se il quiz aperto non entra nello schermo.
Accessibilità: scene inattive `inert` + `aria-hidden`, annuncio `aria-live` («Atto II di IV: …»), indicatore con `aria-current`, bersagli ≥44 px. Reduced motion: nessuna transizione, numeri subito finali, sfondo fermo. Safe area rispettata. Prestazioni: solo `transform`/`opacity`, sfondo a gradienti CSS (nessuna immagine aggiuntiva), nessun `overflow:hidden` globale.

## Test (Chromium, 320–430 px, con e senza safe area)
intro_scenes 324 PASS / 0 FAIL: testi originali per scena, un solo «Inizia il viaggio» visibile, nessun testo duplicato, scene inattive nascoste, indicatore, statistiche e giorni corretti, quiz raggiungibile, swipe/tasti/rotella/pulsanti, Tab senza focus su scene inattive, Home da ogni scena, ritorno alla copertina, portale → TVA Archives → indietro (pulsante, «Torna all'app», history.back → Home con barra schede), reduced motion. Regressione: rs_test 33/33, nav_test 29/29, lm_test, a2_test, in1_fb, leg_test, rel_test, tree_arti_test: 0 fallimenti; ios.py 288/288 (esentati solo l'illustrazione a tutto schermo e il titolo solo-screen-reader).

## Da verificare su iPhone reale
Gesto di swipe con momentum, rimbalzo di Safari, comportamento del tasto «indietro» in PWA, resa degli emoji nelle statistiche.
