from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch()
    c,pg,e=boot(b); pg.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); pg.wait_for_timeout(900)
    print(pg.evaluate("()=>[...document.querySelectorAll('.hm-p,.hm-q,.a2-sbox input')].filter(e=>e.getBoundingClientRect().height<44).map(e=>(e.dataset.portal||e.className)+':'+e.getBoundingClientRect().height)"))
    c2,p2,e2=boot(b,320,844); p2.evaluate("()=>tvaAtlas2.ext.api.nav('home')"); p2.wait_for_timeout(900)
    print(p2.evaluate("()=>[...document.querySelectorAll('.hm-p-t b,.hm-stats span')].filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent+':'+e.scrollWidth+'/'+e.clientWidth)"))
    b.close()
