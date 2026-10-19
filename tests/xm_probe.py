import sys,json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
      const UM=tvaUniverse, uid='uni-earth-10005-fox-verse';
      const g=UM.get(uid);
      const nm=e=>e.num+':'+(e.title||'').slice(0,18);
      const D=tvaTime.data();
      return {
        titoli:g.titoli.map(nm), appart:g.appartenenza.map(nm), cross:g.crossover.map(nm),
        gi:Object.values(D.E).filter(e=>/^(0(1[2-9]|2[0-4]))$/.test(e.num||'')||e.id==='item-117').sort((a,b)=>a.gi-b.gi).map(e=>[e.id,e.gi,e.vn,e.title]),
        idxOrder:Object.keys(tvaIdx.titoli).filter(k=>/^item-0(1[2-9]|2[0-4])$/.test(k)),
        lisOrder:[...document.querySelectorAll('li.card-wrap[id^=item-]')].map(l=>l.id.slice(5)).slice(11,26)
      }}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); print(errs); b.close()
