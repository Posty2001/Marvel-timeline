import json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
 const all=[...document.querySelectorAll('[id^="anim-"].card-wrap')];
 return all.map(e=>{const t=e.textContent.replace(/\\s+/g,' ').trim();return [e.id,e.dataset.uni,t.slice(0,170)]})}""")
    for x in r[:40]: print(x)
    # item cards: struttura di un item (anno, periodo)
    r2=pg.evaluate("""()=>{const li=document.getElementById('item-098');return li.textContent.replace(/\\s+/g,' ').slice(0,700)}"""); print(r2)
    b.close()
