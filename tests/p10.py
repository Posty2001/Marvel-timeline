import json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const I=tvaIdx,UM=tvaUniverse;const o=[];
      Object.values(I.titoli).forEach(t=>{if(t.kind!=='item')return;const u=UM.uscita(t.num);const tx=t.li.textContent.replace(/\\s+/g,' ');
        const m=tx.match(/.{0,50}(previst|annunciat|TBD|stima|stimat|uscir|in arrivo|in produzione|data di uscita|ufficial).{0,60}/ig);
        if((u&&u.data&&u.data>'2026-06-30')||!u||!u.data||(m&&m.length)) o.push([t.num,t.title,u&&u.data,u&&u.precisione,(m||[]).slice(0,3)])});
      return o}""")
    for x in r: print(json.dumps(x,ensure_ascii=False))
    b.close()
