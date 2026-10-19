from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaGo('arc','org:org-shield')"); pg.wait_for_timeout(600)
    print(pg.evaluate("()=>tvaAtlas2.getState().screen+' '+tvaAtlas2.getState().eid"))
    print(pg.evaluate("()=>document.querySelector('.a2-scroll').innerText.slice(0,2200)"))
    pg.screenshot(path='f4_org1.png')
    print(errs); b.close()
