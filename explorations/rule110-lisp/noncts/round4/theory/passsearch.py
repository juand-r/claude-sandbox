"""Route 12 viability test: can a rigid head pass a stationary cell and come
out as the SAME head (up to translation)?

A universal particle TM must traverse unboundedly long stretches of tape, so
it needs head cycles h1 -> h2 -> ... -> h1 through cells (pass-throughs,
possibly rewriting the cell).  This script enumerates small rigid packets of
k base gliders of one head lattice (A: (3,2) or B: (4,-2)), collides each
with small stationary cells (single class, Lemma R4-L1), and records every
CLEAN outcome (one stationary object + one rigid head packet) in a reaction
graph.  It then reports
  (a) fixpoints   h + c -> c' + h   (same head out),
  (b) head cycles  (closed walks in the head graph through clean steps),
  (c) all clean steps, saved for later closure searches.
Usage: nice -n 10 python3 passsearch.py FAM KMAX WMAX [cells,comma,sep]
Output: pass_FAM_KMAX_WMAX.jsonl (resumable: done pairs are skipped).
"""
import json, os, sys, time, itertools
import ptm
from r110lib import build_row

FAM = sys.argv[1]            # 'A' or 'B'
KMAX = int(sys.argv[2])
WMAX = int(sys.argv[3])
CELLS = sys.argv[4].split(',') if len(sys.argv) > 4 else ['C1', 'C2', 'C3']
G = ptm.LIB.gliders[FAM]
P = (G.p, G.d)
OUT = os.path.join(ptm.HERE, f'pass_{FAM}_{KMAX}_{WMAX}.jsonl')


def valid(pl):
    try:
        build_row([ptm.LIB.gliders[n].state_at(t, x, 0) for n, t, x in pl])
        return True
    except ValueError:
        return False


def rigid(pl):
    """The packet alone keeps its shape (no internal interaction)."""
    try:
        res = ptm.simulate(ptm.LIB, pl, 300)
    except (ValueError, RuntimeError):
        return False
    if not res['settled'] or any(p[0] == '?' for p in res['products']):
        return False
    return ptm.canon(res['products']) == ptm.canon(pl)


def packets():
    """All rigid packets of 1..KMAX gliders, span <= WMAX cells at time 0, canonical, unique."""
    seen = set()
    # candidate offsets of one more glider relative to the first: t in [0,p), x in (0, WMAX]
    offs = [(t, x) for t in range(G.p) for x in range(1, WMAX + 1)]
    frontier = [[(FAM, 0, 0)]]
    for k in range(1, KMAX + 1):
        nxt = []
        for pl in frontier:
            key = ptm.canon(pl)
            if key in seen:
                continue
            seen.add(key)
            yield key
            if k == KMAX:
                continue
            last = max(ptm._start(e) for e in pl)
            for t, x in offs:
                e = (FAM, t, x)
                s = ptm._start(e)
                if s <= last + 1 or s - ptm._start(pl[0]) > WMAX:
                    continue
                cand = pl + [e]
                if valid(cand) and rigid(cand):
                    nxt.append(cand)
        frontier = nxt


done = set()
if os.path.exists(OUT):
    for line in open(OUT):
        j = json.loads(line)
        done.add((json.dumps(j['h']), j['c']))
t0 = time.time()
n = 0
with open(OUT, 'a') as f:
    for key in packets():
        n += 1
        for c in CELLS:
            if (json.dumps(key), c) in done:
                continue
            r = ptm.react(key, c)
            rec = {'h': key, 'c': c, 'kind': r['kind']}
            if r['kind'] in ('clean', 'absorbed'):
                rec.update(c_out=r['cell'], dx=r['dx'])
            if r['kind'] == 'clean':
                rec.update(h_out=r['head'], dir_out=ptm.direction(r['head']),
                           fix=(r['head'] == key))
                if r['head'] == key:
                    print('FIXPOINT', rec, flush=True)
            f.write(json.dumps(rec) + '\n')
        if n % 50 == 0:
            f.flush()
            print(n, 'packets', round(time.time() - t0), 's', flush=True)
print('total packets', n, round(time.time() - t0), 's')
