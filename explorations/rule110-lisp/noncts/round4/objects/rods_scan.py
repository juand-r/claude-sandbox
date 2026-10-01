"""Which periodic backgrounds X (backgrounds_p20.txt) can form rods in ether:
interfaces ether|X (front) and X|ether (back) moving with a common period
(P, D) (glider speeds of the library). wallsat.interfaces, W <= WMAX.
Usage: python3 rods_scan.py WMAX out.jsonl"""
import json, sys
import wallsat as WS, cone
ETH = '11111000100110'
WMAX, OUT = int(sys.argv[1]), sys.argv[2]
vecs = {'E(-4/15)': [(15, -4), (30, -8)], 'B(-1/2)': [(4, -2), (12, -6)], 'G(-1/3)': [(42, -14)],
        'C(0)': [(7, 0)], 'F(-1/9)': [(36, -4)], 'A(2/3)': [(3, 2)], 'D(1/2)': [(10, 2)]}
bE = cone.Background(ETH)
done = set()
try:
    for l in open(OUT):
        r = json.loads(l); done.add((r['tile'], r['speed']))
except FileNotFoundError:
    pass
for line in open('backgrounds_p20.txt'):
    p, t, sh, dens, tile = line.split()
    if tile in ('0', ETH) or int(p) == 14 and tile == '00010011011111':
        continue
    bX = cone.Background(tile)
    for name, PDs in vecs.items():
        if (tile, name) in done:
            continue
        PD = next((pd for pd in PDs if WS.lattice_ok(bX, *pd) and WS.lattice_ok(bE, *pd)), None)
        if PD is None:
            continue
        f = WS.interfaces(ETH, tile, PD[0], PD[1], WMAX)
        b = WS.interfaces(tile, ETH, PD[0], PD[1], WMAX)
        rec = {'tile': tile, 'p': int(p), 'speed': name, 'PD': PD, 'WMAX': WMAX,
               'fronts': len(f), 'backs': len(b),
               'front_ex': min(f.items(), key=lambda z: z[1][0]) if f else None,
               'back_ex': min(b.items(), key=lambda z: z[1][0]) if b else None}
        print(json.dumps(rec), flush=True)
        with open(OUT, 'a') as fh:
            fh.write(json.dumps(rec) + '\n')
