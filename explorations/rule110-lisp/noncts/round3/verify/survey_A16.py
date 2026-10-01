"""Check coupler 06:02 item 3 with my code: A + E^n (n = 1..15) and
A^2..A^4 + E^1..6, all classes (t0 < 3 x 14 offsets), T = 2500: list
outcomes; flag any outcome containing a left-mover (B, Bbar, G) together
with exactly one counter."""
import v3
from survey_left import survey
import survey_left
survey_left.T = 2500
LEFTM = {"B", "Bbar", "Bhat", "G"}
for L, ns in (("A", range(1, 16)), ("A^2", range(1, 7)), ("A^3", range(1, 7)), ("A^4", range(1, 7))):
    for n in ns:
        R = "E" if n == 1 else f"E^{n}"
        res = survey(L, R)
        flag = [k for k in res if any(p in LEFTM for p in k.split(" + "))]
        print(f"{L} + {R}: " + " | ".join(f"{k} x{len(v)}" for k, v in res.items())
              + (f"   LEFT-MOVER: {flag}" if flag else ""), flush=True)
