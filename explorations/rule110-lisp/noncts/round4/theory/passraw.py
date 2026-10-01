"""Route 12, Lemma L4 target S1 by exhaustive simulation: does any small
rigid head train PASS a stationary cell and come out as ITSELF?

Heads: shuttle's SAT enumeration of ALL trains of width <= 30 with period
(3,2) (6398, A lattice) or (10,2) (1071, D lattice): read-only from
../shuttle/trains_P_D_30.jsonl (t = 0 row, left ether phase 0, right pR).
Cells: library stationary objects (default C1, C2, C3).
Each pair is ONE collision (Lemma L1: single class).  We build the row
(collider build_row, so ether consistency is checked), run the exact
automaton (collider's packed stepper), and classify the products with
collider's typer.  For every CLEAN pass (one stationary object + moving
objects all of the head's own period, to the right of the cell) we test
whether the outgoing head is the incoming train: signatures (object keys
and relative starts) of the outgoing moving objects over p consecutive
steps are compared with those of the train evolved alone.
Output: passraw_P_D_<cells>.jsonl.  Usage:
  nice -n 10 python3 passraw.py P D [cells,comma,sep] [limit]
Positive control (control_fix): a train against NO cell must be reported
as identical to itself; a negative control: two different trains must not.
"""
import json, os, sys, time
import ptm
from collide import products_of
from r110lib import build_row, _pack_batch, _unpack_batch, _step_state, objects, obj_key, TILE

P_, D_ = int(sys.argv[1]), int(sys.argv[2])
CELLS = sys.argv[3].split(',') if len(sys.argv) > 3 else ['C1', 'C2', 'C3']
LIMIT = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else None
SRC = (os.path.join(ptm.HERE, f'../shuttle/trains_{P_}_{D_}_30.jsonl') if D_ > 0
       else os.path.join(ptm.HERE, f'trains_{P_}_{D_}_30.jsonl'))
OUT = os.path.join(ptm.HERE, f'passraw_{P_}_{D_}_{"-".join(CELLS)}.jsonl')
GAP = 40
CHUNK = 50


def head_state(tr):
    return (tr['bits'], 0, tr['pR'], 0)


def cell_state(cell, after, pR):
    """Library cell at time 0, start >= after, left ether phase matching pR."""
    g = ptm.LIB.gliders[cell]
    b, l, r, s = g.state_at(0, 0, 0)
    # shifting the cell by k cells shifts its start and keeps labels relative
    k0 = after - s
    for k in range(k0, k0 + 2 * TILE):
        if (l - (s + k) - pR) % TILE == 0 and (k % 2 == 0):
            st = g.state_at(0, k, 0)
            if (st[1] - st[3] - pR) % TILE == 0 and st[3] >= after:
                return st
    # fall back: try every shift with the lattice condition only
    for k in range(k0, k0 + 4 * TILE):
        st = g.state_at(0, k, 0)
        if (st[1] - st[3] - pR) % TILE == 0 and st[3] >= after:
            return st
    raise ValueError('no ether-consistent cell placement')


def sigs(state_pack, x0, n, steps, lo=None):
    """Signatures of the moving objects (start >= lo) over `steps` steps."""
    out = []
    s = state_pack
    for _ in range(steps):
        row = _unpack_batch(s, 1)[0]
        objs = [o for o in objects(row) if lo is None or o[0] >= lo]
        if objs:
            a0 = objs[0][0]
            out.append(tuple((obj_key(row, *o), o[0] - a0) for o in objs))
        s = _step_state(s)
    return set(out)


def sigs_left(state_pack, steps, hi):
    out = []
    s = state_pack
    for _ in range(steps):
        row = _unpack_batch(s, 1)[0]
        objs = [o for o in objects(row) if o[1] <= hi]
        if objs:
            a0 = objs[0][0]
            out.append(tuple((obj_key(row, *o), o[0] - a0) for o in objs))
        s = _step_state(s)
    return set(out)


def train_sigs(tr):
    row, x0 = build_row([head_state(tr)], pad=80)
    return sigs(_pack_batch(row[None, :]), x0, 1, P_)


def cell_left_state(cell, before, absR):
    """Library cell at time 0 ending <= before whose RIGHT ether has absolute phase absR."""
    g = ptm.LIB.gliders[cell]
    best = None
    for k in range(-400, 400):
        st = g.state_at(0, k, 0)
        if st[3] + len(st[0]) <= before and (st[2] - st[3] - absR) % TILE == 0:
            best = st
    if best is None:
        raise ValueError('no ether-consistent left cell placement')
    return best


def collide(tr, cell, tmax=2500):
    if D_ > 0:
        hs = head_state(tr)
        cs = cell_state(cell, len(tr['bits']) + GAP, tr['pR'])
    else:
        S = 400
        hs = (tr['bits'], 0, tr['pR'], S)          # same train translated to start S
        cs = cell_left_state(cell, S - GAP, (0 - S) % TILE)
    row, x0 = build_row([hs, cs], pad=int(tmax * 0.7) + 120)
    s = _pack_batch(row[None, :])
    T = 0
    while T < tmax:
        for _ in range(CHUNK):
            s = _step_state(s)
        T += CHUNK
        cur = _unpack_batch(s, 1)[0]
        ok, prods, objs = products_of(ptm.LIB, cur, x0, T)
        if ok:
            return prods, objs, s, x0, T
    return None, None, None, x0, T


def main():
    trains = [json.loads(l) for l in open(SRC)]
    if LIMIT:
        trains = trains[:LIMIT]
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            j = json.loads(line); done.add((j['i'], j['c']))
    t0 = time.time()
    nclean = nfix = 0
    with open(OUT, 'a') as f:
        for i, tr in enumerate(trains):
            tsig = None
            for c in CELLS:
                if (i, c) in done:
                    continue
                try:
                    prods, objs, s, x0, T = collide(tr, c)
                except (ValueError, RuntimeError) as e:
                    f.write(json.dumps({'i': i, 'c': c, 'kind': 'error', 'why': repr(e)}) + '\n'); continue
                rec = {'i': i, 'c': c, 'bits': tr['bits'], 'pR': tr['pR']}
                if prods is None:
                    rec['kind'] = 'unsettled'
                else:
                    st = [p for p in prods if ptm.period(p[0]) == ptm.STAT]
                    mv = [p for p in prods if ptm.period(p[0]) != ptm.STAT]
                    pers = {ptm.period(p[0]) for p in mv}
                    rec['out'] = [p[0] for p in prods]
                    if len(st) == 1 and pers == {(P_, D_)} or (D_ > 0 and len(st) == 1 and pers and pers <= ptm.RIGHT):
                        rec['kind'] = 'pass'
                        nclean += 1
                        if tsig is None:
                            tsig = train_sigs(tr)
                        # moving objects right of the cell
                        cell_end = max(o[1] for o in objs if True)  # placeholder, refined below
                        row = _unpack_batch(s, 1)[0]
                        allobjs = objects(row)
                        # the cell is the stationary object: products are sorted left->right;
                        # moving ones (v>0) are to its right.
                        k = [p[0] for p in prods].index(st[0][0])
                        if D_ > 0:
                            osig = sigs(s, x0, 1, P_, lo=allobjs[k][1])
                        else:
                            osig = sigs_left(s, P_, allobjs[k][0])
                        rec['fix'] = bool(tsig & osig)
                        if rec['fix']:
                            nfix += 1
                            print('FIXPOINT', rec, flush=True)
                    elif len(st) == 1 and pers and pers <= (ptm.LEFT if D_ > 0 else ptm.RIGHT):
                        rec['kind'] = 'reflect'
                    elif len(st) == 1 and not mv:
                        rec['kind'] = 'absorbed'
                    else:
                        rec['kind'] = 'dirty'
                f.write(json.dumps(rec) + '\n')
            if i % 200 == 0:
                f.flush()
                print(i, 'trains', round(time.time() - t0), 's; passes', nclean, 'fixpoints', nfix, flush=True)
    print('done', len(trains), 'trains; passes', nclean, 'fixpoints', nfix)


def controls():
    trains = [json.loads(l) for l in open(SRC)][:40]
    a, b = trains[0], trains[1]
    sa, sb = train_sigs(a), train_sigs(b)
    # train vs itself shifted in time by evolving: must intersect
    row, x0 = build_row([head_state(a)], pad=200)
    s = _pack_batch(row[None, :])
    for _ in range(3 * P_ + 1):
        s = _step_state(s)
    later = sigs(s, x0, 1, P_)
    print('control: train vs itself later ->', bool(sa & later), '(must be True)')
    print('control: two different trains ->', bool(sa & sb), '(must be False)')


if __name__ == '__main__':
    if len(sys.argv) > 4 and sys.argv[4] == 'controls':
        controls()
    else:
        main()
