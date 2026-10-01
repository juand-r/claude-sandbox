"""T1 (partial, no zero test): a FIXED left stream of INC (IL) and DEC (A)
packets operating an E counter, built greedily slot by slot with the exact
CA in the loop over inputs V_TRAIN, then validated out of sample.
Input v is written as E + v B's from the right (absorbed first).
Usage: python3 t1_nonzero.py WORD VMIN VMAX [SPACING]"""
import sys, json, time
import t1lib as L

SP = 90
GAP = 120 + 50 * 18     # room for inputs up to v = 12 written by B's


def model(w, v):
    for c in w:
        v += 1 if c == "I" else -1
    return v


def Tfor(nslots):
    return int((GAP + SP * nslots) * 15 / 14) + 50 * 40 + 900


if __name__ == "__main__":
    word = sys.argv[1]
    vmin, vmax = int(sys.argv[2]), int(sys.argv[3])
    slots = []
    t0clock = time.time()
    for j, op in enumerate(word):
        x = -GAP - SP * j
        found = None
        for t0 in range(3):
            for dx in range(0, 14, 1):
                trial = slots + [(op, t0, x - dx)]
                T = Tfor(j + 1)
                ok = True
                for v in range(vmin, vmax + 1):
                    objs, placed = L.outcome(trial, v, T)
                    if L.value(objs) != model(word[:j + 1], v):
                        ok = False
                        break
                if ok:
                    found = (op, t0, placed[0][2])   # snapped x of the new (leftmost) item
                    break
            if found:
                break
        if not found:
            print(f"slot {j} ({op}): no placement works for all v in {vmin}..{vmax}")
            sys.exit(1)
        slots.append(found)
        print(f"slot {j} {op}: t0={found[1]} x={found[2]}", flush=True)
    json.dump({"word": word, "slots": slots, "spacing": SP}, open(f"t1_{word}.json", "w"))
    print(f"built in {time.time() - t0clock:.0f}s")
