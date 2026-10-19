import sys
from playwright.sync_api import sync_playwright
from map3b_test_helpers import *
import map3b_test_helpers as H
VPS=[(320,568),(320,480),(360,640),(375,667),(390,844),(430,932),(844,390),(1024,768)]
def overlap_rects(r):
    bad=[]
    for i in range(len(r)):
        for j in range(i+1,len(r)):
            a,c=r[i],r[j]
            if a[0]<c[2]-1 and a[2]>c[0]+1 and a[1]<c[3]-1 and a[3]>c[1]+1: bad.append((a[4],c[4]))
    return bad
with sync_playwright() as p:
    b=p.chromium.launch()
    for (w,h) in VPS:
        tag=f'{w}x{h}'
        ctx,pg,errs=boot(b,w,h); cdp=ctx.new_cdp_session(pg)
        open_map(pg)
        ok(tag+' mappa aperta',st(pg)['screen']=='mappa')
        def noover(label):
            r=pg.evaluate("()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,a:[...document.querySelectorAll('#atlas2 *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>innerWidth+1||r.left<-1)&&!e.closest('.mp-stage')&&!e.closest('.mp-chips-s')&&!e.closest('.a2-jump')}).map(e=>e.className+'|'+(e.textContent||'').slice(0,20)).slice(0,5)})")
            ok(f'{tag} {label}: nessun overflow orizzontale',r['sw']<=r['cw'] and not r['a'],r)
        noover('overview')
        # bersagli ≥44
        small=pg.evaluate("()=>[...document.querySelectorAll('#atlas2 .mp-bar button,#atlas2 .mp-ctl button,#atlas2 .mp-pills button')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.width<43.5||r.height<43.5)}).map(e=>e.id||e.className)")
        ok(tag+' comandi ≥44px',not small,small)
        # testi >= 11px
        tiny=pg.evaluate("()=>[...document.querySelectorAll('#atlas2 .mp-bar *,#atlas2 .mp-pills *,#atlas2 .mp-ctl *,#atlas2 .mp-lb')].filter(e=>{const c=getComputedStyle(e);return e.childNodes.length&&[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim())&&(parseFloat(c.fontSize)<(e.classList.contains('mp-lb')?11:9.4))}).map(e=>e.className+':'+getComputedStyle(e).fontSize)")
        ok(tag+' testi leggibili',not tiny,tiny)
        r=pg.evaluate("()=>[...document.querySelectorAll('.mp-lb')].map(e=>{const r=e.getBoundingClientRect();return [r.x,r.y,r.right,r.bottom,e.textContent]})")
        ok(tag+' etichette senza sovrapposizioni',not overlap_rects(r),overlap_rects(r)); ok(tag+' etichette presenti',len(r)>=6,len(r))
        wr=pg.evaluate("()=>{const r=document.querySelector('.mp-wrap').getBoundingClientRect();return [r.x,r.y,r.right,r.bottom]}")
        ok(tag+' mappa adattata: tutti i nodi dentro l\'area',pg.evaluate("()=>[...document.querySelectorAll('.mp-n .mp-hit')].every(e=>{const r=e.getBoundingClientRect(),w=document.querySelector('.mp-wrap').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=w.top&&r.bottom<=w.bottom})"))
        hits=pg.evaluate("()=>[...document.querySelectorAll('.mp-n .mp-hit')].map(e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2,r.width/2]})")
        mind=min(((a[0]-c[0])**2+(a[1]-c[1])**2)**.5-(a[2]+c[2]) for i,a in enumerate(hits) for c in hits[i+1:]); ok(tag+' bersagli non sovrapposti',mind>=-0.5,mind)
        # selezione + anteprima
        x,y=center(pg,'uni-earth-199999-mcu'); pg.touchscreen.tap(x,y); pg.wait_for_timeout(600)
        sh=pg.evaluate("()=>{const s=document.querySelector('.mp-sheet'),r=s.getBoundingClientRect(),n=document.querySelector('.mp-n.sel .mp-hit').getBoundingClientRect(),w=document.querySelector('.mp-wrap').getBoundingClientRect();return {h:r.height,wh:w.height,top:r.top,nb:n.bottom,nt:n.top,sw:s.scrollWidth,cw:s.clientWidth,btn:document.querySelector('#mpOpenDossier').getBoundingClientRect().bottom,sb:r.bottom,vh:innerHeight}}")
        ok(tag+' anteprima ≤ 50% dell\'area mappa (≤58% se l\'altezza è ≤520px)',sh['h']<=sh['wh']*(0.58 if h<=520 else 0.5)+1,sh); ok(tag+' anteprima: pulsante dossier visibile',sh['btn']<=sh['vh']+1 and sh['btn']<=sh['sb']+1,sh)
        ok(tag+' anteprima: niente overflow orizzontale',sh['sw']<=sh['cw']+1,sh); ok(tag+' selezionato non coperto',sh['nb']<=sh['top']+2,sh)
        noover('selezione')
        for panel,btnid in [('legenda','#mpLegenda'),('filtri','#mpFiltri'),('fuori','#mpFuori')]:
            pg.click(btnid); pg.wait_for_timeout(350); noover('pannello '+panel)
            pr=pg.evaluate("()=>{const p=document.querySelector('.mp-panel').getBoundingClientRect();return [p.top,p.bottom,innerHeight]}"); ok(f'{tag} pannello {panel} dentro lo schermo',pr[0]>=0 and pr[1]<=pr[2]+1,pr)
            ok(f'{tag} pannello {panel}: chiudi raggiungibile',pg.evaluate("()=>{const r=document.querySelector('#mpPanelX').getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight&&r.width>=43.5}"))
            pg.click('#mpPanelX'); pg.wait_for_timeout(250)
        pg.click('.mp-sheet .mp-x'); pg.click('#mpModeList'); pg.wait_for_timeout(400); noover('elenco')
        ok(tag+' elenco: righe ≥44px',pg.evaluate("()=>[...document.querySelectorAll('.mp-rmain,.mp-rmap')].every(e=>e.getBoundingClientRect().height>=43.5&&e.getBoundingClientRect().width>=43.5)"))
        ok(tag+' elenco: nessun testo troncato oltre il bordo',pg.evaluate("()=>[...document.querySelectorAll('.mp-rt b,.mp-rt small')].every(e=>e.scrollWidth<=e.clientWidth+1)"))
        ok(tag+' nessun errore JS',not errs,errs); ctx.close()
    # reduced motion
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block',reduced_motion='reduce'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(H.U); pg.wait_for_timeout(1200); pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500); pg.click('#appTabAtlante'); pg.wait_for_timeout(700)
    open_map(pg); pg.click('#mpZin'); pg.wait_for_timeout(60); z=mp(pg)['v']['z']; ok('reduced-motion: zoom immediato (nessuna animazione)',z>1.6,z)
    anim=pg.evaluate("()=>[...document.querySelectorAll('#atlas2 .mp-wrap *')].filter(e=>{const c=getComputedStyle(e);return c.animationName!=='none'}).length"); ok('reduced-motion: nessuna animazione CSS',anim==0,anim)
    ok('reduced-motion: nessun errore',not errs,errs); ctx.close()
    b.close()
print('test',H.N[0],'fallimenti',len(H.F),H.F); sys.exit(1 if H.F else 0)
