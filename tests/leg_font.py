from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    print(pg.evaluate("()=>[getComputedStyle(document.querySelector('#atlas2 .a2-ttl b')).fontFamily, getComputedStyle(document.body).fontFamily]"))
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('reliquiario',{arc:'art',eid:null})"); pg.wait_for_timeout(600)
    print(pg.evaluate("()=>['.a2-hero h2','.a2-rel-panel','.a2-gem span','.a2-rel-panel p'].map(s=>{const e=document.querySelector(s);return s+' '+(e?getComputedStyle(e).fontFamily+' | '+getComputedStyle(e).backgroundColor:'-')})"))
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('personaggi',{pf:'tutti',pq:''})"); pg.wait_for_timeout(500)
    print(pg.evaluate("()=>['.a2-head h2','.a2-prow'].map(s=>{const e=document.querySelector(s);return s+' '+(e?getComputedStyle(e).fontFamily:'-')})"))
    b.close()
