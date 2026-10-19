from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    def go(st,name,full=False):
        pg.evaluate("(s)=>{tvaAtlas2.setState(s);tvaAtlas2.onOpen()}",st); pg.wait_for_timeout(500)
        pg.screenshot(path='f4shots/%s.png'%name,full_page=False)
    info={}
    pg.evaluate("()=>{tvaAtlas2.openHome()}"); pg.wait_for_timeout(500); pg.screenshot(path='f4shots/01_home.png')
    for cat in ['org','art','evt','luo','cos','spe','mis']:
        go({'screen':'arch','arc':cat,'eid':None,'af':'tutti','aq':'','au':'tutti'},'arch_'+cat)
        info[cat]=pg.evaluate("()=>({rows:document.querySelectorAll('#tvaAtlas2Body .a2-lrow, .a2-body .a2-lrow, [class*=a2-lrow]').length, txt:document.body.innerText.slice(0,0)})")
    print(info)
    go({'screen':'personaggi','pf':'tutti','pq':''},'pers_list')
    go({'screen':'attori'},'attori')
    go({'screen':'potenza','arc':'pot','eid':None,'af':'tutti','aq':'','au':'tutti'},'potenza')
    print(errs)
