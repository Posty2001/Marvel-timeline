import re
p='/home/claude/work/tools/'
js=open(p+'atlas2.js',encoding='utf-8').read()
new=open(p+'dossier.js',encoding='utf-8').read()
a=js.index('    /* ---------- schermata: scheda universo')
b=js.index('    /* ---------- apertura / stato ---------- */')
js=js[:a]+new+'\n'+js[b:]
open(p+'atlas2.js','w',encoding='utf-8').write(js)
css=open(p+'atlas2.css',encoding='utf-8').read()
m='/* ==== DOSSIER3A ==== */'
if m in css: css=css[:css.index(m)]
css=css.rstrip()+'\n'+m+'\n'+open(p+'dossier.css','r',encoding='utf-8').read()
open(p+'atlas2.css','w',encoding='utf-8').write(css)
print('ok')
