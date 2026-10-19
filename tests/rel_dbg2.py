from playwright.sync_api import sync_playwright
from leg_shot import boot
RT=['famiglia','relazione','organizzazione','variante','universo','titolo','attore']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('relationshipGraphToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{tvaRelGraph.render('universo-mcu',false,false)}"); pg.wait_for_timeout(300)
    print(pg.evaluate("""()=>[...document.querySelectorAll('#rgSvg .rg-satellite')].map(g=>{const t=[...g.querySelectorAll('text')].map(x=>x.outerHTML.slice(0,160));return g.dataset.node+' '+t.join(' | ')}).slice(0,40)"""))
    print(pg.evaluate("()=>document.querySelector('#rgSvg').getAttribute('viewBox')+' '+document.querySelector('#rgSvg').outerHTML.length"))
    b.close()
