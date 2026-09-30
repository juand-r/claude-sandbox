"""Independent check of 'spec F' (synth/collider): an E-E packet moving at
-4/15 that turns an F into a lone stationary C3 (nothing else).
Search: packets E(A,f1_1)-g e-E(x) from Martinez strings (g = 0, 1), kept
only if the pair is a stable (15,-4) object; then F(A,f1_1)-n e-packet for
n = 8..13, looking for outcome exactly ['C3']."""
import r110check as r

def stable_pair(spec):
    e, l, h = r.outcome(spec, T=400, pad=80)
    return l == e and all(n.startswith("E") and not n.startswith("E-") for n in l) and len(l) >= 1

hits = []
Es = [k for k in r.PHASES if k.startswith("E(")]
for y in Es:
    for g in (0, 1):
        pk = f"E(A,f1_1)-{g}e-{y}"
        try:
            if not stable_pair(pk):
                continue
        except Exception as ex:
            continue
        for n in range(8, 14):
            spec = f"F(A,f1_1)-{n}e-{pk}"
            e, l, _ = r.outcome(spec, T=1600, pad=240)
            if l == ["C3"] and e == l:
                hits.append(spec)
                print("HIT", spec, flush=True)
print("hits:", len(hits))
