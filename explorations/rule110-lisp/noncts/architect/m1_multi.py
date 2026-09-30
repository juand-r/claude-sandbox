"""Lane with SEVERAL messengers: 4-F train, 3 C1 messengers, 16 Ebars.
Consecutive messengers (the next one further left) must meet every F and
every Ebar in the lane classes, i.e. (derived from single displacements)
  M_{j+1} - M_j = v  with  v = f_C1(F) ... solved numerically below by
  requiring the class of F vs M_{j+1} (after F crossed M_j) and of Ebar
  vs M_{j+1} (after the Ebar crossed M_j) to be the lane classes.
Then the whole configuration is simulated for several timings."""
from m1_yb import design, build, M, kMF, kFS, kMS
from yb import disp
from rx import cls_of, run, LIB

cF, fC = disp(M, "F", kMF)       # C1 disp, F disp (C1 x F class 1)
cE, eC = disp(M, "Ebar", kMS)    # C1 disp, Ebar disp (C1 x Ebar class 1)


def lane_ok(v):
    """Messenger M1 = M0 + v (to the left). F that crossed M0 meets M1;
    Ebar that crossed M0 meets M1."""
    from rx import canonical_reps
    rF = canonical_reps(LIB, M, "F")[kMF]          # F rel to M0 (class kMF)
    # F after crossing M0: F + fC ; rel to M1 = rF + fC - v
    try:
        k1 = cls_of(M, (0, 0), "F", (rF[0] + fC[0] - v[0], rF[1] + fC[1] - v[1]))
    except AssertionError:
        return False
    rE = canonical_reps(LIB, M, "Ebar")[kMS]
    try:
        k2 = cls_of(M, (0, 0), "Ebar", (rE[0] + eC[0] - v[0], rE[1] + eC[1] - v[1]))
    except AssertionError:
        return False
    return k1 == kMF and k2 == kMS


if __name__ == "__main__":
    vs = [(t, x) for t in range(0, 7) for x in range(-160, -30) if lane_ok((t, x))]
    print("messenger spacings (first few):", vs[:6], flush=True)
    v = min(vs, key=lambda q: abs(q[1] + 60))
    G, S = design()
    ok = 0
    for a in range(0, 30, 6):
        pl = build(G, S, a)
        M0 = pl[0]
        Ms = [M0, (M, M0[1] + v[0], M0[2] + v[1]), (M, M0[1] + 2 * v[0], M0[2] + 2 * v[1])]
        pl = Ms + pl[1:]
        try:
            prods = run(pl, 14000)
            names = sorted(p[0] for p in prods)
            good = names == sorted([M] * 3 + ["F"] * 4 + ["Ebar"] * 16)
        except Exception as e:
            good, names = False, str(e)[:100]
        ok += good
        print("a", a, "v", v, "CLEAN" if good else names, flush=True)
    print(f"{ok}/5 clean")
