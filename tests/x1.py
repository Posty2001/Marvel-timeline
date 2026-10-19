import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const o={};
     o.dom=[...document.querySelectorAll('#sec-1d ~ ul.items:first-of-type li.card-wrap, h3#sec-1d + ul.items li.card-wrap')].map(l=>l.dataset.item);
     const alt=marvelGetAltTimelineData(); o.altRec=alt.map((a,i)=>[i,a.num,a.title]).filter(x=>x[1]>=11&&x[1]<=24||x[1]==117);
     o.allDomOrder=[...document.querySelectorAll('li.card-wrap[data-item]')].map(l=>l.dataset.item).join(',').slice(0,900);
     o.hdr=[...document.querySelectorAll('#item-012 .card-head, #item-012 summary')].slice(0,2).map(e=>e.textContent.replace(/\\s+/g,' ').slice(0,200));
     return o}""")
    print(json.dumps(r,ensure_ascii=False,indent=0)[:3500]); b.close()
