import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const I=tvaIdx;const an=Object.values(I.titoli).filter(t=>t.kind==='anim');
      const atl=JSON.parse(document.getElementById('atlasData').textContent);const A=new Set(atl.animate.map(a=>a.id));
      const noU=an.filter(t=>!(t.unis||[]).length);
      return {n:an.length,inAtl:an.filter(t=>A.has(t.id)).length,atl:atl.animate.length,extra:an.filter(t=>!A.has(t.id)).map(t=>t.id+'|'+t.title+'|'+(t.unis||[]).length+'|'+t.li.className),noU:noU.length,
        dup:an.map(t=>t.id).filter((x,i,a)=>a.indexOf(x)!==i)}}""")
    print(json.dumps(r,ensure_ascii=False,indent=0)); 
    pg.evaluate("()=>{tvaAtlas2.enter()}"); pg.wait_for_timeout(500)
    print(pg.evaluate("()=>Object.values(tvaIdx.titoli).filter(t=>t.kind==='anim').length"))
    b.close()
