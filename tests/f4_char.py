from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for sid,st in [('char wolverine',{'screen':'char','eid':'char-wolverine'}),('char xavier',{'screen':'char','eid':'char-charles-xavier'}),('char fury',{'screen':'char','eid':'char-nick-fury'}),('char tbd',{'screen':'char','eid':'char-a-bomb'}),
                   ('attore',{'screen':'attore','eid':'att-hugh-jackman'}),('uni',{'screen':'uni','uid':'uni-earth-10005-fox-verse'}),('potscheda',{'screen':'potscheda','arc':'pot','eid':'char-wolverine'})]:
        pg.evaluate("(s)=>{tvaAtlas2.setState(s);tvaAtlas2.onOpen()}",st); pg.wait_for_timeout(600)
        r=pg.evaluate("()=>{const b=document.querySelector('.a2-scroll');return {h:[...b.querySelectorAll('h2,h3,.a2-sec-t,.a2-sechd,.a2-kick')].map(x=>x.textContent.trim().slice(0,40)).filter(Boolean).slice(0,30),len:b.scrollHeight}}")
        print(sid,r)
    print(errs)
