"""T1 full: a FIXED left stream over {I (I_L), D (A), Z (Z_L)} built greedily
with the exact CA in the loop on inputs V_TRAIN (input = E + v B's from the
right), then validated on other inputs.  Model: I: v+1; D: v-1 (only used
at v >= 1); Z: v-1 if v > 0, else v = 0 and one A answer leaves right.
Usage: python3 t1_build.py WORD VMIN VMAX         (build; writes t1z_<WORD>.json)
       python3 t1_build.py WORD VLO VHI check     (validate + control)"""
import sys, json, time
import t1lib as L

SP = 90
GAP = 120 + 50 * 18


def model(w, v):
    a = 0
    for c in w:
        if c == "I":
            v += 1
        elif c == "D":
            v -= 1
        elif v > 0:
            v -= 1
        else:
            a += 1
    return v, a


def Tfor(n):
    return int((GAP + SP * n) * 15 / 14) + 50 * 40 + 1500


def ok_for(slots, word, vs):
    T = Tfor(len(slots))
    for v in vs:
        objs, placed = L.outcome(slots, v, T)
        if L.counter_and_answers(objs) != model(word, v):
            return False
    return True


def build(word, vs):
    slots = []
    for j, op in enumerate(word):
        x = -GAP - SP * j
        found = None
        for t0 in range(3):
            for dx in range(14):
                trial = slots + [(op, t0, x - dx)]
                if ok_for(trial, word[:j + 1], vs):
                    _, placed = L.outcome(trial, vs[0], 10)
                    found = (op, t0, placed[0][2])
                    break
            if found:
                break
        if not found:
            raise SystemExit(f"slot {j} ({op}): nothing works for {vs}")
        slots.append(found)
    return slots


def check(word, slots, vs):
    T = Tfor(len(slots))
    progs, bad = set(), 0
    for v in vs:
        objs, placed = L.outcome(slots, v, T)
        row, org, _ = L.build(slots, v, T)
        ex = [p for p in placed if p[0] == "E"][0][2]
        progs.add((org, row[:ex - 60 - org].tobytes()))
        got, want = L.counter_and_answers(objs), model(word, v)
        bad += got != want
        print(f"v={v:2d}: model {want}  CA {got}")
    k = len(slots) // 2
    ctl = list(slots)
    op, t0, x = ctl[k]
    ctl[k] = (op, (t0 + 1) % 3, x)
    cbad = sum(L.counter_and_answers(L.outcome(ctl, v, T)[0]) != model(word, v) for v in vs)
    print(f"identical program cells: {len(progs) == 1}; mismatches {bad}; "
          f"control (slot {k} to another class) mismatches {cbad} (must be > 0)")
    return bad == 0 and len(progs) == 1 and cbad > 0


if __name__ == "__main__":
    word, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    fn = f"t1z_{word}.json"
    if len(sys.argv) > 4 and sys.argv[4] == "check":
        slots = [tuple(s) for s in json.load(open(fn))["slots"]]
        print("OK" if check(word, slots, range(a, b + 1)) else "FAILED")
    else:
        t = time.time()
        slots = build(word, list(range(a, b + 1)))
        json.dump({"word": word, "slots": slots, "train": [a, b]}, open(fn, "w"))
        print(f"built {len(slots)} slots in {time.time() - t:.0f}s")
