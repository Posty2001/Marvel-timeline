import json,collections
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
 const UM=tvaUniverse, alt=marvelGetAltTimelineData(), atl=JSON.parse(document.getElementById('atlasData').textContent);
 const out={n_alt:alt.length,alt_keys:Object.keys(alt[0]),atlas_keys:Object.keys(atl),opera_keys:Object.keys(atl.opere[0]),n_opere:atl.opere.length,opera0:atl.opere[0],
  studios:{},sagas:{}};
 alt.forEach(a=>{out.studios[a.studio]=(out.studios[a.studio]||0)+1;out.sagas[a.saga]=(out.sagas[a.saga]||0)+1});
 const O={};atl.opere.forEach(o=>O[o.id]=o);
 // coverage on 138
 let rel=0,relAtl=0,amb=0,ambY=0,ambApp=0,mism=0,prec={},dis=[],aw=0;
 const rows=[];
 alt.forEach(a=>{const id=('000'+a.num).slice(-3),o=O[id]||{};
   if(a.release)rel++; if(o.uscita)relAtl++; if(a.release&&o.uscita&&a.release!==o.uscita)mism++;
   if(o.precisioneUscita)prec[o.precisioneUscita]=(prec[o.precisioneUscita]||0)+1;
   if(o.ambientazione)amb++; const y=UM.annoAmbientazione(o.ambientazione); if(y.y!==null){ambY++; if(y.approx)ambApp++}
   rows.push([id,a.title,a.release||null,o.uscita||null,o.precisioneUscita||null,o.ambientazione||null,y.y,y.approx,(o.universi||[]).length,a.studio]);});
 out.cov={rel_alt:rel,rel_atlas:relAtl,mismatch:mism,prec:prec,amb_text:amb,amb_year:ambY,amb_approx:ambApp};
 out.rows=rows;
 // per universe
 out.uni=UM.ids().map(id=>{const g=UM.get(id);const t=g.titoli;let r=0,ay=0,ap=0,a=0,ys=[],rs=[];
   t.forEach(x=>{const o=O[x.id.replace('item-','')]||{}; if(o.uscita){r++;rs.push(o.uscita)}; if(o.ambientazione)a++; const y=UM.annoAmbientazione(o.ambientazione); if(y.y!==null){ay++;ys.push(y.y);if(y.approx)ap++}});
   rs.sort(); ys.sort((p,q)=>p-q);
   return {id,nome:g.breve,n:t.length,app:g.appartenenza.length,cross:g.crossover.length,var:g.varianti.length,rel:r,amb:a,ay:ay,ap:ap,ymin:ys[0],ymax:ys[ys.length-1],rmin:rs[0],rmax:rs[rs.length-1],ev:g.eventiChiave.length,evs:g.eventiChiave}});
 out.titoli_senza_universo=0; return out}""")
    json.dump(r,open('c3_probe.json','w'),ensure_ascii=False,indent=1)
    print({k:v for k,v in r.items() if k not in('rows','uni')})
    for u in r['uni']: print(u['nome'][:22].ljust(22),u['n'],'rel',u['rel'],'amb',u['amb'],'yr',u['ay'],'approx',u['ap'],u['ymin'],u['ymax'],u['rmin'],u['rmax'],'ev',u['ev'])
    b.close()
