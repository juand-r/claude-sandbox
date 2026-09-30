"""Three-body (Yang-Baxter-type) check for a messenger M (v=0), memory F
(v=-1/9) and stream S (v=-4/15), all pairwise clean crossings.

Initial order M < F < S. Two event orders are possible:
  (1) F-M, S-M, S-F        (2) S-F, S-M, F-M
With the incoming classes fixed, the class of each meeting in each order
follows from the single-crossing displacements. A triple of incoming
classes is 'consistent' if all six meetings are clean-crossing classes.
Prints every consistent triple. Also records whether the final positions
agree (they always do if the classes are equal in both orders)."""
from yb import sol_classes, disp
from rx import *


def cls_rel(X, Y, rel):
    try:
        return cls_of(X, (0, 0), Y, rel)
    except AssertionError:
        return None


def check(M):
    out = []
    SFM = sol_classes(M, "F")
    SFS = sol_classes("F", "Ebar")
    SMS = sol_classes(M, "Ebar")
    D = {}
    for k in SFM:
        D["MF", k] = disp(M, "F", k)       # (dM, dF)
    for k in SFS:
        D["FS", k] = disp("F", "Ebar", k)  # (dF, dS)
    for k in SMS:
        D["MS", k] = disp(M, "Ebar", k)    # (dM, dS)
    for kMF in SFM:
        dM_F, dF_M = D["MF", kMF]
        for kFS in SFS:
            dF_S, dS_F = D["FS", kFS]
            for kMS in SMS:
                dM_S, dS_M = D["MS", kMS]
                rMF = canonical_reps(LIB, M, "F")[kMF]
                rFS = canonical_reps(LIB, "F", "Ebar")[kFS]
                rMS = canonical_reps(LIB, M, "Ebar")[kMS]
                # order 1: F-M fresh; S-M with M displaced by F; S-F with
                # S displaced by M and F displaced by M
                o1 = (kMF,
                      cls_rel(M, "Ebar", (rMS[0] - dM_F[0], rMS[1] - dM_F[1])),
                      cls_rel("F", "Ebar", (rFS[0] + dS_M[0] - dF_M[0],
                                            rFS[1] + dS_M[1] - dF_M[1])))
                # order 2: S-F fresh; S-M with S displaced by F; F-M with F
                # displaced by S and M displaced by S
                o2 = (cls_rel(M, "F", (rMF[0] + dF_S[0] - dM_S[0],
                                       rMF[1] + dF_S[1] - dM_S[1])),
                      cls_rel(M, "Ebar", (rMS[0] + dS_F[0], rMS[1] + dS_F[1])),
                      kFS)
                ok1 = o1[1] in SMS and o1[2] in SFS
                ok2 = o2[0] in SFM and o2[1] in SMS
                out.append(((kMF, kFS, kMS), o1, o2, ok1, ok2))
    return out


if __name__ == "__main__":
    for M in ["C1", "C2"]:
        for trip, o1, o2, ok1, ok2 in check(M):
            tag = "CONSISTENT" if ok1 and ok2 else ("order1 ok" if ok1 else "") + (" order2 ok" if ok2 else "")
            print(M, "in(MF,FS,MS)=", trip, "order1 (MF,MS,FS)=", o1,
                  "order2=", o2, tag)
