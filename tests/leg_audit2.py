from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const o=id=>document.getElementById(id);
      const pr=s=>s.length>1400?s.slice(0,1400)+'…':s;
      return {kang:pr(o('chrono-kang').outerHTML), tree:pr(o('tree-ff').outerHTML), treeN:['tree-ff','tree-asgard','tree-wakanda','tree-stark'].map(i=>i+':'+o(i).innerText.length),
       chrN:[...document.querySelectorAll('[id^=chrono-]')].map(e=>e.id+':'+e.innerText.length+':'+e.querySelectorAll('a,button,[data-go],[onclick]').length)}}""")
    for k,v in r.items(): print(k,v); print()
    cards=pg.evaluate("""()=>{const o=document.getElementById('tvaArchivesOverlayEl');const out={};
      for(const t of ['Timeline delle Incursioni','Percorso: Maratona Weekend','Chi manca ancora: tutto ciò che non è mai apparso','Chi è più forte?','Cronologie Personaggio']){
        const d=[...o.querySelectorAll('details.card')].find(x=>(x.querySelector('summary .title')?.textContent||'').startsWith(t)); out[t]=d?{len:d.innerText.length,head:d.innerText.slice(0,350),inter:d.querySelectorAll('button,a,input,[data-go]').length}:null}
      return out}""")
    for k,v in cards.items(): print(k,json.dumps(v,ensure_ascii=False)); print()
    b.close()
