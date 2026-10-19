import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const s=document.getElementById('atlasData').textContent;const atl=JSON.parse(s);const t={},r={};
     atl.opere.forEach(o=>{t[o.tipo]=(t[o.tipo]||0)+1;r[o.ruolo]=(r[o.ruolo]||0)+1});
     const alt=marvelGetAltTimelineData();
     return {len:s.length,tipi:t,ruoli:r,alt0:alt[0],altTags:[...new Set(alt.map(a=>a.tag))],icons:[...new Set(alt.map(a=>a.icon))],nums:alt.map(a=>a.num).slice(-4),
      varianti:atl.opere.filter(o=>o.ruolo!=='primario').map(o=>o.id+o.ruolo).slice(0,10)}}""")
    print(json.dumps(r,ensure_ascii=False)); b.close()
