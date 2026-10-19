from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const A=tvaAtlas2.ext.api,I=A.IDX;const T=Object.entries(I.titoli);const g=k=>T.filter(([i,e])=>(e.kind+(e.variant?'+v':''))===k).slice(0,6).map(([i,e])=>i+':'+e.title);
      const ph=Object.keys(A.PTIPO).filter(k=>A.PTIPO[k]==='segnaposto');
      return {p4:g('p4'),anim:g('anim'),v:g('item+v'),ph, ptipi:Object.values(A.PTIPO).reduce((o,t)=>(o[t]=(o[t]||0)+1,o),{}),
        graphUni:(document.getElementById('multiverseGraphData')||{}).id}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
