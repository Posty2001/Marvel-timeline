from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for tog in ['multiverseGraphToggle','universeTimelineToggle','altTimelineToggle','relationshipGraphToggle','kangTvaGraphToggle']:
        pg.evaluate("()=>{marvelChiudiOverlay()}"); pg.wait_for_timeout(200)
        pg.evaluate("(t)=>{const c=document.getElementById(t);c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}",tog); pg.wait_for_timeout(900)
        print(tog, pg.evaluate("""(t)=>{const o=document.getElementById(t).parentNode.querySelector('.'+({multiverseGraphToggle:'multiverse-graph-overlay',universeTimelineToggle:'universe-timeline-overlay',altTimelineToggle:'alt-timeline-overlay',relationshipGraphToggle:'relationship-graph-overlay',kangTvaGraphToggle:'kang-tva-overlay'})[t]);
        return [...o.querySelectorAll('svg')].map(s=>{const r=s.getBoundingClientRect();const p=s.parentElement;return {w:Math.round(r.width),h:Math.round(r.height),vb:s.getAttribute('viewBox'),par:p.className,pw:p.clientWidth,psw:p.scrollWidth,id:s.id}})}""",tog))
    pg.evaluate("()=>{marvelChiudiOverlay()}")
    # relation graph with a search
    pg.evaluate("()=>{const c=document.getElementById('relationshipGraphToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(600)
    pg.fill('#rgSearchInput','Wanda'); pg.wait_for_timeout(500)
    print(pg.evaluate("()=>document.getElementById('rgSearchResults').innerHTML.slice(0,400)"))
    print(errs); b.close()
