# Adaptive Ring System

A finite universe of self-modifying "rings." Each ring is 36 bits and is at
once data, an elementary cellular-automaton rule, and a node in a
transformation network --- there is no controller, fitness, or energy. All
behaviour emerges from rings transforming one another and themselves under
reproduction, mutation, death, and a hard population cap.

The full specification and every design decision (with rationale) is in
[`DESIGN.md`](DESIGN.md). Read that first.

## Files

| file                  | purpose                                            |
|-----------------------|----------------------------------------------------|
| `DESIGN.md`           | specification + resolved ambiguities + rationale   |
| `ring_system.py`      | the simulator (semantics, tick cycle, logging)     |
| `test_ring_system.py` | tests for the load-bearing semantics               |
| `viz.py`              | dashboard viewer (animated GIF + summary figure)   |
| `run.py`              | CLI: run a simulation, log, save history, render    |
| `artifact.html`       | self-contained interactive dashboard (live knobs)  |
| `REPORT.md`           | **synthesis report** of the investigation (read this) |
| `RESEARCH_PLAN.md`    | operational defs + metrics for "self-organization" |
| `analyze.py`          | discriminating metrics (churn vs. organization)    |
| `experiments.py`      | battery of configs + side-by-side metric table     |
| `spatial_probes.py`   | E5/E8 domain-trajectory and invasion probes        |
| `EXPERIMENTS.md`      | experiment log E1--E13 (+ reflections), full detail |
| `TRAJECTORY.md`       | the tree of explored paths (map of the program)    |
| `REFERENCES.md`       | related literature + why each is relevant          |
| `NOTES.md`            | running log of observations                         |

The simulator has experimental knobs --- `mut_scale`, `protect`,
`transform_off`, `spawn_code`/`death_code` (heritable reproduction trigger),
`base_death` (turnover), `local_addr`/`local_range` (spatial addressing),
`self_template` (emergent heredity), `overwrite_birth`, `cyclic_dominance` ---
**all defaulting to the faithful spec**. The full list and which experiment
introduced each is in `DESIGN.md` section 10; `artifact.html` exposes the main
ones as live toggles.

**Read `REPORT.md` for the findings.** Headline: the faithful system is pure
churn; local addressing + heredity (imposed or, via self-templating, emergent)
produces emergent spatial domains; emergent heredity then unlocks robust
adaptation and sustained open-ended novelty --- but not complexity growth.

> **Note on the grid:** by default the universe has no geometry --- addresses
> are absolute slot indices and the 16x16 grid is cosmetic. It becomes real 2-D
> space only under `local_addr` (the "H4" modification). All spatial results use
> that mode. See `DESIGN.md` section 3.7.

## How to run

```bash
pip install numpy matplotlib pillow

python3 test_ring_system.py                 # 12 tests, all should pass

python3 run.py --ticks 400 --init 16 --render
#   -> out/metrics.jsonl   per-tick metrics (one JSON object per line)
#   -> out/history.npz     state history for replay
#   -> out/summary.png     whole-run metric figure
#   -> out/evolution.gif   animated dashboard

# re-render an existing run without re-simulating:
python3 viz.py out/history.npz --gif out/evolution.gif --summary out/summary.png
```

`run.py --init 1` starts from a single ring; `--init N` from N random rings.
`--print-every K` prints a readable metric line every K ticks.

## Reading the dashboard

- **universe grid** --- the 256 slots as a 16x16 grid, coloured by each
  ring's RULE value; dark cells are empty slots. *Adjacency is meaningful only
  under local addressing* (see the grid note above); in the default absolute
  mode this grid is a cosmetic tiling of the slots.
- **genome raster** --- every occupied ring as a row of 36 bits, with the
  RULE / PULL / PUSH / ORDER / SPAWN / DEATH / MUTATION field boundaries
  marked. This is the population's DNA at a glance.
- **traces** --- population and diversity over time; the summary figure adds
  activity (bits changed per tick) and mean mutation level.

## Sample output

A 400-tick run from 16 random rings (`run.py --ticks 400 --init 16`):

![dashboard animation](sample_evolution.gif)

![run summary](sample_summary.png)

## What we observe

The sample run above is the **faithful spec** (absolute addressing, no
modifications). It looks lively --- stable population, high genotype diversity
--- but that liveliness is **high-entropy churn, not organization**: roughly the
whole population is replaced each tick and no structure persists (this is the E1
finding; the apparent diversity is entropy). Genuine self-organization appears
only under the modifications --- see `REPORT.md` for the real results and
`EXPERIMENTS.md` for the full investigation.
