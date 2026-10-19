from playwright.sync_api import sync_playwright
import json,re
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const cards=[...document.querySelectorAll('details.card')].map(c=>{c.__i=(c.id||(c.closest('[id]')||{}).id||'');return c}).filter(c=>c.__i&&!/^(item|p4|anim|uni|cronologie)/.test(c.__i));
      const sents=(c,re)=>c.innerText.split(/(?<=[.;!?])\\s+|\\n+/).filter(s=>re.test(s)).map(s=>s.trim().slice(0,150));
      const seeds={'Kree':/\\bKree\\b/i,'Skrull':/\\bSkrull/i,'Asgardiani':/Asgardian|Asgard\\b/i,'Celestiali':/Celestial/i,'Eterni':/\\bEterni\\b/i,'Deviants':/Deviant/i,'Chitauri':/Chitauri/i,'Xandariani':/Xandar/i,'Talokanil':/Talokan/i,'Inumani':/Inumani|Inhuman/i,'Mutanti':/\\bmutant/i,'Vampiri':/vampir/i,'Simbionti':/simbiot|symbiot/i,'Wakandiani':/Wakand/i,
        'Kamar-Taj':/Kamar-Taj/i,'Darkhold':/Darkhold/i,'Vishanti':/Vishanti/i,'Stregoneria':/stregon/i,'Magia':/\\bmagi[ac]/i,'ArtiMistiche':/arti mistiche|mistic/i,'Agamotto':/Agamotto/i};
      const out={};
      for(const [k,re] of Object.entries(seeds)){const hit=cards.filter(c=>re.test(c.innerText));out[k]={n:hit.length,ids:hit.slice(0,40).map(c=>c.__i),ex:hit.length?sents(hit[0],re).slice(0,2):[]}}
      return out}""")
    for k,v in r.items(): print(k,v['n'],v['ids'][:14]); print('   ',v['ex'])
    b.close()
