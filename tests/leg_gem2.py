from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>[...document.querySelectorAll('#tvaArchivesOverlayEl li[id^="art-"]')].map(li=>({id:li.id,f:Object.fromEntries([...li.querySelectorAll('.detail-row')].filter(r=>!r.classList.contains('tva-row')).map(r=>[r.querySelector('.detail-k')?.textContent.trim(),r.querySelector('.detail-v')?.textContent.trim()]))}))""")
    for x in r[:8]: print(json.dumps(x,ensure_ascii=False)); print()
    # gemme chrono
    c=pg.evaluate("()=>document.getElementById('chrono-gemme-dell-infinito')?.innerText.slice(0,1800)"); print(c)
    # classic card Le Gemme dell'Infinito
    g=pg.evaluate("""()=>{const d=[...document.querySelectorAll('#tvaArchivesOverlayEl details.card')].find(x=>/Le Gemme/.test(x.querySelector('summary .title')?.textContent||''));return d?d.innerText.slice(0,1500):null}"""); print(g)
    b.close()
