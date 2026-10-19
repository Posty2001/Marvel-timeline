from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    q="""()=>{const c=document.querySelector('li#item-125');const t=c.querySelector('.title');const r=t.getBoundingClientRect();return [Math.round(r.right),getComputedStyle(t).whiteSpace,getComputedStyle(t).display,getComputedStyle(c.querySelector('.item-top')).display,getComputedStyle(c.querySelector('.item-body')).minWidth,document.documentElement.scrollWidth,c.className]}"""
    print('full',pg.evaluate(q))
    pg.evaluate("()=>window.marvelEsploraUniverso('uni-earth-828','x')"); pg.wait_for_timeout(300)
    print('filt',pg.evaluate(q))
    print(pg.evaluate("()=>{const c=document.querySelector('li#item-125');return [c.outerHTML.slice(0,900), getComputedStyle(c).display, getComputedStyle(c,'::before').display]}"))
    pg.evaluate("()=>window.marvelUniFiltroReset()")
    pg.evaluate("()=>{document.querySelectorAll('li.card-wrap').forEach(l=>{if(l.id=='item-125')l.setAttribute('data-uf-rel','1')})}")
    b.close()
