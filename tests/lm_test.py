import re, datetime
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
OLD=open('/home/claude/work/backups/N18b_pre_living.html',encoding='utf-8').read()
oa=OLD.index('<div class="intro-screen"'); oblk=OLD[oa:OLD.index('<div class="onboarding-screen"',oa)]
OLDNUM=re.findall(r'class="intro-stat-num">([^<]*)<',oblk); OLDLBL=re.findall(r'class="intro-stat-lbl">([^<]*)<',oblk)
fails=[]
def chk(c,m):
    print('PASS' if c else 'FAIL',m)
    if not c: fails.append(m)
def new(b,vw,**kw):
    ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=vw[0]<600,has_touch=vw[0]<600,service_workers='block',**kw); pg=ctx.new_page(); pg.errs=[]
    pg.on('pageerror',lambda e:pg.errs.append(str(e))); return ctx,pg
OVER="""()=>{const W=innerWidth;const bad=[];for(const e of document.querySelectorAll('#intro *')){const r=e.getBoundingClientRect();if(e.closest('.lm-scene')||e.closest('.lm-art')||(e.closest('.intro-logo')&&document.getElementById('intro').classList.contains('lm-art-ready')))continue;if(r.width>1&&r.width>0&&(r.right>W+0.5||r.left<-0.5))bad.push(e.className+':'+Math.round(r.left)+'-'+Math.round(r.right))}
 const s=document.getElementById('lmScroll');return {page:document.documentElement.scrollWidth-W,sc:s.scrollWidth-s.clientWidth,bad:bad.slice(0,5)}}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    # 1-4: apertura, CTA nella prima viewport, overflow, tocco, titolo
    for vw in [(320,568),(360,640),(375,667),(390,844),(430,932),(844,390),(768,1024)]:
        ctx,pg=new(b,vw); pg.goto(U); pg.wait_for_timeout(2600); t=str(vw)
        chk(pg.evaluate("()=>getComputedStyle(document.getElementById('intro')).display!=='none'"),f'{t} intro visibile')
        chk(pg.evaluate("()=>document.querySelector('#intro h1').textContent.replace(/\\s+/g,' ').trim()")=='MARVEL MULTIVERSE',f'{t} titolo HTML MARVEL MULTIVERSE')
        chk('Infinite realtà. Un unico viaggio.' in pg.evaluate("()=>document.querySelector('.intro-tagline').textContent"),f'{t} sottotitolo')
        bt=pg.evaluate("()=>{const r=document.getElementById('journeyStartBtn').getBoundingClientRect();return [r.top,r.bottom,r.height,r.width,innerHeight]}")
        if vw[1]>vw[0]: chk(bt[1]<=bt[4] and bt[2]>=44 and bt[3]>=44,f'{t} CTA nella prima viewport e >=44px {bt}')
        else: chk(bt[2]>=44,f'{t} CTA >=44px (landscape: raggiungibile con scroll) {bt}')
        o=pg.evaluate(OVER); chk(o['page']<=0 and o['sc']<=0 and not o['bad'],f'{t} nessun overflow orizzontale {o}')
        al=pg.evaluate("()=>{const q=s=>document.querySelector(s);const b=q('#journeyStartBtn').getBoundingClientRect(),i=q('.lm-art-img').getBoundingClientRect();return [(b.y+b.height/2-i.y)/i.height*100,(b.x+b.width/2-i.x)/i.width*100,b.width/i.width*100,q('#intro').classList.contains('lm-art-ready'),getComputedStyle(q('#journeyStartBtn')).backgroundColor,getComputedStyle(q('.intro-logo')).clip]}")
        chk(al[3] and abs(al[0]-86.81)<0.4 and abs(al[1]-50)<0.6 and 60<al[2]<64,f'{t} pulsante HTML allineato a quello dipinto {al}')
        chk(al[4] in ('rgba(0, 0, 0, 0)','transparent'),f'{t} un solo pulsante visibile (HTML trasparente)')
        # tutti i controlli interattivi >=44px
        small=pg.evaluate("()=>[...document.querySelectorAll('#intro button,#intro summary')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.height<43.5)}).map(e=>e.id||e.className)"); chk(not small,f'{t} aree di tocco >=44 {small}')
        chk(not pg.errs,f'{t} nessun errore JS {pg.errs}'); ctx.close()
    # statistiche e countdown
    ctx,pg=new(b,(390,844)); pg.goto(U); pg.wait_for_timeout(1500)
    st=pg.evaluate("()=>[...document.querySelectorAll('.intro-stat')].map(e=>[e.querySelector('.intro-stat-num').textContent,e.querySelector('.intro-stat-lbl').textContent])")
    chk([x[0] for x in st]==['176','138','27','300','~527'],f'valori statistiche coerenti con la Home {st}')
    chk([x[1].split(' ')[0] for x in st]==['opere','titoli','universi','personaggi','ore'],'etichette esplicite')
    chk(len(st)==5,'5 statistiche (176 opere, 138 Timeline, 27, 300, ~527 ore)')
    ctx.close()
    def cdstate(date):
        c=b.new_context(viewport={'width':390,'height':844},service_workers='block'); q=c.new_page(); q.clock.install(time=date); q.goto(U); q.wait_for_timeout(1200)
        r=q.evaluate("()=>['icdDoomsday','icdSecretWars'].map(i=>{const e=document.getElementById(i);const h=e.closest('.intro-cd');return [e.textContent,h.dataset.state,getComputedStyle(h.querySelector('.lm-state')).display,getComputedStyle(h.querySelector('.lm-cap')).display]})"); c.close(); return r
    r=cdstate(datetime.datetime(2026,10,17,12,0)); chk(r[0][1]=='future' and r[0][0].isdigit() and r[1][1]=='future' and r[0][3]!='none',f'countdown futuro {r}')
    d1=(datetime.date(2026,12,18)-datetime.date(2026,10,17)).days; d2=(datetime.date(2027,12,17)-datetime.date(2026,10,17)).days
    chk(abs(int(r[0][0])-d1)<=1 and abs(int(r[1][0])-d2)<=1,f'giorni coerenti con le date configurate {r[0][0]}/{r[1][0]} vs {d1}/{d2}')
    r=cdstate(datetime.datetime(2026,12,18,12,0)); chk(r[0][0]=='OGGI' and r[0][1]=='today' and r[0][2]!='none',f'countdown oggi {r}')
    r=cdstate(datetime.datetime(2027,1,10,12,0)); chk(r[0][0]=='USCITO' and r[0][1]=='out' and r[1][1]=='future',f'countdown trascorso/misto {r}')
    # JS disattivato -> dati non disponibili: placeholder visibile e nessuna rottura
    c=b.new_context(viewport={'width':390,'height':844},java_script_enabled=False,service_workers='block'); q=c.new_page(); q.goto(U); q.wait_for_timeout(800)
    chk(q.evaluate("()=>document.getElementById('icdDoomsday').textContent")=='—' and q.evaluate("()=>getComputedStyle(document.getElementById('journeyStartBtn')).display")!='none','senza JS: placeholder countdown e CTA presenti'); c.close()
    # CTA -> onboarding -> viaggio avviato
    ctx,pg=new(b,(390,844)); pg.goto(U); pg.wait_for_timeout(1200)
    pg.click('#journeyStartBtn'); pg.wait_for_timeout(300)
    chk(pg.evaluate("()=>!document.getElementById('onboardingScreen').hidden"),'Inizia il viaggio apre onboarding')
    pg.wait_for_selector('#onboardingStartBtn:visible',timeout=6000); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(500)
    chk(pg.evaluate("()=>journeyStarted.checked && getComputedStyle(document.getElementById('intro')).display==='none'"),'viaggio avviato, intro chiusa')
    chk(pg.evaluate("()=>getComputedStyle(document.getElementById('homeHub')).display!=='none'"),'Home interna visibile dopo il viaggio'); chk(not pg.errs,f'errori {pg.errs}'); ctx.close()
    # portale TVA e quiz: Atti II–IV non più nel flusso visibile dell'intro (DOM e logica conservati); l'accesso all'Atlante resta da Home/tab
    ctx,pg=new(b,(390,844)); pg.goto(U); pg.wait_for_timeout(1200)
    chk(pg.evaluate("()=>['lmTvaPortal','quizGoBtn'].every(i=>!!document.getElementById(i))&&!document.querySelector('.lm-act4').classList.contains('is-on')"),'portale TVA e quiz nel DOM, nell\'Atto IV (non attivo sulla copertina)')
    chk(pg.evaluate("()=>getComputedStyle(document.querySelector('.lm-act4')).visibility==='hidden'"),'quiz non visibile sulla copertina (è nell\'Atto IV)'); ctx.close()
    # reduced motion
    ctx,pg=new(b,(390,844),reduced_motion='reduce'); pg.goto(U); pg.wait_for_timeout(500)
    an=pg.evaluate("()=>['.intro-logo-sub','.lm-t1','.intro-tagline','#journeyStartBtn','.lm-glow','.lm-cue::after'].map(s=>{const e=document.querySelector(s.replace('::after',''));const cs=getComputedStyle(e,s.includes('::after')?'::after':null);return [s,cs.animationName,cs.opacity]})")
    chk(all(a[1]=='none' for a in an) and all(float(a[2])>=0.99 or a[0]=='.lm-glow' for a in an),f'reduced-motion: nessuna animazione, contenuto subito visibile {an}')
    chk(pg.evaluate("()=>getComputedStyle(document.querySelector('.lm-l2')).transform")=='none','reduced-motion: nessun parallasse')
    ctx.close()
    # animazioni attive + parallasse con scroll
    ctx,pg=new(b,(390,844)); pg.goto(U); pg.wait_for_timeout(2600)
    chk(pg.evaluate("()=>getComputedStyle(document.querySelector('.intro-logo-sub')).opacity")=='1','titolo visibile dopo l’animazione')
    pg.evaluate("()=>{const s=document.getElementById('lmScroll');s.style.scrollBehavior='auto';s.scrollTop=500}"); pg.wait_for_timeout(300)
    chk(pg.evaluate("()=>document.getElementById('lmScroll').scrollTop")==0,'scroll interno dell\'intro bloccato (vista singola)'); ctx.close()
    # illustrazione: file presente, errore -> fallback SVG con titolo e pulsante HTML visibili
    ctx,pg=new(b,(390,844)); pg.goto(U); pg.wait_for_timeout(1500)
    chk(pg.evaluate("()=>{const i=document.querySelector('.lm-art-img');return i.naturalWidth===941&&i.naturalHeight===1672&&document.getElementById('intro').classList.contains('lm-art-ready')}"),'illustrazione caricata (941x1672) e attiva'); 
    chk(pg.evaluate("()=>/TIME VARIANCE AUTHORITY/.test(document.querySelector('.lm-act1 .intro-eyebrow').textContent)&&/ARCHIVIO CENTRALE/.test(document.querySelector('.lm-act1 .intro-eyebrow').textContent)&&getComputedStyle(document.querySelector('.lm-act1 .intro-eyebrow')).position==='absolute'&&document.querySelector('.lm-act1 .intro-eyebrow').getBoundingClientRect().width>100"),'TVA · ARCHIVIO CENTRALE come dettaglio editoriale visibile'); ctx.close()
    ctx,pg=new(b,(390,844)); pg.route('**/living-multiverse.webp',lambda r:r.abort()); pg.goto(U); pg.wait_for_timeout(1500)
    chk(pg.evaluate("()=>!document.getElementById('intro').classList.contains('lm-art-ready')&&getComputedStyle(document.querySelector('.lm-art')).display==='none'&&getComputedStyle(document.querySelector('.lm-l1')).display!=='none'&&document.getElementById('journeyStartBtn').getBoundingClientRect().width>150&&getComputedStyle(document.querySelector('.intro-logo')).position!=='absolute'"),'immagine mancante: fallback SVG + titolo e pulsante HTML'); ctx.close()
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block',reduced_motion='reduce'); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(1200)
    chk(pg.evaluate("()=>[...document.querySelectorAll('.lm-fx,#journeyStartBtn,.lm-art-img')].every(e=>getComputedStyle(e).animationName==='none')"),'reduced-motion: nessuna animazione sull\'illustrazione'); 
    chk(pg.evaluate("()=>document.getElementById('intro').classList.contains('lm-art-ready')"),'reduced-motion: illustrazione statica visibile'); ctx.close()
    # navigazione: dopo il viaggio l'app interna e l'Atlante restano integri
    ctx,pg=new(b,(390,844)); pg.goto(U); pg.wait_for_timeout(800)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
    chk(pg.evaluate("()=>getComputedStyle(document.getElementById('intro')).display==='none'"),'gate #journeyStarted: intro nascosta con il checkbox'); ctx.close()
    b.close()
print('FAILS',len(fails),fails)
