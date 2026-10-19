import sys
from playwright.sync_api import sync_playwright
F=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.set_default_timeout(8000)
    pg.goto(F); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.getElementById('appTabMissioni').click()"); pg.wait_for_timeout(1200)
    print(pg.evaluate("()=>[document.getElementById('missioneSagaTesto').textContent,document.getElementById('missioneTematicaTesto').textContent,typeof marvelGetAltTimelineData]"))
    pg.evaluate("()=>{const c=document.querySelector('#item-001 .watch-check');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    print(pg.evaluate("()=>[document.getElementById('missioneSagaTesto').textContent,document.getElementById('missioneTematicaTesto').textContent]"))
    b.close()
