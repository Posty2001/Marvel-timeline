from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for id in ['uni-fantastic-four-1994','uni-earth-199999-mcu']:
        r=pg.evaluate("""(id)=>{const li=document.getElementById(id);const c=li.querySelector('.detail-panel').innerText.replace(/\\n+/g,' | ').slice(0,700);tvaAtlas2.openUni(id);const a=document.getElementById('atlas2');return {classic:c,native:a.innerText.replace(/\\n+/g,' | ').slice(0,1500),rows:a.querySelectorAll('.a2-prow,.a2-row').length,more:[...a.querySelectorAll('.a2-more,.a2-sec h3,.a2-h3')].map(x=>x.textContent)}}""",id)
        print(id);print(r['classic']);print('--');print(r['native']);print(r['rows'],r['more']);print()
    b.close()
