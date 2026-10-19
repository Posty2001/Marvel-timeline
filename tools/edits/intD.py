import sys; sys.path.insert(0,'/home/claude/work/tools/edits')
from jb import edit_json,rep
p='/home/claude/work/index.html'; s=open(p,encoding='utf-8').read()
NID='uni-fantastic-four-1994'
# 1) opera N°028: data-uni + riga UNIVERSO
a=s.index('<li class="card-wrap" id="item-028"'); b=s.index('</li>',s.index('</details>',a))
seg=s[a:b]
assert seg.count('data-uni="uni-earth-121698"')==1 and seg.count('<span class="detail-v">Legacy, continuità isolata</span>')==1
seg=seg.replace('data-uni="uni-earth-121698"','data-uni="%s"'%NID).replace('<span class="detail-v">Legacy, continuità isolata</span>','<span class="detail-v">Legacy, Fantastic Four (1994), continuità isolata</span>')
s=s[:a]+seg+s[b:]
# 2) card Atlante (prima di Earth-121698, ordine cronologico 1994 -> 2005 -> 2015)
card='''<li class="card-wrap" id="%s" data-search="fantastic four (1994)"><details class="card">
          <summary>
            <span class="ic">&#127760;</span>
            <div class="item-body"><div class="item-top"><span class="title">Fantastic Four (1994)</span></div></div>
            <span class="chev">&#9656;</span>
          </summary>
          <div class="detail-panel">
            <div class="detail-row"><span class="detail-k">DESCRIZIONE</span><span class="detail-v">Universo isolato del film Fantastic Four (1994), prodotto da Roger Corman su commissione e mai distribuito ufficialmente.</span></div>
            <div class="detail-row"><span class="detail-k">COMPARE IN</span><span class="detail-v">Parte 1bis &middot; 1F</span></div>
          </div>
        </details></li>
'''%NID
anchor='<li class="card-wrap" id="uni-earth-121698"'
assert s.count(anchor)==1
s=s.replace(anchor,card+anchor)
# 3) mvMapData
def mvf(o):
    U=o['universi']; u=U['uni-earth-121698']
    assert u['titoliIds']==['028','029','030']
    u['titoli']=2; u['film']=2; u['titoliIds']=['029','030']
    new={"nome":"Fantastic Four (1994)","titoli":1,"personaggi":0,"eventi":0,"varianti":0,"film":1,"serie":0,
         "personaggiPrincipali":["Reed Richards","Sue Storm","Johnny Storm","Ben Grimm","Victor von Doom"],"titoliIds":["028"]}
    out={}
    for k,v in U.items():
        if k=='uni-earth-121698': out[NID]=new
        out[k]=v
    o['universi']=out
    L=o['famiglie']['legacy']['universi']; L.insert(L.index('uni-earth-121698'),NID)
s=edit_json(s,'mvMapData',mvf)
open(p,'w',encoding='utf-8').write(s); print('intD ok')
