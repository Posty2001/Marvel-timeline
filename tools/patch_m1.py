#!/usr/bin/env python3
"""Blocco M1 (idempotente). Dopo patch_sync.py: ordine personalizzato nel profilo, leggibilita' Home, bersaglio ricerca Home."""
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,tag):
    global s
    if new in s: return
    assert s.count(old)==1,'ancora non trovata: '+tag
    s=s.replace(old,new)
s=s.replace('rewards: true, tesseraLook: true, customOrder: true };','rewards: true, tesseraLook: true };')  # pulizia di una prima versione del patch
# 1) profilo: nuovo campo opzionale (retrocompatibile: i vecchi backup non lo contengono)
rep("      tesseraLook: 'marvel-ultimate-timeline-tessera-look'\n    };","      tesseraLook: 'marvel-ultimate-timeline-tessera-look',\n      customOrder: 'marvelGuideCustomTimelineOrder' /* M1 */\n    };",'keys')
rep("          if (data[campo] === undefined) {\n            if (PROFILE_CAMPI_RECENTI[campo])",
"          if (data[campo] === undefined) {\n            if (campo === 'customOrder') { /* M1: profili precedenti non contengono l'ordine personalizzato: quello locale resta com'e' */\n              try { scritture[chiaveStorage] = localStorage.getItem(chiaveStorage); } catch(eCo) { scritture[chiaveStorage] = null; }\n              return;\n            }\n            if (PROFILE_CAMPI_RECENTI[campo])",'assente')
ANC="        tesseraId: function(v) { return stringaDa(v, 'tesseraId', null, /^VAR-\\d{6}$/, 12); },\n"
CO="""        customOrder: function(v) { /* M1: elenco dei numeri scheda nell'ordine scelto; {} / [] = nessun ordine personalizzato */
          if (oggettoVuoto(v) || (Array.isArray(v) && v.length === 0)) return null;
          if (!Array.isArray(v) || v.length > 500) throw erroreProfilo('“customOrder” deve essere un elenco di numeri scheda.');
          var vistiO = {};
          v.forEach(function(n) {
            if (typeof n !== 'number' || n % 1 !== 0 || n < 1 || n > 9999 || vistiO[n]) throw erroreProfilo('“customOrder” contiene un numero scheda non valido o ripetuto.');
            vistiO[n] = true;
          });
          return JSON.stringify(v);
        },
"""
rep(ANC,ANC+CO,'norm')
rep("tesseraLook: 'Aspetto tessera', missioneXpBank","tesseraLook: 'Aspetto tessera', customOrder: 'Ordine personalizzato', missioneXpBank",'nomi')
# 2) CSS Home
css="""/* M1-CSS */
.hm-kick, .hm-ch-n, .hm-stats span { font-size: 0.6875rem; }
@media (max-width: 340px) { .hm-stats span { font-size: 0.6875rem; letter-spacing: 0.04em; } }
html .hm-console .a2-sbox input:not(#rs) { min-height: 44px; }
/* M1-CSS-END */"""
import re
if '/* M1-CSS */' in s: s=re.sub(r'/\* M1-CSS \*/.*?/\* M1-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    assert s.count('</head>')==1; s=s.replace('</head>','<style id="m1-css">\n'+css+'\n</style>\n</head>')
s=s.replace('20261022-2100-blocco4-0e','20261022-2230-m1')
open(P,'w',encoding='utf-8').write(s)
