from playwright.sync_api import sync_playwright
U='http://127.0.0.1:8124/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_context(viewport={'width':375,'height':667}).new_page()
    pg.route('**/assets/images/tva/*',lambda r:r.abort())
    pg.goto(U); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{journeyStarted.checked=true; journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(300)
    pg.evaluate("()=>document.querySelector('.a2-tiles').scrollIntoView()"); pg.wait_for_timeout(1500)
    print(pg.evaluate("()=>[...document.querySelectorAll('.a2-tile')].map(t=>t.className+'|'+t.children.length+'|'+[...t.children].map(c=>c.className).join(','))"))
    print(pg.evaluate("()=>[...document.querySelectorAll('.a2-bgimg')].map(i=>[i.complete,i.naturalWidth,i.loading,i.getBoundingClientRect().top])"))
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('potenza')"); pg.wait_for_timeout(300)
    print(pg.evaluate("()=>document.querySelector('.a2-ttl b').textContent"))
