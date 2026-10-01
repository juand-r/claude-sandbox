"""M2 validation: take the stream chosen by adaptive_ca.py (JSON), run it for
inputs v = 0..VTEST (including values the assembler never saw), compare with
the abstract model, and run a negative control (one slot moved to another
phase class). Exact CA, my typer. Also checks the result is stable between T
and T + 3000 (no unfinished collisions)."""
import json, sys
import vlib
import adaptive_ca as A

def final(word, slots, v, vmax, T=None, extra=0, shift=False):
    prefix_x = [60 + j * 80 for j in range(max(vmax, v))]
    # inputs larger than the assembler's VMAX need more prefix slots. The
    # program is moved right by a multiple of 14 cells: (0, 14k) lies in the
    # lattice <P_E, P_G>, so no packet changes class relative to E or to each
    # other (and I check this invariance on in-sample inputs with shift=True).
    if v > vmax or shift:
        k = -(-max(0, v - vmax) * 80 // 14) + (1 if shift else 0)
        slots = [(p, t0, x + 14 * k) for p, t0, x in slots]
    T = T or 15 * (slots[-1][2] + 250) + 3000
    T += extra
    items = A.scene(v, slots, prefix_x)
    row, org, placed = vlib.build_right(items, T=T)
    r = vlib.evolve(row, T)
    ids = [n.split("@")[0] for n, x, w, k in vlib.identify(r, org, T=T)]
    return ids

def value(ids):
    rest = [i for i in ids if i != "Bbar"]
    if len(rest) == 1 and (rest[0] == "E" or rest[0].startswith("E^")):
        return 0 if rest[0] == "E" else int(rest[0][2:]) - 1
    return None

if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    vtest = int(sys.argv[2])
    word, slots, vmax = d["word"], [tuple(s) for s in d["slots"]], d["vmax"]
    ok = True
    for v in range(vtest + 1):
        ids = final(word, slots, v, vmax)
        ids2 = final(word, slots, v, vmax, extra=3000)
        got, exp = value(ids), A.model(word, v)
        good = got == exp and ids == ids2
        ok &= good
        print(f"v={v:2d}: CA value {got} (objects {sorted(set(ids))}, stable {ids == ids2}), "
              f"model {exp}  {'OK' if good else 'MISMATCH'}{'  (beyond assembler VMAX)' if v > vmax else ''}", flush=True)
    # invariance check: in-sample inputs with the program moved by 14 cells
    inv = all(value(final(word, slots, v, vmax, shift=True)) == A.model(word, v)
              for v in range(vmax + 1))
    print("program moved by (0,14): all in-sample inputs still match:", inv)
    ok &= inv
    # negative control: the slot of the LAST Z, moved to the next phase
    # pick the last slot where some in-sample input meets a class-sensitive
    # zero event (Z or J at value 0)
    i = max(k for k, s in enumerate(slots)
            if s[0] in "ZJ" and any(A.model(word[:k], v) == 0 for v in range(vmax + 1)))
    bad = list(slots)
    p, t0, x = bad[i]
    bad[i] = (p, t0 + 1, x)
    changed = 0
    for v in range(vmax + 1):
        got = value(final(word, bad, v, vmax))
        changed += got != A.model(word, v)
    print(f"control (slot {i} {p} t0 {t0}->{t0+1}): {changed}/{vmax+1} inputs now differ from the model")
    print("M2 VALIDATION", "PASS" if ok and changed > 0 else "FAIL")
