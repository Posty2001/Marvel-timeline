import sys
from playwright.sync_api import sync_playwright
from leg_shot import boot
from map3b_test_helpers import open_map
W=int(sys.argv[1]);H=int(sys.argv[2]);out=sys.argv[3]
import os; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,W,H)
    pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(300)
    pg.evaluate("()=>tvaAtlas2.openUni&&0")
    ids=pg.evaluate("()=>tvaUniverse.ids()")
    pg.evaluate("(u)=>tvaAtlas2.setState({screen:'mappa',mp:Object.assign({},tvaAtlas2.getState().mp,{sel:u})})",ids[0]); pg.wait_for_timeout(900)
    pg.screenshot(path=f'{out}/link_mappa_anteprima.png')
    print(pg.evaluate("()=>[...document.querySelectorAll('.mp-acts button')].map(b=>[b.textContent,Math.round(b.getBoundingClientRect().width),Math.round(b.getBoundingClientRect().height),Math.round(b.getBoundingClientRect().bottom)])"),H)
    pg.evaluate("(u)=>tvaAtlas2.openUni(u)",ids[0]); pg.wait_for_timeout(700); pg.screenshot(path=f'{out}/link_dossier.png')
    print(errs); b.close()
