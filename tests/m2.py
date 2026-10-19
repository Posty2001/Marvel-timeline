import sys,json
from playwright.sync_api import sync_playwright
from leg_shot import boot
W=int(sys.argv[1]) if len(sys.argv)>1 else 390; H=int(sys.argv[2]) if len(sys.argv)>2 else 844
O='/tmp/claude-0/t/shots/'
import os; os.makedirs(O,exist_ok=True)
def center(pg,u):
    r=pg.evaluate("(u)=>{const e=document.querySelector('.mp-n[data-u=\"'+u+'\"] .mp-hit').getBoundingClientRect();return [e.x+e.width/2,e.y+e.height/2]}",u); return r
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,W,H)
    pg.evaluate("()=>document.querySelector('.hm-p[data-portal=multiverso]').scrollIntoView({block:'center'})"); pg.wait_for_timeout(200)
    pg.click('.hm-p[data-portal=multiverso]'); pg.wait_for_timeout(1000)
    pg.screenshot(path=O+f'a_overview_{W}.png')
    x,y=center(pg,'uni-earth-199999-mcu'); pg.touchscreen.tap(x,y); pg.wait_for_timeout(700)
    pg.screenshot(path=O+f'b_sel_mcu_{W}.png')
    pg.click('#mpLegenda'); pg.wait_for_timeout(500); pg.screenshot(path=O+f'c_legend_{W}.png'); pg.click('#mpPanelX'); pg.wait_for_timeout(300)
    pg.click('#mpFiltri'); pg.wait_for_timeout(500); pg.screenshot(path=O+f'd_filters_{W}.png'); pg.click('#mpPanelX'); pg.wait_for_timeout(300)
    pg.click('#mpFuori'); pg.wait_for_timeout(500); pg.screenshot(path=O+f'e_fuori_{W}.png'); pg.click('#mpPanelX'); pg.wait_for_timeout(300)
    pg.click('#mpModeList'); pg.wait_for_timeout(500); pg.screenshot(path=O+f'f_list_{W}.png')
    pg.click('#mpModeMap'); pg.wait_for_timeout(500)
    for i in range(3): pg.click('#mpZin'); pg.wait_for_timeout(450)
    pg.screenshot(path=O+f'g_zoom_{W}.png')
    print(errs)
    b.close()
