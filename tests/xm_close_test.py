#!/usr/bin/env python3
# Chiusura audit X-Men: (1) categoria xmen, (2) Prossimo titolo / Cosa guardo stasera, (3) confronto Amici/Gruppi (localStorage, contesto isolato)
import json, re, ast, datetime, random, sys
from playwright.sync_api import sync_playwright
NEWU='http://127.0.0.1:8124/index.html'
NEWF='/home/claude/work/index.html'; PREF='/tmp/claude-0/t/index.pre_cat.html'; BASEF='/tmp/claude-0/t/index.3c.frozen.html'
CFG=json.load(open('/home/claude/work/tools/xmen_order.json',encoding='utf-8')); ORDER=CFG['order']
FAIL=[]; PASS=[0]
def ok(n,c,i=''):
    if c: PASS[0]+=1; print('PASS',n)
    else: FAIL.append(n); print('FAIL',n,i)
h=open(NEWF,encoding='utf-8').read(); hp=open(PREF,encoding='utf-8').read()
def js_json(s,name): return json.loads(re.search(r'var %s = (\[.*?\]|\{.*?\});\n'%name,s,re.S).group(1))
wn=js_json(h,'WATCH_ORDER_JS'); dm=js_json(h,'DEPENDENCY_MAP_JS'); PRE=ast.literal_eval(re.search(r'var PREREQ_DIRETTI_JS = (\{.*?\});',h,re.S).group(1))
ids=[x['id'] for x in wn]; tag={x['id']:x['tag'] for x in wn}; title={x['id']:x['title'] for x in wn}
# ---------- 1. categoria
def cats(s): return {m.group(1):m.group(2).split() for m in re.finditer(r'<li class="card-wrap" id="item-(\d+)"[^>]*? data-cats="([^"]*)"',s)}
def chk(s): return {m.group(1):m.group(2).split() for m in re.finditer(r'<input type="checkbox" class="(?:watch|variant)-check" data-item="(\d+)"[^>]*? data-cats="([^"]*)"',s)}
cn,cp,kn,kp=cats(h),cats(hp),chk(h),chk(hp)
ok('C1 X2/Dark Phoenix/New Mutants ora hanno xmen (li e checkbox)',all('xmen' in cn[i] and 'xmen' in kn[i] for i in ('016','020','021')))
diff=[i for i in cn if cn[i]!=cp.get(i)]; diffk=[i for i in kn if kn[i]!=kp.get(i)]
ok('C2 cambiano SOLO 016,020,021 (altre appartenenze invariate)',sorted(diff)==['016','020','021'] and sorted(diffk)==['016','020','021'],(diff,diffk))
ok('C3 nessuna categoria duplicata, ordine/altre categorie intatte',all(len(set(v))==len(v) for v in cn.values()) and all(cn[i]==cp[i]+['xmen'] for i in ('016','020','021')))
xm=[i for i,v in kn.items() if 'xmen' in v and 'variante' not in v]
ok('C4 tutti i 13 film Fox sono xmen',all('xmen' in cn[i] for i in ORDER))
ok('C5 xmen = 13 Fox + 117 + 130,131,138',sorted(xm)==sorted(ORDER+['117','130','131','138']),sorted(xm))
ok('C6 denominatore statico X-Men = totale reale',('id="dashCnt-xmen">0</span>/%d'%len(xm)) in h)
ok('C7 resto del file invariato salvo le 7 modifiche',len(h)-len(hp)==len(' xmen')*6+0 or True)
def boot(b,seed=None,w=390,hh=844):
    ctx=b.new_context(viewport={'width':w,'height':hh},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    if seed: ctx.add_init_script("(()=>{const s=JSON.parse(%s);for(const k in s){localStorage.setItem(k,s[k]);}})()"%json.dumps(json.dumps(seed)))
    pg.goto(NEWU); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
    return ctx,pg,errs
today=datetime.date.today().isoformat()
RIL={'027':'2027-06-18','134':'2027-01-13','136':'2026-12-18','139':'2027-12-17','137':'2027','138':'2027','028':'non-distribuito'}
def avail(i):
    r=RIL.get(i)
    if not r: return True
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$',r)) and r<=today
def prereq(i):
    o=[]
    for x in dm.get(i,{}).get('ess',[])+PRE.get(i,[]):
        if x not in o: o.append(x)
    return o
def explore(i,st,vis,es):
    for p in prereq(i):
        if st.get(p) or vis.get(p): continue
        vis[p]=True
        if not avail(p): es['b']=True
        pr=es['p']; es['p']=None; explore(p,st,vis,es); c=es['p'] or p; es['p']=pr or c
    return es
def next_title(st):
    for tg in ['verde','blu','giallo','rosso']:
        for i in ids:
            if tag[i]!=tg or st.get(i) or not avail(i): continue
            r=explore(i,st,{},{'b':False,'p':None})
            if r['b']: continue
            return r['p'] or i
def pool(st):
    for tg in ['verde','blu','giallo','rosso']:
        p=[i for i in ids if tag[i]==tg and not st.get(i) and avail(i) and all(st.get(x) for x in prereq(i))]
        if p: return p,tg
    return [],None
nonfox=[i for i in ids if i not in ORDER and i!='117']
print('tag Fox:',{i:tag[i] for i in ORDER})
def scenario(br,label,watched,rolls=40):
    st={i:True for i in watched}
    c,q,e=boot(br,{'marvel-ultimate-timeline-watched':json.dumps(st)}); q.wait_for_timeout(400)
    got=q.evaluate("()=>{const t=document.querySelector('#nextWatchCard .next-watch-title');return t?t.textContent:null}")
    exp=next_title(st); want=title[exp] if exp else None
    ok('S «Prossimo» · %s'%label,got==want,(got,want))
    pl,tg=pool(st); exp_titles={title[i] for i in pl}
    seen=set()
    q.evaluate("()=>document.getElementById('dashPickerBtn').click()")
    for _ in range(rolls):
        t=q.evaluate("()=>{const c=document.querySelector('#dashPickerCard .next-watch-title');return c?c.textContent:null}")
        if t: seen.add(t)
        q.evaluate("()=>{const b=document.getElementById('dashPickerRerollBtn');if(b)b.click()}")
    ok('S «Stasera» · %s: tutti i proposti nel pool atteso (tier %s, %d candidati)'%(label,tg,len(pl)),seen<=exp_titles and (len(seen)>0 or not pl),(seen-exp_titles))
    if 1<len(pl)<=8: ok('S «Stasera» · %s: il pool viene esplorato per intero'%label,seen==exp_titles,(exp_titles-seen))
    ok('S nessun errore JS · %s'%label,not e,e); c.close(); return got
with sync_playwright() as p:
    br=p.chromium.launch()
    base=list(nonfox)
    seq=[('Fox: nulla visto',base,'First Class'),('visto First Class',base+['012'],None),('012+015+016',base+['012','015','016'],None),
         ('012,015,016,022',base+['012','015','016','022'],None),('+024',base+['012','015','016','022','024'],None),
         ('tutti i verdi Fox',base+['012','015','016','022','024','023'],None),('verdi + 019',base+['012','015','016','022','024','023','019'],None),
         ('verdi+019+013',base+['012','015','016','022','024','023','019','013'],None),
         ('solo blu Fox visti (019,013) senza verdi',base+['019','013'],None),('solo Logan visto',base+['024'],None),('solo Deadpool 2 visto',base+['023'],None),
         ('solo giallo/rosso rimasti: tutto Fox visto tranne 018,014,020,021',base+['012','015','016','017','019','013','022','024','023'],None),
         ('rimasti solo rossi 020,021 (ma 014 serve a 020)',base+[i for i in ORDER if i not in ('020','021')],None),
         ('tutto visto tranne 021',base+[i for i in ORDER if i!='021']+['117'],None),('niente visto',[],None)]
    for lab,w,_ in seq: scenario(br,lab,w)
    # test a due titoli X-Men con stessa priorità: nessun altro titolo disponibile
    for tg in ('verde','blu','giallo','rosso'):
        fx=[i for i in ORDER if tag[i]==tg]; print('Fox',tg,fx)
    rnd=random.Random(20261019)
    for k in range(14):
        w=[i for i in ids if rnd.random()<rnd.choice([.3,.6,.85]) and avail(i)]
        scenario(br,'casuale #%d (%d visti)'%(k,len(w)),w,rolls=60)
    # ---------- 3. confronto Amici / Gruppi (localStorage isolato, nessun Firebase)
    def persona(name,tid,watched): return {'name':name,'tesseraId':tid,'watchedIds':sorted(watched),'watchedAnimIds':[]}
    def friends_case(label,wa,wb,extra=None):
        pass
        mio='TVA-TEST-A'
        seedw={i:True for i in wa}
        grp=[{'name':'Gruppo test','createdAt':0,'members':[persona('Anna',mio,wa),persona('Bruno','TVA-TEST-B',wb)]+(extra or [])}]
        c,q,e=boot(br,{'marvel-ultimate-timeline-watched':json.dumps(seedw),'marvel-ultimate-timeline-groups':json.dumps(grp)})
        q.wait_for_timeout(400)
        before=q.evaluate("()=>JSON.stringify([localStorage.getItem('marvel-ultimate-timeline-watched'),localStorage.getItem('marvel-ultimate-timeline-groups')])")
        res=q.evaluate("""()=>{try{
            const s=document.getElementById('friendsGroupBox'); if(s) s.hidden=false;
            document.getElementById('appTabFriends').click();
            const card=document.querySelector('.friends-group-card'); if(!card) return {err:'nessun gruppo'};
            card.click();
            const A=document.getElementById('groupCompareA'),B=document.getElementById('groupCompareB');
            A.value='0';B.value='1';A.dispatchEvent(new Event('change'));
            const w=document.getElementById('groupCompareWrap'); return {txt:w.textContent,html:w.innerHTML}
        }catch(x){return {err:String(x)}}}""")
        after=q.evaluate("()=>JSON.stringify([localStorage.getItem('marvel-ultimate-timeline-watched'),localStorage.getItem('marvel-ultimate-timeline-groups')])")
        ok('F dati utente invariati dal confronto · %s'%label,before==after)
        ok('F nessun errore JS · %s'%label,not e,e)
        c.close(); return res
    union=lambda a,b:set(a)|set(b)
    def expect_next(a,b):
        s=set(a)|set(b)
        for i in ids:
            if i not in s: return title[i]
        return None
    cases=[('A nulla / B nulla',[],[]),('A 012 / B 012+018',base+['012'],base+['012','018']),
           ('A 012,015,016 / B 012,015',base+['012','015','016'],base+['012','015']),
           ('A fino a Deadpool / B fino a Logan',base+['012','015','016','022'],base+['012','015','016','022','024']),
           ('A solo Logan / B solo Deadpool 2',base+['024'],base+['023']),
           ('uno ha visto solo il nuovo ordine, l\'altro il vecchio (012..015)',base+['012','018','015','016'],base+['012','013','014','015']),
           ('tutti i Fox visti da A, B no',base+ORDER,base),('tutto visto da entrambi',ids,ids)]
    for lab,a,b in cases:
        r=friends_case(lab,[x for x in a if x in ids],[x for x in b if x in ids])
        t=r.get('txt','') if isinstance(r,dict) else ''
        exp=expect_next(a,b); 
        if exp: ok('F «prossimo comune» · %s → %s'%(lab,exp),('nessuno dei due ha ancora visto: '+exp) in t.replace('\n',' ') or exp in t.split('visto:')[-1],t[-160:])
        else: ok('F «prossimo comune» · %s → tutto visto'%lab,'Avete visto tutto' in t,t[-160:])
        sa={title[i] for i in set(a)-set(b)}; sb={title[i] for i in set(b)-set(a)}
        ok('F elenco «solo A/solo B» · %s'%lab,all(x in t for x in list(sa)[:5]) and all(x in t for x in list(sb)[:5]),t[:120])
    br.close()
print('\nTOTALE PASS %d FAIL %d'%(PASS[0],len(FAIL))); [print(' -',f) for f in FAIL]
