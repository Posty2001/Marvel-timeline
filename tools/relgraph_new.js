    /* RG-LAYOUT-BEGIN — Grafo delle Relazioni: due colonne senza sovrapposizioni, filtri per tipo con conteggi, messaggi per zero risultati */
    var RG_ORDER = ['famiglia', 'relazione', 'variante', 'organizzazione', 'attore', 'universo', 'titolo'];
    var RG_RT_NAME = { famiglia: 'Famiglia', relazione: 'Relazione', organizzazione: 'Organizzazione', variante: 'Variante', universo: 'Universo', titolo: 'Titolo', attore: 'Attore' };
    var RG_RT_COLOR = { famiglia: '#D2B184', relazione: '#DB777C', variante: '#B58CE0', organizzazione: '#6FB5C4', attore: '#B58CE0', universo: '#5DB874', titolo: '#8D8A84' };
    var RG_PAGE = 14, rgLimit = {};
    function rgActiveTypes() { return RG_ORDER.filter(function (t) { return rgActiveFilters[t] !== false; }); }
    // unisce le connessioni verso lo stesso nodo: un solo nodo, con tutte le relazioni che superano i filtri
    function rgMergeConns(conns, active) {
      var by = {}, order = [];
      conns.forEach(function (c) {
        if (active.indexOf(c.rtype) < 0) return;
        var k = c.id; if (!by[k]) { by[k] = { id: c.id, name: c.name, type: c.type, rtypes: [], labels: [] }; order.push(k); }
        if (by[k].rtypes.indexOf(c.rtype) < 0) by[k].rtypes.push(c.rtype);
        if (by[k].labels.indexOf(c.label) < 0) by[k].labels.push(c.label);
      });
      var out = order.map(function (k) { return by[k]; });
      out.forEach(function (o) { o.rank = Math.min.apply(null, o.rtypes.map(function (t) { return RG_ORDER.indexOf(t); })); });
      return out.map(function (o, i) { return { o: o, i: i }; }).sort(function (a, b) { return a.o.rank - b.o.rank || a.i - b.i; }).map(function (x) { return x.o; });
    }
    function rgWrap(name, max) {
      var w = name.split(/(?<=\/)|\s+/).filter(Boolean), l1 = '', i = 0;
      while (i < w.length && (l1 + (l1 ? ' ' : '') + w[i]).length <= max) { l1 += (l1 ? ' ' : '') + w[i]; i++; }
      if (!l1) { return [name.length > max ? name.slice(0, max - 1) + '…' : name]; }
      var l2 = w.slice(i).join(' '); if (l2.length > max) l2 = l2.slice(0, max - 1) + '…';
      return l2 ? [l1, l2] : [l1];
    }
    function rgUpdateFilterUi(node) {
      var cnt = {}; (node ? node.conns : []).forEach(function (c) { (cnt[c.rtype] = cnt[c.rtype] || {})[c.id] = 1; });
      rgFilterBtns.forEach(function (b) {
        var t = b.getAttribute('data-rtype'), n = node ? Object.keys(cnt[t] || {}).length : null, on = rgActiveFilters[t] !== false;
        b.classList.toggle('active', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.classList.toggle('rg-empty', node ? n === 0 : false);
        var fc = b.querySelector('.rg-fc'); if (!fc) { fc = document.createElement('span'); fc.className = 'rg-fc'; b.appendChild(fc); }
        fc.textContent = n === null ? '' : String(n);
        b.setAttribute('aria-label', RG_RT_NAME[t] + (n === null ? '' : ', ' + n + (n === 1 ? ' collegamento' : ' collegamenti')) + (on ? ', attivo' : ', disattivato'));
      });
    }

    function rgRenderGraph(nodeId, pushHistory, keepLimit) {
      var node = getRelationshipGraph()[nodeId];
      if (!node || !rgSvg) return;
      if (pushHistory && rgCurrentId && rgCurrentId !== nodeId) { rgHistory.push(rgCurrentId); }
      if (!keepLimit && rgCurrentId !== nodeId) rgLimit[nodeId] = 0;
      rgCurrentId = nodeId;
      var active = rgActiveTypes(), merged = rgMergeConns(node.conns, active), limit = RG_PAGE + (rgLimit[nodeId] || 0), shown = merged.slice(0, limit);
      var nL = Math.ceil(shown.length / 2), rows = Math.max(nL, shown.length - nL, 1), SP = 66, Y0 = 56, H = Math.max(360, Y0 * 2 + (rows - 1) * SP), cy = H / 2, cx = 500, DX = 215;
      var P = [];
      P.push('<g class="rg-lines">');
      var pos = shown.map(function (c, i) {
        var left = i < nL, r = left ? i : i - nL, n = left ? nL : shown.length - nL, y = cy + (r - (n - 1) / 2) * SP, x = left ? cx - DX : cx + DX;
        return { c: c, x: x, y: y, left: left };
      });
      pos.forEach(function (p) {
        var strong = p.c.rtypes.some(function (t) { return t !== 'titolo'; }), col = RG_RT_COLOR[p.c.rtypes[0]] || '#8D8A84', dx = p.left ? -1 : 1;
        P.push('<path class="mg-edge rg-edge' + (strong ? '' : ' rg-weak') + '" d="M' + cx + ' ' + cy + ' C' + (cx + dx * 120) + ' ' + cy + ' ' + (p.x - dx * 110) + ' ' + p.y + ' ' + p.x + ' ' + p.y + '" style="stroke:' + col + ';" fill="none"></path>');
      });
      P.push('</g><g class="mg-nodes">');
      P.push('<g class="mg-node mg-active" data-node="' + rgEscAttr(nodeId) + '"><circle cx="' + cx + '" cy="' + cy + '" r="46" fill="var(--marvel-red)"></circle>' +
        '<text x="' + cx + '" y="' + (cy + 6) + '" text-anchor="middle" style="font-size:22px;">' + rgIconFor(node.type) + '</text>' +
        '<text x="' + cx + '" y="' + (cy - 62) + '" text-anchor="middle" class="mg-node-label rg-hub-label" style="font-size:19px;">' + rgEscAttr(rgWrap(node.name, 30)[0]) + '</text></g>');
      pos.forEach(function (p) {
        var c = p.c, color = RG_NODE_COLORS[c.type] || RG_NODE_COLORS.char, tx = p.x + (p.left ? -30 : 30), anc = p.left ? 'end' : 'start', nm = rgWrap(c.name, 24), lab = c.labels.join(' · ');
        if (lab.length > 30) lab = lab.slice(0, 29) + '…';
        var y0 = p.y - (nm.length === 2 ? 10 : 2), t = '<text x="' + tx + '" y="' + y0 + '" text-anchor="' + anc + '" class="mg-node-label rg-nm" style="font-size:16px;">';
        nm.forEach(function (l, k) { t += '<tspan x="' + tx + '" dy="' + (k ? '1.15em' : '0') + '">' + rgEscAttr(l) + '</tspan>'; });
        t += '</text><text x="' + tx + '" y="' + (y0 + (nm.length === 2 ? 38 : 22)) + '" text-anchor="' + anc + '" class="rg-rl" style="font-size:12.5px;fill:' + (RG_RT_COLOR[c.rtypes[0]] || '#A8A39A') + ';">' + rgEscAttr(lab) + '</text>';
        P.push('<g class="mg-node rg-satellite" data-node="' + rgEscAttr(c.id) + '" data-label="' + rgEscAttr(lab) + '" data-rt="' + c.rtypes.join(',') + '" tabindex="0" role="button" aria-label="' + rgEscAttr(c.name + ', ' + lab) + '">' +
          '<title>' + rgEscAttr(c.name + ' — ' + lab) + '</title><circle cx="' + p.x + '" cy="' + p.y + '" r="21" fill="' + color + '" stroke="' + (RG_RT_COLOR[c.rtypes[0]] || '#8D8A84') + '" stroke-width="3"></circle>' +
          '<text x="' + p.x + '" y="' + (p.y + 6) + '" text-anchor="middle" style="font-size:16px;">' + rgIconFor(c.type) + '</text>' + t + '</g>');
      });
      var emptyMsg = '';
      if (!shown.length) {
        emptyMsg = !active.length ? 'Nessun tipo di relazione selezionato: attiva almeno un filtro.' : 'Nessun collegamento di tipo ' + active.map(function (t) { return RG_RT_NAME[t]; }).join(', ') + ' per ' + node.name + ' nei dati della guida.';
        P.push('<text x="' + cx + '" y="' + (cy + 96) + '" text-anchor="middle" class="rg-zero" style="font-size:17px;">Nessun collegamento da mostrare</text>');
      }
      P.push('</g>');
      rgSvg.setAttribute('data-vb', '0 0 1000 ' + H); rgSvg.setAttribute('viewBox', '0 0 1000 ' + H);
      rgSvg.innerHTML = P.join('');
      rgUpdateFilterUi(node);

      var totalAll = rgMergeConns(node.conns, RG_ORDER).length, rest = merged.length - shown.length;
      rgInfoPanel.style.display = 'block';
      rgInfoPanel.innerHTML = '<strong>' + rgEscAttr(node.name) + '</strong><p role="status" aria-live="polite">' + shown.length + (shown.length === 1 ? ' collegamento mostrato' : ' collegamenti mostrati') + ' su ' + merged.length + ' con i filtri attivi (' + totalAll + ' totali).</p>' +
        (emptyMsg ? '<p class="rg-empty-msg">' + rgEscAttr(emptyMsg) + '</p>' : '') +
        (rest > 0 ? '<button type="button" class="lv-episode-item" id="rgMoreBtn">Mostra altri ' + Math.min(RG_PAGE, rest) + ' (' + rest + ' non mostrati)</button>' : '') +
        (rgHistory.length ? '<button type="button" class="lv-episode-item" id="rgBackBtn">&#8592; Torna a ' + rgEscAttr(getRelationshipGraph()[rgHistory[rgHistory.length-1]].name) + '</button>' : '');

