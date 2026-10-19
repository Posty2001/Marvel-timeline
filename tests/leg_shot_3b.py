import sys
from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8125/index.html'
def boot(b,w=390,h=844):
    ctx=b.new_context(viewport={'width':w,'height':h},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); pg=ctx.new_page(); pg.set_default_timeout(8000)
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.click('#appTabAtlante'); pg.wait_for_timeout(700)
    return ctx,pg,errs
if __name__=='__main__':
    with sync_playwright() as p:
        b=p.chromium.launch(); ctx,pg,errs=boot(b)
        steps=[('graph',"tvaAtlas2&&document.getElementById('multiverseGraphToggle')"),]
        for name,tog in [('graph','multiverseGraphToggle'),('utl','universeTimelineToggle'),('atl','altTimelineToggle'),('rel','relationshipGraphToggle'),('kang','kangTvaGraphToggle'),('classic','tvaArchivesToggle')]:
            pg.evaluate("()=>{marvelChiudiOverlay()}"); pg.wait_for_timeout(200)
            pg.evaluate("(t)=>{const c=document.getElementById(t);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",tog); pg.wait_for_timeout(1200)
            pg.screenshot(path=f'leg_{name}.png')
            print(name, pg.evaluate("()=>({shell:getComputedStyle(document.getElementById('tvaShell')).display,tab:getComputedStyle(document.getElementById('appTabbar')).display,sw:document.documentElement.scrollWidth})"))
        print(errs); b.close()
