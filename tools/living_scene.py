#!/usr/bin/env python3
"""Genera la scena SVG originale «Infinite Realtà» (3 livelli parallasse) -> tools/living_scene.html.
Tutto procedurale e deterministico (seed fisso): nessuna immagine di terzi. viewBox 390x844, preserveAspectRatio slice."""
import random, math
R = random.Random(20261017)
GOLD, RED, IVO, INK = '#D2B184', '#DB777C', '#F2E8D8', '#101014'
f = lambda v: ('%.1f' % v).rstrip('0').rstrip('.')

# ---------------- LIVELLO 0: cielo, nebulose, stelle (statico) ----------------
def layer0():
    o = ['<svg class="lm-svg lm-l0" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice" focusable="false" aria-hidden="true">',
         '<defs>'
         '<linearGradient id="lmSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07070b"/><stop offset=".42" stop-color="#14091a"/><stop offset=".72" stop-color="#2a0e1a"/><stop offset="1" stop-color="#0b0709"/></linearGradient>'
         '<radialGradient id="lmNebA" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#8e2a3a" stop-opacity=".55"/><stop offset=".55" stop-color="#4a1026" stop-opacity=".25"/><stop offset="1" stop-color="#4a1026" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="lmNebB" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#d2b184" stop-opacity=".28"/><stop offset="1" stop-color="#d2b184" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="lmNebC" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#3b2a6b" stop-opacity=".4"/><stop offset="1" stop-color="#3b2a6b" stop-opacity="0"/></radialGradient>'
         '</defs>',
         '<rect width="390" height="844" fill="url(#lmSky)"/>',
         '<ellipse cx="90" cy="150" rx="210" ry="150" fill="url(#lmNebA)"/>',
         '<ellipse cx="330" cy="330" rx="190" ry="170" fill="url(#lmNebA)" opacity=".8"/>',
         '<ellipse cx="195" cy="300" rx="170" ry="260" fill="url(#lmNebB)"/>',
         '<ellipse cx="40" cy="520" rx="150" ry="120" fill="url(#lmNebC)"/>',
         '<ellipse cx="360" cy="640" rx="170" ry="140" fill="url(#lmNebC)" opacity=".7"/>',
         '<g>']
    cols = [IVO, IVO, IVO, GOLD, '#f6c8b8']
    for i in range(150):
        x, y = R.uniform(0, 390), R.uniform(0, 844)
        r = R.choice([.35, .45, .55, .7, .9, 1.15])
        op = R.uniform(.35, .95)
        o.append('<circle cx="%s" cy="%s" r="%s" fill="%s" opacity="%s"/>' % (f(x), f(y), r, R.choice(cols), f(op)[:4]))
    o.append('</g></svg>')
    return ''.join(o)

# ---------------- sfere-universo ----------------
def orb_defs(i, cx, cy, r, sky):
    return ('<clipPath id="lmC%d"><circle cx="%s" cy="%s" r="%s"/></clipPath>'
            '<radialGradient id="lmS%d" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></radialGradient>'
            '<radialGradient id="lmV%d" cx=".5" cy=".5" r=".5"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".72"/></radialGradient>'
            '<radialGradient id="lmG%d" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#db777c" stop-opacity=".30"/><stop offset="1" stop-color="#db777c" stop-opacity="0"/></radialGradient>'
            % (i, f(cx), f(cy), f(r), i, sky[0], sky[1], i, i))

def orb_wrap(i, cx, cy, r, inner, rim_rot=-35):
    return ('<g><circle cx="%s" cy="%s" r="%s" fill="url(#lmG%d)"/>'
            '<g clip-path="url(#lmC%d)"><rect x="%s" y="%s" width="%s" height="%s" fill="url(#lmS%d)"/>%s'
            '<circle cx="%s" cy="%s" r="%s" fill="url(#lmV%d)"/></g>'
            '<circle cx="%s" cy="%s" r="%s" fill="none" stroke="%s" stroke-opacity=".55" stroke-width="1.1"/>'
            '<path d="M%s %s A%s %s 0 0 1 %s %s" fill="none" stroke="#f6e3c0" stroke-opacity=".85" stroke-width="1.6" stroke-linecap="round" transform="rotate(%d %s %s)"/>'
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#fff" opacity=".07" transform="rotate(-28 %s %s)"/></g>'
            % (f(cx), f(cy), f(r * 1.45), i, i, f(cx - r), f(cy - r), f(2 * r), f(2 * r), i, inner,
               f(cx), f(cy), f(r), i,
               f(cx), f(cy), f(r), GOLD,
               f(cx - r * .92), f(cy - r * .4), f(r * .98), f(r * .98), f(cx + r * .15), f(cy - r * .96), rim_rot, f(cx), f(cy),
               f(cx - r * .3), f(cy - r * .42), f(r * .26), f(r * .11), f(cx - r * .3), f(cy - r * .42)))

def city(cx, cy, r):
    o = ['<circle cx="%s" cy="%s" r="%s" fill="#f0a36a" opacity=".22"/>' % (f(cx), f(cy + r * .5), f(r * .9))]
    x = cx - r
    while x < cx + r:
        w = R.uniform(r * .1, r * .2); h = R.uniform(r * .25, r * .95)
        o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#120d17"/>' % (f(x), f(cy + r * .7 - h), f(w), f(h + r)))
        if h > r * .6:
            o.append('<path d="M%s %s L%s %s L%s %s Z" fill="#120d17"/>' % (f(x + w * .2), f(cy + r * .7 - h), f(x + w * .5), f(cy + r * .7 - h - r * .3), f(x + w * .8), f(cy + r * .7 - h)))
        for k in range(int(h / (r * .09))):
            if R.random() < .42:
                o.append('<rect x="%s" y="%s" width="%s" height="%s" fill="#f1c27d" opacity=".8"/>' % (f(x + R.uniform(.15, .75) * w), f(cy + r * .7 - h + k * r * .09 + 2), f(max(.8, w * .12)), f(r * .035)))
        x += w + r * .015
    o.append('<path d="M%s %s Q%s %s %s %s" fill="none" stroke="#ffd9a0" stroke-opacity=".7" stroke-width="1.2"/>' % (f(cx - r), f(cy - r * .05), f(cx), f(cy - r * .5), f(cx + r), f(cy + r * .05)))
    o.append('<circle cx="%s" cy="%s" r="1.8" fill="#fff" opacity=".9"/>' % (f(cx + r * .3), f(cy - r * .32)))
    return ''.join(o)

def ringed(cx, cy, r):
    return ('<circle cx="%s" cy="%s" r="%s" fill="#2a1030"/><circle cx="%s" cy="%s" r="%s" fill="#6b2744" opacity=".6"/>'
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="2" opacity=".85" transform="rotate(-18 %s %s)"/>'
            '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="none" stroke="%s" stroke-width="1" opacity=".5" transform="rotate(-18 %s %s)"/>'
            '<circle cx="%s" cy="%s" r="%s" fill="#c9a37a"/><circle cx="%s" cy="%s" r="%s" fill="#e8d2aa"/>'
            % (f(cx - r * .1), f(cy + r * .1), f(r * .55), f(cx - r * .22), f(cy - r * .02), f(r * .35),
               f(cx - r * .1), f(cy + r * .1), f(r * .95), f(r * .26), GOLD, f(cx - r * .1), f(cy + r * .1),
               f(cx - r * .1), f(cy + r * .1), f(r * 1.1), f(r * .31), GOLD, f(cx - r * .1), f(cy + r * .1),
               f(cx + r * .55), f(cy - r * .5), f(r * .13), f(cx - r * .62), f(cy - r * .55), f(r * .07)))

def shattered(cx, cy, r):
    o = ['<circle cx="%s" cy="%s" r="%s" fill="#c1535c" opacity=".18"/>' % (f(cx), f(cy), f(r * .8))]
    for k in range(9):
        a = k * 2 * math.pi / 9 + R.uniform(-.2, .2); d = r * (.25 + R.uniform(0, .45)); s = r * R.uniform(.12, .3)
        px, py = cx + d * math.cos(a), cy + d * math.sin(a)
        pts = ' '.join('%s,%s' % (f(px + s * math.cos(t) * R.uniform(.6, 1.2)), f(py + s * math.sin(t) * R.uniform(.6, 1.2))) for t in (0, 1.3, 2.5, 3.7, 5.0))
        o.append('<polygon points="%s" fill="#1c1018" stroke="%s" stroke-opacity=".8" stroke-width=".9"/>' % (pts, GOLD))
    o.append('<path d="M%s %s L%s %s L%s %s L%s %s" fill="none" stroke="#ffd9a0" stroke-width="1.6" opacity=".9"/>' % (f(cx - r * .6), f(cy - r * .5), f(cx - r * .1), f(cy - r * .05), f(cx + r * .15), f(cy + r * .15), f(cx + r * .65), f(cy + r * .55)))
    return ''.join(o)

def spiral(cx, cy, r):
    o = []
    for arm in range(3):
        pts = []
        for t in range(0, 60):
            a = t * .22 + arm * 2.094; d = t * r / 60 * 1.05
            pts.append('%s,%s' % (f(cx + d * math.cos(a)), f(cy + d * math.sin(a) * .8)))
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="%s" stroke-linecap="round"/>' % (' '.join(pts), (RED, GOLD, '#f6c8b8')[arm], (.9, .8, .7)[arm], (2.4, 1.6, 1.2)[arm]))
    o.append('<circle cx="%s" cy="%s" r="%s" fill="#fff3d6"/><circle cx="%s" cy="%s" r="%s" fill="#f1c27d" opacity=".5"/>' % (f(cx), f(cy), f(r * .1), f(cx), f(cy), f(r * .28)))
    return ''.join(o)

def desert(cx, cy, r):
    return ('<circle cx="%s" cy="%s" r="%s" fill="#ffd79a"/><circle cx="%s" cy="%s" r="%s" fill="#f09a6a" opacity=".35"/>'
            '<path d="M%s %s Q%s %s %s %s T%s %s V%s H%s Z" fill="#3a1a1c"/>'
            '<path d="M%s %s L%s %s L%s %s" fill="none" stroke="#1a0e12" stroke-width="2.4"/>'
            % (f(cx + r * .1), f(cy - r * .1), f(r * .32), f(cx + r * .1), f(cy - r * .1), f(r * .55),
               f(cx - r), f(cy + r * .35), f(cx - r * .4), f(cy + r * .1), f(cx + r * .1), f(cy + r * .4), f(cx + r), f(cy + r * .3), f(cy + r), f(cx - r),
               f(cx - r * .3), f(cy + r * .3), f(cx - r * .22), f(cy + r * .02), f(cx - r * .14), f(cy + r * .32)))

def ice(cx, cy, r):
    o = ['<circle cx="%s" cy="%s" r="%s" fill="#e8d2aa" opacity=".35"/>' % (f(cx - r * .3), f(cy - r * .3), f(r * .5))]
    for k in range(5):
        x = cx - r + k * r * .5
        o.append('<polygon points="%s,%s %s,%s %s,%s" fill="#2a1a2e" stroke="#f6e3c0" stroke-opacity=".6" stroke-width=".7"/>' % (f(x), f(cy + r), f(x + r * .28), f(cy + r * (.1 + .2 * (k % 2))), f(x + r * .56), f(cy + r)))
    return ''.join(o)

def tower(cx, cy, r):
    return ('<rect x="%s" y="%s" width="%s" height="%s" fill="#150c14"/><polygon points="%s,%s %s,%s %s,%s" fill="#150c14"/><circle cx="%s" cy="%s" r="%s" fill="#f0a36a" opacity=".5"/>'
            % (f(cx - r * .13), f(cy - r * .3), f(r * .26), f(r * 1.4), f(cx - r * .13), f(cy - r * .3), f(cx), f(cy - r * .8), f(cx + r * .13), f(cy - r * .3), f(cx + r * .3), f(cy - r * .4), f(r * .22)))

ORBS = [  # cx, cy, r, sky, scena, rotazione bordo
    (84, 176, 62, ('#e0826a', '#2c1228'), city, -40),
    (316, 120, 48, ('#5a2d5a', '#150c1c'), ringed, -20),
    (338, 306, 64, ('#7a2a3a', '#190c14'), shattered, -60),
    (50, 372, 44, ('#3b2a6b', '#12091c'), spiral, -30),
    (150, 58, 26, ('#e9a06a', '#3a1620'), desert, -50),
    (252, 40, 20, ('#7aa0b8', '#1a1530'), ice, -45),
    (22, 520, 28, ('#a8434f', '#1a0c14'), tower, -20),
    (368, 506, 24, ('#5a2d5a', '#150c1c'), ringed, -30),
    (112, 275, 16, ('#e9a06a', '#2c1228'), desert, -40),
    (268, 214, 14, ('#5a2d5a', '#150c1c'), spiral, -40),
]

def layer_orbs(sel):
    o = ['<svg class="lm-svg %s" viewBox="0 0 390 844" preserveAspectRatio="xMidYMid slice" focusable="false" aria-hidden="true"><defs>' % sel[0]]
    body = []
    for i, (cx, cy, r, sky, scene, rot) in enumerate(ORBS):
        if i not in sel[1]:
            continue
        o.append(orb_defs(i, cx, cy, r, sky))
        body.append(orb_wrap(i, cx, cy, r, scene(cx, cy, r), rot))
    return o, body

# ---------------- LIVELLO 1: universi lontani + correnti + frattura ----------------
RIFT = [(199, 14), (190, 66), (204, 128), (183, 196), (206, 262), (186, 328), (203, 394), (189, 456), (197, 512), (195, 548)]
def rift_poly(w):
    n = len(RIFT) - 1
    m = [max(.08, math.sin(math.pi * i / n) ** .7) for i in range(n + 1)]
    left = [(x - w * m[i] * (1 + .5 * math.sin(i * 1.7)), y) for i, (x, y) in enumerate(RIFT)]
    right = [(x + w * m[i] * (1 + .5 * math.cos(i * 1.3)), y) for i, (x, y) in enumerate(RIFT)]
    pts = left + right[::-1]
    return ' '.join('%s,%s' % (f(x), f(y)) for x, y in pts)

def layer1():
    o, body = layer_orbs(('lm-l1', {4, 5, 7, 8, 9, 3}))
    o.append('<linearGradient id="lmCur" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#db777c" stop-opacity="0"/><stop offset=".5" stop-color="#e8928e"/><stop offset="1" stop-color="#d2b184"/></linearGradient>')
    o.append('<linearGradient id="lmRiftG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6e4" stop-opacity=".0"/><stop offset=".12" stop-color="#fff6e4"/><stop offset=".55" stop-color="#f1c98a"/><stop offset="1" stop-color="#db777c" stop-opacity=".0"/></linearGradient>')
    o.append('<linearGradient id="lmRay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1c98a" stop-opacity=".0"/><stop offset=".6" stop-color="#f1c98a" stop-opacity=".16"/><stop offset="1" stop-color="#db777c" stop-opacity=".0"/></linearGradient>')
    o.append('<radialGradient id="lmHalo" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ffe7bd" stop-opacity=".85"/><stop offset=".25" stop-color="#e8928e" stop-opacity=".45"/><stop offset="1" stop-color="#8e2a3a" stop-opacity="0"/></radialGradient>')
    o.append('</defs>')
    # raggi volumetrici dalla frattura
    for k, (dx, w) in enumerate([(-150, 40), (-90, 26), (-40, 18), (40, 18), (100, 28), (160, 44)]):
        o.append('<polygon points="%s,120 %s,120 %s,560 %s,560" fill="url(#lmRay)"/>' % (f(193 - w * .08), f(197 + w * .08), f(197 + dx + w), f(193 + dx - w)))
    # alone e frattura
    o.append('<ellipse cx="195" cy="270" rx="150" ry="300" fill="url(#lmHalo)" opacity=".5"/>')
    o.append('<polygon points="%s" fill="#8e2a3a" opacity=".5"/>' % rift_poly(22))
    o.append('<polygon points="%s" fill="#e8928e" opacity=".7"/>' % rift_poly(13))
    o.append('<polygon points="%s" fill="url(#lmRiftG)"/>' % rift_poly(7))
    o.append('<polyline points="%s" fill="none" stroke="#fffaf0" stroke-width="1.4" opacity=".95"/>' % ' '.join('%s,%s' % p for p in RIFT))
    # crepe che si diramano nello spazio
    for (x, y), side in zip(RIFT[1:-1], [-1, 1, -1, 1, -1, 1, -1]):
        L = R.uniform(30, 80); a = R.uniform(-.5, .5)
        o.append('<path d="M%s %s l%s %s l%s %s" fill="none" stroke="#f1c98a" stroke-opacity=".6" stroke-width=".8"/>' % (f(x), f(y), f(side * L * .55), f(L * a), f(side * L * .45), f(-L * a * .6)))
    # correnti di energia fra universi e frattura
    cur = [
        'M84 176 C130 210 150 250 192 292', 'M316 120 C280 160 240 200 200 262',
        'M338 306 C300 320 250 330 202 346', 'M50 372 C100 360 150 372 190 388',
        'M150 58 C170 120 186 170 194 214', 'M252 40 C238 110 214 170 200 214',
        'M22 520 C90 480 150 470 192 452', 'M368 506 C300 480 250 468 202 452',
        'M20 120 C80 240 120 330 188 404', 'M372 200 C310 260 250 320 204 380',
    ]
    for k, d in enumerate(cur):
        o.append('<path d="%s" fill="none" stroke="#8e2a3a" stroke-opacity=".38" stroke-width="7" stroke-linecap="round"/>' % d)
        o.append('<path d="%s" fill="none" stroke="url(#lmCur)" stroke-opacity=".9" stroke-width="1.6" stroke-linecap="round" %s/>' % (d, 'stroke-dasharray="1 7"' if k % 3 == 2 else ''))
    o.extend(body)
    # piccole particelle d'oro lungo le correnti
    for i in range(46):
        o.append('<circle cx="%s" cy="%s" r="%s" fill="#f1c98a" opacity="%s"/>' % (f(R.uniform(20, 370)), f(R.uniform(60, 520)), f(R.uniform(.5, 1.3)), f(R.uniform(.3, .85))[:4]))
    o.append('</svg>')
    return ''.join(o)

# ---------------- LIVELLO 2: sfere grandi in primo piano + rovine ----------------
def layer2():
    o, body = layer_orbs(('lm-l2', {0, 1, 2, 6}))
    o.append('<linearGradient id="lmRuin" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1320"/><stop offset="1" stop-color="#07060a"/></linearGradient>')
    o.append('<linearGradient id="lmFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1c98a" stop-opacity=".0"/><stop offset=".5" stop-color="#db777c" stop-opacity=".22"/><stop offset="1" stop-color="#07060a" stop-opacity=".9"/></linearGradient>')
    o.append('</defs>')
    o.extend(body)
    # orizzonte luminoso e piattaforma monumentale
    o.append('<rect x="0" y="560" width="390" height="284" fill="url(#lmFloor)"/>')
    o.append('<ellipse cx="195" cy="560" rx="140" ry="9" fill="#f1c98a" opacity=".35"/><ellipse cx="195" cy="560" rx="60" ry="3.5" fill="#fff6e4" opacity=".7"/>')
    o.append('<path d="M0 844 V700 L22 700 L26 640 L54 640 L60 700 L90 712 L120 760 L120 844Z" fill="url(#lmRuin)"/>')
    o.append('<path d="M390 844 V690 L366 690 L360 628 L334 636 L330 700 L300 716 L270 770 L270 844Z" fill="url(#lmRuin)"/>')
    o.append('<path d="M26 640 H54 M22 700 H60 M366 690 H390 M334 636 H360" stroke="#D2B184" stroke-opacity=".6" stroke-width="1.2"/>')
    o.append('<path d="M126 844 L150 760 L168 700 H222 L240 760 L264 844" fill="none" stroke="#D2B184" stroke-opacity=".25" stroke-width="1"/>')
    o.append('</svg>')
    return ''.join(o)

if __name__ == '__main__':
    out = layer0() + '\n' + layer1() + '\n' + layer2()
    open('/home/claude/work/tools/living_scene.html', 'w', encoding='utf-8').write(out)
    print('byte', len(out.encode()))
