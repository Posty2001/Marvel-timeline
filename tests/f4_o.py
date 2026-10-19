from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{tvaAtlas2.setState({screen:'dossier',arc:'org',eid:'org-s-h-i-e-l-d'});tvaAtlas2.onOpen()}"); pg.wait_for_timeout(500)
    print(pg.evaluate("()=>document.querySelector('.a2-scroll').innerText.replace(/\\n+/g,' | ').slice(900,3000)"))
