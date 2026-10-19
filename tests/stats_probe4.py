from leg_shot import *
import json
with sync_playwright() as p:
    b=p.chromium.launch(); ctx,pg,errs=boot(b)
    r=pg.evaluate("""()=>{const A=tvaAtlas2.ext.api,I=A.IDX;const T=Object.values(I.titoli);
      const set=f=>{const s=new Set();T.filter(f).forEach(t=>(t.unis||[]).forEach(u=>s.add(u)));return s};
      const all=set(()=>true), core=set(t=>t.kind==='item'&&!t.variant), noP4=set(t=>t.kind!=='p4'), itemAnim=set(t=>(t.kind==='item'||t.kind==='anim'));
      const only=(a,b)=>[...a].filter(x=>!b.has(x));
      return {all:all.size,core:core.size,noP4:noP4.size,itemAnim:itemAnim.size,uniN:Object.keys(A.UNI).length,
       notInTitles:Object.keys(A.UNI).filter(u=>!all.has(u)),p4only:only(all,noP4),unisSample:T.slice(0,2).map(t=>t.unis),
       ukeysTitles:Object.keys(A.UNI).slice(0,3)}}""")
    print(json.dumps(r,ensure_ascii=False,indent=1)); b.close()
