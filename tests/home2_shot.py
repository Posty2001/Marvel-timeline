from leg_shot import *
import sys
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(1800)
    H=pg.evaluate("()=>{const s=document.querySelector('.a2-scroll');return [s.scrollHeight,s.clientHeight]}"); print(H)
    n=0; y=0
    while True:
        pg.evaluate("(y)=>{document.querySelector('.a2-scroll').scrollTop=y}",y); pg.wait_for_timeout(500)
        pg.screenshot(path=f'/home/claude/outputs/fase2_home_390_{n}.png'); n+=1
        if y+H[1]>=H[0]-2: break
        y+=700
    print(n,errs); b.close()
