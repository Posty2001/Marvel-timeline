import re,sys
p='/home/claude/work/tools/'
js=open(p+'atlas2.js',encoding='utf-8').read()
new=open(p+'homev2.js',encoding='utf-8').read()
a=js.index('    /* ---------- schermata: Home TVA Archives')
b=js.index('    /* ---------- schermata: catalogo ---------- */')
js=js[:a]+new+js[b:]
open(p+'atlas2.js','w',encoding='utf-8').write(js)
css=open(p+'atlas2.css',encoding='utf-8').read()
m='/* ==== HOME2 ==== */'
if m in css: css=css[:css.index(m)]
css=css.rstrip()+'\n'+m+'\n'+open(p+'home2.css',encoding='utf-8').read()
open(p+'atlas2.css','w',encoding='utf-8').write(css)
print('ok')
