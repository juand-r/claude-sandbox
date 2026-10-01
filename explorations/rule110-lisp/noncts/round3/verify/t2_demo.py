"""T2 integrated demonstration: both coupling directions in ONE exact run,
fixed programs on both sides, several inputs.
Program (time order):
  left:  I I          (y = 2)
  right: [input: v1 GB5's] J I   (x = 0 ? y += 2 : x += 2)
  left:  Z Z Z        (each: y > 0 ? y -= 1 : x -= 1)
Model: v1 = 0 -> (x, y) = (0, 1);  v1 > 0 -> (v1 + 1, 0)
(the x = 0 branch uses R1 -> R2, the x > 0 branch uses R2 -> R1).
The left program's slots are placed greedily (3 x 14 per slot) with the
exact CA in the loop on training inputs; the R1 phase class t1 is scanned.
Usage: python3 t2_demo.py VTRAIN_MAX VCHECK_MAX"""
import sys, json
import t1lib as L
import v3, vlib, engine
sys.path.insert(0, v3.R2V)
import adaptive_ca as AC
L.register_IL()

D = 600
LEFT = "IIZZZ"
XS = [-1020, -1110, -23000, -23100, -23200]   # Z's arrive after the Bbar (~t = 22600)


def model(word, v1):
    x, y = v1, 0
    for i, c in enumerate(word):
        if i == 2:                      # the right block happens here
            if x == 0:
                y += 2
            else:
                x += 2
        if c == "I":
            y += 1
        elif c == "Z":
            if y > 0:
                y -= 1
            else:
                x -= 1
    return x, y


def scene(slots, v1, t1, block=True):
    prog = [(L.OPS[o], t, x) for o, t, x in slots][::-1]
    right = [("E", 0, 0), ("E", t1, D)]
    for j in range(v1):
        right += AC.parts("I", t1, D + 150 + 110 * j)
    xj = D + 447 + 14 * 63      # keep the J-R1 relation of t2_class (multiple of 14)
    if block:
        right += AC.parts("J", 5 + t1, xj) + AC.parts("I", 5 + t1, xj + 110)
    items = prog + right
    c0 = (L.C_E - sum(vlib.LIB[n].w for n, _, _ in prog)) % 14
    return items, c0


def outcome(slots, v1, t1, T=40000, block=True):
    items, c0 = scene(slots, v1, t1, block)
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    objs = [v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T)]
    val = lambda b: 0 if b == "E" else (int(b[2:]) - 1 if b.startswith("E^") else None)
    if len(objs) == 2 and None not in (val(objs[0]), val(objs[1])):
        return (val(objs[1]), val(objs[0])), objs, row, placed
    return None, objs, row, placed


def build(vs, t1):
    slots = []
    for j, op in enumerate(LEFT):
        found = None
        for t0 in range(3):
            for dx in range(14):
                trial = slots + [(op, t0, XS[j] - dx)]
                blk = j >= 2
                want = (lambda v: model(LEFT[:j + 1], v)) if blk else (lambda v: (v, j + 1))
                if all(outcome(trial, v, t1, block=blk)[0] == want(v) for v in vs):
                    found = (op, t0, outcome(trial, vs[0], t1)[3][0][2])
                    break
            if found:
                break
        if not found:
            return None, j
        slots.append(found)
    return slots, None


if __name__ == "__main__":
    vt, vc = int(sys.argv[1]), int(sys.argv[2])
    for t1 in range(3):
        slots, fail = build(list(range(vt + 1)), t1)
        if slots is None:
            print(f"t1={t1}: greedy fails at left slot {fail}")
            continue
        print(f"t1={t1}: left slots {slots}")
        progs, bad = set(), 0
        for v in range(vc + 1):
            got, objs, row, placed = outcome(slots, v, t1)
            ex = [p for p in placed if p[0] == "E"][0][2]
            progs.add(row[:ex - 60 - (placed[0][2] - 400)].tobytes()[:0])
            bad += got != model(LEFT, v)
            print(f"   v1={v}: model (x,y)={model(LEFT, v)}  CA {got}  {objs}")
        print(f"   mismatches {bad}")
        json.dump({"t1": t1, "slots": slots}, open("t2_demo.json", "w"))
        break
