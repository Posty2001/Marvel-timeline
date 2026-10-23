#!/usr/bin/env python3
"""Sincronizza ID TMDB e poster_path dei titoli del catalogo -> assets/images/catalog/tmdb_map.json.
La chiave NON va nel codice: esporta TMDB_READ_TOKEN (token v4, consigliato) oppure TMDB_API_KEY (v3) nella tua shell.
  python3 tools/tmdb_sync.py            # sincronizza, scrive tmdb_map.json e tmdb_review.json (titoli non risolti)
  python3 tools/tmdb_sync.py --dry      # non scrive
Regole: nessun abbinamento a caso. Accetta solo corrispondenza esatta del titolo normalizzato (film: anno di uscita +-1);
tutto il resto va in tmdb_review.json e si risolve in tmdb_overrides.json. Poi: bash tools/build_4.sh."""
import os,re,json,sys,time,unicodedata,urllib.request,urllib.parse,urllib.error
R=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D=R+'/assets/images/catalog/'
def norm(x): x=unicodedata.normalize('NFD',x.lower()); x=''.join(c for c in x if not unicodedata.combining(c)); return re.sub(r'[^a-z0-9]+',' ',x).strip()
def api(path,**q):
    h={'Accept':'application/json'}; tok=os.environ.get('TMDB_READ_TOKEN'); key=os.environ.get('TMDB_API_KEY')
    if tok: h['Authorization']='Bearer '+tok
    elif key: q['api_key']=key
    else: sys.exit('Imposta TMDB_READ_TOKEN o TMDB_API_KEY (non salvarli nel repository).')
    q.setdefault('language','it-IT')
    req=urllib.request.Request('https://api.themoviedb.org/3'+path+'?'+urllib.parse.urlencode(q),headers=h)
    for tent in range(4):
        try:
            with urllib.request.urlopen(req,timeout=20) as r: return json.load(r)
        except urllib.error.HTTPError as e:   # mai stampare URL o intestazioni: possono contenere la chiave
            if e.code==429 and tent<3: time.sleep(2+3*tent); continue
            if e.code in (401,403): sys.exit('TMDB: credenziali rifiutate (HTTP %d). Controlla il secret.'%e.code)
            if e.code==404: return {}
            sys.exit('TMDB: errore HTTP %d su %s'%(e.code,path))
        except Exception as e:
            if tent<3: time.sleep(2); continue
            sys.exit('TMDB: rete non raggiungibile (%s)'%type(e).__name__)
def catalogo():
    s=open(R+'/index.html',encoding='utf-8').read()
    a={o['id']:o for o in json.loads(re.search(r'id="atlasData">(.*?)</script>',s,re.S).group(1))['opere']}
    out=[]
    for num,t,yr in re.findall(r'<li class="card-wrap" id="item-(\d+)".*?<span class="title">(.*?)</span> <span class="yr">(.*?)</span>',s,re.S):
        o=a.get(num,{}); out.append((num,re.sub(r'<[^>]+>','',t).replace('&amp;','&').strip(),yr,o.get('tipo','film')))
    return out
def risolvi(num,titolo,yr,tipo):
    m=re.search(r'\s+S(\d+)$',titolo); season=int(m.group(1)) if m else None; base=titolo[:m.start()] if m else titolo
    kinds=['movie'] if tipo=='film' else ['tv'] if tipo=='serie' else ['movie','tv']
    cand=[]
    for k in kinds:
        q={'query':base}
        if k=='movie' and yr.isdigit(): q['year']=yr
        res=api('/search/'+k,**q).get('results',[])
        if not res: res=api('/search/'+k,**dict(q,language='en-US')).get('results',[])
        for r in res:
            nm=r.get('title') or r.get('name') or ''; on=r.get('original_title') or r.get('original_name') or ''
            if norm(base) in (norm(nm),norm(on)):
                y=(r.get('release_date') or r.get('first_air_date') or '')[:4]
                if k=='movie' and yr.isdigit() and y.isdigit() and abs(int(y)-int(yr))>1: continue
                cand.append((k,r['id'],nm,y,(r.get('overview') or '')[:90]))
    return (cand[0][:2]+(season,)) if len(cand)==1 else (None,cand,season)
def poster(t,i,s):
    if t=='tv' and s:
        p=api('/tv/%d/season/%d'%(i,s)).get('poster_path')
        if p: return p
    return api('/%s/%d'%(t,i)).get('poster_path')
def main():
    dry='--dry' in sys.argv; os.makedirs(D,exist_ok=True); ov=json.load(open(D+'tmdb_overrides.json'))['voci'] if os.path.exists(D+'tmdb_overrides.json') else {}; mp={}; rev=[]
    for num,tit,yr,tipo in catalogo():
        o=ov.get(num)
        if o and o.get('skip'): continue
        if o: t,i,s=o['t'],o['id'],o.get('s')
        else:
            r=risolvi(num,tit,yr,tipo)
            if r[0] is None: rev.append({'id':num,'titolo':tit,'anno':yr,'tipo':tipo,'candidati':r[1]}); continue
            t,i,s=r
        p=poster(t,i,s)
        if not p or not re.match(r'^/[A-Za-z0-9_-]+\.(jpg|png)$',p): rev.append({'id':num,'titolo':tit,'anno':yr,'tipo':tipo,'motivo':'poster assente'}); continue
        mp[num]={'t':t,'id':i,'p':p}; 
        if s: mp[num]['s']=s
    print('risolti',len(mp),'da rivedere',len(rev))
    if os.environ.get('GITHUB_STEP_SUMMARY'): open(os.environ['GITHUB_STEP_SUMMARY'],'a').write('### TMDB sync\n- Titoli abbinati: %d\n- Da rivedere: %d\n'%(len(mp),len(rev)))
    if not dry:
        json.dump({'versione':1,'voci':dict(sorted(mp.items()))},open(D+'tmdb_map.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        json.dump(rev,open(D+'tmdb_review.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
if __name__=='__main__': main()
