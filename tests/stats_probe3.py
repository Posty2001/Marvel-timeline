from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const A=tvaAtlas2.ext.api,I=A.IDX;const t=Object.values(I.titoli)[0];
      const uk=Object.keys(t);
      const U=A.UNI; const sample=U[Object.keys(U)[0]];
      return {tkeys:uk,ukeys:Object.keys(sample),sample:JSON.stringify(sample).slice(0,300)}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
