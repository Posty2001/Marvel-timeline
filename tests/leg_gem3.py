from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const M=tvaAtlas2.arcModel();const T=id=>tvaIdx.titoli[id].title+' '+id.slice(5);
      return M.list.filter(e=>e.cat==='art'||e.id.startsWith('evt-')||e.id.startsWith('pia-vormir')||e.id==='org-hydra'||e.id==='luo-wakanda').slice(0,40).map(e=>e.id+' | ver: '+e.titles.map(t=>T(t)+'['+(e.why[t]||'')+']').join('; ')+' | UNCONF: '+e.unconf.map(T).join('; ')+' | cited:'+e.cited.join(',')) }""")
    print('\n'.join(r)); print(errs)
    b.close()
