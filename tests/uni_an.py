import re,json,sys
F=sys.argv[1] if len(sys.argv)>1 else '/home/claude/work/index.html'
s=open(F,encoding='utf-8').read()
d=json.loads(re.search(r'<script type="application/json" id="mvMapData">(.*?)</script>',s,re.S).group(1))
print('chiavi top:',list(d.keys()))
U=d['universi']
cards={}
for m in re.finditer(r'<li class="card-wrap" id="item-(\d+)"([^>]*)>',s):
    attrs=m.group(2); uni=re.search(r'data-uni="([^"]*)"',attrs)
    t=re.search(r'id="item-%s".*?class="title">(.*?)</span>'%m.group(1),s[m.start():m.start()+60000],re.S)
    cards[m.group(1)]=(uni.group(1) if uni else None, re.sub(r'<[^>]+>','',t.group(1)).strip() if t else '?')
print('card',len(cards),'senza data-uni:',[k for k,v in cards.items() if not v[0]])
print('valori data-uni con spazi (multi):',[(k,v[0]) for k,v in cards.items() if v[0] and ' ' in v[0]][:10])
bycard={}
for k,(u,t) in cards.items():
    for x in (u or '').split(): bycard.setdefault(x,[]).append(k)
print('universi in mvMapData:',len(U),'| universi con data-uni nelle card:',len(bycard))
for uid,u in U.items():
    ids=u.get('titoliIds') or []
    c=sorted(bycard.get(uid,[]))
    flag='' if sorted(ids)==c else '  <-- DIFF'
    print(f"{uid:45s} {u['nome'][:34]:34s} titoli={u.get('titoli')} ids={len(ids)} cardAttr={len(c)}{flag}")
print('data-uni nelle card non presenti in mvMapData:',sorted(set(bycard)-set(U)))
