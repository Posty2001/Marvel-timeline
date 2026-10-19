import re,json,collections
s=open('/home/claude/work/index.html',encoding='utf-8').read()
A=json.loads(re.search(r'id="atlasData">(.*?)</script>',s,re.S).group(1))
res=[]
def ok(n,c,d=''): res.append(c); print('PASS' if c else 'FAIL',n,d)
P=A['personaggi']; cont=[c for c in P if c['conta']]; I=A['conteggi']['incarnazioni']
pairs=[(c['id'],i['id']) for c in P for i in c.get('incarnazioni',[])]
ok('nessun doppio conteggio: coppie (pagina,incarnazione) uniche',len(pairs)==len(set(pairs)),[k for k,v in collections.Counter(pairs).items() if v>1])
ok('vecchio contatore ambiguo assente','incarnazioni_documentate' not in A['conteggi'])
ver=sum(1 for c in cont for i in c.get('incarnazioni',[]) if i['stato']=='verificata'); nv=sum(1 for c in cont for i in c.get('incarnazioni',[]) if i['stato']!='verificata')
ok('incarnazioni verificate = ricalcolo',I['incarnazioni_verificate']==ver,(I['incarnazioni_verificate'],ver))
ok('incarnazioni non verificate = ricalcolo',I['incarnazioni_non_verificate']==nv,(I['incarnazioni_non_verificate'],nv))
ok('pagine con incarnazioni = ricalcolo',I['pagine_con_incarnazioni']==sum(1 for c in cont if c.get('incarnazioni')))
ok('identità narrative = len(identita) e id unici',I['identita_narrative']==len(A['identita'])==len({i['id'] for i in A['identita']}))
ok('ogni incarnazione ha stato esplicito',all(i.get('stato') in ('verificata','non-verificato') for c in P for i in c.get('incarnazioni',[])))
ok('incarnazioni non verificate senza universi (non contano come appartenenza)',all(not i['universi'] for c in P for i in c.get('incarnazioni',[]) if i['stato']!='verificata'))
ok('universi delle verificate ⊆ appartenenza',all(set(i['universi'])<=set(c['appartenenza']) for c in cont for i in c.get('incarnazioni',[]) if i['stato']=='verificata'))
ok('aggregate: ≥2 incarnazioni',all(len(c['incarnazioni'])>=2 for c in P if c['tipo']=='aggregata'))
ids={c['id'] for c in P}; ok('identità: pagine esistenti, senza duplicati',all(p in ids for i in A['identita'] for p in i['pagine']) and all(len(i['pagine'])==len(set(i['pagine'])) for i in A['identita']))
print('valori:',I)
print('TOTALE FALLITI',res.count(False))
