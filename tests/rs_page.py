import sys
from playwright.sync_api import sync_playwright
tab=sys.argv[1]; tag=sys.argv[2]; sel=sys.argv[3] if len(sys.argv)>3 else None; w=int(sys.argv[4]) if len(sys.argv)>4 else 390
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':w,'height':844},is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.evaluate("(t)=>document.getElementById('appTab'+t).click()",tab); pg.wait_for_timeout(900)
    if sel:
        pg.evaluate("(s)=>{const e=document.querySelector(s); if(e) e.scrollIntoView({block:'start'}); }",sel); pg.wait_for_timeout(500)
    pg.screenshot(path=f'/tmp/claude-0/t/rs_{tag}.png'); print(errs); b.close()
