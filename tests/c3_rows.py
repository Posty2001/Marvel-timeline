import json
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const UM=tvaUniverse;const o={};
    ['mcu','fox'].forEach(k=>{const id=UM.ids().find(i=>i.includes(k==='mcu'?'199999':'10005'));const g=UM.get(id);
      o[k]=(r=>Array.isArray(r)?r:(r.lista||r.list||r.items||r.righe||Object.values(r)[0]))(UM.ordina(g.titoli.filter(t=>t.kind!=='anim'),'ambientazione')).map(t=>{const a=UM.ambientazione(t.num);const an=UM.annoAmbientazione(a);const u=UM.uscita(t.num);return [t.num,t.title,an&&an.y,an&&an.approx,(a||'').slice(0,30),u&&u.data]})});
    o.links=UM.links().map(l=>[l.a,l.b,l.stato,l.label||l.etichetta||'']); return o}""")
    json.dump(r,open('c3_rows.json','w'),ensure_ascii=False)
    for k in('mcu','fox'):
        print(k,len(r[k]))
        for x in r[k][:60]: print(x)
    print(r['links'])
    b.close()
