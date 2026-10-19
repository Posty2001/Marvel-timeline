P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(s.count(old),old[:70]); s=s.replace(old,new)
rep('''    <button type="button" class="at-mode-btn at-mode-active" data-mode="chrono">&#8987; Cronologico</button>
    <button type="button" class="at-mode-btn" data-mode="release">&#127916; Uscita</button>''',
'''    <button type="button" class="at-mode-btn at-mode-active" data-mode="recommended" title="Ordine di visione consigliato dalla guida (predefinito)">&#129517; Consigliato</button>
    <button type="button" class="at-mode-btn" data-mode="release" title="Ordine di uscita reale">&#127916; Uscita</button>
    <button type="button" class="at-mode-btn" data-mode="events" title="Per anno di ambientazione, separato per continuit&agrave;">&#8987; Eventi</button>''')
rep("      if (mode === 'chrono') {\n        html = data.map(","      if (mode === 'chrono' || mode === 'recommended') {\n        atModeNote.textContent = 'Ordine di visione consigliato dalla guida: \\u00e8 quello predefinito. Non \\u00e8 n\\u00e9 l\\'ordine di uscita n\\u00e9 una cronologia degli eventi.';\n        atModeNote.style.display = 'block';\n        html = data.map(")
rep("      } else if (mode === 'saga') {\n        var sagas = [];",
'''      } else if (mode === 'events') {
        html = atEventiHtml(data);
        atModeNote.textContent = 'Per anno di ambientazione dichiarato nella scheda, DENTRO ogni continuit\\u00e0: continuit\\u00e0 diverse non vengono fuse in un\\'unica linea del tempo. ~ = data approssimata o dibattuta; i titoli senza data sicura (o non ancora usciti) restano in coda al proprio gruppo.';
        atModeNote.style.display = 'block';
      } else if (mode === 'saga') {
        var sagas = [];''')
# funzioni di supporto prima di atRender
rep("    function atRender(mode) {",
'''    // ---- Modalit\\u00e0 "Eventi": nessun dato nuovo e nessuna scheda duplicata. Legge l'ambientazione gi\\u00e0 presente in
    // atlasData.opere, ne ricava (se c'\\u00e8) il primo anno e raggruppa per continuit\\u00e0. Se la data non \\u00e8 sicura, lo dice. ----
    var AT_MESI_RE = /^\\d{1,2}\\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\\s+\\d{4}$/i;
    function atAnnoEvento(amb) {
      var t = String(amb || '').trim();
      var out = { y: null, inc: false, periodo: false };
      if (!t || /^TBD$/i.test(t) || AT_MESI_RE.test(t) || /contemporanea|atemporale|fuori dal tempo|Battleworld|gotica/i.test(t) && !/\\b(1\\d{3}|20\\d{2})\\b/.test(t)) return out;
      var m;
      if ((m = t.match(/^(?:dal\\s+)?(\\d{3,4})\\s*a\\.C\\./i)) || (m = t.match(/dal\\s+(\\d{3,4})\\s*a\\.C\\./i))) { out.y = -parseInt(m[1], 10); out.periodo = true; }
      else if ((m = t.match(/\\b(1\\d{3}|20\\d{2})\\b/))) { out.y = parseInt(m[1], 10); }
      else if ((m = t.match(/(inizio|primi|metà|meta)\\s+anni\\s+2000/i))) { out.y = /inizio/i.test(m[1]) ? 2000 : (/primi/i.test(m[1]) ? 2001 : 2005); out.inc = true; }
      else if ((m = t.match(/anni\\s+'(\\d)0/))) { out.y = 1900 + parseInt(m[1], 10) * 10; out.inc = true; }
      else if ((m = t.match(/metà\\s+'(\\d)00/i))) { out.y = 1000 + parseInt(m[1], 10) * 100 + 50; out.inc = true; }
      if (out.y !== null) {
        if (/\\d{4}\\s*[-\\u2013]\\s*\\d{2,4}|dal |dagli |a\\.C\\./i.test(t)) out.periodo = true;
        if (/dibattut|alt\\.|universo alt|multiplo|\\/ futuro/i.test(t)) out.inc = true;
      }
      return out;
    }
    function atFmtAnno(y) { return y < 0 ? (-y) + ' a.C.' : String(y); }
    function atEventiHtml(data) {
      var atlas = null;
      try { atlas = JSON.parse(document.getElementById('atlasData').textContent); } catch(eAtl) {}
      var opere = {}, nomiUni = {};
      if (atlas) {
        (atlas.opere || []).forEach(function(o) { opere[o.id] = o; });
        (atlas.universi || []).forEach(function(u) { nomiUni[u.id] = u.nome; });
      }
      var gruppi = {}, ordineGruppi = [];
      data.forEach(function(item, idx) {
        var id = ('000' + item.num).slice(-3), o = opere[id] || {};
        var uid = (o.universi && o.universi[0]) || ('studio-' + item.studio);
        if (!gruppi[uid]) { gruppi[uid] = { label: nomiUni[uid] || item.studio, items: [], uid: uid }; ordineGruppi.push(uid); }
        gruppi[uid].items.push({ item: item, idx: idx, ev: atAnnoEvento(o.ambientazione), amb: o.ambientazione || '' });
      });
      ordineGruppi.sort(function(a, b) {
        var ma = a === 'uni-earth-199999-mcu' ? 0 : 1, mb = b === 'uni-earth-199999-mcu' ? 0 : 1;
        return ma - mb;
      });
      var html = '';
      ordineGruppi.forEach(function(uid) {
        var g = gruppi[uid];
        var datati = g.items.filter(function(x) { return x.ev.y !== null; }).sort(function(a, b) { return a.ev.y - b.ev.y || a.idx - b.idx; });
        var nd = g.items.filter(function(x) { return x.ev.y === null; });
        html += '<li class="at-group-head">' + atEsc(g.label) + '</li>';
        datati.forEach(function(x) {
          var sub = 'Scheda N&deg;' + window.marvelNumeroVisibile(x.item.num) + ' &middot; ' + (x.ev.inc ? '~' : '') + atFmtAnno(x.ev.y) + (x.ev.periodo ? ' (periodo)' : '') + ' &middot; ' + atEsc(x.amb.length > 60 ? x.amb.slice(0, 57) + '\\u2026' : x.amb);
          html += atRowHtml(x.item, {}).replace(/<span class="at-row-sub">[^<]*<\\/span>/, '<span class="at-row-sub">' + sub + '</span>');
        });
        if (nd.length) {
          html += '<li class="at-group-head at-group-sub">Senza data sicura (ordine consigliato)</li>';
          nd.forEach(function(x) {
            var sub = 'Scheda N&deg;' + window.marvelNumeroVisibile(x.item.num) + ' &middot; data non determinabile' + (x.amb ? ' (' + atEsc(x.amb.length > 40 ? x.amb.slice(0, 37) + '\\u2026' : x.amb) + ')' : '');
            html += atRowHtml(x.item, {}).replace(/<span class="at-row-sub">[^<]*<\\/span>/, '<span class="at-row-sub">' + sub + '</span>');
          });
        }
      });
      return html;
    }

    function atRender(mode) {''')
rep("          atRender('chrono');\n        }\n      });\n    }\n  } catch(errAltTimeline)","          atRender('recommended');\n        }\n      });\n    }\n  } catch(errAltTimeline)")
rep("Timeline Alternativa: stessi 139 titoli, cinque modi","Timeline Alternativa: stessi 138 titoli, sei modi")
open(P,'w',encoding='utf-8').write(s); print('ok')
