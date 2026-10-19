from leg_shot import *
import json,hashlib,re,subprocess
F=[0]
def ok(n,c,x=''):
    print(('PASS ' if c else 'FAIL ')+n,x); F[0]+= 0 if c else 1
OLD=open('/tmp/claude-0/t/index.3c.frozen.html',encoding='utf-8').read()  # baseline 3C congelata (outputs/index.html ora e' la build X-Men)
NEW=open('/home/claude/work/index.html',encoding='utf-8').read()
def jd(s,i):
    m=re.search(r'<script[^>]*id="%s"[^>]*>(.*?)</script>'%i,s,re.S); return m.group(1) if m else None
# --- 1. integrita' dei dati sorgente (byte per byte) ---
# Aggiornato per il nuovo ordine di visione X-Men (ottobre 2026): mvMapData/atlasData/altTimelineData cambiano SOLO per
# l'ordine dei 13 titoli Fox e per i N° visibili; si confronta quindi il contenuto canonico (liste ordinate, N° normalizzati).
# Il controllo dell'ordine stesso e' in xm_test.py. relationshipGraphData resta confrontato byte per byte.
def _canon(x):
    if isinstance(x,dict): return {k:_canon(v) for k,v in x.items()}
    if isinstance(x,list): return sorted((_canon(v) for v in x),key=lambda v:json.dumps(v,sort_keys=True))
    if isinstance(x,str): return re.sub(r'N(?:\u00b0|&deg;)\d{3}','N#',x.replace('N\u00b0','N\u00b0'))
    return x
for i in ['mvMapData','atlasData','relationshipGraphData','altTimelineData']:
    a,b=jd(OLD,i),jd(NEW,i)
    if i=='relationshipGraphData': ok('sorgente invariata '+i,a is not None and a==b)
    else:
        try: ok('sorgente invariata (contenuto canonico, ordine X-Men escluso) '+i,_canon(json.loads(a))==_canon(json.loads(b)))
        except Exception as e: ok('sorgente invariata '+i,False,e)
ok('mvNavigate occorrenze invariate',OLD.count('mvNavigate')==NEW.count('mvNavigate'),(OLD.count('mvNavigate'),NEW.count('mvNavigate')))
ok('card-wrap invariate (elementi <li class="card-wrap">)',OLD.count('class="card-wrap')==NEW.count('class="card-wrap'),(OLD.count('class="card-wrap'),NEW.count('class="card-wrap')))
for pat in ['id="multiverseGraphToggle"','id="universeTimelineToggle"','id="altTimelineToggle"','data-items=']:
    ok('overlay legacy presente '+pat,OLD.count(pat)==NEW.count(pat),(OLD.count(pat),NEW.count(pat)))
gm=lambda s:s[s.index('<div class="multiverse-graph-overlay">'):s.index('<div class="universe-timeline-overlay">')]
ok('grafo storico HTML invariato',gm(OLD)==gm(NEW))
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    reqs=[]; pg.on('request',lambda r: reqs.append(r.url) if 'uni_' in r.url and r.url.endswith('.webp') else None)
    ids=pg.evaluate("()=>tvaUniverse.ids()")
    ok('27 universi nel modello',len(ids)==27 and len(set(ids))==27)
    A=pg.evaluate("()=>tvaUniverse.audit()")
    ok('audit: 13 archi del grafo tutti mappati',A['archiGrafoStorico']==13 and A['archiMappati']==13,A)
    ok('audit: 12 nodi mappati, 4 speciali',A['nodiMappati']==12 and A['speciali']==4)
    L={ (x['a'],x['b']):x['stato'] for x in pg.evaluate("()=>tvaUniverse.links()")}
    byp=lambda a,b2:[v for (x,y),v in L.items() if (a in x or a in y) and (b2 in x or b2 in y)]
    ok('stati: etichetta Documentato nella guida',pg.evaluate("()=>tvaUniverse.stati.confermato")=='Documentato nella guida' and not pg.evaluate("()=>document.body.innerHTML.includes('>Confermato<')"))
    ok('MCU-Fox confermato',byp('199999','10005')==['confermato'])
    ok('MCU-TVA confermato',byp('199999','tva-fuori')==['confermato'])
    ok('MCU-Raimi/Garfield confermati',byp('199999','96283')==['confermato'] and byp('199999','120703')==['confermato'])
    ok('MCU-SSU legacy (cameo non riscontrato)',byp('199999','sony-s-s')==['legacy'])
    ok('MCU-838 da verificare (N°102 assegnato al solo MCU)',byp('199999','earth-83')==['verificare'])
    ok('MCU-828 da verificare (previsto vs crossover Atlante)',byp('199999','earth-82')==['verificare'])
    ok('MCU-What If da verificare (solo Atlante)',byp('199999','rami-di-')==['verificare'])
    ok('nessuna relazione verso/da entita\' speciali tra i 27',all(u in ids for x in pg.evaluate("()=>tvaUniverse.links()") for u in (x['a'],x['b'])))
    sp=pg.evaluate("()=>tvaUniverse.special()")
    ok('4 speciali, nessuno tra i 27',{s['id'] for s in sp}=={'void','battleworld','legacy','animazione'} and not any(s['id'] in ids or ('uni-'+s['id']) in ids for s in sp))
    ok('Battleworld previsto -> da verificare',[r['stato'] for s in sp if s['id']=='battleworld' for r in s['relazioni']]==['verificare'])
    ok('Void: tutte le relazioni legacy',all(r['stato']=='legacy' for s in sp if s['id']=='void' for r in s['relazioni']) and len([1 for s in sp if s['id']=='void' for r in s['relazioni']])==3)
    ok('Legacy isolati: 4 membri espliciti + Hulk 2003 incerto',[(len(s['membri']),s['membriIncerti']) for s in sp if s['id']=='legacy']==[(4,['uni-hulk-2003-verse'])] and 'uni-hulk-2003-verse' not in [m for s in sp if s['id']=='legacy' for m in s['membri']])
    ok('mvMapData/atlas non mutati a runtime',pg.evaluate("()=>JSON.parse(document.getElementById('mvMapData').textContent).universi && Object.keys(JSON.parse(document.getElementById('mvMapData').textContent).universi).length")==27)
    # --- 2. i 27 dossier ---
    bad=[]; secEmpty=[]; mism=[]
    for u in ids:
        pg.evaluate("(u)=>tvaAtlas2.openUni(u)",u); pg.wait_for_timeout(120)
        r=pg.evaluate("""(u)=>{const R=document.querySelector('#atlas2 .a2-scroll');const h2=R.querySelector('.ud-hero h2');
          const secs=[...R.querySelectorAll('section.a2-sec')];
          const empt=secs.filter(s=>[...s.children].filter(c=>c.tagName!=='H3').length===0).map(s=>s.querySelector('h3').textContent);
          const ix=[...R.querySelectorAll('.ud-ix')].map(b=>b.dataset.ix), mod=[...R.querySelectorAll('[data-mod]')].map(s=>s.dataset.mod);
          const m=tvaUniverse.get(u);
          const lk=[...R.querySelectorAll('.ud-lk')].length, ref=m.collegamenti.length+m.speciali.filter(x=>x.stato).length;
          return {h:h2&&h2.textContent,empt,ix,mod,lk,ref,w:R.scrollWidth-R.clientWidth,nT:m.titoli.length,rows:R.querySelectorAll('.a2-sec-prim .a2-row,.a2-sec-cro .a2-row,.a2-sec-var .a2-row').length,cn:tvaIdx.titoliDi(u).length+m.varianti.length}}""",u)
        nm=pg.evaluate("(u)=>JSON.parse(document.getElementById('mvMapData').textContent).universi[u].nome",u)
        if r['h']!=nm: bad.append((u,'titolo',r['h']))
        if r['empt']: secEmpty.append((u,r['empt']))
        if r['ix']!=r['mod']: mism.append((u,r['ix'],r['mod']))
        if r['lk']!=r['ref']: bad.append((u,'collegamenti resi',r['lk'],r['ref']))
        if r['w']>1: bad.append((u,'overflow',r['w']))
        if r['rows']!=r['cn']: bad.append((u,'righe titoli',r['rows'],r['cn']))
    ok('27 dossier: titolo = nome, collegamenti resi = modello, righe titoli = dati, no overflow',not bad,bad[:4])
    ok('nessuna sezione vuota nei 27 dossier',not secEmpty,secEmpty[:3])
    ok('indice moduli = sezioni presenti',not mism,mism[:3])
    ok('nessun errore JS',not errs,errs)
    # asset opzionali: al massimo una richiesta per asset mancante (cache negativa)
    rq=[u.split('/')[-1] for u in reqs]; from collections import Counter
    ok('asset famiglia mancanti: richiesta singola per file',max(Counter(rq).values())==1 if rq else True,Counter(rq))
    lost=pg.evaluate("()=>{const out=[];for(const u of tvaUniverse.ids()){const sh=new Set();tvaIdx.titoliDi(u).forEach(e=>e.unis.forEach(o=>{if(o!==u)sh.add(o)}));const con=new Set(tvaUniverse.get(u).collegamenti.map(c=>c.con));const miss=[...sh].filter(o=>!con.has(o));if(miss.length)out.push([u,miss]);}return out}")
    ok('nessun universo in comune nei titoli perso dai collegamenti',not lost,lost)
    # --- 3. navigazione ---
    def st(): return pg.evaluate("()=>{const s=tvaAtlas2.getState();return [s.screen,s.uid]}")
    mcu='uni-earth-199999-mcu'
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",mcu); pg.wait_for_timeout(400)
    pg.evaluate("()=>{const b=document.querySelector('.ud-lk .ud-lk-h .a2-chip');b.scrollIntoView({block:'center'})}"); pg.wait_for_timeout(200)
    tgt=pg.evaluate("()=>document.querySelector('.ud-lk .ud-lk-h .a2-chip').dataset.go")
    pg.click('.ud-lk .ud-lk-h .a2-chip'); pg.wait_for_timeout(700)
    ok('collegamento -> dossier dell\'altro universo',st()==['uni',tgt.split(':')[1]],st())
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(600)
    ok('indietro -> dossier MCU',st()==['uni',mcu],st())
    pg.evaluate("()=>{const b=document.querySelector('.ud-lk .ud-ref');b.scrollIntoView({block:'center'})}"); pg.wait_for_timeout(200)
    pg.click('.ud-lk .ud-ref'); pg.wait_for_timeout(900)
    ok('titolo di riferimento -> scheda titolo (esce dall\'Atlante)',pg.evaluate("()=>!document.getElementById('atlas2Toggle').checked"),st())
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(900)
    ok('indietro dal titolo -> dossier MCU',st()==['uni',mcu],st())
    pg.click('.ud-ix[data-ix=personaggi]'); pg.wait_for_timeout(300)
    y=pg.evaluate("()=>document.querySelector('#atlas2 .a2-scroll').scrollTop"); ok('indice: scorre al modulo',y>500,y)
    pg.evaluate("()=>{const c=document.querySelector('#ud-personaggi .a2-chip[data-go^=\"char:\"]');c.scrollIntoView({block:'center'})}"); pg.wait_for_timeout(200)
    pg.click('#ud-personaggi .a2-chip[data-go^="char:"]'); pg.wait_for_timeout(900)
    ok('personaggio -> scheda personaggio',st()[0]!='uni',st())
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(900)
    ok('indietro dal personaggio -> dossier MCU',st()==['uni',mcu],st())
    # tre ordini
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",mcu); pg.wait_for_timeout(300)
    for modo,lbl in [('uscita','Per data di uscita'),('ambientazione','Per ambientazione')]:
        pg.click(f'.a2-sec-prim .a2-f:has-text("{lbl}")'); pg.wait_for_timeout(300)
        ord_=pg.evaluate("""()=>[...document.querySelectorAll('.a2-sec-prim .a2-row')].map(b=>b.dataset.go.slice(5))""")
        okord=pg.evaluate("(l)=>{const m=tvaUniverse; return l.map(i=>i.replace('item-',''))}",ord_)
        if modo=='uscita':
            d=[pg.evaluate("(n)=>(tvaUniverse.uscita(n)||{}).data||'9999'",n) for n in okord]; ok('ordine per uscita non decrescente',d==sorted(d))
        else:
            ys=[pg.evaluate("(n)=>tvaUniverse.annoAmbientazione(tvaUniverse.ambientazione(n)).y",n) for n in okord]
            dated=[y for y in ys if y is not None]; first_none=next((i for i,y in enumerate(ys) if y is None),len(ys))
            ok('ordine per ambientazione non decrescente, non datati in coda',dated==sorted(dated) and all(y is None for y in ys[first_none:]),(len(dated),len(ys)))
        ok('stessi titoli in ogni ordine',sorted(okord)==sorted(pg.evaluate("(u)=>tvaIdx.titoliDi(u).filter(e=>tvaIdx.ruoloDi(e)==='appartenenza').map(e=>e.num)",mcu)))
    pg.click('.a2-sec-prim .a2-f:has-text("Ordine della guida")'); pg.wait_for_timeout(200)
    # filtro timeline + cronologie
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",'uni-earth-10005-fox-verse'); pg.wait_for_timeout(300)
    pg.click('.ud-acts .a2-ghost'); pg.wait_for_timeout(700); ok('Cronologie raggiungibili dal dossier',st()[0]=='cronologie',st())
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(700); ok('indietro -> dossier',st()==['uni','uni-earth-10005-fox-verse'],st())
    pg.click('.ud-acts .a2-primary'); pg.wait_for_timeout(1200)
    ok('Timeline filtrata aperta (fuori da Atlante)',pg.evaluate("()=>!document.getElementById('atlas2Toggle').checked"))
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(1000); ok('indietro dalla Timeline -> dossier',st()==['uni','uni-earth-10005-fox-verse'],st())
    # grafo classico dal dossier
    pg.click('#ud-collegamenti .a2-ghost'); pg.wait_for_timeout(900)
    ok('grafo classico apribile',pg.evaluate("()=>document.getElementById('multiverseGraphToggle').checked"))
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(900)
    ok('indietro dal grafo -> dossier',st()==['uni','uni-earth-10005-fox-verse'],st())
    # elementi speciali nel dossier MCU
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",mcu); pg.wait_for_timeout(300)
    txt=pg.evaluate("()=>document.getElementById('ud-collegamenti').innerText")
    ok('MCU: Battleworld e Void come speciali, non come universi',('Battleworld' in txt) and ('Void' in txt) and 'Realtà speciale' in txt and 'Luogo' in txt)
    ok('MCU: nessun "Confermato" tra i dubbi',pg.evaluate("()=>[...document.querySelectorAll('.ud-lk-ok')].every(c=>c.innerText.includes('Documentato nella guida'))") and pg.evaluate("()=>document.querySelectorAll('.ud-lk-vf .ud-st-ok').length")==0)
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",'uni-blade-verse'); pg.wait_for_timeout(300)
    t2=pg.evaluate("()=>document.getElementById('ud-famiglia').innerText"); ok('Blade: elencato esplicitamente',('esplicitamente' in t2) and ('ambigua' not in t2)); ok('Blade: appartiene a «Legacy isolati» (raggruppamento) senza collegamenti inventati',('Legacy isolati' in t2) and pg.evaluate("()=>!document.getElementById('ud-collegamenti')"),t2[:120])
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",'uni-hulk-2003-verse'); pg.wait_for_timeout(300)
    th=pg.evaluate("()=>document.getElementById('ud-famiglia').innerText"); ok('Hulk 2003: appartenenza ambigua dichiarata, universo intatto',('ambigua' in th) and 'uni-hulk-2003-verse' in pg.evaluate("()=>tvaUniverse.ids()"))
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",'uni-earth-838'); pg.wait_for_timeout(300)
    t3=pg.evaluate("()=>document.querySelector('#atlas2 .a2-scroll').textContent"); ok('838: «Non documentato» elenca titoli ed eventi assenti',('Non documentato' in t3) and 'film e serie' in t3)
    # --- 4. overlay legacy e progressi ---
    pg.evaluate("()=>{marvelChiudiOverlay()}"); pg.wait_for_timeout(300)
    for t in ['multiverseGraphToggle','universeTimelineToggle','altTimelineToggle']:
        pg.evaluate("(t)=>{marvelChiudiOverlay();const c=document.getElementById(t);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",t); pg.wait_for_timeout(700)
        ok('overlay legacy '+t,pg.evaluate("(t)=>document.getElementById(t).checked&&document.querySelector('.'+({multiverseGraphToggle:'multiverse-graph-overlay',universeTimelineToggle:'universe-timeline-overlay',altTimelineToggle:'alt-timeline-overlay'})[t]).getClientRects().length>0",t))
    ok('nessun errore JS finale',not errs,errs)
    # --- 5. reduced motion + larghezze ---
    for w in (320,360,390,430):
        c2=b.new_context(viewport={'width':w,'height':844},is_mobile=True,has_touch=True,reduced_motion='reduce',service_workers='block'); q=c2.new_page(); e2=[]; q.on('pageerror',lambda e:e2.append(str(e)))
        q.goto(U); q.wait_for_timeout(1000); q.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); q.wait_for_timeout(400); q.click('#appTabAtlante'); q.wait_for_timeout(500)
        wo=[]
        for u in ids:
            q.evaluate("(u)=>tvaAtlas2.openUni(u)",u); q.wait_for_timeout(60)
            v=q.evaluate("()=>{const R=document.querySelector('#atlas2 .a2-scroll');return [R.scrollWidth-R.clientWidth, document.documentElement.scrollWidth-innerWidth]}")
            if v[0]>1 or v[1]>1: wo.append((u,v))
        ok(f'{w}px: nessun overflow orizzontale nei 27 dossier',not wo and not e2,wo[:2]+e2[:1]); c2.close()
    print('FAILS',F[0]); b.close()
