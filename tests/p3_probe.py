from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{const c=document.getElementById('altTimelineToggle');c.checked=true;c.dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(800)
    pg.evaluate("()=>document.querySelector('#atModes [data-mode=events]').click()"); pg.wait_for_timeout(500)
    r=pg.evaluate("""()=>{const out=[];let g=null;document.querySelectorAll('#atList > *, .at-list > *, #altTimelineList > *').forEach(n=>{if(n.classList.contains('at-group-head')){ if(n.classList.contains('at-group-sub')){g.nd=true;} else {g={name:n.textContent,d:0,nd:0,sub:false};out.push(g);} } else if(g){ if(g.sub||g.nd) g.nd=(typeof g.nd==='number'?g.nd:0)+1; else g.d++; }});return out}""")
    print('TOT datati',sum(x['d'] for x in r),'non datati',sum(x['nd'] if isinstance(x['nd'],int) else 0 for x in r),'gruppi',len(r))
    modes=pg.evaluate("()=>[...document.querySelectorAll('#atModes .at-mode-btn')].map(b=>b.dataset.mode+':'+b.textContent.trim())"); print(modes)
    print(pg.evaluate("()=>document.getElementById('atModes').parentElement.className+' | list id candidates: '+[...document.querySelectorAll('.alt-timeline-overlay [id]')].map(e=>e.id).join(',')"))
    b.close()
