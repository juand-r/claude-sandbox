"""Rename library objects everywhere (gliders.json, collisions.json).

Evidence for the names (all from the catalog, see NOTES.md):
- Cook's ossifier packet A^4 (the A-velocity object in block B of Cook's
  construction, identified in an assembled row) is v2/3s4w0, not the
  Martinez string (111110)^4.
- B strips one A at a time: v2/3s12w1 -B-> v2/3s4w0 -B-> v2/3s10w0
  -B-> v2/3s2w0 -B-> A -B-> nothing, so these are tight A^5..A^2.
- A^2 + v-2/4s12w1 -> nothing, A^3 + v-2/4s4w6 -> nothing: B^2, B^3.
- Martinez's (111110)^n packets are wider A-packets; renamed Aw<n>.
- Second batch (RENAME2): the extendible E: B + E -> v-4/15s1w6 and each
  further B (single class, one product) adds slip 6 and ~3.5 cells:
  E^2 .. E^9 (scholar's E_n, Cook's extendible E).
Usage: python rename.py [2|3]   (1 = default, 2 = E^n, 3 = GBk = G + k B's)
"""
import json
import sys

RENAME = {"A2": "Aw2", "A3": "Aw3", "A4": "Aw4", "A5": "Aw5", "A6": "Aw6",
          "v2/3s2w0": "A^2", "v2/3s10w0": "A^3", "v2/3s4w0": "A^4",
          "v2/3s12w1": "A^5", "v-2/4s12w1": "B^2", "v-2/4s4w6": "B^3"}


RENAME2 = {"v-4/15s1w6": "E^2", "v-4/15s7w9": "E^3", "v-4/15s13w13": "E^4",
           "v-4/15s5w16": "E^5", "v-4/15s11w19": "E^6", "v-4/15s3w23": "E^7",
           "v-4/15s9w26": "E^8", "v-4/15s1w29": "E^9"}
# batch 3: G carrying k B's (G + B^k -> one object, class-independent;
# each further B attaches, single product, both classes)
RENAME3 = {"v-14/42s10w13": "GB1", "v-14/42s2w17": "GB2", "v-14/42s8w19": "GB3",
           "v-14/42s0w23": "GB4", "v-14/42s6w28": "GB5", "v-14/42s12w33": "GB6",
           "v-14/42s4w34": "GB7", "v-14/42s10w38": "GB8"}
if len(sys.argv) > 1 and sys.argv[1] == "2":
    RENAME = RENAME2
if len(sys.argv) > 1 and sys.argv[1] == "3":
    RENAME = RENAME3


def rn(n):
    return RENAME.get(n, n)


def main():
    lib = json.load(open("gliders.json"))
    names = {g["name"] for g in lib["gliders"]}
    for new in RENAME.values():
        if new in names:
            sys.exit(f"{new} already exists; already renamed?")
    for g in lib["gliders"]:
        g["name"] = rn(g["name"])
        if g.get("parts"):
            g["parts"] = [[rn(p[0])] + list(p[1:]) for p in g["parts"]]
        if g["name"] in RENAME.values():
            g["note"] = "renamed by rename.py (see its docstring)"
    json.dump(lib, open("gliders.json", "w"), indent=0)
    rows = json.load(open("collisions.json"))
    for r in rows:
        r["X"], r["Y"] = rn(r["X"]), rn(r["Y"])
        r["products"] = [[rn(p[0])] + list(p[1:]) for p in r["products"]]
    json.dump(rows, open("collisions.json", "w"), indent=0)


if __name__ == "__main__":
    main()
