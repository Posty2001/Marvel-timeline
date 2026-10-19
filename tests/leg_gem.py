from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('reliquiario',{arc:'art',eid:null})"); pg.wait_for_timeout(800)
    pg.screenshot(path='leg_reliq0.png')
    ids=pg.evaluate("()=>[...document.querySelectorAll('[data-gem]')].map(b=>b.dataset.gem)"); print(ids)
    for i in ids:
        pg.evaluate("(i)=>document.querySelector('[data-gem=\"'+i+'\"]').click()",i); pg.wait_for_timeout(200)
        r=pg.evaluate("""()=>{const p=document.querySelector('.a2-rel-panel');return {h:p.querySelector('h3')?.textContent,d:(p.querySelector('.a2-descr2')||{}).textContent,t:[...p.querySelectorAll('ol li')].map(l=>l.textContent.replace(/\\s+/g,' ').trim().slice(0,50)),c:[...p.querySelectorAll('.a2-chips button, .a2-chips a, button[data-go^=char]')].map(x=>x.textContent.trim())}}""")
        print(json.dumps(r,ensure_ascii=False)[:1100]); print()
    pg.evaluate("(i)=>document.querySelector('[data-gem]').click()",ids[0]); pg.wait_for_timeout(300)
    pg.screenshot(path='leg_reliq1.png',full_page=False)
    b.close()
