"""Packets: bound groups of same-velocity gliders, used as single inputs.

A packet is built from base gliders placed at given seed events (all with
the same velocity), checked to be a stable periodic object by standalone
simulation (r110lib.isolate_glider on the union of its defects), and
registered in the library under the name  g1@(t,x)+g2@(t,x)+...  where
the events are relative to the first glider's seed event (0,0). If the
same object (any phase) is already in the library, the existing name is
returned instead (e.g. two adjacent A's = A2).

enumerate_pairs(g, h, max_gap) lists every distinct 2-glider packet g,h
(h to the right of g) with 0 <= gap <= max_gap cells at time 0, up to
translation: h's event relative to g is taken mod P_h and mod P_g.
Unstable placements (the two interact) are reported separately; they are
collisions in their own right.
"""

from fractions import Fraction

from r110lib import TILE, Glider, build_row, isolate_glider, obj_key, objects


def packet_key(lib, parts):
    """Union object key of the parts placed at time 0."""
    sts = [lib.gliders[n].state_at(t0, x0, 0) for n, t0, x0 in parts]
    row, x0 = build_row(sts, pad=40)
    objs = objects(row)
    a, b = objs[0][0], objs[-1][1]
    return obj_key(row, a, b, objs[0][2], objs[-1][3]), x0 + a


def make_packet(lib, parts):
    """Register (or find) the packet. -> (name, event of its seed relative
    to the first part's seed) or raises ValueError if unstable."""
    vel = {lib.gliders[n].velocity for n, _, _ in parts}
    if len(vel) != 1:
        raise ValueError("packet parts must share one velocity")
    key, start = packet_key(lib, parts)
    hit = lib.lookup(key)
    if hit is None:
        g = isolate_glider(*key)      # raises ValueError if not periodic
        if g.velocity not in vel:
            raise ValueError("packet settles to a different velocity")
        k0 = g.phases[0][:3]
        if k0 in lib.index:           # transient into a known object
            raise ValueError(f"packet is not stable: becomes {lib.index[k0]}")
        if key not in {ph[:3] for ph in g.phases}:
            raise ValueError("packet state is a transient")
        g.name = "+".join(f"{n}@({t},{x})" for n, t, x in parts)
        g.parts = [tuple(p) for p in parts]
        g.note = "packet (collider/packets.py)"
        # parts are relative to the first part's seed; the glider's seed
        # (phase 0, time 0) starts at column `start`, so shift the parts
        g.parts = [(n, t, x - start) for n, t, x in parts]
        lib.add(g)
        return g.name
    name, k = hit
    return name


def enumerate_pairs(lib, g, h, max_gap=30):
    """-> (stable packet names, unstable relative events)."""
    G, H = lib.gliders[g], lib.gliders[h]
    if G.velocity != H.velocity:
        raise ValueError("different velocities")
    bg, lg, rg, sg = G.state_at(0, 0, 0)
    endg = sg + len(bg)
    names, unstable, seen = [], [], set()
    for t in range(0, -H.p, -1):
        bh, lh, rh, s_rel = H.state_at(t, 0, 0)
        base = (lh - s_rel - rg) % TILE
        x = endg - s_rel + (base - (endg - s_rel)) % TILE
        while s_rel + x - endg <= max_gap:
            parts = [(g, 0, 0), (h, t, x)]
            try:
                key, _ = packet_key(lib, parts)
            except ValueError:
                x += TILE
                continue
            if key not in seen:
                seen.add(key)
                try:
                    nm = make_packet(lib, parts)
                    if nm not in names:
                        names.append(nm)
                except ValueError as e:
                    unstable.append((parts, str(e)))
            x += TILE
    return names, unstable
