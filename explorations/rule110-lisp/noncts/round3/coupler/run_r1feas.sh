#!/bin/sh
# R1-face feasibility table: X (3,2) width 30 + E^4 -> Y | E^(4-K), all classes.
cd "$(dirname "$0")"
for PY in 12,-6 4,-2; do
 for K in 2 1 -1 -2; do
  for SX in 8 2 10 4 12 0 6; do
   python3 sat_shuttle.py --only r1 --wx 30 --wy 30 --ns1 4 --T1 260 --py $PY --sx $SX --K $K
  done
 done
done
echo ALLDONE
