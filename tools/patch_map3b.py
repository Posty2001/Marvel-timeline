#!/usr/bin/env python3
"""Fase 3B — integra la Mappa del Multiverso in atlas2.js/atlas2.css (idempotente). Da eseguire dopo patch_dossier.py e prima di inject_net.py."""
p='/home/claude/work/tools/'
js=open(p+'atlas2.js',encoding='utf-8').read()
new=open(p+'map3b.js',encoding='utf-8').read().rstrip('\n')
B='    /* ==== MAP3B:BEGIN'; E_='    /* ==== MAP3B:END ==== */'
anchor='    /* ---------- apertura / stato ---------- */'
if B in js:
    a=js.index(B); b=js.index(E_)+len(E_); js=js[:a]+new.lstrip('\n')+js[b:]
else:
    i=js.index(anchor); js=js[:i]+new+'\n\n'+js[i:]
def rep(old,newv,cnt=1,guard=None):
    global js
    if (guard or newv) in js: return   # guard: marcatore che la modifica e' gia' presente (anche se patch successive, es. 3C, hanno aggiunto altro accanto)
    assert js.count(old)==cnt,(old,js.count(old)); js=js.replace(old,newv)
# schermata registrata
rep("relazioni: renderRelazioni, catalogo: renderCatalogo,","relazioni: renderRelazioni, mappa: renderMappa, catalogo: renderCatalogo,",1,"mappa: renderMappa")
rep("      if (sc === 'universi') return 'Multiverso';","      if (sc === 'universi') return 'Multiverso';\n      if (sc === 'mappa') return 'Mappa';")
# stato (preservato fra dossier e ritorno)
rep("af: ST.af, aq: ST.aq, au: ST.au, y: body.scrollTop };","af: ST.af, aq: ST.aq, au: ST.au, mp: mpSnap(), y: body.scrollTop };",1,"mp: mpSnap(),")
rep("        draw(); requestAnimationFrame(function () { requestAnimationFrame(function () { setScroll(s.y); }); });","        if (s.mp) ST.mp = JSON.parse(JSON.stringify(s.mp));\n        draw(); requestAnimationFrame(function () { requestAnimationFrame(function () { setScroll(s.y); }); });",1,"if (s.mp) ST.mp")
# nuova azione 'map' e destinazioni
rep("      else if (t === 'tl') openTimeline();","      else if (t === 'map') openMappa();\n      else if (t === 'tl') openTimeline();")
rep("d: 'Il grafico dei rami del multiverso.', kw: 'grafico mappa rami', act: ['tog', 'multiverseGraphToggle'] }","d: 'La mappa interattiva dei 27 universi.', kw: 'grafico mappa rami grafo', act: ['map'] }")
rep("var mp = btn('a2-primary a2-map', 'Apri la mappa del Multiverso', function () { run(['tog', 'multiverseGraphToggle']); }); body.appendChild(mp);",
    "var mp = btn('a2-primary a2-map', 'Apri la mappa del Multiverso', function () { openMappa(); }); mp.id = 'a2OpenMap'; body.appendChild(mp);\n      var mp2 = btn('a2-ghost a2-map2', 'Grafo classico', function () { run(['tog', 'multiverseGraphToggle']); }); mp2.id = 'a2OpenClassic'; body.appendChild(mp2);")
rep("sub: 'Il grafo dei rami', go: ['sez', 'multiverso']","sub: 'La mappa dei rami', go: ['sez', 'multiverso']",2) if js.count("sub: 'Il grafo dei rami'")==2 else rep("sub: 'Il grafo dei rami', go: ['sez', 'multiverso']","sub: 'La mappa dei rami', go: ['sez', 'multiverso']",1)
open(p+'atlas2.js','w',encoding='utf-8').write(js)
# homev2.js: stessa etichetta del portale (la destinazione e' in SEZ.multiverso)
h=open(p+'homev2.js',encoding='utf-8').read()
h=h.replace("sub: 'Il grafo dei rami', go: ['sez', 'multiverso']","sub: 'La mappa dei rami', go: ['sez', 'multiverso']")
open(p+'homev2.js','w',encoding='utf-8').write(h)
# CSS
css=open(p+'atlas2.css',encoding='utf-8').read(); m='/* ==== MAP3B ==== */'
if m in css: css=css[:css.index(m)]
css=css.rstrip()+'\n'+m+'\n'+open(p+'map3b.css',encoding='utf-8').read()
open(p+'atlas2.css','w',encoding='utf-8').write(css)
print('ok map3b')
