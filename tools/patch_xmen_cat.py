#!/usr/bin/env python3
"""Aggiunge la categoria gia' esistente 'xmen' a X2 (016), Dark Phoenix (020), The New Mutants (021)
sia su <li data-cats> sia sulla checkbox; allinea il denominatore statico del contatore X-Men. Idempotente."""
import re,sys
p='/home/claude/work/index.html'; s=open(p,encoding='utf-8').read(); n=0
for i in ('016','020','021'):
    for pat,new in ((r'(id="item-%s" data-item="%s"[^>]*? data-cats=")film fox(")'%(i,i),r'\1film fox xmen\2'),
                    (r'(<input type="checkbox" class="watch-check" data-item="%s" data-cats=")film fox(")'%i,r'\1film fox xmen\2')):
        s,k=re.subn(pat,new,s); n+=k
# denominatore statico = numero reale di checkbox con xmen
tot=len(re.findall(r'<input type="checkbox" class="watch-check" data-item="\d+" data-cats="[^"]*\bxmen\b',s))
s,k=re.subn(r'(id="dashCnt-xmen">0</span>/)\d+',r'\g<1>%d'%tot,s); n+=k
open(p,'w',encoding='utf-8').write(s); print('modifiche',n,'totale xmen',tot)
