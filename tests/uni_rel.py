import re,json,html,sys
F=sys.argv[1] if len(sys.argv)>1 else '/home/claude/work/index.html'
s=open(F,encoding='utf-8').read()
d=json.loads(re.search(r'<script type="application/json" id="mvMapData">(.*?)</script>',s,re.S).group(1))
U=d['universi']
cards=[]
for m in re.finditer(r'<li class="card-wrap" id="item-(\d+)"([^>]*)>(.*?)</li>\s*(?=<li class="card-wrap"|</ul>|<h3|</div>)',s,re.S):
    cid=m.group(1); uni=re.search(r'data-uni="([^"]*)"',m.group(2)); body=m.group(3)
    uv=re.search(r'<span class="detail-k">UNIVERSO</span><span class="detail-v">(.*?)</span>',body,re.S)
    t=re.search(r'class="title">(.*?)</span>',body,re.S)
    cards.append((cid,html.unescape(re.sub(r'<[^>]+>','',t.group(1))).strip() if t else '?',(uni.group(1) if uni else '').split(),html.unescape(uv.group(1)).strip() if uv else None))
print(len(cards))
multi=[c for c in cards if len(c[2])>1]
print('card con UNIVERSO dichiarato:',sum(1 for c in cards if c[3]),'/',len(cards))
for c in multi: print(c[0],c[1],'| attr',c[2],'| UNIVERSO:',c[3])
print('--- card senza UNIVERSO dichiarato:',[(c[0],c[1][:20],c[2]) for c in cards if not c[3]][:30])
