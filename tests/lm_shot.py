import sys
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
with sync_playwright() as p:
    b=p.chromium.launch()
    for vw in [(390,844),(320,568),(375,667)]:
        ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(U); pg.wait_for_timeout(3200)
        t=str(vw[0])
        pg.screenshot(path=f'/tmp/claude-0/t/lm_{t}_a.png')
        for i,y in enumerate([0.9,1.8,2.7]):
            pg.evaluate("(y)=>{const s=document.getElementById('lmScroll');s.style.scrollBehavior='auto';s.scrollTop=s.clientHeight*y}",y); pg.wait_for_timeout(400)
            pg.screenshot(path=f'/tmp/claude-0/t/lm_{t}_{i+1}.png')
        print(t,errs, pg.evaluate("()=>[document.documentElement.scrollWidth,document.getElementById('lmScroll').scrollWidth,document.getElementById('lmScroll').clientWidth,document.getElementById('lmScroll').scrollHeight]"))
    b.close()
