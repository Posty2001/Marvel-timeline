/* TC-JS-BEGIN: Blocco 3.2 - Tessera TVA: identita', editor Personalizza, foto locale, esportazione PNG, Carriera e Collezione.
   Nessun XP/badge/ricompensa nuovi. Le preferenze cosmetiche vivono SOLO in tvaRewards (equip); qui si salvano solo avatar e 3 distintivi in evidenza. */
(function () {
  'use strict';
  var W = window, D = document;
  if (W.tvaTessera) return;
  var A = W.tvaCardArt, RW = W.tvaRewards;
  if (!A || !RW) return;

  var LOOK_KEY = 'marvel-ultimate-timeline-tessera-look', PHOTO_KEY = 'marvel-ultimate-timeline-tessera-photo', NAME_KEY = 'marvel-ultimate-timeline-user-name';
  var SLOTS = ['titolo', 'cornice', 'tema', 'effetto'];
  var TABS = [['avatar', 'Avatar'], ['titolo', 'Titoli'], ['cornice', 'Cornici'], ['tema', 'Temi'], ['effetto', 'Effetti']];
  var CAT_NAME = { titolo: 'Titoli agente', cornice: 'Cornici', tema: 'Temi', effetto: 'Effetti' };
  var BY = {}; RW.catalog.forEach(function (r) { BY[r.id] = r; });
  var AV_IDS = A.avatars.map(function (a) { return a.id; });
  var BADGE_RE = /^[a-z][a-z-]{2,30}$/;

  function el(tag, cls, txt) { var e = D.createElement(tag); if (cls) e.className = cls; if (txt !== undefined) e.textContent = txt; return e; }
  function $(id) { return D.getElementById(id); }
  function isObj(v) { return v !== null && typeof v === 'object' && !Array.isArray(v); }
  function decode(s) { if (!/&/.test(s)) return s; var t = D.createElement('textarea'); t.innerHTML = s; return t.value; }

  /* ---------- dati: look (avatar + 3 distintivi) e foto locale ---------- */
  function sanitizeLook(o) {
    var out = { v: 1 };
    if (!isObj(o)) return out;
    if (typeof o.a === 'string' && (o.a === 'photo' || AV_IDS.indexOf(o.a) !== -1)) out.a = o.a;
    if (Array.isArray(o.b)) { var seen = {}; out.b = o.b.filter(function (x) { if (typeof x !== 'string' || !BADGE_RE.test(x) || seen[x]) return false; seen[x] = 1; return true; }).slice(0, 3); }
    if (typeof o.ts === 'number' && isFinite(o.ts) && o.ts > 0) out.ts = o.ts;
    return out;
  }
  function lookLoad() { try { return sanitizeLook(JSON.parse(localStorage.getItem(LOOK_KEY) || 'null')); } catch (e) { return { v: 1 }; } }
  function lookSave(o) { try { localStorage.setItem(LOOK_KEY, JSON.stringify(sanitizeLook(o))); return true; } catch (e) { return false; } }
  function lookMerge(localRaw, remote) {   // vince la scelta piu' recente (come per le preferenze cosmetiche)
    var a = sanitizeLook((function () { try { return JSON.parse(localRaw || 'null'); } catch (e) { return null; } })()), b = sanitizeLook(remote);
    return JSON.stringify((b.ts || 0) > (a.ts || 0) ? b : a);
  }
  var PHOTO_RE = /^data:image\/jpeg;base64,[A-Za-z0-9+\/=]+$/;
  function photoGet() { try { var p = localStorage.getItem(PHOTO_KEY); return p && p.length < 600000 && PHOTO_RE.test(p) ? p : null; } catch (e) { return null; } }

  /* ---------- lettura dello stato reale (sola lettura) ---------- */
  function badgesAll() {
    var out = [];
    Array.prototype.forEach.call(D.querySelectorAll('.badge-chip'), function (c) {
      var id = (c.id || '').replace(/^badge-/, ''); if (!id) return;
      out.push({ id: id, name: decode(c.getAttribute('data-name') || id), got: c.classList.contains('badge-unlocked') });
    });
    return out;
  }
  function earned() { return badgesAll().filter(function (b) { return b.got; }); }
  function nameNow() {
    var i = $('tesseraNameInput'), v = i ? i.value.trim() : '';
    if (!v) { try { v = (localStorage.getItem(NAME_KEY) || '').trim(); } catch (e) {} }
    return v.slice(0, 20);
  }
  function xpNow() {
    var xi = W.marvelXpInfo, sub = $('tesseraXpSub'), m = sub && sub.textContent.match(/(\d+)\s*\/\s*(\d+)/), lv = $('tesseraLivello'), xt = $('tesseraXpTotale');
    return {
      level: xi && typeof xi.livello === 'number' ? xi.livello : (lv ? parseInt(lv.textContent, 10) || 1 : 1),
      xp: xi && typeof xi.xp === 'number' ? xi.xp : (xt ? parseInt(xt.textContent, 10) || 0 : 0),
      cur: m ? +m[1] : 0, need: m ? +m[2] : 100
    };
  }
  function variantId() { var e = $('tesseraId'); return e ? e.textContent.trim() : 'VAR-000000'; }

  /* "vista" = tutto cio' che la Tessera mostra; la bozza dell'editor e' una copia di questa struttura */
  function current() {
    var eq = RW.equipped(), lk = lookLoad(), got = earned(), ids = got.map(function (b) { return b.id; }), ph = photoGet();
    var kind = lk.a === 'photo' && ph ? 'photo' : 'preset', aid = lk.a && lk.a !== 'photo' ? lk.a : 'agente';
    var b = Array.isArray(lk.b) ? lk.b.filter(function (x) { return ids.indexOf(x) !== -1; }) : ids.slice(0, 3);
    return { name: nameNow(), avatar: { kind: kind, id: aid }, badges: b.slice(0, 3), titolo: eq.titolo, cornice: eq.cornice, tema: eq.tema, effetto: eq.effetto, photo: ph };
  }
  function toModel(v) {
    var x = xpNow(), all = badgesAll(), nm = {}; all.forEach(function (b) { nm[b.id] = b.name; });
    var bs = v.badges.filter(function (id) { return nm[id]; }).map(function (id) { return { id: id, name: nm[id] }; });
    return {
      name: v.name || 'Variante', titleId: v.titolo, id: variantId(), title: BY[v.titolo] ? BY[v.titolo].nome : 'Nuova Variante', level: x.level, xp: x.xp, xpCur: x.cur, xpNeed: x.need, badges: bs,
      avatar: v.avatar.kind === 'photo' && v.photo ? { kind: 'photo', url: v.photo } : { kind: 'preset', id: v.avatar.id },
      frame: v.cornice, theme: v.tema, fx: v.effetto,
      frameName: BY[v.cornice] ? BY[v.cornice].nome : '', themeName: BY[v.tema] ? BY[v.tema].nome : '', fxName: v.effetto && BY[v.effetto] ? BY[v.effetto].nome : ''
    };
  }

  /* ---------- carta in-app ---------- */
  var heroKey = '';
  function renderHero(force) {
    var box = $('tcHero'); if (!box) return;
    var w = box.clientWidth; if (!w) return;
    var layout = w >= 520 ? 'wide' : 'compact', svg;
    try { svg = A.build(toModel(current()), layout, { uid: 'hero' }); } catch (e) { if (W.console) console.error('Tessera TVA:', e); return; }
    if (!force && svg === heroKey) return;
    heroKey = svg; box.innerHTML = svg; box.setAttribute('data-layout', layout);
  }
  var rq = 0;
  function scheduleHero() { if (rq) return; rq = W.requestAnimationFrame ? W.requestAnimationFrame(function () { rq = 0; renderHero(); }) : setTimeout(function () { rq = 0; renderHero(); }, 16); }

  /* ---------- struttura della sezione ---------- */
  function buildSection() {
    var wrap = D.querySelector('#tesseraOverlayEl .tessera-wrap'), card = $('tesseraCard'), oldBtn = $('tesseraCondividiBtn');
    if (!wrap || !card || $('tcHero')) return false;
    var sub = D.querySelector('#tesseraOverlayEl .mg-sub'); if (sub) sub.textContent = 'La tua identità ufficiale negli Archivi Temporali.';
    var hero = el('div', 'tc-hero'); hero.id = 'tcHero'; hero.setAttribute('aria-live', 'off');
    var acts = el('div', 'tc-actions'); acts.id = 'tcActions';
    var bp = el('button', 'tc-btn tc-btn-main', 'PERSONALIZZA'); bp.type = 'button'; bp.id = 'tcPersonalizzaBtn';
    var bs = oldBtn ? oldBtn.cloneNode(false) : el('button'); bs.type = 'button'; bs.id = 'tesseraCondividiBtn'; bs.className = 'tc-btn tc-btn-alt'; bs.textContent = 'CONDIVIDI';
    if (oldBtn && oldBtn.parentNode) oldBtn.parentNode.removeChild(oldBtn);
    acts.appendChild(bp); acts.appendChild(bs);
    var care = el('details', 'tc-sec'); care.id = 'tcCareer'; var cs = el('summary', 'tc-sum', 'Carriera TVA'); care.appendChild(cs);
    var cb = el('div', 'tc-sec-body'); care.appendChild(cb);
    var miss = el('div', 'tc-miss'); miss.id = 'tcMissions'; cb.appendChild(miss);
    var bdg = el('div', 'tc-badges'); bdg.id = 'tcBadges'; cb.appendChild(bdg);
    wrap.insertBefore(hero, card); wrap.insertBefore(acts, card); wrap.insertBefore(care, card);
    cb.insertBefore(card, miss);   // la scheda esistente (livello, XP, statistiche) viene riutilizzata, non duplicata
    card.classList.add('tc-career-card');
    var coll = el('details', 'tc-sec'); coll.id = 'tcCollection'; coll.appendChild(el('summary', 'tc-sum', '')); var colb = el('div', 'tc-sec-body'); colb.id = 'tcCollBody'; coll.appendChild(colb);
    care.parentNode.insertBefore(coll, care.nextSibling);
    bp.addEventListener('click', function () { openEditor('avatar'); });
    bs.addEventListener('click', openShare);
    care.addEventListener('toggle', function () { if (care.open) { renderMissions(); renderBadges(); } });
    coll.addEventListener('toggle', renderCollection);
    return true;
  }
  function renderMissions() {
    var box = $('tcMissions'); if (!box) return; box.textContent = '';
    var st = W.marvelMissioniInfo && W.marvelMissioniInfo.stato;
    box.appendChild(el('h4', 'tc-h', 'Missioni di questa settimana'));
    if (!st) { box.appendChild(el('p', 'tc-note', 'Missioni e Stagioni TVA si consultano nella Centrale TVA: i progressi compariranno qui appena li avrai aperti.')); return; }
    var ul = el('ul', 'tc-ml');
    [['settimanale', 'Settimanale'], ['tematica', 'Tematica'], ['saga', 'Saga'], ['segreta', 'Segreta']].forEach(function (k) {
      var m = st[k[0]]; if (!m) return;
      var li = el('li', m.done ? 'tc-done' : ''); li.appendChild(el('span', 'tc-ml-n', k[1])); li.appendChild(el('span', 'tc-ml-v', m.done ? 'Completata' : (m.cur + ' / ' + m.tot)));
      ul.appendChild(li);
    });
    box.appendChild(ul);
  }
  function renderBadges() {
    var box = $('tcBadges'); if (!box) return; box.textContent = '';
    var all = badgesAll(), n = all.filter(function (b) { return b.got; }).length;
    box.appendChild(el('h4', 'tc-h', 'Distintivi · ' + n + '/' + all.length));
    var ul = el('ul', 'tc-bl');
    all.forEach(function (b) {
      var li = el('li', b.got ? 'tc-got' : 'tc-no'); li.setAttribute('aria-label', b.name + (b.got ? ' (ottenuto)' : ' (non ottenuto)'));
      li.innerHTML = '<svg viewBox="-24 -24 48 48" aria-hidden="true" focusable="false"><circle r="21" fill="rgba(0,0,0,.3)" stroke="currentColor" stroke-width="2"/><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + A.glyph(b.id) + '</g></svg>';
      li.appendChild(el('span', '', b.name)); ul.appendChild(li);
    });
    box.appendChild(ul);
  }

  /* ---------- collezione definitiva (sola lettura: equipaggiare si fa nell'editor) ---------- */
  function reqText(r) { if (r.cond.k === 'always') return 'Sempre disponibile'; var p = RW.progress(r.id); return r.desc + (p && p.tot > 1 ? ' (' + p.cur + '/' + p.tot + ')' : ''); }
  function renderCollection() {
    var coll = $('tcCollection'), body = $('tcCollBody'); if (!coll || !body) return;
    var st = RW.state(), eq = RW.equipped(), n = RW.unlocked().length;
    coll.firstChild.textContent = 'Collezione · ' + n + '/' + RW.catalog.length;
    if (!coll.open) return;
    body.textContent = '';
    body.appendChild(el('p', 'tc-note', 'Ricompense cosmetiche (48). I 14 distintivi sono separati: li trovi in «Carriera TVA». Tocca una voce per aprirla nell’editor.'));
    SLOTS.forEach(function (c) {
      var list = RW.catalog.filter(function (r) { return r.cat === c; }), got = list.filter(function (r) { return RW.isUnlocked(r.id, st); }).length;
      var sec = el('section', 'tc-cg'); sec.appendChild(el('h4', 'tc-h', CAT_NAME[c] + ' · ' + got + '/' + list.length));
      var ul = el('ul', 'tc-cl');
      list.forEach(function (r) {
        var open = RW.isUnlocked(r.id, st), on = eq[c] === r.id, li = el('li'), b = el('button', 'tc-crow tc-r-' + r.rar + (open ? '' : ' tc-lockrow') + (on ? ' tc-on' : ''));
        b.type = 'button'; b.setAttribute('data-id', r.id);
        b.appendChild(el('span', 'tc-cn', r.nome));
        b.appendChild(el('span', 'tc-cr', RW.rarities[r.rar] + (on ? ' · In uso' : '')));
        b.appendChild(el('span', 'tc-cd', open ? (r.cond.k === 'always' ? 'Sempre disponibile' : 'Sbloccata il ' + st.u[r.id]) : 'Bloccata · ' + reqText(r)));
        b.addEventListener('click', function () { openEditor(c, r.id); });
        li.appendChild(b); ul.appendChild(li);
      });
      sec.appendChild(ul); body.appendChild(sec);
    });
  }

  /* =====================  EDITOR PERSONALIZZA  ===================== */
  var ed = null;
  function overlayHost() { return $('tesseraOverlayEl') || D.body; }
  function copyView(v) { return { name: v.name, avatar: { kind: v.avatar.kind, id: v.avatar.id }, badges: v.badges.slice(), titolo: v.titolo, cornice: v.cornice, tema: v.tema, effetto: v.effetto, photo: v.photo }; }
  function trapKeys(root, onEsc) {
    root.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.stopPropagation(); onEsc(); return; }
      if (e.key !== 'Tab') return;
      var f = Array.prototype.filter.call(root.querySelectorAll('button:not([disabled]),input:not([disabled]),select,[tabindex="0"]'), function (x) { return x.offsetParent !== null; });
      if (!f.length) return; var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && D.activeElement === first) { e.preventDefault(); last.focus(); } else if (!e.shiftKey && D.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
  function openEditor(tab, focusId) {
    if (ed) return;
    var base = current(), root = el('div', 'tc-ed'); root.id = 'tcEditor'; root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true'); root.setAttribute('aria-label', 'Personalizza la Tessera');
    ed = { root: root, base: base, draft: copyView(base), tab: tab || 'avatar', opener: D.activeElement, photoChanged: false, note: '' };
    if (focusId && BY[focusId] && RW.isUnlocked(focusId)) ed.draft[BY[focusId].cat] = focusId;
    root.innerHTML = '<div class="tc-ed-top"><button type="button" class="tc-btn tc-btn-ghost" id="tcEdCancel">Annulla</button><h3>Personalizza<small class="tc-ed-state" id="tcEdState" role="status" aria-live="polite"></small></h3><button type="button" class="tc-btn tc-btn-main tc-btn-idle" id="tcEdSave">Salva</button></div>' +
      '<div class="tc-ed-main"><div class="tc-ed-prev" id="tcEdPrev"></div><div class="tc-ed-side"><div class="tc-ed-tabs" role="tablist" aria-label="Categorie" id="tcEdTabs"></div><p class="tc-ed-note" id="tcEdNote" role="status" aria-live="polite"></p><div class="tc-ed-body" id="tcEdBody" role="tabpanel"></div></div></div>';
    overlayHost().appendChild(root);
    var tabs = $('tcEdTabs');
    TABS.forEach(function (t) {
      var b = el('button', 'tc-tab', t[1]); b.type = 'button'; b.id = 'tcTab-' + t[0]; b.setAttribute('role', 'tab'); b.setAttribute('data-tab', t[0]);
      b.addEventListener('click', function () { ed.tab = t[0]; ed.note = ''; renderEd(); });
      tabs.appendChild(b);
    });
    $('tcEdCancel').addEventListener('click', closeEditor); $('tcEdSave').addEventListener('click', saveEditor);
    trapKeys(root, function () { if (ed && ed.ph) closePhoto(); else closeEditor(); });
    root.addEventListener('focusin', function (e) { if (e.target && e.target.tagName === 'INPUT' && (e.target.type === 'text')) root.classList.add('tc-kb'); });
    root.addEventListener('focusout', function (e) { if (e.target && e.target.tagName === 'INPUT') root.classList.remove('tc-kb'); });
    renderEd(); var t0 = $('tcTab-' + ed.tab); if (t0) t0.focus();
  }
  function closeEditor() {
    if (!ed) return; var r = ed.root, op = ed.opener; if (ed.ph) closePhoto(); ed = null;
    if (r.parentNode) r.parentNode.removeChild(r);
    try { if (op && op.focus && D.contains(op)) op.focus(); } catch (e) {}
    scheduleHero();
  }
  function saveEditor() {
    if (!ed) return; var d = ed.draft, b = ed.base, changed = SLOTS.filter(function (s) { return d[s] !== b[s]; });
    for (var i = 0; i < changed.length; i++) { var s = changed[i]; if (d[s] === null ? s !== 'effetto' : !RW.isUnlocked(d[s])) { setNote('Impossibile salvare: «' + CAT_NAME[s] + '» non è sbloccato.'); return; } }
    if (ed.photoChanged) {
      try { if (d.photo) localStorage.setItem(PHOTO_KEY, d.photo); else localStorage.removeItem(PHOTO_KEY); }
      catch (e) { setNote('Spazio insufficiente sul dispositivo: la foto non è stata salvata. Nessuna modifica applicata.'); return; }
    }
    for (var j = 0; j < changed.length; j++) { var r = RW.equip(changed[j], d[changed[j]]); if (!r.ok) { setNote('Salvataggio non riuscito (' + r.reason + ').'); return; } }
    if (d.name !== b.name) setName(d.name);
    var av = d.avatar.kind === 'photo' && d.photo ? 'photo' : d.avatar.id;
    if (!lookSave({ v: 1, a: av, b: d.badges.slice(0, 3), ts: Date.now() })) { setNote('Salvataggio delle preferenze non riuscito (spazio del dispositivo).'); return; }
    try { D.dispatchEvent(new CustomEvent('tva:look', { detail: { saved: true } })); } catch (e2) {}
    closeEditor(); renderHero(true); renderCollection();
  }
  function setName(v) {
    var i = $('tesseraNameInput'); v = (v || '').trim().slice(0, 20);
    if (i) { i.value = v; i.dispatchEvent(new Event('input', { bubbles: true })); } else { try { localStorage.setItem(NAME_KEY, v); } catch (e) {} }
  }
  function setNote(t) { if (ed) { ed.note = t; var n = $('tcEdNote'); if (n) n.textContent = t; } }

  var prevKey = '';
  function renderPrev() {
    var box = $('tcEdPrev'); if (!box || !ed) return; var w = box.clientWidth || 320, layout = w >= 520 ? 'wide' : 'compact';
    var svg = A.build(toModel(ed.draft), layout, { uid: 'edp' }); if (svg === prevKey && box.firstChild) return; prevKey = svg; box.innerHTML = svg;
  }
  function dirtyList() {   /* differenze tra bozza e stato salvato (la bozza non e' mai scritta in memoria prima di «Salva») */
    var d = ed.draft, b = ed.base, n = [];
    SLOTS.forEach(function (s) { if (d[s] !== b[s]) n.push(s); });
    if (d.name !== b.name) n.push('name');
    if (d.avatar.kind !== b.avatar.kind || d.avatar.id !== b.avatar.id || ed.photoChanged) n.push('avatar');
    if (JSON.stringify(d.badges) !== JSON.stringify(b.badges)) n.push('badges');
    return n;
  }
  function updateDirty() {
    if (!ed) return; var n = dirtyList().length, btn = $('tcEdSave'), st = $('tcEdState'); if (!btn) return;
    btn.textContent = n ? 'Salva · ' + n : 'Salva'; btn.classList.toggle('tc-btn-idle', !n); btn.classList.toggle('tc-btn-dirty', !!n);
    btn.setAttribute('aria-label', n ? 'Salva ' + n + (n === 1 ? ' modifica' : ' modifiche') : 'Salva (nessuna modifica da salvare)');
    if (st) { st.textContent = n ? '● Non salvato' : '✓ Salvato'; st.classList.toggle('tc-ed-state-dirty', !!n); }
  }
  var thTok = 0;
  function renderEd() {
    if (!ed) return;
    Array.prototype.forEach.call($('tcEdTabs').children, function (b) { var on = b.getAttribute('data-tab') === ed.tab; b.setAttribute('aria-selected', on ? 'true' : 'false'); b.classList.toggle('tc-tab-on', on); b.tabIndex = on ? 0 : -1; });
    $('tcEdNote').textContent = ed.note || '';
    var body = $('tcEdBody'), keep = body.scrollTop, same = body.getAttribute('data-tab') === ed.tab;
    body.textContent = ''; body.setAttribute('data-tab', ed.tab); body.setAttribute('aria-labelledby', 'tcTab-' + ed.tab);
    if (ed.tab === 'avatar') panelAvatar(body); else panelRewards(body, ed.tab);
    if (same) body.scrollTop = keep; else body.scrollTop = 0;
    renderPrev(); updateDirty();
  }
  function tile(cls, selected, locked, label, thumbHtml, sub, onClick) {
    var b = el('button', 'tc-tile ' + cls + (selected ? ' tc-sel' : '') + (locked ? ' tc-lock' : '')); b.type = 'button';
    b.setAttribute('aria-pressed', selected ? 'true' : 'false'); if (locked) b.setAttribute('aria-disabled', 'true');
    if (thumbHtml) { var t = el('span', 'tc-tile-th'); t.innerHTML = thumbHtml; b.appendChild(t); }
    b.appendChild(el('span', 'tc-tile-n', label)); if (sub) b.appendChild(el('span', 'tc-tile-s', sub));
    b.addEventListener('click', onClick); return b;
  }
  var LOCKSVG = '<svg class="tc-lk" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><rect x="3" y="7" width="10" height="7" rx="1.5" fill="currentColor"/><path d="M5 7V5a3 3 0 0 1 6 0v2" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>';
  function panelRewards(body, cat) {
    var st = RW.state(), list = RW.catalog.filter(function (r) { return r.cat === cat; }), grid = el('div', 'tc-grid tc-grid-' + cat);
    body.appendChild(el('p', 'tc-hint', 'Le voci bloccate mostrano il requisito: tocca per leggerlo. Si equipaggia soltanto ciò che è già sbloccato.'));
    if (cat === 'effetto') {
      var noneT = tile('tc-none', ed.draft.effetto === null, false, 'Nessuno', '<svg viewBox="0 0 250 158" class="tc-thumb" aria-hidden="true"><rect width="250" height="158" fill="#0d0809"/><circle cx="125" cy="79" r="26" fill="#2a1a1f" stroke="#D2B184"/></svg>', 'Nessun effetto', function () { ed.draft.effetto = null; ed.note = ''; renderEd(); }); (function () { var row = el('span', 'tc-tile-st'); if (ed.base.effetto === null) row.appendChild(el('span', 'tc-chip tc-chip-use', 'In uso')); if (ed.draft.effetto === null && ed.base.effetto !== null) row.appendChild(el('span', 'tc-chip tc-chip-sel', '✓ Selezionata · da salvare')); if (row.firstChild) noneT.appendChild(row); })(); grid.appendChild(noneT);
    }
    var deferred = cat === 'tema', queue = [], tmodel = deferred ? toModel(ed.draft) : null;
    var stateTags = function (t, isBase, isSel) {   /* stati nel testo, mai sopra la miniatura: IN USO (salvato) / SELEZIONATA (bozza, da salvare) */
      var row = el('span', 'tc-tile-st');
      if (isBase) row.appendChild(el('span', 'tc-chip tc-chip-use', 'In uso'));
      if (isSel && !isBase) row.appendChild(el('span', 'tc-chip tc-chip-sel', '✓ Selezionata · da salvare'));
      if (row.firstChild) t.appendChild(row);
    };
    list.forEach(function (r, i) {
      var open = RW.isUnlocked(r.id, st), sel = ed.draft[cat] === r.id, isBase = ed.base[cat] === r.id;
      var th = cat === 'titolo' ? '' : deferred ? '<svg viewBox="0 0 280 200" class="tc-thumb" aria-hidden="true"><rect width="280" height="200" fill="' + A.themeBg(r.id) + '"/></svg>' : A.thumb(cat, r.id, 'tt' + i, { theme: ed.draft.tema, frame: ed.draft.cornice });
      var sub = open ? RW.rarities[r.rar] : '';
      var t = tile('tc-r-' + r.rar, sel, !open, r.nome, th, sub, function () {
        if (!open) { ed.note = 'Bloccata: ' + r.nome + ' — ' + reqText(r); renderEd(); return; }
        ed.draft[cat] = r.id; ed.note = ''; renderEd();
      });
      var thEl = t.querySelector('.tc-tile-th');
      if (thEl && !deferred) thEl.appendChild(el('span', 'tc-chip tc-chip-' + r.rar, RW.rarities[r.rar]));   /* temi: anteprima reale senza badge sopra (la rarita' e' nel testo) */
      if (deferred && thEl) queue.push({ host: thEl, id: r.id, n: i });
      if (open) stateTags(t, isBase, sel);
      if (!open) { var s = el('span', 'tc-tile-s tc-req'); s.innerHTML = LOCKSVG; s.appendChild(D.createTextNode(' Bloccata')); t.appendChild(s); t.appendChild(el('span', 'tc-tile-q', reqText(r))); t.setAttribute('aria-label', r.nome + ', bloccata. ' + reqText(r)); }
      else t.setAttribute('aria-label', r.nome + ', ' + RW.rarities[r.rar] + (isBase ? ', in uso' : '') + (sel && !isBase ? ', selezionata, da salvare' : sel ? ', selezionata' : ''));
      grid.appendChild(t);
    });
    if (deferred) {   /* anteprime reali dei temi: composizione compatta della Tessera, create una per frame per non bloccare l'apertura della scheda */
      var tok = ++thTok, step = function () {
        if (!ed || tok !== thTok || !queue.length) return; var q = queue.shift();
        try { var tmp = D.createElement('span'); tmp.innerHTML = A.thumb('tema', q.id, 'tt' + q.n, { theme: ed.draft.tema, frame: ed.draft.cornice, model: tmodel }); var sv = tmp.firstChild, old = q.host.querySelector('svg'); if (sv && old) q.host.replaceChild(sv, old); } catch (e) {}
        (W.requestAnimationFrame || W.setTimeout)(step);
      };
      (W.requestAnimationFrame || W.setTimeout)(step);
    }
    body.appendChild(grid);
  }
  function panelAvatar(body) {
    var d = ed.draft;
    var f = el('label', 'tc-lbl', 'Nome agente'); f.setAttribute('for', 'tcEdName'); body.appendChild(f);
    var inp = el('input', 'tc-input'); inp.type = 'text'; inp.id = 'tcEdName'; inp.maxLength = 20; inp.value = d.name; inp.autocomplete = 'off'; inp.setAttribute('autocapitalize', 'words'); inp.placeholder = 'Il tuo nome…';
    inp.addEventListener('input', function () { d.name = inp.value.slice(0, 20); renderPrev(); updateDirty(); });
    body.appendChild(inp);
    body.appendChild(el('h4', 'tc-h', 'Avatar'));
    var grid = el('div', 'tc-grid tc-grid-av');
    A.avatars.forEach(function (a, i) {
      var sel = d.avatar.kind === 'preset' && d.avatar.id === a.id;
      grid.appendChild(tile('tc-av', sel, false, a.nome, A.avatarThumb({ avatar: { kind: 'preset', id: a.id } }, 'av' + i), '', function () { d.avatar = { kind: 'preset', id: a.id }; ed.note = ''; renderEd(); }));
    });
    if (d.photo) grid.appendChild(tile('tc-av', d.avatar.kind === 'photo', false, 'La tua foto', A.avatarThumb({ avatar: { kind: 'photo', url: d.photo } }, 'avp'), '', function () { d.avatar = { kind: 'photo', id: d.avatar.id }; ed.note = ''; renderEd(); }));
    body.appendChild(grid);
    body.appendChild(el('h4', 'tc-h', 'Foto personale'));
    var row = el('div', 'tc-row');
    var file = el('input'); file.type = 'file'; file.accept = 'image/*'; file.id = 'tcFile'; file.className = 'tc-file'; file.tabIndex = -1; file.setAttribute('aria-label', 'Scegli una foto');
    var up = el('button', 'tc-btn tc-btn-alt', d.photo ? 'Cambia foto' : 'Carica foto'); up.type = 'button'; up.id = 'tcUpBtn'; up.addEventListener('click', function () { file.value = ''; file.click(); });
    file.addEventListener('change', function () { if (file.files && file.files[0]) startPhoto(file.files[0], null); });
    row.appendChild(up); row.appendChild(file);
    if (d.photo) {
      var edb = el('button', 'tc-btn tc-btn-alt', 'Modifica'); edb.type = 'button'; edb.id = 'tcPhEditBtn'; edb.addEventListener('click', function () { startPhoto(null, d.photo); }); row.appendChild(edb);
      var rm = el('button', 'tc-btn tc-btn-ghost', 'Rimuovi'); rm.type = 'button'; rm.id = 'tcPhRemoveBtn';
      rm.addEventListener('click', function () { d.photo = null; ed.photoChanged = true; if (d.avatar.kind === 'photo') d.avatar = { kind: 'preset', id: 'agente' }; ed.note = 'Foto rimossa (si applica al salvataggio).'; renderEd(); });
      row.appendChild(rm);
    }
    body.appendChild(row);
    body.appendChild(el('p', 'tc-hint', 'La foto resta solo su questo dispositivo: non viene caricata online né sincronizzata, e non è inclusa nei backup.'));
    var got = earned(); body.appendChild(el('h4', 'tc-h', 'Distintivi in evidenza · ' + d.badges.length + '/3'));
    if (!got.length) body.appendChild(el('p', 'tc-hint', 'Non hai ancora distintivi: appariranno qui appena ne otterrai uno.'));
    else {
      var bl = el('div', 'tc-bpick');
      got.forEach(function (b) {
        var on = d.badges.indexOf(b.id) !== -1, btn = el('button', 'tc-bchip' + (on ? ' tc-sel' : '')); btn.type = 'button'; btn.setAttribute('aria-pressed', on ? 'true' : 'false'); btn.setAttribute('data-badge', b.id);
        btn.innerHTML = '<svg viewBox="-24 -24 48 48" aria-hidden="true" focusable="false"><g fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" transform="scale(1.5)">' + A.glyph(b.id) + '</g></svg>';
        btn.appendChild(el('span', '', b.name));
        btn.addEventListener('click', function () {
          var i = d.badges.indexOf(b.id);
          if (i !== -1) d.badges.splice(i, 1);
          else if (d.badges.length >= 3) { ed.note = 'Puoi esporne al massimo tre: deseleziona un distintivo per sceglierne un altro.'; renderEd(); return; }
          else d.badges.push(b.id);
          ed.note = ''; renderEd();
        });
        bl.appendChild(btn);
      });
      body.appendChild(bl);
    }
  }

  /* =====================  FOTO: caricamento, ritaglio, regolazioni  ===================== */
  var MAX_BYTES = 30 * 1024 * 1024, MAX_PIXELS = 120e6, WORK = 1024, OUT = 384;
  function decodeImage(file, dataUrl) {
    return new Promise(function (res, rej) {
      if (file) {
        if (file.type && (!/^image\//i.test(file.type) || /svg/i.test(file.type))) return rej(new Error('Formato non supportato: scegli un’immagine JPEG, PNG o WebP.'));
        if (file.size > MAX_BYTES) return rej(new Error('Immagine troppo grande (oltre 30 MB). Scegline una più piccola.'));
      }
      var url = dataUrl || URL.createObjectURL(file), img = new Image(), done = false;
      var fin = function (fn, v) { if (done) return; done = true; if (!dataUrl) { try { URL.revokeObjectURL(url); } catch (e) {} } fn(v); };
      var to = setTimeout(function () { fin(rej, new Error('Lettura dell’immagine troppo lenta o non riuscita.')); }, 20000);
      img.onload = function () { clearTimeout(to); fin(res, img); };
      img.onerror = function () { clearTimeout(to); fin(rej, new Error('Formato non supportato o immagine illeggibile (i file HEIC non sono sempre leggibili: prova JPEG o PNG).')); };
      img.src = url;   // i browser moderni applicano l'orientamento EXIF (image-orientation: from-image)
    });
  }
  function toWork(img) {
    var w = img.naturalWidth, h = img.naturalHeight; if (!w || !h) throw new Error('Immagine vuota.');
    if (w * h > MAX_PIXELS) throw new Error('Risoluzione troppo alta per questo dispositivo (oltre 120 megapixel).');
    var k = Math.min(1, WORK / Math.max(w, h)), c = D.createElement('canvas'); c.width = Math.max(1, Math.round(w * k)); c.height = Math.max(1, Math.round(h * k));
    var x = c.getContext('2d'); if (!x) throw new Error('Memoria insufficiente per elaborare l’immagine.');
    x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high'; x.fillStyle = '#000'; x.fillRect(0, 0, c.width, c.height); x.drawImage(img, 0, 0, c.width, c.height);
    return c;
  }
  function startPhoto(file, dataUrl) {
    if (!ed) return; setNote('Lettura dell’immagine…');
    decodeImage(file, dataUrl).then(function (img) { var c = toWork(img); img.onload = img.onerror = null; img.src = ''; setNote(''); openPhoto(c); })
      .catch(function (e) { setNote(e && e.message ? e.message : 'Immagine non utilizzabile.'); });
  }
  function openPhoto(src) {
    var S = Math.max(200, Math.min(320, (W.innerWidth || 360) - 56, Math.round((W.innerHeight || 640) * 0.42))), dpr = Math.min(2, W.devicePixelRatio || 1);
    var p = { src: src, S: S, zoom: 1, cx: src.width / 2, cy: src.height / 2, br: 0, ct: 0, root: el('div', 'tc-ph') };
    ed.ph = p; p.root.id = 'tcPhoto'; p.root.setAttribute('role', 'dialog'); p.root.setAttribute('aria-modal', 'true'); p.root.setAttribute('aria-label', 'Ritaglia e regola la foto');
    p.root.innerHTML = '<div class="tc-ph-box"><h3>La tua foto</h3><div class="tc-ph-view" id="tcPhView" style="width:' + S + 'px;height:' + S + 'px"><canvas id="tcPhCv" tabindex="0" aria-label="Anteprima: trascina per spostare l’inquadratura, frecce da tastiera per muoverla" width="' + Math.round(S * dpr) + '" height="' + Math.round(S * dpr) + '" style="width:' + S + 'px;height:' + S + 'px"></canvas><svg class="tc-ph-guide" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="49" fill="none" stroke="#D2B184" stroke-width=".7" stroke-dasharray="3 2"/><rect x="10" y="1" width="80" height="98" fill="none" stroke="#efe4c9" stroke-opacity=".7" stroke-width=".5" stroke-dasharray="2 2"/></svg></div>' +
      '<p class="tc-hint">Il cerchio è il ritaglio della carta verticale, il rettangolo quello della carta orizzontale.</p>' +
      '<label class="tc-sl">Zoom<input type="range" id="tcPhZoom" min="1" max="4" step="0.01" value="1"></label><label class="tc-sl">Luminosità<input type="range" id="tcPhBr" min="-50" max="50" step="1" value="0"></label><label class="tc-sl">Contrasto<input type="range" id="tcPhCt" min="-50" max="50" step="1" value="0"></label>' +
      '<div class="tc-row"><button type="button" class="tc-btn tc-btn-ghost" id="tcPhReset">Ripristina</button><button type="button" class="tc-btn tc-btn-ghost" id="tcPhCancel">Annulla</button><button type="button" class="tc-btn tc-btn-main" id="tcPhOk">Conferma</button></div><p class="tc-ed-note" id="tcPhNote" role="status"></p></div>';
    ed.root.appendChild(p.root);
    var cv = $('tcPhCv'), ctx = cv.getContext('2d'), drag = null;
    function scl() { return Math.max(S / src.width, S / src.height) * p.zoom; }
    function clamp() { var sc = scl(), hw = S / 2 / sc; p.cx = Math.min(src.width - hw, Math.max(hw, p.cx)); p.cy = Math.min(src.height - hw, Math.max(hw, p.cy)); }
    function draw() {
      clamp(); var sc = scl(), k = cv.width / S; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.fillStyle = '#000'; ctx.fillRect(0, 0, cv.width, cv.height);
      ctx.drawImage(src, (S / 2 - p.cx * sc) * k, (S / 2 - p.cy * sc) * k, src.width * sc * k, src.height * sc * k);
      cv.style.filter = 'brightness(' + (1 + p.br / 100) + ') contrast(' + (1 + p.ct / 100) + ')';   // anteprima: filtro CSS economico; il risultato finale usa una tabella di conversione
    }
    cv.addEventListener('pointerdown', function (e) { drag = { x: e.clientX, y: e.clientY, cx: p.cx, cy: p.cy }; try { cv.setPointerCapture(e.pointerId); } catch (x) {} e.preventDefault(); });
    cv.addEventListener('pointermove', function (e) { if (!drag) return; var sc = scl(); p.cx = drag.cx - (e.clientX - drag.x) / sc; p.cy = drag.cy - (e.clientY - drag.y) / sc; draw(); });
    var up = function () { drag = null; }; cv.addEventListener('pointerup', up); cv.addEventListener('pointercancel', up);
    cv.addEventListener('keydown', function (e) { var st = 16 / scl(), m = { ArrowLeft: [-st, 0], ArrowRight: [st, 0], ArrowUp: [0, -st], ArrowDown: [0, st] }[e.key]; if (m) { p.cx += m[0]; p.cy += m[1]; draw(); e.preventDefault(); } });
    $('tcPhZoom').addEventListener('input', function (e) { p.zoom = +e.target.value; draw(); });
    $('tcPhBr').addEventListener('input', function (e) { p.br = +e.target.value; draw(); });
    $('tcPhCt').addEventListener('input', function (e) { p.ct = +e.target.value; draw(); });
    $('tcPhReset').addEventListener('click', function () { p.zoom = 1; p.br = 0; p.ct = 0; p.cx = src.width / 2; p.cy = src.height / 2; $('tcPhZoom').value = 1; $('tcPhBr').value = 0; $('tcPhCt').value = 0; draw(); });
    $('tcPhCancel').addEventListener('click', closePhoto);
    $('tcPhOk').addEventListener('click', function () {
      try { var url = renderPhoto(p); if (url.length > 400000) throw new Error('Foto troppo pesante.'); ed.draft.photo = url; ed.draft.avatar = { kind: 'photo', id: ed.draft.avatar.id }; ed.photoChanged = true; closePhoto(); ed.note = 'Foto pronta: premi Salva per confermarla.'; renderEd(); }
      catch (e) { var n = $('tcPhNote'); if (n) n.textContent = e && e.message ? e.message : 'Elaborazione non riuscita.'; }
    });
    p.draw = draw; draw(); $('tcPhCv').focus();
  }
  function renderPhoto(p) {   // risultato finale: ritaglio quadrato OUT x OUT, luminosita'/contrasto con tabella (nessun ctx.filter: assente su Safari)
    var c = D.createElement('canvas'); c.width = c.height = OUT; var x = c.getContext('2d'); if (!x) throw new Error('Memoria insufficiente.');
    var sc = Math.max(p.S / p.src.width, p.S / p.src.height) * p.zoom, k = OUT / p.S;
    x.fillStyle = '#000'; x.fillRect(0, 0, OUT, OUT); x.imageSmoothingQuality = 'high';
    x.drawImage(p.src, (p.S / 2 - p.cx * sc) * k, (p.S / 2 - p.cy * sc) * k, p.src.width * sc * k, p.src.height * sc * k);
    if (p.br || p.ct) {
      var b = 1 + p.br / 100, ct = 1 + p.ct / 100, lut = new Uint8ClampedArray(256), i;
      for (i = 0; i < 256; i++) lut[i] = ((i * b) - 128) * ct + 128;
      var id = x.getImageData(0, 0, OUT, OUT), a = id.data; for (i = 0; i < a.length; i += 4) { a[i] = lut[a[i]]; a[i + 1] = lut[a[i + 1]]; a[i + 2] = lut[a[i + 2]]; }
      x.putImageData(id, 0, 0);
    }
    return c.toDataURL('image/jpeg', 0.82);
  }
  function closePhoto() { if (!ed || !ed.ph) return; var r = ed.ph.root; ed.ph = null; if (r.parentNode) r.parentNode.removeChild(r); var b = $('tcUpBtn'); if (b) b.focus(); }

  /* =====================  CONDIVISIONE: PNG della carta verticale  ===================== */
  /* 3.2.4: 1080x1800 (3x la carta a 360 px) + riduzione del rumore di dithering dei gradienti (quantizzazione a 6 bit con arrotondamento, errore max 3/255): ~1.7 MB contro ~4.5-5 MB a 1440x2400, nessuna differenza visibile. */
  var EXPORT_W = 1080, EXPORT_H = 1800;
  function quantize(x, w, h) { try { var id = x.getImageData(0, 0, w, h), d = id.data, i, v; for (i = 0; i < d.length; i += 4) { v = d[i]; d[i] = v > 252 ? 255 : (v + 2) & 252; v = d[i + 1]; d[i + 1] = v > 252 ? 255 : (v + 2) & 252; v = d[i + 2]; d[i + 2] = v > 252 ? 255 : (v + 2) & 252; } x.putImageData(id, 0, 0); } catch (e) { /* canvas non leggibile: si esporta senza quantizzazione */ } }
  function exportPng(view) {
    return new Promise(function (res, rej) {
      var svg;
      try { svg = A.build(toModel(view), 'vertical', { uid: 'ex' }); } catch (e) { return rej(new Error('Composizione della carta non riuscita.')); }
      svg = svg.replace(/(<svg[^>]*?) width="720" height="1200"/, '$1 width="' + EXPORT_W + '" height="' + EXPORT_H + '"');   // dimensione nativa 2x: Safari rasterizza gli SVG alla dimensione intrinseca
      var img = new Image(), fired = false, to = setTimeout(function () { if (!fired) { fired = true; rej(new Error('Tempo scaduto durante la creazione dell’immagine.')); } }, 15000);
      img.onload = function () {
        if (fired) return; fired = true; clearTimeout(to);
        try {
          var c = D.createElement('canvas'); c.width = EXPORT_W; c.height = EXPORT_H; var x = c.getContext('2d'); if (!x) throw new Error('canvas');
          x.drawImage(img, 0, 0, EXPORT_W, EXPORT_H); quantize(x, EXPORT_W, EXPORT_H);
          var done = function (b) { if (b && b.size > 1000) res(b); else rej(new Error('Immagine vuota: esportazione non riuscita su questo browser.')); };
          if (c.toBlob) c.toBlob(done, 'image/png'); else { var u = c.toDataURL('image/png'), bin = atob(u.split(',')[1]), arr = new Uint8Array(bin.length), i; for (i = 0; i < bin.length; i++) arr[i] = bin.charCodeAt(i); done(new Blob([arr], { type: 'image/png' })); }
        } catch (e) { rej(new Error('Esportazione non riuscita (memoria o canvas non disponibili).')); }
      };
      img.onerror = function () { if (fired) return; fired = true; clearTimeout(to); rej(new Error('Il browser non ha potuto rendere la carta come immagine.')); };
      img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
    });
  }
  var sh = null;
  function openShare() {
    if (sh) return;
    var root = el('div', 'tc-ed tc-sh'); root.id = 'tcShare'; root.setAttribute('role', 'dialog'); root.setAttribute('aria-modal', 'true'); root.setAttribute('aria-label', 'Condividi la Tessera');
    root.innerHTML = '<div class="tc-ed-top"><button type="button" class="tc-btn tc-btn-ghost" id="tcShClose">Chiudi</button><h3>Condividi</h3><span class="tc-spacer"></span></div><div class="tc-sh-main"><div class="tc-sh-img" id="tcShImg" aria-live="polite"><p class="tc-hint">Creazione dell’immagine…</p></div><p class="tc-ed-note" id="tcShNote" role="status"></p><div class="tc-row tc-sh-btns"><button type="button" class="tc-btn tc-btn-main" id="tcShShare" disabled>Condividi</button><button type="button" class="tc-btn tc-btn-alt" id="tcShSave" disabled>Salva PNG</button></div><p class="tc-hint" id="tcShHint">Se il pulsante non funziona, tieni premuta l’immagine e scegli «Salva».</p></div>';
    overlayHost().appendChild(root);
    sh = { root: root, opener: D.activeElement, blob: null, url: null };
    var close = function () { if (!sh) return; var r = sh.root, u = sh.url, op = sh.opener; sh = null; if (u) { try { URL.revokeObjectURL(u); } catch (e) {} } if (r.parentNode) r.parentNode.removeChild(r); try { if (op && op.focus && D.contains(op)) op.focus(); } catch (e) {} };
    sh.close = close; $('tcShClose').addEventListener('click', close); trapKeys(root, close); $('tcShClose').focus();
    var view = current(), fname = 'tessera-tva-' + variantId().replace(/[^A-Za-z0-9-]/g, '') + '.png';
    var shareBtn = $('tcShShare'), saveBtn = $('tcShSave'), canNative = !!(navigator.share && navigator.canShare);
    exportPng(view).then(function (blob) {
      if (!sh) return; sh.blob = blob; sh.url = URL.createObjectURL(blob);
      var box = $('tcShImg'); box.textContent = ''; var im = el('img'); im.src = sh.url; im.alt = 'Anteprima PNG della Tessera TVA verticale'; im.className = 'tc-sh-png'; box.appendChild(im);
      saveBtn.disabled = false;
      var file = null; try { file = new File([blob], fname, { type: 'image/png' }); } catch (e) {}
      var nativeOk = false; try { nativeOk = !!(canNative && file && navigator.canShare({ files: [file] })); } catch (e) {}
      if (nativeOk) shareBtn.disabled = false; else { shareBtn.hidden = true; $('tcShNote').textContent = 'La condivisione diretta non è disponibile su questo dispositivo: usa «Salva PNG».'; }
      shareBtn.addEventListener('click', function () { navigator.share({ files: [file], title: 'La mia Tessera TVA' }).catch(function (e) { if (e && e.name !== 'AbortError') $('tcShNote').textContent = 'Condivisione non riuscita: usa «Salva PNG».'; }); });
      saveBtn.addEventListener('click', function () { var a = el('a'); a.href = sh.url; a.download = fname; a.rel = 'noopener'; D.body.appendChild(a); a.click(); D.body.removeChild(a); });
    }).catch(function (e) {
      if (!sh) return; $('tcShImg').textContent = ''; $('tcShImg').appendChild(el('p', 'tc-hint', e && e.message ? e.message : 'Esportazione non riuscita.'));
      $('tcShNote').textContent = 'Puoi comunque fare uno screenshot della Tessera.'; shareBtn.hidden = true; saveBtn.hidden = true;
    });
  }

  /* ---------- avvio ---------- */
  function refreshAll() { scheduleHero(); var c = $('tcCareer'); if (c && c.open) { renderMissions(); renderBadges(); } renderCollection(); }
  function boot() {
    if (!buildSection()) return;
    var hero = $('tcHero');
    if (W.ResizeObserver) new ResizeObserver(function () { scheduleHero(); if (ed) renderPrev(); }).observe(hero);
    W.addEventListener('resize', function () { scheduleHero(); });
    var x = $('tesseraXpTotale'); if (x && W.MutationObserver) new MutationObserver(scheduleHero).observe(x, { childList: true, characterData: true, subtree: true });
    var s = $('tesseraXpSub'); if (s && W.MutationObserver) new MutationObserver(scheduleHero).observe(s, { childList: true, characterData: true, subtree: true });
    var ni = $('tesseraNameInput'); if (ni) ni.addEventListener('input', scheduleHero);
    ['tva:rewards', 'tva:look', 'tva:missioni2'].forEach(function (ev) { D.addEventListener(ev, refreshAll); });
    var tg = $('tesseraToggle');
    if (tg) tg.addEventListener('change', function () { if (!tg.checked) { if (ed) closeEditor(); if (sh) sh.close(); } else { setTimeout(function () { renderHero(true); renderCollection(); }, 30); } });
    D.addEventListener('tva:avatarart', function () { renderHero(true); if (ed) renderEd(); });
    if (A.avatarArt) A.avatarArt.load();
    refreshAll(); setTimeout(refreshAll, 600); W.addEventListener('load', function () { setTimeout(refreshAll, 500); });
  }
  W.tvaTessera = {
    version: 1, keys: { look: LOOK_KEY, photo: PHOTO_KEY }, current: current, model: toModel, buildSvg: function (layout, view) { return A.build(toModel(view || current()), layout, { uid: 't' + layout }); },
    open: openEditor, close: function () { closeEditor(); }, share: openShare, exportPng: function (view) { return exportPng(view || current()); },
    lookLoad: lookLoad, lookMerge: lookMerge, sanitizeLook: sanitizeLook, photoGet: photoGet, render: function () { renderHero(true); }, renderCollection: renderCollection,
    _state: function () { return { editor: ed, share: sh }; }
  };
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', boot); else boot();
})();
/* TC-JS-END */
