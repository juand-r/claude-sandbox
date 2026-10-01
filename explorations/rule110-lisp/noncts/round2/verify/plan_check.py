"""Plan a program stream with the class-level calculus (with N correctors)
and validate it in the exact CA for inputs 0..VTEST (including inputs not
used by the planner), with a stability check and a negative control.
Usage: python plan_check.py WORD VPLAN VTEST [SPACING]"""
import sys, json, time
import calculus as C
import adaptive_ca as A
import m2_validate as M

def main(word, vplan, vtest, spacing=200):
    t = time.time()
    plan = C.plan_with_correctors(word, list(range(vplan + 1)))
    if plan is None:
        print("NO PLAN"); return False
    full = "".join(P for P, p in plan)
    print("plan:", full, "phases:", "".join(str(p) for P, p in plan), f"({time.time()-t:.1f}s)", flush=True)
    prefix_x = [60 + j * 80 for j in range(vplan)]
    x0 = prefix_x[-1] + spacing
    slots = [(P, p, x0 + i * spacing) for i, (P, p) in enumerate(plan)]
    json.dump({"word": full, "program": word, "vmax": vplan, "spacing": spacing,
               "slots": slots, "ok": True}, open(f"plan_{word}.json", "w"))
    ok = True
    for v in range(vtest + 1):
        ids = M.final(full, slots, v, vplan)
        ids2 = M.final(full, slots, v, vplan, extra=3000)
        got, exp = M.value(ids), A.model(word, v)
        calc = C.run_word(full, [p for P, p in plan], v)
        good = got == exp and ids == ids2
        ok &= good
        print(f"v={v:2d}: CA {got} model {exp} calculus {calc[0] if calc else None} "
              f"{'OK' if good else 'MISMATCH'}{' (not planned)' if v > vplan else ''}", flush=True)
    # control: flip the phase of the first slot where some planned input
    # meets a forced zero event (Z or J at value 0)
    for i, (P, p) in enumerate(plan):
        if P in "ZJ" and any(A.model(full[:i], v) == 0 for v in range(vplan + 1)):
            break
    bad = list(slots); bad[i] = (slots[i][0], (slots[i][1] + 1) % 3, slots[i][2])
    changed = sum(M.value(M.final(full, bad, v, vplan)) != A.model(word, v) for v in range(vplan + 1))
    print(f"control (slot {i} {plan[i][0]} phase +1): {changed}/{vplan+1} inputs differ")
    print("RESULT", "PASS" if ok and changed else "FAIL", f"{time.time()-t:.0f}s", flush=True)
    return ok

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]),
         int(sys.argv[4]) if len(sys.argv) > 4 else 200)
