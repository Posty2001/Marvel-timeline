#!/usr/bin/env python3
"""Fase 1 TVA Archives: modifiche puntuali a index.html fuori dai blocchi iniettati (idempotente)."""
P='/home/claude/work/index.html'
s=open(P,encoding='utf-8').read()
# 1) l'Atlante (.a2) e' un overlay a schermo intero: eccezione alla regola della home hub (apertura dalla card della Home)
if '#journeyStarted:checked ~ #homeHubExited:not(:checked) ~ *:not(.a2):' not in s:
    k='  #journeyStarted:checked ~ #homeHubExited:not(:checked) ~ *:not('
    assert s.count(k)==1
    s=s.replace(k,'  #journeyStarted:checked ~ #homeHubExited:not(:checked) ~ *:not(.a2):not(')
# 2) voce nel menu generale
l='<label for="tvaArchivesToggle" class="sidebar-archive-link">&#128193; TVA Archives</label>'
if 'id="a2SidebarLink"' not in s:
    assert s.count(l)==1
    s=s.replace(l,'<label for="atlas2Toggle" class="sidebar-archive-link" id="a2SidebarLink">&#127756; TVA Archives &mdash; L\'Atlante</label>\n  <label for="tvaArchivesToggle" class="sidebar-archive-link">&#128193; Database classico</label>')
# 3) build
for old in ('20261019-1030-fase4-dossier','20261019-0900-xmen-chiusura','20261019-0600-xmen-ordine','20261019-0200-cronologie','20261018-2100-multiverse-map','20261018-1930-uni-dossier','20261018-1800-home-assets','20261018-1630-stats-fix','20261018-1500-home-osservatorio','20261018-1230-intro-scenes','20261018-1100-rel-trees-arti','20261018-0930-intro-single','20261017-1600-consolidation1','20261017-2100-tva-archives1','20261017-2200-tva-archives2','20261017-2330-tva-archives3','20261017-2359-tva-final1','20261017-2130-tva-copertine','20261017-2230-living-intro','20261017-2330-restyle','20261018-0300-intro-art','20261018-0400-legacy-integration'):
    s=s.replace('content="%s"'%old,'content="20261019-1130-fix-ios-voti"')
open(P,'w',encoding='utf-8').write(s); print('ok')
