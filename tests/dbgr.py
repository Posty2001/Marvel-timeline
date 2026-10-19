import json,sys
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/'+sys.argv[1]
RTD=['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125']
W='marvel-ultimate-timeline-watched'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page()
    pg.on('pageerror',lambda e:print('ERR',e))
    pg.add_init_script("if(!localStorage.getItem('__s')){localStorage.setItem('__s','1');localStorage.setItem(%s,%s);}"%(json.dumps(W),json.dumps(json.dumps({i:True for i in RTD[:-1]}))))
    pg.goto(F); pg.wait_for_timeout(1300)
    pg.evaluate("()=>{document.getElementById('journeyStarted').checked=true;document.getElementById('homeHubExited').checked=true}"); pg.wait_for_timeout(500)
    pg.evaluate("document.querySelector('.watch-check[data-item=\"125\"]').click()"); pg.wait_for_timeout(800)
    k='marvel-ultimate-timeline-missioni-xp-bonus'
    print('before',pg.evaluate("k=>localStorage.getItem(k)",k))
    print("keys-before",pg.evaluate("Object.keys(localStorage)"))
    pg.reload(); pg.wait_for_timeout(1500)
    print('after',pg.evaluate("k=>localStorage.getItem(k)",k))
    print(pg.evaluate("Object.keys(localStorage)"))
    b.close()
