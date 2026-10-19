"""Intro a scene: contenuti originali, navigazione (pulsanti/swipe/tastiera/rotella), indicatore, nessun duplicato, Home diretta, portale TVA."""
from playwright.sync_api import sync_playwright
import datetime
U='http://127.0.0.1:8124/index.html'
fails=[]
def ck(c,m,x=None):
    print(('PASS ' if c else 'FAIL ')+m+('' if c else ' '+str(x)))
    if not c: fails.append(m)
def swipe(pg,cdp,x1,y1,x2,y2):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x1,'y':y1}]})
    for i in range(1,9): cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x1+(x2-x1)*i/8,'y':y1+(y2-y1)*i/8}]}); pg.wait_for_timeout(15)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]}); pg.wait_for_timeout(900)
CUR="()=>tvaIntroScenes.current()"
def newpage(b,vw,vh,sa=False,rm=False):
    ctx=b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block',reduced_motion='reduce' if rm else 'no-preference'); pg=ctx.new_page(); pg.set_default_timeout(8000)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto(U); pg.wait_for_timeout(1500)
    if sa: pg.evaluate("()=>{const r=document.documentElement.style;r.setProperty('--sat','59px');r.setProperty('--sab','34px')}"); pg.wait_for_timeout(300)
    return ctx,pg,errs
VISJS="""()=>{const vis=e=>{if(!e.getClientRects().length)return false;const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return false;for(let n=e;n&&n.id!=='intro';n=n.parentElement){const s=getComputedStyle(n);if(s.visibility==='hidden'||s.display==='none'||parseFloat(s.opacity)<0.05)return false}return true};
 const i=document.getElementById('intro');const tx=[...i.querySelectorAll('h1,h2,p,span,button,summary,small,div')].filter(e=>vis(e)&&e.children.length===0&&e.textContent.trim()).map(e=>e.textContent.trim());
 return {tx,btn:[...i.querySelectorAll('button,summary')].filter(vis).map(b=>(b.getAttribute('aria-label')||b.textContent).trim()),on:[...i.querySelectorAll('.is-on')].length,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,ih:innerHeight,iw:innerWidth}}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw,vh in [(320,568),(360,640),(375,667),(390,844),(430,932)]:
        for sa in (False,True):
            tag='[%dx%d%s]'%(vw,vh,' safe' if sa else '')
            ctx,pg,errs=newpage(b,vw,vh,sa); cdp=ctx.new_cdp_session(pg)
            ck(pg.evaluate("()=>tvaIntroScenes.count")==4 and pg.evaluate(CUR)==0,tag+' 4 scene, parte dalla copertina')
            exp={0:['TIME VARIANCE AUTHORITY','ARCHIVIO CENTRALE','TVA ARCHIVE','The definitive interactive Marvel viewing experience.'],1:['Atto II'.upper() if False else 'Atto II','Il Multiverso si espande','titoli','universi','personaggi','ore complessive di visione','Numeri calcolati dai dati reali della guida, non arrotondati per impressionare.'],2:['Atto III','Il futuro del Multiverso','Avengers: Doomsday','Avengers: Secret Wars'],3:['Atto IV','Il portale TVA','Esplora TVA Archives','L’Archivio del Multiverso','Non sai da dove iniziare?']}
            for i in range(4):
                pg.evaluate("(i)=>tvaIntroScenes.go(i)",i); pg.wait_for_timeout(1900 if i else 600)
                v=pg.evaluate(VISJS); tx=v['tx']
                miss=[t for t in exp[i] if not any(t.lower() in x.lower() for x in tx)]
                ck(not miss,tag+' scena %d: testi originali presenti'%(i+1),(miss,tx))
                ck(v['sw']==vw and v['sh']<=vh+1,tag+' scena %d: nessun overflow di pagina'%(i+1),(v['sw'],v['sh']))
                cta=[x for x in v['btn'] if 'inizia il viaggio' in x.lower()]
                ck(len(cta)==1,tag+' scena %d: un solo «Inizia il viaggio» visibile'%(i+1),v['btn'])
                dup=[t for t in set(tx) if tx.count(t)>1 and len(t)>3 and t!='Evento futuro della Timeline']
                ck(not dup,tag+' scena %d: nessun testo duplicato'%(i+1),dup)
                others=pg.evaluate("(i)=>[...document.querySelectorAll('#intro .lm-sc')].filter((s,k)=>k!==i&&(s.getAttribute('inert')===null||getComputedStyle(s).visibility!=='hidden')).length",i)
                ck(others==0,tag+' scena %d: le altre scene sono inerti e nascoste'%(i+1),others)
                nav=pg.evaluate("()=>{const r=e=>e.getBoundingClientRect();const n=document.querySelector('.lm-nav'),pr=document.querySelector('.lm-prog');return {nb:r(n).bottom<=innerHeight+0.5,top:r(pr).top>=0,cur:document.querySelectorAll('.lm-seg.is-cur').length,done:document.querySelectorAll('.lm-seg.is-done').length,aria:document.querySelector('.lm-seg[aria-current=step]').getAttribute('aria-label')}}")
                ck(nav['nb'] and nav['top'] and nav['cur']==1 and nav['done']==i,tag+' scena %d: indicatore di avanzamento coerente'%(i+1),nav)
                if i==3 and vw in(320,390):
                    pg.evaluate("()=>{document.querySelector('details.intro-quiz').open=true}"); pg.wait_for_timeout(300)
                    pg.click('#quizOptsTempo [data-tempo=tutto]'); pg.wait_for_timeout(200); pg.click('#quizOptsStile [data-stile=cronologico]'); pg.wait_for_timeout(300)
                    r=pg.evaluate("()=>{const s=document.querySelector('.lm-act4');const b=document.getElementById('quizGoBtn').getBoundingClientRect();const n=document.querySelector('.lm-nav').getBoundingClientRect();s.scrollTop=s.scrollHeight;const b2=document.getElementById('quizGoBtn').getBoundingClientRect();return {txt:document.getElementById('quizResultText').textContent,reach:b2.bottom<=n.top+1&&b2.top>=0,sh:s.scrollHeight,ch:s.clientHeight}}")
                    ck('cronologica' in r['txt'].lower() or 'timeline alternativa' in r['txt'].lower(),tag+' quiz: risultato mostrato',r['txt'])
                    ck(r['reach'],tag+' quiz aperto: «Vai lì» raggiungibile scorrendo la scena e non coperto dalla navigazione',r)
                    if vw==390 and not sa: pg.evaluate("()=>{document.querySelector('.lm-act4').scrollTop=0}"); pg.screenshot(path='/tmp/claude-0/t/shots_leg/scena4_quiz_390.png')
            # dati: contatori finali e giorni
            pg.evaluate("()=>tvaIntroScenes.go(1)"); pg.wait_for_timeout(2200)
            nums=pg.evaluate("()=>[...document.querySelectorAll('.intro-stat-num')].map(e=>e.textContent)"); ck(nums==['176','138','27','300','~527'],tag+' statistiche originali dopo l\'animazione',nums)
            pg.evaluate("()=>tvaIntroScenes.go(2)"); pg.wait_for_timeout(2200)
            d=lambda s:(datetime.date.fromisoformat(s)-datetime.date.today()).days
            cd=pg.evaluate("()=>[icdDoomsday.textContent,icdSecretWars.textContent]"); ck(cd==[str(d('2026-12-18')),str(d('2027-12-17'))],tag+' contatori giorni corretti',(cd,d('2026-12-18'),d('2027-12-17')))
            ctx.close()
    # navigazione e input (390x844)
    ctx,pg,errs=newpage(b,390,844); cdp=ctx.new_cdp_session(pg)
    pg.click('.lm-next'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==1,'pulsante avanti')
    pg.click('.lm-next'); pg.wait_for_timeout(900); pg.click('.lm-prev'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==1,'pulsante indietro')
    pg.click('.lm-seg >> nth=3'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==3,'tocco sull\'indicatore: salta all\'atto')
    ck(pg.evaluate("()=>document.querySelector('.lm-next').disabled"),'ultima scena: avanti disattivato')
    pg.click('.lm-seg >> nth=0'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==0 and pg.evaluate("()=>document.querySelector('.lm-prev').disabled"),'prima scena: indietro disattivato')
    swipe(pg,cdp,195,600,195,250); ck(pg.evaluate(CUR)==1,'swipe su → scena successiva')
    swipe(pg,cdp,195,300,195,650); ck(pg.evaluate(CUR)==0,'swipe giù → scena precedente')
    swipe(pg,cdp,330,400,60,400); ck(pg.evaluate(CUR)==1,'swipe sinistra → successiva')
    swipe(pg,cdp,60,400,330,400); ck(pg.evaluate(CUR)==0,'swipe destra → precedente')
    swipe(pg,cdp,195,400,195,380); ck(pg.evaluate(CUR)==0,'micro-movimento ignorato')
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(900); pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==2,'tastiera: frecce avanti')
    pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==1,'tastiera: freccia indietro')
    pg.keyboard.press('End'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==3,'tastiera: End'); pg.keyboard.press('Home'); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==0,'tastiera: Home')
    pg.mouse.move(195,400); pg.mouse.wheel(0,300); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==1,'rotella → successiva')
    pg.mouse.wheel(0,-300); pg.wait_for_timeout(900); ck(pg.evaluate(CUR)==0,'rotella → precedente')
    ck(pg.evaluate("()=>document.getElementById('lmScroll').scrollTop")==0 and pg.evaluate("()=>scrollY")==0,'nessuno scroll di pagina durante la navigazione')
    ck(pg.evaluate("()=>document.getElementById('lmScroll').parentElement.querySelector('.lm-live').textContent").startswith('Atto'),'annuncio live per screen reader')
    # Tab: il focus non finisce mai in scene inerti
    pg.evaluate("()=>tvaIntroScenes.go(2)"); pg.wait_for_timeout(900); bad=0
    for _ in range(14):
        pg.keyboard.press('Tab'); bad+=pg.evaluate("()=>{const a=document.activeElement;return a&&a.closest&&a.closest('#intro .lm-sc:not(.is-on)')?1:0}")
    ck(bad==0,'Tab: nessun focus su scene non attive',bad)
    ck(not errs,'nessun errore JS (navigazione)',errs); ctx.close()
    # Inizia il viaggio da ogni scena → onboarding → Home
    for i in range(4):
        ctx,pg,errs=newpage(b,390,844)
        pg.evaluate("(i)=>tvaIntroScenes.go(i)",i); pg.wait_for_timeout(1500)
        pg.click('#journeyStartBtn' if i==0 else '.lm-skip'); pg.wait_for_timeout(600)
        ck(pg.evaluate("()=>!document.getElementById('onboardingScreen').hidden"),'scena %d: «Inizia il viaggio» avvia l\'onboarding senza completare le scene'%(i+1))
        pg.wait_for_function("()=>!document.getElementById('onboardingStep2').hidden",timeout=6000); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(700)
        h=pg.evaluate("()=>({j:journeyStarted.checked,intro:getComputedStyle(document.getElementById('intro')).display,home:getComputedStyle(document.querySelector('.home-hub')).display!=='none'})")
        ck(h['j'] and h['intro']=='none' and h['home'],'scena %d: arrivo in Home'%(i+1),h)
        if i==2:
            pg.evaluate("()=>{const c=document.getElementById('journeyStarted');c.checked=false;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
            ck(pg.evaluate(CUR)==0 and pg.evaluate("()=>getComputedStyle(document.getElementById('intro')).display")!='none','ritorno dalla Home: copertina, scena I')
            v=pg.evaluate(VISJS); ck(v['sw']==390,'ritorno: nessun overflow')
        ck(not errs,'scena %d: nessun errore JS'%(i+1),errs); ctx.close()
    # Portale TVA → onboarding → TVA Archives direttamente; indietro
    ctx,pg,errs=newpage(b,390,844)
    pg.evaluate("()=>tvaIntroScenes.go(3)"); pg.wait_for_timeout(1600); pg.click('#lmTvaPortal'); pg.wait_for_timeout(1000)
    ck(pg.evaluate("()=>!document.getElementById('onboardingScreen').hidden"),'portale: onboarding esistente')
    pg.wait_for_function("()=>!document.getElementById('onboardingStep2').hidden",timeout=6000); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(1200)
    st=pg.evaluate("()=>({atl:!!document.querySelector('#atlas2')&&getComputedStyle(document.querySelector('#atlas2')).display!=='none'&&document.querySelector('#atlas2').getClientRects().length>0,intro:getComputedStyle(document.getElementById('intro')).display,txt:(document.querySelector('#tvaShell')||document.body).innerText.slice(0,80)})")
    ck(st['atl'] and st['intro']=='none','portale: apre direttamente TVA Archives (non la Home)',st)
    pg.screenshot(path='/tmp/claude-0/t/shots_leg/portale_atlas_390.png')
    ctx.close()
    ST="()=>({atlas:document.getElementById('atlas2').getClientRects().length>0,intro:getComputedStyle(document.getElementById('intro')).display,home:getComputedStyle(document.querySelector('.home-hub')).display,tabs:getComputedStyle(document.getElementById('appTabbar')).display})"
    for act in ('a2-back','a2-exit','history'):
        ctx,pg,errs=newpage(b,390,844)
        pg.evaluate("()=>tvaIntroScenes.go(3)"); pg.wait_for_timeout(1500); pg.click('#lmTvaPortal'); pg.wait_for_timeout(900)
        pg.wait_for_function("()=>!document.getElementById('onboardingStep2').hidden",timeout=6000); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(1200)
        if act=='a2-back': pg.click('.a2-back')
        elif act=='a2-exit': pg.click('.a2-exit')
        else: pg.go_back()
        pg.wait_for_timeout(900); st=pg.evaluate(ST)
        ck(not st['atlas'] and st['intro']=='none' and st['home']!='none' and st['tabs']!='none','portale → TVA Archives → indietro (%s): Home e barra schede ripristinate'%act,st)
        ck(not errs,'portale indietro (%s): nessun errore'%act,errs); ctx.close()
    # reduced motion
    ctx,pg,errs=newpage(b,390,844,rm=True)
    pg.evaluate("()=>tvaIntroScenes.go(1)"); pg.wait_for_timeout(250)
    ck(pg.evaluate("()=>[...document.querySelectorAll('.intro-stat-num')].map(e=>e.textContent).join()")=='176,138,27,300,~527','reduced motion: numeri subito al valore finale')
    ck(pg.evaluate("()=>[...document.querySelectorAll('#intro .lm-sc')].every(s=>getComputedStyle(s).transitionDuration.split(',').every(x=>parseFloat(x)===0))"),'reduced motion: nessuna transizione di scena')
    ck(pg.evaluate("()=>getComputedStyle(document.querySelector('.lm-bp')).animationName")=='none','reduced motion: sfondo senza animazioni')
    ck(not errs,'reduced motion: nessun errore',errs); ctx.close()
    b.close()
print('TOTALE',len(fails),'FAIL'); 
