  // ---- Sistema di voto: 5 stelle con mezzi voti (0,5 – 5), salvate in localStorage ----
  // Stessa chiave e stesso oggetto { idTitolo: voto } di sempre: nessuna seconda sorgente di verita'.
  // Un voto intero gia' salvato (1..5) e' un valore valido della nuova scala e non viene toccato.
  var RATINGS_KEY = 'marvel-ultimate-timeline-ratings';
  function ratingNorm(v) {
    v = Number(v);
    if (!isFinite(v) || v < 0.5) return 0;
    return Math.min(5, Math.round(v * 2) / 2);
  }
  function ratingFmt(v) { return String(v).replace('.', ','); }
  function loadRatings() {
    var out = {};
    try {
      var r = JSON.parse(localStorage.getItem(RATINGS_KEY) || '{}');
      if (r && typeof r === 'object' && !Array.isArray(r)) Object.keys(r).forEach(function(k) { var n = ratingNorm(r[k]); if (n > 0) out[k] = n; });
    } catch(e) {}
    return out;
  }
  function saveRatings(r) {
    try {
      var s = JSON.stringify(r);
      localStorage.setItem(RATINGS_KEY, s);
      return localStorage.getItem(RATINGS_KEY) === s;   // il voto conta come salvato solo se rileggibile
    } catch(e) { return false; }
  }
  // Stelle in miniatura (sola lettura), usate dove il voto e' solo mostrato (es. "ultimo titolo visto")
  function ratingMiniHtml(v) {
    v = ratingNorm(v); var h = '<span class="rw-mini" role="img" aria-label="Voto ' + ratingFmt(v) + ' su 5">';
    for (var i = 1; i <= 5; i++) h += '<i class="rw-s" style="--f:' + (v >= i ? 1 : (v >= i - 0.5 ? 0.5 : 0)) + '"></i>';
    return h + '</span>';
  }
  function ratingEl(tag, cls, txt) { var e = document.createElement(tag); if (cls) e.className = cls; if (txt) e.textContent = txt; return e; }
  function ratingBuild(widget, id) {
    widget.classList.add('rw2');
    widget.textContent = '';
    var lid = 'rw-l-' + id;
    var top = ratingEl('div', 'rw-top'), lab = ratingEl('span', 'rw-label', 'La tua valutazione'); lab.id = lid;
    var reset = ratingEl('button', 'rw-reset', 'Azzera'); reset.type = 'button'; reset.hidden = true; reset.setAttribute('aria-label', 'Azzera la valutazione');
    top.appendChild(lab); top.appendChild(reset);
    var main = ratingEl('div', 'rw-main'), stars = ratingEl('div', 'rw-stars');
    stars.setAttribute('role', 'slider'); stars.tabIndex = 0; stars.setAttribute('aria-labelledby', lid);
    stars.setAttribute('aria-valuemin', '0'); stars.setAttribute('aria-valuemax', '5'); stars.setAttribute('aria-valuestep', '0.5');
    stars.setAttribute('aria-description', 'Frecce destra e sinistra: mezzo voto. Toccando una stella si sceglie il voto intero, toccandola di nuovo il mezzo voto.');
    var sp = [];
    for (var i = 1; i <= 5; i++) {
      var s = ratingEl('span', 'rw-s'); s.setAttribute('data-k', String(i)); s.setAttribute('aria-hidden', 'true');
      stars.appendChild(s); sp.push(s);
    }
    // Interazione a due passaggi (nessuna zona di tocco stretta): 1° tocco su una stella = voto intero; 2° tocco sulla stessa stella = mezzo voto (k - 0,5); 3° = di nuovo intero.
    var hint = ratingEl('span', 'rw-hint', 'Tocca 2 volte per \u00bd'); hint.setAttribute('aria-hidden', 'true'); top.appendChild(hint);
    var val = ratingEl('span', 'rw-val'); val.setAttribute('aria-hidden', 'true');
    var vb = ratingEl('b', '', '—'), vs = ratingEl('span', 'rw-of', ' / 5'); val.appendChild(vb); val.appendChild(vs);
    main.appendChild(stars); main.appendChild(val);
    var live = ratingEl('span', 'rw-live'); live.setAttribute('role', 'status'); live.setAttribute('aria-live', 'polite');
    widget.appendChild(top); widget.appendChild(main); widget.appendChild(live);
    var cur = 0;
    function paint(v, animIdx) {
      cur = v;
      sp.forEach(function(s, k) { s.style.setProperty('--f', v >= k + 1 ? '1' : (v >= k + 0.5 ? '0.5' : '0')); });
      vb.textContent = v ? ratingFmt(v) : '—'; val.classList.toggle('rw-empty', !v);
      reset.hidden = !v; hint.hidden = !!v;
      stars.setAttribute('aria-valuenow', String(v));
      stars.setAttribute('aria-valuetext', v ? ratingFmt(v) + ' su 5' : 'Nessun voto');
      if (animIdx != null && sp[animIdx]) { var s = sp[animIdx]; s.classList.remove('rw-pop'); void s.offsetWidth; s.classList.add('rw-pop'); }
    }
    function commit(v) {
      v = ratingNorm(v);
      if (v === cur) return;
      var r = loadRatings();
      if (v > 0) r[id] = v; else delete r[id];
      if (!saveRatings(r)) { live.textContent = 'Voto non salvato: memoria del dispositivo non disponibile.'; return; }
      paint(v, v > 0 ? Math.ceil(v) - 1 : null);
      live.textContent = v ? 'Voto ' + ratingFmt(v) + ' su 5' : 'Valutazione azzerata';
      try { updateTessera(); } catch(eRatingXp) {}
      // le card "voto medio" (Home hub, Dashboard) si ricalcolano da updateProgress()
      try { updateProgress(); } catch(eRatingProgress) {}
    }
    stars.addEventListener('click', function(e) {
      var st = e.target && e.target.closest ? e.target.closest('.rw-s') : null;
      if (!st) return;
      var k = parseInt(st.getAttribute('data-k'), 10);
      commit(cur === k ? k - 0.5 : k);   // stessa stella gia' piena -> mezzo voto; altrimenti voto intero
    });
    stars.addEventListener('keydown', function(e) {
      var k = e.key, v = null;
      if (k === 'ArrowRight' || k === 'ArrowUp') v = Math.min(5, cur + 0.5);
      else if (k === 'ArrowLeft' || k === 'ArrowDown') v = Math.max(0, cur - 0.5);
      else if (k === 'PageUp') v = Math.min(5, cur + 1);
      else if (k === 'PageDown') v = Math.max(0, cur - 1);
      else if (k === 'End') v = 5;
      else if (k === 'Home' || k === 'Delete' || k === 'Backspace' || k === '0') v = 0;
      else if (/^[1-5]$/.test(k)) v = parseInt(k, 10);
      if (v === null) return;
      e.preventDefault(); commit(v);
    });
    reset.addEventListener('click', function() { commit(0); });
    paint(loadRatings()[id] || 0);
  }
  try {
    var widgets = Array.prototype.slice.call(document.querySelectorAll('.rating-widget'));
    widgets.forEach(function(widget) {
      var id = widget.getAttribute('data-item');
      ratingBuild(widget, id);
      // posizione: subito sotto titolo e informazioni principali, prima della descrizione lunga (primo sotto-gruppo)
      var card = widget.closest('details.card'), panel = null;
      if (card) for (var c = card.firstElementChild; c; c = c.nextElementSibling) { if (c.classList.contains('detail-panel')) { panel = c; break; } }
      if (panel) {
        var first = null;
        for (var q = panel.firstElementChild; q; q = q.nextElementSibling) { if (q.classList.contains('sub-group')) { first = q; break; } }
        panel.insertBefore(widget, first);
      }
    });
  } catch(errRating) {
    if (window.console) console.error('Marvel guide - blocco voto:', errRating);
  }

