#!/usr/bin/env python3
"""Shell immersiva TVA per gli overlay classici. Idempotente."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
css=open(T+'shell.css',encoding='utf-8').read().rstrip()+'\n'
if '/* SH-CSS-BEGIN' in s: s=re.sub(r'/\* SH-CSS-BEGIN.*?/\* SH-CSS-END \*/\n',lambda m:css,s,flags=re.S)
else:
    i=s.index('/* RS-ALL-END */\n')+len('/* RS-ALL-END */\n'); s=s[:i]+css+s[i:]
js='<script id="tva-shell">\n'+open(T+'shell.js',encoding='utf-8').read()+'</script>\n'
if '<script id="tva-shell">' in s: s=re.sub(r'<script id="tva-shell">.*?</script>\n',lambda m:js,s,flags=re.S)
else:
    i=s.rindex('</body>'); s=s[:i]+js+s[i:]
open(P,'w',encoding='utf-8').write(s); print('ok')
