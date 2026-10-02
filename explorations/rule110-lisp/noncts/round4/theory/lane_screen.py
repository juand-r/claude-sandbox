"""Row 7 screen: can the F lane host an abort by class shift (Lemma N2)?

Data: collider's verified catalog (../../collider/reactions.json, read
only): F (X) against every catalogued Ebar-speed packet Y (single Ebar and
83 Ebar pairs / compounds), all 12 classes each.  A rigid Ebar packet has
period P_Ebar, so every such packet meets F in the same class group
G = Lambda / <P_F, P_Ebar>, which is Z_6 x Z_2 (Lambda = ether lattice with
basis (7,0), (3,2); P_F = (6,-2), P_Ebar = (6,-4) in that basis; the map
(a, b) -> (a mod 6, b mod 2) has kernel exactly <P_F, P_Ebar>).
Class labels: the catalog's Y_event differences (in Lambda) mapped by that
homomorphism (relative to the packet's class 0).
Per packet type: CROSS = classes whose products are the same packet + F;
KICK = classes whose products are F alone (the packet is absorbed and F
displaced: address's "lock and key" kicks).
Lemma N2 (THEORY s.4.2) with ONE packet type for all kicks: a k-marker
design exists iff there are f != 0 with kick + f in CROSS and e_0..e_{k-1}
in G with  e_r - e_j in (CROSS & (CROSS - f)) - kick  (j < r),
           e_r - e_j in (CROSS - f) - kick            (j > r),
and a gate class g with g - e_j in CROSS for all j.
Usage: python3 lane_screen.py  -> lane_screen.log
"""
import json, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, '../../collider/reactions.json')))
M1, M2 = 6, 2


def label(dt, dx):
    assert (dx + 4 * dt) % 14 == 0, (dt, dx)       # in the ether lattice
    b = dx // 2
    a7 = dt - 3 * b
    assert a7 % 7 == 0
    return ((a7 // 7) % M1, b % M2)


def add(u, v):
    return ((u[0] + v[0]) % M1, (u[1] + v[1]) % M2)


def neg(u):
    return ((-u[0]) % M1, (-u[1]) % M2)


G = [(a, b) for a in range(M1) for b in range(M2)]
ZERO = (0, 0)


def feasible(cross, kick, k):
    cross = set(cross)
    for f in G:
        if f == ZERO or add(kick, f) not in cross:
            continue
        up = {add(c, neg(kick)) for c in cross if add(c, f) in cross}      # (CROSS & (CROSS - f)) - kick
        down = {add(c, neg(kick)) for c in G if add(add(c, f), (0, 0)) in cross}  # (CROSS - f) - kick
        if not up:
            continue
        for rest in itertools.product(G, repeat=k - 1):
            e = (ZERO,) + rest
            ok = True
            for r in range(k):
                for j in range(k):
                    if j == r:
                        continue
                    d = add(e[r], neg(e[j]))
                    if (j < r and d not in up) or (j > r and d not in down):
                        ok = False
                        break
                if not ok:
                    break
            if ok and any(all(add(g, neg(e[j])) in cross for j in range(k)) for g in G):
                return f, e
    return None


def main():
    shapes = {}
    for r in R:
        if r['X'] != 'F' or not r['Y'].startswith('Ebar'):
            continue
        shapes.setdefault(r['Y'], []).append(r)
    n_kick = n_two = 0
    feas = {3: [], 5: []}
    lines = []
    for Y, rs in sorted(shapes.items()):
        rs.sort(key=lambda r: r['cls'])
        ev0 = rs[0]['Y_event']
        lab = {r['cls']: label(r['Y_event'][0] - ev0[0], r['Y_event'][1] - ev0[1]) for r in rs}
        assert len(set(lab.values())) == len(rs) == 12, (Y, lab)
        cross = {lab[r['cls']] for r in rs if r['kind'] == 'crossing' and sorted(r['out']) == sorted([Y, 'F'])}
        kick = [lab[r['cls']] for r in rs if r['out'] == ['F']]
        n_kick += bool(kick)
        n_two += len(cross) >= 2
        res = {}
        for kc in kick:
            for k in (3, 5):
                w = feasible(cross, kc, k)
                if w is not None:
                    res.setdefault(k, (kc, w))
        for k in (3, 5):
            if k in res:
                feas[k].append(Y)
        lines.append(f'{Y}: |CROSS| = {len(cross)}, kick classes {kick}, feasible k=3: {res.get(3)}, k=5: {res.get(5)}')
    print('\n'.join(lines))
    print(f'\npacket types vs F: {len(shapes)}; with a kick (absorption) class: {n_kick}; '
          f'with >= 2 crossing classes: {n_two}')
    print(f'single-type class-shift abort feasible with 3 markers: {len(feas[3])} {feas[3][:8]}')
    print(f'                                  with 5 markers: {len(feas[5])} {feas[5][:8]}')


if __name__ == '__main__':
    main()
