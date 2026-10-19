from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8765/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page()
    pg.on('pageerror',lambda e:print('ERR',e)); pg.on('console',lambda m:print('C',m.text[:200]))
    pg.goto(U); pg.wait_for_timeout(2500)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}")
    for i in range(5): pg.evaluate("document.getElementById('appTabHome').click()"); pg.wait_for_timeout(80)
    print(pg.evaluate("!!document.getElementById('tvaDbgPanel')"), pg.evaluate("localStorage.getItem('tva-debug-layout')"))
    print(pg.evaluate("document.getElementById('appTabHome').getBoundingClientRect().width"))
    # click via real mouse
    for i in range(5): pg.mouse.click(30,820); pg.wait_for_timeout(80)
    print(pg.evaluate("!!document.getElementById('tvaDbgPanel')"))
    b.close()
