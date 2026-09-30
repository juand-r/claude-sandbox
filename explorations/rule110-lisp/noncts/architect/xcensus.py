"""Census view of a crossing-counter run: after a fixed-stream program,
type every defect in the final row with the project's census
(../../census.py: C, A, E families) and check that the remaining defects
are F's (invariant under F's period (36,-4)). The register gap is also
read directly from the row."""
import sys
import numpy as np
sys.path.insert(0, "../..")
from census import census, MAX_DT
from xstream import build, SLOT_LEN
from rx import history

if __name__ == "__main__":
    prog = sys.argv[1].split(",") if len(sys.argv) > 1 else ["INC", "INC", "DEC", "INC", "NOP", "INC"]
    pl = build(prog)
    T = 36 * (SLOT_LEN + 5) * len(prog) + 6000
    H, x0 = history(pl, T)
    tail = H[-(MAX_DT + 40):]
    cs = census(tail)
    kinds = [k for _, _, k in cs]
    print("program", prog, "T", T)
    print("census:", {k: kinds.count(k) for k in sorted(set(kinds))})
    last, then = tail[-1], tail[-1 - 36]
    Fpos = []
    for a, b, k in cs:
        if k == "?":
            ok = np.array_equal(last[a - 2:b + 2], then[a + 2:b + 6])
            print("  '?' defect at", a + x0, "width", b - a, "F-invariant" if ok else "NOT F-invariant")
            if ok:
                Fpos.append(a + x0)
    if len(Fpos) == 2:
        n = prog.count("INC") - prog.count("DEC")
        print("F gap in row:", Fpos[1] - Fpos[0], "expected about %.1f (n=%d)" % (43 + 9.33 * n, n))
