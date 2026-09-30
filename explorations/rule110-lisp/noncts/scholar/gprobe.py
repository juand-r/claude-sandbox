"""G as a zero-test probe for the E_n counter.
1. G + E_n for n = 1..6, all G phases, 2 separations: does G cross E_n
   (n >= 2) and react with E_1?
2. After a G has crossed E_n, does an A in the DEC class (label (20,10) of
   ecount.py) still decrement? (the crossing displaces E_n)"""
from collections import defaultdict
import r110check as r
import ecount as EC


def en(n):
    return "E(A,f1_1)" + (("-6e-" + "-4e-".join(["B(f1_1)"] * (n - 1))) if n > 1 else "")


def part1():
    gs = [k for k in r.PHASES if k.startswith("G(")]
    for n in range(4, 7):
        out = defaultdict(int)
        for g in gs:
            for m in (10, 11):
                spec = f"{en(n)}-{m}e-{g}"
                T = 2600 + 300 * n
                e, l, _ = r.outcome(spec, T=T, pad=int(0.13 * T) + 80)
                out[tuple(sorted(l)) + (() if e == l else ("UNSETTLED",))] += 1
        print(f"E_{n} + G:", dict(out), flush=True)


def part2():
    # A(f3_1) has label (20,10) for any m (see ecount.label)
    for n in range(1, 6):
        out = defaultdict(int)
        for g in [k for k in r.PHASES if k.startswith("G(")][:6]:
            spec = f"A(f3_1)-{160 + 4 * n}e-{en(n)}-10e-{g}"
            T = 4200 + 300 * n
            e, l, _ = r.outcome(spec, T=T, pad=int(0.13 * T) + 200)
            out[tuple(sorted(l)) + (() if e == l else ("UNSETTLED",))] += 1
        print(f"A(DEC class) after G probe, E_{n}:", dict(out), flush=True)


if __name__ == "__main__":
    print("label of A(f3_1):", EC.label("A(f3_1)", 160))
    part1()
    part2()
