"""E_n as a unary counter: B increments (single class), A decrements.

Construction: E(A,f1_1) at the origin, k B's behind it (they catch up and
extend it to E_{k+1}), and one A far to the left. Because B x E_n is
single-class, the trajectory of E_{k+1} is a fixed shift of E_1's, whatever
the B timing, so the class of the A is labelled relative to E_1's anchor:
    label = (anchor(A) - anchor(E_1)) mod <P_A, P_E> = <(3,2),(15,-4)>
(3 labels). For each n and label we record the outcome; the question is
whether one label decrements every E_n (then a fixed A stream is a DEC for
any counter value) or whether the DEC label drifts with n.

Run: python ecount.py [nmax]"""
import sys
from collections import defaultdict
import classes as C
import r110check as r

P_A, P_E = (3, 2), (15, -4)


def label(a_phase, m):
    """Class label of A(a_phase) placed m tiles left of E(A,f1_1)."""
    ta, xa = C.anchor(a_phase)
    te, xe = C.anchor("E(A,f1_1)")
    off = len(r.PHASES[a_phase]) + 14 * m        # column where E starts
    v = (te - ta, off + xe - xa)                 # E_1 anchor minus A anchor
    return C.reduce_mod((-v[0], -v[1]), P_A, P_E)


def main(nmax=7):
    for k in range(0, nmax):
        bs = ("-6e-" + "-4e-".join(["B(f1_1)"] * k)) if k else ""
        out = defaultdict(set)
        for a in ["A(f1_1)", "A(f2_1)", "A(f3_1)"]:
            for m in range(100 + 4 * k, 103 + 4 * k):
                spec = f"{a}-{m}e-E(A,f1_1){bs}"
                e, l, _ = r.outcome(spec, T=2600 + 400 * k, pad=330 + 30 * k)
                out[label(a, m)].add(tuple(sorted(l)) + (() if e == l else ("UNSETTLED",)))
        print(f"E_{k + 1} + A:", {lab: sorted(v) for lab, v in sorted(out.items())}, flush=True)


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
