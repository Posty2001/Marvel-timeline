# Patch X-Men: Logan prima di Deadpool e Deadpool 2 (percorso editoriale).
# ID stabili (data-item/id/note/chiavi di salvataggio INVARIATI); cambiano solo posizione nel DOM,
# numero visibile (N°) e i riferimenti testuali / liste ordinate che dipendono dalla posizione.
import re,json,sys
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
MAP={'022':'023','023':'024','024':'022'}   # numero visibile vecchio -> nuovo (Deadpool, Deadpool 2, Logan)
# 1) riferimenti testuali N° (inclusi i <span class="rec">)
cnt=[0]
def rep(m):
    cnt[0]+=1; return m.group(1)+MAP[m.group(2)]
s=re.sub(r'(N&deg;|N°)(02[234])(?!\d)',rep,s)
print('riferimenti N° rimappati:',cnt[0])
# 2) riordino blocchi <li> nel DOM: 022(Dp) 023(Dp2) 024(Logan) -> 024 022 023
def blk(n):
    a=s.index('<li class="card-wrap" id="item-%s"'%n); b=s.index('</li>',a)+5
    assert '<li' not in s[a+5:b], 'li annidato'
    return a,b
a22,b22=blk('022'); a23,b23=blk('023'); a24,b24=blk('024')
assert s[b22:a23].strip()=='' and s[b23:a24].strip()=='', 'blocchi non contigui'
L22,L23,L24=s[a22:b22],s[a23:b23],s[a24:b24]
s=s[:a22]+L24+'\n    '+L22+'\n    '+L23+s[b24:]
# 3) nota editoriale nella scheda di Logan (collegamenti)
old="X-23 (Dafne Keen) riappare in Deadpool &amp; Wolverine; chiude l'arco di Wolverine"
if old not in s: old=old.replace('&amp;','&')
assert s.count(old)==1, s.count(old)
nota=old+". Posizionato prima di Deadpool per scelta editoriale del percorso (arco di Wolverine prima dei film di Deadpool): non indica precedenza cronologica, il film &egrave; ambientato nel 2029"
s=s.replace(old,nota)
# 4) WATCH_ORDER_JS
m=re.search(r'var WATCH_ORDER_JS = (\[.*?\]);\n',s,re.S); W=json.loads(m.group(1))
ids=[x['id'] for x in W]; i=ids.index('022'); assert ids[i:i+3]==['022','023','024']
W[i:i+3]=[W[i+2],W[i],W[i+1]]
s=s[:m.start(1)]+json.dumps(W,ensure_ascii=False)+s[m.end(1):]
# 5) DEPENDENCY_MAP_JS: ordine dei prerequisiti di 117
old='"117": {"ess": ["022", "023", "024", "095"]'; assert s.count(old)==1
s=s.replace(old,'"117": {"ess": ["024", "022", "023", "095"]')
# 6) mvMapData: elenco titoli del Fox-Verse
old='"021", "022", "023", "024", "117"]'; assert s.count(old)==1
s=s.replace(old,'"021", "024", "022", "023", "117"]')
# 7) atlasData.opere (ordine array) e altTimelineData (ordine array)
def reorder_json(s,sid,key,getid):
    m=re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)'%sid,s,re.S)
    raw=m.group(2); D=json.loads(raw)
    arr=D[key] if key else D
    ids=[getid(x) for x in arr]; i=ids.index(getid_target[0]); assert [ids[i],ids[i+1],ids[i+2]]==list(getid_target)
    arr[i:i+3]=[arr[i+2],arr[i],arr[i+1]]
    # serializzazione identica al formato esistente (separatori di json.dumps di default)
    sep=(', ',': ') if ', "' in raw[:200] or '", "' in raw[:200] else (',',':')
    out=json.dumps(D,ensure_ascii=('\\u' in raw),separators=sep)
    return s[:m.start(2)]+out+s[m.end(2):]
getid_target=('022','023','024')
s=reorder_json(s,'atlasData','opere',lambda x:x['id'])
getid_target=(22,23,24)
s=reorder_json(s,'altTimelineData',None,lambda x:x['num'])
open(P,'w',encoding='utf-8').write(s)
print('ok')
