from leg_shot import *
from PIL import Image
def open_t(pg,tog):
    pg.evaluate("()=>{marvelChiudiOverlay()}"); pg.wait_for_timeout(200)
    pg.evaluate("(t)=>{const c=document.getElementById(t);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",tog); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    open_t(pg,'kangTvaGraphToggle'); pg.screenshot(path='g_kang1.png')
    pg.evaluate("()=>document.querySelector('.kang-tva-overlay').scrollTo?0:0")
    pg.evaluate("()=>{const o=document.querySelector('.kang-tva-overlay');o.scrollTop=520}"); pg.wait_for_timeout(300); pg.screenshot(path='g_kang2.png')
    open_t(pg,'relationshipGraphToggle'); pg.fill('#rgSearchInput','Wanda'); pg.wait_for_timeout(400); pg.click('#rgSearchResults button'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{const o=document.querySelector('.relationship-graph-overlay');const v=o.querySelector('.a2-vp');v.scrollIntoView()}"); pg.wait_for_timeout(300); pg.screenshot(path='g_rel1.png')
    pg.click('.relationship-graph-overlay .a2-vp-b >> nth=0'); pg.click('.relationship-graph-overlay .a2-vp-b >> nth=0'); pg.wait_for_timeout(300); pg.screenshot(path='g_rel2.png')
    print(pg.evaluate("()=>[...document.querySelectorAll('.a2-vp')].map(v=>v.getAttribute('data-z'))"))
    open_t(pg,'multiverseGraphToggle'); pg.evaluate("()=>{const d=document.querySelector('.multiverse-graph-overlay');[...d.querySelectorAll('details')].forEach(x=>x.open=true);d.querySelector('.a2-vp')&&d.querySelector('.a2-vp').scrollIntoView()}"); pg.wait_for_timeout(400); pg.screenshot(path='g_mv.png')
    print(errs,pg.evaluate("document.documentElement.scrollWidth")); b.close()
ims=[Image.open(f'g_{n}.png') for n in ['kang1','kang2','rel1','rel2','mv']]
w,h=ims[0].size; s=Image.new('RGB',(w*5//2,h//2))
for i,m in enumerate(ims): s.paste(m.resize((w//2,h//2)),(i*w//2,0))
s.save('g_sheet.png')
