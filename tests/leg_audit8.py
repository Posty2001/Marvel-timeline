from playwright.sync_api import sync_playwright
from leg_shot import boot
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const out={};
      for (const [k,t] of [['graph','multiverseGraphToggle'],['utl','universeTimelineToggle'],['atl','altTimelineToggle'],['rel','relationshipGraphToggle'],['kang','kangTvaGraphToggle']]){
        const ov=document.getElementById(t).nextElementSibling; // overlay?
        const cont=document.querySelector('#'+t+' ~ *');
        out[k]=null}
      return out}""")
    # find overlay elements by their toggle's sibling selectors in CSS: look at element containing label for toggle
    r=pg.evaluate("""()=>{const out={};
      for (const [k,t] of [['graph','multiverseGraphToggle'],['utl','universeTimelineToggle'],['atl','altTimelineToggle'],['rel','relationshipGraphToggle'],['kang','kangTvaGraphToggle']]){
        const lb=[...document.querySelectorAll('label.mg-back-btn[for='+t+']')][0]; let ov=lb.parentElement; while(ov && !(ov.id||/overlay|mg-/.test(ov.className)) && ov.parentElement) ov=ov.parentElement;
        const svgs=[...ov.querySelectorAll('svg')].map(s=>({id:s.id,vb:s.getAttribute('viewBox'),w:s.getAttribute('width'),cls:s.getAttribute('class'),r:Math.round(s.getBoundingClientRect().width)}));
        out[k]={id:ov.id,cls:ov.className,svgs:svgs.slice(0,6),nodes:ov.querySelectorAll('.mg-node,.kg-node,[data-node],g.node').length,html:ov.innerHTML.length,scrollers:[...ov.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return /(auto|scroll)/.test(s.overflowX)&&e.scrollWidth>e.clientWidth+4}).map(e=>e.className||e.id).slice(0,5)}}
      return out}""")
    for k,v in r.items(): print(k,json.dumps(v,ensure_ascii=False)); print()
    b.close()
