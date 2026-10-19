/* SH-JS-BEGIN: intestazione immersiva TVA (Indietro · titolo · App Marvel) per gli overlay classici */
(function () {
  'use strict';
  var D = document, W = window; if (W.__tvaShell) return; W.__tvaShell = true;
  var IDS = ['multiverseGraphToggle', 'universeTimelineToggle', 'altTimelineToggle', 'relationshipGraphToggle', 'kangTvaGraphToggle', 'tvaArchivesToggle'];
  function $(i) { return D.getElementById(i); }
  function build() {
    if ($('tvaShell') || !D.body) return;
    var h = D.createElement('header'); h.id = 'tvaShell'; h.setAttribute('role', 'banner');
    h.innerHTML = '<button type="button" class="ts-back" aria-label="Indietro"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>'
      + '<div class="ts-ttl"><span class="ts-eyebrow">TVA ARCHIVES</span><b class="ts-t"></b></div>'
      + '<button type="button" class="ts-exit" aria-label="Torna all’app Marvel"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 11l8-7 8 7M6 10v10h12V10"/></svg><span>App Marvel</span></button>';
    D.body.appendChild(h);
    function home() { try { if (W.marvelChiudiOverlay) W.marvelChiudiOverlay(); } catch (e) {} var t = $('appTabHome'); if (t) t.click(); }
    h.querySelector('.ts-back').addEventListener('click', function () {
      var st = W.tvaNavStato ? W.tvaNavStato() : null;
      if (st && st.depth > 0 && W.tvaBack && W.tvaBack()) return;
      home();
    });
    h.querySelector('.ts-exit').addEventListener('click', function () {
      if (W.tvaTornaApp && W.tvaTornaApp()) return;
      home();
    });
    var bb = $('tvaBackBtn');
    function lbl() { var t = bb && bb.querySelector('.tva-back-t'); var b = h.querySelector('.ts-back'); b.setAttribute('aria-label', t && !bb.hidden ? t.textContent : 'Indietro'); b.title = b.getAttribute('aria-label'); }
    if (bb && W.MutationObserver) new MutationObserver(lbl).observe(bb, { childList: true, subtree: true, attributes: true }); lbl();
  }
  if (D.readyState === 'loading') D.addEventListener('DOMContentLoaded', build); else build();
})();
/* SH-JS-END */
