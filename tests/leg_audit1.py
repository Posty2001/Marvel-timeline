from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('tvaArchivesToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(1200)
    r=pg.evaluate("""()=>{const o=document.getElementById('tvaArchivesOverlayEl');
     const tabs=[...o.querySelectorAll('input[name],input[id^=dbtab]')].map(i=>i.id+':'+(i.type)).slice(0,30);
     const cards=[...o.querySelectorAll('details.card > summary .title')].map(e=>e.textContent.trim().slice(0,60));
     const labels=[...o.querySelectorAll('label[for^=dbtab]')].map(l=>l.getAttribute('for')+'='+l.textContent.trim().slice(0,30));
     const chr=[...o.querySelectorAll('[data-target]')].map(e=>e.dataset.target+'='+e.textContent.trim().slice(0,30));
     const ids=[...o.querySelectorAll('[id]')].map(e=>e.id).slice(0,100);
     return {tabs,cards,labels,chr,ids,len:o.innerHTML.length}}""")
    for k,v in r.items(): print(k,v)
    b.close()
