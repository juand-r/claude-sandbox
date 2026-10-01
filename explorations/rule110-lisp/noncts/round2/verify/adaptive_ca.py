"""Independent integration: build a FIXED G-speed program stream for an E
counter by choosing, slot by slot, a seed phase t0 for each packet such that
the exact Rule 110 run matches the abstract model for EVERY input value in V
(inputs are written by an I-prefix in fixed slots next to the counter).
Everything is mine: builder (vlib.build_right), translation of gate's packet
shapes (part offsets via xlate.mapping), exact engine, my typer.

Abstract model (gate's packets, values n >= 0):
  I: n+1   N: n   Z: n-1 if n>0 else 6   W: n if n>0 else 7
  X: n+1 if n>0 else 8   J: n+1 if n>0 else 0 (+ a Bbar that leaves left)
Allowed leftovers: Bbar only (escapes left, nothing is there).

Usage: python adaptive_ca.py WORD VMAX [SPACING]   e.g. JJJJJZZZZZZ 4
Writes the chosen placements to adaptive_<WORD>.json."""
import json, sys, time
import vlib, libgen, xlate
libgen.load()

PARTS = {
    "Z": [("GB3", 0, 0), ("GB4", -25, 46)],
    "W": [("GB3", 0, 0), ("GB5", -14, 40)],
    "X": [("GB5", 0, 0), ("GB4", -4, 56)],
    "J": [("GB1", 0, 0), ("GB1", -1, 36)],
    "I": [("GB5", 0, 0)], "N": [("GB4", 0, 0)], "D": [("GB3", 0, 0)],
}

def model(word, v):
    n = v
    for c in word:
        if c == "I": n += 1
        elif c == "N": pass
        elif c == "D": n = max(n - 1, 0)
        elif c == "Z": n = n - 1 if n > 0 else 6
        elif c == "W": n = n if n > 0 else 7
        elif c == "X": n = n + 1 if n > 0 else 8
        elif c == "J": n = n + 1 if n > 0 else 0
    return n

def my_offset(g1, g2, dt, dx):
    T1, X1, _ = xlate.mapping(g1)
    T2, X2, _ = xlate.mapping(g2)
    return dt + T2 - T1, dx + X2 - X1

def parts(p, t0, x):
    """Items of packet p with its first part at my seed (t0, x)."""
    out = []
    g0 = PARTS[p][0][0]
    for g, dt, dx in PARTS[p]:
        mdt, mdx = my_offset(g0, g, dt, dx)
        out.append((g, t0 + mdt, x + mdx))
    return out

def scene(v, slots, prefix_x):
    items = [("E", 0, 0)]
    for j in range(v):
        items += parts("I", 0, prefix_x[j])
    for p, t0, x in slots:
        items += parts(p, t0, x)
    return items

def outcome(items, T):
    """-> (counter value or None, ids, class). class = phase mod 3 of the
    counter at time T: for two counters of the same type observed at the
    same T, phase mod 3 is the class of their offset in the ether lattice
    modulo <P_E, P_G> (t mod 3 is a homomorphism with exactly that kernel,
    since P_E = (15,-4), P_G = (42,-14) and (3,2) = 3 P_E - P_G)."""
    row, org, placed = vlib.build_right(items, T=T)
    r = vlib.evolve(row, T)
    full = [n for n, x, w, k in vlib.identify(r, org, T=T)]
    ids = [n.split("@")[0] for n in full]
    rest = [(i, f) for i, f in zip(ids, full) if i != "Bbar"]
    if len(rest) == 1 and (rest[0][0] == "E" or rest[0][0].startswith("E^")):
        nm, f = rest[0]
        cls = int(f.split("@")[1]) % 3
        return (0 if nm == "E" else int(nm[2:]) - 1), ids, cls
    return None, ids, None

CONSISTENT = False   # strict class consistency per value (too strict: see NOTES)

def run(word, vmax, spacing=110, prefix_sp=80):
    prefix_x = [60 + j * prefix_sp for j in range(vmax)]
    x = prefix_x[-1] + spacing if vmax else 60 + spacing
    slots = []
    log = []
    for i, p in enumerate(word):
        cands = list(range(42))
        chosen = None
        for t0 in cands:
            trial = slots + [(p, t0, x)]
            T = 15 * (x + 250) + 3000
            ok = True
            cls_of_value = {}
            for v in range(vmax + 1):
                try:
                    got, ids, cls = outcome(scene(v, trial, prefix_x), T)
                except ValueError:
                    ok = False; break
                if got != model(word[:i + 1], v):
                    ok = False; break
                # same value must mean same trajectory class for every input
                if CONSISTENT and cls_of_value.setdefault(got, cls) != cls:
                    ok = False; break
            if ok:
                chosen = t0; break
        if chosen is None:
            print(f"slot {i} ({p}): NO phase works for all v <= {vmax}", flush=True)
            return slots, False
        slots.append((p, chosen, x))
        print(f"slot {i} ({p}) at x={x}: t0={chosen}", flush=True)
        x += spacing
    return slots, True

if __name__ == "__main__":
    word = sys.argv[1]; vmax = int(sys.argv[2])
    sp = int(sys.argv[3]) if len(sys.argv) > 3 else 110
    t = time.time()
    slots, ok = run(word, vmax, sp)
    json.dump({"word": word, "vmax": vmax, "spacing": sp, "slots": slots, "ok": ok},
              open(f"adaptive_{word}.json", "w"))
    print("OK" if ok else "FAILED", f"{time.time() - t:.0f}s")
