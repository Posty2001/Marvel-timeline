from playwright.sync_api import sync_playwright
from leg_shot import boot
def st(pg): return pg.evaluate("()=>({a2:atlas2Toggle.checked,classic:tvaArchivesToggle.checked,shell:getComputedStyle(document.getElementById('tvaShell')).display,tab:getComputedStyle(appTabbar).display,scr:(window.tvaAtlas2&&tvaAtlas2.ext.api.ST.screen),title:document.querySelector('.ts-t')?.textContent})")
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>tvaAtlas2.ext.api.nav('personaggi',{pf:'tutti',pq:''})"); pg.wait_for_timeout(600)
    pg.click('#atlas2 .a2-prow >> nth=3'); pg.wait_for_timeout(1200); print('char',st(pg)); pg.screenshot(path='leg_char.png')
    # scheda: lista bottoni
    print(pg.evaluate("()=>[...document.querySelectorAll('#atlas2 button, #atlas2 a')].filter(b=>b.offsetParent).map(b=>b.textContent.trim().slice(0,40)).slice(0,30)"))
    b.close()
