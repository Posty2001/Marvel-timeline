import sys
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
tag=sys.argv[1] if len(sys.argv)>1 else 'a'
vw=(int(sys.argv[2]),int(sys.argv[3])) if len(sys.argv)>3 else (390,844)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':vw[0],'height':vw[1]},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(800)
    pg.screenshot(path=f'/tmp/claude-0/t/rs_{tag}_home.png')
    for t in ['Timeline','Atlante','Missioni','Tessera','Friends']:
        pg.evaluate("(t)=>document.getElementById('appTab'+t).click()",t); pg.wait_for_timeout(900)
        pg.screenshot(path=f'/tmp/claude-0/t/rs_{tag}_{t}.png')
        print(t, pg.evaluate("()=>[getComputedStyle(document.getElementById('appTabbar')).display, document.documentElement.scrollWidth, innerWidth]"))
    print(errs); b.close()
