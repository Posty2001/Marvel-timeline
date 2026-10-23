# Problemi preesistenti nei test storici (registrati, non modificati)

Test: `tests/tva_test.py` (suite storica Atlante/Cronologie). Verificato il 2026-10-23: gli **stessi 8 controlli** falliscono sulla build precedente a M3 (M2.1, `20261023-0600-m21`) e sulla build M3.2 (`20261023-1400-m32`). I test **non sono stati modificati** per ottenere PASS; l'unica modifica è G1 (14→15 voci) per il Reliquiario aggiunto volutamente in M3.2, che passa.

| # | Controllo (nome esatto) | Sezione |
|---|---|---|
| 1 | `G arti n schede` | Atlante – Arti Mistiche |
| 2 | `G multiverso atlante chiuso` | Atlante – Multiverso |
| 3 | `G reliquiario atlante chiuso` | Atlante – Reliquiario |
| 4 | `H cronologie righe 15!=10` | Cronologie |
| 5 | `H cronologie[0] apre sezione` | Cronologie |
| 6 | `H cronologie[1] apre sezione` | Cronologie |
| 7 | `H cronologie[2] apre sezione` | Cronologie |
| 8 | `H cronologie[6] ritorno` | Cronologie |

Natura probabile (da confermare, non corretta): aspettative di un'architettura Atlante/Cronologie precedente (es. 10 righe nel catalogo Cronologie, ora 15; ritorno dopo apertura sezione). Nessun impatto osservato sulle funzioni dell'app nelle verifiche M3.2.

Altri falsi positivi noti: `ui_audit` – «contrasto testo ≥ 4.5:1» sulle etichette `.ud-st` (contrasto reale misurato 5,4:1 e 6,7:1).
