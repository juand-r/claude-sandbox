#!/bin/sh
# Can ANY B-family train (period (4,-2), width <= 30) reflect at a back
# face? R2-back-only SAT: E^4 + Y -> E^(4+K) | X (X any A-family train).
cd "$(dirname "$0")"
for K in 1 2 3 -1 0; do
  for SX in 8 2 10 4 12 0 6; do
    python3 sat_shuttle.py --only r2 --py 4,-2 --wy 30 --wx 24 --ns2 4 --T2 260 --sx $SX --K $K
  done
done
echo ALLDONE
