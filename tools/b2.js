/* B2-JS-BEGIN: Centrale TVA (Panoramica / Missioni / Operazioni / Strumenti). Riorganizza i componenti ESISTENTI (stessi nodi, stessi id, stessi listener): nulla viene duplicato o riscritto. */
(function () {
  'use strict';
  var D = document, W = window, H = D.documentElement;
  function $(i) { return D.getElementById(i); }
  function el(t, c, x) { var e = D.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var dash = $('dashboard'); if (!dash || dash.__cen) return; dash.__cen = true;
  dash.classList.add('cen');
  function move(node, to, before) { if (node && to) { if (before) to.insertBefore(node, before); else to.appendChild(node); } return node; }
  function titleOf(id) { var t = D.querySelector('#item-' + id + ' .title'); return t ? t.textContent.trim() : ('Scheda ' + id); }
  function numOf(id) { try { return W.marvelNumeroVisibile ? W.marvelNumeroVisibile(id) : id; } catch (e) { return id; } }
  function seen(id) { var c = D.querySelector('.watch-check[data-item="' + id + '"]'); return !!(c && c.checked); }
  function info() { return W.marvelMissioniInfo || {}; }

  /* ---------- guscio: intestazione, navigazione a 4 sezioni, pannelli ---------- */
  var head = dash.querySelector('.dash-head');
  if (head) { var h2 = head.querySelector('h2'); if (h2) h2.textContent = 'Centrale TVA'; var sub = head.querySelector('.part-sub'); if (sub) sub.textContent = 'Il centro operativo della tua Variante: stato, missioni, operazioni e strumenti.'; head.classList.add('cen-head'); }
  var SECS = [['panoramica', '📊', 'Panoramica'], ['missioni', '🎯', 'Missioni'], ['operazioni', '🛠️', 'Operazioni'], ['strumenti', '🧰', 'Strumenti']];
  var nav = el('div', 'cen-nav'); nav.setAttribute('role', 'tablist'); nav.setAttribute('aria-label', 'Sezioni della Centrale TVA');
  var panels = {};
  SECS.forEach(function (s) {
    var b = el('button', 'cen-tab'); b.type = 'button'; b.id = 'cenTab-' + s[0]; b.setAttribute('role', 'tab'); b.setAttribute('aria-controls', 'cenPan-' + s[0]); b.setAttribute('data-sec', s[0]);
    b.innerHTML = '<span class="cen-tab-ic" aria-hidden="true">' + s[1] + '</span><span class="cen-tab-l">' + s[2] + '</span>';
    nav.appendChild(b);
    var p = el('div', 'cen-panel'); p.id = 'cenPan-' + s[0]; p.setAttribute('role', 'tabpanel'); p.setAttribute('aria-labelledby', b.id); p.setAttribute('data-sec', s[0]); p.hidden = true; panels[s[0]] = p;
  });
  head.after(nav); var anchor = nav; SECS.forEach(function (s) { anchor.after(panels[s[0]]); anchor = panels[s[0]]; });

  /* ---------- PANORAMICA ---------- */
  var P = panels.panoramica;
  var agent = el('section', 'cen-agent'); agent.setAttribute('aria-label', 'Agente e livello');
  agent.innerHTML = '<div class="cen-ag-top"><div class="cen-ag-id"><span class="cen-ag-kick">AGENTE TVA</span><span class="cen-ag-name" data-f="name">Variante</span><span class="cen-ag-var" data-f="var">VAR-000000</span></div>' +
    '<div class="cen-ag-rank"><span class="cen-ag-rk" data-f="rank">Recluta</span><span class="cen-ag-lv">LV. <b data-f="lv">1</b></span></div></div>' +
    '<div class="cen-ag-xp"><div class="cen-bar" role="progressbar" aria-label="Progresso verso il livello successivo" aria-valuemin="0" aria-valuemax="100"><i data-f="bar"></i></div><div class="cen-ag-xpl"><span><b data-f="xp">0</b> XP</span><span data-f="xpsub">—</span></div></div>' +
    '<div class="cen-ag-bot"><span>Distintivi <b data-f="badges">0/14</b></span><button type="button" class="cen-link" data-act="tessera">Apri la Tessera ›</button></div>';
  P.appendChild(agent);
  function setF(root, f, v) { var n = root.querySelector('[data-f="' + f + '"]'); if (n) n.textContent = v; }
  function refreshAgent() {
    var nm = $('tesseraNameInput'), g = function (i) { var e = $(i); return e ? e.textContent.trim() : ''; };
    setF(agent, 'name', (nm && nm.value.trim()) || 'Variante'); setF(agent, 'var', g('tesseraId')); setF(agent, 'rank', g('tesseraRank')); setF(agent, 'lv', g('tesseraLivello'));
    setF(agent, 'xp', g('tesseraXpTotale')); setF(agent, 'xpsub', g('tesseraXpSub')); setF(agent, 'badges', g('tesseraBadges'));
    var f = $('tesseraXpFill'), w = (f && f.style.width) || '0%', bar = agent.querySelector('[data-f="bar"]'); if (bar) bar.style.width = w;
    var pb = agent.querySelector('.cen-bar'); if (pb) pb.setAttribute('aria-valuenow', String(parseInt(w, 10) || 0));
  }
  move($('dashHoloFill') && dash.querySelector('.dash-holo-main'), P);
  move($('dashLastNext'), P);
  var mprev = el('section', 'cen-card cen-prev'); mprev.innerHTML = '<div class="cen-card-h"><h3>Missioni attive</h3><button type="button" class="cen-link" data-go-sec="missioni" data-go-sub="attive">Tutte ›</button></div><div class="cen-prev-rows" data-f="rows"></div>';
  P.appendChild(mprev);
  var sprev = el('section', 'cen-card cen-prev'); sprev.innerHTML = '<div class="cen-card-h"><h3>Stagione in corso</h3><button type="button" class="cen-link" data-go-sec="missioni" data-go-sub="stagioni">Dettagli ›</button></div><div class="cen-prev-rows" data-f="srows"></div>';
  P.appendChild(sprev);
  var short = el('section', 'cen-short'); short.setAttribute('aria-label', 'Collegamenti rapidi');
  short.innerHTML = '<button type="button" class="cen-sbtn" data-go-sec="missioni">🎯<span>Missioni</span></button><button type="button" class="cen-sbtn" data-go-sec="operazioni">🛠️<span>Operazioni</span></button><button type="button" class="cen-sbtn" data-go-sec="strumenti">🧰<span>Strumenti</span></button><button type="button" class="cen-sbtn" data-act="atlante">🗺️<span>Atlante</span></button>';
  P.appendChild(short);
  move($('bollettinoBox'), P);
  var MROWS = [['missioneSettimanale', 'settimanale'], ['missioneTematica', 'tematica'], ['missioneSaga', 'saga'], ['missioneSegreta', 'segreta']];
  function refreshPreview() {
    var host = mprev.querySelector('[data-f="rows"]'); host.textContent = '';
    MROWS.forEach(function (m) {
      var r = $(m[0]); if (!r) return;
      var t = (r.querySelector('.missione-testo') || {}).textContent || '—', fr = (r.querySelector('.missione-frac') || {}).textContent || '', pct = (r.querySelector('.missione-fill') || { style: {} }).style.width || '0%', done = r.classList.contains('missione-completa');
      var row = el('button', 'cen-pr' + (done ? ' cen-pr-done' : '')); row.type = 'button'; row.setAttribute('data-mission', m[1]);
      row.innerHTML = '<span class="cen-pr-t">' + esc(t.trim()) + '</span><span class="cen-pr-f">' + (done ? '✓' : esc(fr)) + '</span><span class="cen-bar cen-bar-s"><i style="width:' + esc(done ? '100%' : pct) + '"></i></span>';
      host.appendChild(row);
    });
    var sh = sprev.querySelector('[data-f="srows"]'); sh.textContent = '';
    var num = ($('stagioneTvaNum') || {}).textContent || '', nome = ($('stagioneTvaNome') || {}).textContent || '', fr2 = ($('stagioneTvaFrac') || {}).textContent || '0/10', w2 = ($('stagioneTvaFill') || { style: {} }).style.width || '0%';
    var sr = el('button', 'cen-pr'); sr.type = 'button'; sr.setAttribute('data-mission', 'stagione');
    sr.innerHTML = '<span class="cen-pr-t">' + esc(num.trim()) + ' · ' + esc(nome.trim()) + '</span><span class="cen-pr-f">' + esc(fr2) + '</span><span class="cen-bar cen-bar-s"><i style="width:' + esc(w2) + '"></i></span>';
    sh.appendChild(sr);
  }

  /* ---------- MISSIONI ---------- */
  var M = panels.missioni;
  var SUBS = [['attive', 'Attive'], ['stagioni', 'Stagioni'], ['speciali', 'Speciali'], ['archivio', 'Archivio']];
  var subnav = el('div', 'cen-subnav'); subnav.setAttribute('role', 'tablist'); subnav.setAttribute('aria-label', 'Tipi di missione');
  var subp = {};
  SUBS.forEach(function (s) {
    var b = el('button', 'cen-stab', s[1]); b.type = 'button'; b.id = 'cenSub-' + s[0]; b.setAttribute('role', 'tab'); b.setAttribute('data-sub', s[0]); b.setAttribute('aria-controls', 'cenSubPan-' + s[0]); subnav.appendChild(b);
    var p = el('div', 'cen-subpanel'); p.id = 'cenSubPan-' + s[0]; p.setAttribute('role', 'tabpanel'); p.setAttribute('aria-labelledby', b.id); p.hidden = true; subp[s[0]] = p;
  });
  M.appendChild(subnav); SUBS.forEach(function (s) { M.appendChild(subp[s[0]]); });
  // Attive: le quattro missioni esistenti (stessi nodi e id), sempre aperte, ciascuna con il proprio dossier
  var dm = $('dashMissioni'); if (dm) { dm.open = true; var dsum = dm.querySelector('summary'); if (dsum) dsum.addEventListener('click', function (e) { e.preventDefault(); }); subp.attive.appendChild(dm); dm.classList.add('cen-dm'); }
  // Stagioni
  var stag = $('stagioneTvaCard'); if (stag) subp.stagioni.appendChild(stag);
  var stagDos = el('div', 'cen-dos cen-dos-open'); stagDos.id = 'cenDos-stagione'; subp.stagioni.appendChild(stagDos);
  // Speciali
  var rtd = $('roadToDoomsday'); if (rtd) subp.speciali.appendChild(rtd);
  var rtdDos = el('div', 'cen-dos cen-dos-open'); rtdDos.id = 'cenDos-rtd'; subp.speciali.appendChild(rtdDos);
  // Archivio
  var arch = el('div', 'cen-arch'); arch.id = 'cenArchive'; subp.archivio.appendChild(arch);

  var MDEF = {
    settimanale: { t: 'Completa 3 titoli questa settimana', d: 'Segna come visti 3 titoli qualsiasi della guida durante la settimana in corso (da lunedì a domenica).', req: function (s) { return 'Titoli visti questa settimana: ' + s.cur + ' su ' + s.tot + '.'; } },
    tematica: { d: 'Segna come visto almeno un titolo della categoria indicata, non ancora visto all’inizio della settimana.', req: function (s) { return 'Almeno 1 titolo della categoria della settimana.'; } },
    saga: { d: 'Completa tutti i titoli della saga scelta per la settimana.', req: function (s) { return 'Titoli visti: ' + s.cur + ' su ' + s.tot + '.'; } },
    segreta: { d: 'La TVA non rivela l’obiettivo finché non lo hai raggiunto.', req: function (s) { return s.done ? 'Obiettivo raggiunto.' : 'Obiettivo nascosto.'; } }
  };
  function weekEnd() { var d = new Date(); d.setHours(0, 0, 0, 0); var k = (d.getDay() + 6) % 7; d.setDate(d.getDate() + (6 - k)); return d; }
  function fmtDate(d) { return d.toLocaleDateString('it-IT', { weekday: 'long', day: 'numeric', month: 'long' }); }
  function workChip(id, extra) {
    var b = el('button', 'cen-work' + (seen(id) ? ' cen-work-seen' : '')); b.type = 'button'; b.setAttribute('data-cen-item', id);
    b.setAttribute('aria-label', 'Apri la scheda N° ' + numOf(id) + ' ' + titleOf(id) + (seen(id) ? ' (visto)' : ' (da vedere)'));
    b.innerHTML = '<span class="cen-work-n">N°' + esc(numOf(id)) + '</span><span class="cen-work-t">' + esc(titleOf(id)) + '</span><span class="cen-work-s" aria-hidden="true">' + (seen(id) ? '✓' : '›') + '</span>';
    return b;
  }
  function worksBlock(label, ids) {
    var d = el('details', 'cen-works'); var s = el('summary', '', label + ' (' + ids.length + ')'); d.appendChild(s);
    var box = el('div', 'cen-works-b'); ids.forEach(function (id) { box.appendChild(workChip(id)); }); d.appendChild(box); return d;
  }
  function buildDossier(key) {
    var mi = info(), st = (mi.stato || {})[key], box = el('div', 'cen-dos-in');
    if (!st) { box.appendChild(el('p', 'cen-note', 'Dati della missione non ancora disponibili: aprila di nuovo tra un istante.')); return box; }
    var def = MDEF[key], row = $({ settimanale: 'missioneSettimanale', tematica: 'missioneTematica', saga: 'missioneSaga', segreta: 'missioneSegreta' }[key]);
    var title = row ? ((row.querySelector('.missione-testo') || {}).textContent || def.t).trim() : (def.t || '');
    var dl = el('dl', 'cen-dl');
    function add(k, v, html) { dl.appendChild(el('dt', '', k)); var dd = el('dd'); if (html) dd.innerHTML = v; else dd.textContent = v; dl.appendChild(dd); }
    add('Descrizione', def.d);
    add('Requisiti', def.req(st));
    add('Stato', st.done ? 'Completata' + (st.rewarded ? ' · ricompensa già assegnata' : '') : 'In corso');
    var rew = '+' + st.xp + ' XP' + (key === 'segreta' ? ' · distintivo «Cacciatore di Varianti»' : '');
    add('Ricompensa', rew);
    add('Scadenza', 'domenica ' + weekEnd().toLocaleDateString('it-IT', { day: 'numeric', month: 'long' }) + ' (poi la missione si rinnova)');
    box.appendChild(dl);
    if (key === 'segreta') {
      if (st.done && st.id) { var h = el('p', 'cen-note', 'Titolo scoperto:'); box.appendChild(h); box.appendChild(workChip(st.id)); }
      else box.appendChild(el('p', 'cen-note', 'Per proteggere la sorpresa, titolo e indizi restano nascosti fino al completamento.'));
    } else {
      // tematica/saga in corso: i titoli ancora da vedere sono quelli gia' proposti dal componente esistente (.tva-mis, mostrato sotto il dossier)
      var ids = key === 'settimanale' ? (st.ids || []) : key === 'tematica' ? ((mi.tematica && mi.tematica.ids) || []) : ((mi.saga && mi.saga.ids) || []);
      var lab = key === 'settimanale' ? 'Titoli registrati questa settimana' : key === 'tematica' ? 'Titoli idonei' : 'Titoli della saga';
      if (key === 'settimanale') { if (ids.length) box.appendChild(worksBlock(lab, ids)); else box.appendChild(el('p', 'cen-note', 'Nessun titolo registrato finora: segna un titolo come visto nella Timeline.')); }
      else if (st.done && ids.length) box.appendChild(worksBlock(lab, ids));
    }
    return box;
  }
  // dossier apribile per ciascuna missione attiva
  MROWS.forEach(function (m) {
    var r = $(m[0]); if (!r) return;
    var b = el('button', 'cen-dbtn', 'Dossier'); b.type = 'button'; b.setAttribute('aria-expanded', 'false'); b.setAttribute('data-mission', m[1]);
    var dos = el('div', 'cen-dos'); dos.hidden = true; dos.id = 'cenDos-' + m[1]; b.setAttribute('aria-controls', dos.id);
    r.appendChild(b); r.appendChild(dos); r.setAttribute('data-cen-m', m[1]);
    b.addEventListener('click', function () { toggleDossier(m[1]); });
  });
  function toggleDossier(key, force) {
    var dos = $('cenDos-' + key), b = D.querySelector('.cen-dbtn[data-mission="' + key + '"]'); if (!dos || !b) return;
    var open = force === undefined ? dos.hidden : force;
    dos.hidden = !open; var rw = b.closest('.missione-row'); if (rw) rw.classList.toggle('cen-open', open); b.setAttribute('aria-expanded', open ? 'true' : 'false'); b.textContent = open ? 'Chiudi dossier' : 'Dossier';
    if (open) { dos.textContent = ''; dos.appendChild(buildDossier(key)); }
  }
  function renderStagione() {
    var mi = info(), s = mi.stagione; stagDos.textContent = ''; var box = el('div', 'cen-dos-in');
    if (!s) { stagDos.appendChild(box); return; }
    var dl = el('dl', 'cen-dl');
    function add(k, v) { dl.appendChild(el('dt', '', k)); dl.appendChild(el('dd', '', v)); }
    add('Descrizione', 'Ogni missione completata, di qualunque tipo, conta per la stagione in corso. A quota 10 la stagione si chiude e ne parte una nuova.');
    add('Progresso', s.prog + ' su 10 missioni (' + (s.idx + 1) + 'ª stagione)');
    add('Ricompense', '+500 XP e il titolo Variante «' + s.titolo + '» alla chiusura della stagione');
    add('Scadenza', 'Nessuna: la stagione avanza con le missioni completate.');
    box.appendChild(dl);
    var done = (mi.titoliStagione || []);
    if (done.length) { var p = el('p', 'cen-note', 'Stagioni concluse: ' + done.join(' · ')); box.appendChild(p); }
    stagDos.appendChild(box);
  }
  function renderRtd() {
    rtdDos.textContent = ''; var box = el('div', 'cen-dos-in'); var fr = ($('rtdFrac') || {}).textContent || '0/16', stt = ($('rtdStato') || {}).textContent || '';
    var dl = el('dl', 'cen-dl');
    function add(k, v) { dl.appendChild(el('dt', '', k)); dl.appendChild(el('dd', '', v)); }
    add('Requisiti', 'Vedere le 16 schede del percorso (' + fr + '). Il progresso è automatico: legge gli stessi titoli visti della Timeline.');
    add('Stato', stt);
    add('Ricompensa', '+300 XP e il distintivo «Sopravvissuto all’Incursione» (assegnati una sola volta)');
    add('Scadenza', 'Nessuna.');
    box.appendChild(dl); rtdDos.appendChild(box);
  }
  function parseKey(k, mi) {
    if (k === 'road-to-doomsday-v1') return { w: 'Speciali', ic: '🌀', t: 'Road to Doomsday — Operazione Incursione', xp: (mi.rtdXp || 300) };
    var m = /^(\d{4}-W\d{2})-(settimanale|tematica|saga|segreta)(?:-(.+))?$/.exec(k); if (!m) return { w: '', ic: '•', t: k, xp: 0 };
    var st = (mi.stato || {})[m[2]] || {}, nomi = mi.catNomi || {}, t;
    if (m[2] === 'settimanale') t = 'Completa 3 titoli in una settimana';
    else if (m[2] === 'tematica') t = 'Guarda ' + (nomi[m[3]] || m[3]);
    else if (m[2] === 'saga') t = 'Completa: ' + String(m[3]).replace(/^\d[A-Z]? · /, '');
    else t = 'Scoperta: ' + titleOf(m[3]);
    return { w: m[1], ic: { settimanale: '🟢', tematica: '🔵', saga: '🟣', segreta: '🔴' }[m[2]], t: t, xp: st.xp || 0 };
  }
  function renderArchive() {
    var mi = info(), bank = mi.bank || { totale: 0, ricompensate: [] }; arch.textContent = '';
    var head2 = el('div', 'cen-arch-h'); head2.innerHTML = '<span>Missioni concluse: <b>' + bank.ricompensate.length + '</b></span><span>XP da missioni: <b>' + (bank.totale || 0) + '</b></span>'; arch.appendChild(head2);
    if (!bank.ricompensate.length) { arch.appendChild(el('p', 'cen-note', 'Nessuna missione conclusa finora. Quando ne completi una, comparirà qui; i premi restano assegnati una sola volta.')); }
    var last = null, list = null;
    bank.ricompensate.slice().reverse().forEach(function (k) {
      var p = parseKey(k, mi);
      if (p.w !== last) { last = p.w; arch.appendChild(el('h4', 'cen-arch-w', p.w ? 'Settimana ' + p.w : 'Speciali')); list = el('ul', 'cen-arch-l'); arch.appendChild(list); }
      var li = el('li'); li.innerHTML = '<span aria-hidden="true">' + p.ic + '</span><span class="cen-arch-t">' + esc(p.t) + '</span><span class="cen-arch-x">' + (p.xp ? '+' + p.xp + ' XP' : '') + '</span>'; list.appendChild(li);
    });
    var ts = mi.titoliStagione || [];
    if (ts.length) { arch.appendChild(el('h4', 'cen-arch-w', 'Stagioni concluse')); var l2 = el('ul', 'cen-arch-l'); ts.forEach(function (t, i) { var li = el('li'); li.innerHTML = '<span aria-hidden="true">🌐</span><span class="cen-arch-t">Stagione ' + String(i + 1).padStart(2, '0') + ' · titolo «' + esc(t) + '»</span><span class="cen-arch-x">+500 XP</span>'; l2.appendChild(li); }); arch.appendChild(l2); }
    if (bank.ricompensate.length >= 200) arch.appendChild(el('p', 'cen-note', 'Lo storico conserva le ultime 200 missioni concluse.'));
  }

  /* ---------- OPERAZIONI (nodi esistenti, spostati) ---------- */
  var O = panels.operazioni;
  function grp(cls, title, help) { var g = el('section', 'cen-card cen-grp ' + cls); g.appendChild(el('h3', '', title)); if (help) g.appendChild(el('p', 'cen-help', help)); O.appendChild(g); return g; }
  var gP = grp('', 'Progresso di visione', 'Azioni di massa sui titoli visti. Aggiornano progresso, XP e distintivi con le regole di sempre.');
  var gB = grp('', 'Backup e ripristino', 'Esporta il tuo profilo in un file, importalo su un altro dispositivo o ripristina la copia di sicurezza automatica.');
  var gS = grp('', 'Sincronizzazione cloud', null);
  var gA = grp('', 'Aspetto', null);
  var gD = grp('cen-danger', 'Zona pericolosa', 'Queste azioni cancellano dati. Ognuna richiede conferme esplicite e non può essere annullata.');
  var mk = $('markAllBtn'); if (mk) { var w1 = el('div', 'cen-op'); w1.appendChild(mk); w1.appendChild(el('p', 'cen-help', 'Segna tutte le schede come viste (o, se sono già tutte viste, come non viste).')); gP.appendChild(w1); }
  var rb = $('resetBtn');
  if (rb) {
    var w2 = el('div', 'cen-op'); w2.appendChild(rb); w2.appendChild(el('p', 'cen-help', 'Azzera solo i titoli segnati come visti. Voti, note e preferiti restano.')); gD.appendChild(w2);
    ['resetConfirmOverlay', 'resetConfirmOverlay2'].forEach(function (i) { move($(i), w2); });
  }
  var ra = $('resetAllBtn');
  if (ra) {
    var w3 = el('div', 'cen-op'); w3.appendChild(ra); w3.appendChild(el('p', 'cen-help', 'Cancella titoli visti, voti, note, preferiti, XP, missioni, serie attiva e tessera (prima viene salvata una copia di sicurezza).')); gD.appendChild(w3);
    ['resetAllConfirmOverlay', 'resetAllConfirmOverlay2'].forEach(function (i) { move($(i), w3); });
  }
  var ex = $('exportBtn'), im = $('importBtn'), imf = $('importFile');
  if (ex) { var row = el('div', 'cen-op cen-op-row'); row.appendChild(ex); if (im) row.appendChild(im); if (imf) row.appendChild(imf); gB.appendChild(row); }
  move($('autoBackupHint'), gB);
  var sw = D.querySelector('.sync-wrap'); if (sw) { var st0 = sw.querySelector('.sync-title'); if (st0) st0.style.display = 'none'; gS.appendChild(sw); }
  var dmLabel = D.querySelector('label[for="darkModeToggle"]'); if (dmLabel) gA.appendChild(dmLabel);
  if (!gA.children[1]) gA.hidden = true;
  // «Segna tutti NON visti» cancella il progresso: conferma esplicita (la semantica del comando resta invariata)
  if (mk) mk.addEventListener('click', function (e) {
    if (mk.__ok) { mk.__ok = false; return; }
    if (!/NON VISTI/.test(mk.textContent)) return;
    e.stopImmediatePropagation(); e.preventDefault();
    var ov = el('div', 'reset-confirm-overlay'); ov.style.display = 'flex'; ov.innerHTML = '<div class="reset-confirm-box" role="alertdialog" aria-modal="true" aria-label="Conferma"><p><b>Segnare tutti i titoli come non visti?</b> Il progresso di visione verrà azzerato (voti, note e preferiti restano).</p><div class="reset-confirm-actions"><button type="button" class="reset-confirm-cancel">Annulla</button><button type="button" class="reset-confirm-ok">Sì, azzera i visti</button></div></div>';
    D.body.appendChild(ov);
    ov.querySelector('.reset-confirm-cancel').addEventListener('click', function () { ov.remove(); });
    ov.querySelector('.reset-confirm-ok').addEventListener('click', function () { ov.remove(); mk.__ok = true; mk.click(); });
  }, true);

  /* ---------- STRUMENTI ---------- */
  var S = panels.strumenti;
  var pk = $('dashPicker'); if (pk) { var c1 = el('section', 'cen-card cen-tool'); c1.appendChild(pk); S.appendChild(c1); }
  var dd = dash.querySelector('details.dash-details-all'); if (dd) { dd.classList.add('cen-stats'); S.appendChild(dd); }
  var cmp = $('modalita-confronto'); if (cmp) { cmp.classList.add('cen-cmp'); S.appendChild(cmp); }

  /* ---------- navigazione interna ---------- */
  var ST = { sec: 'panoramica', sub: 'attive', y: {} };
  function setSecUI(sec) {
    SECS.forEach(function (s) { var on = s[0] === sec, b = $('cenTab-' + s[0]); b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; b.classList.toggle('cen-on', on); panels[s[0]].hidden = !on; });
    H.setAttribute('data-cen-sec', sec);
  }
  function setSubUI(sub) {
    SUBS.forEach(function (s) { var on = s[0] === sub, b = $('cenSub-' + s[0]); b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; b.classList.toggle('cen-on', on); subp[s[0]].hidden = !on; });
  }
  function refreshAll() { try { refreshAgent(); refreshPreview(); renderStagione(); renderRtd(); renderArchive(); MROWS.forEach(function (m) { var d = $('cenDos-' + m[1]); if (d && !d.hidden) { d.textContent = ''; d.appendChild(buildDossier(m[1])); } }); } catch (e) { if (W.console) console.error('Centrale TVA:', e); } }
  function navTop() { return Math.max(0, Math.round(nav.getBoundingClientRect().top + (W.pageYOffset || 0)) - 8); }
  function openSec(sec, opts) {
    opts = opts || {};
    if (!panels[sec]) sec = 'panoramica';
    if (H.getAttribute('data-tva-view') !== 'centrale') { var t = $('appTabMissioni'); if (t && !opts.noTab) t.click(); else H.setAttribute('data-tva-view', 'centrale'); }
    ST.y[ST.sec] = W.pageYOffset || 0;
    var changed = sec !== ST.sec; ST.sec = sec; setSecUI(sec);
    if (sec === 'missioni') { if (opts.sub) ST.sub = opts.sub; setSubUI(ST.sub); }
    refreshAll();
    if (opts.noScroll) return;
    var y = (changed && ST.y[sec] != null && !opts.fresh) ? ST.y[sec] : navTop();
    W.scrollTo({ top: Math.min(y, Math.max(0, D.documentElement.scrollHeight - W.innerHeight)), behavior: 'instant' });
  }
  function openMission(key) {
    var sub = key === 'rtd' ? 'speciali' : key === 'stagione' ? 'stagioni' : 'attive';
    openSec('missioni', { sub: sub, fresh: true, noScroll: true }); refreshAll();
    var target = null;
    if (sub === 'attive') { toggleDossier(key, true); target = $('cenDos-' + key) && $({ settimanale: 'missioneSettimanale', tematica: 'missioneTematica', saga: 'missioneSaga', segreta: 'missioneSegreta' }[key]); }
    else target = sub === 'speciali' ? $('roadToDoomsday') : $('stagioneTvaCard');
    if (key === 'rtd') { var rd = $('rtdDetails'); if (rd) rd.open = true; }
    requestAnimationFrame(function () { if (target) { var y = Math.max(0, Math.round(target.getBoundingClientRect().top + (W.pageYOffset || 0)) - 70); W.scrollTo({ top: y, behavior: 'instant' }); target.classList.add('us-flash'); setTimeout(function () { target.classList.remove('us-flash'); }, 1600); } });
    return true;
  }
  W.tvaCentrale = {
    open: function (sec, sub) { openSec(sec, { sub: sub, fresh: true }); return true; },
    openMission: openMission,
    getState: function () { ST.y[ST.sec] = W.pageYOffset || 0; return { sec: ST.sec, sub: ST.sub, y: ST.y[ST.sec], open: MROWS.filter(function (m) { var d = $('cenDos-' + m[1]); return d && !d.hidden; }).map(function (m) { return m[1]; }) }; },
    setState: function (s) { if (!s) return; ST.y[s.sec] = s.y; ST.sub = s.sub || ST.sub; ST.sec = s.sec; setSecUI(s.sec); if (s.sec === 'missioni') setSubUI(ST.sub); if (s.open) MROWS.forEach(function (m) { toggleDossier(m[1], s.open.indexOf(m[1]) >= 0); }); refreshAll(); },
    sections: SECS.map(function (s) { return s[0]; })
  };
  // clic su schede e controlli
  nav.addEventListener('click', function (e) { var b = e.target.closest('.cen-tab'); if (b) openSec(b.getAttribute('data-sec'), { noTab: true }); });
  nav.addEventListener('keydown', function (e) { rove(e, '.cen-tab', function (b) { openSec(b.getAttribute('data-sec'), { noTab: true }); }); });
  subnav.addEventListener('click', function (e) { var b = e.target.closest('.cen-stab'); if (b) { ST.sub = b.getAttribute('data-sub'); setSubUI(ST.sub); if (ST.sub === 'archivio') renderArchive(); } });
  subnav.addEventListener('keydown', function (e) { rove(e, '.cen-stab', function (b) { ST.sub = b.getAttribute('data-sub'); setSubUI(ST.sub); }); });
  function rove(e, sel, act) {
    if (['ArrowRight', 'ArrowLeft', 'Home', 'End'].indexOf(e.key) < 0) return;
    var all = Array.prototype.slice.call(e.currentTarget.querySelectorAll(sel)), i = all.indexOf(D.activeElement); if (i < 0) return;
    e.preventDefault(); var n = e.key === 'Home' ? 0 : e.key === 'End' ? all.length - 1 : (i + (e.key === 'ArrowRight' ? 1 : -1) + all.length) % all.length;
    all[n].focus(); act(all[n]);
  }
  dash.addEventListener('click', function (e) {
    var g = e.target.closest('[data-go-sec]'); if (g) { var sec = g.getAttribute('data-go-sec'); openSec(sec, { sub: g.getAttribute('data-go-sub') || undefined, noTab: true, fresh: true }); return; }
    var a = e.target.closest('[data-act]'); if (a) { var t = $(a.getAttribute('data-act') === 'tessera' ? 'appTabTessera' : 'appTabAtlante'); if (t) t.click(); return; }
    var m = e.target.closest('[data-mission]'); if (m && !m.classList.contains('cen-dbtn')) { openMission(m.getAttribute('data-mission')); return; }
    var w = e.target.closest('[data-cen-item]'); if (w) { var id = w.getAttribute('data-cen-item'); if (W.tvaGo) W.tvaGo('item', id); }
  });
  // aprire un titolo dalla Centrale: la cronologia interna ricorda da dove si arriva (Indietro riporta alla stessa sezione)
  D.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('#dashboard #nextWatchCard, #dashboard #lastWatchedCard, #dashboard #dashPickerCard, #dashboard #dashPickerWatchBtn, #dashboard .rtd-link') : null;
    if (t && W.tvaPushNav) W.tvaPushNav('Centrale TVA');
  }, true);
  // ancore #cen-<sezione>[-sub] e #dashboard
  function fromHash() {
    var h = (W.location.hash || '').replace(/^#/, ''), m = /^cen-(panoramica|missioni|operazioni|strumenti)(?:-(attive|stagioni|speciali|archivio))?$/.exec(h);
    if (m) { openSec(m[1], { sub: m[2], fresh: true }); return true; } return false;
  }
  D.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href^="#cen-"], a[href="#dashboard"], a[href="#database"]') : null; if (!a) return;
    var h = a.getAttribute('href');
    if (h === '#database') { e.preventDefault(); var t = $('appTabAtlante'); if (t) t.click(); return; }
    e.preventDefault(); if (h === '#dashboard') openSec('panoramica', { fresh: true }); else { var m = /^#cen-(\w+)(?:-(\w+))?$/.exec(h); if (m) openSec(m[1], { sub: m[2], fresh: true }); }
  }, true);
  W.addEventListener('hashchange', fromHash);

  /* ---------- aggiornamento dei dati (sola lettura sulle fonti esistenti) ---------- */
  var raf = 0; function later() { if (!raf) raf = requestAnimationFrame(function () { raf = 0; try { refreshAgent(); refreshPreview(); } catch (e) {} }); }
  try {
    var mo = new MutationObserver(later), tc = $('tesseraCard'); if (tc) mo.observe(tc, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['style', 'class'] });
    var mo2 = new MutationObserver(later); [$('dashMissioni'), $('stagioneTvaCard')].forEach(function (n) { if (n) mo2.observe(n, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ['style', 'class'] }); });
  } catch (e) {}
  var nmi = $('tesseraNameInput'); if (nmi) nmi.addEventListener('input', later);
  D.addEventListener('tva:missioni2', function () { refreshAll(); });
  D.addEventListener('change', function (e) { if (e.target && e.target.classList && e.target.classList.contains('watch-check')) setTimeout(refreshAll, 60); });

  /* ---------- pulizia Timeline ---------- */
  (function () {
    var gt = $('gtimeline'), ind = $('indice');
    if (gt && ind && !gt.querySelector('.gtl-det')) {
      var tbl = gt.querySelector('.tl-table'), sb = gt.querySelector('.toc-sub'), det = el('details', 'gtl-det');
      det.appendChild(el('summary', '', 'Timeline Riassuntiva · 9 checkpoint'));
      if (sb) det.appendChild(sb); if (tbl) det.appendChild(tbl);
      gt.textContent = ''; gt.appendChild(det); ind.after(gt);
    }
    var as = D.querySelector('.advanced-filters > summary'); if (as) as.innerHTML = '⚙️ Filtri avanzati e modalità spoiler';
  })();

  setSecUI('panoramica'); setSubUI('attive'); refreshAll();
  if (!fromHash()) { /* resta su Panoramica */ }
  H.setAttribute('data-cen', 'ready');
})();
/* B2-JS-END */
