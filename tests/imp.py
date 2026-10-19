import json, re, os, copy, sys, time
from playwright.sync_api import sync_playwright

NEW = 'file:///home/claude/work/index.html'
BASE = 'file:///home/claude/work/index.baseline.html'
D = '/tmp/claude-0/t/imp'; os.makedirs(D, exist_ok=True)
src = open('/home/claude/work/index.html', encoding='utf-8').read()
OBJ = dict(re.findall(r"(\w+): '(marvel-ultimate-timeline-[a-z0-9-]+)'", re.search(r'var PROFILE_OBJ_KEYS = \{(.*?)\};', src, re.S).group(1)))
STR = dict(re.findall(r"(\w+): '(marvel-ultimate-timeline-[a-z0-9-]+)'", re.search(r'var PROFILE_STR_KEYS = \{(.*?)\};', src, re.S).group(1)))
ALLK = {**OBJ, **STR}
AUTOBK = 'marvel-ultimate-timeline-auto-backup'
assert len(OBJ) == 16 and len(STR) == 10

RTD = ['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
INIT = """
(function(){
  var oST = window.setTimeout;
  window.__toasts = []; window.__marker = 'vivo'; window.__blockAutosave = __BLOCK__;
  window.setTimeout = function(fn, ms){
    if (ms === 5000 && window.__blockAutosave) return 0;
    if (ms === 1200 && window.__holdReload) { window.__pendingReload = fn; return 0; }
    return oST.apply(window, arguments);
  };
  var oSet = Storage.prototype.setItem;
  Storage.prototype.setItem = function(k, v){
    if (window.__failKey && k === window.__failKey && window.__failMode === 'throw') { throw new DOMException('quota', 'QuotaExceededError'); }
    if (window.__failKey && k === window.__failKey && window.__failMode === 'silent') { return; }
    return oSet.call(this, k, v);
  };
  new MutationObserver(function(ms){ ms.forEach(function(m){ m.addedNodes.forEach(function(n){ if (n.classList && n.classList.contains('lv-toast-msg')) window.__toasts.push(n.textContent); }); }); }).observe(document, {childList:true, subtree:true});
})();
"""
res = []
def ok(name, cond, extra=''):
    res.append((name, bool(cond))); print('PASS' if cond else 'FAIL', name, extra)

def empty(v):
    if v is None or v == '' : return True
    try:
        j = json.loads(v) if isinstance(v, str) else v
    except Exception:
        return False
    return j in ({}, [], None, '')

def norm(v):
    if empty(v): return None
    try: return json.loads(v)
    except Exception: return v

def snap(pg, keys=None):
    return pg.evaluate("(ks)=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k)}return o}", keys)

def prof(snapshot):
    return {k: norm(snapshot.get(v)) for k, v in ALLK.items()}

def base_profile(fav='Thor'):
    return {
      'watched': {i: True for i in RTD + ['001','002','125']},
      'watchedAnim': {'ironman94': True},
      'favorites': {'001': True, '041': True},
      'notes': {'001': 'nota di prova', '041': 'altra nota'},
      'ratings': {'001': 4, '041': 5},
      'lastWatched': {'id': '125', 'ts': 1760000000000},
      'filters': {'activeFilters': {'verde': True, 'blu': True, 'giallo': False, 'rosso': True}, 'activeStudios': {'mcu': True, 'fox': True, 'sony': True, 'legacy': True, 'animazione': True}, 'activeTypes': {'film': True, 'serie': True, 'speciale': True}, 'favOnly': False, 'weekendOnly': False},
      'friends': {},
      'groups': [{'name': 'Team', 'members': [{'name': 'Tu', 'tesseraId': 'VAR-123456', 'watchedIds': ['001','002'], 'watchedAnimIds': ['ironman94']}], 'createdAt': 1760000000000}],
      'watchDays': {'2026-10-10': True, '2026-10-11': True},
      'missioneSettimana': {'settimana': '2026-W41', 'titoli': ['001']},
      'missioneSnapshot': {'settimana': '2026-W41', 'visti': ['001']},
      'missioneXpBank': {'totale': 480, 'ricompensate': ['road-to-doomsday-v1', '2026-W41-tematica']},
      'titoliStagione': ['Custode'],
      'roadToDoomsday': {'completata': True, 'data': '2026-10-10'},
      'badgesEarned': ['primo-passo', 'essenziale', 'cinefilo'],
      'tesseraId': 'VAR-654321', 'onboardingFatto': '', 'favChar': fav, 'custodeSeen': '1', 'darkMode': '1',
      'preferredMode': 'uscita', 'spoilerMode': 'spoilerLight', 'spoilerCutoff': '100', 'userName': 'Franco', 'stagioneFesteggiata': '1',
    }

def seed(pg, p, extra=None):
    d = {}
    for k, v in p.items():
        if k in OBJ:
            if k == 'friends' or empty(v): continue
            d[OBJ[k]] = json.dumps(v)
        else:
            if v != '': d[STR[k]] = v
    if extra: d.update(extra)
    pg.evaluate("(d)=>{localStorage.clear();sessionStorage.clear();for(const k in d)localStorage.setItem(k,d[k])}", d)

def file_of(p, name, version='2.0', schema=1, app='marvel-ultimate-timeline'):
    f = {'app': app, 'version': version, 'schemaVersion': schema, 'exportedAt': '2026-10-16T00:00:00.000Z'}
    f.update(p); path = os.path.join(D, name); open(path, 'w', encoding='utf-8').write(json.dumps(f, indent=2)); return path

def raw_file(text, name):
    path = os.path.join(D, name); open(path, 'w', encoding='utf-8').write(text); return path

with sync_playwright() as p:
    b = p.chromium.launch()
    def newpage(url=NEW, seedp=None, extra=None, hold=True, block=True, dialogs=None):
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, accept_downloads=True)
        ctx.add_init_script(INIT.replace('__BLOCK__', 'true' if block else 'false'))
        pg = ctx.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        dl = [] if dialogs is None else dialogs
        pg.on('dialog', lambda d: (dl.append(d.message), d.accept()))
        pg.goto(url)
        if seedp is not None or extra:
            seed(pg, seedp or {}, extra); pg.evaluate("()=>{window.__blockAutosave=%s;window.__holdReload=%s}" % ('true' if block else 'false', 'true' if hold else 'false'))
            pg.reload(); pg.wait_for_timeout(300)
        pg.evaluate("()=>{window.__blockAutosave=%s;window.__holdReload=%s}" % ('true' if block else 'false', 'true' if hold else 'false'))
        pg.wait_for_timeout(1200)
        return ctx, pg, errs, dl
    def do_export(pg):
        with pg.expect_download() as d:
            pg.evaluate("()=>document.getElementById('exportBtn').click()")
        path = os.path.join(D, 'export_%d.json' % int(time.time() * 1000)); d.value.save_as(path); return path
    def do_import(pg, path, wait=500):
        pg.evaluate("()=>{window.__toasts=[];window.__marker='vivo';window.__pendingReload=null}")
        pg.set_input_files('#importFile', path); pg.wait_for_timeout(wait)
        return pg.evaluate("()=>({toasts:window.__toasts.slice(),marker:window.__marker,pend:!!window.__pendingReload})")
    def xp(pg):
        return pg.evaluate("()=>({xp:(document.getElementById('tesseraXpTotale')||{}).textContent, badges:document.querySelectorAll('.badge-chip.unlocked, .badge-chip.sbloccato').length})")

    P1 = base_profile()
    # ---------- 1. export attuale -> reimport senza perdita ----------
    ctxA, pgA, eA, _ = newpage(seedp=P1)
    fav_ok = pgA.evaluate("()=>[...document.querySelectorAll('#tesseraFavSelect option')].map(o=>o.value).filter(Boolean)[0]")
    pgA.close(); ctxA.close()
    P1 = base_profile(fav_ok)
    ctxA, pgA, eA, _ = newpage(seedp=P1)
    pgA.wait_for_timeout(800)
    SA = prof(snap(pgA)); fexp = do_export(pgA); XA = xp(pgA)
    exported = json.load(open(fexp, encoding='utf-8'))
    ok('1a export: app/version/schemaVersion e 26 campi', exported['app'] == 'marvel-ultimate-timeline' and exported['version'] == '2.0' and exported['schemaVersion'] == 1 and all(k in exported for k in ALLK))
    ctxB, pgB, eB, dlB = newpage(seedp=base_profile(fav_ok) | {'watched': {'040': True}, 'userName': 'Altro', 'notes': {'040': 'x'}, 'badgesEarned': ['maratoneta'], 'roadToDoomsday': {'completata': True}, 'missioneXpBank': {'totale': 9999, 'ricompensate': ['zzz']}, 'favorites': {'040': True}, 'ratings': {'040': 1}})
    r = do_import(pgB, fexp)
    SB = prof(snap(pgB))
    diff = {k: (SA[k], SB[k]) for k in ALLK if SA[k] != SB[k]}
    ok('1b reimport: stato identico all\'export (nessuna perdita, nessuna traccia del profilo precedente)', not diff, str(list(diff.items())[:3]))
    ok('1c conferma mostrata con numeri e nessun errore', len(dlB) == 1 and 'SOSTITUIR' in dlB[0].upper() and any('importato correttamente' in t for t in r['toasts']), str(r['toasts']))
    pgB.evaluate("()=>window.__pendingReload && window.__pendingReload()"); pgB.wait_for_timeout(2500)
    XB = xp(pgB)
    ok('1d dopo il reload XP e badge uguali alla sorgente', XA == XB, '%s vs %s' % (XA, XB))
    rtd_state = pgB.evaluate("()=>[localStorage.getItem('%s'), localStorage.getItem('%s')]" % (OBJ['roadToDoomsday'], OBJ['missioneXpBank']))
    ok('1e premio Road e banca XP del file conservati (nessun doppio premio)', json.loads(rtd_state[0])['completata'] is True and json.loads(rtd_state[1])['totale'] == 480 and json.loads(rtd_state[1])['ricompensate'].count('road-to-doomsday-v1') == 1, str(rtd_state))
    badges_after = json.loads(pgB.evaluate("()=>localStorage.getItem('%s')" % OBJ['badgesEarned']))
    ok('1f badge storici del file conservati', {'primo-passo', 'essenziale', 'cinefilo'} <= set(badges_after) and 'maratoneta' not in badges_after, str(badges_after))
    ok('1g nessun errore di pagina', not eA and not eB, str(eA + eB))
    ctxB.close()

    # ---------- 2. profilo valido vuoto sostituisce profilo pieno ----------
    ctxE, pgE, _, _ = newpage()  # profilo vuoto
    fempty = do_export(pgE); ctxE.close()
    ctxF, pgF, eF, dlF = newpage(seedp=base_profile(fav_ok))
    before = snap(pgF); r = do_import(pgF, fempty)
    after = snap(pgF); pa = prof(after)
    resid = {k: v for k, v in pa.items() if v is not None and k != 'tesseraId'}
    ok('2a profilo vuoto: nome, note, preferiti, voti, spunte e premi tutti azzerati', not resid, str(resid))
    bk = json.loads(after.get(AUTOBK, 'null') or 'null')
    ok('2b copia di sicurezza del profilo pieno creata nella stessa operazione', bk and len(bk['watched']) == len(P1['watched']) and bk['userName'] == 'Franco' and bk['badgesEarned'] == ['primo-passo', 'essenziale', 'cinefilo'])
    ok('2c toast di successo', any('importato correttamente' in t for t in r['toasts']))
    # 2d copia non sovrascritta dopo il reload (autosave sospeso una volta) e recuperabile dal pulsante
    pgF.evaluate("()=>{window.__blockAutosave=false;window.__holdReload=false}")
    hold = pgF.evaluate("()=>sessionStorage.getItem('marvel-ultimate-timeline-backup-hold')")
    ok('2d flag di sospensione autosave impostato', hold == '1')
    pgF.evaluate("()=>window.__pendingReload && window.__pendingReload()"); pgF.wait_for_timeout(1500)
    pgF.wait_for_timeout(6500)
    bk2 = json.loads(pgF.evaluate("()=>localStorage.getItem('%s')" % AUTOBK) or 'null')
    ok('2e dopo reload + 6,5 s la copia precedente non e\' stata sovrascritta', bk2 and len(bk2['watched']) == len(P1['watched']) and bk2['userName'] == 'Franco')
    ctxF.close()

    # ---------- 3. vecchio export (baseline) con migrazione ----------
    old_p = base_profile(fav_ok)
    base_green = None
    ctxO, pgO, eO, _ = newpage(url=BASE)
    base_green = pgO.evaluate("()=>[...document.querySelectorAll('.card-wrap[data-item]')].filter(w=>w.getAttribute('data-tag')==='verde').map(w=>w.getAttribute('data-item'))")
    seed(pgO, {k: v for k, v in old_p.items() if k not in ('roadToDoomsday', 'badgesEarned')} | {'watched': {i: True for i in base_green}})
    pgO.reload(); pgO.wait_for_timeout(1500)
    fold = do_export(pgO); ctxO.close()
    oldj = json.load(open(fold, encoding='utf-8'))
    ok('3a export del baseline: 24 campi, senza roadToDoomsday/badgesEarned', 'badgesEarned' not in oldj and 'roadToDoomsday' not in oldj and all(k in oldj for k in ALLK if k not in ('roadToDoomsday', 'badgesEarned')), str(sorted(oldj.keys())[:4]))
    ctxN, pgN, eN, dlN = newpage(seedp=base_profile(fav_ok))  # profilo locale con premi e badge che NON devono sopravvivere
    r = do_import(pgN, fold)
    sN = snap(pgN)
    ok('3b migrazione: badge storici e premio Road del profilo locale rimossi (non ereditati)', sN.get(OBJ['badgesEarned']) is None and sN.get(OBJ['roadToDoomsday']) is None, str((sN.get(OBJ['badgesEarned']), sN.get(OBJ['roadToDoomsday']))))
    ok('3c la conferma segnala i campi reimpostati', dlN and 'roadToDoomsday' in dlN[0] and 'badgesEarned' in dlN[0], str(dlN))
    ok('3d dati del file applicati (visti = verdi del baseline, nome, banca XP)', len(json.loads(sN[OBJ['watched']])) == len(base_green) and sN[STR['userName']] == 'Franco' and json.loads(sN[OBJ['missioneXpBank']])['totale'] == 480)
    pgN.evaluate("()=>window.__pendingReload && window.__pendingReload()"); pgN.wait_for_timeout(2500)
    storico = json.loads(pgN.evaluate("()=>localStorage.getItem('%s')" % OBJ['badgesEarned']) or 'null')
    rtd = pgN.evaluate("()=>localStorage.getItem('%s')" % OBJ['roadToDoomsday'])
    ok('3e dopo il reload lo storico e\' rigenerato solo dai dati importati (essenziale si, cinefilo/cronista no) e Road non assegnato', storico is not None and 'essenziale' in storico and 'cinefilo' not in storico and rtd is None, str((storico, rtd)))
    ctxN.close()

    # ---------- 4. file estranei / incompleti / tipi e valori errati ----------
    ctxI, pgI, eI, dlI = newpage(seedp=base_profile(fav_ok))
    good = {k: v for k, v in base_profile(fav_ok).items()}
    def mod(**kw):
        d = copy.deepcopy(good); d.update(kw); return d
    cases = {
      'json vuoto {}': raw_file('{}', 'c_empty.json'),
      'array []': raw_file('[]', 'c_arr.json'),
      'null': raw_file('null', 'c_null.json'),
      'stringa': raw_file('"ciao"', 'c_str.json'),
      'testo non json': raw_file('questo non e json', 'c_txt.json'),
      'json troncato': raw_file('{"app":"marvel-ultimate-timeline","version":"2.0"', 'c_trunc.json'),
      'file estraneo (altra app)': file_of(good, 'c_other.json', app='altra-app'),
      'senza app': raw_file(json.dumps({'version': '2.0', 'schemaVersion': 1, 'watched': {}}), 'c_noapp.json'),
      'versione 3.0': file_of(good, 'c_v3.json', version='3.0'),
      'schema 2': file_of(good, 'c_s2.json', schema=2),
      'schema stringa': file_of(good, 'c_sstr.json', schema='1'),
      'solo intestazione': raw_file(json.dumps({'app': 'marvel-ultimate-timeline', 'version': '2.0', 'schemaVersion': 1}), 'c_head.json'),
      'senza watched': file_of({k: v for k, v in good.items() if k != 'watched'}, 'c_nowatched.json'),
      'watched come array': file_of(mod(watched=['001']), 'c_w_arr.json'),
      'id titolo inesistente 999': file_of(mod(watched={'999': True}), 'c_w_999.json'),
      'id titolo senza zeri': file_of(mod(watched={'1': True}), 'c_w_1.json'),
      'valore spunta non booleano': file_of(mod(watched={'001': 'si'}), 'c_w_val.json'),
      '__proto__ come chiave': raw_file(json.dumps(good).replace('"watched": {', '"watched": {"__proto__": true, ', 1), 'c_proto.json'),
      'voto 7': file_of(mod(ratings={'001': 7}), 'c_r7.json'),
      'voto 3.5': file_of(mod(ratings={'001': 3.5}), 'c_r35.json'),
      'nota non testo': file_of(mod(notes={'001': 5}), 'c_n5.json'),
      'preferito inesistente': file_of(mod(favorites={'abc': True}), 'c_fav.json'),
      'serie animata inesistente': file_of(mod(watchedAnim={'nonesiste': True}), 'c_anim.json'),
      'lastWatched id errato': file_of(mod(lastWatched={'id': '777', 'ts': 1}), 'c_lw.json'),
      'filtri tipo errato': file_of(mod(filters={'activeFilters': {'verde': 'si'}}), 'c_fil.json'),
      'gruppo senza membri': file_of(mod(groups=[{'name': 'x'}]), 'c_grp.json'),
      'membro con tesseraId errato': file_of(mod(groups=[{'name': 'x', 'members': [{'name': 'a', 'tesseraId': 'XX', 'watchedIds': [], 'watchedAnimIds': []}]}]), 'c_grp2.json'),
      'data giorno non valida': file_of(mod(watchDays={'2026-13-45': True}), 'c_wd.json'),
      'settimana errata': file_of(mod(missioneSettimana={'settimana': 'oggi', 'titoli': []}), 'c_ms.json'),
      'banca XP negativa': file_of(mod(missioneXpBank={'totale': -5, 'ricompensate': []}), 'c_xpn.json'),
      'banca XP totale testo': file_of(mod(missioneXpBank={'totale': '480', 'ricompensate': []}), 'c_xps.json'),
      'banca XP ricompensate non elenco': file_of(mod(missioneXpBank={'totale': 5, 'ricompensate': 'x'}), 'c_xpr.json'),
      'titoliStagione non elenco': file_of(mod(titoliStagione={'a': 1}), 'c_ts.json'),
      'Road completata testo': file_of(mod(roadToDoomsday={'completata': 'si'}), 'c_rtd.json'),
      'badge sconosciuto': file_of(mod(badgesEarned=['hack']), 'c_bd.json'),
      'badge oggetto': file_of(mod(badgesEarned={'primo-passo': True}), 'c_bd2.json'),
      'nome 21 caratteri': file_of(mod(userName='x' * 21), 'c_nm.json'),
      'nome con controllo': file_of(mod(userName='a\u0001b'), 'c_nm2.json'),
      'nome numerico': file_of(mod(userName=5), 'c_nm3.json'),
      'tesseraId errato': file_of(mod(tesseraId='ABC'), 'c_tid.json'),
      'dark mode 2': file_of(mod(darkMode='2'), 'c_dm.json'),
      'modalita timeline errata': file_of(mod(preferredMode='boh'), 'c_pm.json'),
      'spoiler mode errata': file_of(mod(spoilerMode='tutto'), 'c_sm.json'),
      'cutoff 999': file_of(mod(spoilerCutoff='999'), 'c_co.json'),
      'personaggio preferito inesistente': file_of(mod(favChar='Personaggio Inventato'), 'c_fc.json'),
      'stagione festeggiata testo': file_of(mod(stagioneFesteggiata='tre'), 'c_sf.json'),
      'campo null': file_of(mod(notes=None), 'c_null2.json'),
    }
    pre = snap(pgI); bad = []
    dlI.clear()
    for nome, path in cases.items():
        r = do_import(pgI, path, wait=350)
        now = snap(pgI)
        errtoast = any('annullata' in t for t in r['toasts'])
        ok_state = (now == pre) and r['marker'] == 'vivo' and not r['pend']
        if not (errtoast and ok_state) or any('importato correttamente' in t for t in r['toasts']):
            bad.append((nome, r['toasts'][:1], now == pre))
    ok('4 %d file non validi: tutti rifiutati con messaggio, profilo e copia di sicurezza identici, nessun reload, nessuna conferma' % len(cases), not bad and not dlI, str(bad[:4]))
    msgs = {}
    for nome in ('json vuoto {}', 'file estraneo (altra app)', 'versione 3.0', 'voto 7', 'solo intestazione', 'id titolo inesistente 999'):
        r = do_import(pgI, cases[nome], wait=350); msgs[nome] = r['toasts'][0] if r['toasts'] else ''
    for n, m in msgs.items(): print('   msg[%s] = %s' % (n, m))
    ctxI.close()

    # file valido con campi extra ignorati e BOM
    ctxV, pgV, _, dlV = newpage(seedp=base_profile(fav_ok))
    extra = dict(good); extra['campoSconosciuto'] = {'a': 1}
    pth = os.path.join(D, 'v_extra.json'); open(pth, 'w', encoding='utf-8').write('﻿' + json.dumps({'app': 'marvel-ultimate-timeline', 'version': '2.0', 'schemaVersion': 1, **extra}))
    r = do_import(pgV, pth)
    ok('4b file valido con BOM e campo extra sconosciuto: importato, campo extra ignorato', any('importato correttamente' in t for t in r['toasts']) and 'campoSconosciuto' not in json.dumps(snap(pgV)))
    # annulla la conferma: nulla cambia
    pre = snap(pgV); pgV.remove_listener('dialog', pgV._impl_obj) if False else None
    ctxV.close()

    # ---------- 5. errore di scrittura durante l'importazione ----------
    for mode in ('throw', 'silent'):
        ctxW, pgW, eW, dlW = newpage(seedp=base_profile(fav_ok))
        tgt = file_of(base_profile(fav_ok) | {'userName': 'Nuovo', 'ratings': {'002': 3}, 'notes': {}}, 'w_%s.json' % mode)
        pre = snap(pgW)
        pgW.evaluate("(m)=>{window.__failKey='%s';window.__failMode=m}" % OBJ['ratings'], mode)
        r = do_import(pgW, tgt, wait=500)
        pgW.evaluate("()=>{window.__failKey=null}")
        now = snap(pgW)
        ok('5 (%s) errore a meta\' scrittura: profilo e copia di sicurezza ripristinati, nessun "riuscita", nessun reload' % mode,
           now == pre and any('NON riuscita' in t and 'ripristinato' in t for t in r['toasts']) and not any('importato correttamente' in t for t in r['toasts']) and not r['pend'], str(r['toasts']))
        ctxW.close()

    # ---------- 6. ripristino backup ----------
    # 6a backup reale prodotto dall'app (autosave dopo 5 s)
    ctxR, pgR, eR, dlR = newpage(seedp=base_profile(fav_ok), block=False, hold=False)
    pgR.wait_for_timeout(6500)
    bkraw = pgR.evaluate("()=>localStorage.getItem('%s')" % AUTOBK)
    ok('6a l\'app ha prodotto da sola la copia automatica (formato reale)', bkraw and json.loads(bkraw)['app'] == 'marvel-ultimate-timeline' and json.loads(bkraw)['schemaVersion'] == 1)
    SAref = prof(snap(pgR)); ctxR.close()
    ctxS, pgS, eS, dlS = newpage(url=NEW, seedp=base_profile(fav_ok) | {'watched': {'040': True}, 'userName': 'Altro', 'notes': {}, 'badgesEarned': ['maratoneta']}, extra={AUTOBK: bkraw}, hold=True, block=True)
    vis = pgS.evaluate("()=>!document.getElementById('autoBackupHint').hidden")
    ok('6b con una copia valida compare il pulsante di ripristino', vis)
    pgS.evaluate("()=>{window.__toasts=[]}")
    pgS.evaluate("()=>document.getElementById('autoBackupRestoreBtn').click()"); pgS.wait_for_timeout(500)
    SS = prof(snap(pgS)); diff = {k: (SAref[k], SS[k]) for k in ALLK if SAref[k] != SS[k] and k != 'lastWatched'}
    ok('6c ripristino: il profilo corrente e\' sostituito dalla copia (nome, note, premi, visti), nulla del precedente resta', not diff and SS['userName'] == 'Franco' and SS['badgesEarned'] == ['primo-passo', 'essenziale', 'cinefilo'], str(list(diff.items())[:3]))
    ok('6d ripristino: toast di riuscita', any('ripristinata' in t for t in pgS.evaluate("()=>window.__toasts")))
    ctxS.close()
    # 6e backup non valido (ma con visti, cosi' il pulsante compare)
    badbk = json.loads(bkraw); badbk['ratings'] = {'001': 99}
    ctxT, pgT, eT, dlT = newpage(url=NEW, seedp=base_profile(fav_ok) | {'userName': 'Attuale'}, extra={AUTOBK: json.dumps(badbk)}, hold=True, block=True)
    vis = pgT.evaluate("()=>!document.getElementById('autoBackupHint').hidden")
    pre = snap(pgT)
    pgT.evaluate("()=>{window.__toasts=[]}"); pgT.evaluate("()=>document.getElementById('autoBackupRestoreBtn').click()"); pgT.wait_for_timeout(500)
    ok('6e backup non valido: rifiutato, profilo e copia invariati, nessuna conferma', vis and snap(pgT) == pre and any('Ripristino annullato' in t for t in pgT.evaluate("()=>window.__toasts")) and not dlT, str(pgT.evaluate("()=>window.__toasts")))
    ctxT.close()
    # 6f backup scritto da una versione precedente (senza campi recenti): accettato con reset dei due campi
    oldbk = json.loads(bkraw); oldbk.pop('badgesEarned'); oldbk.pop('roadToDoomsday')
    ctxU, pgU, eU, dlU = newpage(url=NEW, seedp=base_profile(fav_ok) | {'userName': 'Attuale'}, extra={AUTOBK: json.dumps(oldbk)}, hold=True, block=True)
    pgU.evaluate("()=>document.getElementById('autoBackupRestoreBtn').click()"); pgU.wait_for_timeout(500)
    sU = snap(pgU)
    ok('6f backup di versione precedente: ripristinato, badge/Road del profilo corrente non ereditati', sU[STR['userName']] == 'Franco' and sU.get(OBJ['badgesEarned']) is None and sU.get(OBJ['roadToDoomsday']) is None)
    ctxU.close()
    # 6g errore di scrittura durante il ripristino
    ctxX, pgX, eX, dlX = newpage(url=NEW, seedp=base_profile(fav_ok) | {'userName': 'Attuale'}, extra={AUTOBK: bkraw}, hold=True, block=True)
    pre = snap(pgX); pgX.evaluate("()=>{window.__toasts=[];window.__failKey='%s';window.__failMode='throw'}" % OBJ['notes'])
    pgX.evaluate("()=>document.getElementById('autoBackupRestoreBtn').click()"); pgX.wait_for_timeout(500)
    pgX.evaluate("()=>{window.__failKey=null}")
    ok('6g errore di scrittura nel ripristino: profilo invariato, nessun "ripristinata"', snap(pgX) == pre and any('NON riuscito' in t for t in pgX.evaluate("()=>window.__toasts")) and not any('ripristinata' in t for t in pgX.evaluate("()=>window.__toasts")))
    ctxX.close()
    # 6h la copia pre-import e' recuperabile con lo stesso pulsante dopo il reload
    ctxY, pgY, eY, dlY = newpage(seedp=base_profile(fav_ok))
    fe = file_of(base_profile(fav_ok) | {'userName': 'Importato', 'watched': {'040': True}}, 'y.json')
    do_import(pgY, fe)
    pgY.evaluate("()=>{window.__holdReload=false;window.__blockAutosave=true}")
    pgY.evaluate("()=>window.__pendingReload && window.__pendingReload()"); pgY.wait_for_timeout(1800)
    vis = pgY.evaluate("()=>!document.getElementById('autoBackupHint').hidden")
    ok('6h dopo l\'import la copia del profilo precedente e\' offerta dal pulsante di ripristino', vis)
    pgY.evaluate("()=>document.getElementById('autoBackupRestoreBtn').click()"); pgY.wait_for_timeout(500)
    sY = snap(pgY)
    ok('6i ripristino della copia pre-import riporta il profilo di partenza', sY[STR['userName']] == 'Franco' and len(json.loads(sY[OBJ['watched']])) == len(P1['watched']))
    ctxY.close()

    # ---------- 7. conferma rifiutata, profilo precedente vuoto, file troppo grande ----------
    ctx7 = b.new_context(viewport={'width': 390, 'height': 844}); ctx7.add_init_script(INIT.replace('__BLOCK__', 'true'))
    pg7 = ctx7.new_page(); msgs7 = []
    pg7.on('dialog', lambda d: (msgs7.append(d.message), d.dismiss()))
    pg7.goto(NEW); seed(pg7, base_profile(fav_ok)); pg7.reload(); pg7.wait_for_timeout(1200)
    pg7.evaluate("()=>{window.__blockAutosave=true;window.__holdReload=true}")
    pre = snap(pg7); r = do_import(pg7, file_of(base_profile(fav_ok) | {'userName': 'Diverso'}, 'z1.json'))
    ok('7a conferma rifiutata: nessuna scrittura, nessun reload', snap(pg7) == pre and len(msgs7) == 1 and not r['pend'] and not any('importato' in t for t in r['toasts']))
    big = os.path.join(D, 'z_big.json'); open(big, 'w').write('{"app":"marvel-ultimate-timeline","x":"' + 'a' * (6 * 1024 * 1024) + '"}')
    r = do_import(pg7, big, wait=600)
    ok('7b file da 6 MB rifiutato senza modifiche', snap(pg7) == pre and any('troppo grande' in t for t in r['toasts']), str(r['toasts']))
    ctx7.close()
    ctx8, pg8, e8, d8 = newpage(extra={AUTOBK: json.dumps({'app': 'marvel-ultimate-timeline', 'marcatore': 'vecchia-copia'})})
    pg8.evaluate("()=>localStorage.removeItem('%s')" % OBJ['watched'])
    r = do_import(pg8, file_of(base_profile(fav_ok), 'z2.json'))
    ok('7c profilo precedente vuoto: la copia di sicurezza gia\' presente non viene toccata', 'vecchia-copia' in (pg8.evaluate("()=>localStorage.getItem('%s')" % AUTOBK) or '') and any('importato correttamente' in t for t in r['toasts']))
    ctx8.close()
    b.close()

fails = [n for n, c in res if not c]
print('\nTOTALE', len(res), 'FALLITI', fails)
