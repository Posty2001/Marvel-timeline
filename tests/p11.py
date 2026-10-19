import json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const I=tvaIdx;const o={};
      ['item-027','item-131','item-132','item-134','item-135','item-136','item-137','item-138','item-139','item-133','item-128','item-051'].forEach(id=>{const t=I.titoli[id];const x=t.li;
       o[id]=[x.textContent.replace(/\\s+/g,' ').slice(0,230), Array.from(x.querySelectorAll('[class*=status],[class*=badge],[class*=stato],.tag,.pill')).slice(0,4).map(e=>e.className+':'+e.textContent.trim().slice(0,30))]});
      // all distinct status-like emoji tokens across items
      const c={};Object.values(I.titoli).forEach(t=>{const m=t.li.textContent.replace(/\\s+/g,' ').match(/(📢 Annunciato|📅[^A-Z]{0,25}|🆕[^A-Z]{0,20}|⏳[^A-Z]{0,20}|In produzione|In arrivo|già uscit[ao]|Previst[oa])/g);(m||[]).forEach(k=>c[k]=(c[k]||0)+1)});o.cnt=c;return o}""")
    print(json.dumps(r,ensure_ascii=False,indent=0)[:5000]); b.close()
