import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const I=tvaIdx;const an=Object.values(I.titoli).filter(t=>t.kind==='anim');
      const rows=t=>Array.from(t.li.querySelectorAll('.detail-row')).map(r=>[r.querySelector('.detail-k')?.textContent.trim(),r.querySelector('.detail-v')?.textContent.trim().slice(0,70)]);
      const o={sample:rows(an[0]),sample2:rows(an[5]),list:an.map(t=>[t.id,t.title,t.unis.length,(rows(t).find(r=>/AMBIENT/i.test(r[0]))||[])[1]]),
       ks:[...new Set(an.flatMap(t=>rows(t).map(r=>r[0])))],
       itemKs:[...new Set(Object.values(I.titoli).filter(t=>t.kind==='item').slice(0,5).flatMap(t=>rows(t).map(r=>r[0])))],
       nounassigned_items:Object.values(I.titoli).filter(t=>t.kind==='item'&&!t.unis.length).map(t=>t.id+'|'+t.title),
       tl_ids:(()=>{const s=new Set();document.querySelectorAll('#altTimelineToggle ~ * [data-num]').forEach(x=>s.add(x.dataset.num));return s.size})(),
       uscitaF:tvaUniverse.uscita('139'),
       opere:Object.keys(JSON.parse(document.querySelector('script#tvaAtlasData,script[type="application/json"]')?.textContent||'{}')).slice(0,3)};
      return o}""")
    print(json.dumps(r,ensure_ascii=False,indent=0)[:5500]); b.close()
