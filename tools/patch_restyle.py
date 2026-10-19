#!/usr/bin/env python3
"""Restyling grafico coordinato. Idempotente: rimpiazza i blocchi RS-* se già presenti.
Tocca solo presentazione: CSS aggiunto in coda al <style>, script emoji->icone/Home, tema scuro predefinito (chiave v2)."""
import re, json
P = '/home/claude/work/index.html'; T = '/home/claude/work/tools/'
s = open(P, encoding='utf-8').read()
D = 'html.marvel-dark-mode:not(#rs)'
css = open(T + 'restyle_icons.css', encoding='utf-8').read().rstrip() + '\n' + open(T + 'restyle.css', encoding='utf-8').read().replace('@D@', D).rstrip() + '\n'
css_block = '/* RS-ALL-BEGIN */\n' + css + '/* RS-ALL-END */\n'
if '/* RS-ALL-BEGIN */' in s:
    s = re.sub(r'/\* RS-ALL-BEGIN \*/.*?/\* RS-ALL-END \*/\n', lambda m: css_block, s, flags=re.S)
else:
    i = s.index('</style>'); s = s[:i] + css_block + s[i:]

# --- JS ---
m = json.load(open(T + 'restyle_map.json')); js = open(T + 'restyle.js', encoding='utf-8').read().replace('/*RS_MAP*/{}/*RS_MAP_END*/', json.dumps(m))
js_block = '<script id="rs-skin">\n' + js + '</script>\n'
if '<script id="rs-skin">' in s:
    s = re.sub(r'<script id="rs-skin">.*?</script>\n', lambda mm: js_block, s, flags=re.S)
else:
    i = s.rindex('</body>'); s = s[:i] + js_block + s[i:]

# --- tema scuro predefinito (chiave v2; nessuna chiave => scuro; il tema chiaro resta raggiungibile dall'interruttore) ---
early = ('<script id="rs-early">try{var __v=localStorage.getItem("marvel-skin-v2-dark");if(__v!=="0")document.documentElement.classList.add("marvel-dark-mode");}catch(e){document.documentElement.classList.add("marvel-dark-mode");}</script>\n')
if 'id="rs-early"' not in s:
    i = s.index('<meta name="tva-build"'); j = s.index('\n', i) + 1; s = s[:j] + early + s[j:]
old = "if (savedDark === '1' && darkModeToggleEl) darkModeToggleEl.checked = true;"
new = ("var savedV2 = null; try { savedV2 = localStorage.getItem('marvel-skin-v2-dark'); } catch(eV2) {}\n"
       "      if ((savedV2 === null ? true : savedV2 === '1') && darkModeToggleEl) darkModeToggleEl.checked = true;")
if old in s: s = s.replace(old, new)
old2 = "try { localStorage.setItem(DARK_MODE_KEY, darkModeToggleEl.checked ? '1' : '0'); } catch(eDarkSave) {}"
new2 = old2 + "\n        try { localStorage.setItem('marvel-skin-v2-dark', darkModeToggleEl.checked ? '1' : '0'); } catch(eDarkSave2) {}"
if old2 in s and 'eDarkSave2' not in s: s = s.replace(old2, new2)
s = s.replace('<meta name="theme-color" content="#c8272a">', '<meta name="theme-color" content="#101014">')
open(P, 'w', encoding='utf-8').write(s)
print('ok', len(s))
