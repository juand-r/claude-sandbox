"""Classify leader-variant scan rows by read outcomes.
Region counts at T=60000: read0 region ~26 (Y) / ~3 (N); read1 region
~24-25 accepted / ~0-2 rejected. A tape gives a 2-letter outcome, '?' if
the counts fit neither (garbage)."""
import json, sys
def letter0(c): return "Y" if 22 <= c <= 28 else "N" if c <= 4 else "?"
def letter1(c): return "Y" if 20 <= c <= 28 else "N" if c <= 3 else "?"
REF = {"YYNN": "YY", "YNYN": "YN", "NYYN": "NY", "NNYY": "NN"}
for path in sys.argv[1:]:
    for line in open(path):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        out = {t: letter0(v[0][0]) + letter1(v[0][1]) for t, v in d["r"].items()}
        clean = all("?" not in o for o in out.values())
        kind = ("BASE" if out == REF else
                "FORCED-N" if all(o[1] == "N" for o in out.values()) else
                "STATE-DEP" if clean else "garbage")
        if kind != "garbage":
            print(path, d["k"], d["off"], kind, out, {t: v[2] for t, v in d["r"].items()})
