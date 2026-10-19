from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1500)
    pg.screenshot(path='/home/claude/outputs/fase2_home_attuale_390_top.png')
    pg.screenshot(path='/home/claude/outputs/fase2_home_attuale_390_full.png',full_page=False)
    h=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return [s.scrollHeight,s.clientHeight]}"); print(h)
    for i,y in enumerate((800,1600)):
        pg.evaluate("(y)=>{document.querySelector('.a2-scroll').scrollTop=y}",y); pg.wait_for_timeout(400); pg.screenshot(path=f'/home/claude/outputs/fase2_home_attuale_390_p{i+2}.png')
    print(errs); b.close()
