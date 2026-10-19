import sys,json
from playwright.sync_api import sync_playwright
from leg_shot import boot
W=int(sys.argv[1]) if len(sys.argv)>1 else 390; H=int(sys.argv[2]) if len(sys.argv)>2 else 844
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,W,H)
    pg.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(200)
    pg.click('.hm-p[data-portal=multiverso]'); pg.wait_for_timeout(1000)
    print('screen',pg.evaluate("()=>tvaAtlas2.stato().screen"), 'nodes',pg.evaluate("()=>document.querySelectorAll('.mp-n').length"))
    pg.screenshot(path=f'/tmp/claude-0/t/m1_{W}.png')
    print(errs)
    b.close()
