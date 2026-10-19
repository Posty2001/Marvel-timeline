from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for cid in ['char-wade-wilson-deadpool','char-charles-xavier','char-aunt-may' ]:
        pg.evaluate("(c)=>tvaGo('char',c)",cid); pg.wait_for_timeout(500)
        print('=====',cid, pg.evaluate("()=>tvaAtlas2.getState().screen"))
        print(pg.evaluate("()=>document.querySelector('.a2-scroll').innerText.slice(0,1400)"))
        pg.screenshot(path='f4_char_%s.png'%cid[5:12])
    print(errs); b.close()
