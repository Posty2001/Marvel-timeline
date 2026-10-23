#!/usr/bin/env python3
"""Blocco M2.1 (idempotente). Dopo patch_m2.py: periodo narrativo senza anni non sostenuti da fonti ufficiali + posizione cronologica Disney+ separata."""
import re,json
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
# Periodo narrativo (testo; nessuna cifra non sostenuta: il parser delle Cronologie lascia senza anno cio' che non contiene anni)
AMB={
 '075':'New York, otto anni dopo la battaglia di New York (cartello sullo schermo; anno non univoco)',
 '090':'Europa, dopo il Ritorno degli scomparsi (post-Endgame; anno non ufficiale)',
 '093':'New Jersey, post-Endgame (anno non ufficiale)',
 '094':'post-Endgame, dopo WandaVision (anno non ufficiale)',
 '095':'fuori dal tempo (parte dalla fuga di Loki durante la battaglia di New York)',
 '097':'San Francisco/Cina, post-Endgame (anno non ufficiale)',
 '098':'dal 5000 a.C. al presente post-Endgame (anno non ufficiale)',
 '099':'New York, subito dopo Far From Home (anno non ufficiale)',
 '100':'New York, Natale 2024 (indicazione della produzione; non datato sullo schermo)',
 '101':'Londra/Egitto, post-Endgame (anno non ufficiale)',
 '103':'Jersey City, post-Endgame (anno non ufficiale)',
 '104':'spazio/Nuova Asgard, post-Endgame (anno non ufficiale)',
 '105':'Los Angeles, post-Endgame (anno non ufficiale)',
 '108':'Wakanda, post-Endgame (anno non ufficiale)',
 '109':'Regno Quantico, post-Endgame (anno non ufficiale)',
 '110':'spazio, dopo Love and Thunder e il Holiday Special (anno non ufficiale)',
 '111':'globale, post-Endgame (anno non ufficiale)',
}
# Posizione cronologica: ordine della lista "Marvel Cinematic Universe timeline in chronological order" (marvel.com, Disney+), titoli dopo Endgame. Ordine, non data.
# nota: l'elenco ufficiale e': Loki, What If, WandaVision, Falcon&WS, Shang-Chi, Eternals, Doctor Strange 2, Hawkeye, Moon Knight, Wakanda Forever, She-Hulk, Ms. Marvel, Love and Thunder, Werewolf, Holiday, Quantumania, GotG3, Secret Invasion
POS=['095','096','093','094','097','098','102','100','101','108','105','103','104','106','107','109','110','111']
j=re.search(r'(<script type="application/json" id="atlasData">)(.*?)(</script>)',s,re.S); atl=json.loads(j.group(2))
for o in atl['opere']:
    if o['id'] in AMB: o['ambientazione']=AMB[o['id']]
    if o['id'] in POS: o['posizioneDisney']={'n':POS.index(o['id'])+1,'su':len(POS),'fonte':'marvel.com — MCU timeline Disney+ (ordine, non data)'}
s=s[:j.start(2)]+json.dumps(atl,separators=(',',':'),ensure_ascii=False)+s[j.end(2):]
def li(n,fn):
    global s
    m=re.search(r'<li class="card-wrap" id="item-%s".*?</li>'%n,s,re.S); s=s[:m.start()]+fn(m.group(0))+s[m.end():]
for n,txt in AMB.items():
    li(n,lambda t:re.sub(r'(AMBIENTAZIONE</[^>]+>\s*<[^>]+>)(.*?)(<)',lambda m:m.group(1)+txt.replace('&','&amp;')+m.group(3),t,count=1,flags=re.S))
for k,n in enumerate(POS):
    row='<div class="detail-row lvl-light"><span class="detail-k">POSIZIONE CRONOLOGICA</span><span class="detail-v">n. %d su %d tra i titoli dopo Endgame nella timeline Disney+ (ordine, non data)</span></div>'%(k+1,len(POS))
    def f(t,row=row):
        t=re.sub(r'<div class="detail-row[^"]*"><span class="detail-k">POSIZIONE CRONOLOGICA</span>.*?</div>','',t,count=1,flags=re.S)
        i=t.index('AMBIENTAZIONE'); e=t.index('</div>',i)+6
        return t[:e]+row+t[e:]
    li(n,f)
s=s.replace('20261023-0100-m2','20261023-0600-m21')
open(P,'w',encoding='utf-8').write(s)
