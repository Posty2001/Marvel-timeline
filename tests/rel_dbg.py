from playwright.sync_api import sync_playwright
from leg_shot import boot
RT=['famiglia','relazione','organizzazione','variante','universo','titolo','attore']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('relationshipGraphToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
    big=pg.evaluate("()=>Object.entries(tvaRelGraph.data()).sort((a,b)=>b[1].conns.length-a[1].conns.length).slice(0,6).map(x=>x[0])")
    for nid in big:
      for on in (RT,['universo'],['titolo'],['famiglia','organizzazione','attore']):
        pg.evaluate("([id,on])=>{for(const t of %s)tvaRelGraph.filters[t]=on.includes(t);tvaRelGraph.render(id,false,false)}"%RT,[nid,on]); pg.wait_for_timeout(100)
        for page in range(3):
            r=pg.evaluate("""()=>{const bs=[...document.querySelectorAll('#rgSvg text')].filter(t=>t.textContent.trim()).map(t=>{const r=t.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom,t.textContent.slice(0,16),t.getAttribute('class'),t.parentNode.getAttribute('class')]});let n=[];for(let i=0;i<bs.length;i++)for(let j=i+1;j<bs.length;j++){const a=bs[i],c=bs[j];if(a[0]<c[2]-0.5&&c[0]<a[2]-0.5&&a[1]<c[3]-0.5&&c[1]<a[3]-0.5)n.push([a,c])}return n}""")
            if r: print(nid,on,page,r[0]); pg.screenshot(path='/tmp/claude-0/t/shots_leg/rel_dbg.png'); b.close(); raise SystemExit
            mb=pg.query_selector('#rgMoreBtn')
            if not mb: break
            mb.click(); pg.wait_for_timeout(100)
    b.close()
