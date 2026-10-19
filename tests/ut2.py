from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('universeTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(900)
    pg.evaluate("()=>document.querySelector('.a2-ut-bar').scrollIntoView()"); pg.wait_for_timeout(200); pg.screenshot(path='g_ut1.png')
    pg.click('.a2-ut-j >> nth=4'); pg.wait_for_timeout(900); pg.screenshot(path='g_ut2.png')
    print(pg.evaluate("()=>document.querySelector('.universe-timeline-overlay .mg-scroll').scrollLeft"),errs); b.close()
