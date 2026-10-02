"""Graph search (cycles.py) on shuttle's exhaustive single-wall tables
(../shuttle/bounce_table.jsonl, format in ../shuttle/export.py).

Identities: a wall is its time-phase canonical form (wall_canon /
wall_out_canon); a head is (p, d, canonical form).  Input heads' canonical
forms are computed with shuttle's own canon_bits (imported read-only) so
inputs and outputs match.  Only heads whose period is EXACTLY (3,2),
(10,2) or (4,-2) are kept as states (verify 00:0x scope warning: other
outputs, e.g. Ebar or F trains, are multi-class against a wall, so the
table's single entry does not describe them); a run that produces such a
head ends as 'unknown'.
Usage: nice -n 10 python3 tables_search.py   -> tables_search.log
"""
import json, os, sys, math, time
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
SH = os.path.join(HERE, '../shuttle')
sys.path.insert(0, SH)
_cwd = os.getcwd(); os.chdir(SH)
from bgraph import canon_bits            # read-only reuse of shuttle's canonical form
os.chdir(_cwd)
import cycles

LATT = {(3, 2): 'R', (10, 2): 'R', (4, -2): 'L'}


def load(path=os.path.join(SH, 'bounce_table.jsonl')):
    T = cycles.DictTable()
    cache = {}
    kinds = Counter()
    for line in open(path):
        j = json.loads(line)
        h = j['head']
        key = (h['p'], h['d'], h['bits'], h['pR'])
        if key not in cache:
            cache[key] = (h['p'], h['d']) + tuple(canon_bits(h['bits'], h['pR'], h['p']))
        hid = cache[key]
        hdir = LATT.get((h['p'], h['d']))
        if hdir is None:
            continue
        wid = tuple(j['wall_canon'])
        kind = j['kind']
        kinds[(j['side'], kind)] += 1
        if kind in ('reflect', 'pass'):
            ho = j['head_out']
            pd = (ho['p'], ho['d'])
            if pd not in LATT:
                T.add(hid, hdir, wid, 'nonlattice-' + kind)
                continue
            hoid = pd + tuple(j['head_out_canon'])
            T.add(hid, hdir, wid, kind, tuple(j['wall_out_canon']), j['wall_out']['dx'], hoid, LATT[pd])
        else:
            T.add(hid, hdir, wid, kind)
    return T, kinds


def main():
    t0 = time.time()
    T, kinds = load()
    print('rows by (side, kind):', dict(kinds))
    print('heads', len(T.dir), 'walls', len(T.walls()), 'entries', len(T.t), round(time.time() - t0), 's', flush=True)
    found, lengths = cycles.bouncers(T, nmax=400)
    print('perpetual bouncers:', len(found))
    for f in found[:20]:
        print('  ', f)
    print('bounce run lengths (steps before death):', dict(sorted(lengths.items())))
    rat = cycles.ratchets(T, nmax=400)
    esc = [r for r in rat if r[2][0] in ('ESCAPE', 'ALIVE')]
    print('ratchet runs on uniform tapes with >= 4 steps:', len(rat), '; escapes/alive:', len(esc))
    for r in sorted(rat, key=lambda r: -r[2][1])[:15]:
        print('  ', r[0][:2], r[1][:1], r[2])
    print('done', round(time.time() - t0), 's')


if __name__ == '__main__':
    main()
