#!/usr/bin/env python3
"""Blocco 4.0C: sincronizzazione cloud - stato reale, nessun overwrite automatico, validazione codice (idempotente). Dopo patch_b32.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
js=open(T+'sync40c.js',encoding='utf-8').read().rstrip('\n')+'\n'
if '/* SYNC40C-BEGIN' in s:
    s=re.sub(r'    /\* SYNC40C-BEGIN.*?/\* SYNC40C-END \*/\n',lambda m:js,s,flags=re.S)
else:
    a=s.find("    var syncRef = null;\n    var syncPollTimer = null;\n    var syncLastAppliedStr = null;")
    b=s.find("  } catch (errSync) {")
    assert a>0 and b>a and s.count("  } catch (errSync) {")==1,'ancore sync non trovate'
    s=s[:a]+js+s[b:]
css="""/* SYNC40C-CSS */
.sync-conflict { margin: .5rem 0 0; padding: .6rem .7rem; border: 1px solid var(--marvel-red); border-radius: 6px; font-size: .8rem; line-height: 1.4; }
.sync-conflict[hidden] { display: none; }
.sync-conflict-msg { margin: 0 0 .5rem; }
.sync-conflict-diff { margin: 0 0 .5rem; padding: .4rem .5rem; white-space: pre-wrap; word-break: break-word; font-family: 'IBM Plex Mono', monospace; font-size: .72rem; border-radius: 4px; background: rgba(127,127,127,.12); }
.sync-conflict-diff[hidden] { display: none; }
.sync-conflict-actions { display: flex; flex-wrap: wrap; gap: .4rem; }
.sync-conflict-actions button[hidden] { display: none; }
.sync-conflict-actions button:disabled { opacity: .4; cursor: not-allowed; }
/* SYNC40C-CSS-END */"""
if '/* SYNC40C-CSS */' in s: s=re.sub(r'/\* SYNC40C-CSS \*/.*?/\* SYNC40C-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    assert s.count('</head>')==1; s=s.replace('</head>','<style id="sync40c-css">\n'+css+'\n</style>\n</head>')
open(P,'w',encoding='utf-8').write(s)

# ---- 4.0E: getTesseraId rilegge il valore realmente persistito (due schede in concorrenza non producono ID diversi) ----
s=open(P,encoding='utf-8').read()
old_id="      var code = 'VAR-' + Math.floor(100000 + Math.random() * 900000);\n      localStorage.setItem('marvel-ultimate-timeline-tessera-id', code);\n      return code;"
new_id="      var code = 'VAR-' + Math.floor(100000 + Math.random() * 900000);\n      localStorage.setItem('marvel-ultimate-timeline-tessera-id', code);\n      return localStorage.getItem('marvel-ultimate-timeline-tessera-id') || code; /* 4.0E: vale quanto persistito */"
if new_id not in s:
    assert s.count(old_id)==1,'getTesseraId ancora non unica'
    s=s.replace(old_id,new_id,1)
open(P,'w',encoding='utf-8').write(s)
print('patch_sync ok')
