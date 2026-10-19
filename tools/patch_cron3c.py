#!/usr/bin/env python3
"""Fase 3C — integra le Cronologie del Multiverso in atlas2.js/atlas2.css (idempotente). Da eseguire dopo patch_dossier.py e patch_map3b.py, prima di inject_net.py."""
p='/home/claude/work/tools/'
js=open(p+'atlas2.js',encoding='utf-8').read()
new=open(p+'cron3c.js',encoding='utf-8').read().rstrip('\n')
B='    /* ==== CRON3C:BEGIN'; E_='    /* ==== CRON3C:END ==== */'
anchor='    /* ---------- apertura / stato ---------- */'
if B in js:
    a=js.index(B); b=js.index(E_)+len(E_); js=js[:a]+new.lstrip('\n')+js[b:]
else:
    i=js.index(anchor); js=js[:i]+new+'\n\n'+js[i:]
def rep(old,newv,cnt=1):
    global js
    if newv in js: return
    assert js.count(old)==cnt,(old,js.count(old)); js=js.replace(old,newv)
rep("mappa: renderMappa, catalogo: renderCatalogo,","mappa: renderMappa, cron: renderCron, catalogo: renderCatalogo,")
rep("      if (sc === 'mappa') return 'Mappa';","      if (sc === 'mappa') return 'Mappa';\n      if (sc === 'cron') return 'Cronologia';")
rep("mp: mpSnap(), y: body.scrollTop };","mp: mpSnap(), cr: crSnap(), y: body.scrollTop };")
rep("        if (s.mp) ST.mp = JSON.parse(JSON.stringify(s.mp));","        if (s.mp) ST.mp = JSON.parse(JSON.stringify(s.mp));\n        if (s.cr) ST.cr = JSON.parse(JSON.stringify(s.cr));")
hub="      var s1 = el('section', 'a2-cat'); s1.appendChild(el('h3', '', 'Timeline'));"
newhub="""      var s0 = el('section', 'a2-cat'); s0.appendChild(el('h3', '', 'Esplora il tempo'));
      [['Cronologia di un universo', 'Il percorso dei titoli di un universo, con date certe, approssimative e mancanti distinte.', 'uni'], ['Cronologie parallele', 'Confronta due universi senza inventare corrispondenze fra epoche.', 'par'],
       ['Esplora nel tempo', 'Cerca un titolo e filtra per universo, periodo, saga e tipo.', 'exp']].forEach(function (p) { var r0 = row({ n: p[0], d: p[1], art: 'cronologie' }, function () { crOpen(p[2]); }); r0.setAttribute('data-cr', p[2]); s0.appendChild(r0); });
      body.appendChild(s0);
"""
rep(hub,newhub+hub)
open(p+'atlas2.js','w',encoding='utf-8').write(js)
css=open(p+'atlas2.css',encoding='utf-8').read(); m='/* ==== CRON3C ==== */'
if m in css: css=css[:css.index(m)]
css=css.rstrip()+'\n'+m+'\n'+open(p+'cron3c.css',encoding='utf-8').read()
open(p+'atlas2.css','w',encoding='utf-8').write(css)
print('ok cron3c')
