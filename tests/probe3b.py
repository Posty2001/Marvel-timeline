import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const m=window.tvaUniverse;const ids=m.ids();const g=m.get(ids[3]);
    const sh=o=>{const r={};for(const k in o){const v=o[k];r[k]=Array.isArray(v)?'['+v.length+']'+JSON.stringify(v[0]||'').slice(0,160):(typeof v==='object'&&v?JSON.stringify(v).slice(0,160):v)}return r};
    const MV=JSON.parse(document.getElementById('mvMapData').textContent);
    return {g:sh(g),link:m.links()[0],spec:m.special().map(s=>sh(s)),famKeys:Object.keys(MV.famiglie||{}),fam0:JSON.stringify(Object.values(MV.famiglie)[0]).slice(0,300),uk:sh(MV.universi[ids[3]]),mkeys:Object.keys(m),stati:m.stati,tipi:m.tipi}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:6000])
