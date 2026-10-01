"""One B (or one A) against EVERY stationary object of width <= 34
(shuttle's SAT enumeration ../shuttle/trains_7_0_34.jsonl, 5077 objects,
plus trains_7_0_20.jsonl): single class (Lemma L1), one exact run each.

Questions (route 22 U2, routes 12/14 reflections):
  B + O -> O' + B-train with >= 2 B's     (fan-out; O' == O is a doubler)
  B + O -> O' + B, O' != O                 (toggle / pass with rewrite)
  B + O -> O'  (absorbed)                  (toggle half)
  B + O -> O' + right-movers (A/D)         (L-reflection: bouncer wall)
For A (mode A): reflections A + O -> O' + B-family and passes.
Output bscan_<mode>.jsonl.  Usage: nice -n 10 python3 bscan.py B|A
"""
import json, os, sys, time
import ptm
from collide import products_of
from r110lib import build_row, _pack_batch, _unpack_batch, _step_state, TILE

MODE = sys.argv[1] if len(sys.argv) > 1 else 'B'
SRCS = [os.path.join(ptm.HERE, '../shuttle/trains_7_0_20.jsonl'),
        os.path.join(ptm.HERE, '../shuttle/trains_7_0_34.jsonl')]
OUT = os.path.join(ptm.HERE, f'bscan_{MODE}.jsonl')
GAP = 40
G = ptm.LIB.gliders[MODE]


def nbase(name):
    g = ptm.LIB.gliders[name]
    if g.parts:
        return len(g.parts)
    if name in ('B^2', 'A^2'):
        return 2
    if name in ('B^3', 'A^3'):
        return 3
    if name in ('A^4',):
        return 4
    if name in ('A^5',):
        return 5
    return 1 if name in ('A', 'B') else None   # None: compound without a parse


def place_mover(obj_end, absR, left_of=None):
    """library glider state at time 0 with ether-consistent placement."""
    best = None
    for k in range(-600, 600):
        st = G.state_at(0, k, 0)
        if left_of is None:
            if st[3] >= obj_end + GAP and (st[1] - st[3] - absR) % TILE == 0:
                return st
        else:
            if st[3] + len(st[0]) <= left_of - GAP and (st[2] - st[3] - absR) % TILE == 0:
                best = st
    if best is None:
        raise ValueError('no placement')
    return best


def run(o, tmax=1500):
    os_ = (o['bits'], 0, o['pR'], 0)
    if MODE == 'B':
        ms = place_mover(len(o['bits']), o['pR'])            # B to the right
    else:
        ms = place_mover(None, 0, left_of=0)                  # A to the left (abs phase 0)
    row, x0 = build_row([os_, ms], pad=int(tmax * 0.7) + 120)
    s = _pack_batch(row[None, :])
    T = 0
    while T < tmax:
        for _ in range(50):
            s = _step_state(s)
        T += 50
        ok, prods, objs = products_of(ptm.LIB, _unpack_batch(s, 1)[0], x0, T)
        if ok:
            return prods
    return None


def classify(prods):
    if prods is None:
        return 'unsettled', None
    st = [p for p in prods if ptm.period(p[0]) == ptm.STAT]
    mv = [p for p in prods if ptm.period(p[0]) != ptm.STAT]
    if len(st) != 1:
        return 'dirty', None
    if not mv:
        return 'absorbed', 0
    pers = {ptm.period(p[0]) for p in mv}
    back = ptm.LEFT if MODE == 'B' else ptm.RIGHT        # same direction as the input
    turn = ptm.RIGHT if MODE == 'B' else ptm.LEFT
    nb = [nbase(p[0]) for p in mv]
    count = None if None in nb else sum(nb)
    if pers <= back:
        return 'pass', count
    if pers <= turn:
        return 'reflect', count
    return 'dirty', None


def main():
    objs = []
    seen = set()
    for src in SRCS:
        for line in open(src):
            o = json.loads(line)
            k = (o['bits'], o['pR'])
            if k not in seen:
                seen.add(k); objs.append(o)
    t0 = time.time()
    cnt = {}
    with open(OUT, 'w') as f:
        for i, o in enumerate(objs):
            try:
                prods = run(o)
            except (ValueError, RuntimeError) as e:
                f.write(json.dumps({'i': i, 'kind': 'error', 'why': repr(e)}) + '\n'); continue
            kind, count = classify(prods)
            rec = {'i': i, 'bits': o['bits'], 'pR': o['pR'], 'kind': kind, 'count': count,
                   'out': [p[0] for p in prods] if prods else None}
            if kind in ('pass', 'reflect'):
                # does the stationary object come back identical? (name equality)
                pass
            cnt[kind] = cnt.get(kind, 0) + 1
            f.write(json.dumps(rec) + '\n')
            if kind == 'pass' and (count is None or count >= 2):
                print('FANOUT?', rec, flush=True)
            if i % 500 == 0:
                f.flush()
                print(i, cnt, round(time.time() - t0), 's', flush=True)
    print('done', len(objs), cnt, round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
