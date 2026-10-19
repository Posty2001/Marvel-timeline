#!/usr/bin/env python3
"""Schede native dell'Atlante + guardia dell'archivio classico. Idempotente."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
css=open(T+'scheda.css',encoding='utf-8').read().rstrip()+'\n'
if '/* SC-CSS-BEGIN' in s: s=re.sub(r'/\* SC-CSS-BEGIN.*?/\* SC-CSS-END \*/\n',lambda m:css,s,flags=re.S)
else:
    i=s.index('/* SH-CSS-END */\n')+len('/* SH-CSS-END */\n') if '/* SH-CSS-END */\n' in s else s.index('/* RS-ALL-END */\n')+len('/* RS-ALL-END */\n'); s=s[:i]+css+s[i:]
js='<script id="tva-scheda">\n'+open(T+'scheda.js',encoding='utf-8').read()+'</script>\n'
if '<script id="tva-scheda">' in s: s=re.sub(r'<script id="tva-scheda">.*?</script>\n',lambda m:js,s,flags=re.S)
else:
    i=s.rindex('</body>'); s=s[:i]+js+s[i:]
g='<script id="tva-graphvp">\n'+open(T+'graphvp.js',encoding='utf-8').read()+'</script>\n'
if '<script id="tva-graphvp">' in s: s=re.sub(r'<script id="tva-graphvp">.*?</script>\n',lambda m:g,s,flags=re.S)
else:
    i=s.rindex('</body>'); s=s[:i]+g+s[i:]
ft='<script id="tva-famtree">\n'+open(T+'famtree.js',encoding='utf-8').read()+'</script>\n'
if '<script id="tva-famtree">' in s: s=re.sub(r'<script id="tva-famtree">.*?</script>\n',lambda m:ft,s,flags=re.S)
else:
    i=s.rindex('</body>'); s=s[:i]+ft+s[i:]
open(P,'w',encoding='utf-8').write(s); print('ok scheda')
