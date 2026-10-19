from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for i in ['chrono-simbionte-venom','chrono-tva','chrono-battleworld','tree-asgard']:
        print(i, pg.evaluate("(i)=>document.getElementById(i).outerHTML.replace(/\\s+/g,' ').slice(0,2600)",i)); print()
    for t in ['Timeline delle Incursioni','Percorso: Maratona Weekend']:
        print(t, pg.evaluate("""(t)=>{const d=[...document.querySelectorAll('#tvaArchivesOverlayEl details.card')].find(x=>(x.querySelector('summary .title')?.textContent||'').startsWith(t));return d.outerHTML.replace(/\\s+/g,' ').slice(0,3800)}""",t)); print()
    b.close()
