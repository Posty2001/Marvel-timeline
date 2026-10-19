import sys
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/'+(sys.argv[1] if len(sys.argv)>1 else 'index.html')
JS="""()=>{const W=document.documentElement.clientWidth;
const bad=[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);return r.width>0&&r.right>W+1&&cs.visibility!=='hidden'&&cs.display!=='none'&&!e.closest('[hidden]')}).slice(0,8).map(e=>(e.id||e.className||e.tagName)+':'+Math.round(e.getBoundingClientRect().right));
return {sw:document.documentElement.scrollWidth,bsw:document.body.scrollWidth,W,bad}}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,375,390,430):
        pg=b.new_page(viewport={'width':w,'height':760}); pg.goto(F); pg.wait_for_timeout(600)
        print(w,'init',pg.evaluate(JS))
        pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(500)
        print(w,'app',pg.evaluate(JS))
        pg.close()
    b.close()
