"""Intro a vista singola: nessun vecchio atto raggiungibile, onboarding/Home intatti, scroll altrove funzionante."""
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
fails=[]
def ck(c,m,x=None):
    print(('PASS ' if c else 'FAIL ')+m+('' if c else ' '+str(x)))
    if not c: fails.append(m)
def swipe(pg,x,y1,y2,cdp):
    cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y1}]})
    for i in range(1,9): cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y1+(y2-y1)*i/8}]}); pg.wait_for_timeout(15)
    cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw,vh in [(320,568),(360,640),(375,667),(390,844),(430,932)]:
        for sa in (False,True):
            tag='[%dx%d%s]'%(vw,vh,' safe' if sa else '')
            ctx=b.new_context(viewport={'width':vw,'height':vh},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000)
            errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
            pg.goto(U); pg.wait_for_timeout(1500)
            if sa: pg.evaluate("()=>{const r=document.documentElement.style;r.setProperty('--sat','59px');r.setProperty('--sab','34px')}"); pg.wait_for_timeout(300)
            cdp=ctx.new_cdp_session(pg)
            r=pg.evaluate("""()=>{const i=document.getElementById('intro'),sc=document.getElementById('lmScroll'),lo=i.querySelector('.lm-lower');
              const vis=[...lo.querySelectorAll('*')].filter(e=>e.getClientRects().length).length;
              return {shown:getComputedStyle(i).display!=='none',ready:i.classList.contains('lm-art-ready'),lowerDisp:getComputedStyle(lo).display,visLower:vis,sh:sc.scrollHeight,ch:sc.clientHeight,ov:getComputedStyle(sc).overflowY,docSH:document.documentElement.scrollHeight,ih:innerHeight,ids:['icdDoomsday','icdSecretWars','lmTvaPortal','journeyStartBtn'].map(x=>!!document.getElementById(x))}}""")
            ck(r['shown'] and r['ready'],tag+' copertina visibile (art-ready)',r)
            ck(r['lowerDisp']=='none' and r['visLower']==0,tag+' Atti II–IV fuori dal flusso visibile',r)
            ck(r['sh']<=r['ch']+1 and r['ov']=='hidden',tag+' nessun contenuto scorrevole sotto la copertina (%d/%d)'%(r['sh'],r['ch']),r)
            ck(all(r['ids']),tag+' ID/logica conservati (countdown, portale, pulsante)',r['ids'])
            # tentativi di scroll: wheel, swipe touch, tastiera, scrollTo
            pg.mouse.move(vw/2,vh/2); pg.mouse.wheel(0,1200); pg.wait_for_timeout(300)
            swipe(pg,vw/2,vh*0.8,vh*0.1,cdp); pg.wait_for_timeout(300)
            pg.keyboard.press('PageDown'); pg.keyboard.press('End'); pg.keyboard.press('Space'); pg.wait_for_timeout(300)
            pg.evaluate("()=>{document.getElementById('lmScroll').scrollTop=9999;window.scrollTo(0,9999)}"); pg.wait_for_timeout(300)
            a=pg.evaluate("()=>({st:document.getElementById('lmScroll').scrollTop,w:scrollY,top:Math.round(document.querySelector('.lm-art-img').getBoundingClientRect().top)})")
            ck(a['st']==0 and a['w']==0,tag+' dopo i tentativi di scroll nulla si sposta',a)
            if vw==390 and not sa: pg.screenshot(path='/tmp/claude-0/t/shots_leg/intro_dopo_scroll_390.png')
            if vw==320 and sa: pg.screenshot(path='/tmp/claude-0/t/shots_leg/intro_dopo_scroll_320_safe.png')
            if vw==430 and sa: pg.screenshot(path='/tmp/claude-0/t/shots_leg/intro_dopo_scroll_430_safe.png')
            # tab: il focus non entra mai nei contenuti nascosti
            bad=0
            for i in range(14):
                pg.keyboard.press('Tab'); bad+=pg.evaluate("()=>{const a=document.activeElement;return a&&a.closest&&a.closest('.lm-lower')?1:0}")
            ck(bad==0,tag+' Tab non raggiunge contenuti nascosti',bad)
            # pulsante reale: unico, cliccabile, onboarding → Home
            nbtn=pg.evaluate("()=>[...document.querySelectorAll('#intro button')].filter(b=>b.getClientRects().length).length")
            ck(nbtn==1,tag+' un solo pulsante visibile (Inizia il viaggio)',nbtn)
            pg.click('#journeyStartBtn'); pg.wait_for_timeout(700)
            ck(pg.evaluate("()=>!document.getElementById('onboardingScreen').hidden"),tag+' onboarding parte')
            pg.wait_for_function("()=>!document.getElementById('onboardingStep2').hidden",timeout=6000)
            pg.click('#onboardingStartBtn'); pg.wait_for_timeout(700)
            h=pg.evaluate("()=>({j:journeyStarted.checked,intro:getComputedStyle(document.getElementById('intro')).display,home:!!document.querySelector('.home-hub')&&getComputedStyle(document.querySelector('.home-hub')).display!=='none'})")
            ck(h['j'] and h['intro']=='none' and h['home'],tag+' Home raggiunta normalmente',h)
            if vw in (390,320) and not sa:
                # scroll nella Home
                sc=pg.evaluate("""()=>{const hh=document.querySelector('.home-hub');const c=[hh,...hh.querySelectorAll('*')].find(e=>e.scrollHeight>e.clientHeight+20&&/auto|scroll/.test(getComputedStyle(e).overflowY));return c?{sh:c.scrollHeight,ch:c.clientHeight}:null}""")
                pg.mouse.move(vw/2,vh/2); pg.mouse.wheel(0,400); pg.wait_for_timeout(300)
                mv=pg.evaluate("""()=>{const hh=document.querySelector('.home-hub');const c=[hh,...hh.querySelectorAll('*')].find(e=>e.scrollTop>0);return !!c||scrollY>0}""")
                ck(sc is None or mv,tag+' la Home scorre ancora',(sc,mv))
                # Atlante
                pg.click('#appTabAtlante'); pg.wait_for_timeout(700)
                pg.evaluate("()=>tvaAtlas2.ext.api.nav('personaggi',{pf:'tutti',pq:''})"); pg.wait_for_timeout(500)
                pg.mouse.move(vw/2,vh/2); pg.mouse.wheel(0,600); pg.wait_for_timeout(300)
                ck(pg.evaluate("()=>document.querySelector('.a2-scroll').scrollTop")>50,tag+' TVA Archives scorre ancora')
                # ritorno alla copertina (riapertura intro): stesso stato a vista singola
                pg.evaluate("()=>{const c=document.getElementById('journeyStarted');c.checked=false;c.dispatchEvent(new Event('change',{bubbles:true}));history.back&&0}"); pg.wait_for_timeout(600)
                rr=pg.evaluate("()=>{const i=document.getElementById('intro'),sc=document.getElementById('lmScroll');return {shown:getComputedStyle(i).display!=='none',st:sc.scrollTop,sh:sc.scrollHeight,ch:sc.clientHeight,home:[...document.querySelectorAll('.home-hub,#atlas2')].some(e=>e.getClientRects().length)}}")
                ck(rr['shown'] and rr['st']==0 and rr['sh']<=rr['ch']+1 and not rr['home'],tag+' ritorno alla copertina: vista singola, a scroll 0',rr)
                pg.mouse.wheel(0,900); pg.wait_for_timeout(300)
                ck(pg.evaluate("()=>document.getElementById('lmScroll').scrollTop")==0,tag+' ritorno: scroll ancora bloccato')
                pg.screenshot(path='/tmp/claude-0/t/shots_leg/intro_ritorno_390.png') if vw==390 else None
                pg.click('#journeyStartBtn'); pg.wait_for_timeout(600); ck(pg.evaluate("()=>!document.getElementById('onboardingScreen').hidden"),tag+' ritorno: il pulsante riavvia l\'onboarding')
            ck(not errs,tag+' nessun errore JS',errs)
            ctx.close()
    # dati salvati non toccati
    b.close()
print('TOTALE',len(fails),'FAIL')
