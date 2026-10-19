from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const out={};for(const cid of ['char-charles-xavier','char-xavier','char-xavier-giovane-e-anziano']){const c=tvaIdx.personaggi[cid];out[cid]={name:c.name,apps:c.apps.map(a=>{const t=tvaIdx.titoli[a];return t?[a,t.title,marvelNumeroVisibile(String(a).replace('item-',''))]:a})}};
      const L=document.getElementById('char-charles-xavier');out.txt=L.textContent.replace(/\\s+/g,' ').slice(0,900);return out}""")
    print(json.dumps(r,ensure_ascii=False,indent=0)[:2600])
