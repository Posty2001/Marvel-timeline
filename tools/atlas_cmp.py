import atlas_lib as L,json,re,collections
s,mv,fam,works,anim,chars=L.load('/home/claude/work/index.html')
AD=json.loads(re.search(r'id="atlasData">(.*?)</script>',s,re.S).group(1))
ok=True
def chk(c,m):
    global ok
    if not c: ok=False; print('FAIL',m)
chk({u['id'] for u in AD['universi']}==set(mv['universi']),'universi')
chk({o['id'] for o in AD['opere']}==set(works) and len(AD['opere'])==139,'opere 139')
chk({a['id'] for a in AD['animate']}==set(anim) and len(AD['animate'])==37,'anim 37')
chk({c['id'] for c in AD['personaggi']}==set(chars) and len(AD['personaggi'])==304,'personaggi 304')
for o in AD['opere']: chk(o['universi']==works[o['id']]['uni'],'data-uni '+o['id'])
for u,x in mv['universi'].items():
    chk(sorted(x['titoliIds'])==sorted(o['id'] for o in AD['opere'] if u in o['universi']) if 'titoliIds' in x else True,'titoliIds '+u)
tit=collections.Counter(len([o for o in AD['opere'] if u in o['universi']]) for u in mv['universi'])
print('titoli per uni: confronto con mvMapData.titoli')
for u,x in mv['universi'].items():
    d=sum(1 for o in AD['opere'] if u in o['universi'])
    if d!=x['titoli']: print('  DIFF titoli',u,x['titoli'],d)
print('--- personaggi: salvato vs derivato(certi) [+dubbi]')
cnt=collections.defaultdict(set);dub=collections.defaultdict(set)
for c in AD['personaggi']:
    if c['stato']=='segnaposto-da-escludere-dai-conteggi': continue
    for u in c['appartenenza']: cnt[u].add(c['id'])
    for u in c['dubbio']: dub[u].add(c['id'])
for u,x in mv['universi'].items():
    if x['personaggi']!=len(cnt[u]): print(f"  DIFF {u}: salvato={x['personaggi']} atlasData={len(cnt[u])} (+{len(dub[u])} dubbi)")
glob=set(c['id'] for c in AD['personaggi'] if c['appartenenza'] and c['stato']!='segnaposto-da-escludere-dai-conteggi')
print('globali unici con almeno un universo:',len(glob),'senza universo:',[c['id'] for c in AD['personaggi'] if not c['appartenenza']])
ov=[c['id'] for c in AD['personaggi'] if c.get('override')]
print('override documentati atlasData vs DOM:',ov)
cn=AD['conteggi']; chk(cn['pagine_uniche']==len(chars)==304,'pagine uniche'); chk(cn['pagine_conteggiabili']==300,'conteggiabili')
chk(cn['pagine_ordinarie']+cn['varianti_con_pagina_autonoma']+cn['pagine_aggregate']==cn['pagine_conteggiabili'],'somma tipologie')
chk(all(c['conta']==(c['tipo']!='segnaposto') for c in AD['personaggi']),'flag conta')
chk(all(len(c['incarnazioni'])>=2 for c in AD['personaggi'] if c['tipo']=='aggregata'),'incarnazioni')
print('OK' if ok else 'ERRORI')
