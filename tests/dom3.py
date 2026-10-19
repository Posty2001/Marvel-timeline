from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto('file:///home/claude/work/index.html'); pg.wait_for_timeout(800)
    r=pg.evaluate("""()=>{const out={};for(const sid of ['cap0','parte1','parte1bis','parte2','parte3','dopo-sw','parte4','serieanimate']){
      const root=document.getElementById(sid)||document.querySelector('.'+sid);
      const cs=[...root.querySelectorAll('.card-wrap')];
      out[sid]={tot:cs.length,withUni:cs.filter(c=>c.hasAttribute('data-uni')).length,
       noUni:cs.filter(c=>!c.hasAttribute('data-uni')).map(c=>{const t=c.querySelector('.title');return [c.id||'-',(t?t.textContent:c.textContent).trim().replace(/\\s+/g,' ').slice(0,38),c.getAttribute('data-type'),c.getAttribute('data-studio'),c.getAttribute('data-cats')]})}}
      return out}""")
    for k,v in r.items():
        print(k,v['tot'],v['withUni'],len(v['noUni']))
        for x in v['noUni'][:60]: print('    ',x)
    b.close()
