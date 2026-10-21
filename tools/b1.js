/* B1-JS-BEGIN */
(function () {
  var D = document, H = D.documentElement;
  function setView(v) { if (H.getAttribute('data-tva-view') !== v) H.setAttribute('data-tva-view', v); }
  H.setAttribute('data-tva-view', 'timeline');
  window.tvaViewForTab = function (tab) { setView(tab === 'missioni' ? 'centrale' : 'timeline'); };
  // cambio vista indotto da uno scroll: la scheda attiva in basso segue (solo tra Timeline e Centrale)
  function goView(v) {
    try { var a = D.querySelector('.app-tab-active'), t = a && a.getAttribute('data-tab'); if (v === 'centrale' && window.marvelUniFiltroReset) window.marvelUniFiltroReset();
      if (window.marvelAggiornaTab && (!t || t === 'timeline' || t === 'missioni')) window.marvelAggiornaTab(v === 'centrale' ? 'missioni' : 'timeline'); } catch (e) {}
    setView(v);
  }
  // la voce Centrale TVA mostra gli strumenti; ogni altra destinazione torna al percorso di visione
  var orig = window.aggiornaTabAttiva;
  D.addEventListener('click', function (e) {
    var t = e.target && e.target.closest ? e.target.closest('.app-tab, a[href^="#"]') : null;
    if (!t) return;
    if (t.classList.contains('app-tab')) { setView(t.getAttribute('data-tab') === 'missioni' ? 'centrale' : 'timeline'); return; }
    var h = t.getAttribute('href');
    if (h === '#dashboard' || h === '#database') setView('centrale'); else if (h && h.length > 1) setView('timeline');
  }, true);
  // qualsiasi scroll verso un elemento nascosto dalla vista corrente cambia vista (ricerca globale, hub, link interni)
  var sv = Element.prototype.scrollIntoView;
  Element.prototype.scrollIntoView = function () {
    try {
      var v = H.getAttribute('data-tva-view');
      if (v === 'centrale' && this.closest && this.closest('.part, .card-wrap, #cover, #indice, #gtimeline')) goView('timeline');
      else if (v === 'timeline' && this.closest && this.closest('#dashboard, #database')) goView('centrale');
    } catch (e) {}
    return sv.apply(this, arguments);
  };
})();
/* B1-JS-END */
