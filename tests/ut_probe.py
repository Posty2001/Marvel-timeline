from g_shot import open_t
from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    open_t(pg,'universeTimelineToggle')
    print(pg.evaluate("""()=>{const d=[...document.querySelectorAll('.ut-dot')].map(x=>x.getBoundingClientRect().x+x.getBoundingClientRect().width/2-document.querySelector('.ut-svg').getBoundingClientRect().x);const sc=document.querySelector('.universe-timeline-overlay .mg-scroll');return {minx:Math.min(...d),maxx:Math.max(...d),sl:sc.scrollLeft,cw:sc.clientWidth,sw:sc.scrollWidth,ml:[...document.querySelectorAll('.ut-marker-label')].map(m=>m.textContent)}}"""))
    pg.evaluate("()=>document.querySelector('.ut-body').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path='g_ut1.png')
    b.close()
