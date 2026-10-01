"""Explore the natural particle TM of Rule 110 (route 12, ptm.py).

For every library head packet (A/D/B lattice) and every blank cell type, run
the natural TM on an all-blank tape (and on a tape with one 'wall' cell of
another type) and report how each run ends:
  dirty     a reaction left something that is not (one cell + one head)
  absorbed  the head was absorbed (one cell, nothing moving)
  escape    the head runs off into blank tape, repeating by translation
  alive     still clean after NMAX steps (interesting: inspect!)
Results: explore.jsonl.  Usage: nice -n 10 python3 explore.py [NMAX]
"""
import json, sys, time, os
import ptm

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore.jsonl')
blanks = ['C1', 'C2', 'C3']
heads = [n for n, g in ptm.LIB.gliders.items() if (g.p, g.d) in ptm.RIGHT | ptm.LEFT]
t0 = time.time()
with open(OUT, 'w') as f:
    for b in blanks:
        for hn in heads:
            k = ptm.canon([(hn, 0, 0)])
            for wall in [None] + blanks:
                if wall == b:
                    continue
                d = ptm.direction(k)
                # wall one cell away on the side the head moves to first
                init = {} if wall is None else {(3 if d == 'R' else -3): wall}
                r = ptm.run(k, b, init=init, start=0, nmax=NMAX)
                rec = {k2: r[k2] for k2 in ('outcome', 'steps', 'heads', 'cells', 'lo', 'hi', 'drift')}
                rec.update(head=hn, blank=b, wall=wall)
                f.write(json.dumps(rec) + '\n')
                if r['outcome'] == 'alive' or r['steps'] >= 20:
                    print(rec, flush=True)
        f.flush()
        print('blank', b, 'done', round(time.time() - t0), 's, cache', len(ptm._cache), flush=True)
