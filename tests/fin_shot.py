from leg_shot import *
def open_t(pg,tog):
    pg.evaluate("()=>{marvelChiudiOverlay()}"); pg.wait_for_timeout(200)
    pg.evaluate("(t)=>{const c=document.getElementById(t);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",tog); pg.wait_for_timeout(900)
O='shots_leg/'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    A="tvaAtlas2.ext.api.nav"
    pg.evaluate("()=>"+A+"('personaggi',{pf:'tutti',pq:''})"); pg.wait_for_timeout(500); pg.screenshot(path=O+'01_personaggi.png')
    pg.click('#atlas2 .a2-prow >> nth=3'); pg.wait_for_timeout(800); pg.screenshot(path=O+'02_scheda_personaggio.png')
    for n,f in [('03_cronologie',"chrono',{eid:'chrono-gemme-dell-infinito'}"),('04_alberi',"alberi',{eid:'tree-asgard'}"),('05_attori',"attori',{eid:null,aq:''}"),('06_incursioni',"doc',{eid:'inc'}")]:
        pg.evaluate("()=>"+A+"('"+f+")"); pg.wait_for_timeout(600); pg.screenshot(path=O+n+'.png')
    pg.evaluate("()=>"+A+"('arte',{eid:'art-gemma-della-mente'})"); pg.wait_for_timeout(300)
    pg.evaluate("()=>tvaAtlas2.openArc('art','art-gemma-della-mente')"); pg.wait_for_timeout(700); pg.screenshot(path=O+'07_gemma_dossier.png')
    # reliquiario
    pg.evaluate("()=>"+A+"('reliquiario')"); pg.wait_for_timeout(700); pg.screenshot(path=O+'08_reliquiario.png')
    pg.query_selector_all('#atlas2 .a2-gem')[1].click(); pg.wait_for_timeout(700); pg.evaluate("()=>document.querySelector('.a2-rel-panel').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path=O+'09_reliquiario_gemma.png')
    open_t(pg,'kangTvaGraphToggle'); pg.screenshot(path=O+'10_kang.png')
    open_t(pg,'relationshipGraphToggle'); pg.fill('#rgSearchInput','Wanda'); pg.wait_for_timeout(300); pg.click('#rgSearchResults button'); pg.wait_for_timeout(800)
    pg.evaluate("()=>document.querySelector('.relationship-graph-overlay .a2-vp').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path=O+'11_relazioni.png')
    open_t(pg,'multiverseGraphToggle'); pg.evaluate("()=>document.querySelector('.multiverse-graph-overlay .a2-vp').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path=O+'12_multiverso.png')
    open_t(pg,'universeTimelineToggle'); pg.evaluate("()=>document.querySelector('.a2-ut-bar').scrollIntoView()"); pg.wait_for_timeout(300); pg.screenshot(path=O+'13_timeline_universi.png')
    print(errs); b.close()
