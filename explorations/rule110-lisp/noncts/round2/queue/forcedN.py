"""Forced-N leader X (K with E2 -> E9) in a periodic program [sim].

Program {A0, A1}; the leader of every A1 copy is X. Claim: X consumes one
tape symbol and always rejects, i.e. the machine is the CTS {A0, ''}
(empty A1). Read outcomes are observed per appendant region
(splice.read_outcomes_row, decoder-free). Control: the same program with
plain K must follow the CTS {A0, A1}.
    python forcedN.py TAPE NREADS"""
import sys
from splice import *
import encoder as enc
import cts

def leaderX():
    m = Machine("YYNN", ["YNNNNN"], 4000, left_periods=1, right_periods=2)
    _, placed = enc.assemble("YYNN", ["YNNNNN"], 1, 2)
    K0 = [p for p in placed if p.block.name == "K"][0]
    Kpos = K0.gspan(0)[0]
    new = replace_exact(m.row, m.origin + Kpos + 41, m.origin + Kpos + 72,
                        [(en_tiles(9), 14, 9)], 0, 0)
    blocks, _ = enc.load_blocks()
    return make_block("X", blocks["K"], K0, new, m.origin)

def run(tape, apps, nread, useX):
    seq = enc._right_block_seq(apps)
    # seq = <app0 body> K <app1 body> K : the first K leads app1
    i = seq.index("K")
    period = seq[:i] + ("X" if useX else "K") + seq[i + 1:]
    reps = nread // 2 + 3
    v = enc._left_v(apps)
    T = (nread + 3) * 2 * 30 * v
    m = Machine(tape, None, T, right_names=period * reps,
                left_names=(enc.OSSIFIER + "A" * v) * (T // (30 * v) + 3))
    lead = [(a, b) for n, a, b in m.blocks if n in "GKX"]
    # components only: from the end of one leader block to the start of the next
    regions = [(b1, a2) for (a1, b1), (a2, b2) in zip(lead, lead[1:])][:nread]
    got, times = read_outcomes_row(m.row, m.origin, regions, T,
                                   per_symbol=[len(apps[j % 2]) for j in range(nread)])
    return got, times

if __name__ == "__main__":
    tape, nread = sys.argv[1], int(sys.argv[2])
    apps = ["YNNNNN", "NNNNNN"]
    leaderX()
    for useX, ref_apps in ((True, ["YNNNNN", ""]), (False, apps)):
        got, times = run(tape, apps, nread, useX)
        ref = ""
        for i, (_, t, _) in enumerate(cts.run(tape, ref_apps, nread)):
            if t and i < nread:
                ref += t[0] if ref_apps[i % 2] else "N"
        print(f"X={useX}: observed {got} reference {ref[:nread]} "
              f"{'MATCH' if got == ref[:nread] else 'DIFFER'} times {times}", flush=True)
