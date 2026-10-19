#!/usr/bin/env python3
"""Intro «The Living Multiverse — Infinite Realtà»: sostituisce SOLO la presentazione della schermata iniziale (#intro).
Idempotente. Preserva: ids/classi usati dalla logica (journeyStartBtn, icdDoomsday, icdSecretWars, quiz*), valori delle statistiche
(letti dal markup esistente), cancello #journeyStarted, onboarding, quiz. Il portale TVA riusa avviaViaggioConOnboarding + tvaAtlas2.enter."""
import re, math
P = '/home/claude/work/index.html'; T = '/home/claude/work/tools/'
s = open(P, encoding='utf-8').read()
css = open(T + 'living.css', encoding='utf-8').read().rstrip() + '\n'
scene = open(T + 'living_scene.html', encoding='utf-8').read()

# ---------- CSS ----------
if '/* LM-INTRO-BEGIN' in s:
    i = s.index('/* LM-INTRO-BEGIN'); j = s.index('/* LM-INTRO-END */', i) + len('/* LM-INTRO-END */\n')
    s = s[:i] + css + s[j:]
else:
    mk = "/* ---- Home hub: schermata di navigazione tra l'intro e il documento vero e proprio ---- */\n"
    assert mk in s
    s = s.replace(mk, css + mk, 1)

# ---------- markup ----------
a = s.index('<div class="intro-screen')
if 'data-lm' in s[a:a + 120]:
    b = s.index('<!--/lm-intro-->', a) + len('<!--/lm-intro-->')
else:
    b = s.index('<div class="intro-honest-note">', a); b = s.index('</div>', b) + len('</div>')
    for _ in range(3):  # foot, content, intro
        b = s.index('</div>', b) + len('</div>')
old = s[a:b]
nums = re.findall(r'class="intro-stat-num">([^<]*)<', old)
assert len(nums) == 4, nums
quiz = old[old.index('<details class="intro-quiz">'):old.index('</details>') + len('</details>')]
labels = ['titoli', 'universi', 'personaggi', 'ore complessive di visione']
stats = ''.join('<div class="intro-stat"><span class="intro-stat-num">%s</span><span class="intro-stat-lbl">%s</span></div>' % (n, l) for n, l in zip(nums, labels))
ticks = ''
for k in range(15):
    ang = math.pi * (1 - k / 14.0)
    x1, y1 = 100 + 80 * math.cos(ang), 56 - 80 * math.sin(ang) * 1.0
    x2, y2 = 100 + 86 * math.cos(ang), 56 - 86 * math.sin(ang) * 1.0
    ticks += 'M%.1f %.1f L%.1f %.1f' % (x1, y1, x2, y2)
portal = ('<svg class="lm-portal-svg" viewBox="0 0 200 120" aria-hidden="true" focusable="false"><defs>'
          '<radialGradient id="lmPg" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#fff2d2"/><stop offset=".38" stop-color="#e8928e" stop-opacity=".8"/><stop offset="1" stop-color="#8e2a3a" stop-opacity="0"/></radialGradient>'
          '<linearGradient id="lmPb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#fff2d2" stop-opacity=".9"/><stop offset="1" stop-color="#fff2d2" stop-opacity="0"/></linearGradient></defs>'
          '<path d="M30 120V58a70 70 0 0 1 140 0v62Z" fill="url(#lmPg)"/>'
          '<path d="M92 120V74a8 8 0 0 1 16 0v46Z" fill="#fff6e4"/><path d="M92 76 L40 -10 H160 L108 76Z" fill="url(#lmPb)" opacity=".45"/>'
          '<path d="M22 120V58a78 78 0 0 1 156 0v62" fill="none" stroke="#D2B184" stroke-width="2"/>'
          '<path d="M36 120V60a64 64 0 0 1 128 0v60" fill="none" stroke="#D2B184" stroke-opacity=".75" stroke-width="1.4"/>'
          '<path d="M52 120V62a48 48 0 0 1 96 0v58" fill="none" stroke="#D2B184" stroke-opacity=".5" stroke-width="1"/>'
          '<path d="%s" fill="none" stroke="#D2B184" stroke-opacity=".8" stroke-width="1"/>'
          '<path d="M8 119.2H192" stroke="#D2B184" stroke-width="1.2"/><path d="M20 115H180" stroke="#D2B184" stroke-opacity=".35"/></svg>') % ticks
arr = '<svg class="lm-arr" viewBox="0 0 24 12" aria-hidden="true" focusable="false"><path d="M1 6h20M16 1l5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def cd(i, idn, nm, short, date):
    return ('<div class="intro-cd" data-state="na"><span class="lm-ev-k">Evento futuro della Timeline</span><span class="lm-ev-name">%s</span>'
            '<span id="%s">&mdash;</span><span class="intro-cd-lbl"><span class="lm-cap">GIORNI A %s</span><span class="lm-state"></span> <small>(%s)</small></span></div>') % (nm, idn, short, date)
new = ('<div class="intro-screen lm" id="intro" data-lm>\n'
  '  <div class="lm-scene" aria-hidden="true">\n' + scene + '\n    <div class="lm-glow"></div><div class="lm-veil"></div><div class="lm-veil2"></div>\n  </div>\n'
  '  <div class="lm-scroll" id="lmScroll">\n'
  '  <div class="intro-content lm-flow">\n'
  '    <header class="intro-head lm-act1">\n'
  '      <div class="lm-art" aria-hidden="true"><div class="lm-art-box"><img class="lm-art-img" src="assets/images/intro/living-multiverse.webp" alt="" width="941" height="1672" decoding="async" fetchpriority="high"><div class="lm-fx lm-fx-core"></div><div class="lm-fx lm-fx-crack"></div><div class="lm-fx lm-fx-em lm-fx-em1"></div><div class="lm-fx lm-fx-em lm-fx-em2"></div><div class="lm-fx lm-fx-foot"></div></div></div>\n'
  '      <div class="lm-editorial" aria-hidden="true">THE LIVING MULTIVERSE</div>\n'
  '      <div class="intro-eyebrow">TIME VARIANCE AUTHORITY</div>\n'
  '      <div class="lm-sp1"></div>\n'
  '      <h1 class="intro-logo"><span class="lm-t1">MARVEL</span> <span class="intro-logo-sub">MULTIVERSE</span></h1>\n'
  '      <p class="intro-tagline">Infinite realt&agrave;. Un unico viaggio.</p>\n'
  '      <div class="lm-cta-wrap"><button type="button" class="intro-btn" id="journeyStartBtn"><span>Inizia il viaggio</span>' + arr + '</button></div>\n'
  '      <div class="lm-sp2"></div>\n'
  '      <span class="lm-cue" aria-hidden="true"></span>\n'
  '    </header>\n'
  '    <div class="lm-lower">\n'
  '      <section class="lm-act lm-act2" aria-labelledby="lmH2">\n'
  '        <span class="lm-kick">Atto II</span><h2 class="lm-h2" id="lmH2"><span>Il Multiverso si espande</span></h2>\n'
  '        <div class="intro-stats">' + stats + '<i class="lm-dia" aria-hidden="true"></i></div>\n'
  '        <div class="intro-honest-note">Numeri calcolati dai dati reali della guida, non arrotondati per impressionare.</div>\n'
  '      </section>\n'
  '      <section class="lm-act lm-act3" aria-labelledby="lmH3">\n'
  '        <span class="lm-kick">Atto III</span><h2 class="lm-h2" id="lmH3"><span>Il futuro del Multiverso</span></h2>\n'
  '        <div class="intro-ticker">' + cd(0, 'icdDoomsday', 'Avengers: Doomsday', 'DOOMSDAY', '18 DIC 2026') + cd(1, 'icdSecretWars', 'Avengers: Secret Wars', 'SECRET WARS', '17 DIC 2027') + '</div>\n'
  '      </section>\n'
  '      <section class="lm-act lm-act4" aria-labelledby="lmH4">\n'
  '        <span class="lm-kick">Atto IV</span><h2 class="lm-h2" id="lmH4"><span>Il portale TVA</span></h2>\n'
  '        <button type="button" class="lm-portal" id="lmTvaPortal">' + portal + '<span class="lm-portal-t">Esplora TVA Archives</span><span class="lm-portal-s">L&rsquo;Archivio del Multiverso</span></button>\n'
  '        <div class="lm-foot intro-foot">\n    ' + quiz.replace('&#129300; ', '') + '\n        </div>\n'
  '      </section>\n'
  '    </div>\n'
  '  </div>\n  </div>\n'
  '</div><!--/lm-intro-->')
s = s[:a] + new + s[b:]

# ---------- JS ----------
js = r'''  /* LM-INTRO-JS-BEGIN — Intro «Living Multiverse»: stato countdown, portale TVA, parallasse, asset opzionale (solo presentazione) */
  try {
    var lmIntro = document.getElementById('intro');
    if (lmIntro && lmIntro.hasAttribute('data-lm')) {
      var lmRM = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
      ['icdDoomsday', 'icdSecretWars'].forEach(function(id) {
        var e = document.getElementById(id), h = e && e.closest ? e.closest('.intro-cd') : null; if (!h) return;
        var t = (e.textContent || '').trim();
        h.setAttribute('data-state', /^\d+$/.test(t) ? 'future' : (t === 'OGGI' ? 'today' : (t === 'USCITO' ? 'out' : 'na')));
      });
      var lmPortal = document.getElementById('lmTvaPortal');
      if (lmPortal) lmPortal.addEventListener('click', function() {
        if (lmPortal.getAttribute('data-busy')) return;
        lmPortal.setAttribute('data-busy', '1');
        var vai = function() {
          lmPortal.removeAttribute('data-busy'); lmIntro.classList.remove('lm-enter');
          avviaViaggioConOnboarding(function() { try { if (window.tvaAtlas2 && typeof window.tvaAtlas2.enter === 'function') window.tvaAtlas2.enter(); } catch (eLmA) {} });
        };
        if (lmRM) vai(); else { lmIntro.classList.add('lm-enter'); setTimeout(vai, 420); }
      });
      var lmSc = document.getElementById('lmScroll');
      if (lmSc) {
        var lmRaf = 0;
        lmSc.addEventListener('scroll', function() {
          if (lmRaf) return;
          lmRaf = requestAnimationFrame(function() {
            lmRaf = 0; var h = lmSc.clientHeight || 1;
            lmIntro.style.setProperty('--lm-p', Math.max(0, Math.min(1, lmSc.scrollTop / (h * 0.9))).toFixed(3));
          });
        }, { passive: true });
      }
      /* Illustrazione approvata (assets/images/intro/living-multiverse.webp): elemento dominante dell'Atto I.
         Se il file non carica, si toglie lm-art-on e ricompare la scena SVG con titolo e pulsante HTML. */
      if (lmSc) lmSc.addEventListener('scroll', function() { if (lmIntro.classList.contains('lm-art-ready') && lmSc.scrollTop !== 0) lmSc.scrollTop = 0; }, { passive: true });
      var lmImg = lmIntro.querySelector('.lm-art-img');
      if (lmImg) {
        var lmOk = function() { if (lmImg.naturalWidth > 0) { lmIntro.classList.add('lm-art-ready'); if (lmSc) lmSc.scrollTop = 0; } };
        if (lmImg.complete) { if (lmImg.naturalWidth > 0) lmOk(); else lmIntro.classList.remove('lm-art-ready'); } else lmImg.addEventListener('load', lmOk);
        lmImg.addEventListener('error', function() { lmIntro.classList.remove('lm-art-ready'); });
      }
    }
  } catch (eLmIntro) { if (window.console) console.error('Marvel guide - intro Living Multiverse:', eLmIntro); }
  /* LM-INTRO-JS-END */
'''
if '/* LM-INTRO-JS-BEGIN' in s:
    i = s.index('  /* LM-INTRO-JS-BEGIN'); j = s.index('/* LM-INTRO-JS-END */\n', i) + len('/* LM-INTRO-JS-END */\n')
    s = s[:i] + js + s[j:]
else:
    mk = "    if (window.console) console.error('Marvel guide - blocco countdown:', errCountdown);\n  }\n"
    assert s.count(mk) == 1
    s = s.replace(mk, mk + js, 1)
pl = '<link rel="preload" as="image" href="assets/images/intro/living-multiverse.webp" type="image/webp" fetchpriority="high">\n'
if pl not in s:
    i = s.index('<meta name="tva-build"'); j = s.index('\n', i) + 1; s = s[:j] + pl + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok', len(s.encode()))
