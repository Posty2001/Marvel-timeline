from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('universeTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(900)
    print(pg.evaluate("""()=>{const r=document.querySelector('.ut-label-row[data-lane=tva]'),l=document.querySelector('.ut-lane-line[data-lane=tva]');const cs=getComputedStyle(r);const lab=document.querySelector('.ut-labels-fixed');return {row:r.getBoundingClientRect().toJSON(),line:l.getBoundingClientRect().toJSON(),disp:cs.display,ai:cs.alignItems,pt:cs.paddingTop,pb:cs.paddingBottom,lh:cs.lineHeight,tr:lab.style.transform,labTop:lab.getBoundingClientRect().top,svgTop:document.querySelector('.ut-svg').getBoundingClientRect().top}}"""))
    b.close()
