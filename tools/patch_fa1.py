#!/usr/bin/env python3
"""Patch F-A1 (idempotente, dopo patch_c26): autenticazione facoltativa email/password (Firebase Auth compat).
Aggiunge: script firebase-auth-compat, 2 host in connect-src, pannello «Account personale» (Impostazioni > Operazioni), modulo JS isolato.
NON tocca: profilo, progressi, voti, XP, badge, Timeline, sync/, rooms/, regole, database. Nessuna scrittura su localStorage/RTDB."""
import re
P='/home/claude/work/index.html'; SW='/home/claude/work/sw.js'
BUILD='20261023-2355-fa1'
s=open(P,encoding='utf-8').read()
def rep(old,new,marker):
    global s
    if marker in s: return
    assert s.count(old)==1,(old[:70],s.count(old)); s=s.replace(old,new)

# 1) CSP: solo i due host necessari alle chiamate email/password (nessun wildcard googleapis)
rep("connect-src 'self' https://*.firebaseio.com","connect-src 'self' https://identitytoolkit.googleapis.com https://securetoken.googleapis.com https://*.firebaseio.com",'identitytoolkit.googleapis.com')

# 2) SDK Auth (stessa versione/origine dei due SDK esistenti)
rep('<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-database-compat.js"></script>\n',
    '<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-database-compat.js"></script>\n<script src="https://www.gstatic.com/firebasejs/10.13.0/firebase-auth-compat.js"></script>\n','firebase-auth-compat.js')

# 3) CSS
CSS='''<style id="fa1-css">
/* FA1-CSS */
.fa-wrap { margin-top: .2rem; }
.fa-wrap [hidden] { display: none !important; }
.fa-note { font-size: .8rem; line-height: 1.45; margin: 0 0 .6rem; color: var(--ink-soft); }
.fa-who { font-family: 'IBM Plex Mono', monospace; font-size: .8rem; margin: 0 0 .5rem; word-break: break-all; color: var(--ink); }
.fa-badge { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: .68rem; letter-spacing: .04em; padding: .15rem .5rem; border-radius: 4px; margin: 0 0 .5rem; }
.fa-badge-ok { background: rgba(46,138,62,.14); color: #1f6b2d; }
.fa-badge-warn { background: rgba(200,140,0,.14); color: #7a5510; }
#darkModeToggle:checked ~ * .fa-badge-ok { color: #6fcf86; }
#darkModeToggle:checked ~ * .fa-badge-warn, #darkModeToggle:checked ~ * .fa-msg-busy, #darkModeToggle:checked ~ * .fa-net { color: #d9a441; }
.fa-form { display: flex; flex-direction: column; gap: .55rem; margin: 0; }
.fa-field { display: flex; flex-direction: column; gap: .2rem; }
.fa-field label { font-family: 'IBM Plex Mono', monospace; font-size: .7rem; letter-spacing: .04em; color: var(--ink-soft); }
.fa-in { width: 100%; box-sizing: border-box; min-height: 44px; padding: .6rem .8rem; font-size: 16px; font-family: 'Spectral', serif; border: 2px solid var(--ink); border-radius: 4px 10px 4px 10px; background: var(--paper); color: var(--ink); box-shadow: 1.5px 1.5px 0 rgba(36,29,20,.15); }
.fa-in:focus { outline: 2px solid var(--marvel-red); outline-offset: 1px; border-color: var(--marvel-red); }
.fa-in[aria-invalid="true"] { border-color: var(--marvel-red); }
.fa-pwrow { display: flex; gap: .4rem; align-items: stretch; }
.fa-pwrow .fa-in { flex: 1 1 0; width: auto; min-width: 0; }
.fa-pwrow .reset-btn { flex: 0 0 auto; width: auto; min-width: 5.2rem; }
.fa-hint { font-size: .72rem; color: var(--ink-soft); margin: 0; }
.fa-actions { display: flex; flex-wrap: wrap; gap: .4rem; align-items: center; margin-top: .2rem; }
.fa-link { background: none; border: 0; padding: .6rem .2rem; min-height: 44px; font-family: 'IBM Plex Mono', monospace; font-size: .72rem; color: var(--studio-sony); text-decoration: underline; cursor: pointer; }
.fa-msg { font-family: 'IBM Plex Mono', monospace; font-size: .74rem; line-height: 1.4; margin: .55rem 0 0; padding: .4rem .6rem; border-radius: 4px; display: block; word-break: break-word; }
.fa-msg-ok { background: rgba(46,138,62,.12); color: #1f6b2d; }
.fa-msg-busy { background: rgba(200,140,0,.12); color: #7a5510; }
.fa-msg-err { background: rgba(200,39,42,.1); color: var(--marvel-red); }
#darkModeToggle:checked ~ * .fa-msg-ok { color: #6fcf86; }
.fa-net { font-family: 'IBM Plex Mono', monospace; font-size: .7rem; color: #7a5510; margin: 0 0 .5rem; }
.fa-wrap button:disabled { opacity: .5; cursor: not-allowed; }
@media (max-width: 420px) { .fa-actions .reset-btn { flex: 1 1 100%; } }
/* FA1-CSS-END */
</style>
'''
rep('<style id="m1-css">',CSS+'<style id="m1-css">','FA1-CSS')

# 4) HTML (inserito dopo il blocco Sync; il Centro Impostazioni lo sposta nel proprio gruppo)
HTML='''    <div class="fa-wrap" id="faAccount" aria-live="polite" data-fa-state="init">
      <p class="fa-net" id="faNet" hidden>&#128246; Sei offline: accesso e registrazione richiedono la connessione. L'archivio locale funziona normalmente.</p>
      <div id="faViewInit" data-fa-view="init"><p class="fa-note">Controllo dell'account in corso&hellip;</p></div>
      <div id="faViewUnavailable" data-fa-view="unavailable" hidden>
        <p class="fa-note">&#9888;&#65039; Il servizio account non &egrave; disponibile in questo momento (componente non caricato o stato non determinato). L'archivio locale funziona normalmente e nulla &egrave; stato modificato.</p>
        <button type="button" class="reset-btn" id="faRetryInit">Riprova</button>
      </div>
      <div id="faViewOut" data-fa-view="out" hidden>
        <p class="fa-note">L'account personale &egrave; <strong>facoltativo</strong>: puoi usare tutta la guida senza accedere. Per ora l'account serve solo a identificarti; <strong>non sincronizza ancora i tuoi dati</strong> e non modifica nulla di ci&ograve; che hai salvato su questo dispositivo.</p>
        <div class="fa-actions">
          <button type="button" class="reset-btn reset-btn-info" id="faGoLogin">Accedi</button>
          <button type="button" class="reset-btn" id="faGoRegister">Crea account</button>
        </div>
      </div>
      <form class="fa-form" id="faFormLogin" data-fa-view="login" novalidate hidden>
        <div class="fa-field"><label for="faLoginEmail">Email</label>
          <input class="fa-in" id="faLoginEmail" type="email" inputmode="email" autocomplete="email" autocapitalize="off" autocorrect="off" spellcheck="false" maxlength="254" required></div>
        <div class="fa-field"><label for="faLoginPw">Password</label>
          <div class="fa-pwrow"><input class="fa-in" id="faLoginPw" type="password" autocomplete="current-password" maxlength="128" required>
          <button type="button" class="reset-btn" data-fa-toggle="faLoginPw" aria-label="Mostra o nascondi la password" aria-pressed="false">Mostra</button></div></div>
        <div class="fa-actions"><button type="submit" class="reset-btn reset-btn-info" id="faLoginBtn">Accedi</button>
          <button type="button" class="fa-link" data-fa-go="reset">Password dimenticata?</button>
          <button type="button" class="fa-link" data-fa-go="register">Crea account</button>
          <button type="button" class="fa-link" data-fa-go="out">Annulla</button></div>
      </form>
      <form class="fa-form" id="faFormRegister" data-fa-view="register" novalidate hidden>
        <div class="fa-field"><label for="faRegEmail">Email</label>
          <input class="fa-in" id="faRegEmail" type="email" inputmode="email" autocomplete="email" autocapitalize="off" autocorrect="off" spellcheck="false" maxlength="254" required></div>
        <div class="fa-field"><label for="faRegPw">Password (almeno 8 caratteri)</label>
          <div class="fa-pwrow"><input class="fa-in" id="faRegPw" type="password" autocomplete="new-password" maxlength="128" minlength="8" required>
          <button type="button" class="reset-btn" data-fa-toggle="faRegPw" aria-label="Mostra o nascondi la password" aria-pressed="false">Mostra</button></div></div>
        <div class="fa-field"><label for="faRegPw2">Conferma password</label>
          <input class="fa-in" id="faRegPw2" type="password" autocomplete="new-password" maxlength="128" required></div>
        <p class="fa-hint">Ti invieremo un'email con un link per verificare l'indirizzo. La password non viene mai salvata nella guida.</p>
        <div class="fa-actions"><button type="submit" class="reset-btn reset-btn-info" id="faRegBtn">Crea account</button>
          <button type="button" class="fa-link" data-fa-go="login">Ho gi&agrave; un account</button>
          <button type="button" class="fa-link" data-fa-go="out">Annulla</button></div>
      </form>
      <form class="fa-form" id="faFormReset" data-fa-view="reset" novalidate hidden>
        <p class="fa-note">Inserisci l'email dell'account: se esiste, riceverai un link per scegliere una nuova password.</p>
        <div class="fa-field"><label for="faResetEmail">Email</label>
          <input class="fa-in" id="faResetEmail" type="email" inputmode="email" autocomplete="email" autocapitalize="off" autocorrect="off" spellcheck="false" maxlength="254" required></div>
        <div class="fa-actions"><button type="submit" class="reset-btn reset-btn-info" id="faResetBtn">Invia il link</button>
          <button type="button" class="fa-link" data-fa-go="login">Torna all'accesso</button></div>
      </form>
      <div id="faViewVerify" data-fa-view="verify" hidden>
        <span class="fa-badge fa-badge-warn">EMAIL DA VERIFICARE</span>
        <p class="fa-who" id="faVerifyWho"></p>
        <p class="fa-note">Abbiamo inviato un link di verifica a questo indirizzo. Aprilo (controlla anche lo spam), poi torna qui. L'account non &egrave; utilizzabile finch&eacute; l'email non &egrave; verificata.</p>
        <div class="fa-actions">
          <button type="button" class="reset-btn reset-btn-info" id="faCheckBtn">Ho verificato</button>
          <button type="button" class="reset-btn" id="faResendBtn">Reinvia il link</button>
          <button type="button" class="reset-btn" id="faLogoutBtn2">Esci</button>
        </div>
      </div>
      <div id="faViewIn" data-fa-view="in" hidden>
        <span class="fa-badge fa-badge-ok">ACCOUNT VERIFICATO</span>
        <p class="fa-who" id="faInWho"></p>
        <p class="fa-note">Sei collegato. I tuoi dati restano su questo dispositivo e <strong>non sono ancora sincronizzati con l'account</strong>: progressi, voti, XP, badge e Timeline non vengono letti n&eacute; modificati.</p>
        <div class="fa-actions"><button type="button" class="reset-btn" id="faLogoutBtn">Esci</button></div>
      </div>
      <p class="fa-msg" id="faMsg" role="status" hidden></p>
    </div>
'''
rep('''      <button type="button" id="syncDisconnectBtn" class="reset-btn" hidden>Disattiva sync su questo dispositivo</button>
    </div>
''','''      <button type="button" id="syncDisconnectBtn" class="reset-btn" hidden>Disattiva sync su questo dispositivo</button>
    </div>
'''+HTML,'id="faAccount"')

# 5) Centro Impostazioni: gruppo dedicato prima della Sincronizzazione cloud
rep("  var gS = grp('', 'Sincronizzazione cloud', null);\n",
    "  var gAcc = grp('', 'Account personale (facoltativo)', null);   // FA1\n  var gS = grp('', 'Sincronizzazione cloud', null);\n",'var gAcc = grp')
rep("gS.appendChild(sw); }\n","gS.appendChild(sw); }\n  var faA = $('faAccount'); if (faA) gAcc.appendChild(faA);   // FA1\n",'var faA = $')

# 6) Modulo JS isolato
JS=r'''<script id="fa1-js">/* FA1: autenticazione facoltativa email/password. Non legge/scrive il profilo, ne' localStorage, ne' RTDB. */
(function () {
  'use strict';
  var $ = function (i) { return document.getElementById(i); };
  var root = $('faAccount'); if (!root) return;
  var VIEWS = { init: 'faViewInit', unavailable: 'faViewUnavailable', out: 'faViewOut', login: 'faFormLogin', register: 'faFormRegister', reset: 'faFormReset', verify: 'faViewVerify', 'in': 'faViewIn' };
  var auth = null, busy = false, current = null, unsub = null, watchdog = null, resendUntil = 0, resendTimer = null, status = 'init', lastCreds = null;
  var OP_TIMEOUT = 20000, INIT_TIMEOUT = 8000, RESEND_COOLDOWN = 60;

  function show(view) {
    status = view; root.setAttribute('data-fa-state', view);
    Object.keys(VIEWS).forEach(function (k) { var e = $(VIEWS[k]); if (e) e.hidden = (k !== view); });
    clearPw();
  }
  function clearPw() { ['faLoginPw', 'faRegPw', 'faRegPw2'].forEach(function (i) { var e = $(i); if (e) { e.value = ''; e.type = 'password'; } }); root.querySelectorAll('[data-fa-toggle]').forEach(function (b) { b.textContent = 'Mostra'; b.setAttribute('aria-pressed', 'false'); }); }
  function msg(text, kind) { var m = $('faMsg'); if (!text) { m.hidden = true; m.textContent = ''; return; } m.hidden = false; m.className = 'fa-msg fa-msg-' + (kind || 'ok'); m.textContent = text; }
  function setBusy(b, label, btn) {
    busy = b; root.setAttribute('aria-busy', b ? 'true' : 'false');
    root.querySelectorAll('button, input').forEach(function (e) { if (b) { e.setAttribute('data-fa-was', e.disabled ? '1' : '0'); e.disabled = true; } else { e.disabled = e.getAttribute('data-fa-was') === '1' && false; e.removeAttribute('data-fa-was'); } });
    if (b) { if (btn) { btn.setAttribute('data-fa-label', btn.textContent); btn.textContent = label || 'Attendere…'; } }
    else { root.querySelectorAll('[data-fa-label]').forEach(function (x) { x.textContent = x.getAttribute('data-fa-label'); x.removeAttribute('data-fa-label'); }); refreshResend(); }
  }
  function online() { return typeof navigator === 'undefined' || navigator.onLine !== false; }
  function updateNet() { var n = $('faNet'); if (n) n.hidden = online(); }

  var MAP = {
    'auth/invalid-email': 'L’indirizzo email non è valido.',
    'auth/missing-email': 'Inserisci l’indirizzo email.',
    'auth/missing-password': 'Inserisci la password.',
    'auth/email-already-in-use': 'Esiste già un account con questa email. Prova ad accedere oppure usa “Password dimenticata?”.',
    'auth/weak-password': 'Password troppo debole: usa almeno 8 caratteri.',
    'auth/invalid-credential': 'Email o password non corretti.',
    'auth/wrong-password': 'Email o password non corretti.',
    'auth/user-not-found': 'Email o password non corretti.',
    'auth/invalid-login-credentials': 'Email o password non corretti.',
    'auth/user-disabled': 'Questo account è stato disabilitato.',
    'auth/too-many-requests': 'Troppi tentativi. Attendi qualche minuto e riprova.',
    'auth/network-request-failed': 'Connessione assente o instabile. Controlla la rete e riprova: nulla è stato modificato.',
    'auth/operation-not-allowed': 'L’accesso con email e password non è abilitato per questa app.',
    'auth/unauthorized-continue-uri': 'Dominio non autorizzato per il link di verifica. L’account non è stato compromesso: avvisa lo sviluppatore.',
    'auth/invalid-continue-uri': 'Indirizzo di ritorno del link non valido. Avvisa lo sviluppatore.',
    'auth/missing-continue-uri': 'Indirizzo di ritorno del link mancante. Avvisa lo sviluppatore.',
    'auth/requires-recent-login': 'Per questa operazione devi accedere di nuovo.',
    'auth/internal-error': 'Errore temporaneo del servizio. Riprova tra poco.',
    'auth/timeout': 'L’operazione ha impiegato troppo tempo. Riprova.',
    'auth/web-storage-unsupported': 'Il browser blocca l’archiviazione necessaria alla sessione. Disattiva la navigazione privata e riprova.',
    'auth/quota-exceeded': 'Limite di richieste del servizio raggiunto. Riprova più tardi.'
  };
  function errText(e) {
    var c = e && e.code ? String(e.code) : '';
    if (!online() && (!c || c === 'auth/network-request-failed')) c = 'auth/network-request-failed';
    var t = MAP[c] || 'Operazione non riuscita. Riprova.';
    return c && !MAP[c] ? t + ' (codice: ' + c.slice(0, 60) + ')' : t;
  }
  function withTimeout(p) {
    return new Promise(function (res, rej) {
      var t = setTimeout(function () { rej({ code: 'auth/timeout' }); }, OP_TIMEOUT);
      Promise.resolve(p).then(function (v) { clearTimeout(t); res(v); }, function (e) { clearTimeout(t); rej(e); });
    });
  }
  function emailOk(v) { return typeof v === 'string' && v.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v); }
  function actionSettings() {
    try { var l = location; if (l.protocol === 'https:' || l.hostname === 'localhost' || l.hostname === '127.0.0.1') return { url: l.origin + l.pathname, handleCodeInApp: false }; } catch (e) {}
    return null;
  }
  function sendVerif(u) { var a = actionSettings(); return a ? u.sendEmailVerification(a) : u.sendEmailVerification(); }

  /* ---- init / sessione ---- */
  function getAuth() {
    if (typeof firebase === 'undefined' || !firebase.auth || typeof FIREBASE_CONFIG === 'undefined') return null;
    try {
      if (!firebase.apps || !firebase.apps.length) firebase.initializeApp(FIREBASE_CONFIG);
      var a = firebase.auth(); a.languageCode = 'it'; return a;
    } catch (e) { return null; }
  }
  function startSession() {
    show('init'); msg('');
    if (unsub) { try { unsub(); } catch (e) {} unsub = null; }
    clearTimeout(watchdog);
    auth = getAuth();
    if (!auth) { show('unavailable'); return; }
    var got = false;
    watchdog = setTimeout(function () { if (!got) show('unavailable'); }, INIT_TIMEOUT);
    try {
      unsub = auth.onAuthStateChanged(function (u) { got = true; clearTimeout(watchdog); onUser(u); }, function () { got = true; clearTimeout(watchdog); show('unavailable'); });
    } catch (e) { show('unavailable'); }
  }
  function onUser(u) {
    current = u || null;
    if (!u) { if (status === 'in' || status === 'verify' || status === 'init' || status === 'unavailable') show('out'); return; }
    renderUser(u);
    if (!u.emailVerified && online() && u.reload) { u.reload().then(function () { if (auth && auth.currentUser === u) renderUser(u); }).catch(function () {}); }
  }
  function renderUser(u) {
    var who = (u.email || '').slice(0, 254);
    if (u.emailVerified) { $('faInWho').textContent = who; show('in'); }
    else { $('faVerifyWho').textContent = who; show('verify'); refreshResend(); }
  }
  function refreshResend() {
    var b = $('faResendBtn'); if (!b || busy) return; clearTimeout(resendTimer);
    var left = Math.ceil((resendUntil - Date.now()) / 1000);
    if (left > 0) { b.disabled = true; b.textContent = 'Reinvia il link (' + left + ' s)'; resendTimer = setTimeout(refreshResend, 1000); }
    else { b.disabled = false; b.textContent = 'Reinvia il link'; }
  }

  /* ---- azioni ---- */
  function run(btn, label, fn) {
    if (busy) return Promise.resolve();
    if (!online()) { msg(MAP['auth/network-request-failed'], 'err'); updateNet(); return Promise.resolve(); }
    if (!auth) auth = getAuth(); if (!auth) { show('unavailable'); return Promise.resolve(); }
    msg(label, 'busy'); setBusy(true, label, btn);
    return withTimeout(fn()).then(function (r) { setBusy(false); return r; }, function (e) { setBusy(false); msg(errText(e), 'err'); return null; });
  }
  function markInvalid(ids) { ['faLoginEmail', 'faLoginPw', 'faRegEmail', 'faRegPw', 'faRegPw2', 'faResetEmail'].forEach(function (i) { var e = $(i); if (e) e.removeAttribute('aria-invalid'); }); (ids || []).forEach(function (i) { var e = $(i); if (e) { e.setAttribute('aria-invalid', 'true'); } }); if (ids && ids.length) { var f = $(ids[0]); if (f && f.focus) try { f.focus(); } catch (x) {} } }

  $('faFormRegister').addEventListener('submit', function (ev) {
    ev.preventDefault(); markInvalid([]);
    var email = $('faRegEmail').value.trim(), p1 = $('faRegPw').value, p2 = $('faRegPw2').value;
    if (!emailOk(email)) { markInvalid(['faRegEmail']); return msg(MAP['auth/invalid-email'], 'err'); }
    if (p1.length < 8) { markInvalid(['faRegPw']); return msg(MAP['auth/weak-password'], 'err'); }
    if (p1.length > 128) { markInvalid(['faRegPw']); return msg('La password può avere al massimo 128 caratteri.', 'err'); }
    if (p1.toLowerCase() === email.toLowerCase()) { markInvalid(['faRegPw']); return msg('La password non può coincidere con l’email.', 'err'); }
    if (p1 !== p2) { markInvalid(['faRegPw2']); return msg('Le due password non coincidono.', 'err'); }
    run($('faRegBtn'), 'Creazione account…', function () {
      return auth.createUserWithEmailAndPassword(email, p1).then(function (cred) {
        var u = cred.user || auth.currentUser;
        return sendVerif(u).then(function () { resendUntil = Date.now() + RESEND_COOLDOWN * 1000; return 'sent'; }, function (e) { return { err: e }; }).then(function (r) {
          renderUser(u);
          if (r === 'sent') msg('Account creato. Ti abbiamo inviato l’email di verifica.', 'ok');
          else msg('Account creato, ma l’invio dell’email di verifica non è riuscito: ' + errText(r.err) + ' Usa “Reinvia il link”.', 'err');
        });
      });
    });
  });
  $('faFormLogin').addEventListener('submit', function (ev) {
    ev.preventDefault(); markInvalid([]);
    var email = $('faLoginEmail').value.trim(), pw = $('faLoginPw').value;
    if (!emailOk(email)) { markInvalid(['faLoginEmail']); return msg(MAP['auth/invalid-email'], 'err'); }
    if (!pw) { markInvalid(['faLoginPw']); return msg(MAP['auth/missing-password'], 'err'); }
    run($('faLoginBtn'), 'Accesso in corso…', function () {
      return auth.signInWithEmailAndPassword(email, pw).then(function (cred) {
        var u = cred.user || auth.currentUser;
        return (u.reload ? u.reload().catch(function () {}) : Promise.resolve()).then(function () { renderUser(u); msg(u.emailVerified ? 'Accesso eseguito.' : 'Accesso eseguito: verifica l’email per usare l’account.', u.emailVerified ? 'ok' : 'busy'); });
      });
    });
  });
  $('faFormReset').addEventListener('submit', function (ev) {
    ev.preventDefault(); markInvalid([]);
    var email = $('faResetEmail').value.trim();
    if (!emailOk(email)) { markInvalid(['faResetEmail']); return msg(MAP['auth/invalid-email'], 'err'); }
    run($('faResetBtn'), 'Invio in corso…', function () {
      var a = actionSettings();
      return (a ? auth.sendPasswordResetEmail(email, a) : auth.sendPasswordResetEmail(email)).then(null, function (e) { if (e && e.code === 'auth/user-not-found') return; throw e; }).then(function () {
        msg('Se l’indirizzo è registrato, riceverai a breve un’email con il link per scegliere una nuova password.', 'ok');
      });
    });
  });
  $('faResendBtn').addEventListener('click', function () {
    if (Date.now() < resendUntil) return;
    var u = auth && auth.currentUser; if (!u) return show('out');
    run($('faResendBtn'), 'Invio…', function () { return sendVerif(u).then(function () { resendUntil = Date.now() + RESEND_COOLDOWN * 1000; msg('Link di verifica inviato di nuovo. Controlla anche lo spam.', 'ok'); }); }).then(refreshResend);
  });
  function check() {
    var u = auth && auth.currentUser; if (!u) return show('out');
    return run($('faCheckBtn'), 'Controllo…', function () { return u.reload().then(function () { renderUser(u); msg(u.emailVerified ? 'Email verificata. Account attivo.' : 'L’email non risulta ancora verificata. Apri il link ricevuto e riprova.', u.emailVerified ? 'ok' : 'busy'); }); });
  }
  $('faCheckBtn').addEventListener('click', check);
  function logout() {
    if (busy) return; if (!auth) return show('out');
    msg('Uscita…', 'busy'); busy = true;
    withTimeout(auth.signOut()).then(function () { busy = false; show('out'); msg('Sei uscito dall’account. I dati restano su questo dispositivo, invariati.', 'ok'); }, function (e) { busy = false; msg(errText(e), 'err'); });
  }
  $('faLogoutBtn').addEventListener('click', logout); $('faLogoutBtn2').addEventListener('click', logout);
  $('faGoLogin').addEventListener('click', function () { msg(''); show('login'); $('faLoginEmail').focus(); });
  $('faGoRegister').addEventListener('click', function () { msg(''); show('register'); $('faRegEmail').focus(); });
  $('faRetryInit').addEventListener('click', startSession);
  root.addEventListener('click', function (ev) {
    var t = ev.target.closest ? ev.target.closest('[data-fa-go],[data-fa-toggle]') : null; if (!t || busy) return;
    var g = t.getAttribute('data-fa-go');
    if (g) { var carry = ''; var src = status === 'login' ? $('faLoginEmail') : status === 'register' ? $('faRegEmail') : status === 'reset' ? $('faResetEmail') : null; if (src) carry = src.value; msg(''); markInvalid([]); show(g); var dst = g === 'login' ? $('faLoginEmail') : g === 'register' ? $('faRegEmail') : g === 'reset' ? $('faResetEmail') : null; if (dst) { if (carry) dst.value = carry; try { dst.focus(); } catch (e) {} } return; }
    var tid = t.getAttribute('data-fa-toggle'); if (tid) { var inp = $(tid), sh = inp.type === 'password'; inp.type = sh ? 'text' : 'password'; t.textContent = sh ? 'Nascondi' : 'Mostra'; t.setAttribute('aria-pressed', sh ? 'true' : 'false'); if (tid === 'faRegPw') { var i2 = $('faRegPw2'); if (i2 && sh) i2.type = 'text'; else if (i2) i2.type = 'password'; } }
  });
  window.addEventListener('online', function () { updateNet(); if (status === 'unavailable') startSession(); });
  window.addEventListener('offline', updateNet);
  document.addEventListener('visibilitychange', function () { if (!document.hidden && status === 'verify' && online() && auth && auth.currentUser && !busy) { auth.currentUser.reload().then(function () { if (auth.currentUser && auth.currentUser.emailVerified) { renderUser(auth.currentUser); msg('Email verificata. Account attivo.', 'ok'); } }).catch(function () {}); } });

  try { Object.defineProperty(window, 'tvaAuth', { value: Object.freeze({ getStatus: function () { return status; } }), configurable: false }); } catch (e) {}
  updateNet();
  /* Avvio ritardato: nessun lavoro di rete finche' la pagina non e' caricata; il Firebase SDK si inizializza una volta sola. */
  if (document.readyState === 'complete') startSession(); else window.addEventListener('load', function () { setTimeout(startSession, 0); });
})();
</script>
'''
rep("<script>/* M341 */(function(){try{window.addEventListener('storage'", JS+"<script>/* M341 */(function(){try{window.addEventListener('storage'",'id="fa1-js"')

s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+BUILD,s)
open(P,'w',encoding='utf-8').write(s)
w=open(SW,encoding='utf-8').read()
w=re.sub(r"const SW_BUILD = '[^']*';","const SW_BUILD = '%s';"%BUILD,w)
w=re.sub(r"const CACHE_NAME = '[^']*';","const CACHE_NAME = 'marvel-timeline-cache-%s';"%BUILD,w)
open(SW,'w',encoding='utf-8').write(w)
print('ok',BUILD)
