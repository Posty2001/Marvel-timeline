# TVA Archives — M3.3 Capitolo 0 → «Prologo — Prima del Tempo»
Build 20261023-1500-m33 (md5 f9276775f9d2365c417ba77931583838). Nessun commit/push/deploy.

| Punto | Esito |
|---|---|
| Card unica, chiusa di default, icona 🌌, titolo, sottotitolo, «5 letture» | OK (54px a 390, 51px a 320) |
| Tocco → mostra le 5 letture 0.1–0.5, ciascuna espandibile, testi originali | OK |
| Rimossi part-tab, intestazione h2, tag, separatore ::before | OK |
| Parte 1 subito dopo la card chiusa | gap ≤ 24px |
| ID (#cap0, item), testi, link TOC/sidebar/tl-row, progressi, XP, cronologia | invariati; i link a #cap0 ora aprono anche il prologo |
| Espansione: salti / overflow orizzontale (390/360/320) | nessuno |
Test: cap0_test 37/37; m32, m31, m3, rs, stats_fix, b321, home2, leg tutti OK. Patch idempotente, md5 identico su doppia esecuzione.
Da verificare su iPhone reale: tocco/animazione apertura, aspetto con tastiera/zoom testo.
