#!/bin/sh
# Batch 2: wider X and Y (30/30), Y in the Bbar family, all slips of X.
cd "$(dirname "$0")"
P="python3 sat_shuttle.py --wx 30 --wy 30 --ns1 4 --ns2 4 --T1 240 --T2 280 --py 12,-6"
for K in 2 1 -1; do
  for SX in 8 2 10 4 12 0 6; do
    $P --sx $SX --K $K
  done
done
echo ALLDONE
