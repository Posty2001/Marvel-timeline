from leg_shot import *
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    for cat in ['org','art','evt','luo','cos','spe','mis','pot']:
        pg.evaluate("(s)=>{tvaAtlas2.setState(s);tvaAtlas2.onOpen()}",{'screen':'potenza' if cat=='pot' else 'arch','arc':cat,'eid':None,'af':'tutti','aq':'','au':'tutti'}); pg.wait_for_timeout(500)
        r=pg.evaluate("""()=>{const body=document.querySelector('.a2-scroll'); const cards=[...body.querySelectorAll('button,a')].filter(x=>x.className&&/a2-(arc|lrow|card|ent)/.test(x.className)); return {n:cards.length,cls:[...new Set(cards.map(x=>x.className))].slice(0,4),head:body.querySelector('.a2-lead, .a2-head p, header p')?.textContent?.slice(0,120)}}""")
        print(cat,r)
