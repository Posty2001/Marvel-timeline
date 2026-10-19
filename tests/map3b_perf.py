import sys,statistics
from playwright.sync_api import sync_playwright
from map3b_test_helpers import *
import map3b_test_helpers as H
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=H.boot(b); cdp=ctx.new_cdp_session(pg)
    open_map(pg)
    cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    pg.evaluate("""()=>{window.__ft=[];let l=performance.now();function f(t){window.__ft.push(t-l);l=t;if(window.__run)requestAnimationFrame(f)}window.__run=true;requestAnimationFrame(f)}""")
    # pan lungo + pinch
    for i in range(3):
        pan(pg,cdp,(250,500),(120,380),steps=40); pan(pg,cdp,(120,380),(260,520),steps=40)
    pinch(pg,cdp,(195,500),70,230,steps=40); pinch(pg,cdp,(195,500),230,70,steps=40)
    pg.evaluate("()=>{window.__run=false}"); ft=pg.evaluate("()=>window.__ft.slice(2)")
    ft.sort(); p95=ft[int(len(ft)*.95)]; ok('frame p95 con CPU 4× più lenta < 50 ms',p95<50,p95); print('frames>50ms',sum(1 for x in ft if x>50),sorted(ft)[-5:]); print('frames',len(ft),'p50',round(statistics.median(ft),1),'p95',round(p95,1),'max',round(max(ft),1))
    # dimensione scena
    nn=pg.evaluate("()=>document.querySelectorAll('.mp-stage *').length"); print('nodi DOM scena',nn); ok('scena leggera (<900 elementi)',nn<900,nn)
    fx=pg.evaluate("()=>[...document.querySelectorAll('#atlas2 .mp-wrap *')].filter(e=>{const c=getComputedStyle(e);return c.filter!=='none'||(c.backdropFilter&&c.backdropFilter!=='none')}).length"); ok('nessun filter/backdrop-filter',fx==0,fx)
    cdp.send('Emulation.setCPUThrottlingRate',{'rate':1})
    # asset opzionale: assente -> fallback, una sola richiesta; presente -> adottato
    reqs=[]; pg.on('request',lambda r: reqs.append(r.url) if 'mappa_sfondo' in r.url else None)
    ok('sfondo procedurale senza asset',pg.evaluate("()=>!document.querySelector('.mp-bg-img')||!document.querySelector('.mp-bg').classList.contains('hm-has-img')"))
    print('errori',errs); ok('nessun errore JS',not errs,errs); b.close()
print('test',H.N[0],'fallimenti',len(H.F),H.F); sys.exit(1 if H.F else 0)
