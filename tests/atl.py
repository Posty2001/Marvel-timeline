import re,sys,json,html
p=sys.argv[1]
s=open(p,encoding='utf-8').read()
# 1 letter groups
bad=0
for m in re.finditer(r'<details class="letter-group" id="letter-(\w)">\s*<summary class="letter-summary"><span class="char-letter">\w</span><span class="letter-count">(\d+) personaggi</span>.*?</details>(?=<details class="letter-group"|\s*</details>)',s,re.S):
    n=len(re.findall(r'<li class="card-wrap" id="char-',m.group(0)))
    if n!=int(m.group(2)): print('LETTER MISMATCH',m.group(1),m.group(2),n); bad+=1
chars=re.findall(r'<li class="card-wrap" id="(char-[^"]+)"',s)
print('char pages',len(chars),'dups',len(chars)-len(set(chars)))
# 2 mvNavigate targets
allids=set(re.findall(r'\bid="([^"]+)"',s))
tg=set(re.findall(r"mvNavigate\('([^']+)'",s))
print('dead mvNavigate',sorted(t for t in tg if t not in allids))
# 3 graph nodes
gm=re.search(r'"char-[a-z0-9-]+": \{"type": "char", "name": ".*?", "conns"',s)
# find big graph dict: locate first node key
i=s.find('"char-edwin-jarvis": {"type": "char"')
# walk back to dict start
st=s.rfind('{"',0,i-1)
# simpler: collect all node keys with conns
nodes=dict()
for m in re.finditer(r'"((?:char|att|org|uni|universo|ev)[a-z0-9-]*)": \{"type": "(\w+)", "name": "([^"]*)", "conns": \[',s):
    nodes[m.group(1)]=m.start()
print('graph nodes',len(nodes))
conn_ids=set(re.findall(r'\{"id": "([^"]+)", "type": "\w+", "name": "[^"]*", "label"',s))
print('conn ids not nodes',sorted(c for c in conn_ids if c not in nodes)[:20], len([c for c in conn_ids if c not in nodes]))
print('char pages without node',[c for c in chars if c not in nodes][:20])
print('nodes char- without page',[n for n in nodes if n.startswith('char-') and n not in chars][:20])
# 4 options vs pages
sel=re.findall(r'<option value="([^"]*)">',s)
# name map
nm=re.search(r'"Edwin Jarvis": "char-edwin-jarvis"',s)
names=re.findall(r'"([^"]+)": "(char-[a-z0-9-]+)"',s)
nmap=dict(names)
print('name map entries',len(nmap),'dead',[v for v in nmap.values() if v not in chars])
titles={}
for c in chars:
    i=s.find('id="%s"'%c); t=re.search(r'class="title">(.*?)</span>',s[i:i+600]).group(1); titles[c]=html.unescape(t)
missing=[t for t in titles.values() if t not in nmap]
print('page titles not in name map',missing[:10],len(missing))
opts=set(html.unescape(o) for o in sel)
print('page titles not in options',[t for t in titles.values() if t not in opts][:10])
# 5 uni stats
for m in re.finditer(r'"(uni-[a-z0-9-]+)": \{"nome": "([^"]*)","titoli": (\d+),"personaggi": (\d+)',s):
    pass
print('done')
