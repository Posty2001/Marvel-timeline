#!/usr/bin/env python3
"""Correzioni iPhone / navigazione / voto a mezze stelle (idempotente). Eseguire dopo patch_fase1.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read(); n0=len(s)
def must(cond,msg):
    if not cond: raise SystemExit('ERRORE: '+msg)
# --- CSS
css=open(T+'fix_ios.css',encoding='utf-8').read().strip()
if '/* FX-CSS-BEGIN' in s:
    s=re.sub(r'/\* FX-CSS-BEGIN.*?/\* FX-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    must(s.count('</head>')==1,'</head>'); s=s.replace('</head>','<style id="fx-ios">\n'+css+'\n</style>\n</head>')
# --- 1) onboarding: stato esplicito (l'intro viene smontata mentre l'onboarding e' attivo)
a="      onboardingEl.hidden = false;\n"
if "classList.add('tva-onb')" not in s:
    must(s.count(a)==1,'onboarding show'); s=s.replace(a,a+"      document.documentElement.classList.add('tva-onb');   // l'introduzione non resta montata sotto la registrazione\n")
    b="        onboardingEl.hidden = true;\n        if (journeyCb) journeyCb.checked = true;\n"
    must(s.count(b)==1,'onboarding hide'); s=s.replace(b,"        onboardingEl.hidden = true;\n        document.documentElement.classList.remove('tva-onb');\n        if (journeyCb) journeyCb.checked = true;\n")
    c="      if (window.console) console.error('Marvel guide - onboarding:', eOnboarding);\n"
    must(s.count(c)==1,'onboarding catch'); s=s.replace(c,c+"      document.documentElement.classList.remove('tva-onb');\n")
# --- 3) voto: blocco JS
blk=open(T+'fix_rating_block.js',encoding='utf-8').read()
i=s.find('  // ---- Sistema di voto'); j=s.find('  // ---- Note personali: salvate in localStorage')
must(i>0 and j>i,'blocco voto')
s=s[:i]+blk+s[j:]
# next-watch stars
o="          starsHtml = '<span class=\"next-watch-stars\">' + '&#9733;'.repeat(voto) + '&#9734;'.repeat(5 - voto) + '</span>';"
if o in s: s=s.replace(o,"          starsHtml = '<span class=\"next-watch-stars\">' + ratingMiniHtml(voto) + '</span>';")
# validazione import profilo: ammessi multipli di 0,5 tra 0,5 e 5
v="typeof v[k] !== 'number' || Math.floor(v[k]) !== v[k] || v[k] < 0 || v[k] > 5) throw erroreProfilo('“ratings” contiene un voto non valido per ' + k + ' (ammessi 1-5).');"
if v in s: s=s.replace(v,"typeof v[k] !== 'number' || Math.round(v[k] * 2) / 2 !== v[k] || v[k] < 0 || v[k] > 5) throw erroreProfilo('“ratings” contiene un voto non valido per ' + k + ' (ammessi multipli di 0,5 da 0,5 a 5).');")
# --- 2) Esplora il Multiverso: apre la Mappa 3B (Home hub + scheda guida), grafo classico resta secondario
h='<label for="multiverseGraphToggle" class="home-hub-btn"><span class="home-hub-btn-ic">&#128506;&#65039;</span> Esplora il Multiverso</label>'
if h in s: s=s.replace(h,'<button type="button" class="home-hub-btn" id="homeHubMapBtn"><span class="home-hub-btn-ic">&#128506;&#65039;</span> Esplora il Multiverso</button>')
g='        <label for="multiverseGraphToggle" class="mg-open-btn">&#128302; Apri il Grafico del Multiverso</label>'
if g in s: s=s.replace(g,'        <button type="button" class="mg-open-btn" id="guideMapBtn">&#128506;&#65039; Apri la Mappa del Multiverso</button>\n        <label for="multiverseGraphToggle" class="mg-open-btn" style="background:transparent;border:1px solid var(--marvel-red);box-shadow:none;margin-left:.4rem">Grafo classico</label>')
js='''<script id="tva-fixnav">
/* Punti d'ingresso al Multiverso: aprono la Mappa 3B (Atlante); il grafo classico resta raggiungibile come opzione secondaria. */
(function(){
  function apri(){
    try { var a=window.tvaAtlas2&&window.tvaAtlas2.ext&&window.tvaAtlas2.ext.api; if(a&&a.openMappa){ a.openMappa(); return; } } catch(e){ if(window.console) console.error('openMappa:',e); }
    var t=document.getElementById('multiverseGraphToggle'); if(t){ t.checked=true; t.dispatchEvent(new Event('change',{bubbles:true})); }   // ripiego: grafo classico
  }
  ['homeHubMapBtn','guideMapBtn'].forEach(function(id){ var b=document.getElementById(id); if(b) b.addEventListener('click',apri); });
})();
</script>
'''
if 'id="tva-fixnav"' not in s:
    must(s.count('</body>')>=1,'body'); k=s.rfind('</body>'); s=s[:k]+js+s[k:]
open(P,'w',encoding='utf-8').write(s); print('fix ok',len(s)-n0)
