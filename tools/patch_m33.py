#!/usr/bin/env python3
"""Blocco M3.3 (idempotente, dopo patch_m32): Capitolo 0 -> singola card compatta «Prologo — Prima del Tempo» (chiusa di default)."""
import re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
if 'class="cap0-pro"' not in s:
    m=re.search(r'<section class="part cat-ch0" id="cap0">(.*?)</section>',s,flags=re.S)
    assert m
    inner=m.group(1)
    u=re.search(r'<ul class="items">.*</ul>',inner,flags=re.S); assert u
    ul=u.group(0)
    assert ul.count('<details class="card">')==5
    new=('<section class="part cat-ch0" id="cap0">\n'
     '      <details class="cap0-pro">\n'
     '        <summary>\n'
     '          <span class="cap0-ic" aria-hidden="true">&#127756;</span>\n'
     '          <span class="cap0-txt"><span class="cap0-title">Prologo &mdash; Prima del Tempo</span>'
     '<span class="cap0-sub"><span class="cap0-n">5 letture</span><span class="cap0-st">Le Ere dell\'Universo Marvel</span></span></span>\n'
     '          <span class="cap0-chev" aria-hidden="true">&#9656;</span>\n'
     '        </summary>\n'
     '        <div class="cap0-body">'+ul+'</div>\n'
     '      </details>\n    </section>')
    s=s[:m.start()]+new+s[m.end():]
CSS='''/* M33-CSS */
#cap0.part { margin: 0.7rem auto 0; padding: 0 1rem; }
#cap0.part::before { display: none; }
#cap0 { padding-top: 0; padding-bottom: 0; }
#cap0 + #parte1 { margin-top: 0.7rem; }
#cap0 + #parte1::before { margin-bottom: 0.6rem; }
#cap0 details.cap0-pro { border: 1px solid rgba(210,177,132,0.3); border-left: 3px solid rgba(210,177,132,0.7); border-radius: 10px; background: rgba(20,16,12,0.6); overflow: hidden; }
#cap0 details.cap0-pro > summary { list-style: none; display: flex; align-items: center; gap: 0.65rem; min-height: 3rem; padding: 0.4rem 0.75rem; cursor: pointer; -webkit-tap-highlight-color: transparent; }
#cap0 details.cap0-pro > summary::-webkit-details-marker { display: none; }
#cap0 .cap0-ic { flex: 0 0 auto; width: 2rem; height: 2rem; display: grid; place-items: center; font-size: 1.15rem; border-radius: 50%; background: radial-gradient(circle at 35% 30%, rgba(120,90,200,0.55), rgba(20,16,40,0.9)); }
#cap0 .cap0-txt { flex: 1 1 auto; min-width: 0; display: flex; flex-direction: column; gap: 0.1rem; }
#cap0 .cap0-title { font-size: 1rem; line-height: 1.2; font-weight: 700; }
#cap0 .cap0-sub { display: flex; align-items: center; gap: 0.45rem; min-width: 0; font-size: 0.72rem; line-height: 1.3; }
#cap0 .cap0-st { min-width: 0; opacity: 0.75; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
#cap0 .cap0-n { flex: 0 0 auto; font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; letter-spacing: 0.08em; white-space: nowrap; padding: 0.12rem 0.45rem; border-radius: 999px; border: 1px dashed rgba(210,177,132,0.5); color: rgba(210,177,132,0.95); }
#cap0 .cap0-chev { flex: 0 0 auto; font-size: 0.85rem; opacity: 0.7; transition: transform 0.15s; }
#cap0 details.cap0-pro[open] > summary .cap0-chev { transform: rotate(90deg); }
#cap0 details.cap0-pro[open] > summary { border-bottom: 1px solid rgba(210,177,132,0.18); }
#cap0 .cap0-body { padding: 0.45rem 0.5rem 0.2rem; }
#cap0 .cap0-body > ul.items { margin: 0; padding: 0; }
#cap0 .cap0-body .card-wrap { margin: 0 0 0.3rem; }
@media (max-width: 360px) { #cap0 .cap0-title { font-size: 0.92rem; } #cap0 .cap0-sub { font-size: 0.68rem; } #cap0 .cap0-n { font-size: 0.56rem; padding: 0.1rem 0.35rem; } #cap0 details.cap0-pro > summary { gap: 0.5rem; padding: 0.4rem 0.6rem; } }
'''
s=re.sub(r'/\* M33-CSS \*/.*?(?=</style>)','',s,flags=re.S)
k=s.index('</style>'); s=s[:k]+CSS+s[k:]
JS='''<script>/* M33 cap0 */
(function () {
  function det() { return document.querySelector('#cap0 details.cap0-pro'); }
  function openPro() { var d = det(); if (d && !d.open) d.open = true; }
  document.addEventListener('click', function (e) { var a = e.target && e.target.closest && e.target.closest('a[href="#cap0"]'); if (a) openPro(); }, true);
  function fromHash() { if (location.hash === '#cap0') openPro(); }
  window.addEventListener('hashchange', fromHash); fromHash();
})();
</script>'''
s=re.sub(r'<script>/\* M33 cap0 \*/.*?</script>\n?','',s,flags=re.S)
k=s.rindex('</body>'); s=s[:k]+JS+'\n'+s[k:]
s=re.sub(r'(name="tva-build" content=")[^"]*',lambda m:m.group(1)+'20261023-1500-m33',s)
open(P,'w',encoding='utf-8').write(s)
