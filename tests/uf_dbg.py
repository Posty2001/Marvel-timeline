from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    print('base sw',pg.evaluate("document.documentElement.scrollWidth"))
    print(pg.evaluate("""()=>{const m=JSON.parse(document.getElementById('mvMapData').textContent).universi;return ['uni-earth-828','uni-tva-fuori-dal-tempo','uni-rami-di-what-if'].map(k=>[k,m[k].titoliIds,m[k].natura])}"""))
    print(pg.evaluate("()=>{const c=document.querySelector('[data-item=\"133\"]');return [c.dataset.uni,c.className,c.id]}"))
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-828','x')"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const v=[...document.querySelectorAll('li.card-wrap')].filter(l=>!l.closest('.tva-archives-overlay')&&l.offsetParent!==null).map(l=>l.dataset.item);return [v,document.getElementById('mvUniversoVuoto').hidden,document.getElementById('mvUniversoVuoto').innerText, document.documentElement.scrollWidth]}"""))
    print(pg.evaluate("""()=>{const W=innerWidth;return [...document.querySelectorAll('body *')].filter(e=>e.offsetParent!==null&&e.getBoundingClientRect().right>W+2&&!e.closest('.sidebar,.tva-archives-overlay')).slice(0,8).map(e=>e.tagName+'#'+e.id+'.'+(e.className+'').slice(0,30)+' '+Math.round(e.getBoundingClientRect().right))}"""))
    b.close()
