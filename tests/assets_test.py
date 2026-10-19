from leg_shot import *
import io, statistics
from PIL import Image
F=[0]
def ok(n,c,x=''):
    print(('PASS ' if c else 'FAIL ')+n,x); F[0]+= 0 if c else 1
ASSET={'home_hero':(1600,1600,'.hm-orb'),'eventi':(1680,400,'eventi'),'luoghi':(960,1260,'luoghi'),'specie_civilta':(1200,940,'specie'),'organizzazioni':(1200,940,'organizzazioni'),'universi':(1200,920,'universi'),'attori':(1200,830,'attori'),'reliquiario':(1200,920,'reliquiario')}
LIM={'home_hero':250,'eventi':80,'luoghi':140,'specie_civilta':130,'organizzazioni':130,'universi':130,'attori':120,'reliquiario':130}
import os
for k,(w,h,_) in ASSET.items():
    f='/home/claude/work/assets/images/tva/%s.webp'%k; im=Image.open(f); kb=os.path.getsize(f)/1024
    ok(f'file {k}: {im.size} {kb:.0f}KB',im.size==(w,h) and kb<=LIM[k])
def lum(rgb):
    def c(v):
        v/=255; return v/12.92 if v<=0.03928 else ((v+0.055)/1.055)**2.4
    return 0.2126*c(rgb[0])+0.7152*c(rgb[1])+0.0722*c(rgb[2])
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (390,320):
        ctx,pg,errs=boot(b,W,844); r404=[]; pg.on('response',lambda r: r404.append(r.url) if r.status>=400 else None)
        pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(800)
        # scorri tutta la pagina (lazy) e verifica caricamento
        H=pg.evaluate("()=>document.querySelector('.a2-scroll').scrollHeight")
        for y in range(0,H,400): pg.evaluate("(y)=>document.querySelector('.a2-scroll').scrollTop=y",y); pg.wait_for_timeout(200)
        pg.wait_for_timeout(800)
        res=pg.evaluate("""()=>({orb:document.querySelector('.hm-orb img'),}) && [...document.querySelectorAll('.hm-orb img,.hm-p-img')].map(i=>({s:i.getAttribute('src'),nw:i.naturalWidth,nh:i.naturalHeight,fit:getComputedStyle(i).objectFit,w:i.clientWidth,h:i.clientHeight}))""")
        ok(f'[{W}] 8 immagini dedicate caricate',len([x for x in res if any(a in (x['s'] or '') for a in ASSET) and x['nw']>0 and not any(t in x['s'] for t in ('multiverso','personaggi','cronologie','relazioni','artefatti','entita_cosmiche','arti_mistiche','classifica_poteri'))])==8,[(x['s'].split('/')[-1],x['nw']) for x in res])
        ok(f'[{W}] tutte le copertine caricate (naturalWidth>0)',all(x['nw']>0 for x in res),[x['s'] for x in res if x['nw']==0])
        ok(f'[{W}] object-fit cover (nessuna deformazione)',all(x['fit']=='cover' for x in res))
        ok(f'[{W}] nessuna risposta 4xx/5xx',not r404,r404)
        ok(f'[{W}] nessun errore JS',not errs,errs)
        ok(f'[{W}] fallback SVG non attivo',pg.evaluate("()=>!document.querySelector('.hm-scene')"))
        # leggibilita' del titolo: sfondo (testo nascosto) sotto .hm-p-t ; contrasto avorio (#F2E8D8)
        worst=(99,'')
        keys=pg.evaluate("()=>[...document.querySelectorAll('.hm-p')].map(e=>e.dataset.portal)")
        for k in keys:
            pg.evaluate("(k)=>{document.querySelector('.hm-p[data-portal=\"'+k+'\"]').scrollIntoView({block:'center'});document.querySelectorAll('.hm-p-t').forEach(e=>e.style.visibility='hidden')}",k); pg.wait_for_timeout(250)
            bx=pg.evaluate("(k)=>{const r=document.querySelector('.hm-p[data-portal=\"'+k+'\"] .hm-p-t').getBoundingClientRect();return [r.x,r.y,r.width,r.height]}",k)
            png=pg.screenshot(clip={'x':max(0,bx[0]),'y':bx[1],'width':max(4,min(bx[2],W-bx[0])),'height':max(4,bx[3])}); im=Image.open(io.BytesIO(png)).convert('RGB')
            ls=sorted(lum(px) for px in im.getdata()); l90=ls[int(len(ls)*0.9)]
            cr=(lum((242,232,216))+0.05)/(l90+0.05)
            if cr<worst[0]: worst=(cr,k)
            pg.evaluate("()=>document.querySelectorAll('.hm-p-t').forEach(e=>e.style.visibility='')")
            if cr<4.5: print('   titolo basso contrasto',k,round(cr,2))
        ok(f'[{W}] contrasto titoli >=4.5 (peggiore {worst[1]} {worst[0]:.1f})',worst[0]>=4.5)
        ctx.close()
    # prestazioni scorrimento (Chromium headless, CPU rallentata 4x)
    ctx,pg,errs=boot(b); cdp=ctx.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate',{'rate':4})
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1200)
    r=pg.evaluate("""()=>new Promise(res=>{const s=document.querySelector('.a2-scroll');const H=s.scrollHeight-s.clientHeight;let last=performance.now(),g=[],y=0;function f(t){g.push(t-last);last=t;y+=14;s.scrollTop=y;if(y<H)requestAnimationFrame(f);else res(g)}requestAnimationFrame(f)})""")
    r=sorted(r); p50=r[len(r)//2]; p95=r[int(len(r)*.95)]; print('frame ms p50/p95/max',round(p50,1),round(p95,1),round(r[-1],1),len(r))
    ok('scorrimento: p95 frame < 50ms con CPU 4x piu lenta',p95<50)
    ctx.close()
    # fallback: asset mancante / 404 / file corrotto, uno alla volta
    for k,(w,h,sel) in ASSET.items():
        for mode in ('abort','corrotto'):
            c2=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); p2=c2.new_page(); e2=[]; p2.on('pageerror',lambda e:e2.append(str(e)))
            if mode=='abort': p2.route(f'**/assets/images/tva/{k}.webp',lambda r:r.fulfill(status=404,body=''))
            else: p2.route(f'**/assets/images/tva/{k}.webp',lambda r:r.fulfill(body=b'non e un webp',content_type='image/webp'))
            p2.goto(U); p2.wait_for_timeout(900); p2.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); p2.wait_for_timeout(400); p2.click('#appTabAtlante'); p2.wait_for_timeout(500)
            p2.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); p2.wait_for_timeout(500)
            hh=p2.evaluate("()=>document.querySelector('.a2-scroll').scrollHeight")
            for y in range(0,hh,500): p2.evaluate("(y)=>document.querySelector('.a2-scroll').scrollTop=y",y); p2.wait_for_timeout(120)
            p2.wait_for_timeout(600)
            if k=='home_hero': good=p2.evaluate("()=>{const i=document.querySelector('.hm-orb img');return !!i&&i.naturalWidth>0&&/multiverso/.test(i.src)}")
            else: good=p2.evaluate("(s)=>{const e=document.querySelector('.hm-p[data-portal='+s+']');const i=e.querySelector('.hm-p-img');return (!!e.querySelector('.hm-scene'))||(!!i&&i.naturalWidth>0&&!/%s/.test(i.src))}"%k,sel)
            ok(f'fallback {k} ({mode})',good and not e2,e2)
            c2.close()
    b.close()
print('FALLITI',F[0])
