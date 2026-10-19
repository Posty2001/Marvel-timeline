import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const UM=tvaUniverse;const out=[];
    UM.ids().forEach(id=>{const g=UM.get(id);let n=0,rel=0,y=0,ap=0,nd=0,items=0,anim=0;
      g.titoli.forEach(t=>{n++; if(t.kind==='anim')anim++; else items++;
        const u=UM.uscita(t.num||t.id), a=t.num?UM.ambientazione(t.num):null; const an=a?UM.annoAmbientazione(a):null;
        if(u&&u.data)rel++; if(an&&an.y!=null){y++; if(an.approx)ap++;} else nd++;});
      out.push([g.nome.slice(0,28),n,items,anim,rel,y,ap,nd,g.eventiChiave.length,g.crossover.length])});
    return out}""")
    for x in r: print(x)
    b.close()
