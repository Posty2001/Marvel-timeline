from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':320,'height':640})
    pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300); pg.click('#appTabAtlante'); pg.wait_for_timeout(700)
    print(pg.evaluate("()=>['.sidebar-open-btn','.a2-ttl','.a2-top','.a2-exit'].map(s=>[s,!!document.querySelector(s)])"))
    b.close()
