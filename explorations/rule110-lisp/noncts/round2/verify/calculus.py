"""A class-level calculus for E^n program streams, measured by me
(calib.py -> calib.json), plus a planning assembler and a differential test
against the exact CA.

State of the counter: (m, t) = (value, seed phase mod 3 in my convention).
A packet P placed with seed phase p acts by the measured table
  tab[P, m, t, p] -> (m', t') or invalid.
For m > 7 the table is extended by class-free translation (checked: for
every packet type the m = 2..7 rows are p-independent translations).

plan(word, V): depth-first search over p in {0,1,2} per slot so that every
input v in V gives valid events and the model value at every slot.
check(word, phases, V): run the exact CA with adaptive_ca's geometry and
compare (value, class) with the calculus at the end."""
import json, sys, random, os
import adaptive_ca as A

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = json.load(open(os.path.join(HERE, "calib.json")))
MMAX = 7
SPACING = 200     # >= 160 needed: at 110 a 2-part packet and the next one overlap at the counter (3-body)

def step(P, m, t, p):
    if m > MMAX:
        r = TAB[f"{P},{MMAX},{t},0"]
        return (m + (r[0] - MMAX), r[1])
    r = TAB[f"{P},{m},{t},{p}"]
    return None if r is None else tuple(r)

def run_word(word, phases, v, prefix_phase=0):
    s = (0, 0)                      # E at (0,0): value 0, seed phase 0
    for _ in range(v):
        s = step("I", s[0], s[1], prefix_phase)
        if s is None:
            return None
    for P, p in zip(word, phases):
        s = step(P, s[0], s[1], p)
        if s is None:
            return None
    return s

def plan(word, V, prefix_phase=0):
    """DFS; returns phases or None."""
    starts = []
    for v in V:
        s = (0, 0)
        for _ in range(v):
            s = step("I", s[0], s[1], prefix_phase)
        starts.append(s)
    best = [None]
    seen = set()

    def dfs(i, states, phases):
        if i == len(word):
            best[0] = list(phases); return True
        key = (i, tuple(states))
        if key in seen:
            return False
        seen.add(key)
        P = word[i]
        for p in range(3):
            nxt = []
            ok = True
            for v, st in zip(V, states):
                ns = step(P, st[0], st[1], p)
                if ns is None or ns[0] != A.model(word[:i + 1], v):
                    ok = False; break
                nxt.append(ns)
            if ok and dfs(i + 1, nxt, phases + [p]):
                return True
        return False

    sys.setrecursionlimit(10000)
    dfs(0, starts, [])
    return best[0]

def ca_state(word, phases, v, vmax, spacing=110, prefix_sp=80):
    prefix_x = [60 + j * prefix_sp for j in range(max(vmax, v))]
    x0 = (prefix_x[vmax - 1] if vmax else 60) + spacing
    slots = [(P, p, x0 + i * spacing) for i, (P, p) in enumerate(zip(word, phases))]
    if v > vmax:
        k = -(-(v - vmax) * prefix_sp // 14)
        slots = [(P, p, x + 14 * k) for P, p, x in slots]
    T = 15 * (slots[-1][2] + 250) + 3000
    got, ids, cls = A.outcome(A.scene(v, slots, prefix_x), T)
    if got is None:
        return None, ids
    # A.outcome returns phase mod 3 at time T; convert to seed phase
    return (got, (T - _phase(word, phases, v, vmax, slots, prefix_x, T)) % 3), ids

def _phase(word, phases, v, vmax, slots, prefix_x, T):
    import vlib
    row, org, placed = vlib.build_right(A.scene(v, slots, prefix_x), T=T)
    r = vlib.evolve(row, T)
    for n, x, w, k in vlib.identify(r, org, T=T):
        nm = n.split("@")[0]
        if nm == "E" or nm.startswith("E^"):
            return int(n.split("@")[1])
    return 0

if __name__ == "__main__":
    # differential test: random words and random phases, abstract vs CA
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    agree = disagree = conservative = 0
    for _ in range(n):
        L = rng.randint(3, 10)
        word = "".join(rng.choice("IZJNXWD") for _ in range(L))
        phases = [rng.randrange(3) for _ in range(L)]
        vmax = 4
        for v in range(vmax + 1):
            pred = run_word(word, phases, v)
            got, ids = ca_state(word, phases, v, vmax, spacing=SPACING)
            # calculus says invalid -> CA must not give a clean counter, or
            # we only count it as "both invalid" if CA is not clean either
            if pred is None:
                conservative += 1          # calculus declines; CA may still be clean
                continue
            same = got == tuple(pred)
            agree += same; disagree += not same
            if not same:
                print("DISAGREE", word, phases, v, "calculus", pred, "CA", got, ids, flush=True)
    print(f"calculus valid: {agree} agree with CA, {disagree} disagree; calculus declined {conservative}")


def plan_with_correctors(word, V, max_per_gap=2, corrector="N", prefix_phase=0):
    """Like plan, but before each program packet the planner may insert up
    to max_per_gap corrector packets (default N = GB4, a NOP whose zero
    event is a value-robust reflection of the class). Returns the full
    packet list [(P, p), ...] or None."""
    starts = []
    for v in V:
        s = (0, 0)
        for _ in range(v):
            s = step("I", s[0], s[1], prefix_phase)
        starts.append(s)
    seen = set()
    out = [None]
    sys.setrecursionlimit(20000)

    def dfs(i, states, k, acc):
        if i == len(word):
            out[0] = list(acc); return True
        key = (i, tuple(states), k)
        if key in seen:
            return False
        seen.add(key)
        P = word[i]
        for p in range(3):                       # place the program packet
            nxt, ok = [], True
            for v, st in zip(V, states):
                ns = step(P, st[0], st[1], p)
                if ns is None or ns[0] != A.model(word[:i + 1], v):
                    ok = False; break
                nxt.append(ns)
            if ok and dfs(i + 1, nxt, 0, acc + [(P, p)]):
                return True
        if k < max_per_gap:                      # or insert a corrector
            for p in range(3):
                nxt, ok = [], True
                for v, st in zip(V, states):
                    ns = step(corrector, st[0], st[1], p)
                    if ns is None or ns[0] != st[0]:
                        ok = False; break
                    nxt.append(ns)
                if ok and dfs(i, nxt, k + 1, acc + [(corrector, p)]):
                    return True
        return False

    dfs(0, starts, 0, [])
    return out[0]
