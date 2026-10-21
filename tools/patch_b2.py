#!/usr/bin/env python3
"""Blocco 2: Centrale TVA (idempotente). Eseguire dopo patch_b1.py."""
import re
P='/home/claude/work/index.html'; T='/home/claude/work/tools/'
s=open(P,encoding='utf-8').read()
def must(c,m):
    if not c: raise SystemExit('ERRORE: '+m)
def rep(old,new,tag):
    global s
    if new in s: return          # gia' applicato (new puo' contenere old)
    must(old in s,tag); s=s.replace(old,new,1)
css=open(T+'b2.css',encoding='utf-8').read().strip()
if '/* B2-CSS-BEGIN' in s: s=re.sub(r'/\* B2-CSS-BEGIN.*?/\* B2-CSS-END \*/',lambda m:css,s,flags=re.S)
else:
    must(s.count('</head>')==1,'head'); s=s.replace('</head>','<style id="b2-css">\n'+css+'\n</style>\n</head>')
# 1) dati reali delle missioni per i dossier (sola lettura: nessuna regola XP toccata)
anchor="      if (stFillEl) stFillEl.style.width = (progressoStagione * 10) + '%';\n"
aug=anchor+"""      try {   // B2: stato reale delle missioni esposto in sola lettura alla Centrale TVA
        var _wk = []; try { var _d = JSON.parse(localStorage.getItem(MISSIONE_SETTIMANA_KEY) || 'null'); if (_d && _d.settimana === week && Array.isArray(_d.titoli)) _wk = _d.titoli.slice(); } catch(eWk) {}
        var _mi = window.marvelMissioniInfo || (window.marvelMissioniInfo = {}), _bk = bankStagione.ricompensate || [];
        var _ts = []; try { _ts = JSON.parse(localStorage.getItem('marvel-ultimate-timeline-titoli-stagione') || '[]'); } catch(eTs) {}
        _mi.week = week; _mi.bank = bankStagione; _mi.catNomi = CAT_MISSIONE_NOMI; _mi.rtdXp = RTD_XP; _mi.titoliStagione = _ts;
        _mi.stato = {
          settimanale: { cur: Math.min(contatoreSett, obiettivoSett), tot: obiettivoSett, done: completa1, xp: 250, ids: _wk, rewarded: _bk.indexOf(week + '-settimanale') !== -1 },
          tematica: { cur: Math.min(vistiCatNuovi, 1), tot: 1, done: completa2, xp: 150, cat: catScelta, rewarded: _bk.indexOf(week + '-tematica-' + catScelta) !== -1 },
          saga: { cur: vistiSaga, tot: totaleSaga, done: completa3, xp: 300, nome: sagaScelta, rewarded: !!sagaScelta && _bk.indexOf(week + '-saga-' + sagaScelta) !== -1 },
          segreta: { cur: completa4 ? 1 : 0, tot: 1, done: completa4, xp: 500, id: completa4 ? idSegreto : null, rewarded: !!idSegreto && _bk.indexOf(week + '-segreta-' + idSegreto) !== -1 }
        };
        _mi.stagione = { idx: indiceStagioneAttuale, prog: progressoStagione, nome: datiStagione.nome, titolo: datiStagione.titolo, ic: datiStagione.ic };
        document.dispatchEvent(new CustomEvent('tva:missioni2'));
      } catch(eMisInfo2) {}
"""
# idempotenza: rimuove eventuali inserimenti precedenti, poi inserisce una sola volta
s=re.sub(r"      try \{   // B2: stato reale delle missioni.*?\} catch\(eMisInfo2\) \{\}\n",'',s,flags=re.S)
must(s.count(anchor)==1,'ancora updateMissioni')
s=s.replace(anchor,aug,1)
# pulizia di eventuali duplicati dovuti a una versione precedente di questa patch
_l="    try { if (window.tvaViewForTab) window.tvaViewForTab(nomeTab); } catch(eView) {}\n"
while _l+_l in s: s=s.replace(_l+_l,_l)
# 2) la scheda attiva determina la vista (Timeline / Centrale TVA)
rep("""  function aggiornaTabAttiva(nomeTab) {
    try {""","""  function aggiornaTabAttiva(nomeTab) {
    try { if (window.tvaViewForTab) window.tvaViewForTab(nomeTab); } catch(eView) {}
    try {""",'aggiornaTab')
# 3) cronologia interna: la Centrale ricorda sezione/sotto-sezione/posizione
rep("        a2: (W.tvaAtlas2 && $('atlas2Toggle') && $('atlas2Toggle').checked) ? W.tvaAtlas2.getState() : null };","        cen: (W.tvaCentrale && act && act.getAttribute('data-tab') === 'missioni') ? W.tvaCentrale.getState() : null,\n        a2: (W.tvaAtlas2 && $('atlas2Toggle') && $('atlas2Toggle').checked) ? W.tvaAtlas2.getState() : null };",'snapshot')
rep("        if (s.a2 && W.tvaAtlas2) W.tvaAtlas2.setState(s.a2);\n      } catch (e) { if (W.console) console.error('tvaNet restore', e); }","        if (s.a2 && W.tvaAtlas2) W.tvaAtlas2.setState(s.a2);\n        if (s.cen && W.tvaCentrale) W.tvaCentrale.setState(s.cen);\n      } catch (e) { if (W.console) console.error('tvaNet restore', e); }",'restore')
rep("      if (s.tab === 'home') return 'Home';\n","      if (s.tab === 'home') return 'Home';\n      if (s.tab === 'missioni') return 'Centrale TVA';\n",'ctxLabel')
# 4) JS
js=open(T+'b2.js',encoding='utf-8').read().strip(); sc='<script id="b2-js">\n'+js+'\n</script>\n'
if '/* B2-JS-BEGIN' in s: s=re.sub(r'<script id="b2-js">.*?</script>\n',lambda m:sc,s,flags=re.S)
else:
    must(s.count('</body>')==1,'body'); s=s.replace('</body>',sc+'</body>')
open(P,'w',encoding='utf-8').write(s); print('b2 ok')
