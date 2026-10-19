from playwright.sync_api import sync_playwright
import json,re
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(1500)
    r=pg.evaluate("""()=>{
      const t=txt=>[...document.querySelectorAll('details.card')].find(c=>(c.querySelector('.title')||{}).textContent.trim().startsWith(txt));
      const m=t('Chi manca');
      const html=m.querySelector('.card-body, .body, div:last-child')?m.innerHTML.length:0;
      // structure: print class names of children recursively depth 3
      const walk=(e,d)=>d>3?'':[...e.children].map(c=>'  '.repeat(d)+c.tagName+'.'+c.className+' | '+c.textContent.trim().slice(0,60).replace(/\\n/g,' ')).slice(0,14).join('\\n')+'\\n';
      const ch=[...document.querySelectorAll('li[id^=char-],details[id^=char-]')];
      const mk=ch.filter(c=>/entit[àa] cosmic|celestial|cosmic|eterni[tà]|personificazion/i.test(c.innerText)).map(c=>c.id+' :: '+(c.querySelector('.title')||{}).textContent.trim());
      const sp=ch.filter(c=>/specie|razza|popolo|civilt|alieni|kree|skrull|asgard|deviant|celestial|kronan|chitauri|xandar|sakaar/i.test(c.innerText)).length;
      const mg=ch.filter(c=>/magi|mistic|stregon|incantes|arti mistiche|sorcer|hexe|darkhold/i.test(c.innerText)).map(c=>c.id).length;
      return {struct:m.innerHTML.slice(0,2500),mk,sp,mg}}""")
    print(r['struct']); print(r['mk']); print(r['sp'],r['mg']); b.close()
