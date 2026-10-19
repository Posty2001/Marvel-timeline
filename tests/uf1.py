import json,re,sys
from playwright.sync_api import sync_playwright
F=sys.argv[1] if len(sys.argv)>1 else 'file:///home/claude/work/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(800)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(300)
    for uid,nome in (('uni-earth-828','Earth-828'),('uni-earth-121698','Earth-121698')):
        pg.evaluate("([u,n])=>window.marvelEsploraUniverso(u,n)",[uid,nome]); pg.wait_for_timeout(500)
        r=pg.evaluate("""()=>{const vis=[...document.querySelectorAll('li.card-wrap')].filter(l=>!l.closest('.tva-archives-overlay')&&l.offsetParent!==null).map(l=>l.id);
         const blocks=[...document.body.children].filter(e=>e.offsetParent!==null&&!['SCRIPT','INPUT','STYLE','NOSCRIPT'].includes(e.tagName)&&!e.classList.contains('app-tabbar')&&!e.classList.contains('sidebar')).map(e=>e.tagName.toLowerCase()+(e.id?'#'+e.id:'')+(e.className&&typeof e.className==='string'?'.'+e.className.split(' ')[0]:''));
         const heads=[...document.querySelectorAll('h2,h3.sec-h')].filter(h=>h.offsetParent!==null).map(h=>h.textContent.trim().slice(0,40));
         return {vis,blocks,heads,banner:document.getElementById('mvUniversoBanner').innerText.replace(/\\n/g,' | '),vuoto:document.getElementById('mvUniversoVuoto').hidden?'':document.getElementById('mvUniversoVuoto').innerText}}""")
        print(nome,json.dumps(r,ensure_ascii=False,indent=1))
    pg.screenshot(path='/tmp/claude-0/t/uf_121698.png')
    print(errs)
    b.close()
