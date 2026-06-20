"""Spatial probes for the H4 regime (local addressing + heritable rule).

Reproduces the E5 analysis in EXPERIMENTS.md:
  * domain_trajectory  -- how the coexisting rule-domains evolve over time
  * invasion_test      -- does a host domain resist an injected foreign patch?

Run: python3 spatial_probes.py
"""

from __future__ import annotations

import numpy as np

import ring_system as rs

SIDE = 16
STABLE = dict(local_addr=True, protect=((0, 8), (8, 16), (16, 24)), mut_scale=0.3)


def _set_rule(u, slot, val):
    for i in range(8):
        u.bits[slot, i] = (val >> (7 - i)) & 1


def _rule_count(u, r):
    return int(np.sum((rs.get_field(u.bits, rs.RULE) == r) & u.occupied))


def components(occ, rule):
    """Connected same-rule components (4-neighbour torus). Returns lists of
    member slots, largest first."""
    lab = -np.ones(rs_nmax := len(occ), dtype=int)
    comps = []
    for s in range(rs_nmax):
        if not occ[s] or lab[s] >= 0:
            continue
        ci = len(comps); lab[s] = ci; stack = [s]; mem = []
        while stack:
            c = stack.pop(); mem.append(c)
            cx, cy = c % SIDE, c // SIDE
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = ((cy + dy) % SIDE) * SIDE + (cx + dx) % SIDE
                if occ[n] and lab[n] < 0 and rule[n] == rule[c]:
                    lab[n] = ci; stack.append(n)
        comps.append(mem)
    comps.sort(key=len, reverse=True)
    return comps


def domain_trajectory(seed=1, warmup=0, total=800, sample=None):
    """Print pop / Moran / #domains / largest-domain over a long run."""
    import analyze
    u = rs.Universe(nmax=256, seed=seed, record_history=True, **STABLE)
    u.seed_random(256); u.run(total)
    b = np.stack(u.history_bits); o = np.stack(u.history_occ)
    sample = sample or [0, 50, 100, 200, 400, 600, total]
    print(f"domain trajectory (seed {seed})")
    print("tick  pop  moran  #domains(>=3)  largest")
    for t in sample:
        rule = rs.get_field(b[t], rs.RULE)
        comps = components(o[t], rule)
        big = [c for c in comps if len(c) >= 3]
        largest = len(comps[0]) if comps else 0
        m = analyze.spatial_moran(b, o, t, SIDE)
        print(f"{t:4d}  {int(o[t].sum()):3d}  {m:5.3f}  {len(big):3d}          {largest:3d}")


def invasion_test(seeds=range(4), warmup=400, follow=150):
    """Mutual invasion between the two largest distinct domains: inject each
    one's rule into half of the other's territory, then watch both.

    If each rule reclaims its home and loses the away patch -> mutual boundary
    resistance (self-maintenance). If one rule wins BOTH territories ->
    competitive dominance / hierarchy (no self-maintenance)."""
    print(f"\nmutual invasion test (two largest domains)")
    for seed in seeds:
        u = rs.Universe(nmax=256, seed=seed, record_history=False, **STABLE)
        u.seed_random(256); u.run(warmup)
        rule = rs.get_field(u.bits, rs.RULE)
        comps = components(u.occupied, rule)
        A = comps[0]; rA = int(rule[A[0]])
        B = next((c for c in comps[1:] if int(rule[c[0]]) != rA), None)
        if B is None:
            print(f"  seed {seed}: no distinct second domain, skipped"); continue
        rB = int(rule[B[0]])
        for s in A[: len(A) // 2]:      # inject rB into half of A's home
            _set_rule(u, s, rB)
        for s in B[: len(B) // 2]:      # inject rA into half of B's home
            _set_rule(u, s, rA)
        a0, b0 = _rule_count(u, rA), _rule_count(u, rB)
        u.run(follow)
        a1, b1 = _rule_count(u, rA), _rule_count(u, rB)
        if a1 > a0 * 0.6 and b1 < b0 * 0.4:
            verdict = f"rule {rA} dominates"
        elif b1 > b0 * 0.6 and a1 < a0 * 0.4:
            verdict = f"rule {rB} dominates"
        elif a1 < a0 * 0.5 and b1 < b0 * 0.5:
            verdict = "both shrink (mutual)"
        else:
            verdict = "mixed"
        print(f"  seed {seed}: rA={rA}({len(A)}) rB={rB}({len(B)})  "
              f"rA {a0}->{a1}, rB {b0}->{b1}  [{verdict}]")


if __name__ == "__main__":
    domain_trajectory(seed=1)
    invasion_test(seeds=range(6))
