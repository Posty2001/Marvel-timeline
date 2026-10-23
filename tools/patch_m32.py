#!/usr/bin/env python3
"""Blocco M3.2 (idempotente, dopo patch_m31): scheda Opera mobile — locandina e voto a 5 stelle nella riga principale (fuori dal pannello espandibile)."""
import re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
# 1) il voto resta lo stesso widget (stessa logica/chiave): cambia solo dove viene montato
OLD="""      if (panel) {
        panel.insertBefore(widget, panel.firstChild);   // Blocco 1: subito sotto il titolo
      }"""
NEW="""      var m32b = card && card.querySelector(':scope > summary');
      if (m32b) {   /* M3.2: voto nella riga principale; i gesti sulle stelle non aprono/chiudono la scheda */
        m32b.appendChild(widget); widget.classList.add('rw-inline');
        ['click', 'keydown', 'keyup', 'pointerup'].forEach(function (tp) { widget.addEventListener(tp, function (ev) { ev.stopPropagation(); if (tp === 'click' || ((ev.key === ' ' || ev.key === 'Enter') && ev.target.closest && ev.target.closest('.rw-stars'))) ev.preventDefault(); }); });
      } else if (panel) {
        panel.insertBefore(widget, panel.firstChild);   // Blocco 1: subito sotto il titolo
      }"""
if 'm32b' not in s:
    assert s.count(OLD)==1; s=s.replace(OLD,NEW)
# 2) locandina nella riga principale (sostituisce le miniature M3.1 nel pannello)
s=re.sub(r'<script>/\* M31 timeline thumbs.*?</script>','',s,flags=re.S)
s=re.sub(r'<script>/\* M32 poster.*?</script>','',s,flags=re.S)
JS="""<script>/* M32 poster */(function(){try{var M=window.TVA_IMG_MANIFEST||{},T=window.tvaTmdb;
function lw(li,pn){var num=li.getAttribute('data-item'),m=M['item:'+num],ok=!!(m&&m.src&&m.licence&&m.verified===true),t=!ok&&T?T.poster(num,'thumb'):null,t2=T?T.poster(num,'thumb'):null;if(!ok&&!t)return;
var sm=li.querySelector('details.card > summary');if(!sm||sm.querySelector('.m3-tl'))return;
var im=new Image();im.className='m3-tl';im.alt='';im.width=52;im.height=78;im.loading='lazy';im.decoding='async';im.referrerPolicy='no-referrer';
function usaT(){im.setAttribute('data-src','tmdb');im.srcset=t2.srcset;im.src=t2.src;}
im.onerror=function(){if(ok&&t2&&im.getAttribute('data-src')!=='tmdb'){ok=false;usaT();}else{im.remove();li.classList.remove('m3-hp');}};
if(ok)im.src=m.src;else usaT();sm.insertBefore(im,sm.firstChild);li.classList.add('m3-hp');}
Array.prototype.forEach.call(document.querySelectorAll('.card-wrap[id^="item-"]'),lw);}catch(e){}})();</script>"""
if '</body>' in s and s.count('</body>')==1: s=s.replace('</body>',JS+'</body>',1)

# 4) Atlante: collegamento al Reliquiario (stessa schermata gia' esistente, azione 'rel'; nessun contenuto duplicato)
OLDG="""{ k: 'artefatti', n: 'Artefatti', art: 'gemma', st: 'dis', d: 'Artefatti, Gemme dell’Infinito e il Reliquiario.', kw: 'gemme infinito guanto reliquie oggetti reliquiario', act: ['arc', 'art'] },"""
NEWG=OLDG+"""
        { k: 'reliquiario', n: 'Reliquiario', art: 'gemma', st: 'dis', d: 'Le sei Gemme dell’Infinito: schede, titoli e personaggi.', kw: 'gemme infinito guanto reliquiario spazio mente realtà potere anima tempo', act: ['rel'] },"""
if "kw: 'gemme infinito guanto reliquiario spazio" not in s:
    assert s.count(OLDG)==1; s=s.replace(OLDG,NEWG)
s=s.replace("artefatti: 'artefatti', art: 'artefatti',","artefatti: 'artefatti', reliquiario: 'artefatti', art: 'artefatti',") if "reliquiario: 'artefatti'" not in s else s


# 5) Attribuzione TMDB nella sezione Credits (requisito del servizio) + Privacy onesta sul caricamento delle locandine
CRED_MARK='m3-tmdb-credit'
if CRED_MARK not in s:
    k=s.index('&#127917; Credits</summary>'); e=s.index('</p>',k)+4
    credit=('\n      <p class="info-text m3-tmdb-credit"><img class="m3-tmdb-logo" src="assets/images/tmdb-logo.svg" alt="TMDB" height="12" hidden onload="this.hidden=false" onerror="this.remove()"> '
            'Le locandine, quando disponibili, provengono da <a href="https://www.themoviedb.org" target="_blank" rel="noopener noreferrer">TMDB</a>. '
            'This product uses the TMDB API but is not endorsed or certified by TMDB.</p>')
    s=s[:e]+credit+s[e:]
PRIV_OLD='Nessun dato viene inviato da nessuna parte, nessun tracciamento, nessuna pubblicit&agrave;.</p>'
PRIV_NEW=PRIV_OLD+'\n      <p class="info-text">Unica eccezione: le locandine dei titoli vengono caricate dai server di TMDB (image.tmdb.org), che vedono l&rsquo;indirizzo IP del dispositivo come per qualsiasi immagine web. Nessun dato della guida, dei progressi o dei voti viene inviato.</p>'
if 'Unica eccezione: le locandine' not in s:
    assert s.count(PRIV_OLD)==1; s=s.replace(PRIV_OLD,PRIV_NEW)
if '.m3-tmdb-logo' not in s:
    k=s.index('</style>'); s=s[:k]+'.m3-tmdb-logo{height:12px;width:auto;vertical-align:middle;margin-right:.4rem;opacity:.9}\n'+s[k:]

# 3) CSS
CSS="""/* M32-CSS */
.card-wrap .m3-tl { display: none; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary { display: grid; grid-template-columns: 3.25rem minmax(0, 1fr) auto; grid-template-rows: auto auto auto; column-gap: 0.65rem; row-gap: 0.12rem; align-items: start; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary > .m3-tl { display: block; grid-column: 1; grid-row: 1 / 4; width: 3.25rem; height: 4.875rem; aspect-ratio: 2 / 3; object-fit: cover; border-radius: 6px; border: 1px solid rgba(210,177,132,0.35); background: #1a1713; margin: 0; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary > .rec { grid-column: 2; grid-row: 1; min-width: 0; padding: 0; opacity: 0.92; font-size: 0.7rem; letter-spacing: 0.06em; align-self: end; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary > .ic { display: none; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary > .item-body { grid-column: 2; grid-row: 2; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary > .chev { grid-column: 3; grid-row: 1 / 3; align-self: center; }
html:not(#rs) .card-wrap.m3-hp > details.card > summary > .rating-widget { grid-column: 2 / 4; grid-row: 3; }
html:not(#rs) .card-wrap > details.card > summary { flex-wrap: wrap; }
html:not(#rs) .card-wrap:not(.m3-hp) > details.card > summary > .rating-widget { flex: 1 0 100%; order: 9; }
html:not(#rs) .card-wrap summary .rating-widget.rw2.rw-inline { margin: 0.25rem 0 0; padding: 0; border: 0; background: none; box-shadow: none; max-width: 100%; column-gap: 0.4rem; cursor: default; }
html:not(#rs) .card-wrap summary .rw-inline .rw-s { width: 1.6rem; height: 2.25rem; }
html:not(#rs) .card-wrap > details.card > summary .item-top { flex-direction: row; align-items: center; gap: 0.15rem 0.5rem; }
html:not(#rs) .card-wrap > details.card > summary .item-top > .title { flex: 1 0 100%; }
html:not(#rs) .card-wrap > details.card > summary .item-top > .tag { margin-left: 0; }
html:not(#rs) .card-wrap summary .rw-inline .rw-hint { display: none; }
html:not(#rs) .card-wrap summary .rw-inline .rw-val { font-size: 0.95rem; }
html:not(#rs) .card-wrap summary .rw-inline .rw-val .rw-of { display: none; }
html:not(#rs) .card-wrap summary .rw-inline .rw-reset { grid-column: 1 / -1; grid-row: 2; justify-self: start; margin-top: -0.2rem; }
"""
CSS+= '''@media (max-width: 360px) {
  html:not(#rs) .card-wrap.m3-hp > details.card > summary { grid-template-columns: 2.7rem minmax(0, 1fr) auto; column-gap: 0.5rem; }
  html:not(#rs) .card-wrap.m3-hp > details.card > summary > .m3-tl { width: 2.7rem; height: 4.05rem; grid-row: 1 / 3; }
  html:not(#rs) .card-wrap.m3-hp > details.card > summary > .rating-widget { grid-column: 1 / -1; }
  html:not(#rs) .card-wrap summary .rw-inline .rw-s { width: 1.45rem; }
  html:not(#rs) .card-wrap summary .rating-widget.rw2.rw-inline { grid-template-columns: auto auto 1fr; }
  html:not(#rs) .card-wrap summary .rw-inline .rw-stars { grid-column: 1; grid-row: 1; }
  html:not(#rs) .card-wrap summary .rw-inline .rw-val { grid-column: 2; grid-row: 1; justify-self: start; }
  html:not(#rs) .card-wrap summary .rw-inline .rw-reset { grid-row: 1; grid-column: 3; margin-top: 0; justify-self: end; }
}
'''
s=re.sub(r'/\* M32-CSS \*/.*?(?=</style>)','',s,flags=re.S)
k=s.index('</style>'); s=s[:k]+CSS+s[k:]
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+'20261023-1400-m32',s)
open(P,'w',encoding='utf-8').write(s)
