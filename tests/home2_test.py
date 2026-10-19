from leg_shot import *
F=[0]
def ok(n,c,x=''):
    print(('PASS ' if c else 'FAIL ')+n,x); F[0]+= 0 if c else 1
EXP={'multiverso':('tog',None),'universi':('scr','universi'),'cronologie':('scr','cronologie'),'eventi':('arc','evt'),'personaggi':('scr','personaggi'),'poteri':('scr','potenza'),
 'relazioni':('scr','relazioni'),'attori':('scr','attori'),'cosmiche':('arc','cos'),'luoghi':('arc','luo'),'specie':('arc','spe'),'organizzazioni':('arc','org'),
 'artefatti':('arc','art'),'reliquiario':('scr','reliquiario'),'arti':('arc','mis')}
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1200)
    ids=pg.evaluate("()=>[...document.querySelectorAll('.hm-p')].map(e=>e.dataset.portal)")
    ok('15 portali distinti',len(ids)==15 and len(set(ids))==15 and set(ids)==set(EXP),ids)
    ok('nessun link duplicato (quick vs portali)',pg.evaluate("()=>document.querySelectorAll('[data-quick]').length")==2)
    for k in ids:
        pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(300)
        pg.evaluate("(k)=>document.querySelector('.hm-p[data-portal=\"'+k+'\"]').scrollIntoView({block:'center'})",k); pg.wait_for_timeout(150)
        pg.click(f'.hm-p[data-portal="{k}"]'); pg.wait_for_timeout(900)
        r=pg.evaluate("()=>{const a=tvaAtlas2.ext.api;return {s:a.ST.screen,arc:a.ST.arc,g:document.getElementById('multiverseGraphToggle').checked,h:(document.querySelector('.a2-ttl,.a2-top b')||{}).innerText}}")
        t,v=EXP[k]
        if k=='multiverso': good=(r['s']=='mappa' and not r['g'])   # 3B: il portale apre la nuova mappa (il grafo classico resta accessibile dalla mappa)
        elif k=='reliquiario': good=r['s']=='reliquiario'
        elif t=='scr': good=r['s']==v
        else: good=r['s']=='arch' and r['arc']==v
        ok('portale '+k,good,r)
        if True:
            pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(500)
            ok('  back->home '+k,pg.evaluate("()=>tvaAtlas2.ext.api.ST.screen")=='home')
    # quick
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(300)
    pg.click('[data-quick=confronto]'); pg.wait_for_timeout(600); ok('quick confronto',pg.evaluate("()=>tvaAtlas2.ext.api.ST.screen")=='confronto')
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(400)
    pg.click('[data-quick=indice]'); pg.wait_for_timeout(600); ok('quick indice',pg.evaluate("()=>tvaAtlas2.ext.api.ST.screen")=='catalogo')
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(400)
    # ricerca
    pg.fill('#a2HomeSearch','Thor'); pg.wait_for_timeout(700)
    ok('ricerca Thor',pg.evaluate("()=>document.querySelectorAll('.hm-res .a2-resbox').length")>0)
    pg.fill('#a2HomeSearch',''); pg.wait_for_timeout(300)
    # statistiche = dati reali
    st=pg.evaluate("()=>[...document.querySelectorAll('.hm-stats b')].map(e=>+e.textContent)")
    ok('stats 27/300/138',st==[27,300,138],st)
    # slot asset: hero fallback + auto-load
    ok('hero usa home_hero.webp',pg.evaluate("()=>document.querySelector('.hm-orb').dataset.src")=='assets/images/tva/home_hero.webp')
    ok('asset dedicati caricati (niente SVG)',pg.evaluate("()=>['eventi','luoghi','specie','organizzazioni'].every(k=>!document.querySelector('.hm-p[data-portal='+k+'] .hm-scene'))"))
    ok('overflow orizzontale 0',pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return s.scrollWidth<=s.clientWidth}"))
    ok('safe-area / h1 unico',pg.evaluate("()=>document.querySelectorAll('.a2-scroll h1').length")==1)
    ok('tap target >=44',pg.evaluate("()=>[...document.querySelectorAll('.hm-p,.hm-q,.hm-console .a2-sbox')].every(e=>e.getBoundingClientRect().height>=44)"))
    ok('JS errors',not errs,errs)
    # auto-load: servo un asset finto home_hero.webp
    ctx.close()
    for w in (320,360,414,430):
        c2,p2,e2=boot(b,w,844); p2.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); p2.wait_for_timeout(900)
        r=p2.evaluate("()=>{const s=document.querySelector('.a2-scroll');return [s.scrollWidth,s.clientWidth,[...document.querySelectorAll('.hm-p-t b,.hm-stats span')].filter(e=>e.scrollWidth>e.clientWidth+1).length]}")
        ok(f'no overflow {w}px',r[0]<=r[1] and r[2]==0,r); p2.screenshot(path=f'/home/claude/outputs/fase2_home_{w}_top.png'); c2.close()
    # reduced motion
    c3=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',is_mobile=True,has_touch=True,service_workers='block'); p3=c3.new_page()
    p3.goto(U); p3.wait_for_timeout(1000); p3.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); p3.wait_for_timeout(400); p3.click('#appTabAtlante'); p3.wait_for_timeout(600)
    p3.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); p3.wait_for_timeout(600)
    ok('reduced-motion: nessuna animazione',p3.evaluate("()=>['.hm-orb-img','.hm-beam','.hm-pt'].every(q=>getComputedStyle(document.querySelector(q)).animationName==='none')")); c3.close()
    # auto-load asset: intercetto home_hero.webp ed eventi.webp con immagini reali
    import base64
    png=open('/home/claude/work/assets/images/tva/cronologie.webp','rb').read()
    c4=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); p4=c4.new_page()
    p4.route('**/assets/images/tva/home_hero.webp',lambda r:r.fulfill(body=png,content_type='image/webp'))
    p4.route('**/assets/images/tva/eventi.webp',lambda r:r.fulfill(body=png,content_type='image/webp'))
    p4.goto(U); p4.wait_for_timeout(1000); p4.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); p4.wait_for_timeout(400); p4.click('#appTabAtlante'); p4.wait_for_timeout(600)
    p4.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); p4.wait_for_timeout(1200)
    ok('slot hero auto-load',p4.evaluate("()=>document.querySelector('.hm-orb').dataset.src")=='assets/images/tva/home_hero.webp')
    ok('slot eventi auto-load (niente SVG)',p4.evaluate("()=>{const e=document.querySelector('.hm-p[data-portal=eventi]');return e.dataset&&e.querySelector('.hm-p-bg').dataset.src==='assets/images/tva/eventi.webp'&&!e.querySelector('.hm-scene')}")); c4.close()
    b.close()
print('FALLITI',F[0])
