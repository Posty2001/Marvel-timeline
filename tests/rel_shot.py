from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    print(pg.evaluate("()=>Object.keys(tvaAtlas2.ext.api.SEZ||{})"))
    pg.evaluate("()=>tvaAtlas2.ext.api.run?0:0")
    # apri Reliquiario tramite UI
    pg.evaluate("()=>{const a=tvaAtlas2.ext.api;a.nav('reliquiario')}"); pg.wait_for_timeout(900)
    pg.screenshot(path='r_1.png')
    print(pg.evaluate("()=>({scr:tvaAtlas2.state&&tvaAtlas2.state.scr,t:(document.querySelector('#atlas2 h1,#atlas2 .a2-title')||{}).textContent})"))
    g=pg.query_selector_all('#atlas2 .a2-gem'); print(len(g))
    if g: g[0].click(); pg.wait_for_timeout(700); pg.evaluate("()=>document.querySelector('.a2-rel-panel')&&document.querySelector('.a2-rel-panel').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path='r_2.png')
    print(errs); b.close()
