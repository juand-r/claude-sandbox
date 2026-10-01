"""Enumerate all (4,-2) (B-lattice) trains of width <= W, every even right
phase, with shuttle's SAT enumerator (imported read-only from
../shuttle/trains.py); output in THIS directory: trains_4_-2_W.jsonl.
Usage: nice -n 10 python3 btrains.py W"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../shuttle'))
_cwd = os.getcwd(); os.chdir(os.path.join(HERE, '../shuttle'))
from trains import enumerate_trains, check_periodic, trim
os.chdir(_cwd)
W = int(sys.argv[1])
p, d = 4, -2
out = os.path.join(HERE, f'trains_{p}_{d}_{W}.jsonl')
seen = set()
with open(out, 'w') as fh:
    for pR in range(0, 14):
        rows = enumerate_trains(p, d, W, pR)
        n = 0
        for r in rows:
            t = ''.join(map(str, trim(r, pR)))
            if (t, pR) in seen:
                continue
            seen.add((t, pR))
            assert check_periodic(r, pR, p, d), ('not periodic', t)
            fh.write(json.dumps(dict(p=p, d=d, pR=pR, bits=t)) + '\n'); n += 1
        print('pR', pR, 'found', len(rows), 'kept', n, flush=True)
