from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
def st(pg): return pg.evaluate("()=>({a2:atlas2Toggle.checked,classic:tvaArchivesToggle.checked,scr:tvaAtlas2.ext.api.ST.screen,eid:tvaAtlas2.ext.api.ST.eid,tab:getComputedStyle(appTabbar).display,title:document.querySelector('.a2-ttl b')?.textContent,sw:document.documentElement.scrollWidth,depth:tvaNavStato().depth})")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('personaggi',{pf:'tutti',pq:''})"); pg.wait_for_timeout(500)
    pg.click('#atlas2 .a2-prow >> nth=3'); pg.wait_for_timeout(900); print('char',st(pg)); pg.screenshot(path='leg_n_char.png')
    # link interno: correlati
    pg.evaluate("()=>{const b=document.querySelector('#atlas2 .a2-v .mv-inline-link');b&&b.click()}"); pg.wait_for_timeout(700); print('correlato',st(pg))
    pg.evaluate("()=>tvaBack()"); pg.wait_for_timeout(500); print('back',st(pg))
    # chrono
    for nm,fn in [('chrono',"tvaAtlas2.ext.api.nav('chrono',{eid:'chrono-gemme-dell-infinito'})"),('alberi',"tvaAtlas2.ext.api.nav('alberi',{eid:'tree-asgard'})"),('attori',"tvaAtlas2.ext.api.nav('attori',{eid:null,aq:''})"),('inc',"tvaAtlas2.ext.api.nav('doc',{eid:'inc'})"),('mar',"tvaAtlas2.ext.api.nav('doc',{eid:'mar'})")]:
        pg.evaluate("()=>"+fn); pg.wait_for_timeout(600); print(nm,st(pg)); pg.screenshot(path=f'leg_n_{nm}.png')
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('attori',{eid:null,aq:''})"); pg.wait_for_timeout(300)
    pg.click('#atlas2 .a2-prow >> nth=2'); pg.wait_for_timeout(700); print('attore',st(pg)); pg.screenshot(path='leg_n_attore.png')
    # guardia classico
    pg.evaluate("()=>{marvelChiudiOverlay();const c=document.getElementById('tvaArchivesToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600); print('guardia',st(pg))
    print(errs); b.close()
