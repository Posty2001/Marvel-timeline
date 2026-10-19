from playwright.sync_api import sync_playwright
S="()=>({atlas:document.getElementById('atlas2').getClientRects().length>0,intro:getComputedStyle(document.getElementById('intro')).display,home:getComputedStyle(document.querySelector('.home-hub')).display,hh:homeHubExited.checked,j:journeyStarted.checked,tabs:getComputedStyle(document.getElementById('appTabbar')).display,len:history.length})"
def run(act):
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1500)
        pg.evaluate("()=>tvaIntroScenes.go(3)"); pg.wait_for_timeout(1500); pg.click('#lmTvaPortal'); pg.wait_for_timeout(900)
        pg.wait_for_function("()=>!document.getElementById('onboardingStep2').hidden"); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(1200)
        print(act,'prima',pg.evaluate(S))
        if act=='a2-back': pg.click('.a2-back')
        elif act=='a2-exit': pg.click('.a2-exit')
        else: pg.go_back()
        pg.wait_for_timeout(900); print(act,'dopo ',pg.evaluate(S),errs)
        pg.screenshot(path='/tmp/claude-0/t/shots_leg/portale_back_%s.png'%act)
        b.close()
for a in ('a2-back','a2-exit','history'): run(a)
