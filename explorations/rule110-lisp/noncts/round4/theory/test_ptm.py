"""Differential test of ptm.react against the census (lnscan2.jsonl), which
used collider's collide_pair directly (its own class enumeration and
placement).  For N random census pairs: same product cell, same moving
product names, same cleanliness.  Control: the same heads against a
DIFFERENT cell must disagree with the census record in most cases (the test
can fail).  Usage: python3 test_ptm.py [N] [seed]
"""
import json, random, sys
import ptm

N = int(sys.argv[1]) if len(sys.argv) > 1 else 120
rnd = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
recs = [json.loads(l) for l in open(ptm.HERE + '/lnscan2.jsonl')]
recs = [r for r in recs if 'err' not in r and r['settled']]
sample = rnd.sample(recs, N)


def _strip(n):
    """auto-registered names get #k suffixes in order of discovery, which
    differs between processes; compare up to that suffix."""
    return n.split('#')[0]


def summary_census(r):
    st = sorted(_strip(p[0]) for p in r['S_out'])
    mv = sorted(_strip(p[0]) for p in r['H_out'])
    return st, mv


def summary_ptm(res):
    raw = res.get('raw') or []
    st = sorted(_strip(p[0]) for p in raw if ptm.period(p[0]) == ptm.STAT)
    mv = sorted(_strip(p[0]) for p in raw if ptm.period(p[0]) != ptm.STAT)
    return st, mv


agree = 0
bad = []
for r in sample:
    res = ptm.react(ptm.canon([(r['H'], 0, 0)]), r['S'])
    if 'why' in res:
        bad.append((r['H'], r['S'], res['why']))
        continue
    census_kind = ('clean' if r['H_out'] else 'absorbed') if r['clean'] else 'dirty'
    if summary_ptm(res) == summary_census(r) and res['kind'] == census_kind:
        agree += 1
    else:
        bad.append((r['H'], r['S'], summary_ptm(res), summary_census(r)))
print(f'agree {agree}/{N}')
for b in bad[:10]:
    print('DISAGREE', b)
# control: swap the cell for another of the census cells
cells = sorted({r['S'] for r in recs})
ctrl_agree = 0
for r in sample:
    other = rnd.choice([c for c in cells if c != r['S']])
    res = ptm.react(ptm.canon([(r['H'], 0, 0)]), other)
    if summary_ptm(res) == summary_census(r):
        ctrl_agree += 1
print(f'control (wrong cell) agrees {ctrl_agree}/{N}  (should be small)')
