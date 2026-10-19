import re,json,collections
S=open('/home/claude/work/index.html',encoding='utf-8').read()
res=[]
def ok(n,c,d=''): res.append(bool(c)); print('PASS' if c else 'FAIL',n,d)
ids=re.findall(r'\bid="([^"]+)"',S)
dup=[k for k,v in collections.Counter(ids).items() if v>1]
ok('nessun id duplicato nel DOM',not dup,dup[:5])
items=set(re.findall(r'<li class="card-wrap[^"]*" id="item-(\d+)"',S)); ok('139 li item (138 + variante)',len(items)==139 and '133' in items)
checks=set(re.findall(r'<input type="checkbox" class="watch-check" data-item="(\d+)"',S)); ok('138 watch-check, senza 133',len(checks)==138 and '133' not in checks)
refs=set(re.findall(r'href="#item-(\d+)"',S))|set(re.findall(r"item-(\d{3})",S)); 
ok('ogni riferimento item-NNN esiste',all(r in items for r in refs),[r for r in refs if r not in items])
W=json.loads(re.search(r'var WATCH_ORDER_JS = (\[.*?\]);',S).group(1)); ok('WATCH_ORDER_JS = 138 id = watch-check',{e['id'] for e in W}==checks and len(W)==138)
alt=json.loads(re.search(r'id="altTimelineData">(.*?)</script>',S,re.S).group(1)); ok('altTimelineData = 138 e ogni voce ha una scheda',{'%03d'%x['num'] for x in alt}==checks)
mv=json.loads(re.search(r'id="mvMapData">(.*?)</script>',S,re.S).group(1))
allm=set(); bad=[]
for u,d in mv['universi'].items():
    for i in d.get('titoliIds',[]):
        allm.add(i); 
        if i not in checks: bad.append((u,i))
ok('mvMapData: tutti i titoliIds sono titoli autonomi esistenti',not bad,bad[:4])
at=json.loads(re.search(r'id="atlasData">(.*?)</script>',S,re.S).group(1))
ok('atlasData.opere: 139 voci, 133 = variante di 089',len(at['opere'])==139 and [o for o in at['opere'] if o['id']=='133'][0]['variantDi']=='089')
ok('atlasData: tutte le opere hanno una scheda',{o['id'] for o in at['opere']}==items)
ok('atlasData: 27 universi con natura',len(at['universi'])==27 and all(u.get('natura') for u in at['universi']))
# riferimenti N° nelle pagine Atlante
rec=dict(re.findall(r'<li class="card-wrap[^"]*" id="item-(\d+)"(?:(?!</li>).)*?<span class="rec">N&deg;(\d+)</span>',S,re.S))
vis=set(rec.values()); nref=set(re.findall(r'N&deg;(\d{3})\b',S))|set(re.findall(r'N°(\d{3})\b',S))
miss=sorted(n for n in nref if n not in vis and n!='133')
ok('tutti i N° citati nel testo esistono come numero visibile',not miss,miss[:10])
ok('N°133 non citato come scheda autonoma fuori dalla variante',len(re.findall(r'N&deg;133|N°133',S))<=3,re.findall(r'.{40}N&deg;133.{30}',S)[:3])
bo=json.loads(re.search(r'id="bollettinoPool">(.*?)</script>',S,re.S).group(1))
ok('bollettino: ogni "num" punta a una scheda esistente',all(('%03d'%x['num']) in items for x in bo if 'num' in x))
print('TOTALE',len(res),'FALLITI',[i for i,x in enumerate(res) if not x])
