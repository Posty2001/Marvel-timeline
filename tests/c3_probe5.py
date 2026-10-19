import json,re,collections
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
 const atl=JSON.parse(document.getElementById('atlasData').textContent), UM=tvaUniverse; const o={};
 o.sig={}; o.ruolo={}; o.tipo={}; o.prec={}; o.uni_count={};
 atl.opere.forEach(x=>{o.sig[x.significatoAnnoCard]=(o.sig[x.significatoAnnoCard]||0)+1;o.ruolo[x.ruolo]=(o.ruolo[x.ruolo]||0)+1;o.tipo[x.tipo]=(o.tipo[x.tipo]||0)+1;o.prec[x.precisioneUscita]=(o.prec[x.precisioneUscita]||0)+1;const k=(x.universi||[]).length;o.uni_count[k]=(o.uni_count[k]||0)+1});
 // anim
 const cards=[...document.querySelectorAll('[id^="anim-"].card-wrap')];
 o.anim=cards.map(e=>{const t=e.textContent.replace(/\\s+/g,' ');const m=t.match(/AMBIENTAZIONE(.*?)DURATA/);return [e.id,e.dataset.uni||null,m?m[1].trim():null]});
 o.anim_state=atl.animate.map(a=>[a.id,a.stato,a.certezza,(a.universi||[]).join(',')]);
 return o}""")
    print({k:r[k] for k in ['sig','ruolo','tipo','prec','uni_count']})
    print(len(r['anim']),sum(1 for a in r['anim'] if a[1]),'con universo nel DOM')
    st=collections.Counter(a[1] for a in r['anim_state']); print(st)
    for a in r['anim']: print(a)
    json.dump(r,open('c3_probe5.json','w'),ensure_ascii=False)
    b.close()
