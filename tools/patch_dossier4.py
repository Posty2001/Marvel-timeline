#!/usr/bin/env python3
"""Fase 4 — Dossier e Archivi. Idempotente. Uso: patch_dossier4.py hook | inject
 hook   : punti di aggancio minimi nei sorgenti (tools/atlas2.js, tools/net_module.js) e nell'index.html (esposizione in sola lettura delle dipendenze)
 inject : inietta tools/xref.js, tools/dossier4.js, tools/dossier4.css in index.html (in coda al body, dopo gli altri moduli)"""
import re,sys
W='/home/claude/work/'; T=W+'tools/'; P=W+'index.html'
def rd(p): return open(p,encoding='utf-8').read()
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
def rep(s,old,new,tag):
    if new in s: return s
    assert s.count(old)==1,(tag,s.count(old))
    return s.replace(old,new)
def hook():
    a=rd(T+'atlas2.js')
    # 1) la ricerca universale puo' essere sostituita da un modulo successivo (ritorna true se ha gestito la query)
    a=rep(a,"    function drawResults(box, raw) {\n      box.textContent = '';\n",
          "    function drawResults(box, raw) {\n      box.textContent = '';\n      if (EXT.drawResults && EXT.drawResults(box, raw)) return;   /* F4: ricerca tollerante (dossier4.js) */\n",'drawResults')
    # 2) API aggiuntive per i ponti (nessuna logica nuova)
    a=rep(a,"setScroll: setScroll, openArchive: openArchive,","setScroll: setScroll, NOTA_NUM: NOTA_NUM, openMappa: openMappa, crOpen: crOpen, openUni: openUni, openArchive: openArchive,",'extapi')
    wr(T+'atlas2.js',a)
    n=rd(T+'net_module.js')
    n=rep(n,"W.tvaNavStato = function () { return { depth: stack.length, last: stack.length ? stack[stack.length - 1] : null }; };",
          "W.tvaNavStato = function () { return { depth: stack.length, last: stack.length ? stack[stack.length - 1] : null, labels: stack.map(function (x) { return x.lbl || ''; }) }; };",'navstato')
    wr(T+'net_module.js',n)
    s=rd(P)
    # 3) dipendenze: esposizione in sola lettura (nessuna modifica ai dati ne' alla logica dei suggerimenti)
    mark="    '128': ['122'], '131': ['130'], '134': ['120'], '135': ['093'], '137': ['128'], '138': ['131']\n  };\n"
    add=mark+"  /* F4: lettura (copia) per il Dossier Opera; non modifica PREREQ_DIRETTI_JS / DEPENDENCY_MAP_JS */\n  window.marvelDipendenzeLettura = function() { return JSON.parse(JSON.stringify({ prereq: PREREQ_DIRETTI_JS, map: DEPENDENCY_MAP_JS, motivi: DEP_MOTIVI_JS })); };\n"
    s=rep(s,mark,add,'dip')
    wr(P,s)
    print('hook ok')
def inject():
    s=rd(P)
    css='/* D4-CSS-BEGIN */\n'+rd(T+'dossier4.css').rstrip()+'\n/* D4-CSS-END */\n'
    if '/* D4-CSS-BEGIN */' in s: s=re.sub(r'/\* D4-CSS-BEGIN \*/.*?/\* D4-CSS-END \*/\n',lambda m:css,s,flags=re.S)
    else:
        k='/* SC-CSS-END */\n'; assert s.count(k)==1
        i=s.index(k)+len(k); s=s[:i]+css+s[i:]
    for sid,f in (('tva-xref','xref.js'),('tva-dossier4','dossier4.js')):
        js='<script id="%s">\n'%sid+rd(T+f)+'</script>\n'
        if '<script id="%s">'%sid in s: s=re.sub(r'<script id="%s">.*?</script>\n'%sid,lambda m:js,s,flags=re.S)
        else:
            i=s.rindex('</body>'); s=s[:i]+js+s[i:]
    wr(P,s); print('inject ok',len(s.encode()))
{'hook':hook,'inject':inject}[sys.argv[1]]()
