from playwright.sync_api import sync_playwright
import json,datetime
R=[]
def ck(n,c,d=''): R.append(c); print(('PASS ' if c else 'FAIL ')+n+(' '+str(d)[:260] if not c else ''))
IMG=open('/home/claude/work/assets/images/tva/cronologie.webp','rb').read()
U='http://127.0.0.1:8124/index.html'
def ctx(b,w=390,pre=None,tmdb='ok',date=None):
    cx=b.new_context(viewport={'width':w,'height':844},is_mobile=True,has_touch=True,service_workers='block')
    if date: cx.add_init_script("(()=>{const R=Date,off=%d-R.now();class D extends R{constructor(...a){a.length?super(...a):super(R.now()+off)} static now(){return R.now()+off}};window.Date=D})()"%int(date.timestamp()*1000))
    if pre: cx.add_init_script("(()=>{if(!sessionStorage.getItem('m34seed')){sessionStorage.setItem('m34seed','1');const o=%s;for(const k in o)localStorage.setItem(k,o[k]);}})()"%json.dumps({k:(v if isinstance(v,str) else json.dumps(v)) for k,v in pre.items()}))
    pg=cx.new_page(); pg.errs=[]; pg.on('pageerror',lambda e:pg.errs.append(str(e)))
    pg.route('**/image.tmdb.org/**',(lambda r:r.fulfill(body=IMG,content_type='image/webp')) if tmdb=='ok' else (lambda r:r.abort()))
    return cx,pg
def start(pg,url=U):
    pg.goto(url); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
g=lambda pg,e:pg.evaluate("(e)=>document.querySelector(e)&&document.querySelector(e).textContent.replace(/\\s+/g,' ').trim()",e)
with sync_playwright() as p:
    b=p.chromium.launch()
    cx,pg=ctx(b); start(pg)
    ck('build id',pg.evaluate("document.querySelector('meta[name=tva-build]').content")=='20261023-1730-m342')
    ck('1 header: Bentornato, Variante + % + barra',g(pg,'#homeHubHello')=='Bentornato, Variante' and pg.evaluate("()=>!!document.querySelector('#homeHub .home-hub-greeting .rs-prog > i')") and g(pg,'#hhgPct')=='0')
    ck('2 card Prossimo titolo: titolo/anno-universo/CTA',g(pg,'#hhsNextValue')=='Spider-Man' and '2002' in g(pg,'#m34NextMeta') and 'Inizia' in g(pg,'#m34NextCta'),(g(pg,'#hhsNextValue'),g(pg,'#m34NextMeta')))
    ck('2b locandina TMDB a sinistra del titolo',pg.evaluate("()=>{const i=document.querySelector('#m34Poster img');const t=document.querySelector('#hhsNextValue');return !!i&&i.getAttribute('data-src')==='tmdb'&&i.src.includes('image.tmdb.org')&&i.getBoundingClientRect().right<=t.getBoundingClientRect().left+1}"))
    ck('3 tre statistiche: completati/ore/voto',pg.evaluate("()=>[...document.querySelectorAll('#homeHub .m34-stat span')].map(e=>e.textContent).join('|')")=='Titoli completati|Ore viste|Voto medio')
    ck('3b completati = n/totale reali',g(pg,'#hhsDone').startswith('0/') and int(g(pg,'#hhsDone').split('/')[1])>100,g(pg,'#hhsDone'))
    ck('4 due accessi: Atlante e Tessera',pg.evaluate("()=>[...document.querySelectorAll('#homeHub .home-hub-nav .m34-acc')].map(e=>e.textContent.replace(/[^A-Za-z ]/g,'').trim()).join('|')")=='Atlante|Tessera TVA')
    ck('5 una sola missione in evidenza + Centrale TVA',pg.evaluate("()=>document.querySelectorAll('#homeHub .m34-mis').length===1")and g(pg,'#m34MName')=='Completa 3 titoli questa settimana' and 'Centrale' in g(pg,'#m34MGo'))
    ck('scorciatoie ridondanti rimosse dalla Home',pg.evaluate("()=>!document.querySelector('#homeHub #hhsRank,#homeHub #hhsStreak,#homeHub #hhsBadgeRow,#homeHub #homeHubStartBtn,#homeHub #homeHubSearchBtn,#homeHub #homeHubMapBtn,#homeHub #hhsContinueRow,#homeHub .home-hub-btn') && getComputedStyle(document.querySelector('#homeHub .a2-entry')||document.body).display!=='block' || !document.querySelector('#homeHub .a2-entry')"))
    ck('funzioni ancora nelle sezioni (mappa, ricerca, timeline alt, database, tessera, atlante)',pg.evaluate("()=>!!(guideMapBtn&&searchBox&&document.querySelector('label[for=altTimelineToggle].mg-open-btn')&&document.querySelector('label[for=tvaArchivesToggle].sidebar-archive-link')&&document.querySelector('label[for=tesseraToggle].sidebar-archive-link')&&document.querySelector('label[for=atlas2Toggle].sidebar-archive-link')&&cvContinueBtn)"))
    # accessi
    pg.touchscreen.tap(*pg.evaluate("()=>{const r=m34Atl.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(500)
    ck('Atlante apre l\'Atlante',pg.evaluate("()=>atlas2Toggle.checked"))
    pg.evaluate("()=>appTabHome.click()"); pg.wait_for_timeout(400)
    pg.touchscreen.tap(*pg.evaluate("()=>{const r=m34Tes.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(500)
    ck('Tessera apre la Tessera',pg.evaluate("()=>tesseraToggle.checked"))
    pg.evaluate("()=>appTabHome.click()"); pg.wait_for_timeout(400)
    pg.touchscreen.tap(*pg.evaluate("()=>{const r=m34MGo.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(600)
    ck('Centrale TVA aperta dalla missione',pg.evaluate("()=>document.documentElement.getAttribute('data-tva-view')==='centrale'"),pg.evaluate("()=>document.documentElement.getAttribute('data-tva-view')"))
    ck('nessun errore JS',not pg.errs,pg.errs); cx.close()
    # CTA -> scheda
    cx,pg=ctx(b); start(pg); pg.touchscreen.tap(*pg.evaluate("()=>{const r=m34NextCta.getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]}")); pg.wait_for_timeout(900)
    ck('CTA principale porta alla scheda del titolo',pg.evaluate("()=>getComputedStyle(homeHub).display==='none'||homeHubExited.checked")); cx.close()
    # overflow 3 larghezze
    for w in (390,360,320):
        cx,pg=ctx(b,w,pre={'marvel-ultimate-timeline-ratings':{'001':4.5}}); start(pg)
        r=pg.evaluate("()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,bad:[...document.querySelectorAll('#homeHub *')].filter(e=>e.offsetParent&&e.getBoundingClientRect().right>%d+1).map(e=>e.className).slice(0,4),h:homeHub.querySelector('.home-hub-inner').getBoundingClientRect().bottom,tab:appTabbar.getBoundingClientRect().top})"%w)
        ck(f'{w}: nessun overflow orizzontale',not r['bad'] and r['sw']<=r['cw']+1,r)
        ck(f'{w}: tutta la Home sopra la tab bar (no scroll)',r['h']<=r['tab'],r)
        cx.close()
    # voto medio
    cx,pg=ctx(b,pre={'marvel-ultimate-timeline-ratings':{'001':2,'002':3.5,'003':5}}); start(pg)
    ck('voto medio da voti salvati al caricamento (3.5)',g(pg,'#hhsRating')=='3.5 ⭐',g(pg,'#hhsRating'))
    pg.evaluate("()=>appTabTimeline.click()"); pg.wait_for_timeout(600); pg.evaluate("()=>document.querySelector('#item-004').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300)
    pg.touchscreen.tap(*pg.evaluate("()=>{const e=document.querySelectorAll('#item-004 .rw-s')[4].getBoundingClientRect();return [e.left+e.width/2,e.top+e.height/2]}")); pg.wait_for_timeout(400)
    ck('nuovo voto 5 -> media 3.9 (2+3.5+5+5)/4',g(pg,'#hhsRating')=='3.9 ⭐',g(pg,'#hhsRating'))
    pg.evaluate("()=>localStorage.setItem('marvel-ultimate-timeline-ratings','{}')"); pg.reload(); pg.wait_for_timeout(1000)
    ck('profilo senza voti -> «Nessun voto»',g(pg,'#hhsRating')=='Nessun voto',g(pg,'#hhsRating')); cx.close()
    cx,pg=ctx(b,pre={'marvel-ultimate-timeline-ratings':{'010':4}}); start(pg)
    ck('altro profilo (voto singolo 4) -> 4.0',g(pg,'#hhsRating')=='4.0 ⭐',g(pg,'#hhsRating')); cx.close()
    # locandina: fallback
    for mode,lab in (('abort','TMDB non raggiungibile'),):
        cx,pg=ctx(b,tmdb=mode); start(pg)
        ck('fallback emblema se la locandina non carica (nessuna immagine rotta, nessun vuoto)',pg.evaluate("()=>{const b=m34Poster;return !b.querySelector('img')&&!b.classList.contains('m34-has')&&getComputedStyle(m34Pfb).display!=='none'&&b.getBoundingClientRect().height>40}"))
        cx.close()
    cx,pg=ctx(b,pre={'tvaTmdbOff':'1'}); start(pg)
    ck('interruttore TMDB off -> emblema',pg.evaluate("()=>!m34Poster.querySelector('img')&&getComputedStyle(m34Pfb).display!=='none'")); cx.close()
    # prossimo titolo: ordine / progressi
    cx,pg=ctx(b); start(pg); seq=[]; okp=True
    for i in range(8):
        n=pg.evaluate("()=>{const t=hhsNextValue.textContent;return t}")
        nid=pg.evaluate("()=>window.marvelHomeNext&&window.marvelHomeNext.id")
        tag=pg.evaluate("(i)=>document.getElementById('item-'+i).getAttribute('data-tag')",nid)
        w=pg.evaluate("(i)=>JSON.parse(localStorage.getItem('marvel-ultimate-timeline-watched')||'{}')[i]",nid)
        seq.append((nid,tag,w)); 
        left_v=pg.evaluate("()=>{const st=JSON.parse(localStorage.getItem('marvel-ultimate-timeline-watched')||'{}');return [...document.querySelectorAll('.card-wrap[data-tag=verde][id^=item-]')].filter(e=>!st[e.getAttribute('data-item')]&&!e.classList.contains('card-variant')).length}")
        if w or (left_v>0 and tag!='verde'): okp=False
        pg.evaluate("(i)=>{const c=document.querySelector('#item-'+i+' input.watch-check, #item-'+i+' input[type=checkbox]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",nid); pg.wait_for_timeout(300)
    ids=[s[0] for s in seq]
    ck('prossimo titolo: mai già visto, verdi prima, avanza con i progressi',okp and len(set(ids))==len(ids),seq)
    ck('home aggiornata dopo i progressi (completati=8)',g(pg,'#hhsDone').startswith('8/'),g(pg,'#hhsDone'))
    ck('CTA «Continua» dopo il primo titolo',g(pg,'#m34NextCta').startswith('Continua')); cx.close()
    # tutto visto
    cx,pg=ctx(b); start(pg)
    pg.evaluate("()=>{window.marvelHomeNext=null;document.dispatchEvent(new CustomEvent('tva:homenext'))}")
    ck('stato «tutto visto»: emblema trofeo, CTA nascosta',g(pg,'#m34NextMeta').startswith('Hai completato') and pg.evaluate("()=>getComputedStyle(m34NextCta).display==='none'")); cx.close()
    # missioni: nessuna descrizione vuota/segnaposto in 14 settimane + 4 sezioni
    bad=[]
    for wk in range(14):
        d=datetime.datetime(2026,10,23)+datetime.timedelta(days=7*wk)
        cx,pg=ctx(b,date=d); start(pg)
        r=pg.evaluate("()=>['missioneSettimanale','missioneTematica','missioneSaga','missioneSegreta'].map(i=>document.getElementById(i).querySelector('.missione-testo').textContent.trim())")
        if any((not t) or t=='—' for t in r) or not g(pg,'#m34MName') or g(pg,'#m34MName')=='—': bad.append((str(d.date()),r))
        cx.close()
    ck('missioni: nessuna descrizione vuota o «—» (14 settimane)',not bad,bad[:2])
    # stati vuoti
    cx,pg=ctx(b); start(pg)
    pg.evaluate("()=>{['missioneSettimanale','missioneTematica','missioneSaga'].forEach(i=>document.getElementById(i).classList.add('missione-completa'));document.dispatchEvent(new CustomEvent('tva:missioni'))}")
    ck('tutte completate -> stato vuoto dedicato',g(pg,'#m34MName').startswith('Tutte le missioni') and pg.evaluate("()=>m34Mis.classList.contains('m34-empty')")and 'Centrale' in g(pg,'#m34MGo'))
    pg.evaluate("()=>{['missioneSettimanale','missioneTematica','missioneSaga'].forEach(i=>{const r=document.getElementById(i);r.classList.remove('missione-completa');r.querySelector('.missione-testo').textContent='—'});document.dispatchEvent(new CustomEvent('tva:missioni'))}")
    ck('nessuna missione valida -> «Nessuna missione attiva»',g(pg,'#m34MName').startswith('Nessuna missione attiva') and pg.evaluate("()=>m34Mis.classList.contains('m34-empty')")); cx.close()
    print(sum(R),'/',len(R))
# --- effetti collaterali al caricamento: stesso localStorage della build precedente (nessun XP/ricompensa/snapshot/celebrazione) ---
import json as _j
def snap(b,url,seed):
    cx=b.new_context(viewport={'width':390,'height':844},service_workers='block')
    cx.add_init_script("(()=>{if(!sessionStorage.getItem('s')){sessionStorage.setItem('s','1');const o=%s;for(const k in o)localStorage.setItem(k,o[k]);}})()"%_j.dumps(seed))
    pg=cx.new_page(); pg.goto(url); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(800)
    d=pg.evaluate("()=>Object.fromEntries(Object.keys(localStorage).sort().map(k=>[k,localStorage.getItem(k)]))"); cel=pg.evaluate("()=>!document.getElementById('missioneCelebrazione').hidden"); cx.close(); return d,cel
with sync_playwright() as p2:
    b2=p2.chromium.launch()
    wk=datetime.datetime.now().isocalendar()
    wid='%d-W%02d'%(wk[0],wk[1])
    seed={'marvel-ultimate-timeline-watched':_j.dumps({k:True for k in ['001','002','003','004','005']}),'marvel-ultimate-timeline-ratings':_j.dumps({'001':4}),
          'marvel-ultimate-timeline-missione-settimana':_j.dumps({'settimana':wid,'titoli':['001','002','003']})}
    a,ca=snap(b2,'http://127.0.0.1:8127/index.html',seed); c,cc=snap(b2,U,seed)
    ign={'marvel-ultimate-timeline-tessera-id'}
    diff=[k for k in set(a)|set(c) if k not in ign and a.get(k)!=c.get(k)]
    ck('caricamento: nessuna celebrazione/ricompensa/XP/snapshot scritti (identico a build precedente)',not diff and not cc and not ca,(diff,ca,cc))
    print(sum(R),'/',len(R))
