from playwright.sync_api import sync_playwright
R=[]
def ck(n,c,d=''): R.append(c); print(('PASS ' if c else 'FAIL ')+n+(' '+str(d)[:250] if not c else ''))
U='http://127.0.0.1:8124/index.html'
def start(b,w):
    cx=b.new_context(viewport={'width':w,'height':844},is_mobile=True,has_touch=True,service_workers='block'); pg=cx.new_page(); pg.errs=[]
    pg.on('pageerror',lambda e:pg.errs.append(str(e)))
    pg.route('**/image.tmdb.org/**',lambda r:r.abort())
    pg.goto(U); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.evaluate("()=>{document.getElementById('appTabTimeline').click()}"); pg.wait_for_timeout(800)
    return pg
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (390,360,320):
        pg=start(b,w)
        if w==390:
            ck('build id',pg.evaluate("document.querySelector('meta[name=tva-build]').content")=='20261023-1600-m34')
            ck('una sola card prologo, chiusa',pg.evaluate("()=>{const d=document.querySelectorAll('#cap0 details.cap0-pro');return d.length===1&&!d[0].open}"))
            t=pg.evaluate("()=>{const s=document.querySelector('#cap0 summary');return s.textContent.replace(/\\s+/g,' ')}")
            ck('titolo/sottotitolo/5 letture',all(x in t for x in ['Prologo','Prima del Tempo','5 letture']),t)
            ck('niente part-tab/part-head/h2/img in #cap0',pg.evaluate("()=>!document.querySelector('#cap0 .part-tab,#cap0 .part-head,#cap0 h2,#cap0 img')"))
            ck('5 letture 0.1-0.5 intatte, id #cap0',pg.evaluate("()=>[...document.querySelectorAll('#cap0 details.card .rec')].map(x=>x.textContent).join()")=='0.1,0.2,0.3,0.4,0.5')
            ck('letture chiuse e testi presenti',pg.evaluate("()=>[...document.querySelectorAll('#cap0 details.card')].every(d=>!d.open&&d.querySelector('.trama').textContent.length>80)"))
        
        ck(f'{w}: card chiusa compatta (<=70px)',pg.evaluate("()=>document.querySelector('#cap0').getBoundingClientRect().height")<=70,pg.evaluate("()=>document.querySelector('#cap0').getBoundingClientRect().height"))
        gap=pg.evaluate("()=>document.querySelector('#parte1').getBoundingClientRect().top-document.querySelector('#cap0').getBoundingClientRect().bottom")
        ck(f'{w}: Parte 1 segue subito (gap<=24px)',gap<=24,gap)
        pg.evaluate("()=>document.querySelector('#cap0').scrollIntoView({block:'start'})"); pg.wait_for_timeout(200)
        y0=pg.evaluate("()=>document.querySelector('#cap0 summary').getBoundingClientRect().top")
        pg.touchscreen.tap(w/2,y0+20); pg.wait_for_timeout(300)
        ck(f'{w}: tap apre',pg.evaluate("()=>document.querySelector('#cap0 details.cap0-pro').open"))
        y1=pg.evaluate("()=>document.querySelector('#cap0 summary').getBoundingClientRect().top")
        ck(f'{w}: nessun salto del summary',abs(y1-y0)<1,(y0,y1))
        ck(f'{w}: 5 letture visibili',pg.evaluate("()=>[...document.querySelectorAll('#cap0 details.card')].every(d=>d.getBoundingClientRect().height>30)"))
        # apri una lettura
        pg.evaluate("()=>document.querySelector('#cap0 details.card summary').click()"); pg.wait_for_timeout(250)
        ck(f'{w}: lettura espandibile',pg.evaluate("()=>document.querySelector('#cap0 details.card').open&&document.querySelector('#cap0 details.card .trama').getBoundingClientRect().height>20"))
        ov=pg.evaluate("()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,bad:[...document.querySelectorAll('#cap0 *')].filter(e=>e.getBoundingClientRect().right>%d+1).length})"%w)
        ck(f'{w}: nessun overflow orizzontale',ov['bad']==0 and ov['sw']<=ov['cw']+1,ov)
        pg.touchscreen.tap(w/2,pg.evaluate("()=>document.querySelector('#cap0 summary').getBoundingClientRect().top")+20); pg.wait_for_timeout(250)
        ck(f'{w}: tap richiude',not pg.evaluate("()=>document.querySelector('#cap0 details.cap0-pro').open"))
        if w==390:
            pg.screenshot(path='cap0_closed.png',clip={'x':0,'y':max(0,pg.evaluate("()=>document.querySelector('#cap0').getBoundingClientRect().top")-20),'width':w,'height':260})
            # ancore
            for sel in ['a.sidebar-content-link[href="#cap0"]','#indice a.toc-group-title[href="#cap0"]','a.tl-row[href="#cap0"]']:
                ex=pg.evaluate("(s)=>!!document.querySelector(s)",sel)
                if ex:
                    pg.evaluate("()=>{document.querySelector('#cap0 details.cap0-pro').open=false}")
                    pg.evaluate("(s)=>document.querySelector(s).click()",sel); pg.wait_for_timeout(500)
                    ck('ancora apre prologo: '+sel,pg.evaluate("()=>document.querySelector('#cap0 details.cap0-pro').open"))
                else: print('skip (assente in DOM)',sel)
            pg.goto(U+'#cap0'); pg.wait_for_timeout(1200)
            ck('apertura da hash #cap0',pg.evaluate("()=>document.querySelector('#cap0 details.cap0-pro').open"))
        ck(f'{w}: nessun errore JS',not pg.errs,pg.errs)
    print(sum(R),'/',len(R))
