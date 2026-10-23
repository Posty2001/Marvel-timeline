    /* SYNC40C-BEGIN — Blocco 4.0C: sincronizzazione cloud con stato reale, nessuna applicazione automatica del cloud */
    // Stati: off | connecting | synced | auth | offline | conflict. «Sincronizzazione riuscita» compare SOLO dopo una
    // conferma reale (lettura iniziale + set().then). Il profilo cloud NON viene mai applicato in automatico: ogni
    // differenza richiede una scelta esplicita e il ripristino passa da normalizzaProfilo + sostituisciProfilo
    // (transazione con copia di sicurezza recuperabile).
    var SYNC_TIMEOUT_MS = 10000;
    var SYNC_RETRY_DELAYS = [5000, 15000, 45000, 120000];
    var SYNC_POLL_MS = 4000;
    var syncState = 'off';
    var syncCode = null;
    var syncGen = 0;
    var syncRetryCount = 0;
    var syncRetryTimer = null;
    var syncPushing = false;
    var syncLastPushedStr = null;
    var syncLastRemoteRaw = null;
    var syncConflictRaw = null;
    var syncConflictBox = null;

    function syncConfigured() {
      return typeof firebase !== 'undefined' && FIREBASE_CONFIG && FIREBASE_CONFIG.apiKey !== 'INSERISCI_QUI';
    }

    function syncSetStatus(msg, kind) {
      if (!syncStatusEl) { if (window.console) console.warn('Marvel guide - sync:', msg); return; }
      syncStatusEl.hidden = false;
      syncStatusEl.textContent = msg;
      syncStatusEl.setAttribute('role', 'status');
      syncStatusEl.setAttribute('aria-live', 'polite');
      syncStatusEl.className = 'sync-status ' + (kind === 'ok' ? 'sync-status-ok' : kind === 'busy' ? 'sync-status-busy' : 'sync-status-err');
      syncStatusEl.setAttribute('data-sync-state', syncState);
    }

    var SYNC_LABELS = {
      off: ['Non collegato', 'err'],
      connecting: ['🔄 Connessione in corso…', 'busy'],
      synced: ['✅ Sincronizzazione riuscita', 'ok'],
      auth: ['⛔ Errore di autorizzazione: il database rifiuta l’accesso a questo codice. Sincronizzazione sospesa; i tuoi dati locali non sono stati toccati e NON risultano sincronizzati.', 'err'],
      offline: ['⚠️ Connessione non disponibile. I dati locali sono al sicuro ma NON risultano sincronizzati.', 'err'],
      conflict: ['⚠️ Conflitto tra dati locali e cloud: scegli come procedere. Nulla è stato modificato.', 'err'],
      initfail: ['\u26A0\uFE0F Sincronizzazione sospesa: il profilo locale non risulta inizializzato. Nessun dato \u00e8 stato toccato n\u00e9 inviato; ricarica la pagina e riprova.', 'err']
    };
    function syncSetState(stato, extra) {
      syncState = stato;
      var l = SYNC_LABELS[stato] || SYNC_LABELS.off;
      syncSetStatus(l[0] + (extra ? ' ' + extra : ''), l[1]);
      if (syncDisconnectBtn) syncDisconnectBtn.hidden = (stato === 'off' && !syncCode);
      if (stato !== 'conflict') syncHideConflict();
    }

    // ---- Validazione del codice: finisce in un percorso Firebase, quindi niente separatori ('/'), niente
    // caratteri riservati ('. $ # [ ] '), niente spazi. I codici generati dall'app (8 caratteri
    // A-Z/2-9) restano validi; ammessi anche '-' e '_' interni. ----
    function syncNormalizzaCodice(raw) {
      var c = String(raw == null ? '' : raw).trim().toUpperCase();
      if (!c) return { ok: false, motivo: 'Genera o incolla prima un codice qui sopra.' };
      if (c.length < 4 || c.length > 32) return { ok: false, motivo: 'Il codice deve avere da 4 a 32 caratteri.' };
      if (!/^[A-Z0-9][A-Z0-9_-]*[A-Z0-9]$/.test(c)) return { ok: false, motivo: 'Codice non valido: usa solo lettere, numeri e, all’interno, “-” o “_” (niente spazi, “/”, “.”, “$”, “#”, “[”, “]”).' };
      return { ok: true, code: c };
    }

    // ---- Profilo locale/remoto ----
    function syncGetFullProfile() {
      function safeGetObj(key) { try { return JSON.parse(localStorage.getItem(key) || '{}'); } catch(e) { return {}; } }
      function safeGetStr(key) { try { return localStorage.getItem(key) || ''; } catch(e) { return ''; } }
      var profile = { app: PROFILE_APP_ID, version: PROFILE_SUPPORTED_VERSIONS[0], schemaVersion: PROFILE_SUPPORTED_SCHEMA };
      for (var ok in PROFILE_OBJ_KEYS) { profile[ok] = safeGetObj(PROFILE_OBJ_KEYS[ok]); }
      for (var sk in PROFILE_STR_KEYS) { profile[sk] = safeGetStr(PROFILE_STR_KEYS[sk]); }
      return profile;
    }

    function syncStabile(o) {
      if (o === null || typeof o !== 'object') return JSON.stringify(o);
      if (Array.isArray(o)) return '[' + o.map(syncStabile).join(',') + ']';
      return '{' + Object.keys(o).sort().map(function(k) { return JSON.stringify(k) + ':' + syncStabile(o[k]); }).join(',') + '}';
    }

    // Converte il valore remoto nel formato del profilo validato e lo fa passare da normalizzaProfilo.
    function syncValidaRemoto(raw) {
      function ko(m) { return { ok: false, motivo: m }; }
      if (typeof raw !== 'string') return ko('i dati nel cloud non sono nel formato atteso.');
      if (raw.length > PROFILE_MAX_BYTES) return ko('i dati nel cloud sono troppo grandi per essere un profilo.');
      var obj;
      try { obj = JSON.parse(raw); } catch(e) { return ko('i dati nel cloud non sono un JSON leggibile.'); }
      if (!profiloOggettoSemplice(obj)) return ko('i dati nel cloud non contengono un profilo.');
      var cand = {};
      Object.keys(obj).forEach(function(k) { if (k !== '__proto__') cand[k] = obj[k]; });
      // i profili scritti dalle versioni precedenti non portano versione: sono nel formato 2.0/schema 1
      if (cand.version === undefined) cand.version = PROFILE_SUPPORTED_VERSIONS[0];
      if (cand.schemaVersion === undefined) cand.schemaVersion = PROFILE_SUPPORTED_SCHEMA;
      var esito;
      try { esito = normalizzaProfilo(cand); } catch(eN) { return ko('profilo nel cloud non leggibile.'); }
      if (!esito.ok) return ko(esito.motivo);
      esito.grezzo = cand;
      return esito;
    }

    // 'uguale' | 'diverso' | 'invalido'
    function syncConfronta(raw) {
      var rem = syncValidaRemoto(raw);
      if (!rem.ok) return { tipo: 'invalido', motivo: rem.motivo };
      var loc = null;
      try { loc = normalizzaProfilo(costruisciProfiloCompleto()); } catch(eL) { loc = null; }
      if (loc && loc.ok && syncStabile(loc.scritture) === syncStabile(rem.scritture)) return { tipo: 'uguale', rem: rem };
      return { tipo: 'diverso', rem: rem };
    }


    // ---- Barriera di inizializzazione (Blocco 4.0E) ----
    // Nessuna lettura/confronto/scrittura cloud parte finché il profilo locale non è inizializzato. Condizioni verificabili
    // (nessun ritardo fisso): (1) marvelInit ha restituito il controllo; (2) la pagina è «complete»; (3) il modulo ricompense ha
    // completato la prima valutazione post-caricamento (scrive 'rewards' in modo asincrono) senza errori e a profilo pronto;
    // (4) l'ID tessera esiste; (5) l'istantanea locale è identica prima e dopo un passaggio dell'event loop (ripetuto se cambia).
    var syncInitPromise = null, syncInitOk = false;
    function syncImpronta() { try { return JSON.stringify(syncGetFullProfile()); } catch(e) { return ''; } }
    function syncInitBarrier() {
      if (syncInitPromise) return syncInitPromise;
      syncInitPromise = new Promise(function(resolve) {
        var giri = 0;
        function fin(ok, motivo) { syncInitOk = ok; resolve({ ok: ok, motivo: motivo || '' }); }
        function verifica() {
          var rw = window.tvaRewards;
          var attesa = (rw && rw.ready && typeof rw.ready.then === 'function') ? rw.ready : Promise.resolve({ ok: true, evaluated: true });
          attesa.then(function(r) {
            if (r && r.ok === false) { fin(false, 'valutazione ricompense non riuscita'); return; }
            if (r && r.evaluated === false) { fin(false, 'profilo locale non pronto'); return; }
            var id = null;
            try { id = localStorage.getItem(PROFILE_STR_KEYS.tesseraId); } catch(eId) { fin(false, 'archivio del browser non leggibile'); return; }
            if (!id) { fin(false, 'ID tessera non generato'); return; }
            var prima = syncImpronta();
            setTimeout(function() {
              if (syncImpronta() === prima || ++giri >= 10) fin(true);
              else verifica();
            }, 0);
          }, function() { fin(false, 'inizializzazione interrotta'); });
        }
        Promise.resolve().then(function() {
          if (document.readyState === 'complete') verifica();
          else window.addEventListener('load', verifica, { once: true });
        });
      });
      return syncInitPromise;
    }

    // Un 'diverso' viene riconfermato dopo un passaggio dell'event loop: un conflitto si dichiara solo se la differenza persiste.
    function syncConfrontaStabile(raw, gen, cb) {
      var c1 = syncConfronta(raw);
      if (c1.tipo !== 'diverso') { cb(c1); return; }
      setTimeout(function() { if (gen !== syncGen) return; cb(syncConfronta(raw)); }, 0);
    }

    // ---- Classificazione errori ----
    function syncClassificaErrore(err) {
      var code = String(err && err.code || '').toLowerCase();
      var msg = String(err && err.message || '').toLowerCase();
      if (code.indexOf('permission') !== -1 || msg.indexOf('permission_denied') !== -1 || msg.indexOf('permission denied') !== -1) return 'auth';
      return 'transient';
    }
    function syncTimeout(promise) {
      return new Promise(function(resolve, reject) {
        var t = setTimeout(function() { var e = new Error('timeout'); e.code = 'sync/timeout'; reject(e); }, SYNC_TIMEOUT_MS);
        promise.then(function(v) { clearTimeout(t); resolve(v); }, function(e) { clearTimeout(t); reject(e); });
      });
    }

    // ---- Timer e listener ----
    var syncRef = null;
    var syncPollTimer = null;
    function syncStopTimers() {
      if (syncPollTimer) { clearInterval(syncPollTimer); syncPollTimer = null; }
      if (syncRetryTimer) { clearTimeout(syncRetryTimer); syncRetryTimer = null; }
    }
    function syncDetach() {
      syncStopTimers();
      if (syncRef) { try { syncRef.off(); } catch(eOff) {} }
      syncRef = null;
      syncPushing = false;
      syncGen++;
    }

    function syncHandleError(err, ctx, gen) {
      if (gen !== syncGen) return;
      if (window.console) console.error('Marvel guide - sync (' + ctx + '):', err && (err.code || err.message) || err);
      var tipo = syncClassificaErrore(err);
      syncPushing = false;
      if (tipo === 'auth') {
        var code = syncCode;
        syncDetach();
        syncCode = code; // il codice resta salvato (nessun tentativo automatico ulteriore), i dati locali non si toccano
        syncSetState('auth');
        return;
      }
      syncStopTimers();
      if (syncRetryCount >= SYNC_RETRY_DELAYS.length) {
        var c2 = syncCode;
        syncDetach();
        syncCode = c2;
        syncSetState('offline', 'Tentativi esauriti.');
        syncShowRetry();
        return;
      }
      var d = SYNC_RETRY_DELAYS[syncRetryCount++];
      syncSetState('offline', 'Nuovo tentativo tra ' + Math.round(d / 1000) + ' s (' + syncRetryCount + '/' + SYNC_RETRY_DELAYS.length + ').');
      syncRetryTimer = setTimeout(function() {
        syncRetryTimer = null;
        if (gen !== syncGen) return;
        if (ctx === 'push' && syncRef) { syncSetState('connecting'); syncPushNow(false, gen, true); }
        else syncConnect(syncCode, { retry: true });
      }, d);
    }

    function syncStartPolling(gen) {
      if (syncPollTimer) clearInterval(syncPollTimer);
      syncPollTimer = setInterval(function() { syncPushNow(false, gen); }, SYNC_POLL_MS);
    }

    function syncPushNow(first, gen, forced) {
      if (!syncRef || gen !== syncGen || syncPushing) return;
      if (!first && !forced && syncState !== 'synced') return;
      var str = JSON.stringify(syncGetFullProfile());
      if (!first && str === syncLastPushedStr) {
        if (forced) { syncRetryCount = 0; syncSetState('synced'); if (!syncPollTimer) syncStartPolling(gen); }
        return;
      }
      syncPushing = true;
      var ref = syncRef, prevRaw = syncLastRemoteRaw;
      syncLastRemoteRaw = str; // l'eco locale della mia scrittura non deve sembrare un cambiamento remoto
      syncTimeout(ref.set(str)).then(function() {
        if (gen !== syncGen) return;
        syncPushing = false;
        syncLastPushedStr = str;
        syncRetryCount = 0;
        syncSetState('synced');
        if (first) syncActivate(str, gen);
        else if (!syncPollTimer) syncStartPolling(gen);
      }).catch(function(err) {
        if (gen === syncGen) syncLastRemoteRaw = prevRaw;
        syncHandleError(err, 'push', gen);
      });
    }

    function syncListen(gen) {
      syncRef.on('value', function(snap) {
        if (gen !== syncGen || syncState !== 'synced') return;
        var raw = snap.val();
        if (raw === syncLastRemoteRaw) return;      // eco della mia scrittura o valore già verificato
        if (raw === null && syncLastRemoteRaw === null) return;
        syncConfrontaStabile(raw, gen, function(cmp) {
          if (gen !== syncGen || syncState !== 'synced') return;
          if (cmp.tipo === 'uguale') { syncLastRemoteRaw = raw; return; }
          syncEnterConflict(raw, cmp);              // MAI applicato in automatico
        });
      }, function(err) { syncHandleError(err, 'listen', gen); });
    }

    function syncActivate(raw, gen) {
      syncLastRemoteRaw = raw;
      syncRetryCount = 0;
      try { localStorage.setItem(SYNC_CODE_KEY, syncCode); } catch(eSv) {}
      syncSetState('synced');
      syncListen(gen);
      syncStartPolling(gen);
    }

    // ---- Connessione verificata ----
    function syncConnect(code, opts) {
      opts = opts || {};
      var v = syncNormalizzaCodice(code);
      if (!v.ok) { syncSetStatus('⚠️ ' + v.motivo, 'err'); return; }
      if (!syncConfigured()) { syncSetStatus('⚠️ Sincronizzazione non ancora configurata su questo file.', 'err'); return; }
      if (!opts.retry && syncState === 'connecting' && syncCode === v.code) return; // richiesta duplicata: un solo collegamento in corso
      var retryCount = opts.retry ? syncRetryCount : 0;
      syncDetach();
      syncRetryCount = retryCount;
      syncCode = v.code;
      var gen = syncGen;
      syncSetState('connecting', syncInitOk ? '' : '(preparazione del profilo locale)');
      syncInitBarrier().then(function(init) {
        if (gen !== syncGen) return;
        if (!init.ok) {
          if (window.console) console.warn('Marvel guide - sync sospesa:', init.motivo);
          var cI = syncCode; syncDetach(); syncCode = cI;
          syncSetState('initfail');
          return;
        }
        syncSetState('connecting');
        syncAvvia(v.code, gen);
      });
    }

    function syncAvvia(code, gen) {
      var v = { code: code };
      try {
        if (!firebase.apps || !firebase.apps.length) { firebase.initializeApp(FIREBASE_CONFIG); }
        syncRef = firebase.database().ref('sync/' + v.code);
      } catch (errInit) {
        syncSetStatus('⚠️ Errore di configurazione Firebase.', 'err');
        syncState = 'offline';
        if (window.console) console.error('Marvel guide - sync init:', errInit);
        return;
      }
      syncTimeout(syncRef.once('value')).then(function(snap) {
        if (gen !== syncGen) return;
        var raw = snap.val();
        if (raw === null || raw === undefined) {
          // nessun dato remoto: primo dispositivo; lo stato è «riuscito» solo dopo la conferma della scrittura
          syncSetState('connecting');
          syncPushNow(true, gen);
          return;
        }
        syncConfrontaStabile(raw, gen, function(cmp) {
          if (gen !== syncGen) return;
          if (cmp.tipo === 'uguale') { syncLastPushedStr = JSON.stringify(syncGetFullProfile()); syncActivate(raw, gen); return; }
          syncEnterConflict(raw, cmp);
        });
      }).catch(function(err) { syncHandleError(err, 'connect', gen); });
    }

    // ---- Conflitto: scelta esplicita ----
    function syncEnsureBox() {
      if (syncConflictBox || !syncStatusEl || !syncStatusEl.parentNode) return syncConflictBox;
      var b = document.createElement('div');
      b.id = 'syncConflictBox'; b.className = 'sync-conflict'; b.hidden = true;
      b.innerHTML = '<p class="sync-conflict-msg" id="syncConflictMsg"></p>' +
        '<pre class="sync-conflict-diff" id="syncConflictDiff" hidden></pre>' +
        '<div class="sync-conflict-actions">' +
        '<button type="button" class="reset-btn reset-btn-info" id="syncKeepLocalBtn">Mantieni dati locali</button>' +
        '<button type="button" class="reset-btn" id="syncShowDiffBtn">Visualizza differenze</button>' +
        '<button type="button" class="reset-btn" id="syncRestoreBtn">Ripristina dal cloud</button>' +
        '<button type="button" class="reset-btn" id="syncRetryBtn" hidden>Riprova</button></div>';
      syncStatusEl.parentNode.insertBefore(b, syncStatusEl.nextSibling);
      syncConflictBox = b;
      document.getElementById('syncKeepLocalBtn').addEventListener('click', syncKeepLocal);
      document.getElementById('syncShowDiffBtn').addEventListener('click', syncShowDiff);
      document.getElementById('syncRestoreBtn').addEventListener('click', syncRestoreFromCloud);
      document.getElementById('syncRetryBtn').addEventListener('click', function() { syncRetryCount = 0; syncConnect(syncCode, {}); });
      return b;
    }
    function syncHideConflict() { if (syncConflictBox) syncConflictBox.hidden = true; }
    function syncShowRetry() {
      var b = syncEnsureBox(); if (!b) return;
      b.hidden = false;
      document.getElementById('syncConflictMsg').textContent = 'Sincronizzazione ferma dopo ' + SYNC_RETRY_DELAYS.length + ' tentativi. Puoi riprovare manualmente.';
      document.getElementById('syncConflictDiff').hidden = true;
      ['syncKeepLocalBtn', 'syncShowDiffBtn', 'syncRestoreBtn'].forEach(function(id) { document.getElementById(id).hidden = true; });
      document.getElementById('syncRetryBtn').hidden = false;
    }
    function syncEnterConflict(raw, cmp) {
      var code = syncCode;
      syncDetach();                 // nessuna scrittura/lettura automatica finché l'utente non sceglie
      syncCode = code;
      syncConflictRaw = raw;
      syncSetState('conflict');
      var b = syncEnsureBox(); if (!b) return;
      b.hidden = false;
      document.getElementById('syncConflictDiff').hidden = true;
      ['syncKeepLocalBtn', 'syncShowDiffBtn', 'syncRestoreBtn'].forEach(function(id) { document.getElementById(id).hidden = false; });
      document.getElementById('syncRetryBtn').hidden = true;
      var restore = document.getElementById('syncRestoreBtn');
      restore.disabled = cmp.tipo === 'invalido';
      document.getElementById('syncConflictMsg').textContent = cmp.tipo === 'invalido'
        ? 'Il profilo nel cloud non è valido (' + cmp.motivo + ') e non può essere ripristinato. I tuoi dati locali restano intatti.'
        : 'Il profilo nel cloud è diverso da quello di questo dispositivo. Nessun dato è stato modificato né inviato: scegli cosa fare.';
    }
    function syncKeepLocal() {
      syncDetach();
      syncCode = null;
      syncConflictRaw = null;
      try { localStorage.removeItem(SYNC_CODE_KEY); } catch(eRm) {}
      syncSetState('off');
      syncSetStatus('Dati locali mantenuti. Sincronizzazione non attiva: il cloud non è stato modificato.', 'err');
    }
    function syncShowDiff() {
      var pre = document.getElementById('syncConflictDiff'); if (!pre) return;
      var rem = syncValidaRemoto(syncConflictRaw), righe = [];
      if (!rem.ok) { righe.push('Cloud non leggibile: ' + rem.motivo); }
      else {
        var loc = null;
        try { loc = normalizzaProfilo(costruisciProfiloCompleto()); } catch(eD) {}
        var conta = function(s) { try { var o = JSON.parse(s); return o && typeof o === 'object' ? Object.keys(o).length : (s ? 1 : 0); } catch(e) { return s ? 1 : 0; } };
        var nomi = { watched: 'Titoli visti', watchedAnim: 'Serie animate viste', favorites: 'Preferiti', notes: 'Note', ratings: 'Voti', badgesEarned: 'Badge', groups: 'Gruppi', friends: 'Amici', rewards: 'Premi/XP', tesseraLook: 'Aspetto tessera', missioneXpBank: 'XP missioni' };
        var derivati = { badgesEarned: 1, rewards: 1, missioneSnapshot: 1, missioneXpBank: 1, titoliStagione: 1 }, soloDerivati = true;
        Object.keys(PROFILE_OBJ_KEYS).forEach(function(k) {
          var sk = PROFILE_OBJ_KEYS[k], a = loc && loc.ok ? loc.scritture[sk] : null, b = rem.scritture[sk];
          if (a === b) return;
          if (!derivati[k]) soloDerivati = false;
          righe.push((nomi[k] || k) + (derivati[k] ? ' (campo derivato)' : '') + ': locale ' + conta(a) + ' · cloud ' + conta(b));
        });
        Object.keys(PROFILE_STR_KEYS).forEach(function(k) {
          var sk = PROFILE_STR_KEYS[k], a = loc && loc.ok ? loc.scritture[sk] : null, b = rem.scritture[sk];
          if (a !== b) { soloDerivati = false; righe.push(k + (k === 'tesseraId' ? ' (generato automaticamente)' : '') + ': valore diverso'); }
        });
        if (!righe.length) righe.push('Nessuna differenza di contenuto rilevata.');
        else if (soloDerivati) righe.push('Le differenze riguardano solo campi derivati (ricalcolabili): i dati inseriti da te coincidono. Resta comunque una scelta tua; nulla viene unito in automatico.');
      }
      pre.textContent = righe.join('\n');
      pre.hidden = false;
    }
    function syncRestoreFromCloud() {
      if (!syncInitOk) { showToast('Ripristino non disponibile: il profilo locale non \u00e8 ancora inizializzato.', 6000); return; }
      var rem = syncValidaRemoto(syncConflictRaw);
      if (!rem.ok) { showToast('Ripristino annullato: ' + rem.motivo + ' I dati locali non sono stati modificati.', 8000); return; }
      var testo = 'Ripristinare il profilo dal cloud? Sostituirà TUTTO il profilo di questo dispositivo (' + riassuntoProfiloAttuale() + ' titoli visti) con quello del cloud (' + rem.titoliVisti + ' titoli visti). Una copia di sicurezza del profilo attuale verrà salvata e potrai recuperarla da “Ripristina copia di sicurezza”.';
      if (rem.mancanti.length) testo += '\n\nCampi assenti nel cloud, che verranno reimpostati: ' + rem.mancanti.join(', ') + '.';
      if (!window.confirm(testo)) { showToast('Ripristino annullato. Nessun dato è stato modificato.'); return; }
      var ris = sostituisciProfilo(rem, true);
      if (!ris.ok) { showToast('Ripristino NON riuscito: ' + ris.motivo + (ris.ripristinato ? ' Il profilo precedente è stato ripristinato.' : ''), 8000); return; }
      try { localStorage.setItem(SYNC_CODE_KEY, syncCode); } catch(eC) {}
      showToast('Profilo ripristinato dal cloud. Ricarico…');
      setTimeout(function() { location.reload(); }, 1200);
    }

    function syncGenCode() {
      var chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // 32 simboli, esclusi 0/O e 1/I/l
      var code = '', i;
      var cr = window.crypto || window.msCrypto;
      if (cr && cr.getRandomValues) {
        var buf = new Uint8Array(8); cr.getRandomValues(buf);
        for (i = 0; i < 8; i++) { code += chars.charAt(buf[i] % 32); } // 256 % 32 === 0: nessun bias
      } else {
        for (i = 0; i < 8; i++) { code += chars.charAt(Math.floor(Math.random() * chars.length)); }
      }
      return code;
    }

    if (syncGenBtn && syncCodeInput) {
      syncGenBtn.addEventListener('click', function() { syncCodeInput.value = syncGenCode(); });
    }
    if (syncConnectBtn && syncCodeInput) {
      syncConnectBtn.addEventListener('click', function() {
        try { syncConnect(syncCodeInput.value, {}); }
        catch (errClick) {
          syncSetStatus('⚠️ Errore imprevisto: ' + (errClick && errClick.message ? errClick.message : errClick), 'err');
          if (window.console) console.error('Marvel guide - sync click:', errClick);
        }
      });
    }
    if (syncDisconnectBtn) {
      syncDisconnectBtn.addEventListener('click', function() {
        syncDetach();
        syncCode = null; syncConflictRaw = null;
        try { localStorage.removeItem(SYNC_CODE_KEY); } catch(eRm2) {}
        syncSetState('off');
        syncSetStatus('Sincronizzazione disattivata su questo dispositivo. I dati locali non sono stati modificati.', 'err');
      });
    }

    // Riconnessione automatica: mostra «Connessione in corso» e passa dalla stessa verifica reale (una sola
    // sequenza con tentativi limitati); non mostra mai «riuscita» senza conferma e non applica dati cloud.
    syncSetState('off');
    var savedSyncCode = null;
    try { savedSyncCode = localStorage.getItem(SYNC_CODE_KEY); } catch(eRd) {}
    if (savedSyncCode) {
      var vSaved = syncNormalizzaCodice(savedSyncCode);
      if (!vSaved.ok) {
        syncSetStatus('⚠️ Il codice salvato non è valido e non verrà usato: ' + vSaved.motivo, 'err');
      } else if (syncConfigured()) {
        if (syncCodeInput) syncCodeInput.value = vSaved.code;
        syncConnect(vSaved.code, {});
      }
    }
    /* SYNC40C-END */
