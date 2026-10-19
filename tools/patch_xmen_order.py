#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ordine di visione editoriale X-Men (build 20261019-xmen).

Riordina le 13 schede Fox nelle STESSE 13 posizioni di guida (012..024) secondo tools/xmen_order.json.
ID stabili (data-item, id, chiavi di salvataggio) INVARIATI. Cambiano solo:
  - posizione nel DOM e numero visibile (N°, scritto in <span class="rec">);
  - tutti i riferimenti testuali «N°» che dipendono dalla posizione (una sola tabella old->new);
  - le righe PRIMA/ULTIMA/ALTRE APP. delle schede personaggio (primo/ultimo in ordine di guida);
  - WATCH_ORDER_JS, DEPENDENCY_MAP_JS['117'].ess, altTimelineData, atlasData.opere, mvMapData.titoliIds;
  - note editoriali (Logan, Deadpool, Deadpool 2, Days of Future Past, intestazione sezione Fox);
  - un helper window.marvelPosizioneGuida (posizione di guida di un ID) accanto alle altre due funzioni di conversione.
Idempotente: se il DOM e' gia' nell'ordine richiesto non fa nulla.
D&W (117) e tutte le altre schede non vengono toccate. Le viste per uscita/ambientazione non dipendono da questo ordine.
"""
import re, json, sys, html

P = '/home/claude/work/index.html'
CFG = json.load(open('/home/claude/work/tools/xmen_order.json', encoding='utf-8'))
NEW = CFG['order']
TITLES = CFG['titles']
s = open(P, encoding='utf-8').read()

# ---------------------------------------------------------------- stato corrente
ids_dom = re.findall(r'<li class="card-wrap" id="item-(\d+)"', s)
pos = {i: k for k, i in enumerate(ids_dom)}
cur = sorted(NEW, key=lambda i: pos[i])
k0 = pos[cur[0]]
assert [pos[i] for i in cur] == list(range(k0, k0 + 13)), 'le 13 schede Fox non sono contigue'
if cur == NEW:
    print('xmen_order: gia applicato (DOM nell\'ordine richiesto)'); sys.exit(0)

def li_span(n):
    a = s.index('<li class="card-wrap" id="item-%s"' % n); b = s.index('</li>', a) + 5
    assert '<li' not in s[a + 5:b]
    return a, b

def rec_of(n):
    a, b = li_span(n)
    return re.search(r'class="rec">N(?:&deg;|°)(\d{3})</span>', s[a:b]).group(1)

old_vis = {i: rec_of(i) for i in cur}
slot_nums = [old_vis[i] for i in cur]                    # numeri visibili degli slot, in ordine di posizione
assert slot_nums == sorted(slot_nums), slot_nums
new_vis = {i: slot_nums[k] for k, i in enumerate(NEW)}   # il k-esimo titolo del nuovo ordine prende il k-esimo numero
VMAP = {old_vis[i]: new_vis[i] for i in NEW}
assert sorted(VMAP) == sorted(VMAP.values())
name_of_old = {old_vis[i]: html.unescape(re.search(r'class="title">(.*?)</span>', s[li_span(i)[0]:li_span(i)[1]]).group(1)) for i in NEW}
for i in NEW:
    assert name_of_old[old_vis[i]] == TITLES[i], (i, name_of_old[old_vis[i]], TITLES[i])
print('mappa N° vecchio->nuovo:', {k: VMAP[k] for k in sorted(VMAP)})

# ---------------------------------------------------------------- 0) helper + commento nel codice principale
old_comment = "(es. Logan prima di Deadpool)"
assert s.count(old_comment) == 1
s = s.replace(old_comment, "(es. l'ordine di visione editoriale dei film X-Men)")
old_c2 = "(es. Logan N°022 ha id 024)"
assert s.count(old_c2) == 1
s = s.replace(old_c2, "(es. in un percorso editoriale la scheda con id 018 puo' avere N°013)")
anchor = "  window.marvelIdDaNumeroVisibile = function(num) { var k = ('000' + num).slice(-3); return _costruisciNumVis().visToId[k] || k; };\n"
assert s.count(anchor) == 1
helper = anchor + (
    "  // Posizione di guida (0-based, ordine del DOM = ordine di visione del percorso) di un id a 3 cifre; null se non e' una scheda numerata.\n"
    "  // Unica fonte per ordinare liste di id 'nell'ordine della guida' (dossier, Atlante, relazioni): l'ordine per id NON coincide con la guida.\n"
    "  var _posGuidaCache = null;\n"
    "  window.marvelPosizioneGuida = function(id) {\n"
    "    if (!_posGuidaCache) { _posGuidaCache = {}; Array.prototype.slice.call(document.querySelectorAll('.card-wrap[id^=\"item-\"]')).forEach(function(n, k) { _posGuidaCache[n.id.slice(5)] = k; }); }\n"
    "    var mm = /^(?:item-)?(\\d{3})$/.exec(String(id)); if (!mm) return null; return Object.prototype.hasOwnProperty.call(_posGuidaCache, mm[1]) ? _posGuidaCache[mm[1]] : null;\n"
    "  };\n")
s = s.replace(anchor, helper)

# ---------------------------------------------------------------- 1) correzioni di dato (etichetta esplicita, numero sbagliato da prima)
fix = [
    ('Nightcrawler <span class="us-result-ref">&mdash; N&deg;013, Fox-Verse (X2)</span>',
     'Nightcrawler <span class="us-result-ref">&mdash; N&deg;@@%s@@, Fox-Verse (X2)</span>' % new_vis['016']),
    ('Hank McCoy/Beast <span class="us-result-ref">&mdash; N&deg;015, Fox-Verse (X-Men 3)</span>',
     'Hank McCoy/Beast <span class="us-result-ref">&mdash; N&deg;@@%s@@, Fox-Verse (X-Men 3)</span>' % new_vis['017']),
]
for a, b in fix:
    assert s.count(a) == 1, a
    s = s.replace(a, b)

# ---------------------------------------------------------------- 2) validazione dei riferimenti titolati + rimappa N° (una sola passata)
REF = re.compile(r'(N&deg;|N°)(0(?:1[2-9]|2[0-4]))(?!\d)')
n_titled = 0
for m in REF.finditer(s):
    tail = s[m.end():m.end() + 70]
    t = re.match(r'\s*(?:&mdash;|—)\s*([^<,;]*)', tail)
    if t and m.group(2) in name_of_old:
        want = name_of_old[m.group(2)]
        got = html.unescape(t.group(1)).strip()
        assert got.startswith(want), 'riferimento incoerente: %s -> %r (atteso %r)' % (m.group(0), got, want)
        n_titled += 1
print('riferimenti N° con titolo verificati:', n_titled)

stat = {'remapped': 0, 'same': 0, 'skipped': 0}
def sub(m):
    before = s_work[max(0, m.start() - 40):m.start()]
    if 'ut-marker-label">' in before:        # tacca dell'asse del grafo (ogni 20 posizioni), non un titolo
        stat['skipped'] += 1; return m.group(0)
    new = VMAP.get(m.group(2))
    if new is None: stat['skipped'] += 1; return m.group(0)
    if new == m.group(2): stat['same'] += 1; return m.group(0)
    stat['remapped'] += 1
    return m.group(1) + new
s_work = s
s = REF.sub(sub, s_work)
s = re.sub(r'@@(\d{3})@@', r'\1', s)
print('N° rimappati:', stat)

# ---------------------------------------------------------------- 3) righe PRIMA/ULTIMA/ALTRE APP. delle schede personaggio
ROW = re.compile(r'(<span class="detail-k">(PRIMA APP\.|ULTIMA APP\.|ALTRE APP\.)</span><span class="detail-v">)(.*?)(</span></div>)', re.S)
ITEM = re.compile(r'N&deg;(\d{3}) &mdash; ([^<]*?)(?=, N&deg;\d{3} &mdash; |$)')

def parse_rows(blk):
    rows = {}
    for r in ROW.finditer(blk):
        items = [(m.group(1), m.group(2)) for m in ITEM.finditer(r.group(3))]
        if ', '.join('N&deg;%s &mdash; %s' % it for it in items) != r.group(3):
            # riga con testo libero (es. serie animate senza N°): la scheda non e' modellabile; deve non contenere numeri di slot
            assert not any(n in VMAP for n in re.findall(r'N(?:&deg;|°)(\d{3})', r.group(3))), ('riga non modellabile con numeri Fox', r.group(3))
            return {}
        rows[r.group(2)] = items
    return rows

def derive(rows, mapfn):
    P = rows.get('PRIMA APP.', []); U = rows.get('ULTIMA APP.', []); A = rows.get('ALTRE APP.', [])
    name = {}
    for lst in (P, U, A):
        for n, t in lst: name[n] = t
    S = sorted(set(name))
    flag_u_in_a = bool(U) and U[0][0] in [n for n, _ in A]
    return P, U, A, name, S, flag_u_in_a

def build(rows, nmap):
    """Ricostruisce (PRIMA, ULTIMA, ALTRE) da un insieme di numeri; nmap = vecchio->nuovo numero.
    Il testo del titolo resta quello della riga d'origine (alcune righe scrivono '&amp;', altre '&')."""
    P, U, A, name, S, flag = derive(rows, None)
    inv = {nmap.get(n, n): n for n in S}
    Sn = sorted(inv)
    def nm(key, n):
        own = dict(rows.get(key, []))
        return own.get(inv[n], name[inv[n]])
    out = {}
    if P: out['PRIMA APP.'] = [(Sn[0], nm('PRIMA APP.', Sn[0]))]
    if U: out['ULTIMA APP.'] = [(Sn[-1], nm('ULTIMA APP.', Sn[-1]))]
    if 'ALTRE APP.' in rows:
        mid = [n for n in Sn[1:] if not (U and n == Sn[-1] and not flag)] if len(Sn) > 1 else []
        out['ALTRE APP.'] = [(n, nm('ALTRE APP.', n)) for n in mid]
    return out

def card_blocks():
    for m in re.finditer(r'<li class="card-wrap" id="(char-[^"]+)"', s):
        a = m.start(); b = s.index('</li>', a) + 5
        yield m.group(1), a, b

# autotest: con la mappa identita' il modello deve riprodurre ESATTAMENTE le righe di tutte le schede (stato corrente, N° gia' rimappati)
nrows = 0
for cid, a, b in card_blocks():
    rows = parse_rows(s[a:b])
    if not rows: continue
    nrows += 1
n_touch = 0
# le righe sono gia' state rimappate dalla passata 2: ora vanno solo riordinate. Modello su stato post-rimappa.
def rewrite_rows(blk):
    rows = parse_rows(blk)
    if not rows: return blk, False
    exp = build(rows, {})
    changed = False
    def r(m):
        nonlocal changed
        key = m.group(2)
        new = exp.get(key)
        if new is None: return m.group(0)
        txt = ', '.join('N&deg;%s &mdash; %s' % it for it in new)
        if txt != m.group(3): changed = True
        return m.group(1) + txt + m.group(4)
    return ROW.sub(r, blk), changed

# prova del modello sullo stato ORIGINALE (prima di qualsiasi rimappa): ricostruzione identica per tutte le schede
s_orig = open(P, encoding='utf-8').read()
for m in re.finditer(r'<li class="card-wrap" id="(char-[^"]+)"', s_orig):
    a = m.start(); b = s_orig.index('</li>', a) + 5; blk = s_orig[a:b]
    rows = parse_rows(blk)
    if not rows: continue
    exp = build(rows, {})
    for key, items in rows.items():
        assert exp.get(key, items) == items, ('modello PRIMA/ULTIMA/ALTRE non riproduce', m.group(1), key, items, exp.get(key))
print('modello PRIMA/ULTIMA/ALTRE verificato su', nrows, 'schede personaggio')

out = []; last = 0; rewritten = []
for cid, a, b in card_blocks():
    blk = s[a:b]
    nb, ch = rewrite_rows(blk)
    if ch: rewritten.append(cid)
    out.append(s[last:a]); out.append(nb); last = b
out.append(s[last:]); s = ''.join(out)
print('schede personaggio con righe APP. riordinate:', len(rewritten), rewritten)

# ---------------------------------------------------------------- 4) riordino blocchi <li> nel DOM
blocks = {}
for i in cur:
    a, b = li_span(i); blocks[i] = s[a:b]
a0 = li_span(cur[0])[0]; b0 = li_span(cur[-1])[1]
between = [s[li_span(cur[k])[1]:li_span(cur[k + 1])[0]] for k in range(12)]
assert all(x.strip() == '' for x in between), 'contenuto inatteso tra le schede Fox'
s = s[:a0] + '\n    '.join(blocks[i] for i in NEW) + s[b0:]

# ---------------------------------------------------------------- 5) WATCH_ORDER_JS
m = re.search(r'var WATCH_ORDER_JS = (\[.*?\]);\n', s, re.S); W = json.loads(m.group(1))
ids = [x['id'] for x in W]; i0 = ids.index(cur[0])
assert ids[i0:i0 + 13] == cur, 'WATCH_ORDER_JS: slot Fox inatteso'
byid = {x['id']: x for x in W}
W[i0:i0 + 13] = [byid[i] for i in NEW]
s = s[:m.start(1)] + json.dumps(W, ensure_ascii=False) + s[m.end(1):]

# ---------------------------------------------------------------- 6) DEPENDENCY_MAP_JS: ordine dei prerequisiti Fox di D&W nell'ordine di guida
m = re.search(r'var DEPENDENCY_MAP_JS = (\{.*?\});\n', s, re.S); DM = json.loads(m.group(1))
for tgt, cats in DM.items():
    for cat in ('ess', 'cons', 'opz'):
        lst = cats[cat]; slots = [k for k, x in enumerate(lst) if x in NEW]
        if len(slots) > 1:
            srt = sorted((lst[k] for k in slots), key=NEW.index)
            for k, v in zip(slots, srt): lst[k] = v
            print('DEPENDENCY_MAP', tgt, cat, '->', lst)
raw = m.group(1)
sep = (', ', ': ')
assert json.dumps(json.loads(raw), ensure_ascii=False, separators=sep) == raw, 'formato DEPENDENCY_MAP_JS non round-trip'
s = s[:m.start(1)] + json.dumps(DM, ensure_ascii=False, separators=sep) + s[m.end(1):]

# ---------------------------------------------------------------- 7) blocchi JSON ordinati: altTimelineData, atlasData.opere, mvMapData (titoliIds Fox)
def reorder_slice(arr, getid):
    ids = [getid(x) for x in arr]; i0 = ids.index(cur[0])
    assert ids[i0:i0 + 13] == cur, ('slice Fox inatteso', ids[i0:i0 + 13])
    by = {getid(x): x for x in arr[i0:i0 + 13]}
    arr[i0:i0 + 13] = [by[i] for i in NEW]

def json_block(sid, fn, sep, ea):
    global s
    m = re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)' % sid, s, re.S)
    raw = m.group(2); D = json.loads(raw)
    assert json.dumps(D, ensure_ascii=ea, separators=sep) == raw, sid + ' non round-trip'
    fn(D)
    s = s[:m.start(2)] + json.dumps(D, ensure_ascii=ea, separators=sep) + s[m.end(2):]
json_block('atlasData', lambda D: reorder_slice(D['opere'], lambda x: x['id']), (',', ':'), False)
json_block('altTimelineData', lambda D: reorder_slice(D, lambda x: '%03d' % x['num']), (', ', ': '), True)
old_inner = ', '.join('"%s"' % i for i in cur); new_inner = ', '.join('"%s"' % i for i in NEW)
print('liste ID Fox (mvMapData) da riordinare:', s.count(old_inner))
assert s.count(old_inner) >= 1
s = s.replace(old_inner, new_inner)
assert s.count(old_inner) == 0

# ---------------------------------------------------------------- 8) note editoriali
def rep_once(old, new, where=''):
    global s
    assert s.count(old) == 1, ('nota non trovata/duplicata', where, s.count(old))
    s = s.replace(old, new)

# Logan: nota nei collegamenti + blocco «Perché questo ordine»
old_nota = "Posizionato prima di Deadpool per scelta editoriale del percorso (arco di Wolverine prima dei film di Deadpool): non indica precedenza cronologica, il film &egrave; ambientato nel 2029"
new_nota = "Nel percorso editoriale segue Deadpool e precede Deadpool 2, cos&igrave; Deadpool 2 non anticipa gli spoiler di Logan: non indica precedenza cronologica, il film &egrave; ambientato nel 2029"
rep_once(old_nota, new_nota, 'logan-collegamenti')

a, b = li_span('024'); blk = s[a:b]
i1 = blk.index('<details class="sub-group sub-order-why">'); i2 = blk.index('</details>', i1) + len('</details>')
why = ('<details class="sub-group sub-order-why">\n          <summary>&#129517; Perch&eacute; questo ordine</summary>\n          <div class="sub-group-body">'
       '<div class="detail-row "><span class="detail-k">ORDINE DI USCITA</span><span class="detail-v ">Deadpool (2016) &rarr; Logan (2017) &rarr; Deadpool 2 (2018).</span></div>'
       '<div class="detail-row "><span class="detail-k">ORDINE CONSIGLIATO QUI</span><span class="detail-v ">Deadpool &rarr; Logan &rarr; Deadpool 2. &Egrave; un ordine di visione editoriale di questa guida, non una cronologia canonica: Logan chiude l&rsquo;arco di Wolverine (Hugh Jackman) prima di Deadpool 2, che ne anticipa alcuni sviluppi, e il percorso prosegue poi verso Deadpool &amp; Wolverine (N&deg;117), che attinge a entrambe le linee.</span></div>'
       '<div class="detail-row "><span class="detail-k">CRONOLOGIA INTERNA</span><span class="detail-v ">Non dipende da questa posizione. Logan &egrave; ambientato nel 2029, cio&egrave; in un futuro rispetto al presente dei due Deadpool. I film Fox non formano un&rsquo;unica linea del tempo continua (dopo X-Men: Giorni di un futuro passato la continuit&agrave; viene riscritta) e questa guida non sostiene che le varie incarnazioni di Wolverine siano un solo personaggio coerente.</span></div>'
       '<div class="detail-row "><span class="detail-k">SE PREFERISCI</span><span class="detail-v ">L&rsquo;ordine di uscita e quello per ambientazione sono disponibili nella Timeline alternativa (modalit&agrave; &laquo;Uscita&raquo; ed &laquo;Eventi&raquo;). Gli identificativi e i progressi delle schede non cambiano.</span></div></div>\n        </details>')
blk = blk[:i1] + why + blk[i2:]
s = s[:a] + blk + s[b:]

# Deadpool e Deadpool 2: nota di posizione
old_dp = "Essenziale per Deadpool &amp; Wolverine. In questo percorso segue Logan (N&deg;%s) per scelta editoriale, non per cronologia: vedi &laquo;Perch&eacute; questo ordine&raquo; nella scheda di Logan" % VMAP['022']
assert s.count(old_dp) == 1, s.count(old_dp)
s = s.replace(old_dp, "Essenziale per Deadpool &amp; Wolverine. In questo percorso precede Logan (N&deg;%s) per scelta editoriale, non per cronologia: vedi &laquo;Perch&eacute; questo ordine&raquo; nella scheda di Logan" % new_vis['024'])
old_d2 = "Introduce Domino e Cable, essenziale per Deadpool &amp; Wolverine. In questo percorso segue Logan (N&deg;%s) per scelta editoriale, non per cronologia: vedi &laquo;Perch&eacute; questo ordine&raquo; nella scheda di Logan" % VMAP['022']
assert s.count(old_d2) == 1, s.count(old_d2)
s = s.replace(old_d2, "Introduce Domino e Cable, essenziale per Deadpool &amp; Wolverine. In questo percorso segue Logan (N&deg;%s) per scelta editoriale, non per cronologia: vedi &laquo;Perch&eacute; questo ordine&raquo; nella scheda di Logan" % new_vis['024'])

# Days of Future Past: blocco «Perché questa posizione» (stesso schema delle altre note d'ordine)
a, b = li_span('013'); blk = s[a:b]
MK = '</details></div>\n      <details class="watch-picker">'
mk = MK if blk.count(MK) == 1 else None
assert mk, 'marker DOFP non trovato'
dofp = ('</details><details class="sub-group sub-order-why">\n          <summary>&#129517; Perch&eacute; questa posizione</summary>\n          <div class="sub-group-body">'
        '<div class="detail-row "><span class="detail-k">ORDINE DI USCITA</span><span class="detail-v ">X-Men (2000), X2 (2003), X-Men: The Last Stand (2006), X-Men Origins: Wolverine (2009), X-Men: First Class (2011), The Wolverine (2013), Days of Future Past (2014).</span></div>'
        '<div class="detail-row "><span class="detail-k">ORDINE CONSIGLIATO QUI</span><span class="detail-v ">Dopo The Wolverine, la cui scena post-credit prepara questo film, e prima di Apocalypse. &Egrave; un ordine di visione editoriale, non una cronologia canonica: arrivarci dopo la trilogia originale e i prequel/spin-off di Wolverine aiuta a capire la riscrittura temporale che il film mette in atto.</span></div>'
        '<div class="detail-row "><span class="detail-k">SE PREFERISCI</span><span class="detail-v ">L&rsquo;ordine di uscita e quello per ambientazione sono disponibili nella Timeline alternativa. Gli identificativi e i progressi delle schede non cambiano.</span></div></div>\n        </details></div>\n      <details class="watch-picker">')
blk = blk.replace(mk, dofp)
s = s[:a] + blk + s[b:]

# intestazione sezione Fox: avviso d'ordine editoriale (dopo la lista, prima della sezione successiva)
sec_end = '</li></ul>\n<h3 class="sec-h" id="sec-1e">'
assert s.count(sec_end) == 1
note = ('</li></ul><div class="note-clip xmen-order-note"><span class="note-label">ORDINE DI VISIONE</span> &mdash; '
        'la sequenza dei film Fox &egrave; un percorso editoriale pensato per seguire la progressione narrativa, capire la riscrittura temporale di Days of Future Past e ridurre gli spoiler '
        '(soprattutto quelli di Logan in Deadpool 2): non &egrave; una cronologia canonica rigorosa. Per l&rsquo;ordine di uscita o per ambientazione usa la Timeline alternativa. '
        'Deadpool &amp; Wolverine resta nella sezione MCU.</div>\n<h3 class="sec-h" id="sec-1e">')
s = s.replace(sec_end, note)

open(P, 'w', encoding='utf-8').write(s)
print('ok: ordine X-Men applicato ->', ' '.join(NEW))
