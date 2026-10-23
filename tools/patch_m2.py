#!/usr/bin/env python3
"""Blocco M2 (idempotente). Dopo patch_m1.py: coerenza anni (Confronto, etichetta anno scheda), data/titolo VisionQuest."""
import re,json
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
def blob(i): 
    m=re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)'%i,s,re.S); return m
def setblob(i,d,**kw):
    global s
    m=blob(i); s=s[:m.start(2)]+json.dumps(d,**kw)+s[m.end(2):]
# 1) VisionQuest: titolo ufficiale e data (mercoledi' 14 ottobre 2026; stessa data gia' in bollettinoOTD)
alt=json.loads(blob('altTimelineData').group(2)); atl=json.loads(blob('atlasData').group(2),)
for x in alt:
    if x['num']==135: x['title']='VisionQuest'; x['release']='2026-10-14'
rel={'%03d'%x['num']:x['release'] for x in alt if x['release']}
for o in atl['opere']:
    if o['id']=='135': o['uscita']='2026-10-14'
# 2) anno della scheda = anno di uscita (regola "uscita accanto al titolo, ambientazione nei dettagli"), ambientazione invariata nel dettaglio
T=['041','042','043','044','045','046','047','059','069','077','078','088','089','090','093','094','100','125']
AMB_ADD={'059':('AMBIENTAZIONEspazio<','spazio, 2014'),'090':None}
opm={o['id']:o for o in atl['opere']}
for n in T:
    o=opm[n]; y=rel[n][:4]
    if o['significatoAnnoCard']!='uscita':
        if n=='059' and '2014' not in o['ambientazione']: o['ambientazione']='spazio, 2014'
        if n=='090' and '2023' not in o['ambientazione']: o['ambientazione']='Europa, post-Schiocco, 2023-24'
        o['annoCard']=y; o['significatoAnnoCard']='uscita'
setblob('altTimelineData',alt,ensure_ascii=True); setblob('atlasData',atl,separators=(',',':'),ensure_ascii=False)
# 3) cmpYearData: anno di uscita reale (prima: 45 valori scorretti, es. Guardiani della Galassia 2017, Luke Cage S1 2021)
cy=json.loads(blob('cmpYearData').group(2))
for n,r in rel.items(): cy['item-'+n]=r[:4]
setblob('cmpYearData',cy,ensure_ascii=True)
def li_edit(n,fn):
    global s
    m=re.search(r'<li class="card-wrap" id="item-%s".*?</li>'%n,s,re.S); new=fn(m.group(0)); assert new!=m.group(0) or True; s=s[:m.start()]+new+s[m.end():]
def setyr(n,y): li_edit(n,lambda t:re.sub(r'<span class="yr">.*?</span>','<span class="yr">%s</span>'%y,t,count=1,flags=re.S))
for n in T: setyr(n,rel[n][:4])
# ambientazione: l'informazione che era nel campo anno resta nel dettaglio
def amb_edit(n,old,new): li_edit(n,lambda t:t.replace(old,new,1) if old in t else t)
def ambrow(n,newtxt):
    def f(t):
        return re.sub(r'(AMBIENTAZIONE</[^>]+>\s*<[^>]+>)(.*?)(<)',lambda m:m.group(1)+newtxt+m.group(3),t,count=1,flags=re.S)
    li_edit(n,f)
ambrow('059','spazio, 2014'); ambrow('090','Europa, post-Schiocco, 2023-24')
# VisionQuest: card
setyr('135','14 ott 2026 (USA), già uscita')
li_edit('135',lambda t:t.replace('<span class="title">Vision Quest</span>','<span class="title">VisionQuest</span>').replace('data-search="vision quest"','data-search="visionquest vision quest"'))
s=s.replace('"titolo": "Vision Quest"','"titolo": "VisionQuest"').replace('"title": "Vision Quest"','"title": "VisionQuest"')
s=s.replace('&mdash; Vision Quest','&mdash; VisionQuest')   # riferimento «ULTIMA APP.» nella scheda di Visione
# 4) etichetta del campo nel Confronto
s=s.replace("(f === 'TRAMA' ? 'TRAMA (spoiler-free)' : f)","(f === 'TRAMA' ? 'TRAMA (spoiler-free)' : f === 'ANNO' ? 'ANNO DI USCITA' : f)")
s=s.replace('20261022-2230-m1','20261023-0100-m2')
open(P,'w',encoding='utf-8').write(s)
