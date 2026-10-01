"""Natural particle TM from EVERY small train (route 12, zig-zag search).

verify (board 23:19): a universal particle TM needs, by pigeonhole, a cycle
of the full reaction walk (passes AND reflections) with net crossing, not
necessarily a pure pass cycle.  The direct way to look for such walks is to
run the natural TM (ptm.run) from many heads on uniform blank tapes and see
whether any run survives many clean steps.

Heads: all trains of width <= 30 on the A (3,2), D (10,2) and B (4,-2)
lattices (shuttle's and my SAT enumerations).  A raw train is first turned
into the library's own representation (simulate it alone, type it), so all
later steps use cached exact reactions (ptm.react).
Tapes: uniform C1, C2 or C3 (blank), head starting next to cell 0.
Output explore2.jsonl; prints every run with >= 4 clean steps.
Usage: nice -n 10 python3 explore2.py [NMAX]
"""
import json, os, sys, time
import ptm
from collide import products_of
from r110lib import build_row, _pack_batch, _unpack_batch, _step_state

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 200
OUT = os.path.join(ptm.HERE, 'explore2.jsonl')
SRCS = [(3, 2, os.path.join(ptm.HERE, '../shuttle/trains_3_2_30.jsonl')),
        (10, 2, os.path.join(ptm.HERE, '../shuttle/trains_10_2_30.jsonl')),
        (4, -2, os.path.join(ptm.HERE, 'trains_4_-2_30.jsonl'))]


def as_head(tr):
    row, x0 = build_row([(tr['bits'], 0, tr['pR'], 0)], pad=120)
    s = _pack_batch(row[None, :])
    for T in range(1, 4 * tr['p'] + 1):
        s = _step_state(s)
    ok, prods, _ = products_of(ptm.LIB, _unpack_batch(s, 1)[0], x0, T)
    if not ok or any(ptm.period(p[0]) != (tr['p'], tr['d']) for p in prods):
        return None
    return ptm.canon(prods)


def main():
    t0 = time.time()
    n = 0
    with open(OUT, 'w') as f:
        for p, d, src in SRCS:
            for i, line in enumerate(open(src)):
                tr = json.loads(line)
                key = as_head(tr)
                if key is None:
                    f.write(json.dumps({'p': p, 'd': d, 'i': i, 'outcome': 'not-a-head'}) + '\n')
                    continue
                for blank in ('C1', 'C2', 'C3'):
                    r = ptm.run(key, blank, nmax=NMAX)
                    rec = {k: r[k] for k in ('outcome', 'steps', 'heads', 'cells', 'lo', 'hi', 'drift')}
                    rec.update(p=p, d=d, i=i, blank=blank)
                    f.write(json.dumps(rec) + '\n')
                    if r['steps'] >= 4:
                        print(rec, [t[2] for t in r['trace'][:12]], flush=True)
                n += 1
                if n % 500 == 0:
                    f.flush()
                    print(n, 'heads', round(time.time() - t0), 's, cache', len(ptm._cache), flush=True)
    print('done', n, round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
