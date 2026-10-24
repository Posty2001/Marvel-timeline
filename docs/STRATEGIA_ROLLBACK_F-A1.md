# F-A1 — Strategia di rollback del deploy (nessuna modifica a Firebase)

**Principio:** F-A1 è solo codice statico (`index.html`, `sw.js`). Non scrive su RTDB, non cambia regole, `sync/`, `rooms/`. Il rollback è quindi **solo del sito**.

## Punto di ritorno
- Ultimo stato noto buono: commit **`fbf3399`**, build **`20261023-1520-c26`**, `index.html` md5 `73ed07167ca5c197fd01c2346f597d99`, `sw.js` md5 `b76146704ba055d64aad183b9307c31c`.
- Archivio di sicurezza fuori da Git: `TVA_C26_build.zip` (già in outputs).
- Proposta (da autorizzare con la pubblicazione): tag leggero `pre-fa1` su `fbf3399` prima del commit F-A1, e F-A1 come **un solo commit**, così il rollback è un singolo `revert`.

## Procedure (in ordine di preferenza)
| # | Procedura | Quando | Passi |
|---|---|---|---|
| 1 | **Revert del commit F-A1** (consigliata) | Qualsiasi problema | `git revert <hash-F-A1>` → push su `main` (nessuna riscrittura della storia) → attendi il deploy Pages. In alternativa pulsante «Revert» della PR/commit su GitHub |
| 2 | Ripristino file | Revert non possibile | `git checkout fbf3399 -- index.html sw.js` → commit «rollback F-A1» → push |
| 3 | Disattivazione mirata (hotfix) | Solo il pannello Account dà problemi | Rimuovere il tag `<script …firebase-auth-compat.js>`: il modulo va in «non disponibile» da solo e l'app resta intatta (verificato nei test). Richiede comunque un deploy |

## Cosa succede ai dispositivi
- **Service worker**: la cache è per build (`marvel-timeline-cache-<build>`). Il ritorno a c26 installa un SW con nome cache diverso; all'attivazione elimina **solo** le cache con prefisso dell'app (guardia C3), quindi la cache fa-1 sparisce. `index.html` viene messo in cache solo se la sua build coincide con quella del SW (nessuna versione mista).
- **Utenti già aggiornati**: al prossimo avvio online ricevono c26 (network-first); chi è offline resta su fa1 finché non si collega. Nessuna azione richiesta.
- **Sessione Auth**: resta nell'archivio del browser (IndexedDB) ma c26 non la usa; ripubblicando F-A1 la sessione riprende. Nessun dato locale (progressi, voti, XP, badge, preferenze, Timeline) viene toccato da deploy o rollback.
- **Account creati in Authentication**: rimangono finché non li elimini tu da Console (non influiscono su RTDB). Non serve eliminarli per il rollback.

## Verifica dopo il rollback (2 minuti)
1. `curl -s https://posty2001.github.io/marvel-timeline/index.html | grep -o 'tva-build" content="[^"]*'` → `20261023-1520-c26`.
2. `curl -s .../sw.js | grep SW_BUILD` → stessa build.
3. Su iPhone: apri due volte online; il gruppo «Account personale» **non** deve comparire; progressi e Timeline invariati (confronto coi 4 valori annotati).
4. Esegui `python3 tests/run_suites.py --only c3_test,c2_test` sul repository ripristinato.

## Cosa NON serve
Nessuna modifica a regole RTDB, dati remoti, `sync/`, `rooms/`, impostazioni Auth, credenziali o utenti. Nessuna migrazione inversa (F-A1 non migra nulla).

## Limiti
La finestra tra push e propagazione di GitHub Pages è di alcuni minuti; non è verificabile dal sandbox (dominio non raggiungibile). Il tag `pre-fa1` e il revert non sono stati eseguiti: richiedono la tua autorizzazione.
