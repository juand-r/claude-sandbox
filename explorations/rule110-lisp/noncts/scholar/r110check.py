"""Independent collision checker (scholar's verification tool).

Deliberately separate from collider/ and synth/ code so that their claims can
be re-checked by a second implementation.

Building rows. Martinez et al. publish ether-compatible strings for every
glider phase (data/listPhasesR110.txt, verified by verify_phases.py). In
their notation a configuration is written  X-ne-Y  : the string of glider
phase X, then n copies of the ether tile, then glider phase Y. build()
accepts exactly that notation, e.g.  "A(f1_1)-4e-E-(A,f1_1)".

Typing. Every defect cluster at a late time is typed by its minimal
spacetime period (p, d) (local invariance) and its width (ether phase slip
across it, mod 14; Cook 2004 s.3.1). Families are identified from the
(p, d, width) of the verified phase strings.

Run as a script for a self-test on the 18 "soliton" collisions claimed in
Martinez-Adamatzky-Chen-Chua (arXiv:1301.6258, s.3.1).
"""

import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from engine import ETHER, parse, step  # noqa: E402
from census import clusters, ether_phase  # noqa: E402

DATA = Path(__file__).parent / "data" / "listPhasesR110.txt"
TILE = 14
PAD = 160           # ether tiles on each side of a built configuration
MAX_P = 100         # longest glider period we try to detect (H is 92)


def load_phases():
    pat = re.compile(r"^\[([01]+)\]\s*=\s*(\S+?\([^)]*\))")
    out = {}
    for line in DATA.read_text().splitlines():
        m = pat.match(line)
        if m:
            out[m.group(2)] = m.group(1)
    return out


PHASES = load_phases()


TOKEN = re.compile(r"(?P<eth>\d*e)(?=-|$)|(?P<gl>[A-Za-z]+\d*[-^]?\([^)]*\))")


def tokens(spec):
    """Strict tokenizer for Martinez notation X-ne-Y: every character of the
    spec must be consumed (tokens separated by '-'), else ValueError."""
    out, i = [], 0
    while i < len(spec):
        m = TOKEN.match(spec, i)
        if not m:
            raise ValueError(f"cannot parse {spec!r} at {i}: {spec[i:]!r}")
        out.append(("e", int(m.group("eth")[:-1] or 1)) if m.group("eth")
                   else ("g", m.group("gl")))
        i = m.end()
        if i < len(spec):
            if spec[i] != "-":
                raise ValueError(f"expected '-' in {spec!r} at {i}")
            i += 1
    return out


def build(spec, pad=PAD):
    """Martinez notation -> row (uint8), plus the index where spec starts."""
    parts = []
    for kind, val in tokens(spec):
        if kind == "e":
            parts.append(ETHER * val)
        else:
            if val not in PHASES:
                raise KeyError(f"unknown glider phase {val!r}")
            parts.append(PHASES[val])
    body = "".join(parts)
    return parse(ETHER * pad + body + ETHER * pad), TILE * pad


def evolve(row, n):
    h = np.empty((n + 1, len(row)), dtype=np.uint8)
    h[0] = row
    for t in range(n):
        h[t + 1] = step(h[t])
    return h


def local_period(h, t, a, b, margin=6):
    """Minimal (p, d) with h[t][a-m:b+m] == h[t-p][a-m-d:b+m-d]."""
    lo, hi = a - margin, b + margin
    ref = h[t, lo:hi]
    for p in range(1, MAX_P + 1):
        for d in range(-p, p + 1):
            lo2, hi2 = lo - d, hi - d
            if lo2 < 0 or hi2 > h.shape[1]:
                continue
            if np.array_equal(h[t - p, lo2:hi2], ref):
                return p, d
    return None


def width(row, a, b):
    """Ether phase slip across the defect [a, b): right phase - left phase."""
    ph = ether_phase(row)
    left = [ph[x] for x in range(max(0, a - 40), a - TILE + 1) if ph[x] >= 0]
    right = [ph[x] for x in range(b, min(len(ph), b + 40)) if ph[x] >= 0]
    if not left or not right:
        return None
    return (right[0] - left[-1]) % TILE


def _family_table():
    """(p, d, width) -> family name, from the verified phase strings."""
    table = {}
    for name, bits in PHASES.items():
        fam = name.split("(")[0]
        if fam in ("e", "Gun") or not name.endswith("f1_1)"):
            continue
        row = parse(ETHER * 30 + bits + ETHER * 30)
        h = evolve(row, 2 * MAX_P + 10)
        cl = [c for c in clusters(h[-1]) if 100 < c[0] < len(row) - 100]
        if len(cl) == 0:
            continue
        a, b = cl[0][0], cl[-1][1]
        pd = local_period(h, len(h) - 1, a, b)
        w = width(h[-1], a, b)
        if pd is not None:
            table.setdefault((pd[0], pd[1], w), set()).add(fam)
    return table


_FAMILIES = None


def family(p, d, w):
    global _FAMILIES
    if _FAMILIES is None:
        _FAMILIES = _family_table()
    names = _FAMILIES.get((p, d, w))
    if names:
        return "/".join(sorted(names))
    # trains of k identical gliders (A^k, B^k, ...): widths add (mod 14)
    for (p2, d2, w2), fams in _FAMILIES.items():
        if (p2, d2) == (p, d) and w is not None:
            for k in range(2, 8):
                if (k * w2) % TILE == w:
                    return "/".join(f + "^" + str(k) for f in sorted(fams))
    return f"?({p},{d},w{w})"


def objects(h, t, lo=0, hi=None, merge=20):
    """Typed objects at time t: list of (start, end, name). Defect clusters
    closer than `merge` cells are merged (one object)."""
    hi = h.shape[1] if hi is None else hi
    cl = [c for c in clusters(h[t]) if c[0] >= lo and c[1] <= hi]
    groups = []
    for a, b in cl:
        if groups and a - groups[-1][1] < merge:
            groups[-1][1] = b
        else:
            groups.append([a, b])
    out = []
    for a, b in groups:
        pd = local_period(h, t, a, b)
        w = width(h[t], a, b)
        name = family(pd[0], pd[1], w) if pd else "?"
        out.append((a, b, name))
    return out


def outcome(spec, T=600, pad=PAD):
    """Run a configuration and return the typed objects at times T-150 and T
    (both, so a caller can check the result has settled)."""
    row, s0 = build(spec, pad)
    h = evolve(row, T)
    margin = T + 20        # wrap-seam light cone (speed <= 1 cell/step)
    lo, hi = margin, len(row) - margin
    if lo >= hi:
        raise ValueError("pad too small for T")
    names = lambda t: [o[2] for o in objects(h, t, lo, hi)]
    return names(T - 150), names(T), h


def inputs(spec):
    """Family names of the glider phases in a spec, typed by simulation of
    each phase alone (so the typing is the same as for outputs)."""
    out = []
    for tok in [v for k, v in tokens(spec) if k == "g"]:
        row = parse(ETHER * 30 + PHASES[tok] + ETHER * 30)
        h = evolve(row, 2 * MAX_P + 10)
        obj = objects(h, len(h) - 1, 100, len(row) - 100)
        out += [o[2] for o in obj]
    return out


SOLITONS = [  # arXiv:1301.6258 s.3.1, (a)-(r): claimed X + Y -> {Y, X}
    "A(f1_1)-6e-G(C,f1_1)", "C1(A,f1_1)-3e-E-(B,f1_1)",
    "C1(A,f1_1)-3e-E-(C,f1_1)", "F(A,f1_1)-3e-B(f4_1)",
    "C2(A,f1_1)-3e-E-(C,f1_1)", "C1(A,f1_1)-2e-F(B,f1_1)",
    "C2(A,f1_1)-2e-F(A,f1_1)", "A(f1_1)-4e-E-(A,f1_1)",
    "A(f1_1)-4e-E-(B,f1_1)", "A(f1_1)-4e-E-(C,f1_1)",
    "A(f1_1)-4e-E-(H,f1_1)", "F(A,f1_1)-e-E-(A,f1_1)",
    "F(A,f1_1)-e-E-(C,f1_1)", "F(A,f1_1)-e-E-(D,f1_1)",
    "F(A,f1_1)-e-E-(E,f1_1)", "F(G,f1_1)-e-E-(A,f1_1)",
    "F(G,f1_1)-e-E-(B,f1_1)", "F(G,f1_1)-e-E-(H,f1_1)",
]


def main():
    bad = 0
    for spec in SOLITONS:
        early, late, _ = outcome(spec, T=900)
        before = inputs(spec)
        ok = sorted(late) == sorted(before) and early == late
        bad += not ok
        print(f"{spec:32s} in:{before}  out:{late}  "
              f"{'soliton' if ok else 'NOT a clean crossing'}")
    print(f"{len(SOLITONS)} claimed solitons, {bad} fail")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
