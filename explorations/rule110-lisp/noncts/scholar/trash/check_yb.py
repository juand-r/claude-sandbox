"""Independent test of architect's order-independence (Yang-Baxter) claim:
a C1 messenger, a 4-F memory train and a train of Ebars can all cross each
other cleanly in ANY order, for the right choice of classes.

Construction (my builder, Martinez strings):
   C1 - k tiles - F-train (4 x F(A,f1_1), gap 2 tiles) - 6 tiles -
   Ebar-train (m Ebars, gap j tiles)
Step 1: find (Ebar phase y, gap j) such that the Ebar train alone crosses
        the F train cleanly.
Step 2: for C1 phases c and offsets k0, keep configurations whose final
        census is exactly {C1, 4 F, m Ebar} (all crossings clean).
Step 3: vary the messenger's entry by k = k0 + 4 i (4 tiles = 56 cells
        preserves the C1 x F and C1 x Ebar classes in the absence of
        crossings) and count clean outcomes. Order independence predicts
        all clean; a pairwise-clean but order-dependent choice fails for
        some k.
Usage: python check_yb.py M   (M = number of Ebars, default 6)"""
import sys
import r110check as r

M = int(sys.argv[1]) if len(sys.argv) > 1 else 6
TRAIN = "-2e-".join(["F(A,f1_1)"] * 4)


def ebar_train(y, j, m):
    return f"-{j}e-".join([y] * m)


def clean(spec, want, T):
    e, l, _ = r.outcome(spec, T=T, pad=T // 14 + 150)
    return e == l and sorted(l) == sorted(want), l


def main():
    ys = [k for k in r.PHASES if k.startswith("E-(")]
    step1 = []
    for y in ys:
        for j in (3, 4, 5, 6):
            spec = f"{TRAIN}-6e-{ebar_train(y, j, M)}"
            ok, _ = clean(spec, ["F"] * 4 + ["E-"] * M, T=1600 + 150 * M)
            if ok:
                step1.append((y, j))
    print("step1 Ebar trains crossing the F train cleanly:", len(step1), step1[:8], flush=True)
    want = ["C1"] + ["F"] * 4 + ["E-"] * M
    for y, j in step1[:6]:
        for c in [k for k in r.PHASES if k.startswith("C1(")]:
            for k0 in (1, 2, 3, 4):
                spec = f"{c}-{k0}e-{TRAIN}-6e-{ebar_train(y, j, M)}"
                ok, l = clean(spec, want, T=3000 + 150 * M)
                if not ok:
                    continue
                res = []
                for i in range(8):
                    k = k0 + 4 * i
                    spec2 = f"{c}-{k}e-{TRAIN}-6e-{ebar_train(y, j, M)}"
                    ok2, l2 = clean(spec2, want, T=3000 + 150 * M + 600 * i)
                    res.append(ok2)
                print(f"y={y} j={j} C1={c} k0={k0}: clean for k=k0+4i, i=0..7: "
                      f"{sum(res)}/8 {res}", flush=True)


if __name__ == "__main__":
    main()
