"""Net back effect Delta_c = d_c - a_c per class from w4 results (a_c =
number of A gliders emitted; trailing B's eat them). Flags records whose
three Delta's (per rod size) are pairwise distinct."""
import sys, json, re


def count_A(name):
    if name == "A":
        return 1
    m = re.match(r"A\^(\d+)$", name)
    if m:
        return int(m.group(1))
    parts = name.split("_")
    if all(p == "A" or re.match(r"A\^\d+$", p) or p.isdigit() for p in parts) and "A" in name:
        return sum(count_A(p) for p in parts if not p.isdigit())
    return None


def rod_n(name):
    if name == "E":
        return 1
    m = re.match(r"E\^(\d+)$", name)
    if m:
        return int(m.group(1))
    m = re.match(r"v-4/15s(\d+)w(\d+)$", name)
    if m:     # standard rods E^n, n >= 10: width floor((10n-1)/3), slip 9+6(n-1)
        sl, w = int(m.group(1)), int(m.group(2))
        c = [n for n in range(2, 200) if (10 * n - 1) // 3 == w and (9 + 6 * (n - 1)) % 14 == sl]
        return c[0] if len(c) == 1 else None
    return None


def deltas(rec, N):
    """Delta per class from the simulated products (rod size change minus
    number of A's); None if not clean or not a standard rod."""
    out = []
    for k in range(3):
        ok, prods = rec["sims"][f"{N}:{k}"]
        if not ok or not isinstance(prods, list):
            return None
        rods = [p for p in prods if p.startswith("E") or p.startswith("v-4/15")]
        rest = [p for p in prods if p not in rods]
        if len(rods) != 1:
            return None
        if any(count_A(p) is None for p in rest):
            return None
        a = sum(count_A(p) for p in rest)
        n2 = rod_n(rods[0])
        if n2 is None:
            return None
        out.append(n2 - N - a)
    return out


if __name__ == "__main__":
    for fn in sys.argv[1:]:
        for l in open(fn):
            r = json.loads(l)
            if "sims" not in r:
                continue
            ds = [deltas(r, int(key.split(":")[0])) for key in ("%s:0" % n for n in sorted({int(k.split(':')[0]) for k in r['sims']}))]
            flag = any(dd is not None and len(set(dd)) == 3 for dd in ds)
            print("DISTINCT" if flag else "-", r["px"], r["phiR"], r["d"], ds, r["X"])
