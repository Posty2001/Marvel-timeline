import sys,os
from playwright.sync_api import sync_playwright
from leg_shot import boot
O='/tmp/claude-0/t/final/'; os.makedirs(O,exist_ok=True)
def center(pg,u): return pg.evaluate("(u)=>{const e=document.querySelector('.mp-n[data-u=\"'+u+'\"] .mp-hit').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]}",u)
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(390,844)]:
        ctx,pg,errs=boot(b,W,H)
        pg.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(200)
        pg.screenshot(path=O+f'3b_{W}_00_home_portale.png')
        pg.click('.hm-p[data-portal=multiverso]'); pg.wait_for_timeout(1000)
        pg.screenshot(path=O+f'3b_{W}_01_mappa.png')
        x,y=center(pg,'uni-earth-96283-raimi-verse'); pg.touchscreen.tap(x,y); pg.wait_for_timeout(700); pg.screenshot(path=O+f'3b_{W}_02_selezione_anteprima.png')
        pg.click('.mp-sheet .mp-x'); pg.click('#mpFit'); pg.wait_for_timeout(400)
        pg.fill('#mpSearch','garf'); pg.wait_for_timeout(400); pg.screenshot(path=O+f'3b_{W}_03_ricerca.png')
        pg.click('.mp-sg-i'); pg.wait_for_timeout(800); pg.screenshot(path=O+f'3b_{W}_04_zoom_ricerca.png')
        pg.click('.mp-sheet .mp-x'); pg.click('#mpFit'); pg.wait_for_timeout(400)
        pg.click('#mpLegenda'); pg.wait_for_timeout(450); pg.screenshot(path=O+f'3b_{W}_05_legenda.png'); pg.click('#mpPanelX'); pg.wait_for_timeout(250)
        pg.click('#mpFiltri'); pg.wait_for_timeout(300); pg.click('.mp-fc[data-v=legacy]'); pg.click('[data-rel=verificare]'); pg.wait_for_timeout(300); pg.screenshot(path=O+f'3b_{W}_06_filtri.png'); pg.click('#mpPanelX'); pg.wait_for_timeout(350); pg.screenshot(path=O+f'3b_{W}_07_mappa_filtrata.png')
        pg.click('#mpFiltri'); pg.click('#mpReset'); pg.click('#mpPanelX'); pg.wait_for_timeout(300)
        pg.click('#mpFuori'); pg.wait_for_timeout(450); pg.screenshot(path=O+f'3b_{W}_08_fuori_mappa.png')
        pg.click('.mp-sp [data-sp=void]'); pg.wait_for_timeout(800); pg.screenshot(path=O+f'3b_{W}_09_void_evidenziato.png'); pg.click('.mp-hlx'); pg.wait_for_timeout(200)
        pg.click('#mpModeList'); pg.wait_for_timeout(500); pg.screenshot(path=O+f'3b_{W}_10_elenco.png')
        pg.evaluate("()=>document.querySelector('.mp-list').scrollTop=900"); pg.wait_for_timeout(200); pg.screenshot(path=O+f'3b_{W}_11_elenco_scroll.png')
        print(W,errs); ctx.close()
    b.close()
