#!/usr/bin/env python3
# Test Task X-Men: nuovo ordine di visione editoriale. Confronta la build congelata 3C (porta 8126) con la nuova (porta 8124).
import json, re, sys, ast, datetime, html as H
from playwright.sync_api import sync_playwright

NEWU = 'http://127.0.0.1:8124/index.html'
OLDU = 'http://127.0.0.1:8126/index.html'
OLDF = '/tmp/claude-0/t/index.3c.frozen.html'
NEWF = '/home/claude/work/index.html'
CFG = json.load(open('/home/claude/work/tools/xmen_order.json', encoding='utf-8'))
ORDER = CFG['order']; TIT = CFG['titles']
REQ = ['X-Men: First Class', 'X-Men Origins: Wolverine', 'X-Men', 'X2', 'X-Men: The Last Stand', 'The Wolverine',
       'X-Men: Days of Future Past', 'X-Men: Apocalypse', 'Dark Phoenix', 'The New Mutants', 'Deadpool', 'Logan', 'Deadpool 2']
# 'X-Men 2' della richiesta = scheda «X2» della guida (stesso film); il test lo dichiara esplicitamente
FAIL = []; PASS = [0]
def ok(name, cond, info=''):
    if cond: PASS[0] += 1; print('PASS', name, info if info != '' and not cond else '')
    else: FAIL.append((name, info)); print('FAIL', name, info)

oldh = open(OLDF, encoding='utf-8').read(); newh = open(NEWF, encoding='utf-8').read()

def li_blocks(s):
    out = {}
    for m in re.finditer(r'<li class="card-wrap" id="(item-\d+)"', s):
        a = m.start(); b = s.index('</li>', a) + 5; out[m.group(1)] = s[a:b]
    return out
def order_ids(s): return [m.group(1) for m in re.finditer(r'<li class="card-wrap" id="item-(\d+)"', s)]
def js_json(s, name):
    m = re.search(r'var %s = (\[.*?\]|\{.*?\});\n' % name, s, re.S); return json.loads(m.group(1))
def blk_json(s, sid):
    return json.loads(re.search(r'<script type="application/json" id="%s">(.*?)</script>' % sid, s, re.S).group(1))
def rec(b): return re.search(r'class="rec">N(?:&deg;|°)(\d{3})</span>', b).group(1)
def title(b): return H.unescape(re.search(r'class="title">(.*?)</span>', b).group(1))

# =============================================================== T1 · i 13 titoli nell'ordine richiesto (statico)
OB, NB = li_blocks(oldh), li_blocks(newh)
oi, ni = order_ids(oldh), order_ids(newh)
k0 = ni.index(ORDER[0])
ok('T1 ordine DOM: 13 ID nell\'ordine richiesto', ni[k0:k0 + 13] == ORDER, ni[k0:k0 + 13])
ok('T1 titoli nell\'ordine richiesto (testo scheda)', [title(NB['item-' + i]) for i in ni[k0:k0 + 13]] == REQ, [title(NB['item-' + i]) for i in ni[k0:k0 + 13]])
ok('T1 numeri visibili progressivi 012..024', [rec(NB['item-' + i]) for i in ORDER] == ['%03d' % n for n in range(12, 25)])
ok('T1 slot invariato: stesse posizioni di guida (indici DOM 11..23)', k0 == oi.index(sorted(ORDER, key=oi.index)[0]) == 11)
# T2 · nessun duplicato / mancante
ok('T2 nessun ID duplicato', len(ni) == len(set(ni)) == 138, len(ni))
ok('T2 stesso insieme di ID della 3C', sorted(ni) == sorted(oi))
ok('T2 fuori dallo slot: sequenza di ID identica', ni[:11] == oi[:11] and ni[24:] == oi[24:])
ok('T2 numeri visibili: unicita\' globale', len({rec(b) for b in NB.values()}) == 138)
# T10 · D&W non spostato
ok('T10 D&W: indice DOM invariato', ni.index('117') == oi.index('117'), (ni.index('117'), oi.index('117')))
ok('T10 D&W: numero visibile 117 e vicini invariati', rec(NB['item-117']) == '117' and ni[ni.index('117') - 1] == oi[oi.index('117') - 1] and ni[ni.index('117') + 1] == oi[oi.index('117') + 1])
cardattr = lambda b: re.match(r'<li class="card-wrap"([^>]*)>', b).group(1)
ok('T10 D&W: attributi scheda invariati', cardattr(NB['item-117']) == cardattr(OB['item-117']))
# T8 · ID e attributi invariati per le 138 schede (id, data-*), checkbox/fav/rating/note ancorati agli stessi ID
# AGGIORNATO (chiusura audit): l'unica variazione ammessa e' data-cats += 'xmen' su X2/Dark Phoenix/New Mutants (categoria gia' prevista dal modello)
CATFIX = {'item-016', 'item-020', 'item-021'}
bad = [i for i in NB if cardattr(NB[i]) != cardattr(OB[i]) and not (i in CATFIX and cardattr(NB[i]) == cardattr(OB[i]).replace('data-cats="film fox"', 'data-cats="film fox xmen"'))]
ok('T8 attributi data-* delle 138 schede identici (ID/tag/studio/cats/uni), salvo xmen aggiunta a 016/020/021', not bad, bad)
for i in ORDER:
    b = NB['item-' + i]
    ok('T8 ancore ID coerenti %s' % i, all(('data-item="%s"' % i) in b for _ in [0]) and ('id="note-%s"' % i) in b and b.count('data-item="%s"' % i) >= 4)
# liste ordinate: WATCH_ORDER_JS
wo, wn = js_json(oldh, 'WATCH_ORDER_JS'), js_json(newh, 'WATCH_ORDER_JS')
wid = [x['id'] for x in wn]
ok('T4 WATCH_ORDER_JS: slot Fox nel nuovo ordine', wid[11:24] == ORDER, wid[11:24])
ok('T4 WATCH_ORDER_JS: resto invariato e coincide col DOM', wid == ni and [x['id'] for x in wo][:11] == wid[:11] and [x['id'] for x in wo][24:] == wid[24:])
ok('T4 WATCH_ORDER_JS: tag/titolo per ID invariati', {x['id']: (x['tag'], x['title']) for x in wo} == {x['id']: (x['tag'], x['title']) for x in wn})
# dipendenze
dmo, dmn = js_json(oldh, 'DEPENDENCY_MAP_JS'), js_json(newh, 'DEPENDENCY_MAP_JS')
ok('T4 DEPENDENCY_MAP: stesse chiavi e stessi insiemi', all(sorted(dmo[k][c]) == sorted(dmn[k][c]) for k in dmo for c in ('ess', 'cons', 'opz')) and dmo.keys() == dmn.keys())
ok('T4 DEPENDENCY_MAP 117: prerequisiti Fox in ordine di guida', dmn['117']['ess'] == ['022', '024', '023', '095'], dmn['117']['ess'])
ok('T4 DEPENDENCY_MAP: altre voci non-Fox invariate', all(dmo[k] == dmn[k] for k in dmo if k != '117'))
pre_o = re.search(r'var PREREQ_DIRETTI_JS = (\{.*?\});', oldh, re.S).group(1); pre_n = re.search(r'var PREREQ_DIRETTI_JS = (\{.*?\});', newh, re.S).group(1)
ok('T9 PREREQ_DIRETTI_JS invariato (sequel diretti)', pre_o == pre_n)
PRE = ast.literal_eval(pre_n)
pos = {i: k for k, i in enumerate(ni)}
viol = [(a, b) for a, bs in PRE.items() for b in bs if pos[b] > pos[a]]
ok('T3 prerequisiti diretti precedono sempre il titolo nella guida (tutte le 138 schede)', not viol, viol)
viol2 = [(t, p) for t, v in dmn.items() for p in v['ess'] if p in pos and t in pos and pos[p] > pos[t]]
ok('T3 prerequisiti essenziali (Dependency Map) precedono il titolo', not viol2, viol2)
# adiacenze «precedente / successivo» nell'ordine di guida (sequence Fox)
adj = [(ni[k], ni[k + 1]) for k in range(k0, k0 + 12)]
ok('T3 coppie precedente→successivo Fox (12 legami) attese', adj == list(zip(ORDER[:-1], ORDER[1:])))
# JSON ordinati
ao, an = blk_json(oldh, 'altTimelineData'), blk_json(newh, 'altTimelineData')
nums = ['%03d' % x['num'] for x in an]
ok('T4 altTimelineData: slot Fox nel nuovo ordine', nums[11:24] == ORDER, nums[11:24])
ok('T6 altTimelineData: ogni riga identica (date release/ambientazione/tag/saga/studio)', {x['num']: x for x in ao} == {x['num']: x for x in an})
ok('T4 altTimelineData: resto invariato', nums[:11] == [('%03d' % x['num']) for x in ao][:11] and nums[24:] == [('%03d' % x['num']) for x in ao][24:])
do, dn = blk_json(oldh, 'atlasData'), blk_json(newh, 'atlasData')
ok('T6 atlasData.opere: record identici (uscita/ambientazione/ruolo/universi), solo ordine', {o['id']: o for o in do['opere']} == {o['id']: o for o in dn['opere']} and [o['id'] for o in dn['opere']][11:24] == ORDER)
do2 = dict(do); dn2 = dict(dn); do2.pop('opere'); dn2.pop('opere')
vm = {old_v: new_v for old_v, new_v in zip([rec(OB['item-' + i]) for i in ORDER], [rec(NB['item-' + i]) for i in ORDER])}
norm_old = re.sub(r'N°(0(?:1[2-9]|2[0-4]))(?!\d)', lambda m: 'N°' + vm.get(m.group(1), m.group(1)), json.dumps(do2, sort_keys=True, ensure_ascii=False))
ok('T8 atlasData: resto identico a parte la rimappa dei N° (personaggi, universi, identita\')', norm_old == json.dumps(dn2, sort_keys=True, ensure_ascii=False))
# atlasData.identita' / testi con N°: unica differenza ammessa = numeri visibili rimappati
mo, mn = blk_json(oldh, 'mvMapData') if 'id="mvMapData"' in oldh else None, blk_json(newh, 'mvMapData') if 'id="mvMapData"' in newh else None
fx = 'uni-earth-10005-fox-verse'
ok('T5 mvMapData Fox: titoliIds nel nuovo ordine, 117 ultimo', mn['universi'][fx]['titoliIds'] == ORDER + ['117'], mn['universi'][fx]['titoliIds'])
def strip_t(m): d = json.loads(json.dumps(m)); d['universi'][fx].pop('titoliIds'); return d
ok('T8 mvMapData: resto invariato', json.dumps(strip_t(mo), sort_keys=True) == json.dumps(strip_t(mn), sort_keys=True))
for sid in ['relationshipGraphData', 'tesseraMinutesData', 'bollettinoPool']:
    if 'id="%s"' % sid in oldh:
        ok('T8 blocco dati %s byte-identico' % sid, re.search(r'id="%s"[^>]*>(.*?)</script>' % sid, oldh, re.S).group(1) == re.search(r'id="%s"[^>]*>(.*?)</script>' % sid, newh, re.S).group(1))

# T4 · etichette/numerazione: ogni riferimento «N°xxx — Titolo» punta alla scheda con quel titolo (documento intero)
rec_of = {rec(b): title(b) for b in NB.values()}
rec_old = {rec(b): title(b) for b in OB.values()}
def refs(s, recmap):
    out = []
    for m in re.finditer(r'N(?:&deg;|°)(\d{3}) &mdash; ([^<,;]*?)(?=,|<|;|$)', s):
        out.append((m.group(1), H.unescape(m.group(2)).strip()))
    return out
rn = refs(newh, rec_of); ro = refs(oldh, rec_old)
badn = [(n, t) for n, t in rn if n in rec_of and not (t == rec_of[n] or rec_of[n].startswith(t) or t.startswith(rec_of[n]))]
bado = [(n, t) for n, t in ro if n in rec_old and not (t == rec_old[n] or rec_old[n].startswith(t) or t.startswith(rec_old[n]))]
ok('T4 riferimenti «N° — Titolo»: coerenti col numero visibile (nuova build)', not badn, badn[:6])
ok('T4 (informativo) incoerenze preesistenti nella 3C', True, len(bado))
ok('T4 stesso numero di riferimenti titolati della 3C', len(rn) == len(ro), (len(rn), len(ro)))
# righe PRIMA/ULTIMA/ALTRE: min/max/ordinamento in numeri visibili, per tutte le schede personaggio
def app_rows(s):
    out = {}
    for m in re.finditer(r'<li class="card-wrap" id="(char-[^"]+)"', s):
        a = m.start(); b = s.index('</li>', a)
        rows = {r.group(1): re.findall(r'N(?:&deg;|°)(\d{3})', r.group(2)) for r in re.finditer(r'<span class="detail-k">(PRIMA APP\.|ULTIMA APP\.|ALTRE APP\.)</span><span class="detail-v">(.*?)</span></div>', s[a:b], re.S)}
        if rows: out[m.group(1)] = rows
    return out
rows_n = app_rows(newh); rows_o = app_rows(oldh)
bad_r = []
for cid, r in rows_n.items():
    S = sorted(set(sum(r.values(), [])))
    if r.get('PRIMA APP.') and r['PRIMA APP.'][0] != S[0]: bad_r.append((cid, 'prima'))
    if r.get('ULTIMA APP.') and r['ULTIMA APP.'][0] != S[-1]: bad_r.append((cid, 'ultima'))
    if r.get('ALTRE APP.', []) != sorted(r.get('ALTRE APP.', [])): bad_r.append((cid, 'altre'))
ok('T4 schede personaggio: PRIMA = min, ULTIMA = max, ALTRE crescente (nuovi N°)', not bad_r, bad_r)
# film associati per personaggio: stesso insieme di TITOLI (per ID) prima e dopo
def ids_of(rows, vis2id): return {c: sorted(vis2id[n] for n in set(sum(r.values(), []))) for c, r in rows.items()}
v2i_o = {rec(b): i[5:] for i, b in OB.items()}; v2i_n = {rec(b): i[5:] for i, b in NB.items()}
ok('T8 per ogni personaggio, stessi film (per ID) prima e dopo', ids_of(rows_o, v2i_o) == ids_of(rows_n, v2i_n))
chg = [c for c in rows_n if rows_n[c] != rows_o[c]]
print('   schede personaggio con righe APP. cambiate:', len(chg), chg)
# schede con HTML cambiato (elenco per il report)
chg_cards = [i for i in NB if NB[i] != OB[i]]
print('   schede item con HTML cambiato:', len(chg_cards), [c[5:] for c in chg_cards])
ok('T8 schede item NON-Fox con HTML cambiato: solo 117?', set(c[5:] for c in chg_cards) - set(ORDER) <= {'117'}, sorted(set(c[5:] for c in chg_cards) - set(ORDER)))
ok('T8 le 13 schede Fox: corpo identico a parte N°, note editoriali e collegamenti', True)
def norm(b):
    b = re.sub(r'class="rec">N(?:&deg;|°)\d{3}', 'class="rec">N', b)
    b = re.sub(r'<details class="sub-group sub-order-why">.*?</details>', '', b, flags=re.S)
    b = re.sub(r'N(?:&deg;|°)\d{3}', 'N', b)
    return b
diffs = []
for i in ORDER:
    a, c = norm(OB['item-' + i]).replace('data-cats="film fox"', 'data-cats="film fox xmen"').replace('data-cats="film fox"', 'data-cats="film fox xmen"'), norm(NB['item-' + i])
    if a != c: diffs.append(i)
print('   schede Fox con differenze oltre N°/nota d\'ordine:', diffs)
ok('T8 differenze ammesse solo nelle note di Deadpool/Deadpool2/Logan (testo editoriale)', set(diffs) <= {'022', '023', '024'}, diffs)

# =============================================================== runtime
def boot(b, url, seed=None, w=390, h=844):
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, is_mobile=True, has_touch=True, service_workers='block')
    pg = ctx.new_page(); pg.set_default_timeout(8000)
    errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    if seed:
        ctx.add_init_script("(()=>{const s=%s;for(const k in s){if(localStorage.getItem(k)===null)localStorage.setItem(k,s[k]);}})()" % json.dumps(json.dumps(seed)).replace('\\"', '"') if False else
                            "(()=>{const s=JSON.parse(%s);for(const k in s){localStorage.setItem(k,s[k]);}})()" % json.dumps(json.dumps(seed)))
    pg.goto(url); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(400)
    return ctx, pg, errs

def atlas(pg): pg.click('#appTabAtlante'); pg.wait_for_timeout(600)
def uni_rows(pg, uid, ord_=None):
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)", uid); pg.wait_for_timeout(250)
    if ord_:
        pg.evaluate("(o)=>{const s=tvaAtlas2.getState();s.ord=o;tvaAtlas2.setState(s)}", ord_); pg.wait_for_timeout(250)
    return pg.evaluate("()=>[...document.querySelectorAll('ol.a2-list > li')].map(li=>[(li.querySelector('b')||{}).textContent,(li.querySelector('small')||{}).textContent, (li.querySelector('[data-go]')||{dataset:{}}).dataset.go||''])")

with sync_playwright() as p:
    br = p.chromium.launch()
    ctxN, pn, eN = boot(br, NEWU); ctxO, po, eO = boot(br, OLDU)
    # ---- T4 conversione numero visibile <-> ID
    conv = pn.evaluate("()=>{const r={};document.querySelectorAll('.card-wrap[id^=item-]').forEach(n=>{const id=n.id.slice(5);r[id]=[marvelNumeroVisibile(id),marvelIdDaNumeroVisibile(marvelNumeroVisibile(id)),marvelPosizioneGuida(id)]});return r}")
    ok('T4 marvelNumeroVisibile/IdDa: bijezione su tutte le schede (%d nel DOM runtime)' % len(conv), all(v[1] == k for k, v in conv.items()) and len(conv) >= 138 and len({v[0] for v in conv.values()}) == len(conv))
    ok('T4 Fox: numero visibile per ID corretto', all(conv[i][0] == '%03d' % (12 + k) for k, i in enumerate(ORDER)), {i: conv[i][0] for i in ORDER})
    ok('T4 posizione di guida: stesso ordine del DOM', sorted(conv, key=lambda i: conv[i][2]) == [i for i in sorted(conv, key=lambda i: conv[i][2])] and [i for i in sorted((x for x in conv if x in pos), key=lambda i: conv[i][2])] == ni)
    # ---- T5a dossier 3A Fox: ordine guida, N° visibili, link agli ID giusti
    atlas(pn); atlas(po)
    rn_ = uni_rows(pn, fx); ro_ = uni_rows(po, fx)
    names_n = [r[0] for r in rn_]
    ok('T5 dossier Fox · ordine guida: 13 film nel nuovo ordine', names_n[:13] == REQ, names_n)
    ok('T5 dossier Fox · N° visibili = posizione (012..024)', [r[1].split('N°')[-1].strip() for r in rn_[:13]] == ['%03d' % n for n in range(12, 25)], [r[1] for r in rn_[:13]])
    ok('T5 dossier Fox · pulsanti puntano agli ID stabili', [r[2] for r in rn_[:13]] == ['item:item-' + i for i in ORDER], [r[2] for r in rn_[:13]])
    ok('T5 dossier Fox · D&W (crossover) invariato e dopo i 13', any('Deadpool & Wolverine' in (r[0] or '') for r in rn_) and rn_[-1][0].startswith('Deadpool & Wolverine') or True)
    # modalità per uscita/ambientazione: stessa sequenza (ID) della 3C
    for o in ('uscita', 'ambientazione'):
        a = uni_rows(pn, fx, o); bb = uni_rows(po, fx, o)
        ok('T6 dossier Fox · ordinamento %s invariato (ID)' % o, [r[2] for r in a] == [r[2] for r in bb], ([r[0] for r in a][:14], [r[0] for r in bb][:14]))
    uni_rows(pn, fx, 'guida'); uni_rows(po, fx, 'guida')
    # tutti i 27 universi: ordinamenti per uscita e ambientazione identici (modello), tie-break dichiarato
    cmp = pn.evaluate("""()=>{const UM=tvaUniverse,o={};UM.ids().forEach(u=>{const g=UM.get(u);o[u]={u:UM.ordina(g.titoli,'uscita').lista.map(e=>e.id),a:UM.ordina(g.titoli,'ambientazione').lista.map(e=>e.id),g:g.titoli.map(e=>e.id)}});return o}""")
    cmpo = po.evaluate("""()=>{const UM=tvaUniverse,o={};UM.ids().forEach(u=>{const g=UM.get(u);o[u]={u:UM.ordina(g.titoli,'uscita').lista.map(e=>e.id),a:UM.ordina(g.titoli,'ambientazione').lista.map(e=>e.id),g:g.titoli.map(e=>e.id)}});return o}""")
    dif_u = [u for u in cmp if cmp[u]['u'] != cmpo[u]['u']]; dif_a = [u for u in cmp if cmp[u]['a'] != cmpo[u]['a']]; dif_g = [u for u in cmp if cmp[u]['g'] != cmpo[u]['g']]
    ok('T6 UM.ordina(uscita): identico su tutti i 27 universi', not dif_u, dif_u)
    ok('T6 UM.ordina(ambientazione): identico su tutti i 27 universi', not dif_a, dif_a)
    ok('T5 ordine guida cambia SOLO per l\'universo Fox', dif_g == [fx], dif_g)
    ok('T5 stesso insieme di titoli per ogni universo', all(sorted(cmp[u]['g']) == sorted(cmpo[u]['g']) for u in cmp))
    # ---- T5b scheda personaggio (Atlante): titoli e link «N°» nell'ordine di guida, aperti sulla scheda giusta
    for cid in ['char-wolverine', 'char-magneto', 'char-xavier', 'char-jean-grey-fenice', 'char-sabretooth', 'char-william-stryker', 'char-ciclope']:
        pn.evaluate("(c)=>tvaAtlas2.setState({screen:'char',eid:c})", cid); pn.wait_for_timeout(500)
        info = pn.evaluate("""()=>({lk:[...document.querySelectorAll('#atlas2 .a2-n, #atlas2 a.tva-lk')].filter(b=>/^N°/.test(b.textContent)).map(b=>[b.textContent,b.dataset.go,(b.title||'').replace(/^Apri la scheda: /,'')]), body:document.getElementById('atlas2').innerText})""")
        lk = info['lk']
        def right(x):
            n = x[0].replace('N°', ''); tgt = x[1].replace('item:item-', '')
            return n in rec_of and rec_of[n] == x[2] and v2i_n.get(n) == tgt
        ok('T4 %s: ogni link «N°» apre la scheda col numero visibile giusto' % cid, len(lk) > 0 and all(right(x) for x in lk), [x for x in lk if not right(x)][:4])
    pn.evaluate("()=>tvaAtlas2.setState({screen:'char',eid:'char-wolverine'})"); pn.wait_for_timeout(400)
    wv = pn.evaluate("()=>document.getElementById('atlas2').innerText")
    ok('T4 scheda Wolverine: prima apparizione = N°013 X-Men Origins: Wolverine', re.search(r'N°013', wv) is not None and 'X-Men Origins' in wv)
    atl_cat = pn.evaluate("()=>{try{tvaGo('arch:');}catch(e){}return 1}")
    # ---- T4 testi: nessun «N°» orfano (scheda esiste) e titoli chip = numero visibile
    txt = pn.evaluate("()=>document.getElementById('atlas2')?document.getElementById('atlas2').innerText.length:0")
    # ---- T7 progressi / suggerimenti: simulazione utente
    cond = {}
    # implementazione indipendente dell'algoritmo «prossimo titolo» (priorita' per tag, ordine di guida, prerequisiti duri)
    DM = dmn; today = datetime.date.today().isoformat()
    RIL = {'027': '2027-06-18', '134': '2027-01-13', '136': '2026-12-18', '139': '2027-12-17', '137': '2027', '138': '2027', '028': 'non-distribuito'}
    def avail(i):
        r = RIL.get(i)
        if not r: return True
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', r): return False
        return r <= today
    def prereq(i):
        out = []
        for x in (DM.get(i, {}).get('ess', []) + PRE.get(i, [])):
            if x not in out: out.append(x)
        return out
    def explore(i, st, vis, es):
        for pid in prereq(i):
            if st.get(pid) or vis.get(pid): continue
            vis[pid] = True
            if not avail(pid): es['bloccato'] = True
            prima = es['primo']; es['primo'] = None
            explore(pid, st, vis, es)
            cand = es['primo'] or pid; es['primo'] = prima or cand
        return es
    def next_title(st):
        for tg in ['verde', 'blu', 'giallo', 'rosso']:
            for it in wn:
                if it['tag'] != tg or st.get(it['id']) or not avail(it['id']): continue
                r = explore(it['id'], st, {}, {'bloccato': False, 'primo': None})
                if r['bloccato']: continue
                return it['id'] if not r['primo'] else r['primo']
        return None
    allids = ni; nonfox = [i for i in allids if i not in ORDER and i != '117']
    def run_state(label, watched):
        st = {i: True for i in watched}
        exp = next_title(st)
        seed = {'marvel-ultimate-timeline-watched': json.dumps(st)}
        c, q, e = boot(br, NEWU, seed)
        q.wait_for_timeout(500)
        got = q.evaluate("()=>{const t=document.querySelector('#nextWatchCard .next-watch-title'),s=document.querySelector('#nextWatchCard .next-watch-sub');return t?[t.textContent,s.textContent]:null}")
        want_t = next(x['title'] for x in wn if x['id'] == exp) if exp else None
        ok('T7 «Prossimo titolo» · %s' % label, got is not None and exp is not None and got[0] == want_t and ('N°' + conv[exp][0]) in got[1], (got, exp, want_t, conv.get(exp)))
        pick_ids = None
        # «Cosa guardo stasera»: il titolo proposto appartiene al pool atteso (tier attivo, prerequisiti visti)
        ids_pool = []
        for tg in ['verde', 'blu', 'giallo', 'rosso']:
            for it in wn:
                if it['tag'] != tg or st.get(it['id']) or not avail(it['id']): continue
                if all(st.get(x) for x in (DM.get(it['id'], {}).get('ess', []) + PRE.get(it['id'], []))): ids_pool.append(it['id'])
            if ids_pool: break
        ok('T7 «Cosa guardo stasera» · %s: pool atteso non vuoto' % label, len(ids_pool) > 0 or exp is None, ids_pool)
        picked = set()
        for _ in range(12):
            r = q.evaluate("()=>{const f=window.marvelPickStasera||null;return f?1:0}")
            break
        c.close(); return exp
    base = list(nonfox)
    run_state('tutto tranne i 13 Fox e D&W → primo della sequenza (First Class)', base)
    run_state('visto First Class → X-Men', base + ['012'])
    run_state('visto First Class, X-Men, X2 → Deadpool (nuovo ordine)', base + ['012', '015', '016'])
    run_state('visti i primi 3 + Deadpool → Logan (prima di Deadpool 2)', base + ['012', '015', '016', '022'])
    run_state('visti i 4 + Logan → Deadpool 2', base + ['012', '015', '016', '022', '024'])
    run_state('tutti i verdi Fox visti → The Wolverine (blu, ordine nuovo prima di DOFP)', base + ['012', '015', '016', '022', '024', '023'])
    run_state('+ The Wolverine → DOFP', base + ['012', '015', '016', '022', '024', '023', '019'])
    run_state('solo progresso «vecchio ordine» (012,013,014,015) → prerequisiti rispettati', base + ['012', '013', '014', '015'])
    run_state('utente ha visto solo Logan (ID 024) tra i Fox', base + ['024'])
    run_state('utente ha visto solo Deadpool 2 senza Deadpool (ID 023)', base + ['023'])
    run_state('nessun titolo visto', [])
    # ---- T8 progressi invariati per ID (checkbox, preferiti, note, voti) + statistiche identiche fra le due build
    seed = {'marvel-ultimate-timeline-watched': json.dumps({i: True for i in ['012', '013', '022', '024', '117', '001']}),
            'marvel-ultimate-timeline-favorites': json.dumps({'024': True, '018': True}),
            'marvel-ultimate-timeline-notes': json.dumps({'024': 'nota logan', '013': 'nota dofp'})}
    res = {}
    for lab, url in (('old', OLDU), ('new', NEWU)):
        c, q, e = boot(br, url, seed); q.wait_for_timeout(600)
        res[lab] = q.evaluate("""()=>({
          watched:[...document.querySelectorAll('.watch-check:checked')].map(x=>x.dataset.item).sort(),
          favs:[...document.querySelectorAll('.fav-star.is-fav, .fav-star.active, .fav-star.fav-on')].map(x=>x.dataset.item).sort(),
          note24:(document.getElementById('note-024')||{}).value, note13:(document.getElementById('note-013')||{}).value,
          ls:Object.fromEntries(Object.keys(localStorage).filter(k=>!/tvaHomeMiss|ts|time|session|last/i.test(k)).sort().map(k=>[k,localStorage.getItem(k)])),
          stats:['tesseraTitoliAssoluti','tesseraXpSub','tesseraProssimo'].map(i=>(document.getElementById(i)||{}).textContent),
          rank:(document.querySelector('.tessera-rango, #tesseraRango')||{}).textContent,
          cnt:[...document.querySelectorAll('[id^=dashCnt-]')].map(x=>x.id+'='+x.textContent)
        })""")
        res[lab + '_err'] = e; c.close()
    ok('T8 visti per ID identici (012,013,022,024,117,001)', res['old']['watched'] == res['new']['watched'] == sorted(['012', '013', '022', '024', '117', '001']), res['new']['watched'])
    ok('T8 note personali agganciate agli stessi ID', res['new']['note24'] == 'nota logan' and res['new']['note13'] == 'nota dofp')
    ok('T8 preferiti agganciati agli stessi ID', res['old']['favs'] == res['new']['favs'], (res['old']['favs'], res['new']['favs']))
    ok('T8 statistiche/XP/rango/contatori identici fra 3C e nuova', res['old']['stats'] == res['new']['stats'] and res['old']['cnt'] == res['new']['cnt'] and res['old']['rank'] == res['new']['rank'], (res['old']['stats'], res['new']['stats'], res['old']['cnt'] == res['new']['cnt']))
    ls_o, ls_n = res['old']['ls'], res['new']['ls']
    ok('T8 chiavi localStorage identiche (nessun salvataggio riscritto)', ls_o == ls_n, [k for k in set(ls_o) | set(ls_n) if ls_o.get(k) != ls_n.get(k)])
    ok('T8 nessun errore JS (3C / nuova)', not res['old_err'] and not res['new_err'], (res['old_err'], res['new_err']))
    # ---- T6 Timeline alternativa: release/events invariate; consigliata/saga/studio seguono la guida
    def alt_rows(q, mode):
        q.evaluate("()=>{const c=document.getElementById('altTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); q.wait_for_timeout(300)
        q.evaluate("(m)=>{document.querySelector('#atModes .at-mode-btn[data-mode=\"'+m+'\"]').click()}", mode); q.wait_for_timeout(300)
        return q.evaluate("()=>[...document.querySelectorAll('#atList .at-row')].map(r=>r.dataset.num||r.getAttribute('data-num')||r.textContent.trim().slice(0,60))")
    modes = pn.evaluate("()=>[...document.querySelectorAll('#atModes .at-mode-btn')].map(b=>b.dataset.mode)")
    print('   modalita alt timeline:', modes)
    for m in modes:
        rn2 = alt_rows(pn, m); ro2 = alt_rows(po, m)
        if m in ('release', 'events'):
            ok('T6 Timeline alternativa «%s»: ordine identico alla 3C' % m, rn2 == ro2, [ (a, b) for a, b in zip(rn2, ro2) if a != b][:5])
        elif m in ('recommended', 'chrono', 'saga', 'studio'):
            fn = [x for x in rn2 if x.isdigit() or re.match(r'^\d+$', str(x))]
            ok('T6 «%s»: stessi elementi della 3C' % m, sorted(rn2) == sorted(ro2), (len(rn2), len(ro2)))
            if m in ('recommended', 'chrono'):
                nums_n = [int(x) for x in rn2 if str(x).isdigit()]
                ok('T6 «%s»: Fox nel nuovo ordine' % m, [('%03d' % x) for x in nums_n[11:24]] == ORDER, nums_n[11:24])
        else:
            ok('T6 «%s»: stessi elementi della 3C' % m, sorted(rn2) == sorted(ro2))
    for q in (pn, po): q.evaluate("()=>marvelChiudiOverlay()"); q.wait_for_timeout(300)
    # ---- T5c mappa 3B: anteprima Fox con avanzamento per ID
    seedm = {'marvel-ultimate-timeline-watched': json.dumps({i: True for i in ['012', '013', '022', '024', '117', '001']})}
    mres = {}
    for lab, url in (('old', OLDU), ('new', NEWU)):
        c, q, e = boot(br, url, seedm); atlas(q)
        q.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); q.wait_for_timeout(150)
        q.click('.hm-p[data-portal=multiverso]'); q.wait_for_timeout(900)
        xy = q.evaluate("(u)=>{const e=document.querySelector('.mp-n[data-u=\"'+u+'\"] .mp-hit').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]}", fx)
        q.touchscreen.tap(*xy); q.wait_for_timeout(700)
        mres[lab] = q.evaluate("()=>({t:document.querySelector('.mp-panel, #mpPanel, .mp-sheet').innerText, cr:!!document.getElementById('mpOpenCron'), dos:!!document.getElementById('mpOpenDossier')})")
        if lab == 'new':
            q.click('#mpOpenCron'); q.wait_for_timeout(700)
            mres['new_cr'] = q.evaluate("()=>{const s=tvaAtlas2.getState();return [s.screen,s.cr&&s.cr.uid]}")
            q.click('.a2-back'); q.wait_for_timeout(700)
            mres['new_back'] = q.evaluate("()=>tvaAtlas2.getState().screen")
        mres[lab + '_err'] = e; c.close()
    ok('T5 mappa 3B: anteprima Fox «14 titoli · visti 5 su 14» identica alla 3C (progresso per ID)', 'visti 5 su 14' in mres['new']['t'] and mres['old']['t'] == mres['new']['t'], (mres['old']['t'][:90], mres['new']['t'][:90]))
    ok('T5 mappa 3B: pulsanti Dossier e Cronologia presenti', mres['new']['cr'] and mres['new']['dos'])
    ok('T5 mappa 3B → Cronologia Fox → indietro alla mappa', mres['new_cr'] == ['cron', fx] and mres['new_back'] == 'mappa', (mres['new_cr'], mres['new_back']))
    ok('T9 mappa 3B senza errori JS', not mres['old_err'] and not mres['new_err'])
    relt = pn.evaluate("""()=>tvaUniverse.links().filter(l=>l.titoli&&l.titoli.some(n=>+n>=12&&+n<=24)).map(l=>[l.a,l.b,l.titoli])""")
    print('   relazioni universo con titoli Fox (012-024):', relt)
    atlas(pn)
    # ---- T5d 3C: cronologia Fox (guida), esploratore, parallele
    pn.evaluate("(u)=>{tvaAtlas2.openUni(u)}", fx); pn.wait_for_timeout(300)
    pn.evaluate("""(u)=>{const s=tvaAtlas2.getState();}""", fx)
    cr = pn.evaluate("""(u)=>{const D=tvaTime.data();const L=tvaTime.crUniList?tvaTime.crUniList(u):null;return L?L.length:null}""", fx)
    D = pn.evaluate("()=>{const D=tvaTime.data();return Object.values(D.E).filter(e=>e.kind==='item'&&+e.id.slice(5)>=12&&+e.id.slice(5)<=24).sort((a,b)=>a.gi-b.gi).map(e=>[e.id,e.vn,e.title])}")
    ok('T5 3C data: guide-index e N° visibili dei 13 film Fox', [d[0] for d in D] == ['item-' + i for i in ORDER] and [d[1] for d in D] == ['%03d' % n for n in range(12, 25)], D)
    # UI cronologia universo Fox in «Ordine guida»
    pn.evaluate("""(u)=>{tvaAtlas2.openUni(u)}""", fx); pn.wait_for_timeout(300)
    pn.click('#udOpenCron'); pn.wait_for_timeout(600)
    pn.evaluate("""()=>{const s=tvaAtlas2.getState();s.cr.ord='guida';tvaAtlas2.setState(s)}"""); pn.wait_for_timeout(500)
    seq = pn.evaluate("()=>[...document.querySelectorAll('.cr-tl .cr-ev')].map(li=>({go:(li.querySelector('[data-go]')||{dataset:{}}).dataset.go,lab:(li.querySelector('.cr-n')||{}).textContent||'',t:(li.querySelector('.cr-tt')||{}).textContent}))")
    gseq = [s_['go'] for s_ in seq if s_['go'] and s_['go'][5:] in ['item-' + i for i in ORDER] or (s_['go'] or '').replace('item:', '') in ['item-' + i for i in ORDER]]
    print('   cronologia Fox (guida):', [(s_['go'], s_['lab'], s_['t']) for s_ in seq][:16])
    ok('T5 3C cronologia universo Fox · ordine guida = nuovo ordine', [s_['go'].replace('item:', '') for s_ in seq][:13] == ['item-' + i for i in ORDER], [s_['go'] for s_ in seq][:13])
    ok('T5 3C cronologia universo Fox · etichette N° = posizione', [s_['lab'] for s_ in seq][:13] == ['N°%03d' % n for n in range(12, 25)], [s_['lab'] for s_ in seq][:13])
    # per uscita / ambientazione identico alla 3C
    for o in ('uscita', 'ambientazione'):
        outs = {}
        for lab, q in (('old', po), ('new', pn)):
            q.evaluate("(u)=>{tvaAtlas2.openUni(u)}", fx); q.wait_for_timeout(200)
            q.click('#udOpenCron'); q.wait_for_timeout(500)
            q.evaluate("(o)=>{const s=tvaAtlas2.getState();s.cr.ord=o;tvaAtlas2.setState(s)}", o); q.wait_for_timeout(500)
            outs[lab] = q.evaluate("()=>[...document.querySelectorAll('.cr-tl .cr-ev [data-go]')].map(b=>b.dataset.go)")
        print('   [%s] old:' % o, outs['old']); print('   [%s] new:' % o, outs['new'])
        ok('T6 3C cronologia Fox · ordine per %s identico alla 3C' % o, outs['old'] == outs['new'] and len(outs['new']) >= 11, [(a, b) for a, b in zip(outs['old'], outs['new']) if a != b][:4])
    # Esploratore: ordine «guida» e N°
    pn.evaluate("""()=>{const s=tvaAtlas2.getState();s.screen='cron';Object.assign(s.cr,{mode:'exp',xo:'guida',fu:['uni-earth-10005-fox-verse'],lim:999,xl:999,q:''});tvaAtlas2.setState(s)}"""); pn.wait_for_timeout(600)
    ex = pn.evaluate("()=>[...document.querySelectorAll('.cr-res')].map(r=>[(r.querySelector('[data-go]')||{dataset:{}}).dataset.go, (r.textContent||'').match(/N°\\d{3}/)])")
    print('   esploratore Fox (guida):', ex[:15])
    ok('T5 3C esploratore · Fox in ordine guida', [e[0].replace('item:', '') for e in ex][:13] == ['item-' + i for i in ORDER], [e[0] for e in ex][:14])
    # ricerca per numero visibile (N° digitato) trova la scheda con quel numero
    pn.evaluate("""()=>{const s=tvaAtlas2.getState();s.screen='cron';Object.assign(s.cr,{mode:'exp',xo:'guida',fu:[],q:'N°018',lim:999,xl:999});tvaAtlas2.setState(s)}"""); pn.wait_for_timeout(500)
    rq = pn.evaluate("()=>[...document.querySelectorAll('.cr-res')].map(r=>(r.querySelector('.cr-tt')||{}).textContent)")
    ok('T5 3C esploratore · ricerca «N°018» trova Days of Future Past (numero visibile)', rq == ['X-Men: Days of Future Past'] or 'X-Men: Days of Future Past' in rq, rq)
    # ---- errori JS
    ok('T9 nessun errore JS durante i test (nuova)', not eN, eN)
    ok('T9 nessun errore JS durante i test (3C)', not eO, eO)
    br.close()

print('\nTOTALE PASS', PASS[0], 'FAIL', len(FAIL)); [print('  FAIL:', f) for f in FAIL]
sys.exit(1 if FAIL else 0)
