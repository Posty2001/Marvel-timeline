import json,re
from playwright.sync_api import sync_playwright
from leg_shot import boot
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    pg.evaluate("()=>{document.getElementById('altTimelineToggle').checked=true;document.getElementById('altTimelineToggle').dispatchEvent(new Event('change',{bubbles:true}))}"); pg.wait_for_timeout(500)
    pg.click('.at-mode-btn[data-mode=events]'); pg.wait_for_timeout(500)
    rows=pg.evaluate("""()=>[...document.querySelectorAll('#atList li')].map(l=>l.classList.contains('at-group-head')?['H',l.textContent]:['R',l.dataset.num,l.querySelector('.at-row-sub').textContent])""")
    UMy=pg.evaluate("""()=>{const UM=tvaUniverse,atl=JSON.parse(document.getElementById('atlasData').textContent),O={};atl.opere.forEach(o=>O[o.id]=o);const r={};Object.keys(O).forEach(id=>{const y=UM.annoAmbientazione(O[id].ambientazione);r[id]=[y.y,y.approx]});return r}""")
    diff=[];n=0
    for r in rows:
        if r[0]!='R': continue
        n+=1; num=('000'+r[1])[-3:]; sub=r[2]
        m=re.search(r'·\s*(~?)(\d+)( a\.C\.)?( \(periodo\))?',sub)
        if 'non determinabile' in sub or not m:
            ay=None
        else:
            ay=(-int(m.group(2)) if m.group(3) else int(m.group(2)))
        um=UMy.get(num,[None,None])[0]
        if ay!=um: diff.append((num,sub[:90],'alt=',ay,'um=',um))
    print('righe',n,'differenze',len(diff))
    for d in diff: print(d)
    print(pg.evaluate("()=>{const atl=JSON.parse(document.getElementById('atlasData').textContent);const c={};atl.opere.forEach(o=>c[o.precisioneUscita]=(c[o.precisioneUscita]||0)+1);return c}"))
    b.close()
