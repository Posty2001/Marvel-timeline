import re
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def sub(old,new,cnt=1):
    global s
    assert s.count(old)==cnt,(old[:70],s.count(old)); s=s.replace(old,new)

# 1) variabili safe-area (unica fonte) + altezza barra
sub("""  --accent-green: #2c5a3e;
}""","""  --accent-green: #2c5a3e;
  /* Safe area iOS (notch / Dynamic Island / home indicator). In Safari con barre visibili i valori sono 0;
     in modalita' standalone (PWA, status bar translucida) sat e' l'altezza di barra di stato + isola. */
  --sat: env(safe-area-inset-top, 0px);
  --sab: env(safe-area-inset-bottom, 0px);
  --sal: env(safe-area-inset-left, 0px);
  --sar: env(safe-area-inset-right, 0px);
  --tabbar-h: calc(3.25rem + var(--sab));
}""")
# 2) html: niente auto-ingrandimento del testo, niente zoom da doppio tap (il pinch resta attivo)
sub("html { scroll-behavior: smooth; background: var(--paper); }","html { scroll-behavior: smooth; background: var(--paper); -webkit-text-size-adjust: 100%; text-size-adjust: 100%; touch-action: manipulation; }")
# 3) body
sub("""  line-height: 1.5;
  padding-bottom: 8.5rem;
}""","""  line-height: 1.5;
  padding-bottom: calc(var(--tabbar-h) + 2.5rem);
  padding-left: var(--sal); padding-right: var(--sar);
  touch-action: manipulation;
}""")
# 4) barra inferiore ridisegnata
a=s.index('.app-tabbar {\n  position: fixed;'); b=s.index('.skip-link {')
s=s[:a]+""".app-tabbar {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 270;
  display: flex; align-items: stretch; justify-content: stretch;
  box-sizing: border-box; height: var(--tabbar-h);
  padding: 0 var(--sar) var(--sab) var(--sal);
  background: rgba(15,13,10,0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(239,228,201,0.14);
  box-shadow: 0 -2px 12px rgba(0,0,0,0.25);
  transform: translateZ(0); -webkit-transform: translateZ(0); will-change: transform;
}
"""+s[b:]
a=s.index('.app-tab {\n  display: flex;'); b=s.index('@media (min-width: 700px) {\n  .app-tabbar {')
s=s[:a]+""".app-tab {
  position: relative; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.2rem;
  flex: 1 1 0; min-width: 0; margin: 0; padding: 0.3rem 0.1rem;
  cursor: pointer; text-decoration: none; background: none; border: none; border-radius: 0;
  font-family: 'IBM Plex Mono', monospace; color: rgba(239,228,201,0.55);
  -webkit-tap-highlight-color: transparent; touch-action: manipulation;
  transition: color 0.15s, background 0.15s;
}
.app-tab-ic { width: 1.45rem; height: 1.45rem; flex-shrink: 0; }
.app-tab-lbl { font-size: 0.6rem; letter-spacing: 0; line-height: 1; white-space: nowrap; max-width: 100%; }
@media (min-width: 375px) { .app-tab-lbl { font-size: 0.64rem; letter-spacing: 0.02em; } }
@media (min-width: 420px) { .app-tab-lbl { font-size: 0.68rem; } }
.app-tab:hover, .app-tab:active { color: #efe4c9; background: rgba(239,228,201,0.06); }
.app-tab.app-tab-active { color: var(--marvel-red); background: rgba(200,39,42,0.10); }
.app-tab.app-tab-active::before {
  content: ""; position: absolute; top: 0; left: 28%; right: 28%; height: 2px; border-radius: 0 0 2px 2px; background: var(--marvel-red);
}
"""+s[b:]
# 5) intro / onboarding: safe area + centratura "sicura" (il contenuto alto non viene piu' tagliato in cima)
sub("""  background: #0f0d0a; color: #efe4c9; overflow-y: auto; text-align: center;
  padding: 2rem 1.5rem; z-index: 250;
}""","""  background: #0f0d0a; color: #efe4c9; overflow-y: auto; text-align: center;
  padding: 2rem 1.5rem; z-index: 250;
  align-items: flex-start; box-sizing: border-box;
  padding: calc(2rem + var(--sat)) calc(1.5rem + var(--sar)) calc(2rem + var(--sab)) calc(1.5rem + var(--sal));
}""")
sub("""  background: #0f0d0a; color: #efe4c9; overflow-y: auto; text-align: center;
  padding: 2rem 1.5rem; z-index: 600;
}""","""  background: #0f0d0a; color: #efe4c9; overflow-y: auto; text-align: center;
  padding: 2rem 1.5rem; z-index: 600;
  align-items: flex-start; box-sizing: border-box;
  padding: calc(2rem + var(--sat)) calc(1.5rem + var(--sar)) calc(2rem + var(--sab)) calc(1.5rem + var(--sal));
}""")
sub(".onboarding-content { position: relative; z-index: 2; max-width: 520px; }",".onboarding-content { position: relative; z-index: 2; max-width: 520px; margin-top: auto; margin-bottom: auto; }")
sub(".intro-content { position: relative; z-index: 2; max-width: 640px; }",".intro-content { position: relative; z-index: 2; max-width: 640px; margin-top: auto; margin-bottom: auto; }")
# 6) home hub
sub("""  padding: 2.5rem 1.5rem; text-align: center; box-sizing: border-box;
}""","""  padding: calc(2.5rem + var(--sat)) calc(1.5rem + var(--sar)) calc(var(--tabbar-h) + 1.5rem) calc(1.5rem + var(--sal));
  text-align: center; box-sizing: border-box;
}""")
# 7) overlay a schermo intero
sub("""  overflow-y: auto; -webkit-overflow-scrolling: touch;
  padding-bottom: calc(6rem + env(safe-area-inset-bottom, 0px));
  box-sizing: border-box;""","""  overflow-y: auto; -webkit-overflow-scrolling: touch;
  padding-top: var(--sat);
  padding-bottom: calc(var(--tabbar-h) + 1.5rem);
  padding-left: var(--sal); padding-right: var(--sar);
  box-sizing: border-box;""")
sub("""  min-height: 100vh; min-height: 100dvh; background: #0f0d0a; color: #efe4c9;
  padding-bottom: calc(6rem + env(safe-area-inset-bottom, 0px));
  box-sizing: border-box;""","""  min-height: 100vh; min-height: 100dvh; background: #0f0d0a; color: #efe4c9;
  padding-top: var(--sat);
  padding-bottom: calc(var(--tabbar-h) + 1.5rem);
  box-sizing: border-box;""")
# Database/Atlante: sfondo carta -> l'inset superiore va nell'intestazione scura, non come striscia chiara
sub(".tva-archives-overlay { background: var(--paper) !important; color: var(--ink); }",".tva-archives-overlay { background: var(--paper) !important; color: var(--ink); padding-top: 0; }\n.tva-archives-overlay .mg-header { padding-top: calc(1.4rem + var(--sat)); }")
# 8) hero e timbro (Timeline)
sub("  padding: 4.5rem 1.5rem 3rem;\n  max-width: 900px;","  padding: max(4.5rem, calc(var(--sat) + 1.5rem)) 1.5rem 3rem;\n  max-width: 900px;")
sub("  position: absolute;\n  top: 2.2rem;\n  right: 2rem;","  position: absolute;\n  top: max(2.2rem, calc(var(--sat) + 0.8rem));\n  right: 2rem;")
# 9) banner sticky universo
sub("  box-shadow: 0 2px 10px rgba(0,0,0,0.25);\n}\n.mv-universo-banner[hidden]","  box-shadow: 0 2px 10px rgba(0,0,0,0.25);\n  padding-top: calc(0.7rem + var(--sat));\n}\n.mv-universo-banner[hidden]")
# 10) player locale, toast, dialoghi
sub(".lv-header { padding: 0.9rem 1rem; flex-shrink: 0; }",".lv-header { padding: calc(0.9rem + var(--sat)) calc(1rem + var(--sar)) 0.9rem calc(1rem + var(--sal)); flex-shrink: 0; }")
sub("  position: fixed; left: 50%; bottom: 1.5rem; transform: translateX(-50%);\n  background: var(--ink);","  position: fixed; left: 50%; bottom: calc(var(--tabbar-h) + 0.8rem); transform: translateX(-50%);\n  background: var(--ink);")
sub("  position: fixed; inset: 0; z-index: 500; background: rgba(15,13,10,0.75);\n  display: flex; align-items: center; justify-content: center; padding: 1.2rem;","  position: fixed; inset: 0; z-index: 500; background: rgba(15,13,10,0.75);\n  display: flex; align-items: center; justify-content: center; padding: calc(1.2rem + var(--sat)) calc(1.2rem + var(--sar)) calc(1.2rem + var(--sab)) calc(1.2rem + var(--sal));")
sub("  background: rgba(10,8,5,0.82); padding: 1.2rem; backdrop-filter: blur(3px);","  background: rgba(10,8,5,0.82); padding: calc(1.2rem + var(--sat)) calc(1.2rem + var(--sar)) calc(1.2rem + var(--sab)) calc(1.2rem + var(--sal)); backdrop-filter: blur(3px);")
# 11) strato finale iOS
blk="""
/* ================= iOS: stabilita' tipo app nativa =================
   - Striscia di sicurezza in alto: in standalone (status bar translucida) nulla scorre sotto orologio/Dynamic Island
     e le icone bianche della status bar restano leggibili anche sulle schermate chiare. Con sat=0 (Safari) non esiste.
   - Zoom: NESSUN user-scalable=no / maximum-scale: il pinch resta disponibile (accessibilita'). Si eliminano solo le
     cause involontarie: doppio tap (touch-action: manipulation) e auto-zoom al focus dei campi (<16px) su touch. */
body::before {
  content: ""; position: fixed; top: 0; left: 0; right: 0; height: var(--sat);
  background: #0f0d0a; z-index: 650; pointer-events: none;
}
a, button, label, summary, input, select, textarea, [role="button"] { touch-action: manipulation; }
@media (hover: none) and (pointer: coarse) {
  input:not([type="checkbox"]):not([type="radio"]):not([type="range"]):not([type="file"]):not([type="hidden"]):not([type="button"]):not([type="submit"]):not([type="reset"]),
  select, textarea { font-size: 16px !important; }
}
"""
i=s.index('</style>'); s=s[:i]+blk+s[i:]
open(P,'w',encoding='utf-8').write(s); print('ok')
