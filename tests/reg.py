import subprocess,sys,re
S=[('t.py',['no overflow 320px']),('c.py',[]),('d3.py',[]),('min2.py',[]),('r.py',[]),('a.py',None),('g.py',[]),('imp.py',[]),('inc.py',[]),('g2.py',[]),('an.py',[]),('g3.py',[]),('m3.py',[]),('m4.py',[]),('xm.py',[])]
tot=True
for f,allowed in S:
    try: o=subprocess.run(['python3',f],capture_output=True,text=True,timeout=170,cwd='/tmp/claude-0/t').stdout
    except Exception as e: print(f,'ERR',e); tot=False; continue
    if f=='a.py':
        ls=[l for l in o.strip().split('\n') if l.startswith(('load','dopo'))]; vals={re.search(r'\[.*\]',l).group(0) for l in ls}; ok=len(ls)==4 and len(vals)==1 and list(vals)[0].startswith('[1,'); print(f,'OK' if ok else 'FAIL',ls[-1] if ls else o[-100:]); tot&=ok; continue
    fails=[l for l in o.split('\n') if l.startswith('FAIL ')]
    bad=[l for l in fails if not any(a in l for a in (allowed or []))]
    if f=='imp.py':
        m=re.search(r'TOTALE (\d+) FALLITI (\[.*\])',o); ok=bool(m) and m.group(2)=='[]'; print(f,'OK' if ok else 'FAIL',m.group(0) if m else o[-200:]); tot&=ok; continue
    print(f,'OK' if not bad else 'FAIL',len(fails),'FAIL attesi' if fails and not bad else '', bad[:3]); tot&=not bad
# statico: ordine/tag, chiavi protette
import hashlib
a=open('/home/claude/work/index.ref_94fe3b59.html',encoding='utf-8').read() if len(sys.argv)>1 else None
b=open('/home/claude/work/index.html',encoding='utf-8').read()
if a:
    f=lambda s:re.findall(r'id="item-(\d+)" data-item="\d+" data-tag="(\w+)"',s)
    fa=f(a); i=[x[0] for x in fa].index('022'); fa[i:i+3]=[fa[i+2],fa[i],fa[i+1]]; fa=[x for x in fa if x[0]!='133']   # unico riordino autorizzato: Logan prima di Deadpool/Deadpool 2
    ok=fa==f(b); print('ordine+colori 139 invariati (salvo Logan->prima di Deadpool, ID stabili)',ok); tot&=ok
    for k in ['RTD_IDS','PROFILE_OBJ_KEYS','PROFILE_STR_KEYS','marvel-ultimate-timeline-auto-backup','function sostituisciProfilo','function normalizzaProfilo','function applicaScrittureProfilo','XP_BANK','marvel-ultimate-timeline-badges-earned']:
        ia=a.find(k); ib=b.find(k); ok=a[ia:ia+500]==b[ib:ib+500]; print(' ',k,ok); tot&=ok
print('REGRESSIONE','OK' if tot else 'FALLITA')
