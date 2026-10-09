"""Evaluate a Lisp expression on Rule 110.

    python lisp110.py "(car (quote (a b)))"            # compile, run the CTS
    python lisp110.py --gliders "(car (quote (a b)))"  # run it on gliders
    python lisp110.py --depth 3 "(define (last l) ...) (last (quote (a b c)))"

The expression is compiled (lisp_bus.py) to a bus program, hence to a
cyclic tag system: a tape (the quoted data) and an appendant table (the
program). Without --gliders the CTS itself is run and the value decoded
from its final queue. With --gliders the CTS is laid out with Cook's
glider blocks and Rule 110 is simulated by the event engine; every read
is checked against the CTS and the value is decoded from the glider
reads alone (experiments.lisp_gliders).

Supported: quote car cdr cons atom? eq? cond t, lambda, define. Calls of
defined functions are inlined up to --depth (default 4) at compile time;
a deeper recursion is reported as an error, not a wrong value.
"""

import argparse
import time

from lisp import run as lisp_run
from lisp_bus import LispBus

EVENTS_PER_READ_BIT = 45     # REPORT section 7: crossings of the queue
JUNK_EVENTS = 8              # ... and of the junk left of the queue, x reads^2


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("src")
    ap.add_argument("--depth", type=int, default=4)
    ap.add_argument("--gliders", action="store_true")
    ap.add_argument("--v", type=int, default=None, help="ossifier spacing")
    ap.add_argument("--no-rope", action="store_true",
                    help="simulate the debris left of the queue event by event")
    ap.add_argument("--full-check", action="store_true",
                    help="read every read with the full census (default: the light "
                         "check, with the full census on every 64th read)")
    a = ap.parse_args()

    t0 = time.time()
    lb = LispBus(a.src, a.depth)
    comp = lb.compile_bus()
    B = comp.pm.B
    reads = comp.p * B
    queue = [len(l) * B for l in comp.live[:-1]]
    sum_q = sum(q * q for q in queue)
    print(f"compiled in {time.time() - t0:.1f}s: {lb.n} registers, "
          f"{comp.passes} passes, symbol width {B} bits")
    print(f"CTS: {len(comp.pm.appendants())} appendants, tape "
          f"{len(comp.initial_tape(lb.values)) * B} bits, {reads} reads, "
          f"queue <= {max(queue)} bits")
    est = EVENTS_PER_READ_BIT * sum_q + JUNK_EVENTS * reads ** 2
    print(f"estimated glider cost: ~{est:.1g} events "
          f"(~{est / 2.3e6 / 60:.0f} min at 2.3e6 events/s)")
    if a.gliders:
        from experiments import lisp_gliders
        lisp_gliders(a.src, a.v, depth=a.depth, rope=not a.no_rope,
                     check="full" if a.full_check else "light")
        return
    value = lb.decode(comp.run(lb.values))
    print(f"value (CTS): {value}")
    print(f"lisp.py:     {lisp_run(a.src)}")


if __name__ == "__main__":
    main()
