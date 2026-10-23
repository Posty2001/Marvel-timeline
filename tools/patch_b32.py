#!/usr/bin/env python3
"""Blocco 3.2: Tessera TVA - identita', personalizzazione, condivisione (idempotente). Eseguire dopo patch_b31.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
def must(c,m):
    if not c: raise SystemExit('ERRORE: '+m)
def rep(old,new,tag):
    global s
    if '/* SYNC40C-BEGIN' in s and ('profile[ok] !== undefined' in old or '_val' in old): return  # sync sostituito in 4.0C
    if new in s: return
    if tag=='keys' and "tesseraLook: 'marvel-ultimate-timeline-tessera-look'" in s: return  # M1 ha aggiunto customOrder dopo tesseraLook
    must(s.count(old)==1,tag+' (ancora non unica/assente: %d)'%s.count(old)); s=s.replace(old,new,1)
css=open(T+'tc.css',encoding='utf-8').read().strip()
if '/* TC-CSS-BEGIN' in s: s=re.sub(r'/\* TC-CSS-BEGIN.*?/\* TC-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    must(s.count('</head>')==1,'head'); s=s.replace('</head>','<style id="tc-css">\n'+css+'\n</style>\n</head>')
# profilo: nuova chiave 'tesseraLook' (avatar scelto + 3 distintivi in evidenza). La foto NON e' nel profilo (resta locale).
rep("      rewards: 'marvel-ultimate-timeline-rewards'\n    };","      rewards: 'marvel-ultimate-timeline-rewards',\n      tesseraLook: 'marvel-ultimate-timeline-tessera-look'\n    };",'keys')
rep("badgesEarned: true, rewards: true };","badgesEarned: true, rewards: true, tesseraLook: true };",'recenti')
norm="""        tesseraLook: function(v) {
          if (oggettoVuoto(v)) return null;
          if (!profiloOggettoSemplice(v) || v.v !== 1) throw erroreProfilo('“tesseraLook” non e’ valido.');
          var out = { v: 1 };
          if (v.a !== undefined) { if (typeof v.a !== 'string' || !/^[a-z][a-z-]{1,30}$/.test(v.a)) throw erroreProfilo('“tesseraLook.a” non e’ valido.'); out.a = v.a; }
          if (v.b !== undefined) {
            if (!Array.isArray(v.b) || v.b.length > 3) throw erroreProfilo('“tesseraLook.b” non e’ valido.');
            v.b.forEach(function(x) { if (typeof x !== 'string' || !/^[a-z][a-z-]{2,30}$/.test(x)) throw erroreProfilo('“tesseraLook.b” contiene una voce non valida.'); });
            out.b = v.b.slice();
          }
          if (v.ts !== undefined) { if (typeof v.ts !== 'number' || !isFinite(v.ts) || v.ts <= 0) throw erroreProfilo('“tesseraLook.ts” non e’ valido.'); out.ts = v.ts; }
          return JSON.stringify(out);
        },
"""
rep("        tesseraId: function(v) { return stringaDa(v, 'tesseraId'", norm+"        tesseraId: function(v) { return stringaDa(v, 'tesseraId'",'norm')
rep("continue; }\n          localStorage.setItem(PROFILE_OBJ_KEYS[ok], JSON.stringify(_val));",
    "continue; }\n          if (ok === 'tesseraLook' && window.tvaTessera) { try { localStorage.setItem(PROFILE_OBJ_KEYS[ok], window.tvaTessera.lookMerge(localStorage.getItem(PROFILE_OBJ_KEYS[ok]), _val)); } catch(eLkM) {} continue; }\n          localStorage.setItem(PROFILE_OBJ_KEYS[ok], JSON.stringify(_val));",'sync')
# azzeramento totale: rimuove anche la foto locale (non fa parte del profilo)
rep("        for (var skR in PROFILE_STR_KEYS) { localStorage.removeItem(PROFILE_STR_KEYS[skR]); }\n","        for (var skR in PROFILE_STR_KEYS) { localStorage.removeItem(PROFILE_STR_KEYS[skR]); }\n        localStorage.removeItem('marvel-ultimate-timeline-tessera-photo');   // B3.2: foto personale (solo locale)\n",'wipe')
art=open(T+'tc_art.js',encoding='utf-8').read().strip(); js=open(T+'tc.js',encoding='utf-8').read().strip()
sc='<script id="tc-art-js">\n'+art+'\n</script>\n<script id="tc-js">\n'+js+'\n</script>\n'
if '/* TCART-JS-BEGIN' in s: s=re.sub(r'<script id="tc-art-js">.*?</script>\n<script id="tc-js">.*?</script>\n',lambda m:sc,s,flags=re.S)
else:
    must(s.count('</body>')==1,'body'); s=s.replace('</body>',sc+'</body>')
open(P,'w',encoding='utf-8').write(s); print('b32 ok')
