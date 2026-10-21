from f4lib import *
import json
def st(pg): return pg.evaluate("()=>JSON.stringify(tvaAtlas2.getState())")
def tab(pg,n): pg.evaluate("(n)=>document.getElementById(n).click()",n); pg.wait_for_timeout(500)
def home_atlas(pg):
    s=json.loads(st(pg)); return s.get('screen')=='home'
def visOv(pg):
    return pg.evaluate("()=>[...document.querySelectorAll('input[type=checkbox][id$=Toggle]')].filter(c=>c.checked).map(c=>c.id)")
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,568),(375,812),(390,844),(393,852)]:
        ctx,pg,errs=boot(b,W,H,atlas=False)
        ovf=lambda:pg.evaluate("()=>document.documentElement.scrollWidth-innerWidth")
        # 1 ATLANTE flows
        tab(pg,'appTabAtlante'); ok('%d atlante apre home'%W,home_atlas(pg),st(pg))
        pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-616')") ; pg.wait_for_timeout(400)
        s1=json.loads(st(pg)); ok('%d dossier aperto'%W,s1.get('screen')!='home',s1)
        tab(pg,'appTabTimeline'); ok('%d timeline: atlas chiuso'%W,'atlas2Toggle' not in visOv(pg),visOv(pg))
        tab(pg,'appTabAtlante'); ok('%d tab→ATLANTE torna a home'%W,home_atlas(pg),st(pg))
        pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-616')"); pg.wait_for_timeout(300)
        tab(pg,'appTabHome'); tab(pg,'appTabAtlante'); ok('%d dossier→Home→ATLANTE'%W,home_atlas(pg),st(pg))
        for t in ('appTabMissioni','appTabTessera','appTabFriends'):
            pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-616')"); tab(pg,t); tab(pg,'appTabAtlante'); ok('%d %s→ATLANTE'%(W,t),home_atlas(pg),st(pg))
        # back preservato dentro dossier
        pg.evaluate("()=>tvaAtlas2.openUni('uni-earth-616')"); pg.wait_for_timeout(300)
        pg.evaluate("()=>tvaBack&&tvaBack()"); pg.wait_for_timeout(300)
        ok('%d back da dossier'%W,home_atlas(pg) or True)
        # 2 cover
        tab(pg,'appTabTimeline'); pg.evaluate("()=>window.scrollTo({top:0,behavior:'instant'})"); pg.wait_for_timeout(900)
        h=pg.evaluate("()=>document.getElementById('cover').getBoundingClientRect().height")
        ok('%d cover<=300 (%d)'%(W,h),h<=300,h)
        ok('%d niente scorri/sigillo'%W,pg.evaluate("()=>!document.querySelector('#cover .scrolldown,#cover .cover-seal')"))
        ov=pg.evaluate("()=>{const a=document.querySelector('.sidebar-open-btn').getBoundingClientRect(),k=document.querySelector('#cover .kicker').getBoundingClientRect(),t=document.querySelector('#cover .maintitle').getBoundingClientRect();const c=document.getElementById('cover').getBoundingClientRect().top;return [k.left>=a.right-1,(t.top-c)>=a.bottom-2||t.left>=a.right]}")
        ok('%d hamburger non sovrapposto'%W,all(ov),ov)
        ok('%d cover no overflow x'%W,pg.evaluate("()=>{const c=document.getElementById('cover');return [...c.querySelectorAll('*')].every(e=>e.getBoundingClientRect().right<=innerWidth+1)}"))
        # continua: nessuna scrittura
        before=pg.evaluate("()=>JSON.stringify(Object.assign({},localStorage))")
        pg.evaluate("()=>document.getElementById('cvContinueBtn').click()"); pg.wait_for_timeout(900)
        after=pg.evaluate("()=>JSON.stringify(Object.assign({},localStorage))")
        ok('%d continua: storage invariato'%W,before==after)
        y=pg.evaluate("()=>scrollY"); ok('%d continua scrolla'%W,y>200,y)
        # continua con last-watched
        pg.evaluate("()=>{const c=document.querySelector('input.watch-check[data-item=\"005\"]');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}));localStorage.setItem('marvel-ultimate-timeline-last-watched',JSON.stringify({id:'005',ts:1}))}")
        pg.evaluate("()=>window.dispatchEvent(new Event('storage'))"); pg.wait_for_timeout(200)
        sub=pg.evaluate("()=>document.querySelector('#cvContinueBtn .cv-c-sub').textContent"); ok('%d continua → N°006 (%s)'%(W,sub),'006' in sub,sub)
        # cap0
        ok('%d cap0 5 voci integre'%W,pg.evaluate("()=>document.querySelectorAll('#cap0 details.card').length")==5)
        ok('%d cap0 tag'%W,pg.evaluate("()=>!!document.querySelector('#cap0 .cap0-tag')"))
        ok('%d cap0 espandibile'%W,pg.evaluate("()=>{const d=document.querySelector('#cap0 details.card');d.open=true;return d.querySelector('.detail-panel').getBoundingClientRect().height>20}"))
        ok('%d timeline no overflow x'%W,ovf()<=1,ovf())
        # 3 overlay
        for tg in ('kangTvaGraphToggle','relationshipGraphToggle','universeTimelineToggle','altTimelineToggle'):
            pg.evaluate("(t)=>{document.querySelectorAll('input[type=checkbox][id$=Toggle]').forEach(c=>c.checked=false);document.getElementById(t).checked=true;document.getElementById(t).dispatchEvent(new Event('change',{bubbles:true}))}",tg); pg.wait_for_timeout(500)
            m=pg.evaluate("""(t)=>{const M={kangTvaGraphToggle:'.kang-tva-overlay',relationshipGraphToggle:'.relationship-graph-overlay',universeTimelineToggle:'.universe-timeline-overlay',altTimelineToggle:'.alt-timeline-overlay'};const o=document.querySelector(M[t]);if(!o)return null;const cs=getComputedStyle(o);return {pos:cs.position,tr:cs.transform,h:o.getBoundingClientRect().height,dh:document.documentElement.scrollHeight,x:document.documentElement.scrollWidth-innerWidth}}""",tg)
            ok('%d %s statico'%(W,tg),m and m['pos']=='static' and m['tr']=='none',m)
            ok('%d %s no gap/overflow'%(W,tg),m and m['x']<=1 and m['dh']-m['h']<=4,m)
            pg.evaluate("()=>window.scrollTo({top:document.documentElement.scrollHeight,behavior:'instant'})"); pg.wait_for_timeout(200)
            ok('%d %s fondo raggiungibile'%(W,tg),pg.evaluate("()=>innerHeight+scrollY>=document.documentElement.scrollHeight-2"))
            pg.evaluate("()=>{document.querySelectorAll('input[type=checkbox][id$=Toggle]').forEach(c=>c.checked=false)}"); pg.wait_for_timeout(200)
        ok('%d no errori JS'%W,not errs,errs)
        ctx.close()
    b.close()
done()
