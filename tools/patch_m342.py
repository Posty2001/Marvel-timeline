#!/usr/bin/env python3
"""Patch M3.4.2 (idempotente, dopo patch_m341): «Cosa guardo dopo» (Timeline) usa la stessa selezione della Home (trovaProssimoHome)."""
import re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,marker):
    global s
    if marker in s: return
    assert s.count(old)==1,(old[:70],s.count(old)); s=s.replace(old,new)
rep("  function updateNextWatch() {\n    try {\n      var next = trovaProssimoPerPriorita();",
    "  function updateNextWatch() {\n    try {\n      var next = trovaProssimoHome();   /* M342: stessa selezione della Home (standard/personalizzata) */",
    'M342: stessa selezione')
# la card Timeline si aggiorna insieme alla Home (cambio modalita'/ordine), senza duplicare l'algoritmo
rep("        try { document.dispatchEvent(new CustomEvent('tva:homenext')); } catch (eM34n) {}",
    "        try { document.dispatchEvent(new CustomEvent('tva:homenext')); } catch (eM34n) {}\n        try { updateNextWatch(); } catch (eM342) {}   /* M342 */",
    'eM342')
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+'20261023-1730-m342',s)
open(P,'w',encoding='utf-8').write(s)
