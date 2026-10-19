from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for cat,eid in [('org','org-s-h-i-e-l-d'),('evt','evt-il-blip'),('evt','bat-battaglia-di-new-york'),('art','art-mjolnir'),('luo','luo-wakanda'),('luo','pia-asgard'),('cos','char-galactus'),('spe','spe-asgardiani'),('mis','mis-stregoneria')]:
        pg.evaluate("(s)=>{tvaAtlas2.setState(s);tvaAtlas2.onOpen()}",{'screen':'dossier','arc':cat,'eid':eid}); pg.wait_for_timeout(400)
        r=pg.evaluate("()=>{const b=document.querySelector('.a2-scroll');return [b.querySelectorAll('h3').length?[...b.querySelectorAll('h3')].map(x=>x.textContent.trim().slice(0,30)):[],b.scrollHeight]}")
        print(cat,eid,r)
