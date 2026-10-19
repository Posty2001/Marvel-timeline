P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def rep(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(s.count(old),old[:80]); s=s.replace(old,new)
# --- Vision Quest ---
rep('"release": "2026-10-14"}','"release": "2026-10-13"}')
rep('"uscita":"2026-10-14","significatoAnnoCard":"uscita","ruolo":"primario","precisioneUscita":"giorno"}','"uscita":"2026-10-13","significatoAnnoCard":"uscita","ruolo":"primario","precisioneUscita":"giorno"}')
rep('<span class="yr">14 ott 2026, già uscita</span>','<span class="yr">13 ott 2026 (USA), già uscita</span>')
# --- Encore: stato personale nella sezione Versioni alternative ---
rep('<a href="#item-133" class="variant-goto" data-goto="133">Apri la scheda Encore &rarr;</a></span></div></div>',
    '<a href="#item-133" class="variant-goto" data-goto="133">Apri la scheda Encore &rarr;</a></span></div><div class="detail-row lvl-light"><span class="detail-k">LA TUA VISIONE</span><span class="detail-v lvl-light"><span class="variant-state" data-variant-state="133">Versione Encore non segnata.</span> Annotazione personale: non modifica il completamento di Endgame, n&eacute; XP o titoli.</span></div></div>')
rep("""    Array.prototype.slice.call(document.querySelectorAll('.variant-check')).forEach(function(vchk) {
      var vid = vchk.getAttribute('data-item');
      var vwrap = vchk.closest ? vchk.closest('.card-wrap') : null;
      if (loadStateRaw()[vid]) { vchk.checked = true; if (vwrap) vwrap.classList.add('watched'); }
      vchk.addEventListener('change', function() {
        setVariantSeen(vid, vchk.checked);
        if (vwrap) vwrap.classList.toggle('watched', vchk.checked);
      });
    });""","""    Array.prototype.slice.call(document.querySelectorAll('.variant-check')).forEach(function(vchk) {
      var vid = vchk.getAttribute('data-item');
      var vwrap = vchk.closest ? vchk.closest('.card-wrap') : null;
      function aggiornaStatoVariante() {
        var st = document.querySelector('[data-variant-state="' + vid + '"]');
        if (st) st.textContent = vchk.checked ? '\\u2713 Versione Encore segnata come vista.' : 'Versione Encore non segnata.';
      }
      if (loadStateRaw()[vid]) { vchk.checked = true; if (vwrap) vwrap.classList.add('watched'); }
      aggiornaStatoVariante();
      vchk.addEventListener('change', function() {
        setVariantSeen(vid, vchk.checked);
        if (vwrap) vwrap.classList.toggle('watched', vchk.checked);
        aggiornaStatoVariante();
      });
    });""")
# --- RTD: chiarimenti ---
rep("Le 16 schede della lista &laquo;Countdown to Avengers: Doomsday&raquo; di Marvel/Disney+ (consiglio, non obbligo), nell&rsquo;ordine di visione. Il livello (essenziale, consigliato, facoltativo) &egrave; della guida e si legge nella scheda N&deg;136.",
    "Le 16 schede sono la watchlist ufficiale &laquo;Countdown to Avengers: Doomsday&raquo; di Marvel/Disney+ (un consiglio, non un obbligo). I livelli Essenziale, Consigliato e Facoltativo accanto a ogni titolo sono classificazioni editoriali di TVA Archive, non indicazioni di Marvel; il dettaglio &egrave; nella scheda N&deg;136.")
rep("tierEl.title = 'Livello nel percorso verso Doomsday (N\\u00B0136)';","tierEl.title = 'Classificazione editoriale TVA Archive (non ufficiale Marvel) nel percorso verso Doomsday, N\\u00B0136';")
rep("<b>Come leggere i livelli.</b> Essenziale:","<b>Due cose distinte.</b> &#128203; = titolo nella watchlist ufficiale Marvel/Disney+ (15 titoli, 16 schede). Essenziale, Consigliato e Facoltativo sono invece classificazioni editoriali di TVA Archive, non indicazioni di Marvel. <b>Come leggere i livelli.</b> Essenziale:")
rep("var lkHtml = '', whyHtml = '';","var lkHtml = '', whyHtml = '';\n            var inListaMarvel = ['015','016','041','051','084','089','095','097','099','102','108','112','117','121','123','125'].indexOf(n) !== -1;")
rep("""lkHtml = ' <span class="dep-chip-lk">'""","""lkHtml = (inListaMarvel ? ' <span class="dep-chip-off" title="Nella watchlist ufficiale Marvel/Disney+" aria-label="Nella watchlist ufficiale Marvel/Disney+">&#128203;</span>' : '') + ' <span class="dep-chip-lk">'""")
rep(".dep-chip-lk { font-size: 0.72rem; letter-spacing: 0.1em; }",".dep-chip-lk, .dep-chip-off { font-size: 0.72rem; letter-spacing: 0.1em; }")
open(P,'w',encoding='utf-8').write(s); print('ok')
