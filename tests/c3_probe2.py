import json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{
 const UM=tvaUniverse, atl=JSON.parse(document.getElementById('atlasData').textContent);
 const out={};
 out.animate_n=atl.animate.length; out.animate0=atl.animate[0]; out.animate_keys=Object.keys(atl.animate[0]);
 const g=UM.get('uni-marvel-animation-universe-2006-2017'); out.anim_titles=g.titoli.slice(0,3).map(t=>({id:t.id,kind:t.kind,title:t.title,num:t.num}));
 out.kinds={}; UM.ids().forEach(id=>UM.get(id).titoli.forEach(t=>out.kinds[t.kind]=(out.kinds[t.kind]||0)+1));
 // titoli senza universo / cross
 const seen=new Set(); UM.ids().forEach(id=>UM.get(id).titoli.forEach(t=>seen.add(t.id))); out.titles_in_model=seen.size;
 // ambientazioni MCU non parse
 const O={};atl.opere.forEach(o=>O[o.id]=o);
 const mcu=UM.get('uni-earth-199999-mcu').titoli; out.mcu_noyear=mcu.filter(t=>t.kind==='item'&&UM.annoAmbientazione((O[t.num]||{}).ambientazione).y===null).map(t=>t.num+'|'+t.title+'|'+((O[t.num]||{}).ambientazione||''));
 out.mcu_neg=mcu.filter(t=>{const y=UM.annoAmbientazione((O[t.num]||{}).ambientazione);return y.y!==null&&y.y<1900}).map(t=>t.num+'|'+((O[t.num]||{}).ambientazione||'')+'|'+UM.annoAmbientazione((O[t.num]||{}).ambientazione).y);
 out.mcu_approx=mcu.filter(t=>{const y=UM.annoAmbientazione((O[t.num]||{}).ambientazione);return y.approx}).map(t=>t.num+'|'+(O[t.num]||{}).ambientazione+'|'+UM.annoAmbientazione((O[t.num]||{}).ambientazione).y);
 out.eventi_mcu=UM.get('uni-earth-199999-mcu').eventiChiave;
 // parser divergence: reimplement not available -> test via alt-timeline events mode DOM
 return out}""")
    json.dump(r,open('c3_probe2.json','w'),ensure_ascii=False,indent=1); print(json.dumps(r,ensure_ascii=False)[:4500]); b.close()
