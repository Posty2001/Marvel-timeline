import sys,json
from playwright.sync_api import sync_playwright
from leg_shot import boot
from cron3c_test import setcr,hub
W=int(sys.argv[1]); H=int(sys.argv[2]); out=sys.argv[3]
import os; os.makedirs(out,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b,W,H); hub(pg)
    ids=pg.evaluate("()=>tvaUniverse.ids()"); mcu=ids[0]; fox=[i for i in ids if '10005' in i][0]
    def shot(n,scroll=0):
        pg.evaluate("(y)=>{document.querySelector('.a2-scroll').scrollTop=y}",scroll); pg.wait_for_timeout(500); pg.screenshot(path=f'{out}/{n}.png')
    shot('01_hub')
    setcr(pg,mode='uni',uid=mcu); shot('02_universo_mcu_ambientazione')
    setcr(pg,mode='uni',uid=mcu); shot('02b_universo_mcu_spina',560)
    setcr(pg,mode='uni',uid=mcu,ord='uscita'); shot('03_universo_mcu_uscita',560)
    setcr(pg,mode='uni',uid=[i for i in ids if 'fantastic' in i][0]); shot('04_universo_dati_insufficienti')
    setcr(pg,mode='uni',uid=[i for i in ids if 'legion' in i][0]); shot('05_universo_vuoto')
    setcr(pg,mode='par',pA=mcu,pB=fox); shot('06_parallele_riepilogo')
    setcr(pg,mode='par',pA=mcu,pB=fox,lim=999); shot('07_parallele_corsie',720)
    setcr(pg,mode='par',pA=mcu,pB=fox,pm='proprie'); shot('08_parallele_proprie',560)
    setcr(pg,mode='par',pA=mcu,pB=fox,pm='ab',ps='B'); shot('09_parallele_ab')
    setcr(pg,mode='exp',q='agents'); shot('10_esplora_ricerca')
    setcr(pg,mode='exp',fu=[mcu],fp=['b3'],ft=['serie']); shot('11_esplora_filtri_attivi')
    setcr(pg,mode='exp',fu=['_na']); shot('12_esplora_non_assegnate')
    setcr(pg,mode='exp'); pg.click('#crFbtn'); pg.wait_for_timeout(400); pg.screenshot(path=f'{out}/13_esplora_sheet_filtri.png')
    pg.keyboard.press('Escape'); setcr(pg,mode='uni',uid=mcu); pg.click('#crUniSel'); pg.wait_for_timeout(400); pg.screenshot(path=f'{out}/14_selettore_universo.png')
    print(errs); b.close()
