import sys; sys.path.insert(0,'/home/claude/work/tools/edits')
from jb import edit_json,rep
p='/home/claude/work/index.html'; s=open(p,encoding='utf-8').read()
# 1) helper (sola lettura su prerequisitiDuri) prima di initDependencyMaps
s=rep(s,"  function initDependencyMaps() {","""  // Etichette delle mappe: un titolo marcato consigliato/opzionale ma gia' bloccante per catena
  // (prerequisitiDuri transitivo) viene mostrato tra gli ESSENZIALI con l'indicazione dell'antecedente.
  // Solo presentazione: DEPENDENCY_MAP_JS e prerequisitiDuri non cambiano.
  function chiusuraAntecedentiDuri(id, out) {
    prerequisitiDuri(id).forEach(function(x) { if (!out[x]) { out[x] = true; chiusuraAntecedentiDuri(x, out); } });
    return out;
  }
  function antecedenteViaCatena(target, n) {
    var pre = prerequisitiDuri(target);
    if (pre.indexOf(n) !== -1) return null;
    for (var i = 0; i < pre.length; i++) { if (chiusuraAntecedentiDuri(pre[i], {})[n]) return pre[i]; }
    return null;
  }
  function titoloPerDipendenza(n) {
    for (var i = 0; i < WATCH_ORDER_JS.length; i++) { if (WATCH_ORDER_JS[i].id === n) return WATCH_ORDER_JS[i].title; }
    return 'Scheda ' + n;
  }
  function initDependencyMaps() {""")
s=rep(s,"""        var catHtml = '';
        CAT_DEFS.forEach(function(def) {
          var key = def[0], label = def[1], icon = def[2];
          var nums = cats[key];""","""        var catHtml = '';
        var viaCatena = {};
        var catsMostrate = { ess: cats.ess.slice(), cons: [], opz: [] };
        ['cons', 'opz'].forEach(function(k) {
          cats[k].forEach(function(n) {
            var via = antecedenteViaCatena(targetNum, n);
            if (via) { catsMostrate.ess.push(n); viaCatena[n] = via; } else { catsMostrate[k].push(n); }
          });
        });
        CAT_DEFS.forEach(function(def) {
          var key = def[0], label = def[1], icon = def[2];
          var nums = catsMostrate[key];""")
s=rep(s,"""&#11036;</span> ' + titolo + '</button>';""","""&#11036;</span> ' + titolo + (viaCatena[n] ? ' <span class="dep-chip-via">(obbligatorio via ' + titoloPerDipendenza(viaCatena[n]) + ')</span>' : '') + '</button>';""")
s=rep(s,".dep-chip-check { font-size: 0.75rem; }",".dep-chip-check { font-size: 0.75rem; }\n.dep-chip-via { font-size: 0.75rem; opacity: 0.8; }")
# 2) serie MCU: 41 film + 53 serie/speciali = 94 titoli
def mvf(o):
    u=o['universi']['uni-earth-199999-mcu']; assert (u['titoli'],u['film'],u['serie'])==(94,41,52); u['serie']=53
s=edit_json(s,'mvMapData',mvf)
open(p,'w',encoding='utf-8').write(s); print('intC ok')
