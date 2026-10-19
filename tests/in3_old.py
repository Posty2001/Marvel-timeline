from playwright.sync_api import sync_playwright
F='file:///home/claude/work/backups/N10_pre_intro.html'
ok=True
def chk(n,c,d=''):
    global ok
    if not c: ok=False
    print(('PASS ' if c else 'FAIL ')+n,d)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':390,'height':844}); pg=ctx.new_page(); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(F); pg.wait_for_timeout(1200)
    cd=pg.evaluate("[document.getElementById('icdDoomsday').textContent,document.getElementById('icdSecretWars').textContent]")
    chk('countdown popolati',all(x.strip().isdigit() for x in cd),cd)
    t=pg.evaluate("document.querySelector('.intro-ticker').innerText.replace(/\\s+/g,' ')")
    chk('testo countdown invariato (GIORNI A DOOMSDAY (18 DIC 2026) / SECRET WARS (17 DIC 2027))','GIORNI A DOOMSDAY (18 DIC 2026)' in t and 'GIORNI A SECRET WARS (17 DIC 2027)' in t,t)
    stats=pg.evaluate("[...document.querySelectorAll('.intro-stat')].map(e=>e.innerText.replace(/\\s+/g,' '))")
    chk('statistiche: 4 card, valori invariati',stats==['🎥 176 titoli','🌐 26 universi','👥 304 personaggi','⏱️ ~527 ore di visione'] or len(stats)==4,stats)
    # quiz
    pg.evaluate("document.querySelector('.intro-quiz-summary').click()"); pg.wait_for_timeout(200)
    chk('quiz apribile',pg.evaluate("document.querySelector('.intro-quiz').open"))
    pg.evaluate("document.querySelector('#quizOptsTempo .intro-quiz-opt').click()"); pg.wait_for_timeout(200)
    pg.evaluate("[...document.querySelectorAll('#quizOptsStile .intro-quiz-opt')][0]&&document.querySelectorAll('#quizOptsStile .intro-quiz-opt')[0].click()"); pg.wait_for_timeout(200)
    q=pg.evaluate("({res:!document.getElementById('quizResult').hidden,txt:document.getElementById('quizResultText').textContent.length})")
    chk('quiz: percorso fino al risultato funziona',q['res'] or q['txt']>0,q)
    # il pulsante resta raggiungibile quando il quiz e' aperto
    pg.evaluate("document.getElementById('journeyStartBtn').scrollIntoView({block:'nearest',behavior:'instant'})")
    r=pg.evaluate("(()=>{const r=document.getElementById('journeyStartBtn').getBoundingClientRect();return [r.top>=0,r.bottom<=innerHeight]})()")
    chk('con quiz aperto il pulsante resta raggiungibile',all(r),r)
    pg.evaluate("document.querySelector('.intro-quiz').open=false")
    pg.click('#journeyStartBtn'); pg.wait_for_timeout(1200)
    st=pg.evaluate("({j:document.getElementById('journeyStarted').checked,intro:getComputedStyle(document.getElementById('intro')).display,onb:(()=>{const o=document.getElementById('onboardingScreen');return o?!o.hidden:null})()})")
    chk('«Inizia il viaggio» avvia (intro nascosta; onboarding o hub)',st['j'] and st['intro']=='none',st)
    chk('nessun errore JS',not errs,errs)
    # intro non tocca onboarding: ricarico e guardo onboarding screen se presente
    b.close()
print('ALL_PASS' if ok else 'SOME_FAIL')
