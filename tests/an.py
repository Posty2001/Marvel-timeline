import re,json,collections
s=open('/home/claude/work/index.html',encoding='utf-8').read()
A=json.loads(re.search(r'id="atlasData">(.*?)</script>',s,re.S).group(1)); mv=json.loads(re.search(r'id="mvMapData">(.*?)</script>',s,re.S).group(1))
res=[]
def ok(n,c,d=''): res.append(c); print('PASS' if c else 'FAIL',n,d)
MAU='uni-marvel-animation-universe-2006-2017'; C=A['conteggi']; P={c['id']:c for c in A['personaggi']}
cnt=collections.Counter(u for a in A['animate'] for u in a['universi'])
ok('schede animate MAU = 13',cnt[MAU]==13,cnt[MAU]); ok('schede animate classificate = 21 / 37',C['schede_animate_classificate']==21 and C['schede_animate_totali']==37)
ok('altre animate invariate (anni 90: 4, anni 80: 3, X-Men 97: 1)',cnt['uni-marvel-productions-universe-anni-90']==4 and cnt['uni-marvel-productions-universe-anni-80']==3 and cnt['uni-x-men-97-verse']==1)
na=next(a for a in A['animate'] if a['id']=='anim-nextavengersheroesof08')
ok('Next Avengers: MAU, base definizione-universo, nota esplicita, nessun collegamento',na['universi']==[MAU] and na['base']=='definizione-universo' and 'non prova di continuità' in na['nota'] and 'propostaNonApplicata' not in na)
for k in ('char-james-rogers','char-torunn'):
    c=P[k]; ok(k+': MAU, base definizione-universo, nessun collegamento narrativo',c['appartenenza']==[MAU] and c['assegnazione']['base']=='definizione-universo' and not c['collegamentiMultiversoMCU'] and not c.get('crossover') and not c.get('incarnazioni'))
ok('pagine MAU invariate = 4 (non alterate dalla scheda animata)',C['pagine_per_universo'][MAU]['pagine']==4)
ok('300 pagine conteggiabili, tutte con almeno un universo',C['pagine_conteggiabili']==300 and C['pagine_conteggiabili_senza_universo']==0 and all(c['appartenenza'] for c in P.values() if c['conta']))
ok('nessun nuovo universo (27)',len(A['universi'])==len(mv['universi'])==27)
ok('conteggio pagine invariato dalle animate: pagine+animate non sommate',C['pagine_uniche']==304 and 'totale_generale' not in C)
print('TOTALE FALLITI',res.count(False))
