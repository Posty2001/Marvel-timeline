from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    A="tvaAtlas2.ext.api"
    keys=pg.evaluate("()=>tvaAtlas2.ext.api.GRP.flatMap(g=>g.items.map(i=>i.k))")
    out=[]
    for k in keys+['__rel']:
        pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(250)
        if k=='__rel': pg.evaluate("()=>tvaAtlas2.ext.api.run(['rel'])")
        else: pg.evaluate("(k)=>tvaAtlas2.ext.api.go?tvaAtlas2.ext.api.SEZ&&0:0",k); pg.evaluate("(k)=>{const a=tvaAtlas2.ext.api;const s=a.SEZ[k];a.run(s.act)}",k)
        pg.wait_for_timeout(900)
        r=pg.evaluate("()=>({st:tvaAtlas2.ext.api.ST.screen,ttl:(document.querySelector('.a2-ttl')||{}).innerText,h:(document.querySelector('.a2-head h2,.a2-cover-t h1,h1,h2')||{}).innerText,atlas:document.getElementById('atlas2').getClientRects().length>0,ov:['multiverseGraphToggle','tvaArchivesToggle'].map(i=>document.getElementById(i).checked)})")
        out.append((k,r))
        if k=='multiverso': pg.evaluate("()=>marvelChiudiOverlay()"); pg.wait_for_timeout(300)
    for k,r in out: print(k,r)
    print(errs); b.close()
