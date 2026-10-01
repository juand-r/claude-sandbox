"""Does an A-DEC from the left change the class in which the NEXT A must
arrive?  R1 = E^6 at (0,0).  k A's (k = 0..3) are sent from the left, each
placed (scan 3 x 14) in whatever class DECs the counter as it is then
(greedy, exact CA).  Then report which placements of a probe A at a FIXED
spacetime line family DEC R1 after the k A's: if the DEC placement (t0, x)
of the probe is the same for every k, A-DECs do not change R1's left-end
class; if it rotates with k, a data-dependent number of incoming A's breaks
a fixed program."""
import v3, vlib, engine

T = 3000


def outcome(items):
    c0 = (0 - sum(vlib.LIB[n].w for n, _, _ in items[:-1])) % 14
    row, org, placed = vlib.build(items, c0=c0, T=T)
    r = engine.unpack(engine.step_packed_n(engine.pack(row), T), len(row))
    return [v3.base(n) for n, x, w, k in vlib.identify(r, org, T=T)], placed


R = ("E^6", 0, 0)
sent = []
for k in range(4):
    # probe classes after k A's: the probe is the next A, placed further left
    xs = -200 - 120 * k
    good = []
    for t0 in range(3):
        for dx in range(14):
            o, placed = outcome([("A", t0, xs - dx)] + sent[::-1] + [R])
            if o == [f"E^{5 - k}"]:
                good.append((t0, placed[0][2]))
    good = sorted(set(good))
    # canonical class of the probe line: (t0, x) -> lateral position x - (2/3) t0 mod 14*?
    lines = sorted(set((3 * x - 2 * t0) % 42 for t0, x in good))
    print(f"after {k} A's: probe placements that DEC: {good}; key (3x-2t) mod 42: {lines}")
    sent.append(("A", good[0][0], good[0][1]))
