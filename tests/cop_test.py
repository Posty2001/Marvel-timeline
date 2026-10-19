from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
fails=[]
def chk(c,m):
    if not c: fails.append(m); print('FAIL',m)
JS_IMG="""()=>[...document.querySelectorAll('.a2-bgimg,.a2-lrow-img img')].map(i=>({ok:i.complete&&i.naturalWidth>0,src:i.getAttribute('src'),r:i.getBoundingClientRect().width>0}))"""
def setup(pg):
    pg.goto(U); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(300)
def nav(pg,s): pg.evaluate("()=>"+s); pg.wait_for_timeout(500)
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw in [(320,568),(375,667),(430,932)]:
        ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=True,has_touch=True); pg=ctx.new_page(); errs=[]; bad404=[]
        pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('response',lambda r: bad404.append(r.url) if r.status>=400 and 'fonts' not in r.url else None)
        setup(pg); tag=str(vw[0])
        # Home tiles
        pg.evaluate("()=>document.querySelector('.a2-tiles').scrollIntoView()"); pg.wait_for_timeout(600)
        im=pg.evaluate(JS_IMG); chk(len(im)==4 and all(x['ok'] for x in im),f'{tag} home tiles {im}')
        pg.screenshot(path=f'/tmp/claude-0/t/cop_home_{tag}.png')
        ov=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return s.scrollWidth-s.clientWidth}"); chk(ov<=0,f'{tag} home overflow {ov}')
        # Catalogo
        nav(pg,"tvaAtlas2.ext.api.nav('catalogo')"); pg.wait_for_timeout(600)
        pg.evaluate("()=>document.querySelectorAll('.a2-lrow-img img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(600)
        im=pg.evaluate(JS_IMG); chk(len(im)==9 and all(x['ok'] for x in im),f'{tag} catalogo {len(im)} {[x for x in im if not x["ok"]]}')
        sq=pg.evaluate("()=>[...document.querySelectorAll('.a2-lrow-img')].every(c=>{const r=c.getBoundingClientRect();return Math.abs(r.width-r.height)<0.6&&r.width>=36})"); chk(sq,f'{tag} thumb quadrati')
        ov=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return s.scrollWidth-s.clientWidth}"); chk(ov<=0,f'{tag} catalogo overflow {ov}')
        pg.screenshot(path=f'/tmp/claude-0/t/cop_cat_{tag}.png')
        # archivi + dossier
        for cat,n in (('art','artefatti'),('cos','entita_cosmiche'),('mis','arti_mistiche'),('org',None),('evt',None),('luo',None),('spe',None)):
            nav(pg,f"tvaAtlas2.ext.api.nav('arch',{{arc:'{cat}',eid:null,af:'tutti',aq:'',au:'tutti'}})")
            im=pg.evaluate(JS_IMG); hero_has=pg.evaluate("()=>!!document.querySelector('.a2-arc-hero.a2-has-img')")
            if n: chk(hero_has and len(im)==1 and im[0]['ok'] and n in im[0]['src'],f'{tag} {cat} hero img {im}')
            else: chk(not hero_has and not im,f'{tag} {cat} nessuna img attesa {im}')
            ov=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return s.scrollWidth-s.clientWidth}"); chk(ov<=0,f'{tag} {cat} overflow {ov}')
            # titolo leggibile (h2 sopra immagine) e dossier del primo elemento
            first=pg.evaluate("()=>{const c=document.querySelector('.a2-arcard');return c&&c.getAttribute('data-arc')}")
            if first:
                pg.evaluate("()=>document.querySelector('.a2-arcard').click()"); pg.wait_for_timeout(500)
                im=pg.evaluate(JS_IMG); h=pg.evaluate("()=>!!document.querySelector('.a2-arc-hero.a2-has-img')")
                if n: chk(h and im and im[0]['ok'],f'{tag} {cat} dossier {im}')
                else: chk(not h,f'{tag} {cat} dossier no img')
                if n and cat=='art': pg.screenshot(path=f'/tmp/claude-0/t/cop_doss_{tag}.png')
                ov=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return s.scrollWidth-s.clientWidth}"); chk(ov<=0,f'{tag} {cat} dossier overflow {ov}')
            if cat=='cos': pg.screenshot(path=f'/tmp/claude-0/t/cop_arch_{tag}.png')
        # potenza
        nav(pg,"tvaAtlas2.ext.api.nav('potenza')") if False else pg.evaluate("()=>tvaAtlas2.ext.api.go?0:0")
        nav(pg,"tvaAtlas2.ext.api.nav('potenza')")
        im=pg.evaluate(JS_IMG); chk(any('classifica_poteri' in x['src'] and x['ok'] for x in im),f'{tag} potenza {im}')
        chk(not errs,f'{tag} errori JS {errs}'); chk(not bad404,f'{tag} 404 {bad404}')
        print(tag,'ok',len(errs),bad404[:3]); ctx.close()
    # fallback: blocco immagini -> emblemi / nessun elemento rotto
    ctx=b.new_context(viewport={'width':375,'height':667},service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/assets/images/tva/*',lambda r:r.abort()); setup(pg)
    pg.evaluate("()=>document.querySelector('.a2-tiles').scrollIntoView()"); pg.wait_for_timeout(800)
    chk(pg.evaluate("()=>document.querySelectorAll('.a2-tile .a2-tile-bg').length")==4 and pg.evaluate("()=>document.querySelectorAll('.a2-has-img,.a2-bgimg').length")==0,'fallback home tile decor')
    nav(pg,"tvaAtlas2.ext.api.nav('catalogo')"); pg.evaluate("()=>document.querySelectorAll('.a2-lrow-img img').forEach(i=>i.loading='eager')"); pg.wait_for_timeout(800)
    chk(pg.evaluate("()=>document.querySelectorAll('.a2-lrow-img').length")==0 and pg.evaluate("()=>document.querySelectorAll('.a2-lrow-ic').length")>=9,'fallback catalogo icone')
    nav(pg,"tvaAtlas2.ext.api.nav('arch',{arc:'art',eid:null,af:'tutti',aq:'',au:'tutti'})"); pg.wait_for_timeout(500)
    chk(pg.evaluate("()=>!document.querySelector('.a2-arc-hero.a2-has-img')&&!!document.querySelector('.a2-arc-hero .a2-arc-ic')"),'fallback hero art icon')
    pg.evaluate("()=>document.querySelector('.a2-arcard').click()"); pg.wait_for_timeout(500)
    chk(pg.evaluate("()=>!document.querySelector('.a2-has-img')&&!!document.querySelector('.a2-cov-hero svg')"),'fallback dossier emblema')
    chk(not errs,f'fallback errori {errs}'); print('fallback ok')
    print('FAILS',len(fails),fails); b.close()
