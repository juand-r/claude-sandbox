"""Perpetual-bouncer search (routes 12 and 14, milestone): one head between
two walls V (left) and W (right).  State = (head, V type, W type, side).
Every step is one exact single-class reaction (ptm.react, cached).  A run
is a BOUNCER if the state repeats (walls may have moved: we report the net
wall displacement per period; nonzero = the interval grows or shrinks for
ever, a stream-free non-periodic process).

Seeds: every right-moving library head H and right wall W such that
H + W is a clean REFLECTION (outgoing head on the B lattice), combined with
every left wall V among the stationary library objects of <= 2 C parts.
Usage: nice -n 10 python3 bounce.py [NMAX]   -> bounce.jsonl
"""
import json, os, sys, time
import ptm

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
OUT = os.path.join(ptm.HERE, 'bounce.jsonl')


def nparts(name):
    g = ptm.LIB.gliders[name]
    return len(g.parts) if g.parts else name.count('_C') + 1


def bounce(h, V, W, nmax):
    """head h (right-mover) about to hit W; V is the left wall."""
    side = 'R'
    walls = {'L': V, 'R': W}
    disp = {'L': 0, 'R': 0}
    seen = {}
    for step in range(nmax):
        st = (h, walls['L'], walls['R'], side)
        if st in seen:
            s0, d0 = seen[st]
            return {'outcome': 'BOUNCER', 'period': step - s0, 'start': s0,
                    'net_dL': disp['L'] - d0['L'], 'net_dR': disp['R'] - d0['R']}
        seen[st] = (step, dict(disp))
        r = ptm.react(h, walls[side])
        if r['kind'] != 'clean':
            return {'outcome': r['kind'], 'steps': step}
        d = ptm.direction(r['head'])
        walls[side] = r['cell']
        disp[side] += r['dx']
        if (side == 'R' and d == 'R') or (side == 'L' and d == 'L'):
            return {'outcome': 'pass', 'steps': step + 1}
        h = r['head']
        side = 'L' if side == 'R' else 'R'
    return {'outcome': 'alive', 'steps': nmax}


def main():
    heads = [n for n, g in ptm.LIB.gliders.items() if (g.p, g.d) in ptm.RIGHT]
    cells = [n for n, g in ptm.LIB.gliders.items() if (g.p, g.d) == ptm.STAT and nparts(n) <= 2]
    t0 = time.time()
    seeds = []
    for H in heads:
        k = ptm.canon([(H, 0, 0)])
        for W in cells:
            r = ptm.react(k, W)
            if r['kind'] == 'clean' and ptm.direction(r['head']) == 'L':
                seeds.append((H, k, W))
    print(len(heads), 'heads', len(cells), 'cells,', len(seeds), 'R-reflections', round(time.time() - t0), 's', flush=True)
    best = 0
    with open(OUT, 'w') as f:
        for H, k, W in seeds:
            for V in cells:
                res = bounce(k, V, W, NMAX)
                res.update(H=H, V=V, W=W)
                f.write(json.dumps(res) + '\n')
                n = res.get('steps', res.get('period', 0) + res.get('start', 0))
                if res['outcome'] in ('BOUNCER', 'alive') or n >= 3:
                    print(res, flush=True)
            f.flush()
    print('done', round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
