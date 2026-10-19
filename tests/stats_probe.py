from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
      const E=tvaAtlas2.ext||{}; const keys=Object.keys(E);
      const API=E.api||{}; 
      const I=API.IDX||null; const U=API.UNI||null;
      const out={extkeys:keys,apikeys:Object.keys(API)};
      if(I){const T=Object.values(I.titoli);const by={};T.forEach(e=>{const k=(e.kind||'?')+(e.variant?'+variant':'');by[k]=(by[k]||0)+1});out.titoli=by;out.total=T.length;
        out.ids=Object.keys(I.titoli).slice(0,5);
        const P=Object.values(I.personaggi);out.pers=P.length;}
      if(U){out.uni=Object.keys(U).length;out.uniNames=Object.keys(U)}
      return out}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:3000]); b.close()
