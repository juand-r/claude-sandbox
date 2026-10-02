"""nearend.py - row 7 (near-end lane, abort by CLASS SHIFT) as an executable
model with class arithmetic, compiled from Minsky machines through
verify's guarded-block machine (round2/verify/gbm.py, read-only).

Abstract lane physics (all classes in one cyclic group Z_n):
- k markers X_0..X_{k-1} in the lane, downstream of a CONTROL POINT where
  flags live; the program stream arrives from upstream and meets the
  control point first, then X_0, X_1, ...  Register i is stored in marker
  X_i's position: pos_i = base_i + u * r_i + d_m * (crossings X_i has had).
- A packet's class at a marker = (packet offset - marker position) mod n.
  At a marker a packet either KICKS it (class == KICK: the packet is
  absorbed and the marker moves by +-u: INC/DEC of that register), or
  CROSSES it (class in CROSS: the packet's offset changes by d_p and the
  MARKER is displaced by d_m), or makes DEBRIS (any other class: failure).
- Zero test: a DEC kick on a register at 0 creates a FLAG at the control
  point instead (the zero answer is born stationary at the control point).
- A packet crossing a flag has its offset shifted by f and displaces the
  flag by d_f.  The GATE packet ending each block is absorbed by a flag
  (removing it) if its class at the flag is GATE_ABS; with no flag it
  crosses all markers and leaves.
- Abort by class shift: while a flag exists, every later packet of the
  block arrives at the markers shifted by f; the design requires that the
  shifted classes are crossing classes everywhere (spec F3), so the rest
  of the block does nothing to the registers.
Compiler: each slot's launch offset is computed ONCE at compile time from
the positions predicted for the no-abort branch (a fixed stream, the same
for every input).  This is correct for every input exactly when
  (C1) u = 0 mod n                (register values do not change classes),
  (C2) d_m = 0 mod n              (crossings do not change marker classes:
                                   the F6 crossing balance, in its
                                   strongest, padding-free form),
  (C3) d_f * (number of packets crossing the flag before the gate) is the
       same for every abort point of a block (here: d_f = 0 mod n),
  (C4) f maps every kick class and every packet's downstream class into
       CROSS (the shifted packets cross everything).
Differential test vs the GBM interpreter and vs scholar's Minsky
interpreter; controls violate C1, C2, C4 one at a time and must fail.
Run: python3 nearend.py   (exit 0 = as predicted)
"""
import os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../round2/verify'))
sys.path.insert(0, os.path.join(HERE, '../../scholar'))
from gbm import compile_minsky as gbm_compile, run_gbm, halted, X, Y, P, F, G
from csm import run_minsky, random_minsky

K = 5                       # registers x, y, P, F, G -> markers X_0..X_4


class Phys:
    def __init__(self, n=56, u=56, d_m=0, d_p=3, f=5, d_f=0, kick=0, gate_abs=0):
        self.n, self.u, self.d_m, self.d_p, self.f, self.d_f = n, u, d_m, d_p, f, d_f
        self.kick, self.gate_abs = kick, gate_abs
        # crossing classes: everything except the kick class (generous physics;
        # the point of the model is the bookkeeping, not the class tables)
        self.cross = set(range(n)) - {kick}
        self.base = [11 * i + 1 for i in range(K)]     # marker base positions mod n


def compile_stream(blocks, ph):
    """Fixed stream: list of blocks; each block a list of slots
    (kind, reg, launch_offset); the last slot of every block is the gate.
    Offsets are computed from the NO-ABORT prediction of marker positions
    (mod n), assuming registers never matter (C1) - the compiler does not
    know the input."""
    n = ph.n
    pos = list(ph.base)                       # predicted marker positions mod n
    flagpos = 0
    stream = []
    for blk in blocks:
        slots = []
        for op, r in blk:
            # the packet crosses markers 0..r-1, then kicks marker r
            # choose launch offset o so that class at r == kick
            o = (ph.kick + pos[r] - ph.d_p * r) % n
            slots.append((op, r, o))
            for j in range(r):
                pos[j] = (pos[j] + ph.d_m) % n        # predicted crossing displacement
            pos[r] = (pos[r] + (ph.u if op == 'INC' else -ph.u)) % n
        # gate: no flag in the prediction -> it crosses all markers
        o_gate = (ph.gate_abs + flagpos) % n          # class at a flag would be gate_abs
        slots.append(('GATE', None, o_gate))
        for j in range(K):
            pos[j] = (pos[j] + ph.d_m) % n
        stream.append(slots)
    return stream


def run_lane(stream, regs, ph, cycles):
    """Exact class-level execution.  Returns (regs, ok)."""
    n = ph.n
    regs = list(regs)
    pos = [(ph.base[i] + ph.u * regs[i]) % n for i in range(K)]
    for _ in range(cycles):
        for slots in stream:
            flag = None                                # flag position (mod n) or None
            for op, r, o in slots:
                off = o
                if flag is not None:
                    cls_f = (off - flag) % n
                    if op == 'GATE':
                        if cls_f != ph.gate_abs:
                            return regs, False         # gate fails to remove the flag
                        flag = None
                        continue
                    off = (off + ph.f) % n             # class shift by the flag
                    flag = (flag + ph.d_f) % n
                for j in range(K):
                    c = (off - pos[j]) % n
                    if op != 'GATE' and j == r and c == ph.kick:
                        if op == 'INC':
                            regs[r] += 1
                            pos[r] = (pos[r] + ph.u) % n
                        elif regs[r] == 0:
                            flag = 0                   # zero answer: a flag at the control point
                        else:
                            regs[r] -= 1
                            pos[r] = (pos[r] - ph.u) % n
                        break                          # packet absorbed
                    if c in ph.cross:
                        off = (off + ph.d_p) % n
                        pos[j] = (pos[j] + ph.d_m) % n
                        continue
                    return regs, False                 # debris
                # a packet that crossed everything leaves the lane
    return regs, True


def differential(ph, n_random=150, seed=4, budget=400):
    rng = random.Random(seed)
    tests = [([('DEC', 0, 1, 2), ('INC', 1, 0), ('HALT',)], [3, 2]),
             ([('DEC', 1, 1, 3), ('INC', 0, 2), ('INC', 0, 0), ('HALT',)], [0, 3])]
    for _ in range(n_random):
        tests.append((random_minsky(rng.randrange(2, 7), rng=rng), [rng.randrange(4), rng.randrange(4)]))
    compared = fails = 0
    for prog, regs in tests:
        mreg, ms, mh = run_minsky(prog, regs, budget)
        if not mh:
            continue
        compared += 1
        blocks = gbm_compile(prog)
        stream = compile_stream(blocks, ph)
        start = [regs[0], regs[1], 1, 0, 0]          # GBM convention: P = 1 = first state
        out, ok = run_lane(stream, start, ph, ms + 3)
        ref = run_gbm(blocks, start, ms + 3)
        ok = ok and out == ref and out[:2] == mreg and halted(prog, out)
        fails += not ok
    return compared, fails


def main():
    good = Phys()
    c, f0 = differential(good)
    print(f'conditions C1-C4 hold (u = d_m = d_f = 0 mod n, f != 0): {c} halting Minsky runs, {f0} failures (must be 0)')
    res = {}
    for name, ph in (('C1 violated: u = 3', Phys(u=3)),
                     ('C2 violated: crossings displace markers by d_m = 7 (order 8 in Z_56)', Phys(d_m=7)),
                     ('C2 violated: d_m = 14 (order 4)', Phys(d_m=14)),
                     ('C3 violated: crossings displace the flag by d_f = 3', Phys(d_f=3)),
                     ('C4 violated: f = 0 (no class shift: aborted kicks still kick)', Phys(f=0))):
        cc, ff = differential(ph)
        res[name] = ff
        print(f'control {name}: {ff}/{cc} failures (must be > 0)')
    ok = f0 == 0 and c > 0 and all(v > 0 for v in res.values())
    print('as predicted:', ok)
    return 0 if ok else 1




def feasible(n, cross, kick=0, k=K, dps=None):
    """Is there a class-shift abort design with markers whose crossing
    classes are `cross` (a subset of Z_n, kick class `kick` not in it)?
    Unknowns: marker bases b_0..b_{k-1}, packet crossing displacement d_p,
    flag shift f != 0, gate class.  Constraints (spec F2-F4):
      packet aimed at r, at upstream j < r: c = kick + b_r - b_j - d_p (r - j)
         must be in cross, and c + f in cross (after a zero, it is shifted);
      at its target: kick + f in cross;
      downstream j > r when shifted: c + f in cross, c as above;
      gate (no flag): some gate offset g with g + d_p j - b_j in cross for all j.
    Returns a witness (bases, d_p, f) or None.  Exhaustive."""
    import itertools
    cross = set(cross)
    for d_p in (dps if dps is not None else range(n)):
        for f in range(1, n):
            if (kick + f) % n not in cross:
                continue
            # bases up to a global translation: b_0 = 0
            for rest in itertools.product(range(n), repeat=k - 1):
                b = (0,) + rest
                ok = True
                for r in range(k):
                    for j in range(k):
                        if j == r:
                            continue
                        c = (kick + b[r] - b[j] - d_p * (r - j)) % n
                        if j < r and c not in cross:
                            ok = False; break
                        if (c + f) % n not in cross:
                            ok = False; break
                    if not ok:
                        break
                if not ok:
                    continue
                if any(all(((g + d_p * j - b[j]) % n) in cross for j in range(k)) for g in range(n)):
                    return b, d_p, f
    return None


def feasibility_report():
    print('Lemma N1 check (single crossing class, Z_4, as Ebar x C2):', feasible(4, {1}, kick=0, k=3))
    print('two crossing classes in Z_4 (as Ebar x C1), kick in a third:', feasible(4, {1, 3}, kick=0, k=3),
          '/', feasible(4, {1, 2}, kick=0, k=3))
    rng = random.Random(1)
    hits = 0
    trials = 20
    for _ in range(trials):
        cr = set(rng.sample(range(1, 12), 7))
        if feasible(12, cr, kick=0, k=3) is not None:
            hits += 1
    print(f'Z_12 with 7 random crossing classes (as Ebar pair x F, 7 of 12), 3 markers: {hits}/{trials} feasible')


if __name__ == '__main__':
    if sys.argv[1:] == ['feasibility']:
        feasibility_report()
    else:
        sys.exit(main())
