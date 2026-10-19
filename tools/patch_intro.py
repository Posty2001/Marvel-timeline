import re
p='/home/claude/work/index.html'
s=open(p,encoding='utf-8').read()
def rep(old,new):
    global s
    assert s.count(old)==1,(old[:60],s.count(old)); s=s.replace(old,new)

# 1) base .intro-screen: ancorata con top/bottom (niente 100vh/100dvh/-webkit-fill-available)
rep(""".intro-screen {
  position: fixed; top: 0; left: 0; right: 0; height: 100vh; height: 100dvh; display: flex; align-items: center; justify-content: center;
  background: #0f0d0a; color: #efe4c9; overflow-y: auto; text-align: center;
  padding: 2rem 1.5rem; z-index: 250;
  align-items: flex-start; box-sizing: border-box;
  padding: calc(2rem + var(--sat)) calc(1.5rem + var(--sar)) calc(2rem + var(--sab)) calc(1.5rem + var(--sal));
}""","""/* Schermata iniziale — redesign responsive. Ancorata con top/bottom:0 (NON 100vh/100dvh/-webkit-fill-available:
   su iOS standalone queste unita' possono non coincidere con lo schermo vero). Le misure verticali derivano
   dall'altezza disponibile (--ivh = 1dvh dove supportata, altrimenti 1vh) via clamp(); overflow-y:auto resta
   solo come ripiego per schermi molto piccoli / testo ingrandito, non per nascondere contenuti. */
:root { --ivh: 1vh; }
@supports (height: 1dvh) { :root { --ivh: 1dvh; } }
.intro-screen {
  position: fixed; top: 0; right: 0; bottom: 0; left: 0; height: auto; z-index: 250;
  display: flex; align-items: flex-start; justify-content: center; box-sizing: border-box;
  background: #0f0d0a; color: #efe4c9; text-align: center;
  overflow-y: auto; -webkit-overflow-scrolling: touch; overscroll-behavior: contain;
  padding:
    calc(var(--sat) + clamp(0.6rem, calc(var(--ivh) * 3), 1.6rem))
    calc(var(--sar) + clamp(1rem, 5vw, 1.5rem))
    calc(var(--sab) + clamp(0.6rem, calc(var(--ivh) * 3), 1.6rem))
    calc(var(--sal) + clamp(1rem, 5vw, 1.5rem));
}""")
# 2) standalone: l'intro non usa piu' fill-available
rep("""  .intro-screen, .onboarding-screen {
    height: -webkit-fill-available;""","""  .onboarding-screen {
    height: -webkit-fill-available;""")
# 3) rimuovi regole ticker/media superate dalla nuova struttura
for pat in [r"@media \(max-width: 480px\) \{\n  \.intro-ticker-sep \{[^}]*\}\n\}\n", r"@media \(max-width: 560px\) \{\n  \.intro-stats \{ grid-template-columns: repeat\(2, 1fr\); \}\n\}\n",
            r"^\.intro-ticker \{[^}]*\}\n", r"^\.intro-ticker span\[id\] \{[^}]*\}\n", r"^\.intro-ticker-sep \{[^}]*\}\n", r"^\.intro-ticker-bolt \{[^}]*\}\n"]:
    m=re.findall(pat,s,re.M); assert len(m)==1,(pat,len(m)); s=re.sub(pat,'',s,count=1,flags=re.M)
# 4) nuove regole (prima della Home hub)
css=r"""/* ---- Schermata iniziale: struttura head / main / foot ---- */
.intro-screen .intro-content {
  width: 100%; max-width: 640px; margin: auto; display: flex; flex-direction: column;
  gap: clamp(0.7rem, calc(var(--ivh) * 2.6), 1.7rem);
}
.intro-head { display: flex; flex-direction: column; align-items: center; }
.intro-screen .intro-eyebrow {
  font-size: clamp(0.56rem, 2.6vw, 0.7rem); letter-spacing: 0.16em; line-height: 1.45;
  margin-bottom: clamp(0.45rem, calc(var(--ivh) * 1.7), 1.1rem); text-wrap: balance;
}
@media (min-width: 400px) { .intro-screen .intro-eyebrow { letter-spacing: 0.24em; } }
.intro-screen .intro-logo { font-size: clamp(1.85rem, min(9vw, calc(var(--ivh) * 6.2)), 3.4rem); }
.intro-screen .intro-logo-sub { font-size: clamp(0.85rem, min(3.6vw, calc(var(--ivh) * 2.5)), 1.3rem); }
.intro-screen .intro-sub {
  font-size: clamp(0.8rem, min(3.4vw, calc(var(--ivh) * 2.2)), 1.3rem); letter-spacing: 0.3em;
  margin: clamp(0.3rem, calc(var(--ivh) * 1), 0.7rem) 0 0;
}
.intro-screen .intro-tagline { margin: clamp(0.25rem, calc(var(--ivh) * 0.8), 0.5rem) 0 0; color: rgba(239,228,201,0.6); }
.intro-main { display: flex; flex-direction: column; gap: clamp(0.5rem, calc(var(--ivh) * 1.5), 1rem); }
/* statistiche: griglia 2x2 (4 colonne solo sopra 560px), card orizzontali compatte */
.intro-screen .intro-stats { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.5rem; margin: 0; }
@media (min-width: 560px) { .intro-screen .intro-stats { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
.intro-screen .intro-stat {
  display: grid; grid-template-columns: auto minmax(0, 1fr); grid-template-areas: "ic num" "ic lbl";
  column-gap: 0.5rem; align-items: center; justify-content: center; text-align: left;
  padding: clamp(0.3rem, calc(var(--ivh) * 0.9), 0.55rem) 0.5rem;
}
.intro-screen .intro-stat-ic { grid-area: ic; font-size: clamp(1.1rem, calc(var(--ivh) * 3), 1.4rem); margin: 0; }
.intro-screen .intro-stat-num { grid-area: num; font-size: clamp(1.05rem, calc(var(--ivh) * 2.9), 1.5rem); line-height: 1.1; }
.intro-screen .intro-stat-lbl { grid-area: lbl; font-size: 0.62rem; margin: 0; line-height: 1.2; opacity: 0.75; overflow-wrap: anywhere; }
/* countdown: due tile affiancati */
.intro-ticker { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.5rem; }
.intro-cd {
  display: flex; flex-direction: column; align-items: center; justify-content: center; min-width: 0;
  padding: clamp(0.3rem, calc(var(--ivh) * 0.9), 0.55rem) 0.4rem;
  border: 1px solid rgba(200,39,42,0.4); border-radius: 4px; background: rgba(200,39,42,0.07);
}
.intro-cd > span[id] {
  font-family: 'Special Elite', monospace; font-weight: 700; line-height: 1.1; color: var(--marvel-red);
  font-size: clamp(1.2rem, calc(var(--ivh) * 3.4), 1.7rem); text-shadow: 0 0 8px rgba(200,39,42,0.5);
}
.intro-cd-lbl {
  font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; letter-spacing: 0.04em; line-height: 1.25;
  color: #efe4c9; opacity: 0.85; margin-top: 0.15rem; overflow-wrap: anywhere;
}
/* pulsante principale */
.intro-screen #journeyStartBtn {
  display: flex; align-items: center; justify-content: center; width: 100%; max-width: 22rem; margin: 0 auto;
  min-height: 3rem; padding: 0.65rem 1.2rem; box-sizing: border-box; font-size: clamp(0.9rem, 4vw, 1rem);
}
/* parte secondaria, meno prominente */
.intro-foot { display: flex; flex-direction: column; align-items: center; gap: 0.15rem; }
.intro-screen .intro-quiz { margin: 0; width: 100%; }
.intro-screen .intro-quiz-summary { display: flex; align-items: center; justify-content: center; min-height: 44px; }
.intro-screen .intro-flicker { margin: 0; font-size: 0.62rem; opacity: 0.8; }
.intro-screen .intro-honest-note { margin: 0.2rem 0 0; font-size: 0.6rem; }
/* telefono in orizzontale / altezze molto basse: due colonne */
@media (orientation: landscape) and (max-height: 520px) {
  .intro-screen .intro-content {
    max-width: 880px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1.1fr);
    grid-template-areas: "head main" "foot main"; align-items: center; column-gap: clamp(1rem, 4vw, 2rem); row-gap: 0.4rem;
  }
  .intro-head { grid-area: head; } .intro-main { grid-area: main; } .intro-foot { grid-area: foot; }
  .intro-screen .intro-logo { font-size: clamp(1.7rem, calc(var(--ivh) * 9), 2.6rem); }
  .intro-screen .intro-eyebrow { margin-bottom: 0.4rem; }
}
"""
rep("/* ---- Home hub: schermata di navigazione tra l'intro e il documento vero e proprio ---- */\n", css+"/* ---- Home hub: schermata di navigazione tra l'intro e il documento vero e proprio ---- */\n")
# 5) markup
a=s.index('<div class="intro-screen" id="intro">'); b=s.index('<div class="intro-honest-note">',a); b=s.index('</div>',b)+len('</div>')
old=s[a:b]
quiz=old[old.index('    <details class="intro-quiz">'):old.index('</details>')+len('</details>')]
stats=old[old.index('    <div class="intro-stats">'):old.index('    <div class="intro-ticker">')]
new='''<div class="intro-screen" id="intro">
  <div class="intro-scanlines"></div>
  <div class="intro-content">
    <header class="intro-head">
      <div class="intro-eyebrow">TIME VARIANCE AUTHORITY &middot; ARCHIVIO CENTRALE</div>
      <h1 class="intro-logo">MARVEL<span class="intro-logo-sub">MULTIVERSE</span></h1>
      <div class="intro-sub">TVA ARCHIVE</div>
      <p class="intro-tagline">The definitive interactive Marvel viewing experience.</p>
    </header>
    <div class="intro-main">
'''+stats.replace('    <div class="intro-stats">','      <div class="intro-stats">',1)+'''      <div class="intro-ticker">
        <div class="intro-cd"><span id="icdDoomsday">&mdash;</span><span class="intro-cd-lbl">GIORNI A DOOMSDAY <small>(18 DIC 2026)</small></span></div>
        <div class="intro-cd"><span id="icdSecretWars">&mdash;</span><span class="intro-cd-lbl">GIORNI A SECRET WARS <small>(17 DIC 2027)</small></span></div>
      </div>
      <button type="button" class="intro-btn" id="journeyStartBtn">&#128640; Inizia il viaggio</button>
    </div>
    <div class="intro-foot">
'''+quiz+'''
      <div class="intro-flicker">&#9889; ACCESSO ARCHIVIO TVA IN CORSO... &#9889;</div>
      <div class="intro-honest-note">Numeri calcolati dai dati reali della guida, non arrotondati per impressionare.</div>
    </div>
  </div>
</div>'''
s=s[:a]+new+s[b:]
open(p,'w',encoding='utf-8').write(s); print('ok')
