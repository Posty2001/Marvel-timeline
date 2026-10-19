import sys,re; sys.path.insert(0,'/home/claude/work/tools/edits')
from jb import edit_json,rep
p='/home/claude/work/index.html'; s=open(p,encoding='utf-8').read()
# 1) riga UNIVERSI della pagina Kingpin (Spider-Verse)
a=s.index('<li class="card-wrap" id="char-kingpin"'); b=s.index('</details></li>',a)
seg=s[a:b]; old='<span class="detail-v">Animato Sony, NON canonico MCU · MCU</span>'
assert seg.count(old)==1; seg=seg.replace(old,'<span class="detail-v">Animato Sony, NON canonico MCU</span>'); s=s[:a]+seg+s[b:]
# 2) link inline errati nelle 3 pagine MCU (Hawkeye): -> Wilson Fisk/Kingpin
LK="mvNavigate('char-kingpin','char','K')\" class=\"mv-inline-link\">Kingpin</a>"
LF="mvNavigate('char-wilson-fisk-kingpin','char','W')\" class=\"mv-inline-link\">Kingpin</a>"
for cid in ('char-yelena-belova','char-clint-barton','char-kate-bishop'):
    a=s.index('<li class="card-wrap" id="%s"'%cid); b=s.index('</details></li>',a); seg=s[a:b]
    assert seg.count(LK)==1,cid; s=s[:a]+seg.replace(LK,LF)+s[b:]
# 3) grafo
E3={"type":"char"}
def g(o):
    K=o['char-kingpin']['conns']; n0=len(K)
    o['char-kingpin']['conns']=[c for c in K if c['id'] not in ('char-yelena-belova','char-clint-barton','char-kate-bishop','universo-mcu')]
    assert len(o['char-kingpin']['conns'])==n0-4
    for cid in ('char-yelena-belova','char-clint-barton','char-kate-bishop'):
        hit=[c for c in o[cid]['conns'] if c['id']=='char-kingpin']; assert len(hit)==1
        hit[0]['id']='char-wilson-fisk-kingpin'; hit[0]['name']='Wilson Fisk/Kingpin'
    F=o['char-wilson-fisk-kingpin']['conns']
    ins=[i for i,c in enumerate(F) if c['type']=='universo']; pos=ins[0] if ins else len(F)
    for k,(cid,nm) in enumerate((('char-yelena-belova','Yelena Belova'),('char-clint-barton','Clint Barton/Occhio di Falco'),('char-kate-bishop','Kate Bishop'))):
        F.insert(pos+k,{"id":cid,"type":"char","name":nm,"label":"Appare insieme in","rtype":"titolo"})
    um=o['universo-mcu']['conns']; n1=len(um)
    o['universo-mcu']['conns']=[c for c in um if c['id']!='char-kingpin']; assert len(o['universo-mcu']['conns'])==n1-1
s=edit_json(s,'relationshipGraphData',g)
# 4) conteggio salvato MCU coerente con la riga (Kingpin non piu' MCU)
def mvf(o):
    u=o['universi']['uni-earth-199999-mcu']; assert u['personaggi']==207; u['personaggi']=206
s=edit_json(s,'mvMapData',mvf)
open(p,'w',encoding='utf-8').write(s); print('intE ok')
