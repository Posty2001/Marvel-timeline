from leg_shot import *
O='/home/claude/outputs/'
RT=['famiglia','relazione','organizzazione','variante','universo','titolo','attore']
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    A="tvaAtlas2.ext.api.nav"
    # relazioni
    pg.evaluate("()=>{const c=document.getElementById('relationshipGraphToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(700)
    pg.evaluate("()=>{for(const t of %s)tvaRelGraph.filters[t]=!['famiglia','relazione'].includes(t);tvaRelGraph.render('char-peter-parker',false,false)}"%RT); pg.wait_for_timeout(500)
    pg.screenshot(path=O+'shot_relazioni_peter_parker_390.png')
    pg.evaluate("()=>{for(const t of %s)tvaRelGraph.filters[t]=t==='famiglia';tvaRelGraph.render('char-thor',false,false)}"%RT); pg.wait_for_timeout(500)
    pg.screenshot(path=O+'shot_relazioni_thor_famiglia_390.png')
    pg.evaluate("()=>{for(const t of %s)tvaRelGraph.filters[t]=t==='famiglia';tvaRelGraph.render('char-wanda-maximoff',false,false)}"%RT); pg.wait_for_timeout(500)
    pg.screenshot(path=O+'shot_relazioni_zero_390.png')
    ctx.close(); ctx,pg,errs=boot(b)
    for t in ['tree-ff','tree-asgard']:
        pg.evaluate("()=>"+A+"('alberi',{eid:'%s'})"%t); pg.wait_for_timeout(700)
        pg.evaluate("()=>document.querySelector('.a2-ft').scrollIntoView({block:'start'})"); pg.evaluate("()=>window.scrollBy(0,-120)"); pg.wait_for_timeout(300)
        pg.screenshot(path=O+'shot_alberi_%s_390.png'%t)
    pg.evaluate("()=>"+A+"('arch',{arc:'mis',eid:null,af:'tutti',aq:'',au:'tutti'})"); pg.wait_for_timeout(700)
    pg.screenshot(path=O+'shot_arti_mistiche_lista_390.png',full_page=False)
    pg.evaluate("()=>{const d=document.querySelector('.a2-gaps');if(d)d.open=true}"); 
    pg.evaluate("()=>{const d=document.querySelector('.a2-gaps');if(d)d.scrollIntoView({block:'center'})}"); pg.wait_for_timeout(300)
    pg.screenshot(path=O+'shot_arti_mistiche_lacune_390.png')
    ids=pg.evaluate("()=>tvaAtlas2.arcModel().cat.mis.map(e=>e.id)"); print(ids)
    pg.evaluate("(id)=>tvaAtlas2.ext.api.nav('arch',{arc:'mis',eid:id,af:'tutti',aq:'',au:'tutti'})",ids[0]); pg.wait_for_timeout(700)
    pg.screenshot(path=O+'shot_arti_mistiche_dossier_390.png',full_page=False)
    print(errs); b.close()
