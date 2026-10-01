"""Window behaviour table: for each library G-speed packet, its outcomes
on E (round-3 coupler scan_reflect_M1.jsonl) and on E^2 (scan_e2.jsonl,
mine). Prints packets that are NEUTRAL on E^2 (single product E^2) in
some class, with their outcomes on E. Usage: python wtable.py [all]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dl import LIB, CHAIN, COUP, HERE


def nm(p):
    return ('E^%d' % (CHAIN.index(p) + 1)) if p in CHAIN else p


def load():
    M1 = {}
    for l in open(os.path.join(COUP, 'scan_reflect_M1.jsonl')):
        r = json.loads(l)
        M1[r['Y']] = r
    M2 = {}
    for l in open(os.path.join(HERE, 'scan_e2.jsonl')):
        r = json.loads(l)
        M2[r['Y']] = r
    return M1, M2


if __name__ == "__main__":
    M1, M2 = load()
    for Y, r in M2.items():
        if 'rows' not in r:
            print("ERR", Y, r.get('error'))
            continue
        neu = [row['cls'] for row in r['rows'] if row['settled'] and
               [p[0] for p in row['products']] == ['E^2']]
        if neu or 'all' in sys.argv:
            eo = [(row['cls'], [nm(p[0]) for p in row['products']]) for row in M1[Y]['rows']]
            e2 = [(row['cls'], [nm(p[0]) for p in row['products']]) for row in r['rows']]
            print(Y, "slip", LIB.gliders[Y].slip, "| E^2:", e2, "| E:", eo)
