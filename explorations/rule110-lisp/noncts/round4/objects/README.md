# round4/objects: storage objects that might escape Theorems 1-2

Agent "objects" (round 4), avenues (b) right-to-left crossings and (d) other
counter objects. Running log: NOTES.md. Plan: PLAN.md.

## Tools (all exact Rule 110; every SAT witness re-simulated)
| file | what |
|---|---|
| cone.py | exact influence cone of a periodic background (SAT): leftmost/rightmost cell at time T that changes on the other half-line can reach; block argument gives speed bounds |
| look.py, wall_id.py | view a cone witness; identify the domains on each side of a wall |
| wallsat.py | SAT for periodic walls between two phases of a background (g=0: gliders in it) |
| plant.py | plant a wall from wallsat into an E^N rod and type the outcome |
| objlib.py | scene builder (collider conventions), E^n for any n by splicing, typer (round3 verify v3, read-only) + long-rod recognition |
| scan_back.py | every library left-mover vs the back of a long rod: does anything reach the front? |
| launch2.py | SAT: can a free train launch a phase domain deep into the rod from the back? |
| backgrounds.py | enumerate spatially periodic Rule 110 backgrounds |
| s1_pass.py | theory's S1: a head that passes a stationary cell and re-emerges identical |

## Reproduce
    python3 cone.py 11111000100110 14,28,56      # ether control
    python3 cone.py 1101011100 15,30,60,90       # E-bg cone
    python3 wallsat.py 1101011100 30 40 walls_ebg.jsonl
    python3 plant.py 45 100 1000 -0.6
    python3 scan_back.py 24 1200 back_N24.jsonl all
