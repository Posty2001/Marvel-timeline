/* PRE5-JS-BEGIN */
(function(){
  'use strict';
  var KEY = 'marvel-ultimate-timeline-last-watched';
  function lastId(){ try { var r = JSON.parse(localStorage.getItem(KEY) || 'null'); return r && r.id ? String(r.id) : null; } catch(e){ return null; } }
  function checks(){ return Array.prototype.slice.call(document.querySelectorAll('li.card-wrap input.watch-check[data-item]')); }
  function visible(el){ var w = el.closest('li.card-wrap'); return !!(w && w.getClientRects().length); }
  function pick(){
    var all = checks(); if (!all.length) return null;
    var lid = lastId(), idx = -1, i;
    if (lid) for (i = 0; i < all.length; i++) if (all[i].getAttribute('data-item') === lid) { idx = i; break; }
    var order = idx >= 0 ? all.slice(idx + 1).concat(all.slice(0, idx + 1)) : all;
    for (i = 0; i < order.length; i++) if (!order[i].checked && visible(order[i])) return { cb: order[i], first: idx < 0 && !all.some(function(c){ return c.checked; }) };
    for (i = 0; i < all.length; i++) if (visible(all[i])) return { cb: all[i], first: false };
    return null;
  }
  function titleOf(cb){ var w = cb.closest('li.card-wrap'), t = w && w.querySelector('.title'); return t ? t.textContent.trim() : ''; }
  function label(){
    var btn = document.getElementById('cvContinueBtn'); if (!btn) return;
    var p = pick(), sub = btn.querySelector('.cv-c-sub'), lbl = btn.querySelector('.cv-c-lbl');
    if (!p) { sub.textContent = ''; return; }
    lbl.textContent = p.first ? 'Inizia il percorso' : 'Continua il percorso';
    sub.textContent = 'N°' + p.cb.getAttribute('data-item') + ' · ' + titleOf(p.cb);
  }
  function go(){
    var p = pick(); if (!p) return;
    var hx = document.getElementById('homeHubExited'), jc = document.getElementById('journeyStarted');
    if (jc && !jc.checked) jc.checked = true;
    if (hx && !hx.checked) hx.checked = true;
    var w = p.cb.closest('li.card-wrap'); if (!w) return;
    var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    try { w.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' }); } catch(e){ w.scrollIntoView(); }
    var c = w.querySelector('details.card') || w;
    c.classList.remove('cv-flash'); void c.offsetWidth; c.classList.add('cv-flash');
    setTimeout(function(){ c.classList.remove('cv-flash'); }, 1600);
  }
  function init(){
    var btn = document.getElementById('cvContinueBtn'); if (!btn || btn.__pre5) return; btn.__pre5 = 1;
    btn.addEventListener('click', go);
    document.addEventListener('change', function(e){ if (e.target && e.target.classList && e.target.classList.contains('watch-check')) label(); });
    window.addEventListener('storage', label);
    label();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  setTimeout(label, 600);
  /* overlay iOS: ora sono contenuto di pagina; all'apertura si riparte dall'alto */
  ['kangTvaGraphToggle','relationshipGraphToggle','universeTimelineToggle','altTimelineToggle'].forEach(function(id){
    var t = document.getElementById(id); if (!t) return;
    t.addEventListener('change', function(){ try { window.scrollTo({ top: 0, behavior: 'instant' }); } catch(e){ window.scrollTo(0, 0); } });
  });
})();
/* PRE5-JS-END */
