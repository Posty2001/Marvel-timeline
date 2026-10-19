from leg_shot import *
O='/home/claude/outputs/f3_base_'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    A="tvaAtlas2.ext.api"
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('universi')"); pg.wait_for_timeout(900); pg.screenshot(path=O+'universi.png')
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('uni',{uid:'uni-earth-10005-fox-verse'})"); pg.wait_for_timeout(900); pg.screenshot(path=O+'dossier_fox.png')
    pg.evaluate("()=>{document.querySelector('.a2-scroll').scrollTop=700}"); pg.wait_for_timeout(300); pg.screenshot(path=O+'dossier_fox_2.png')
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('cronologie')"); pg.wait_for_timeout(900); pg.screenshot(path=O+'cronologie.png')
    pg.evaluate("()=>tvaAtlas2.ext.api.run(['tog','multiverseGraphToggle'])"); pg.wait_for_timeout(1200); pg.screenshot(path=O+'mv_overlay.png')
    pg.evaluate("()=>{const e=document.getElementById('mvMapOldGraphBtn');e&&e.click()}"); pg.wait_for_timeout(800); pg.screenshot(path=O+'mv_graph_old.png')
    pg.evaluate("()=>marvelChiudiOverlay()"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{const c=document.getElementById('universeTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(1000); pg.screenshot(path=O+'ut_overlay.png')
    pg.evaluate("()=>marvelChiudiOverlay()"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{const c=document.getElementById('altTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(1000); pg.screenshot(path=O+'alt_overlay.png')
    print(errs); b.close()
