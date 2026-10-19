from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ok('xref presente',pg.evaluate("()=>!!window.tvaXref&&typeof tvaXref.cerca==='function'"))
    r=pg.evaluate("()=>{const o=tvaXref.opera('item-023');return {t:o.titolo,vis:o.vis,g:o.guida,u:o.uscita,am:o.ambientazione,ch:o.personaggi.length,at:o.attori.length,saga:o.saga,dip:o.dip.richiede,arc:o.archivi.length}}")
    print(r)
    pg.evaluate("()=>tvaGo('item','item-023')"); pg.wait_for_timeout(500)
    ok('opera aperta',pg.evaluate("()=>tvaAtlas2.getState().screen")=='opera')
    print(pg.evaluate("()=>document.querySelector('.a2-opera').innerText.slice(0,1500)"))
    pg.screenshot(path='f4_opera1.png')
    print(errs); b.close()
done()
