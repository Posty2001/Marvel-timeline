from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>Object.keys(tvaIdx.titoli).filter(k=>/item-0(4|5|6|7|8|9)\\d/.test(k)).sort().map(k=>k+' '+(tvaIdx.titoli[k].titolo||tvaIdx.titoli[k].name||tvaIdx.titoli[k].li.querySelector('.title')?.textContent.trim()))""")
    print('\n'.join(r)); b.close()
