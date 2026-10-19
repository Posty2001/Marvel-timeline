import json,re,random
from playwright.sync_api import sync_playwright
s=open('/home/claude/work/index.html',encoding='utf-8').read()
W=json.loads(re.search(r'var WATCH_ORDER_JS = (\[.*?\]);',s).group(1))
blk=re.search(r'var PREREQ_DIRETTI_JS = (\{.*?\n  \});',s,re.S).group(1)
T=json.loads(blk.replace("'",'"').replace('\n',' ').replace(',  }','}').replace(', }','}'))
M=json.loads(re.search(r'var DEPENDENCY_MAP_JS = (\{.*?\});',s,re.S).group(1))
R={"027":"2027-06-18","028":"mai","134":"2027-01-13","136":"2026-12-18","137":"2027-03-31","138":"2027-12-31","139":"2027-12-17"}
TAG={e['id']:{'verde':'v','blu':'b','giallo':'g','rosso':'r'}[e['tag']] for e in W}
def hard(i): return list(dict.fromkeys(T.get(i,[])+M.get(i,{}).get('ess',[])))
def disp(i,today):
    r=R.get(i); return True if not r else (False if r=='mai' else r<=today)
def res(i,st,vis):
    for p in hard(i):
        if st.get(p) or p in vis: continue
        vis.add(p)
        if not disp(p,today_g): return ('B',None)
        sub=res(p,st,vis)
        if sub[0]=='B': return sub
        return ('O',sub[1] or p)
    return ('O',None)
today_g='2026-10-16'
V2I={v:k for k,v in re.findall(r'id="item-(\d+)"(?:(?!</li>).)*?<span class="rec">N&deg;(\d+)</span>',s,re.S)}
def vid(x): return V2I.get(x,x)
def ref_next(st,today):
    global today_g; today_g=today
    for t in 'vbgr':
        for e in W:
            i=e['id']
            if TAG[i]!=t or st.get(i) or not disp(i,today): continue
            r=res(i,st,set())
            if r[0]=='B': continue
            return r[1] or i
    return None
def ref_cands(st,today):
    global today_g; today_g=today
    for t in 'vbgr':
        c=[e['id'] for e in W if TAG[e['id']]==t and not st.get(e['id']) and disp(e['id'],today) and all(st.get(p) for p in hard(e['id']))]
        if c: return set(c)
    return set()
res_list=[]
def ok(n,c,x=''): res_list.append((n,bool(c))); print('PASS' if c else 'FAIL',n,x)
KEY='marvel-ultimate-timeline-watched'
START="()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(state,clock=None):
        ctx=b.new_context(viewport={'width':390,'height':844})
        pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        if clock: pg.clock.install(time=clock)
        pg.goto('file:///home/claude/work/index.html'); pg.evaluate("(s)=>{localStorage.clear();localStorage.setItem('%s',s)}"%KEY,json.dumps(state)); pg.reload(); pg.wait_for_timeout(1200); pg.evaluate(START); pg.wait_for_timeout(200)
        return ctx,pg,errs
    def nxt(pg):
        t=pg.evaluate("()=>{const b=document.getElementById('dashLastNext');const c=document.getElementById('nextWatchCard');const blk=document.getElementById('nextWatchBlock');return blk&&blk.style.display!=='none'?c.textContent:null}")
        m=re.search(r'N°(\d{3})',t or ''); return vid(m.group(1)) if m else None
    def pick(pg,n=60):
        out=set()
        for _ in range(n):
            t=pg.evaluate("()=>{const f=window.__x;document.getElementById('dashPickerRerollBtn').click();const r=document.getElementById('dashPickerResult');return r.hidden?'EMPTY':document.getElementById('dashPickerCard').textContent}")
            m=re.search(r'N°(\d{3})',t); out.add(vid(m.group(1)) if m else 'EMPTY')
        return out
    ctx,pg,errs=page({})
    ok('profilo vuoto: prossimo = 001 Spider-Man',nxt(pg)=='001',nxt(pg))
    pk=pick(pg); ok('profilo vuoto: picker solo titoli sbloccati',pk<=ref_cands({}, '2026-10-16'),str(sorted(pk)))
    ok('profilo vuoto: mai 002/023',not ({'002','023'}&pk))
    ctx.close()
    # casi mirati
    allv={e['id']:True for e in W}
    st=dict(allv); st['121']=False; st['094']=False
    for i in ('134','136','137','138','139','027','028'): st[i]=False
    ctx,pg,_=page({k:v for k,v in st.items() if v}); ok('121 verde bloccato da 094: suggerisce 094',nxt(pg)=='094',nxt(pg)); ctx.close()
    st=dict(allv)
    for i in ('134','136','137','138','139','027','028'): st[i]=False
    ctx,pg,_=page({k:v for k,v in st.items() if v}); ok('restano solo non usciti: nessun suggerimento',nxt(pg) is None,str(nxt(pg))); ctx.close()
    ctx,pg,_=page({k:v for k,v in st.items() if v},clock='2026-12-20T12:00:00'); ok('dopo il 18/12/2026 Doomsday si abilita',nxt(pg)=='136',str(nxt(pg))); ctx.close()
    st2=dict(st); st2['125']=False
    ctx,pg,_=page({k:v for k,v in st2.items() if v},clock='2026-12-20T12:00:00'); ok('Doomsday con First Steps non visto: suggerisce 125',nxt(pg)=='125',str(nxt(pg))); ctx.close()
    # casuali vs riferimento
    random.seed(7); bad=[]; badp=[]
    for k in range(25):
        frac=random.choice([0.1,0.3,0.5,0.7,0.9])
        stt={e['id']:True for e in W if random.random()<frac}
        ctx,pg,errs=page(stt)
        got=nxt(pg); exp=ref_next(stt,'2026-10-16')
        if got!=exp: bad.append((frac,got,exp))
        pk=pick(pg,25)
        cand=ref_cands(stt,'2026-10-16')
        if cand:
            if not pk<=cand: badp.append((sorted(pk-cand)))
        else:
            if pk!={'EMPTY'}: badp.append(('atteso vuoto',sorted(pk)))
        ctx.close()
    ok('25 profili casuali: prossimo titolo = riferimento indipendente',not bad,str(bad[:3]))
    ok('25 profili casuali: picker mai fuori dai candidati sbloccati',not badp,str(badp[:3]))
print('FAILED:',[n for n,c in res_list if not c])
