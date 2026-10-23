#!/usr/bin/env python3
"""Blocco 3.1: ricompense cosmetiche (idempotente). Eseguire dopo patch_b2.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
def must(c,m):
    if not c: raise SystemExit('ERRORE: '+m)
def rep(old,new,tag,chk=None):
    global s
    if '/* SYNC40C-BEGIN' in s and ('profile[ok] !== undefined' in old or '_val' in old): return  # sync sostituito in 4.0C
    if new in s or (chk and chk in s): return
    must(s.count(old)==1,tag+' (ancora non unica/assente: %d)'%s.count(old)); s=s.replace(old,new,1)
css=open(T+'rw.css',encoding='utf-8').read().strip()
if '/* RW-CSS-BEGIN' in s: s=re.sub(r'/\* RW-CSS-BEGIN.*?/\* RW-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    must(s.count('</head>')==1,'head'); s=s.replace('</head>','<style id="rw-css">\n'+css+'\n</style>\n</head>')
# 1) XP e livello gia' calcolati dall'app, esposti in sola lettura (nessuna formula toccata)
rep("        if (xpSubEl) xpSubEl.textContent = xpResiduo + ' / ' + xpPerLivelloCorrente + ' al prossimo livello';\n",
    "        if (xpSubEl) xpSubEl.textContent = xpResiduo + ' / ' + xpPerLivelloCorrente + ' al prossimo livello';\n        window.marvelXpInfo = { xp: xpTotale, livello: livelloAttuale };   // B3.1: sola lettura per le ricompense cosmetiche\n",'xpinfo')
# 2) profilo (backup, ripristino, sincronizzazione): nuova chiave 'rewards'
rep("      badgesEarned: 'marvel-ultimate-timeline-badges-earned'\n    };","      badgesEarned: 'marvel-ultimate-timeline-badges-earned',\n      rewards: 'marvel-ultimate-timeline-rewards'\n    };",'keys',"rewards: 'marvel-ultimate-timeline-rewards'")
rep("var PROFILE_CAMPI_RECENTI = { roadToDoomsday: true, badgesEarned: true };","var PROFILE_CAMPI_RECENTI = { roadToDoomsday: true, badgesEarned: true, rewards: true };",'recenti',"badgesEarned: true, rewards: true")
norm="""        rewards: function(v) {
          if (oggettoVuoto(v)) return null; // "{}" = nessuno stato cosmetico: si rideriva dai dati importati
          if (!profiloOggettoSemplice(v) || v.v !== 1) throw erroreProfilo('“rewards” non e’ valido.');
          var okId = /^(titolo|cornice|tema|effetto)-[a-z0-9-]{2,40}$/, slotti = ['titolo', 'cornice', 'tema', 'effetto'], out = { v: 1, u: {}, e: {}, t: {} };
          if (v.u !== undefined) {
            if (!profiloOggettoSemplice(v.u) || Object.keys(v.u).length > 200) throw erroreProfilo('“rewards.u” non e’ valido.');
            Object.keys(v.u).forEach(function(k) { if (!okId.test(k) || typeof v.u[k] !== 'string' || !reIsoGiorno.test(v.u[k])) throw erroreProfilo('“rewards.u” contiene una voce non valida (' + profiloTronca(k) + ').'); out.u[k] = v.u[k]; });
          }
          [['e', 'e'], ['t', 't']].forEach(function(p) {
            if (v[p[0]] === undefined) return;
            if (!profiloOggettoSemplice(v[p[0]])) throw erroreProfilo('“rewards.' + p[0] + '” non e’ valido.');
            slotti.forEach(function(sl) {
              var x = v[p[0]][sl]; if (x === undefined) return;
              if (p[0] === 'e' && (x === null || (typeof x === 'string' && okId.test(x)))) out.e[sl] = x;
              else if (p[0] === 't' && typeof x === 'number' && isFinite(x) && x > 0) out.t[sl] = x;
              else throw erroreProfilo('“rewards.' + p[0] + '.' + sl + '” non e’ valido.');
            });
          });
          return JSON.stringify(out);
        },
"""
rep("        tesseraId: function(v) { return stringaDa(v, 'tesseraId'", norm+"        tesseraId: function(v) { return stringaDa(v, 'tesseraId'",'norm',"        rewards: function(v) {")
# 3) sincronizzazione: le preferenze cosmetiche piu' recenti non vengono sovrascritte da dati obsoleti
rep("        if (profile[ok] !== undefined) localStorage.setItem(PROFILE_OBJ_KEYS[ok], JSON.stringify(profile[ok]));",
    "        if (profile[ok] !== undefined) {\n          var _val = profile[ok];\n          if (ok === 'rewards' && window.tvaRewards) { try { localStorage.setItem(PROFILE_OBJ_KEYS[ok], window.tvaRewards.merge(localStorage.getItem(PROFILE_OBJ_KEYS[ok]), _val)); } catch(eRwM) {} continue; }\n          localStorage.setItem(PROFILE_OBJ_KEYS[ok], JSON.stringify(_val));\n        }",'sync',"ok === 'rewards' && window.tvaRewards")
# 4) Reset progresso: come per i distintivi, azzera lo storico di sblocco (le preferenze salvate restano, ma valgono solo se ancora sbloccate)
rep("      try { localStorage.removeItem(BADGE_STORICO_KEY); } catch(eBsReset) {}\n","      try { localStorage.removeItem(BADGE_STORICO_KEY); } catch(eBsReset) {}\n      try { if (window.tvaRewards) window.tvaRewards.resetUnlocks(); } catch(eRwReset) {}\n",'reset')
js=open(T+'rw.js',encoding='utf-8').read().strip(); sc='<script id="rw-js">\n'+js+'\n</script>\n'
if '/* RW-JS-BEGIN' in s: s=re.sub(r'<script id="rw-js">.*?</script>\n',lambda m:sc,s,flags=re.S)
else:
    must(s.count('</body>')==1,'body'); s=s.replace('</body>',sc+'</body>')
open(P,'w',encoding='utf-8').write(s); print('b31 ok')
