from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(200)
    pg.click('.hm-p[data-portal=multiverso]'); pg.wait_for_timeout(1000)
    r=pg.evaluate("()=>{const e=document.querySelector('.mp-n[data-u=\"uni-earth-199999-mcu\"] .mp-hit').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]}"); print(r)
    print(pg.evaluate("()=>tvaAtlas2.stato().mp.panel"))
    pg.touchscreen.tap(*r); pg.wait_for_timeout(700)
    print(pg.evaluate("()=>[tvaAtlas2.stato().mp.panel,tvaAtlas2.stato().mp.sel,document.querySelectorAll('.mp-panel').length,document.querySelectorAll('.mp-sheet').length]"))
    pg.screenshot(path='shots/dbg.png'); print(errs); b.close()
