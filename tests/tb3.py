import json,re,shutil,time,urllib.request
from playwright.sync_api import sync_playwright
R='/tmp/claude-0/t/srv/'; U='http://127.0.0.1:8765/index.html'
src=open('/home/claude/work/index.html',encoding='utf-8').read()
def setbuild(b):
    open(R+'index.html','w',encoding='utf-8').write(re.sub(r'name="tva-build" content="[^"]+"','name="tva-build" content="%s"'%b,src,count=1))
def st(): return json.loads(urllib.request.urlopen('http://127.0.0.1:8765/__state').read())
def setrange(b): urllib.request.urlopen('http://127.0.0.1:8765/__setrange?b='+(b or ''))
ok=True
def chk(n,c,d=''):
    global ok
    if not c: ok=False
    print(('PASS ' if c else 'FAIL ')+n,d)
shutil.copy('/home/claude/work/sw.js',R+'sw.js')
with sync_playwright() as p:
    b=p.chromium.launch()
    def newpage(vw=390,vh=844):
        ctx=b.new_context(viewport={'width':vw,'height':vh}); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); return ctx,pg,errs
    def ready(pg):
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}")
    # --- A: build coerente, nessun reload, nessun pannello
    setbuild('BLD-A'); setrange(None)
    ctx,pg,errs=newpage(); pg.goto(U); pg.wait_for_function("navigator.serviceWorker.controller||true"); pg.wait_for_timeout(2500)
    pg.reload(); pg.wait_for_timeout(3500)
    s=st(); chk('A1 build coerente: nessun reload extra (full GET <=2 per install+reload)',s['full']<=2 and s['range']>=1,s)
    chk('A2 nessun pannello debug di default',pg.evaluate("!document.getElementById('tvaDbgPanel')"))
    chk('A3 meta build presente',pg.evaluate("document.querySelector('meta[name=tva-build]').content")=='BLD-A')
    ready(pg); pg.wait_for_timeout(300)
    off=pg.evaluate("()=>{const r=document.getElementById('appTabbar').getBoundingClientRect();return [r.top,r.bottom,r.left,r.right,document.documentElement.scrollHeight,document.documentElement.scrollWidth,document.body.getBoundingClientRect().height,innerHeight]}")
    # SW risponde
    sw=pg.evaluate("""()=>new Promise(res=>{const c=navigator.serviceWorker.controller; if(!c){res('no-ctrl');return}const ch=new MessageChannel();ch.port1.onmessage=e=>res(e.data);c.postMessage({type:'tva-get-version'},[ch.port2]);setTimeout(()=>res('timeout'),2000)})""")
    chk('A4 SW risponde con versione',isinstance(sw,dict) and sw['swBuild']=='20261017-sw8' and sw['cache'].endswith('v8'),sw)
    # cache: niente 206, html completo
    cc=pg.evaluate("""async()=>{const ks=await caches.keys();const c=await caches.open(ks.find(k=>k.endsWith('v8'))||ks[0]);const reqs=await c.keys();const out=[];for(const r of reqs){const x=await c.match(r);out.push([r.url.split('/').pop()||'/',x.status])}return {ks,out}}""")
    chk('A5 cache v8 senza risposte 206 e vecchie cache rimosse',all(st_==200 for _,st_ in cc['out']) and cc['ks']==['marvel-timeline-cache-v8'],cc)
    # attivazione ?debugLayout=1
    ctx.close()
    ctx,pg,errs=newpage(); pg.goto(U); pg.wait_for_timeout(2500); pg.reload(); pg.wait_for_timeout(2500); pg.goto(U+'?debugLayout=1'); pg.wait_for_timeout(3500); ready(pg); pg.wait_for_timeout(1500)
    txt=pg.evaluate("document.getElementById('tvaDbgPanel')&&document.getElementById('tvaDbgPanel').innerText")
    chk('B1 pannello presente con ?debugLayout=1',bool(txt))
    print(txt)
    chk('B2 build in esecuzione/rete/cache coerenti',txt.count('BLD-A')>=3,'')
    chk('B3 mostra SW e safe area e tabbar',all(k in txt for k in ('SW in esecuzione','safe area','tabbar','visualViewport','innerWidth x innerHeight','display-mode standalone')))
    chk('B4 flag salvato',pg.evaluate("localStorage.getItem('tva-debug-layout')")=='1')
    on=pg.evaluate("()=>{const r=document.getElementById('appTabbar').getBoundingClientRect();return [r.top,r.bottom,r.left,r.right,document.documentElement.scrollHeight,document.documentElement.scrollWidth,document.body.getBoundingClientRect().height,innerHeight]}")
    chk('B5 il debug NON altera il layout (tabbar, scrollHeight, body)',on==off,(off,on))
    pg.screenshot(path='/tmp/claude-0/t/dbg.png')
    # chiudi
    pg.evaluate("[...document.querySelectorAll('#tvaDbgPanel button')].find(b=>b.textContent==='CHIUDI').click()"); pg.wait_for_timeout(200)
    chk('B6 CHIUDI rimuove pannello e flag',pg.evaluate("!document.getElementById('tvaDbgPanel')&&!localStorage.getItem('tva-debug-layout')&&!document.getElementById('tvaDbgProbe')"))
    chk('B7 nessun errore JS',not errs,errs)
    # 5 tap
    pg.goto(U); pg.wait_for_timeout(2500); ready(pg)
    for i in range(5): pg.evaluate("document.getElementById('appTabHome').click()"); pg.wait_for_timeout(80)
    chk('B8 5 tocchi sulla barra aprono il pannello',pg.evaluate("!!document.getElementById('tvaDbgPanel')"))
    for i in range(5): pg.evaluate("document.getElementById('appTabHome').click()"); pg.wait_for_timeout(80)
    chk('B9 altri 5 tocchi lo chiudono',pg.evaluate("!document.getElementById('tvaDbgPanel')"))
    ctx.close()
    # --- C: build di rete diversa -> un solo reload, anti-loop, dati intatti
    setrange('BLD-B')
    ctx,pg,errs=newpage(); pg.goto(U); pg.wait_for_timeout(500)
    pg.evaluate("localStorage.setItem('marvel-ultimate-timeline-watched',JSON.stringify({'015':true}));localStorage.setItem('marvel-ultimate-timeline-xp-test','keep')"); 
    n0=st()['full']; pg.wait_for_timeout(6000)
    s=st(); chk('C1 mismatch -> esattamente 1 reload (anti-loop)',s['full']-n0==1 or s['full']==2,s)
    pg.wait_for_timeout(3000); s2=st(); chk('C2 nessun secondo reload',s2['full']==s['full'],(s,s2))
    chk('C3 salvataggi/localStorage intatti dopo il reload',pg.evaluate("localStorage.getItem('marvel-ultimate-timeline-watched')")=='{"015":true}' and pg.evaluate("localStorage.getItem('marvel-ultimate-timeline-xp-test')")=='keep')
    chk('C4 sessionStorage guard impostato',pg.evaluate("sessionStorage.getItem('tva-build-reload')")=='BLD-B')
    ctx.close()
    # --- D: offline
    setrange(None); setbuild('BLD-A')
    ctx,pg,errs=newpage(); pg.goto(U); pg.wait_for_timeout(2500); pg.reload(); pg.wait_for_timeout(2500)
    ctx.set_offline(True); pg.reload(); pg.wait_for_timeout(2500)
    chk('D1 offline: pagina servita dalla cache, nessun errore',pg.evaluate("document.querySelector('meta[name=tva-build]').content")=='BLD-A' and not errs,errs)
    ctx.close()
    # --- E: HTML aggiornato sul server + max-age=3600: il nuovo SW non serve la versione vecchia
    setrange(None); setbuild('BLD-A')
    ctx,pg,errs=newpage(); pg.goto(U); pg.wait_for_timeout(2500); pg.reload(); pg.wait_for_timeout(2500)
    setbuild('BLD-NEW'); pg.goto(U); pg.wait_for_timeout(2500)
    got=pg.evaluate("document.querySelector('meta[name=tva-build]').content")
    chk('E1 SW v8: dopo aggiornamento server (con max-age=3600) la pagina mostra la build nuova',got=='BLD-NEW',got)
    ctx.close()
    # --- F: stesso scenario con SW v7 (prova della causa "cache HTTP stantia")
    shutil.copy('/home/claude/work/backups/sw_v7.js',R+'sw.js'); setbuild('BLD-A'); setrange(None)
    ctx,pg,errs=newpage(); pg.goto(U); pg.wait_for_timeout(2500); pg.reload(); pg.wait_for_timeout(2500)
    setbuild('BLD-NEW'); pg.goto(U); pg.wait_for_timeout(2500)
    got=pg.evaluate("document.querySelector('meta[name=tva-build]').content")
    print('INFO F1 SW v7 + server con max-age=3600, HTML aggiornato sul server -> pagina mostra:',got)
    ctx.close()
    b.close()
print('ALL_PASS' if ok else 'SOME_FAIL')
