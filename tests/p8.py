import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const I=tvaIdx;const o={keys:Object.keys(I)};
      const an=Object.values(I.titoli).filter(t=>t.kind==='anim');o.nanim=an.length;
      o.a0=an[0]&&Object.keys(an[0]);o.a0v=an[0]&&Object.fromEntries(Object.entries(an[0]).filter(([k,v])=>typeof v!=='object'));
      const li=an[0].li; o.html=li.innerText.slice(0,500); o.cls=li.className; o.id=li.id;
      o.fnames=Object.keys(I).filter(k=>typeof I[k]==='function');
      const t0=Object.values(I.titoli).find(t=>t.kind==='item'); o.i0=Object.fromEntries(Object.entries(t0).filter(([k,v])=>typeof v!=='object'));
      o.nitems=Object.values(I.titoli).filter(t=>t.kind==='item').length;
      return o}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:3000]); b.close()
