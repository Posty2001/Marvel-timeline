from leg_shot import *
OUT='/home/claude/outputs/'
def sc(pg,sel,off=0):
    pg.evaluate("([s,o])=>{const R=document.querySelector('#atlas2 .a2-scroll');const t=document.querySelector(s);const ih=(document.querySelector('.ud-index')||{offsetHeight:0}).offsetHeight;R.scrollTop=t.getBoundingClientRect().top-R.getBoundingClientRect().top+R.scrollTop-ih-o}",[sel,off]); pg.wait_for_timeout(350)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    op=lambda u:(pg.evaluate("(u)=>tvaAtlas2.openUni(u)",u),pg.wait_for_timeout(900))
    op('uni-earth-199999-mcu'); pg.screenshot(path=OUT+'fase3a_01_mcu_hero_390.png')
    pg.click('.a2-sec-prim .a2-f:has-text("Per ambientazione")'); pg.wait_for_timeout(400); sc(pg,'#ud-titoli',6); pg.screenshot(path=OUT+'fase3a_02_mcu_titoli_ambientazione_390.png')
    pg.click('.a2-sec-prim .a2-f:has-text("Ordine della guida")'); pg.wait_for_timeout(200)
    sc(pg,'#ud-collegamenti',6); pg.screenshot(path=OUT+'fase3a_03_mcu_collegamenti_confermati_390.png')
    pg.evaluate("()=>{document.querySelectorAll('#ud-collegamenti details.ud-prov')[0].open=true}"); pg.wait_for_timeout(200)
    pg.evaluate("()=>{const R=document.querySelector('#atlas2 .a2-scroll');const h=[...document.querySelectorAll('#ud-collegamenti h4')].find(x=>/Da verificare/.test(x.textContent));R.scrollTop=h.getBoundingClientRect().top-R.getBoundingClientRect().top+R.scrollTop-60}"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{const d=[...document.querySelectorAll('#ud-collegamenti .ud-lk-vf details.ud-prov')][0];if(d)d.open=true}"); pg.wait_for_timeout(250); pg.screenshot(path=OUT+'fase3a_04_mcu_da_verificare_390.png')
    pg.evaluate("()=>{const R=document.querySelector('#atlas2 .a2-scroll');const h=[...document.querySelectorAll('#ud-collegamenti h4')].find(x=>/Luoghi e realt/.test(x.textContent));R.scrollTop=h.getBoundingClientRect().top-R.getBoundingClientRect().top+R.scrollTop-60}"); pg.wait_for_timeout(300); pg.screenshot(path=OUT+'fase3a_05_mcu_speciali_390.png')
    op('uni-earth-10005-fox-verse'); pg.screenshot(path=OUT+'fase3a_06_fox_hero_390.png')
    op('uni-earth-838'); pg.evaluate("()=>{document.querySelector('#atlas2 .a2-scroll').scrollTop=520}"); pg.wait_for_timeout(300); pg.screenshot(path=OUT+'fase3a_07_earth838_390.png')
    pg.evaluate("()=>{const R=document.querySelector('#atlas2 .a2-scroll');R.scrollTop=R.scrollHeight}"); pg.wait_for_timeout(300); pg.screenshot(path=OUT+'fase3a_08_earth838_non_documentato_390.png')
    op('uni-blade-verse'); pg.evaluate("()=>{const R=document.querySelector('#atlas2 .a2-scroll');R.scrollTop=R.scrollHeight}"); pg.wait_for_timeout(300); pg.screenshot(path=OUT+'fase3a_09_blade_raggruppamento_390.png')
    op('uni-x-men-97-verse'); pg.screenshot(path=OUT+'fase3a_10_xmen97_animazione_390.png')
    ctx2=b.new_context(viewport={'width':320,'height':640},device_scale_factor=2,is_mobile=True,has_touch=True,service_workers='block'); q=ctx2.new_page()
    q.goto(U); q.wait_for_timeout(1000); q.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); q.wait_for_timeout(400); q.click('#appTabAtlante'); q.wait_for_timeout(500)
    q.evaluate("()=>tvaAtlas2.openUni('uni-earth-199999-mcu')"); q.wait_for_timeout(800); q.screenshot(path=OUT+'fase3a_11_mcu_hero_320.png')
    print(errs)
