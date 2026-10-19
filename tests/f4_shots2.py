from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    def go(st,name):
        pg.evaluate("(s)=>{tvaAtlas2.setState(s);tvaAtlas2.onOpen()}",st); pg.wait_for_timeout(600); pg.screenshot(path='f4shots/%s.png'%name)
    go({'screen':'dossier','arc':'org','eid':'org-s-h-i-e-l-d'},'dos_org')
    go({'screen':'dossier','arc':'evt','eid':'evt-il-blip'},'dos_evt')
    go({'screen':'char','eid':'char-wolverine'},'char_wolverine')
    go({'screen':'attore','eid':'att-tobey-maguire'},'att')
    print(pg.evaluate("()=>[...document.querySelectorAll('[id^=org-],[id^=evt-],[id^=att-hugh]')].slice(0,3).map(x=>x.id)"))
    print(errs)
