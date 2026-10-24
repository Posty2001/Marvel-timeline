import sys,json
from playwright.sync_api import sync_playwright
art=open('/home/claude/work/tools/tc_art.js',encoding='utf-8').read()
exec(open('/tmp/claude-0/t/gal.py').read().split("items=[]")[0].split("what=sys.argv[1]")[1].replace("sys.argv","[]")) if False else None
FR=['cornice-standard-tva','cornice-bronzo-temporale','cornice-argento-cronologico','cornice-oro-archivista','cornice-acciaio-mutante','cornice-energia-arcana','cornice-tecnologia-stark','cornice-wakanda','cornice-asgard','cornice-vuoto-temporale','cornice-incursione-rossa','cornice-nexus-supremo']
TH=['tema-tva-classico','tema-archivio-notturno','tema-cronologia-dorata','tema-multiverso-cremisi','tema-tecnologia-futuristica','tema-universo-mutante','tema-energia-mistica','tema-ombre-del-vuoto','tema-nexus-cosmico','tema-fine-del-tempo']
M={'name':'Franco Posteraro','title':'Sovrano delle Linee Temporali','id':'VAR-345047','level':22,'xp':8473,'xpCur':73,'xpNeed':730,'badges':[{'id':'critico','name':'Critico Ufficiale'},{'id':'linea-sacra','name':'Guardiano della Linea Sacra'},{'id':'cinefilo','name':'Cinefilo TVA'}],'avatar':{'kind':'preset','id':'agente'},'fx':None,'frameName':'x','themeName':'y'}
JS="""([FR,TH,M])=>{const out=[];let n=0;
for(const f of FR)for(const t of TH)for(const lay of ['wide','compact','vertical']){
 const d=document.createElement('div');d.style.cssText='position:absolute;left:0;top:0;width:800px';d.innerHTML=tvaCardArt.build(Object.assign({},M,{frame:f,theme:t}),lay,{uid:'z'+(n++)});document.body.appendChild(d);
 const svg=d.firstChild,r0=svg.getBoundingClientRect(),vb=svg.viewBox.baseVal,k=vb.width/r0.width;
 const gs=[...svg.children].filter(e=>e.tagName=='g');const fr=gs[gs.length-1];
 const box=e=>{const r=e.getBoundingClientRect();return [(r.left-r0.left)*k,(r.top-r0.top)*k,(r.right-r0.left)*k,(r.bottom-r0.top)*k]};
 const content=[...svg.querySelectorAll('text, .tc-avatar, rect[stroke-width="3"], g[transform] > circle[fill="rgba(0,0,0,0.35)"]')].filter(e=>!fr.contains(e)).map(box);
 [...svg.querySelectorAll('clipPath')].forEach(c=>{const q=c.firstElementChild;if(q&&!fr.contains(c)){const bb=q.getBBox();content.push([bb.x,bb.y,bb.x+bb.width,bb.y+bb.height])}});
 const hits=[];
 for(const e of fr.querySelectorAll('path,rect,polygon,circle,ellipse')){
  if(e.closest('defs')||(e.getAttribute('fill')||'').startsWith('url(#')&&e.tagName=='circle'&&e.getAttribute('r')=='34')continue;const b=box(e),w=b[2]-b[0],h=b[3]-b[1];
  if(w>vb.width*0.45&&h>vb.height*0.45)continue; // anelli perimetrali
  if(w>vb.width*0.45||h>vb.height*0.45){ /* segmenti lunghi: controlla solo il tratto */ }
  for(const c of content){const ix=Math.min(b[2],c[2])-Math.max(b[0],c[0]),iy=Math.min(b[3],c[3])-Math.max(b[1],c[1]);if(ix>2&&iy>2){hits.push([e.tagName,Math.round(ix),Math.round(iy)]);break}}
 }
 out.push([f,t,lay,hits.length,hits.slice(0,3)]);d.remove();
}
return out}"""
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':900,'height':900})
    pg.set_content('<body style="margin:0">'); pg.add_script_tag(content=art)
    r=pg.evaluate(JS,[FR,TH,M]); b.close()
bad=[x for x in r if x[3]>0]
print(len(r),'render; overlap:',len(bad))
from collections import Counter
print(Counter((x[0][9:],x[2]) for x in bad).most_common(30))
for x in bad[:12]: print(x)
