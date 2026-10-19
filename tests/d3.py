import json,re
from playwright.sync_api import sync_playwright
s0=open('/home/claude/work/index.html',encoding='utf-8').read()
W=json.loads(re.search(r'var WATCH_ORDER_JS = (\[.*?\]);',s0).group(1))
T=json.loads(re.search(r'var PREREQ_DIRETTI_JS = (\{.*?\n  \});',s0,re.S).group(1).replace("'",'"').replace('\n',' ').replace(', }','}'))
M=json.loads(re.search(r'var DEPENDENCY_MAP_JS = (\{.*?\});',s0,re.S).group(1))
TAG={e['id']:e['tag'] for e in W}
res=[]
def ok(n,c,x=''): res.append(c); print('PASS' if c else 'FAIL',n,x)
START="()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"
ok('tabella: 64 titoli, 69 relazioni; 073=%s 123=%s 074=%s 129=%s'%(T['073'],T['123'],T['074'],T['129']),len(T)==64 and sum(map(len,T.values()))==69 and T['074']==['065'] and T['129']==['086'] and T['073']==['060','065','072'] and T['123']==['069'])
ok('mappe invariate (9, ess intatti)',sorted(M)==['051','067','084','089','099','102','117','136','139'] and M['136']['ess']==['089','112','123','125'])
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(state):
        pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('file:///home/claude/work/index.html'); pg.evaluate("(s)=>{localStorage.clear();localStorage.setItem('marvel-ultimate-timeline-watched',s)}",json.dumps(state)); pg.reload(); pg.wait_for_timeout(900); pg.evaluate(START); pg.wait_for_timeout(150); return pg,errs
    def nxt(pg):
        t=pg.evaluate("()=>{const blk=document.getElementById('nextWatchBlock');const c=document.getElementById('nextWatchCard');return blk&&blk.style.display!=='none'?c.textContent:null}")
        m=re.search(r'N°(\d{3})',t or ''); return m.group(1) if m else None
    def picks(pg,n=30):
        o=set()
        for _ in range(n):
            t=pg.evaluate("()=>{document.getElementById('dashPickerRerollBtn').click();const r=document.getElementById('dashPickerResult');return r.hidden?'EMPTY':document.getElementById('dashPickerCard').textContent}")
            m=re.search(r'N°(\d{3})',t); o.add(m.group(1) if m else 'EMPTY')
        return o
    NA={'027','028','134','136','137','138','139'}
    base={e['id']:True for e in W if e['id'] not in NA}
    # A: Defenders senza JJ/LC visti
    st=dict(base); 
    for k in ('073','061','068'): st.pop(k)
    st2={k:v for k,v in st.items() if k not in ('079','080','087','082','122','128')}  # i seguiti non visti non interferiscono
    pg,e=page(st); n=nxt(pg); pk=picks(pg)
    ok('A: con 061/068 non visti, 073 è tra i suggeribili (prossimo=%s, picker=%s)'%(n,sorted(pk)),'073' in pk and not e)
    # B: Thunderbolts* senza FWS visto
    st=dict(base)
    for k in ('123','094'): st.pop(k)
    pg,e=page(st); n=nxt(pg); pk=picks(pg,20)
    ok('B: con 094 non visto, il prossimo è 123 (verde) e non 094 (prossimo=%s)'%n,n=='123' and not e)
    # C: 069 non visto continua a bloccare 123
    st=dict(base)
    for k in ('123','069'): st.pop(k)
    pg,e=page(st); n=nxt(pg); ok('C: 069 non visto: il prossimo passa da 069 (prossimo=%s)'%n,n=='069')
    # D: salvataggio intatto
    pg,e=page({'061':True}); ls=pg.evaluate("()=>localStorage.getItem('marvel-ultimate-timeline-watched')"); ok('D: stato salvato invariato',json.loads(ls)=={'061':True})
    # E: testo consigli
    pg,e=page({}); t=pg.evaluate("()=>[document.getElementById('item-073').textContent,document.getElementById('item-123').textContent]")
    ok('E: consigli presenti nelle schede',('Luke Cage S1 (N°068)' in t[0]) and ('Falcon and the Winter Soldier (N°094)' in t[1]))
print('ALL_PASS' if all(res) else 'FAILED')
