# F-A1 — Procedura di test reale su iPhone (da eseguire DOPO la pubblicazione autorizzata)

Scopo: provare con Firebase reale ciò che il sandbox non può provare (SDK reale, CSP, email, Safari/PWA).
Regole: usa **solo un indirizzo email di tua proprietà** (es. un alias dedicato); nessuna password riutilizzata da altri servizi; l'account di prova lo crei **tu**. Non toccare Console, regole, `sync/`, `rooms/`.

## 0. Prerequisiti (una tantum, sul Mac/PC)
- Pagina pubblicata: apri `https://posty2001.github.io/marvel-timeline/` e verifica la build (vedi §A).
- Console → Authentication → Impostazioni: dominio `posty2001.github.io` autorizzato (già fatto); modello email in italiano.
- Facoltativo ma consigliato: Safari Mac con iPhone collegato → Sviluppo → [iPhone] → Web Inspector (per vedere Console e Rete). In alternativa usa i controlli «solo schermata» sotto.

## A. Verifica build e aggiornamento (iPhone)
1. Safari → apri il sito. Impostazioni → (in fondo) / Centrale TVA → Operazioni: deve comparire il gruppo **Account personale (facoltativo)**. Se non compare: chiudi la scheda/PWA, riapri online due volte (aggiornamento service worker per build).
2. Annota: build mostrata (se visibile) o con Web Inspector `document.querySelector('meta[name=tva-build]').content` = `20261023-2355-fa1` (o l'id che ti darò alla pubblicazione).

## B. Controlli CSP/rete (Web Inspector, se disponibile) — **criterio di stop**
- Console: **nessun** messaggio «Refused to load/connect… Content Security Policy».
- In particolare **nessuna** richiesta/violazione verso `apis.google.com` (se compare: **STOP**, annota URL esatto, non proseguire: decisione sulla CSP spetta a te).
- Rete (durante registrazione/login): gli host contattati per l'Auth devono essere **solo** `identitytoolkit.googleapis.com` e, a sessione attiva, `securetoken.googleapis.com`. Ogni altro host nuovo → annota e segnala.

## C. Salvataggio dati prima di iniziare (obbligatorio)
1. Centrale TVA → Operazioni → «Esporta profilo»: salva il file in File/iCloud.
2. Annota 4 valori a campione: titoli visti (n.), un voto, XP/livello, modalità Timeline attiva.

## D. Casi di test (compila PASS/FAIL e note)
| # | Passi | Esito atteso |
|---|---|---|
| D1 | Senza accedere: segna un titolo come visto | Funziona; nessuna richiesta di login |
| D2 | Account → «Crea account»: email di prova, password ≥ 8, conferma **diversa** → invia | Errore «non coincidono», nessuna email |
| D3 | Stesso form con dati corretti | Passa a «EMAIL DA VERIFICARE»; email **in italiano** da «TVA Archives» entro ~1 min (controlla spam) |
| D4 | «Reinvia il link» subito | Pulsante bloccato con conto alla rovescia 60 s; poi reinvio ok |
| D5 | Premi «Ho verificato» **prima** di aprire il link | Messaggio «non risulta ancora verificata» |
| D6 | Apri il link nell'email (Safari) → pagina Firebase «email verificata» → torna alla guida (link di ritorno o scheda) → «Ho verificato» | «ACCOUNT VERIFICATO» (anche al solo ritorno sulla scheda) |
| D7 | Chiudi del tutto Safari (e la PWA se installata), riapri | Sessione ancora attiva (account verificato) |
| D8 | «Esci» | Torna a «Accedi / Crea account»; messaggio che i dati restano; **dati invariati** (confronta i 4 valori di §C) |
| D9 | Login con password **sbagliata** | «Email o password non corretti» (nessun dettaglio) |
| D10 | Login con email **inesistente** | Stesso identico messaggio |
| D11 | Login corretto | «ACCOUNT VERIFICATO» |
| D12 | «Password dimenticata?» con email di prova → link ricevuto (italiano) → scegli nuova password → torna → login con la **nuova** | Messaggio neutro all'invio; reset ok; vecchia password rifiutata |
| D13 | Reset con email **sconosciuta** | **Stesso** messaggio neutro; nessuna email |
| D14 | Modalità aereo → prova «Accedi» | Banner offline e messaggio chiaro; nessun blocco; l'archivio funziona |
| D15 | Rete tornata → «Accedi» | Funziona senza ricaricare |
| D16 | Tastiera iOS: campo email (tastiera email, niente maiuscola automatica), password con «Mostra/Nascondi», suggerimento Portachiavi | Nessuno zoom automatico, nessun elemento coperto dalla tastiera, pulsanti raggiungibili |
| D17 | Tema scuro e chiaro, Dynamic Type grande | Testi leggibili, niente sovrapposizioni |
| D18 | PWA installata (Aggiungi a Home): ripeti D3–D8 | Come in Safari; il link email si apre in Safari: rientro nella PWA manuale (annota se la sessione è condivisa) |
| D19 | A fine prove confronta i 4 valori di §C | **Identici** (nessuna perdita/modifica) |

## E. Esito
Riporta: tabella D1–D19 (PASS/FAIL/note), screenshot di eventuali errori, eventuali messaggi in console. In caso di FAIL grave (perdita dati, violazione CSP, blocco dell'archivio) applica subito il rollback del documento «Strategia di rollback».

## F. Pulizia (a tua discrezione)
L'account di prova resta in Authentication (non nel database). Puoi eliminarlo tu da Console → Authentication → Utenti; non è richiesto per il rollback e non influisce su `sync/`, `rooms/` né sulle regole.
