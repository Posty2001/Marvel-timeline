from leg_shot import *
import json
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    A="tvaAtlas2.ext.api.nav"
    for t in ['tree-ff','tree-asgard','tree-wakanda','tree-stark']:
        pg.evaluate("()=>"+A+"('alberi',{eid:'%s'})"%t); pg.wait_for_timeout(700)
        r=pg.evaluate("""()=>{const s=document.querySelector('.ft-svg');if(!s)return null;const M=window.__m;return {n:s.querySelectorAll('.ft-node').length,marr:s.querySelectorAll('.ft-marr').length/2,par:s.querySelectorAll('.ft-par').length,adopt:s.querySelectorAll('.ft-adopt').length,sib:s.querySelectorAll('.ft-sib').length,partner:s.querySelectorAll('.ft-partner').length,links:s.querySelectorAll('.ft-link').length,vb:s.getAttribute('viewBox'),sw:document.documentElement.scrollWidth}}""")
        print(t,r)
        pg.evaluate("()=>document.querySelector('.a2-ft').scrollIntoView({block:'center'})"); pg.wait_for_timeout(300); pg.screenshot(path='tr_%s.png'%t)
    print(errs); b.close()
ims=[Image.open('tr_%s.png'%t) for t in ['tree-ff','tree-asgard','tree-wakanda','tree-stark']]
w,h=ims[0].size; s=Image.new('RGB',(w*2,h//2*1))
for i,m in enumerate(ims): s.paste(m.resize((w//2,h//2)),(i*w//2,0))
s.save('tr_sheet.png')
