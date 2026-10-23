/* RW-JS-BEGIN: Blocco 3.1 - Ricompense cosmetiche TVA (48). Quattro strati separati: 1) CATALOGO statico, 2) VALUTAZIONE dei requisiti
   (dati reali gia' esistenti, sola lettura), 3) STATO di sblocco (storico persistente), 4) PREFERENZE equipaggiate. Nessun XP, valuta o contatore nuovo. */
(function () {
  'use strict';
  var W = window, D = document;
  if (W.tvaRewards) return;

  /* ---------- 1) CATALOGO (versione 1) ----------
     id permanente = '<categoria>-<slug>'. 'tier': 1 iniziale (14), 2 intermedia (20), 3 avanzata (10), 4 leggendaria (4).
     'rar': c comune, n non comune, r raro, e epico, l leggendario. 'cond': condizione verificabile (vedi EVAL). */
  var VERSION = 1;
  var CATS = [['titolo', 'Titoli agente'], ['cornice', 'Cornici Tessera'], ['tema', 'Temi Tessera'], ['effetto', 'Effetti cosmetici']];
  function R(id, nome, desc, rar, tier, cond) { return { id: id, cat: id.split('-')[0], nome: nome, desc: desc, rar: rar, tier: tier, cond: cond }; }
  var CATALOG = [
    // --- Titoli agente (20) ---
    R('titolo-nuova-variante', 'Nuova Variante', 'Il titolo con cui ogni agente comincia.', 'c', 1, { k: 'always' }),
    R('titolo-recluta-tva', 'Recluta TVA', 'Primo titolo visionato.', 'c', 1, { k: 'titles', n: 1 }),
    R('titolo-osservatore-temporale', 'Osservatore Temporale', 'Chi osserva la Linea Temporale con costanza.', 'c', 1, { k: 'level', n: 2 }),
    R('titolo-custode-archivi', 'Custode degli Archivi', 'Chi annota e valuta ciò che vede.', 'c', 1, { k: 'ratings', n: 1 }),
    R('titolo-esploratore-multiverso', 'Esploratore del Multiverso', 'Chi attraversa più di un universo produttivo.', 'c', 1, { k: 'studios', n: 2 }),
    R('titolo-agente-del-tempo', 'Agente del Tempo', 'Un agente ormai operativo.', 'n', 2, { k: 'level', n: 5 }),
    R('titolo-analista-linee-temporali', 'Analista delle Linee Temporali', 'Venticinque titoli analizzati.', 'n', 2, { k: 'titles', n: 25 }),
    R('titolo-guardiano-nexus', 'Guardiano del Nexus', 'Prima missione TVA completata.', 'n', 2, { k: 'missions', n: 1 }),
    R('titolo-cacciatore-anomalie', 'Cacciatore di Anomalie', 'Tre distintivi conquistati.', 'n', 2, { k: 'badges', n: 3 }),
    R('titolo-archivista-supremo', 'Archivista Supremo', 'Cinque note personali negli archivi.', 'n', 2, { k: 'notes', n: 5 }),
    R('titolo-sorvegliante-incursioni', 'Sorvegliante delle Incursioni', 'Road to Doomsday completata.', 'r', 2, { k: 'rtd' }),
    R('titolo-custode-sacra-timeline', 'Custode della Sacra Timeline', 'Distintivo «Linea Sacra» ottenuto.', 'r', 2, { k: 'badge', id: 'linea-sacra' }),
    R('titolo-viaggiatore-vuoto', 'Viaggiatore del Vuoto', 'Metà della guida completata.', 'r', 2, { k: 'pct', n: 50 }),
    R('titolo-sentinella-multiverso', 'Sentinella del Multiverso', 'Almeno un titolo per ciascuno dei cinque studi.', 'r', 2, { k: 'studios', n: 5 }),
    R('titolo-maestro-varianti', 'Maestro delle Varianti', 'Distintivo «Cacciatore di Varianti» ottenuto.', 'r', 3, { k: 'badge', id: 'cacciatore-varianti' }),
    R('titolo-comandante-tva', 'Comandante TVA', 'Livello agente 14.', 'e', 3, { k: 'level', n: 14 }),
    R('titolo-architetto-temporale', 'Architetto Temporale', 'Tutti i titoli obbligatori visti (distintivo «Essenziale»).', 'e', 3, { k: 'badge', id: 'essenziale' }),
    R('titolo-sovrano-linee-temporali', 'Sovrano delle Linee Temporali', 'Due Stagioni TVA concluse (20 missioni).', 'e', 3, { k: 'seasons', n: 2 }),
    R('titolo-leggenda-multiverso', 'Leggenda del Multiverso', 'Tutti i 138 titoli visti.', 'e', 3, { k: 'titles', n: 'all' }),
    R('titolo-colui-che-rimane', 'Colui che Rimane', 'Rango massimo: guida completa, 14 distintivi e tutte le Serie Animate.', 'l', 4, { k: 'rankmax' }),
    // --- Cornici Tessera (12) ---
    R('cornice-standard-tva', 'Standard TVA', 'La cornice ufficiale, sempre disponibile.', 'c', 1, { k: 'always' }),
    R('cornice-bronzo-temporale', 'Bronzo Temporale', 'Cinque titoli visti.', 'c', 1, { k: 'titles', n: 5 }),
    R('cornice-argento-cronologico', 'Argento Cronologico', 'Livello agente 4.', 'c', 1, { k: 'level', n: 4 }),
    R('cornice-oro-archivista', "Oro dell'Archivista", 'Sei distintivi conquistati.', 'n', 2, { k: 'badges', n: 6 }),
    R('cornice-acciaio-mutante', 'Acciaio Mutante', 'Tutti i titoli dello studio Fox visti.', 'n', 2, { k: 'studioall', s: 'fox' }),
    R('cornice-energia-arcana', 'Energia Arcana', 'Distintivo «Collezionista» (tutti gli speciali).', 'r', 2, { k: 'badge', id: 'collezionista' }),
    R('cornice-tecnologia-stark', 'Tecnologia Stark', 'Quaranta titoli MCU visti.', 'r', 2, { k: 'studiocount', s: 'mcu', n: 40 }),
    R('cornice-wakanda', 'Wakanda', 'Venti serie viste.', 'r', 2, { k: 'typecount', t: 'serie', n: 20 }),
    R('cornice-asgard', 'Asgard', 'Distintivo «Cinefilo» (tutti i film).', 'e', 3, { k: 'badge', id: 'cinefilo' }),
    R('cornice-vuoto-temporale', 'Vuoto Temporale', 'Tre quarti della guida completati.', 'e', 3, { k: 'pct', n: 75 }),
    R('cornice-incursione-rossa', 'Incursione Rossa', 'Una Stagione TVA conclusa (10 missioni).', 'e', 3, { k: 'seasons', n: 1 }),
    R('cornice-nexus-supremo', 'Nexus Supremo', 'Tutti i 138 titoli visti e tre Stagioni TVA concluse.', 'l', 4, { k: 'all', of: [{ k: 'titles', n: 'all' }, { k: 'seasons', n: 3 }] }),
    // --- Temi Tessera (10) ---
    R('tema-tva-classico', 'TVA Classico', 'Il tema ufficiale, sempre disponibile.', 'c', 1, { k: 'always' }),
    R('tema-archivio-notturno', 'Archivio Notturno', 'Tre titoli preferiti.', 'c', 1, { k: 'favs', n: 3 }),
    R('tema-cronologia-dorata', 'Cronologia Dorata', 'Prima nota personale.', 'c', 1, { k: 'notes', n: 1 }),
    R('tema-multiverso-cremisi', 'Multiverso Cremisi', 'Tre missioni TVA completate.', 'n', 2, { k: 'missions', n: 3 }),
    R('tema-tecnologia-futuristica', 'Tecnologia Futuristica', 'Dieci voti assegnati.', 'n', 2, { k: 'ratings', n: 10 }),
    R('tema-universo-mutante', 'Universo Mutante', 'Cinque titoli Fox visti.', 'n', 2, { k: 'studiocount', s: 'fox', n: 5 }),
    R('tema-energia-mistica', 'Energia Mistica', 'Livello agente 10.', 'r', 2, { k: 'level', n: 10 }),
    R('tema-ombre-del-vuoto', 'Ombre del Vuoto', 'Dieci Serie Animate viste.', 'r', 3, { k: 'anim', n: 10 }),
    R('tema-nexus-cosmico', 'Nexus Cosmico', 'Tutte le Serie Animate viste.', 'e', 3, { k: 'anim', n: 'all' }),
    R('tema-fine-del-tempo', 'Fine del Tempo', 'Livello agente 18.', 'l', 4, { k: 'level', n: 18 }),
    // --- Effetti cosmetici (6) ---
    R('effetto-scansione-temporale', 'Scansione Temporale', 'Quindici titoli visti.', 'c', 1, { k: 'titles', n: 15 }),
    R('effetto-bagliore-dorato', 'Bagliore Dorato', 'Due distintivi conquistati.', 'c', 1, { k: 'badges', n: 2 }),
    R('effetto-energia-cremisi', 'Energia Cremisi', 'Cinque titoli preferiti.', 'c', 1, { k: 'favs', n: 5 }),
    R('effetto-distorsione-nexus', 'Distorsione Nexus', 'Cinque missioni TVA completate.', 'n', 2, { k: 'missions', n: 5 }),
    R('effetto-particelle-cosmiche', 'Particelle Cosmiche', 'Cinque Serie Animate viste.', 'r', 2, { k: 'anim', n: 5 }),
    R('effetto-aura-leggendaria', 'Aura Leggendaria', 'Tutti i 14 distintivi conquistati.', 'l', 4, { k: 'badges', n: 'all' })
  ];
  var BY_ID = {}; CATALOG.forEach(function (r) { BY_ID[r.id] = r; });
  var RAR = { c: 'Comune', n: 'Non comune', r: 'Raro', e: 'Epico', l: 'Leggendario' };
  var SLOT = { titolo: 'titolo', cornice: 'cornice', tema: 'tema', effetto: 'effetto' };
  var DEFAULTS = { titolo: 'titolo-nuova-variante', cornice: 'cornice-standard-tva', tema: 'tema-tva-classico', effetto: null };
  var KEY = 'marvel-ultimate-timeline-rewards';
  var ID_RE = /^(titolo|cornice|tema|effetto)-[a-z0-9-]{2,40}$/, DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

  /* ---------- 2) VALUTAZIONE (sola lettura sui dati esistenti) ---------- */
  function jget(key, def) { try { var v = JSON.parse(localStorage.getItem(key) || 'null'); return v === null || v === undefined ? def : v; } catch (e) { return def; } }
  function cnt(o, pos) { if (!o || typeof o !== 'object') return 0; return Object.keys(o).filter(function (k) { return pos ? o[k] > 0 : !!o[k]; }).length; }
  function snapshot() {
    var s = { total: 0, titles: 0, studios: {}, studioTot: {}, types: {}, badgesIds: {}, badges: 0, badgesTot: 0, anim: 0, animTot: 0 };
    var checks = D.querySelectorAll('.watch-check');
    s.total = checks.length;
    Array.prototype.forEach.call(checks, function (c) {
      var w = c.closest ? c.closest('.card-wrap') : null, st = w && w.getAttribute('data-studio'), ty = w && w.getAttribute('data-type');
      if (st) s.studioTot[st] = (s.studioTot[st] || 0) + 1;
      if (c.checked) { s.titles++; if (st) s.studios[st] = (s.studios[st] || 0) + 1; if (ty) s.types[ty] = (s.types[ty] || 0) + 1; }
    });
    var an = D.querySelectorAll('.anim-watch-check'); s.animTot = an.length;
    Array.prototype.forEach.call(an, function (c) { if (c.checked) s.anim++; });
    var chips = D.querySelectorAll('.badge-chip'); s.badgesTot = chips.length;
    Array.prototype.forEach.call(chips, function (c) { if (c.classList.contains('badge-unlocked')) { s.badges++; s.badgesIds[(c.id || '').replace(/^badge-/, '')] = true; } });
    s.ratings = cnt(jget('marvel-ultimate-timeline-ratings', {}), true);
    s.favs = cnt(jget('marvel-ultimate-timeline-favorites', {}), false);
    s.notes = Object.keys(jget('marvel-ultimate-timeline-notes', {}) || {}).length;
    var bank = jget('marvel-ultimate-timeline-missioni-xp-bonus', null), list = bank && Array.isArray(bank.ricompensate) ? bank.ricompensate : [];
    s.missions = list.filter(function (k) { return typeof k === 'string' && k !== 'road-to-doomsday-v1' && /-(settimanale|tematica|saga|segreta)/.test(k); }).length;
    var ts = jget('marvel-ultimate-timeline-titoli-stagione', []); s.seasons = Array.isArray(ts) ? ts.length : 0;
    var rtd = jget('marvel-ultimate-timeline-road-to-doomsday', null); s.rtd = !!(rtd && rtd.completata === true) || list.indexOf('road-to-doomsday-v1') !== -1;
    var xi = W.marvelXpInfo; s.level = xi && typeof xi.livello === 'number' ? xi.livello : null; s.xp = xi && typeof xi.xp === 'number' ? xi.xp : null;
    s.ready = s.total > 0 && s.badgesTot > 0 && s.level !== null;
    return s;
  }
  function res(cur, tot) { return { cur: Math.min(cur, tot), tot: tot, ok: cur >= tot }; }
  var EVAL = {
    always: function () { return { cur: 1, tot: 1, ok: true }; },
    level: function (s, c) { return s.level === null ? { cur: 0, tot: c.n, ok: false } : res(s.level, c.n); },
    titles: function (s, c) { return res(s.titles, c.n === 'all' ? s.total : c.n); },
    pct: function (s, c) { var need = Math.ceil(s.total * c.n / 100); return res(s.titles, need); },
    studios: function (s, c) { return res(Object.keys(s.studios).length, c.n); },
    studiocount: function (s, c) { return res(s.studios[c.s] || 0, c.n); },
    studioall: function (s, c) { var t = s.studioTot[c.s] || 0; return t ? res(s.studios[c.s] || 0, t) : { cur: 0, tot: 1, ok: false }; },
    typecount: function (s, c) { return res(s.types[c.t] || 0, c.n); },
    badges: function (s, c) { return res(s.badges, c.n === 'all' ? s.badgesTot : c.n); },
    badge: function (s, c) { return { cur: s.badgesIds[c.id] ? 1 : 0, tot: 1, ok: !!s.badgesIds[c.id] }; },
    missions: function (s, c) { return res(s.missions, c.n); },
    seasons: function (s, c) { return res(s.seasons, c.n); },
    rtd: function (s) { return { cur: s.rtd ? 1 : 0, tot: 1, ok: s.rtd }; },
    ratings: function (s, c) { return res(s.ratings, c.n); },
    notes: function (s, c) { return res(s.notes, c.n); },
    favs: function (s, c) { return res(s.favs, c.n); },
    anim: function (s, c) { return res(s.anim, c.n === 'all' ? s.animTot : c.n); },
    rankmax: function (s) { var ok = s.total > 0 && s.titles >= s.total && s.badgesTot > 0 && s.badges >= s.badgesTot && s.animTot > 0 && s.anim >= s.animTot; return { cur: ok ? 1 : 0, tot: 1, ok: ok }; },
    all: function (s, c) { var parts = c.of.map(function (x) { return check(x, s); }), ok = parts.every(function (p) { return p.ok; }), first = parts.filter(function (p) { return !p.ok; })[0] || parts[0]; return { cur: first.cur, tot: first.tot, ok: ok }; }
  };
  function check(cond, snap) { var f = EVAL[cond.k]; if (!f) return { cur: 0, tot: 1, ok: false }; try { return f(snap, cond); } catch (e) { return { cur: 0, tot: 1, ok: false }; } }

  /* ---------- 3-4) STATO di sblocco + PREFERENZE (una sola chiave versionata, validata in lettura) ---------- */
  function isObj(v) { return v !== null && typeof v === 'object' && !Array.isArray(v); }
  function sanitize(o) {
    var st = { v: VERSION, u: {}, e: {}, t: {} };
    if (!isObj(o)) return st;
    if (isObj(o.u)) Object.keys(o.u).forEach(function (id) { if (ID_RE.test(id) && typeof o.u[id] === 'string' && DATE_RE.test(o.u[id])) st.u[id] = o.u[id]; });
    if (isObj(o.e)) Object.keys(SLOT).forEach(function (sl) { var v = o.e[sl]; if (v === null || (typeof v === 'string' && ID_RE.test(v))) st.e[sl] = v; });
    if (isObj(o.t)) Object.keys(SLOT).forEach(function (sl) { var v = o.t[sl]; if (typeof v === 'number' && isFinite(v) && v > 0) st.t[sl] = v; });
    return st;
  }
  var corruptNoted = false;
  function load() {
    var raw = null;
    try { raw = localStorage.getItem(KEY); } catch (e) { return sanitize(null); }
    if (raw === null) return sanitize(null);
    try { return sanitize(JSON.parse(raw)); }
    catch (e) {   // dato corrotto: lo si conserva (copia una sola volta) e si riparte da uno stato vuoto, senza propagare l'errore
      if (!corruptNoted) { corruptNoted = true; try { if (localStorage.getItem(KEY + '-bak') === null) localStorage.setItem(KEY + '-bak', raw); } catch (e2) {} }
      return sanitize(null);
    }
  }
  function save(st) { try { localStorage.setItem(KEY, JSON.stringify(st)); return true; } catch (e) { return false; } }
  function today() { var d = new Date(), p = function (n) { return (n < 10 ? '0' : '') + n; }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()); }

  // i predefiniti (cond 'always') sono sempre disponibili e NON vengono scritti: un profilo nuovo non genera alcuna scrittura/sincronizzazione
  function isUnlocked(id, st) { st = st || load(); var r = BY_ID[id]; return !!r && (r.cond.k === 'always' || !!st.u[id]); }
  function unlockedIds(st) { st = st || load(); return CATALOG.filter(function (r) { return isUnlocked(r.id, st); }).map(function (r) { return r.id; }); }
  // preferenza effettiva: quella salvata se valida (categoria giusta, nel catalogo, sbloccata), altrimenti il predefinito. Il dato salvato NON viene toccato.
  function effective(st) {
    st = st || load(); var out = {};
    Object.keys(SLOT).forEach(function (sl) {
      var v = st.e[sl];
      if (v && BY_ID[v] && BY_ID[v].cat === sl && isUnlocked(v, st)) out[sl] = v;
      else out[sl] = DEFAULTS[sl];
    });
    return out;
  }
  function equip(slot, id) {
    if (!SLOT[slot]) return { ok: false, reason: 'slot' };
    var st = load();
    if (id === null) { if (slot !== 'effetto') return { ok: false, reason: 'obbligatorio' }; }
    else {
      var r = BY_ID[id]; if (!r) return { ok: false, reason: 'sconosciuta' };
      if (r.cat !== slot) return { ok: false, reason: 'categoria' };
      if (!isUnlocked(id, st)) return { ok: false, reason: 'bloccata' };
    }
    st.e[slot] = id; st.t[slot] = Date.now();
    if (!save(st)) return { ok: false, reason: 'salvataggio' };
    notify('equip'); return { ok: true };
  }
  function resetUnlocks() { var st = load(); st.u = {}; save(st); notify('reset'); }
  // unione per la sincronizzazione: lo stato di sblocco segue il profilo che arriva (come visti e XP); per ogni preferenza vince la piu' recente
  function merge(localRaw, remote) {
    var a = sanitize((function () { try { return JSON.parse(localRaw || 'null'); } catch (e) { return null; } })()), b = sanitize(remote), out = { v: VERSION, u: b.u, e: {}, t: {} };
    Object.keys(SLOT).forEach(function (sl) {
      var ta = a.t[sl] || 0, tb = b.t[sl] || 0, pick = (tb > ta || (ta === 0 && tb === 0 && b.e[sl] !== undefined)) ? b : a;
      if (pick.e[sl] !== undefined) out.e[sl] = pick.e[sl];
      if (pick.t[sl]) out.t[sl] = pick.t[sl];
    });
    return JSON.stringify(out);
  }

  function evaluate() {
    var snap = snapshot(); if (!snap.ready) return [];
    var st = load(), added = [];
    CATALOG.forEach(function (r) { if (r.cond.k === 'always' || st.u[r.id]) return; if (check(r.cond, snap).ok) { st.u[r.id] = today(); added.push(r.id); } });
    if (added.length && save(st)) {
      var vis = added;
      if (vis.length) toast('🎴 ' + (vis.length === 1 ? 'Nuova ricompensa cosmetica: ' + BY_ID[vis[0]].nome : vis.length + ' nuove ricompense cosmetiche sbloccate'));
      notify('unlock', added);
    }
    return added;
  }
  function notify(type, ids) { try { D.dispatchEvent(new CustomEvent('tva:rewards', { detail: { type: type, ids: ids || [] } })); } catch (e) {} }
  function toast(msg) { try { var t = D.createElement('div'); t.className = 'lv-toast-msg'; t.setAttribute('role', 'status'); t.textContent = msg; D.body.appendChild(t); setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 3200); } catch (e) {} }
  var timer = 0;
  // Blocco 4.0E: segnale esplicito di «prima valutazione post-caricamento completata». La sincronizzazione cloud attende questo
  // segnale (non un ritardo fisso) prima di confrontare il profilo locale: la valutazione scrive 'rewards' in modo asincrono.
  var loaded = (D.readyState === 'complete'), readyDone = false, readyRes = null;
  var readyP = new Promise(function (res) { readyRes = res; });
  function settle(ok, ev) { if (readyDone) return; readyDone = true; readyRes({ ok: ok, evaluated: ev }); }
  function schedule() { if (timer) return; timer = setTimeout(function () { timer = 0; var ok = true, ev = false; try { ev = !!snapshot().ready; evaluate(); } catch (e) { ok = false; if (W.console) console.error('Ricompense TVA:', e); } if (loaded && !timer) settle(ok, ev); }, 80); }

  W.tvaRewards = {
    version: VERSION, catalog: CATALOG, categories: CATS.map(function (c) { return c[0]; }), defaults: DEFAULTS, rarities: RAR, storageKey: KEY,
    state: function () { return load(); }, unlocked: function () { return unlockedIds(); }, equipped: function () { return effective(); }, isUnlocked: isUnlocked, equip: equip,
    ready: readyP, idle: function () { return !timer; },
    evaluate: evaluate, snapshot: snapshot, progress: function (id) { var r = BY_ID[id]; return r ? check(r.cond, snapshot()) : null; },
    resetUnlocks: resetUnlocks, merge: merge
  };
  // aggiornamento: dopo ogni ricalcolo della Tessera (XP/livello/distintivi), a missioni aggiornate e al caricamento
  function boot() {
    schedule();
    var x = D.getElementById('tesseraXpTotale');
    if (x && W.MutationObserver) new MutationObserver(schedule).observe(x, { childList: true, characterData: true, subtree: true });
    D.addEventListener('tva:missioni2', schedule);
    W.addEventListener('load', function () { loaded = true; schedule(); setTimeout(schedule, 400); });
    setTimeout(schedule, 800);
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})();
/* RW-JS-END */
