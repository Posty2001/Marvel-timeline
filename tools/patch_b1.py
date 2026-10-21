#!/usr/bin/env python3
"""Blocco 1 (idempotente). Eseguire dopo patch_pre5.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
def must(c,m):
    if not c: raise SystemExit('ERRORE: '+m)
css=open(T+'b1.css',encoding='utf-8').read().strip()
if '/* B1-CSS-BEGIN' in s: s=re.sub(r'/\* B1-CSS-BEGIN.*?/\* B1-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    must(s.count('</head>')==1,'head'); s=s.replace('</head>','<style id="b1-css">\n'+css+'\n</style>\n</head>')
# 1) tab: Missioni -> Centrale TVA (id e data-tab invariati)
o='<span class="app-tab-lbl">MISSIONI</span>'
if o in s: s=s.replace(o,'<span class="app-tab-lbl">CENTRALE<br>TVA</span>')
a='<button type="button" class="app-tab" id="appTabMissioni" data-tab="missioni">'
if a in s: s=s.replace(a,'<button type="button" class="app-tab" id="appTabMissioni" data-tab="missioni" aria-label="Centrale TVA">')
# 2) voto: widget subito sotto il titolo (primo elemento del pannello)
f=T+'fix_rating_block.js'
# (il posizionamento e' nel blocco JS gia' iniettato)
old="""        var first = null;
        for (var q = panel.firstElementChild; q; q = q.nextElementSibling) { if (q.classList.contains('sub-group')) { first = q; break; } }
        panel.insertBefore(widget, first);"""
if old in s: s=s.replace(old,"        panel.insertBefore(widget, panel.firstChild);")
# 3) Continua dalla Home senza ultimo titolo: va al percorso, non alla dashboard
d="""              var dash = document.getElementById('dashboard');
              if (dash && dash.scrollIntoView) dash.scrollIntoView({ behavior: 'smooth', block: 'start' });
            });"""
if d in s: s=s.replace(d,"""              var cvb = document.getElementById('cvContinueBtn');
              if (cvb) cvb.click();
            });""")

# 5) Grafo delle Relazioni: etichette piu' grandi/compatte, vista ritagliata sul contenuto (stessa logica, stessi dati)
def rep(old,new,tag):
    global s
    if old in s: s=s.replace(old,new)
    else: must(new in s,'grafo: '+tag)
rep("SP = 66, Y0 = 56, H = Math.max(360, Y0 * 2 + (rows - 1) * SP), cy = H / 2, cx = 500, DX = 215;","SP = 76, Y0 = 56, H = Math.max(300, Y0 * 2 + (rows - 1) * SP), cy = H / 2, cx = 500, DX = 190;",'layout')
rep("nm = rgWrap(c.name, 24), lab = c.labels.join(' · ');\n        if (lab.length > 30) lab = lab.slice(0, 29) + '\u2026';","nm = rgWrap(c.name, 17), lab = c.labels.join(' \u00b7 ');\n        if (lab.length > 24) lab = lab.slice(0, 23) + '\u2026';",'wrap')
rep("var y0 = p.y - (nm.length === 2 ? 10 : 2), t =","var y0 = p.y - (nm.length === 2 ? 12 : 2), t =",'y0')
rep('class="mg-node-label rg-nm" style="font-size:16px;">','class="mg-node-label rg-nm" style="font-size:20px;">','fs nm')
rep("(y0 + (nm.length === 2 ? 38 : 22))","(y0 + (nm.length === 2 ? 44 : 27))",'sub y')
rep("class=\"rg-rl\" style=\"font-size:12.5px;","class=\"rg-rl\" style=\"font-size:15px;",'fs sub')
rep("rgSvg.setAttribute('data-vb', '0 0 1000 ' + H); rgSvg.setAttribute('viewBox', '0 0 1000 ' + H);","rgSvg.setAttribute('data-vb', '80 0 840 ' + H); rgSvg.setAttribute('viewBox', '80 0 840 ' + H);",'vb')
rep("var B = computeBase(vbs, sparse, o.aspect);","var B = computeBase(vbs, sparse, o.aspect || (svg.closest('.relationship-graph-overlay') ? vbs[2] / vbs[3] : 0));",'base1')
rep("var nb = computeBase(nv, sparse, o.aspect);","var nb = computeBase(nv, sparse, o.aspect || (svg.closest('.relationship-graph-overlay') ? nv[2] / nv[3] : 0));",'base2')

# 4) JS
js=open(T+'b1.js',encoding='utf-8').read().strip(); sc='<script id="b1-js">\n'+js+'\n</script>\n'
if '/* B1-JS-BEGIN' in s: s=re.sub(r'<script id="b1-js">.*?</script>\n',lambda m:sc,s,flags=re.S)
else:
    must(s.count('</body>')==1,'body'); s=s.replace('</body>',sc+'</body>')
open(P,'w',encoding='utf-8').write(s); print('b1 ok')
