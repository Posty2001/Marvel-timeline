import re,sys
p='/home/claude/work/index.html'; s=open(p,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:80],s.count(old))
    s=s.replace(old,new)
# 1) pagina FF Victor von Doom: via l'attribuzione a RDJ
old="""<span class="detail-k">&#128279; COLLEGAMENTI</span><span class="detail-v">Interpretato da: <a href="javascript:void(0)" onclick="mvNavigate('att-robert-downey-jr','att','R')" class="mv-inline-link">Robert Downey Jr.</a></span>"""
new="""<span class="detail-k">&#128279; COLLEGAMENTI</span><span class="detail-v">Interpretato da: attori diversi per ciascuna continuità dei film Fantastic Four (nessuna scheda attore in Atlante) &middot; Il Dottor Destino MCU è un&rsquo;altra incarnazione: <a href="javascript:void(0)" onclick="mvNavigate('char-robert-downey-jr-dottor-destino','char','R')" class="mv-inline-link">Robert Downey Jr./Dottor Destino</a></span>"""
rep(old,new)
# 2) pagina Doom MCU: aggiungi riga attore
old="""<div class="detail-row"><span class="detail-k">UNIVERSI</span><span class="detail-v">MCU multiversale</span></div>
                
                <div class="detail-row"><span class="detail-k">POTERI</span><span class="detail-v">Sovrano della Latveria"""
new="""<div class="detail-row"><span class="detail-k">UNIVERSI</span><span class="detail-v">MCU multiversale</span></div>
                <div class="detail-row"><span class="detail-k">&#128279; COLLEGAMENTI</span><span class="detail-v">Interpretato da: <a href="javascript:void(0)" onclick="mvNavigate('att-robert-downey-jr','att','R')" class="mv-inline-link">Robert Downey Jr.</a></span></div>
                <div class="detail-row"><span class="detail-k">POTERI</span><span class="detail-v">Sovrano della Latveria"""
rep(old,new)
# 3) scheda attore: ruolo MCU distinto dai film FF
rep("<li>Victor von Doom/Dottor Destino <span class=\"us-result-ref\">&mdash; N&deg;136, MCU (Avengers: Doomsday, nuovo ruolo confermato)</span></li>",
    "<li>Dottor Destino (MCU, incarnazione distinta dal Victor von Doom dei film Fantastic Four) <span class=\"us-result-ref\">&mdash; N&deg;136, MCU (Avengers: Doomsday, nuovo ruolo confermato)</span></li>")
# 4) grafo
sys.path.insert(0,'/home/claude/work/tools/edits')
from jb import edit_json
def g(obj):
    v=obj['char-victor-von-doom']['conns']; n0=len(v)
    obj['char-victor-von-doom']['conns']=[c for c in v if c['id']!='att-robert-downey-jr']; assert len(obj['char-victor-von-doom']['conns'])==n0-1
    a=obj['att-robert-downey-jr']['conns']
    for c in a:
        if c['id']=='char-victor-von-doom':
            c['id']='char-robert-downey-jr-dottor-destino'; c['name']='Robert Downey Jr./Dottor Destino'
    d=obj['char-robert-downey-jr-dottor-destino']['conns']
    idx=[i for i,c in enumerate(d) if c['id']=='universo-mcu-multiversale'][0]
    d.insert(idx,{"id":"att-robert-downey-jr","type":"attore","name":"Robert Downey Jr.","label":"Interpretato da","rtype":"attore"})
s=edit_json(s,'relationshipGraphData',g)
open(p,'w',encoding='utf-8').write(s)
print('intB ok')
