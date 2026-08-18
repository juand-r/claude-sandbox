# rule110-lisp

A Lisp interpreter that executes on the Rule 110 cellular automaton.

The construction is a tower of verified translations:

    mini-Lisp  ->  machine model  ->  cyclic tag system  ->  Rule 110 gliders

The glider level follows Cook (2004), "Universality in Elementary Cellular
Automata". The machine-to-cyclic-tag step follows the polynomial-overhead
approach of Neary & Woods (2006) rather than the exponential Cocke-Minsky
2-tag route, so that computations are physically runnable as far down the
tower as compute allows.

## Layout

- `PLAN.md`    - live work plan with milestones, checked off as completed
- `NOTES.md`   - findings, hypotheses, dead ends (created as work proceeds)
- `engine.py`  - Layer 0: fast Rule 110 simulator + ether tooling
- `tests/`     - pytest suite; every layer is differentially tested

## Running

    pip install numpy pytest pillow
    pytest explorations/rule110-lisp/tests -q
