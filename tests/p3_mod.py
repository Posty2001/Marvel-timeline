from leg_shot import *
import json
from collections import Counter
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    uids=pg.evaluate("()=>Object.keys(tvaAtlas2.ext.api.UNI)")
    res={}
    for u in uids:
        pg.evaluate("(u)=>tvaAtlas2.ext.api.nav('uni',{uid:u})",u); pg.wait_for_timeout(150)
        res[u]=pg.evaluate("()=>({h:[...document.querySelectorAll('.a2-scroll h3')].map(e=>e.textContent.replace(/\\s*\\(.*$/,'')),descr:!!document.querySelector('.a2-descr'),guida:!!document.querySelector('.a2-hero .a2-note')})")
    c=Counter(); 
    for u,r in res.items():
        for h in r['h']: c[h]+=1
    print(c); print('descr',sum(r['descr'] for r in res.values()),'nella guida',sum(r['guida'] for r in res.values()))
    empty=[u for u,r in res.items() if len(r['h'])<=2]; print('quasi vuoti',len(empty),[e[:30] for e in empty])
    # eventi archivio per universo?
    ev=pg.evaluate("()=>{const a=tvaAtlas2.ext.api;return Object.keys(a.IDX).join(',')}"); print(ev)
    print(errs); b.close()
