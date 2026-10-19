#!/usr/bin/env python3
"""Intro a scene: markup (testi originali recuperati), CSS e JS. Idempotente."""
import re
P = '/home/claude/work/index.html'; T = '/home/claude/work/tools/'
s = open(P, encoding='utf-8').read()
css = open(T + 'scenes.css', encoding='utf-8').read().rstrip(); js = open(T + 'scenes.js', encoding='utf-8').read().rstrip()
# 1) eyebrow originale completo ("TIME VARIANCE AUTHORITY · ARCHIVIO CENTRALE") e dettagli editoriali originali
old = '<div class="intro-eyebrow">TIME VARIANCE AUTHORITY</div>\n      <div class="lm-sp1">'
if old in s:
    s = s.replace(old, '<div class="intro-eyebrow"><span>TIME VARIANCE AUTHORITY</span><span class="lm-eb2">ARCHIVIO CENTRALE</span></div>\n      <div class="lm-sp1">', 1)
tag = '<p class="intro-tagline">Infinite realt&agrave;. Un unico viaggio.</p>'
if 'class="lm-detail"' not in s:
    assert s.count(tag) == 1
    s = s.replace(tag, tag + '\n      <p class="lm-detail"><span class="lm-detail-k">TVA ARCHIVE</span><span class="lm-detail-t" lang="en">The definitive interactive Marvel viewing experience.</span></p>', 1)
# 2) icone originali delle statistiche
for lbl, ic in (('titoli', '&#127909;'), ('universi', '&#127760;'), ('personaggi', '&#128101;'), ('ore complessive di visione', '&#9201;&#65039;')):
    a = '<div class="intro-stat"><span class="intro-stat-num">'
    pat = re.compile(r'<div class="intro-stat">(<span class="intro-stat-num">[^<]*</span><span class="intro-stat-lbl">%s</span>)' % re.escape(lbl))
    s = pat.sub(lambda m: '<div class="intro-stat"><span class="intro-stat-ic" aria-hidden="true">%s</span>%s' % (ic, m.group(1)), s, count=1) if ('intro-stat-ic" aria-hidden="true">%s' % ic) not in s else s
# 2b) statistiche coerenti con la Home (valori di riserva = dati reali; all'avvio vengono riletti da tvaAtlas2.stats())
if 'data-stat="opere"' not in s:
    def _st(ic, num, key, lbl): return '<div class="intro-stat"><span class="intro-stat-ic" aria-hidden="true">%s</span><span class="intro-stat-num" data-stat="%s">%s</span><span class="intro-stat-lbl">%s</span></div>' % (ic, key, num, lbl)
    m1 = re.search(r'<div class="intro-stat"><span class="intro-stat-ic" aria-hidden="true">&#127909;</span><span class="intro-stat-num">176</span><span class="intro-stat-lbl">titoli</span></div>', s)
    assert m1
    s = s.replace(m1.group(0), _st('&#127909;', 176, 'opere', 'opere totali (con varianti e serie animate)') + _st('&#127902;&#65039;', 138, 'timeline', 'titoli della Timeline'), 1)
    for old, new, key in ((26, 27, 'universi'), (304, 300, 'personaggi')):
        a = '<span class="intro-stat-num">%d</span>' % old
        assert s.count(a) == 1, (old, s.count(a))
        s = s.replace(a, '<span class="intro-stat-num" data-stat="%s">%d</span>' % (key, new), 1)
# 3) riga d'accesso originale (flicker) nell'Atto IV
if 'class="lm-flicker"' not in s:
    m = '<div class="lm-foot intro-foot">'
    assert s.count(m) == 1
    s = s.replace(m, '<p class="lm-flicker" aria-hidden="true">&#9889; ACCESSO ARCHIVIO TVA IN CORSO&hellip; &#9889;</p>\n        ' + m, 1)
# 4) css / js
blk = '<style id="tva-scenes-css">\n' + css + '\n</style>'
s = re.sub(r'<style id="tva-scenes-css">.*?</style>', lambda _: blk, s, flags=re.S) if 'id="tva-scenes-css"' in s else s.replace('</head>', blk + '\n</head>', 1)
sj = '<script id="tva-scenes">\n' + js + '\n</script>'
s = re.sub(r'<script id="tva-scenes">.*?</script>', lambda _: sj, s, flags=re.S) if 'id="tva-scenes"' in s else s[:s.rfind('</body>')] + sj + '\n' + s[s.rfind('</body>'):]
open(P, 'w', encoding='utf-8').write(s)
print('scenes ok')
