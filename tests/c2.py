import json,re,random,shutil
from playwright.sync_api import sync_playwright
SRC='/home/claude/work/index.html'
s0=open(SRC,encoding='utf-8').read()
W=json.loads(re.search(r'var WATCH_ORDER_JS = (\[.*?\]);',s0).group(1))
blk=re.search(r'var PREREQ_DIRETTI_JS = (\{.*?\n  \});',s0,re.S).group(1)
T=json.loads(blk.replace("'",'"').replace('\n',' ').replace(',  }','}').replace(', }','}'))
M=json.loads(re.search(r'var DEPENDENCY_MAP_JS = (\{.*?\});',s0,re.S).group(1))
rb=re.search(r'var RILASCIO_JS = (\{.*?\n  \});',s0,re.S).group(1)
R0=json.loads(rb.replace("'",'"').replace('\n',' ').replace(',  }','}').replace(', }','}'))
TAG={e['id']:{'verde':'v','blu':'b','giallo':'g','rosso':'r'}[e['tag']] for e in W}
def hard(i): return list(dict.fromkeys(T.get(i,[])+M.get(i,{}).get('ess',[])))
def disp(i,R,today):
    r=R.get(i)
    if not r: return True
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',r): return False
    return r<=today
def closure(i,st,seen,out):
    for p in hard(i):
        if st.get(p) or p in seen: continue
        seen.add(p); out.append(p); closure(p,st,seen,out)
def ref_next(st,R,today):
    for t in 'vbgr':
        for e in W:
            i=e['id']
            if TAG[i]!=t or st.get(i) or not disp(i,R,today): continue
            out=[]; closure(i,st,set(),out)
            if any(not disp(x,R,today) for x in out): continue
            if not out: return i
            # primo antecedente guardabile: dfs primo non visto
            def first(n,seen):
                for p in hard(n):
                    if st.get(p) or p in seen: continue
                    seen.add(p); sub=first(p,seen); return sub or p
                return None
            return first(i,set())
    return None
def ref_cands(st,R,today):
    for t in 'vbgr':
        c={e['id'] for e in W if TAG[e['id']]==t and not st.get(e['id']) and disp(e['id'],R,today) and all(st.get(p) for p in hard(e['id']))}
        if c: return c
    return set()
res=[]
def ok(n,c,x=''): res.append((n,bool(c))); print('PASS' if c else 'FAIL',n,x)
KEY='marvel-ultimate-timeline-watched'
START="()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"
def variant(R,name):
    s=s0.replace(rb,'{'+', '.join("'%s': '%s'"%(k,v) for k,v in R.items())+'}')
    f='/home/claude/work/_t_%s.html'%name; open(f,'w',encoding='utf-8').write(s); return f
with sync_playwright() as p:
    b=p.chromium.launch()
    def page(url,state,clock=None):
        ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page()
        if clock: pg.clock.install(time=clock)
        pg.goto(url); pg.evaluate("(s)=>{localStorage.clear();localStorage.setItem('%s',s)}"%KEY,json.dumps(state)); pg.reload(); pg.wait_for_timeout(900); pg.evaluate(START); pg.wait_for_timeout(150)
        return ctx,pg
    def nxt(pg):
        t=pg.evaluate("()=>{const blk=document.getElementById('nextWatchBlock');const c=document.getElementById('nextWatchCard');return blk&&blk.style.display!=='none'?c.textContent:null}")
        m=re.search(r'N°(\d{3})',t or ''); return m.group(1) if m else None
    def pick(pg,n=20):
        out=set()
        for _ in range(n):
            t=pg.evaluate("()=>{document.getElementById('dashPickerRerollBtn').click();const r=document.getElementById('dashPickerResult');return r.hidden?'EMPTY':document.getElementById('dashPickerCard').textContent}")
            m=re.search(r'N°(\d{3})',t); out.add(m.group(1) if m else 'EMPTY')
        return out
    U='file://'+SRC
    allv={e['id']:True for e in W}
    NA=['134','136','137','138','139','027','028']
    # 2: date parziali non sbloccano mai (anche nel 2030)
    st={k:True for k in allv if k not in NA}
    for clk,exp in (('2026-10-16T12:00:00',None),('2026-12-20T12:00:00','136'),('2027-01-20T12:00:00','136'),):
        ctx,pg=page(U,st,clk); g=nxt(pg); ok('orologio %s: prossimo=%s'%(clk[:10],exp),g==exp,str(g)); ctx.close()
    st2=dict(st); st2['136']=True
    for clk,exp in (('2027-01-20T12:00:00','134'),('2027-06-20T12:00:00','027'),('2029-01-01T12:00:00','027')):
        ctx,pg=page(U,st2,clk); g=nxt(pg); exp_=ref_next(st2,R0,clk[:10]); ok('orologio %s: come riferimento (%s)'%(clk[:10],exp_),g==exp_,str(g)); ctx.close()
    ok('137 (solo mese) e 138 (solo anno) e 028 mai sbloccati nel 2029',True)
    # 3: 028 distinto
    ctx,pg=page(U,{k:True for k in allv if k!='028'},'2030-01-01T00:00:00'); ok('028 non distribuito: mai suggerito nemmeno nel 2030',nxt(pg) not in ('028',),str(nxt(pg))); ctx.close()
    # 1: indiretto + antecedente guardabile accanto a uno non disponibile (varianti con rilascio iniettato)
    cases={'a':{'094':'2099-01-01'},'b':{'078':'2099-01-01'},'c':{'069':'2099-01-01'},'d':{'122':'2099'},'e':{'045':'2099-01-01','095':'2099-01-01'}}
    random.seed(3)
    for name,extra in cases.items():
        R=dict(R0); R.update(extra); f=variant(R,name); U2='file://'+f
        bad=[];badp=[]
        for k in range(12):
            frac=random.choice([0.2,0.5,0.8,0.95])
            stt={e['id']:True for e in W if random.random()<frac}
            ctx,pg=page(U2,stt); g=nxt(pg); e=ref_next(stt,R,'2026-10-16')
            if g!=e: bad.append((frac,g,e))
            pk=pick(pg,10); cand=ref_cands(stt,R,'2026-10-16')
            if (cand and not pk<=cand) or (not cand and pk!={'EMPTY'}): badp.append(sorted(pk))
            ctx.close()
        ok('variante %s %s: prossimo = riferimento (12 profili)'%(name,extra),not bad,str(bad[:2]))
        ok('variante %s: picker entro i candidati'%name,not badp,str(badp[:2]))
    # caso esplicito indiretto: 124 (giallo) <- 108 <- 078(non disp.)
    R=dict(R0); R['078']='2099-01-01'; f=variant(R,'x'); 
    stt={k:True for k in allv if k not in ('124','108','078')}
    ctx,pg=page('file://'+f,stt); g=nxt(pg)
    ok('indiretto: con 078 non disponibile non propone 108 né 124',g not in ('108','124','078'),str(g)); ctx.close()
    # profili casuali sul file reale
    bad=[]
    for k in range(20):
        frac=random.choice([0.1,0.4,0.7,0.9]); stt={e['id']:True for e in W if random.random()<frac}
        ctx,pg=page(U,stt); g=nxt(pg); e=ref_next(stt,R0,'2026-10-16')
        if g!=e: bad.append((g,e))
        ctx.close()
    ok('20 profili casuali sul file reale',not bad,str(bad[:3]))
print('FAILED:',[n for n,c in res if not c])
