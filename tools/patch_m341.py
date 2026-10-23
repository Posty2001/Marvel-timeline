#!/usr/bin/env python3
"""Patch M3.4.1 (idempotente, dopo patch_m34): «Prossimo titolo» della Home rispetta la Timeline attiva (standard / personalizzata)."""
import re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,marker):
    global s
    if marker in s: return
    assert s.count(old)==1,(old[:70],s.count(old)); s=s.replace(old,new)

# 1) logica: Timeline personalizzata = ordine salvato (marvelGuideCustomTimelineOrder) quando la modalita' attiva salvata e' «custom»
FN='''  /* M341: Timeline attiva. L'app salvava solo l'ordine personalizzato (marvelGuideCustomTimelineOrder); la modalita' scelta non era persistita:
     ora «marvelGuideActiveTimelineMode» = 'custom' | 'standard' (solo UI locale: non tocca progressi, voti, XP, ricompense, profilo/sync). */
  var M341_MODE_KEY = 'marvelGuideActiveTimelineMode', M341_ORDER_KEY = 'marvelGuideCustomTimelineOrder';
  function m341OrdinePersonalizzato() {
    try {
      if (localStorage.getItem(M341_MODE_KEY) !== 'custom') return null;
      var o = JSON.parse(localStorage.getItem(M341_ORDER_KEY) || 'null');
      if (!Array.isArray(o) || !o.length) return null;   // sequenza vuota/assente: si torna al comportamento standard
      return o;
    } catch (eM341o) { return null; }
  }
  function trovaProssimoHome() {
    var ordine = m341OrdinePersonalizzato();
    if (!ordine) return trovaProssimoPerPriorita();   // standard: comportamento invariato
    var state = loadState(), byId = {}, visti = {}, seq = [];
    WATCH_ORDER_JS.forEach(function (it) { byId[it.id] = it; });
    ordine.forEach(function (n) {   // numeri scheda nell'ordine salvato; mancanti/duplicati ignorati
      var id = ('000' + parseInt(n, 10)).slice(-3);
      if (byId[id] && !visti[id]) { visti[id] = true; seq.push(byId[id]); }
    });
    WATCH_ORDER_JS.forEach(function (it) { if (!visti[it.id]) seq.push(it); });   // titoli non presenti nell'ordine salvato: in coda, come nella vista Personalizzato
    for (var i = 0; i < seq.length; i++) {
      var it = seq[i];
      if (state[it.id] || !titoloDisponibile(it.id)) continue;
      var ris = esploraAntecedenti(it.id, state, {}, { bloccato: false, primo: null });   // stessi vincoli (prerequisiti, uscite) della logica standard
      if (ris.bloccato) continue;
      if (!ris.primo) return it;
      var pre = byId[ris.primo]; if (pre) return pre;
    }
    return null;   // percorso completato (o nulla di disponibile)
  }
'''
rep("  function trovaProssimoPerPriorita() {", FN+"  function trovaProssimoPerPriorita() {", 'function trovaProssimoHome')
rep("        var next = trovaProssimoPerPriorita();\n        window.marvelHomeNext = next || null;   /* M34 */",
    "        var next = trovaProssimoHome();   /* M341 */\n        window.marvelHomeNext = next || null;   /* M34 */", 'trovaProssimoHome();   /* M341 */')

# 2) persistenza modalita' + aggiornamento immediato della Home
rep("      try { localStorage.setItem(AT_CUSTOM_KEY, JSON.stringify(order)); } catch(e) {}",
    "      try { localStorage.setItem(AT_CUSTOM_KEY, JSON.stringify(order)); } catch(e) {}\n      try { if (window.marvelUpdateHomeHub) window.marvelUpdateHomeHub(); } catch(eM341a) {}   /* M341 */",
    'eM341a')
rep("          btn.classList.add('at-mode-active');\n          atRender(btn.getAttribute('data-mode'));",
    "          btn.classList.add('at-mode-active');\n          try { localStorage.setItem('marvelGuideActiveTimelineMode', btn.getAttribute('data-mode') === 'custom' ? 'custom' : 'standard'); if (window.marvelUpdateHomeHub) window.marvelUpdateHomeHub(); } catch(eM341b) {}   /* M341 */\n          atRender(btn.getAttribute('data-mode'));",
    'eM341b')
rep("          atRendered = true;\n          atRender('recommended');",
    "          atRendered = true;\n          var m341c = false; try { m341c = localStorage.getItem('marvelGuideActiveTimelineMode') === 'custom'; } catch(eM341c) {}   /* M341: riapre sulla modalita' salvata */\n          if (m341c) { modeBtns.forEach(function(b) { b.classList.toggle('at-mode-active', b.getAttribute('data-mode') === 'custom'); }); atRender('custom'); }\n          else atRender('recommended');",
    'eM341c')
# modeBtns e' dichiarata dentro if (atModesEl): renderla visibile al listener sotto
rep("    var atRendered = false;\n    if (atModesEl) {\n      var modeBtns = Array.prototype.slice.call(atModesEl.querySelectorAll('.at-mode-btn'));",
    "    var atRendered = false;\n    var modeBtns = atModesEl ? Array.prototype.slice.call(atModesEl.querySelectorAll('.at-mode-btn')) : [];\n    if (atModesEl) {",
    'var modeBtns = atModesEl ?')

# 3) aggiornamento da altra scheda/finestra
JS='''<script>/* M341 */(function(){try{window.addEventListener('storage',function(e){if(e.key==='marvelGuideActiveTimelineMode'||e.key==='marvelGuideCustomTimelineOrder'||e.key==='marvel-ultimate-timeline-watched'||e.key===null){if(window.marvelUpdateHomeHub)window.marvelUpdateHomeHub();}});}catch(e){}})();</script>'''
s=re.sub(r'<script>/\* M341 \*/.*?</script>\n?','',s,flags=re.S)
k=s.rindex('</body>'); s=s[:k]+JS+'\n'+s[k:]
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+'20261023-1700-m341',s)
open(P,'w',encoding='utf-8').write(s)
