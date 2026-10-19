from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{tvaAtlas2.setState({screen:'search',sq:'s.h.i.e.l.d'});tvaAtlas2.onOpen()}"); pg.wait_for_timeout(300)
    print(pg.evaluate("()=>[...document.querySelectorAll('.a2-resbox')].map(g=>[g.querySelector('h3').textContent,[...g.querySelectorAll('button,a')].map(x=>x.textContent.trim()).slice(0,8)])"))
