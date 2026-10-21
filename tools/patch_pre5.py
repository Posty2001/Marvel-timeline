#!/usr/bin/env python3
"""Sprint di rifinitura pre-Fase 5 (idempotente). Eseguire dopo patch_fix_ios.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
def must(c,m):
    if not c: raise SystemExit('ERRORE: '+m)
# CSS
css=open(T+'pre5.css',encoding='utf-8').read().strip()
if '/* PRE5-CSS-BEGIN' in s:
    s=re.sub(r'/\* PRE5-CSS-BEGIN.*?/\* PRE5-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    must(s.count('</head>')==1,'head'); s=s.replace('</head>','<style id="pre5-css">\n'+css+'\n</style>\n</head>')
# 1) ATLANTE: sempre schermata principale
old="if (terzetto[1] === 'atlas2Toggle' && window.tvaAtlas2) { try { window.tvaAtlas2.onOpen(); } catch(eA2o) {} }"
new="if (terzetto[1] === 'atlas2Toggle' && window.tvaAtlas2) { try { (window.tvaAtlas2.openHome || window.tvaAtlas2.onOpen)(); } catch(eA2o) {} }"
if old in s: s=s.replace(old,new)
else: must(new in s,'tab atlante')
# 2) copertina compatta
cov=re.search(r'<div class="cover" id="cover">.*?<div class="cover-seal">.*?</div>\n</div>\n',s,flags=re.S)
newcov='''<div class="cover" id="cover">
  <div class="cv-top"><div class="kicker">Time Variance Archive &middot; Fascicolo</div></div>
  <h1 class="maintitle">Marvel Ultimate Timeline</h1>
  <div class="subtitle">Ordine di visione definitivo &middot; film, serie e speciali</div>
  <div class="cover-grid">
    <div><b>138</b>titoli</div>
    <div><b>4</b>livelli</div>
    <div><b>3</b>canoni</div>
    <div><b>1943&ndash;2027</b>arco</div>
  </div>
  <button type="button" class="cv-continue" id="cvContinueBtn"><span class="cv-c-lbl">Continua il percorso</span><span class="cv-c-sub"></span></button>
  <p class="cover-note">Include titoli annunciati fino a Secret Wars (dic 2027).</p>
</div>
'''
if cov: s=s[:cov.start()]+newcov+s[cov.end():]
else: must('id="cvContinueBtn"' in s,'cover')
# Capitolo 0 tag
t='<div class="part-tab">CAPITOLO 0</div>'
if 'class="cap0-tag"' not in s:
    must(s.count(t)==1,'cap0'); s=s.replace(t,t+'<span class="cap0-tag">Lettura editoriale &middot; nessun titolo da guardare</span>')
# JS
js=open(T+'pre5.js',encoding='utf-8').read().strip()
sc='<script id="pre5-js">\n'+js+'\n</script>\n'
if '/* PRE5-JS-BEGIN' in s:
    s=re.sub(r'<script id="pre5-js">.*?</script>\n',lambda m:sc,s,flags=re.S)
else:
    must(s.count('</body>')==1,'body'); s=s.replace('</body>',sc+'</body>')
open(P,'w',encoding='utf-8').write(s); print('pre5 ok')
