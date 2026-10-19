from f4lib import *
with sync_playwright() as p:
    b=p.chromium.launch()
    for W,H in [(320,640),(375,812),(390,844),(393,852)]:
        ctx=b.new_context(viewport={'width':W,'height':H},is_mobile=True,has_touch=True,service_workers='block',device_scale_factor=2); pg=ctx.new_page(); pg.set_default_timeout(8000); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(U); pg.wait_for_timeout(800)
        pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(300)
        pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(500)
        bad=[];small=[];n=0
        js="""()=>{const r=document.querySelector('.a2');const W=innerWidth;const o=[];
         if(document.documentElement.scrollWidth>W+1)o.push('doc '+document.documentElement.scrollWidth);
         const sc=document.querySelector('.a2-scroll');if(sc&&sc.scrollWidth>sc.clientWidth+1)o.push('scroll '+sc.scrollWidth);
         const s=[];r.querySelectorAll('button,a,[data-go],.d4-tf-b,.d4-jump *').forEach(e=>{const b=e.getBoundingClientRect();if(b.width&&b.height&&(b.height<43.5)&&getComputedStyle(e).visibility!=='hidden'&&e.offsetParent&&(e.matches('button,a,[data-go]')))s.push((e.className||e.tagName)+':'+Math.round(b.height))});
         return {o,s:s.slice(0,4),ns:s.length}}"""
        def chk(lbl):
            global n
            r=pg.evaluate(js); n+=1
            if r['o']: bad.append((lbl,r['o']))
            if r['ns']: small.append((lbl,r['ns'],r['s']))
        its=pg.evaluate("()=>Object.keys(tvaIdx.titoli).filter((_,i)=>i%5==0)")
        for i in its: pg.evaluate("(i)=>tvaGo('item',i)",i); pg.wait_for_timeout(60); chk('item '+i)
        for c in pg.evaluate("()=>Object.keys(tvaIdx.personaggi).filter((_,i)=>i%15==0)"): pg.evaluate("(i)=>tvaGo('char',i)",c); pg.wait_for_timeout(60); chk('char '+c)
        for a in pg.evaluate("()=>tvaAtlas2.arcModel().list.filter((_,i)=>i%4==0).map(e=>e.cat+':'+e.id)"): pg.evaluate("(i)=>tvaGo('arc',i)",a); pg.wait_for_timeout(60); chk('arc '+a)
        for a in pg.evaluate("()=>tvaXref.attori().list.filter((_,i)=>i%6==0).map(a=>a.id)"): pg.evaluate("(i)=>tvaGo('att',i)",a); pg.wait_for_timeout(60); chk('att '+a)
        for q in ['shield','x men','jackman']:
            pg.evaluate("(q)=>{tvaAtlas2.setState({screen:'cerca',q:q})}",q); pg.wait_for_timeout(200); chk('cerca '+q)
        ok('VP%d nessun overflow orizzontale (%d schermate)'%(W,n),not bad,bad[:3])
        print('  target <44px (info):',len(small),small[:2])
        ok('VP%d nessun errore JS'%W,errs==[],errs[:2]); ctx.close()
    # reduced motion
    ctx=b.new_context(viewport={'width':390,'height':844},reduced_motion='reduce',service_workers='block'); pg=ctx.new_page(); pg.goto(U); pg.wait_for_timeout(700)
    pg.evaluate("()=>{journeyStarted.checked=true;homeHubExited.checked=true;journeyStarted.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.evaluate("()=>tvaAtlas2.enter()"); pg.wait_for_timeout(400); pg.evaluate("()=>tvaGo('item','item-023')"); pg.wait_for_timeout(300)
    an=pg.evaluate("()=>[...document.querySelectorAll('.d4-opera, .d4-opera *')].filter(e=>{const c=getComputedStyle(e);return c.animationName!=='none'&&parseFloat(c.animationDuration)>0.01}).length")
    ok('VP-RM nessuna animazione attiva con reduced-motion',an==0,an)
    b.close()
done()
