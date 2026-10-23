#!/usr/bin/env python3
"""Registro immagini TVA Archives. Nessuna immagine viene scelta automaticamente.
  list [--kind K] [--missing]     elenca gli ID di catalogo e se hanno un'immagine registrata
  scan                            confronta assets/images/catalog/ con manifest.json (file non registrati / voci senza file / dimensioni)
  register kind:id --licence L --credit C [--src PATH] [--verify]   aggiunge/aggiorna la voce (w/h letti dal file; verified solo con --verify)
Dopo la modifica: bash tools/build_4.sh (il manifest viene incorporato nella build)."""
import json,re,sys,os,argparse
R='/home/claude/work'; MAN=R+'/assets/images/catalog/manifest.json'; DIR=R+'/assets/images/catalog/'
def ids():
    s=open(R+'/index.html',encoding='utf-8').read()
    a=json.loads(re.search(r'id="atlasData">(.*?)</script>',s,re.S).group(1)); out=[]
    out+=[('item',o['id'],o.get('tipo','')) for o in a['opere'] if not str(o['id']).startswith('133')]
    out+=[('anim',o.get('id'),'') for o in a.get('animate',[])]
    out+=[('chr',o['id'],o.get('nome','')) for o in a['personaggi']]
    out+=[('uni',o['id'],o.get('nome','')) for o in a['universi']]
    return out
def load(): return json.load(open(MAN,encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='c'); l=sp.add_parser('list'); l.add_argument('--kind'); l.add_argument('--missing',action='store_true'); sp.add_parser('scan')
    r=sp.add_parser('register'); r.add_argument('key'); r.add_argument('--licence',required=True); r.add_argument('--credit',required=True); r.add_argument('--src'); r.add_argument('--verify',action='store_true')
    A=ap.parse_args(); m=load()
    if A.c=='list':
        for k,i,n in ids():
            if A.kind and k!=A.kind: continue
            has=(k+':'+str(i)) in m['voci']
            if A.missing and has: continue
            print(('OK  ' if has else '--  ')+k+':'+str(i)+'  '+str(n))
    elif A.c=='scan':
        files=sorted(f for f in os.listdir(DIR) if f.endswith('.webp')); reg={v['src'].split('/')[-1] for v in m['voci'].values()}
        print('file non registrati:',[f for f in files if f not in reg]); print('voci senza file:',[k for k,v in m['voci'].items() if not os.path.exists(R+'/'+v['src'])])
        print('voci non verificate:',[k for k,v in m['voci'].items() if not v.get('verified')])
    elif A.c=='register':
        k=A.key; kind,_,i=k.partition(':'); src=A.src or 'assets/images/catalog/%s__%s.webp'%(kind,i)
        if not os.path.exists(R+'/'+src): sys.exit('file mancante: '+src)
        from PIL import Image
        w,h=Image.open(R+'/'+src).size
        m['voci'][k]={'src':src,'w':w,'h':h,'licence':A.licence,'credit':A.credit,'verified':bool(A.verify)}
        m['voci']=dict(sorted(m['voci'].items())); json.dump(m,open(MAN,'w',encoding='utf-8'),ensure_ascii=False,indent=2); print('registrata',k,w,h,'verified=',bool(A.verify))
main()
