from leg_shot import *
import collections,json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    ids=pg.evaluate("()=>Object.keys(tvaIdx.personaggi)")
    res=pg.evaluate("""(ids)=>{const out={};for(const id of ids){tvaAtlas2.setState({screen:'char',eid:id});tvaAtlas2.onOpen();const b=document.querySelector('.a2-scroll');out[id]=[...b.querySelectorAll('h3')].map(x=>x.textContent.trim()).filter(Boolean).length;}return out}""",ids)
    c=collections.Counter(res.values()); print(sorted(c.items()))
    pg.evaluate("()=>1"); print(errs)
    # apps count distribution
    apps=pg.evaluate("()=>Object.values(tvaIdx.personaggi).map(c=>c.apps.length)")
    print('apps==1:',sum(1 for a in apps if a==1),'>=5:',sum(1 for a in apps if a>=5),'max',max(apps))
