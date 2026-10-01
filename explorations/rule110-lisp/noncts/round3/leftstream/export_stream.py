"""Export exact rows of a left-stream program for inputs VS (one stream
text, t0 fixed from max(VS)), re-run each exported row from its cells and
compare with the model. Output: stream_<PROG>.json.
Usage: python export_stream.py PROG VS [i:j control]"""
import json
import sys
from lsl import export, run_exported
from lstream import place_program, counter, model, outcome, T0, GAP

if __name__ == "__main__":
    prog = sys.argv[1]
    vs = [int(a) for a in sys.argv[2].split(",")]
    pert = tuple(map(int, sys.argv[3].split(":"))) if len(sys.argv) > 3 else None
    t0 = max(T0, 200 + 180 * max(vs))
    stream = sorted(place_program(prog, GAP, t0, pert), key=lambda s: s[2])
    out = []
    bad = 0
    for v in vs:
        T = t0 + GAP * len(prog) + 800
        exp = model(prog, v)
        sc = export(stream + counter(v), T, expect={"value": exp[0], "answers_right": exp[1]},
                    note=f"program {prog}, input v = {v} (counter E^{v+1} = E + {v} B's), control {pert}")
        ok, prods = run_exported(sc)
        got = outcome(prods)
        good = ok and got[2] == [] and (got[0], got[1]) == exp
        bad += not good
        sc["result"] = [p[0] for p in prods]
        out.append(sc)
        print(v, got, exp, "OK" if good else "MISMATCH")
    name = f"stream_{prog}{'_ctl%d_%d' % pert if pert else ''}.json"
    json.dump(out, open(name, "w"))
    print(name, "mismatches", bad)
