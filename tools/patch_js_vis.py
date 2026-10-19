P='/home/claude/work/index.html'; s=open(P,encoding='utf-8').read()
def sub(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:60],s.count(old)); s=s.replace(old,new)
i=s.index('  var WATCH_ORDER_JS = '); j=s.index('\n',i)+1
helper='''  // ---- Numero VISIBILE (N°) <-> ID stabile della scheda. L'id (data-item) e' l'identita' dell'opera e
  // la chiave di TUTTI i salvataggi (visti, preferiti, voti, note, badge, gruppi, backup, sync): non cambia mai.
  // Il numero visibile e' la posizione nel percorso, scritta nello <span class="rec"> della scheda. Un percorso
  // editoriale puo' riordinare delle schede (es. Logan prima di Deadpool) senza toccare gli id: questa e' l'unica
  // tabella di conversione, ricavata dal DOM, quindi sempre coerente con cio' che l'utente legge. ----
  var _numVisCache = null;
  function _costruisciNumVis() {
    if (_numVisCache) return _numVisCache;
    var idToVis = {}, visToId = {};
    Array.prototype.slice.call(document.querySelectorAll('.card-wrap[id^="item-"]')).forEach(function(n) {
      var id = n.id.slice(5), r = n.querySelector('.rec'), m = r && r.textContent.match(/(\\d+)/);
      var v = m ? m[1] : id; idToVis[id] = v; visToId[v] = id;
    });
    _numVisCache = { idToVis: idToVis, visToId: visToId };
    return _numVisCache;
  }
  window.marvelNumeroVisibile = function(id) { var k = ('000' + id).slice(-3); return _costruisciNumVis().idToVis[k] || k; };
  window.marvelIdDaNumeroVisibile = function(num) { var k = ('000' + num).slice(-3); return _costruisciNumVis().visToId[k] || k; };
'''
s=s[:j]+helper+s[j:]
sub("'<span class=\"next-watch-sub\">Scheda N&deg;' + item.id + ' &middot; Visto il '","'<span class=\"next-watch-sub\">Scheda N&deg;' + window.marvelNumeroVisibile(item.id) + ' &middot; Visto il '")
sub("'<span class=\"next-watch-sub\">Scheda N&deg;' + it.id + '</span></span>'","'<span class=\"next-watch-sub\">Scheda N&deg;' + window.marvelNumeroVisibile(it.id) + '</span></span>'")
sub("'<span class=\"next-watch-sub\">Scheda N&deg;' + next.id + ' &middot; tocca per andarci</span>'","'<span class=\"next-watch-sub\">Scheda N&deg;' + window.marvelNumeroVisibile(next.id) + ' &middot; tocca per andarci</span>'")
sub("var sub = 'Scheda N&deg;' + item.num;","var sub = 'Scheda N&deg;' + window.marvelNumeroVisibile(item.num);")
sub("""          var n = m.replace('N°', '');
          if (nums.indexOf(n) === -1) nums.push(n);""","""          var n = window.marvelIdDaNumeroVisibile(m.replace('N°', ''));
          if (nums.indexOf(n) === -1) nums.push(n);""")
open(P,'w',encoding='utf-8').write(s); print('ok')
