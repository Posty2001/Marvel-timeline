#!/usr/bin/env python3
"""Esecuzione riproducibile delle suite TVA Archives (Playwright/Chromium).

Uso:  python3 tests/run_suites.py [--jobs N] [--only a,b] [--list] [--out DIR] [--timeout S]

Cosa fa (nessuna modifica ai file di test: la riscrittura avviene su COPIE temporanee):
  * avvia un server HTTP locale per ogni suite sulla radice del progetto (cartella che contiene index.html);
  * sostituisce nelle copie i percorsi/porte storici (file:///home/claude/work, 127.0.0.1:8124 ...) con quelli reali;
  * allinea le build-id fissate nei test (es. 20261023-1730-m342) alla build corrente (stampa le sostituzioni);
  * classifica ogni suite: PASS | FAIL | BLOCKED | NOT RUN, con motivazione, e confronta i FAIL con quelli documentati
    in tests/KNOWN_FAILS.json (un FAIL non documentato e' segnalato come NUOVO). Un FAIL non diventa mai PASS.
Requisiti: python3, playwright + chromium, Pillow (solo c4_contrast). Nessun accesso alla rete necessario
(le immagini TMDB/font non sono raggiungibili in sandbox: le suite usano i fallback locali).
"""
import argparse, concurrent.futures as cf, json, os, re, shutil, socket, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LEGACY_ROOT = '/home/claude/work'
LEGACY_PORTS = {'8124'}          # radice del progetto
REF_PATTERNS = [                  # dipendenze da build di riferimento / altri server: non fanno parte del repo
    (r'index\.3c\.frozen\.html', 'build di riferimento index.3c.frozen.html'),
    (r'index\.pre_[a-z0-9_]+\.html', 'build di riferimento index.pre_*.html'),
    (r'backups/N\d+[a-z0-9_]*\.html', 'backup storico backups/N*.html'),
    (r'\b812[5-9]\b', 'server aggiuntivo (porte 8125-8129: altra build/cartella di riferimento)'),
]
BUILD_RE = re.compile(r'\d{8}-\d{4}-(?:m\d+[a-z0-9]*|c\d+[a-z0-9]*)')

def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p

def current_build():
    t = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read(20000)
    m = re.search(r'name="tva-build" content="([^"]+)"', t)
    return m.group(1) if m else None

def load_known():
    p = os.path.join(HERE, 'KNOWN_FAILS.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}

def parse(out):
    npass = len(re.findall(r'^\s*PASS\b', out, re.M)); fails = [l.strip() for l in out.splitlines() if re.match(r'^\s*FAIL\b', l)]
    m = re.search(r'^test (\d+) fallimenti (\d+)', out, re.M)            # map3b_test
    if m and not npass: npass = int(m.group(1)) - int(m.group(2))
    m2 = re.search(r'PASS (\d+) FAIL (\d+)', out)                          # PASS n FAIL m [...]
    if m2 and not npass: npass = int(m2.group(1))
    summary = re.findall(r'^(?:FAILS|FALLITI|TOTALE \d+ FALLITI|FAILS \(con schede\)|test \d+ fallimenti)\s*(\d+)?', out, re.M)
    complete = bool(re.search(r'^(FAILS|FALLITI|TOTALE|test \d+ fallimenti|PASS \d+ FAIL|FAILS \(con schede\))', out, re.M))
    return npass, fails, complete

def run_one(name, opts, build, known):
    src = os.path.join(HERE, name + '.py')
    r = {'suite': name, 'pass': 0, 'fail': 0, 'status': None, 'reason': '', 'seconds': 0, 'fail_names': [], 'subs': []}
    if not os.path.exists(src):
        r.update(status='NOT RUN', reason='file di test assente'); return r
    text = open(src, encoding='utf-8').read()
    for pat, why in REF_PATTERNS:
        if re.search(pat, text):
            # una dipendenza e' soddisfatta solo se il file esiste davvero accanto al progetto (fixtures/)
            r.update(status='NOT RUN', reason='dipendenza esterna non inclusa nel repo: ' + why); return r
    port = free_port()
    wd = tempfile.mkdtemp(prefix='tva_suite_%s_' % name)
    out_dir = os.path.join(opts.out, 'artifacts'); os.makedirs(out_dir, exist_ok=True)
    def subst(x):
        x = re.sub(r"open\('/tmp/claude-0/t/([A-Za-z0-9_]+\.py)'\)", r"open('\1')", x)   # percorsi storici di suite che leggono altre suite
        x = x.replace('file://' + LEGACY_ROOT + '/', 'file://' + ROOT + '/').replace(LEGACY_ROOT, ROOT)
        x = re.sub(r'(?<![0-9])8124(?![0-9])', str(port), x)
        x = x.replace('/home/claude/outputs/', out_dir + '/')
        for d in set(re.findall(r'(' + re.escape(out_dir) + r'/[A-Za-z0-9_\-]+)/', x)): os.makedirs(d, exist_ok=True)
        for b in set(BUILD_RE.findall(x)) - {build}:
            x = x.replace(b, build); r['subs'].append('%s -> %s' % (b, build))
        return x
    t = subst(text)
    todo, done = list(set(re.findall(r'^\s*(?:from|import)\s+([A-Za-z0-9_]+)', text, re.M))), set()
    while todo:   # librerie locali (b32lib -> f4lib, leg_shot...) con le stesse sostituzioni, anche transitive
        mod = todo.pop()
        mp = os.path.join(HERE, mod + '.py')
        if mod in done or mod == name or not os.path.exists(mp): continue
        done.add(mod); lt = open(mp, encoding='utf-8').read()
        open(os.path.join(wd, mod + '.py'), 'w', encoding='utf-8').write(subst(lt))
        todo += re.findall(r'^\s*(?:from|import)\s+([A-Za-z0-9_]+)', lt, re.M)
    for sib in set(re.findall(r"open\('(?:/tmp/claude-0/t/)?([A-Za-z0-9_]+\.py)'\)", text)):   # suite che leggono il codice di un'altra suite (es. m342 -> m341)
        sp = os.path.join(HERE, sib)
        if os.path.exists(sp): open(os.path.join(wd, sib), 'w', encoding='utf-8').write(subst(open(sp, encoding='utf-8').read()))
    tmp = os.path.join(wd, name + '.py'); open(tmp, 'w', encoding='utf-8').write(t)
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', ROOT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    env = dict(os.environ, PYTHONPATH=HERE + os.pathsep + os.environ.get('PYTHONPATH', ''), TVA_ROOT=ROOT, PYTHONIOENCODING='utf-8')
    t0 = time.time()
    try:
        p = subprocess.run([sys.executable, '-u', tmp], cwd=wd, env=env, capture_output=True, text=True, timeout=opts.timeout)
        out = (p.stdout or '') + (p.stderr or ''); rc = p.returncode; to = False
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b'').decode('utf-8', 'replace') if isinstance(e.stdout, bytes) else (e.stdout or '')); rc = None; to = True
    finally:
        srv.terminate()
        shutil.rmtree(wd, ignore_errors=True)
    r['seconds'] = round(time.time() - t0)
    npass, fails, complete = parse(out)
    r['pass'], r['fail'], r['fail_names'] = npass, len(fails), fails
    tb = 'Traceback (most recent call last)' in out
    open(os.path.join(opts.out, name + '.log'), 'w', encoding='utf-8').write(out)
    blk = known.get('_blocked', {}).get(name, '')
    if to:
        r.update(status='BLOCKED', reason='timeout %ds (esecuzione incompleta)' % opts.timeout)
    elif tb and not complete:
        last = [l for l in out.splitlines() if re.search(r'(Error|Exception)', l)][-1:] or ['']
        r.update(status='BLOCKED', reason='esecuzione interrotta: ' + last[0].strip()[:200] + ((' | causa: ' + blk) if blk else ''))
    elif fails:
        kn = known.get(name, {})
        undoc = [f for f in fails if not any(k in f for k in kn.get('checks', []))]
        r['status'] = 'FAIL'
        r['reason'] = ('%d FAIL documentati in KNOWN_FAILS.json (%s)' % (len(fails), kn.get('why', '')) if not undoc
                       else '%d FAIL NON documentati (nuovi): %s' % (len(undoc), '; '.join(u[:80] for u in undoc[:3])))
        r['new'] = len(undoc)
    elif npass or complete:
        r.update(status='PASS', reason='')
    else:
        r.update(status='BLOCKED', reason='nessuna asserzione rilevata nell\'output')
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=1); ap.add_argument('--only', default=''); ap.add_argument('--list', action='store_true')
    ap.add_argument('--out', default=os.path.join(HERE, 'results')); ap.add_argument('--timeout', type=int, default=600)
    opts = ap.parse_args()
    man = json.load(open(os.path.join(HERE, 'SUITES.json'), encoding='utf-8'))
    names = [s['name'] for s in man['suites']]
    if opts.list:
        for s in man['suites']: print('%-16s %s' % (s['name'], s.get('area', ''))); return
    if opts.only: names = [n for n in names if n in opts.only.split(',')]
    os.makedirs(opts.out, exist_ok=True)
    build = current_build(); known = load_known()
    print('Radice: %s | build: %s | suite: %d | jobs: %d' % (ROOT, build, len(names), opts.jobs), flush=True)
    res = []
    with cf.ThreadPoolExecutor(opts.jobs) as ex:
        futs = {ex.submit(run_one, n, opts, build, known): n for n in names}
        for f in cf.as_completed(futs):
            r = f.result(); res.append(r)
            print('%-9s %-16s pass=%-4d fail=%-3d %4ds  %s' % (r['status'], r['suite'], r['pass'], r['fail'], r['seconds'], r['reason'][:110]), flush=True)
    order = {n: i for i, n in enumerate(names)}; res.sort(key=lambda r: order[r['suite']])
    json.dump({'build': build, 'results': res}, open(os.path.join(opts.out, 'RESULTS.json'), 'w'), indent=1, ensure_ascii=False)
    cnt = {k: sum(1 for r in res if r['status'] == k) for k in ('PASS', 'FAIL', 'BLOCKED', 'NOT RUN')}
    print('\nRIEPILOGO build %s: %s' % (build, ' | '.join('%s %d' % kv for kv in cnt.items())))
    with open(os.path.join(opts.out, 'RESULTS.md'), 'w', encoding='utf-8') as f:
        f.write('# Risultati suite - build %s\n\n| Suite | Stato | PASS | FAIL | Motivazione |\n|---|---|---|---|---|\n' % build)
        for r in res: f.write('| %s | %s | %d | %d | %s |\n' % (r['suite'], r['status'], r['pass'], r['fail'], r['reason'].replace('|', '/')))
        f.write('\n**Totale:** ' + ' | '.join('%s %d' % kv for kv in cnt.items()) + '\n')
    sys.exit(1 if cnt['FAIL'] or cnt['BLOCKED'] else 0)

if __name__ == '__main__':
    main()
