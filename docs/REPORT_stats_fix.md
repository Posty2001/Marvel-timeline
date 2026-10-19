# Report test — correzione statistiche intro (build 20261018-1630-stats-fix)

Sorgente unica: `tvaAtlas2.stats()` (Home e introduzione). Valori: universi 27 · personaggi 300 · titoli della Timeline 138 · opere totali 176 (138 + 1 variante + 37 animate).
Intro: 5 statistiche con etichette esplicite («opere totali (con varianti e serie animate)», «titoli della Timeline»); il testo statico resta solo come riserva se i dati non sono disponibili. «~527 ore» invariato: la sorgente non è ancora verificata.
Home: invariata (solo uso di stats()).
404: gli 8 asset opzionali assenti generano al massimo 1 richiesta 404 per build; poi l'assenza è ricordata (localStorage per build id) e non si ripete. Nuovi file ritrovati alla build successiva o con tvaAtlas2.img.reprobe().

Test: stats_fix_test (build id, stats()=27/300/138/176, intro=stats(), intro=Home, etichette, reload senza 404, caricamento asset dopo reprobe) 0 fallimenti · home2_test (15 portali, back, ricerca, overflow 320–430, reduced motion, slot asset) 0 · intro_scenes, lm_test, nav_test, a2_test, leg_test, rel_test, tree_arti_test, rs_test, ios (288 controlli): 0 fallimenti.
Test aggiornati perché fissavano i vecchi valori errati (26/304, 4 statistiche) o il vecchio pulsante «Tutti gli archivi».
Limiti: verifica solo su Chromium; da provare su iPhone reale.
