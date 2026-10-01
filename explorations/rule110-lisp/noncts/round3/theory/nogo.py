"""nogo.py - executable checks of the two-counter no-go theorems (THEORY.md s.3).

Abstract two-stream machine ("2SM"), synchronous version:
  * counters x (driven by stream 1) and y (driven by stream 2), values >= 0;
  * a program phase t = step mod L (both streams periodic with period L);
  * a MODE per side, m1 (for x) and m2 (for y): the op that stream i applies
    at phase t is prog_i[t][m_i] (a filter / class selecting the packet's
    effect), so modes set the drift while both counters are large;
  * autonomous mode maps auto_i[t][m] (data-independent mode changes);
  * ops: +1, +2, 0, -1. A -1 on a zero counter is a ZERO EVENT: the counter
    is left at w (w = 0 saturating, w = 6 a non-monotone wrap like gate's
    Z6), the own mode is reset by a table, and a KICK of any sign is sent
    to the other counter with a delay of 1..D steps (a signal in flight;
    on arrival it is clamped at 0);
  * coupling classes:
      "value"  : zero events change only the other counter's VALUE (T1);
      "oneway" : x's zero may also set y's mode, not vice versa (T2);
      "cross"  : both directions may set the other's mode (control: the
                 theorems do not cover it and it can be non-periodic);
      "shuttle": modes are blind (never change), but a SHARED gap state q
                 adds a drift to both counters while it runs, and zero events
                 of either counter switch q (control; THEORY.md s.4).

Theorem T1/T2 (THEORY.md): in classes "value" and "oneway" every orbit is
eventually periodic (the per-period record of modes, in-flight signals and
zero events). The check below runs random machines of each class and
reports how many are NOT periodic within the horizon. For "value" and
"oneway" this must be 0 (a nonzero count would refute the theorem or
reveal a transient longer than the horizon). For "cross" and "shuttle"
the hand-built doubling machines must be detected as non-periodic, which
shows that the checker can fail.

Random programs rarely compute anything, so the random part is weak
evidence (round-2 verify made the same point); the proofs carry the claim.

Run: python nogo.py      (exit 1 on any failure)
"""
import random
import sys

OPS = (+1, +2, 0, -1)


def eventual_period(seq, min_reps=3, max_pre_frac=0.25):
    """Smallest (preperiod, period) with seq periodic from preperiod on, at
    least min_reps full periods observed, and preperiod <= max_pre_frac * len.
    The last condition matters: a machine whose zero events get rarer and
    rarer (doubling gaps) ends in a long quiet stretch that looks periodic.
    (Mistake caught by the controls on the first run, NOTES.md.)"""
    n = len(seq)
    for p in range(1, n // min_reps + 1):
        i = n - p - 1
        while i >= 0 and seq[i] == seq[i + p]:
            i -= 1
        pre = i + 1
        if n - pre >= min_reps * p and pre <= max_pre_frac * n:
            return pre, p
    return None


class Machine:
    """One 2SM instance. Tables are plain lists/dicts so a machine can be
    printed and rerun."""

    def __init__(self, L, M1, M2, prog1, prog2, auto1, auto2, zero1, zero2,
                 kind, shuttle=None):
        self.L, self.M1, self.M2 = L, M1, M2
        self.prog1, self.prog2 = prog1, prog2      # [t][m] -> op
        self.auto1, self.auto2 = auto1, auto2      # [t][m] -> m'
        # zero tables: (t, m_own, q) -> dict(own=m', kick=k, delay=d,
        #                                     cross=m_other' or None, q=q')
        self.zero1, self.zero2 = zero1, zero2
        self.kind = kind
        # shuttle: dict q -> (dx, dy) applied every step while q runs
        self.shuttle = shuttle or {0: (0, 0)}

    def run(self, x, y, periods, cap=None, q0=0):
        """Simulate `periods` program periods. Returns the list of per-period
        records (modes, q, pending signals, zero events in the period).
        cap: stop early (return None) if a value exceeds cap."""
        m1 = m2 = 0
        q = q0
        pending = []                      # [arrival_step, target, kick]
        records = []
        step = 0
        for _ in range(periods):
            events = []
            start = (m1, m2, q, tuple(sorted((a - step, tg, k) for a, tg, k in pending)))
            for t in range(self.L):
                m1 = self.auto1[t][m1]
                m2 = self.auto2[t][m2]
                dxs, dys = self.shuttle[q]
                # shuttle (shared gap process): a source that is empty ends it
                if dxs < 0 and x + dxs < 0 or dys < 0 and y + dys < 0:
                    which = 1 if (dxs < 0 and x + dxs < 0) else 2
                    events.append((t, "s%d" % which))
                    tab = self.zero1 if which == 1 else self.zero2
                    e = tab[(t, m1 if which == 1 else m2, q)]
                    q = e["q"]
                else:
                    x += dxs
                    y += dys
                for side in (1, 2):
                    m = m1 if side == 1 else m2
                    op = (self.prog1 if side == 1 else self.prog2)[t][m]
                    val = x if side == 1 else y
                    if op == -1 and val == 0:
                        tab = self.zero1 if side == 1 else self.zero2
                        e = tab[(t, m, q)]
                        events.append((t, side))
                        val = e["wrap"]
                        if side == 1:
                            m1 = e["own"]
                            if e["cross"] is not None:
                                m2 = e["cross"]
                        else:
                            m2 = e["own"]
                            if e["cross"] is not None:
                                m1 = e["cross"]
                        q = e["q"]
                        if e["kick"]:
                            pending.append([step + e["delay"], 3 - side, e["kick"]])
                    else:
                        val += op
                    if side == 1:
                        x = val
                    else:
                        y = val
                arrived = [p for p in pending if p[0] <= step]
                pending = [p for p in pending if p[0] > step]
                for _, tg, k in arrived:
                    if tg == 1:
                        x = max(0, x + k)
                    else:
                        y = max(0, y + k)
                step += 1
            records.append((start, tuple(events)))
            if cap is not None and max(x, y) > cap:
                return None
        return records


def random_machine(rng, kind, L=None, M=None, D=3):
    L = L or rng.randint(2, 6)
    M1 = M or rng.randint(1, 3)
    M2 = M or rng.randint(1, 3)
    Q = 1
    shuttle = None
    if kind == "shuttle":
        M1 = M2 = 1                       # blind streams: no modes at all
        Q = 3
        shuttle = {0: (0, 0)}
        for qq in (1, 2):
            shuttle[qq] = (rng.choice((-1, 1, 2)), rng.choice((-1, 1, 2)))
    prog1 = [[rng.choice(OPS) for _ in range(M1)] for _ in range(L)]
    prog2 = [[rng.choice(OPS) for _ in range(M2)] for _ in range(L)]
    # autonomous mode maps: mostly identity, sometimes a fixed change
    auto1 = [[m if rng.random() < 0.8 else rng.randrange(M1) for m in range(M1)]
             for _ in range(L)]
    auto2 = [[m if rng.random() < 0.8 else rng.randrange(M2) for m in range(M2)]
             for _ in range(L)]

    def ztab(Mown, Mother, cross_ok):
        tab = {}
        for t in range(L):
            for m in range(Mown):
                for qq in range(Q):
                    tab[(t, m, qq)] = dict(
                        own=rng.randrange(Mown),
                        kick=rng.choice((0, 0, 1, 2, -1, 6, -2)),
                        delay=rng.randint(1, D),
                        cross=(rng.randrange(Mother) if cross_ok and rng.random() < 0.7
                               else None),
                        wrap=rng.choice((0, 0, 0, 6)),
                        q=(rng.randrange(Q) if kind == "shuttle" else 0))
        return tab

    zero1 = ztab(M1, M2, kind in ("oneway", "cross"))
    zero2 = ztab(M2, M1, kind == "cross")
    return Machine(L, M1, M2, prog1, prog2, auto1, auto2, zero1, zero2, kind, shuttle)


def doubling_cross():
    """Hand-built CROSS-mode machine that doubles a value for ever.
    Mode A (m1 = m2 = 0): x -= 1 and y += 2 per period (a transfer x -> y).
    x's zero sets BOTH modes to B (own and cross).
    Mode B (m1 = m2 = 1): y -= 1 and x += 1 per period (transfer y -> x).
    y's zero sets both modes back to A. Values double each round, so the gaps
    between zero events double: not eventually periodic."""
    L = 2
    # phase 0: the draining side tests/decrements; phase 1: the other side adds
    prog1 = [[-1, 0], [0, +1]]          # [t][m1]
    prog2 = [[0, -1], [+2, 0]]          # [t][m2]
    ident = [[0, 1], [0, 1]]
    zero1, zero2 = {}, {}
    for t in range(L):
        for m in range(2):
            zero1[(t, m, 0)] = dict(own=1, kick=0, delay=1, cross=1, wrap=0, q=0)
            zero2[(t, m, 0)] = dict(own=0, kick=0, delay=1, cross=0, wrap=0, q=0)
    return Machine(L, 2, 2, prog1, prog2, ident, [row[:] for row in ident],
                   zero1, zero2, "cross")


def doubling_shuttle():
    """Hand-built SHUTTLE machine with BLIND streams (no modes): stream 1 adds
    nothing, stream 2 adds +1 every period. The shared gap state q is a
    shuttle: q = 1 moves x -> y (x -1, y +1 per step), q = 2 moves y -> x.
    The shuttle reverses when its source is empty. During x -> y, y also gets
    the stream's +1: ratio 1.5; during y -> x the stream's +1 slows the drain:
    ratio 2. Net growth x3 per round: not eventually periodic."""
    L = 2
    prog1 = [[0], [0]]
    prog2 = [[0], [+1]]
    ident = [[0], [0]]
    shuttle = {0: (0, 0), 1: (-1, +1), 2: (+1, -1)}
    zero1, zero2 = {}, {}
    for t in range(L):
        for qq in range(3):
            zero1[(t, 0, qq)] = dict(own=0, kick=0, delay=1, cross=None, wrap=0, q=2)
            zero2[(t, 0, qq)] = dict(own=0, kick=0, delay=1, cross=None, wrap=0, q=1)
    m = Machine(L, 1, 1, prog1, prog2, ident, [r[:] for r in ident], zero1, zero2,
                "shuttle", shuttle)
    return m


def check_class(kind, n, seed, periods=3000):
    rng = random.Random(seed)
    nonper = 0
    examples = []
    for _ in range(n):
        mach = random_machine(rng, kind)
        x0, y0 = rng.randrange(12), rng.randrange(12)
        rec = mach.run(x0, y0, periods, cap=10 ** 7)
        if rec is None:                   # exploded: growth is fine, rerun shorter
            continue
        if eventual_period(rec) is None:
            nonper += 1
            if len(examples) < 2:
                examples.append((x0, y0))
    return nonper, examples


def main():
    rc = 0
    # 1. the theorem classes: must be eventually periodic
    for kind, n in (("value", 3000), ("oneway", 3000)):
        bad, ex = check_class(kind, n, seed=11)
        print(f"class {kind:7s}: {n} random machines, {bad} not eventually "
              f"periodic within 3000 periods (must be 0)")
        rc |= bad > 0
    # 2. controls: hand-built machines outside the theorem must be flagged
    for name, mach in (("cross doubling", doubling_cross()),
                       ("shuttle x3 (blind streams)", doubling_shuttle())):
        q0 = 1 if mach.kind == "shuttle" else 0
        rec = mach.run(1, 0, 4000, cap=10 ** 12, q0=q0)
        if rec is None:                   # values exploded: use the prefix
            rec = mach.run(1, 0, 300, q0=q0)
        per = eventual_period(rec)
        ev = [i for i, r in enumerate(rec) if r[1]]
        print(f"control {name}: eventually periodic = {per is not None}; "
              f"first zero-event periods {ev[:10]}")
        rc |= per is not None
    # 3. random machines outside the theorem: some should be non-periodic
    for kind in ("cross", "shuttle"):
        bad, ex = check_class(kind, 3000, seed=12)
        print(f"class {kind:7s} (not covered): {bad}/3000 random machines "
              f"not eventually periodic within the horizon")
    return rc


if __name__ == "__main__":
    sys.exit(main())
