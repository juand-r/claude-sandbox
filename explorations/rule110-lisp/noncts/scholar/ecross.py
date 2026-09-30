"""WARNING (retracted in part): the G rows for n >= 2 are WRONG. The G
started 150+ cells behind E_n and catches it at relative speed 1/15, so it
had not arrived by the end of the run; "E_n + G -> E_n + G" meant "nothing
happened yet". Correct: E_n + G -> E_(n-1) + A^3 (see NOTES.md). The D1, D2,
Bbar and Bhat rows collided and stand.

Which gliders pass or modify E_n (n = 1..3) from either side?
Left side (right-movers): D1, D2. Right side (fast left-movers): G, Bbar,
Bhat (they catch E_n from behind). Outcome types over several phases and
separations; E_n built as E(A,f1_1) + (n-1) B's."""
from collections import defaultdict
import r110check as r


def en(n):
    return "E(A,f1_1)" + (("-6e-" + "-4e-".join(["B(f1_1)"] * (n - 1))) if n > 1 else "")


def main():
    for n in (1, 2, 3):
        for x in ("D1", "D2"):
            out = defaultdict(int)
            for ph in [k for k in r.PHASES if k.startswith(x + "(")][:6]:
                for m in (60, 61):
                    e, l, _ = r.outcome(f"{ph}-{m}e-{en(n)}", T=2800, pad=330)
                    out[tuple(sorted(l)) + (() if e == l else ("UNSETTLED",))] += 1
            print(f"{x} + E_{n}:", dict(out), flush=True)
        for y in ("G", "B-", "B^"):
            out = defaultdict(int)
            for ph in [k for k in r.PHASES if k.startswith(y + "(") and k != "B(A,f4_1)"][:8]:
                for m in (3, 4):
                    spec = f"{en(n)}-{4 + 4 * n}e-{ph}" if n == 1 else f"{en(n)}-{m + 8}e-{ph}"
                    e, l, _ = r.outcome(spec, T=2800, pad=330)
                    out[tuple(sorted(l)) + (() if e == l else ("UNSETTLED",))] += 1
            print(f"E_{n} + {y}:", dict(out), flush=True)


if __name__ == "__main__":
    main()
