from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const M=tvaAtlas2.arcModel();return {mis:M.cat.mis.map(e=>({id:e.id,name:e.name,chars:e.chars.length,arcs:e.arcs.length,tit:e.titles.length,unis:e.unis.length,lim:!!e.limited,s:e.sintesi,def:(e.ex[0]||{}).txt})),gaps:M.misGaps}}""")
    import json; print(json.dumps(r,ensure_ascii=False,indent=1)); print(errs); b.close()
