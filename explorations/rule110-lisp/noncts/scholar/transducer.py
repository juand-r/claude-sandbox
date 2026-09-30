"""Distance-register transducer for two C1 markers and single Ebars.

Register = two stationary C1 markers M_L (left) and M_R (right); value =
their gap. A stream Ebar arrives from the right, meets M_R, then (if it
crossed) M_L. Both C1 x Ebar crossings displace the marker, by different
amounts in the two crossing classes (dist_register.py), so the gap can
change.

State of the register as seen by Ebars: the residue of the anchor vector
M_R - M_L modulo the lattice <P_C, P_Ebar> = <(7,0),(30,-8)> (4 residues
in the relevant coset). Input: the class of the Ebar relative to M_R (4
classes). This script measures, by direct simulation, for every (residue,
class) with the Ebar crossing both markers:
    gap change, the marker displacements, the new residue,
and whether the Ebar crossed M_R but reacted with M_L, etc.
Output: a table, plus a check that each entry is a function of
(residue, class) (every entry is sampled several times).
"""
from collections import defaultdict
import classes as C
import locate as L
import r110check as r

P_C, P_E = (7, 0), (30, -8)
T = 1800


def anchor_of(h, t, fam, lo, hi):
    a = L.find(h, t, fam, lo, hi)
    return a


def run():
    table = defaultdict(set)
    samples = defaultdict(int)
    cphases = [k for k in r.PHASES if k.startswith("C1(")]
    ephases = [k for k in r.PHASES if k.startswith("E-(")]
    for cR in cphases:
        for m in (3, 4, 5, 6):
            for y in ephases[::3]:
                spec = f"C1(A,f1_1)-{m}e-{cR}-9e-{y}"
                row, s0 = r.build(spec, pad=260)
                h = r.evolve(row, T)
                aC = sorted(L.find(h, 0, "C1", s0 - 30, s0 + 14 * m + 60), key=lambda a: a[1])
                aE = L.find(h, 0, "E-", s0 + 14 * m, s0 + 14 * (m + 20))
                if len(aC) != 2 or len(aE) != 1:
                    continue
                aL_, aR_ = aC
                resid = C.reduce_mod((aR_[0] - aL_[0], aR_[1] - aL_[1]), P_C, P_E)
                ecls = C.reduce_mod((aE[0][0] - aR_[0], aE[0][1] - aR_[1]), P_C, P_E)
                e, l, _ = r.outcome(spec, T=T, pad=260)
                if e != l:
                    table[(resid, ecls)].add(("UNSETTLED",))
                    continue
                if sorted(l) != ["C1", "C1", "E-"]:
                    table[(resid, ecls)].add(tuple(sorted(l)))
                    samples[(resid, ecls)] += 1
                    continue
                after = sorted(L.find(h, T - 7, "C1", s0 - 80, s0 + 14 * m + 140), key=lambda a: a[1])
                if len(after) != 2:
                    table[(resid, ecls)].add(("anchor?",))
                    continue
                dL = ((after[0][0] - aL_[0]) % 7, after[0][1] - aL_[1])
                dR = ((after[1][0] - aR_[0]) % 7, after[1][1] - aR_[1])
                new = C.reduce_mod((after[1][0] - after[0][0], after[1][1] - after[0][1]), P_C, P_E)
                table[(resid, ecls)].add(("cross", dL, dR, dR[1] - dL[1], new))
                samples[(resid, ecls)] += 1
    for k in sorted(table):
        v = table[k]
        print(f"residue {k[0]} ebar-class {k[1]}  n={samples[k]:2d}  "
              f"{'FUNCTION' if len(v) == 1 else 'NOT A FUNCTION'}  {sorted(v)}")


if __name__ == "__main__":
    run()
