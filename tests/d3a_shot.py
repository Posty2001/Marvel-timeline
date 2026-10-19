from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ids=pg.evaluate("()=>tvaUniverse.ids()")
    for i,u in enumerate(['uni-earth-199999-mcu','uni-earth-10005-fox-verse','uni-earth-838','uni-blade-verse']):
        pg.evaluate("(u)=>tvaAtlas2.openUni(u)",u); pg.wait_for_timeout(900)
        pg.screenshot(path=f'/tmp/claude-0/t/d3a_{i}_top.png')
        h=pg.evaluate("()=>document.querySelector('#atlas2 .a2-scroll').scrollHeight")
        print(u,h,errs)
    pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-199999-mcu')"); pg.wait_for_timeout(600)
    pg.click('.ud-ix[data-ix=collegamenti]'); pg.wait_for_timeout(500)
    pg.screenshot(path='/tmp/claude-0/t/d3a_mcu_lk.png')
