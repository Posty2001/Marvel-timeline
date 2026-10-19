#!/usr/bin/env python3
"""Reiniezione idempotente dei blocchi TVA NET + Atlante 2.0 (CSS + 2 <script>) in index.html a partire da tools/*.css|js."""
import sys,re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
T='/home/claude/work/tools/'
net_css=open(T+'net.css',encoding='utf-8').read().rstrip()
a2_css=open(T+'atlas2.css',encoding='utf-8').read().rstrip()
net_js=open(T+'net_module.js',encoding='utf-8').read().rstrip()
a2_js=open(T+'atlas2.js',encoding='utf-8').read().rstrip()
# CSS
i=s.index('/* ---- TVA NET: collegamenti'); j=s.index('\n.mv-map-old-link {',i)
s=s[:i]+net_css+'\n'+a2_css+'\n'+s[j:]
# JS (due blocchi <script> consecutivi)
def swap(s,marker,js):
    ms=marker if isinstance(marker,(list,tuple)) else [marker]
    i=-1
    for m in ms:
        i=s.find('<script>\n'+m)
        if i>=0: break
    assert i>=0,ms
    j=s.index('</script>',i)
    return s[:i]+'<script>\n'+js+'\n'+s[j:]
s=swap(s,'/* ===== TVA NET',net_js)
s=swap(s,['/* ===== TVA ARCHIVES','/* ===== ATLANTE MULTIVERSALE 2.0'],a2_js)
um_js=open(T+'universe_model.js',encoding='utf-8').read().rstrip()
if '<script>\n/* ===== TVA UNIVERSE MODEL' in s:
    s=swap(s,'/* ===== TVA UNIVERSE MODEL',um_js)
else:
    k=s.index('<script>\n/* ===== TVA NET'); k=s.index('</script>',k)+len('</script>')
    s=s[:k]+'\n<script>\n'+um_js+'\n</script>'+s[k:]
arc_js=open(T+'archivi.js',encoding='utf-8').read().rstrip()
if '<script>\n/* ===== TVA ARCHIVES — ARCHIVI' in s:
    s=swap(s,'/* ===== TVA ARCHIVES — ARCHIVI',arc_js)
else:
    k=s.index('<script>\n/* ===== TVA ARCHIVES'); k=s.index('</script>',k)+len('</script>')
    s=s[:k]+'\n<script>\n'+arc_js+'\n</script>'+s[k:]
open(P,'w',encoding='utf-8').write(s)
print('iniettato; byte',len(s.encode('utf-8')))
