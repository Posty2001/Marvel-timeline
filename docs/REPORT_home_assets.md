# Report — Home TVA con asset definitivi (build 20261018-1800-home-assets)

**Asset:** 8/8 ricevuti e installati in assets/images/tva/. Dimensioni esatte e pesi entro i limiti (hero 249/250 KB, eventi 76/80, luoghi 131/140, specie 129/130, organizzazioni 113/130, universi 124/130, attori 111/120, reliquiario 129/130).
**Modifiche a index.html (solo Home):** (1) hero: l'illustrazione è un'immagine con alto e basso, quindi tolti cerchio e rotazione → dissolvenza verso il basso e deriva lentissima (solo transform; fermo con riduzione movimento); (2) ritagli/zoom delle copertine condivise applicati solo come ripiego: con l'asset dedicato l'immagine è mostrata in cover; (3) puntini-Gemma del Reliquiario rimossi quando l'illustrazione dedicata è caricata (le Gemme sono già nell'immagine); (4) immagini dei portali in lazy-load. 15 portali, disposizione, destinazioni, statistiche, intro: invariati.

**Test (Chromium, Playwright):**
- 15 portali → destinazione corretta e ritorno alla Home: 0 fallimenti (home2_test).
- 8 asset caricati a 390 e 320 px, tutte le copertine naturalWidth>0, object-fit cover (nessuna deformazione), 0 risposte 4xx/5xx, 0 errori JS.
- Contrasto titolo/sfondo ≥ 4,5 su tutti i 15 portali (peggiore: Attori 5,3).
- Fallback: per ciascuno degli 8 asset, simulati 404 e file corrotto → ripiego automatico (copertina condivisa o composizione SVG), senza errori.
- Scorrimento: con CPU rallentata 4× frame p50/p95 16,7 ms, max 33 ms.
- Regressione: intro, Home Marvel/navigazione, lm, a2, leg, rel, alberi/arti, rs, ios (288 controlli): 0 fallimenti. Aggiornati due test obsoleti (copertine SVG ora sostituite).

**Da verificare su iPhone reale (non verificabile qui):** nitidezza e colore su schermo OLED, resa del ritaglio, fluidità dello scorrimento con Safari/PWA, comportamento della cache del service worker (dopo il deploy può servire un index.html vecchio: chiudere e riaprire la PWA).

**Segnalazioni sui contenuti delle immagini (decisione tua):**
- `specie_civilta.webp`: al centro-sinistra c'è un essere-albero molto simile a Groot e in basso una creatura simile a Rocket → contrasta con la regola «nessun personaggio Marvel riconoscibile». Consiglio di rigenerarla.
- `attori.webp`: silhouette con capelli lunghi e mantello che ricordano Thor; non sono volti reali, ma valuta se è accettabile.
- `eventi.webp`: la zona sinistra non è scura come da brief; titolo comunque leggibile (contrasto verificato).
- `luoghi.webp`: cielo chiaro/azzurro, più luminoso della palette; titolo leggibile.
