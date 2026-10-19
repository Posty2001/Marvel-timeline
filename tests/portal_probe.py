from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8124/index.html'); pg.wait_for_timeout(1500)
    pg.evaluate("()=>tvaIntroScenes.go(3)"); pg.wait_for_timeout(1500); pg.click('#lmTvaPortal'); pg.wait_for_timeout(900)
    pg.wait_for_function("()=>!document.getElementById('onboardingStep2').hidden"); pg.click('#onboardingStartBtn'); pg.wait_for_timeout(1200)
    print(pg.evaluate("()=>[...document.querySelectorAll('button,a,label')].filter(b=>b.getClientRects().length&&b.getBoundingClientRect().top<130).map(b=>b.tagName+'#'+b.id+'.'+b.className+'|'+(b.getAttribute('aria-label')||b.textContent).trim().slice(0,30))"))
    print(pg.evaluate("()=>({atlas:[...document.querySelectorAll('[id*=tlas]')].filter(e=>e.getClientRects().length).map(e=>e.id),intro:getComputedStyle(document.getElementById('intro')).display,hash:location.hash,j:journeyStarted.checked,hh:homeHubExited.checked})"))
    pg.screenshot(path='/tmp/claude-0/t/shots_leg/portale_atlas_390.png')
    b.close()
