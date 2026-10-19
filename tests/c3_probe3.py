import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
 const li=document.getElementById('anim-theavengersearthsmig10'); const o={};
 o.exists=!!li; o.text=li?li.innerText.slice(0,400):null; o.cls=li?li.className:null;
 o.attrs=li?[...li.attributes].map(a=>a.name+'='+a.value.slice(0,40)):null;
 const all=[...document.querySelectorAll('[id^="anim-"]')].filter(e=>e.tagName==='LI'||e.classList.contains('card-wrap')||e.classList.contains('anim-card'));
 o.n_anim=all.length; o.samples=all.slice(0,6).map(e=>e.id+' :: '+e.innerText.replace(/\\s+/g,' ').slice(0,160));
 // anni nei titoli animati
 const withYear=all.filter(e=>/\\b(19|20)\\d{2}\\b/.test(e.innerText.slice(0,200))).length; o.anim_with_year=withYear;
 // timeline principale / universo / cronologie tematiche
 o.parte1=!!document.getElementById('parte1'); o.items=document.querySelectorAll('li[id^="item-"]').length;
 o.chrono=[...document.querySelectorAll('[data-target^="chrono-"]')].map(e=>e.dataset.target);
 o.chrono_cards=[...document.querySelectorAll('[id^="chrono-"]')].map(e=>e.id+'|'+e.tagName+'|'+(e.innerText||'').replace(/\\s+/g,' ').slice(0,80));
 o.ut=document.querySelector('.universe-timeline-overlay')?document.querySelector('.universe-timeline-overlay').innerText.replace(/\\s+/g,' ').slice(0,500):null;
 o.ut_html_len=document.querySelector('.universe-timeline-overlay')?document.querySelector('.universe-timeline-overlay').innerHTML.length:0;
 return o}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)[:5000]); b.close()
