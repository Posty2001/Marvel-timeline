from leg_shot import *
O='/home/claude/outputs/'
RT=['famiglia','relazione','organizzazione','variante','universo','titolo','attore']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    A="tvaAtlas2.ext.api.nav"
    pg.evaluate("()=>{const c=document.getElementById('relationshipGraphToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
    for name,id,on in (('peter_parker','char-peter-parker',lambda t:t not in('famiglia','relazione')),('thor_famiglia','char-thor',lambda t:t=='famiglia'),('zero_wanda_famiglia','char-wanda-maximoff',lambda t:t=='famiglia')):
        pg.evaluate("([id,on])=>{for(const t of %s)tvaRelGraph.filters[t]=on.includes(t);tvaRelGraph.render(id,false,false)}"%RT,[id,[t for t in RT if on(t)]]); pg.wait_for_timeout(500)
        pg.evaluate("()=>{const e=document.querySelector('.relationship-graph-overlay .a2-vp');e.scrollIntoView({block:'start'});window.scrollBy(0,-110)}"); pg.wait_for_timeout(300)
        pg.screenshot(path=O+'shot_relazioni_%s_390.png'%name)
    ctx.close(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>"+A+"('arch',{arc:'mis',eid:null,af:'tutti',aq:'',au:'tutti'})"); pg.wait_for_timeout(600)
    pg.evaluate("()=>{const d=document.querySelector('.a2-gaps');d.open=true;d.scrollIntoView({block:'start'});window.scrollBy(0,-110)}"); pg.wait_for_timeout(300)
    pg.screenshot(path=O+'shot_arti_mistiche_lacune_390.png')
    pg.evaluate("()=>{[...document.querySelectorAll('.a2-card,[data-eid]')].find(e=>/Stregoneria/.test(e.textContent)).click()}"); pg.wait_for_timeout(700)
    pg.screenshot(path=O+'shot_arti_mistiche_dossier_390.png')
    pg.evaluate("()=>window.scrollBy(0,700)"); pg.wait_for_timeout(300); pg.screenshot(path=O+'shot_arti_mistiche_dossier2_390.png')
    print(errs); b.close()
