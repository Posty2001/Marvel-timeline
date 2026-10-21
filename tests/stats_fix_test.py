from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
F=[0]
def ok(n,c,x=''):
    print(('PASS ' if c else 'FAIL ')+n,x); F[0]+= 0 if c else 1
with sync_playwright() as p:
    b=p.chromium.launch()
    ctx=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; reqs=[]
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('response',lambda r: reqs.append((r.url.split('/')[-1],r.status)) if '/assets/images/tva/' in r.url else None)
    pg.goto(U); pg.wait_for_timeout(1500)
    ok('build id',pg.evaluate("()=>document.querySelector('meta[name=tva-build]').content")=='20261021-1900-blocco1')
    api=pg.evaluate("()=>tvaAtlas2.stats()"); print(api)
    ok('stats() 27/300/138/176',[api['universi'],api['personaggi'],api['titoliTimeline'],api['opereTotali']]==[27,300,138,176])
    # intro: vai alla scena II
    pg.evaluate("()=>{const n=document.querySelector('.lm-next');n&&n.click()}"); pg.wait_for_timeout(2500)
    ints=pg.evaluate("()=>[...document.querySelectorAll('.intro-stat')].map(e=>[e.querySelector('.intro-stat-num').textContent.trim(),e.querySelector('.intro-stat-lbl').textContent.trim(),e.querySelector('.intro-stat-num').dataset.stat||''])")
    print(ints)
    d={x[2]:x[0] for x in ints if x[2]}
    ok('intro = stats()',d.get('universi')=='27' and d.get('personaggi')=='300' and d.get('timeline')=='138' and d.get('opere')=='176',d)
    ok('etichette esplicite',any('Timeline' in x[1] for x in ints) and any('opere totali' in x[1] for x in ints))
    ok('ore invariato (~527)',any(x[0].startswith('~527') or x[0]=='~527' for x in ints),ints[-1])
    ok('niente "26" / "304" / "titoli" generico',not any(x[0] in ('26','304') for x in ints) and not any(x[1]=='titoli' for x in ints))
    pg.screenshot(path='/home/claude/outputs/intro_stats_fix_390.png')
    # Home coerente
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.click('#appTabAtlante'); pg.wait_for_timeout(700); pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1200)
    hs=pg.evaluate("()=>[...document.querySelectorAll('.hm-stats b')].map(e=>+e.textContent)")
    ok('Home 27/300/138',hs==[27,300,138],hs)
    ok('Home e intro: stessi valori',hs[0]==int(d['universi']) and hs[1]==int(d['personaggi']) and hs[2]==int(d['timeline']))
    first=[r for r in reqs if r[1]==404]; print('404 al primo avvio:',sorted(first))
    n1=len(first); ctx2=None
    # secondo caricamento stesso contesto (localStorage): nessun nuovo 404
    reqs.clear(); pg.reload(); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500); pg.click('#appTabAtlante'); pg.wait_for_timeout(600); pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1200)
    ok('reload: 0 richieste 404',len([r for r in reqs if r[1]==404])==0,[r for r in reqs if r[1]==404])
    ok('reload: asset dedicati presenti (niente SVG)',pg.evaluate("()=>!document.querySelector('.hm-scene')"))
    # nuovo asset: reprobe -> caricamento automatico
    png=open('/home/claude/work/assets/images/tva/cronologie.webp','rb').read()
    pg.route('**/assets/images/tva/eventi.webp',lambda r:r.fulfill(body=png,content_type='image/webp'))
    pg.evaluate("()=>tvaAtlas2.img.reprobe()"); pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(300); pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1200)
    ok('dopo reprobe: eventi.webp si carica',pg.evaluate("()=>document.querySelector('.hm-p[data-portal=eventi] .hm-p-bg').dataset.src")=='assets/images/tva/eventi.webp')
    ok('JS errors',not errs,errs)
    b.close()
print('FALLITI',F[0])
