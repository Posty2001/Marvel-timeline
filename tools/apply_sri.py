#!/usr/bin/env python3
"""Applica integrity+crossorigin ai 3 <script> Firebase 10.13.0 di un index.html, usando SOLO hash calcolati dal tuo script (sri_firebase.sh/.ps1).
Non calcola ne' inventa hash. Rifiuta formati non validi. Idempotente. Uso: python3 tools/apply_sri.py sri_firebase.json index.html"""
import json, re, sys
FILES = ['firebase-app-compat.js', 'firebase-database-compat.js', 'firebase-auth-compat.js']
def main(jp, hp):
    d = json.load(open(jp, encoding='utf-8-sig')); s = open(hp, encoding='utf-8').read()
    for f in FILES:
        v = d.get(f); h = v.get('integrity') if isinstance(v, dict) else v
        if not isinstance(h, str) or not re.fullmatch(r'sha384-[A-Za-z0-9+/]{64}', h): sys.exit('hash non valido per %s: %r' % (f, h))
        tag = '<script src="https://www.gstatic.com/firebasejs/10.13.0/%s"' % f
        if s.count(tag) != 1: sys.exit('tag script non trovato (o duplicato): ' + f)
        m = re.search(re.escape(tag) + r'([^>]*)></script>', s)
        if ' integrity="' in m.group(1):
            if ('integrity="%s"' % h) not in m.group(1): sys.exit('integrity gia\' presente e DIVERSO per ' + f)
            continue
        s = s.replace(m.group(0), tag + ' integrity="%s" crossorigin="anonymous"></script>' % h)
    open(hp, 'w', encoding='utf-8').write(s); print('SRI applicato a', len(FILES), 'script in', hp)
if __name__ == '__main__':
    if len(sys.argv) != 3: sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
