from playwright.sync_api import sync_playwright
from leg_shot import boot
import json,collections
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const k={};document.querySelectorAll('#tvaArchivesOverlayEl li[id^="uni-"]').forEach(li=>{li.querySelectorAll('.detail-row').forEach(r=>{const t=(r.querySelector('.detail-k')||{}).textContent;k[t.trim()]=(k[t.trim()]||0)+1})});
      const li=document.getElementById('uni-earth-199999-mcu');return {k,html:li.querySelector('.detail-panel').innerHTML.replace(/\\s+/g,' ').slice(0,1800)}}""")
    print(json.dumps(r['k'],ensure_ascii=False)); print(r['html'])
    b.close()
