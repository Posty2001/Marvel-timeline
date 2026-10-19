from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    print(pg.evaluate("()=>[String(mvNavigateTo).slice(0,400), String(mvNavigate).slice(0,200)]"))
    print(pg.evaluate("()=>{try{return tvaGo('char','char-thor')}catch(e){return String(e)}}"), pg.evaluate("()=>[tvaAtlas2.openChar&&1, atlas2Toggle.checked, tvaAtlas2.ext.api.ST.screen]"))
    b.close()
