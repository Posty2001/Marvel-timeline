import json
from playwright.sync_api import sync_playwright
F='file:///home/claude/work/index.html'
JS="""()=>{
 const I=window.tvaIdx, out={};
 const gos=(root,k)=>[...root.querySelectorAll('[data-go^="'+k+':"]')].map(a=>a.getAttribute('data-go').slice(k.length+1));
 // A: item->uni
 const A={}; Object.values(I.titoli).forEach(t=>{A[t.id]=[...new Set(gos(t.li,'uni'))]});
 const B={}; // uni->item (indice) e classica
 const uids=Object.keys(JSON.parse(document.getElementById('mvMapData').textContent).universi);
 const Bidx={},Bcls={},Ba2={};
 uids.forEach(u=>{Bidx[u]=I.titoliDi(u).map(e=>e.id);const c=document.getElementById(u);Bcls[u]=[...new Set(gos(c,'item'))]});
 const missAB=[],extraAB=[];
 Object.keys(A).forEach(id=>A[id].forEach(u=>{if(!Bidx[u]||!Bidx[u].includes(id))missAB.push(id+'->'+u)}));
 uids.forEach(u=>Bidx[u].forEach(id=>{if(!(A[id]||[]).includes(u))extraAB.push(u+'->'+id)}));
 out.itemUni={itemsWithUni:Object.values(A).filter(x=>x.length).length,missAB:missAB.slice(0,10),nMissAB:missAB.length,extraAB:extraAB.slice(0,10),nExtraAB:extraAB.length};
 const clsMiss=[];uids.forEach(u=>{Bidx[u].forEach(id=>{if(!Bcls[u].includes(id))clsMiss.push(u+':'+id)});Bcls[u].forEach(id=>{if(!Bidx[u].includes(id))clsMiss.push('extra '+u+':'+id)})});
 out.classicUniItems={n:clsMiss.length,s:clsMiss.slice(0,10)};
 // B: item->char vs char->item
 const IC={}; Object.values(I.titoli).forEach(t=>{IC[t.id]=[...new Set(gos(t.li,'char'))]});
 const CI={}; Object.values(I.personaggi).forEach(c=>{CI[c.id]=[...new Set(gos(c.li,'item'))]});
 const m1=[],m2=[];
 Object.keys(IC).forEach(id=>IC[id].forEach(c=>{if(!(CI[c]||[]).includes(id))m1.push(id+'->'+c)}));
 Object.keys(CI).forEach(c=>CI[c].forEach(id=>{if(!(IC[id]||[]).includes(id.length&&c))/*noop*/0; if(!(IC[id]||[]).includes(c))m2.push(c+'->'+id)}));
 out.itemChar={items:Object.values(IC).filter(x=>x.length).length,chars:Object.values(CI).filter(x=>x.length).length,nItemNoBack:m1.length,s1:m1.slice(0,8),nCharNoBack:m2.length,s2:m2.slice(0,8)};
 // C: char->uni vs uni->char
 const CU={}; Object.values(I.personaggi).forEach(c=>{CU[c.id]=[...new Set(gos(c.li,'uni'))]});
 const UC={}; uids.forEach(u=>{UC[u]=[...new Set(gos(document.getElementById(u),'char'))]});
 const UCi={}; uids.forEach(u=>UCi[u]=I.personaggiDi(u));
 const n1=[],n2=[],n3=[];
 Object.keys(CU).forEach(c=>CU[c].forEach(u=>{if(!UCi[u].includes(c))n1.push(c+'->'+u)}));
 uids.forEach(u=>UCi[u].forEach(c=>{if(!(CU[c]||[]).includes(u))n2.push(u+'->'+c)}));
 uids.forEach(u=>{UC[u].forEach(c=>{if(!UCi[u].includes(c))n3.push('cls-extra '+u+':'+c)});UCi[u].forEach(c=>{if(!UC[u].includes(c))n3.push('cls-miss '+u+':'+c)})});
 out.charUni={charsWithUni:Object.values(CU).filter(x=>x.length).length,nCharNoBack:n1.length,s1:n1.slice(0,8),nUniNoChar:n2.length,s2:n2.slice(0,12),nClassicDiff:n3.length,s3:n3.slice(0,8)};
 return out}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844}); pg.goto(F); pg.wait_for_timeout(1500)
    print(json.dumps(pg.evaluate(JS),indent=1,ensure_ascii=False)); b.close()
