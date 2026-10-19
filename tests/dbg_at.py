import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto('file://'+f); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true;document.getElementById('altTimelineToggle').checked=true}")
    pg.click('.at-mode-btn[data-mode="custom"]'); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>{const r=[...document.querySelectorAll('#atList .at-row')].find(e=>/Logan/.test(e.textContent)&&!/Wolv/.test(e.textContent));const n=r.getAttribute('data-num');r.click();return [n,!!document.getElementById('item-'+n)]}"""))
