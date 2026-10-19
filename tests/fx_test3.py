import sys
from f4lib import *
import f4lib
URL=sys.argv[1] if len(sys.argv)>1 else U; TAG=sys.argv[2] if len(sys.argv)>2 else 'dopo'
O='/home/claude/outputs/fix_ios/'
def open_graph(pg,detailed):
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(500)
    pg.evaluate("()=>tvaAtlas2.openUniversi()"); pg.wait_for_timeout(500)
    pg.evaluate("()=>document.getElementById('a2OpenClassic').click()"); pg.wait_for_timeout(800)
    if detailed: pg.evaluate("()=>mvMapOldGraphBtn.click()"); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(390,844),(320,568)]:
        t='[%s %d] '%(TAG,W)
        ctx=b.new_context(viewport={'width':W,'height':H},is_mobile=True,has_touch=True,service_workers='block',device_scale_factor=2); pg=ctx.new_page(); pg.set_default_timeout(8000); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(URL); pg.wait_for_timeout(1000); open_graph(pg,True)
        m=pg.evaluate("""()=>{const o=document.querySelector('.multiverse-graph-overlay'),c=getComputedStyle(o);const de=document.documentElement;
          return {pos:c.position,h:Math.round(o.getBoundingClientRect().height),ovSH:o.scrollHeight,ovCH:o.clientHeight,docSH:de.scrollHeight,ih:innerHeight,fixedTransform:c.transform!=='none'||c.willChange!=='auto'}}""")
        print(t,m)
        # percorri tutta la pagina: ogni elemento atteso deve poter arrivare al centro ed essere colpibile
        sel=['.mg-header h2','.mg-legend','.a2-vp-stage','.a2-vp-stage ~ *','.mg-footnote']
        res={}
        def scroll_to(y):
            pg.evaluate("(y)=>{const o=document.querySelector('.multiverse-graph-overlay');const sc=(o.scrollHeight>o.clientHeight+2)?o:null;(sc||window).scrollTo({top:y,behavior:'instant'})}",y); pg.wait_for_timeout(200)
        # altezza scrollabile effettiva
        tot=pg.evaluate("()=>{const o=document.querySelector('.multiverse-graph-overlay');return o.scrollHeight>o.clientHeight+2?o.scrollHeight-o.clientHeight:document.documentElement.scrollHeight-innerHeight}")
        ys=[0,tot/2,tot]
        for k,y in zip(('alto','centro','basso'),ys):
            scroll_to(y); pg.screenshot(path=O+'%s_grafo_%s_%d.png'%(TAG,k,W))
        r=pg.evaluate("""()=>{const o=document.querySelector('.multiverse-graph-overlay');const foot=o.querySelector('.mg-footnote');const b=foot.getBoundingClientRect();
           const stage=o.querySelector('.a2-vp-stage');const sb=stage?stage.getBoundingClientRect():null;
           const rest=innerHeight-b.bottom;return {footBottom:Math.round(b.bottom),ih:innerHeight,gapBelowFootnote:Math.round(rest),stageVisible:!!sb}}""")
        print(t,'fondo pagina:',r,'scroll tot',round(tot))
        ok(t+'contenuto finale (nota) raggiungibile e area vuota sotto <= 120px',r['footBottom']<=r['ih']+1 and r['gapBelowFootnote']<=120,r)
        # il grafo (stage) e i comandi sono raggiungibili: scroll fino al grafo e hit-test
        scroll_to(0)
        hit=pg.evaluate("""()=>{const st=document.querySelector('.multiverse-graph-overlay .a2-vp-stage');st.scrollIntoView({block:'center',behavior:'instant'});const r=st.getBoundingClientRect();const e=document.elementFromPoint(r.left+r.width/2,r.top+r.height/2);
          const btns=[...document.querySelectorAll('.multiverse-graph-overlay .a2-vp button')].map(x=>{x.scrollIntoView({block:'nearest',behavior:'instant'});const q=x.getBoundingClientRect();const h=document.elementFromPoint(q.left+q.width/2,q.top+q.height/2);return [x.textContent.trim().slice(0,2),!!h&&(h===x||x.contains(h)),Math.round(q.height)]});
          return {stage:!!e&&st.contains(e),btns,nodes:document.querySelectorAll('.multiverse-graph-overlay .mg-node').length}}""")
        ok(t+'grafo dettagliato raggiungibile e colpibile; comandi zoom ok',hit['stage'] and all(x[1] for x in hit['btns']) and len(hit['btns'])>=3,hit)
        # tocco su un nodo: pannello dettagli
        pg.evaluate("()=>document.querySelector('.multiverse-graph-overlay .mg-node[data-node=mcu]').dispatchEvent(new MouseEvent('click',{bubbles:true}))"); pg.wait_for_timeout(500)
        ip=pg.evaluate("()=>{const i=document.querySelector('.multiverse-graph-overlay .mg-info-panel');const r=i.getBoundingClientRect();return {h:Math.round(r.height),txt:i.innerText.length}}")
        ok(t+'tocco su un nodo: pannello dettagli popolato',ip['h']>40 and ip['txt']>20,ip)
        # viewport dinamica
        for hh in (H-100,H,H-70):
            pg.set_viewport_size({'width':W,'height':hh}); pg.wait_for_timeout(250)
            ok(t+'viewport %d: nessun overflow orizzontale della pagina'%hh,pg.evaluate("()=>document.documentElement.scrollWidth<=innerWidth+1"))
            g=pg.evaluate("()=>{const o=document.querySelector('.multiverse-graph-overlay');const r=o.getBoundingClientRect();return {top:r.top,bottom:r.bottom,ih:innerHeight}}")
            ok(t+'viewport %d: il fondo della pagina e\' dietro al viewport (nessuna area scoperta)'%hh,g['bottom']>=g['ih']-1,g)
        pg.set_viewport_size({'width':W,'height':H})
        ok(t+'nessun errore JS',errs==[],errs[:2]); ctx.close()
    b.close()
done()
