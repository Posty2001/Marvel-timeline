from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("(s)=>{tvaAtlas2.setState(s);tvaAtlas2.onOpen()}",{'screen':'dossier','arc':'evt','eid':'evt-il-blip'}); pg.wait_for_timeout(400)
    print(pg.evaluate("()=>document.querySelector('.a2-scroll').innerText.replace(/\\n+/g,' | ').slice(900,2400)"))
